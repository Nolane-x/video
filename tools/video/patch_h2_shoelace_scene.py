#!/usr/bin/env python3
"""Apply the reproducible shoe-tying action fix to an extracted H2 source-v2 tree.

This is intentionally a patch to a temporary extracted source tree. It never edits
the archived source-v2 Release asset or the canonical H2 master MP4.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BEAN = Path("packs/dem/bean.js")
SHOTS = Path("projects/one-more-scroll-h2/story/shots.json")

OLD_ARM = "const arm = (k, ang) => seg2(sx(k), shY, ang[0], 12.5 * U, ang[1], 12 * U, f);"
NEW_ARM = "const arm = (k, ang) => seg2(sx(k), shY, ang[0], 12.5 * U * (p.armScale || 1), ang[1], 12 * U * (p.armScale || 1), f);"
POSE_LINE = "  knees:    { aF: [0.9, 1.8], aB: [0.8, 1.7], lF: [2.3, -0.15], lB: [2.2, -0.2], drop: 26, lean: 0.25, head: [3, 4] },   // ngoi bo goi duoi dat"
TIE_POSE = "  tieShoes: { aF: [-0.18, -0.18], aB: [0.32, 0.4], lF: [2.3, -0.15], lB: [2.2, -0.2], drop: 26, lean: 0.25, head: [3, 4], armScale: 1.42 }, // both hands reach the floor-level shoe laces"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def patch(root: Path) -> dict:
    bean_path = root / BEAN
    shots_path = root / SHOTS
    if not bean_path.is_file() or not shots_path.is_file():
        raise SystemExit(f"Not an extracted H2 source tree: missing {BEAN} or {SHOTS}")

    bean = bean_path.read_text(encoding="utf-8")
    if "tieShoes: {" not in bean:
        if POSE_LINE not in bean:
            raise SystemExit("Expected knees pose declaration not found; refusing an unsafe patch.")
        bean = bean.replace(POSE_LINE, POSE_LINE + "\n" + TIE_POSE, 1)
    if NEW_ARM not in bean:
        if OLD_ARM not in bean:
            raise SystemExit("Expected arm() function not found; refusing an unsafe patch.")
        bean = bean.replace(OLD_ARM, NEW_ARM, 1)
    bean_path.write_text(bean, encoding="utf-8")

    data = json.loads(shots_path.read_text(encoding="utf-8"))
    shot = next((s for s in data.get("shots", []) if s.get("id") == "b17"), None)
    if shot is None:
        raise SystemExit("Expected shot b17 (shoe-tying scene) not found.")
    actor = next((a for a in shot.get("args", {}).get("actors", []) if a.get("who") == "hoodie"), None)
    if actor is None:
        raise SystemExit("Expected hoodie protagonist in shot b17 not found.")
    actor["pose"] = "kneel"
    actor["poseAt"] = [
        [0.0, "kneel"],
        [0.65, "knees"],
        [1.0, "tieShoes"],
        [3.5, "tieShoes"],
        [4.1, "kneel"],
    ]
    # Keep the lace prop at the feet/hands' meeting point and preserve the source-v2 set.
    shot["args"].setdefault("setArgs", {})["shoelace"] = True
    shot["args"]["setArgs"]["shoeX"] = 0.72
    shot["notes"] = (
        "P1 fix: after a short kneeling settle, both hands extend to the floor-level "
        "shoe laces for a sustained tying action. Keep both shoes, hands and feet visible; "
        "verify the contact in the moving preview before a full render."
    )
    shots_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Assertions make the patch idempotent and fail-closed.
    patched_bean = bean_path.read_text(encoding="utf-8")
    patched_shots = json.loads(shots_path.read_text(encoding="utf-8"))
    patched_shot = next(s for s in patched_shots["shots"] if s["id"] == "b17")
    assert "tieShoes: {" in patched_bean and NEW_ARM in patched_bean
    assert [1.0, "tieShoes"] in patched_shot["args"]["actors"][0]["poseAt"]
    return {
        "status": "patch_applied",
        "source_v2_story": "31 shots / 155 seconds",
        "patched_shot_id": "b17",
        "pose": "tieShoes",
        "pose_duration_seconds": 2.5,
        "arms_scale": 1.42,
        "arm_reach": "both arms angled toward the floor-level laces; contact must be checked visually",
        "bean_js_sha256": sha256(bean_path),
        "shots_json_sha256": sha256(shots_path),
        "safety": "does not edit the canonical H2 master or the archived source-v2 ZIP"
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = patch(args.source_root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
