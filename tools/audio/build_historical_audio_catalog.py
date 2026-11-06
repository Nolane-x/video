#!/usr/bin/env python3
"""Build an offline searchable audio catalog from the pinned Build 76 Release volumes."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".oga", ".flac", ".m4a", ".aac", ".opus", ".aif", ".aiff"}
MAX_TOTAL_BYTES = 3 * 1024 * 1024 * 1024
MAX_FILE_BYTES = 256 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,channel_layout,bits_per_raw_sample",
        "-show_entries", "format=duration,bit_rate,format_name", "-of", "json", str(path)
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    if result.returncode:
        raise ValueError((result.stderr or "ffprobe failed")[-500:])
    data = json.loads(result.stdout or "{}")
    streams = data.get("streams") or []
    if not streams:
        raise ValueError("No audio stream found")
    stream, fmt = streams[0], data.get("format") or {}
    return {
        "codec": stream.get("codec_name"),
        "sample_rate_hz": int(stream["sample_rate"]) if str(stream.get("sample_rate", "")).isdigit() else None,
        "channels": stream.get("channels"),
        "channel_layout": stream.get("channel_layout"),
        "bits_per_sample": stream.get("bits_per_raw_sample"),
        "duration_seconds": float(fmt["duration"]) if fmt.get("duration") else None,
        "bit_rate_bps": int(fmt["bit_rate"]) if str(fmt.get("bit_rate", "")).isdigit() else None,
        "container": fmt.get("format_name"),
    }


def extract_archives(archive_dir: Path, output_dir: Path) -> list[Path]:
    media_root = output_dir / "media"
    media_root.mkdir(parents=True, exist_ok=True)
    archives = sorted(archive_dir.glob("video-assets-*-audio-*.zip"))
    if not archives:
        raise FileNotFoundError("No audio source archives were downloaded")
    extracted, total = [], 0
    for archive_path in archives:
        match = re.fullmatch(r"video-assets-(.+)-audio-\d+\.zip", archive_path.name)
        if not match:
            raise ValueError("Unknown audio archive name: " + archive_path.name)
        lane = match.group(1)
        with zipfile.ZipFile(archive_path) as archive:
            if len(archive.infolist()) > 100000:
                raise ValueError("Archive member count exceeds safety limit")
            bad = archive.testzip()
            if bad:
                raise ValueError("ZIP CRC failure: " + bad)
            for info in archive.infolist():
                if info.is_dir():
                    continue
                member = PurePosixPath(info.filename)
                if member.is_absolute() or ".." in member.parts or "\\" in info.filename:
                    raise ValueError("Unsafe ZIP path: " + info.filename)
                mode = (info.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK:
                    raise ValueError("ZIP symlinks are not accepted")
                if member.suffix.lower() not in AUDIO_EXTS:
                    continue
                if info.file_size < 1 or info.file_size > MAX_FILE_BYTES:
                    raise ValueError("Audio file outside size limit: " + info.filename)
                relative = member.parts[1:] if member.parts and member.parts[0] == "video-asset-library" else member.parts
                destination = media_root / lane / Path(*relative)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    raise ValueError("Duplicate audio path: " + str(destination))
                total += info.file_size
                if total > MAX_TOTAL_BYTES:
                    raise ValueError("Extracted audio exceeds 3 GiB safety ceiling")
                with archive.open(info) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target, 1024 * 1024)
                if destination.stat().st_size != info.file_size:
                    raise ValueError("Extracted size mismatch: " + info.filename)
                extracted.append(destination)
    return extracted


def load_metadata(manifest_dir: Path) -> dict:
    records = {}
    for file in sorted(manifest_dir.glob("asset-shard--*.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        lane = str(data.get("lane") or file.stem.replace("asset-shard--", ""))
        for item in data.get("assets", []):
            path = str(item.get("path") or "").replace("\\", "/")
            if not path:
                continue
            key = (lane, path)
            if key in records:
                raise ValueError("Duplicate source metadata entry: " + repr(key))
            records[key] = item
    return records


def rights_class(lane: str, license_name: str) -> str:
    if lane == "nasa":
        return "government_media_conditions"
    value = license_name.strip().lower()
    if "cc0" in value or value in {"public domain", "publicdomain", "pdm"}:
        return "public_cc0_pd"
    if lane in {"kenney", "opengameart", "wikimedia", "usgs"}:
        return "item_level_rights_review"
    return "blocked_or_review"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, required=True)
    parser.add_argument("--manifest-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    media_files = extract_archives(args.archive_dir, args.output_dir)
    metadata = load_metadata(args.manifest_dir)
    assets, rejected = [], []
    for path in media_files:
        relative = path.relative_to(args.output_dir / "media").as_posix()
        parts = PurePosixPath(relative).parts
        lane = parts[0]
        item_path = PurePosixPath(*parts[1:]).as_posix()
        item = metadata.get((lane, item_path))
        try:
            if not item:
                raise ValueError("No source-shard record; provenance cannot be verified")
            if item.get("redistributable") is not True:
                raise ValueError("Source shard does not mark this media redistributable")
            media = probe(path)
            digest = sha256(path)
            expected = str(item.get("sha256") or "").lower()
            if not expected or digest != expected:
                raise ValueError("SHA-256 missing or differs from source shard")
            license_name = str(item.get("license") or "")
            assets.append({
                "id": str(item.get("id") or f"{lane}-{digest[:16]}"),
                "title": str(item.get("title") or item.get("description") or path.stem),
                "creator": str(item.get("creator") or item.get("artist") or ""),
                "provider": str(item.get("provider") or lane),
                "category": str(item.get("category") or item.get("asset_category") or lane),
                "lane": lane,
                "path": relative,
                "sha256": digest,
                "size_bytes": path.stat().st_size,
                "source_page": item.get("source_page") or item.get("source_landing_url"),
                "license": license_name,
                "license_url": item.get("license_url"),
                "rights_class": rights_class(lane, license_name),
                "redistributable_in_source_record": True,
                "audition_status": "not_auditioned",
                **media,
            })
        except Exception as exc:
            rejected.append({"path": relative, "reason": str(exc)[:500]})

    if not assets:
        raise RuntimeError("No audio passed source metadata, redistribution, checksum and ffprobe validation")
    assets.sort(key=lambda entry: (entry["provider"].lower(), entry["title"].lower()))
    payload = {
        "schema_version": "1.0.0",
        "source_release": "video-asset-library-build-41184526545",
        "summary": {
            "extracted_audio_files": len(media_files),
            "catalogued_audio_files": len(assets),
            "rejected_audio_files": len(rejected),
            "audio_bytes": sum(item["size_bytes"] for item in assets),
            "human_auditioned": 0,
        },
        "assets": assets,
        "rejected": rejected,
        "notice": "Automated index only. Every sound still requires human audition and exact item-level rights review.",
    }
    (args.output_dir / "audio-catalog.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cards = []
    for item in assets:
        esc = html.escape
        source = f'<a href="{esc(item["source_page"], quote=True)}" target="_blank" rel="noreferrer">Source</a>' if item.get("source_page") else ""
        license_link = f'<a href="{esc(item["license_url"], quote=True)}" target="_blank" rel="noreferrer">License</a>' if item.get("license_url") else ""
        search = esc(" ".join(str(item.get(k) or "") for k in ("title", "creator", "provider", "category", "lane", "license")).lower(), quote=True)
        src = esc("media/" + item["path"], quote=True)
        meta = esc(f'{item.get("codec")} · {item.get("sample_rate_hz")} Hz · {item.get("channels")} ch · {item.get("duration_seconds")} s')
        cards.append(
            f'<article class="card" data-search="{search}"><b>{esc(item["title"])}</b>'
            f'<p>{esc(item["provider"])} · {esc(item["category"])} · {esc(item["rights_class"])}</p>'
            f'<p>{meta}</p><audio controls preload="none" src="{src}"></audio>'
            f'<p>Not auditioned · {source} {license_link}</p></article>'
        )
    page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nolane Historical Audio Catalog</title><style>
body{font:15px system-ui;background:#111820;color:#eef3f7;margin:24px}input{box-sizing:border-box;width:100%;padding:12px;margin:14px 0;background:#202b35;color:inherit;border:1px solid #52616e;border-radius:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}.card{background:#1c2832;border:1px solid #3e4d58;border-radius:10px;padding:14px;min-width:0}
p{font-size:12px;color:#c1ccd4;overflow-wrap:anywhere}audio{width:100%}a{color:#9addd0}.hidden{display:none}.notice{padding:12px;border-left:3px solid #d7aa57}
</style><h1>Nolane Historical Audio Library</h1><p id="count"></p><div class="notice">Automated metadata catalog only. All sounds are marked NOT AUDITIONED. Verify exact item-level rights and listen before production. NASA media uses its specific government-media conditions; it is not labelled CC0.</div>
<input id="q" type="search" placeholder="Search title, creator, source, category or license"><div class="grid" id="grid">""" + "".join(cards) + """</div><script>
const q=document.getElementById('q'),cards=[...document.querySelectorAll('.card')];
function update(){let n=0;const s=q.value.toLowerCase();for(const c of cards){const ok=c.dataset.search.includes(s);c.classList.toggle('hidden',!ok);if(ok)n++}document.getElementById('count').textContent=n+' / '+cards.length+' audio files';}
q.addEventListener('input',update);update();
</script></html>"""
    (args.output_dir / "ASSET_CATALOG.html").write_text(page, encoding="utf-8")
    (args.output_dir / "README.md").write_text(
        "# Historical Audio Library\n\nOpen ASSET_CATALOG.html in a browser for offline search and preview. "
        "All files are marked not auditioned until a human listens to them. Read audio-catalog.json for provenance, rights and hashes.\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["summary"], indent=2))
    print(f"Rejected: {len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
