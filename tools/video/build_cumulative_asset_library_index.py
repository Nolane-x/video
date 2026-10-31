#!/usr/bin/env python3
"""Build a content-addressed cumulative index across published video asset-library Releases."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote

TARGET_BYTES = 50_000_000_000


def _safe_sha256(value: object, label: str) -> str:
    digest = str(value or "").strip().lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise RuntimeError(f"{label} does not contain a valid SHA-256 digest")
    return digest


def _safe_relative_path(value: object, label: str) -> str:
    relative = str(value or "").strip()
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
        raise RuntimeError(f"{label} contains an unsafe relative path: {relative!r}")
    return relative


def _release_download_url(repository: str, tag: str, asset_name: str) -> str:
    return (
        f"https://github.com/{repository}/releases/download/"
        f"{quote(tag, safe='-._')}/{quote(asset_name, safe='-._')}"
    )


def merge_published_release_indexes(releases: list[dict]) -> dict:
    """Merge published indexes and deduplicate exact byte-identical resources by SHA-256.

    Every provenance occurrence is retained. If a byte-identical file appears under
    multiple item records or licenses, this function does not merge the rights claims;
    it records each origin separately so a downstream editor can choose a source whose
    license and attribution requirements fit the intended use.
    """
    if not releases:
        raise ValueError("At least one published release index is required")

    release_tags = []
    unique_by_sha: dict[str, dict] = {}
    bundle_rows = []
    release_file_bytes = 0
    release_asset_counts = 0
    seen_release_tags = set()

    for release in releases:
        tag = str(release.get("release_tag") or "").strip()
        repository = str(release.get("repository") or "").strip()
        if not tag or not repository or "/" not in repository:
            raise RuntimeError("Every source index must declare release_tag and owner/repository")
        if tag in seen_release_tags:
            raise RuntimeError(f"Duplicate source release index: {tag}")
        seen_release_tags.add(tag)
        release_tags.append(tag)

        assets = release.get("assets")
        if not isinstance(assets, list):
            raise RuntimeError(f"Release {tag} has no assets array")
        bundles = release.get("bundles")
        if not isinstance(bundles, list):
            raise RuntimeError(f"Release {tag} has no bundles array")

        bundle_for_path: dict[str, dict] = {}
        local_bundle_names = set()
        for bundle in bundles:
            if not isinstance(bundle, dict):
                raise RuntimeError(f"Release {tag} contains a non-object bundle")
            name = str(bundle.get("name") or "").strip()
            digest = _safe_sha256(bundle.get("sha256"), f"{tag}/{name or 'bundle'}")
            archive_bytes = int(bundle.get("archive_bytes") or 0)
            paths = bundle.get("paths")
            if not name or name in local_bundle_names:
                raise RuntimeError(f"Release {tag} has a duplicate or missing bundle name")
            if archive_bytes <= 0 or archive_bytes >= 1_900_000_000:
                raise RuntimeError(f"Release {tag} bundle {name} has an invalid archive byte count")
            if not isinstance(paths, list) or not paths:
                raise RuntimeError(f"Release {tag} bundle {name} has no path coverage")
            clean_paths = []
            for raw_path in paths:
                path = _safe_relative_path(raw_path, f"{tag}/{name}")
                if path in bundle_for_path:
                    raise RuntimeError(f"Release {tag} packages {path} into more than one volume")
                bundle_for_path[path] = bundle
                clean_paths.append(path)
            local_bundle_names.add(name)
            bundle_rows.append({
                "release_tag": tag,
                "name": name,
                "sha256": digest,
                "archive_bytes": archive_bytes,
                "uncompressed_bytes": int(bundle.get("uncompressed_bytes") or 0),
                "file_count": int(bundle.get("file_count") or len(clean_paths)),
                "paths": clean_paths,
                "download_url": _release_download_url(repository, tag, name),
            })

        seen_ids = set()
        seen_paths = set()
        indexed_bytes_for_release = 0
        for asset in assets:
            if not isinstance(asset, dict):
                raise RuntimeError(f"Release {tag} contains a non-object asset record")
            asset_id = str(asset.get("id") or "").strip()
            path = _safe_relative_path(asset.get("path"), f"{tag}/asset")
            digest = _safe_sha256(asset.get("sha256"), f"{tag}/{path}")
            size = int(asset.get("size_bytes") or 0)
            if not asset_id or size <= 0:
                raise RuntimeError(f"Release {tag} has an asset with missing ID or byte count: {path}")
            if asset.get("redistributable") is not True or not asset.get("license"):
                raise RuntimeError(f"Release {tag} has an asset without a redistributable license record: {path}")
            if asset_id in seen_ids or path in seen_paths:
                raise RuntimeError(f"Release {tag} has a duplicate asset ID or path: {asset_id}/{path}")
            seen_ids.add(asset_id)
            seen_paths.add(path)

            bundle = bundle_for_path.get(path)
            if not bundle:
                raise RuntimeError(f"Release {tag} does not package indexed asset {path} in any volume")
            bundle_name = bundle["name"]
            origin = {
                "release_tag": tag,
                "repository": repository,
                "asset_id": asset_id,
                "path": path,
                "size_bytes": size,
                "sha256": digest,
                "provider": asset.get("provider"),
                "title": asset.get("title"),
                "license": asset.get("license"),
                "license_url": asset.get("license_url"),
                "source_page": asset.get("source_page"),
                "redistributable": True,
                "bundle_name": bundle_name,
                "bundle_sha256": bundle["sha256"],
                "download_url": _release_download_url(repository, tag, bundle_name),
            }
            # Keep the exact rights evidence/provenance fields, not just a normalized license.
            rights_evidence = {
                key: value for key, value in asset.items()
                if "rights" in key.lower() or "license" in key.lower()
                or key in {
                    "record_access", "media_access", "record_id", "rights_statement",
                    "item_page_copyright_marker_absent", "license_verified_from_item_page",
                    "license_verified_from_item_metadata",
                }
            }
            origin["rights_evidence"] = rights_evidence
            row = unique_by_sha.get(digest)
            if row is None:
                unique_by_sha[digest] = {
                    "sha256": digest,
                    "size_bytes": size,
                    "canonical_asset": {
                        "id": asset_id,
                        "path": path,
                        "type": asset.get("type"),
                        "provider": asset.get("provider"),
                        "title": asset.get("title"),
                        "category": asset.get("category"),
                    },
                    "origins": [origin],
                }
            else:
                if int(row["size_bytes"]) != size:
                    raise RuntimeError(
                        f"SHA-256 {digest} has inconsistent byte sizes across releases"
                    )
                row["origins"].append(origin)
            indexed_bytes_for_release += size

        declared_bytes = release.get("summary", {}).get("indexed_resource_bytes")
        if declared_bytes is not None and int(declared_bytes) != indexed_bytes_for_release:
            raise RuntimeError(
                f"Release {tag} index total mismatch: "
                f"declared={declared_bytes}, computed={indexed_bytes_for_release}"
            )
        release_file_bytes += indexed_bytes_for_release
        release_asset_counts += len(assets)

    unique_rows = sorted(unique_by_sha.values(), key=lambda row: (row["canonical_asset"]["provider"] or "", row["sha256"]))
    unique_bytes = sum(int(row["size_bytes"]) for row in unique_rows)
    duplicate_bytes = release_file_bytes - unique_bytes
    if duplicate_bytes < 0:
        raise RuntimeError("Cumulative unique bytes exceed the summed release resource bytes")

    origin_occurrences = sum(len(row["origins"]) for row in unique_rows)
    summary = {
        "target_bytes": TARGET_BYTES,
        "target_gb": 50,
        "target_reached": unique_bytes >= TARGET_BYTES,
        "unique_resource_bytes": unique_bytes,
        "unique_resource_gb": round(unique_bytes / 1_000_000_000, 3),
        "unique_resource_gib": round(unique_bytes / (1024 ** 3), 3),
        "unique_asset_count": len(unique_rows),
        "source_release_count": len(release_tags),
        "source_release_tags": release_tags,
        "release_asset_occurrences": release_asset_counts,
        "origin_occurrences": origin_occurrences,
        "duplicate_resource_occurrences": origin_occurrences - len(unique_rows),
        "summed_release_resource_bytes_before_dedup": release_file_bytes,
        "duplicate_resource_bytes_removed": duplicate_bytes,
    }
    return {
        "schema_version": "1.0.0",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "deduplication": {
            "key": "SHA-256 of exact downloaded resource file bytes",
            "policy": (
                "Exact byte-identical assets are counted once toward unique bytes. Every source "
                "occurrence and its own license/rights evidence remain separately recorded. "
                "Deduplication does not merge, broaden or waive license terms."
            ),
        },
        "summary": summary,
        "assets": unique_rows,
        "release_bundles": sorted(bundle_rows, key=lambda row: (row["release_tag"], row["name"])),
    }


def load_release_inputs(input_dir: Path) -> list[dict]:
    """Load one subdirectory per release, each with ASSET_INDEX.json and ASSET_BUNDLES.json."""
    input_dir = Path(input_dir)
    release_dirs = sorted(path for path in input_dir.iterdir() if path.is_dir())
    if not release_dirs:
        raise FileNotFoundError(f"No release input folders found in {input_dir}")
    releases = []
    for folder in release_dirs:
        index_path = folder / "ASSET_INDEX.json"
        bundles_path = folder / "ASSET_BUNDLES.json"
        if not index_path.is_file() or not bundles_path.is_file():
            raise FileNotFoundError(f"{folder} is missing ASSET_INDEX.json or ASSET_BUNDLES.json")
        index = json.loads(index_path.read_text(encoding="utf-8"))
        bundles = json.loads(bundles_path.read_text(encoding="utf-8"))
        if not isinstance(index, dict) or not isinstance(bundles, dict):
            raise RuntimeError(f"{folder} release metadata roots must be JSON objects")
        release = dict(index)
        release["bundles"] = bundles.get("bundles")
        releases.append(release)
    return releases


def write_cumulative_index(cumulative: dict, output_dir: Path) -> tuple[Path, Path]:
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "CUMULATIVE_ASSET_INDEX.json"
    downloads_path = output_dir / "CUMULATIVE_ASSET_DOWNLOADS.json"
    index_path.write_text(
        json.dumps(cumulative, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    downloads = {
        "schema_version": "1.0.0",
        "built_at": cumulative["built_at"],
        "summary": cumulative["summary"],
        "instructions": (
            "Download the listed source Release volume for each resource. Several resources "
            "may share one ZIP volume. Identical SHA-256 file bytes are counted only once in "
            "unique_resource_bytes even when they occur in multiple published Releases."
        ),
        "bundles": cumulative["release_bundles"],
    }
    downloads_path.write_text(
        json.dumps(downloads, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return index_path, downloads_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", default="dist/cumulative")
    args = parser.parse_args()
    releases = load_release_inputs(Path(args.input_dir))
    cumulative = merge_published_release_indexes(releases)
    paths = write_cumulative_index(cumulative, Path(args.output_dir))
    print(json.dumps({
        "summary": cumulative["summary"],
        "index_path": str(paths[0]),
        "downloads_path": str(paths[1]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
