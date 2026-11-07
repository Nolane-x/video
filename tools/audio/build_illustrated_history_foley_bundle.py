#!/usr/bin/env python3
"""Acquire and package a small, provenance-rich CC0 Foley collection.

Raw media stays out of Git history. Every item remains un-auditioned until a
human listens to it; successful probing is not creative or legal approval.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import stat
import subprocess
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

AUDIO_EXTENSIONS = {".wav", ".wave", ".ogg", ".oga", ".mp3", ".flac", ".m4a", ".aac", ".aiff", ".aif", ".opus"}
USER_AGENT = "Nolane-Video-Illustrated-History-Foley/1.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_zip_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"Unsafe ZIP member path: {item.filename}")
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError(f"ZIP symlink member is not allowed: {item.filename}")
            target = (destination / Path(*name.parts)).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"ZIP member escapes extraction directory: {item.filename}")
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(item) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def download_source(source: dict[str, Any], destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(source["download_url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    size = destination.stat().st_size
    minimum = int(source.get("minimum_bytes", 1))
    if size < minimum:
        raise ValueError(f"{source['source_id']} download too small: {size} < {minimum}")
    digest = sha256_file(destination)
    expected = source.get("expected_sha256")
    if expected and digest.lower() != expected.lower():
        raise ValueError(f"{source['source_id']} SHA-256 mismatch: {digest}")
    return {
        "source_id": source["source_id"],
        "download_url": source["download_url"],
        "download_filename": source["download_filename"],
        "download_size_bytes": size,
        "download_sha256": digest,
        "expected_sha256_pinned": bool(expected),
    }


def extract_source(source: dict[str, Any], archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    kind = source["archive_type"]
    if kind == "7z":
        executable = shutil.which("7z") or shutil.which("7zz")
        if not executable:
            raise RuntimeError("7z/7zz is required to extract OpenGameArt .7z packs")
        subprocess.run(
            [executable, "x", "-y", f"-o{destination}", str(archive_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    elif kind == "zip":
        safe_zip_extract(archive_path, destination)
    elif kind == "file":
        shutil.copy2(archive_path, destination / source["download_filename"])
    else:
        raise ValueError(f"Unsupported archive type: {kind}")

    root = destination.resolve()
    for path in destination.rglob("*"):
        if path.is_file() and not path.resolve().is_relative_to(root):
            raise ValueError(f"Extracted path escapes source directory: {path}")


def probe_audio(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,format_name:stream=codec_name,codec_type,sample_rate,channels,channel_layout,bits_per_sample,bits_per_raw_sample",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = [stream for stream in data.get("streams", []) if stream.get("codec_type") == "audio"]
    if not streams:
        raise ValueError(f"No audio stream detected in {path}")
    stream = streams[0]
    duration = float(data.get("format", {}).get("duration", 0) or 0)
    if duration <= 0:
        raise ValueError(f"Invalid or missing duration for {path}")
    return {
        "duration_seconds": round(duration, 6),
        "container_format": data.get("format", {}).get("format_name"),
        "codec": stream.get("codec_name"),
        "sample_rate_hz": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
        "channels": int(stream["channels"]) if stream.get("channels") is not None else None,
        "channel_layout": stream.get("channel_layout"),
        "bits_per_sample": stream.get("bits_per_sample") or stream.get("bits_per_raw_sample"),
    }


def build_bundle(manifest: dict[str, Any], download_root: Path, output_root: Path, probe=probe_audio) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    package_root = output_root / "package"
    if package_root.exists():
        shutil.rmtree(package_root)
    assets_root = package_root / "assets"
    assets_root.mkdir(parents=True)

    acquisition_records: list[dict[str, Any]] = []
    asset_by_hash: dict[str, dict[str, Any]] = {}
    source_counts: Counter[str] = Counter()

    for source in manifest["sources"]:
        source_id = source["source_id"]
        archive_path = download_root / source_id / source["download_filename"]
        if not archive_path.is_file():
            raise FileNotFoundError(f"Missing acquired source: {archive_path}")
        archive_sha = sha256_file(archive_path)
        expected = source.get("expected_sha256")
        if expected and archive_sha.lower() != expected.lower():
            raise ValueError(f"{source_id} archive SHA-256 mismatch")

        extracted_root = download_root / source_id / "extracted"
        extract_source(source, archive_path, extracted_root)
        acquisition_records.append({
            "source_id": source_id,
            "title": source["title"],
            "creator": source["creator"],
            "source_page": source["source_page"],
            "download_url": source["download_url"],
            "download_filename": source["download_filename"],
            "archive_sha256": archive_sha,
            "archive_size_bytes": archive_path.stat().st_size,
            "license": source["license"],
            "license_url": source["license_url"],
            "rights_class": source["rights_class"],
        })

        for audio_path in sorted(extracted_root.rglob("*")):
            if not audio_path.is_file() or audio_path.suffix.lower() not in AUDIO_EXTENSIONS:
                continue
            if "__MACOSX" in audio_path.parts or audio_path.name.startswith("._") or audio_path.name == ".DS_Store":
                continue
            relative = audio_path.relative_to(extracted_root)
            digest = sha256_file(audio_path)
            if digest in asset_by_hash:
                existing = asset_by_hash[digest]
                if source_id not in existing["source_ids"]:
                    existing["source_ids"].append(source_id)
                continue

            metadata = probe(audio_path)
            rel_posix = PurePosixPath(relative.as_posix())
            target_rel = PurePosixPath("assets") / source_id / rel_posix
            target = package_root.joinpath(*target_rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(audio_path, target)
            source_counts[source_id] += 1
            asset_by_hash[digest] = {
                "asset_id": f"ihf-{digest[:16]}",
                "title": audio_path.stem.replace("_", " ").replace("-", " "),
                "path": target_rel.as_posix(),
                "original_filename": audio_path.name,
                "source_ids": [source_id],
                "creator": source["creator"],
                "source_page": source["source_page"],
                "license": source["license"],
                "license_url": source["license_url"],
                "rights_class": source["rights_class"],
                "sha256": digest,
                "size_bytes": audio_path.stat().st_size,
                **metadata,
                "tags": source.get("tags", []),
                "human_auditioned": False,
                "approved_for_final_mix": False,
                "review_note": "Metadata/codec probe only. Human listening and contextual approval still required.",
            }

    assets = sorted(asset_by_hash.values(), key=lambda item: (item["source_ids"][0], item["original_filename"].lower()))
    if not assets:
        raise RuntimeError("No audio assets were discovered in the acquired source packs")

    catalog = {
        "schema_version": 1,
        "collection": manifest["collection"],
        "release_tag": manifest["release_tag"],
        "generated_by": "tools/audio/build_illustrated_history_foley_bundle.py",
        "assets": assets,
        "summary": {
            "source_count": len(acquisition_records),
            "audio_asset_count": len(assets),
            "source_audio_counts": dict(source_counts),
            "unique_audio_bytes": sum(item["size_bytes"] for item in assets),
            "human_auditioned": 0,
            "approved_for_final_mix": 0,
        },
    }
    (package_root / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_root / "source-register.json").write_text(json.dumps(acquisition_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_root / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme = f"""# {manifest['collection']}

This is a curated CC0 1.0 source pack for historical/illustrated video production.

- Original audio files are preserved in their downloaded formats.
- Per-file source pages, creators, license URLs and SHA-256 hashes are in catalog.json and source-register.json.
- Every item is initially marked human_auditioned=false and approved_for_final_mix=false.
- A successful download and FFprobe check is not a listening/quality approval.
- The crowd file is a creator-edited voice-group effect, not an authentic historical field recording.
- The six-horse file is described as a horse approach-and-pass recording.
- Weapon-impact and generic thwack files must be matched to the material and visual contact, not reused indiscriminately.

Open AUDIO_PREVIEW.html in a browser to audition the extracted files offline. Retain the CC0 and provenance records with the media.
"""
    (package_root / "README.md").write_text(readme, encoding="utf-8")

    rows = []
    for item in assets:
        title = html.escape(item["title"])
        path = html.escape(item["path"], quote=True)
        meta = html.escape(f"{item['duration_seconds']:.2f}s · {item.get('codec') or 'audio'} · {item.get('sample_rate_hz') or '?'} Hz · {item.get('channels') or '?'} ch")
        creator = html.escape(item["creator"])
        search_value = html.escape((title + " " + " ".join(item["tags"])).lower(), quote=True)
        rows.append(f'<article data-search="{search_value}"><h3>{title}</h3><p>{meta}</p><p>Creator: {creator}</p><audio controls preload="none" src="{path}"></audio><p><small>CC0 · Not yet human-auditioned · {html.escape(item["source_ids"][0])}</small></p></article>')
    preview = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Illustrated History Foley Preview</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;background:#111;color:#eee}input{width:100%;padding:.8rem;font:inherit}article{padding:1rem;margin:1rem 0;border:1px solid #444;border-radius:12px}audio{width:100%}small{color:#bbb}</style><h1>Illustrated History Foley — Offline audition</h1><p>Search by cue, then listen to the exact file. None of these entries is pre-approved for a final mix.</p><input id="search" placeholder="Search horse, katana, arrow, crowd, forge…">""" + "".join(rows) + """<script>const q=document.querySelector('#search');q.addEventListener('input',()=>{const v=q.value.toLowerCase();document.querySelectorAll('article').forEach(x=>x.hidden=!x.dataset.search.includes(v))})</script></html>"""
    (package_root / "AUDIO_PREVIEW.html").write_text(preview, encoding="utf-8")

    package_name = f"{manifest['release_tag']}.zip"
    package_path = output_root / package_name
    if package_path.exists():
        package_path.unlink()
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(package_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(package_root).as_posix())

    report = {
        "collection": manifest["collection"],
        "release_tag": manifest["release_tag"],
        "package": package_name,
        "package_size_bytes": package_path.stat().st_size,
        "package_sha256": sha256_file(package_path),
        "source_count": len(acquisition_records),
        "audio_asset_count": len(assets),
        "source_audio_counts": dict(source_counts),
        "human_auditioned": 0,
        "approved_for_final_mix": 0,
        "status": "ACQUIRED_AND_PROBED_NOT_HUMAN_AUDITIONED",
    }
    (output_root / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_root / "SHA256SUMS.txt").write_text(f"{report['package_sha256']}  {package_name}\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--download", action="store_true", help="Download all sources before building")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.download_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.download:
        records = []
        for source in manifest["sources"]:
            destination = args.download_dir / source["source_id"] / source["download_filename"]
            records.append(download_source(source, destination))
        (args.output_dir / "download-manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = build_bundle(manifest, args.download_dir, args.output_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
