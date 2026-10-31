"""ElevenLabs adapter with paginated, live voice discovery.

An account's full library is not assumed to be Vietnamese-capable. The
catalogue retains verified-language metadata and can be filtered client-side.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_ROOT = "https://api.elevenlabs.io"


class ElevenLabsError(RuntimeError):
    pass


def _request(method: str, path: str, *, payload: dict[str, Any] | None = None,
             query: dict[str, Any] | None = None) -> tuple[bytes, str]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ElevenLabsError("Set ELEVENLABS_API_KEY in the environment or secret store")
    url = API_ROOT + path
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
    headers = {"xi-api-key": api_key, "Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return response.read(), response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read(2048).decode("utf-8", errors="replace")
        raise ElevenLabsError(f"ElevenLabs returned HTTP {exc.code}: {detail}") from None
    except urllib.error.URLError as exc:
        raise ElevenLabsError(f"Cannot reach ElevenLabs: {getattr(exc, 'reason', exc)}") from None


def _language_aliases(language: str) -> set[str]:
    value = language.strip().lower().replace("_", "-")
    aliases = {
        "vi": {"vi", "vietnamese"},
        "vi-vn": {"vi", "vietnamese"},
        "en": {"en", "english"},
        "en-us": {"en", "english"},
        "ja": {"ja", "japanese"},
        "zh": {"zh", "chinese"},
    }
    return aliases.get(value, {value.split("-")[0], value})


def list_voices(language: str | None = None, page_size: int = 100,
                max_pages: int = 20) -> list[dict[str, Any]]:
    if not 1 <= page_size <= 100 or max_pages < 1:
        raise ValueError("page_size must be 1–100 and max_pages must be positive")
    page_token = None
    results: list[dict[str, Any]] = []
    for _ in range(max_pages):
        body, _ = _request(
            "GET", "/v2/voices",
            query={"page_size": page_size, "next_page_token": page_token},
        )
        try:
            page = json.loads(body.decode("utf-8"))
        except ValueError as exc:
            raise ElevenLabsError("ElevenLabs returned invalid voice catalogue JSON") from exc
        for voice in page.get("voices", []):
            verified = voice.get("verified_languages") or []
            languages = [
                item.get("language")
                for item in verified
                if isinstance(item, dict) and item.get("language")
            ]
            item = {
                "id": voice.get("voice_id"),
                "name": voice.get("name"),
                "provider": "elevenlabs",
                "type": voice.get("category", "library"),
                "labels": voice.get("labels") or {},
                "verified_languages": languages,
                "preview_url": voice.get("preview_url"),
            }
            if language:
                aliases = _language_aliases(language)
                if not any(str(x).lower() in aliases for x in languages):
                    continue
            results.append(item)
        page_token = page.get("next_page_token")
        if not page_token:
            break
    return results


def synthesize(
    text: str,
    voice: str,
    output_path: str | Path,
    *,
    language: str = "vi",
    speed: float = 1.0,
    settings: dict[str, Any] | None = None,
) -> Path:
    if not voice:
        raise ValueError("An ElevenLabs voice_id is required")
    if not 0.7 <= speed <= 1.2:
        raise ValueError("ElevenLabs speed must be between 0.7 and 1.2")
    options = settings or {}
    model_id = str(options.get("model_id", "eleven_flash_v2_5"))
    body = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": float(options.get("stability", 0.5)),
            "similarity_boost": float(options.get("similarity_boost", 0.75)),
            "style": float(options.get("style", 0.0)),
            "use_speaker_boost": bool(options.get("use_speaker_boost", True)),
            "speed": speed,
        },
    }
    if language:
        body["language_code"] = language
    audio, _ = _request(
        "POST",
        f"/v1/text-to-speech/{urllib.parse.quote(voice, safe='')}",
        payload=body,
        query={"output_format": options.get("output_format", "mp3_44100_128")},
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(audio)
    return destination
