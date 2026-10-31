"""Technical and intelligibility checks for generated voice-over segments.

The report intentionally separates measurable audio/ASR signals from the
human review needed for naturalness, emotional delivery and voice identity.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any

from client import VoiceStudioClient


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value).lower()
    value = "".join(
        ch if ch.isalnum() or ch.isspace() else " "
        for ch in value
    )
    return " ".join(value.split())


def edit_distance(left: list[str] | str, right: list[str] | str) -> int:
    """Memory-bounded Levenshtein distance."""
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (a != b),
            ))
        previous = current
    return previous[-1]


def compare_text(reference: str, hypothesis: str) -> dict[str, Any]:
    expected = normalize_text(reference)
    actual = normalize_text(hypothesis)
    expected_words = expected.split()
    actual_words = actual.split()
    expected_chars = expected.replace(" ", "")
    actual_chars = actual.replace(" ", "")
    word_errors = edit_distance(expected_words, actual_words)
    char_errors = edit_distance(expected_chars, actual_chars)
    return {
        "wer": word_errors / max(1, len(expected_words)),
        "cer": char_errors / max(1, len(expected_chars)),
        "word_errors": word_errors,
        "character_errors": char_errors,
        "expected_word_count": len(expected_words),
        "recognized_word_count": len(actual_words),
        "reference": reference,
        "transcript": hypothesis,
    }


def _probe_audio(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    ffmpeg = shutil.which("ffmpeg")
    if not ffprobe or not ffmpeg:
        raise RuntimeError("ffmpeg and ffprobe are required for audio diagnostics")
    probe = subprocess.run(
        [
            ffprobe, "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate",
            "-show_entries", "format=duration,size",
            "-of", "json", str(path),
        ],
        check=False, capture_output=True, text=True, timeout=30,
    )
    if probe.returncode:
        raise RuntimeError(probe.stderr.strip() or "ffprobe could not read the audio file")
    payload = json.loads(probe.stdout or "{}")
    streams = payload.get("streams") or []
    if not streams:
        raise RuntimeError("No audio stream found")
    stream = streams[0]
    duration = float((payload.get("format") or {}).get("duration") or 0.0)
    original_rate = int(stream.get("sample_rate") or 0)
    channels = int(stream.get("channels") or 0)
    codec = str(stream.get("codec_name") or "unknown")

    command = [
        ffmpeg, "-nostdin", "-v", "error", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1",
        "-ar", "16000", "pipe:1",
    ]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    frame_bytes = 640  # 20 ms of mono PCM16 at 16 kHz
    total_samples = 0
    clipped_samples = 0
    sum_squares = 0
    peak = 0
    silent_frames = 0
    leading_silent_frames = 0
    trailing_silent_frames = 0
    seen_voice = False
    pending = b""
    assert process.stdout is not None
    try:
        while True:
            chunk = process.stdout.read(frame_bytes)
            if not chunk:
                break
            pending += chunk
            while len(pending) >= frame_bytes:
                frame, pending = pending[:frame_bytes], pending[frame_bytes:]
                samples = [
                    int.from_bytes(frame[i:i + 2], "little", signed=True)
                    for i in range(0, frame_bytes, 2)
                ]
                if not samples:
                    continue
                frame_peak = max(abs(x) for x in samples)
                frame_rms = math.sqrt(sum(x * x for x in samples) / len(samples))
                total_samples += len(samples)
                sum_squares += sum(x * x for x in samples)
                clipped_samples += sum(abs(x) >= 32760 for x in samples)
                peak = max(peak, frame_peak)
                is_silent = frame_rms <= 327.68  # approximately -40 dBFS
                if is_silent:
                    silent_frames += 1
                    if not seen_voice:
                        leading_silent_frames += 1
                    trailing_silent_frames += 1
                else:
                    seen_voice = True
                    trailing_silent_frames = 0
        if pending:
            # An incomplete final PCM sample indicates a broken decoder stream.
            if len(pending) % 2:
                raise RuntimeError("Decoder returned an incomplete PCM16 sample")
            samples = [
                int.from_bytes(pending[i:i + 2], "little", signed=True)
                for i in range(0, len(pending), 2)
            ]
            total_samples += len(samples)
            sum_squares += sum(x * x for x in samples)
            clipped_samples += sum(abs(x) >= 32760 for x in samples)
            peak = max(peak, max((abs(x) for x in samples), default=0))
    finally:
        process.stdout.close()
    exit_code = process.wait(timeout=30)
    if exit_code or total_samples == 0:
        raise RuntimeError("ffmpeg could not decode a usable audio stream")

    rms = math.sqrt(sum_squares / total_samples) / 32768
    peak_dbfs = 20 * math.log10(max(peak / 32768, 1e-12))
    rms_dbfs = 20 * math.log10(max(rms, 1e-12))
    decoded_duration = total_samples / 16000
    frame_duration = 0.02
    return {
        "codec": codec,
        "sample_rate_hz": original_rate,
        "channels": channels,
        "duration_s": round(duration or decoded_duration, 3),
        "decoded_duration_s": round(decoded_duration, 3),
        "peak_dbfs": round(peak_dbfs, 2),
        "rms_dbfs": round(rms_dbfs, 2),
        "clipped_sample_ratio": round(clipped_samples / total_samples, 8),
        "silence_ratio_below_minus_40_db": round(
            silent_frames / max(1, round(decoded_duration / frame_duration)), 4
        ),
        "leading_silence_s": round(leading_silent_frames * frame_duration, 3),
        "trailing_silence_s": round(trailing_silent_frames * frame_duration, 3),
    }


def _technical_findings(metrics: dict[str, Any]) -> list[str]:
    findings = []
    if metrics["duration_s"] < 0.25:
        findings.append("Audio is unusually short; check for truncated synthesis.")
    if metrics["sample_rate_hz"] < 16000:
        findings.append("Source sample rate is below 16 kHz.")
    if metrics["clipped_sample_ratio"] > 0.001:
        findings.append("Clipping detected; review gain/mastering.")
    if metrics["peak_dbfs"] > -0.1:
        findings.append("Peak is very close to 0 dBFS; review true-peak headroom.")
    if metrics["rms_dbfs"] < -38:
        findings.append("Average level is very low; check for near-silence.")
    if metrics["trailing_silence_s"] > 1.5:
        findings.append("Long trailing silence; check the render or trim policy.")
    if metrics["silence_ratio_below_minus_40_db"] > 0.8:
        findings.append("Most decoded frames are near-silent.")
    return findings


def audit_report(
    generation_report: dict[str, Any],
    report_path: Path,
    *,
    asr: bool = False,
    language: str | None = None,
) -> dict[str, Any]:
    client = VoiceStudioClient()
    rows = []
    for item in generation_report.get("segments", []):
        row = {
            "id": item.get("id"),
            "speaker_id": item.get("speaker_id"),
            "voice": item.get("voice"),
            "provider": item.get("provider"),
            "engine": item.get("engine"),
            "status": item.get("status"),
        }
        relative = item.get("file")
        if not relative:
            row["technical_status"] = "skipped"
            row["reason"] = "No generated audio path in the report"
            rows.append(row)
            continue
        audio_path = (report_path.parent / relative).resolve()
        if not audio_path.is_file():
            row["technical_status"] = "error"
            row["reason"] = f"Missing audio file: {relative}"
            rows.append(row)
            continue
        try:
            metrics = _probe_audio(audio_path)
            findings = _technical_findings(metrics)
            row["audio"] = metrics
            row["technical_findings"] = findings
            row["technical_status"] = "warning" if findings else "pass"
        except Exception as exc:
            row["technical_status"] = "error"
            row["reason"] = str(exc)

        if asr and item.get("expected_text"):
            try:
                transcript = client.transcribe(
                    audio_path,
                    language=language or item.get("language"),
                )
                row["intelligibility_proxy"] = compare_text(
                    str(item["expected_text"]), transcript
                )
                row["intelligibility_proxy"]["status"] = "available"
            except Exception as exc:
                row["intelligibility_proxy"] = {
                    "status": "unavailable",
                    "reason": str(exc),
                }
        rows.append(row)

    statuses = [row.get("technical_status") for row in rows]
    output = {
        "schema_version": 1,
        "source_report": str(report_path),
        "segment_count": len(rows),
        "technical_pass": statuses.count("pass"),
        "technical_warning": statuses.count("warning"),
        "technical_error": statuses.count("error"),
        "segments": rows,
        "human_review": {
            "status": "required",
            "checklist": [
                "Naturalness and absence of synthetic artifacts",
                "Vietnamese tones, consonants, names and numbers are pronounced correctly",
                "Emotion, pacing and pauses fit the scene",
                "The same character keeps a consistent vocal identity across scenes",
                "The voice is distinguishable from other cast members",
                "Speaker authorization and model/output terms are documented",
            ],
            "note": "ASR WER/CER is only a pronunciation/intelligibility proxy. It does not score naturalness, timbre, emotion or similarity to a reference speaker.",
        },
    }
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path,
                        help="voice-generation-report.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--asr", action="store_true",
                        help="Run generated audio through VoiceStudio's configured ASR")
    parser.add_argument("--language", default=None,
                        help="ASR language code, e.g. vi; defaults to each segment's language")
    args = parser.parse_args()
    try:
        report_path = args.report.resolve()
        generation_report = json.loads(report_path.read_text(encoding="utf-8"))
        result = audit_report(
            generation_report, report_path, asr=args.asr, language=args.language
        )
        output = args.output or report_path.parent / "voice-quality-report.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    except Exception as exc:
        print(f"Voice QA failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "report": str(output),
        "technical_pass": result["technical_pass"],
        "technical_warning": result["technical_warning"],
        "technical_error": result["technical_error"],
        "human_review": "required",
    }, ensure_ascii=False, indent=2))
    return 0 if result["technical_error"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
