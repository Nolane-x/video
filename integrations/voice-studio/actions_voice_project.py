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
import shutil
from pathlib import Path
from typing import Any

from audio_mastering import normalize_voice_file
from caption_delivery import write_subtitles
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


def _subtitle_timestamp(seconds: float, *, webvtt: bool = False) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    separator = "." if webvtt else ","
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{separator}{millis:03d}"


def _write_caption_assets(output_dir: Path, timeline_dir: Path) -> dict[str, Any]:
    """Export sentence-level SRT/VTT from H2's estimated line timestamps."""
    lines = json.loads((timeline_dir / "lines.json").read_text(encoding="utf-8"))
    blocks = json.loads((timeline_dir / "blocks.json").read_text(encoding="utf-8"))
    master_path = timeline_dir / "voice.wav"
    master_duration = float(_probe_audio(master_path)["duration_s"])
    block_ids = {str(item.get("id")) for item in blocks}
    if not lines or not block_ids:
        raise RuntimeError("Cannot export captions without H2 blocks and sentence lines")

    plain: list[tuple[int, int, str]] = []
    labelled: list[tuple[int, int, str]] = []
    previous_end_ms = 0
    for index, item in enumerate(lines, 1):
        block_id = str(item.get("block") or "")
        text = " ".join(str(item.get("text") or "").split())
        if block_id not in block_ids or not text:
            raise RuntimeError(f"Invalid H2 caption line {index}: missing block or text")
        try:
            start_s = float(item["start"])
            end_s = float(item["end"])
        except (KeyError, TypeError, ValueError):
            raise RuntimeError(f"Invalid H2 timestamp on caption line {index}") from None
        if not (0 <= start_s < end_s <= master_duration + 0.05):
            raise RuntimeError(f"Caption line {index} falls outside the master audio")
        start_ms = max(previous_end_ms, round(start_s * 1000))
        end_ms = min(round(master_duration * 1000), round(end_s * 1000))
        if end_ms <= start_ms:
            raise RuntimeError(f"Caption line {index} has no positive display duration")
        plain.append((start_ms, end_ms, text))
        speaker = " ".join(str(item.get("char") or "").split())
        labelled.append((start_ms, end_ms, f"{speaker}: {text}" if speaker else text))
        previous_end_ms = end_ms

    def render_srt(cues: list[tuple[int, int, str]]) -> str:
        rows = []
        for cue_no, (start, end, text) in enumerate(cues, 1):
            rows.append(
                f"{cue_no}\n"
                f"{_subtitle_timestamp(start / 1000)} --> {_subtitle_timestamp(end / 1000)}\n"
                f"{text}\n"
            )
        return "\n".join(rows) + "\n"

    def render_vtt(cues: list[tuple[int, int, str]]) -> str:
        rows = ["WEBVTT", ""]
        for start, end, text in cues:
            rows.extend([
                f"{_subtitle_timestamp(start / 1000, webvtt=True)} --> "
                f"{_subtitle_timestamp(end / 1000, webvtt=True)}",
                text,
                "",
            ])
        return "\n".join(rows)

    files = {
        "captions-sentence.srt": render_srt(plain),
        "captions-sentence.vtt": render_vtt(plain),
        "captions-speaker-labelled.srt": render_srt(labelled),
        "captions-speaker-labelled.vtt": render_vtt(labelled),
    }
    outputs = {}
    for filename, content in files.items():
        destination = output_dir / filename
        destination.write_text(content, encoding="utf-8")
        outputs[filename] = {
            "bytes": destination.stat().st_size,
            "sha256": _sha256(destination),
        }
    word_timed = write_subtitles(timeline_dir, output_dir)
    metadata = {
        "status": "generated",
        "line_count": len(lines),
        "sentence_cue_count": len(lines),
        "word_timed_cue_count": word_timed["cue_count"],
        "speaker_labels": "available in sentence-level speaker-labelled variants",
        "alignment_type": "estimated_word_and_sentence_timestamps",
        "alignment_source": "H2 prep_voice.py proportional word/sentence timing heuristic",
        "not_forced_aligned": True,
        "master_duration_s": round(master_duration, 3),
        "outputs": outputs,
        "word_timed": {
            "cue_count": word_timed["cue_count"],
            "files": word_timed["files"],
            "timing_method": word_timed["timing_method"],
        },
        "note": (
            "captions.srt/vtt/ass are grouped from H2 estimated word timings; "
            "captions-sentence.srt/vtt retain sentence-level cues; speaker-labelled "
            "variants are for review. None are ASR forced-alignment ground truth."
        ),
    }
    _write_json(output_dir / "caption-export-report.json", metadata)
    return metadata


def _write_delivery_readme(output_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Voice-over delivery package",
        "",
        f"- Project: {report.get('project')}",
        f"- Production status: **{report.get('status')}**",
        f"- Dialogue segments: {report.get('generated_segments')}/{report.get('segment_count')}",
        "- Master audio: h2-project/timeline/voice.wav",
        "- H2 timeline: h2-project/timeline/blocks.json, lines.json, words.json",
        f"- Caption file count: {len(report.get('captions', {}).get('outputs', {}))}",
        "",
        "## Handoff",
        "",
        "1. Use the H2 voice.wav file as the assembled voice track.",
        "2. Use voice/V001.wav … voice/V010.wav for per-line edits or replacement.",
        "3. Import captions.srt or captions.vtt for shorter word-timed caption cues.",
        "4. Use captions-sentence.srt/vtt for sentence-level captions.",
        "5. Use speaker-labelled caption variants for review and speaker attribution.",
        "6. Use captions.ass when you need a styled subtitle track.",
        "7. Use H2 blocks.json, lines.json and words.json to drive the edit timeline.",
        "",
        "## Timing limitation",
        "",
        "Caption line timing is estimated by H2's proportional sentence-boundary heuristic. "
        "It has not been forced-aligned by an ASR model and must be reviewed before publication.",
        "",
        "## Audio and rights",
        "",
        "Every segment is loudness-normalized to -20 LUFS with a -2.5 dBTP ceiling, "
        "then checked for codec, sample rate, clipping, silence and SHA-256 integrity.",
        "Technical QA does not certify naturalness, acting, pronunciation accuracy or voice similarity.",
        "This example uses KorvaTTS released preset voices; model and output terms must be checked "
        "before commercial distribution.",
    ]
    (output_dir / "README-DELIVERY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_voice_cast_report(
    output_dir: Path,
    manifest: dict[str, Any],
    generation: dict[str, Any],
    segment_evidence: list[dict[str, Any]],
    quality: dict[str, Any],
) -> dict[str, Any]:
    """Write an auditable speaker-to-voice map and per-character delivery stats."""
    evidence_by_id = {
        str(item.get("id")): item for item in segment_evidence if item.get("id")
    }
    quality_by_id = {
        str(item.get("id")): item
        for item in quality.get("segments", [])
        if item.get("id")
    }
    generated_by_speaker: dict[str, list[dict[str, Any]]] = {}
    for item in generation.get("segments", []):
        speaker_id = str(item.get("speaker_id") or "")
        if speaker_id:
            generated_by_speaker.setdefault(speaker_id, []).append(item)

    speakers = []
    for speaker_id, cast in sorted((manifest.get("cast") or {}).items()):
        segments = generated_by_speaker.get(str(speaker_id), [])
        evidence = [evidence_by_id.get(str(item.get("id")), {}) for item in segments]
        metrics = [
            row.get("audio") or {}
            for row in evidence
            if isinstance(row.get("audio"), dict)
        ]
        fingerprints = {
            str(item.get("voice_identity_fingerprint"))
            for item in segments
            if item.get("voice_identity_fingerprint")
        }
        duration_s = sum(float(row.get("duration_s", 0.0)) for row in metrics)
        rms_values = [
            float(row["rms_dbfs"])
            for row in metrics
            if isinstance(row.get("rms_dbfs"), (int, float))
        ]
        peaks = [
            float(row["peak_dbfs"])
            for row in metrics
            if isinstance(row.get("peak_dbfs"), (int, float))
        ]
        quality_rows = [
            quality_by_id.get(str(item.get("id")), {})
            for item in segments
        ]
        speakers.append({
            "speaker_id": str(speaker_id),
            "provider": str(cast.get("provider") or ""),
            "engine": str(cast.get("engine") or "korva-onnx"),
            "voice_id": str(cast.get("voice") or ""),
            "language": str(cast.get("language") or manifest.get("language") or "vi"),
            "speed": cast.get("speed", 1.0),
            "seed": cast.get("seed"),
            "character": next(
                (
                    str(item.get("character"))
                    for item in segments
                    if item.get("character")
                ),
                str(speaker_id),
            ),
            "segment_count": len(segments),
            "segment_ids": [str(item.get("id")) for item in segments],
            "audio_files": [
                str(item.get("file"))
                for item in segments
                if item.get("file")
            ],
            "total_audio_duration_s": round(duration_s, 3),
            "mean_rms_dbfs": round(sum(rms_values) / len(rms_values), 2) if rms_values else None,
            "max_peak_dbfs": round(max(peaks), 2) if peaks else None,
            "identity_fingerprint_count": len(fingerprints),
            "identity_status": "consistent" if len(fingerprints) <= 1 and segments else "review",
            "technical_status": (
                "error" if any(row.get("technical_status") == "error" for row in quality_rows)
                else "warning" if any(row.get("technical_status") == "warning" for row in quality_rows)
                else "pass" if segments else "missing"
            ),
        })

    report = {
        "schema_version": 1,
        "project": manifest.get("project"),
        "language": manifest.get("language", "vi"),
        "speaker_count": len(speakers),
        "segment_count": sum(item["segment_count"] for item in speakers),
        "speaker_identity_drift": sum(
            item["identity_fingerprint_count"] > 1 for item in speakers
        ),
        "speakers": speakers,
        "note": (
            "Voice identity is tracked by the manifest/provider/engine/voice/settings fingerprint. "
            "This is configuration consistency evidence, not biometric speaker-similarity analysis."
        ),
    }
    destination = output_dir / "voice-cast-report.json"
    _write_json(destination, report)
    return {
        "path": destination.name,
        "speaker_count": report["speaker_count"],
        "segment_count": report["segment_count"],
        "speaker_identity_drift": report["speaker_identity_drift"],
    }


def _write_artifact_manifest(output_dir: Path, report: dict[str, Any]) -> dict[str, Any]:
    """Hash every delivery file after reports and README have been finalized."""
    root = output_dir.resolve()
    files = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file() or path.name == "artifact-manifest.json":
            continue
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            raise ValueError(f"Delivery artifact escapes output directory: {path}") from None
        relative = path.relative_to(output_dir).as_posix()
        files.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
            "kind": (
                "audio" if path.suffix.lower() in {".wav", ".mp3", ".flac"}
                else "subtitle" if path.suffix.lower() in {".srt", ".vtt", ".ass"}
                else "timeline" if "timeline" in path.parts
                else "report" if path.suffix.lower() == ".json"
                else "documentation" if path.suffix.lower() in {".md", ".txt"}
                else "other"
            ),
        })
    manifest = {
        "schema_version": 1,
        "project": report.get("project"),
        "status": report.get("status"),
        "runner_run_id": (report.get("runner") or {}).get("run_id"),
        "model_revision": (report.get("model") or {}).get("revision"),
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "files": files,
        "self_hash_note": "This manifest intentionally excludes its own file to avoid a recursive checksum.",
    }
    destination = output_dir / "artifact-manifest.json"
    _write_json(destination, manifest)
    return {
        "path": destination.name,
        "file_count": manifest["file_count"],
        "total_bytes": manifest["total_bytes"],
    }


def run_project(
    manifest_path: Path,
    output_dir: Path,
    *,
    model_revision: str,
) -> dict[str, Any]:
    if importlib.metadata.version("korvatts") != PACKAGE_VERSION:
        raise RuntimeError(f"Expected korvatts=={PACKAGE_VERSION}")
    manifest_path = manifest_path.resolve()
    try:
        manifest_path.relative_to(REPO_ROOT)
    except ValueError:
        raise ValueError("Project manifest must stay inside the checked-out repository") from None
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
    manifest_copy = output_dir / "project-manifest.json"
    shutil.copy2(manifest_path, manifest_copy)
    report = generate(data, output_dir, plan_only=False, stop_on_error=False)
    generation_path = output_dir / "voice-generation-report.json"
    quality_path = output_dir / "voice-quality-report.json"
    generation = json.loads(generation_path.read_text(encoding="utf-8"))

    # KorvaTTS samples can peak close to full scale. Apply -3 dB before the
    # H2 concatenation stage, then refresh the report hashes so every output
    # remains auditable after mastering.
    for item in generation.get("segments", []):
        relative = item.get("file")
        audio_path = (output_dir / relative).resolve() if relative else None
        if not audio_path or not audio_path.is_file():
            continue
        try:
            audio_path.relative_to(output_dir.resolve())
        except ValueError:
            raise ValueError(f"Generation report audio path escapes output: {relative}") from None
        item["mastering"] = normalize_voice_file(
            audio_path, target_lufs=-20.0, true_peak_db=-2.5, loudness_range=7.0
        )
        item["file"] = Path(relative).with_suffix(".wav").as_posix()
        mastered_path = output_dir / item["file"]
        item["sha256"] = _sha256(mastered_path)
        item["bytes"] = mastered_path.stat().st_size
    _write_json(generation_path, generation)

    segment_evidence: list[dict[str, Any]] = []
    for item in generation.get("segments", []):
        row = {
            "id": item.get("id"),
            "speaker_id": item.get("speaker_id"),
            "voice": item.get("voice"),
            "status": item.get("status"),
            "mastering": item.get("mastering"),
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
    cast_report = _write_voice_cast_report(
        output_dir, data, generation, segment_evidence, quality
    )

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
            # H2's timeline builder intentionally appends 1.5 s of silence at
            # the end of the master. Do not report that designed pad as a defect
            # when the measured tail stays within a small decoder tolerance.
            if 1.5 <= h2["master_audio"]["trailing_silence_s"] <= 1.65:
                h2["master_technical_findings"] = [
                    finding for finding in h2["master_technical_findings"]
                    if not finding.startswith("Long trailing silence")
                ]
            h2["intentional_trailing_pad_s"] = 1.5
            blocks_path = output_dir / h2["timeline_dir"] / "blocks.json"
            lines_path = output_dir / h2["timeline_dir"] / "lines.json"
            words_path = output_dir / h2["timeline_dir"] / "words.json"
            blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
            lines = json.loads(lines_path.read_text(encoding="utf-8"))
            words = json.loads(words_path.read_text(encoding="utf-8"))
            expected_ids = {str(item["id"]) for item in segments}
            actual_ids = {str(item.get("id")) for item in blocks}
            if actual_ids != expected_ids:
                raise RuntimeError(
                    f"H2 block coverage mismatch: missing={sorted(expected_ids - actual_ids)}, "
                    f"unexpected={sorted(actual_ids - expected_ids)}"
                )
            if not lines or not words:
                raise RuntimeError("H2 prep_voice.py produced empty line or word timestamps")
            h2["block_count"] = len(blocks)
            h2["line_count"] = len(lines)
            h2["word_count"] = len(words)
            h2["timestamp_coverage"] = "all_project_blocks"
        except Exception as exc:
            h2_error = f"{type(exc).__name__}: {exc}"

    captions = None
    caption_error = None
    if h2 is not None and h2_error is None:
        try:
            captions = _write_caption_assets(output_dir, output_dir / h2["timeline_dir"])
        except Exception as exc:
            caption_error = f"{type(exc).__name__}: {exc}"

    failed = int(generation.get("failed_segments", 0))
    status = "complete" if (
        all_segments_ready and segment_errors == 0 and h2 is not None
        and h2_error is None and captions is not None and caption_error is None
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
            "project_manifest": {
                "path": "project-manifest.json",
                "sha256": _sha256(manifest_copy),
            },
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
            "mastering": {
                "method": "FFmpeg loudnorm",
                "integrated_loudness_lufs": -20.0,
                "true_peak_ceiling_dbtp": -2.5,
                "loudness_range_lu": 7.0,
            },
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
        "captions": captions,
        "caption_error": caption_error,
        "voice_cast_report": cast_report,
        "artifact_manifest": "artifact-manifest.json",
        "quality_report": "voice-quality-report.json",
        "generation_report": "voice-generation-report.json",
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
    if status == "complete":
        _write_delivery_readme(output_dir, result)
    artifact_manifest = _write_artifact_manifest(output_dir, result)
    result["artifact_manifest_summary"] = artifact_manifest
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
