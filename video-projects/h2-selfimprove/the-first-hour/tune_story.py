#!/usr/bin/env python3
"""Project-specific art-direction pass for THE FIRST HOUR.

The generic 01-PHIM parser supplies a starting point. This pass makes the
critical actions, camera blocking, and character-to-set contact explicit.
It is intentionally idempotent and fails loudly when the storyboard schema
changes, so it cannot silently ship a half-patched film.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

if len(sys.argv) != 2:
    raise SystemExit("usage: tune_story.py path/to/story/shots.json")

path = Path(sys.argv[1])
story = json.loads(path.read_text(encoding="utf-8"))
shots = story.get("shots")
if not isinstance(shots, list) or len(shots) != 29:
    raise SystemExit(f"Expected 29 shots, found {len(shots) if isinstance(shots, list) else 'invalid'}")

by_id = {s.get("id", "").lower(): s for s in shots}
required = {f"b{i:02d}" for i in range(1, 30)}
if set(by_id) != required:
    raise SystemExit("Shot IDs drifted: " + ", ".join(sorted(set(by_id) ^ required)))


def get(shot_id: str) -> dict[str, Any]:
    return by_id[shot_id]


def args_for(shot_id: str) -> dict[str, Any]:
    shot = get(shot_id)
    shot.setdefault("args", {})
    return shot["args"]


def actor(
    who: str,
    x: Any,
    pose: str,
    face: str = "neutral",
    **extra: Any,
) -> dict[str, Any]:
    return {"who": who, "x": x, "pose": pose, "face": face, **extra}


def camera(x: float, y: float, z0: float, z1: float, dur: float = 5.4) -> dict[str, Any]:
    return {"from": [x, y, z0], "to": [x, y, z1], "at": 0.25, "dur": dur}


# B15 — stop two lines colliding on the same center point.
a = args_for("b15")
a["texts"] = [
    {"kind": "narr", "t": "He finally saw the cost.", "at": 0.35, "dur": 2.0, "x": 0.5, "y": 0.34, "size": 66, "maxW": 0.82},
    {"kind": "big", "t": "He had been absent from his own life.", "at": 2.55, "dur": 3.0, "x": 0.5, "y": 0.56, "size": 78, "maxW": 0.90},
]

# B16 — this is the physical reset before the message, so its caption must
# match the action on screen (the message itself is shown on the next insert).
s = get("b16")
s["tpl"] = "scene"
a = args_for("b16")
a["texts"] = [{"kind":"narr","t":"For once, he sat up and looked toward the light.","at":0.35,"dur":5.3,"size":55,"maxW":0.82}]
a.pop("bed", None)
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.17, "bedW": 0.29, "windowX": 0.42,
        "deskX": 0.74, "calendar": False, "clock": False, "lamp": False,
    },
    "actors": [actor("hero", "bed.sit", "sit", "neutral", facing=1, look=-0.2)],
    "cam": camera(0.45, 0.50, 1.0, 1.07),
})

# B18 — a visible turning point: he faces the sunrise and lowers his attention
# from the screen, instead of being rendered holding a phone.
s = get("b18")
s["tpl"] = "scene"
a = args_for("b18")
a.pop("bed", None)
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.15, "bedW": 0.29, "windowX": 0.48,
        "deskX": 0.72, "laptop": True, "calendar": False, "clock": False, "lamp": True,
    },
    "actors": [actor("hero", 0.64, "open", "determined", facing=-1, at=0.15,
                     walk={"to":0.43,"at":0.25,"dur":2.8,"speed":0.72})],
    "cam": camera(0.52, 0.50, 1.0, 1.20),
})

# B19 — show the movement toward the desk, not a second generic notebook insert.
s = get("b19")
s["tpl"] = "scene"
a = args_for("b19")
a.pop("bed", None)
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.13, "bedW": 0.28, "windowX": 0.35,
        "deskX": 0.70, "laptop": True, "lamp": True, "calendar": False, "clock": False,
    },
    "actors": [
        actor("hero", 0.34, "relaxed", "determined", facing=1,
              walk={"to": "desk.seat", "at": 0.35, "dur": 3.7, "speed": 0.75})
    ],
    "cam": camera(0.55, 0.61, 1.0, 1.08),
})

# B20 — make the written action the visual narration; remove the tiny
# redundant subtitle so the page, lettering, and moving hand own the frame.
s = get("b20")
s["tpl"] = "note"
a = args_for("b20")
a.update({
    "text": "ONE TASK.\nTEN MINUTES.",
    "at": 0.45,
    "cps": 7.5,
    "x": 0.5,
    "y": 0.50,
    "s": 0.96,
    "cam": camera(0.5, 0.51, 1.0, 1.08),
    "texts": [],
})

# B21 — recompose the work shot around the visible desk and laptop, with a slow
# deliberate push rather than a repeated static bedroom-wide.
a = args_for("b21")
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.13, "bedW": 0.28, "windowX": 0.34,
        "deskX": 0.70, "laptop": True, "lamp": True, "calendar": False, "clock": False,
    },
    "actors": [actor("hero", "desk.seat", "sitdesk", "determined", facing=1, look=0.15)],
    # A tighter desk-side shot removes empty bedroom space and makes the
    # laptop/work posture carry the beat.
    "cam": camera(0.66, 0.63, 1.0, 1.48),
})

# B22 — the temptation interrupts with a small visible camera tremor.
a = args_for("b22")
a["cam"] = camera(0.50, 0.52, 1.0, 1.08, 4.9)
a["shake"] = [{"at": 1.0, "amt": 1.5, "dur": 0.65}, {"at": 3.3, "amt": 1.0, "dur": 0.5}]

# B23 — correct the blocking: his hands return to the laptop; the shadow retreats
# toward frame edge and fades instead of standing beside a phone-holding hero.
a = args_for("b23")
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.13, "bedW": 0.28, "windowX": 0.34,
        "deskX": 0.70, "laptop": True, "lamp": True, "calendar": False, "clock": False,
    },
    "actors": [
        actor("hero", "desk.seat", "sitdesk", "determined", facing=1, look=0.15),
        actor("voice", 0.91, "reach", "grin", facing=-1, at=0.35, scale=0.58, out=3.0, fade=1.25),
    ],
    "cam": camera(0.66, 0.63, 1.0, 1.42),
})

# B25 — use the native punching-bag pose and oscillating bag, rather than a
# generic standing figure next to exercise equipment.
a = args_for("b25")
a.update({
    "set": "gym",
    "setArgs": {"bag": True, "bagX": 0.53, "swing": 0.17, "spot": 0.48, "barbell": False},
    "actors": [actor("band", 0.42, "punch", "determined", facing=1, scale=0.92)],
    "cam": camera(0.50, 0.60, 1.0, 1.08),
    "fx": [{"kind": "speed", "at": 0.65, "dur": 4.8, "x": 0.54, "y": 0.55, "color": "#e2a34a", "dir": -1}],
})

# B26 — enforce real café staging: two seated characters facing each other
# across the café table, with the window, hanging lamp, and rain animation behind.
s = get("b26")
s["tpl"] = "scene"
a = args_for("b26")
a.update({
    "set": "cafe",
    "setArgs": {"lampX": 0.50},
    "actors": [
        actor("hero", "table.left", "sit", "smile", facing=1, scale=0.88),
        actor("friend", "table.right", "sit", "smile", facing=-1, scale=0.88, at=0.18),
    ],
    "cam": camera(0.50, 0.55, 1.0, 1.07),
})

# B27 — split the returned temptation into three readable beats and reduce the
# shadow's scale so the audience can see the character is no longer dominated.
a = args_for("b27")
a.update({
    "set": "bedroom",
    "setArgs": {
        "sky": "dawn", "bedX": 0.13, "bedW": 0.28, "windowX": 0.34,
        "deskX": 0.70, "laptop": True, "lamp": True, "calendar": False, "clock": False,
    },
    "actors": [
        actor("hero", "desk.seat", "sitdesk", "determined", facing=1, look=0.15),
        actor("voice", 0.91, "reach", "grin", facing=-1, at=0.2, scale=0.42, out=5.2, fade=0.55),
    ],
    "cam": camera(0.66, 0.62, 1.0, 1.38, 7.35),
    "texts": [
        {"kind": "narr", "t": "The voice returned.", "at": 0.35, "dur": 2.05, "x": 0.12, "y": 0.30, "size": 44, "maxW": 0.22},
        {"kind": "tempt", "t": "just one more scroll.", "at": 2.60, "dur": 1.95, "x": 0.80, "y": 0.31, "size": 46},
        {"kind": "narr", "t": "But it sounded smaller now.", "at": 4.80, "dur": 2.80, "x": 0.12, "y": 0.30, "size": 44, "maxW": 0.22},
    ],
})

# Caption-safe-area and read-time regression guard for the encoded 2.39:1 picture.
for shot in shots:
    duration = float(shot["end"]) - float(shot["start"])
    for tx in shot.get("args", {}).get("texts", []):
        kind = tx.get("kind")
        if kind in ("narr", "big") and tx.get("y") is not None:
            text_y = float(tx["y"])
            assert 0.16 <= text_y <= 0.84, (
                f"Caption falls in/too close to cinematic bars: {shot['id']} / {tx.get('t')!r} at y={text_y}"
            )
        if kind in ("narr", "big", "tempt") and tx.get("t"):
            at = float(tx.get("at", 0.3))
            dur = float(tx.get("dur", duration - at - 0.1))
            assert dur > 0 and at + dur <= duration + 0.02, (
                f"Caption timing exceeds shot: {shot['id']} / {tx.get('t')!r}"
            )
# The returning-voice beat must have enough time to read all three captions.
b27_text = {tx.get("t"): tx for tx in get("b27").get("args", {}).get("texts", [])}
assert b27_text["The voice returned."]["dur"] >= 2.0
assert b27_text["just one more scroll."]["dur"] >= 1.8
assert b27_text["But it sounded smaller now."]["dur"] >= 2.7
assert abs(float(get("b27")["end"]) - float(get("b27")["start"]) - 8.0) < 0.02
assert by_id["b27"]["args"]["texts"][0]["x"] <= 0.25 and by_id["b27"]["args"]["texts"][2]["x"] <= 0.25
assert by_id["b27"]["args"]["texts"][0]["maxW"] <= 0.23 and by_id["b27"]["args"]["texts"][2]["maxW"] <= 0.23
story["duration"] = float(shots[-1]["end"])
path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Art direction applied: {len(shots)} shots; duration={story['duration']}s")
for shot_id in ("b15", "b16", "b18", "b19", "b20", "b21", "b22", "b23", "b25", "b26", "b27"):
    s = get(shot_id)
    print(f"  {shot_id}: {s['tpl']} / {s['start']:.1f}-{s['end']:.1f}s / {s.get('scene','')[:60]}")
