#!/usr/bin/env python3
"""Build a searchable, per-item-rights audio catalog from the existing Build 76 release.

Downloads source archives only to a temporary runner directory. It never commits
or republishes audio binaries. Unknown/ambiguous rights remain review_required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

REPO = "Nolane-x/video"
RELEASE_TAG = "video-asset-library-build-41184526545"
RELEASE_API = f"https://api.github.com/repos/{REPO}/releases/tags/{RELEASE_TAG}"
ASSET_INDEX_NAME = "ASSET_INDEX.json"
AUDIO_EXTENSIONS = {".wav", ".wave", ".mp3", ".ogg", ".oga", ".flac", ".aiff", ".aif", ".m4a", ".aac", ".opus"}
PATH_KEYS = ("path", "file_path", "relative_path", "asset_path", "archive_path", "member", "filename", "file")
LICENSE_KEYS = ("license", "license_id", "license_spdx", "spdx_id", "license_name", "usage_rights", "rights")
SOURCE_KEYS = ("source_url", "source_page", "original_url", "file_url", "download_url", "url")
ATTRIBUTION_KEYS = ("attribution", "attribution_text", "credit", "creator", "author")
HASH_KEYS = ("sha256", "file_sha256", "checksum_sha256")


def request_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "Nolane-Audio-Library-Indexer/1.0", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.loads(response.read())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def download_verified(url: str, destination: Path, expected_bytes: int | None = None) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and (expected_bytes is None or destination.stat().st_size == expected_bytes):
        return {"path": str(destination), "bytes": destination.stat().st_size, "sha256": sha256_file(destination), "cached": True}
    temp = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    total = 0
    req = urllib.request.Request(url, headers={"User-Agent": "Nolane-Audio-Library-Indexer/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=180) as response, temp.open("wb") as out:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                out.write(block)
                digest.update(block)
                total += len(block)
        if expected_bytes is not None and total != expected_bytes:
            raise ValueError(f"Size mismatch for {destination.name}: expected {expected_bytes}, got {total}")
        temp.replace(destination)
        return {"path": str(destination), "bytes": total, "sha256": digest.hexdigest(), "cached": False}
    except Exception:
        temp.unlink(missing_ok=True)
        raise


def walk_dicts(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_dicts(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_dicts(value)


def first_string(record: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            for nested_key in ("name", "id", "url", "spdx_id", "value"):
                nested = value.get(nested_key)
                if isinstance(nested, str) and nested.strip():
                    return nested.strip()
    return None


def normalize_path(value: str) -> str:
    value = value.replace("\\", "/").strip().lstrip("./")
    return re.sub(r"/+", "/", value).casefold()


def is_audio_path(value: str) -> bool:
    return Path(value.split("?", 1)[0]).suffix.casefold() in AUDIO_EXTENSIONS


def rights_status(license_value: str | None, explicit_redistributable: Any) -> str:
    text = (license_value or "").strip().casefold()
    if explicit_redistributable is False:
        return "source_only_or_not_redistributable"
    if any(term in text for term in ("nasa media usage guidelines", "nasa media usage", "agency media usage guidelines")):
        return "source_specific_review_required"
    if any(term in text for term in ("noncommercial", "non-commercial", "cc-by-nc", "cc by-nc", "no derivatives", "no-derivatives", "cc-by-nd", "cc by-nd")):
        return "not_approved_for_default_commercial_use"
    if any(term in text for term in ("cc0", "cc-zero", "public domain", "public-domain")):
        return "redistributable_candidate"
    if any(term in text for term in ("cc-by-sa", "cc by-sa", "cc by sa", "sharealike", "share-alike", "share alike")):
        return "share_alike_required"
    if any(term in text for term in ("cc-by", "cc by", "attribution")):
        return "attribution_required"
    if explicit_redistributable is True:
        return "redistributable_candidate_license_needs_review"
    return "review_required"


def build_asset_registry(index_data: Any) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    by_path: dict[str, dict[str, Any]] = {}
    by_basename: dict[str, list[dict[str, Any]]] = {}
    for record in walk_dicts(index_data):
        path = first_string(record, PATH_KEYS)
        if not path or not is_audio_path(path):
            continue
        lic = first_string(record, LICENSE_KEYS)
        entry = {
            "indexed_path": path,
            "license": lic,
            "source_url": first_string(record, SOURCE_KEYS),
            "attribution_text": first_string(record, ATTRIBUTION_KEYS),
            "sha256": first_string(record, HASH_KEYS),
            "redistributable": record.get("redistributable"),
            "rights_status": rights_status(lic, record.get("redistributable")),
        }
        by_path[normalize_path(path)] = entry
        by_basename.setdefault(Path(path).name.casefold(), []).append(entry)
    return by_path, by_basename


def match_rights(member: str, by_path: dict[str, dict[str, Any]], by_basename: dict[str, list[dict[str, Any]]]) -> tuple[dict[str, Any] | None, str]:
    key = normalize_path(member)
    if key in by_path:
        return by_path[key], "exact_path"
    suffix_hits = [v for k, v in by_path.items() if key.endswith("/" + k) or k.endswith("/" + key)]
    unique = {x.get("indexed_path"): x for x in suffix_hits}
    if len(unique) == 1:
        return next(iter(unique.values())), "unique_suffix"
    candidates = by_basename.get(Path(member).name.casefold(), [])
    if len(candidates) == 1:
        return candidates[0], "unique_basename"
    if len(candidates) > 1 or len(unique) > 1:
        return None, "ambiguous"
    return None, "no_index_match"


def zip_audio_inventory(archive_path: Path, archive_name: str, archive_url: str,
                        by_path: dict[str, dict[str, Any]], by_basename: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    total_audio_bytes = 0
    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"Corrupt archive member {bad} in {archive_name}")
        for info in archive.infolist():
            member = info.filename
            if info.is_dir() or not is_audio_path(member):
                continue
            total_audio_bytes += info.file_size
            rights, method = match_rights(member, by_path, by_basename)
            entries.append({
                "asset_id": hashlib.sha256(f"{archive_name}\0{member}".encode("utf-8")).hexdigest()[:20],
                "title": Path(member).stem.replace("_", " ").replace("-", " "),
                "archive_name": archive_name,
                "archive_download_url": archive_url,
                "archive_member": member,
                "compressed_size_bytes": info.compress_size,
                "size_bytes": info.file_size,
                "format": Path(member).suffix.lower().lstrip("."),
                "sha256": rights.get("sha256") if rights else None,
                "source_url": rights.get("source_url") if rights else None,
                "license": rights.get("license") if rights else None,
                "attribution_text": rights.get("attribution_text") if rights else None,
                "rights_status": rights.get("rights_status") if rights else "review_required",
                "rights_match_method": method,
                "auditioned_by_human": False,
                "approved_for_final_mix": False,
                "notes": "Archive inventory only. Human audition and exact license confirmation are required before final use."
            })
    summary = {
        "archive_name": archive_name,
        "archive_size_bytes": archive_path.stat().st_size,
        "archive_sha256": sha256_file(archive_path),
        "audio_member_count": len(entries),
        "audio_uncompressed_bytes": total_audio_bytes,
        "rights_status_counts": dict(Counter(x["rights_status"] for x in entries))
    }
    return entries, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=Path("audio-library/SOURCES.json"))
    parser.add_argument("--download-dir", type=Path, default=Path("/tmp/nolane-audio-library"))
    parser.add_argument("--output", type=Path, default=Path("build/audio-catalog.json"))
    parser.add_argument("--report", type=Path, default=Path("build/AUDIO-LIBRARY-REPORT.md"))
    args = parser.parse_args()

    source_doc = json.loads(args.sources.read_text(encoding="utf-8"))
    release = request_json(RELEASE_API)
    release_assets = {asset["name"]: asset for asset in release.get("assets", [])}
    if release.get("tag_name") != RELEASE_TAG:
        raise ValueError("Unexpected asset-library release tag")

    index_asset = release_assets.get(ASSET_INDEX_NAME)
    if not index_asset:
        raise ValueError(f"Missing {ASSET_INDEX_NAME} in {RELEASE_TAG}")
    index_path = args.download_dir / ASSET_INDEX_NAME
    downloads = [download_verified(index_asset["browser_download_url"], index_path, index_asset["size"])]
    index_data = json.loads(index_path.read_text(encoding="utf-8"))
    by_path, by_basename = build_asset_registry(index_data)

    all_entries: list[dict[str, Any]] = []
    archive_summaries: list[dict[str, Any]] = []
    for source in source_doc["existing_build"]["archives"]:
        name = source["name"]
        asset = release_assets.get(name)
        if not asset:
            raise ValueError(f"Release asset missing: {name}")
        if asset["size"] != source["size_bytes"]:
            raise ValueError(f"Release size changed for {name}: expected {source['size_bytes']}, got {asset['size']}")
        path = args.download_dir / name
        downloads.append(download_verified(asset["browser_download_url"], path, source["size_bytes"]))
        entries, summary = zip_audio_inventory(path, name, asset["browser_download_url"], by_path, by_basename)
        summary["source_family"] = source["source_family"]
        archive_summaries.append(summary)
        all_entries.extend(entries)

    counts = Counter(entry["rights_status"] for entry in all_entries)
    license_counts = Counter(entry.get("license") or "UNKNOWN" for entry in all_entries)
    archive_counts = {item["archive_name"]: item["audio_member_count"] for item in archive_summaries}
    catalog = {
        "schema_version": "1.0.0",
        "generated_from_release": RELEASE_TAG,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_index_records": len(by_path),
        "archive_count": len(archive_summaries),
        "audio_asset_count": len(all_entries),
        "rights_status_counts": dict(counts),
        "license_counts": dict(license_counts),
        "archives": archive_summaries,
        "archive_audio_member_counts": archive_counts,
        "assets": all_entries,
        "policy": {
            "human_audition_required": True,
            "unknown_rights_fail_closed": True,
            "source_only_files_must_not_be_redistributed": True,
            "asset_binaries_are_not_embedded_in_this_catalog": True
        },
        "download_checksums": [{"file": Path(x["path"]).name, "bytes": x["bytes"], "sha256": x["sha256"]} for x in downloads]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Audio library build report", "",
        f"- Source release: {RELEASE_TAG}",
        f"- Audio files indexed: {len(all_entries)}",
        f"- Per-item index records: {len(by_path)}",
        f"- Rights status: {dict(counts)}",
        f"- License values: {dict(license_counts)}",
        f"- Archive counts: {archive_counts}", "",
        "## Archive audit", "",
        "| Archive | Audio files | Audio bytes | SHA-256 |",
        "|---|---:|---:|---|"
    ]
    for summary in archive_summaries:
        lines.append(f"| {summary['archive_name']} | {summary['audio_member_count']} | {summary['audio_uncompressed_bytes']} | {summary['archive_sha256']} |")
    lines.extend([
        "", "## Release gate", "",
        "No audio entry is approved for a final mix by this automated inventory alone. Human audition and exact license review remain mandatory. Unknown or ambiguous asset-index matches are marked review_required."
    ])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"audio_asset_count": len(all_entries), "rights_status_counts": dict(counts), "license_counts": dict(license_counts), "archive_audio_member_counts": archive_counts, "catalog": str(args.output), "report": str(args.report)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
