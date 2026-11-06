#!/usr/bin/env python3
"""Search the generated metadata index without assuming a sound has been auditioned."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Any


def search_assets(catalog: dict[str, Any], query: str, limit: int = 30,
                  include_review_required: bool = False) -> list[dict[str, Any]]:
    terms = [x.casefold() for x in re.findall(r"[a-z0-9]+", query)]
    results = []
    for asset in catalog.get("assets", []):
        status = asset.get("rights_status", "review_required")
        if not include_review_required and status in {
            "review_required", "source_only_or_not_redistributable",
            "not_approved_for_default_commercial_use"
        }:
            continue
        haystack = " ".join(str(asset.get(key) or "") for key in (
            "title", "archive_name", "archive_member", "format", "license",
            "source_url", "attribution_text"
        )).casefold()
        score = sum(2 if term in str(asset.get("title", "")).casefold() else 1
                    for term in terms if term in haystack)
        if not terms:
            score = 1
        if score <= 0:
            continue
        results.append((score, asset))
    results.sort(key=lambda pair: (-pair[0], pair[1].get("title", "").casefold()))
    selected = []
    for score, asset in results[:max(1, limit)]:
        item = dict(asset)
        item["search_score"] = score
        item["final_use_gate"] = (
            "requires_human_audition_and_project_license_review"
            if not item.get("auditioned_by_human") or not item.get("approved_for_final_mix")
            else "project_review_required"
        )
        selected.append(item)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("audio-library/generated/audio-catalog.json"))
    parser.add_argument("--query", default="")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--include-review-required", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    results = search_assets(catalog, args.query, args.limit, args.include_review_required)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['title']} | {item['format']} | {item['rights_status']} | {item['archive_name']} :: {item['archive_member']}")
            print(f"  auditioned={item['auditioned_by_human']} final_use_gate={item['final_use_gate']}")
    print(f"Matches: {len(results)} (none are approved merely by search)", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
