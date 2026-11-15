"""Deterministic FFmpeg loudness mastering for spoken-word TTS artifacts.

This is a post-synthesis engineering pass, not a naturalness processor. It
targets a common integrated loudness and true-peak ceiling so blind auditions
are not biased by raw provider gain differences.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path
from typing import Any


_LOUDNORM_OBJECT = re.compile(r"\{\s*\"input_i\".*?\}", re.DOTALL)


class AudioMasteringError(RuntimeError):
    """Raised when the FFmpeg mastering pass fails validation."""


def parse_loudnorm_stats(stderr: str) -> dict[str, str]:
    """Parse FFmpeg loudnorm's final JSON statistics block."""
    matches = _LOUDNORM_OBJECT.findall(stderr or "")
    if not matches:
        raise AudioMasteringError("FFmpeg loudnorm did not emit its JSON measurements")
    try:
        payload = json.loads(matches[-1])
    except (json.JSONDecodeError, TypeError) as exc:
        raise AudioMasteringError("FFmpeg loudnorm emitted malformed JSON measurements") from exc
    required = ("input_i", "input_tp", "output_i", "output_tp", "output_lra")
    if any(key not in payload for key in required):
        raise AudioMasteringError("FFmpeg loudnorm measurements are incomplete")
    return {key: str(payload[key]) for key in required}


def _finite_measurement(stats: dict[str, str], key: str) -> float:
    try:
        value = float(stats[key])
    except (TypeError, ValueError, KeyError):
        raise AudioMasteringError(f"Invalid loudnorm measurement: {key}") from None
    if not math.isfinite(value):
        raise AudioMasteringError(f"Non-finite loudnorm measurement: {key}")
    return value


def normalize_voice_file(
    source: str | Path,
    *,
    target_lufs: float = -20.0,
    true_peak_db: float = -2.5,
    loudness_range: float = 7.0,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    """Normalize one audio file in place and return measured before/after data.

    The final file is lossless mono PCM WAV at 44.1 kHz. MP3 inputs are
    intentionally converted to WAV so downstream video and audition tools
    operate on one deterministic format.
    """
    path = Path(source).resolve()
    if not path.is_file() or path.stat().st_size <= 44:
        raise AudioMasteringError(f"Audio source is missing or too small: {path}")
    if not (-30.0 <= target_lufs <= -14.0):
        raise ValueError("target_lufs must be between -30 and -14 LUFS")
    if not (-6.0 <= true_peak_db <= -1.0):
        raise ValueError("true_peak_db must be between -6 and -1 dBTP")
    if not (1.0 <= loudness_range <= 20.0):
        raise ValueError("loudness_range must be between 1 and 20 LU")

    temporary = path.with_name(path.stem + ".mastered.tmp.wav")
    filter_value = (
        f"loudnorm=I={target_lufs:g}:TP={true_peak_db:g}:"
        f"LRA={loudness_range:g}:print_format=json"
    )
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-v", "info", "-y",
        "-i", str(path),
        "-af", filter_value,
        "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le",
        str(temporary),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        temporary.unlink(missing_ok=True)
        raise AudioMasteringError(
            f"FFmpeg loudness mastering exceeded {timeout_seconds} seconds"
        ) from exc
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise AudioMasteringError(f"Cannot start FFmpeg: {exc}") from None

    if completed.returncode != 0 or not temporary.is_file() or temporary.stat().st_size <= 44:
        temporary.unlink(missing_ok=True)
        detail = (completed.stderr or completed.stdout or "").strip()[-2500:]
        raise AudioMasteringError(
            "FFmpeg loudness mastering failed"
            + (f": {detail}" if detail else f" (exit {completed.returncode})")
        )

    try:
        stats = parse_loudnorm_stats(completed.stderr)
        input_i = _finite_measurement(stats, "input_i")
        input_tp = _finite_measurement(stats, "input_tp")
        output_i = _finite_measurement(stats, "output_i")
        output_tp = _finite_measurement(stats, "output_tp")
        output_lra = _finite_measurement(stats, "output_lra")
        if abs(output_i - target_lufs) > 1.0:
            raise AudioMasteringError(
                f"Integrated loudness target missed: {output_i:.2f} LUFS "
                f"(target {target_lufs:.2f} LUFS)"
            )
        if output_tp > true_peak_db + 0.3:
            raise AudioMasteringError(
                f"True-peak ceiling missed: {output_tp:.2f} dBTP "
                f"(limit {true_peak_db:.2f} dBTP)"
            )
        if temporary.stat().st_size <= 44:
            raise AudioMasteringError("Mastered WAV is unexpectedly small")
        original_suffix = path.suffix.lower()
        final_path = path.with_suffix(".wav") if original_suffix != ".wav" else path
        temporary.replace(final_path)
        if final_path != path:
            path.unlink(missing_ok=True)
        return {
            "filter": "ffmpeg-loudnorm",
            "target_integrated_loudness_lufs": target_lufs,
            "true_peak_ceiling_dbtp": true_peak_db,
            "loudness_range_target_lu": loudness_range,
            "input_integrated_loudness_lufs": round(input_i, 2),
            "input_true_peak_dbtp": round(input_tp, 2),
            "output_integrated_loudness_lufs": round(output_i, 2),
            "output_true_peak_dbtp": round(output_tp, 2),
            "output_loudness_range_lu": round(output_lra, 2),
            "output_path": final_path.name,
            "output_bytes": final_path.stat().st_size,
        }
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
