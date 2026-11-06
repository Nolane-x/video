#!/usr/bin/env python3
"""Extract only rights-cleared audio candidates into an offline, searchable preview bank."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

AUDIO_EXTENSIONS = {".wav", ".wave", ".mp3", ".ogg", ".oga", ".flac", ".aiff", ".aif", ".m4a", ".aac", ".opus"}
MAX_MEMBER_BYTES = 256 * 1024 * 1024


def sha256_stream(stream, destination: Path) -> str:
    digest = hashlib.sha256()
    with destination.open("wb") as output:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
            output.write(block)
    return digest.hexdigest()


def is_cc0_or_public_domain(license_name: str | None) -> bool:
    value = (license_name or "").strip().casefold()
    return "cc0" in value or "cc-zero" in value or value in {"public domain", "public-domain", "pdm"}


def probe_audio(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,channel_layout",
        "-show_entries", "format=duration,bit_rate", "-of", "json", str(path),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
        if result.returncode != 0:
            return {"probe_status": "failed", "probe_error": (result.stderr or "ffprobe failed")[-300:]}
        data = json.loads(result.stdout or "{}")
        streams = data.get("streams") or []
        if not streams:
            return {"probe_status": "no_audio_stream"}
        stream = streams[0]
        media_format = data.get("format") or {}
        return {
            "probe_status": "ok",
            "codec": stream.get("codec_name"),
            "sample_rate_hz": int(stream["sample_rate"]) if str(stream.get("sample_rate", "")).isdigit() else None,
            "channels": stream.get("channels"),
            "channel_layout": stream.get("channel_layout"),
            "duration_seconds": float(media_format["duration"]) if media_format.get("duration") else None,
            "bit_rate_bps": int(media_format["bit_rate"]) if str(media_format.get("bit_rate", "")).isdigit() else None,
        }
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        return {"probe_status": "failed", "probe_error": str(exc)[:300]}


def safe_member_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or "\\" in raw:
        raise ValueError("unsafe archive member path")
    return path


def extract_preview_bank(catalog: dict[str, Any], download_dir: Path, output_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    media_dir = output_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    archive_names = sorted({str(item["archive_name"]) for item in catalog.get("assets", []) if item.get("rights_status") == "redistributable_candidate"})
    opened: dict[str, zipfile.ZipFile] = {}
    extracted: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    try:
        for name in archive_names:
            archive_path = download_dir / name
            if not archive_path.is_file():
                raise FileNotFoundError(f"Missing downloaded source pack: {archive_path}")
            archive = zipfile.ZipFile(archive_path)
            bad = archive.testzip()
            if bad:
                archive.close()
                raise ValueError(f"ZIP CRC failure in {name}: {bad}")
            opened[name] = archive

        for item in catalog.get("assets", []):
            if item.get("rights_status") != "redistributable_candidate":
                continue
            asset_id = str(item.get("asset_id") or "")
            archive_name = str(item.get("archive_name") or "")
            member_name = str(item.get("archive_member") or "")
            if not asset_id or asset_id in seen_ids:
                rejected.append({"asset_id": asset_id, "reason": "missing or duplicate asset id"})
                continue
            seen_ids.add(asset_id)
            license_name = str(item.get("license") or "")
            if not is_cc0_or_public_domain(license_name):
                rejected.append({"asset_id": asset_id, "reason": "candidate status without explicit CC0/Public Domain license"})
                continue
            if item.get("rights_match_method") not in {"exact_path", "unique_suffix"}:
                rejected.append({"asset_id": asset_id, "reason": "source manifest match is not exact/unique-suffix"})
                continue
            archive = opened.get(archive_name)
            if archive is None:
                rejected.append({"asset_id": asset_id, "reason": "source archive not opened"})
                continue
            try:
                safe_member_path(member_name)
                info = archive.getinfo(member_name)
                if info.is_dir():
                    raise ValueError("member is a directory")
                if ((info.external_attr >> 16) & 0o170000) == stat.S_IFLNK:
                    raise ValueError("symlink member rejected")
                suffix = Path(member_name).suffix.casefold()
                if suffix not in AUDIO_EXTENSIONS:
                    raise ValueError("unsupported audio extension")
                if info.file_size < 1 or info.file_size > MAX_MEMBER_BYTES:
                    raise ValueError("audio file outside size limit")
                destination = media_dir / f"{asset_id}{suffix}"
                with archive.open(info) as source:
                    computed_sha = sha256_stream(source, destination)
                expected_sha = str(item.get("sha256") or "").strip().lower()
                if expected_sha and computed_sha != expected_sha:
                    destination.unlink(missing_ok=True)
                    raise ValueError("per-file SHA-256 does not match source manifest")
                probe = probe_audio(destination)
                if probe.get("probe_status") != "ok":
                    destination.unlink(missing_ok=True)
                    raise ValueError("ffprobe rejected source audio: " + str(probe.get("probe_error") or probe.get("probe_status")))
                output_item = dict(item)
                output_item.update({
                    "preview_path": f"media/{destination.name}",
                    "computed_sha256": computed_sha,
                    "source_sha256_verified": bool(expected_sha),
                    "auditioned_by_human": False,
                    "approved_for_final_mix": False,
                    **probe,
                })
                extracted.append(output_item)
            except (KeyError, OSError, ValueError, zipfile.BadZipFile) as exc:
                rejected.append({"asset_id": asset_id, "reason": str(exc)[:500]})
    finally:
        for archive in opened.values():
            archive.close()

    if not extracted:
        raise RuntimeError("No CC0/Public Domain preview audio passed extraction and validation")
    return extracted, rejected


def write_catalog(output_dir: Path, assets: list[dict[str, Any]], rejected: list[dict[str, str]]) -> None:
    payload = {
        "schema_version": "1.0.0",
        "source_release": "video-asset-library-build-41184526545",
        "summary": {
            "playable_audio_files": len(assets),
            "total_audio_bytes": sum(int(item["size_bytes"]) for item in assets),
            "human_auditioned": 0,
            "approved_for_final_mix": 0,
            "rejected_or_skipped": len(rejected),
        },
        "assets": assets,
        "rejected_or_skipped": rejected,
        "policy": "CC0/Public Domain candidates only. Human audition and project-specific review remain mandatory.",
    }
    (output_dir / "preview-catalog.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cards = []
    for item in assets:
        esc = html.escape
        title = esc(str(item.get("title") or Path(item["archive_member"]).stem))
        archive = esc(str(item.get("archive_name") or ""))
        member = esc(str(item.get("archive_member") or ""))
        creator = esc(str(item.get("attribution_text") or "Creator/credit not present in catalog"))
        license_name = esc(str(item.get("license") or "CC0/Public Domain candidate"))
        source_url = item.get("source_url")
        source_link = f'<a href="{esc(str(source_url), quote=True)}" target="_blank" rel="noreferrer">Source record</a>' if source_url else ""
        preview = esc(str(item["preview_path"]), quote=True)
        duration = item.get("duration_seconds")
        duration_text = f"{float(duration):.2f}s" if isinstance(duration, (int, float)) else "duration unknown"
        tech = esc(f'{item.get("codec") or "audio"} · {item.get("sample_rate_hz") or "—"} Hz · {item.get("channels") or "—"} ch · {duration_text}')
        search = esc(" ".join(str(item.get(k) or "") for k in ("title", "archive_name", "archive_member", "license", "attribution_text", "source_url")).casefold(), quote=True)
        cards.append(
            f'<article class="card" data-search="{search}">'
            f'<div class="title">{title}</div><div class="meta">{archive}</div>'
            f'<div class="meta">{member}</div><div class="meta">{license_name} · {creator}</div>'
            f'<audio controls preload="none" src="{preview}"></audio>'
            f'<div class="meta">{tech}</div><div class="meta">NOT AUDITIONED · NOT APPROVED FOR FINAL MIX · {source_link}</div>'
            f'</article>'
        )

    page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nolane Audio Preview Bank</title><style>
:root{color-scheme:dark}body{font:15px system-ui;background:#101820;color:#eef3f7;margin:24px}h1{margin:0 0 8px}.note{max-width:1000px;padding:12px;border-left:3px solid #d7aa57;background:#202a32;color:#dbe4ea;margin:16px 0}
#q{box-sizing:border-box;width:100%;padding:12px;background:#202b35;color:inherit;border:1px solid #52616e;border-radius:8px;margin:10px 0 16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}.card{background:#1c2832;border:1px solid #3e4d58;border-radius:10px;padding:14px;min-width:0}.title{font-weight:700;overflow-wrap:anywhere}.meta{font-size:12px;color:#becbd5;margin:5px 0;overflow-wrap:anywhere}audio{width:100%;margin:8px 0}a{color:#9addd0}.hidden{display:none}
</style><h1>Nolane Audio Preview Bank</h1><p id="count"></p><div class="note">Only exact CC0/Public Domain candidates with a matched source record are included. All files are still marked NOT AUDITIONED and NOT APPROVED FOR FINAL MIX. Listen to every selected cue and verify its item-level license and attribution before production use.</div>
<input id="q" type="search" placeholder="Search weapon, footsteps, horse, rain, crowd, music, creator, filename..."><div class="grid" id="grid">""" + "".join(cards) + """</div><script>
const q=document.getElementById('q'),cards=[...document.querySelectorAll('.card')];
function update(){let shown=0;const term=q.value.toLowerCase();for(const card of cards){const ok=card.dataset.search.includes(term);card.classList.toggle('hidden',!ok);if(ok)shown++}document.getElementById('count').textContent=shown+' / '+cards.length+' playable recordings'}
q.addEventListener('input',update);update();
</script></html>"""
    (output_dir / "AUDIO_PREVIEW_BANK.html").write_text(page, encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# Nolane Audio Preview Bank\n\n"
        "Open AUDIO_PREVIEW_BANK.html locally in a modern browser. Use the search field to filter by filename, source or metadata, then play a candidate directly.\n\n"
        "This package includes only CC0/Public Domain candidates that matched the source manifest by exact path or unique suffix. Every file remains NOT AUDITIONED and NOT APPROVED FOR FINAL MIX until a human checks the recording and item-level rights.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("audio-library/generated/audio-catalog.json"))
    parser.add_argument("--download-dir", type=Path, default=Path("/tmp/nolane-audio-library"))
    parser.add_argument("--output-dir", type=Path, default=Path("build/audio-preview-bank"))
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    assets, rejected = extract_preview_bank(catalog, args.download_dir, args.output_dir)
    write_catalog(args.output_dir, assets, rejected)
    summary = {
        "playable_audio_files": len(assets),
        "audio_bytes": sum(int(item["size_bytes"]) for item in assets),
        "rejected_or_skipped": len(rejected),
        "human_auditioned": 0,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
