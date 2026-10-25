#!/usr/bin/env python3
"""Validate the data-driven shot plan before a full render.

Run from repo root:
  python tools/video/validate_story.py video-projects/remotion/public/story/shots.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SETTINGS = {
    "bedroom", "phone", "street", "busStop", "classroom", "calendar",
    "bathroom", "mirror", "void", "desk", "kitchen", "stairs", "park",
    "gym", "cafe", "bus", "library", "dawn", "end",
}
POSES = {
    "scroll", "walk", "tired", "slump", "stand", "write", "drink",
    "tie", "punch", "meet", "listen", "hero",
}
SHOT_FIELDS = {"id", "start", "end", "tpl", "line", "emotion", "action", "soundCues", "args"}
ARG_FIELDS = {
    "title", "subtitle", "setting", "pose", "x0", "x1", "y0", "y1",
    "scale", "shirt", "shadow", "shadowX", "zoom0", "zoom1", "pan0", "pan1",
}

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: python tools/video/validate_story.py <shots.json>")
    path = Path(sys.argv[1])
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse JSON {path}: {exc}")
    for key in ("title", "duration", "fps", "shots"):
        if key not in plan:
            fail(f"missing top-level field: {key}")
    duration, fps, shots = plan["duration"], plan["fps"], plan["shots"]
    if not isinstance(duration, (int, float)) or duration <= 0:
        fail("duration must be a positive number")
    if not isinstance(fps, int) or fps <= 0:
        fail("fps must be a positive integer")
    if not isinstance(shots, list) or not shots:
        fail("shots must be a non-empty list")

    errors: list[str] = []
    seen: set[str] = set()
    previous_end = 0.0
    total_frames = round(duration * fps)

    for index, shot in enumerate(shots, 1):
        prefix = f"shot {index}"
        missing = SHOT_FIELDS - set(shot)
        if missing:
            errors.append(f"{prefix} missing fields {sorted(missing)}")
            continue
        shot_id = shot["id"]
        if shot_id in seen:
            errors.append(f"duplicate id {shot_id}")
        seen.add(shot_id)
        start, end = shot["start"], shot["end"]
        if not all(isinstance(v, (int, float)) for v in (start, end)):
            errors.append(f"{shot_id}: start/end must be numeric")
            continue
        if abs(start - previous_end) > 1e-6:
            errors.append(f"{shot_id}: timeline gap/overlap; starts {start}, expected {previous_end}")
        if end <= start:
            errors.append(f"{shot_id}: end must be after start")
        if abs(start * fps - round(start * fps)) > 1e-6 or abs(end * fps - round(end * fps)) > 1e-6:
            errors.append(f"{shot_id}: boundaries must align to frames")
        if not shot["action"].strip():
            errors.append(f"{shot_id}: action is empty")
        if not isinstance(shot["soundCues"], list):
            errors.append(f"{shot_id}: soundCues must be a list")
        args = shot["args"]
        missing_args = ARG_FIELDS - set(args)
        if missing_args:
            errors.append(f"{shot_id}: args missing {sorted(missing_args)}")
        else:
            if args["setting"] not in SETTINGS:
                errors.append(f"{shot_id}: unsupported setting {args['setting']!r}")
            if args["pose"] not in POSES:
                errors.append(f"{shot_id}: unsupported pose {args['pose']!r}")
            if args["title"] != shot["args"].get("title"):
                errors.append(f"{shot_id}: title field mismatch")
            if not (0 < args["scale"] <= 3):
                errors.append(f"{shot_id}: scale outside (0, 3]")
            if args["zoom0"] <= 0 or args["zoom1"] <= 0:
                errors.append(f"{shot_id}: camera zoom must be positive")
        previous_end = end

    if abs(previous_end - duration) > 1e-6:
        errors.append(f"timeline ends at {previous_end}s, but plan says {duration}s")
    if round(previous_end * fps) != total_frames:
        errors.append("total frame count does not match duration × FPS")

    if errors:
        print("\n".join(f"- {e}" for e in errors), file=sys.stderr)
        raise SystemExit(1)

    print(f"PASS: {len(shots)} shots; {duration:.3f}s; {fps} fps; {total_frames} frames.")
    print("Note: schema/time validation is not visual QA. Render contact sheets and motion proofs.")

if __name__ == "__main__":
    main()
