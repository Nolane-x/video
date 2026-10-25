#!/usr/bin/env python3
"""Import the exact prior-session H2 master into this repository, with strict provenance checks.

1) Download the exact attachment named one-more-scroll-h2-final.mp4.
2) Run from repository root:
   python tools/video/archive_h2_master.py "C:\\Users\\YOU\\Downloads\\one-more-scroll-h2-final.mp4"
3) Review generated contact sheets and git status, then commit/push the resulting files.

The hash check prevents importing the Remotion render or another similarly named MP4 by mistake.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

EXPECTED_SHA256 = "be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f"
EXPECTED_SIZE = 31_547_778
EXPECTED_DURATION = 155.0
REPO_ROOT = Path(__file__).resolve().parents[2]
FILM_DIR = REPO_ROOT / "video-library" / "one-more-scroll"
DEST = FILM_DIR / "one-more-scroll-h2-final.mp4"
MANIFEST = FILM_DIR / "manifest.json"
QA = FILM_DIR / "QA.md"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def run_json(args: list[str]) -> dict:
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(args)}\n{result.stderr}")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Path to the exact H2 MP4 downloaded from the prior ChatGPT attachment")
    args = parser.parse_args()
    source = args.video.expanduser().resolve()
    if not source.is_file():
        parser.error(f"file not found: {source}")
    if shutil.which("ffprobe") is None or shutil.which("ffmpeg") is None:
        parser.error("FFmpeg and ffprobe must be installed and available on PATH")

    size = source.stat().st_size
    sha = digest(source)
    if size != EXPECTED_SIZE:
        parser.error(f"unexpected file size {size}; expected {EXPECTED_SIZE}. Do not import an unverified file.")
    if sha.lower() != EXPECTED_SHA256:
        parser.error(f"SHA-256 mismatch: {sha}. The file is not the known H2 master.")
    probe = run_json([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json", str(source)
    ])
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(probe.get("format", {}).get("duration", 0))
    if not video or not audio:
        parser.error("MP4 must contain both video and audio streams")
    if (video.get("width"), video.get("height"), video.get("r_frame_rate")) != (1920, 1080, "24/1"):
        parser.error(f"unexpected video stream metadata: {video}")
    if video.get("codec_name") != "h264" or audio.get("codec_name") != "aac":
        parser.error(f"unexpected codecs: video={video.get('codec_name')}, audio={audio.get('codec_name')}")
    if (audio.get("sample_rate"), audio.get("channels")) != ("48000", 2):
        parser.error(f"unexpected audio format: {audio}")
    if abs(duration - EXPECTED_DURATION) > 0.1:
        parser.error(f"unexpected duration {duration}; expected approximately {EXPECTED_DURATION}s")

    FILM_DIR.mkdir(parents=True, exist_ok=True)
    if DEST.exists() and digest(DEST) != EXPECTED_SHA256:
        parser.error(f"destination exists with different content: {DEST}; move it aside before retrying")
    shutil.copy2(source, DEST)
    (FILM_DIR / "one-more-scroll-h2-final.mp4.sha256").write_text(
        f"{sha}  one-more-scroll-h2-final.mp4\n", encoding="utf-8"
    )

    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(DEST),
        "-vf", "fps=1/5,scale=320:-1,tile=4x8", "-frames:v", "1",
        str(FILM_DIR / "original-h2-contact-sheet-shots.jpg")
    ], check=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(DEST),
        "-vf", "fps=1/10,scale=320:-1,tile=4x4", "-frames:v", "1",
        str(FILM_DIR / "original-h2-contact-sheet-overview.jpg")
    ], check=True)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    master = manifest["canonical_master"]
    master["storage_status"] = "committed to GitHub repository by archive_h2_master.py"
    master["repository_path"] = "video-library/one-more-scroll/one-more-scroll-h2-final.mp4"
    master["sha256"] = sha
    master["size_bytes"] = size
    master["fresh_probe"] = {
        "duration_seconds": duration,
        "width": video["width"],
        "height": video["height"],
        "fps": video["r_frame_rate"],
        "video_codec": video["codec_name"],
        "audio_codec": audio["codec_name"],
        "audio_sample_rate_hz": int(audio["sample_rate"]),
        "audio_channels": int(audio["channels"])
    }
    for item in manifest.get("prior_session_files", []):
        if item.get("file") == "one-more-scroll-h2-final.mp4":
            item["storage"] = "GitHub repository binary at video-library/one-more-scroll/one-more-scroll-h2-final.mp4"
            item["repository_path"] = master["repository_path"]
            item["sha256"] = sha
            item["size_bytes"] = size
    manifest["known_unverified"] = [
        issue for issue in manifest.get("known_unverified", [])
        if "exact canonical H2 master is not archived" not in issue
        and "exact H2 master is not archived as a durable GitHub binary" not in issue
    ]
    manifest.setdefault("archived_h2_master", {})
    manifest["archived_h2_master"] = {
        "repository_path": master["repository_path"],
        "sha256": sha,
        "size_bytes": size,
        "imported_by": "tools/video/archive_h2_master.py",
        "note": "Original H2 Canvas/Chromium master; keep separate from the Remotion render."
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Update QA with import/probe evidence while leaving visual sign-off explicit.
    qa_text = QA.read_text(encoding="utf-8") if QA.exists() else ""
    qa_text = qa_text.replace(
        "- [ ] Archive the exact H2 master to durable GitHub storage.",
        "- [x] Archive the exact H2 master to durable GitHub storage."
    ).replace(
        "- [ ] Record its SHA-256 and fresh ffprobe output.",
        "- [x] Record its SHA-256 and fresh ffprobe output."
    )
    if "Exact H2 master imported into GitHub" not in qa_text:
        qa_text += (
            "\n\n## Exact H2 master imported into GitHub\n"
            f"- Repository path: {master['repository_path']}\n"
            f"- SHA-256: {sha}\n"
            f"- Size: {size:,} bytes\n"
            f"- ffprobe: {duration:.3f}s, 1920x1080, 24 fps, H.264 + AAC stereo 48 kHz.\n"
            "- Contact sheets were generated. This confirms import/integrity, not artistic sign-off; inspect the previously noted face, shoe-tying and staircase issues.\n"
        )
    QA.write_text(qa_text, encoding="utf-8")

    # Remove stale "not archived" state text and replace it with the newly verified location.
    state_path = REPO_ROOT / "docs" / "STATE.md"
    if state_path.exists():
        lines = state_path.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if "**Storage truth:**" not in line and "The exact H2 master SHA-256 is" not in line]
        for i, line in enumerate(kept):
            if line.startswith("- Related session attachments:"):
                kept.insert(i + 1, f"- Exact H2 master archived at {master['repository_path']} (SHA-256 {sha}, {size:,} bytes). The Remotion render remains a separate file.")
                break
        state_path.write_text("\n".join(kept) + "\n", encoding="utf-8")

    print("H2 master imported and validated:")
    print(f"  path: {DEST.relative_to(REPO_ROOT)}")
    print(f"  size: {size:,} bytes")
    print(f"  SHA-256: {sha}")
    print("  generated per-shot and overview contact sheets")
    print("Next: review the contact sheets, then git add/commit/push the generated binary, manifest and sheets.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
