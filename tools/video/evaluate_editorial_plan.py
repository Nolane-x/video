#!/usr/bin/env python3
"""Editorial preflight for a video shot plan.

This evaluates the creative plan, not the finished moving picture. It never
claims that a passing plan proves visual, audio or artistic approval.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_BRIEF_FIELDS = (
    "audience",
    "platform",
    "language",
    "aspectRatio",
    "viewerPromise",
    "hook",
    "payoff",
    "narrationPolicy",
    "visualGrammar",
)
NARRATION_POLICIES = {"voiceover", "dialogue", "none-by-design", "music-led"}
SHOT_LANGUAGE_FIELDS = ("shotSize", "cameraAngle", "cameraMove", "composition", "visualPurpose")

CONTACT_ACTION_PATTERNS = tuple(re.compile(pattern, re.IGNORECASE) for pattern in (
    r"\b(?:punch(?:es|ed|ing)?|hit(?:s|ting)?|strike(?:s|ing)?|struck|land(?:s|ed|ing)?|grab(?:s|bed|bing)?|catch(?:es|ing)?|caught)\b",
    r"\b(?:pick(?:s|ed)? up|put(?:s)? down|set(?:s)? down|place(?:s|d)?|lower(?:s|ed)?|release(?:s|d)?)\s+(?:the|a|an|their|his|her|its)\b",
    r"\b(?:open|opens|opened|opening)\s+(?:the|a|an|their|his|her|its)\b",
    r"\b(?:close|closes|closed|closing)\s+(?:the|a|an|their|his|her|its)\b",
    r"\b(?:write|writes|writing|wrote|written)\b",
    r"\b(?:tie|ties|tied|tying)\s+(?:the|their|his|her|both)\b",
))


def requires_motion_proof(action: str) -> bool:
    """Detect actual contact/prop verbs, not adjectives such as 'message remains open'."""
    return any(pattern.search(action) for pattern in CONTACT_ACTION_PATTERNS)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _finding(code: str, severity: str, message: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "message": message,
        "evidence": evidence or {},
    }


def _arc_errors(arc: Any, duration: float) -> list[str]:
    if not isinstance(arc, list) or not arc:
        return ["musicArc must be a non-empty array with intentional silence represented explicitly"]
    rows: list[tuple[float, float, str]] = []
    for index, item in enumerate(arc):
        if not isinstance(item, dict):
            return [f"musicArc[{index}] must be an object"]
        start, end, track = item.get("start"), item.get("end"), item.get("track")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not _nonempty(track):
            return [f"musicArc[{index}] needs numeric start/end and a named track or intentional-silence"]
        if end <= start:
            return [f"musicArc[{index}] end must be after start"]
        rows.append((float(start), float(end), str(track)))
    rows.sort()
    errors: list[str] = []
    if abs(rows[0][0]) > 1e-6:
        errors.append(f"musicArc starts at {rows[0][0]}s, expected 0s")
    cursor = 0.0
    for start, end, track in rows:
        if start > cursor + 1e-6:
            errors.append(f"musicArc gap {cursor:.3f}–{start:.3f}s has no music or explicit silence")
        if start < cursor - 1e-6:
            errors.append(f"musicArc overlap near {start:.3f}s")
        cursor = max(cursor, end)
    if abs(cursor - duration) > 1e-6:
        errors.append(f"musicArc ends at {cursor:.3f}s, expected {duration:.3f}s")
    return errors


def evaluate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        return {
            "schemaVersion": 1,
            "status": "BLOCKED",
            "recommendation": "REVISE_PLAN",
            "planReadinessScore": 0,
            "findings": [_finding("shots.missing", "P0", "A non-empty shot list is required.")],
            "scoreBreakdown": {},
            "metrics": {},
            "limitations": ["This is a plan-level preflight, not a review of rendered video/audio."],
        }

    duration = plan.get("duration")
    duration = float(duration) if isinstance(duration, (int, float)) else 0.0
    brief = plan.get("creativeBrief")
    brief = brief if isinstance(brief, dict) else {}

    brief_present = 0
    for key in REQUIRED_BRIEF_FIELDS:
        if _nonempty(brief.get(key)):
            brief_present += 1
        else:
            findings.append(_finding(
                f"brief.{key}", "P1",
                f"Creative brief is missing required field: {key}.",
                {"field": key},
            ))

    policy_value = brief.get("narrationPolicy")
    policy = policy_value if isinstance(policy_value, str) else ""
    if policy and policy not in NARRATION_POLICIES:
        findings.append(_finding(
            "audio.invalid-narration-policy", "P1",
            f"narrationPolicy must be one of {sorted(NARRATION_POLICIES)}.",
            {"value": policy},
        ))
    if policy in {"none-by-design", "music-led"} and not _nonempty(brief.get("narrationRationale")):
        findings.append(_finding(
            "audio.no-narration-rationale", "P1",
            "A no-voiceover/music-led choice needs a story-specific rationale and a clear alternative for carrying meaning.",
        ))
    if policy in {"voiceover", "dialogue"} and not _nonempty(brief.get("speechPlan")):
        findings.append(_finding(
            "audio.missing-speech-plan", "P1",
            "Voiceover/dialogue is selected but no narration/dialogue plan is supplied.",
        ))

    audio_plan = plan.get("audioPlan")
    if policy in {"voiceover", "dialogue"}:
        narration_segments = audio_plan.get("narration") if isinstance(audio_plan, dict) else None
        if not isinstance(narration_segments, list) or not narration_segments:
            findings.append(_finding(
                "audio.missing-timed-narration", "P1",
                "Voiceover/dialogue requires timed narration segments and real audio file paths in audioPlan.narration.",
            ))
        else:
            for index, segment in enumerate(narration_segments):
                if not isinstance(segment, dict):
                    findings.append(_finding("audio.invalid-narration-segment", "P1", f"audioPlan.narration[{index}] must be an object."))
                    continue
                if not _nonempty(segment.get("file")):
                    findings.append(_finding("audio.narration-file-missing", "P1", f"audioPlan.narration[{index}] needs a generated/approved audio filename."))
                if not isinstance(segment.get("start"), (int, float)) or not isinstance(segment.get("end"), (int, float)) or segment["end"] <= segment["start"]:
                    findings.append(_finding("audio.narration-timing-invalid", "P1", f"audioPlan.narration[{index}] has invalid start/end timing."))
    if isinstance(audio_plan, dict) and "soundCues" in audio_plan:
        cues = audio_plan.get("soundCues")
        if not isinstance(cues, list):
            findings.append(_finding("audio.sound-cues-invalid", "P1", "audioPlan.soundCues must be an array."))
        else:
            for index, cue in enumerate(cues):
                if not isinstance(cue, dict) or not _nonempty(cue.get("file")):
                    findings.append(_finding("audio.sound-cue-file-missing", "P1", f"audioPlan.soundCues[{index}] needs a file."))
                    continue
                if not isinstance(cue.get("start"), (int, float)) or not isinstance(cue.get("duration"), (int, float)) or cue["duration"] <= 0:
                    findings.append(_finding("audio.sound-cue-timing-invalid", "P1", f"audioPlan.soundCues[{index}] needs valid start/duration."))
                elif cue["start"] < 0 or cue["start"] + cue["duration"] > duration + 0.05:
                    findings.append(_finding("audio.sound-cue-out-of-range", "P1", f"audioPlan.soundCues[{index}] falls outside the composition."))

    story_arc = brief.get("storyArc")
    if not isinstance(story_arc, list) or len(story_arc) < 3:
        findings.append(_finding(
            "story.arc-incomplete", "P1",
            "The brief needs at least three named story beats/acts (setup, development, payoff) with their purpose.",
            {"storyArcCount": len(story_arc) if isinstance(story_arc, list) else 0},
        ))
        story_arc_ok = False
    else:
        story_arc_ok = all(isinstance(x, dict) and _nonempty(x.get("name")) and _nonempty(x.get("purpose")) for x in story_arc)
        if not story_arc_ok:
            findings.append(_finding(
                "story.arc-purpose-missing", "P1",
                "Each story beat needs a name and an explicit viewer/story purpose.",
            ))

    if not _nonempty(brief.get("pacingRationale")):
        findings.append(_finding(
            "pacing.rationale-missing", "P2",
            "Explain the intended rhythm (variation, holds, acceleration and release); do not inherit a fixed timing grid by default.",
        ))

    ids: list[str] = []
    durations: list[float] = []
    templates: list[str] = []
    settings: list[str] = []
    poses: list[str] = []
    language_complete = 0
    story_function_complete = 0
    motion_proof_complete = 0
    captions_complete = 0
    reading_speed_max = 0.0
    shot_language_missing: list[str] = []
    contact_actions: list[str] = []
    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            findings.append(_finding("shot.invalid", "P0", f"Shot {index + 1} is not an object."))
            continue
        shot_id = str(shot.get("id") or f"shot-{index + 1:03d}")
        ids.append(shot_id)
        start, end = shot.get("start"), shot.get("end")
        if isinstance(start, (int, float)) and isinstance(end, (int, float)) and end > start:
            shot_duration = float(end) - float(start)
            durations.append(shot_duration)
        else:
            shot_duration = 0.0
            findings.append(_finding("shot.invalid-time", "P0", f"{shot_id} has invalid timing."))

        tpl = shot.get("tpl") or shot.get("template") or "unspecified"
        templates.append(str(tpl))
        args = shot.get("args") if isinstance(shot.get("args"), dict) else {}
        setting = args.get("setting") or shot.get("setting") or "unspecified"
        pose = args.get("pose") or shot.get("pose") or "unspecified"
        settings.append(str(setting))
        poses.append(str(pose))

        shot_language = shot.get("shotLanguage")
        if isinstance(shot_language, dict) and all(_nonempty(shot_language.get(k)) for k in SHOT_LANGUAGE_FIELDS):
            language_complete += 1
        else:
            shot_language_missing.append(shot_id)

        if _nonempty(shot.get("storyFunction")):
            story_function_complete += 1

        action = shot.get("action") if isinstance(shot.get("action"), str) else ""
        motion_proof = shot.get("motionProof")
        if isinstance(motion_proof, dict) and all(_nonempty(motion_proof.get(k)) for k in ("keyAction", "contactOrChange", "followThrough")):
            motion_proof_complete += 1
        if requires_motion_proof(action):
            contact_actions.append(shot_id)
            if not isinstance(motion_proof, dict):
                findings.append(_finding(
                    "motion.contact-proof-missing", "P1",
                    f"{shot_id} describes a physical action but has no key-action/contact/follow-through proof plan.",
                    {"shotId": shot_id, "action": action},
                ))

        subtitle = args.get("subtitle") or shot.get("line")
        if _nonempty(subtitle) and shot_duration > 0:
            captions_complete += 1
            words = len(str(subtitle).split())
            reading_speed = words / shot_duration * 60.0
            reading_speed_max = max(reading_speed_max, reading_speed)
            if reading_speed > 180:
                findings.append(_finding(
                    "text.reading-speed-high", "P1",
                    f"{shot_id} requires about {reading_speed:.0f} words/minute to read its on-screen line.",
                    {"shotId": shot_id, "words": words, "durationSeconds": round(shot_duration, 2)},
                ))

    if len(ids) != len(set(ids)):
        findings.append(_finding("shot.duplicate-ids", "P0", "Shot IDs must be unique."))

    ordered_shots = sorted(
        (
            float(shot["start"]), float(shot["end"]), str(shot.get("id") or "unknown")
        )
        for shot in shots
        if isinstance(shot, dict)
        and isinstance(shot.get("start"), (int, float))
        and isinstance(shot.get("end"), (int, float))
        and shot.get("end") > shot.get("start")
    )
    if ordered_shots:
        if abs(ordered_shots[0][0]) > 0.05:
            findings.append(_finding(
                "timeline.start-gap", "P0",
                f"Timeline starts at {ordered_shots[0][0]:.3f}s instead of 0s.",
            ))
        cursor = 0.0
        for start, end, shot_id in ordered_shots:
            if start > cursor + 0.05:
                findings.append(_finding(
                    "timeline.gap", "P0",
                    f"Timeline has an uncovered gap from {cursor:.3f}s to {start:.3f}s.",
                    {"shotId": shot_id},
                ))
            elif start < cursor - 0.05:
                findings.append(_finding(
                    "timeline.overlap", "P0",
                    f"Shot {shot_id} overlaps the preceding shot near {start:.3f}s.",
                    {"shotId": shot_id},
                ))
            cursor = max(cursor, end)
        if duration > 0 and abs(cursor - duration) > 0.05:
            findings.append(_finding(
                "timeline.duration-mismatch", "P0",
                f"Last shot ends at {cursor:.3f}s, but composition duration is {duration:.3f}s.",
            ))
    if durations:
        mean_duration = statistics.mean(durations)
        duration_cv = statistics.pstdev(durations) / mean_duration if mean_duration else 0.0
        distinct_durations = len({round(x, 3) for x in durations})
        uniform_duration = len(durations) >= 6 and duration_cv < 0.08 and distinct_durations <= 2
        if uniform_duration and not _nonempty(brief.get("pacingRationale")):
            findings.append(_finding(
                "pacing.uniform-grid", "P1",
                "Nearly every shot has the same duration. A fixed grid needs an explicit creative justification and beat-level evidence.",
                {"shotCount": len(durations), "durationCV": round(duration_cv, 4), "distinctDurations": distinct_durations},
            ))
        elif uniform_duration:
            findings.append(_finding(
                "pacing.uniform-grid-review", "P2",
                "Uniform shot timing is explicitly intended; verify it against the actual music, speech and story beats.",
                {"shotCount": len(durations), "durationCV": round(duration_cv, 4), "distinctDurations": distinct_durations},
            ))
        for index, shot_duration in enumerate(durations):
            if shot_duration > 9.0:
                shot = shots[index]
                if not _nonempty(shot.get("holdRationale")):
                    findings.append(_finding(
                        "pacing.long-hold-unjustified", "P2",
                        f"{ids[index]} holds for {shot_duration:.1f}s without a stated reason.",
                        {"shotId": ids[index], "durationSeconds": round(shot_duration, 2)},
                    ))
    else:
        mean_duration, duration_cv, distinct_durations, uniform_duration = 0.0, 0.0, 0, False

    template_counts = Counter(templates)
    dominant_template, dominant_count = template_counts.most_common(1)[0]
    template_share = dominant_count / len(templates)
    if template_share > 0.60 and not _nonempty(brief.get("templateRepetitionRationale")):
        findings.append(_finding(
            "visual.template-dominance", "P1",
            "One shot template dominates the plan. Similar templates need explicit variation in framing, action, environment and visual purpose.",
            {"template": dominant_template, "count": dominant_count, "shotCount": len(templates), "share": round(template_share, 4)},
        ))
    elif template_share > 0.60:
        findings.append(_finding(
            "visual.template-dominance-review", "P2",
            "Template reuse is deliberate; independently verify that each use creates a distinct visual beat.",
            {"template": dominant_template, "share": round(template_share, 4)},
        ))

    camera_share = language_complete / len(shots)
    if camera_share < 0.80:
        findings.append(_finding(
            "visual.shot-language-incomplete", "P1",
            "At least 80% of shots must specify framing, angle, camera move, composition and visual purpose before production.",
            {"completeShots": language_complete, "shotCount": len(shots), "coverage": round(camera_share, 4), "missingShotIds": shot_language_missing[:20]},
        ))
    story_share = story_function_complete / len(shots)
    if story_share < 0.90:
        findings.append(_finding(
            "story.shot-function-incomplete", "P1",
            "At least 90% of shots must state what changes for the viewer/story, not only what object is on screen.",
            {"completeShots": story_function_complete, "shotCount": len(shots), "coverage": round(story_share, 4)},
        ))

    if duration > 0:
        arc_errors = _arc_errors(plan.get("musicArc"), duration)
        for message in arc_errors:
            findings.append(_finding("audio.music-arc-invalid", "P1", message))

    if captions_complete < len(shots):
        findings.append(_finding(
            "text.coverage-plan-incomplete", "P1",
            "Each shot needs an explicit subtitle/transcript coverage decision or a reasoned no-text exemption.",
            {"shotsWithText": captions_complete, "shotCount": len(shots)},
        ))

    # Plan-readiness subscores are transparent completeness heuristics, not a
    # subjective artistic rating of the rendered film.
    brief_score = round(20 * brief_present / len(REQUIRED_BRIEF_FIELDS))
    story_score = round(20 * (0.5 * (1 if story_arc_ok else 0) + 0.5 * story_share))
    pacing_score = 15 if not uniform_duration else (6 if _nonempty(brief.get("pacingRationale")) else 2)
    visual_score = round(15 * min(1.0, camera_share) * min(1.0, (1.0 - max(0.0, template_share - 0.35))))
    motion_score = round(10 * (motion_proof_complete / len(contact_actions))) if contact_actions else 5
    audio_score = 10 if _nonempty(policy) and not _arc_errors(plan.get("musicArc"), duration) else 3
    text_score = round(10 * captions_complete / len(shots))
    breakdown = {
        "brief": brief_score,
        "story": story_score,
        "pacing": pacing_score,
        "visualLanguage": visual_score,
        "motionPlan": motion_score,
        "audioPlan": audio_score,
        "textPlan": text_score,
    }
    score = sum(breakdown.values())

    p0 = sum(1 for f in findings if f["severity"] == "P0")
    p1 = sum(1 for f in findings if f["severity"] == "P1")
    p2 = sum(1 for f in findings if f["severity"] == "P2")
    blocked = p0 > 0 or p1 > 0 or score < 75
    return {
        "schemaVersion": 1,
        "status": "BLOCKED" if blocked else "PLAN_READY_FOR_RENDER",
        "recommendation": "REVISE_PLAN" if blocked else "PROCEED_TO_BLOCKING_AND_PREVIEW",
        "planReadinessScore": score,
        "scoreBreakdown": breakdown,
        "severityCounts": {"P0": p0, "P1": p1, "P2": p2},
        "metrics": {
            "shotCount": len(shots),
            "durationSeconds": duration,
            "shotDurationMeanSeconds": round(mean_duration, 3),
            "shotDurationCoefficientOfVariation": round(duration_cv, 4),
            "distinctShotDurations": distinct_durations,
            "uniformDurationGrid": uniform_duration,
            "templateCounts": dict(template_counts),
            "dominantTemplate": dominant_template,
            "dominantTemplateShare": round(template_share, 4),
            "uniqueSettings": len(set(settings)),
            "uniquePoses": len(set(poses)),
            "cameraLanguageCoverage": round(camera_share, 4),
            "storyFunctionCoverage": round(story_share, 4),
            "motionProofCoverage": round(motion_proof_complete / len(contact_actions), 4) if contact_actions else None,
            "captionPlanCoverage": round(captions_complete / len(shots), 4),
            "maximumEstimatedReadingSpeedWpm": round(reading_speed_max, 1),
        },
        "findings": findings,
        "limitations": [
            "This is an editorial-plan preflight; it does not watch the rendered video or listen to its final mix.",
            "A plan-ready result only authorizes a blocking/animatic preview, never a production release.",
            "Final approval still requires full moving-picture and audio review, caption verification, and resolved P0/P1 defects.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to the shot-plan JSON")
    parser.add_argument("--output", type=Path, help="Write a JSON preflight report")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when the plan is blocked")
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        report = evaluate_plan(plan)
    except Exception as exc:
        parser.exit(2, f"Editorial preflight could not evaluate plan: {exc}\n")

    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 1 if args.strict and report["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
