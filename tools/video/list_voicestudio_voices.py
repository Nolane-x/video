#!/usr/bin/env python3
"""List canonical English/Vietnamese VoiceStudio voices for video narration.

Reads the published manifest; it never guesses voice IDs and keeps each
source's commercial-use notice visible. The commercial filter only selects
entries whose upstream source explicitly states generated-audio commercial
permission. It is not legal advice or a guarantee of all downstream rights.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MANIFEST_URL = (
    "https://github.com/Nolane-x/VoiceStudio/releases/download/"
    "voice-library-latest/manifest.json"
)
COMMERCIAL_ALLOWED_MARKERS = frozenset({
    "upstream-model-card-permits-generated-audio",
    "apache-2.0-model-and-voice-assets",
})


def read_manifest(path: str | None, timeout: float = 30.0) -> dict[str, Any]:
    if path:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        request = Request(
            MANIFEST_URL,
            headers={
                "Accept": "application/json",
                "User-Agent": "Nolane-Video-VoiceCatalog/1.0",
            },
        )
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("voices"), list):
        raise ValueError("Manifest must be a JSON object with a voices array")
    return payload


def engine_matches(voice: dict[str, Any], requested: str) -> bool:
    if requested == "all":
        return True
    actual = str(voice.get("engine", "")).casefold()
    return requested in actual


def select_voices(
    manifest: dict[str, Any],
    *,
    language: str = "all",
    engine: str = "all",
    commercial_permitted_only: bool = False,
    limit: int = 0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for voice in manifest["voices"]:
        if not isinstance(voice, dict):
            continue
        if language != "all" and voice.get("language") != language:
            continue
        if not engine_matches(voice, engine):
            continue
        rights = voice.get("rights") or {}
        if commercial_permitted_only and rights.get("commercial_use") not in COMMERCIAL_ALLOWED_MARKERS:
            continue
        rows.append({
            "voice_id": voice.get("id", ""),
            "display_name": voice.get("display_name", ""),
            "language": voice.get("language", ""),
            "engine": voice.get("engine", ""),
            "sample_rate": voice.get("sample_rate"),
            "duration_seconds": voice.get("duration_seconds"),
            "sample_text": voice.get("sample_text", ""),
            "rights_status": rights.get("rights_status", "unknown"),
            "commercial_use": rights.get("commercial_use", "not-stated"),
            "upstream_quality_grade": voice.get("upstream_quality_grade"),
            "quality_grade_source": voice.get("quality_grade_source"),
            "attribution_required": rights.get("attribution_required"),
            "notice": rights.get("notice", ""),
        })
    rows.sort(key=lambda row: (row["language"], row["engine"], row["voice_id"]))
    return rows[:limit] if limit > 0 else rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", help="local manifest.json; defaults to the latest VoiceStudio release")
    parser.add_argument("--language", choices=["all", "en", "vi"], default="all")
    parser.add_argument("--engine", choices=["all", "piper", "vieneu", "kokoro"], default="all")
    parser.add_argument(
        "--commercial-permitted-only",
        action="store_true",
        help="only include sources whose manifest notice explicitly permits commercial use of generated audio",
    )
    parser.add_argument("--limit", type=int, default=0, help="maximum rows; 0 means no limit")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit < 0:
        raise ValueError("--limit must be zero or positive")
    manifest = read_manifest(args.manifest)
    voices = select_voices(
        manifest,
        language=args.language,
        engine=args.engine,
        commercial_permitted_only=args.commercial_permitted_only,
        limit=args.limit,
    )
    counts = manifest.get("counts") or {}
    if args.json:
        print(json.dumps({
            "manifest_built_at": manifest.get("built_at"),
            "manifest_counts": counts,
            "selection_count": len(voices),
            "selection": voices,
            "rights_note": (
                "The commercial filter reflects the exact upstream rights statement "
                "recorded in the manifest; review attribution and source terms before publication."
            ),
        }, ensure_ascii=False, indent=2))
    else:
        print(
            f"VoiceStudio manifest: {manifest.get('built_at', 'unknown build')} | "
            f"catalog EN={counts.get('en', '?')} VI={counts.get('vi', '?')}"
        )
        print(f"Selected: {len(voices)} voice(s)")
        print("VOICE ID | LANGUAGE | DISPLAY NAME | ENGINE | RIGHTS | COMMERCIAL USE")
        for voice in voices:
            print(
                f"{voice['voice_id']} | {voice['language']} | {voice['display_name']} | "
                f"{voice['engine']} | {voice['rights_status']} | {voice['commercial_use']}"
            )
        print(
            "Note: source permission labels are evidence recorded in the manifest, "
            "not a substitute for reviewing the source terms and attribution."
        )
    if not voices:
        print("No voices matched the requested filters.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Voice catalog lookup failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
