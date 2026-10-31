"""Build a local audition gallery from VoiceStudio-owned voices.

This uses the user's saved profiles and/or VoiceStudio archetype previews.
It does not train, clone, or accept a model licence on the user's behalf.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from client import VoiceStudioClient


LANGUAGE_LABELS = {
    "vi": "Vietnamese",
    "vi-vn": "Vietnamese",
    "en": "English",
    "en-us": "English",
    "zh": "Chinese",
    "zh-cn": "Chinese",
}


def _language_label(language: str | None) -> str | None:
    if not language:
        return None
    key = language.strip().lower().replace("_", "-")
    return LANGUAGE_LABELS.get(key, language.strip())


def _language_matches(value: Any, requested: str | None) -> bool:
    if not requested:
        return True
    if not value or str(value).strip().lower() in {"auto", "none"}:
        return True
    aliases = {
        "vi": {"vi", "vi-vn", "vietnamese"},
        "en": {"en", "en-us", "english"},
        "zh": {"zh", "zh-cn", "chinese"},
    }
    req = requested.strip().lower().replace("_", "-")
    allowed = aliases.get(req.split("-")[0], {req, req.split("-")[0]})
    actual = str(value).strip().lower().replace("_", "-")
    return actual in allowed or actual.split("-")[0] in allowed


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-_")
    return (cleaned or "voice")[:72]


def _profile_rows(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        return [row for row in raw if isinstance(row, dict)]
    if isinstance(raw, dict):
        items = raw.get("items") or raw.get("profiles") or []
        return [row for row in items if isinstance(row, dict)]
    return []


def collect_auditions(
    client: VoiceStudioClient,
    output_dir: Path,
    *,
    source: str = "profiles",
    language: str | None = "vi",
    search: str | None = None,
    limit: int = 20,
    delay: float = 0.5,
    benchmark_text: str | None = None,
    engine: str | None = None,
    blind: bool = False,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    tasks: list[tuple[str, dict[str, Any]]] = []

    if source in {"profiles", "both"}:
        profiles = _profile_rows(client.list_profiles())
        for profile in profiles:
            if not _language_matches(profile.get("language"), language):
                continue
            name = str(profile.get("name") or profile.get("id") or "Voice profile")
            if search and search.casefold() not in name.casefold():
                continue
            tasks.append(("profile", profile))
        tasks = tasks[:limit]

    if source in {"archetypes", "both"}:
        archetypes = client.list_archetypes(
            language=_language_label(language),
            search=search,
            limit=min(limit, 500),
        )
        tasks.extend(("archetype", item) for item in archetypes)

    if source == "archetypes":
        tasks = tasks[:limit]
    # For source=both, each source contributes up to --limit entries so a large
    # saved-profile library cannot crowd archetypes out of the comparison.

    audio_dir = output_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    for index, (kind, item) in enumerate(tasks, 1):
        identifier = str(item.get("id") or item.get("profile_id") or f"voice-{index:03d}")
        name = str(item.get("name") or identifier)
        filename_key = f"candidate-{index:03d}" if blind else _safe_filename(identifier)
        destination = audio_dir / f"{index:03d}-{filename_key}.audio"
        row: dict[str, Any] = {
            "kind": kind,
            "id": identifier,
            "name": name,
            "language": item.get("language"),
            "instruct": item.get("instruct"),
            "use_case": item.get("use_case"),
            "gender": (item.get("facets") or {}).get("gender"),
            "age": (item.get("facets") or {}).get("age"),
            "pitch": (item.get("facets") or {}).get("pitch"),
            "engine": item.get("engine") or item.get("design_recipe", {}).get("engine"),
            "is_featured": item.get("is_featured"),
            "status": "pending",
        }
        if blind:
            row["blind_label"] = f"Candidate {index:02d}"
        try:
            if kind == "profile" and benchmark_text:
                if not engine:
                    raise ValueError("--engine is required when --text-file is used")
                audio_path = client.synthesize(
                    benchmark_text, destination,
                    engine=engine, voice=identifier,
                    language=language,
                )
                row["benchmark_text"] = benchmark_text
                row["benchmark_engine"] = engine
            elif kind == "profile":
                audio_path = client.profile_audio(identifier, destination)
            else:
                row["preview_state"] = client.archetype_preview_state(identifier)
                audio_path = client.preview_archetype(identifier, destination)
            row["audio_file"] = audio_path.relative_to(output_dir).as_posix()
            row["bytes"] = audio_path.stat().st_size
            row["status"] = "ready"
        except Exception as exc:  # one unavailable preview must not lose the rest
            row["status"] = "failed"
            row["error"] = str(exc)
        entries.append(row)
        print(f"[{index}/{len(tasks)}] {name}: {row['status']}")
        if delay > 0 and index < len(tasks):
            time.sleep(delay)

    result = {
        "schema_version": 1,
        "source": source,
        "requested_language": language,
        "requested_search": search,
        "requested_limit": limit,
        "total": len(entries),
        "ready": sum(row["status"] == "ready" for row in entries),
        "failed": sum(row["status"] == "failed" for row in entries),
        "entries": entries,
        "blind": blind,
        "human_review": {
            "required": True,
            "note": "Listen to the clips. Metadata and successful HTTP responses do not establish naturalness, pronunciation, voice rights or character suitability.",
        },
    }
    (output_dir / "voice-auditions.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_html(result, output_dir / "index.html", blind=blind)
    return result


def _write_html(data: dict[str, Any], destination: Path, *, blind: bool = False) -> None:
    cards = []
    for item in data["entries"]:
        name = html.escape(
            str(item.get("blind_label") if blind else item.get("name", "Voice"))
        )
        meta = "Blind listening candidate" if blind else " · ".join(
            html.escape(str(value))
            for value in (
                item.get("kind"),
                item.get("language"),
                item.get("gender"),
                item.get("age"),
                item.get("pitch"),
                item.get("use_case"),
            )
            if value
        )
        audio = ""
        if item.get("audio_file"):
            src = html.escape(item["audio_file"], quote=True)
            audio = f'<audio controls preload="none" src="{src}"></audio>'
        else:
            audio = f'<p class="error">{html.escape(str(item.get("error", "Preview unavailable")))}</p>'
        instruct = "" if blind else html.escape(str(item.get("instruct") or ""))
        identifier = "" if blind else f'<code>{html.escape(str(item.get("id", "")))}</code>'
        cards.append(
            f'<article><h2>{name}</h2><p class="meta">{meta}</p>{audio}'
            f'<p class="instruct">{instruct}</p>{identifier}</article>'
        )
    document = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nolane Voice Audition</title>
<style>
:root{color-scheme:dark;background:#11131a;color:#f1f2f5;font:15px system-ui,sans-serif}
body{max-width:1100px;margin:32px auto;padding:0 18px}
header{margin-bottom:26px}h1{font-size:28px;margin:0 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
article{background:#1d202a;border:1px solid #363a46;border-radius:14px;padding:16px;min-width:0}
h2{font-size:18px;margin:0 0 6px}.meta,.instruct{color:#b8bdc9;font-size:13px}
audio{width:100%;margin:12px 0}code{color:#9aa3b8;font-size:11px;overflow-wrap:anywhere}
.error{color:#ffadad;overflow-wrap:anywhere}
.notice{color:#b8bdc9;max-width:800px;line-height:1.5}
</style></head><body>
<header><h1>Nolane Voice Audition</h1>
<p class="notice">A local audition sheet generated from VoiceStudio. Listen before selecting a permanent character voice. This page does not score naturalness automatically.</p>
</header><main class="grid">""" + "\n".join(cards) + "</main></body></html>"
    destination.write_text(document, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("profiles", "archetypes", "both"), default="profiles")
    parser.add_argument("--language", default="vi", help="e.g. vi, Vietnamese, English, or all")
    parser.add_argument("--search")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=Path("out/voice-auditions"))
    parser.add_argument("--text-file", type=Path,
                        help="Use the same fixed script for each saved profile (A/B test)")
    parser.add_argument("--engine", help="Exact installed VoiceStudio engine ID used with --text-file")
    parser.add_argument("--blind", action="store_true",
                        help="Hide voice names/IDs in the local audition HTML")
    args = parser.parse_args()
    if not 1 <= args.limit <= 500:
        parser.error("--limit must be between 1 and 500")
    if args.delay < 0:
        parser.error("--delay cannot be negative")
    language = None if args.language.lower() == "all" else args.language
    if args.text_file and args.source == "archetypes":
        parser.error("--text-file is for saved profiles; archetype previews use their curated sample text")
    if args.text_file and not args.engine:
        parser.error("--engine is required with --text-file")
    benchmark_text = None
    if args.text_file:
        try:
            benchmark_text = args.text_file.read_text(encoding="utf-8").strip()
        except OSError as exc:
            parser.error(f"Cannot read --text-file: {exc}")
        if not benchmark_text or len(benchmark_text) > 4096:
            parser.error("--text-file must contain 1–4096 characters")
    try:
        result = collect_auditions(
            VoiceStudioClient(), args.output,
            source=args.source, language=language, search=args.search,
            limit=args.limit, delay=args.delay,
            benchmark_text=benchmark_text, engine=args.engine, blind=args.blind,
        )
    except Exception as exc:
        print(f"Voice audition failed: {exc}", file=sys.stderr)
        return 2
    print(
        f"Audition gallery: {result['ready']} ready, {result['failed']} failed. "
        f"Open {args.output / 'index.html'}"
    )
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
