#!/usr/bin/env python3
"""Regression-test the exact four-shard CFR-240 interpolation used in CI."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

FPS = 240
EXPECTED_TOTAL = 9394
PART_FRAMES = (2353, 2352, 2352, 2337)
CHUNK_RANGES = ((1, 296), (295, 590), (589, 884), (883, 1176))
MCI = (
    "minterpolate=fps=240:mi_mode=mci:mc_mode=obmc:me_mode=bilat:"
    "me=hexbs:search_param=16:vsbmc=0,scale=160:90:flags=lanczos"
)
TRIMS = (
    "trim=end_frame=2353,setpts=PTS-STARTPTS",
    "trim=start_frame=1:end_frame=2353,setpts=PTS-STARTPTS",
    "trim=start_frame=1:end_frame=2353,setpts=PTS-STARTPTS",
    "trim=start_frame=1:end_frame=2337,setpts=PTS-STARTPTS,"
    "tpad=stop_mode=clone:stop=1,trim=end_frame=2337",
)


def run(args: list[str]) -> str:
    result = subprocess.run(
        args, check=True, text=True, capture_output=True
    )
    return result.stdout


def probe(path: Path) -> dict:
    return json.loads(run([
        "ffprobe", "-v", "error", "-count_frames", "-show_streams",
        "-show_format", "-of", "json", str(path)
    ]))


def main() -> int:
    missing = [tool for tool in ("ffmpeg", "ffprobe") if not shutil.which(tool)]
    if missing:
        raise SystemExit("Missing required media tools: " + ", ".join(missing))

    with tempfile.TemporaryDirectory(prefix="hybrid-240fps-regression-") as td:
        root = Path(td)
        source = root / "source"
        source.mkdir()
        run([
            "ffmpeg", "-hide_banner", "-v", "error", "-y",
            "-f", "lavfi", "-i", "testsrc2=s=160x90:r=30:d=39.2",
            "-frames:v", "1176", str(source / "frame_%05d.png"),
        ])
        actual = sorted(path.name for path in source.glob("frame_*.png"))
        expected_names = [f"frame_{index:05d}.png" for index in range(1, 1177)]
        assert actual == expected_names, (len(actual), actual[:3], actual[-3:])

        for index, (first, last) in enumerate(CHUNK_RANGES):
            chunk = root / f"chunk-{index}"
            chunk.mkdir()
            for local_index, global_index in enumerate(range(first, last + 1), start=1):
                (chunk / f"frame_{local_index:05d}.png").symlink_to(
                    (source / f"frame_{global_index:05d}.png").resolve()
                )

        processes: list[tuple[int, subprocess.Popen[str]]] = []
        for index, expected_frames in enumerate(PART_FRAMES):
            output = root / f"part-{index}.mp4"
            command = [
                "ffmpeg", "-hide_banner", "-v", "error", "-y",
                "-filter_threads", "1", "-threads", "1",
                "-framerate", "30", "-start_number", "1", "-i",
                str(root / f"chunk-{index}" / "frame_%05d.png"),
                "-vf", MCI + "," + TRIMS[index],
                "-frames:v", str(expected_frames), "-an",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                "-pix_fmt", "yuv420p", "-r", "240", "-fps_mode", "cfr",
                "-video_track_timescale", "240000", str(output),
            ]
            processes.append((index, subprocess.Popen(
                command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )))

        for index, process in processes:
            _stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(
                    f"Interpolation shard {index} failed ({process.returncode}): {stderr[-2000:]}"
                )
            path = root / f"part-{index}.mp4"
            streams = probe(path).get("streams", [])
            video = next(s for s in streams if s.get("codec_type") == "video")
            frames = int(video.get("nb_read_frames") or video.get("nb_frames") or 0)
            assert frames == PART_FRAMES[index], (index, frames, PART_FRAMES[index], video)
            assert video.get("r_frame_rate") == "240/1", (index, video)
            assert video.get("avg_frame_rate") == "240/1", (index, video)
            assert (int(video["width"]), int(video["height"])) == (160, 90), (index, video)
            assert video.get("pix_fmt") == "yuv420p", (index, video)
            print(f"Interpolation shard {index}: PASS ({frames} frames)")

        concat_list = root / "parts.txt"
        concat_list.write_text(
            "".join(f"file '{root / f'part-{index}.mp4'}'\n" for index in range(4)),
            encoding="utf-8",
        )
        result = root / "result.mp4"
        run([
            "ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat",
            "-safe", "0", "-i", str(concat_list), "-c", "copy",
            "-movflags", "+faststart", str(result),
        ])
        meta = probe(result)
        video = next(s for s in meta["streams"] if s.get("codec_type") == "video")
        total = int(video.get("nb_read_frames") or video.get("nb_frames") or 0)
        duration = float(meta["format"]["duration"])
        assert total == EXPECTED_TOTAL, (total, video)
        assert video.get("r_frame_rate") == "240/1" and video.get("avg_frame_rate") == "240/1", video
        assert (int(video["width"]), int(video["height"])) == (160, 90), video
        assert video.get("pix_fmt") == "yuv420p", video
        assert abs(duration - EXPECTED_TOTAL / FPS) <= 0.01, duration

        sample = run([
            "ffmpeg", "-hide_banner", "-v", "error", "-i", str(result),
            "-vf", "select='not(mod(n,4))',scale=96:54,format=gray",
            "-frames:v", "180", "-f", "framemd5", "-",
        ])
        hashes = [
            line.split(",")[-1].strip()
            for line in sample.splitlines()
            if line and not line.startswith("#")
        ]
        unique = len(set(hashes))
        assert len(hashes) >= 170 and unique >= 170, (len(hashes), unique)
        print(
            "PARALLEL 240FPS REGRESSION PASS:", total, "frames;", duration,
            "seconds; unique 60fps samples", unique, "/", len(hashes)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
