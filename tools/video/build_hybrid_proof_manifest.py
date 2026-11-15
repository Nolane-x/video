#!/usr/bin/env python3
"""Create a frame-attested manifest for the Constantinople hybrid 240fps proof."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED_FRAMES = 9394
EXPECTED_DURATION = EXPECTED_FRAMES / 240
EXPECTED_SIZE = (1920, 1080)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def build_manifest(
    *,
    video_path: Path,
    metadata_path: Path,
    voice_manifest_path: Path,
    score_path: Path,
    cannon_fire_path: Path,
    cannon_impact_path: Path,
    source_run_id: str,
    source_sha: str,
) -> dict[str, Any]:
    paths = {
        "video": video_path,
        "metadata": metadata_path,
        "voice manifest": voice_manifest_path,
        "score": score_path,
        "cannon fire": cannon_fire_path,
        "cannon impact": cannon_impact_path,
    }
    for label, path in paths.items():
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Missing or empty {label}: {path}")

    metadata = load_json(metadata_path)
    streams = metadata.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if video is None or audio is None:
        raise ValueError("Hybrid proof must contain both video and audio streams")

    frames = int(video.get("nb_read_frames") or video.get("nb_frames") or 0)
    if frames != EXPECTED_FRAMES:
        raise ValueError(f"Expected {EXPECTED_FRAMES} decoded frames, got {frames}")
    if (int(video.get("width", 0)), int(video.get("height", 0))) != EXPECTED_SIZE:
        raise ValueError(f"Expected 1920x1080 video, got {video.get('width')}x{video.get('height')}")
    if video.get("r_frame_rate") != "240/1" or video.get("avg_frame_rate") != "240/1":
        raise ValueError("Video must be constant 240/1 fps in both rate fields")
    duration = float(metadata.get("format", {}).get("duration", 0))
    if abs(duration - EXPECTED_DURATION) > 0.03:
        raise ValueError(f"Expected about {EXPECTED_DURATION:.6f}s, got {duration:.6f}s")
    if str(audio.get("sample_rate")) != "48000" or int(audio.get("channels", 0)) != 2:
        raise ValueError("Audio must be stereo 48 kHz")

    voice = load_json(voice_manifest_path)
    voice_id = voice.get("voice_id")
    voice_audio = voice.get("audio", {})
    voice_sha = voice_audio.get("sha256")
    if not voice_id or not isinstance(voice_sha, str) or len(voice_sha) != 64:
        raise ValueError("Voice manifest lacks a verified voice ID or source SHA-256")

    return {
        "status": "RENDERED_HYBRID_240FPS_PROOF_PENDING_HUMAN_REVIEW",
        "project": "53 Days to the End of an Empire",
        "sequence": "The great bombard — crew preparation, loading, recoil, flight, wall impact and repair",
        "classification": "illustrative 3D historical reconstruction; not archival footage",
        "engine": "Blender Eevee + FFmpeg motion-compensated interpolation",
        "source_run_id": str(source_run_id),
        "source_commit_sha": source_sha,
        "dimensions": [int(video["width"]), int(video["height"])],
        "output_fps": video["r_frame_rate"],
        "average_fps": video["avg_frame_rate"],
        "decoded_frames": frames,
        "source_3d_keyframe_fps": 30,
        "interpolated_to_240fps": True,
        "source_keyframes": 1176,
        "parallel_keyframe_shards": 4,
        "duration_seconds": duration,
        "video_codec": video.get("codec_name"),
        "audio_codec": audio.get("codec_name"),
        "audio_sample_rate": str(audio["sample_rate"]),
        "audio_channels": int(audio["channels"]),
        "narration": {
            "voice_id": voice_id,
            "source_sha256": voice_sha,
            "source_time_start": 220.760,
            "excerpt_duration": 39.140,
        },
        "audio_assets": [
            {
                "name": "Eye of the Storm",
                "url": "https://opengameart.org/content/eye-of-the-storm-0",
                "license": "CC0-1.0",
                "sha256": sha256_file(score_path),
                "human_auditioned": False,
            },
            {
                "name": "Cannon fire 1",
                "url": "https://opengameart.org/content/battle-at-sea",
                "license": "CC0-1.0",
                "sha256": sha256_file(cannon_fire_path),
                "human_auditioned": False,
            },
            {
                "name": "Cannon impact",
                "url": "https://opengameart.org/content/battle-at-sea",
                "license": "CC0-1.0",
                "sha256": sha256_file(cannon_impact_path),
                "human_auditioned": False,
            },
        ],
        "limitations": [
            "Generic large-bombard design, not a verified replica of Orban's exact gun.",
            "Optical-flow frames may require visual review around fast debris and cuts.",
            "CC0 score and effects are modern candidate recordings; human audition remains required.",
            "This is a 39-second proof, not the complete film.",
        ],
        "sha256_video": sha256_file(video_path),
        "video_bytes": video_path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--voice-manifest", type=Path, required=True)
    parser.add_argument("--score", type=Path, required=True)
    parser.add_argument("--cannon-fire", type=Path, required=True)
    parser.add_argument("--cannon-impact", type=Path, required=True)
    parser.add_argument("--source-run-id", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = build_manifest(
        video_path=args.video,
        metadata_path=args.metadata,
        voice_manifest_path=args.voice_manifest,
        score_path=args.score,
        cannon_fire_path=args.cannon_fire,
        cannon_impact_path=args.cannon_impact,
        source_run_id=args.source_run_id,
        source_sha=args.source_sha,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": manifest["status"],
        "frames": manifest["decoded_frames"],
        "fps": manifest["output_fps"],
        "sha256_video": manifest["sha256_video"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
