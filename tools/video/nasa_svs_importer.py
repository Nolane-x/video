#!/usr/bin/env python3
"""Rights-gated downloader for NASA Scientific Visualization Studio videos."""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://svs.gsfc.nasa.gov"
SEARCH_TERMS = ("Earth", "Moon", "Mars", "Sun", "Ocean", "Climate", "Spacecraft", "Galaxy", "Aurora", "Hurricane", "Volcano", "Asteroid", "Eclipse", "Weather", "Telescope", "Wildfire", "Spaceflight")
MAX_PAGES = 170
MAX_SEARCH_JSON_BYTES = 2 * 1024 * 1024
MAX_PER_TERM = 10
MAX_DOWNLOADS = 36
MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_METADATA_BYTES = 64 * 1024 * 1024
MAX_VIDEO_BYTES = 300 * 1024 * 1024
MAX_TOTAL_BYTES = 4 * 1024 * 1024 * 1024
MIN_VIDEO_BYTES = 20 * 1024
UA = "NolaneVideoAssetLibrary-NASA-SVS/1.0 (+https://github.com/Nolane-x/video)"
VIDEO_EXTS = {".mp4", ".webm", ".mpg"}
MIME = {
    ".mp4": {"video/mp4", "application/mp4", "application/octet-stream", "binary/octet-stream"},
    ".webm": {"video/webm", "application/octet-stream", "binary/octet-stream"},
    ".mpg": {"video/mpeg", "application/octet-stream", "binary/octet-stream"},
}
MUSIC_MARKER = re.compile(
    r"licensed music|music\s+credit|music\s*[:=]|music\s+(?:by|from)\b|"
    r"copyright(?:ed)?\s+(?:music|audio|footage|material)|"
    r"third[- ]party\s+(?:music|audio|footage|content)|used with permission|"
    r"not in the public domain|not public domain|permission required|rights holder|licensed soundtrack",
    re.IGNORECASE,
)


def normalize_svs_media_url(raw_url: str) -> str | None:
    """Upgrade only exact NASA SVS HTTP URLs under /vis/ to HTTPS."""
    try:
        u = urllib.parse.urlsplit(str(raw_url or "").strip())
        if u.scheme.casefold() not in {"http", "https"} or (u.hostname or "").casefold() != "svs.gsfc.nasa.gov":
            return None
        if u.username or u.password or u.port or u.query or u.fragment:
            return None
        path = urllib.parse.unquote(u.path)
        if not path.startswith("/vis/") or ".." in Path(path).parts:
            return None
        if Path(path).suffix.casefold() not in VIDEO_EXTS:
            return None
        return urllib.parse.urlunsplit(("https", "svs.gsfc.nasa.gov", u.path, "", ""))
    except (TypeError, ValueError):
        return None


def iter_video_candidates(page: dict[str, Any]) -> list[dict[str, Any]]:
    rows, seen = [], set()
    main = page.get("main_video")
    if isinstance(main, dict) and str(main.get("media_type") or "").casefold() == "movie":
        url = normalize_svs_media_url(main.get("url", ""))
        if url:
            row = dict(main)
            row["url"] = url
            rows.append(row)
            seen.add(url)
    for group in page.get("media_groups") or []:
        if not isinstance(group, dict):
            continue
        group_text = " ".join(str(group.get(k) or "") for k in ("title", "caption", "description", "notes"))
        for item in group.get("items") or []:
            if not isinstance(item, dict):
                continue
            for key in ("media", "instance"):
                media = item.get(key)
                if not isinstance(media, dict) or str(media.get("media_type") or "").casefold() != "movie":
                    continue
                url = normalize_svs_media_url(media.get("url", ""))
                if not url or url in seen:
                    continue
                row = dict(media)
                row.update({"url": url, "group_caption": str(item.get("caption") or group.get("caption") or "")[:1500],
                            "group_description": group_text[:2500]})
                rows.append(row)
                seen.add(url)
    return rows


def page_rights_exception_markers(page: dict[str, Any]) -> list[str]:
    fields = []
    for key in ("title", "description", "notes", "usage_notes", "copyright", "rights",
                "music_notes", "music", "soundtrack", "audio_notes"):
        value = page.get(key)
        if isinstance(value, str) and value.strip():
            fields.append(value)
    main_video = page.get("main_video")
    if isinstance(main_video, dict):
        fields.extend(str(main_video.get(k) or "") for k in ("alt_text", "caption", "notes", "copyright"))
    for group in page.get("media_groups") or []:
        if not isinstance(group, dict):
            continue
        fields.extend(str(group.get(k) or "") for k in ("title", "caption", "description", "notes"))
        for item in group.get("items") or []:
            if not isinstance(item, dict):
                continue
            fields.extend(str(item.get(k) or "") for k in ("title", "caption"))
            for key in ("media", "instance"):
                media = item.get(key)
                if isinstance(media, dict):
                    fields.extend(str(media.get(k) or "") for k in ("alt_text", "caption", "notes", "copyright"))
    for credit in page.get("credits") or []:
        if isinstance(credit, dict) and any(x in str(credit.get("role") or "").casefold() for x in ("music", "soundtrack")):
            fields.append("music credit role: " + str(credit.get("role") or ""))
    return sorted({m.group(0).casefold() for m in MUSIC_MARKER.finditer("\n".join(fields))})


def _has_audio_track(value: Any) -> bool:
    return value not in (None, False, "", [], {})


def _score(media: dict[str, Any]) -> tuple[int, int, int]:
    try:
        pixels = max(0, int(media.get("width") or 0)) * max(0, int(media.get("height") or 0))
    except (TypeError, ValueError):
        pixels = 0
    ext = Path(urllib.parse.urlsplit(media.get("url", "")).path).suffix.casefold()
    return pixels, {".mp4": 3, ".webm": 2, ".mpg": 1}.get(ext, 0), int(not _has_audio_track(media.get("audio_track")))


def choose_video_candidate(page: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    if str(page.get("page_type") or "").casefold() != "visualization":
        return None, "not-visualization"
    if str(page.get("progress") or "").casefold() != "complete":
        return None, "not-complete"
    if str(page.get("studio") or "").casefold() != "svs":
        return None, "not-svs-studio"
    markers = page_rights_exception_markers(page)
    if markers:
        return None, "page-has-third-party-music-or-rights-note: " + ", ".join(markers)
    main = page.get("main_video")
    if isinstance(main, dict) and _has_audio_track(main.get("audio_track")):
        return None, "main-video-has-explicit-audio-track-metadata; manual soundtrack review required"
    candidates = [x for x in iter_video_candidates(page) if not _has_audio_track(x.get("audio_track"))]
    if not candidates:
        return None, "no-allowlisted-video-without-unreviewed-audio-track"
    candidates.sort(key=_score, reverse=True)
    return candidates[0], "complete-svs-visualization; no page-level licensed-music marker"


def _json(url: str) -> tuple[dict[str, Any], int]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=35) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_JSON_BYTES:
            raise RuntimeError("NASA SVS JSON exceeds response ceiling")
        body = response.read(MAX_JSON_BYTES + 1)
    if len(body) > MAX_JSON_BYTES:
        raise RuntimeError("NASA SVS JSON exceeds response ceiling")
    result = json.loads(body.decode("utf-8-sig"))
    if not isinstance(result, dict):
        raise RuntimeError("NASA SVS returned non-object JSON")
    return result, len(body)


def _search_pages(report: list[dict[str, Any]]) -> list[tuple[int, str]]:
    found, seen = [], set()
    for term in SEARCH_TERMS:
        query = urllib.parse.urlencode({"studio": "SVS", "search": term, "limit": "100", "offset": "0"})
        try:
            data, _ = _json(BASE + "/api/search/?" + query, MAX_SEARCH_JSON_BYTES)
            added = 0
            for row in data.get("results") or []:
                if not isinstance(row, dict) or str(row.get("result_type") or "").casefold() != "visualization":
                    continue
                if not str(row.get("id") or "").isdigit():
                    continue
                page_id = int(row["id"])
                if page_id in seen:
                    continue
                seen.add(page_id)
                found.append((page_id, term))
                added += 1
                if added >= MAX_PER_TERM or len(found) >= MAX_PAGES:
                    break
            report.append({"id": "nasa-svs-search-" + term.casefold(), "status": "searched",
                           "query": term, "unique_page_ids_added": added, "source_page": BASE + "/search/"})
        except Exception as exc:
            report.append({"id": "nasa-svs-search-" + term.casefold(), "status": "search-failed",
                           "query": term, "reason": str(exc)[:350], "source_page": BASE + "/search/"})
        if len(found) >= MAX_PAGES:
            break
        time.sleep(0.12)
    return found[:MAX_PAGES]


def _download(url: str) -> tuple[bytes, str, str]:
    normalized = normalize_svs_media_url(url)
    if not normalized:
        raise RuntimeError("URL is outside official NASA SVS /vis/ allow-list")
    req = urllib.request.Request(normalized, headers={
        "User-Agent": UA, "Accept": "video/mp4,video/webm,video/mpeg,application/octet-stream,*/*",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=75) as response:
        if normalize_svs_media_url(response.geturl()) != normalized:
            raise RuntimeError("media redirect left exact allow-listed URL")
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_VIDEO_BYTES:
            raise RuntimeError("video exceeds per-file ceiling")
        body = response.read(MAX_VIDEO_BYTES + 1)
        ctype = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().lower()
    if len(body) > MAX_VIDEO_BYTES or len(body) < MIN_VIDEO_BYTES:
        raise RuntimeError("video byte size outside allowed range")
    ext = Path(urllib.parse.urlsplit(normalized).path).suffix.casefold()
    if ctype not in MIME[ext]:
        raise RuntimeError(f"unexpected MIME type: {ctype}")
    if ext == ".mp4" and not (len(body) >= 12 and b"ftyp" in body[:64]):
        raise RuntimeError("MP4 signature missing")
    if ext == ".webm" and not body.startswith(b"\x1a\x45\xdf\xa3"):
        raise RuntimeError("WebM signature missing")
    if ext == ".mpg" and not any(body.startswith(x) for x in (b"\x00\x00\x01\xba", b"\x00\x00\x01\xb3", b"\x00\x00\x01\x00")):
        raise RuntimeError("MPEG start code missing")
    return body, ctype, normalized


def _credits(page: dict[str, Any]) -> list[dict[str, str]]:
    result = []
    for group in page.get("credits") or []:
        if not isinstance(group, dict):
            continue
        role = str(group.get("role") or "")
        for person in group.get("people") or []:
            if isinstance(person, dict):
                result.append({"role": role[:120], "name": str(person.get("name") or "")[:180],
                               "employer": str(person.get("employer") or "")[:180]})
    return result


def download_nasa_svs_media(root: Path, index: list[dict]) -> list[dict]:
    """Download one best-resolution, rights-screened video per complete SVS visualization."""
    report, seen = [], set()
    total_bytes = metadata_bytes = downloaded = 0
    page_ids = _search_pages(report)
    for page_id, query_term in page_ids:
        if downloaded >= MAX_DOWNLOADS or total_bytes >= MAX_TOTAL_BYTES:
            break
        page_url = f"{BASE}/{page_id}/"
        try:
            page, size = _json(f"{BASE}/api/{page_id}/")
            metadata_bytes += size
            if metadata_bytes > MAX_TOTAL_JSON_BYTES:
                report.append({"id": f"nasa-svs-{page_id}", "status": "metadata-budget-exhausted", "source_page": page_url})
                break
            chosen, reason = choose_video_candidate(page)
            if not chosen:
                report.append({"id": f"nasa-svs-{page_id}", "status": "skipped", "title": str(page.get("title") or "")[:240],
                               "reason": reason, "source_page": page_url})
                time.sleep(0.12)
                continue
            candidates = [x for x in iter_video_candidates(page) if not _has_audio_track(x.get("audio_track"))]
            candidates.sort(key=_score, reverse=True)
            selected, failures = None, []
            for candidate in candidates:
                if candidate["url"] in seen:
                    failures.append("duplicate media URL")
                    continue
                try:
                    blob, ctype, media_url = _download(candidate["url"])
                    if total_bytes + len(blob) > MAX_TOTAL_BYTES:
                        failures.append("aggregate NASA SVS byte ceiling reached")
                        break
                    selected = (candidate, blob, ctype, media_url)
                    break
                except Exception as exc:
                    failures.append(str(exc)[:220])
            if not selected:
                report.append({"id": f"nasa-svs-{page_id}", "status": "skipped" if any("ceiling" in x for x in failures) else "failed",
                               "title": str(page.get("title") or "")[:240], "reason": "; ".join(failures[-3:]) or "no usable movie",
                               "source_page": page_url})
                if any("aggregate NASA SVS byte ceiling" in x for x in failures):
                    break
                time.sleep(0.12)
                continue
            media, blob, ctype, media_url = selected
            ext = Path(urllib.parse.urlsplit(media_url).path).suffix.casefold()
            title = str(page.get("title") or f"NASA SVS visualization {page_id}").strip()
            slug = re.sub(r"-+", "-", re.sub(r"[^a-zA-Z0-9._-]+", "-", title.lower())).strip("-")[:72] or "visualization"
            target = Path(root) / "third-party" / "nasa-svs" / "video" / f"{page_id}-{slug}{ext}"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
            digest = hashlib.sha256(blob).hexdigest()
            categories = page.get("nasa_science_categories") or []
            datasets = [{"name": str(d.get("name") or "")[:240], "organization": str(d.get("organization") or "")[:180],
                         "url": str(d.get("url") or "")[:500]} for d in page.get("datasets") or [] if isinstance(d, dict)]
            entry = {
                "id": f"nasa-svs-video-{page_id}", "path": target.relative_to(root).as_posix(), "type": "nasa-svs-video",
                "title": title[:300], "category": ", ".join(str(x) for x in categories[:5]) or "NASA scientific visualization",
                "description": str(page.get("description") or "")[:3000], "alt_text": str(media.get("alt_text") or "")[:1200],
                "width": media.get("width"), "height": media.get("height"), "release_date": page.get("release_date"),
                "updated_date": page.get("update_date"), "studio": page.get("studio"), "credits": _credits(page),
                "datasets": datasets, "missions": page.get("missions") or [], "science_categories": categories,
                "keywords": page.get("keywords") or [], "search_query": query_term, "source_page": page_url,
                "source_file_url": media_url, "license": "Public Domain (NASA SVS default; not CC0)",
                "license_url": "https://svs.gsfc.nasa.gov/help/",
                "rights_basis": "NASA SVS states its visualizations are public domain unless otherwise noted. This page passed the page-level music/rights screen; no non-empty audio_track metadata was present on the selected video.",
                "usage_notes": "Credit NASA Scientific Visualization Studio and listed creators/datasets. Do not imply NASA endorsement or use NASA insignia as a logo. Review privacy, publicity and third-party data before commercial or promotional use. Not CC0.",
                "license_filter_passed": True, "audio_track_metadata": media.get("audio_track"),
                "size_bytes": len(blob), "sha256": digest, "redistributable": True,
            }
            index.append(entry)
            seen.add(media_url)
            total_bytes += len(blob)
            downloaded += 1
            report.append({"id": entry["id"], "status": "downloaded", "title": title[:240], "source_page": page_url,
                           "source_file_url": media_url, "path": entry["path"], "width": media.get("width"),
                           "height": media.get("height"), "content_type": ctype, "license": entry["license"],
                           "size_bytes": len(blob), "sha256": digest, "rights_filter": "passed", "search_query": query_term})
            time.sleep(0.12)
        except Exception as exc:
            report.append({"id": f"nasa-svs-{page_id}", "status": "failed", "reason": str(exc)[:450], "source_page": page_url})
    report.append({"id": "nasa-svs-build-summary", "status": "summary", "page_requests": len(page_ids),
                   "downloaded_videos": downloaded, "indexed_resource_bytes": total_bytes, "metadata_bytes": metadata_bytes,
                   "max_downloads": MAX_DOWNLOADS, "max_file_bytes": MAX_VIDEO_BYTES, "max_total_bytes": MAX_TOTAL_BYTES,
                   "source_page": "https://svs.gsfc.nasa.gov/"})
    return report
