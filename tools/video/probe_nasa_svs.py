#!/usr/bin/env python3
"""Probe NASA Scientific Visualization Studio metadata and 64-byte MP4 headers only."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any

from nasa_svs_importer import normalize_svs_media_url, page_rights_exception_markers

SEARCH_URL = "https://svs.gsfc.nasa.gov/api/search/"
BASE_URL = "https://svs.gsfc.nasa.gov"
USER_AGENT = "NolaneVideoAssetLibrary-NASA-SVS-Probe/1.0"
SEARCH_PAGE_LIMIT = 100
MAX_PAGE_REQUESTS = 40
MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_TOTAL_JSON_BYTES = 32 * 1024 * 1024
MAX_MOVIE_RANGE_PROBES = 12
MAX_SAMPLE_MOVIE_ROWS = 12

# Restrict rights exceptions to explicit license/copyright language. General mentions
# of music are not enough on their own; the SVS FAQ says licensed music is noted on
# the individual visualization page and that the visual itself can be used without it.
def fetch_json(url: str, timeout: int = 30) -> tuple[dict[str, Any], int]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read(MAX_JSON_BYTES + 1)
        if len(body) > MAX_JSON_BYTES:
            raise RuntimeError("NASA SVS JSON response exceeded configured response ceiling")
    payload = json.loads(body.decode("utf-8-sig"))
    if not isinstance(payload, dict):
        raise RuntimeError("NASA SVS endpoint returned a non-object JSON response")
    return payload, len(body)


def svs_movie_url_is_allowed(url: str) -> bool:
    return normalize_svs_media_url(url) is not None


def probe_movie_header(url: str) -> dict[str, Any]:
    normalized_url = normalize_svs_media_url(url)
    if not normalized_url:
        return {"status": "rejected-url"}
    url = normalized_url
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "video/mp4,video/webm,application/octet-stream,*/*",
            "Accept-Encoding": "identity",
            "Range": "bytes=0-63",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            sample = response.read(65)
            content_range = response.headers.get("Content-Range", "")
            total_size = None
            if "/" in content_range:
                try:
                    total_size = int(content_range.rsplit("/", 1)[-1])
                except ValueError:
                    total_size = None
            suffix = url.casefold().split("?", 1)[0]
            if suffix.endswith((".mp4", ".mpg", ".dv")):
                signature_ok = len(sample) >= 12 and sample[4:8] == b"ftyp" if suffix.endswith(".mp4") else len(sample) >= 4
            else:
                signature_ok = sample.startswith(b"\x1a\x45\xdf\xa3")
            return {
                "status": "header-verified" if signature_ok else "bad-signature",
                "http_status": getattr(response, "status", 200),
                "content_type": response.headers.get("Content-Type", ""),
                "content_range": content_range,
                "remote_size_bytes": total_size,
                "bytes_read": len(sample),
                "signature_ok": signature_ok,
            }
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read(512).decode("utf-8", "replace")
        except Exception:
            body = ""
        return {"status": "range-failed", "http_status": exc.code, "reason": body[:400] or str(exc)[:300]}
    except Exception as exc:
        return {"status": "range-failed", "reason": str(exc)[:400]}


def iter_media_objects(page: dict[str, Any]):
    seen = set()
    for group in page.get("media_groups") or []:
        if not isinstance(group, dict):
            continue
        for item in group.get("items") or []:
            if not isinstance(item, dict):
                continue
            for key in ("media", "instance"):
                media = item.get(key)
                if not isinstance(media, dict):
                    continue
                url = str(media.get("url") or "")
                if not url or url in seen:
                    continue
                seen.add(url)
                yield media, group


def collect_page_text(page: dict[str, Any]) -> list[str]:
    text_fields = []
    for key in ("title", "description", "notes", "usage_notes", "copyright", "rights", "music_notes"):
        value = page.get(key)
        if isinstance(value, str) and value.strip():
            text_fields.append(value)
    for group in page.get("media_groups") or []:
        if not isinstance(group, dict):
            continue
        for key in ("title", "caption", "description", "notes"):
            value = group.get(key)
            if isinstance(value, str) and value.strip():
                text_fields.append(value)
    return text_fields


def inspect_page(page_id: int) -> tuple[dict[str, Any], int]:
    url = f"{BASE_URL}/api/{int(page_id)}/"
    page, size = fetch_json(url, timeout=35)
    if str(page.get("page_type") or "").casefold() != "visualization":
        return {"id": page_id, "status": "not-visualization", "page_type": page.get("page_type")}, size
    if str(page.get("progress") or "").casefold() != "complete":
        return {"id": page_id, "status": "not-complete", "progress": page.get("progress")}, size

    matches = page_rights_exception_markers(page)
    movies = []
    all_movie_items = []
    for media, group in iter_media_objects(page):
        if str(media.get("media_type") or "").casefold() != "movie":
            continue
        row = {
            "url": normalize_svs_media_url(str(media.get("url") or "")) or str(media.get("url") or ""),
            "audio_track": media.get("audio_track"),
            "filename": str(media.get("filename") or ""),
            "width": media.get("width"),
            "height": media.get("height"),
            "alt_text": str(media.get("alt_text") or "")[:300],
            "group_widget": group.get("widget"),
            "group_description": str(group.get("description") or "")[:500],
        }
        all_movie_items.append(row)
        if svs_movie_url_is_allowed(row["url"]):
            movies.append(row)

    credits = page.get("credits") if isinstance(page.get("credits"), list) else []
    return {
        "id": int(page_id),
        "status": "inspected",
        "page_url": f"{BASE_URL}/{int(page_id)}/",
        "title": str(page.get("title") or "")[:250],
        "release_date": page.get("release_date"),
        "studio": page.get("studio"),
        "progress": page.get("progress"),
        "main_video_type": (page.get("main_video") or {}).get("media_type") if isinstance(page.get("main_video"), dict) else None,
        "movie_count": len(all_movie_items),
        "allowlisted_movie_count": len(movies),
        "public_domain_exception_markers": matches,
        "exception_flagged": bool(matches),
        "credit_groups": len(credits),
        "movie_samples": movies[:5],
    }, size


def main() -> None:
    started = time.monotonic()
    total_json_bytes = 0
    search_url = SEARCH_URL + "?" + urllib.parse.urlencode(
        {"studio": "SVS", "limit": str(SEARCH_PAGE_LIMIT), "offset": "0"}
    )
    search, size = fetch_json(search_url)
    total_json_bytes += size
    results = search.get("results") or []
    page_ids = [
        int(row["id"]) for row in results
        if isinstance(row, dict)
        and str(row.get("result_type") or "").casefold() == "visualization"
        and str(row.get("id") or "").isdigit()
    ][:MAX_PAGE_REQUESTS]

    inspected = []
    for page_id in page_ids:
        if total_json_bytes >= MAX_TOTAL_JSON_BYTES:
            break
        try:
            row, size = inspect_page(page_id)
            total_json_bytes += size
            inspected.append(row)
            time.sleep(0.12)
        except Exception as exc:
            inspected.append({"id": page_id, "status": "page-failed", "reason": str(exc)[:350]})

    movie_rows = [
        (page, movie)
        for page in inspected
        if page.get("status") == "inspected" and not page.get("exception_flagged")
        for movie in page.get("movie_samples", [])
    ]
    range_checks = []
    for page, movie in movie_rows[:MAX_MOVIE_RANGE_PROBES]:
        range_checks.append({
            "page_id": page["id"],
            "title": page["title"],
            "url": movie["url"],
            "result": probe_movie_header(movie["url"]),
        })

    summary = {
        "probe": "NASA Scientific Visualization Studio metadata and 64-byte video headers only",
        "search_total_count": search.get("count"),
        "search_results_returned": len(results),
        "page_requests_attempted": len(page_ids),
        "page_requests_inspected": sum(row.get("status") == "inspected" for row in inspected),
        "page_requests_failed": sum(row.get("status") == "page-failed" for row in inspected),
        "complete_pages": sum(row.get("status") == "inspected" for row in inspected),
        "pages_with_public_domain_exception_markers": sum(bool(row.get("exception_flagged")) for row in inspected),
        "movie_items_in_sample": sum(int(row.get("movie_count") or 0) for row in inspected),
        "allowlisted_movie_items_in_sample": sum(int(row.get("allowlisted_movie_count") or 0) for row in inspected),
        "sample_pages": inspected[:MAX_SAMPLE_MOVIE_ROWS],
        "range_checks": range_checks,
        "json_bytes_read": total_json_bytes,
        "media_downloaded": False,
        "max_range_bytes_per_video": 65,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    print("NASA_SVS_PROBE_SUMMARY=" + json.dumps(summary, ensure_ascii=False))
    if summary["page_requests_inspected"] == 0:
        raise SystemExit("NASA SVS probe inspected no complete visualizations.")


if __name__ == "__main__":
    main()
