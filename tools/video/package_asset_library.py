#!/usr/bin/env python3
"""Build independently downloadable, checksummed resource packs from ASSET_INDEX.json."""
from __future__ import annotations
import hashlib, json, shutil, sys, zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath

MAX_PART_RAW_BYTES = 480 * 1024 * 1024
MAX_PART_ZIP_BYTES = 650 * 1024 * 1024
LEGACY_FULL_ZIP_LIMIT = 1500 * 1024 * 1024

GROUP_INFO = {
    "stickers-memes": ("Stickers, reaction graphics and editable meme templates", "Original CC0 transparent SVG stickers and reusable meme layouts"),
    "original-visual-design": ("Original visual design assets", "Original CC0 backgrounds, overlays, illustrations, infographics, textures and icons"),
    "motion-video-loops": ("Motion graphics and looping video", "Original generated motion loops and reusable video overlays"),
    "audio-sfx-music": ("Audio, sound effects and music", "Procedural sound design and licensed audio packages"),
    "game-art-2d": ("2D game art and sprite packs", "CC0 sprite sheets, tiles, UI assets and 2D illustrations"),
    "game-art-3d": ("3D game art and models", "CC0 3D models, props and environment assets"),
    "3d-models": ("3D models and production assets", "3D models, scene assets and supported exchange formats"),
    "materials-environments": ("PBR materials, HDRI and texture libraries", "Tileable materials, surface maps, decals and environment lighting"),
    "science-footage": ("Science, field footage and documentary media", "Item-rights-verified USGS science photos, video and sound"),
    "public-domain-images": ("Public-domain and open-access photography", "Museum, archive, science and collection images with explicit item-level rights"),
    "typography": ("Fonts and typography", "Font files with their original family license documents"),
    "misc-media": ("Other verified media", "Additional redistributable media and supporting source files"),
}
META_FILES = {"ASSET_INDEX.json", "ASSET_CATALOG.html", "SOURCES_AND_LICENSES.md", "SHA256SUMS.txt", "README.md", "MODULAR_PACKS_INDEX.json"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def group_for_path(rel: str, asset: dict | None = None) -> str:
    p = PurePosixPath(rel)
    low = rel.lower()
    ext = p.suffix.lower()
    asset = asset or {}
    kind = str(asset.get("type") or "").lower()
    provider = str(asset.get("provider") or "").lower()
    category = str(asset.get("asset_category") or "").lower()
    asset_type = str(asset.get("asset_type") or "").lower()

    if low.startswith("originals/stickers/") or low.startswith("originals/meme-templates/"):
        return "stickers-memes"
    if low.startswith("originals/"):
        if "motion" in low or "loops" in low or "video-loop" in kind:
            return "motion-video-loops"
        if "sfx" in low or ext in {".wav", ".mp3", ".ogg", ".oga", ".flac", ".m4a"}:
            return "audio-sfx-music"
        return "original-visual-design"
    if "google-fonts" in low or "google fonts" in provider or ext in {".ttf", ".otf", ".woff", ".woff2"}:
        return "typography"
    if "usgs" in low or "usgs" in provider or "nasa" in low:
        return "science-footage"
    if ext in {".mp4", ".mov", ".m4v", ".webm", ".ogv"}:
        return "science-footage"
    if ext in {".wav", ".mp3", ".ogg", ".oga", ".flac", ".m4a"}:
        return "audio-sfx-music"
    if "opengameart" in low or "opengameart" in provider:
        oga_category = category or (p.parts[2].lower() if len(p.parts) > 2 else "")
        if oga_category == "3d" or "3d" in kind:
            return "game-art-3d"
        if oga_category in {"sfx", "music"}:
            return "audio-sfx-music"
        if oga_category == "textures":
            return "materials-environments"
        if oga_category == "2d":
            return "game-art-2d"
        return "misc-media"
    if "ambientcg" in low:
        if "3dmodel" in asset_type or "3dmodel" in low or ext in {".glb", ".gltf", ".fbx", ".obj", ".blend", ".dae"}:
            return "3d-models"
        return "materials-environments"
    if "polyhaven" in low:
        if "/models/" in low or ext in {".glb", ".gltf", ".fbx", ".obj", ".blend", ".dae"}:
            return "3d-models"
        return "materials-environments"
    if "kenney" in low:
        return "game-art-2d"
    if any(token in low for token in ("met/", "rijksmuseum/", "wikimedia", "loc/", "smithsonian")):
        return "public-domain-images"
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"}:
        return "public-domain-images"
    return "misc-media"


def pack_readme(pack_id: str, title: str, description: str, part: int, parts: int, count: int) -> str:
    return (
        f"# {title}\n\n"
        f"- Pack ID: {pack_id}\n- Part: {part} of {parts}\n- Indexed resources: {count}\n\n"
        f"{description}.\n\n"
        "## Installation\nExtract this ZIP into the asset-library root, keeping the video-asset-library folder paths intact. "
        "Files from different packs can be extracted into the same root; parts are designed to coexist.\n\n"
        "## Integrity and rights\nPACK_SHA256SUMS.txt lists resource-file SHA-256 values. PACK_ASSET_INDEX.json carries "
        "item-level source, license and attribution metadata. Review each item's record and source-specific restrictions "
        "before publishing. A permissive license is not a blanket clearance for trademarks, privacy, publicity, or third-party material.\n"
    )


def package_library(output_dir: Path) -> dict:
    root = output_dir / "video-asset-library"
    index_path = root / "ASSET_INDEX.json"
    if not index_path.is_file():
        raise FileNotFoundError(f"Missing asset index: {index_path}")
    index_doc = json.loads(index_path.read_text(encoding="utf-8"))
    assets = index_doc.get("assets")
    if not isinstance(assets, list):
        raise ValueError("ASSET_INDEX.json has no assets array")

    by_path = {item["path"]: item for item in assets if isinstance(item.get("path"), str)}
    grouped = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if rel not in META_FILES:
                grouped[group_for_path(rel, by_path.get(rel))].append(path)

    packs_dir = output_dir / "packs"
    if packs_dir.exists():
        shutil.rmtree(packs_dir)
    packs_dir.mkdir(parents=True, exist_ok=True)

    pack_records = []
    for group in sorted(grouped):
        title, description = GROUP_INFO.get(group, (group.replace("-", " ").title(), group.replace("-", " ")))
        files = sorted(grouped[group], key=lambda item: item.relative_to(root).as_posix())
        parts, current, current_bytes = [], [], 0
        for path in files:
            size = path.stat().st_size
            if current and current_bytes + size > MAX_PART_RAW_BYTES:
                parts.append(current)
                current, current_bytes = [], 0
            current.append(path)
            current_bytes += size
        if current:
            parts.append(current)

        for part_no, part_files in enumerate(parts, start=1):
            part_id = f"{group}-{part_no:03d}"
            pack_name = f"video-assets-{part_id}.zip"
            pack_path = packs_dir / pack_name
            entries, checksum_lines = [], []
            raw_bytes = 0
            for path in part_files:
                rel = path.relative_to(root).as_posix()
                asset = by_path.get(rel)
                size = path.stat().st_size
                digest = sha256_file(path)
                if asset and asset.get("sha256") and digest != asset["sha256"]:
                    raise RuntimeError(f"ASSET_INDEX SHA-256 mismatch for {rel}")
                entry = dict(asset) if asset else {"path": rel, "title": path.name, "type": "supporting-source-file"}
                entry.update(path=rel, sha256=digest, size_bytes=size)
                entries.append(entry)
                checksum_lines.append(f"{digest}  video-asset-library/{rel}")
                raw_bytes += size

            pack_meta = {
                "schema_version": "1.0.0", "pack_id": part_id, "title": title,
                "description": description, "part": part_no, "parts": len(parts),
                "raw_bytes": raw_bytes, "file_count": len(part_files),
                "asset_count": sum(1 for entry in entries if entry.get("type") != "supporting-source-file"),
                "assets": entries,
            }
            sidecar = f"PACKS/{part_id}"
            with zipfile.ZipFile(pack_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as archive:
                archive.writestr(f"{sidecar}/PACK_README.md", pack_readme(part_id, title, description, part_no, len(parts), len(entries)))
                archive.writestr(f"{sidecar}/PACK_ASSET_INDEX.json", json.dumps(pack_meta, ensure_ascii=False, indent=2) + "\n")
                archive.writestr(f"{sidecar}/PACK_SHA256SUMS.txt", "\n".join(checksum_lines) + "\n")
                source_notes = root / "SOURCES_AND_LICENSES.md"
                if source_notes.is_file():
                    archive.write(source_notes, "video-asset-library/SOURCES_AND_LICENSES.md")
                for path in part_files:
                    archive.write(path, f"video-asset-library/{path.relative_to(root).as_posix()}")
            zip_bytes = pack_path.stat().st_size
            if zip_bytes > MAX_PART_ZIP_BYTES:
                raise RuntimeError(f"Pack exceeded byte ceiling: {pack_name} ({zip_bytes})")
            pack_records.append({
                "pack_id": part_id, "file": f"packs/{pack_name}", "download_name": pack_name,
                "sha256": sha256_file(pack_path), "compressed_bytes": zip_bytes, "raw_bytes": raw_bytes,
                "file_count": len(part_files), "asset_count": pack_meta["asset_count"],
                "part": part_no, "parts": len(parts), "title": title, "description": description,
                "license_types": sorted({str(item.get("license")) for item in entries if item.get("license")}),
                "asset_types": sorted({str(item.get("type")) for item in entries if item.get("type")}),
            })

    archive_path = output_dir / "video-asset-library.zip"
    prior_size = archive_path.stat().st_size if archive_path.is_file() else 0
    legacy_full = prior_size > 0 and prior_size <= LEGACY_FULL_ZIP_LIMIT
    if archive_path.exists() and not legacy_full:
        archive_path.unlink()

    pack_index = {
        "schema_version": "1.0.0", "built_at": index_doc.get("built_at"),
        "repository": index_doc.get("repository"),
        "distribution_mode": "full-library-plus-modular-packs" if legacy_full else "modular-packs-with-catalog-archive",
        "max_part_raw_bytes": MAX_PART_RAW_BYTES, "max_part_zip_bytes": MAX_PART_ZIP_BYTES,
        "legacy_full_archive_bytes": prior_size if legacy_full else 0,
        "pack_count": len(pack_records),
        "total_pack_compressed_bytes": sum(item["compressed_bytes"] for item in pack_records),
        "total_pack_raw_bytes": sum(item["raw_bytes"] for item in pack_records),
        "total_pack_files": sum(item["file_count"] for item in pack_records),
        "packs": pack_records,
    }
    index_file = output_dir / "PACKAGES_INDEX.json"
    index_file.write_text(json.dumps(pack_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "PACKAGES_INDEX.md").write_text(
        "# Modular Video Asset Packs\n\n"
        "Download only the categories needed for a project. Each ZIP is independently checksummed and can be "
        "extracted into the same video-asset-library directory. Large categories are split into parts.\n\n"
        + "\n".join(
            f"- {item['title']} — {item['download_name']} — {item['file_count']} files, "
            f"{item['compressed_bytes'] / (1024*1024):.1f} MiB — SHA-256 {item['sha256']}"
            for item in pack_records
        ) + "\n",
        encoding="utf-8",
    )

    if not legacy_full:
        catalog_files = ["ASSET_INDEX.json", "ASSET_CATALOG.html", "SOURCES_AND_LICENSES.md", "SHA256SUMS.txt"]
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as archive:
            for rel in catalog_files:
                file_path = root / rel
                if file_path.is_file():
                    archive.write(file_path, f"video-asset-library/{rel}")

    # Make the modular manifest available in the expanded library and keep it checksummed.
    mod_index_path = root / "MODULAR_PACKS_INDEX.json"
    mod_index_path.write_text(json.dumps(pack_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sums_path = root / "SHA256SUMS.txt"
    if sums_path.is_file():
        lines = [line for line in sums_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        lines = [line for line in lines if line.split("  ", 1)[1] != "MODULAR_PACKS_INDEX.json"]
        lines.append(f"{sha256_file(mod_index_path)}  MODULAR_PACKS_INDEX.json")
        sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    index_doc["summary"]["modular_pack_count"] = pack_index["pack_count"]
    index_doc["summary"]["modular_pack_compressed_bytes"] = pack_index["total_pack_compressed_bytes"]
    index_doc["summary"]["modular_pack_raw_bytes"] = pack_index["total_pack_raw_bytes"]
    index_doc["distribution"] = {
        "mode": pack_index["distribution_mode"],
        "pack_index": "PACKAGES_INDEX.json",
        "maximum_pack_zip_bytes": MAX_PART_ZIP_BYTES,
    }
    index_path.write_text(json.dumps(index_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (output_dir / "VIDEO_ASSET_LIBRARY_BUILD.txt").open("a", encoding="utf-8") as stream:
        stream.write(
            f"distribution_mode={pack_index['distribution_mode']}\n"
            f"pack_count={pack_index['pack_count']}\n"
            f"total_pack_compressed_bytes={pack_index['total_pack_compressed_bytes']}\n"
            f"total_pack_raw_bytes={pack_index['total_pack_raw_bytes']}\n"
            f"catalog_archive_bytes={archive_path.stat().st_size}\n"
        )
    print(json.dumps({k: v for k, v in pack_index.items() if k != "packs"}, indent=2))
    return pack_index


if __name__ == "__main__":
    package_library(Path(sys.argv[1] if len(sys.argv) > 1 else "dist/video-assets").resolve())
