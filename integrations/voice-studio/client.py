"""Small, dependency-free client for the pinned VoiceStudio local API.

VoiceStudio stays a separate application/service. This adapter deliberately
does not import VoiceStudio internals or install its heavy ML dependencies.
"""
from __future__ import annotations

import json
import mimetypes
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid
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
        raw_data: bytes | None = None,
        raw_content_type: str | None = None,
    ) -> tuple[bytes, str]:
        if not path.startswith("/"):
            raise ValueError("API path must start with '/'")
        if payload is not None and raw_data is not None:
            raise ValueError("Use JSON payload or raw multipart data, not both")
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
        data = raw_data
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif raw_data is not None:
            if not raw_content_type:
                raise ValueError("raw_content_type is required with raw_data")
            headers["Content-Type"] = raw_content_type
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

    @staticmethod
    def _save_audio(body: bytes, content_type: str, output_path: str | Path) -> Path:
        if not body:
            raise VoiceStudioError("VoiceStudio returned an empty audio response")
        if "json" in content_type.lower() or "text/" in content_type.lower():
            raise VoiceStudioError(
                "VoiceStudio returned a text/JSON response instead of audio"
            )
        destination = Path(output_path)
        if destination.suffix.lower() in {"", ".audio"}:
            media = content_type.lower()
            extension = (
                ".mp3" if "mpeg" in media or "mp3" in media
                else ".ogg" if "ogg" in media
                else ".flac" if "flac" in media
                else ".wav"
            )
            destination = destination.with_suffix(extension)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".part")
        try:
            temporary.write_bytes(body)
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        return destination

    def download_audio(
        self,
        path: str,
        output_path: str | Path,
        *,
        query: dict[str, Any] | None = None,
    ) -> Path:
        body, content_type = self._request("GET", path, query=query)
        return self._save_audio(body, content_type, output_path)

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
        featured: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Return VoiceStudio's built-in archetype catalogue (up to 500 rows)."""
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        offset = 0
        results: list[dict[str, Any]] = []
        while True:
            remaining = limit - len(results)
            page = self._json(
                "GET",
                "/archetypes",
                query={
                    "lang": language,
                    "q": search,
                    "featured": str(featured).lower() if featured is not None else None,
                    "limit": min(500, remaining),
                    "offset": offset,
                },
            )
            items = page.get("items", []) if isinstance(page, dict) else []
            if not isinstance(items, list):
                raise VoiceStudioError("Unexpected archetype response shape")
            results.extend(item for item in items if isinstance(item, dict))
            if len(items) < min(500, remaining):
                break
            if len(results) >= limit:
                break
            offset += len(items)
        return results[:limit]

    def archetype_preview_state(self, archetype_id: str) -> Any:
        safe_id = urllib.parse.quote(archetype_id, safe="")
        return self._json("GET", f"/archetypes/{safe_id}/preview/state")

    def preview_archetype(
        self, archetype_id: str, output_path: str | Path, *, local: bool = False
    ) -> Path:
        safe_id = urllib.parse.quote(archetype_id, safe="")
        return self.download_audio(
            f"/archetypes/{safe_id}/preview",
            output_path,
            query={"local": str(local).lower()},
        )

    def profile_audio(self, profile_id: str, output_path: str | Path) -> Path:
        safe_id = urllib.parse.quote(profile_id, safe="")
        return self.download_audio(f"/profiles/{safe_id}/audio", output_path)


    def create_design_profile(
        self,
        name: str,
        description: str,
        *,
        engine: str,
        language: str = "vi",
        seed: int | None = 42,
        sample_text: str = "",
    ) -> Any:
        """Save a free-form Voice Design recipe as a reusable VoiceStudio profile.

        This creates a synthetic design profile, not a clone of a real speaker.
        The backend validates the recipe and stores the design with its engine
        and seed; the first profile-audio request lazily renders its preview.
        """
        name = name.strip()
        description = description.strip()
        engine = engine.strip()
        if not name:
            raise ValueError("A designed voice needs a non-empty profile name")
        if not description or len(description) > 2000:
            raise ValueError("Voice description must contain 1–2000 characters")
        if not engine:
            raise ValueError("Pass the exact installed VoiceStudio engine ID")
        if seed is not None and not isinstance(seed, int):
            raise ValueError("Voice design seed must be an integer")
        picks = {
            "Gender": "Auto",
            "Age": "Auto",
            "Pitch": "Auto",
            "Style": "Auto",
            "EnglishAccent": "Auto",
            "ChineseDialect": "Auto",
        }
        fields = {
            "name": name,
            "ref_text": sample_text[:4096],
            "instruct": "",
            "language": language,
            "personality": "Nolane synthetic voice design",
            "kind": "design",
            "vd_states": json.dumps(picks, ensure_ascii=False),
            "design_recipe": json.dumps(
                {"description": description, "picks": picks},
                ensure_ascii=False,
            ),
            "engine": engine,
        }
        if seed is not None:
            fields["seed"] = str(seed)
        boundary = "----NolaneVoiceDesign" + uuid.uuid4().hex
        chunks: list[bytes] = []
        for field_name, value in fields.items():
            chunks.append(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'
                    f"{value}\r\n"
                ).encode("utf-8")
            )
        chunks.append(f"--{boundary}--\r\n".encode("ascii"))
        body, _content_type = self._request(
            "POST",
            "/profiles",
            raw_data=b"".join(chunks),
            raw_content_type=f"multipart/form-data; boundary={boundary}",
        )
        try:
            result = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise VoiceStudioError("VoiceStudio returned an invalid design-profile response") from exc
        if not isinstance(result, dict) or not result.get("id"):
            raise VoiceStudioError(
                "VoiceStudio did not return a saved profile ID for the designed voice"
            )
        return result

    def use_archetype(self, archetype_id: str, name: str | None = None) -> Any:
        safe_id = urllib.parse.quote(archetype_id, safe="")
        return self._json(
            "POST",
            f"/archetypes/{safe_id}/use",
            query={"name": name},
        )

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        language: str | None = None,
        model: str = "whisper-1",
    ) -> str:
        """Round-trip a generated clip through VoiceStudio's configured ASR."""
        source = Path(audio_path)
        if not source.is_file():
            raise FileNotFoundError(source)
        size = source.stat().st_size
        if size <= 0 or size > 64 * 1024 * 1024:
            raise ValueError("ASR input must be between 1 byte and 64 MiB")
        boundary = "----NolaneVoice" + uuid.uuid4().hex
        filename = source.name.replace('"', "_").replace("\r", "_").replace("\n", "_")
        mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks = [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\n{model}\r\n".encode(),
        ]
        if language:
            chunks.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\n{language}\r\n".encode()
            )
        chunks.extend([
            (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
                f"filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n"
            ).encode(),
            source.read_bytes(),
            f"\r\n--{boundary}--\r\n".encode(),
        ])
        body, content_type = self._request(
            "POST",
            "/v1/audio/transcriptions",
            raw_data=b"".join(chunks),
            raw_content_type=f"multipart/form-data; boundary={boundary}",
        )
        try:
            if "json" in content_type.lower():
                payload = json.loads(body.decode("utf-8"))
                transcript = payload.get("text")
            else:
                transcript = body.decode("utf-8")
        except (UnicodeDecodeError, ValueError, AttributeError) as exc:
            raise VoiceStudioError("VoiceStudio ASR returned an invalid transcript") from exc
        if not isinstance(transcript, str):
            raise VoiceStudioError("VoiceStudio ASR response did not contain transcript text")
        return transcript.strip()

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
        return self._save_audio(audio, content_type, output_path)
