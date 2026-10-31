"""Generate reviewable Vietnamese subtitle tracks from the H2 word timeline.

The input word timings are the timing estimator emitted by H2 prep_voice.py,
not ASR-aligned forced timestamps. This module preserves the source text and
makes the approximation explicit in the generated metadata.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


def _normal_word(value: str) -> str:
    normalized = unicodedata.normalize("NFC", str(value)).casefold()
    return "".join(char for char in normalized if char.isalnum())


def _time(value: float, *, vtt: bool = False) -> str:
    milliseconds = max(0, round(float(value) * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    separator = "." if vtt else ","
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}{separator}{millis:03d}"


def _wrap_caption(words: list[str], max_line_chars: int) -> str:
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > max_line_chars:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) > 2:
        raise ValueError(
            f"Caption needs {len(lines)} lines; reduce max_chars or max_line_chars"
        )
    return "\n".join(lines)


def build_cues(
    timeline_dir: Path,
    *,
    max_chars: int = 76,
    max_duration_s: float = 4.2,
    max_line_chars: int = 42,
    min_duration_s: float = 0.75,
) -> list[dict[str, Any]]:
    if not 20 <= max_chars <= 84:
        raise ValueError("max_chars must be between 20 and 84")
    if not 1.0 <= max_duration_s <= 7.0:
        raise ValueError("max_duration_s must be between 1 and 7 seconds")
    if not 20 <= max_line_chars <= 44:
        raise ValueError("max_line_chars must be between 20 and 44")
    if min_duration_s <= 0:
        raise ValueError("min_duration_s must be positive")

    lines = json.loads((timeline_dir / "lines.json").read_text(encoding="utf-8"))
    words = json.loads((timeline_dir / "words.json").read_text(encoding="utf-8"))
    blocks = json.loads((timeline_dir / "blocks.json").read_text(encoding="utf-8"))
    if not isinstance(lines, list) or not lines:
        raise ValueError("H2 timeline lines.json must contain at least one line")
    if not isinstance(words, list) or not words:
        raise ValueError("H2 timeline words.json must contain at least one word")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("H2 timeline blocks.json must contain at least one block")

    block_map = {
        str(item.get("id")): item
        for item in blocks
        if isinstance(item, dict) and item.get("id")
    }
    cursor = 0
    cues: list[dict[str, Any]] = []
    for line_index, line in enumerate(lines, 1):
        if not isinstance(line, dict):
            raise ValueError(f"lines[{line_index - 1}] must be an object")
        line_text = str(line.get("text") or "").strip()
        tokens = line_text.split()
        if not tokens:
            raise ValueError(f"lines[{line_index - 1}] contains no words")
        row_words = words[cursor:cursor + len(tokens)]
        if len(row_words) != len(tokens):
            raise ValueError(
                f"Word timeline ended early at line {line.get('id', line_index)}"
            )
        for token, word in zip(tokens, row_words):
            if _normal_word(token) != _normal_word(str(word.get("w") or "")):
                raise ValueError(
                    f"Word timeline does not match text at line {line.get('id', line_index)}: "
                    f"{token!r} != {word.get('w')!r}"
                )
        cursor += len(tokens)

        groups: list[list[tuple[str, dict[str, Any]]]] = []
        current: list[tuple[str, dict[str, Any]]] = []
        for token, word in zip(tokens, row_words):
            candidate = current + [(token, word)]
            candidate_text = " ".join(item[0] for item in candidate)
            start = float(candidate[0][1]["t"])
            end = float(candidate[-1][1]["e"])
            over_chars = len(candidate_text) > max_chars
            over_time = end - start > max_duration_s
            if current and (over_chars or over_time):
                groups.append(current)
                current = [(token, word)]
            else:
                current = candidate
        if current:
            groups.append(current)

        block_id = str(line.get("block") or "")
        block = block_map.get(block_id, {})
        for group_index, group in enumerate(groups, 1):
            cue_words = [item[0] for item in group]
            start_s = max(float(line.get("start", 0.0)), float(group[0][1]["t"]))
            end_s = min(float(line.get("end", group[-1][1]["e"])), float(group[-1][1]["e"]))
            if end_s <= start_s:
                raise ValueError(f"Invalid subtitle time range in {line.get('id', line_index)}")
            if end_s - start_s < min_duration_s:
                end_s = min(
                    float(line.get("end", end_s)),
                    start_s + min_duration_s,
                )
            cue_text = _wrap_caption(cue_words, max_line_chars)
            cues.append({
                "index": len(cues) + 1,
                "line_id": str(line.get("id") or f"L{line_index:03d}"),
                "block_id": block_id,
                "slot": str(line.get("slot") or block.get("slot") or ""),
                "character": str(line.get("char") or block.get("char") or ""),
                "start": round(start_s, 3),
                "end": round(end_s, 3),
                "text": cue_text,
                "source_word_count": len(group),
            })

    if cursor != len(words):
        raise ValueError(
            f"Word timeline has {len(words) - cursor} unmatched trailing entries"
        )
    for previous, current in zip(cues, cues[1:]):
        if current["start"] < previous["start"]:
            raise ValueError("Subtitle cues are not in chronological order")
        if current["start"] < previous["end"]:
            # The H2 word estimator can produce tiny rounding overlaps. Move
            # the later cue start to the earlier end; never extend cue duration.
            current["start"] = previous["end"]
            if current["end"] <= current["start"]:
                raise ValueError("Subtitle cue overlap collapses a cue to zero duration")
    return cues


def write_subtitles(
    timeline_dir: Path,
    output_dir: Path,
    *,
    max_chars: int = 76,
    max_duration_s: float = 4.2,
    max_line_chars: int = 42,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cues = build_cues(
        timeline_dir,
        max_chars=max_chars,
        max_duration_s=max_duration_s,
        max_line_chars=max_line_chars,
    )
    srt_parts: list[str] = []
    vtt_parts: list[str] = ["WEBVTT", ""]
    ass_dialogue: list[str] = []
    for cue in cues:
        start = _time(cue["start"])
        end = _time(cue["end"])
        srt_parts.append(
            f"{cue['index']}\n{start} --> {end}\n{cue['text']}"
        )
        vtt_parts.append(
            f"{_time(cue['start'], vtt=True)} --> {_time(cue['end'], vtt=True)}\n"
            f"{cue['text']}\n"
        )
        ass_text = cue["text"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        ass_text = ass_text.replace("\n", r"\N")
        ass_dialogue.append(
            f"Dialogue: 0,{_time(cue['start'], vtt=True)[:-1]},{_time(cue['end'], vtt=True)[:-1]},"
            f"Default,,0,0,0,,{ass_text}"
        )

    srt_path = output_dir / "captions.srt"
    vtt_path = output_dir / "captions.vtt"
    ass_path = output_dir / "captions.ass"
    json_path = output_dir / "captions.json"
    srt_path.write_text("\n\n".join(srt_parts) + "\n", encoding="utf-8")
    vtt_path.write_text("\n".join(vtt_parts).rstrip() + "\n", encoding="utf-8")
    ass_header = """[Script Info]
Title: Nolane Vietnamese Voice Captions
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H00FFFFFF,&H0000FFFF,&H00101010,&H80000000,0,0,1,3,1,2,100,100,64,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_path.write_text(ass_header + "\n".join(ass_dialogue) + "\n", encoding="utf-8-sig")
    payload = {
        "schema_version": 1,
        "language": "vi",
        "cue_count": len(cues),
        "source": "H2 prep_voice.py lines.json + words.json",
        "timing_method": (
            "H2 estimated word timings distributed from speech pauses and character-weighted "
            "sentence lengths; not forced-alignment ASR timestamps."
        ),
        "settings": {
            "max_chars_per_cue": max_chars,
            "max_duration_s": max_duration_s,
            "max_line_chars": max_line_chars,
            "max_lines": 2,
        },
        "files": {
            "srt": srt_path.name,
            "vtt": vtt_path.name,
            "ass": ass_path.name,
        },
        "cues": cues,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-chars", type=int, default=76)
    parser.add_argument("--max-duration", type=float, default=4.2)
    parser.add_argument("--max-line-chars", type=int, default=42)
    args = parser.parse_args()
    payload = write_subtitles(
        args.timeline,
        args.output,
        max_chars=args.max_chars,
        max_duration_s=args.max_duration,
        max_line_chars=args.max_line_chars,
    )
    print(json.dumps({
        "cue_count": payload["cue_count"],
        "files": payload["files"],
        "timing_method": payload["timing_method"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
