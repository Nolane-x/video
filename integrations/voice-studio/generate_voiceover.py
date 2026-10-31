"""Generate per-line speech assets for the existing prep_voice.py timeline tool.

Manifest schema:
{
  "project": "science-episode-01",
  "segments": [
    {
      "id": "V001", "slot": "NARRATOR", "character": "Narrator",
      "provider": "voicestudio", "engine": "voxcpm2",
      "voice": "saved-profile-id", "language": "vi",
      "text": "Xin chào..."
    }
  ]
}

Supported providers: voicestudio, korva, google, elevenlabs.
No provider is contacted during --plan-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from client import VoiceStudioClient
from providers import google_cloud, korva, elevenlabs


def _safe_token(value: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-_")
    return text[:64] or fallback


def validate_manifest(data: dict[str, Any]) -> list[dict[str, Any]]:
    segments = data.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("Manifest must contain a non-empty 'segments' array")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(segments, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"segments[{index - 1}] must be an object")
        text = raw.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"segments[{index - 1}].text must be non-empty")
        if len(text) > 4096:
            raise ValueError(
                f"segments[{index - 1}] exceeds 4096 characters; split it into shorter speaker turns"
            )
        item = dict(raw)
        segment_id = str(item.get("id") or f"V{index:03d}")
        if not re.fullmatch(r"V\d{3,}", segment_id):
            raise ValueError(f"Invalid segment id {segment_id!r}; expected V001, V002, ...")
        if segment_id in seen:
            raise ValueError(f"Duplicate segment id: {segment_id}")
        seen.add(segment_id)
        item["id"] = segment_id
        item["slot"] = _safe_token(str(item.get("slot") or "NARRATOR"), "NARRATOR")
        item["character"] = (
            str(item.get("character") or "")
            .replace("|", "/").replace("·", "-").replace("=", "-")
            .replace("\\r", " ").replace("\\n", " ").strip()[:64]
        )
        item["provider"] = str(item.get("provider") or "voicestudio").lower()
        item["voice"] = str(item.get("voice") or "default")
        item["text"] = text.strip()
        item["language"] = str(item.get("language") or data.get("language") or "vi")
        item["engine"] = str(item.get("engine") or data.get("engine") or "omnivoice")
        item["speed"] = float(item.get("speed", data.get("speed", 1.0)))
        if not 0.25 <= item["speed"] <= 4.0:
            raise ValueError(f"segments[{index - 1}].speed must be between 0.25 and 4.0")
        if not isinstance(item.get("settings", {}), dict):
            raise ValueError(f"segments[{index - 1}].settings must be an object")
        if item["provider"] not in {"voicestudio", "korva", "google", "elevenlabs"}:
            raise ValueError(f"Unsupported provider: {item['provider']}")
        normalized.append(item)
    return normalized


def _synthesize(item: dict[str, Any], output_path: Path,
                voice_client: VoiceStudioClient) -> Path:
    provider = item["provider"]
    settings = item.get("settings") or {}
    if provider == "voicestudio":
        return voice_client.synthesize(
            item["text"], output_path,
            engine=item["engine"],
            voice=item["voice"],
            language=item["language"],
            speed=item["speed"],
            instruct=item.get("instruct"),
            description=item.get("description"),
            seed=item.get("seed"),
            extra=settings,
        )
    if provider == "korva":
        return korva.synthesize(
            item["text"], item["voice"], output_path,
            language=item["language"], speed=item["speed"], settings=settings,
        )
    if provider == "google":
        return google_cloud.synthesize(
            item["text"], item["voice"], output_path,
            language=item["language"], speed=item["speed"], settings=settings,
        )
    if provider == "elevenlabs":
        return elevenlabs.synthesize(
            item["text"], item["voice"], output_path,
            language=item["language"], speed=item["speed"], settings=settings,
        )
    raise ValueError(f"Unsupported provider: {provider}")


def _cache_key(item: dict[str, Any]) -> str:
    stable = {
        "provider": item["provider"], "engine": item["engine"],
        "voice": item["voice"], "language": item["language"],
        "speed": item["speed"], "text": item["text"],
        "instruct": item.get("instruct"), "description": item.get("description"),
        "seed": item.get("seed"), "settings": item.get("settings") or {},
    }
    raw = json.dumps(stable, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def generate(data: dict[str, Any], output_dir: Path, *, plan_only: bool = False) -> dict[str, Any]:
    segments = validate_manifest(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = output_dir / ".voice-cache"
    audio_dir = output_dir / "voice"
    if not plan_only:
        cache_dir.mkdir(parents=True, exist_ok=True)
        audio_dir.mkdir(parents=True, exist_ok=True)
    client = VoiceStudioClient()
    script_blocks = []
    outputs = []
    for item in segments:
        ext = ".mp3" if item["provider"] == "elevenlabs" else ".wav"
        cache_key = _cache_key(item)
        cached = cache_dir / f"{cache_key}{ext}"
        target = audio_dir / f"{item['id']}{ext}"
        safe_text = re.sub(r"(?m)^===", " ===", item["text"])
        script_blocks.append(
            f"=== {item['id']} | {item['slot']} · {item['character']} ===\\n"
            f"{safe_text}\\n"
        )
        row = {
            "id": item["id"], "provider": item["provider"], "engine": item["engine"],
            "voice": item["voice"], "language": item["language"],
            "file": f"voice/{target.name}", "cache_key": cache_key,
        }
        if plan_only:
            row["status"] = "planned"
        else:
            if cached.is_file() and cached.stat().st_size > 44:
                shutil.copy2(cached, target)
                row["status"] = "cache_hit"
            else:
                generated = _synthesize(item, cached, client)
                if not generated.is_file() or generated.stat().st_size <= 44:
                    raise RuntimeError(f"{item['id']}: provider produced no usable audio file")
                shutil.copy2(generated, target)
                row["status"] = "generated"
            row["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            row["bytes"] = target.stat().st_size
        outputs.append(row)

    slug = _safe_token(str(data.get("project") or "voiceover"), "voiceover").lower()
    voice_txt = output_dir / f"02-VOICE-{slug}-TTS.txt"
    report = {
        "schema_version": 1,
        "project": slug,
        "status": "plan_only" if plan_only else "generated",
        "segments": outputs,
        "voice_script": voice_txt.name,
        "prep_voice_command": (
            f'python tools/prep_voice.py --project projects/{slug} '
            f'--voice-dir "{audio_dir}" --voice-txt "{voice_txt}"'
        ),
    }
    if not plan_only:
        voice_txt.write_text("\n".join(script_blocks), encoding="utf-8")
        (output_dir / "voice-generation-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = generate(manifest, args.output, plan_only=args.plan_only)
    except Exception as exc:
        print(f"voice pipeline failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
