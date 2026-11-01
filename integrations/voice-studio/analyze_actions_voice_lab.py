"""Join the cross-scenario blind ratings to the private Actions voice map.

This creates a human-reviewed voice shortlist from a completed four-script
Actions benchmark. It never turns engineering metrics or listener opinions
into an objective naturalness or ElevenLabs-equivalence score.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

DIMENSIONS = (
    "naturalness",
    "vietnamese",
    "identity",
    "expression",
    "character_fit",
)


def _mean(values: list[float]) -> float | None:
    return round(sum(values) / len(values), 3) if values else None


def analyze_actions_voice_lab(
    benchmark: dict[str, Any],
    ratings_file: dict[str, Any],
    *,
    min_ratings: int = 3,
    shortlist_size: int = 3,
) -> dict[str, Any]:
    if not 1 <= min_ratings <= len(DIMENSIONS):
        raise ValueError(f"min_ratings must be between 1 and {len(DIMENSIONS)}")
    if not 1 <= shortlist_size <= 10:
        raise ValueError("shortlist_size must be between 1 and 10")
    cases = benchmark.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Actions benchmark must contain a non-empty cases array")

    voices: dict[str, dict[str, Any]] = {}
    case_ids: list[str] = []
    candidate_sets: list[set[str]] = []
    for case_index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"cases[{case_index}] must be an object")
        case_id = str(case.get("id") or "").strip()
        if not case_id or case_id in case_ids:
            raise ValueError(f"Missing or duplicate case ID at index {case_index}")
        case_ids.append(case_id)
        rows = case.get("candidates")
        if not isinstance(rows, list):
            raise ValueError(f"{case_id} must contain a candidates array")
        case_voice_ids: set[str] = set()
        for candidate_index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError(f"{case_id}.candidates[{candidate_index}] must be an object")
            voice_id = str(row.get("id") or "").strip()
            label = str(row.get("blind_label") or "").strip()
            if not voice_id or voice_id in case_voice_ids:
                raise ValueError(f"{case_id} contains a missing or duplicate voice ID")
            if not label:
                raise ValueError(f"{case_id}/{voice_id} is missing its blind label")
            case_voice_ids.add(voice_id)

            voice = voices.setdefault(voice_id, {
                "id": voice_id,
                "name": row.get("name"),
                "provider": row.get("provider") or benchmark.get("provider"),
                "engine": row.get("engine"),
                "blind_label": label,
                "scenarios": {},
            })
            if voice["blind_label"] != label:
                raise ValueError(
                    f"Blind label changed for the same voice between scenarios: {voice_id}"
                )
            if voice["name"] != row.get("name"):
                raise ValueError(f"Voice name changed between scenarios for {voice_id}")
            voice["scenarios"][case_id] = {
                "title": case.get("title") or case_id,
                "status": row.get("status"),
                "technical_status": row.get("technical_status"),
                "technical_findings": row.get("technical_findings") or [],
                "audio_file": row.get("audio_file"),
                "audio_sha256_verified": row.get("audio_sha256_verified") is True,
                "audio_metrics": row.get("audio_metrics"),
                "mastering": row.get("mastering"),
            }
        candidate_sets.append(case_voice_ids)

    if not voices:
        raise ValueError("Actions benchmark contains no voice candidates")
    expected_ids = set.union(*candidate_sets)
    complete_set = all(candidate_set == expected_ids for candidate_set in candidate_sets)

    raw_ratings = ratings_file.get("ratings")
    if not isinstance(raw_ratings, list):
        raise ValueError("Ratings export must contain a ratings array")
    ratings_by_label: dict[str, dict[str, Any]] = {}
    labels = {voice["blind_label"] for voice in voices.values()}
    if len(labels) != len(voices):
        raise ValueError("Blind labels must identify exactly one voice each")
    for index, entry in enumerate(raw_ratings):
        if not isinstance(entry, dict):
            raise ValueError(f"ratings[{index}] must be an object")
        label = str(entry.get("candidate") or "").strip()
        if not label or label not in labels:
            raise ValueError(f"Unknown blind candidate in ratings export: {label!r}")
        if label in ratings_by_label:
            raise ValueError(f"Duplicate ratings entry for {label}")
        raw_dimensions = entry.get("ratings") or {}
        if not isinstance(raw_dimensions, dict):
            raise ValueError(f"{label}.ratings must be an object")
        unknown_dimensions = set(raw_dimensions) - set(DIMENSIONS)
        if unknown_dimensions:
            raise ValueError(f"{label} contains unknown rating dimensions: {sorted(unknown_dimensions)}")
        normalized: dict[str, float] = {}
        for dimension, value in raw_dimensions.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{label}.{dimension} must be a number from 1 to 5")
            numeric = float(value)
            if not math.isfinite(numeric) or not 1 <= numeric <= 5:
                raise ValueError(f"{label}.{dimension} must be a finite number from 1 to 5")
            normalized[dimension] = numeric
        notes = entry.get("notes", "")
        if not isinstance(notes, str):
            raise ValueError(f"{label}.notes must be text")
        ratings_by_label[label] = {"ratings": normalized, "notes": notes.strip()}

    candidate_results: list[dict[str, Any]] = []
    for voice in voices.values():
        entry = ratings_by_label.get(voice["blind_label"], {"ratings": {}, "notes": ""})
        scores = entry["ratings"]
        observed = list(scores.values())
        scenarios = voice["scenarios"]
        ready_count = sum(item.get("status") == "ready" for item in scenarios.values())
        technical_pass = sum(item.get("technical_status") == "pass" for item in scenarios.values())
        technical_warning = sum(item.get("technical_status") == "warning" for item in scenarios.values())
        technical_error = sum(item.get("technical_status") == "error" for item in scenarios.values())
        mastered = [
            item["mastering"]
            for item in scenarios.values()
            if isinstance(item.get("mastering"), dict)
        ]
        true_peaks = [
            float(item["output_true_peak_dbtp"])
            for item in mastered
            if isinstance(item.get("output_true_peak_dbtp"), (int, float))
        ]
        integrated = [
            float(item["output_integrated_loudness_lufs"])
            for item in mastered
            if isinstance(item.get("output_integrated_loudness_lufs"), (int, float))
        ]
        candidate_results.append({
            **{
                key: voice.get(key)
                for key in ("id", "name", "provider", "engine", "blind_label")
            },
            "scenario_count": len(scenarios),
            "scenario_coverage_complete": len(scenarios) == len(case_ids),
            "ready_scenarios": ready_count,
            "technical_pass": technical_pass,
            "technical_warning": technical_warning,
            "technical_error": technical_error,
            "human_rating_count": len(observed),
            "human_dimension_ratings": {dimension: scores.get(dimension) for dimension in DIMENSIONS},
            "human_mean_rating": _mean(observed),
            "eligible_for_human_shortlist": (
                len(observed) >= min_ratings
                and len(scenarios) == len(case_ids)
                and ready_count == len(case_ids)
                and technical_error == 0
            ),
            "listener_notes": entry["notes"] or None,
            "mastering_summary": {
                "measured_sample_count": len(mastered),
                "mean_integrated_loudness_lufs": _mean(integrated),
                "maximum_true_peak_dbtp": max(true_peaks) if true_peaks else None,
            },
            "scenarios": scenarios,
        })

    ranked = [
        row for row in candidate_results
        if row["eligible_for_human_shortlist"] and row["human_mean_rating"] is not None
    ]
    ranked.sort(key=lambda row: (
        -float(row["human_mean_rating"]),
        -row["human_rating_count"],
        str(row["blind_label"]),
    ))
    winner = ranked[0] if ranked else None
    full_human_coverage = sum(row["human_rating_count"] == len(DIMENSIONS) for row in candidate_results)
    ready_voice_count = sum(row["scenario_coverage_complete"] and row["ready_scenarios"] == len(case_ids) for row in candidate_results)
    return {
        "schema_version": 1,
        "status": (
            "complete"
            if benchmark.get("status") == "complete" and complete_set and ready_voice_count == len(candidate_results)
            else "partial"
        ),
        "provider": benchmark.get("provider"),
        "language": benchmark.get("language", "vi"),
        "model": benchmark.get("model"),
        "runner": benchmark.get("runner"),
        "script_case_ids": case_ids,
        "script_count": len(case_ids),
        "voice_count": len(candidate_results),
        "fully_rendered_voice_count": ready_voice_count,
        "rated_voice_count": sum(row["human_rating_count"] > 0 for row in candidate_results),
        "fully_rated_voice_count": full_human_coverage,
        "eligible_voice_count": len(ranked),
        "minimum_rated_dimensions": min_ratings,
        "shortlist_size": shortlist_size,
        "human_rating_winner": (
            {
                "blind_label": winner["blind_label"],
                "id": winner["id"],
                "name": winner["name"],
                "human_mean_rating": winner["human_mean_rating"],
                "human_rating_count": winner["human_rating_count"],
            }
            if winner else None
        ),
        "shortlist": [
            {
                "rank": index,
                "blind_label": row["blind_label"],
                "id": row["id"],
                "name": row["name"],
                "human_mean_rating": row["human_mean_rating"],
                "human_rating_count": row["human_rating_count"],
                "human_dimension_ratings": row["human_dimension_ratings"],
                "listener_notes": row["listener_notes"],
                "mastering_summary": row["mastering_summary"],
            }
            for index, row in enumerate(ranked[:shortlist_size], 1)
        ],
        "candidates": sorted(candidate_results, key=lambda row: row["blind_label"]),
        "methodology": {
            "human_scale": "1–5 subjective listener ratings across five authored dimensions",
            "candidate_mean": "Unweighted mean of the dimensions the listener actually rated",
            "shortlist_eligibility": (
                f"At least {min_ratings} of {len(DIMENSIONS)} dimensions, "
                "all scenarios rendered, and zero technical audio errors"
            ),
            "technical_metrics": "Mastering/FFprobe measurements are engineering checks, not voice-quality scores",
            "limitations": (
                "This is a human-reviewed shortlist for the current scripts, presets and model revision. "
                "It is not an objective TTS naturalness score or an ElevenLabs-equivalence percentage."
            ),
        },
    }


def write_markdown(report: dict[str, Any], destination: Path) -> None:
    lines = [
        "# Actions Vietnamese voice shortlist",
        "",
        f"- Benchmark status: **{report['status']}**",
        f"- Scripts: {report['script_count']}",
        f"- Voices fully rendered: {report['fully_rendered_voice_count']}/{report['voice_count']}",
        f"- Voices rated: {report['rated_voice_count']}/{report['voice_count']}",
        f"- Eligible for shortlist: {report['eligible_voice_count']}",
        f"- Minimum rated dimensions: {report['minimum_rated_dimensions']}/5",
        "",
        "| Rank | Blind label | Voice | Human mean | Ratings | Max true peak dBTP |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for row in report["shortlist"]:
        peak = row["mastering_summary"]["maximum_true_peak_dbtp"]
        lines.append(
            f"| {row['rank']} | {row['blind_label']} | {row['name']} | "
            f"{row['human_mean_rating']:.3f} | {row['human_rating_count']}/5 | "
            f"{peak if peak is not None else '—'} |"
        )
    if not report["shortlist"]:
        lines.append("| — | — | No candidate yet | — | — | — |")
    lines.extend([
        "",
        "## Important interpretation",
        "",
        report["methodology"]["limitations"],
        "Listener ratings and written notes are the selection evidence. Technical audio measurements are separate and do not improve the underlying voice model.",
    ])
    destination.write_text("\\n".join(lines) + "\\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", required=True, type=Path,
                        help="actions-voice-lab.json from the Actions artifact")
    parser.add_argument("--ratings", required=True, type=Path,
                        help="voice-human-ratings-all-scripts.json exported from the combined blind page")
    parser.add_argument("--output", type=Path,
                        help="Output JSON; defaults beside the benchmark report")
    parser.add_argument("--min-ratings", type=int, default=3)
    parser.add_argument("--shortlist-size", type=int, default=3)
    args = parser.parse_args()
    try:
        benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"))
        ratings = json.loads(args.ratings.read_text(encoding="utf-8"))
        report = analyze_actions_voice_lab(
            benchmark,
            ratings,
            min_ratings=args.min_ratings,
            shortlist_size=args.shortlist_size,
        )
        output = args.output or args.benchmark.parent / "voice-shortlist.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
        write_markdown(report, output.with_suffix(".md"))
    except Exception as exc:
        print(f"Actions voice shortlist failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": report["status"],
        "voices": report["voice_count"],
        "rated": report["rated_voice_count"],
        "eligible": report["eligible_voice_count"],
        "winner": report["human_rating_winner"],
        "json": str(output),
        "markdown": str(output.with_suffix(".md")),
        "objective_naturalness_score": None,
        "elevenlabs_equivalence": None,
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
