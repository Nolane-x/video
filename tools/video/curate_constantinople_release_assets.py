#!/usr/bin/env python3
"""Metadata-only scout for the existing Build 76 asset library."""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path
from typing import Any

TERMS = {
    "constantinople": 40, "byzantine": 32, "byzantium": 24, "ottoman": 32,
    "mehmed": 35, "orban": 35, "janissary": 30, "janissaries": 30,
    "theodosian": 24, "golden horn": 20, "bosphorus": 18, "bombard": 32,
    "siege": 24, "medieval": 8, "fortress": 9, "city wall": 9, "castle": 6,
    "armor": 7, "armour": 7, "helmet": 7, "chainmail": 8, "mail armor": 8,
    "sword": 5, "spear": 5, "shield": 5, "cannon": 10, "artillery": 10,
    "stone shot": 10, "horse": 5, "wagon": 5, "cart": 4, "galley": 10,
    "ship": 4, "naval": 4, "harbour": 4, "harbor": 4, "manuscript": 8,
    "miniature": 8, "illumination": 8, "engraving": 7, "painting": 4,
    "map": 3, "archaeology": 5, "historical": 3, "islamic": 4,
    "eastern roman": 15, "battering ram": 12, "siege engine": 12,
    "turkish": 5, "anatolia": 3, "masonry": 4,
}
TEXT_FIELDS = (
    "title", "name", "filename", "file_name", "path", "file_path", "category",
    "type", "description", "tags", "keywords", "provider", "source", "source_id",
    "collection", "subject", "creator", "department", "date", "year",
)
ASSET_FIELDS = ("path", "file_path", "filename", "file_name", "relative_path", "url", "download_url")
LICENSE_FIELDS = ("license", "licence", "rights", "rights_statement", "usage", "access")
VOLUME_FIELDS = ("volume", "volume_name", "archive", "archive_name", "zip", "bundle", "release_asset")

def walk(value: Any, trail: str = "$"):
    if isinstance(value, dict):
        yield value, trail
        for k, v in value.items():
            yield from walk(v, f"{trail}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, f"{trail}[{i}]")

def txt(v: Any) -> str:
    if v is None: return ""
    if isinstance(v, (list, tuple, set)): return " ".join(txt(x) for x in v)
    if isinstance(v, dict): return " ".join(f"{k} {txt(x)}" for k, x in v.items())
    return str(v)

def values(row: dict, fields: tuple[str, ...]) -> list[str]:
    return [txt(row[k]) for k in fields if row.get(k) not in (None, "", [], {})]

def rights(row: dict) -> tuple[str, str]:
    raw = " | ".join(values(row, LICENSE_FIELDS))
    low = raw.casefold()
    if row.get("isPublicDomain") is True or row.get("public_domain") is True:
        return "public-domain", raw or "public-domain flag"
    if "cc0" in low or "creative commons zero" in low:
        return "cc0", raw
    if "public domain" in low or "publicdomainmark" in low or "pdm 1.0" in low:
        return "public-domain", raw
    if "use-in-video" in low or "finished film" in low:
        return "use-in-video-review", raw
    if "cc-by" in low or "cc by" in low or "attribution" in low:
        return "attribution-review", raw
    return "review-required", raw or "no explicit rights field"

def candidate(row: dict, trail: str):
    if not any(k in row for k in ASSET_FIELDS):
        return None
    if not any(k in row for k in ("sha256", "checksum", "id", "asset_id", "object_id", "source_url")):
        return None
    corpus = " ".join(txt(row.get(k)) for k in TEXT_FIELDS).casefold()
    score, hits = 0, []
    for term, weight in TERMS.items():
        if term in corpus:
            score += weight
            hits.append(term)
    if score < 5:
        return None
    provider = " | ".join(values(row, ("provider", "source", "source_id")))
    if any(x in provider.casefold() for x in ("metropolitan museum", "the met", "rijksmuseum", "smithsonian", "library of congress", "wikimedia")):
        score += 10
    if any(x in corpus for x in ("15th century", "fifteenth century", "1453", "15th c.")):
        score += 12
    sha = str(row.get("sha256") or row.get("checksum") or "").lower()
    if not re.fullmatch(r"[a-f0-9]{64}", sha):
        sha = ""
    url = next((str(row[k]) for k in ("source_url", "source_page", "item_url", "url", "download_url") if isinstance(row.get(k), str) and row[k].startswith("http")), "")
    title = next((str(row[k]) for k in ("title", "name", "filename", "file_name", "id") if isinstance(row.get(k), (str, int))), "")
    return {
        "score": score, "matched_terms": hits, "title": title,
        "id": next((str(row[k]) for k in ("id", "asset_id", "object_id") if row.get(k) not in (None, "")), ""),
        "path": next((str(row[k]) for k in ASSET_FIELDS if isinstance(row.get(k), str) and row[k]), ""),
        "sha256": sha, "size_bytes": row.get("size_bytes") or row.get("bytes") or row.get("size"),
        "provider": provider, "category": " | ".join(values(row, ("category", "type", "media_type"))),
        "license_class": rights(row)[0], "license_text": rights(row)[1],
        "source_url": url, "volume_hint": " | ".join(values(row, VOLUME_FIELDS)),
        "redistributable": row.get("redistributable"), "index_location": trail,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--max-candidates", type=int, default=400)
    a = ap.parse_args()
    raw = a.index.read_bytes()
    data = json.loads(raw)
    found, seen = [], set()
    for row, trail in walk(data):
        item = candidate(row, trail)
        if item is None: continue
        key = item["sha256"] or item["path"] or item["id"] or f"{trail}:{item['title']}"
        if key in seen: continue
        seen.add(key)
        found.append(item)
    found.sort(key=lambda x: (x["score"], x["license_class"] in {"cc0", "public-domain"}, bool(x["sha256"]), x["size_bytes"] or 0), reverse=True)
    buckets = Counter(x["license_class"] for x in found)
    providers = Counter(x["provider"] or "(not recorded)" for x in found)
    shortlist = found[:a.max_candidates]
    digest = hashlib.sha256(raw).hexdigest()
    report = {
        "status": "PASS", "release": "video-asset-library-build-41184526545",
        "index_bytes": len(raw), "index_sha256": digest,
        "candidate_count": len(found), "shortlist_count": len(shortlist),
        "rights_class_counts": dict(buckets), "top_providers": providers.most_common(30),
        "policy": "Metadata scout only. Exact item-level rights, source, checksum and visual relevance must be reviewed before use.",
        "shortlist": shortlist,
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    lines = [
        "# Constantinople 1453 - Build 76 asset scout", "",
        f"- Index bytes: {len(raw):,}", f"- Index SHA-256: {digest}",
        f"- Candidate records: {len(found):,}", f"- Rights buckets: {json.dumps(dict(buckets), ensure_ascii=False)}", "",
        "Metadata shortlist only. Rights and visual approval are not implied.", "",
        "| Score | Title | Provider | Category | Rights | Size | SHA-256 | Source |",
        "|---:|---|---|---|---|---:|---|---|",
    ]
    safe = lambda v: str(v or "").replace("|", "/").replace("\n", " ")
    for x in shortlist:
        lines.append(f"| {x['score']} | {safe(x['title'])} | {safe(x['provider'])} | {safe(x['category'])} | {safe(x['license_class'])} | {safe(x['size_bytes'])} | {safe(x['sha256'])[:18]} | {safe(x['source_url'])} |")
    a.output.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"status":"PASS","index_bytes":len(raw),"index_sha256":digest,"candidate_count":len(found),"rights_classes":dict(buckets)}, indent=2))

if __name__ == "__main__":
    main()
