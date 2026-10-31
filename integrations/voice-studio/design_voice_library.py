"""Create reusable, original synthetic VoiceStudio profiles from a voice-design set.

The script creates native design profiles, not cloned real speakers. It writes
progress after every profile so interrupted batches can resume without
recreating completed entries. A live run can ask VoiceStudio to render each
profile's sample; --plan-only makes no API calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from client import VoiceStudioClient


def _fingerprint(engine: str, language: str, item: dict[str, Any]) -> str:
    identity = {
        "engine": engine,
        "language": language,
        "name": item["name"],
        "description": item["description"],
        "seed": item["seed"],
        "sample_text": item["sample_text"],
    }
    raw = json.dumps(identity, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()




def _speaker_id(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", name.casefold()).strip("_")
    return value[:48] or "voice"


def _cast_from_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cast: dict[str, Any] = {}
    for row in rows:
        profile_id = row.get("profile_id")
        if not profile_id or row.get("status") == "failed":
            continue
        speaker = _speaker_id(str(row["name"]))
        cast[speaker] = {
            "provider": "voicestudio",
            "engine": row["engine"],
            "voice": profile_id,
            "language": row["language"],
            "seed": row["seed"],
        }
    return cast


def _write_cast(output_dir: Path, language: str, rows: list[dict[str, Any]]) -> None:
    cast = _cast_from_rows(rows)
    if not cast:
        return
    _write_report(
        output_dir / "voice-cast.json",
        {
            "schema_version": 1,
            "language": language,
            "cast": cast,
        },
    )


def validate_design_set(data: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    engine = str(data.get("engine") or "").strip()
    language = str(data.get("language") or "vi").strip()
    if not engine:
        raise ValueError("Voice design set must specify an exact VoiceStudio engine ID")
    if not language:
        raise ValueError("Voice design set language cannot be empty")
    raw_voices = data.get("voices")
    if not isinstance(raw_voices, list) or not raw_voices:
        raise ValueError("Voice design set must include a non-empty voices array")
    voices: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_speaker_ids: set[str] = set()
    seen_seeds: set[int] = set()
    for index, raw in enumerate(raw_voices, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"voices[{index - 1}] must be an object")
        name = str(raw.get("name") or "").strip()
        description = str(raw.get("description") or "").strip()
        if not name or len(name) > 120:
            raise ValueError(f"voices[{index - 1}].name must contain 1–120 characters")
        if name.casefold() in seen_names:
            raise ValueError(f"Duplicate design-profile name: {name}")
        seen_names.add(name.casefold())
        speaker_id = _speaker_id(name)
        if speaker_id in seen_speaker_ids:
            raise ValueError(f"Voice names collide after speaker_id normalization: {name}")
        seen_speaker_ids.add(speaker_id)
        if not description or len(description) > 2000:
            raise ValueError(
                f"voices[{index - 1}].description must contain 1–2000 characters"
            )
        seed = raw.get("seed", 4200 + index)
        if not isinstance(seed, int):
            raise ValueError(f"voices[{index - 1}].seed must be an integer")
        if seed in seen_seeds:
            raise ValueError("Use a distinct seed for every designed voice in this set")
        seen_seeds.add(seed)
        sample_text = str(raw.get("sample_text") or data.get("sample_text") or "").strip()
        if not sample_text:
            raise ValueError(f"voices[{index - 1}] needs sample_text for profile audition")
        if len(sample_text) > 4096:
            raise ValueError(f"voices[{index - 1}].sample_text exceeds 4096 characters")
        voices.append({
            "name": name,
            "description": description,
            "seed": seed,
            "sample_text": sample_text,
        })
    return engine, language, voices


def _write_report(path: Path, report: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    temporary.replace(path)


def create_library(
    data: dict[str, Any],
    output_dir: Path,
    *,
    create: bool = False,
    render_previews: bool = True,
    resume: bool = True,
    delay: float = 0.5,
    client: VoiceStudioClient | None = None,
) -> dict[str, Any]:
    engine, language, voices = validate_design_set(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = output_dir / "audio"
    if create and render_previews:
        audio_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "voice-design-library.json"
    prior: dict[str, Any] = {}
    if resume and report_path.is_file():
        try:
            prior = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            prior = {}
    previous = {
        row.get("fingerprint"): row
        for row in prior.get("voices", [])
        if isinstance(row, dict) and row.get("fingerprint")
    }
    client = client or VoiceStudioClient()
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(voices, 1):
        fingerprint = _fingerprint(engine, language, item)
        existing = previous.get(fingerprint)
        row: dict[str, Any] = {
            "index": index,
            "name": item["name"],
            "engine": engine,
            "language": language,
            "description": item["description"],
            "seed": item["seed"],
            "sample_text": item["sample_text"],
            "fingerprint": fingerprint,
            "status": "planned" if not create else "pending",
        }
        if not create:
            rows.append(row)
            continue

        profile_id = existing.get("profile_id") if existing else None
        if profile_id:
            row["profile_id"] = profile_id
            row["profile_status"] = "reused"
        else:
            try:
                profile = client.create_design_profile(
                    item["name"],
                    item["description"],
                    engine=engine,
                    language=language,
                    seed=item["seed"],
                    sample_text=item["sample_text"],
                )
                profile_id = str(profile["id"])
                row["profile_id"] = profile_id
                row["profile_status"] = "created"
            except Exception as exc:
                row["status"] = "failed"
                row["error"] = f"{type(exc).__name__}: {exc}"
                rows.append(row)
                _write_report(report_path, {
                    "schema_version": 1, "engine": engine, "language": language,
                    "status": "partial", "voices": rows,
                    "failed": sum(r["status"] == "failed" for r in rows),
                    "preview_failed": sum(r.get("preview_status") == "pending_or_failed" for r in rows),
                    "cast": _cast_from_rows(rows),
                })
                _write_cast(output_dir, language, rows)
                if delay > 0 and index < len(voices):
                    time.sleep(delay)
                continue

        if render_previews:
            filename = f"{index:03d}-{fingerprint[:12]}.audio"
            destination = audio_dir / filename
            try:
                audio_path = client.profile_audio(profile_id, destination)
                row["preview_file"] = audio_path.relative_to(output_dir).as_posix()
                row["preview_bytes"] = audio_path.stat().st_size
                row["preview_status"] = "ready"
            except Exception as exc:
                row["preview_status"] = "pending_or_failed"
                row["preview_error"] = f"{type(exc).__name__}: {exc}"
        else:
            row["preview_status"] = "not_requested"
        row["status"] = "created" if row.get("profile_status") == "created" else "reused"
        rows.append(row)
        _write_report(report_path, {
            "schema_version": 1,
            "engine": engine,
            "language": language,
            "status": "creating",
            "created_or_reused": sum(r["status"] in {"created", "reused"} for r in rows),
            "failed": sum(r["status"] == "failed" for r in rows),
            "preview_failed": sum(r.get("preview_status") == "pending_or_failed" for r in rows),
            "voices": rows,
            "cast": _cast_from_rows(rows),
            "cast_file": "voice-cast.json" if create else None,
            "next_step": "Use voice-cast.json as the cast object in a video project manifest.",
            "human_review_required": True,
        })
        print(f"[{index}/{len(voices)}] {item['name']}: {row['status']} / {row['preview_status']}")
        if delay > 0 and index < len(voices):
            time.sleep(delay)

    failed = sum(row["status"] == "failed" for row in rows)
    preview_failed = sum(row.get("preview_status") == "pending_or_failed" for row in rows)
    incomplete = failed > 0 or (create and render_previews and preview_failed > 0)
    report = {
        "schema_version": 1,
        "engine": engine,
        "language": language,
        "status": "plan_only" if not create else "partial" if incomplete else "complete",
        "created_or_reused": sum(row["status"] in {"created", "reused"} for row in rows),
        "failed": failed,
        "preview_failed": preview_failed,
        "voices": rows,
        "cast": _cast_from_rows(rows),
        "cast_file": "voice-cast.json" if create else None,
        "next_step": (
            "Use voice-cast.json as the cast object in a video project manifest."
            if create else "Review the plan, then run again with --create to save VoiceStudio profiles."
        ),
        "human_review_required": True,
        "quality_note": (
            "Rendered preview files are audition samples, not proof of naturalness, "
            "identity quality, pronunciation accuracy, consent or output rights."
        ),
    }
    _write_report(report_path, report)
    if create:
        _write_cast(output_dir, language, rows)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--create", action="store_true",
                        help="Actually create profiles in the connected VoiceStudio service")
    parser.add_argument("--no-preview", action="store_true",
                        help="Create profiles without rendering their identity sample")
    parser.add_argument("--no-resume", action="store_true",
                        help="Do not reuse profile IDs saved in an earlier local report")
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()
    if args.delay < 0:
        parser.error("--delay cannot be negative")
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = create_library(
            data, args.output,
            create=args.create,
            render_previews=not args.no_preview,
            resume=not args.no_resume,
            delay=args.delay,
        )
    except Exception as exc:
        print(f"Voice design library failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "report": str(args.output / "voice-design-library.json"),
        "status": report["status"],
        "created_or_reused": report["created_or_reused"],
        "failed": report["failed"],
    }, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
