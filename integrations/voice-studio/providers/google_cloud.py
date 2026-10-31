"""Google Cloud Text-to-Speech adapter with dynamic voice discovery."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any


@lru_cache(maxsize=1)
def _client():
    try:
        from google.cloud import texttospeech
    except ImportError as exc:
        raise RuntimeError(
            "Google Cloud TTS is optional. Install: python -m pip install google-cloud-texttospeech"
        ) from exc
    return texttospeech, texttospeech.TextToSpeechClient()


def _normalize_language(language: str) -> str:
    language = language.strip()
    if language.lower() == "vi":
        return "vi-VN"
    if language.lower() == "en":
        return "en-US"
    return language


def list_voices(language: str = "vi-VN") -> list[dict[str, Any]]:
    texttospeech, client = _client()
    language = _normalize_language(language)
    response = client.list_voices(language_code=language)
    return [
        {
            "id": voice.name,
            "name": voice.name,
            "provider": "google",
            "language_codes": list(voice.language_codes),
            "gender": getattr(voice.ssml_gender, "name", str(voice.ssml_gender)).lower(),
            "type": "cloud",
        }
        for voice in response.voices
    ]


def synthesize(
    text: str,
    voice: str,
    output_path: str | Path,
    *,
    language: str = "vi-VN",
    speed: float = 1.0,
    settings: dict[str, Any] | None = None,
) -> Path:
    texttospeech, client = _client()
    options = settings or {}
    audio_encoding = getattr(
        texttospeech.AudioEncoding,
        str(options.get("audio_encoding", "LINEAR16")).upper(),
        texttospeech.AudioEncoding.LINEAR16,
    )
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=_normalize_language(language),
        name=voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=speed,
        pitch=float(options.get("pitch", 0.0)),
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.audio_content)
    return destination
