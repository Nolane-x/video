"""Render one complete Vietnamese voice-over project in GitHub Actions.

This lane intentionally accepts KorvaTTS's released Vietnamese presets only.
It downloads an immutable ONNX model snapshot, runs the existing voice-casting
pipeline, invokes the repository's real H2 prep_voice.py timeline builder, and
produces an auditable artifact. It never falls back to a local workstation or
a different provider.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from generate_voiceover import generate, validate_manifest
from providers import korva
from voice_quality import _probe_audio, _technical_findings, audit_report

MODEL_REPOSITORY = "dogenthq/KorvaTTS"
MODEL_LICENSE = "Apache-2.0"
PACKAGE_VERSION = "0.1.3"
EXPECTED_SAMPLE_RATE = 44_100
QUALITY_STEPS = 32
CPU_THREADS = 4
REPO_ROOT = Path(__file__).resolve().parents[2]
H2_PREP_VOICE = (
    REPO_ROOT
    / "integrations"
    / "h2-selfimprove-studio"
    / "skills"
    / "lam-video-selfimprove"
    / "kit"
    / "tools"
    / "prep_voice.py"
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".part")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_actions_project(data: dict[str, Any]) -> list[dict[str, Any]]:
    if str(data.get("language") or "").lower().split("-")[0] != "vi":
        raise ValueError("The GitHub Actions voice project currently accepts Vietnamese (vi) only")
    cast = data.get("cast")
    if not isinstance(cast, dict) or not cast:
        raise ValueError("Actions voice project requires a non-empty top-level cast")
    available = {voice["id"] for voice in korva.list_voices("vi")}
    for speaker_id, item in cast.items():
        if not isinstance(item, dict):
            raise ValueError(f"cast.{speaker_id} must be an object")
        if str(item.get("provider") or "").lower() != "korva":
            raise ValueError(
                f"cast.{speaker_id} selects {item.get('provider')!r}; this Actions lane only runs KorvaTTS"
            )
        if str(item.get("voice") or "") not in available:
            raise ValueError(f"cast.{speaker_id} uses an unknown KorvaTTS preset")
        settings = item.get("settings") or {}
        if not isinstance(settings, dict):
            raise ValueError(f"cast.{speaker_id}.settings must be an object")
        steps = settings.get("total_steps", QUALITY_STEPS)
        threads = settings.get("num_threads", CPU_THREADS)
        if steps != QUALITY_STEPS or threads != CPU_THREADS:
            raise ValueError(
                f"cast.{speaker_id} must use total_steps={QUALITY_STEPS} and num_threads={CPU_THREADS}"
            )
    segments = validate_manifest(data)
    for segment in segments:
        if not segment.get("speaker_id"):
            raise ValueError(f"Segment {segment['id']} must reference a stable speaker_id")
        if segment["provider"] != "korva":
            raise ValueError(f"Segment {segment['id']} is not routed through KorvaTTS")
        if segment["settings"].get("total_steps", QUALITY_STEPS) != QUALITY_STEPS:
            raise ValueError(f"Segment {segment['id']} has a non-standard inference step count")
        if segment["settings"].get("num_threads", CPU_THREADS) != CPU_THREADS:
            raise ValueError(f"Segment {segment['id']} has an unsupported CPU thread count")
    return segments


def _download_model(revision: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{40,64}", revision):
        raise ValueError("model_revision must be an immutable Hugging Face commit SHA")
    existing = os.environ.get("KORVATTS_ASSETS_DIR")
    if existing:
        assets = Path(existing).resolve()
        if not all((assets / "onnx" / name).is_file() for name in (
            "duration_predictor.onnx", "text_encoder.onnx", "vector_estimator.onnx",
            "vocoder.onnx", "tts.json", "unicode_indexer.json",
        )):
            raise FileNotFoundError("KORVATTS_ASSETS_DIR is missing required ONNX files")
        return assets
    from huggingface_hub import snapshot_download

    assets = Path(snapshot_download(
        repo_id=MODEL_REPOSITORY,
        revision=revision,
        allow_patterns=["onnx/*", "voice_styles/*"],
    )).resolve()
    os.environ["KORVATTS_ASSETS_DIR"] = str(assets)
    return assets


def _run_h2_timing(output_dir: Path, voice_txt: Path, audio_dir: Path) -> dict[str, Any]:
    if not H2_PREP_VOICE.is_file():
        raise FileNotFoundError(f"The pinned H2 prep_voice.py tool is missing: {H2_PREP_VOICE}")
    project_dir = output_dir / "h2-project"
    command = [
        sys.executable, str(H2_PREP_VOICE),
        "--project", str(project_dir),
        "--voice-dir", str(audio_dir),
        "--voice-txt", str(voice_txt),
        "--lang", "vi",
        "--lead", "0.5",
        "--gap", "0.3",
        "--speaker-gap", "0.18",
    ]
    completed = subprocess.run(
        command, cwd=REPO_ROOT, check=False, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=600,
    )
    if completed.returncode:
        raise RuntimeError(
            "H2 prep_voice.py failed: "
            + (completed.stderr[-4000:] or completed.stdout[-4000:] or str(completed.returncode))
        )
    timeline = project_dir / "timeline"
    required = ["voice.wav", "blocks.json", "lines.json", "words.json", "transcript.txt"]
    missing = [name for name in required if not (timeline / name).is_file()]
    if missing:
        raise RuntimeError(f"H2 timing stage did not produce required outputs: {missing}")
    return {
        "command": command,
        "stdout": completed.stdout[-4000:],
        "timeline_dir": timeline.relative_to(output_dir).as_posix(),
        "outputs": {
            name: {
                "path": (timeline / name).relative_to(output_dir).as_posix(),
                "bytes": (timeline / name).stat().st_size,
                "sha256": _sha256(timeline / name),
            }
            for name in required
        },
    }


def run_project(
    manifest_path: Path,
    output_dir: Path,
    *,
    model_revision: str,
) -> dict[str, Any]:
    if importlib.metadata.version("korvatts") != PACKAGE_VERSION:
        raise RuntimeError(f"Expected korvatts=={PACKAGE_VERSION}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    segments = validate_actions_project(data)
    assets = _download_model(model_revision)
    os.environ.setdefault("OMP_NUM_THREADS", str(CPU_THREADS))
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    installed_voices = set(korva._engine(CPU_THREADS).list_voices())
    required_voices = {str(item["voice"]) for item in data["cast"].values()}
    if required_voices - installed_voices:
        raise RuntimeError(
            f"Pinned KorvaTTS snapshot is missing cast presets: {sorted(required_voices - installed_voices)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    report = generate(data, output_dir, plan_only=False, stop_on_error=False)
    generation_path = output_dir / "voice-generation-report.json"
    quality_path = output_dir / "voice-quality-report.json"
    generation = json.loads(generation_path.read_text(encoding="utf-8"))

    segment_evidence: list[dict[str, Any]] = []
    for item in generation.get("segments", []):
        row = {
            "id": item.get("id"),
            "speaker_id": item.get("speaker_id"),
            "voice": item.get("voice"),
            "status": item.get("status"),
        }
        relative = item.get("file")
        audio_path = (output_dir / relative).resolve() if relative else None
        if not audio_path or not audio_path.is_file():
            row["qa_status"] = "error"
            row["error"] = "Audio file is missing"
        else:
            try:
                audio_path.relative_to(output_dir.resolve())
                digest = _sha256(audio_path)
                if digest != item.get("sha256"):
                    raise ValueError("SHA-256 mismatch against generation report")
                row["sha256_verified"] = True
                row["bytes"] = audio_path.stat().st_size
                metrics = _probe_audio(audio_path)
                findings = _technical_findings(metrics)
                if metrics["sample_rate_hz"] != EXPECTED_SAMPLE_RATE:
                    findings.append(
                        f"Expected {EXPECTED_SAMPLE_RATE} Hz, got {metrics['sample_rate_hz']} Hz"
                    )
                row["audio"] = metrics
                row["technical_findings"] = findings
                row["qa_status"] = "warning" if findings else "pass"
            except Exception as exc:
                row["qa_status"] = "error"
                row["error"] = f"{type(exc).__name__}: {exc}"
        segment_evidence.append(row)

    generation_path_obj = generation_path.resolve()
    quality = audit_report(generation, generation_path_obj, asr=False, language="vi")
    _write_json(quality_path, quality)

    all_segments_ready = (
        len(generation.get("segments", [])) == len(segments)
        and all(item.get("status") in {"generated", "cache_hit"} for item in generation.get("segments", []))
    )
    segment_errors = sum(row["qa_status"] == "error" for row in segment_evidence)
    segment_warnings = sum(row["qa_status"] == "warning" for row in segment_evidence)

    h2 = None
    h2_error = None
    if all_segments_ready and segment_errors == 0:
        try:
            h2 = _run_h2_timing(
                output_dir,
                output_dir / generation["voice_script"],
                output_dir / "voice",
            )
            master_path = output_dir / h2["timeline_dir"] / "voice.wav"
            h2["master_audio"] = _probe_audio(master_path)
            h2["master_technical_findings"] = _technical_findings(h2["master_audio"])
        except Exception as exc:
            h2_error = f"{type(exc).__name__}: {exc}"

    failed = int(generation.get("failed_segments", 0))
    status = "complete" if (
        all_segments_ready and segment_errors == 0 and h2 is not None and h2_error is None
    ) else "partial"
    result = {
        "schema_version": 1,
        "status": status,
        "project": generation.get("project"),
        "language": "vi",
        "model": {
            "package": "korvatts",
            "package_version": PACKAGE_VERSION,
            "repository": MODEL_REPOSITORY,
            "revision": model_revision,
            "license": MODEL_LICENSE,
            "assets_path": str(assets),
            "device": "CPU / ONNX Runtime",
        },
        "runner": {
            "os": os.getenv("RUNNER_OS", "unknown"),
            "arch": os.getenv("RUNNER_ARCH", "unknown"),
            "run_id": os.getenv("GITHUB_RUN_ID"),
            "run_number": os.getenv("GITHUB_RUN_NUMBER"),
            "commit": os.getenv("GITHUB_SHA"),
        },
        "synthesis": {
            "steps": QUALITY_STEPS,
            "threads": CPU_THREADS,
            "seed_policy": "Per speaker: fixed manifest seed",
        },
        "segment_count": len(segments),
        "generated_segments": int(generation.get("generated_segments", 0)),
        "failed_segments": failed,
        "technical_pass": sum(row["qa_status"] == "pass" for row in segment_evidence),
        "technical_warning": segment_warnings,
        "technical_error": segment_errors,
        "segments": segment_evidence,
        "h2_timing": h2,
        "h2_error": h2_error,
        "human_listening_required": True,
        "naturalness_score": None,
        "elevenlabs_equivalence": None,
        "limitations": [
            "This Actions lane uses KorvaTTS's ten released preset identities; it does not create custom voices or clone speakers.",
            "Audio engineering checks do not score naturalness, emotional performance or speaker similarity.",
            "A human must listen to the WAVs and H2 voice.wav before approving the cast.",
        ],
    }
    _write_json(output_dir / "actions-voice-project-report.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model-revision", required=True)
    args = parser.parse_args()
    try:
        report = run_project(args.manifest, args.output, model_revision=args.model_revision)
    except Exception as exc:
        print(f"Actions voice project failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": report["status"],
        "project": report["project"],
        "segments": report["segment_count"],
        "generated": report["generated_segments"],
        "failed": report["failed_segments"],
        "technical_pass": report["technical_pass"],
        "technical_warning": report["technical_warning"],
        "technical_error": report["technical_error"],
        "h2_timing": report["h2_timing"] is not None,
        "report": str(args.output / "actions-voice-project-report.json"),
    }, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
