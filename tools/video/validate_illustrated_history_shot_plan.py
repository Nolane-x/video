#!/usr/bin/env python3
"""Validate an illustrated-history shot plan and report motion/audio diversity gates."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

CHANNELS = {"actor", "prop", "environment", "camera", "graphics"}
PHYSICAL_ACTIONS = {"draw", "aim", "release", "impact", "block", "parry", "fall", "board", "row", "other_physical"}
CONTACT_ACTIONS = {"walk", "march", "run"}
FULL_ACTION_PHASES = {"anticipation", "action", "contact", "reaction", "follow_through", "recovery"}
REDISTRIBUTABLE = {"public_cc0_pd", "cc_by_4_attribution_required"}


def validate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    project = plan.get("project") or {}
    shots = plan.get("shots") or []

    if plan.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if project.get("style") != "illustrated_history":
        errors.append("project.style must be illustrated_history")
    try:
        fps = float(project.get("fps", 0))
        if fps <= 0:
            errors.append("project.fps must be greater than zero")
    except (TypeError, ValueError):
        fps = 0
        errors.append("project.fps must be numeric and greater than zero")
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty array")
        shots = []

    seen_ids: set[str] = set()
    scales: set[str] = set()
    angles: set[str] = set()
    locations: set[str] = set()
    channels_seen: set[str] = set()
    action_types: set[str] = set()
    consecutive_keys: Counter[str] = Counter()
    previous_key: str | None = None
    seconds_total = 0.0
    cue_count = 0
    unauditioned_count = 0

    for index, shot in enumerate(shots):
        prefix = f"shots[{index}]"
        shot_id = str(shot.get("shot_id") or "")
        if not shot_id:
            errors.append(f"{prefix}.shot_id is required")
        elif shot_id in seen_ids:
            errors.append(f"{prefix}.shot_id duplicates {shot_id}")
        seen_ids.add(shot_id)

        try:
            start = int(shot.get("start_frame"))
            end = int(shot.get("end_frame"))
            if start < 0 or end <= start:
                errors.append(f"{prefix}: end_frame must be greater than start_frame and start_frame must be non-negative")
            duration = max(0, end - start) / fps if fps > 0 else 0
            seconds_total += duration
        except (TypeError, ValueError):
            errors.append(f"{prefix}: start_frame and end_frame must be integers")
            duration = 0

        for field in ("story_purpose", "location", "scale", "angle", "visual_state_change"):
            if not str(shot.get(field) or "").strip():
                errors.append(f"{prefix}.{field} is required and cannot be blank")
        if shot.get("scale"):
            scales.add(str(shot["scale"]))
        if shot.get("angle"):
            angles.add(str(shot["angle"]))
        if shot.get("location"):
            locations.add(str(shot["location"]))

        camera = shot.get("camera") or {}
        if not camera.get("move"):
            errors.append(f"{prefix}.camera.move is required")
        if len(str(camera.get("motivation") or "").strip()) < 8:
            errors.append(f"{prefix}.camera.motivation must explain why the move is used")

        channels = set(shot.get("motion_channels") or [])
        unknown = channels - CHANNELS
        if unknown:
            errors.append(f"{prefix}.motion_channels has unknown values: {sorted(unknown)}")
        channels_seen |= channels
        if shot.get("motion_led") and len(channels) < 2:
            errors.append(f"{prefix}: a motion-led shot needs at least two independent channels")
        if not shot.get("motion_led") and not str(shot.get("visual_state_change") or "").strip():
            errors.append(f"{prefix}: intentional holds must state their visual purpose")

        action = str(shot.get("action_type") or "none")
        if action != "none":
            action_types.add(action)
        phases = set(shot.get("action_phases") or [])
        required_phases: set[str] = set()
        if action in PHYSICAL_ACTIONS:
            required_phases = FULL_ACTION_PHASES
        elif action in CONTACT_ACTIONS:
            required_phases = {"action", "contact"}
        missing_phases = required_phases - phases
        if missing_phases:
            errors.append(f"{prefix}: {action} action is missing phases {sorted(missing_phases)}")

        key = str(shot.get("composition_key") or shot.get("template_id") or "")
        if key:
            if key == previous_key:
                consecutive_keys[key] += 1
            else:
                previous_key = key
                consecutive_keys[key] = 1
            if consecutive_keys[key] >= 3:
                errors.append(f"{prefix}: composition/template {key!r} repeats three or more shots consecutively")
        else:
            previous_key = None

        for asset_index, asset in enumerate(shot.get("asset_sources") or []):
            asset_prefix = f"{prefix}.asset_sources[{asset_index}]"
            for field in ("asset_id", "source_url", "license", "rights_class"):
                if not str(asset.get(field) or "").strip():
                    errors.append(f"{asset_prefix}.{field} is required")
            if asset.get("rights_class") not in {
                "public_cc0_pd", "cc_by_4_attribution_required", "project_use_only", "private_production_only"
            }:
                errors.append(f"{asset_prefix}.rights_class is not recognized")

        for cue_index, cue in enumerate(shot.get("audio_cues") or []):
            cue_count += 1
            cue_prefix = f"{prefix}.audio_cues[{cue_index}]"
            for field in ("cue_id", "track", "sync_event", "rights_class", "audition_status"):
                if not str(cue.get(field) or "").strip():
                    errors.append(f"{cue_prefix}.{field} is required")
            if cue.get("audition_status") == "not_auditioned":
                unauditioned_count += 1
                if cue.get("approved_for_final_mix") is True:
                    errors.append(f"{cue_prefix}: an unauditioned cue cannot be approved for final mix")
            if cue.get("rights_class") not in {
                "public_cc0_pd", "cc_by_4_attribution_required", "project_use_only", "private_production_only"
            }:
                errors.append(f"{cue_prefix}.rights_class is not recognized")
            if cue.get("approved_for_final_mix") is True and not cue.get("asset_id") and not cue.get("source_file"):
                errors.append(f"{cue_prefix}: approved cue needs asset_id or source_file")

    sample_target = project.get("sample_duration_seconds")
    is_short_sample = isinstance(sample_target, (int, float)) and 30 <= sample_target <= 60
    if is_short_sample:
        if len(scales) < 5:
            warnings.append(f"sample target 30-60s: only {len(scales)} distinct shot scales; aim for at least 5")
        if len(angles) < 5:
            warnings.append(f"sample target 30-60s: only {len(angles)} camera angles; aim for at least 5")
        if len(locations) < 3:
            warnings.append(f"sample target 30-60s: only {len(locations)} locations/states; aim for at least 3")
        if len(action_types) < 3:
            warnings.append(f"sample target 30-60s: only {len(action_types)} action types; aim for at least 3")
        if len(channels_seen) < 3:
            warnings.append("sample target 30-60s: demonstrate at least 3 independent motion channels across the edit")

    if seconds_total > 0:
        for index, shot in enumerate(shots):
            try:
                duration = (int(shot["end_frame"]) - int(shot["start_frame"])) / fps
            except (KeyError, TypeError, ValueError, ZeroDivisionError):
                continue
            if duration > 6 and not str(shot.get("visual_state_change") or "").strip():
                warnings.append(f"shots[{index}] holds longer than 6 seconds without describing internal progression")

    summary = {
        "shot_count": len(shots),
        "duration_seconds": round(seconds_total, 3),
        "distinct_scales": len(scales),
        "distinct_angles": len(angles),
        "distinct_locations": len(locations),
        "action_types": sorted(action_types),
        "motion_channels_used": sorted(channels_seen),
        "audio_cues": cue_count,
        "unauditioned_audio_cues": unauditioned_count,
        "errors": len(errors),
        "warnings": len(warnings),
    }
    return {"status": "fail" if errors else "pass_with_warnings" if warnings else "pass", "summary": summary, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to an illustrated-history shot-plan JSON file")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read shot plan: {exc}", file=sys.stderr)
        return 2
    result = validate_plan(plan)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
