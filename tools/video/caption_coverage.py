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

MIN_READABLE_SAMPLES = 2


def normalize_text(value: str) -> str:
    value = value.replace("Đ", "D").replace("đ", "d")
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
    # OCR commonly emits compact labels such as DAY14 or 6:12AM without spaces.
    # Compare compact alphanumeric forms exactly; do not use fuzzy compact matching.
    compact_expected = "".join(expected_tokens)
    compact_observed = "".join(observed_tokens)
    if compact_expected and compact_expected in compact_observed:
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
    """Resolve explicit text requirements or infer text rendered by the current Remotion scene."""
    explicit_key = next((key for key in ("requiredOnScreenText", "required_on_screen_text") if key in shot), None)
    if explicit_key is not None:
        explicit = shot[explicit_key]
        if not isinstance(explicit, list):
            raise ValueError(f"{explicit_key} must be a list of exact visible strings")
        return [
            {"kind": "required", "text": item.strip()}
            for item in explicit
            if isinstance(item, str) and item.strip()
        ]

    args = shot.get("args") or {}
    if not isinstance(args, dict):
        raise ValueError("Shot args must be a JSON object")
    subtitle = args.get("subtitle") or shot.get("line")
    items: list[dict[str, str]] = []
    if isinstance(subtitle, str) and subtitle.strip():
        items.append({"kind": "subtitle", "text": subtitle.strip()})

    # Dynamic overlays in the current OneMoreScroll Remotion composition.
    day = args.get("day")
    if isinstance(day, str) and day.strip():
        items.append({"kind": "day-counter", "text": day.strip()})

    setting = args.get("setting") or shot.get("setting")
    red_words = args.get("redWords") or args.get("red_words") or []
    if setting in {"phone", "mirror", "void"} and isinstance(red_words, list):
        items.extend(
            {"kind": "red-word", "text": word.strip()}
            for word in red_words
            if isinstance(word, str) and word.strip()
        )

    # Fixed labels painted by the current scene backdrops.
    fixed_labels = {
        "calendar": ("THIS MONTH",),
        "classroom": ("PAY ATTENTION",),
        "bus": ("BUS",),
        "busStop": ("BUS",),
    }
    items.extend(
        {"kind": "scene-label", "text": label}
        for label in fixed_labels.get(setting, ())
    )

    # The current composition switches to its title/subtitle end card only on
    # the final shot. Normal shots show the timed subtitle, not args.title.
    title = args.get("title")
    if index == total - 1 and isinstance(title, str) and title.strip():
        items.append({"kind": "end-card-title", "text": title.strip()})
    return items


def resolve_text_contract(shot: dict[str, Any], index: int, total: int) -> tuple[list[dict[str, str]], str, str]:
    """Require visible text or a reasoned, explicit per-shot no-text exemption."""
    items = expected_text_for_shot(shot, index, total)
    no_text_required = bool(shot.get("noTextRequired", shot.get("no_text_required", False)))
    reason_value = shot.get("noTextReason") or shot.get("no_text_reason") or ""
    reason = reason_value.strip() if isinstance(reason_value, str) else ""

    if no_text_required:
        if items:
            raise ValueError(
                f"{shot.get('id', f'shot-{index + 1:03d}')}: noTextRequired conflicts with required visible text"
            )
        return ([], "approved-no-text" if reason else "missing-text-contract", reason)

    if not items:
        return [], "missing-text-contract", ""
    return items, "tracked", ""


def evaluate_text_samples(expected: str, observed_samples: list[str], threshold: float = 0.67) -> dict[str, Any]:
    """Require readable text in at least two of three sampled frames, not a single lucky OCR hit."""
    scores = [text_coverage(expected, observed) for observed in observed_samples]
    readable_samples = sum(score >= threshold for score in scores)
    minimum_readable_samples = min(MIN_READABLE_SAMPLES, len(scores))
    return {
        "coverage": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "best_sample_coverage": max(scores, default=0.0),
        "readable_samples": readable_samples,
        "sample_count": len(scores),
        "minimum_readable_samples": minimum_readable_samples,
        "passed": bool(scores) and readable_samples >= minimum_readable_samples,
    }


def targeted_ocr_region(item: dict[str, str], shot: dict[str, Any]) -> tuple[str, tuple[int, int, int, int]] | None:
    """Return a known, composition-specific crop for small or localized overlays."""
    args = shot.get("args") or {}
    setting = args.get("setting") or shot.get("setting")
    kind = item.get("kind")

    if kind == "day-counter":
        # Tight crop around the absolute top-left badge, excluding unrelated scene text.
        return ("top-left-day-counter", (25, 12, 140, 68))
    if kind == "subtitle":
        return ("lower-third-subtitle", (80, 575, 1120, 145))
    if kind == "end-card-title":
        return ("centered-end-card", (100, 110, 1080, 500))
    if kind == "scene-label":
        regions = {
            # Camera pan/zoom moves the calendar heading upward through this shot.
            "calendar": ("calendar-heading", (560, 35, 570, 125)),
            # Crop only the gold label, not the dark pole/shadow around it.
            "busStop": ("bus-stop-sign", (900, 153, 72, 52)),
            "bus": ("bus-sign", (80, 280, 280, 120)),
            "classroom": ("classroom-board-label", (470, 220, 530, 130)),
        }
        return regions.get(setting)

    if kind == "red-word":
        words = args.get("redWords") or args.get("red_words") or []
        word_index = next(
            (index for index, word in enumerate(words) if isinstance(word, str) and word.strip() == item.get("text")),
            None,
        )
        if word_index is None:
            return None
        word = str(words[word_index]).strip()
        if " " in word:
            # Multiword phrases occupy distinct negative-space rows, never the same anchor.
            x, y = (330, 95) if word_index == 0 else (330, 160)
            return (f"red-word-{word_index + 1}", (x, y, 260, 70))
        x = 64 + ((word_index * 197 + 80) % 1100)
        y = 150 + ((word_index * 83 + 38) % 330)
        width = max(250, min(500, len(word) * 19 + 100))
        return (f"red-word-{word_index + 1}", (max(0, x - 30), max(0, y - 38), width, 112))
    return None


def targeted_ocr_threshold(item: dict[str, str], shot: dict[str, Any]) -> int | None:
    """Return a restrained binary threshold for known overlay colors/backgrounds."""
    kind = item.get("kind")
    args = shot.get("args") or {}
    setting = args.get("setting") or shot.get("setting")
    if kind == "day-counter":
        return 140
    if kind == "scene-label" and setting in {"busStop", "calendar"}:
        return 80
    return None


def run_checked(command: list[str]) -> str:
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    return result.stdout


def get_video_duration(video: Path) -> float:
    raw = run_checked([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video)
    ]).strip()
    return float(raw)


def ocr_frame(
    video: Path,
    at_seconds: float,
    languages: str,
    work_dir: Path,
    label: str,
    shot: dict[str, Any],
    expected_items: list[dict[str, str]],
    threshold: float,
) -> dict[str, Any]:
    frame = work_dir / f"{label}.png"
    run_checked([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{at_seconds:.3f}", "-i", str(video),
        "-frames:v", "1", "-vf", "scale=iw*2:ih*2:flags=lanczos", str(frame)
    ])
    outputs = []
    for psm in ("11", "6"):
        outputs.append(run_checked([
            "tesseract", str(frame), "stdout", "-l", languages, "--psm", psm
        ]).strip())
    full_frame_text = "\n".join(outputs)

    # Only run focused OCR when whole-frame OCR did not find the expected text.
    # Coordinates are authored in the 1280x720 composition space; the source
    # frame above is already 2x, and each crop is enlarged another 2x.
    region_outputs: dict[str, str] = {}
    combined_text = full_frame_text
    for item_index, item in enumerate(expected_items):
        if text_coverage(item["text"], combined_text) >= threshold:
            continue
        region = targeted_ocr_region(item, shot)
        if region is None:
            continue
        region_name, (x, y, width, height) = region
        if region_name in region_outputs:
            continue
        x = max(0, min(1279, x))
        y = max(0, min(719, y))
        width = max(1, min(width, 1280 - x))
        height = max(1, min(height, 720 - y))
        crop = work_dir / f"{label}-{item_index + 1}-{region_name}.png"
        run_checked([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(frame),
            "-vf",
            (
                f"crop={width * 2}:{height * 2}:{x * 2}:{y * 2},"
                "scale=iw*2:ih*2:flags=lanczos,format=gray,"
                "eq=contrast=1.6:brightness=0.02,"
                "unsharp=5:5:1.0:5:5:0.0"
            ),
            "-frames:v", "1", str(crop)
        ])
        crop_outputs = []
        # The current Remotion counters, signs and kinetic words are English labels.
        # Keep EN/VI for captions; use the less-confusable English model for these tight crops.
        crop_language = languages if item.get("kind") in {"subtitle", "end-card-title"} else "eng"
        for psm in ("7", "11", "8"):
            crop_outputs.append(run_checked([
                "tesseract", str(crop), "stdout", "-l", crop_language, "--psm", psm
            ]).strip())
        # Binarized OCR tuned to each overlay's known foreground/background palette.
        # This adds evidence but keeps the same acceptance threshold and 2-of-3 rule.
        binary_threshold = targeted_ocr_threshold(item, shot)
        if binary_threshold is not None:
            binary_crop = work_dir / f"{label}-{item_index + 1}-{region_name}-binary.png"
            run_checked([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(frame),
                "-vf",
                (
                    f"crop={width * 2}:{height * 2}:{x * 2}:{y * 2},"
                    "scale=iw*2:ih*2:flags=lanczos,format=gray,"
                    f"lut=y='if(gte(val,{binary_threshold}),255,0)'"
                ),
                "-frames:v", "1", str(binary_crop)
            ])
            crop_outputs.append(run_checked([
                "tesseract", str(binary_crop), "stdout",
                "-l", crop_language, "--psm", "7"
            ]).strip())
        region_text = "\n".join(crop_outputs).strip()
        region_outputs[region_name] = region_text
        if region_text:
            combined_text += "\n" + region_text

    return {
        "frame": str(frame),
        "text": combined_text,
        "regions": region_outputs,
    }


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
    shots_without_text_contract = 0
    shots_approved_without_text = 0

    with tempfile.TemporaryDirectory(prefix="nolane-caption-qa-") as temp:
        work_dir = Path(temp)
        for index, shot in enumerate(shots):
            shot_id = str(shot.get("id", f"shot-{index + 1:03d}"))
            start = float(shot.get("start", -1))
            end = float(shot.get("end", -1))
            if start < 0 or end <= start or end > duration + 0.25:
                raise ValueError(f"{shot_id}: invalid time range {start}–{end} for {duration:.3f}s video")
            expected_items, contract_status, no_text_reason = resolve_text_contract(shot, index, len(shots))
            if contract_status == "approved-no-text":
                shots_approved_without_text += 1
                results.append({
                    "shot_id": shot_id, "start": start, "end": end,
                    "status": "approved-no-text", "no_text_reason": no_text_reason
                })
                continue
            if contract_status == "missing-text-contract":
                shots_without_text_contract += 1
                results.append({
                    "shot_id": shot_id, "start": start, "end": end,
                    "status": "missing-text-contract",
                    "error": "Declare requiredOnScreenText, provide an inferable subtitle, or add noTextRequired with noTextReason."
                })
                continue

            sample_records = []
            for sample_index, fraction in enumerate((0.42, 0.58, 0.72), start=1):
                timestamp = start + (end - start) * fraction
                frame_result = ocr_frame(
                    video, timestamp, languages, work_dir,
                    f"{shot_id}-{sample_index}", shot, expected_items, threshold
                )
                sample_records.append({"at_seconds": round(timestamp, 3), **frame_result})

            shot_items = []
            for item in expected_items:
                evaluation = evaluate_text_samples(
                    item["text"], [sample["text"] for sample in sample_records], threshold
                )
                passed = evaluation["passed"]
                total_items += 1
                passed_items += int(passed)
                shot_items.append({
                    **item,
                    **evaluation,
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
                    {
                        "at_seconds": sample["at_seconds"],
                        "ocr_text": sample["text"],
                        "ocr_regions": sample.get("regions", {}),
                    }
                    for sample in sample_records
                ]
            })

    failed = total_items - passed_items
    return {
        "schema_version": 5,
        "video": str(video),
        "shot_manifest": str(shots_path),
        "video_duration_seconds": round(duration, 3),
        "ocr_languages": languages,
        "coverage_threshold": threshold,
        "minimum_readable_samples_per_text_item": MIN_READABLE_SAMPLES,
        "shots_checked": len(shots),
        "shots_without_text_contract": shots_without_text_contract,
        "shots_approved_without_text": shots_approved_without_text,
        "text_items_checked": total_items,
        "text_items_passed": passed_items,
        "text_items_failed": failed,
        "coverage": round(passed_items / total_items, 4) if total_items else 1.0,
        "status": "pass" if failed == 0 and shots_without_text_contract == 0 else "fail",
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
            if shot["status"] == "missing-text-contract":
                print(f"CAPTION CONTRACT BLOCKER [{shot['shot_id']}]: {shot['error']}")
            for item in shot.get("required_text", []):
                if item["status"] != "pass":
                    print(
                        f"CAPTION BLOCKER [{shot['shot_id']}]: {item['text']!r} "
                        f"coverage={item['coverage']} readable_samples={item['readable_samples']}/{item['sample_count']}"
                    )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
