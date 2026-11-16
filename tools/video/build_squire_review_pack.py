#!/usr/bin/env python3
"""Build a compact, normal-speed human-review package from a verified Squire master."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

FPS = 240
EXPECTED_FRAMES = 229896
EXPECTED_DURATION = 957.9
TILE_COLUMNS = 4
TILE_ROWS = 4
SAMPLES_PER_SECOND = 1
MASTER_NAME = "53 Days to the End of an Empire.mp4"
METADATA_FILES = (
    "QA-REPORT.json",
    "QA-REPORT.md",
    "thumbnail.png",
    "captions.srt",
    "captions.vtt",
    "CAPTION-REFLOW-REPORT.json",
    "shots.json",
    "config.json",
    "01-SCRIPT.md",
    "story-bible.md",
    "AUDIO-SOURCE-MANIFEST.json",
    "voice-manifest.json",
    "voice-selection.json",
    "voice-source-manifest.json",
    "alignment-report.json",
    "HYBRID-INSERT-REPORT.json",
    "SHA256SUMS.txt",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_source_identity(run_id: int, artifact_id: int, artifact_name: str, source_sha: str) -> None:
    if run_id <= 0 or artifact_id <= 0:
        raise ValueError("Master run and artifact IDs must be positive integers.")
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise ValueError("Source commit must be a full 40-character SHA-1.")
    if artifact_name != f"squire-constantinople-1453-redesign-240fps-{run_id}":
        raise ValueError("Master artifact name does not match the selected run ID.")


def validate_master_report(report: dict[str, Any], video_path: Path) -> dict[str, Any]:
    """Refuse to build a review pack from a master outside the verified delivery contract."""
    required = {
        "status": "technical_pass",
        "fps": FPS,
        "frames": EXPECTED_FRAMES,
        "resolution": "1920x1080",
    }
    for key, expected in required.items():
        if report.get(key) != expected:
            raise ValueError(f"Master QA field {key!r} must be {expected!r}, got {report.get(key)!r}.")

    duration = float(report.get("duration_seconds", 0))
    if abs(duration - EXPECTED_DURATION) > 1.5:
        raise ValueError(f"Master duration is outside the expected range: {duration:.3f}s.")
    if not video_path.is_file() or video_path.stat().st_size <= 0:
        raise ValueError(f"Master video is missing or empty: {video_path}")

    expected_bytes = report.get("final_bytes")
    if expected_bytes is not None and int(expected_bytes) != video_path.stat().st_size:
        raise ValueError(
            f"Master byte-count mismatch: QA={expected_bytes}, file={video_path.stat().st_size}."
        )
    expected_hash = report.get("final_sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise ValueError("Master QA report does not contain a valid final_sha256.")
    actual_hash = sha256_file(video_path)
    if actual_hash != expected_hash:
        raise ValueError(f"Master SHA-256 mismatch: QA={expected_hash}, file={actual_hash}.")

    # Check the actual delivered media as well as its signed-by-hash QA metadata.
    probe = ffprobe_json(video_path)
    video_streams = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"]
    if not video_streams or not audio_streams:
        raise ValueError("Master container must contain both video and audio streams.")
    video_stream = video_streams[0]
    audio_stream = audio_streams[0]
    if (int(video_stream.get("width", 0)), int(video_stream.get("height", 0))) != (1920, 1080):
        raise ValueError("Actual master stream is not 1920x1080.")
    if video_stream.get("r_frame_rate") != "240/1":
        raise ValueError(f"Actual master nominal rate is not 240/1: {video_stream.get('r_frame_rate')}.")
    try:
        average_rate = float(Fraction(video_stream.get("avg_frame_rate", "0/1")))
    except (ValueError, ZeroDivisionError):
        average_rate = 0.0
    if abs(average_rate - FPS) > 0.01:
        raise ValueError(f"Actual master average rate is not 240fps: {average_rate}.")
    if int(video_stream.get("nb_frames", 0)) != EXPECTED_FRAMES:
        raise ValueError(f"Actual master frame count is not {EXPECTED_FRAMES}: {video_stream.get('nb_frames')}.")
    if audio_stream.get("codec_name") != "aac" or int(audio_stream.get("sample_rate", 0)) != 48000 or int(audio_stream.get("channels", 0)) != 2:
        raise ValueError("Master audio must be AAC stereo at 48kHz.")
    actual_duration = float(probe.get("format", {}).get("duration", 0))
    if abs(actual_duration - duration) > 1.0:
        raise ValueError(f"Actual master duration differs from QA report: {actual_duration:.3f}s vs {duration:.3f}s.")

    return {
        "duration_seconds": duration,
        "resolution": report["resolution"],
        "fps": report["fps"],
        "frames": report["frames"],
        "final_bytes": video_path.stat().st_size,
        "final_sha256": actual_hash,
        "artistic_signoff": report.get("artistic_signoff", "pending human review"),
    }


def timestamp_to_seconds(value: str) -> float:
    match = re.fullmatch(r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{1,3})", value.strip())
    if not match:
        raise ValueError(f"Unsupported subtitle timestamp: {value!r}")
    hours, minutes, seconds, fraction = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(fraction.ljust(3, "0")) / 1000


def parse_srt(text: str) -> list[dict[str, Any]]:
    """Parse SRT cue times/text without changing source timing or wording."""
    cues: list[dict[str, Any]] = []
    for block in re.split(r"\r?\n\s*\r?\n", text.strip()):
        lines = [line.strip("\ufeff\r") for line in block.splitlines() if line.strip()]
        time_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if time_index is None:
            continue
        left, right = (part.strip().split()[0] for part in lines[time_index].split("-->", 1))
        start = timestamp_to_seconds(left)
        end = timestamp_to_seconds(right)
        if end <= start:
            raise ValueError(f"Subtitle cue ends before it starts: {lines[time_index]}")
        cue_text = " ".join(re.sub(r"<[^>]+>", "", line).strip() for line in lines[time_index + 1 :])
        if cue_text:
            cues.append({"start": start, "end": end, "text": cue_text})
    return cues


def build_shot_index(shots: list[dict[str, Any]], cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach all overlapping caption cues to each authored shot for timecoded review."""
    rows: list[dict[str, Any]] = []
    for shot in shots:
        start = float(shot["start"])
        end = float(shot["end"])
        if end <= start:
            raise ValueError(f"Invalid shot interval for {shot.get('id', '<unknown>')}: {start}–{end}")
        overlapping = [
            cue["text"] for cue in cues
            if float(cue["start"]) < end and float(cue["end"]) > start
        ]
        args = shot.get("args") or {}
        rows.append({
            "shot_id": str(shot.get("id") or shot.get("shot_id") or ""),
            "start_seconds": round(start, 3),
            "end_seconds": round(end, 3),
            "duration_seconds": round(end - start, 3),
            "template": str(shot.get("tpl") or ""),
            "beat": str(args.get("beat") or args.get("moment") or args.get("variant") or ""),
            "caption": " | ".join(dict.fromkeys(overlapping)),
        })
    return rows


def expected_contact_sheets(duration_seconds: float) -> int:
    samples = math.ceil(max(0.0, duration_seconds) * SAMPLES_PER_SECOND)
    per_sheet = TILE_COLUMNS * TILE_ROWS
    return max(1, math.ceil(samples / per_sheet))


def run(command: list[str]) -> str:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def ffprobe_json(video_path: Path) -> dict[str, Any]:
    output = run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video_path)
    ])
    return json.loads(output)


def render_review_proxy(video: Path, output: Path) -> dict[str, Any]:
    """Produce a full-length 720p/30fps review copy; never alter the 240fps source."""
    run([
        "ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(video),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", "fps=30,scale=1280:720:flags=lanczos",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-maxrate", "5M", "-bufsize", "10M", "-pix_fmt", "yuv420p",
        "-r", "30", "-fps_mode", "cfr",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", str(output),
    ])
    probe = ffprobe_json(output)
    videos = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "video"]
    audios = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"]
    if not videos or not audios:
        raise RuntimeError("Review proxy must contain both video and audio streams.")
    stream = videos[0]
    if (int(stream.get("width", 0)), int(stream.get("height", 0))) != (1280, 720):
        raise RuntimeError(f"Review proxy dimensions are not 1280x720: {stream.get('width')}x{stream.get('height')}.")
    if stream.get("r_frame_rate") != "30/1":
        raise RuntimeError(f"Review proxy is not CFR 30fps: {stream.get('r_frame_rate')}.")
    if int(audios[0].get("sample_rate", 0)) != 48000 or int(audios[0].get("channels", 0)) != 2:
        raise RuntimeError("Review proxy audio must be stereo 48kHz.")
    source_duration = float(ffprobe_json(video).get("format", {}).get("duration", 0))
    proxy_duration = float(probe.get("format", {}).get("duration", 0))
    if abs(source_duration - proxy_duration) > 1.0:
        raise RuntimeError(f"Review proxy duration drifted: source={source_duration}, proxy={proxy_duration}.")
    return {
        "path": output.name,
        "resolution": "1280x720",
        "fps": 30,
        "duration_seconds": round(proxy_duration, 3),
        "bytes": output.stat().st_size,
        "audio": "AAC stereo 48kHz",
    }


def render_full_audio(video: Path, output: Path) -> dict[str, Any]:
    run([
        "ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(video),
        "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", str(output),
    ])
    return {"path": output.name, "bytes": output.stat().st_size, "duration_seconds": round(float(ffprobe_json(video)["format"]["duration"]), 3)}


def render_contact_sheets(video: Path, output_dir: Path, duration_seconds: float) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = output_dir / "sheet-%03d.jpg"
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    video_filter = (
        f"fps={SAMPLES_PER_SECOND},scale=384:216:flags=lanczos,"
        f"drawtext=fontfile={font}:text='%{{pts\\:hms}}':x=8:y=8:fontsize=16:"
        "fontcolor=white:borderw=2:bordercolor=black,"
        f"tile={TILE_COLUMNS}x{TILE_ROWS}:nb_frames={TILE_COLUMNS*TILE_ROWS}:padding=6:margin=8:color=0x202020"
    )
    run([
        "ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(video),
        "-map", "0:v:0", "-vf", video_filter, "-fps_mode", "vfr", "-q:v", "4", str(pattern),
    ])
    sheets = sorted(path.name for path in output_dir.glob("sheet-*.jpg"))
    minimum = expected_contact_sheets(duration_seconds) - 1  # FFmpeg may omit a final partial tile.
    if len(sheets) < max(1, minimum):
        raise RuntimeError(f"Incomplete contact sheets: {len(sheets)} created, at least {max(1, minimum)} expected.")
    return sheets


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def copy_metadata(source: Path, output: Path) -> list[str]:
    copied: list[str] = []
    for name in METADATA_FILES:
        item = source / name
        if item.is_file():
            output_name = "MASTER-SOURCE-SHA256SUMS.txt" if name == "SHA256SUMS.txt" else name
            shutil.copy2(item, output / output_name)
            copied.append(output_name)
    return copied


def build_review_pack(source: Path, output: Path, run_id: int, artifact_name: str, source_sha: str, artifact_id: int) -> dict[str, Any]:
    validate_source_identity(run_id, artifact_id, artifact_name, source_sha)

    video = source / MASTER_NAME
    report_path = source / "QA-REPORT.json"
    shots_path = source / "shots.json"
    srt_path = source / "captions.srt"
    for required in (video, report_path, shots_path, srt_path, source / "captions.vtt", source / "thumbnail.png"):
        if not required.is_file():
            raise FileNotFoundError(f"Required source artifact file is missing: {required.name}")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    media = validate_master_report(report, video)
    story = json.loads(shots_path.read_text(encoding="utf-8"))
    shots = story.get("shots") or []
    if not shots:
        raise ValueError("Shotbook contains no timed shots; cannot create a review index.")
    cues = parse_srt(srt_path.read_text(encoding="utf-8-sig"))
    if not cues:
        raise ValueError("Caption sidecar contains no parseable cues.")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copied = copy_metadata(source, output)
    proxy = render_review_proxy(video, output / "FULL-FILM-REVIEW-720p30.mp4")
    audio = render_full_audio(video, output / "FULL-AUDIO-REVIEW.mp3")
    sheets = render_contact_sheets(video, output / "contact-sheets", media["duration_seconds"])
    shot_rows = build_shot_index(shots, cues)
    write_csv(output / "SHOT-INDEX.csv", shot_rows, [
        "shot_id", "start_seconds", "end_seconds", "duration_seconds", "template", "beat", "caption"
    ])
    write_csv(output / "REVIEW-LOG-TEMPLATE.csv", [], [
        "timecode", "shot_id", "category", "severity", "issue", "proposed_fix", "status"
    ])

    audit = {
        "status": "review_pack_ready",
        "source_workflow_run_id": run_id,
        "source_artifact_id": artifact_id,
        "source_artifact_name": artifact_name,
        "source_commit_sha": source_sha,
        "master": media,
        "review_proxy": proxy,
        "full_audio_review": audio,
        "contact_sheet_count": len(sheets),
        "contact_sheet_sample_rate_fps": SAMPLES_PER_SECOND,
        "shot_count": len(shot_rows),
        "caption_cue_count": len(cues),
        "copied_metadata_files": copied,
        "human_artistic_signoff": "pending complete human watch/listen",
        "limitations": [
            "The 30fps proxy is for normal-speed review only; the verified 240fps master is unchanged.",
            "One frame per second contact sheets are navigation aids, not a substitute for watching motion.",
            "Automated technical QA and generated review materials do not constitute artistic approval.",
            "Review the entire proxy and complete audio track; record timecoded findings in REVIEW-LOG-TEMPLATE.csv.",
        ],
    }
    (output / "AUDIT-README.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "AUDIT-README.md").write_text(
        "# Constantinople 1453 — full-length human review package\n\n"
        f"- Source master run: [{run_id}](https://github.com/Nolane-x/video/actions/runs/{run_id})\n"
        f"- Source artifact: {artifact_name} (artifact ID {artifact_id})\n"
        f"- Source commit: {source_sha}\n"
        f"- Master: 1920×1080 / native 240fps / {media['frames']:,} frames / {media['duration_seconds']:.1f}s\n"
        f"- Master SHA-256: {media['final_sha256']}\n"
        f"- Review proxy: FULL-FILM-REVIEW-720p30.mp4 (full-length, 720p30, AAC stereo)\n"
        f"- Full audio: FULL-AUDIO-REVIEW.mp3\n"
        f"- Contact sheets: {len(sheets)} sheets at one sample per second\n"
        f"- Shot index: {len(shot_rows)} timecoded shots with overlapping subtitle text\n"
        "\n## Review order\n\n"
        "1. Watch the complete review proxy at normal speed.\n"
        "2. Use the contact sheets and SHOT-INDEX.csv to locate weak or confusing shots.\n"
        "3. Listen to FULL-AUDIO-REVIEW.mp3 from beginning to end.\n"
        "4. Record timecode, shot ID, category, severity and proposed correction in REVIEW-LOG-TEMPLATE.csv.\n"
        "5. Do not mark the master approved until historical accuracy, image quality, captions, continuity and audio are reviewed.\n"
        "\n**Important:** this package does not replace or re-encode the native-240fps delivery master. "
        "The artistic sign-off remains pending until a human completes the full watch/listen.\n",
        encoding="utf-8",
    )

    sums: list[str] = []
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item.name != "SHA256SUMS-REVIEW.txt"):
        sums.append(f"{sha256_file(path)}  {path.relative_to(output).as_posix()}")
    (output / "SHA256SUMS-REVIEW.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="Directory containing the downloaded master artifact")
    parser.add_argument("--output", required=True, type=Path, help="Review-pack output directory")
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--artifact-id", required=True, type=int)
    parser.add_argument("--artifact-name", required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    audit = build_review_pack(args.source, args.output, args.run_id, args.artifact_name, args.source_sha, args.artifact_id)
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
