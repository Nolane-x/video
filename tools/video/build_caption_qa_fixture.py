#!/usr/bin/env python3
"""Build a deterministic English/Vietnamese subtitle fixture for OCR QA testing."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="out/caption-qa")
    args = parser.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    text_files = {
        "en_title": "ONE SMALL STEP",
        "en_subtitle": "The feed can wait.",
        "vi_title": "ĐỪNG BỎ CUỘC",
        "vi_subtitle": "Bạn có thể bắt đầu lại."
    }
    for name, text in text_files.items():
        (out / f"{name}.txt").write_text(text + "\n", encoding="utf-8")

    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def draw_pair(prefix: str) -> str:
        title = (out / f"{prefix}_title.txt").as_posix()
        subtitle = (out / f"{prefix}_subtitle.txt").as_posix()
        return (
            f"drawtext=fontfile={font}:textfile={title}:fontcolor=white:fontsize=50:"
            "x=(w-text_w)/2:y=255:borderw=2:bordercolor=black,"
            f"drawtext=fontfile={font}:textfile={subtitle}:fontcolor=white:fontsize=34:"
            "x=(w-text_w)/2:y=365:borderw=2:bordercolor=black"
        )

    video = out / "caption-qa-fixture.mp4"
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "color=c=0x20202b:s=1280x720:r=24:d=3",
        "-f", "lavfi", "-i", "color=c=0x303c4a:s=1280x720:r=24:d=3",
        "-filter_complex", f"[0:v]{draw_pair('en')}[en];[1:v]{draw_pair('vi')}[vi];[en][vi]concat=n=2:v=1:a=0[v]",
        "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)
    ]
    subprocess.run(command, check=True)

    shots = {
        "title": "Caption coverage QA fixture",
        "duration": 6,
        "fps": 24,
        "shots": [
            {"id": "english", "start": 0, "end": 3, "requiredOnScreenText": [text_files["en_title"], text_files["en_subtitle"]]},
            {"id": "vietnamese", "start": 3, "end": 6, "requiredOnScreenText": [text_files["vi_title"], text_files["vi_subtitle"]]}
        ]
    }
    shots_path = out / "shots.json"
    shots_path.write_text(json.dumps(shots, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"video": str(video), "shots": str(shots_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
