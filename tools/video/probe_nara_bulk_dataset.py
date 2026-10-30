#!/usr/bin/env python3
"""Probe selected NARA AWS bulk-catalog JSON files without downloading media.

This is deliberately metadata-only. It does not call the NARA Catalog API, does not
download any digital object, and does not add assets to the library. It exists to
verify the real bulk-export schema before a rights-gated importer is implemented.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from typing import Any

BUCKET_URL = "https://nara-national-archives-catalog.s3.amazonaws.com/"
RECORD_GROUPS = ("111", "342", "428")
MAX_METADATA_FILE_BYTES = 128 * 1024 * 1024
MAX_TOTAL_METADATA_BYTES = 384 * 1024 * 1024
MAX_LIST_KEYS_PER_GROUP = 20
USER_AGENT = "NolaneVideoAssetLibrary-NARA-BulkDataset-Probe/1.0"


def fetch_bytes(url: str, limit: int, timeout: int = 60) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/xml,application/json,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > limit:
            raise RuntimeError(f"response exceeds configured byte ceiling: {content_length}")
        body = response.read(limit + 1)
        if len(body) > limit:
            raise RuntimeError("response body exceeded configured byte ceiling")
        return body


def _local_name(tag: str) -> str:
    return str(tag).rsplit("}", 1)[-1]


def list_json_objects(record_group: str) -> list[dict[str, Any]]:
    prefix = f"descriptions/record-groups/rg_{record_group}/"
    rows = []
    continuation_token = ""
    first_key_samples = []
    pages_scanned = 0

    for _ in range(10):
        params = {
            "list-type": "2",
            "prefix": prefix,
            "max-keys": str(MAX_LIST_KEYS_PER_GROUP),
        }
        if continuation_token:
            params["continuation-token"] = continuation_token
        query = urllib.parse.urlencode(params)
        xml_body = fetch_bytes(BUCKET_URL + "?" + query, 2 * 1024 * 1024, timeout=30)
        root = ET.fromstring(xml_body)
        pages_scanned += 1
        contents = [element for element in root.iter() if _local_name(element.tag) == "Contents"]

        for item in contents:
            fields = {_local_name(child.tag): (child.text or "") for child in item}
            key = fields.get("Key", "")
            size_text = fields.get("Size", "0")
            modified = fields.get("LastModified", "")
            if key and len(first_key_samples) < 8:
                first_key_samples.append(key)
            if key.endswith(".json"):
                rows.append({"key": key, "size_bytes": int(size_text), "last_modified": modified})

        truncated = False
        next_token = ""
        for element in root.iter():
            name = _local_name(element.tag)
            if name == "IsTruncated":
                truncated = (element.text or "").strip().casefold() == "true"
            elif name == "NextContinuationToken":
                next_token = (element.text or "").strip()
        if not truncated or not next_token:
            break
        continuation_token = next_token

    if not rows:
        raise RuntimeError(
            "S3 listing contained no JSON objects within the bounded scan: "
            + json.dumps({
                "requested_prefix": prefix,
                "pages_scanned": pages_scanned,
                "key_samples": first_key_samples,
            })
        )
    return sorted(rows, key=lambda row: row["key"])


def _restriction_status(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("status") or value.get("restrictionStatus") or "").strip()
    if isinstance(value, str):
        return value.strip()
    return ""


def _as_record(candidate: Any) -> dict[str, Any] | None:
    if not isinstance(candidate, dict):
        return None
    record = candidate.get("record")
    if isinstance(record, dict):
        return record
    source = candidate.get("_source")
    if isinstance(source, dict):
        return _as_record(source)
    if any(key in candidate for key in ("useRestriction", "accessRestriction", "digitalObjects", "levelOfDescription")):
        return candidate
    return None


def iter_records(document: Any):
    """Yield record dictionaries from the common NARA bulk/API envelope variants."""
    seen: set[int] = set()

    def walk(value: Any):
        if isinstance(value, dict):
            record = _as_record(value)
            if record is not None and id(record) not in seen:
                seen.add(id(record))
                yield record
            for child in value.values():
                if isinstance(child, (dict, list)):
                    yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)

    yield from walk(document)


def _digital_objects(record: dict[str, Any]) -> list[dict[str, Any]]:
    value = record.get("digitalObjects")
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def summarize_metadata_file(body: bytes, record_group: str, object_key: str) -> dict[str, Any]:
    document = json.loads(body.decode("utf-8-sig"))
    summary = {
        "record_group": record_group,
        "object_key": object_key,
        "metadata_bytes": len(body),
        "top_level_type": type(document).__name__,
        "top_level_keys": sorted(document.keys())[:40] if isinstance(document, dict) else [],
        "records_seen": 0,
        "item_records": 0,
        "use_unrestricted": 0,
        "access_unrestricted": 0,
        "both_unrestricted": 0,
        "audiovisual_records": 0,
        "records_with_digital_objects": 0,
        "item_records_with_both_rights_and_objects": 0,
        "digital_object_count": 0,
        "candidate_media_count": 0,
        "record_field_keys": Counter(),
        "digital_object_field_keys": Counter(),
        "general_media_types": Counter(),
        "sample_candidate_objects": [],
    }

    for record in iter_records(document):
        summary["records_seen"] += 1
        summary["record_field_keys"].update(record.keys())
        level = str(record.get("levelOfDescription") or "").strip().casefold()
        is_item = level == "item"
        if is_item:
            summary["item_records"] += 1

        use_status = _restriction_status(record.get("useRestriction"))
        access_status = _restriction_status(record.get("accessRestriction"))
        use_ok = use_status.casefold() == "unrestricted"
        access_ok = access_status.casefold() == "unrestricted"
        if use_ok:
            summary["use_unrestricted"] += 1
        if access_ok:
            summary["access_unrestricted"] += 1
        if use_ok and access_ok:
            summary["both_unrestricted"] += 1

        general_types = record.get("generalRecordsTypes") or []
        if isinstance(general_types, str):
            general_types = [general_types]
        normalized_types = [str(value).strip() for value in general_types if str(value).strip()]
        for value in normalized_types:
            summary["general_media_types"][value] += 1
        audiovisual = str(record.get("audiovisual") or "").strip().casefold() in {"true", "1", "yes"}
        is_av = audiovisual or any(
            "moving image" in value.casefold()
            or "motion picture" in value.casefold()
            or "sound recording" in value.casefold()
            or "video" in value.casefold()
            for value in normalized_types
        )
        if is_av:
            summary["audiovisual_records"] += 1

        objects = _digital_objects(record)
        if objects:
            summary["records_with_digital_objects"] += 1
        summary["digital_object_count"] += len(objects)
        if is_item and use_ok and access_ok and objects:
            summary["item_records_with_both_rights_and_objects"] += 1

        for obj in objects:
            summary["digital_object_field_keys"].update(obj.keys())
            url = str(obj.get("objectUrl") or obj.get("url") or "")
            file_name = str(obj.get("objectFilename") or obj.get("filename") or "")
            media_type = str(obj.get("objectType") or obj.get("mediaType") or "")
            if url.startswith("https://") and (file_name or media_type or is_av):
                summary["candidate_media_count"] += 1
                if len(summary["sample_candidate_objects"]) < 3:
                    parsed = urllib.parse.urlsplit(url)
                    summary["sample_candidate_objects"].append({
                        "record_title": str(record.get("title") or "")[:180],
                        "levelOfDescription": record.get("levelOfDescription"),
                        "useRestriction": record.get("useRestriction"),
                        "accessRestriction": record.get("accessRestriction"),
                        "generalRecordsTypes": normalized_types,
                        "audiovisual": record.get("audiovisual"),
                        "object_filename": file_name,
                        "object_file_size": obj.get("objectFileSize"),
                        "object_url_host": parsed.hostname,
                        "object_url_path_prefix": "/".join(parsed.path.split("/")[:4]),
                        "object_type": media_type,
                    })

    summary["record_field_keys"] = sorted(summary["record_field_keys"])
    summary["digital_object_field_keys"] = sorted(summary["digital_object_field_keys"])
    summary["general_media_types"] = dict(summary["general_media_types"].most_common(30))
    return summary


def probe_record_group(record_group: str, remaining_budget: int) -> tuple[dict[str, Any], int]:
    objects = list_json_objects(record_group)
    eligible = [
        row for row in objects
        if 0 < row["size_bytes"] <= MAX_METADATA_FILE_BYTES
    ]
    if not eligible:
        return {
            "record_group": record_group,
            "listed_json_files": len(objects),
            "skipped_large_or_empty": len(objects),
            "status": "no-small-json-sample",
        }, 0

    selected = eligible[0]
    if selected["size_bytes"] > remaining_budget:
        return {
            "record_group": record_group,
            "listed_json_files": len(objects),
            "selected": selected,
            "status": "total-metadata-budget-exhausted",
        }, 0

    url = BUCKET_URL + urllib.parse.quote(selected["key"], safe="/")
    body = fetch_bytes(url, min(MAX_METADATA_FILE_BYTES, remaining_budget), timeout=90)
    summary = summarize_metadata_file(body, record_group, selected["key"])
    summary["listed_json_files"] = len(objects)
    summary["selected_object_size_bytes"] = selected["size_bytes"]
    summary["status"] = "sample-parsed"
    return summary, len(body)


def main() -> None:
    started = time.monotonic()
    total_bytes = 0
    results = []
    for group in RECORD_GROUPS:
        remaining = MAX_TOTAL_METADATA_BYTES - total_bytes
        if remaining <= 0:
            break
        try:
            result, downloaded = probe_record_group(group, remaining)
            total_bytes += downloaded
            results.append(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError, ET.ParseError, RuntimeError) as exc:
            result = {"record_group": group, "status": "probe-failed", "reason": str(exc)[:500]}
            results.append(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    final = {
        "probe": "NARA AWS bulk catalog metadata only",
        "total_metadata_bytes_downloaded": total_bytes,
        "max_metadata_bytes": MAX_TOTAL_METADATA_BYTES,
        "media_downloaded": False,
        "nara_catalog_api_used": False,
        "record_groups": results,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    print("NARA_PROBE_SUMMARY=" + json.dumps(final, ensure_ascii=False))
    if not any(row.get("status") == "sample-parsed" for row in results):
        raise SystemExit("No NARA bulk metadata sample could be parsed; source remains disabled.")


if __name__ == "__main__":
    main()
