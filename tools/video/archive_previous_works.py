#!/usr/bin/env python3
"""Stage prior AI video outputs into the video library with exact SHA-256 checks.

Example (PowerShell):
  python tools/video/archive_previous_works.py --source-dir "$env:USERPROFILE\Downloads\video-previous-works-import-pack\assets"

This copies only catalog entries with archive_enabled=true. It never reports remote archival:
the user must commit/push the staged files, then Verify previous AI video assets validates them on GitHub.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "video-library" / "previous-works-catalog.json"
DEST_ROOT = ROOT / "video-library" / "previous-works"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_json(command: list[str]) -> dict:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{result.stderr}")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path, help="Directory containing downloaded assets with their original filenames")
    parser.add_argument("--strict", action="store_true", help="Fail if any archive-enabled catalog asset is not present in source-dir")
    args = parser.parse_args()
    source_dir = args.source_dir.expanduser().resolve()
    if not source_dir.is_dir():
        parser.error(f"source directory not found: {source_dir}")
    if shutil.which("ffprobe") is None or shutil.which("ffmpeg") is None:
        parser.error("FFmpeg and ffprobe must be available on PATH")

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    eligible = [
        a for a in catalog["assets"]
        if a.get("archive_enabled", False)
        and not str(a.get("storage_status", "")).startswith("archived in GitHub and verified")
    ]
    missing = [a["filename"] for a in eligible if not (source_dir / a["filename"]).is_file()]
    if args.strict and missing:
        parser.error("missing source assets: " + ", ".join(missing))
    if missing:
        print("WARN: not found and skipped: " + ", ".join(missing), file=sys.stderr)

    imported: list[dict] = []
    staged_paths: list[str] = []
    for asset in eligible:
        source = source_dir / asset["filename"]
        if not source.is_file():
            continue
        expected_size = int(asset["size_bytes"])
        expected_sha = asset["sha256"]
        actual_size = source.stat().st_size
        actual_sha = sha256(source)
        if actual_size != expected_size:
            raise SystemExit(f"{asset['filename']}: size mismatch ({actual_size} != {expected_size})")
        if actual_sha.lower() != expected_sha.lower():
            raise SystemExit(f"{asset['filename']}: SHA-256 mismatch ({actual_sha})")

        dest_dir = DEST_ROOT / asset["id"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / asset["filename"]
        if dest.exists() and sha256(dest) != expected_sha:
            raise SystemExit(f"refusing to overwrite different content: {dest}")
        if not dest.exists():
            shutil.copy2(source, dest)

        probe = run_json([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
            "-of", "json", str(dest)
        ])
        streams = probe.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), None)
        if video is None:
            raise SystemExit(f"{asset['filename']}: no video stream")
        audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
        duration = float(probe.get("format", {}).get("duration", 0))
        if abs(duration - float(asset["duration_seconds"])) > 0.25:
            raise SystemExit(f"{asset['filename']}: duration mismatch: {duration}")
        if (video.get("width"), video.get("height"), video.get("r_frame_rate")) != (1280, 720, "24/1"):
            raise SystemExit(f"{asset['filename']}: unexpected video stream: {video}")
        if audio is None or (audio.get("codec_name"), audio.get("sample_rate"), audio.get("channels")) != ("aac", "48000", 2):
            raise SystemExit(f"{asset['filename']}: unexpected audio stream: {audio}")

        interval = max(1, math.ceil(duration / 32))
        contact = dest_dir / "contact-sheet.jpg"
        overview = dest_dir / "overview-sheet.jpg"
        metadata_path = dest_dir / "metadata.json"
        sha_path = dest_dir / (asset["filename"] + ".sha256")
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(dest),
            "-vf", f"fps=1/{interval},scale=320:-1,tile=4x8", "-frames:v", "1", str(contact)
        ], check=True)
        overview_interval = max(1, round(duration / 16))
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(dest),
            "-vf", f"fps=1/{overview_interval},scale=320:-1,tile=4x4", "-frames:v", "1", str(overview)
        ], check=True)

        metadata = {
            "asset_id": asset["id"], "filename": asset["filename"],
            "sha256": actual_sha, "size_bytes": actual_size,
            "duration_seconds": duration, "video": video, "audio": audio,
            "integrity_checked_by": "tools/video/archive_previous_works.py",
            "remote_verification": "pending until pushed and verified by GitHub Actions"
        }
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        sha_path.write_text(f"{actual_sha}  {dest.name}\n", encoding="utf-8")

        asset.update({
            "repository_path": str(dest.relative_to(ROOT)).replace("\\", "/"),
            "metadata_path": str(metadata_path.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet_path": str(contact.relative_to(ROOT)).replace("\\", "/"),
            "overview_sheet_path": str(overview.relative_to(ROOT)).replace("\\", "/"),
            "sha256": actual_sha, "size_bytes": actual_size,
            "duration_seconds": duration,
            "storage_status": "validated and staged locally; awaiting commit/push and remote verification"
        })
        asset["fresh_probe"] = {
            "duration_seconds": duration, "width": video.get("width"), "height": video.get("height"),
            "fps": video.get("r_frame_rate"), "video_codec": video.get("codec_name"),
            "audio_codec": audio.get("codec_name"), "audio_sample_rate_hz": int(audio.get("sample_rate")),
            "audio_channels": audio.get("channels")
        }
        imported.append(asset)
        staged_paths.extend([
            str(dest.relative_to(ROOT)), str(sha_path.relative_to(ROOT)),
            str(contact.relative_to(ROOT)), str(overview.relative_to(ROOT)),
            str(metadata_path.relative_to(ROOT))
        ])
        print(f"Prepared: {asset['id']} — {duration:.2f}s — {actual_size:,} bytes")

    if not imported:
        parser.error("no assets were imported; download at least one archive-enabled file first")
    catalog["updated_at"] = "pending remote verification"
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    staged_paths.append(str(CATALOG_PATH.relative_to(ROOT)))
    subprocess.run(["git", "add", "-f", *staged_paths], cwd=ROOT, check=True)

    print(f"\nPrepared {len(imported)} asset(s). Files are staged locally, not yet archived on GitHub.")
    print("Review the staged diff, commit and push. The GitHub verification workflow will confirm the remote bytes and finalize storage status.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
