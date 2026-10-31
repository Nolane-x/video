#!/usr/bin/env python3
"""Generate synthetic footage, detect a cut, and round-trip a tiny OTIO timeline."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import opentimelineio as otio
from scenedetect import ContentDetector, detect

def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, text=True, capture_output=True)
    return result.stdout

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="out/editorial")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    video = out / "synthetic-two-scene.mp4"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "color=c=red:s=640x360:r=24:d=2",
        "-f", "lavfi", "-i", "color=c=blue:s=640x360:r=24:d=2",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(video)
    ])
    scenes = detect(str(video), ContentDetector(threshold=10.0), start_in_scene=True)
    if len(scenes) < 2:
        raise SystemExit(f"Expected >=2 scenes from synthetic hard cut, detected {len(scenes)}")
    duration = otio.opentime.RationalTime(96, 24)
    source_range = otio.opentime.TimeRange(otio.opentime.RationalTime(0, 24), duration)
    media_ref = otio.schema.ExternalReference(target_url=video.resolve().as_uri(), available_range=source_range)
    clip = otio.schema.Clip(name="Synthetic two-scene proof", media_reference=media_ref, source_range=source_range)
    track = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
    track.append(clip)
    timeline = otio.schema.Timeline(name="Nolane Editorial Interchange Proof")
    timeline.tracks.append(track)
    otio_path = out / "editorial-proof.otio"
    otio.adapters.write_to_file(timeline, str(otio_path))
    reopened = otio.adapters.read_from_file(str(otio_path))
    if len(reopened.tracks[0]) != 1:
        raise SystemExit("OTIO round-trip changed the clip count")
    if round(reopened.duration().to_frames(24)) != 96:
        raise SystemExit("OTIO round-trip changed the frame-accurate duration")
    scene_rows = [
        {"scene_id": f"scene-{index:03d}", "start_seconds": round(start.get_seconds(), 3), "end_seconds": round(end.get_seconds(), 3)}
        for index, (start, end) in enumerate(scenes, start=1)
    ]
    report = {"video": str(video), "duration_seconds": 4, "fps": 24,
        "detected_scene_count": len(scene_rows), "scenes": scene_rows,
        "otio_file": str(otio_path), "otio_clip_count": len(reopened.tracks[0]),
        "otio_duration_frames": round(reopened.duration().to_frames(24))}
    (out / "scene-detection-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
