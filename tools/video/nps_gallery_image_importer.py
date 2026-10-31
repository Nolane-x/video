#!/usr/bin/env python3
"""Rights-gated importer for official NPS NPGallery public-domain photographs."""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from nps_broll_importer import (
    NPGALLERY_BASE,
    NPS_COPYRIGHT_MARK_RE,
    NPS_ITEM_RIGHTS_EXCEPTION_RE,
    NPS_REVIEW_PEOPLE_RE,
    _clean_text,
    _npgallery_is_official_url,
    _slug,
    parse_npgallery_asset_detail,
)

SEARCH_TERMS = (
    "wildlife",
    "forest",
    "mountain",
    "coast",
    "geology",
    "historic",
    "waterfall",
    "desert",
    "night sky",
    "architecture",
    "river",
)
PAGE_SIZE = 60
SEARCH_URLS = {
    term: NPGALLERY_BASE + "/SearchResults?pagesize=60&keyword=" + urllib.parse.quote(term)
    for term in SEARCH_TERMS
}
MAX_SEARCH_RESULTS_PER_TERM = 60
MAX_CANDIDATES = 480
MAX_DOWNLOADS = 300
MAX_ITEM_DETAILS = 600
MAX_PAGE_BYTES = 8 * 1024 * 1024
MAX_METADATA_BYTES = 320 * 1024 * 1024
MAX_IMAGE_BYTES = 80 * 1024 * 1024
MAX_TOTAL_SOURCE_BYTES = 9 * 1024 * 1024 * 1024
MIN_IMAGE_BYTES = 8 * 1024
ALLOWED_FORMATS = {"jpg", "jpeg", "png"}
UA = "NolaneVideoAssetLibrary-NPS-NPGallery-Images/1.0 (+https://github.com/Nolane-x/video)"
JPEG_SIGNATURE = b"\xff\xd8\xff"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
UUID_RE = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
UUID_FULL_RE = re.compile(r"^" + UUID_RE + r"$", re.IGNORECASE)


def normalize_npgallery_page_url(raw_url: str) -> str | None:
    parsed = _npgallery_is_official_url(raw_url)
    if not parsed:
        return None
    if parsed.path == "/SearchResults":
        query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        if set(query) != {"pagesize", "keyword"}:
            return None
        term = query.get("keyword", [""])[0].casefold()
        if query.get("pagesize") != [str(PAGE_SIZE)] or term not in SEARCH_URLS:
            return None
        return SEARCH_URLS[term]
    match = re.fullmatch(r"/AssetDetail/(" + UUID_RE + r")", parsed.path, re.IGNORECASE)
    if not match or parsed.query:
        return None
    return f"{NPGALLERY_BASE}/AssetDetail/{match.group(1).lower()}"


def normalize_npgallery_original_url(raw_url: str, asset_id: str, resource_format: str) -> str | None:
    if not UUID_FULL_RE.fullmatch(str(asset_id or "")):
        return None
    fmt = str(resource_format or "").casefold()
    if fmt not in ALLOWED_FORMATS:
        return None
    parsed = _npgallery_is_official_url(raw_url)
    if not parsed or parsed.query:
        return None
    expected = f"/GetAsset/{asset_id.lower()}/original.{fmt}"
    if parsed.path.casefold() != expected.casefold():
        return None
    return f"{NPGALLERY_BASE}{expected}"


def _extract_search_object(page_html: str) -> dict[str, Any]:
    match = re.search(r"\bvar\s+search\s*=\s*", page_html or "")
    if not match:
        raise RuntimeError("NPGallery search payload was not found")
    start = (page_html or "").find("{", match.end())
    if start < 0:
        raise RuntimeError("NPGallery search payload has no JSON object")
    payload, _ = json.JSONDecoder().raw_decode((page_html or "")[start:])
    if not isinstance(payload, dict):
        raise RuntimeError("NPGallery search payload is not an object")
    return payload


def parse_npgallery_image_search_results(page_html: str, search_url: str) -> list[dict[str, Any]]:
    """Keep only file-backed image assets with full Public Domain rights and an NPS credit."""
    if normalize_npgallery_page_url(search_url) != search_url:
        raise RuntimeError("NPGallery image search URL is outside the exact query allow-list")
    payload = _extract_search_object(page_html)
    eligible: list[dict[str, Any]] = []
    for row in (payload.get("Results") or [])[:MAX_SEARCH_RESULTS_PER_TERM]:
        asset = row.get("Asset") or {}
        rights = asset.get("ConstraintsInformation") or {}
        asset_id = str(asset.get("AssetID") or "").strip()
        photo_credit = str(asset.get("PhotoCredit") or "").strip()
        resource_format = str(asset.get("ResourceFormat") or "").casefold()
        if (
            not UUID_FULL_RE.fullmatch(asset_id)
            or str(asset.get("AssetBaseType") or "").casefold() != "file"
            or str(asset.get("PrimaryType") or "").casefold() != "image"
            or str(asset.get("ResourceType") or "").casefold() != "image"
            or resource_format not in ALLOWED_FORMATS
            or str(rights.get("Constraint") or "").casefold() != "public domain"
            or str(rights.get("GrantingRights") or "").casefold() != "full"
            or "nps" not in photo_credit.casefold()
        ):
            continue
        candidate = dict(asset)
        candidate["NPGallerySearchURL"] = search_url
        eligible.append(candidate)
    return eligible


IMAGE_RIGHTS_EXCEPTION_RE = re.compile(
    r"third[-\s]?party(?:\s+partner)?\s+(?:image|photo|photograph|picture|artwork|content)|"
    r"copyright(?:ed)?\s+(?:image|photo|photograph|picture|artwork)|"
    r"licensed\s+(?:image|photo|photograph|picture|artwork)|"
    r"used\s+with\s+permission|permission\s+(?:is\s+)?required|"
    r"all\s+rights\s+reserved|not\s+(?:in\s+the\s+)?public\s+domain|"
    r"non[-\s]?commercial|not\s+cleared\s+for\s+(?:commercial|public)",
    re.IGNORECASE,
)


def _rights_exception_text(asset: dict[str, Any], detail: dict[str, str]) -> str:
    values = [
        asset.get("Title"),
        asset.get("Description"),
        asset.get("AltText"),
        detail.get("Title"),
        detail.get("Description"),
        detail.get("AltText"),
        detail.get("Copyright"),
    ]
    return " ".join(str(value or "") for value in values)


def npgallery_image_rights_verified(
    asset: dict[str, Any],
    detail: dict[str, str],
    asset_id: str,
) -> bool:
    rights = asset.get("ConstraintsInformation") or {}
    detail_rights = re.sub(
        r"\s+", " ", detail.get("Constraints Information", "")
    ).strip().casefold()
    detail_format = detail.get("Resource Format", "").casefold()
    search_format = str(asset.get("ResourceFormat") or "").casefold()
    search_credit = str(asset.get("PhotoCredit") or "").strip()
    detail_credit = detail.get("PhotoCredit", "").strip()
    exception_text = _rights_exception_text(asset, detail)
    return bool(
        detail.get("Asset ID", "").strip().lower() == asset_id.lower()
        and str(rights.get("Constraint") or "").casefold() == "public domain"
        and str(rights.get("GrantingRights") or "").casefold() == "full"
        and detail_rights.replace(" ", "") == "publicdomain:fullgrantingrights"
        and str(asset.get("PrimaryType") or "").casefold() == "image"
        and str(asset.get("ResourceType") or "").casefold() == "image"
        and detail.get("Resource Type", "").casefold() == "image"
        and search_format in ALLOWED_FORMATS
        and detail_format == search_format
        and detail.get("Access Constraints", "").casefold() == "public can view"
        and "nps" in search_credit.casefold()
        and "nps" in detail_credit.casefold()
        and not NPS_COPYRIGHT_MARK_RE.search(detail_credit)
        and not NPS_ITEM_RIGHTS_EXCEPTION_RE.search(exception_text)
        and not IMAGE_RIGHTS_EXCEPTION_RE.search(exception_text)
        and bool(detail.get("Title"))
    )


def _urlopen_with_retry(
    request: urllib.request.Request,
    *,
    timeout: int,
    attempts: int = 3,
):
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except urllib.error.HTTPError as exc:
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt + 1 >= attempts:
                raise
            retry_after = (exc.headers.get("Retry-After") or "").strip()
            try:
                delay = float(retry_after)
            except ValueError:
                delay = 1.5 * (attempt + 1)
            time.sleep(min(12.0, max(0.5, delay)))
        except urllib.error.URLError:
            if attempt + 1 >= attempts:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("NPGallery request exhausted its retry budget")


def _fetch_npgallery_page(url: str, limit: int = MAX_PAGE_BYTES, timeout: int = 35) -> bytes:
    normalized = normalize_npgallery_page_url(url)
    if not normalized:
        raise RuntimeError("NPGallery page URL is outside the exact official HTTPS allow-list")
    request = urllib.request.Request(
        normalized,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with _urlopen_with_retry(request, timeout=timeout) as response:
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


def _image_signature_is_valid(path: Path, resource_format: str) -> bool:
    with path.open("rb") as handle:
        header = handle.read(32)
    fmt = resource_format.casefold()
    if fmt in {"jpg", "jpeg"}:
        return header.startswith(JPEG_SIGNATURE)
    if fmt == "png":
        return header.startswith(PNG_SIGNATURE)
    return False


def _image_dimensions(path: Path, resource_format: str) -> tuple[int | None, int | None]:
    fmt = resource_format.casefold()
    if fmt == "png":
        with path.open("rb") as handle:
            header = handle.read(24)
        if len(header) >= 24 and header.startswith(PNG_SIGNATURE) and header[12:16] == b"IHDR":
            width = int.from_bytes(header[16:20], "big")
            height = int.from_bytes(header[20:24], "big")
            return (width, height) if width > 0 and height > 0 else (None, None)
        return None, None
    if fmt in {"jpg", "jpeg"}:
        with path.open("rb") as handle:
            data = handle.read(4 * 1024 * 1024)
        if not data.startswith(JPEG_SIGNATURE):
            return None, None
        offset = 2
        sof_markers = {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }
        while offset + 9 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if offset + 2 > len(data):
                break
            segment_length = int.from_bytes(data[offset:offset + 2], "big")
            if segment_length < 2 or offset + segment_length > len(data):
                break
            if marker in sof_markers and segment_length >= 7:
                height = int.from_bytes(data[offset + 3:offset + 5], "big")
                width = int.from_bytes(data[offset + 5:offset + 7], "big")
                return (width, height) if width > 0 and height > 0 else (None, None)
            offset += segment_length
    return None, None


def _download_npgallery_image(
    url: str,
    asset_id: str,
    resource_format: str,
    destination: Path,
    *,
    max_bytes: int = MAX_IMAGE_BYTES,
) -> tuple[int, str]:
    normalized = normalize_npgallery_original_url(url, asset_id, resource_format)
    if not normalized:
        raise RuntimeError("NPGallery original image URL is outside the exact asset-specific allow-list")
    fmt = resource_format.casefold()
    allowed_mimes = {"image/jpeg", "image/jpg"} if fmt in {"jpg", "jpeg"} else {"image/png"}
    request = urllib.request.Request(
        normalized,
        headers={
            "User-Agent": UA,
            "Accept": ", ".join(sorted(allowed_mimes)) + ",application/octet-stream",
            "Accept-Encoding": "identity",
            "Referer": f"{NPGALLERY_BASE}/AssetDetail/{asset_id.lower()}",
        },
    )
    digest = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with _urlopen_with_retry(request, timeout=90) as response:
        final = normalize_npgallery_original_url(response.geturl(), asset_id, fmt)
        if final != normalized:
            raise RuntimeError("NPGallery image download redirected outside the exact original endpoint")
        content_type = response.headers.get("Content-Type", "application/octet-stream").split(";", 1)[0].strip().casefold()
        if content_type not in allowed_mimes | {"application/octet-stream", "binary/octet-stream"}:
            raise RuntimeError(f"unexpected NPGallery image MIME type: {content_type}")
        length = response.headers.get("Content-Length")
        if length and int(length) > min(MAX_IMAGE_BYTES, max_bytes):
            raise RuntimeError("NPGallery image exceeds the remaining source-byte ceiling")
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > min(MAX_IMAGE_BYTES, max_bytes):
                    raise RuntimeError("NPGallery image exceeds the per-file or aggregate byte ceiling")
                digest.update(chunk)
                output.write(chunk)
    if total < MIN_IMAGE_BYTES:
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPGallery original image is unexpectedly small")
    if not _image_signature_is_valid(destination, fmt):
        destination.unlink(missing_ok=True)
        raise RuntimeError("NPGallery original image signature does not match its declared format")
    return total, digest.hexdigest()


def download_nps_npgallery_images(root: Path, index: list[dict]) -> list[dict]:
    """Download bounded NPS photographs only after item-level Full Public Domain rights checks."""
    report: list[dict] = []
    metadata_bytes = 0
    source_bytes = 0
    indexed_bytes = 0
    downloads = 0
    pages_inspected = 0
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    candidate_groups: list[list[dict[str, Any]]] = []

    for term, search_url in SEARCH_URLS.items():
        if metadata_bytes >= MAX_METADATA_BYTES:
            break
        try:
            body = _fetch_npgallery_page(search_url, limit=min(MAX_PAGE_BYTES, MAX_METADATA_BYTES - metadata_bytes))
            metadata_bytes += len(body)
            candidates = parse_npgallery_image_search_results(body.decode("utf-8", "replace"), search_url)
            for candidate in candidates:
                candidate["NPGallerySearchURL"] = search_url
            candidate_groups.append(candidates)
            report.append({
                "id": "nps-photo-search-" + _slug(term),
                "status": "searched",
                "source_page": search_url,
                "eligible_search_records": len(candidates),
                "rights_filter": "file + image + JPG/JPEG/PNG + Public domain + Full Granting Rights + NPS credit",
            })
        except Exception as exc:
            report.append({
                "id": "nps-photo-search-" + _slug(term),
                "status": "search-failed",
                "source_page": search_url,
                "reason": str(exc)[:400],
            })

    # Interleave topic searches so one broad keyword does not monopolize the image budget.
    candidates: list[dict[str, Any]] = []
    positions = [0] * len(candidate_groups)
    while len(candidates) < MAX_CANDIDATES:
        progressed = False
        for group_index, group in enumerate(candidate_groups):
            while positions[group_index] < len(group):
                candidate = group[positions[group_index]]
                positions[group_index] += 1
                asset_id = str(candidate.get("AssetID") or "").lower()
                if not asset_id or asset_id in seen_ids:
                    continue
                seen_ids.add(asset_id)
                candidates.append(candidate)
                progressed = True
                break
            if len(candidates) >= MAX_CANDIDATES:
                break
        if not progressed:
            break

    report.append({
        "id": "nps-photo-candidate-summary",
        "status": "summary",
        "search_terms": list(SEARCH_TERMS),
        "unique_candidate_count": len(candidates),
        "candidate_deduplication": "interleaved topic searches, unique NPGallery AssetID",
    })

    max_detail_candidates = min(MAX_ITEM_DETAILS, max(MAX_DOWNLOADS, MAX_DOWNLOADS * 2))
    for asset in candidates[:max_detail_candidates]:
        if downloads >= MAX_DOWNLOADS or source_bytes >= MAX_TOTAL_SOURCE_BYTES or metadata_bytes >= MAX_METADATA_BYTES:
            break
        asset_id = str(asset.get("AssetID") or "").lower()
        if not UUID_FULL_RE.fullmatch(asset_id):
            continue
        detail_url = f"{NPGALLERY_BASE}/AssetDetail/{asset_id}"
        fmt = str(asset.get("ResourceFormat") or "").casefold()
        try:
            detail_body = _fetch_npgallery_page(
                detail_url,
                limit=min(MAX_PAGE_BYTES, MAX_METADATA_BYTES - metadata_bytes),
            )
            metadata_bytes += len(detail_body)
            pages_inspected += 1
            detail = parse_npgallery_asset_detail(detail_body.decode("utf-8", "replace"))
            if not npgallery_image_rights_verified(asset, detail, asset_id):
                report.append({
                    "id": "nps-photo-" + asset_id[:12],
                    "status": "skipped_rights_exception",
                    "source_page": detail_url,
                    "title": detail.get("Title") or asset.get("Title", ""),
                    "reason": "detail page does not reconfirm Public domain: Full Granting Rights, image format, Public Can View and NPS credit",
                })
                continue
        except Exception as exc:
            report.append({
                "id": "nps-photo-" + asset_id[:12],
                "status": "detail-failed",
                "source_page": detail_url,
                "reason": str(exc)[:350],
            })
            continue

        title = detail.get("Title") or str(asset.get("Title") or "NPS photograph")
        description = detail.get("Description") or str(asset.get("Description") or "")
        alt_text = detail.get("AltText") or str(asset.get("AltText") or "")
        credit = detail.get("PhotoCredit", "").strip()
        original_url = f"{NPGALLERY_BASE}/GetAsset/{asset_id}/original.{fmt}"
        output_path = Path(root) / "third-party" / "nps" / "npgallery" / "images" / (
            f"{_slug(title)}-{asset_id[:10]}.{fmt}"
        )
        source_path = Path(root) / ".staging" / (asset_id + ".nps-image-source." + fmt)
        try:
            remaining = MAX_TOTAL_SOURCE_BYTES - source_bytes
            file_size, source_hash = _download_npgallery_image(
                original_url,
                asset_id,
                fmt,
                source_path,
                max_bytes=min(MAX_IMAGE_BYTES, remaining),
            )
            if source_bytes + file_size > MAX_TOTAL_SOURCE_BYTES:
                source_path.unlink(missing_ok=True)
                report.append({
                    "id": "nps-photo-" + asset_id[:12],
                    "status": "skipped",
                    "source_page": detail_url,
                    "reason": "aggregate NPS image source-byte ceiling reached",
                })
                break
            if source_hash in seen_hashes:
                source_path.unlink(missing_ok=True)
                source_bytes += file_size
                report.append({
                    "id": "nps-photo-" + asset_id[:12],
                    "status": "duplicate",
                    "source_page": detail_url,
                    "source_sha256": source_hash,
                    "reason": "identical original image bytes already imported from an earlier NPGallery asset",
                })
                continue
            seen_hashes.add(source_hash)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(source_path, output_path)
            source_path.unlink(missing_ok=True)
        except Exception as exc:
            source_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
            report.append({
                "id": "nps-photo-" + asset_id[:12],
                "status": "failed",
                "source_page": detail_url,
                "source_file_url": original_url,
                "title": title[:240],
                "reason": str(exc)[:400],
            })
            continue

        output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
        width, height = _image_dimensions(output_path, fmt)
        people_review = bool(NPS_REVIEW_PEOPLE_RE.search(title + " " + description + " " + alt_text))
        unit = detail.get("NPS Units", "").strip()
        search_url = str(asset.get("NPGallerySearchURL") or SEARCH_URLS[SEARCH_TERMS[0]])
        entry = {
            "id": "nps-photo-" + asset_id,
            "path": output_path.relative_to(root).as_posix(),
            "type": "nps-photograph",
            "title": title[:300],
            "description": description[:3000],
            "alt_text": alt_text[:2000],
            "park": unit,
            "collection": "nps-npgallery-curated-image-search",
            "source_page": detail_url,
            "collection_page": search_url,
            "source_file_url": original_url,
            "source_sha256": source_hash,
            "source_sha256_method": "computed after download; NPGallery detail metadata does not publish a per-file SHA-256",
            "source_size_bytes": file_size,
            "sha256": output_hash,
            "size_bytes": output_path.stat().st_size,
            "width": width,
            "height": height,
            "format": fmt,
            "license": "Public Domain (NPGallery item-level Public domain: Full Granting Rights; not CC0)",
            "license_url": detail_url,
            "public_domain_verified": True,
            "rights_basis": "The individual NPGallery Asset Detail page reconfirms the matching Asset ID, Public domain: Full Granting Rights, Resource Type Image, an approved original image format, Access Constraints Public Can View and an NPS PhotoCredit. Search results alone are never treated as sufficient permission.",
            "credit_text": credit,
            "copyright_text": detail.get("Copyright", "")[:1200],
            "credit_required_visible": True,
            "credit_note": "Preserve NPGallery PhotoCredit verbatim; do not imply NPS endorsement.",
            "privacy_publicity_review_required": people_review,
            "commercial_promotional_review_required_if_people_identifiable": people_review,
            "usage_notes": "NPGallery item-level Public Domain with Full Granting Rights, not CC0. Preserve PhotoCredit, do not imply NPS endorsement or use protected NPS insignia, and review identifiable people, private property, cultural sensitivity and third-party marks before commercial/promotional publication.",
            "redistributable": True,
        }
        index.append(entry)
        downloads += 1
        source_bytes += file_size
        indexed_bytes += entry["size_bytes"]
        report.append({
            "id": entry["id"],
            "status": "downloaded",
            "title": title[:240],
            "source_page": detail_url,
            "source_file_url": original_url,
            "path": entry["path"],
            "selected_format": fmt,
            "source_size_bytes": file_size,
            "size_bytes": entry["size_bytes"],
            "source_sha256": source_hash,
            "sha256": output_hash,
            "resolution": f"{width}x{height}" if width and height else None,
            "credit_text": credit,
            "credit_required_visible": True,
            "people_privacy_review_required": people_review,
            "license": entry["license"],
        })
        time.sleep(0.08)

    report.append({
        "id": "nps-npgallery-image-build-summary",
        "status": "summary",
        "search_terms": list(SEARCH_TERMS),
        "search_pages": len(candidate_groups),
        "item_details_inspected": pages_inspected,
        "images_downloaded": downloads,
        "source_bytes_downloaded": source_bytes,
        "indexed_resource_bytes": indexed_bytes,
        "metadata_bytes": metadata_bytes,
        "max_downloads": MAX_DOWNLOADS,
        "max_file_bytes": MAX_IMAGE_BYTES,
        "max_total_source_bytes": MAX_TOTAL_SOURCE_BYTES,
        "source_page": NPGALLERY_BASE,
    })
    return report


