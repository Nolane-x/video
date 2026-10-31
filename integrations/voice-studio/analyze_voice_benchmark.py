"""Summarize blind TTS benchmark ratings without inventing an objective quality score.

The analysis joins listener-entered 1–5 scores to the private identity map in
provider-voice-benchmark.json after the blind listening session is complete.
ASR WER/CER remains a separate pronunciation/intelligibility proxy.
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


def analyze_benchmark(
    benchmark: dict[str, Any],
    ratings: dict[str, Any] | None = None,
    *,
    min_ratings: int = 3,
) -> dict[str, Any]:
    if not 1 <= min_ratings <= len(DIMENSIONS):
        raise ValueError(f"min_ratings must be between 1 and {len(DIMENSIONS)}")
    raw_candidates = benchmark.get("candidates")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise ValueError("Benchmark report must include a non-empty candidates array")

    labels: dict[str, dict[str, Any]] = {}
    for index, candidate in enumerate(raw_candidates, 1):
        if not isinstance(candidate, dict):
            raise ValueError(f"candidates[{index - 1}] must be an object")
        label = str(candidate.get("blind_label") or f"Candidate {index:02d}")
        if label in labels:
            raise ValueError(f"Duplicate benchmark candidate label: {label}")
        labels[label] = candidate

    submitted: dict[str, dict[str, Any]] = {}
    if ratings is not None:
        raw_ratings = ratings.get("ratings")
        if not isinstance(raw_ratings, list):
            raise ValueError("Ratings file must contain a ratings array")
        for index, entry in enumerate(raw_ratings, 1):
            if not isinstance(entry, dict):
                raise ValueError(f"ratings[{index - 1}] must be an object")
            label = str(entry.get("candidate") or "").strip()
            if not label:
                raise ValueError(f"ratings[{index - 1}] is missing its candidate label")
            if label not in labels:
                raise ValueError(f"Unknown candidate in ratings file: {label}")
            if label in submitted:
                raise ValueError(f"Duplicate ratings submitted for {label}")
            submitted[label] = entry

    candidate_results: list[dict[str, Any]] = []
    for index, (label, candidate) in enumerate(labels.items(), 1):
        entry = submitted.get(label, {})
        scores: dict[str, float | None] = {}
        observed: list[float] = []
        for dimension in DIMENSIONS:
            value = entry.get("ratings", {}).get(dimension) if isinstance(entry.get("ratings", {}), dict) else None
            if value is None:
                scores[dimension] = None
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{label}.{dimension} must be a number from 1 to 5 or null")
            numeric = float(value)
            if not math.isfinite(numeric) or not 1 <= numeric <= 5:
                raise ValueError(f"{label}.{dimension} must be a number from 1 to 5 or null")
            scores[dimension] = numeric
            observed.append(numeric)

        proxy = candidate.get("asr_intelligibility_proxy") or {}
        asr_available = proxy.get("status") == "available"
        wer = proxy.get("wer") if asr_available else None
        cer = proxy.get("cer") if asr_available else None
        candidate_results.append({
            "blind_label": label,
            "provider": str(candidate.get("provider") or "unknown"),
            "id": candidate.get("id"),
            "name": candidate.get("name"),
            "engine": candidate.get("engine"),
            "synthesis_status": candidate.get("status"),
            "rating_count": len(observed),
            "dimension_ratings": scores,
            "mean_human_rating": _mean(observed),
            "eligible_for_human_comparison": len(observed) >= min_ratings,
            "asr_status": "available" if asr_available else "not_available",
            "wer": wer,
            "cer": cer,
        })

    providers = sorted({row["provider"] for row in candidate_results})
    provider_results: list[dict[str, Any]] = []
    for provider in providers:
        group = [row for row in candidate_results if row["provider"] == provider]
        eligible = [
            row for row in group
            if row["eligible_for_human_comparison"] and row["mean_human_rating"] is not None
        ]
        asr_rows = [
            row for row in group
            if row["asr_status"] == "available"
            and isinstance(row["wer"], (int, float))
            and isinstance(row["cer"], (int, float))
        ]
        dimension_means = {
            dimension: _mean([
                float(row["dimension_ratings"][dimension])
                for row in eligible
                if row["dimension_ratings"][dimension] is not None
            ])
            for dimension in DIMENSIONS
        }
        best = (
            sorted(
                eligible,
                key=lambda row: (
                    -float(row["mean_human_rating"]),
                    str(row.get("name") or row["blind_label"]),
                ),
            )[0]
            if eligible else None
        )
        provider_results.append({
            "provider": provider,
            "candidate_count": len(group),
            "eligible_candidate_count": len(eligible),
            "human_rating_coverage": round(len(eligible) / len(group), 3) if group else 0.0,
            "mean_candidate_rating": _mean([
                float(row["mean_human_rating"]) for row in eligible
            ]),
            "dimension_means": dimension_means,
            "highest_rated_candidate": (
                {
                    "blind_label": best["blind_label"],
                    "id": best["id"],
                    "name": best["name"],
                    "mean_human_rating": best["mean_human_rating"],
                    "rating_count": best["rating_count"],
                }
                if best else None
            ),
            "asr_sample_count": len(asr_rows),
            "mean_wer": _mean([float(row["wer"]) for row in asr_rows]),
            "mean_cer": _mean([float(row["cer"]) for row in asr_rows]),
        })

    eligible_all = [
        row for row in candidate_results
        if row["eligible_for_human_comparison"] and row["mean_human_rating"] is not None
    ]
    winner = (
        sorted(
            eligible_all,
            key=lambda row: (
                -float(row["mean_human_rating"]),
                str(row.get("provider") or ""),
                str(row.get("name") or row["blind_label"]),
            ),
        )[0]
        if eligible_all else None
    )
    return {
        "schema_version": 1,
        "benchmark_provider_selection": benchmark.get("provider"),
        "language": benchmark.get("language"),
        "script_sha256": benchmark.get("script_sha256"),
        "candidate_count": len(candidate_results),
        "rated_candidate_count": sum(row["rating_count"] > 0 for row in candidate_results),
        "eligible_candidate_count": len(eligible_all),
        "minimum_ratings_per_candidate": min_ratings,
        "human_rating_winner": (
            {
                "blind_label": winner["blind_label"],
                "provider": winner["provider"],
                "id": winner["id"],
                "name": winner["name"],
                "mean_human_rating": winner["mean_human_rating"],
                "rating_count": winner["rating_count"],
            }
            if winner else None
        ),
        "providers": provider_results,
        "candidates": candidate_results,
        "methodology": {
            "human_scale": "1–5; listener-entered subjective scores",
            "candidate_mean": "Unweighted mean of the dimensions actually rated",
            "provider_mean": "Unweighted mean of eligible candidate means, so a heavily rated voice does not dominate",
            "eligibility": f"At least {min_ratings} of {len(DIMENSIONS)} dimensions must be rated",
            "asr": "WER/CER is reported separately as an intelligibility proxy, not naturalness or voice similarity",
            "limitations": "This report is not an objective TTS quality score or an ElevenLabs-equivalence percentage. Listen to full samples and review rights before selecting a production voice.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", required=True, type=Path,
                        help="provider-voice-benchmark.json")
    parser.add_argument("--ratings", type=Path,
                        help="voice-human-ratings.json exported from the blind HTML page")
    parser.add_argument("--min-ratings", type=int, default=3,
                        help="Minimum rated dimensions required for candidate comparison (1–5)")
    parser.add_argument("--output", type=Path,
                        help="Output JSON; defaults beside the benchmark report")
    args = parser.parse_args()
    try:
        benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"))
        ratings = (
            json.loads(args.ratings.read_text(encoding="utf-8"))
            if args.ratings else None
        )
        result = analyze_benchmark(benchmark, ratings, min_ratings=args.min_ratings)
        output = args.output or args.benchmark.parent / "provider-voice-benchmark-analysis.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    except Exception as exc:
        print(f"Voice benchmark analysis failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "analysis": str(output),
        "candidate_count": result["candidate_count"],
        "rated_candidate_count": result["rated_candidate_count"],
        "eligible_candidate_count": result["eligible_candidate_count"],
        "human_rating_winner": result["human_rating_winner"],
        "objective_quality_score": None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
