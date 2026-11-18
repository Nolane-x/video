#!/usr/bin/env python3
"""Place VoiceStudio's verified Vietnamese narration chunks into H2 shot time.

VoiceStudio renders each shot line as a separate named segment. This adapter
moves each segment from the temporary concatenated narration timeline to the
matching H2 shot start, trims only by pitch-preserving atempo within a small
bounded limit, writes a full-length stereo voice.wav, and emits video-aligned
SRT/VTT subtitles.
"""
from __future__ import annotations
import argparse
import json
import math
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 48_000
START_OFFSET = 0.16
TAIL_GUARD = 0.06
MAX_ATEMPO = 1.20
FADE_SECONDS = 0.012

def ts(seconds: float, vtt: bool = False) -> str:
    total = max(0, int(round(seconds * 1000)))
    hh, rem = divmod(total, 3_600_000)
    mm, rem = divmod(rem, 60_000)
    ss, ms = divmod(rem, 1000)
    return f"{hh:02d}:{mm:02d}:{ss:02d}{'.' if vtt else ','}{ms:03d}"

def atempo_wav(samples: np.ndarray, rate: float, tempdir: Path, index: int) -> np.ndarray:
    """Use FFmpeg atempo to shorten a long line without raising its pitch."""
    src = tempdir / f"voice-in-{index:03d}.wav"
    dst = tempdir / f"voice-out-{index:03d}.wav"
    sf.write(src, samples, SAMPLE_RATE, subtype="PCM_16")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(src), "-af", f"atempo={rate:.5f}",
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le", str(dst)
    ], check=True, timeout=120)
    out, sr = sf.read(dst, dtype="float32", always_2d=False)
    if sr != SAMPLE_RATE or out.ndim != 1 or not np.isfinite(out).all():
        raise RuntimeError(f"Invalid atempo output for segment {index}")
    return out

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--artifact-dir", required=True)
    args = parser.parse_args()
    project = Path(args.project)
    artifact = Path(args.artifact_dir)
    story = json.loads((project / "story" / "shots.json").read_text(encoding="utf-8"))
    manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
    audio_meta = manifest["audio"]
    if manifest.get("language") != "vi" or manifest.get("engine") != "vieneu":
        raise RuntimeError("Expected a Vietnamese VieNeu VoiceStudio artifact")
    if audio_meta.get("watermark", {}).get("status") != "verified":
        raise RuntimeError("VoiceStudio AudioSeal watermark was not verified")
    if audio_meta.get("checks") != "passed":
        raise RuntimeError("VoiceStudio audio quality checks did not pass")
    if audio_meta.get("sample_rate") != SAMPLE_RATE or audio_meta.get("channels") != 1:
        raise RuntimeError("VoiceStudio master must be 48 kHz mono")
    narration, sr = sf.read(artifact / "narration.wav", dtype="float32", always_2d=False)
    if sr != SAMPLE_RATE or narration.ndim != 1 or not np.isfinite(narration).all():
        raise RuntimeError("narration.wav must be finite 48 kHz mono")
    if abs(len(narration) / SAMPLE_RATE - float(audio_meta["duration_seconds"])) > 0.06:
        raise RuntimeError("Narration file duration does not match VoiceStudio manifest")

    rows_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in manifest["segments"]:
        rows_by_id[str(row["id"])].append(row)
    shots = story["shots"]
    expected_ids = {shot["id"] for shot in shots}
    found_ids = set(rows_by_id)
    missing = sorted(expected_ids - found_ids)
    extra = sorted(found_ids - expected_ids)
    if missing or extra:
        raise RuntimeError(f"Voice/story segment mismatch; missing={missing}, extra={extra}")

    duration = float(story["duration"])
    total_frames = int(math.ceil(duration * SAMPLE_RATE))
    mix = np.zeros((total_frames, 2), dtype=np.float32)
    cues = []
    report_rows = []
    overlong = []

    with tempfile.TemporaryDirectory(prefix="time-stop-voice-") as tmp:
        tempdir = Path(tmp)
        for index, shot in enumerate(shots, 1):
            sid = shot["id"]
            group = sorted(rows_by_id[sid], key=lambda r: (int(r["chunk_index"]), float(r["start_seconds"])))
            source_start = min(float(r["start_seconds"]) for r in group)
            source_end = max(float(r["end_seconds"]) for r in group)
            src_a = max(0, int(round(source_start * SAMPLE_RATE)))
            src_b = min(len(narration), int(round(source_end * SAMPLE_RATE)))
            segment = narration[src_a:src_b].copy()
            if len(segment) < int(0.12 * SAMPLE_RATE):
                raise RuntimeError(f"{sid} has an empty or implausibly short TTS segment")
            target_start = float(shot["start"]) + START_OFFSET
            slot = float(shot["end"]) - target_start - TAIL_GUARD
            if slot <= 0:
                raise RuntimeError(f"{sid} has no room for narration")
            source_duration = len(segment) / SAMPLE_RATE
            atempo = 1.0
            if source_duration > slot:
                atempo = min(MAX_ATEMPO, source_duration / slot)
                if atempo > 1.001:
                    segment = atempo_wav(segment, atempo, tempdir, index)
            placed_duration = len(segment) / SAMPLE_RATE
            if placed_duration > slot + 0.015:
                overlong.append({"id": sid, "source_duration": round(source_duration, 3), "slot": round(slot, 3), "atempo": round(atempo, 3), "final_duration": round(placed_duration, 3)})
                continue

            fade = min(len(segment) // 4, int(FADE_SECONDS * SAMPLE_RATE))
            if fade > 0:
                segment[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
                segment[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
            start_frame = int(round(target_start * SAMPLE_RATE))
            end_frame = min(total_frames, start_frame + len(segment))
            if start_frame < 0 or end_frame > total_frames or end_frame <= start_frame:
                raise RuntimeError(f"Invalid voice placement for {sid}")
            mono = segment[:end_frame - start_frame]
            mix[start_frame:end_frame, 0] += mono
            mix[start_frame:end_frame, 1] += mono
            cue_end = target_start + len(mono) / SAMPLE_RATE
            cues.append({"start": target_start, "end": cue_end, "text": shot["line"]})
            report_rows.append({
                "shot_id": sid, "video_start": round(target_start, 3),
                "voice_duration": round(len(mono) / SAMPLE_RATE, 3),
                "original_duration": round(source_duration, 3),
                "atempo": round(atempo, 3), "text": shot["line"]
            })
    if overlong:
        raise RuntimeError("Narration could not fit within its shot slots: " + json.dumps(overlong, ensure_ascii=False))

    peak = float(np.max(np.abs(mix)))
    if peak > 0.92:
        mix *= 0.92 / peak
    timeline = project / "timeline"
    timeline.mkdir(parents=True, exist_ok=True)
    voice_path = timeline / "voice.wav"
    sf.write(voice_path, mix, SAMPLE_RATE, subtype="PCM_16")

    srt_lines = []
    vtt_lines = ["WEBVTT", ""]
    for i, cue in enumerate(cues, 1):
        start = ts(cue["start"])
        end = ts(cue["end"])
        srt_lines.extend([str(i), f"{start} --> {end}", cue["text"], ""])
        vtt_lines.extend([f"{ts(cue['start'], True)} --> {ts(cue['end'], True)}", cue["text"].replace("-->", "—>"), ""])
    out = project / "out"
    out.mkdir(parents=True, exist_ok=True)
    (out / "captions.srt").write_text("\n".join(srt_lines), encoding="utf-8")
    (out / "captions.vtt").write_text("\n".join(vtt_lines), encoding="utf-8")
    (out / "voice-placement.json").write_text(json.dumps({
        "status": "passed", "language": manifest["language"], "engine": manifest["engine"],
        "voice_id": manifest["voice_id"], "voice_manifest_job_id": manifest["job_id"],
        "shot_count": len(shots), "placed_segments": len(report_rows),
        "duration_seconds": duration, "audio_sample_rate": SAMPLE_RATE,
        "audio_channels": 2, "voiceover_track": "timeline/voice.wav",
        "source_watermark": audio_meta["watermark"], "source_checks": audio_meta["checks"],
        "segments": report_rows
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "voice-placed", "segments": len(report_rows), "duration": duration,
        "voice_id": manifest["voice_id"], "source_duration": audio_meta["duration_seconds"],
        "timeline_wav_bytes": voice_path.stat().st_size,
        "max_atempo": max(row["atempo"] for row in report_rows)
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
