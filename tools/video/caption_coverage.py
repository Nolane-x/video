#!/usr/bin/env python3
"""OCR-audit required on-screen text against a timed shot manifest."""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path
from typing import Any


def normalize_text(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value.casefold())
    without_marks = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", without_marks))


def text_coverage(expected: str, observed: str) -> float:
    """Return fuzzy token recall, accent-insensitive for Vietnamese OCR variation."""
    normalized_expected = normalize_text(expected)
    normalized_observed = normalize_text(observed)
    expected_tokens = normalized_expected.split()
    observed_tokens = normalized_observed.split()
    if not expected_tokens or not observed_tokens:
        return 0.0
    if normalized_expected in normalized_observed:
        return 1.0
    scores = []
    for token in expected_tokens:
        best = max(
            (difflib.SequenceMatcher(None, token, actual).ratio() for actual in observed_tokens),
            default=0.0,
        )
        scores.append(best if best >= 0.72 else 0.0)
    return round(sum(scores) / len(scores), 4)


def expected_text_for_shot(shot: dict[str, Any], index: int, total: int) -> list[dict[str, str]]:
    """Resolve explicit text contract, or default to subtitle plus final end-card title."""
    explicit = shot.get("requiredOnScreenText") or shot.get("required_on_screen_text")
    if isinstance(explicit, list):
        return [
            {"kind": "required", "text": str(item).strip()}
            for item in explicit
            if isinstance(item, str) and item.strip()
        ]

    args = shot.get("args") or {}
    subtitle = args.get("subtitle") or shot.get("line")
    items: list[dict[str, str]] = []
    if isinstance(subtitle, str) and subtitle.strip():
        items.append({"kind": "subtitle", "text": subtitle.strip()})

    # The current Remotion composition switches to its title/subtitle end card
    # on the final shot. Normal shots show the timed subtitle, not args.title.
    title = args.get("title")
    if index == total - 1 and isinstance(title, str) and title.strip():
        items.append({"kind": "end-card-title", "text": title.strip()})
    return items


def run_checked(command: list[str]) -> str:
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout


def get_video_duration(video: Path) -> float:
    raw = run_checked([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video)
    ]).strip()
    return float(raw)


def ocr_frame(video: Path, at_seconds: float, languages: str, work_dir: Path, label: str) -> dict[str, str]:
    frame = work_dir / f"{label}.png"
    run_checked([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{at_seconds:.3f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=iw*2:ih*2", str(frame)
    ])
    outputs = []
    for psm in ("11", "6"):
        outputs.append(run_checked([
            "tesseract", str(frame), "stdout", "-l", languages, "--psm", psm
        ]).strip())
    return {"frame": str(frame), "text": "\n".join(outputs)}


def audit(video: Path, shots_path: Path, languages: str = "vie+eng",
          threshold: float = 0.67) -> dict[str, Any]:
    if not video.is_file() or video.stat().st_size == 0:
        raise ValueError(f"Video does not exist or is empty: {video}")
    manifest = json.loads(shots_path.read_text(encoding="utf-8"))
    shots = manifest.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("Shot manifest must contain a non-empty shots array")
    duration = get_video_duration(video)
    results = []
    total_items = 0
    passed_items = 0

    with tempfile.TemporaryDirectory(prefix="nolane-caption-qa-") as temp:
        work_dir = Path(temp)
        for index, shot in enumerate(shots):
            shot_id = str(shot.get("id", f"shot-{index + 1:03d}"))
            start = float(shot.get("start", -1))
            end = float(shot.get("end", -1))
            if start < 0 or end <= start or end > duration + 0.25:
                raise ValueError(f"{shot_id}: invalid time range {start}–{end} for {duration:.3f}s video")
            expected_items = expected_text_for_shot(shot, index, len(shots))
            if not expected_items:
                results.append({"shot_id": shot_id, "start": start, "end": end, "status": "no-text-contract"})
                continue

            sample_records = []
            for sample_index, fraction in enumerate((0.42, 0.58, 0.72), start=1):
                timestamp = start + (end - start) * fraction
                frame_result = ocr_frame(video, timestamp, languages, work_dir, f"{shot_id}-{sample_index}")
                sample_records.append({"at_seconds": round(timestamp, 3), **frame_result})

            shot_items = []
            for item in expected_items:
                scores = [text_coverage(item["text"], sample["text"]) for sample in sample_records]
                score = max(scores, default=0.0)
                passed = score >= threshold
                total_items += 1
                passed_items += int(passed)
                shot_items.append({
                    **item,
                    "coverage": score,
                    "threshold": threshold,
                    "status": "pass" if passed else "missing-or-illegible"
                })
            results.append({
                "shot_id": shot_id,
                "start": start,
                "end": end,
                "status": "pass" if all(item["status"] == "pass" for item in shot_items) else "fail",
                "required_text": shot_items,
                "samples": [
                    {"at_seconds": sample["at_seconds"], "ocr_text": sample["text"]}
                    for sample in sample_records
                ]
            })

    failed = total_items - passed_items
    return {
        "schema_version": 1,
        "video": str(video),
        "shot_manifest": str(shots_path),
        "video_duration_seconds": round(duration, 3),
        "ocr_languages": languages,
        "coverage_threshold": threshold,
        "shots_checked": len(shots),
        "text_items_checked": total_items,
        "text_items_passed": passed_items,
        "text_items_failed": failed,
        "coverage": round(passed_items / total_items, 4) if total_items else 1.0,
        "status": "pass" if failed == 0 else "fail",
        "shots": results
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--shots", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--languages", default="vie+eng")
    parser.add_argument("--threshold", type=float, default=0.67)
    args = parser.parse_args()
    report = audit(args.video, args.shots, args.languages, args.threshold)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "shots"}, ensure_ascii=False, indent=2))
    if report["status"] != "pass":
        for shot in report["shots"]:
            for item in shot.get("required_text", []):
                if item["status"] != "pass":
                    print(f"CAPTION BLOCKER [{shot['shot_id']}]: {item['text']!r} coverage={item['coverage']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
