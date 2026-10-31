"""Inspect the dynamically available VoiceStudio and optional provider voices."""
from __future__ import annotations

import argparse
import json
from typing import Any

from client import VoiceStudioClient
from providers import google_cloud, korva, elevenlabs


def get_catalog(provider: str, language: str) -> Any:
    if provider == "voicestudio":
        client = VoiceStudioClient()
        return {
            "engines": client.list_engines(),
            "profiles": client.list_profiles(),
            "voices": client.list_voices(),
            "archetypes": client.list_archetypes(language=language or None, limit=500),
        }
    if provider == "korva":
        return korva.list_voices(language)
    if provider == "google":
        return google_cloud.list_voices(language or "vi-VN")
    if provider == "elevenlabs":
        return elevenlabs.list_voices(language or None)
    raise ValueError(f"Unknown provider: {provider}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("voicestudio", "korva", "google", "elevenlabs"),
                        default="voicestudio")
    parser.add_argument("--language", default="vi")
    args = parser.parse_args()
    try:
        result = get_catalog(args.provider, args.language)
    except Exception as exc:
        parser.exit(2, f"Could not load voice catalogue: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
