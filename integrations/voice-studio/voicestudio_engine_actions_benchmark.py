"""Run a consent-gated Supertonic-3 Vietnamese voice audition through VoiceStudio in GitHub Actions.

This calls the pinned VoiceStudio server's OpenAI-compatible API. It never
accepts the OpenRAIL-M model terms unless --accept-model-license is supplied
by a manually-dispatched Actions run whose operator explicitly confirmed them.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from audio_mastering import normalize_voice_file
from voice_quality import _probe_audio, _technical_findings

ENGINE_ID = "supertonic3"
PACKAGE_VERSION = "1.3.1"
MODEL_REPOSITORY = "Supertone/supertonic-3"
MODEL_REVISION = "724fb5abbf5502583fb520898d45929e62f02c0b"
MODEL_LICENSE = "OpenRAIL-M"
SDK_LICENSE = "MIT"
MODEL_SAMPLE_RATE = 44_100
VOICE_IDS = ("M1", "M3", "M4", "M5", "F3", "F4", "F5")
MAX_TEXT_CHARS = 4096
DEFAULT_TIMEOUT_SECONDS = 1800


class VoiceStudioApiError(RuntimeError):
    """A redacted and bounded VoiceStudio API failure."""


class VoiceStudioApi:
    def __init__(self, base_url: str, api_key: str, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("The Actions engine benchmark only accepts a loopback HTTP VoiceStudio URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("VoiceStudio base URL must not contain credentials, query or fragment")
        if not api_key.strip():
            raise ValueError("VOICESTUDIO_API_KEY is required")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key.strip()
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        expect_audio: bool = False,
    ) -> tuple[bytes, str]:
        body = (
            json.dumps(payload, ensure_ascii=False).encode("utf-8")
            if payload is not None else None
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "audio/wav" if expect_audio else "application/json",
        }
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            self.base_url + path, data=body, headers=headers, method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read(), response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as exc:
            # Never include request headers or the ephemeral key in artifacts.
            detail = exc.read(2048).decode("utf-8", errors="replace")
            raise VoiceStudioApiError(
                f"VoiceStudio API returned HTTP {exc.code}: {detail}"
            ) from None
        except urllib.error.URLError as exc:
            raise VoiceStudioApiError(
                f"Cannot reach the loopback VoiceStudio API: {getattr(exc, 'reason', exc)}"
            ) from None

    def get_json(self, path: str) -> dict[str, Any]:
        data, _ = self.request("GET", path)
        try:
            result = json.loads(data.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise VoiceStudioApiError(f"VoiceStudio returned invalid JSON from {path}") from None
        if not isinstance(result, dict):
            raise VoiceStudioApiError(f"VoiceStudio returned an unexpected response from {path}")
        return result

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        data, _ = self.request("POST", path, payload=payload)
        try:
            result = json.loads(data.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise VoiceStudioApiError(f"VoiceStudio returned invalid JSON from {path}") from None
        if not isinstance(result, dict):
            raise VoiceStudioApiError(f"VoiceStudio returned an unexpected response from {path}")
        return result

    def synthesize(self, text: str, voice: str, destination: Path) -> dict[str, Any]:
        data, content_type = self.request(
            "POST",
            "/v1/audio/speech",
            payload={
                "model": ENGINE_ID,
                "input": text,
                "voice": voice,
                "language": "vi",
                "speed": 1.0,
                "num_step": 12,
                "response_format": "wav",
            },
            expect_audio=True,
        )
        if not data.startswith(b"RIFF") or data[8:12] != b"WAVE":
            raise VoiceStudioApiError(
                f"VoiceStudio did not return a valid WAV for preset {voice} (content-type {content_type})"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".part")
        temporary.write_bytes(data)
        temporary.replace(destination)
        return {
            "content_type": content_type,
            "bytes": destination.stat().st_size,
            "sha256": _sha256(destination),
        }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_suite(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Suite must be a schema_version 1 object")
    if str(data.get("language") or "").lower() != "vi":
        raise ValueError("Supertonic-3 Actions benchmark accepts Vietnamese (vi) only")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Suite must contain at least one case")
    seen: set[str] = set()
    normalized = []
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            raise ValueError(f"cases[{index - 1}] must be an object")
        case_id = str(case.get("id") or "").strip()
        text = str(case.get("text") or "").strip()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,48}", case_id):
            raise ValueError(f"Invalid case ID at index {index - 1}")
        if case_id in seen:
            raise ValueError(f"Duplicate case ID: {case_id}")
        if not text or len(text) > MAX_TEXT_CHARS:
            raise ValueError(f"{case_id} text must contain 1–{MAX_TEXT_CHARS} characters")
        seen.add(case_id)
        normalized.append({
            "id": case_id,
            "title": str(case.get("title") or case_id),
            "purpose": str(case.get("purpose") or ""),
            "text": text,
        })
    data["cases"] = normalized
    return data


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def verify_or_accept_license(api: VoiceStudioApi, *, accept_model_license: bool) -> dict[str, Any]:
    state = api.get_json(f"/api/settings/license/{ENGINE_ID}")
    already_accepted = state.get("accepted") is True
    if not already_accepted:
        if not accept_model_license:
            raise PermissionError(
                "Supertonic-3 is license-gated. Read the OpenRAIL-M model terms and "
                "manually dispatch the GitHub Actions workflow with accept_openrail_m=true."
            )
        accepted = api.post_json(
            "/api/settings/license",
            {"engine_id": ENGINE_ID, "accepted": True},
        )
        if accepted.get("ok") is not True or accepted.get("accepted") is not True:
            raise VoiceStudioApiError("VoiceStudio did not confirm Supertonic-3 license acceptance")
        state = api.get_json(f"/api/settings/license/{ENGINE_ID}")
        already_accepted = state.get("accepted") is True
    if not already_accepted:
        raise VoiceStudioApiError("Supertonic-3 license acceptance did not persist")
    return {
        "engine_id": ENGINE_ID,
        "accepted": True,
        "accepted_in_this_run": not state.get("was_previously_accepted", False),
        "model_license": MODEL_LICENSE,
        "sdk_license": SDK_LICENSE,
        "model_repository": MODEL_REPOSITORY,
        "model_revision": MODEL_REVISION,
        "acceptance_source": "manual workflow_dispatch input" if accept_model_license else "pre-existing CI-local state",
    }


def _master_and_probe(path: Path) -> dict[str, Any]:
    mastering = normalize_voice_file(
        path,
        target_lufs=-20.0,
        true_peak_db=-2.5,
        loudness_range=7.0,
    )
    metrics = _probe_audio(path)
    findings = _technical_findings(metrics)
    if metrics["sample_rate_hz"] != MODEL_SAMPLE_RATE:
        findings.append(
            f"Expected {MODEL_SAMPLE_RATE} Hz, got {metrics['sample_rate_hz']} Hz"
        )
    return {
        "mastering": mastering,
        "audio_metrics": metrics,
        "technical_findings": findings,
        "technical_status": "warning" if findings else "pass",
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
    }


def _write_audition_page(path: Path, title: str, purpose: str, candidates: list[dict[str, Any]]) -> None:
    cards = []
    for row in candidates:
        label = html.escape(str(row["blind_label"]), quote=True)
        audio = html.escape(str(row["audio_file"]), quote=True)
        cards.append(
            f'<article data-label="{label}"><h2>{label}</h2>'
            f'<audio controls preload="none" src="{audio}"></audio>'
            '<div class="ratings">'
            + "".join(
                f'<label>{html.escape(dim)} <select data-rating="{dim}">'
                + '<option value="">—</option>'
                + "".join(f'<option value="{n}">{n}</option>' for n in range(1, 6))
                + '</select></label>'
                for dim in ("naturalness", "vietnamese", "identity", "expression", "character_fit")
            )
            + '</div><label class="notes">Notes<textarea data-notes rows="3"></textarea></label></article>'
        )
    page = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>VoiceStudio Supertonic-3 blind audition</title>
<style>
:root{color-scheme:dark;background:#10131a;color:#eef2f8;font:15px system-ui,sans-serif}
body{max-width:900px;margin:28px auto;padding:0 18px}article{background:#1b202b;border:1px solid #394253;border-radius:12px;padding:16px;margin:14px 0}
audio{display:block;width:100%;margin:10px 0}h1{font-size:26px}h2{font-size:18px}
.ratings{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
label{display:grid;gap:5px;font-size:13px}select,textarea{background:#303747;color:white;border:1px solid #596579;border-radius:7px;padding:7px}
textarea{width:100%;box-sizing:border-box}.muted{color:#aab5c5}
button{background:#e6edf7;color:#121722;border:0;border-radius:8px;padding:10px 14px;font-weight:650}
</style></head><body>""" + (
        f"<h1>{html.escape(title)}</h1><p class='muted'>{html.escape(purpose)}</p>"
        "<p class='muted'>All samples use the same script, Vietnamese language, "
        "voice speed, and 12-step quality setting. Preset identity is hidden during rating.</p>"
        + "\n".join(cards)
        + '<button id="export">Export ratings JSON</button><script>'
        + """document.getElementById('export').addEventListener('click',()=>{
const data={schema_version:1,ratings:[...document.querySelectorAll('article')].map(card=>{
const ratings={};card.querySelectorAll('[data-rating]').forEach(el=>{
ratings[el.dataset.rating]=el.value===''?null:Number(el.value);
});
return {candidate:card.dataset.label,ratings,notes:card.querySelector('[data-notes]').value.trim()};
})};
const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='voice-human-ratings.json';a.click();URL.revokeObjectURL(a.href);
});</script></body></html>"""
    )
    path.write_text(page, encoding="utf-8")


def run_benchmark(
    suite_path: Path,
    output_dir: Path,
    api: VoiceStudioApi,
    *,
    accept_model_license: bool,
    blind_seed: int = 20261031,
) -> dict[str, Any]:
    suite = load_suite(suite_path)
    license_receipt = verify_or_accept_license(
        api, accept_model_license=accept_model_license,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    case_results = []
    for case_index, case in enumerate(suite["cases"], 1):
        voices = list(VOICE_IDS)
        random.Random(blind_seed + case_index).shuffle(voices)
        case_root = output_dir / "cases" / case["id"]
        candidates = []
        for index, voice_id in enumerate(voices, 1):
            label = f"Candidate {index:02d}"
            filename = f"{index:03d}-{label.replace(' ', '-')}.wav"
            destination = case_root / "audio" / filename
            row: dict[str, Any] = {
                "index": index,
                "blind_label": label,
                "provider": "voicestudio",
                "engine": ENGINE_ID,
                "voice_id": voice_id,
                "language": "vi",
                "status": "pending",
                "audio_file": f"audio/{filename}",
            }
            try:
                response = api.synthesize(case["text"], voice_id, destination)
                technical = _master_and_probe(destination)
                row.update({
                    "status": "ready",
                    "raw_response": response,
                    **technical,
                })
            except Exception as exc:
                row["status"] = "failed"
                row["error"] = f"{type(exc).__name__}: {exc}"
            candidates.append(row)
            print(f"[{case_index}/{len(suite['cases'])}] {case['id']} {label}: {row['status']}")

        case_ready = sum(row["status"] == "ready" for row in candidates)
        technical_pass = sum(row.get("technical_status") == "pass" for row in candidates)
        technical_warning = sum(row.get("technical_status") == "warning" for row in candidates)
        technical_error = sum(row["status"] == "failed" or row.get("technical_status") == "error" for row in candidates)
        case_report = {
            "schema_version": 1,
            "case": case,
            "status": "complete" if case_ready == len(VOICE_IDS) and technical_error == 0 else "partial",
            "candidate_count": len(candidates),
            "ready": case_ready,
            "failed": len(candidates) - case_ready,
            "technical_pass": technical_pass,
            "technical_warning": technical_warning,
            "technical_error": technical_error,
            "candidates": candidates,
        }
        case_root.mkdir(parents=True, exist_ok=True)
        _write_json(case_root / "supertonic3-benchmark.json", case_report)
        _write_audition_page(case_root / "index.html", case["title"], case["purpose"], candidates)
        case_results.append(case_report)

    flat = [row for case in case_results for row in case["candidates"]]
    mastered = [row["mastering"] for row in flat if row.get("mastering")]
    true_peaks = [
        float(item["output_true_peak_dbtp"])
        for item in mastered if isinstance(item.get("output_true_peak_dbtp"), (int, float))
    ]
    output_lufs = [
        float(item["output_integrated_loudness_lufs"])
        for item in mastered if isinstance(item.get("output_integrated_loudness_lufs"), (int, float))
    ]
    report = {
        "schema_version": 1,
        "status": "complete" if all(case["status"] == "complete" for case in case_results) else "partial",
        "engine": ENGINE_ID,
        "voice_ids": list(VOICE_IDS),
        "language": "vi",
        "package_version": PACKAGE_VERSION,
        "model": {
            "repository": MODEL_REPOSITORY,
            "revision": MODEL_REVISION,
            "weights_license": MODEL_LICENSE,
            "sdk_license": SDK_LICENSE,
            "sample_rate_hz": MODEL_SAMPLE_RATE,
        },
        "license_receipt": license_receipt,
        "runner": {
            "os": os.getenv("RUNNER_OS", "unknown"),
            "arch": os.getenv("RUNNER_ARCH", "unknown"),
            "run_id": os.getenv("GITHUB_RUN_ID"),
            "commit": os.getenv("GITHUB_SHA"),
        },
        "candidate_count": len(flat),
        "ready_count": sum(row["status"] == "ready" for row in flat),
        "failed_count": sum(row["status"] == "failed" for row in flat),
        "technical_pass": sum(row.get("technical_status") == "pass" for row in flat),
        "technical_warning": sum(row.get("technical_status") == "warning" for row in flat),
        "technical_error": sum(row["status"] == "failed" or row.get("technical_status") == "error" for row in flat),
        "mastering": {
            "target_lufs": -20.0,
            "true_peak_ceiling_dbtp": -2.5,
            "mastered_count": len(mastered),
            "mean_output_lufs": round(sum(output_lufs) / len(output_lufs), 2) if output_lufs else None,
            "maximum_output_true_peak_dbtp": max(true_peaks) if true_peaks else None,
        },
        "human_review_required": True,
        "naturalness_score": None,
        "elevenlabs_equivalence": None,
        "cases": case_results,
    }
    _write_json(output_dir / "supertonic3-actions-benchmark.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--base-url", default="http://127.0.0.1:3900")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--accept-model-license",
        action="store_true",
        help="Explicitly accept the pinned Supertonic-3 OpenRAIL-M terms in this disposable CI container.",
    )
    parser.add_argument("--blind-seed", type=int, default=20261031)
    args = parser.parse_args()
    try:
        api = VoiceStudioApi(
            args.base_url,
            os.environ.get("VOICESTUDIO_API_KEY", ""),
            timeout=args.timeout,
        )
        report = run_benchmark(
            args.suite,
            args.output,
            api,
            accept_model_license=args.accept_model_license,
            blind_seed=args.blind_seed,
        )
    except Exception as exc:
        print(f"Supertonic-3 Actions benchmark failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    summary = {
        "status": report["status"],
        "candidate_count": report["candidate_count"],
        "ready": report["ready_count"],
        "failed": report["failed_count"],
        "technical_pass": report["technical_pass"],
        "technical_warning": report["technical_warning"],
        "technical_error": report["technical_error"],
        "mastering": report["mastering"],
        "report": str(args.output / "supertonic3-actions-benchmark.json"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if report["status"] != "complete" else 0


if __name__ == "__main__":
    raise SystemExit(main())
