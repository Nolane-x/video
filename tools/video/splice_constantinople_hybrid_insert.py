#!/usr/bin/env python3
"""Frame-exactly replace the early Ottoman bombard passage with the Blender proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
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


def backup_original_file(source: Path, destination: Path) -> str:
    """Preserve a rollback copy without duplicating multi-GB video files.

    The staging directory is deliberately created under the segment directory,
    so source and backup share a filesystem. A hard link is therefore the
    preferred zero-copy backup. Fall back to a byte copy only when the
    filesystem does not support hard links.
    """
    try:
        os.link(source, destination)
        if not os.path.samefile(source, destination):
            raise RuntimeError(f"Rollback backup is not the original inode: {destination}")
        return "hardlink"
    except OSError as exc:
        import errno
        if exc.errno not in {
            errno.EXDEV, errno.EPERM, errno.EACCES,
            getattr(errno, "EOPNOTSUPP", errno.EPERM),
            getattr(errno, "ENOTSUP", errno.EPERM),
            errno.ENOSYS,
        }:
            raise
        shutil.copy2(source, destination)
        if source.stat().st_size != destination.stat().st_size:
            raise RuntimeError(f"Rollback backup size mismatch: {destination}")
        return "copy"


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
    for block in re.split(r"\r?\n[ \t]*\r?\n", text.strip()):
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


def assert_video(
    path: Path,
    expected_frames: int,
    expected_duration: float,
    *,
    allow_full_range_input: bool = False,
    decode: bool = True,
) -> dict:
    meta = probe(path)
    video = video_stream(meta)
    if video.get("codec_name") != "h264":
        raise RuntimeError(f"{path.name}: expected H.264 video, got {video.get('codec_name')}")
    allowed_formats = {"yuv420p"}
    if allow_full_range_input:
        # Squire can emit yuvj420p (full-range YUV). It is accepted only as
        # an input format; final shards are normalized to limited-range BT.709.
        allowed_formats.add("yuvj420p")
    if video.get("pix_fmt") not in allowed_formats:
        raise RuntimeError(
            f"{path.name}: unsupported pixel format {video.get('pix_fmt')}; "
            f"expected one of {sorted(allowed_formats)}"
        )
    if not allow_full_range_input and video.get("color_range") in {"pc", "jpeg"}:
        raise RuntimeError(f"{path.name}: output remained full-range ({video.get('color_range')})")
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
    if decode:
        run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(path), "-f", "null", "-"])
    return {
        "frames": frames,
        "duration_seconds": duration,
        "width": 1920,
        "height": 1080,
        "codec": video.get("codec_name"),
        "pixel_format": video.get("pix_fmt"),
        "fps": FPS,
    }


INSERT_SOUND_CUES = (
    {"t": 239.510, "name": "cannon_fire", "gain": -4},
    {"t": 247.010, "name": "siege_impact", "gain": -6},
)


def validate_source_identity(run_id: int, source_sha: str) -> None:
    if int(run_id) <= 0:
        raise ValueError("The GitHub Actions proof run ID must be a positive integer.")
    if not re.fullmatch(r"[0-9a-f]{40}", str(source_sha).lower()):
        raise ValueError("The Blender proof source SHA must be exactly 40 hexadecimal characters.")


def validate_cue_timeline(duration_seconds: float) -> None:
    required_end = max(float(cue["t"]) for cue in INSERT_SOUND_CUES) + 2.0
    if float(duration_seconds) + 1e-6 < required_end:
        raise ValueError(
            f"The Squire project timeline ends at {duration_seconds:.3f}s, "
            f"before the bombard sound cues and tails finish at {required_end:.3f}s."
        )


def validate_hybrid_manifest_identity(
    manifest: dict, expected_run_id: int, expected_sha: str, video_path: Path
) -> None:
    """Bind the media bytes to the exact run and source revision selected by CI."""
    if str(manifest.get("source_run_id", "")) != str(expected_run_id):
        raise RuntimeError(
            "Blender proof run ID does not match the run selected by the master resolver."
        )
    if str(manifest.get("source_commit_sha", "")).lower() != str(expected_sha).lower():
        raise RuntimeError(
            "Blender proof source commit SHA does not match the run selected by the master resolver."
        )
    declared_bytes = manifest.get("video_bytes")
    if declared_bytes is None or int(declared_bytes) != video_path.stat().st_size:
        raise RuntimeError("Blender proof byte count does not match its manifest.")


def validate_existing_shards(segments: Path) -> list[dict]:
    """Validate both source shards and their reports before changing either file."""
    reports: list[dict] = []
    for index in range(4):
        video_path = segments / f"constantinople-segment-{index}.mp4"
        report_path = segments / f"segment-{index}-report.json"
        if not video_path.is_file() or not report_path.is_file():
            raise FileNotFoundError(video_path if not video_path.is_file() else report_path)
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Segment {index} report is missing or invalid JSON.") from exc
        if report.get("status") != "pass":
            raise RuntimeError(f"Segment {index} report is not a passing source report.")
        if int(report.get("segment", -1)) != index:
            raise RuntimeError(f"Segment {index} report identifies the wrong shard.")
        if int(report.get("frames", 0)) != SHARD_FRAMES or int(report.get("fps", 0)) != FPS:
            raise RuntimeError(f"Segment {index} report has the wrong frame count or frame rate.")
        actual_sha = sha256(video_path)
        if report.get("sha256") != actual_sha:
            raise RuntimeError(f"Segment {index} report SHA-256 does not match its source video.")
        if "bytes" in report and int(report["bytes"]) != video_path.stat().st_size:
            raise RuntimeError(f"Segment {index} report byte count does not match its source video.")
        assert_video(
            video_path,
            SHARD_FRAMES,
            SHARD_FRAMES / FPS,
            allow_full_range_input=True,
            decode=False,
        )
        reports.append(report)
    return reports


def normalize_to_tv_range(
    source: Path,
    destination: Path,
    expected_frames: int,
    expected_duration: float,
) -> dict:
    """Re-encode one shard to limited-range BT.709 without changing frame timing."""
    vf = "scale=in_range=auto:out_range=tv:out_color_matrix=bt709,format=yuv420p"
    run([
        shutil.which("ffmpeg") or "ffmpeg",
        "-hide_banner", "-v", "error", "-y", "-i", str(source),
        "-vf", vf, "-an", "-frames:v", str(expected_frames),
        "-c:v", "libx264", "-preset", "slow", "-tune", "animation",
        "-crf", "18", "-maxrate", "48M", "-bufsize", "96M",
        "-pix_fmt", "yuv420p", "-color_range", "tv",
        "-r", "240", "-fps_mode", "cfr", "-video_track_timescale", "240000",
        str(destination),
    ])
    return assert_video(destination, expected_frames, expected_duration)


def add_insert_sound_cues(project: Path) -> dict:
    """Add the two CC0 bombard cues to the original Squire story mix timeline."""
    kit = project.parents[1]
    manifest_path = project / "story" / "AUDIO-SOURCE-MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = {row["alias"]: row for row in manifest.get("assets", [])}
    verified_assets = {}
    for alias in ("cannon_fire", "siege_impact"):
        row = rows.get(alias)
        if not row or row.get("license") != "CC0-1.0":
            raise RuntimeError(f"Missing exact CC0 provenance for SFX alias: {alias}")
        source = kit / row["converted_path"]
        if not source.is_file() or sha256(source) != row["converted_sha256"]:
            raise RuntimeError(f"Converted SFX checksum mismatch: {alias}")
        verified_assets[alias] = {
            "alias": alias,
            "license": row["license"],
            "source": row.get("source"),
            "source_url": row.get("source_url"),
            "converted_sha256": row["converted_sha256"],
            "human_auditioned": row.get("human_auditioned", False),
            "approved_for_final_mix": row.get("approved_for_final_mix", False),
        }

    story_path = project / "story" / "shots.json"
    story = json.loads(story_path.read_text(encoding="utf-8"))
    shots = story.get("shots", [])
    duration = story.get("duration")
    if duration is None and shots:
        duration = max(float(shot.get("end", 0)) for shot in shots)
    if duration is None:
        duration = 0.0
    validate_cue_timeline(float(duration))
    cues = [dict(cue) for cue in INSERT_SOUND_CUES]
    existing = list(story.get("sfx", []))
    for cue in cues:
        matches = [
            item for item in existing
            if item.get("name") == cue["name"]
            and abs(float(item.get("t", -999)) - cue["t"]) < 0.02
        ]
        if len(matches) > 1:
            raise RuntimeError(f"Duplicate bombard sound cue already exists: {cue['name']}")
        if not matches:
            existing.append(cue)
    story["sfx"] = existing
    story_path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"cues": cues, "assets": verified_assets}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--hybrid", type=Path, required=True)
    parser.add_argument("--output-report", type=Path, required=True)
    parser.add_argument("--source-run-id", required=True, type=int)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()

    validate_source_identity(args.source_run_id, args.source_sha)
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
    validate_hybrid_manifest_identity(
        manifest, args.source_run_id, args.source_sha, hybrid
    )
    if manifest.get("status") != "RENDERED_HYBRID_240FPS_PROOF_PENDING_HUMAN_REVIEW":
        raise RuntimeError("Blender proof status is not the expected review-pending state.")
    if manifest.get("source_3d_keyframe_fps") != 30:
        raise RuntimeError("Blender insert must be rendered from 30fps source keyframes.")
    if manifest.get("output_fps") != "240/1" or manifest.get("average_fps") != "240/1":
        raise RuntimeError("Blender proof is not constant native-240fps output.")
    if int(manifest.get("decoded_frames", 0)) != INSERT_FRAMES:
        raise RuntimeError("Blender proof frame count does not match the planned insert.")
    source_digest = sha256(hybrid)
    if source_digest != manifest.get("sha256_video"):
        raise RuntimeError("Blender proof SHA-256 does not match its manifest.")
    assert_video(hybrid, INSERT_FRAMES, INSERT_FRAMES / FPS)
    # Read, hash, decode and validate BOTH source shards before mutating the
    # story timeline or either shard.
    existing_reports = validate_existing_shards(segments)
    audio_insert = add_insert_sound_cues(project)

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
        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "slow", "-tune", "animation",
        "-crf", "18", "-maxrate", "48M", "-bufsize", "96M", "-pix_fmt", "yuv420p",
        "-r", "240", "-fps_mode", "cfr",
        "-frames:v", str(INSERT_FRAMES), "-video_track_timescale", "240000",
        str(captioned),
    ])
    assert_video(captioned, INSERT_FRAMES, INSERT_FRAMES / FPS)

    original_hashes: dict[str, str] = {
        str(index): existing_reports[index]["sha256"] for index in (0, 1)
    }
    replacements: list[dict] = []
    transaction_id = f"{args.source_run_id}-{args.source_sha.lower()[:12]}"
    source_paths = [
        segments / f"constantinople-segment-{index}.mp4"
        for index in range(4)
    ]
    source_report_paths = [
        segments / f"segment-{index}-report.json"
        for index in range(4)
    ]

    # Stage output beside the source shards so every os.replace stays on the
    # same filesystem. Keep backups until both videos AND both reports pass
    # their post-commit checks.
    with tempfile.TemporaryDirectory(
        prefix="squire-hybrid-splice-", dir=str(segments)
    ) as temp:
        temp_dir = Path(temp)
        output0 = temp_dir / "constantinople-segment-0.mp4"
        output1 = temp_dir / "constantinople-segment-1.mp4"
        output2 = temp_dir / "constantinople-segment-2.mp4"
        output3 = temp_dir / "constantinople-segment-3.mp4"
        staged_videos = (output0, output1, output2, output3)

        run([
            ffmpeg_path, "-hide_banner", "-v", "error", "-y",
            "-i", str(source_paths[0]), "-i", str(captioned),
            "-filter_complex",
            (
                f"[0:v]scale=in_range=auto:out_range=tv:out_color_matrix=bt709,"
                f"trim=start_frame=0:end_frame={START_FRAME},settb=expr=1/240,setpts=N[before];"
                f"[1:v]scale=in_range=auto:out_range=tv:out_color_matrix=bt709,"
                f"trim=start_frame=0:end_frame={FIRST_SHARD_INSERT},settb=expr=1/240,setpts=N[insert];"
                "[before][insert]concat=n=2:v=1:a=0,format=yuv420p[outv]"
            ),
            "-map", "[outv]", "-an", "-frames:v", str(SHARD_FRAMES),
            "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "18",
            "-maxrate", "48M", "-bufsize", "96M", "-pix_fmt", "yuv420p", "-color_range", "tv",
            "-r", "240", "-fps_mode", "cfr", "-video_track_timescale", "240000",
            str(output0),
        ])
        run([
            ffmpeg_path, "-hide_banner", "-v", "error", "-y",
            "-i", str(source_paths[1]), "-i", str(captioned),
            "-filter_complex",
            (
                f"[1:v]scale=in_range=auto:out_range=tv:out_color_matrix=bt709,"
                f"trim=start_frame={FIRST_SHARD_INSERT}:end_frame={INSERT_FRAMES},settb=expr=1/240,setpts=N[insert];"
                f"[0:v]scale=in_range=auto:out_range=tv:out_color_matrix=bt709,"
                f"trim=start_frame={SECOND_SHARD_INSERT}:end_frame={SHARD_FRAMES},settb=expr=1/240,setpts=N[after];"
                "[insert][after]concat=n=2:v=1:a=0,format=yuv420p[outv]"
            ),
            "-map", "[outv]", "-an", "-frames:v", str(SHARD_FRAMES),
            "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "18",
            "-maxrate", "48M", "-bufsize", "96M", "-pix_fmt", "yuv420p", "-color_range", "tv",
            "-r", "240", "-fps_mode", "cfr", "-video_track_timescale", "240000",
            str(output1),
        ])

        # The insert occupies shards 0 and 1; untouched shards 2 and 3 still
        # need the same limited-range colour contract before stream-copy concat.
        normalizations: list[dict] = []
        for index in (2, 3):
            verified = normalize_to_tv_range(
                source_paths[index], staged_videos[index],
                SHARD_FRAMES, SHARD_FRAMES / FPS,
            )
            normalizations.append({
                "segment": index,
                **verified,
                "bytes": staged_videos[index].stat().st_size,
                "sha256": sha256(staged_videos[index]),
                "source_pixel_format": probe(source_paths[index])["streams"][0].get("pix_fmt"),
                "target_pixel_format": "yuv420p",
                "target_color_range": "tv",
            })

        staged_reports: list[Path] = []
        for index, replacement in enumerate(staged_videos):
            verified = assert_video(replacement, SHARD_FRAMES, SHARD_FRAMES / FPS)
            digest = sha256(replacement)
            updated_report = dict(existing_reports[index])
            updated_report.update({
                "sha256": digest,
                "bytes": replacement.stat().st_size,
                "pixel_format": verified["pixel_format"],
                "color_range": "tv",
                "color_normalization": "auto-to-limited-range-bt709",
                "transaction_id": transaction_id,
            })
            if index in (0, 1):
                updated_report.update({
                    "visual_insert": "Blender 3D great bombard",
                    "visual_insert_frame_range": [START_FRAME, END_FRAME - 1],
                    "visual_insert_frame_range_convention": "zero-based, inclusive",
                    "hybrid_source_run_id": args.source_run_id,
                    "hybrid_source_sha": args.source_sha.lower(),
                })
                replacements.append({
                    "segment": index,
                    **verified,
                    "bytes": replacement.stat().st_size,
                    "sha256": digest,
                })
            staged_report = temp_dir / f"segment-{index}-report.json"
            staged_report.write_text(
                json.dumps(updated_report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            staged_reports.append(staged_report)

        backup_dir = temp_dir / "backups"
        backup_dir.mkdir()
        commit_items: list[tuple[Path, Path, Path]] = []
        for index in range(4):
            backup_video = backup_dir / f"segment-{index}.mp4.original"
            backup_report = backup_dir / f"segment-{index}.json.original"
            media_backup_mode = backup_original_file(source_paths[index], backup_video)
            backup_original_file(source_report_paths[index], backup_report)
            if media_backup_mode not in {"hardlink", "copy"}:
                raise RuntimeError(f"Unknown rollback backup mode for segment {index}.")
            commit_items.extend([
                (staged_videos[index], source_paths[index], backup_video),
                (staged_reports[index], source_report_paths[index], backup_report),
            ])

        try:
            for staged, destination, _backup in commit_items:
                os.replace(staged, destination)

            # Verify the committed files, not merely the temporary candidates.
            for index in range(4):
                committed = assert_video(
                    source_paths[index], SHARD_FRAMES, SHARD_FRAMES / FPS
                )
                committed_report = json.loads(
                    source_report_paths[index].read_text(encoding="utf-8")
                )
                committed_sha = sha256(source_paths[index])
                if committed_report.get("sha256") != committed_sha:
                    raise RuntimeError(
                        f"Committed segment {index} report SHA-256 mismatch."
                    )
                if committed_report.get("transaction_id") != transaction_id:
                    raise RuntimeError(
                        f"Committed segment {index} belongs to another transaction."
                    )
                if committed["frames"] != SHARD_FRAMES:
                    raise RuntimeError(f"Committed segment {index} frame count changed.")
        except Exception as commit_error:
            rollback_errors = []
            rollback_dir = backup_dir / "rollback"
            rollback_dir.mkdir(exist_ok=True)
            for index, (_staged, destination, backup) in enumerate(commit_items):
                try:
                    restore_path = rollback_dir / f"{index}-{destination.name}"
                    shutil.copy2(backup, restore_path)
                    os.replace(restore_path, destination)
                except Exception as rollback_error:
                    rollback_errors.append(
                        f"{destination.name}: {type(rollback_error).__name__}: {rollback_error}"
                    )
            if rollback_errors:
                raise RuntimeError(
                    "Hybrid splice commit failed and rollback was incomplete: "
                    + "; ".join(rollback_errors)
                ) from commit_error
            raise RuntimeError(
                "Hybrid splice commit failed; all four source shards and reports were restored."
            ) from commit_error
    report = {
        "status": "PASS",
        "hybrid_source_run": args.source_run_id,
        "hybrid_source_sha": args.source_sha.lower(),
        "source_attestation": {
            "provider": "GitHub Actions",
            "branch": "cinematic/constantinople-hybrid-240fps",
            "run_id": args.source_run_id,
            "head_sha": args.source_sha.lower(),
            "selection_contract": (
                "The prepare job selected a successful run whose head SHA matched "
                "the current hybrid branch and whose exact proof artifact was not expired."
            ),
        },
        "transaction_id": transaction_id,
        "hybrid_manifest": manifest,
        "hybrid_video_sha256": source_digest,
        "caption_source": "Squire reflowed project/story/captions.srt",
        "caption_cues": caption_count,
        "master_frame_range": [START_FRAME, END_FRAME],
        "master_frame_range_convention": "zero-based, end-exclusive",
        "master_frame_range_inclusive": [START_FRAME, END_FRAME - 1],
        "master_time_range_seconds": [START_FRAME / FPS, END_FRAME / FPS],
        "fps": FPS,
        "frames": INSERT_FRAMES,
        "reencoded_shards": [0, 1],
        "color_normalized_shards": [0, 1, 2, 3],
        "range_normalizations": normalizations,
        "original_shard_sha256": original_hashes,
        "replacement_shards": replacements,
        "audio_policy": "Original VoiceStudio narration and recorded score retained; verified CC0 cannon and wall-impact cues added to the Squire mix. Hybrid proof audio discarded.",
        "audio_effects": audio_insert,
        "artistic_signoff": "pending full human watch at normal speed",
    }
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("3D insert splice PASS:", report["master_frame_range"], "frames;",
          "replaced shards", [r["sha256"] for r in replacements])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
