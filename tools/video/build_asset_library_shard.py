#!/usr/bin/env python3
"""Build one isolated asset-library source shard and stream size-safe ZIPs to a draft Release."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SOURCE_LANES = {
    "kenney": "download_kenney",
    "kenney-splash": "download_kenney_godot_splashscreens",
    "polyhaven": "download_polyhaven",
    "ambientcg": "download_ambientcg",
    "lazytextures": "download_lazytextures",
    "poly-pizza": "download_poly_pizza",
    "met": "download_met_open_access",
    "smithsonian": "download_smithsonian_open_access",
    "rijksmuseum": "download_rijksmuseum_open_access",
    "nasa": "download_nasa_media",
    "loc": "download_loc_public_domain",
    "wikimedia": "download_wikimedia_public_domain",
    "wikimedia-svg": "download_wikimedia_vector_svg",
    "wikimedia-av": "download_wikimedia_video_audio",
    "usgs": "download_usgs_gallery",
    "noaa": "download_noaa_ocean_exploration",
    "opengameart": "download_opengameart",
    "google-fonts": "download_google_fonts",
    "openmoji": "download_openmoji_assets",
    "internet-archive": "download_internet_archive_videos",
    "openverse": "download_openverse",
}

METADATA_NAMES = {"ASSET_INDEX.json", "ASSET_CATALOG.html", "SOURCES_AND_LICENSES.md", "SHA256SUMS.txt"}


def upload_release_asset(release_tag: str, asset_path: Path) -> None:
    """Upload one completed volume. The caller deletes source files only after this succeeds."""
    result = subprocess.run(
        ["gh", "release", "upload", release_tag, str(asset_path), "--clobber"],
        check=False,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "gh release upload failed").strip()
        raise RuntimeError(f"Could not upload {asset_path.name}: {detail[-1200:]}")


def create_source_volumes(
    root: Path,
    output_dir: Path,
    lane: str,
    assets: list[dict],
    packager,
    release_tag: str | None = None,
) -> list[dict]:
    """Create, validate and optionally upload one volume at a time to bound peak disk use."""
    root = Path(root).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    asset_by_path = {}
    for asset in assets:
        relative = str(asset.get("path") or "")
        path = PurePosixPath(relative)
        if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise RuntimeError(f"Unsafe indexed asset path: {relative!r}")
        if relative in asset_by_path:
            raise RuntimeError(f"Duplicate indexed asset path in {lane}: {relative}")
        asset_by_path[relative] = asset

    actual_files = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name not in METADATA_NAMES
    )
    missing = sorted(set(asset_by_path) - set(actual_files))
    if missing:
        raise FileNotFoundError(f"{lane} shard has indexed assets missing from disk: {missing[:8]}")

    groups: dict[str, list[str]] = {}
    for relative in actual_files:
        category = (
            packager.classify_asset(asset_by_path[relative])
            if relative in asset_by_path
            else packager.classify_unindexed_path(relative)
        )
        groups.setdefault(category, []).append(relative)

    rows = []
    safe_lane = lane.replace("_", "-")
    for category, paths in sorted(groups.items()):
        chunks = packager._chunk_group(paths, root)
        for chunk_number, chunk in enumerate(chunks, start=1):
            filename = f"video-assets-{safe_lane}-{category}-{chunk_number:03d}.zip"
            destination = output_dir / filename
            row = packager._write_zip(destination, root, chunk)
            if destination.stat().st_size >= packager.MAX_RELEASE_ASSET_BYTES:
                raise RuntimeError(f"Release volume is too large: {filename}")
            with zipfile.ZipFile(destination, "r") as archive:
                if archive.testzip() is not None:
                    raise RuntimeError(f"ZIP integrity failure: {filename}")
                expected_names = {
                    (PurePosixPath("video-asset-library") / PurePosixPath(relative)).as_posix()
                    for relative in chunk
                }
                if set(archive.namelist()) != expected_names:
                    raise RuntimeError(f"ZIP coverage mismatch: {filename}")

            row.update(
                category=category,
                source_lane=lane,
                asset_count=sum(relative in asset_by_path for relative in chunk),
            )
            if release_tag:
                upload_release_asset(release_tag, destination)
                # Retain the original files until GitHub confirms upload success.
                destination.unlink()
                for relative in chunk:
                    (root / relative).unlink()
                row["uploaded_to_release"] = True
            else:
                row["uploaded_to_release"] = False
            rows.append(row)
            print(
                f"[Shard:{lane}] volume {filename}: {row['archive_bytes']} archive bytes, "
                f"{row['uncompressed_bytes']} source bytes, {row['file_count']} files"
            )
    return rows


def _load_pipeline_modules(output_dir: Path):
    tool_dir = Path(__file__).resolve().parent
    if str(tool_dir) not in sys.path:
        sys.path.insert(0, str(tool_dir))
    original_argv = sys.argv[:]
    sys.argv = [str(tool_dir / "build_asset_library.py"), str(output_dir)]
    try:
        import build_asset_library as library
        import package_asset_bundles as packager
    finally:
        sys.argv = original_argv
    return library, packager


def _run_originals(library, root: Path, index: list[dict]) -> list[dict]:
    library.generate_originals(root, index)
    sticker_meme_counts = library.generate_sticker_meme_assets(root, index)
    texture_count = library.generate_original_textures(root, index)
    illustration_count = library.generate_original_illustrations(root, index)
    motion_loop_count = library.generate_original_motion_loops(root, index)
    return [{
        "id": "original-assets",
        "status": "generated",
        "sticker_meme_counts": sticker_meme_counts,
        "original_textures": texture_count,
        "original_illustrations": illustration_count,
        "original_motion_loops": motion_loop_count,
    }]


def _validate_and_hash_assets(library, root: Path, assets: list[dict]) -> tuple[list[dict], list[dict]]:
    seen_ids = set()
    seen_paths = set()
    validated = []
    for asset in assets:
        if not isinstance(asset, dict):
            raise RuntimeError("A source importer returned a non-object asset record")
        asset_id = str(asset.get("id") or "")
        relative = str(asset.get("path") or "")
        path_value = PurePosixPath(relative)
        if not asset_id or not relative or path_value.is_absolute() or ".." in path_value.parts or "\\" in relative:
            raise RuntimeError(f"Source importer returned an unsafe asset record: {asset!r}")
        if asset_id in seen_ids or relative in seen_paths:
            raise RuntimeError(f"Duplicate asset id or path in shard: {asset_id} / {relative}")
        seen_ids.add(asset_id)
        seen_paths.add(relative)
        path = root / relative
        if not path.is_file() or path.stat().st_size <= 0:
            raise FileNotFoundError(f"Indexed source asset is missing or empty: {relative}")
        if not asset.get("license") or asset.get("redistributable") is not True:
            raise RuntimeError(f"Asset lacks an explicit redistributable license record: {relative}")
        digest = library.sha256_path(path)
        recorded_digest = asset.get("sha256")
        if recorded_digest and recorded_digest != digest:
            raise RuntimeError(f"Source importer SHA-256 mismatch: {relative}")
        recorded_size = asset.get("size_bytes")
        actual_size = path.stat().st_size
        if recorded_size is not None and int(recorded_size) != actual_size:
            raise RuntimeError(f"Source importer byte count mismatch: {relative}")
        asset["sha256"] = digest
        asset["size_bytes"] = actual_size
        validated.append(asset)

    file_checksums = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in METADATA_NAMES:
            file_checksums.append({
                "path": path.relative_to(root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": library.sha256_path(path),
            })
    return validated, file_checksums


def build_shard(lane: str, output_dir: Path, release_tag: str | None = None) -> dict:
    if lane != "originals" and lane not in SOURCE_LANES:
        raise ValueError(f"Unknown source lane: {lane}")
    output_dir = Path(output_dir).resolve()
    root = output_dir / "video-asset-library"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    library, packager = _load_pipeline_modules(output_dir)
    assets: list[dict] = []
    started = time.monotonic()
    if lane == "originals":
        report = _run_originals(library, root, assets)
    else:
        downloader = getattr(library, SOURCE_LANES[lane])
        report = downloader(root, assets)

    assets, file_checksums = _validate_and_hash_assets(library, root, assets)
    rows = create_source_volumes(
        root=root,
        output_dir=output_dir / "volumes",
        lane=lane,
        assets=assets,
        packager=packager,
        release_tag=release_tag,
    )

    summary = {
        "lane": lane,
        "indexed_asset_count": len(assets),
        "indexed_resource_bytes": sum(int(asset["size_bytes"]) for asset in assets),
        "file_count_in_volumes": sum(int(row["file_count"]) for row in rows),
        "volume_count": len(rows),
        "archive_bytes_uploaded": sum(int(row["archive_bytes"]) for row in rows) if release_tag else 0,
        "report_rows": len(report) if isinstance(report, list) else 1,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "uploaded_to_release": bool(release_tag),
    }
    shard_manifest = {
        "schema_version": "1.0.0",
        "lane": lane,
        "built_at": summary["completed_at"],
        "summary": summary,
        "source_report": report,
        "assets": assets,
        "file_checksums": file_checksums,
        "bundles": rows,
    }
    manifest_path = output_dir / f"asset-shard--{lane}.json"
    manifest_path.write_text(
        json.dumps(shard_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if release_tag:
        upload_release_asset(release_tag, manifest_path)
    return shard_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", required=True, choices=["originals", *sorted(SOURCE_LANES)])
    parser.add_argument("--output-dir", default="dist/video-assets")
    parser.add_argument("--release-tag")
    args = parser.parse_args()
    build_shard(args.lane, Path(args.output_dir), args.release_tag)


if __name__ == "__main__":
    main()
