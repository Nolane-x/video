"""Generate and QA a multi-scenario Vietnamese TTS lab entirely on GitHub Actions."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.metadata
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from audio_mastering import normalize_voice_file
from providers import korva
from provider_voice_benchmark import run_benchmark
from voice_quality import _probe_audio, _technical_findings

MODEL_REPOSITORY = "dogenthq/KorvaTTS"
MODEL_LICENSE = "Apache-2.0"
PACKAGE_VERSION = "0.1.3"
EXPECTED_SAMPLE_RATE = 44_100


def load_suite(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Benchmark suite must be schema_version 1")
    if str(data.get("language") or "").lower() != "vi":
        raise ValueError("Actions voice lab currently accepts Vietnamese only")
    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("Benchmark suite must contain at least one case")
    seen: set[str] = set()
    cases: list[dict[str, str]] = []
    for index, raw in enumerate(raw_cases, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"cases[{index - 1}] must be an object")
        case_id = str(raw.get("id") or "").strip()
        title = str(raw.get("title") or "").strip()
        purpose = str(raw.get("purpose") or "").strip()
        text = str(raw.get("text") or "").strip()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,48}", case_id):
            raise ValueError(f"cases[{index - 1}].id must be a safe lowercase slug")
        if case_id in seen:
            raise ValueError(f"Duplicate benchmark case ID: {case_id}")
        seen.add(case_id)
        if not title or not purpose or not text or len(text) > 4096:
            raise ValueError(f"{case_id} needs title, purpose and 1–4096 characters of text")
        cases.append({"id": case_id, "title": title, "purpose": purpose, "text": text})
    data["cases"] = cases
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def safe_audio_path(root: Path, relative: str) -> Path:
    base = root.resolve()
    try:
        candidate = (base / relative).resolve()
        candidate.relative_to(base)
    except (OSError, ValueError):
        raise ValueError(f"Audio path escapes benchmark output: {relative}") from None
    if not candidate.is_file():
        raise FileNotFoundError(f"Missing benchmark audio: {relative}")
    return candidate


def master_candidates(
    case_root: Path,
    benchmark: dict[str, Any],
) -> dict[str, Any]:
    """Normalize each raw voice to a common loudness/true-peak target before blind QA."""
    report_path = case_root / "provider-voice-benchmark.json"
    for row in benchmark.get("candidates", []):
        if row.get("status") != "ready":
            continue
        try:
            audio_path = safe_audio_path(case_root, str(row.get("audio_file") or ""))
            if not row.get("mastering"):
                mastering = normalize_voice_file(
                    audio_path,
                    target_lufs=-20.0,
                    true_peak_db=-2.5,
                    loudness_range=7.0,
                )
                mastered_path = audio_path.with_suffix(".wav")
                relative = mastered_path.resolve().relative_to(case_root.resolve())
                row["audio_file"] = relative.as_posix()
                row["mastering"] = mastering
                row["sha256"] = hashlib.sha256(mastered_path.read_bytes()).hexdigest()
                row["bytes"] = mastered_path.stat().st_size
            else:
                mastered_path = safe_audio_path(case_root, str(row["audio_file"]))
                digest = hashlib.sha256(mastered_path.read_bytes()).hexdigest()
                if digest != row.get("sha256"):
                    raise ValueError("Previously mastered audio hash no longer matches")
        except Exception as exc:
            row["status"] = "failed"
            row["error"] = f"Mastering failed: {type(exc).__name__}: {exc}"
            row["mastering_error"] = row["error"]
        benchmark["ready"] = sum(item.get("status") == "ready" for item in benchmark["candidates"])
        benchmark["failed"] = sum(item.get("status") == "failed" for item in benchmark["candidates"])
        benchmark["pending"] = sum(item.get("status") == "pending" for item in benchmark["candidates"])
        benchmark["status"] = (
            "complete"
            if benchmark["ready"] == benchmark["candidate_count"] and not benchmark.get("catalogue_errors")
            else "partial"
        )
        _write_json(report_path, benchmark)
    return benchmark


def audit_candidate(case_root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    row = dict(candidate)
    if row.get("status") != "ready" or not row.get("audio_file"):
        row["technical_status"] = "error"
        row["technical_error"] = row.get("error") or "Synthesis produced no audio"
        return row
    try:
        audio_path = safe_audio_path(case_root, str(row["audio_file"]))
        digest = hashlib.sha256(audio_path.read_bytes()).hexdigest()
        if digest != row.get("sha256"):
            raise ValueError("Audio SHA-256 does not match benchmark report")
        metrics = _probe_audio(audio_path)
        findings = _technical_findings(metrics)
        if metrics["sample_rate_hz"] != EXPECTED_SAMPLE_RATE:
            findings.append(f"Expected {EXPECTED_SAMPLE_RATE} Hz, got {metrics['sample_rate_hz']} Hz")
        row["audio_metrics"] = metrics
        row["mastering"] = row.get("mastering")
        row["technical_findings"] = findings
        row["technical_status"] = "warning" if findings else "pass"
        row["audio_sha256_verified"] = True
    except Exception as exc:
        row["technical_status"] = "error"
        row["technical_error"] = f"{type(exc).__name__}: {exc}"
    return row


def write_index(output_dir: Path, report: dict[str, Any]) -> None:
    cards = []
    for case in report["cases"]:
        cid = html.escape(case["id"], quote=True)
        cards.append(
            f'<article><h2>{html.escape(case["title"])}</h2>'
            f'<p>{html.escape(case["purpose"])}</p>'
            f'<p>{case["ready"]}/{case["candidate_count"]} audio · '
            f'{case["technical_pass"]} technical pass · '
            f'{case["technical_warning"]} warnings · {case["technical_error"]} errors</p>'
            f'<a href="cases/{cid}/index.html">Open blind audition</a></article>'
        )
    doc = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nolane Voice Actions Lab</title>
<style>
:root{color-scheme:dark;background:#10131a;color:#f0f2f7;font:15px system-ui,sans-serif}
body{max-width:980px;margin:32px auto;padding:0 18px}h1{font-size:27px}
.muted{color:#aeb6c6;line-height:1.55}
article{background:#1b202b;border:1px solid #353d4d;border-radius:12px;padding:17px;margin:14px 0}
h2{font-size:18px;margin:0 0 8px}a{color:#a9ceff}
</style></head><body><h1>Nolane Voice Actions Lab</h1>
<p class="muted">Rendered by GitHub Actions on a CPU runner. Each candidate in each
case receives the identical Vietnamese text. Candidate names and IDs are hidden
in the listening pages. Technical checks are not naturalness scores.</p>
""" + "\n".join(cards) + "</body></html>"
    (output_dir / "index.html").write_text(doc, encoding="utf-8")


def write_summary(output_dir: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Nolane Voice Actions Lab", "",
        f"- Status: **{report['status']}**",
        f"- GitHub Actions run: {report['runner']['run_id']}",
        f"- Runner: {report['runner']['os']} / {report['runner']['arch']}",
        f"- KorvaTTS: {report['model']['package_version']}",
        f"- Hugging Face model revision: {report['model']['revision']}",
        f"- Model and voice-style licence: {MODEL_LICENSE}",
        f"- Output sample rate target: {EXPECTED_SAMPLE_RATE} Hz",
        "- Device: CPU; 4 ONNX threads; 32 inference steps.",
        "- Every rendered sample is loudness-normalized to -20 LUFS with a -2.5 dBTP true-peak ceiling before blind listening and QA.",
        "- Same text and seed are used for every voice within a test case.",
        "- Blind listening is required; no automatic ElevenLabs-equivalence claim.", "",
        "| Test | Ready | Technical pass | Warnings | Errors |",
        "|---|---:|---:|---:|---:|",
    ]
    for case in report["cases"]:
        lines.append(
            f"| {case['title']} | {case['ready']}/{case['candidate_count']} | "
            f"{case['technical_pass']} | {case['technical_warning']} | {case['technical_error']} |"
        )
    lines.extend(["", "## Per-candidate audio measurements", "",
                  "| Case | Candidate | Voice ID | Duration | RMS dBFS | Peak dBFS | QA |",
                  "|---|---|---|---:|---:|---:|---|"])
    for case in report["cases"]:
        for row in case["candidates"]:
            metrics = row.get("audio_metrics") or {}
            lines.append(
                f"| {case['id']} | {row.get('blind_label', '')} | {row.get('id', '')} | "
                f"{metrics.get('duration_s', '—')} | {metrics.get('rms_dbfs', '—')} | "
                f"{metrics.get('peak_dbfs', '—')} | {row.get('technical_status', 'error')} |"
            )
    lines.extend([
        "", "## Listening", "",
        "Open index.html and follow each case link. Listen to each full sample before rating it.",
        "The blind pages export subjective 1–5 ratings and written reviewer notes.",
        "", "## Limits", "",
        "- This runs the ten released KorvaTTS presets; it does not create custom voices or clone people.",
        "- Audio engineering measurements do not grade pronunciation, emotion, acting or naturalness.",
        "- Loudness mastering removes raw output-level differences; it does not repair pronunciation or improve the underlying voice model.",
        "- ASR WER/CER is not included because this job does not run a VoiceStudio ASR engine.",
        "- This CPU baseline is not evidence of GPU engine performance.",
    ])
    (output_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_lab(
    suite_path: Path, output_dir: Path, *, model_revision: str,
    steps: int = 32, threads: int = 4, plan_only: bool = False,
) -> dict[str, Any]:
    suite = load_suite(suite_path)
    if not re.fullmatch(r"[0-9a-f]{40,64}", model_revision):
        raise ValueError("model_revision must be an immutable Hugging Face commit SHA")
    if steps != 32 or threads != 4:
        raise ValueError("Actions baseline is pinned to 32 inference steps and 4 CPU threads")
    output_dir.mkdir(parents=True, exist_ok=True)

    if plan_only:
        plan = {
            "status": "plan_only",
            "model": {"repository": MODEL_REPOSITORY, "revision": model_revision,
                      "package_version": PACKAGE_VERSION, "license": MODEL_LICENSE},
            "cases": suite["cases"],
            "voices": korva.list_voices("vi"),
            "synthesis": {"device": "cpu", "threads": threads, "total_steps": steps},
        }
        _write_json(output_dir / "plan.json", plan)
        return plan

    installed_version = importlib.metadata.version("korvatts")
    if installed_version != PACKAGE_VERSION:
        raise RuntimeError(f"Expected korvatts=={PACKAGE_VERSION}, found {installed_version}")
    from huggingface_hub import snapshot_download

    assets_path = snapshot_download(
        repo_id=MODEL_REPOSITORY,
        revision=model_revision,
        allow_patterns=["onnx/*", "voice_styles/*"],
    )
    os.environ["KORVATTS_ASSETS_DIR"] = str(assets_path)
    os.environ.setdefault("OMP_NUM_THREADS", str(threads))
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    # One cold ONNX load is shared by every voice and scenario in this process.
    engine = korva._engine(threads)
    available = set(engine.list_voices())
    expected = {item["id"] for item in korva.list_voices("vi")}
    if expected - available:
        raise RuntimeError(f"Model is missing voice styles: {sorted(expected - available)}")

    case_results: list[dict[str, Any]] = []
    incomplete = False
    for index, case in enumerate(suite["cases"], 1):
        case_root = output_dir / "cases" / case["id"]
        benchmark = run_benchmark(
            "korva", case["text"], case_root,
            language="vi", limit=10, seed=4200 + index,
            blind=True, blind_seed=20261031, allow_cloud=False,
            delay=0, asr=False,
        )
        benchmark = master_candidates(case_root, benchmark)
        audited = [audit_candidate(case_root, item) for item in benchmark["candidates"]]
        ready = sum(row.get("status") == "ready" for row in audited)
        passed = sum(row.get("technical_status") == "pass" for row in audited)
        warned = sum(row.get("technical_status") == "warning" for row in audited)
        errored = sum(row.get("technical_status") == "error" for row in audited)
        case_report = {
            "schema_version": 1, "case": case, "provider": "korva",
            "engine": f"korvatts=={installed_version} / ONNX CPU",
            "status": "complete" if ready == 10 and errored == 0 else "partial",
            "candidate_count": len(audited), "ready": ready,
            "failed": benchmark["failed"], "technical_pass": passed,
            "technical_warning": warned, "technical_error": errored,
            "benchmark_report": "provider-voice-benchmark.json",
            "audition_page": "index.html", "candidates": audited,
        }
        _write_json(case_root / "actions-case-report.json", case_report)
        case_results.append({
            "id": case["id"], "title": case["title"], "purpose": case["purpose"],
            "candidate_count": len(audited), "ready": ready,
            "failed": benchmark["failed"], "technical_pass": passed,
            "technical_warning": warned, "technical_error": errored,
            "candidates": audited,
        })
        if ready != 10 or benchmark["status"] != "complete" or errored:
            incomplete = True

    report = {
        "schema_version": 1, "status": "partial" if incomplete else "complete",
        "provider": "korva", "language": "vi",
        "model": {
            "repository": MODEL_REPOSITORY, "revision": model_revision,
            "package_version": installed_version, "license": MODEL_LICENSE,
            "asset_directories_downloaded": ["onnx/", "voice_styles/"],
            "reference_recordings_downloaded": False, "runtime": "CPU / ONNX Runtime",
        },
        "runner": {
            "os": os.getenv("RUNNER_OS", "unknown"),
            "arch": os.getenv("RUNNER_ARCH", "unknown"),
            "image_os": os.getenv("ImageOS"), "image_version": os.getenv("ImageVersion"),
            "run_id": os.getenv("GITHUB_RUN_ID"), "run_number": os.getenv("GITHUB_RUN_NUMBER"),
            "commit": os.getenv("GITHUB_SHA"),
        },
        "synthesis": {
            "device": "cpu", "threads": threads, "total_steps": steps,
            "language": "vi", "blind": True, "blind_seed": 20261031,
            "seed_per_case": "4200 + case index; shared by all voices in a case",
        },
        "case_count": len(case_results),
        "candidate_render_count": sum(c["candidate_count"] for c in case_results),
        "ready_render_count": sum(c["ready"] for c in case_results),
        "failed_render_count": sum(c["failed"] for c in case_results),
        "technical_pass_count": sum(c["technical_pass"] for c in case_results),
        "technical_warning_count": sum(c["technical_warning"] for c in case_results),
        "technical_error_count": sum(c["technical_error"] for c in case_results),
        "cases": case_results, "human_review_required": True,
        "naturalness_score": None, "elevenlabs_equivalence": None,
    }
    _write_json(output_dir / "actions-voice-lab.json", report)
    write_index(output_dir, report)
    write_summary(output_dir, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()
    try:
        report = run_lab(
            args.suite, args.output, model_revision=args.model_revision,
            steps=args.steps, threads=args.threads, plan_only=args.plan_only,
        )
    except Exception as exc:
        print(f"GitHub Actions voice lab failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": report["status"],
        "cases": report.get("case_count", len(report.get("cases", []))),
        "candidate_render_count": report.get("candidate_render_count"),
        "ready_render_count": report.get("ready_render_count"),
        "failed_render_count": report.get("failed_render_count"),
        "report": str(args.output / ("plan.json" if args.plan_only else "actions-voice-lab.json")),
    }, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
