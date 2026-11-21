#!/usr/bin/env python3
"""Build a slower-reading alternate subtitle track without changing narration timing."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
from dataclasses import dataclass
from pathlib import Path


TIME_RE = re.compile(
    r"^(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})[,.](?P<ms>\d{3})$"
)
RANGE_RE = re.compile(
    r"^(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})(?:\s+.*)?$"
)


@dataclass(frozen=True)
class Cue:
    number: int
    start: float
    end: float
    text: str


def parse_time(value: str) -> float:
    match = TIME_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid subtitle timestamp: {value!r}")
    parts = match.groupdict()
    return (
        int(parts["h"]) * 3600
        + int(parts["m"]) * 60
        + int(parts["s"])
        + int(parts["ms"]) / 1000
    )


def format_time(value: float, separator: str) -> str:
    total_ms = int(round(value * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}{separator}{millis:03d}"


def parse_srt(raw: str) -> list[Cue]:
    normalized = raw.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise ValueError("The source SRT is empty")

    cues: list[Cue] = []
    blocks = re.split(r"\n[ \t]*\n+", normalized)
    for index, block in enumerate(blocks, start=1):
        lines = block.split("\n")
        if len(lines) < 3 or not lines[0].strip().isdigit():
            raise ValueError(f"Malformed SRT cue block {index}")
        number = int(lines[0].strip())
        if number != index:
            raise ValueError(f"Expected cue number {index}, found {number}")
        timing = RANGE_RE.fullmatch(lines[1].strip())
        if not timing:
            raise ValueError(f"Malformed timing line in cue {number}")
        start = parse_time(timing.group("start"))
        end = parse_time(timing.group("end"))
        text = "\n".join(lines[2:]).strip()
        if not text:
            raise ValueError(f"Cue {number} has empty text")
        if end <= start:
            raise ValueError(f"Cue {number} ends before it starts")
        if cues and start <= cues[-1].start:
            raise ValueError(f"Cue starts are not strictly increasing at cue {number}")
        cues.append(Cue(number, start, end, text))
    return cues


def percentile_lower(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("Cannot calculate a percentile for an empty list")
    return ordered[math.floor((len(ordered) - 1) * fraction)]


def cue_metrics(cues: list[Cue]) -> dict[str, float]:
    dwell = [cue.end - cue.start for cue in cues]
    cps = [len(cue.text.replace("\n", "")) / seconds for cue, seconds in zip(cues, dwell)]
    return {
        "median_chars_per_second": statistics.median(cps),
        "p90_chars_per_second": percentile_lower(cps, 0.90),
        "max_chars_per_second": max(cps),
        "min_dwell_seconds": min(dwell),
        "max_dwell_seconds": max(dwell),
    }


def wrap_text(text: str, max_line_chars: int = 42, max_lines: int = 2) -> str:
    """Wrap subtitle text at word boundaries without changing its words."""
    if max_line_chars < 1 or max_lines < 1:
        raise ValueError("Line width and maximum line count must be positive")
    words = text.split()
    if not words:
        raise ValueError("Cannot wrap empty subtitle text")

    lines: list[str] = []
    current = ""
    for word in words:
        if len(word) > max_line_chars:
            raise ValueError(f"Word exceeds subtitle line width ({len(word)} > {max_line_chars})")
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_line_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) >= max_lines:
                raise ValueError(f"Subtitle text exceeds the {max_lines}-line limit")
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        raise ValueError(f"Subtitle text exceeds the {max_lines}-line limit")
    return "\n".join(lines)


def wrap_cues(cues: list[Cue], max_line_chars: int = 42, max_lines: int = 2) -> list[Cue]:
    wrapped: list[Cue] = []
    for cue in cues:
        text = wrap_text(cue.text, max_line_chars=max_line_chars, max_lines=max_lines)
        if " ".join(text.split()) != " ".join(cue.text.split()):
            raise AssertionError(f"Word content changed while wrapping cue {cue.number}")
        wrapped.append(Cue(cue.number, cue.start, cue.end, text))
    return wrapped


def render_srt(cues: list[Cue]) -> str:
    blocks = []
    for cue in cues:
        blocks.append(
            f"{cue.number}\n"
            f"{format_time(cue.start, ',')} --> {format_time(cue.end, ',')}\n"
            f"{cue.text}"
        )
    return "\n\n".join(blocks) + "\n"


def render_vtt(cues: list[Cue]) -> str:
    blocks = ["WEBVTT"]
    for cue in cues:
        blocks.append(
            f"{format_time(cue.start, '.')} --> {format_time(cue.end, '.')}\n"
            f"{cue.text}"
        )
    return "\n\n".join(blocks) + "\n"


def build(source: Path, output: Path, duration: float, gap: float, expected_cues: int) -> dict:
    source_bytes = source.read_bytes()
    original = parse_srt(source_bytes.decode("utf-8-sig"))
    if len(original) != expected_cues:
        raise ValueError(f"Expected {expected_cues} cues, found {len(original)}")
    if duration <= 0 or gap < 0:
        raise ValueError("Duration must be positive and the inter-cue gap cannot be negative")
    if original[-1].end > duration:
        raise ValueError("The original final cue extends beyond the video end")
    source_overlap_count = sum(
        original[index].end > original[index + 1].start
        for index in range(len(original) - 1)
    )
    if source_overlap_count:
        raise ValueError(f"The source SRT contains {source_overlap_count} overlapping cues")

    extended: list[Cue] = []
    for index, cue in enumerate(original):
        next_start = original[index + 1].start if index + 1 < len(original) else duration
        new_end = next_start - gap if index + 1 < len(original) else duration
        if new_end <= cue.start:
            raise ValueError(
                f"Insufficient dwell room for cue {cue.number}: "
                f"start={cue.start}, proposed_end={new_end}"
            )
        extended.append(Cue(cue.number, cue.start, new_end, cue.text))

    overlap_count = sum(
        extended[index].end > extended[index + 1].start
        for index in range(len(extended) - 1)
    )
    if overlap_count:
        raise ValueError(f"Extended track contains {overlap_count} overlapping cues")
    if any(a.text != b.text or a.start != b.start for a, b in zip(original, extended)):
        raise AssertionError("Subtitle text or start times changed")

    output.mkdir(parents=True, exist_ok=True)
    srt_path = output / "time-stop-10s-readable-vi.srt"
    vtt_path = output / "time-stop-10s-readable-vi.vtt"
    srt_path.write_text(render_srt(extended), encoding="utf-8", newline="\n")
    vtt_path.write_text(render_vtt(extended), encoding="utf-8", newline="\n")

    wrapped = wrap_cues(extended, max_line_chars=42, max_lines=2)
    wrapped_srt = output / "time-stop-10s-readable-wrapped-vi.srt"
    wrapped_vtt = output / "time-stop-10s-readable-wrapped-vi.vtt"
    wrapped_srt.write_text(render_srt(wrapped), encoding="utf-8", newline="\n")
    wrapped_vtt.write_text(render_vtt(wrapped), encoding="utf-8", newline="\n")
    wrapped_lines = [line for cue in wrapped for line in cue.text.splitlines()]
    max_line_characters = max(map(len, wrapped_lines))
    max_lines_per_cue = max(len(cue.text.splitlines()) for cue in wrapped)
    wrapped_word_text_changes = sum(
        " ".join(source.text.split()) != " ".join(target.text.split())
        for source, target in zip(extended, wrapped)
    )
    if max_line_characters > 42 or max_lines_per_cue > 2 or wrapped_word_text_changes:
        raise AssertionError("Wrapped subtitle output violated its text/line-width constraints")

    report = {
        "status": "passed",
        "source": "Run-30 84-shot Vietnamese VieNeu subtitle track",
        "source_file": source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "variant": "extended-dwell",
        "video_duration_seconds": duration,
        "cue_count": len(original),
        "preserves_original_text_and_cue_starts": True,
        "preserves_voiceover_timing": True,
        "dwell_rule": (
            f"Each cue remains visible until {gap:.2f}s before the next shot's narration cue; "
            f"the final cue ends at {duration:.1f}s."
        ),
        "original": cue_metrics(original),
        "extended": cue_metrics(extended),
        "wrapped_variant": {
            "line_width_limit_characters": 42,
            "max_line_characters": max_line_characters,
            "max_lines_per_cue": 2,
            "max_observed_lines_per_cue": max_lines_per_cue,
            "word_text_changes": wrapped_word_text_changes,
            "files": [wrapped_srt.name, wrapped_vtt.name],
            "cue_text_preserved_after_whitespace_normalization": True,
        },
        "source_overlap_count": source_overlap_count,
        "overlap_count": overlap_count,
        "text_changes": 0,
        "notes": (
            "Supplementary subtitle variant only. The original SRT/VTT, master MP4, WAV "
            "and VoiceStudio timings remain unchanged."
        ),
    }
    (output / "subtitle-readability-qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--video-duration", type=float, default=378.0)
    parser.add_argument("--gap", type=float, default=0.12)
    parser.add_argument("--expected-cues", type=int, default=84)
    args = parser.parse_args()
    report = build(args.input, args.output, args.video_duration, args.gap, args.expected_cues)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
