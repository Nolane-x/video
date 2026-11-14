#!/usr/bin/env python3
"""Frame-exactly replace the early Ottoman bombard passage with the Blender proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

FPS = 240
START_FRAME = 52_982
END_FRAME = 62_376
INSERT_FRAMES = END_FRAME - START_FRAME
SHARD_FRAMES = 57_474
SHARD_BOUNDARY = SHARD_FRAMES
FIRST_SHARD_INSERT = SHARD_BOUNDARY - START_FRAME
SECOND_SHARD_INSERT = INSERT_FRAMES - FIRST_SHARD_INSERT
SECOND_SHARD_SUFFIX = SHARD_FRAMES - SECOND_SHARD_INSERT
STYLE = (
    "FontName=DejaVu Sans,FontSize=44,PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H90000000,BorderStyle=1,Outline=3,Shadow=1,"
    "Alignment=2,MarginV=54"
)


def run(args: list[str], *, capture: bool = True) -> str:
    result = subprocess.run(
        args, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    return result.stdout or ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def probe(path: Path) -> dict:
    return json.loads(run([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams",
        "-show_format", "-of", "json", str(path)
    ]))


def video_stream(meta: dict) -> dict:
    streams = [s for s in meta.get("streams", []) if s.get("codec_type") == "video"]
    if len(streams) != 1:
        raise RuntimeError(f"Expected exactly one video stream, got {len(streams)}")
    return streams[0]


def parse_srt_time(value: str) -> float:
    hours, minutes, rest = value.strip().split(":")
    seconds, millis = rest.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def format_srt_time(value: float) -> str:
    total_ms = max(0, round(value * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def extract_caption_excerpt(source: Path, destination: Path) -> int:
    start = START_FRAME / FPS
    end = END_FRAME / FPS
    text = source.read_text(encoding="utf-8-sig")
    output: list[str] = []
    count = 0
    for block in text.strip().split("\n\n"):
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        a, b = (parse_srt_time(v) for v in lines[1].split("-->"))
        if b <= start or a >= end:
            continue
        a, b = max(a, start), min(b, end)
        if b <= a:
            continue
        count += 1
        output.extend([
            str(count),
            f"{format_srt_time(a - start)} --> {format_srt_time(b - start)}",
            *lines[2:],
            "",
        ])
    if not count:
        raise RuntimeError("No reflowed Squire captions intersect the Blender insert.")
    destination.write_text("\n".join(output), encoding="utf-8")
    return count


def assert_video(path: Path, expected_frames: int, expected_duration: float) -> dict:
    meta = probe(path)
    video = video_stream(meta)
    frames = int(video.get("nb_read_frames") or video.get("nb_frames") or 0)
    duration = float(meta["format"]["duration"])
    if (int(video["width"]), int(video["height"])) != (1920, 1080):
        raise RuntimeError(f"{path.name}: unexpected resolution {video['width']}x{video['height']}")
    if video.get("r_frame_rate") != "240/1" or video.get("avg_frame_rate") != "240/1":
        raise RuntimeError(f"{path.name}: not CFR 240fps")
    if frames != expected_frames:
        raise RuntimeError(f"{path.name}: {frames} frames, expected {expected_frames}")
    if abs(duration - expected_duration) > 0.02:
        raise RuntimeError(f"{path.name}: duration {duration}, expected {expected_duration}")
    run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(path), "-f", "null", "-"])
    return {"frames": frames, "duration_seconds": duration, "width": 1920, "height": 1080}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--hybrid", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    parser.add_argument("--source-run-id", required=True, type=int)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()

    project = args.project.resolve()
    segments = args.segments.resolve()
    hybrid_dir = args.hybrid.resolve()
    output_report = args.output_report.resolve()
    hybrid = hybrid_dir / "constantinople-hybrid-240fps.mp4"
    manifest_path = hybrid_dir / "manifest.json"
    captions_source = project / "story" / "captions.srt"
    for required in (hybrid, manifest_path, captions_source):
        if not required.is_file() or required.stat().st_size == 0:
            raise FileNotFoundError(required)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "RENDERED_HYBRID_240FPS_PROOF_PENDING_HUMAN_REVIEW":
        raise RuntimeError("Blender proof status is not the expected review-pending state.")
    if manifest.get("source_3d_keyframe_fps") != 60:
        raise RuntimeError("Blender insert must be rendered from 60fps source keyframes.")
    if manifest.get("output_fps") != "240/1" or manifest.get("average_fps") != "240/1":
        raise RuntimeError("Blender proof is not constant native-240fps output.")
    if int(manifest.get("decoded_frames", 0)) != INSERT_FRAMES:
        raise RuntimeError("Blender proof frame count does not match the planned insert.")
    source_digest = sha256(hybrid)
    if source_digest != manifest.get("sha256_video"):
        raise RuntimeError("Blender proof SHA-256 does not match its manifest.")
    assert_video(hybrid, INSERT_FRAMES, INSERT_FRAMES / FPS)

    caption_excerpt = hybrid_dir / "insert-captions.srt"
    caption_count = extract_caption_excerpt(captions_source, caption_excerpt)
    filters = run(["ffmpeg", "-hide_banner", "-filters"])
    if "subtitles" not in filters:
        raise RuntimeError("FFmpeg was built without the libass subtitles filter.")
    ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
    captioned = hybrid_dir / "constantinople-hybrid-captioned-240fps.mp4"
    subtitle_path = str(caption_excerpt).replace("\\", "/").replace(":", r"\:")
    vf = f"subtitles=filename='{subtitle_path}':force_style='{STYLE}'"
    run([
        ffmpeg_path, "-hide_banner", "-v", "error", "-y", "-i", str(hybrid),
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "18", "-pix_fmt", "yuv420p", "-r", "240", "-fps_mode", "cfr",
        "-frames:v", str(INSERT_FRAMES), "-video_track_timescale", "240000",
        str(captioned),
    ])
    assert_video(captioned, INSERT_FRAMES, INSERT_FRAMES / FPS)

    original_hashes: dict[str, str] = {}
    replacements: list[dict] = []
    with __import__("tempfile").TemporaryDirectory(prefix="squire-hybrid-splice-") as temp:
        temp_dir = Path(temp)
        original0 = segments / "constantinople-segment-0.mp4"
        original1 = segments / "constantinople-segment-1.mp4"
        for idx, original in enumerate((original0, original1)):
            if not original.is_file():
                raise FileNotFoundError(original)
            assert_video(original, SHARD_FRAMES, SHARD_FRAMES / FPS)
            original_hashes[str(idx)] = sha256(original)

        output0 = temp_dir / "constantinople-segment-0.mp4"
        output1 = temp_dir / "constantinople-segment-1.mp4"
        run([
            ffmpeg_path, "-hide_banner", "-v", "error", "-y",
            "-i", str(original0), "-i", str(captioned),
            "-filter_complex",
            (
                "[0:v]trim=start_frame=0:end_frame=52982,settb=expr=1/240,setpts=N[before];"
                "[1:v]trim=start_frame=0:end_frame=4492,settb=expr=1/240,setpts=N[insert];"
                "[before][insert]concat=n=2:v=1:a=0,format=yuv420p[outv]"
            ),
            "-map", "[outv]", "-an", "-frames:v", str(SHARD_FRAMES),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-maxrate", "48M", "-bufsize", "96M", "-pix_fmt", "yuv420p",
            "-r", "240", "-fps_mode", "cfr", "-video_track_timescale", "240000",
            str(output0),
        ])
        run([
            ffmpeg_path, "-hide_banner", "-v", "error", "-y",
            "-i", str(original1), "-i", str(captioned),
            "-filter_complex",
            (
                "[1:v]trim=start_frame=4492:end_frame=9394,settb=expr=1/240,setpts=N[insert];"
                "[0:v]trim=start_frame=4902:end_frame=57474,settb=expr=1/240,setpts=N[after];"
                "[insert][after]concat=n=2:v=1:a=0,format=yuv420p[outv]"
            ),
            "-map", "[outv]", "-an", "-frames:v", str(SHARD_FRAMES),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-maxrate", "48M", "-bufsize", "96M", "-pix_fmt", "yuv420p",
            "-r", "240", "-fps_mode", "cfr", "-video_track_timescale", "240000",
            str(output1),
        ])
        for idx, replacement in enumerate((output0, output1)):
            verified = assert_video(replacement, SHARD_FRAMES, SHARD_FRAMES / FPS)
            replacements.append({
                "segment": idx,
                **verified,
                "bytes": replacement.stat().st_size,
                "sha256": sha256(replacement),
            })

        # Do not touch the source shards until both replacement files pass QA.
        for idx, replacement in enumerate((output0, output1)):
            destination = segments / f"constantinople-segment-{idx}.mp4"
            os.replace(replacement, destination)
            report_path = segments / f"segment-{idx}-report.json"
            old_report = json.loads(report_path.read_text(encoding="utf-8"))
            old_report["sha256"] = replacements[idx]["sha256"]
            old_report["bytes"] = replacements[idx]["bytes"]
            old_report["visual_insert"] = "Blender 3D great bombard"
            old_report["visual_insert_frame_range"] = [START_FRAME, END_FRAME]
            report_path.write_text(json.dumps(old_report, indent=2) + "\n", encoding="utf-8")

    report = {
        "status": "PASS",
        "hybrid_source_run": args.source_run_id,
        "hybrid_source_sha": args.source_sha,
        "hybrid_manifest": manifest,
        "hybrid_video_sha256": source_digest,
        "caption_source": "Squire reflowed project/story/captions.srt",
        "caption_cues": caption_count,
        "master_frame_range": [START_FRAME, END_FRAME],
        "master_time_range_seconds": [START_FRAME / FPS, END_FRAME / FPS],
        "fps": FPS,
        "frames": INSERT_FRAMES,
        "reencoded_shards": [0, 1],
        "original_shard_sha256": original_hashes,
        "replacement_shards": replacements,
        "audio_policy": "Original Squire/VoiceStudio master mix retained; hybrid proof audio discarded.",
        "artistic_signoff": "pending full human watch at normal speed",
    }
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("3D insert splice PASS:", report["master_frame_range"], "frames;",
          "replaced shards", [r["sha256"] for r in replacements])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
