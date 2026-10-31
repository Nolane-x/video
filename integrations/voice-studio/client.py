"""Small, dependency-free client for the pinned VoiceStudio local API.

VoiceStudio stays a separate application/service. This adapter deliberately
does not import VoiceStudio internals or install its heavy ML dependencies.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class VoiceStudioError(RuntimeError):
    """Safe API failure; secret headers are never included in the message."""


class VoiceStudioClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 180.0,
    ) -> None:
        self.base_url = (base_url or os.getenv(
            "VOICESTUDIO_BASE_URL", "http://127.0.0.1:3900"
        )).rstrip("/")
        self.api_key = api_key if api_key is not None else os.getenv("VOICESTUDIO_API_KEY")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> tuple[bytes, str]:
        if not path.startswith("/"):
            raise ValueError("API path must start with '/'")
        url = self.base_url + path
        if query:
            clean = {k: v for k, v in query.items() if v is not None}
            if clean:
                url += "?" + urllib.parse.urlencode(clean)
        parsed_base = urllib.parse.urlsplit(self.base_url)
        host = (parsed_base.hostname or "").lower()
        loopback_hosts = {"localhost", "127.0.0.1", "::1"}
        if self.api_key and parsed_base.scheme != "https" and host not in loopback_hosts:
            raise VoiceStudioError(
                "Refusing to send VOICESTUDIO_API_KEY over non-HTTPS to a non-loopback host"
            )
        headers = {"Accept": "application/json, audio/wav, audio/*"}
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read()
                content_type = response.headers.get("Content-Type", "")
                return body, content_type
        except urllib.error.HTTPError as exc:
            body = exc.read(4096)
            detail = body.decode("utf-8", errors="replace")
            try:
                obj = json.loads(detail)
                detail = (
                    obj.get("detail")
                    or obj.get("error", {}).get("message")
                    or obj.get("message")
                    or detail
                )
            except (ValueError, AttributeError):
                pass
            raise VoiceStudioError(
                f"VoiceStudio returned HTTP {exc.code} for {method} {path}: {detail}"
            ) from None
        except urllib.error.URLError as exc:
            reason = getattr(exc, "reason", "connection failed")
            raise VoiceStudioError(
                f"Cannot reach VoiceStudio at {self.base_url}: {reason}"
            ) from None
        except TimeoutError:
            raise VoiceStudioError(
                f"VoiceStudio request timed out after {self.timeout:g}s: {method} {path}"
            ) from None

    def _json(self, method: str, path: str, **kwargs: Any) -> Any:
        body, _ = self._request(method, path, **kwargs)
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise VoiceStudioError(f"VoiceStudio returned invalid JSON for {path}") from exc

    def health(self) -> Any:
        return self._json("GET", "/health")

    def list_engines(self) -> Any:
        return self._json("GET", "/engines/tts")

    def list_models(self) -> Any:
        return self._json("GET", "/v1/models")

    def list_voices(self) -> Any:
        """List saved profiles and provider aliases exposed by VoiceStudio."""
        return self._json("GET", "/v1/audio/voices")

    def list_profiles(self) -> Any:
        return self._json("GET", "/profiles")

    def list_archetypes(
        self,
        language: str | None = None,
        search: str | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Return the built-in voice-design catalogue (several hundred entries)."""
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        offset = 0
        results: list[dict[str, Any]] = []
        while True:
            remaining = limit - len(results)
            page = self._json(
                "GET",
                "/archetypes",
                query={"lang": language, "q": search, "limit": min(500, remaining), "offset": offset},
            )
            items = page.get("items", []) if isinstance(page, dict) else []
            if not isinstance(items, list):
                raise VoiceStudioError("Unexpected archetype response shape")
            results.extend(items)
            if len(results) >= limit or len(items) < min(500, remaining):
                break
            offset += len(items)
        return results[:limit]

    def use_archetype(self, archetype_id: str, name: str | None = None) -> Any:
        safe_id = urllib.parse.quote(archetype_id, safe="")
        return self._json(
            "POST",
            f"/archetypes/{safe_id}/use",
            query={"name": name},
        )

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
        *,
        engine: str = "omnivoice",
        voice: str = "default",
        language: str | None = None,
        speed: float | None = None,
        instruct: str | None = None,
        description: str | None = None,
        seed: int | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Path:
        if not text.strip():
            raise ValueError("Cannot synthesize empty text")
        if len(text) > 4096:
            raise ValueError(
                "VoiceStudio's OpenAI-compatible endpoint accepts at most 4096 characters per request; split the segment."
            )
        selected_speed = speed if speed is not None else 1.0
        if not 0.25 <= selected_speed <= 4.0:
            raise ValueError("speed must be between 0.25 and 4.0")
        payload: dict[str, Any] = {
            "model": engine,
            "input": text,
            "voice": voice,
            "response_format": "wav",
        }
        if language:
            payload["language"] = language
        if speed is not None:
            payload["speed"] = speed
        if instruct:
            payload["instruct"] = instruct
        if description:
            payload["description"] = description
        if seed is not None:
            payload["seed"] = seed
        if extra:
            allowed = {
                "duration", "num_step", "guidance_scale", "denoise",
                "preprocess_prompt", "chunk_duration", "chunk_threshold",
            }
            unknown = set(extra) - allowed
            if unknown:
                raise ValueError(f"Unsupported VoiceStudio options: {sorted(unknown)}")
            payload.update(extra)
        audio, content_type = self._request("POST", "/v1/audio/speech", payload=payload)
        if not audio:
            raise VoiceStudioError("VoiceStudio returned an empty audio response")
        if "json" in content_type.lower():
            raise VoiceStudioError(
                "VoiceStudio returned JSON instead of audio; check engine/model availability"
            )
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(audio)
        return destination
