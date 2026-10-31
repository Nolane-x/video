#!/usr/bin/env python3
"""Package a large video asset library into size-safe, independently downloadable ZIP bundles."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

# GitHub Release assets must stay below 2 GiB. The lower limit leaves a wide margin
# for ZIP headers, compression behavior and future changes in the release service.
MAX_BUNDLE_UNCOMPRESSED_BYTES = 1_700_000_000
MAX_RELEASE_ASSET_BYTES = 1_900_000_000
METADATA_FILES = {
    "ASSET_INDEX.json",
    "ASSET_CATALOG.html",
    "SOURCES_AND_LICENSES.md",
    "SHA256SUMS.txt",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def classify_asset(asset: dict) -> str:
    asset_type = str(asset.get("type", "")).lower()
    category = str(asset.get("category", "")).lower()
    path = str(asset.get("path", "")).lower()
    extension = Path(path).suffix.lower()
    if "font" in asset_type or extension in {".ttf", ".otf", ".woff", ".woff2"}:
        return "typography"
    if asset_type in {"original-video-sticker", "original-meme-layout-template", "original-caption-overlay"}:
        return "original-graphics"
    if "openmoji" in asset_type or path.startswith("third-party/openmoji/"):
        return "original-graphics"
    if asset_type.startswith("kenney-godot-splashscreens-") or "kenney/godot-splashscreens" in path:
        return "original-graphics"
    if asset_type.startswith("blender-demo-cc0-"):
        return "3d-models"
    if asset_type.startswith("lazytextures-models-"):
        return "3d-models"
    if asset_type.startswith(("lazytextures-materials-", "lazytextures-hdris-", "lazytextures-textures-")):
        return "3d-textures"
    if asset_type.startswith("lazytextures-other-"):
        return "miscellaneous"
    if "texture" in asset_type or "texture" in category or "surface" in category:
        return "3d-textures"
    if "video" in asset_type or extension in {".mp4", ".mov", ".m4v", ".webm", ".ogv"}:
        return "footage"
    if "audio" in asset_type or "sfx" in asset_type or "sound" in asset_type or "music" in category or extension in {".wav", ".mp3", ".m4a", ".ogg", ".oga", ".flac"}:
        return "audio"
    if any(term in asset_type for term in ("polyhaven", "ambientcg")):
        if extension in {".blend", ".obj", ".fbx", ".glb", ".gltf", ".dae", ".stl", ".abc", ".usd", ".usdz"}:
            return "3d-models"
        return "3d-textures"
    if "opengameart-cc0-3d" in asset_type or "opengameart-cc0-textures" in asset_type:
        return "3d-textures"
    if "opengameart-cc0-2d" in asset_type:
        return "original-graphics"
    if any(term in asset_type for term in ("photograph", "image", "photo", "public-domain-image", "cc0-image")):
        return "photography"
    if extension in {".blend", ".obj", ".fbx", ".glb", ".gltf", ".dae", ".stl", ".abc", ".usd", ".usdz"}:
        return "3d-models"
    if asset_type.startswith("original-") or "sticker" in asset_type or "meme" in asset_type or "caption" in asset_type:
        return "original-graphics"
    if "svg" in asset_type or extension == ".svg":
        return "vector-graphics"
    if extension in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"}:
        return "photography"
    return "miscellaneous"


def classify_unindexed_path(relative_path: str) -> str:
    path = relative_path.lower().replace("\\", "/")
    if "/lazytextures/models/" in path:
        return "3d-models"
    if "/lazytextures/other/" in path:
        return "miscellaneous"
    if "/lazytextures/" in path:
        return "3d-textures"
    if "/kenney/godot-splashscreens/" in path:
        return "original-graphics"
    if "/poly-pizza/" in path:
        return "3d-models"
    if "google-fonts" in path:
        return "typography"
    if "ambientcg" in path or "polyhaven" in path:
        return "3d-textures"
    if "opengameart" in path and ("sfx" in path or "music" in path):
        return "audio"
    if "video-loops" in path:
        return "footage"
    if "sfx" in path or "audio" in path:
        return "audio"
    if "noaa" in path and ("video" in path or path.endswith((".mp4", ".mov"))):
        return "footage"
    if "illustrations" in path or "stickers" in path or "meme" in path or "caption" in path or "overlays" in path or "icons" in path or "backgrounds" in path:
        return "original-graphics"
    if "textures" in path:
        return "3d-textures"
    return "miscellaneous"


def _write_zip(destination: Path, root: Path, relatives: list[str]) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    raw_size = 0
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as archive:
        for rel in sorted(relatives):
            source = root / rel
            if not source.is_file():
                raise FileNotFoundError(f"bundle entry disappeared: {source}")
            size = source.stat().st_size
            raw_size += size
            if size > MAX_BUNDLE_UNCOMPRESSED_BYTES:
                raise RuntimeError(f"single asset exceeds safe bundle size: {rel} ({size} bytes)")
            archive.write(source, (PurePosixPath("video-asset-library") / PurePosixPath(rel)).as_posix())
    archive_size = destination.stat().st_size
    if archive_size >= MAX_RELEASE_ASSET_BYTES:
        raise RuntimeError(f"bundle exceeds the release safety ceiling after compression: {destination.name} ({archive_size} bytes)")
    return {
        "name": destination.name,
        "sha256": sha256_file(destination),
        "archive_bytes": archive_size,
        "uncompressed_bytes": raw_size,
        "file_count": len(relatives),
        "paths": sorted(relatives),
    }


def _chunk_group(paths: list[str], root: Path) -> list[list[str]]:
    chunks = []
    current = []
    current_bytes = 0
    for rel in sorted(paths):
        size = (root / rel).stat().st_size
        if size > MAX_BUNDLE_UNCOMPRESSED_BYTES:
            raise RuntimeError(f"single resource is larger than the safe bundle target: {rel} ({size} bytes)")
        if current and current_bytes + size > MAX_BUNDLE_UNCOMPRESSED_BYTES:
            chunks.append(current)
            current = []
            current_bytes = 0
        current.append(rel)
        current_bytes += size
    if current:
        chunks.append(current)
    return chunks


def package_library(output_dir: Path) -> dict:
    output_dir = Path(output_dir).resolve()
    root = output_dir / "video-asset-library"
    if not root.is_dir():
        raise FileNotFoundError(f"library directory does not exist: {root}")
    index_path = root / "ASSET_INDEX.json"
    if not index_path.is_file():
        raise FileNotFoundError(f"library index is missing: {index_path}")
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assets = index.get("assets")
    if not isinstance(assets, list):
        raise RuntimeError("ASSET_INDEX.json does not contain an assets array")

    asset_by_path = {}
    for asset in assets:
        rel = asset.get("path")
        if not isinstance(rel, str):
            raise RuntimeError("an indexed asset has no relative path")
        if rel in asset_by_path:
            raise RuntimeError(f"duplicate indexed resource path: {rel}")
        if not (root / rel).is_file():
            raise FileNotFoundError(f"indexed resource is missing: {rel}")
        asset_by_path[rel] = asset

    actual_files = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "ASSET_BUNDLES.json"
    )
    missing_indexed = set(asset_by_path) - set(actual_files)
    if missing_indexed:
        raise RuntimeError(f"indexed resources are missing from disk: {sorted(missing_indexed)[:5]}")
    if not METADATA_FILES.issubset(actual_files):
        raise RuntimeError("one or more required library metadata files are missing")

    metadata = [rel for rel in actual_files if rel in METADATA_FILES]
    resource_paths = [rel for rel in actual_files if rel not in METADATA_FILES]
    total_uncompressed = sum((root / rel).stat().st_size for rel in actual_files)
    for old in output_dir.glob("video-assets-*.zip"):
        old.unlink()
    legacy_archive = output_dir / "video-asset-library.zip"
    if legacy_archive.exists():
        legacy_archive.unlink()

    built_at = index.get("built_at", "")
    bundle_rows = []
    if total_uncompressed <= MAX_BUNDLE_UNCOMPRESSED_BYTES:
        # Keep the familiar one-click archive for compact releases.
        row = _write_zip(legacy_archive, root, actual_files)
        row["category"] = "complete-library"
        row["asset_count"] = len(assets)
        bundle_rows.append(row)
        mode = "single-archive"
        instructions = (
            "# Video Asset Library — download instructions\n\n"
            "This build fits in one ZIP. Download video-asset-library.zip and extract it. "
            "The extracted video-asset-library/ folder contains the searchable offline catalog, "
            "asset index, source/rights notes, and all indexed resources.\n"
        )
    else:
        mode = "multi-volume"
        groups: dict[str, list[str]] = {}
        for rel in resource_paths:
            group = classify_asset(asset_by_path[rel]) if rel in asset_by_path else classify_unindexed_path(rel)
            groups.setdefault(group, []).append(rel)

        meta_row = _write_zip(output_dir / "video-assets-catalog.zip", root, metadata)
        meta_row["category"] = "catalog-and-metadata"
        meta_row["asset_count"] = 0
        bundle_rows.append(meta_row)

        for category, paths in sorted(groups.items()):
            for chunk_no, chunk in enumerate(_chunk_group(paths, root), start=1):
                filename = f"video-assets-{category}-{chunk_no:03d}.zip"
                row = _write_zip(output_dir / filename, root, chunk)
                row["category"] = category
                row["asset_count"] = sum(rel in asset_by_path for rel in chunk)
                bundle_rows.append(row)

        instructions = (
            "# Video Asset Library — multi-volume download instructions\n\n"
            "This release is larger than a safe single-file archive. Download ASSET_BUNDLES.json "
            "to see every volume, size and SHA-256. Download video-assets-catalog.zip first; it "
            "contains ASSET_INDEX.json, ASSET_CATALOG.html, SOURCES_AND_LICENSES.md and "
            "SHA256SUMS.txt. Then download the resource ZIP volumes you need. Extract every "
            "selected volume into the same parent folder so the video-asset-library/ paths merge. "
            "Do not rename folders inside the archives. The files are split by media family and "
            "numbered when a family needs more than one volume. Run the SHA-256 checks in "
            "SHA256SUMS.txt after all required volumes have been extracted.\n"
        )

    manifest = {
        "schema_version": "1.0.0",
        "built_at": built_at,
        "mode": mode,
        "max_uncompressed_bundle_bytes": MAX_BUNDLE_UNCOMPRESSED_BYTES,
        "max_release_asset_bytes": MAX_RELEASE_ASSET_BYTES,
        "total_uncompressed_bytes": total_uncompressed,
        "indexed_asset_count": len(assets),
        "indexed_resource_bytes": sum((root / rel).stat().st_size for rel in asset_by_path),
        "bundle_count": len(bundle_rows),
        "bundles": bundle_rows,
        "extraction_root": "video-asset-library/",
        "metadata_files": sorted(METADATA_FILES),
    }
    (output_dir / "ASSET_BUNDLES.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "BUNDLE_INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")

    summary = index.get("summary", {})
    bundle_lines = "\n".join(
        f"- {row['name']}: {row['archive_bytes']} bytes; {row['file_count']} files; sha256={row['sha256']}"
        for row in bundle_rows
    )
    build_text = (
        f"built_at={built_at}\nmode={mode}\nbundle_count={len(bundle_rows)}\n"
        f"total_uncompressed_bytes={total_uncompressed}\n"
        f"indexed_asset_count={len(assets)}\nsummary={json.dumps(summary, ensure_ascii=False)}\n\n"
        f"bundles:\n{bundle_lines}\n"
    )
    (output_dir / "VIDEO_ASSET_LIBRARY_BUILD.txt").write_text(build_text, encoding="utf-8")

    verify_manifest(output_dir, root, manifest)
    print(json.dumps({
        "mode": mode,
        "total_uncompressed_bytes": total_uncompressed,
        "indexed_asset_count": len(assets),
        "bundle_count": len(bundle_rows),
        "bundles": [{k: row[k] for k in ("name", "category", "archive_bytes", "uncompressed_bytes", "file_count", "sha256") if k in row} for row in bundle_rows],
    }, ensure_ascii=False, indent=2))
    return manifest


def verify_manifest(output_dir: Path, root: Path, manifest: dict) -> None:
    output_dir = Path(output_dir)
    root = Path(root)
    included = []
    for row in manifest.get("bundles", []):
        path = output_dir / row["name"]
        if not path.is_file():
            raise FileNotFoundError(f"release bundle missing: {path}")
        size = path.stat().st_size
        if size >= MAX_RELEASE_ASSET_BYTES:
            raise RuntimeError(f"release bundle exceeds safe GitHub asset size: {path.name}")
        if sha256_file(path) != row.get("sha256"):
            raise RuntimeError(f"release bundle SHA-256 mismatch: {path.name}")
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise RuntimeError(f"ZIP integrity failure: {path.name}")
            names = set(archive.namelist())
            for rel in row.get("paths", []):
                archive_path = (PurePosixPath("video-asset-library") / PurePosixPath(rel)).as_posix()
                if archive_path not in names:
                    raise RuntimeError(f"{path.name} does not contain {archive_path}")
                included.append(rel)
    if manifest.get("mode") == "single-archive":
        expected = sorted(
            p.relative_to(root).as_posix()
            for p in root.rglob("*")
            if p.is_file() and p.name != "ASSET_BUNDLES.json"
        )
    else:
        expected = sorted(
            [p.relative_to(root).as_posix() for p in root.rglob("*")
             if p.is_file() and p.name not in METADATA_FILES and p.name != "ASSET_BUNDLES.json"]
            + list(METADATA_FILES)
        )
    if sorted(included) != expected:
        duplicates = sorted({p for p in included if included.count(p) > 1})
        missing = sorted(set(expected) - set(included))
        extra = sorted(set(included) - set(expected))
        raise RuntimeError(f"bundle coverage mismatch; missing={missing[:6]}, extra={extra[:6]}, duplicates={duplicates[:6]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", default="dist/video-assets")
    parser.add_argument("--verify-only", action="store_true", help="verify existing ASSET_BUNDLES.json and its ZIP files")
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    root = output_dir / "video-asset-library"
    if args.verify_only:
        manifest = json.loads((output_dir / "ASSET_BUNDLES.json").read_text(encoding="utf-8"))
        verify_manifest(output_dir, root, manifest)
        print(f"[Package] verified {manifest['bundle_count']} bundle(s), mode={manifest['mode']}")
    else:
        package_library(output_dir)


if __name__ == "__main__":
    main()
