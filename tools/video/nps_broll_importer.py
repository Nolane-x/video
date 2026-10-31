#!/usr/bin/env python3
"""Rights-gated importer for official National Park Service public-domain B-roll."""
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
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

BASE = "https://www.nps.gov"
NPS_PARK_CODES = {"grca", "jotr", "deva", "yose", "saan"}
INDEXES = (
    {
        "id": "grand-canyon",
        "park": "grca",
        "url": "https://www.nps.gov/grca/learn/photosmultimedia/b-roll_hd_index.htm",
        "title": "Grand Canyon National Park B-Roll archive",
    },
    {
        "id": "joshua-tree",
        "park": "jotr",
        "url": "https://www.nps.gov/jotr/learn/photosmultimedia/broll.htm",
        "title": "Joshua Tree National Park B-Roll archive",
    },
    {
        "id": "death-valley",
        "park": "deva",
        "url": "https://www.nps.gov/deva/learn/photosmultimedia/b-roll-footage.htm",
        "title": "Death Valley National Park silent B-Roll archive",
    },
    {
        "id": "yosemite",
        "park": "yose",
        "url": "https://www.nps.gov/yose/learn/photosmultimedia/b-roll.htm",
        "title": "Yosemite National Park B-Roll archive",
    },
    {
        "id": "san-antonio-missions",
        "park": "saan",
        "url": "https://www.nps.gov/saan/learn/photosmultimedia/videos.htm",
        "title": "San Antonio Missions National Historical Park B-Roll archive",
    },
)
MAX_INDEXES = 5
MAX_ITEM_PAGES = 96
MAX_PAGE_BYTES = 8 * 1024 * 1024
MAX_METADATA_BYTES = 160 * 1024 * 1024
MAX_DOWNLOADS = 36
MAX_PARK_ARCHIVE_DOWNLOADS_PER_INDEX = 3
MAX_VIDEO_BYTES = 350 * 1024 * 1024
MAX_TOTAL_SOURCE_BYTES = 4 * 1024 * 1024 * 1024
MIN_VIDEO_BYTES = 256 * 1024
UA = "NolaneVideoAssetLibrary-NPS-Broll/1.0 (+https://github.com/Nolane-x/video)"
UUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
NPS_LEGACY_ID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{16}"
NPS_ARCHIVE_ID_RE = rf"(?:{UUID_RE}|{NPS_LEGACY_ID_RE})"
NPS_PUBLIC_DOMAIN_RE = re.compile(
    r"public\s+domain.{0,180}(?:free|use|download|any\s+purpose)|"
    r"(?:free|downloadable).{0,100}public\s+domain|"
    r"all\s+(?:video\s+files|footage).{0,140}public\s+domain|"
    r"these\s+silent\s+videos.{0,140}public\s+domain",
    re.IGNORECASE | re.DOTALL,
)
NPS_ITEM_RIGHTS_EXCEPTION_RE = re.compile(
    r"third[-\s]?party(?:\s+partner)?\s+(?:footage|material|video|content)|"
    r"copyright(?:ed)?\s+(?:footage|video|music|audio)|"
    r"licensed\s+(?:music|footage|material)|"
    r"used\s+with\s+permission|permission\s+(?:is\s+)?required|"
    r"not\s+(?:in\s+the\s+)?public\s+domain|"
    r"all\s+rights\s+reserved|non[-\s]?commercial|"
    r"not\s+cleared\s+for\s+(?:commercial|public)|"
    r"commercial(?:\s+or\s+promotional)?\s+use\s+(?:is\s+)?not\s+(?:cleared|permitted|authorized)",
    re.IGNORECASE,
)
NPS_MEDIA_PATH_RE = re.compile(
    rf"^/nps-audiovideo/(?:audiovideo/{UUID_RE}(?:240|360|426|480|640|720|854|1080|1280|1440|1920|2160)p\.mp4|"
    rf"legacy/(?:grca|jotr|deva|yose|saan)/{NPS_ARCHIVE_ID_RE}/[A-Za-z0-9._-]+\.mp4)$",
    re.IGNORECASE,
)
NPS_VIEW_PATH = "/media/video/view.htm"
NPS_EMBED_PATH = "/media/video/embed.htm"
NPS_MEDIA_PAGE_PATHS = {NPS_VIEW_PATH, NPS_EMBED_PATH}
NPS_COPYRIGHT_MARK_RE = re.compile(r"(?:©|\(c\)|copyright\s+(?:19|20)\d{2})", re.IGNORECASE)
NPS_DETAIL_PAGE_RE = re.compile(
    r"(?:b[-]?roll|clip|sunclips)",
    re.IGNORECASE,
)
NPS_REVIEW_PEOPLE_RE = re.compile(
    r"\b(?:people|person|visitors?|crowds?|rangers?|staff|employees?|climbers?|hikers?|interview|ceremony|children|students)\b",
    re.IGNORECASE,
)


def _is_official_url(raw_url: str) -> urllib.parse.SplitResult | None:
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if (
            parsed.scheme.casefold() != "https"
            or (parsed.hostname or "").casefold() != "www.nps.gov"
            or parsed.username
            or parsed.password
            or parsed.port
            or parsed.fragment
        ):
            return None
        return parsed
    except (TypeError, ValueError):
        return None


def normalize_nps_page_url(raw_url: str) -> str | None:
    """Accept only NPS media-view pages and park multimedia pages under known park paths."""
    parsed = _is_official_url(raw_url)
    if not parsed:
        return None
    if parsed.path in NPS_MEDIA_PAGE_PATHS:
        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        if set(query) != {"id"} or len(query["id"]) != 1 or not re.fullmatch(NPS_ARCHIVE_ID_RE, query["id"][0]):
            return None
        # The embed endpoint is only a player shell. Canonicalize its exact NPS media ID
        # to view.htm, whose Open Graph metadata exposes the official MP4 rendition.
        return f"{BASE}{NPS_VIEW_PATH}?id={query['id'][0].upper()}"
    if parsed.query:
        return None
    match = re.fullmatch(
        r"/(grca|jotr|deva|yose|saan)/learn/photosmultimedia/[A-Za-z0-9._-]+\.htm",
        parsed.path,
        re.IGNORECASE,
    )
    if not match or match.group(1).lower() not in NPS_PARK_CODES:
        return None
    return urllib.parse.urlunsplit(("https", "www.nps.gov", parsed.path, "", ""))


def normalize_nps_media_url(raw_url: str) -> str | None:
    """Allow only NPS-hosted MP4 renditions in the two verified audiovisual path families."""
    parsed = _is_official_url(raw_url)
    if not parsed or parsed.query:
        return None
    path = urllib.parse.unquote(parsed.path)
    if not NPS_MEDIA_PATH_RE.fullmatch(path):
        return None
    return urllib.parse.urlunsplit(("https", "www.nps.gov", path, "", ""))


def nps_media_response_url_is_allowed(requested_url: str, response_url: str) -> bool:
    requested = normalize_nps_media_url(requested_url)
    response = normalize_nps_media_url(response_url)
    return bool(requested and response and requested == response)


def nps_item_page_rights_exception(title: str, description: str) -> bool:
    return bool(NPS_ITEM_RIGHTS_EXCEPTION_RE.search((title or "") + "\n" + (description or "")))


def _resolution_rank(url: str, label: str = "", resolution: str = "") -> int:
    text = f"{label} {resolution} {url}".casefold()
    explicit = re.search(r"\b(2160|1440|1080|1280|854|720|640|480|426|360|240)p?\b", text)
    if not explicit:
        # NPS audiovisual IDs and their rendition suffix are concatenated (UUID720p.mp4),
        # so the normal word boundary cannot see the height after the final UUID digit.
        explicit = re.search(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
            r"(2160|1920|1440|1280|1080|854|720|640|480|426|360|240)p\.mp4$",
            url.casefold(),
        )
    if explicit:
        value = int(explicit.group(1))
        if "1280x720" in text:
            return 720
        if "854x480" in text:
            return 480
        if "640x360" in text:
            return 360
        if "426x240" in text:
            return 240
        return value
    dimensions = re.search(r"_(\d{3,4})x(\d{3,4})\.mp4$", text)
    if dimensions:
        return int(dimensions.group(2))
    return 0


def _clean_text(value: str, limit: int = 4000) -> str:
    value = html_lib.unescape(str(value or "")).replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


class _NPSHTMLParser(HTMLParser):
    """Extract video player groups and official page links without executing page scripts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.div_depth = 0
        self.video_group: dict[str, Any] | None = None
        self.title_capture_depth: int | None = None
        self.description_capture_depth: int | None = None
        self.h1_depth = 0
        self.h1_parts: list[str] = []
        self.title_parts: list[str] = []
        self.description_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.anchor: dict[str, str] | None = None
        self.video_groups: list[dict[str, Any]] = []
        self.global_media: list[dict[str, str]] = []
        self.all_text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.casefold(): value or "" for key, value in attrs}
        if tag == "meta":
            key = (attr.get("name") or attr.get("property") or attr.get("itemprop") or "").casefold()
            value = attr.get("content") or ""
            if key and value:
                self.meta[key] = value.strip()
                if key in {"og:video", "og:video:secure_url", "twitter:player:stream"}:
                    self.global_media.append({
                        "url": value.strip(),
                        "label": "NPS Open Graph video",
                        "resolution": "",
                    })
        if tag == "h1":
            self.h1_depth += 1
        if tag == "title":
            self.title_parts = []
            self._in_page_title = True
        if tag == "div":
            self.div_depth += 1
            classes = set(attr.get("class", "").casefold().split())
            if "videohero" in classes and self.video_group is None:
                self.video_group = {
                    "depth": self.div_depth,
                    "title_parts": [],
                    "description_parts": [],
                    "sources": [],
                }
            if self.video_group is not None and "vjs-dock-title" in classes:
                self.title_capture_depth = self.div_depth
            if self.video_group is not None and "vjs-dock-description" in classes:
                self.description_capture_depth = self.div_depth
        if tag == "a":
            self.anchor = {
                "href": attr.get("href", ""),
                "title": attr.get("title", ""),
                "text": "",
            }
        if tag == "iframe":
            src = attr.get("src", "")
            if src:
                self.links.append({
                    "href": urllib.parse.urljoin(BASE, src),
                    "title": attr.get("title", ""),
                    "text": "",
                })
        if tag in {"source", "video"}:
            src = attr.get("src", "")
            if src:
                media = {
                    "url": src,
                    "label": attr.get("label", ""),
                    "resolution": attr.get("res", ""),
                }
                self.global_media.append(media)
                if self.video_group is not None:
                    self.video_group["sources"].append(media)

    def handle_data(self, data: str) -> None:
        self.all_text_parts.append(data)
        if self.h1_depth:
            self.h1_parts.append(data)
        if self.title_capture_depth is not None and self.video_group is not None:
            self.video_group["title_parts"].append(data)
        if self.description_capture_depth is not None and self.video_group is not None:
            self.video_group["description_parts"].append(data)
        if getattr(self, "_in_page_title", False):
            self.title_parts.append(data)
        if self.anchor is not None:
            self.anchor["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.anchor is not None:
            self.anchor["text"] = _clean_text(self.anchor["text"], 1000)
            self.links.append(self.anchor)
            self.anchor = None
        if tag == "title":
            self._in_page_title = False
        if tag == "h1" and self.h1_depth:
            self.h1_depth -= 1
        if tag == "div":
            if self.title_capture_depth == self.div_depth:
                self.title_capture_depth = None
            if self.description_capture_depth == self.div_depth:
                self.description_capture_depth = None
            if self.video_group is not None and self.video_group["depth"] == self.div_depth:
                self.video_groups.append(self.video_group)
                self.video_group = None
            self.div_depth = max(0, self.div_depth - 1)

    def result(self) -> dict[str, Any]:
        groups: list[dict[str, Any]] = []
        for row in self.video_groups:
            groups.append({
                "title": _clean_text("".join(row["title_parts"]), 300),
                "description": _clean_text("".join(row["description_parts"]), 3000),
                "sources": row["sources"],
            })
        return {
            "page_title": _clean_text(
                "".join(self.h1_parts) or self.meta.get("og:title") or "".join(self.title_parts),
                300,
            ),
            "description": _clean_text(
                self.meta.get("description")
                or self.meta.get("og:description")
                or self.meta.get("twitter:description")
                or "",
                3000,
            ),
            "links": self.links,
            "video_groups": groups,
            "global_media": self.global_media,
            "page_text": _clean_text("".join(self.all_text_parts), 30000),
        }


def parse_nps_page(page_html: str) -> dict[str, Any]:
    parser = _NPSHTMLParser()
    parser.feed(page_html)
    parser.close()
    return parser.result()


def parse_nps_credit(page_html: str) -> tuple[str, bool]:
    match = re.search(
        r"(?:please\s+)?credit\s+[\"“]([^\"”\r\n]{3,300})[\"”]",
        html_lib.unescape(page_html or ""),
        re.IGNORECASE,
    )
    if match:
        return _clean_text(match.group(1), 300), True
    return "National Park Service", False


def parse_nps_media_page_credit(page_html: str) -> tuple[str, bool]:
    """Accept the item media page only when its visible credit is NPS-owned and unmarked."""
    raw = html_lib.unescape(page_html or "")
    match = re.search(
        r"<h[1-6]\b[^>]*>\s*credit\s*</h[1-6]\s*>(.*?)(?=<h[1-6]\b|$)",
        raw,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return "", False
    credit_html = re.sub(r"<[^>]+>", " ", match.group(1))
    credit = _clean_text(credit_html, 300)
    if not credit or NPS_COPYRIGHT_MARK_RE.search(credit_html):
        return credit, False
    return credit, "nps" in credit.casefold()


def parse_nps_index_page(page_html: str, park: str, index_url: str) -> dict[str, Any]:
    """Require the index's explicit Public Domain wording and return only approved child links."""
    if park not in NPS_PARK_CODES:
        raise ValueError("unsupported NPS park code")
    if not NPS_PUBLIC_DOMAIN_RE.search(html_lib.unescape(page_html or "")):
        raise RuntimeError("NPS index does not contain the required explicit Public Domain statement")
    parsed = parse_nps_page(page_html)
    child_pages: list[str] = []
    media_pages: list[dict[str, str]] = []
    seen = set()
    base_path = f"/{park}/learn/photosmultimedia/"
    for link in parsed["links"]:
        href = link.get("href", "")
        page_url = normalize_nps_page_url(href)
        if not page_url or page_url == index_url or page_url in seen:
            continue
        target = urllib.parse.urlsplit(page_url)
        if target.path == NPS_VIEW_PATH:
            media_pages.append({"url": page_url, "title": link.get("text") or link.get("title") or ""})
            seen.add(page_url)
            continue
        if not target.path.startswith(base_path):
            continue
        filename = target.path.rsplit("/", 1)[-1]
        if not NPS_DETAIL_PAGE_RE.search(filename):
            continue
        child_pages.append(page_url)
        seen.add(page_url)
    return {
        "page_title": parsed["page_title"],
        "description": parsed["description"],
        "video_groups": parsed["video_groups"],
        "global_media": parsed["global_media"],
        "page_text": parsed["page_text"],
        "child_pages": child_pages[:MAX_ITEM_PAGES],
        "media_pages": media_pages[:MAX_ITEM_PAGES],
        "credit_text": parse_nps_credit(page_html)[0],
        "credit_required_visible": parse_nps_credit(page_html)[1],
    }


def _media_candidates_from_group(group: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for item in group.get("sources", []):
        url = normalize_nps_media_url(item.get("url", ""))
        if not url:
            continue
        rank = _resolution_rank(url, item.get("label", ""), item.get("resolution", ""))
        # A bare <video src> may appear before its equivalent labelled <source>.
        # Do not let that unresolved duplicate hide the later 720p/1080p rendition.
        if not rank or url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "label": item.get("label") or f"{rank}p", "resolution": rank})
    out.sort(key=lambda row: row["resolution"], reverse=True)
    return out


def _groups_for_page(parsed: dict[str, Any], page_url: str) -> list[dict[str, Any]]:
    groups = []
    for row in parsed.get("video_groups", []):
        media = _media_candidates_from_group(row)
        if media:
            groups.append({
                "title": row.get("title") or parsed.get("page_title") or "NPS B-roll video",
                "description": row.get("description") or parsed.get("description", ""),
                "media_candidates": media,
            })
    if groups:
        return groups
    sources = []
    seen = set()
    for item in parsed.get("global_media", []):
        url = normalize_nps_media_url(item.get("url", ""))
        if url and url not in seen:
            seen.add(url)
            rank = _resolution_rank(url, item.get("label", ""), item.get("resolution", ""))
            if rank:
                sources.append({"url": url, "label": item.get("label") or f"{rank}p", "resolution": rank})
    for link in parsed.get("links", []):
        url = normalize_nps_media_url(link.get("href", ""))
        if url and url not in seen:
            seen.add(url)
            rank = _resolution_rank(url, link.get("text", ""), "")
            if rank:
                sources.append({"url": url, "label": link.get("text") or f"{rank}p", "resolution": rank})
    sources.sort(key=lambda row: row["resolution"], reverse=True)
    if sources:
        groups.append({
            "title": parsed.get("page_title") or "NPS B-roll video",
            "description": parsed.get("description", ""),
            "media_candidates": sources,
        })
    return groups


def _fetch_nps_page(url: str, limit: int = MAX_PAGE_BYTES, timeout: int = 35) -> bytes:
    normalized = normalize_nps_page_url(url)
    if not normalized:
        raise RuntimeError("NPS page URL is outside the official HTTPS allow-list")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final = normalize_nps_page_url(response.geturl())
        if final != normalized:
            raise RuntimeError("NPS page redirect changed the approved source URL")
        content_type = response.headers.get("Content-Type", "text/html").split(";", 1)[0].strip().casefold()
        if content_type not in {"text/html", "application/xhtml+xml", "application/octet-stream"}:
            raise RuntimeError(f"unexpected NPS page MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise RuntimeError("NPS page exceeded metadata byte ceiling")
        body = response.read(limit + 1)
    if len(body) > limit:
        raise RuntimeError("NPS page exceeded metadata byte ceiling")
    return body


def _download_nps_source(url: str, destination: Path) -> tuple[int, str]:
    normalized = normalize_nps_media_url(url)
    if not normalized:
        raise RuntimeError("NPS media URL is outside the official audiovisual MP4 allow-list")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "video/mp4,application/mp4,application/octet-stream", "Accept-Encoding": "identity"},
    )
    digest = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=90) as response:
        if not nps_media_response_url_is_allowed(normalized, response.geturl()):
            raise RuntimeError("NPS media redirect left the exact official video URL")
        content_type = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
        if content_type not in {"video/mp4", "application/mp4", "application/octet-stream", "binary/octet-stream"}:
            raise RuntimeError(f"unexpected NPS video MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_VIDEO_BYTES:
            raise RuntimeError("NPS video exceeds the per-file byte ceiling")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_VIDEO_BYTES:
                    raise RuntimeError("NPS video exceeds the per-file byte ceiling")
                digest.update(chunk)
                output.write(chunk)
    if total < MIN_VIDEO_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPS video is unexpectedly small")
    with destination.open("rb") as handle:
        header = handle.read(64)
    if len(header) < 12 or b"ftyp" not in header[:32]:
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPS MP4 container signature is missing")
    return total, digest.hexdigest()


def _strip_nps_audio_with_ffmpeg(source: Path, destination: Path) -> dict[str, Any]:
    """Retain only video streams to avoid silently redistributing an uncertain soundtrack."""
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required for NPS silent-footage archiving")
    result = subprocess.run(
        [
            ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-map", "0:v:0", "-c:v", "copy", "-an", "-movflags", "+faststart", str(destination),
        ],
        capture_output=True, text=True, timeout=300, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("FFmpeg NPS silent remux failed: " + (result.stderr or result.stdout or "unknown error")[-600:])
    probe = subprocess.run(
        [
            ffprobe, "-v", "error", "-show_entries", "stream=codec_type,width,height,codec_name:format=duration",
            "-of", "json", str(destination),
        ],
        capture_output=True, text=True, timeout=45, check=False,
    )
    if probe.returncode != 0:
        raise RuntimeError("ffprobe rejected the NPS silent output")
    payload = json.loads(probe.stdout or "{}")
    streams = payload.get("streams") or []
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    if not video or any(stream.get("codec_type") == "audio" for stream in streams):
        raise RuntimeError("NPS silent output must contain video and zero audio streams")
    if destination.stat().st_size < MIN_VIDEO_BYTES:
        raise RuntimeError("NPS silent output is unexpectedly small")
    duration = (payload.get("format") or {}).get("duration")
    try:
        duration = round(float(duration), 3) if duration is not None else None
    except (TypeError, ValueError):
        duration = None
    return {
        "width": video.get("width"),
        "height": video.get("height"),
        "video_codec": video.get("codec_name"),
        "duration_seconds": duration,
    }



NPGALLERY_BASE = "https://npgallery.nps.gov"
NPGALLERY_SEARCH_URL = NPGALLERY_BASE + "/SearchResults?pagesize=60&keyword=b-roll"
NPGALLERY_UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def _npgallery_is_official_url(raw_url: str) -> urllib.parse.SplitResult | None:
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if (
            parsed.scheme.casefold() != "https"
            or (parsed.hostname or "").casefold() != "npgallery.nps.gov"
            or parsed.username
            or parsed.password
            or parsed.port
            or parsed.fragment
        ):
            return None
        return parsed
    except (TypeError, ValueError):
        return None


def normalize_npgallery_page_url(raw_url: str) -> str | None:
    parsed = _npgallery_is_official_url(raw_url)
    if not parsed:
        return None
    if parsed.path == "/SearchResults":
        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        if set(query) != {"pagesize", "keyword"}:
            return None
        if query.get("pagesize") != ["60"] or query.get("keyword", [""])[0].casefold() != "b-roll":
            return None
        return NPGALLERY_SEARCH_URL
    match = re.fullmatch(r"/AssetDetail/(" + NPGALLERY_UUID_RE.pattern[1:-1] + r")", parsed.path, re.IGNORECASE)
    if not match or parsed.query:
        return None
    return f"{NPGALLERY_BASE}/AssetDetail/{match.group(1).lower()}"


def normalize_npgallery_original_url(raw_url: str, asset_id: str) -> str | None:
    if not NPGALLERY_UUID_RE.fullmatch(str(asset_id or "")):
        return None
    parsed = _npgallery_is_official_url(raw_url)
    if not parsed or parsed.query:
        return None
    expected = f"/GetAsset/{asset_id.lower()}/original"
    if parsed.path.casefold() != expected.casefold():
        return None
    return f"{NPGALLERY_BASE}{expected}"


def parse_npgallery_search_results(page_html: str) -> list[dict[str, Any]]:
    """Parse the official NPGallery search payload and retain only clearly eligible MP4 videos."""
    match = re.search(r"\bvar\s+search\s*=\s*", page_html or "")
    if not match:
        raise RuntimeError("NPGallery search payload was not found")
    start = (page_html or "").find("{", match.end())
    if start < 0:
        raise RuntimeError("NPGallery search payload has no JSON object")
    payload, _ = json.JSONDecoder().raw_decode((page_html or "")[start:])
    results = payload.get("Results") or []
    eligible: list[dict[str, Any]] = []
    for row in results[:60]:
        asset = row.get("Asset") or {}
        rights = asset.get("ConstraintsInformation") or {}
        asset_id = str(asset.get("AssetID") or "").strip()
        photo_credit = str(asset.get("PhotoCredit") or "").strip()
        if (
            not NPGALLERY_UUID_RE.fullmatch(asset_id)
            or str(asset.get("AssetBaseType") or "").casefold() != "file"
            or str(asset.get("PrimaryType") or "").casefold() != "video"
            or str(asset.get("ResourceType") or "").casefold() != "video"
            or str(asset.get("ResourceFormat") or "").casefold() != "mp4"
            or str(rights.get("Constraint") or "").casefold() != "public domain"
            or str(rights.get("GrantingRights") or "").casefold() != "full"
            or "nps" not in photo_credit.casefold()
        ):
            continue
        eligible.append(asset)
    return eligible


def _npgallery_label_field(page_html: str, label: str) -> str:
    pattern = (
        r"<label\b[^>]*>\s*" + re.escape(label) +
        r"\s*:\s*</label>\s*<p\b[^>]*>(.*?)</p>"
    )
    match = re.search(pattern, page_html or "", re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    value = re.sub(r"<br\s*/?>", " ", match.group(1), flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)
    return _clean_text(value, 4000)


def parse_npgallery_asset_detail(page_html: str) -> dict[str, str]:
    fields = (
        "Asset ID", "Title", "AltText", "Description", "Copyright",
        "PhotoCredit", "Constraints Information", "Resource Type",
        "Resource Format", "Access Constraints", "Original File Name",
        "File Size (bytes)", "NPS Units",
    )
    parsed = {name: _npgallery_label_field(page_html, name) for name in fields}
    return parsed


def _npgallery_rights_verified(asset: dict[str, Any], detail: dict[str, str], asset_id: str) -> bool:
    search_rights = asset.get("ConstraintsInformation") or {}
    search_credit = str(asset.get("PhotoCredit") or "").strip()
    detail_rights = re.sub(r"\s+", " ", detail.get("Constraints Information", "")).strip().casefold()
    detail_id = detail.get("Asset ID", "").strip().lower()
    detail_credit = detail.get("PhotoCredit", "").strip()
    return bool(
        detail_id == asset_id.lower()
        and str(search_rights.get("Constraint") or "").casefold() == "public domain"
        and str(search_rights.get("GrantingRights") or "").casefold() == "full"
        and detail_rights.replace(" ", "") == "publicdomain:fullgrantingrights"
        and str(asset.get("ResourceType") or "").casefold() == "video"
        and detail.get("Resource Type", "").casefold() == "video"
        and str(asset.get("ResourceFormat") or "").casefold() == "mp4"
        and detail.get("Resource Format", "").casefold() == "mp4"
        and "nps" in search_credit.casefold()
        and "nps" in detail_credit.casefold()
        and not NPS_COPYRIGHT_MARK_RE.search(detail_credit)
        and bool(detail.get("Title"))
    )


def _fetch_npgallery_page(url: str, limit: int = MAX_PAGE_BYTES, timeout: int = 35) -> bytes:
    normalized = normalize_npgallery_page_url(url)
    if not normalized:
        raise RuntimeError("NPGallery page URL is outside the exact official HTTPS allow-list")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final = normalize_npgallery_page_url(response.geturl())
        if final != normalized:
            raise RuntimeError("NPGallery page redirect changed the approved source URL")
        content_type = response.headers.get("Content-Type", "text/html").split(";", 1)[0].strip().casefold()
        if content_type not in {"text/html", "application/xhtml+xml", "application/octet-stream"}:
            raise RuntimeError(f"unexpected NPGallery page MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise RuntimeError("NPGallery page exceeded metadata byte ceiling")
        body = response.read(limit + 1)
    if len(body) > limit:
        raise RuntimeError("NPGallery page exceeded metadata byte ceiling")
    return body


def _download_npgallery_source(
    url: str,
    asset_id: str,
    destination: Path,
    max_bytes: int = MAX_VIDEO_BYTES,
) -> tuple[int, str]:
    normalized = normalize_npgallery_original_url(url, asset_id)
    if not normalized:
        raise RuntimeError("NPGallery original URL is outside the exact asset-specific download allow-list")
    request = urllib.request.Request(
        normalized,
        headers={
            "User-Agent": UA,
            "Accept": "video/mp4,application/mp4,application/octet-stream",
            "Accept-Encoding": "identity",
            "Referer": f"{NPGALLERY_BASE}/AssetDetail/{asset_id.lower()}",
        },
    )
    digest = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=90) as response:
        final = normalize_npgallery_original_url(response.geturl(), asset_id)
        if final != normalized:
            raise RuntimeError("NPGallery original download redirected outside the exact asset endpoint")
        content_type = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
        if content_type not in {"video/mp4", "application/mp4", "application/octet-stream", "binary/octet-stream"}:
            raise RuntimeError(f"unexpected NPGallery original MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > min(MAX_VIDEO_BYTES, max_bytes):
            raise RuntimeError("NPGallery original exceeds the remaining source-byte ceiling")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > min(MAX_VIDEO_BYTES, max_bytes):
                    raise RuntimeError("NPGallery original exceeds the remaining source-byte ceiling")
                digest.update(chunk)
                output.write(chunk)
    if total < MIN_VIDEO_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPGallery original is unexpectedly small")
    with destination.open("rb") as handle:
        header = handle.read(64)
    if len(header) < 12 or b"ftyp" not in header[:32]:
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPGallery original MP4 container signature is missing")
    return total, digest.hexdigest()


def download_npgallery_broll_media(
    root: Path,
    index: list[dict],
    *,
    max_downloads: int,
    max_total_source_bytes: int,
    max_metadata_bytes: int,
    seen_source_hashes: set[str] | None = None,
) -> tuple[list[dict], dict[str, int]]:
    """Import NPGallery candidates only after per-item Full Public Domain rights are rechecked."""
    report: list[dict] = []
    stats = {"videos_downloaded": 0, "source_bytes_downloaded": 0, "indexed_resource_bytes": 0, "metadata_bytes": 0}
    if max_downloads <= 0 or max_total_source_bytes <= 0 or max_metadata_bytes <= 0:
        return report, stats
    try:
        body = _fetch_npgallery_page(NPGALLERY_SEARCH_URL, limit=min(MAX_PAGE_BYTES, max_metadata_bytes))
        stats["metadata_bytes"] += len(body)
        candidates = parse_npgallery_search_results(body.decode("utf-8", "replace"))
        report.append({
            "id": "nps-npgallery-search",
            "status": "searched",
            "source_page": NPGALLERY_SEARCH_URL,
            "search_result_count": len(candidates),
            "rights_filter": "video + MP4 + Public domain + Full Granting Rights + NPS credit",
        })
    except Exception as exc:
        report.append({
            "id": "nps-npgallery-search",
            "status": "search-failed",
            "source_page": NPGALLERY_SEARCH_URL,
            "reason": str(exc)[:400],
        })
        return report, stats

    seen_asset_ids: set[str] = set()
    seen_source_hashes = seen_source_hashes if seen_source_hashes is not None else set()
    for asset in candidates[: min(60, max_downloads)]:
        if (
            stats["videos_downloaded"] >= max_downloads
            or stats["source_bytes_downloaded"] >= max_total_source_bytes
            or stats["metadata_bytes"] >= max_metadata_bytes
        ):
            break
        asset_id = str(asset.get("AssetID") or "").lower()
        if asset_id in seen_asset_ids:
            continue
        seen_asset_ids.add(asset_id)
        detail_url = f"{NPGALLERY_BASE}/AssetDetail/{asset_id}"
        try:
            detail_body = _fetch_npgallery_page(
                detail_url,
                limit=min(MAX_PAGE_BYTES, max_metadata_bytes - stats["metadata_bytes"]),
            )
            stats["metadata_bytes"] += len(detail_body)
            detail_html = detail_body.decode("utf-8", "replace")
            detail = parse_npgallery_asset_detail(detail_html)
            if not _npgallery_rights_verified(asset, detail, asset_id):
                report.append({
                    "id": "nps-npgallery-" + asset_id[:12],
                    "status": "skipped_rights_exception",
                    "source_page": detail_url,
                    "title": detail.get("Title") or asset.get("Title", ""),
                    "reason": "item detail does not reconfirm Public domain: Full Granting Rights, MP4 video and NPS credit",
                })
                continue
        except Exception as exc:
            report.append({
                "id": "nps-npgallery-" + asset_id[:12],
                "status": "detail-failed",
                "source_page": detail_url,
                "reason": str(exc)[:350],
            })
            continue

        title = detail.get("Title") or str(asset.get("Title") or "NPS NPGallery B-roll")
        description = detail.get("Description") or str(asset.get("Description") or "")
        alt_text = detail.get("AltText") or str(asset.get("AltText") or "")
        credit = detail.get("PhotoCredit", "").strip()
        original_url = f"{NPGALLERY_BASE}/GetAsset/{asset_id}/original"
        output_path = Path(root) / "third-party" / "nps" / "npgallery" / (
            f"{_slug(title)}-{asset_id[:10]}.mp4"
        )
        source_path = Path(root) / ".staging" / (asset_id + ".npgallery.source.mp4")
        try:
            remaining = max_total_source_bytes - stats["source_bytes_downloaded"]
            file_size, source_hash = _download_npgallery_source(
                original_url,
                asset_id,
                source_path,
                max_bytes=min(MAX_VIDEO_BYTES, remaining),
            )
            if stats["source_bytes_downloaded"] + file_size > max_total_source_bytes:
                source_path.unlink(missing_ok=True)
                report.append({
                    "id": "nps-npgallery-" + asset_id[:12],
                    "status": "skipped",
                    "source_page": detail_url,
                    "reason": "aggregate NPS source-byte ceiling reached",
                })
                break
            output_path.parent.mkdir(parents=True, exist_ok=True)
            video_info = _strip_nps_audio_with_ffmpeg(source_path, output_path)
            source_path.unlink(missing_ok=True)
        except Exception as exc:
            source_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
            report.append({
                "id": "nps-npgallery-" + asset_id[:12],
                "status": "failed",
                "source_page": detail_url,
                "source_file_url": original_url,
                "title": title[:240],
                "reason": str(exc)[:400],
            })
            continue

        if source_hash in seen_source_hashes:
            output_path.unlink(missing_ok=True)
            stats["source_bytes_downloaded"] += file_size
            report.append({
                "id": "nps-npgallery-" + asset_id[:12],
                "status": "duplicate",
                "source_page": detail_url,
                "source_sha256": source_hash,
                "reason": "identical source bytes already imported from an earlier NPGallery asset",
            })
            continue
        seen_source_hashes.add(source_hash)
        output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
        output_size = output_path.stat().st_size
        people_review = bool(NPS_REVIEW_PEOPLE_RE.search(title + " " + description + " " + alt_text))
        unit = detail.get("NPS Units", "").strip()
        entry = {
            "id": "nps-npgallery-" + asset_id,
            "path": output_path.relative_to(root).as_posix(),
            "type": "nps-broll-video",
            "title": title[:300],
            "description": description[:3000],
            "park": unit,
            "collection": "nps-npgallery-broll-search",
            "source_page": detail_url,
            "collection_page": NPGALLERY_SEARCH_URL,
            "source_file_url": original_url,
            "source_sha256": source_hash,
            "source_sha256_method": "computed after download; NPGallery detail metadata does not publish a per-file SHA-256",
            "source_size_bytes": file_size,
            "sha256": output_hash,
            "size_bytes": output_size,
            "width": video_info.get("width"),
            "height": video_info.get("height"),
            "video_codec": video_info.get("video_codec"),
            "duration_seconds": video_info.get("duration_seconds"),
            "source_resolution_label": "Original MP4",
            "source_resolution_rank": video_info.get("height"),
            "license": "Public Domain (NPGallery item-level Public domain: Full Granting Rights; not CC0)",
            "license_url": detail_url,
            "public_domain_verified": True,
            "rights_basis": "The individual NPGallery asset detail page reconfirms Public domain: Full Granting Rights, Resource Type Video, Resource Format mp4 and an NPS PhotoCredit. The search result alone is never treated as sufficient permission. Do not imply NPS endorsement or use protected NPS insignia.",
            "credit_text": credit,
            "credit_required_visible": True,
            "credit_note": "Preserve the NPGallery PhotoCredit text verbatim; do not imply NPS endorsement.",
            "audio_stripped": True,
            "modifications_disclosed": "Audio streams removed; the original video stream was copied without re-encoding.",
            "privacy_publicity_review_required": people_review,
            "commercial_promotional_review_required_if_people_identifiable": people_review,
            "usage_notes": "NPGallery item-level Public Domain with Full Granting Rights, not CC0. Preserve PhotoCredit, do not imply NPS endorsement, and review identifiable people, private property, third-party marks and context before commercial/promotional publication.",
            "redistributable": True,
        }
        index.append(entry)
        stats["videos_downloaded"] += 1
        stats["source_bytes_downloaded"] += file_size
        stats["indexed_resource_bytes"] += output_size
        report.append({
            "id": entry["id"],
            "status": "downloaded",
            "title": title[:240],
            "source_page": detail_url,
            "source_file_url": original_url,
            "path": entry["path"],
            "selected_format": "Original MP4",
            "source_size_bytes": file_size,
            "size_bytes": output_size,
            "source_sha256": source_hash,
            "sha256": output_hash,
            "resolution": f"{entry['width']}x{entry['height']}",
            "audio_stripped": True,
            "credit_text": credit,
            "credit_required_visible": True,
            "people_privacy_review_required": people_review,
            "license": entry["license"],
        })
    return report, stats


def _slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", _clean_text(value, 240)).strip("-").lower()
    return (value[:80] or "nps-broll")


def download_nps_broll_media(root: Path, index: list[dict]) -> list[dict]:
    """Import bounded NPS B-roll only when a named park archive explicitly grants Public Domain use."""
    report: list[dict] = []
    metadata_bytes = 0
    pages_inspected = 0
    downloads = 0
    source_bytes = 0
    indexed_bytes = 0
    seen_pages = set()
    seen_media = set()
    seen_source_hashes: set[str] = set()
    collection_count = 0

    for source in INDEXES[:MAX_INDEXES]:
        if metadata_bytes >= MAX_METADATA_BYTES or downloads >= MAX_DOWNLOADS:
            break
        collection_url = source["url"]
        collection_count += 1
        try:
            page_body = _fetch_nps_page(collection_url)
            metadata_bytes += len(page_body)
            page_html = page_body.decode("utf-8", "replace")
            parsed_index = parse_nps_index_page(page_html, source["park"], collection_url)
            report.append({
                "id": "nps-index-" + source["id"],
                "status": "searched",
                "source_page": collection_url,
                "title": source["title"],
                "explicit_public_domain_notice": True,
                "child_pages_discovered": len(parsed_index["child_pages"]),
                "media_pages_discovered": len(parsed_index["media_pages"]),
            })
        except Exception as exc:
            report.append({
                "id": "nps-index-" + source["id"],
                "status": "index-failed",
                "source_page": collection_url,
                "reason": str(exc)[:400],
            })
            continue

        collection_credit = parsed_index["credit_text"]
        credit_required = parsed_index["credit_required_visible"]
        downloads_for_index = 0
        page_tasks = [(collection_url, "collection", source)]
        page_tasks.extend((url, "detail", source) for url in parsed_index["child_pages"])
        page_tasks.extend((row["url"], "media", {**source, "media_hint": row.get("title", "")}) for row in parsed_index["media_pages"])

        queued_pages = {row[0] for row in page_tasks}
        task_cursor = 0
        while task_cursor < len(page_tasks) and task_cursor < MAX_ITEM_PAGES:
            page_url, page_kind, source_info = page_tasks[task_cursor]
            task_cursor += 1
            if downloads >= MAX_DOWNLOADS or source_bytes >= MAX_TOTAL_SOURCE_BYTES or metadata_bytes >= MAX_METADATA_BYTES:
                break
            if page_url in seen_pages:
                continue
            seen_pages.add(page_url)
            if page_kind == "collection" and not parsed_index["global_media"] and not parsed_index["video_groups"]:
                continue
            if page_kind != "collection":
                try:
                    body = _fetch_nps_page(page_url)
                    metadata_bytes += len(body)
                    page_html = body.decode("utf-8", "replace")
                    parsed = parse_nps_page(page_html)
                    pages_inspected += 1
                except Exception as exc:
                    report.append({
                        "id": "nps-page-" + hashlib.sha256(page_url.encode("utf-8")).hexdigest()[:12],
                        "status": "page-failed",
                        "source_page": page_url,
                        "reason": str(exc)[:350],
                    })
                    continue
            else:
                parsed = {
                    "page_title": parsed_index["page_title"],
                    "description": parsed_index["description"],
                    "video_groups": parsed_index["video_groups"],
                    "global_media": parsed_index["global_media"],
                    "links": [],
                    "page_text": parsed_index["page_text"],
                }
            media_page_credit = ""
            if page_kind == "media":
                media_page_credit, media_credit_is_pd = parse_nps_media_page_credit(page_html)
                if not media_credit_is_pd:
                    report.append({
                        "id": "nps-rights-" + hashlib.sha256(page_url.encode("utf-8")).hexdigest()[:12],
                        "status": "skipped_rights_exception",
                        "reason": "NPS media detail page lacks an unmarked NPS credit",
                        "source_page": page_url,
                        "credit_text": media_page_credit,
                    })
                    continue

            groups = _groups_for_page(parsed, page_url)
            if page_kind == "detail" and not groups:
                # Archive detail pages often contain only an NPS embed iframe. Follow
                # only its exact NPS media ID, then read view.htm Open Graph MP4 metadata.
                for link in parsed.get("links", []):
                    media_page = normalize_nps_page_url(link.get("href", ""))
                    if not media_page or urllib.parse.urlsplit(media_page).path != NPS_VIEW_PATH:
                        continue
                    if media_page in queued_pages or len(page_tasks) >= MAX_ITEM_PAGES:
                        continue
                    page_tasks.append((
                        media_page,
                        "media",
                        {**source_info, "media_hint": link.get("title") or parsed.get("page_title", "")},
                    ))
                    queued_pages.add(media_page)

            for group_number, group in enumerate(groups, 1):
                if (
                    downloads >= MAX_DOWNLOADS
                    or downloads_for_index >= MAX_PARK_ARCHIVE_DOWNLOADS_PER_INDEX
                    or source_bytes >= MAX_TOTAL_SOURCE_BYTES
                ):
                    break
                title = group.get("title") or source_info["title"]
                description = group.get("description") or ""
                if nps_item_page_rights_exception(title, description + " " + parsed.get("page_text", "")):
                    report.append({
                        "id": "nps-skip-" + hashlib.sha256((page_url + title).encode("utf-8")).hexdigest()[:12],
                        "status": "skipped",
                        "reason": "item caption contains a rights exception",
                        "title": title[:240],
                        "source_page": page_url,
                    })
                    continue
                media_options = group.get("media_candidates") or []
                if not media_options:
                    continue
                selected: dict[str, Any] | None = None
                failures = []
                for media in media_options:
                    url = media["url"]
                    if url in seen_media:
                        continue
                    if source_bytes >= MAX_TOTAL_SOURCE_BYTES:
                        failures.append("aggregate NPS source-byte ceiling reached")
                        break
                    source_path = Path(root) / ".staging" / (hashlib.sha256(url.encode("utf-8")).hexdigest() + ".source.mp4")
                    output_path = Path(root) / "third-party" / "nps" / "broll" / (f"{_slug(title)}-{hashlib.sha256(url.encode('utf-8')).hexdigest()[:10]}.mp4")
                    try:
                        file_size, source_hash = _download_nps_source(url, source_path)
                        if source_bytes + file_size > MAX_TOTAL_SOURCE_BYTES:
                            source_path.unlink(missing_ok=True)
                            failures.append("aggregate NPS source-byte ceiling reached")
                            break
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        video_info = _strip_nps_audio_with_ffmpeg(source_path, output_path)
                        source_path.unlink(missing_ok=True)
                        selected = {
                            "media": media,
                            "source_url": url,
                            "source_size": file_size,
                            "source_sha256": source_hash,
                            "output_path": output_path,
                            "video_info": video_info,
                        }
                        break
                    except Exception as exc:
                        source_path.unlink(missing_ok=True)
                        output_path.unlink(missing_ok=True)
                        failures.append(str(exc)[:300])
                if not selected:
                    if failures:
                        report.append({
                            "id": "nps-fail-" + hashlib.sha256((page_url + title).encode("utf-8")).hexdigest()[:12],
                            "status": "skipped" if any("ceiling" in reason for reason in failures) else "failed",
                            "reason": "; ".join(failures[-3:]),
                            "title": title[:240],
                            "source_page": page_url,
                        })
                    continue

                output_path = selected["output_path"]
                if selected["source_sha256"] in seen_source_hashes:
                    output_path.unlink(missing_ok=True)
                    source_bytes += selected["source_size"]
                    report.append({
                        "id": "nps-duplicate-" + hashlib.sha256(selected["source_url"].encode("utf-8")).hexdigest()[:12],
                        "status": "duplicate",
                        "source_page": page_url,
                        "source_sha256": selected["source_sha256"],
                        "reason": "identical source bytes already imported from another NPS source URL",
                    })
                    continue
                seen_source_hashes.add(selected["source_sha256"])
                output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
                output_size = output_path.stat().st_size
                people_review = bool(NPS_REVIEW_PEOPLE_RE.search(title + " " + description))
                exact_credit = media_page_credit or collection_credit or "National Park Service"
                item_credit_required = credit_required or bool(media_page_credit)
                source_page = page_url
                item_id = hashlib.sha256(selected["source_url"].encode("utf-8")).hexdigest()[:16]
                entry = {
                    "id": "nps-broll-" + item_id,
                    "path": output_path.relative_to(root).as_posix(),
                    "type": "nps-broll-video",
                    "title": title[:300],
                    "description": description[:3000],
                    "park": source_info["park"],
                    "collection": source_info["id"],
                    "source_page": source_page,
                    "collection_page": collection_url,
                    "source_file_url": selected["source_url"],
                    "source_sha256": selected["source_sha256"],
                    "source_sha256_method": "computed after download; NPS does not publish an item checksum on these B-roll pages",
                    "source_size_bytes": selected["source_size"],
                    "sha256": output_hash,
                    "size_bytes": output_size,
                    "width": selected["video_info"].get("width"),
                    "height": selected["video_info"].get("height"),
                    "video_codec": selected["video_info"].get("video_codec"),
                    "duration_seconds": selected["video_info"].get("duration_seconds"),
                    "source_resolution_label": selected["media"].get("label"),
                    "source_resolution_rank": selected["media"].get("resolution"),
                    "license": "Public Domain (explicit National Park Service B-roll collection statement; not CC0)",
                    "license_url": collection_url,
                    "public_domain_verified": True,
                    "rights_basis": "The official NPS collection page explicitly states that the listed B-roll videos are public domain and may be used without an NPS release. Item captions containing third-party, copyrighted, licensed or permission-required material are rejected. Do not imply NPS endorsement or reproduce the protected NPS arrowhead.",
                    "credit_text": exact_credit,
                    "credit_required_visible": item_credit_required,
                    "credit_note": "Preserve the exact NPS item-level credit when present; otherwise preserve any explicit collection credit. Do not imply NPS endorsement.",
                    "audio_stripped": True,
                    "modifications_disclosed": "Audio streams removed; the original video stream was copied without re-encoding.",
                    "privacy_publicity_review_required": people_review,
                    "commercial_promotional_review_required_if_people_identifiable": people_review,
                    "usage_notes": "Public Domain footage from an official NPS B-roll archive, not CC0. Do not imply National Park Service endorsement. Do not use the NPS arrowhead or other protected insignia. Review identifiable people, private property, third-party marks and context before commercial/promotional publication.",
                    "redistributable": True,
                }
                index.append(entry)
                seen_media.add(selected["source_url"])
                downloads += 1
                downloads_for_index += 1
                source_bytes += selected["source_size"]
                indexed_bytes += output_size
                report.append({
                    "id": entry["id"],
                    "status": "downloaded",
                    "title": title[:240],
                    "source_page": source_page,
                    "collection_page": collection_url,
                    "source_file_url": selected["source_url"],
                    "path": entry["path"],
                    "selected_format": selected["media"]["label"],
                    "source_size_bytes": selected["source_size"],
                    "size_bytes": output_size,
                    "source_sha256": selected["source_sha256"],
                    "sha256": output_hash,
                    "resolution": f"{entry['width']}x{entry['height']}",
                    "audio_stripped": True,
                    "credit_text": exact_credit,
                    "credit_required_visible": item_credit_required,
                    "people_privacy_review_required": people_review,
                    "license": entry["license"],
                })
                time.sleep(0.12)

    gallery_report, gallery_stats = download_npgallery_broll_media(
        Path(root),
        index,
        max_downloads=max(0, MAX_DOWNLOADS - downloads),
        max_total_source_bytes=max(0, MAX_TOTAL_SOURCE_BYTES - source_bytes),
        max_metadata_bytes=max(0, MAX_METADATA_BYTES - metadata_bytes),
        seen_source_hashes=seen_source_hashes,
    )
    report.extend(gallery_report)
    downloads += gallery_stats["videos_downloaded"]
    source_bytes += gallery_stats["source_bytes_downloaded"]
    indexed_bytes += gallery_stats["indexed_resource_bytes"]
    metadata_bytes += gallery_stats["metadata_bytes"]

    report.append({
        "id": "nps-broll-build-summary",
        "status": "summary",
        "collection_indexes_checked": collection_count,
        "item_pages_inspected": pages_inspected,
        "park_archive_videos_downloaded": downloads - gallery_stats["videos_downloaded"],
        "max_park_archive_videos_per_index": MAX_PARK_ARCHIVE_DOWNLOADS_PER_INDEX,
        "npgallery_videos_downloaded": gallery_stats["videos_downloaded"],
        "npgallery_source_bytes_downloaded": gallery_stats["source_bytes_downloaded"],
        "videos_downloaded": downloads,
        "source_bytes_downloaded": source_bytes,
        "indexed_resource_bytes": indexed_bytes,
        "metadata_bytes": metadata_bytes,
        "max_downloads": MAX_DOWNLOADS,
        "max_file_bytes": MAX_VIDEO_BYTES,
        "max_total_source_bytes": MAX_TOTAL_SOURCE_BYTES,
        "source_page": "https://www.nps.gov/",
    })
    return report
