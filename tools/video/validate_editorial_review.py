#!/usr/bin/env python3
"""Validate a full-length, independent editorial review attestation.

This validates media identity and review-record completeness. It cannot prove
that a reviewer truthfully watched or listened to the candidate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCORE_FIELDS = (
    "storyClarity", "pacing", "visualVariety", "motionContinuity",
    "audioIntelligibility", "captionLegibility", "referenceFit", "platformFit",
)
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def media_facts(video: Path) -> tuple[str, float]:
    if not video.is_file() or video.stat().st_size == 0:
        raise ValueError(f"candidate video is missing or empty: {video}")
    digest = hashlib.sha256(video.read_bytes()).hexdigest()
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video),
        ],
        check=True, capture_output=True, text=True,
    )
    return digest, float(result.stdout.strip())


def validate_review_data(
    review: dict[str, Any],
    actual_sha256: str | None = None,
    actual_duration: float | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["review manifest must be a JSON object"]
    if review.get("schemaVersion") != 1:
        errors.append("schemaVersion must equal 1")

    candidate = review.get("candidate")
    if not isinstance(candidate, dict):
        errors.append("candidate must be an object")
        candidate = {}
    source_commit = candidate.get("sourceCommit")
    if not isinstance(source_commit, str) or len(source_commit) < 7 or source_commit.startswith("REPLACE_"):
        errors.append("candidate.sourceCommit must identify the exact source commit")
    video_path = candidate.get("videoPath")
    if not isinstance(video_path, str) or not video_path.strip() or video_path.startswith("REPLACE_"):
        errors.append("candidate.videoPath must identify the reviewed MP4")
    declared_hash = candidate.get("sha256")
    if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
        errors.append("candidate.sha256 must be a 64-character hexadecimal digest")
    elif actual_sha256 and declared_hash.lower() != actual_sha256.lower():
        errors.append("candidate.sha256 does not match the actual reviewed MP4")
    declared_duration = candidate.get("durationSeconds")
    if not isinstance(declared_duration, (int, float)) or declared_duration <= 0:
        errors.append("candidate.durationSeconds must be positive")
    elif actual_duration is not None and abs(float(declared_duration) - actual_duration) > 0.10:
        errors.append(
            f"candidate duration {declared_duration:.3f}s differs from ffprobe {actual_duration:.3f}s"
        )

    reviewer = review.get("reviewer")
    if not isinstance(reviewer, dict):
        errors.append("reviewer must be an object")
        reviewer = {}
    if not isinstance(reviewer.get("reviewerId"), str) or not reviewer.get("reviewerId", "").strip() or str(reviewer.get("reviewerId", "")).startswith("REPLACE_"):
        errors.append("reviewer.reviewerId is required")
    if not reviewer.get("role"):
        errors.append("reviewer.role is required")
    if reviewer.get("contextIndependent") is not True:
        errors.append("reviewer.contextIndependent must be true")
    if not isinstance(reviewer.get("reviewedAtUtc"), str) or not reviewer.get("reviewedAtUtc", "").endswith("Z"):
        errors.append("reviewer.reviewedAtUtc must be an ISO-8601 UTC timestamp ending in Z")

    method = review.get("method")
    if not isinstance(method, dict):
        errors.append("method must be an object")
        method = {}
    for key in (
        "fullPlaybackWithAudio", "normalPlaybackSpeed",
        "openEndedFindingsRecordedFirst", "checklistReviewedAfter",
        "checkedAtNativeDeliveryResolution",
    ):
        if method.get(key) is not True:
            errors.append(f"method.{key} must be true for final review")

    coverage = review.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        errors.append("coverage must contain timecoded review segments")
        coverage = []
    else:
        segments = []
        for index, segment in enumerate(coverage):
            if not isinstance(segment, dict):
                errors.append(f"coverage[{index}] must be an object")
                continue
            start, end = segment.get("start"), segment.get("end")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
                errors.append(f"coverage[{index}] has invalid start/end")
                continue
            if segment.get("visualReviewed") is not True or segment.get("audioReviewed") is not True:
                errors.append(f"coverage[{index}] must confirm both visual and audio review")
            segments.append((float(start), float(end), index))
        segments.sort()
        if segments and abs(segments[0][0]) > 0.05:
            errors.append(f"review coverage starts at {segments[0][0]:.3f}s, not 0s")
        cursor = 0.0
        for start, end, index in segments:
            if start > cursor + 0.05:
                errors.append(f"review coverage gap: {cursor:.3f}–{start:.3f}s")
            if start < cursor - 0.05:
                errors.append(f"review coverage overlap near {start:.3f}s")
            cursor = max(cursor, end)
        if actual_duration is not None and abs(cursor - actual_duration) > 0.10:
            errors.append(f"review coverage ends at {cursor:.3f}s, media ends at {actual_duration:.3f}s")
        elif actual_duration is None and isinstance(declared_duration, (int, float)) and abs(cursor - float(declared_duration)) > 0.10:
            errors.append(f"review coverage ends at {cursor:.3f}s, declared duration is {declared_duration:.3f}s")

    scores = review.get("scores")
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
        scores = {}
    score_values = []
    for key in SCORE_FIELDS:
        value = scores.get(key)
        if not isinstance(value, (int, float)) or not 0 <= value <= 10:
            errors.append(f"scores.{key} must be between 0 and 10")
        else:
            score_values.append(float(value))
            if value < 7:
                errors.append(f"scores.{key} is below the release threshold of 7/10")

    evidence = review.get("scoreEvidence")
    if not isinstance(evidence, dict):
        errors.append("scoreEvidence must be an object")
        evidence = {}
    for key in SCORE_FIELDS:
        text = evidence.get(key)
        if not isinstance(text, str) or len(text.strip()) < 20 or text.startswith("Replace "):
            errors.append(f"scoreEvidence.{key} must include specific observations (at least 20 characters)")

    open_findings = review.get("openEndedFindings")
    if not isinstance(open_findings, list) or not open_findings or not all(
        isinstance(item, str) and len(item.strip()) >= 8 and not item.startswith("Replace ")
        for item in open_findings
    ):
        errors.append("openEndedFindings must record the unaided first-pass results")

    defects = review.get("findings")
    if not isinstance(defects, list):
        errors.append("findings must be an array (use [] only after an actual review found no defects)")
        defects = []
    for index, defect in enumerate(defects):
        if not isinstance(defect, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        if defect.get("severity") not in {"P0", "P1", "P2"}:
            errors.append(f"findings[{index}].severity must be P0/P1/P2")
        if not defect.get("defectClass"):
            errors.append(f"findings[{index}].defectClass is required")
        if not isinstance(defect.get("timecodeStart"), (int, float)):
            errors.append(f"findings[{index}].timecodeStart is required")
        if not isinstance(defect.get("description"), str) or not defect.get("description", "").strip():
            errors.append(f"findings[{index}].description is required")
        if not isinstance(defect.get("evidence"), str) or len(defect.get("evidence", "").strip()) < 10:
            errors.append(f"findings[{index}].evidence must include timecoded evidence")
        if defect.get("severity") in {"P0", "P1"} and defect.get("resolved") is not True:
            errors.append(f"unresolved {defect.get('severity')} defect in final review: {defect.get('description', '')}")

    if review.get("decision") != "PASS":
        errors.append("decision must be PASS only after every release condition is met")
    if review.get("limitationsAcknowledged") is not True:
        errors.append("limitationsAcknowledged must be true")
    if len(score_values) == len(SCORE_FIELDS) and sum(score_values) / len(score_values) < 7.5:
        errors.append("average editorial score is below 7.5/10")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="Completed editorial-review JSON")
    parser.add_argument("--video", type=Path, required=True, help="Exact candidate MP4 to verify")
    args = parser.parse_args()
    try:
        review = json.loads(args.review.read_text(encoding="utf-8"))
        digest, duration = media_facts(args.video)
        errors = validate_review_data(review, digest, duration)
    except Exception as exc:
        print(f"EDITORIAL REVIEW VALIDATION: ERROR — {exc}")
        return 2
    if errors:
        print("EDITORIAL REVIEW VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EDITORIAL REVIEW VALIDATION: PASS")
    print(f"- Actual MP4 SHA-256 verified: {digest}")
    print(f"- Full visual/audio coverage recorded: {duration:.3f}s")
    print("- No unresolved P0/P1 defects; all category scores meet thresholds")
    print("- Note: this validates the attestation and media identity, not the truth of the reviewer's claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
