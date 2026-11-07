#!/usr/bin/env python3
"""Validate human Foley audition decisions against the exact source catalog.

This tool never marks an asset as auditioned. It only validates a review JSON
export produced after a person listened to the exact file in AUDIO_PREVIEW.html.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_DECISIONS = {"unreviewed", "keep_candidate", "reject"}
PACK_ID = "nolane-illustrated-history-foley-review-v0.4.0"


def validate_review(catalog: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    if review.get("schema_version") != "1.0.0":
        raise ValueError("Unsupported review schema_version; expected 1.0.0")
    if review.get("pack") != PACK_ID:
        raise ValueError(f"Wrong review pack: expected {PACK_ID!r}")
    assets = {item["asset_id"]: item for item in catalog.get("assets", [])}
    seen: set[str] = set()
    approved: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    auditioned = 0
    reviewed_rows = review.get("decisions")
    if not isinstance(reviewed_rows, list):
        raise ValueError("Review JSON must contain a decisions array")

    for index, row in enumerate(reviewed_rows):
        if not isinstance(row, dict):
            raise ValueError(f"Decision row {index} must be an object")
        asset_id = row.get("asset_id")
        if not isinstance(asset_id, str) or not asset_id:
            raise ValueError(f"Decision row {index} has no asset_id")
        if asset_id in seen:
            raise ValueError(f"Duplicate review decision for {asset_id}")
        seen.add(asset_id)
        asset = assets.get(asset_id)
        if asset is None:
            raise ValueError(f"Unknown asset_id: {asset_id}")
        if row.get("sha256") != asset.get("sha256"):
            raise ValueError(f"SHA-256 mismatch for {asset_id}; re-export from the matching package")
        decision = row.get("decision", "unreviewed")
        if decision not in VALID_DECISIONS:
            raise ValueError(f"Invalid decision for {asset_id}: {decision}")
        heard = row.get("human_auditioned") is True
        is_approved = row.get("approved_for_final_mix") is True
        rating = row.get("rating")
        if rating not in ("", None):
            try:
                numeric_rating = int(rating)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Rating for {asset_id} must be 1-5") from exc
            if numeric_rating not in range(1, 6):
                raise ValueError(f"Rating for {asset_id} must be 1-5")
        if is_approved and not heard:
            raise ValueError(f"{asset_id} cannot be approved before human audition")
        if decision != "unreviewed" and not heard:
            raise ValueError(f"{asset_id} has a listening decision but is not marked human_auditioned")
        if is_approved:
            if decision != "keep_candidate":
                raise ValueError(f"{asset_id} can only be approved when decision=keep_candidate")
            if asset.get("rights_class") != "public_cc0_pd" or asset.get("license") != "CC0-1.0":
                raise ValueError(f"{asset_id} is not in the CC0 public-redistribution rights class")
            approved.append(asset)
        if heard:
            auditioned += 1
        if decision == "keep_candidate":
            kept.append(asset)
        elif decision == "reject":
            rejected.append(asset)

    return {
        "schema_version": "1.0.0",
        "pack": PACK_ID,
        "release_tag": catalog.get("release_tag"),
        "catalog_asset_count": len(assets),
        "decision_count": len(seen),
        "human_auditioned_count": auditioned,
        "kept_candidate_count": len(kept),
        "rejected_count": len(rejected),
        "approved_for_final_mix_count": len(approved),
        "approved_for_final_mix": [
            {
                "asset_id": item["asset_id"],
                "title": item["title"],
                "path": item["path"],
                "sha256": item["sha256"],
                "creator": item["creator"],
                "source_page": item["source_page"],
                "license": item["license"],
                "license_url": item["license_url"],
                "duration_seconds": item["duration_seconds"],
                "codec": item.get("codec"),
                "sample_rate_hz": item.get("sample_rate_hz"),
                "channels": item.get("channels"),
            }
            for item in approved
        ],
        "status": "VALIDATED_WITH_HUMAN_APPROVALS" if approved else "VALIDATED_NO_FINAL_MIX_APPROVALS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-approved", action="store_true")
    args = parser.parse_args()
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        review = json.loads(args.review.read_text(encoding="utf-8"))
        report = validate_review(catalog, review)
        if args.require_approved and report["approved_for_final_mix_count"] < 1:
            raise ValueError("No human-approved cue exists; final-mix cue-sheet generation is blocked")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"Review validation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
