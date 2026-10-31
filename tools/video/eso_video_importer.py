#!/usr/bin/env python3
"""Rights-gated ESO video importer; verifies source hashes and removes all audio."""
from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

BASE = "https://www.eso.org"
FEED_CATEGORIES = ("esocast", "cosmology", "exoplanets", "milky-way", "black-holes")
MAX_FEEDS = 5
MAX_ITEMS_PER_FEED = 40
MAX_PAGE_REQUESTS = 72
MAX_FEED_BYTES = 2 * 1024 * 1024
MAX_PAGE_BYTES = 3 * 1024 * 1024
MAX_METADATA_BYTES = 64 * 1024 * 1024
MAX_DOWNLOADS = 18
MAX_VIDEO_BYTES = 300 * 1024 * 1024
MAX_TOTAL_SOURCE_BYTES = 4 * 1024 * 1024 * 1024
MIN_VIDEO_BYTES = 512 * 1024
UA = "NolaneVideoAssetLibrary-ESO/1.0 (+https://github.com/Nolane-x/video)"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,63}$")
SHA256_RE = re.compile(r"(?i)(?:^|\s)([0-9a-f]{64})(?:\s|$)")
RIGHTS_EXCEPTION_RE = re.compile(
    r"creative\s+commons\s+attribution[-\s]?no.?derivatives|"
    r"\bCC\s*BY\s*[-–]?\s*ND\b|\bno.?derivatives\b|"
    r"\bnon[- ]commercial\b|\bnoncommercial\b|"
    r"not\s+licensed\s+for\s+other\s+uses|"
    r"all\s+rights\s+reserved|permission\s+required|"
    r"not\s+released\s+under\s+(?:the\s+)?(?:usual|standard)?\s*"
    r"(?:creative\s+commons|CC\s*BY)|"
    r"commercial\s+use\s+is\s+not\s+permitted",
    re.IGNORECASE,
)
VIDEO_MIME = {"video/mp4", "application/mp4", "application/octet-stream", "binary/octet-stream"}


def normalize_eso_page_url(raw_url: str) -> str | None:
    """Allow only canonical HTTPS public video pages on www.eso.org."""
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if parsed.scheme.casefold() != "https" or (parsed.hostname or "").casefold() != "www.eso.org":
            return None
        if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
            return None
        match = re.fullmatch(r"/public/videos/([A-Za-z0-9][A-Za-z0-9_-]{1,63})/?", parsed.path)
        if not match:
            return None
        return f"{BASE}/public/videos/{match.group(1)}/"
    except (TypeError, ValueError):
        return None


def normalize_eso_media_url(raw_url: str, video_id: str) -> str | None:
    """Allow only ESO's checksum-published H.264 preview paths on its exact CDN host."""
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if parsed.scheme.casefold() != "https" or (parsed.hostname or "").casefold() != "cdn.eso.org":
            return None
        if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
            return None
        match = re.fullmatch(
            r"/videos/(ultra_hd|hd_1080p25_screen)/([A-Za-z0-9][A-Za-z0-9_-]{1,63})\.mp4",
            urllib.parse.unquote(parsed.path),
        )
        if not match or match.group(2).casefold() != str(video_id).casefold():
            return None
        return urllib.parse.urlunsplit(("https", "cdn.eso.org", parsed.path, "", ""))
    except (TypeError, ValueError):
        return None


def eso_response_url_is_allowed(requested_url: str, response_url: str, video_id: str) -> bool:
    requested = normalize_eso_media_url(requested_url, video_id)
    try:
        response = urllib.parse.urlsplit(str(response_url or "").strip())
    except ValueError:
        return False
    return bool(
        requested
        and response.scheme.casefold() == "https"
        and normalize_eso_media_url(response_url, video_id) == requested
    )


class _ESOPageParser(HTMLParser):
    """Extract the full credit block and per-format archive download rows."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.div_depth = 0
        self.credit_depth: int | None = None
        self.content_depth: int | None = None
        self.in_title = False
        self.in_anchor: dict[str, Any] | None = None
        self.title_parts: list[str] = []
        self.credit_parts: list[str] = []
        self.page_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.rows: list[dict[str, Any]] = []
        self.current_row: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.casefold(): value or "" for key, value in attrs}
        if tag == "meta":
            key = attr.get("name") or attr.get("property")
            value = attr.get("content")
            if key and value:
                self.meta[key.casefold()] = value.strip()
        if tag == "title":
            self.in_title = True
        if tag == "div":
            self.div_depth += 1
            classes = set(attr.get("class", "").casefold().split())
            if "credit" in classes and self.credit_depth is None:
                self.credit_depth = self.div_depth
            if attr.get("id", "").casefold() == "body" and self.content_depth is None:
                self.content_depth = self.div_depth
            if "archive_download" in classes and self.current_row is None:
                self.current_row = {"depth": self.div_depth, "anchors": [], "text": []}
        if self.current_row is not None:
            self.current_row["text"].append(" ")
        if tag == "a":
            self.in_anchor = {
                "href": attr.get("href", ""),
                "data_title": attr.get("data-title", ""),
                "data_content": attr.get("data-content", ""),
                "text": [],
            }
        if tag in {"br", "p", "li"} and self.credit_depth is not None:
            self.credit_parts.append("\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_anchor is not None:
            self.in_anchor["text"].append(data)
        if self.credit_depth is not None:
            self.credit_parts.append(data)
        if self.content_depth is not None and self.div_depth >= self.content_depth:
            self.page_parts.append(data)
        if self.current_row is not None:
            self.current_row["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.in_anchor is not None:
            anchor = self.in_anchor
            anchor["label"] = "".join(anchor.pop("text")).strip()
            if self.current_row is not None:
                self.current_row["anchors"].append(anchor)
            self.in_anchor = None
        if tag == "title":
            self.in_title = False
        if tag == "div":
            if self.current_row is not None and self.current_row["depth"] == self.div_depth:
                self.rows.append(self.current_row)
                self.current_row = None
            if self.credit_depth == self.div_depth:
                self.credit_depth = None
                self.credit_parts.append("\n")
            if self.content_depth == self.div_depth:
                self.content_depth = None
            self.div_depth = max(0, self.div_depth - 1)
        if tag == "p" and self.credit_depth is not None:
            self.credit_parts.append("\n")


def _clean_multiline(parts: list[str]) -> str:
    raw = html_lib.unescape("".join(parts)).replace("\xa0", " ")
    lines = []
    for line in raw.splitlines():
        cleaned = re.sub(r"[ \t]+", " ", line).strip()
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines)


def _parse_size_bytes(row_text: str) -> int | None:
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(B|KB|MB|GB)", row_text, re.IGNORECASE)
    if not match:
        return None
    scale = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}[match.group(2).upper()]
    return int(float(match.group(1)) * scale)


def parse_eso_video_page(video_id: str, page_html: str) -> dict[str, Any]:
    """Extract credit, page text and checksum-published H.264 options from one ESO page."""
    if not VIDEO_ID_RE.fullmatch(str(video_id or "")):
        raise ValueError("invalid ESO video id")
    parser = _ESOPageParser()
    parser.feed(page_html)
    parser.close()
    candidates = []
    for row in parser.rows:
        checksum = None
        for anchor in row["anchors"]:
            if "sha256" in str(anchor.get("data_title") or "").casefold():
                match = SHA256_RE.search(str(anchor.get("data_content") or "").replace("\xa0", " "))
                if match:
                    checksum = match.group(1).lower()
        for anchor in row["anchors"]:
            url = normalize_eso_media_url(anchor.get("href", ""), video_id)
            if not url:
                continue
            label = str(anchor.get("label") or "")
            rank = 2 if "4k ultra hd preview h.264" in label.casefold() else (
                1 if "full hd preview 1080p" in label.casefold() else 0
            )
            if rank and checksum:
                candidates.append({
                    "url": url,
                    "label": label[:120],
                    "expected_source_sha256": checksum,
                    "advertised_size_bytes": _parse_size_bytes(" ".join(row["text"])),
                    "rank": rank,
                })
    candidates.sort(key=lambda row: (row["rank"], row["advertised_size_bytes"] or 0), reverse=True)
    credit = _clean_multiline(parser.credit_parts)
    page_text = _clean_multiline(parser.page_parts)
    title = str(parser.meta.get("og:title") or _clean_multiline(parser.title_parts)).strip()
    description = str(parser.meta.get("description") or "").strip()
    markers = sorted({m.group(0).casefold() for m in RIGHTS_EXCEPTION_RE.finditer(page_text + "\n" + credit)})
    return {
        "title": title[:300],
        "description": description[:3000],
        "credit_text": credit[:12000],
        "page_text": page_text[:20000],
        "rights_exception_markers": markers,
        "media_candidates": candidates,
    }


def parse_eso_feed(feed_xml: bytes, category: str) -> list[dict[str, str]]:
    if len(feed_xml) > MAX_FEED_BYTES:
        raise RuntimeError("ESO RSS feed exceeded configured byte ceiling")
    root = ET.fromstring(feed_xml)
    items = []
    seen = set()
    for item in root.findall(".//item")[:MAX_ITEMS_PER_FEED]:
        link = (item.findtext("link") or "").strip()
        page_url = normalize_eso_page_url(link)
        if not page_url:
            continue
        video_id = urllib.parse.urlsplit(page_url).path.rstrip("/").rsplit("/", 1)[-1]
        if video_id in seen:
            continue
        seen.add(video_id)
        items.append({
            "id": video_id,
            "title": (item.findtext("title") or "").strip()[:300],
            "description": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", item.findtext("description") or "")).strip()[:2000],
            "published": (item.findtext("pubDate") or "").strip()[:80],
            "source_page": page_url,
            "category": category,
        })
    return items


def _fetch_bytes(url: str, limit: int, expected_host: str, timeout: int = 35) -> tuple[bytes, str]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != expected_host or parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
        raise RuntimeError("URL is outside the exact ESO HTTPS host allow-list")
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml,application/xml,text/html,*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final = urllib.parse.urlsplit(response.geturl())
        if final.scheme != "https" or final.hostname != expected_host or final.username or final.password or final.port:
            raise RuntimeError("redirect left the exact official ESO host")
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise RuntimeError("ESO response exceeded configured byte ceiling")
        body = response.read(limit + 1)
        content_type = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
    if len(body) > limit:
        raise RuntimeError("ESO response exceeded configured byte ceiling")
    return body, content_type


def _download_source_video(url: str, video_id: str, expected_sha256: str, destination: Path) -> tuple[int, str]:
    normalized = normalize_eso_media_url(url, video_id)
    if not normalized:
        raise RuntimeError("media URL is outside the checksum-published ESO H.264 allow-list")
    if not re.fullmatch(r"[0-9a-f]{64}", str(expected_sha256 or "")):
        raise RuntimeError("missing valid ESO source SHA-256")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "video/mp4,application/mp4,application/octet-stream", "Accept-Encoding": "identity"},
    )
    digest = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=90) as response:
        if not eso_response_url_is_allowed(normalized, response.geturl(), video_id):
            raise RuntimeError("media redirect left exact ESO CDN URL")
        content_type = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
        if content_type not in VIDEO_MIME:
            raise RuntimeError(f"unexpected ESO media MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_VIDEO_BYTES:
            raise RuntimeError("ESO video exceeds per-file ceiling")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_VIDEO_BYTES:
                    raise RuntimeError("ESO video exceeds per-file ceiling")
                digest.update(chunk)
                output.write(chunk)
    if total < MIN_VIDEO_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError("ESO video is unexpectedly small")
    with destination.open("rb") as handle:
        header = handle.read(64)
    if len(header) < 12 or b"ftyp" not in header[:32]:
        destination.unlink(missing_ok=True)
        raise RuntimeError("ESO MP4 container signature missing")
    actual = digest.hexdigest()
    if actual != expected_sha256:
        destination.unlink(missing_ok=True)
        raise RuntimeError("ESO source SHA-256 does not match the checksum published on the page")
    return total, actual


def _strip_audio_with_ffmpeg(source: Path, destination: Path) -> dict[str, Any]:
    """Copy only the first video stream; do not redistribute ESO's separately restricted music."""
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required for the ESO silent-footage lane")
    result = subprocess.run(
        [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
         "-map", "0:v:0", "-c:v", "copy", "-an", "-movflags", "+faststart", str(destination)],
        capture_output=True, text=True, timeout=300, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("FFmpeg silent remux failed: " + (result.stderr or result.stdout or "unknown error")[-600:])
    probe = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "stream=codec_type,width,height,codec_name",
         "-of", "json", str(destination)],
        capture_output=True, text=True, timeout=45, check=False,
    )
    if probe.returncode != 0:
        raise RuntimeError("ffprobe rejected the silent ESO output")
    payload = json.loads(probe.stdout or "{}")
    streams = payload.get("streams") or []
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    if not video or any(stream.get("codec_type") == "audio" for stream in streams):
        raise RuntimeError("silent ESO remux must contain video and zero audio streams")
    if destination.stat().st_size < MIN_VIDEO_BYTES:
        raise RuntimeError("silent ESO remux is unexpectedly small")
    return {
        "width": video.get("width"),
        "height": video.get("height"),
        "video_codec": video.get("codec_name"),
    }


def download_eso_media(root: Path, index: list[dict]) -> list[dict]:
    """Import bounded ESO public video previews, strip every soundtrack, preserve full credits."""
    report: list[dict] = []
    candidates: list[dict[str, str]] = []
    seen_ids = set()
    metadata_bytes = 0
    page_requests = 0
    downloaded = 0
    total_source_bytes = 0

    for category in FEED_CATEGORIES[:MAX_FEEDS]:
        feed_url = f"{BASE}/public/videos/feed/category/{category}/"
        try:
            feed_body, _ = _fetch_bytes(feed_url, MAX_FEED_BYTES, "www.eso.org")
            metadata_bytes += len(feed_body)
            rows = parse_eso_feed(feed_body, category)
            added = 0
            for row in rows:
                if row["id"] in seen_ids:
                    continue
                seen_ids.add(row["id"])
                candidates.append(row)
                added += 1
                if len(candidates) >= MAX_PAGE_REQUESTS:
                    break
            report.append({"id": "eso-feed-" + category, "status": "searched", "unique_video_pages_added": added, "source_page": feed_url})
        except Exception as exc:
            report.append({"id": "eso-feed-" + category, "status": "feed-failed", "reason": str(exc)[:350], "source_page": feed_url})
        if len(candidates) >= MAX_PAGE_REQUESTS or metadata_bytes >= MAX_METADATA_BYTES:
            break
        time.sleep(0.15)

    for row in candidates[:MAX_PAGE_REQUESTS]:
        if downloaded >= MAX_DOWNLOADS or total_source_bytes >= MAX_TOTAL_SOURCE_BYTES or metadata_bytes >= MAX_METADATA_BYTES:
            break
        video_id = row["id"]
        page_url = row["source_page"]
        page_requests += 1
        try:
            page_body, _ = _fetch_bytes(page_url, MAX_PAGE_BYTES, "www.eso.org")
            metadata_bytes += len(page_body)
            parsed = parse_eso_video_page(video_id, page_body.decode("utf-8", "replace"))
            if not parsed["credit_text"]:
                report.append({"id": "eso-" + video_id, "status": "skipped", "reason": "full credit block missing", "source_page": page_url})
                continue
            if parsed["rights_exception_markers"]:
                report.append({
                    "id": "eso-" + video_id, "status": "skipped",
                    "reason": "page-specific rights exception: " + ", ".join(parsed["rights_exception_markers"]),
                    "source_page": page_url,
                })
                continue
            if not parsed["media_candidates"]:
                report.append({"id": "eso-" + video_id, "status": "skipped", "reason": "no checksum-published H.264 4K/1080p preview", "source_page": page_url})
                continue

            failures = []
            selected = None
            for media in parsed["media_candidates"]:
                advertised = media.get("advertised_size_bytes")
                if advertised and advertised > MAX_VIDEO_BYTES:
                    failures.append("advertised media size exceeds per-file ceiling")
                    continue
                source_path = Path(root) / ".staging" / f"{video_id}.source.mp4"
                output_path = Path(root) / "third-party" / "eso" / "video" / f"{video_id}.mp4"
                try:
                    source_size, source_hash = _download_source_video(
                        media["url"], video_id, media["expected_source_sha256"], source_path
                    )
                    if total_source_bytes + source_size > MAX_TOTAL_SOURCE_BYTES:
                        source_path.unlink(missing_ok=True)
                        failures.append("aggregate ESO source-byte ceiling reached")
                        break
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    video_info = _strip_audio_with_ffmpeg(source_path, output_path)
                    source_path.unlink(missing_ok=True)
                    selected = (media, source_size, source_hash, output_path, video_info)
                    break
                except Exception as exc:
                    source_path.unlink(missing_ok=True)
                    output_path.unlink(missing_ok=True)
                    failures.append(str(exc)[:300])

            if not selected:
                reason = "; ".join(failures[-3:]) or "no usable H.264 preview"
                report.append({"id": "eso-" + video_id, "status": "skipped" if "ceiling" in reason else "failed", "reason": reason, "source_page": page_url})
                if "aggregate ESO source-byte ceiling" in reason:
                    break
                continue

            media, source_size, source_hash, output_path, video_info = selected
            output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
            output_size = output_path.stat().st_size
            title = parsed["title"] or row["title"] or f"ESO video {video_id}"
            entry = {
                "id": f"eso-video-{video_id}",
                "path": output_path.relative_to(root).as_posix(),
                "type": "eso-silent-video",
                "title": title[:300],
                "description": parsed["description"] or row["description"],
                "category": row["category"],
                "published": row["published"],
                "width": video_info.get("width"),
                "height": video_info.get("height"),
                "video_codec": video_info.get("video_codec"),
                "source_page": page_url,
                "source_file_url": media["url"],
                "source_sha256": source_hash,
                "source_size_bytes": source_size,
                "sha256": output_hash,
                "size_bytes": output_size,
                "license": "CC BY 4.0 (ESO public-video default unless item specifies otherwise)",
                "license_url": "https://www.eso.org/public/copyright/",
                "credit_text": parsed["credit_text"],
                "credit_required_visible": True,
                "credit_placement": "Reproduce the complete credit wording unaltered, clearly and visibly; use a visible end credit or on-screen overlay. A description-only credit is insufficient.",
                "audio_stripped": True,
                "audio_policy": "All audio streams removed. ESO music is not covered by the general CC BY 4.0 grant unless explicitly identified as part of the ESO Music Archive.",
                "rights_basis": "Official ESO public-video page; default CC BY 4.0 applies unless that page states an exception. Full credit retained. Page-specific NoDerivatives, non-commercial, permission and other restrictive markers fail closed.",
                "usage_notes": "Keep the full credit visible and unaltered. Do not use the ESO logo or imply ESO endorsement. Audio was stripped; do not restore the original soundtrack without separately verifying its rights.",
                "license_filter_passed": True,
                "redistributable": True,
            }
            index.append(entry)
            total_source_bytes += source_size
            downloaded += 1
            report.append({
                "id": entry["id"], "status": "downloaded", "title": title[:240],
                "source_page": page_url, "source_file_url": media["url"],
                "path": entry["path"], "selected_format": media["label"],
                "source_size_bytes": source_size, "size_bytes": output_size,
                "source_sha256": source_hash, "sha256": output_hash,
                "resolution": f"{video_info.get('width')}x{video_info.get('height')}",
                "audio_stripped": True, "license": entry["license"],
                "credit_required_visible": True,
            })
        except Exception as exc:
            report.append({"id": "eso-" + video_id, "status": "failed", "reason": str(exc)[:450], "source_page": page_url})
        time.sleep(0.15)

    report.append({
        "id": "eso-build-summary", "status": "summary",
        "feeds_checked": min(len(FEED_CATEGORIES), MAX_FEEDS),
        "unique_pages_discovered": len(candidates),
        "pages_inspected": page_requests,
        "downloaded_silent_videos": downloaded,
        "indexed_resource_bytes": sum(int(row["size_bytes"]) for row in index if str(row.get("id", "")).startswith("eso-video-")),
        "source_bytes_downloaded": total_source_bytes,
        "metadata_bytes": metadata_bytes,
        "max_downloads": MAX_DOWNLOADS,
        "max_file_bytes": MAX_VIDEO_BYTES,
        "max_total_source_bytes": MAX_TOTAL_SOURCE_BYTES,
        "source_page": "https://www.eso.org/public/videos/",
    })
    return report
