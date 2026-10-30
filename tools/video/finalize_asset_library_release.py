#!/usr/bin/env python3
"""Merge source-shard manifests, verify uploaded Release assets, and publish the asset-library build."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_asset_library_shard as shard_builder  # noqa: E402

EXPECTED_LANES = {"originals", *shard_builder.SOURCE_LANES.keys()}
TARGET_BYTES = 50_000_000_000
MAX_RELEASE_ASSET_BYTES = 1_900_000_000
METADATA_FILES = (
    "ASSET_INDEX.json",
    "ASSET_CATALOG.html",
    "SOURCES_AND_LICENSES.md",
    "SHA256SUMS.txt",
    "ASSET_BUNDLES.json",
    "BUNDLE_INSTRUCTIONS.md",
    "VIDEO_ASSET_LIBRARY_BUILD.txt",
)


def merge_shard_manifests(
    shard_manifests: list[dict],
    expected_lanes: set[str] | None = None,
) -> dict:
    """Merge independent indexes and enforce path, checksum and volume coverage invariants."""
    expected = EXPECTED_LANES if expected_lanes is None else set(expected_lanes)
    by_lane = {}
    for shard in shard_manifests:
        lane = str(shard.get("lane") or "")
        if lane not in expected:
            raise RuntimeError(f"Unexpected asset shard: {lane!r}")
        if lane in by_lane:
            raise RuntimeError(f"Duplicate manifest for asset shard: {lane}")
        if not isinstance(shard.get("assets"), list) or not isinstance(shard.get("bundles"), list):
            raise RuntimeError(f"Shard {lane} is missing assets or bundle rows")
        if not isinstance(shard.get("file_checksums"), list):
            raise RuntimeError(f"Shard {lane} is missing its file checksum ledger")
        by_lane[lane] = shard

    missing_lanes = sorted(expected - set(by_lane))
    if missing_lanes:
        raise RuntimeError(f"Asset build is missing source shards: {missing_lanes}")

    all_assets = []
    all_files = []
    all_bundles = []
    asset_ids = set()
    asset_paths = set()
    checksum_paths = set()
    bundle_names = set()
    bundle_coverage = set()
    lane_summaries = {}
    lane_reports = {}

    for lane in sorted(expected):
        shard = by_lane[lane]
        lane_assets = shard["assets"]
        lane_files = shard["file_checksums"]
        lane_bundles = shard["bundles"]
        lane_summaries[lane] = shard.get("summary", {})
        lane_reports[lane] = shard.get("source_report", [])

        for asset in lane_assets:
            asset_id = str(asset.get("id") or "")
            relative = str(asset.get("path") or "")
            path = PurePosixPath(relative)
            if not asset_id or not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
                raise RuntimeError(f"Unsafe asset metadata in {lane}: {asset!r}")
            if asset_id in asset_ids:
                raise RuntimeError(f"Duplicate asset ID across shards: {asset_id}")
            if relative in asset_paths:
                raise RuntimeError(f"Duplicate asset path across shards: {relative}")
            if not asset.get("license") or asset.get("redistributable") is not True:
                raise RuntimeError(f"Asset has no verified redistributable license: {relative}")
            digest = str(asset.get("sha256") or "")
            size = int(asset.get("size_bytes") or 0)
            if len(digest) != 64 or size <= 0:
                raise RuntimeError(f"Asset SHA-256 or byte count is invalid: {relative}")
            asset_ids.add(asset_id)
            asset_paths.add(relative)
            all_assets.append(asset)

        for file_row in lane_files:
            relative = str(file_row.get("path") or "")
            path = PurePosixPath(relative)
            digest = str(file_row.get("sha256") or "")
            size = int(file_row.get("size_bytes") or 0)
            if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
                raise RuntimeError(f"Unsafe checksum path in {lane}: {relative!r}")
            if relative in checksum_paths:
                raise RuntimeError(f"Duplicate file path across source shards: {relative}")
            if len(digest) != 64 or size <= 0:
                raise RuntimeError(f"Invalid file checksum record: {relative}")
            checksum_paths.add(relative)
            all_files.append(file_row)

        for bundle in lane_bundles:
            name = str(bundle.get("name") or "")
            digest = str(bundle.get("sha256") or "")
            archive_bytes = int(bundle.get("archive_bytes") or 0)
            paths = bundle.get("paths")
            if not name or name in bundle_names:
                raise RuntimeError(f"Duplicate or missing release volume name: {name!r}")
            if len(digest) != 64 or archive_bytes <= 0 or archive_bytes >= MAX_RELEASE_ASSET_BYTES:
                raise RuntimeError(f"Release volume does not meet the size/hash gate: {name}")
            if not isinstance(paths, list) or not paths:
                raise RuntimeError(f"Release volume has no path coverage: {name}")
            for relative in paths:
                if relative not in checksum_paths and relative not in {str(x.get("path")) for x in lane_files}:
                    raise RuntimeError(f"Release volume references a file absent from the shard ledger: {relative}")
                if relative in bundle_coverage:
                    raise RuntimeError(f"Resource file appears in multiple release volumes: {relative}")
                bundle_coverage.add(relative)
            bundle_names.add(name)
            all_bundles.append(bundle)

    if bundle_coverage != checksum_paths:
        missing = sorted(checksum_paths - bundle_coverage)
        extra = sorted(bundle_coverage - checksum_paths)
        raise RuntimeError(
            f"Release volume coverage mismatch; missing={missing[:8]}, extra={extra[:8]}"
        )

    # Every indexed resource must also appear in the independent file-checksum ledger.
    checksums_by_path = {row["path"]: row for row in all_files}
    for asset in all_assets:
        checksum = checksums_by_path.get(asset["path"])
        if not checksum or checksum["sha256"] != asset["sha256"] or int(checksum["size_bytes"]) != int(asset["size_bytes"]):
            raise RuntimeError(f"Indexed asset does not match its file-checksum record: {asset['path']}")

    license_counts = Counter(str(asset.get("license") or "unlabelled") for asset in all_assets)
    indexed_bytes = sum(int(asset["size_bytes"]) for asset in all_assets)
    all_file_bytes = sum(int(row["size_bytes"]) for row in all_files)
    summary = {
        "target_bytes": TARGET_BYTES,
        "target_gb": 50,
        "target_reached": indexed_bytes >= TARGET_BYTES,
        "indexed_asset_count": len(all_assets),
        "indexed_resource_bytes": indexed_bytes,
        "indexed_resource_gib": round(indexed_bytes / (1024 ** 3), 3),
        "all_packaged_file_count": len(all_files),
        "all_packaged_file_bytes": all_file_bytes,
        "all_packaged_file_gib": round(all_file_bytes / (1024 ** 3), 3),
        "bundle_count": len(all_bundles),
        "license_counts": dict(sorted(license_counts.items())),
        "source_lanes_completed": len(by_lane),
        "source_lane_count": len(expected),
        "by_source_lane": lane_summaries,
    }
    return {
        "schema_version": "1.0.0",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "assets": all_assets,
        "file_checksums": all_files,
        "bundles": sorted(all_bundles, key=lambda row: row["name"]),
        "source_reports": lane_reports,
    }


def write_release_metadata(merged: dict, output_dir: Path, repository: str, release_tag: str) -> list[Path]:
    """Create the global offline catalog, provenance ledger and release manifest from shard metadata."""
    output_dir = Path(output_dir).resolve()
    root = output_dir / "video-asset-library"
    root.mkdir(parents=True, exist_ok=True)

    assets = merged["assets"]
    files = merged["file_checksums"]
    bundles = merged["bundles"]
    summary = dict(merged["summary"])
    index_doc = {
        "schema_version": "1.0.0",
        "built_at": merged["built_at"],
        "repository": f"https://github.com/{repository}",
        "release_tag": release_tag,
        "policy": (
            "Assets are included only when their source importer records a redistributable license "
            "and the exact source/item rights checks pass. The per-asset license, license URL, "
            "source page, provider evidence fields, size and SHA-256 are preserved below. "
            "CC0, Public Domain, CC BY-SA and other licenses are never silently relabelled."
        ),
        "target": {
            "target_bytes": TARGET_BYTES,
            "target_gb": 50,
            "actual_indexed_resource_bytes": summary["indexed_resource_bytes"],
            "actual_indexed_resource_gib": summary["indexed_resource_gib"],
            "reached": summary["target_reached"],
        },
        "summary": summary,
        "source_reports": merged["source_reports"],
        "assets": assets,
    }
    index_path = root / "ASSET_INDEX.json"
    index_path.write_text(json.dumps(index_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    license_lines = [
        "# Video Asset Library — source and license ledger",
        "",
        f"- Release: {release_tag}",
        f"- Indexed assets: {summary['indexed_asset_count']}",
        f"- Actual indexed resource bytes: {summary['indexed_resource_bytes']}",
        f"- 50 GB target reached: {summary['target_reached']}",
        "",
        "Each row below preserves the exact license label and source record from the item importer. "
        "Check the license and any non-copyright restrictions before publishing a video.",
        "",
    ]
    for asset in sorted(assets, key=lambda row: (str(row.get("provider") or ""), str(row.get("id") or ""))):
        evidence = [
            key for key, value in asset.items()
            if ("verified" in key or "rights" in key or "copyright_marker" in key)
            and value is True
        ]
        license_lines.append(
            f"- **{asset.get('id')}** — {asset.get('license')} — "
            f"{asset.get('size_bytes')} bytes — {asset.get('source_page') or 'original repository asset'}"
            + (f" — evidence: {', '.join(evidence)}" if evidence else "")
            + (f" — license: {asset.get('license_url')}" if asset.get("license_url") else "")
        )
    license_path = root / "SOURCES_AND_LICENSES.md"
    license_path.write_text("\n".join(license_lines) + "\n", encoding="utf-8")

    # make_asset_catalog can render metadata-only entries because workers have
    # already hashed and uploaded the files; the catalog links to extraction paths.
    import build_asset_library as library
    library.make_asset_catalog(root, assets, summary)

    checksum_lines = [
        f"{row['sha256']}  {row['path']}"
        for row in sorted(files, key=lambda row: row["path"])
    ]
    sums_path = root / "SHA256SUMS.txt"
    sums_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    bundle_manifest = {
        "schema_version": "1.0.0",
        "built_at": merged["built_at"],
        "mode": "multi-volume",
        "target_bytes": TARGET_BYTES,
        "target_reached": summary["target_reached"],
        "total_uncompressed_bytes": summary["all_packaged_file_bytes"],
        "indexed_asset_count": summary["indexed_asset_count"],
        "indexed_resource_bytes": summary["indexed_resource_bytes"],
        "bundle_count": len(bundles),
        "bundles": bundles,
        "extraction_root": "video-asset-library/",
        "metadata_files": list(METADATA_FILES),
    }
    bundle_path = output_dir / "ASSET_BUNDLES.json"
    bundle_path.write_text(json.dumps(bundle_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    instructions = (
        "# Video Asset Library — distributed multi-volume download\n\n"
        "This build is distributed as independent ZIP volumes so the full collection does not need "
        "to fit on one CI runner or one download at once. Download ASSET_BUNDLES.json to see every "
        "volume, exact compressed size, uncompressed size and SHA-256. Download only the media "
        "families you need, or download all volumes. Extract all selected ZIPs into the same parent "
        "folder; each archive writes under video-asset-library/. After extraction, verify files "
        "with video-asset-library/SHA256SUMS.txt. The asset index records the exact item license "
        "and source for every redistributable resource.\n"
    )
    instructions_path = output_dir / "BUNDLE_INSTRUCTIONS.md"
    instructions_path.write_text(instructions, encoding="utf-8")
    build_text = (
        f"built_at={merged['built_at']}\nrelease_tag={release_tag}\nmode=distributed-multi-volume\n"
        f"target_bytes={TARGET_BYTES}\ntarget_reached={summary['target_reached']}\n"
        f"indexed_asset_count={summary['indexed_asset_count']}\n"
        f"indexed_resource_bytes={summary['indexed_resource_bytes']}\n"
        f"indexed_resource_gib={summary['indexed_resource_gib']}\n"
        f"bundle_count={len(bundles)}\n"
        f"summary={json.dumps(summary, ensure_ascii=False)}\n"
    )
    build_path = output_dir / "VIDEO_ASSET_LIBRARY_BUILD.txt"
    build_path.write_text(build_text, encoding="utf-8")
    return [
        index_path,
        root / "ASSET_CATALOG.html",
        license_path,
        sums_path,
        bundle_path,
        instructions_path,
        build_path,
    ]


def _run_gh_json(args: list[str]) -> dict:
    result = subprocess.run(args, check=True, capture_output=True, text=True, env=os.environ.copy())
    return json.loads(result.stdout)


def verify_release_assets(repository: str, release_tag: str, merged: dict, metadata_paths: list[Path]) -> dict:
    release = _run_gh_json(["gh", "api", f"repos/{repository}/releases/tags/{release_tag}"])
    if not release.get("draft"):
        raise RuntimeError("Release was published before the final validation gate")
    remote_assets = {asset.get("name"): asset for asset in release.get("assets", [])}
    if len(remote_assets) > 1000:
        raise RuntimeError("GitHub Release asset count exceeds 1000")

    expected = []
    for bundle in merged["bundles"]:
        expected.append((bundle["name"], int(bundle["archive_bytes"]), bundle["sha256"]))
    for path in metadata_paths:
        if path.name in remote_assets:
            raise RuntimeError(f"Release metadata name already exists: {path.name}")
        expected.append((path.name, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()))

    for name, size, digest in expected:
        remote = remote_assets.get(name)
        if not remote:
            raise RuntimeError(f"Release is missing uploaded asset: {name}")
        if int(remote.get("size") or 0) != size:
            raise RuntimeError(f"Release asset size mismatch: {name}")
        remote_digest = str(remote.get("digest") or "")
        if remote_digest and remote_digest.lower() != "sha256:" + digest.lower():
            raise RuntimeError(f"Release asset digest mismatch: {name}")
    too_large = [name for name, size, _ in expected if size >= MAX_RELEASE_ASSET_BYTES]
    if too_large:
        raise RuntimeError(f"Release contains asset(s) that are too large: {too_large[:5]}")
    return {"release_id": release["id"], "asset_count": len(remote_assets), "verified_assets": len(expected)}


def publish_release(repository: str, release_tag: str, release_title: str, notes_path: Path) -> dict:
    """Publish a draft only after all volumes and metadata have been verified."""
    release = _run_gh_json(["gh", "api", f"repos/{repository}/releases/tags/{release_tag}"])
    release_id = release["id"]
    result = subprocess.run(
        [
            "gh", "api", f"repos/{repository}/releases/{release_id}",
            "-X", "PATCH", "-F", "draft=false", "-f", f"name={release_title}",
            "-F", f"body=@{notes_path}",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    published = json.loads(result.stdout)
    if published.get("draft") is not False:
        raise RuntimeError("GitHub did not confirm publication of the asset-library Release")
    return published


def finalize_release(manifest_dir: Path, output_dir: Path, repository: str, release_tag: str) -> dict:
    paths = sorted(Path(manifest_dir).glob("asset-shard--*.json"))
    if not paths:
        raise FileNotFoundError("No asset shard manifests were downloaded")
    shards = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    merged = merge_shard_manifests(shards)
    metadata_paths = write_release_metadata(merged, output_dir, repository, release_tag)

    # Upload the aggregate catalog and checksum metadata only after every source job succeeded.
    subprocess.run(
        ["gh", "release", "upload", release_tag, *[str(path) for path in metadata_paths]],
        check=True,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    verified = verify_release_assets(repository, release_tag, merged, metadata_paths)
    summary = merged["summary"]
    actual_gib = summary["indexed_resource_gib"]
    title = f"Nolane Video Asset Library — {summary['indexed_resource_bytes'] / 1_000_000_000:.2f} GB / 50 GB target"
    notes_path = Path(output_dir).resolve() / "RELEASE_NOTES.md"
    notes_path.write_text(
        f"# Nolane Video Asset Library\n\n"
        f"- Actual indexed resource size: **{summary['indexed_resource_bytes']} bytes "
        f"({summary['indexed_resource_bytes'] / 1_000_000_000:.3f} GB)**\n"
        f"- Target: **50 GB**\n"
        f"- Target status: **{'reached' if summary['target_reached'] else 'not reached'}**\n"
        f"- Indexed resources: **{summary['indexed_asset_count']}**\n"
        f"- Download volumes: **{summary['bundle_count']}**\n\n"
        "Every volume is under the release-file safety ceiling. The global index, source/license "
        "ledger, searchable catalog and SHA-256 list are included as separate release assets. "
        "A target below 50 GB is reported as partial progress, never rounded up or described as complete.\n",
        encoding="utf-8",
    )
    published = publish_release(repository, release_tag, title, notes_path)
    return {
        "release_tag": release_tag,
        "release_url": published.get("html_url"),
        "actual_indexed_resource_bytes": summary["indexed_resource_bytes"],
        "actual_indexed_resource_gib": actual_gib,
        "target_bytes": TARGET_BYTES,
        "target_reached": summary["target_reached"],
        "indexed_asset_count": summary["indexed_asset_count"],
        "bundle_count": summary["bundle_count"],
        "release_asset_verification": verified,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-dir", required=True)
    parser.add_argument("--output-dir", default="dist/final")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()
    print(json.dumps(
        finalize_release(
            Path(args.manifest_dir),
            Path(args.output_dir),
            args.repository,
            args.release_tag,
        ),
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
