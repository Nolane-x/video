#!/usr/bin/env python3
"""Rights-gated importer for official CDC B-roll videos."""
from __future__ import annotations

import hashlib
import html
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

BASE = "https://www.cdc.gov"
INDEX_URL = BASE + "/media/b-roll/index.html"
CATEGORY_PATHS = {
    "/media/media/b-roll/cdc-exterior.html",
    "/media/media/b-roll/cdc-in-the-field.html",
    "/media/media/b-roll/cdc-operations-and-facilities.html",
    "/media/media/b-roll/outbreaks-and-diseases.html",
    "/media/media/b-roll/Mosquitoes-and-Ticks.html",
}
MAX_CATEGORY_PAGES = 8
MAX_SECTION_MEDIA_CANDIDATES = 300
MAX_DOWNLOADS = 60
MAX_PAGE_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 300 * 1024 * 1024
MAX_TOTAL_BYTES = 4 * 1024 * 1024 * 1024
MIN_VIDEO_BYTES = 20_000
UA = "NolaneVideoAssetLibrary-CDC/1.0 (+https://github.com/Nolane-x/video)"
ALLOWED_MIME = {"video/mp4", "video/quicktime", "application/mp4", "application/octet-stream"}
RIGHTS_EXCEPTION_RE = re.compile(
    r"\bcopyright(?:ed| holder)?\b|third[- ]party|"
    r"licensed (?:music|footage|content|material)|all rights reserved|"
    r"permission required|not (?:in the )?public domain|"
    r"reproduction prohibited",
    re.IGNORECASE,
)
HUMAN_CONTEXT_RE = re.compile(
    r"\b(patient|patients|children|child|students?|interviewee|interview|"
    r"portrait|vaccination|clinic|hospital|identifiable person)\b",
    re.IGNORECASE,
)
MEDIA_PATH_RE = re.compile(
    r"^/media/video/(?:b-roll|fullvideo)/[A-Za-z0-9._%()/+-]+\.(?:mp4|mov)$",
    re.IGNORECASE,
)


def normalize_cdc_category_url(raw_url: str) -> str | None:
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if (
            parsed.scheme.casefold() != "https"
            or (parsed.hostname or "").casefold() != "www.cdc.gov"
            or parsed.port not in (None, 443)
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in CATEGORY_PATHS
        ):
            return None
        return urllib.parse.urlunsplit(("https", "www.cdc.gov", parsed.path, "", ""))
    except (TypeError, ValueError):
        return None


def normalize_cdc_media_url(raw_url: str) -> str | None:
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or "").strip())
        if (
            parsed.scheme.casefold() != "https"
            or (parsed.hostname or "").casefold() != "www.cdc.gov"
            or parsed.port not in (None, 443)
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or not MEDIA_PATH_RE.fullmatch(parsed.path)
            or re.search(r"%(?![0-9A-Fa-f]{2})", parsed.path)
        ):
            return None
        return urllib.parse.urlunsplit(("https", "www.cdc.gov", parsed.path, "", ""))
    except (TypeError, ValueError):
        return None


def cdc_media_response_url_is_allowed(requested_url: str, response_url: str) -> bool:
    requested = normalize_cdc_media_url(requested_url)
    return bool(requested and normalize_cdc_media_url(response_url) == requested)


class _CDCIndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.links: list[str] = []
        self.anchor_href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.casefold(): value or "" for key, value in attrs}
        if tag == "a":
            self.anchor_href = attr.get("href")

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.anchor_href is not None:
            self.links.append(self.anchor_href)
            self.anchor_href = None


def parse_cdc_index_page(page_html: str) -> list[str]:
    parser = _CDCIndexParser()
    parser.feed(page_html)
    parser.close()
    visible_text = " ".join(" ".join(parser.text_parts).split()).casefold()
    required_notice = (
        "cdc b-roll is produced by the united states government and is in the public domain"
    )
    if required_notice not in visible_text:
        raise RuntimeError("CDC B-roll index does not contain the expected Public Domain notice")
    categories: list[str] = []
    for link in parser.links:
        absolute = urllib.parse.urljoin(BASE + "/", link)
        normalized = normalize_cdc_category_url(absolute)
        if normalized and normalized not in categories:
            categories.append(normalized)
    return categories[:MAX_CATEGORY_PAGES]


class _CDCSectionParser(HTMLParser):
    """Parse one CDC DFE section at a time and bind its heading/caption to its MP4/MOV links."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.div_depth = 0
        self.section_depth: int | None = None
        self.current: dict[str, Any] | None = None
        self.in_heading = False
        self.in_caption = False
        self.anchor: dict[str, Any] | None = None
        self.sections: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.casefold(): value or "" for key, value in attrs}
        if tag == "div":
            self.div_depth += 1
            classes = set(attr.get("class", "").casefold().split())
            if (
                self.current is None
                and "dfe-section" in classes
                and "dfe-section--page-summary" not in classes
            ):
                self.section_depth = self.div_depth
                self.current = {
                    "title_parts": [],
                    "caption_parts": [],
                    "text_parts": [],
                    "media_links": [],
                }
        if self.current is None:
            return
        if tag == "h2":
            self.in_heading = True
        elif tag == "figcaption":
            self.in_caption = True
        elif tag == "a":
            self.anchor = {"href": attr.get("href", ""), "text_parts": []}

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.current is None:
            return
        self.current["text_parts"].append(data)
        if self.in_heading:
            self.current["title_parts"].append(data)
        if self.in_caption:
            self.current["caption_parts"].append(data)
        if self.anchor is not None:
            self.anchor["text_parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current is not None:
            if tag == "h2":
                self.in_heading = False
            elif tag == "figcaption":
                self.in_caption = False
            elif tag == "a" and self.anchor is not None:
                media_url = normalize_cdc_media_url(self.anchor.get("href", ""))
                if media_url:
                    label = " ".join(" ".join(self.anchor["text_parts"]).split())
                    self.current["media_links"].append({
                        "url": media_url,
                        "label": label[:240],
                    })
                self.anchor = None
            elif tag == "div" and self.section_depth == self.div_depth:
                self.sections.append({
                    "title": " ".join(" ".join(self.current["title_parts"]).split())[:300],
                    "caption": " ".join(" ".join(self.current["caption_parts"]).split())[:3500],
                    "section_text": " ".join(" ".join(self.current["text_parts"]).split())[:7000],
                    "media_links": self.current["media_links"],
                })
                self.current = None
                self.section_depth = None
        if tag == "div":
            self.div_depth = max(0, self.div_depth - 1)


def cdc_parse_category_page(page_html: str) -> list[dict[str, Any]]:
    parser = _CDCSectionParser()
    parser.feed(page_html)
    parser.close()
    return [section for section in parser.sections if section["media_links"]]


def cdc_section_rights_exception(section: dict[str, Any]) -> bool:
    text = " ".join([
        str(section.get("title") or ""),
        str(section.get("caption") or ""),
        str(section.get("section_text") or ""),
    ])
    return bool(RIGHTS_EXCEPTION_RE.search(text))


def cdc_choose_video_candidate(section: dict[str, Any]) -> dict[str, Any] | None:
    links = [row for row in section.get("media_links", []) if normalize_cdc_media_url(row.get("url"))]
    if not links:
        return None

    # Prefer a single complete clip over split fragments.
    complete = [
        row for row in links
        if re.search(r"\b(entire clip|full clip|complete clip)\b", str(row.get("label") or ""), re.I)
    ]
    if complete:
        links = complete

    def rank(row: dict[str, Any]) -> tuple[int, int]:
        label = str(row.get("label") or "").casefold()
        url = str(row.get("url") or "").casefold()
        combined = label + " " + url
        score = 0
        if re.search(r"\b4k\b|2160", combined):
            score += 60
        elif re.search(r"\b1080\b|1920", combined):
            score += 50
        elif re.search(r"high[- ]?res|hi[- ]?res|full size", combined):
            score += 40
        elif re.search(r"download file|full size b-roll", combined):
            score += 30
        elif "b-roll video" in label or "download" in label:
            score += 20
        if re.search(r"low[- ]?res|preview", combined):
            score -= 25
        if "alpha" in combined or "transparent" in combined:
            score -= 2
        # Prefer MP4 to MOV when quality labels are otherwise equal.
        if url.endswith(".mp4"):
            score += 1
        return score, len(url)

    return sorted(links, key=rank, reverse=True)[0]


def _fetch_cdc_page(url: str, limit: int = MAX_PAGE_BYTES, timeout: int = 35) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "www.cdc.gov" or parsed.port not in (None, 443):
        raise RuntimeError("CDC page URL failed the exact HTTPS host allow-list")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError("CDC page URL contains credentials, query or fragment")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final = urllib.parse.urlsplit(response.geturl())
        if (
            final.scheme != "https"
            or final.hostname != "www.cdc.gov"
            or final.port not in (None, 443)
            or final.username
            or final.password
            or final.query
            or final.fragment
            or final.path != parsed.path
        ):
            raise RuntimeError("CDC page redirected away from its exact official page")
        content_type = response.headers.get("Content-Type", "text/html").split(";", 1)[0].strip().casefold()
        if content_type not in {"text/html", "application/xhtml+xml"}:
            raise RuntimeError("CDC page response is not HTML")
        length = response.headers.get("Content-Length")
        if length and int(length) > limit:
            raise RuntimeError("CDC page exceeded its byte ceiling")
        body = response.read(limit + 1)
    if len(body) > limit:
        raise RuntimeError("CDC page exceeded its byte ceiling")
    return body


def _download_cdc_video(url: str, destination: Path) -> tuple[int, str, str]:
    normalized = normalize_cdc_media_url(url)
    if not normalized:
        raise RuntimeError("CDC video URL failed the exact official media path allow-list")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "video/mp4,video/quicktime,application/octet-stream", "Accept-Encoding": "identity"},
    )
    digest = hashlib.sha256()
    total = 0
    first = b""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=100) as response:
        if not cdc_media_response_url_is_allowed(normalized, response.geturl()):
            raise RuntimeError("CDC media redirect left the exact official URL")
        mime = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
        if mime not in ALLOWED_MIME:
            raise RuntimeError("unexpected CDC video MIME type: " + mime)
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_FILE_BYTES:
            raise RuntimeError("CDC video exceeds per-file byte ceiling")
        with destination.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_FILE_BYTES:
                    raise RuntimeError("CDC video exceeds per-file byte ceiling")
                if len(first) < 64:
                    first += chunk[:64 - len(first)]
                digest.update(chunk)
                out.write(chunk)
    if total < MIN_VIDEO_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError("CDC video is unexpectedly small")
    if b"ftyp" not in first[:64]:
        destination.unlink(missing_ok=True)
        raise RuntimeError("CDC ISO-BMFF video signature is missing")
    return total, digest.hexdigest(), mime


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(value or "").casefold()).strip("-")
    return (slug[:88] or "cdc-broll")


def download_cdc_broll_videos(root: Path, index: list[dict]) -> list[dict]:
    """Import bounded CDC B-roll files under the CDC B-roll page's public-domain notice."""
    report: list[dict] = []
    total_bytes = 0
    downloaded = 0
    seen_urls: set[str] = set()

    index_body = _fetch_cdc_page(INDEX_URL)
    category_urls = parse_cdc_index_page(index_body.decode("utf-8", "replace"))
    if not category_urls:
        raise RuntimeError("CDC B-roll index did not provide any allow-listed category pages")
    report.append({
        "id": "cdc-broll-index",
        "status": "verified",
        "source_page": INDEX_URL,
        "rights_basis": "The official CDC B-roll index explicitly states that CDC B-roll is produced by the U.S. Government and is in the public domain; CDC requests source credit.",
        "category_pages_discovered": len(category_urls),
    })

    for category_url in category_urls[:MAX_CATEGORY_PAGES]:
        if downloaded >= MAX_DOWNLOADS or total_bytes >= MAX_TOTAL_BYTES:
            break
        try:
            page_body = _fetch_cdc_page(category_url)
            sections = cdc_parse_category_page(page_body.decode("utf-8", "replace"))
            report.append({
                "id": "cdc-broll-category-" + _safe_slug(urllib.parse.urlsplit(category_url).path.rsplit("/", 1)[-1]),
                "status": "inspected",
                "source_page": category_url,
                "sections_with_video_links": len(sections),
            })
        except Exception as exc:
            report.append({
                "id": "cdc-broll-category-" + _safe_slug(category_url),
                "status": "page_failed",
                "source_page": category_url,
                "reason": str(exc)[:350],
            })
            continue

        for section in sections:
            if downloaded >= MAX_DOWNLOADS or total_bytes >= MAX_TOTAL_BYTES:
                break
            title = str(section.get("title") or "CDC B-roll clip")
            caption = str(section.get("caption") or "")
            candidate_urls = section.get("media_links") or []
            chosen = cdc_choose_video_candidate(section)
            if cdc_section_rights_exception(section):
                report.append({
                    "id": "cdc-broll-skipped-" + _safe_slug(title),
                    "status": "skipped_rights_exception",
                    "title": title,
                    "source_page": category_url,
                    "reason": "The exact CDC B-roll section contains a copyright, third-party, licensing or permission exception marker.",
                })
                continue
            if not chosen:
                continue
            media_url = chosen["url"]
            if media_url in seen_urls:
                continue
            seen_urls.add(media_url)
            row_id = "cdc-broll-" + hashlib.sha256((category_url + "|" + title + "|" + media_url).encode("utf-8")).hexdigest()[:18]
            row = {
                "id": row_id,
                "provider": "Centers for Disease Control and Prevention",
                "title": title[:300],
                "caption": caption[:3500],
                "source_page": category_url,
                "source_file_url": media_url,
                "download_label": chosen["label"][:240],
                "license": "Public Domain (official CDC B-roll government-production notice; item exception screen)",
                "license_url": INDEX_URL,
                "rights_verification": "Official CDC B-roll index Public Domain notice plus exact linked B-roll category section inspection",
            }
            target = Path(root) / "third-party" / "cdc" / "video" / (
                _safe_slug(title) + "-" + row_id.rsplit("-", 1)[-1] + Path(urllib.parse.urlsplit(media_url).path).suffix.lower()
            )
            try:
                size, digest, mime = _download_cdc_video(media_url, target)
                if total_bytes + size > MAX_TOTAL_BYTES:
                    target.unlink(missing_ok=True)
                    row.update(
                        status="skipped_total_size_limit",
                        reason="The CDC video would exceed the aggregate CDC B-roll byte budget.",
                    )
                    report.append(row)
                    break
                human_review = bool(HUMAN_CONTEXT_RE.search(title + " " + caption))
                entry = {
                    "id": row_id,
                    "path": target.relative_to(root).as_posix(),
                    "type": "cdc-broll-video",
                    "title": title[:300],
                    "description": caption[:3500],
                    "provider": "Centers for Disease Control and Prevention",
                    "category": "Public health, CDC operations, disease prevention and field B-roll",
                    "source_page": category_url,
                    "source_file_url": media_url,
                    "download_label": chosen["label"][:240],
                    "license": "Public Domain (official CDC B-roll government-production notice; item exception screen)",
                    "license_url": INDEX_URL,
                    "license_verified_from_official_cdc_broll_index": True,
                    "item_rights_exception_screen_passed": True,
                    "credit_required": True,
                    "credit_text": "Centers for Disease Control and Prevention (CDC)",
                    "usage_notes": "Credit CDC as the source. Do not imply CDC endorsement. Footage may depict identifiable people, healthcare interactions or other sensitive real-world contexts; review privacy/publicity releases and intended use before commercial/promotional publication.",
                    "human_context_review_required": human_review,
                    "privacy_publicity_review_required": True,
                    "redistributable": True,
                    "size_bytes": size,
                    "sha256": digest,
                    "mime_type": mime,
                }
                index.append(entry)
                total_bytes += size
                downloaded += 1
                row.update(
                    status="downloaded",
                    path=entry["path"],
                    size_bytes=size,
                    sha256=digest,
                    mime_type=mime,
                    credit_required=True,
                    human_context_review_required=human_review,
                )
                report.append(row)
            except Exception as exc:
                target.unlink(missing_ok=True)
                row.update(status="download_failed", reason=str(exc)[:420])
                report.append(row)
            time.sleep(0.25)

    report.append({
        "id": "cdc-broll-summary",
        "status": "summary",
        "category_pages_inspected": sum(row.get("status") == "inspected" for row in report),
        "downloaded_videos": downloaded,
        "indexed_resource_bytes": total_bytes,
        "max_downloads": MAX_DOWNLOADS,
        "max_file_bytes": MAX_FILE_BYTES,
        "max_total_bytes": MAX_TOTAL_BYTES,
    })
    return report
