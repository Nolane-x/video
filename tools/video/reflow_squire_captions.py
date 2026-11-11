#!/usr/bin/env python3
"""Reflow Squire SRT/WebVTT captions while preserving source cue boundaries."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

TIME_SRT = re.compile(r"^(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})(?:\s+.*)?$")
TIME_VTT = re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})(?:\s+.*)?$")

@dataclass
class Cue:
    start: float
    end: float
    text: str


def parse_time(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        h, m, seconds = 0, int(parts[0]), float(parts[1])
    else:
        h, m, seconds = int(parts[0]), int(parts[1]), float(parts[2])
    return h * 3600 + m * 60 + seconds


def format_time(value: float, vtt: bool = False) -> str:
    ms = max(0, round(value * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{'.' if vtt else ','}{milli:03d}"


def parse_subtitles(path: Path, kind: str) -> list[Cue]:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    pattern = TIME_VTT if kind == "vtt" else TIME_SRT
    cues = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = [line.strip("\ufeff") for line in block.splitlines()]
        index = next((i for i, line in enumerate(lines) if pattern.match(line)), None)
        if index is None:
            continue
        match = pattern.match(lines[index])
        assert match
        payload = re.sub(r"\s+", " ", " ".join(x.strip() for x in lines[index + 1:] if x.strip())).strip()
        if payload:
            start, end = parse_time(match.group(1)), parse_time(match.group(2))
            if end <= start:
                raise ValueError(f"Invalid cue timing in {path}: {lines[index]}")
            cues.append(Cue(start, end, payload))
    if not cues:
        raise ValueError(f"No subtitle cues parsed from {path}")
    return cues


def wrap_words(words: list[str], width: int) -> list[str]:
    lines, current = [], ""
    for word in words:
        if len(word) > width:
            raise ValueError(f"Word exceeds {width}-character caption width: {word!r}")
        candidate = f"{current} {word}" if current else word
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def partition_words(text: str, width: int, max_lines: int) -> list[list[str]]:
    words = text.split()
    n = len(words)
    # First find the fewest cue groups that can each fit max_lines.
    counts = [10**9] * (n + 1)
    counts[n] = 0
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            if len(wrap_words(words[i:j], width)) > max_lines:
                break
            counts[i] = min(counts[i], 1 + counts[j])
    group_count = counts[0]
    if group_count >= 10**9:
        raise ValueError("Caption cannot be laid out at the requested width")
    # Among minimum-size partitions, choose the most balanced character loads.
    target = len(text) / group_count
    memo = {}
    def solve(i: int, left: int):
        key = (i, left)
        if key in memo:
            return memo[key]
        if left == 0:
            return (0.0, []) if i == n else None
        best = None
        for j in range(i + 1, n + 1):
            lines = wrap_words(words[i:j], width)
            if len(lines) > max_lines:
                break
            rest = solve(j, left - 1)
            if rest is None:
                continue
            chunk = " ".join(words[i:j])
            line_penalty = abs(len(lines[0]) - len(lines[-1])) * 0.18 if len(lines) == 2 else 0
            candidate = ((len(chunk) - target) ** 2 + line_penalty + rest[0], [words[i:j]] + rest[1])
            if best is None or candidate[0] < best[0]:
                best = candidate
        memo[key] = best
        return best
    result = solve(0, group_count)
    if result is None:
        raise RuntimeError("Subtitle partition solver failed")
    return result[1]


def reflow(cues: list[Cue], width: int = 42, max_lines: int = 2, min_dwell: float = 0.85):
    output, split_count = [], 0
    for cue in cues:
        groups = partition_words(cue.text, width, max_lines)
        if len(groups) > 1:
            split_count += 1
        captions = ["\n".join(wrap_words(group, width)) for group in groups]
        weights = [max(1, len(" ".join(group))) for group in groups]
        if cue.end - cue.start < min_dwell * len(groups):
            captions, weights = ["\n".join(wrap_words(cue.text.split(), width))], [1]
        total_weight = sum(weights)
        elapsed, current_start = 0, cue.start
        for index, (caption, weight) in enumerate(zip(captions, weights)):
            elapsed += weight
            current_end = cue.end if index == len(captions) - 1 else cue.start + (cue.end - cue.start) * elapsed / total_weight
            output.append(Cue(current_start, current_end, caption))
            current_start = current_end

    for cue in output:
        if cue.end <= cue.start:
            raise ValueError(f"Non-positive cue duration: {cue}")
    for previous, current in zip(output, output[1:]):
        if current.start < previous.end - 0.001:
            raise ValueError(f"Subtitle overlap: {previous} / {current}")
    before = " ".join(c.text for c in cues).split()
    after = " ".join(c.text.replace("\n", " ") for c in output).split()
    if before != after:
        raise ValueError("Reflow changed original caption words")
    lengths = [len(line) for cue in output for line in cue.text.splitlines()]
    report = {
        "source_cues": len(cues), "output_cues": len(output),
        "source_cues_split": split_count,
        "max_line_chars_before": max(len(line) for c in cues for line in c.text.splitlines()),
        "max_line_chars_after": max(lengths, default=0),
        "max_lines_per_cue_after": max(len(c.text.splitlines()) for c in output),
        "min_cue_duration_after_seconds": round(min(c.end - c.start for c in output), 3),
        "preserved_words": len(after), "status": "pass",
    }
    return output, report


def write_subtitles(cues: list[Cue], path: Path, kind: str) -> None:
    blocks = []
    for index, cue in enumerate(cues, 1):
        timing = f"{format_time(cue.start, kind == 'vtt')} --> {format_time(cue.end, kind == 'vtt')}"
        blocks.append(f"{index}\n{timing}\n{cue.text}" if kind == "srt" else f"{timing}\n{cue.text}")
    prefix = "WEBVTT\n\n" if kind == "vtt" else ""
    path.write_text(prefix + "\n\n".join(blocks) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--srt", required=True, type=Path)
    parser.add_argument("--vtt", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--width", type=int, default=42)
    parser.add_argument("--max-lines", type=int, default=2)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_srt = parse_subtitles(args.srt, "srt")
    source_vtt = parse_subtitles(args.vtt, "vtt")
    if len(source_srt) != len(source_vtt):
        raise ValueError(f"SRT/VTT cue count mismatch: {len(source_srt)} vs {len(source_vtt)}")
    for index, (a, b) in enumerate(zip(source_srt, source_vtt), 1):
        if abs(a.start - b.start) > 0.001 or abs(a.end - b.end) > 0.001 or a.text.split() != b.text.split():
            raise ValueError(f"SRT/VTT source mismatch at cue {index}")
    srt, srt_report = reflow(source_srt, args.width, args.max_lines)
    vtt, vtt_report = reflow(source_vtt, args.width, args.max_lines)
    write_subtitles(srt, args.output_dir / "captions.srt", "srt")
    write_subtitles(vtt, args.output_dir / "captions.vtt", "vtt")
    report = {"srt": srt_report, "vtt": vtt_report, "width": args.width, "max_lines": args.max_lines}
    (args.output_dir / "CAPTION-REFLOW-REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
