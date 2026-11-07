#!/usr/bin/env python3
"""Prepare a VoiceStudio job from the Ain Jalut long-form script and live voice manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

MANIFEST_URL = (
    "https://github.com/Nolane-x/VoiceStudio/releases/download/"
    "voice-library-latest/manifest.json"
)
PREFERRED_VOICE = "en-vieneu-v3turbo-adam-3f0c9b"
COMMERCIAL_MARKERS = {
    "upstream-model-card-permits-generated-audio",
    "apache-2.0-model-and-voice-assets",
}


def read_manifest(path: str | None) -> dict:
    if path:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        request = Request(
            MANIFEST_URL,
            headers={"Accept": "application/json", "User-Agent": "Nolane-Squire-Production/1.0"},
        )
        with urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("voices"), list):
        raise ValueError("VoiceStudio manifest is missing its voices array")
    return data


def eligible(row: dict) -> bool:
    rights = row.get("rights") or {}
    checks = row.get("signal_checks") or {}
    return (
        row.get("language") == "en"
        and row.get("watermark") == "verified"
        and checks.get("status") == "passed"
        and rights.get("commercial_use") in COMMERCIAL_MARKERS
    )


def choose_voice(manifest: dict) -> tuple[dict, str]:
    rows = [row for row in manifest["voices"] if isinstance(row, dict) and eligible(row)]
    preferred = next((row for row in rows if row.get("id") == PREFERRED_VOICE), None)
    if preferred:
        return preferred, "Preferred VieNeu v3 Turbo Adam preset from the Squire production guide; current manifest confirms the exact canonical ID and its published permission/check metadata."
    grades = {"A": 0, "A-": 1, "B+": 2, "B": 3, "B-": 4}
    kokoro = [
        row for row in rows
        if "kokoro" in str(row.get("engine", "")).casefold()
        and row.get("upstream_quality_grade") in grades
    ]
    if kokoro:
        kokoro.sort(key=lambda row: (grades[row["upstream_quality_grade"]], row.get("id", "")))
        return kokoro[0], "The preferred VieNeu identity was absent from the live manifest; selected the highest upstream-graded eligible Kokoro English preset."
    bilingual = [row for row in rows if "vieneu" in str(row.get("engine", "")).casefold()]
    if bilingual:
        bilingual.sort(key=lambda row: (row.get("display_name", ""), row.get("id", "")))
        return bilingual[0], "Preferred and curated Kokoro voices were absent; selected an eligible VoiceStudio English VieNeu preset from the live manifest."
    raise RuntimeError("No eligible English narrator passed VoiceStudio signal, watermark and published-permission checks.")


def clean_script(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    text = re.sub(r"\n+\d[\d,]* words\..*$", "", text, flags=re.S).strip()
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        raise ValueError("The script is empty")
    return paragraphs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--manifest")
    args = parser.parse_args()

    manifest = read_manifest(args.manifest)
    voice, rationale = choose_voice(manifest)
    paragraphs = clean_script(Path(args.script))
    segments = []
    for i, paragraph in enumerate(paragraphs, 1):
        # VoiceStudio performs sentence-aware 360-character chunking and refuses truncation.
        if len(paragraph) > 4500:
            raise ValueError(f"Paragraph {i} is too long for the VoiceStudio contract")
        segments.append({
            "id": f"p{i:03d}",
            "text": paragraph,
            "pause_ms_after": 360 if i < len(paragraphs) else 0,
        })
    engine_name = str(voice.get("engine", "")).casefold()
    if "vieneu" in engine_name:
        engine = "vieneu"
    elif "kokoro" in engine_name:
        engine = "kokoro"
    else:
        raise RuntimeError(f"Unsupported selected narrator engine: {voice.get('engine')!r}")
    total_chars = sum(len(row["text"]) for row in segments)
    if total_chars > 30_000:
        raise ValueError(f"Script exceeds VoiceStudio's 30,000-character job limit ({total_chars})")

    job = {
        "schema_version": 1,
        "job_id": "ain-jalut-1260-longform",
        "title": "The Day the Mongols Were Stopped at Ain Jalut",
        "language": "en",
        "engine": engine,
        "voice_id": voice["id"],
        "segments": segments,
    }
    metadata = {
        "schema_version": 1,
        "manifest_built_at": manifest.get("built_at"),
        "manifest_counts": manifest.get("counts"),
        "voice_id": voice["id"],
        "display_name": voice.get("display_name"),
        "engine": voice.get("engine"),
        "upstream_quality_grade": voice.get("upstream_quality_grade"),
        "rights": voice.get("rights"),
        "signal_checks": voice.get("signal_checks"),
        "watermark": voice.get("watermark"),
        "rationale": rationale,
        "paragraph_count": len(segments),
        "script_characters": total_chars,
        "no_real_person_impersonation": True,
    }
    Path(args.output).write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.metadata).write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Selected {voice['id']} ({voice.get('engine')}); {len(segments)} paragraphs, {total_chars} characters.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[squire-voice-job] {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
