"""KorvaTTS adapter: Vietnamese ONNX/CPU voice presets.

Korva currently provides ten shipped preset voices. Voice cloning/training is
not advertised here because it is a separate upstream roadmap capability.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

VOICES = [
    {"id": "bao_kim", "name": "Bảo Kim", "gender": "female", "language": "vi"},
    {"id": "khanh_vy", "name": "Khánh Vy", "gender": "female", "language": "vi"},
    {"id": "ngoc_huyen", "name": "Ngọc Huyền", "gender": "female", "language": "vi"},
    {"id": "phuong_linh", "name": "Phương Linh", "gender": "female", "language": "vi"},
    {"id": "quynh_nhu", "name": "Quỳnh Như", "gender": "female", "language": "vi"},
    {"id": "gia_bao", "name": "Gia Bảo", "gender": "male", "language": "vi"},
    {"id": "hoang_nam", "name": "Hoàng Nam", "gender": "male", "language": "vi"},
    {"id": "huu_dat", "name": "Hữu Đạt", "gender": "male", "language": "vi"},
    {"id": "quang_huy", "name": "Quang Huy", "gender": "male", "language": "vi"},
    {"id": "thanh_phong", "name": "Thanh Phong", "gender": "male", "language": "vi"},
]


def list_voices(language: str = "vi") -> list[dict[str, Any]]:
    if language.lower().split("-")[0] != "vi":
        return []
    return [dict(v, provider="korva", type="preset") for v in VOICES]


@lru_cache(maxsize=2)
def _engine(num_threads: int = 4):
    try:
        from korvatts import TTS
    except ImportError as exc:
        raise RuntimeError(
            "KorvaTTS is optional. Install it with: python -m pip install korvatts"
        ) from exc
    return TTS(device="cpu", num_threads=num_threads)


def synthesize(
    text: str,
    voice: str,
    output_path: str | Path,
    *,
    language: str = "vi",
    speed: float = 1.0,
    settings: dict[str, Any] | None = None,
    seed: int | None = None,
) -> Path:
    if language.lower().split("-")[0] != "vi":
        raise ValueError("KorvaTTS is configured here for Vietnamese (vi) only")
    if voice not in {item["id"] for item in VOICES}:
        raise ValueError(f"Unknown KorvaTTS voice: {voice}")
    if not 0.5 <= speed <= 2.0:
        raise ValueError("speed must be between 0.5 and 2.0")
    options = settings or {}
    num_threads = options.get("num_threads", 4)
    total_steps = options.get("total_steps", 32)
    if isinstance(num_threads, bool) or not isinstance(num_threads, int) or not 1 <= num_threads <= 64:
        raise ValueError("KorvaTTS num_threads must be an integer between 1 and 64")
    if isinstance(total_steps, bool) or not isinstance(total_steps, int) or not 1 <= total_steps <= 32:
        raise ValueError("KorvaTTS total_steps must be an integer between 1 and 32")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ValueError("KorvaTTS seed must be an integer")
    silence = float(options.get("silence_between_chunks", 0.3))
    if silence < 0:
        raise ValueError("KorvaTTS silence_between_chunks must be non-negative")
    engine = _engine(num_threads)
    audio, _duration = engine.synthesize(
        text,
        voice=voice,
        lang="vi",
        total_steps=total_steps,
        speed=speed,
        silence_between_chunks=silence,
        seed=seed,
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    engine.save_audio(audio, str(destination))
    return destination
