"""Generate per-line speech assets for the existing H2 voice timeline tool.

A project can pin a cast once and refer to those speakers by speaker_id. This
prevents a character silently changing voice halfway through an episode.
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


IDENTITY_FIELDS = (
    "provider", "engine", "voice", "language", "instruct",
    "description", "seed", "settings",
)
PREP_VOICE_TOOL = (
    "integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/"
    "kit/tools/prep_voice.py"
)


def _safe_token(value: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-_")
    return text[:64] or fallback


def _identity_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {key: item.get(key) for key in IDENTITY_FIELDS}


def _identity_fingerprint(item: dict[str, Any]) -> str:
    raw = json.dumps(
        _identity_payload(item), sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_manifest(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw_segments = data.get("segments")
    if not isinstance(raw_segments, list) or not raw_segments:
        raise ValueError("Manifest must contain a non-empty 'segments' array")
    cast = data.get("cast", {})
    if not isinstance(cast, dict):
        raise ValueError("'cast' must map speaker_id values to voice settings")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    speaker_fingerprints: dict[str, str] = {}
    for index, raw in enumerate(raw_segments, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"segments[{index - 1}] must be an object")
        speaker_raw = raw.get("speaker_id")
        speaker_id = _safe_token(str(speaker_raw), "") if speaker_raw else ""
        cast_entry = {}
        if speaker_id:
            cast_entry = cast.get(speaker_id, {})
            if not isinstance(cast_entry, dict):
                raise ValueError(f"cast.{speaker_id} must be an object")
        # Segment-specific fields may add text, timing slot or acting notes;
        # voice identity is checked below so a cast member cannot drift.
        item = {**cast_entry, **raw}
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"segments[{index - 1}].text must be non-empty")
        if len(text) > 4096:
            raise ValueError(
                f"segments[{index - 1}] exceeds 4096 characters; split it into shorter speaker turns"
            )
        segment_id = str(item.get("id") or f"V{index:03d}")
        if not re.fullmatch(r"V\d{3,}", segment_id):
            raise ValueError(f"Invalid segment id {segment_id!r}; expected V001, V002, ...")
        if segment_id in seen:
            raise ValueError(f"Duplicate segment id: {segment_id}")
        seen.add(segment_id)
        item["id"] = segment_id
        item["speaker_id"] = speaker_id or None
        item["slot"] = _safe_token(str(item.get("slot") or "NARRATOR"), "NARRATOR")
        item["character"] = (
            str(item.get("character") or speaker_id or "")
            .replace("|", "/").replace("·", "-").replace("=", "-")
            .replace("\r", " ").replace("\n", " ").strip()[:64]
        )
        item["provider"] = str(item.get("provider") or "voicestudio").lower()
        item["voice"] = str(item.get("voice") or "default")
        item["text"] = text.strip()
        item["language"] = str(item.get("language") or data.get("language") or "vi")
        item["engine"] = str(item.get("engine") or data.get("engine") or "omnivoice")
        item["speed"] = float(item.get("speed", data.get("speed", 1.0)))
        speed_min, speed_max = (0.5, 2.0) if item["provider"] == "korva" else (0.7, 1.2) if item["provider"] == "elevenlabs" else (0.25, 4.0)
        if not speed_min <= item["speed"] <= speed_max:
            raise ValueError(
                f"segments[{index - 1}].speed for {item['provider']} must be between {speed_min} and {speed_max}"
            )
        if item.get("seed") is not None and not isinstance(item.get("seed"), int):
            raise ValueError(f"segments[{index - 1}].seed must be an integer")
        if not isinstance(item.get("settings", {}), dict):
            raise ValueError(f"segments[{index - 1}].settings must be an object")
        if item["provider"] not in {"voicestudio", "korva", "google", "elevenlabs"}:
            raise ValueError(f"Unsupported provider: {item['provider']}")
        if speaker_id:
            fingerprint = _identity_fingerprint(item)
            prior = speaker_fingerprints.get(speaker_id)
            if prior is not None and prior != fingerprint:
                raise ValueError(
                    f"Voice identity drift for speaker_id '{speaker_id}'. "
                    "Keep provider/engine/voice/language/style/seed/settings fixed in the cast."
                )
            speaker_fingerprints[speaker_id] = fingerprint
            item["voice_identity_fingerprint"] = fingerprint
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
            seed=item.get("seed"),
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


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def generate(
    data: dict[str, Any],
    output_dir: Path,
    *,
    plan_only: bool = False,
    stop_on_error: bool = False,
) -> dict[str, Any]:
    segments = validate_manifest(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = output_dir / ".voice-cache"
    audio_dir = output_dir / "voice"
    report_path = output_dir / "voice-generation-report.json"
    voice_txt = output_dir / f"02-VOICE-{_safe_token(str(data.get('project') or 'voiceover'), 'voiceover').lower()}-TTS.txt"
    if not plan_only:
        cache_dir.mkdir(parents=True, exist_ok=True)
        audio_dir.mkdir(parents=True, exist_ok=True)
    client = VoiceStudioClient()
    script_blocks: list[str] = []
    outputs: list[dict[str, Any]] = []
    slug = _safe_token(str(data.get("project") or "voiceover"), "voiceover").lower()

    def make_report(status: str) -> dict[str, Any]:
        return {
            "schema_version": 2,
            "project": slug,
            "status": status,
            "planned_segments": len(segments),
            "generated_segments": sum(
                row.get("status") in {"generated", "cache_hit"} for row in outputs
            ),
            "failed_segments": sum(row.get("status") == "failed" for row in outputs),
            "segments": outputs,
            "voice_script": voice_txt.name,
            "prep_voice_command": (
                f'python {PREP_VOICE_TOOL} --project projects/{slug} '
                f'--voice-dir "{audio_dir}" --voice-txt "{voice_txt}" --lang '
                f'{str(data.get("language") or "vi")}'
            ),
            "identity_policy": (
                "speaker_id binds a stable provider/engine/voice/language/style/seed/settings fingerprint"
            ),
        }

    for item in segments:
        ext = ".mp3" if item["provider"] == "elevenlabs" else ".wav"
        cache_key = _cache_key(item)
        cached = cache_dir / f"{cache_key}{ext}"
        target = audio_dir / f"{item['id']}{ext}"
        row: dict[str, Any] = {
            "id": item["id"],
            "speaker_id": item.get("speaker_id"),
            "slot": item["slot"],
            "character": item["character"],
            "provider": item["provider"],
            "engine": item["engine"],
            "voice": item["voice"],
            "language": item["language"],
            "expected_text": item["text"],
            "voice_identity_fingerprint": item.get("voice_identity_fingerprint"),
            "file": f"voice/{target.name}",
            "cache_key": cache_key,
        }
        if plan_only:
            row["status"] = "planned"
            outputs.append(row)
            continue

        try:
            target.unlink(missing_ok=True)
            if cached.is_file() and cached.stat().st_size > 44:
                shutil.copy2(cached, target)
                row["status"] = "cache_hit"
            else:
                generated = _synthesize(item, cached, client)
                if not generated.is_file() or generated.stat().st_size <= 44:
                    raise RuntimeError("provider produced no usable audio file")
                shutil.copy2(generated, target)
                row["status"] = "generated"
            row["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            row["bytes"] = target.stat().st_size
            safe_text = re.sub(r"(?m)^===", " ===", item["text"])
            script_blocks.append(
                f"=== {item['id']} | {item['slot']} · {item['character']} ===\n"
                f"{safe_text}\n"
            )
        except Exception as exc:
            target.unlink(missing_ok=True)
            row["status"] = "failed"
            row["error"] = f"{type(exc).__name__}: {exc}"
        outputs.append(row)

        # Persist progress after every line. If a long job is interrupted, prior
        # segments and their cache entries remain usable on the next run.
        _write_json_atomic(report_path, make_report("generating"))
        voice_txt.write_text("\n".join(script_blocks), encoding="utf-8")

        if row["status"] == "failed" and stop_on_error:
            break

    if plan_only:
        return make_report("plan_only")
    failed = any(row.get("status") == "failed" for row in outputs)
    report = make_report("partial" if failed else "generated")
    _write_json_atomic(report_path, report)
    voice_txt.write_text("\n".join(script_blocks), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--stop-on-error", action="store_true",
                        help="Stop after the first failed audio segment")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = generate(
            manifest, args.output,
            plan_only=args.plan_only,
            stop_on_error=args.stop_on_error,
        )
    except Exception as exc:
        print(f"voice pipeline failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
