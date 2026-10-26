#!/usr/bin/env python3
"""Idempotent, schema-checked art-direction pass for THE WEIGHT OF YES."""
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
expected = {f"b{i:02d}" for i in range(1, 30)}
if set(by_id) != expected:
    raise SystemExit("Shot IDs drifted: " + ", ".join(sorted(set(by_id) ^ expected)))

DURATIONS = [4.0] + [5.0] * 27 + [4.0]
cursor = 0.0
for shot, duration in zip(shots, DURATIONS, strict=True):
    shot["start"] = round(cursor, 3)
    cursor += duration
    shot["end"] = round(cursor, 3)
story["duration"] = cursor
assert abs(cursor - 143.0) < 0.01

def cap(kind: str, text: str, at: float = 0.32, dur: float = 4.25,
        x: float = 0.5, y: float = 0.105, size: int = 53,
        max_w: float = 0.84, **extra: Any) -> dict[str, Any]:
    return {"kind": kind, "t": text, "at": at, "dur": dur,
            "x": x, "y": y, "size": size, "maxW": max_w, **extra}

def narr(text: str, at: float = 0.32, dur: float = 4.25, **extra: Any) -> dict[str, Any]:
    return cap("narr", text, at, dur, **extra)

def actor(who: str, x: Any, pose: str = "stand", face: str = "neutral", **extra: Any) -> dict[str, Any]:
    return {"who": who, "x": x, "pose": pose, "face": face, **extra}

def cam(x: float, y: float, z1: float = 1.08, dur: float = 4.35) -> dict[str, Any]:
    return {"from": [x, y, 1.0], "to": [x, y, z1], "at": 0.22, "dur": dur}

def room(sky: str = "night", **extra: Any) -> dict[str, Any]:
    return {"sky": sky, "stage": True, "bedX": 0.12, "bedW": 0.25,
            "windowX": 0.42, "deskX": 0.72, "laptop": True,
            "lamp": True, "calendar": False, "clock": False, **extra}

def classroom(sky: str = "day", **extra: Any) -> dict[str, Any]:
    return {"sky": sky, "stage": True, "board": "TEAM WORK",
            "desks": [0.20, 0.46, 0.72], **extra}

def apply(sid: str, tpl: str, args: dict[str, Any],
          transition: dict[str, Any] | None = None) -> None:
    s = by_id[sid]
    s["tpl"] = tpl
    s["args"] = args
    s["in"] = transition if transition is not None else {"type": "cut"}

# B01 — one precise, emotionally legible hook. No busy intro animation.
apply("b01", "black", {
    "dust": True, "line": False,
    "texts": [cap("big", "He was everyone's first call.", 0.20, 3.35,
                  y=0.47, size=86, max_w=0.88)]
})

# B02 — a domestic opening, with the hero already looking depleted.
apply("b02", "scene", {
    "set": "kitchen",
    "setArgs": {"sky": "dawn", "stage": True, "tableX": 0.61, "lamp": False},
    "actors": [actor("hero", 0.50, "stand", "tired", facing=1, scale=0.98)],
    "cam": cam(0.50, 0.55, 1.08),
    "texts": [narr("Before his own day began, someone else needed him.", size=49)]
})

# B03 — a request lands in physical space; he accepts before thinking.
apply("b03", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.43, "reach", "smile", facing=-1, scale=0.98),
        actor("friend", 0.69, "reach", "neutral", facing=-1, scale=0.91, hold="book")
    ],
    "cam": cam(0.53, 0.56, 1.10),
    "texts": [narr("“Could you cover this?”", size=56)]
})

# B04 — second favor; keep both eye-lines and the handoff readable.
apply("b04", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.36, "carry", "neutral", facing=1, scale=0.96),
        actor("girl", 0.70, "reach", "smile", facing=-1, scale=0.90),
        actor("friend2", 0.87, "point", "neutral", facing=-1, scale=0.70)
    ],
    "cam": cam(0.54, 0.56, 1.06),
    "texts": [narr("“Can you fix our part, too?”", size=53)]
})

# B05 — favors accumulate, but the hero's own board remains empty.
apply("b05", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.5, "y": 0.50,
    "w": 0.80, "h": 0.68, "subject": "TASK BOARD",
    "sender": "TEAM", "body": "6 favors accepted. Personal project: NOT STARTED.",
    "hud": {"rows": [{"label": "FAVORS", "n": 6}, {"label": "HIS WORK", "n": 0}]},
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("His own task list sat untouched.", size=54)]
})

# B06 — the pressure is social and face-to-face, not endless scrolling.
apply("b06", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.47, "carry", "worried", facing=1, scale=1.00),
        actor("friend", 0.19, "reach", "neutral", facing=1, scale=0.76),
        actor("girl", 0.79, "reach", "smile", facing=-1, scale=0.79)
    ],
    "hud": {"rows": [{"label": "REQUESTS", "n": 3}]},
    "cam": cam(0.50, 0.57, 1.12),
    "texts": [narr("One more message. One more favor.", size=55)]
})

# B07 — "YES" becomes a repeated, deliberate visual motif.
apply("b07", "note", {
    "text": "YES.", "at": 0.35, "cps": 5.2, "x": 0.5, "y": 0.51, "s": 1.10,
    "cam": cam(0.5, 0.52, 1.12),
    "hud": {"rows": [{"label": "FAVORS", "n": 7}, {"label": "HIS TIME", "n": 0}]},
    "texts": [narr("He answered before checking his own plans.", size=48)]
})

# B08 — everyone else leaves with the task done; he stays at the desk.
apply("b08", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", "desk.seat", "sitdesk", "tired", facing=1, scale=1.00),
        actor("friend2", 0.81, "reach", "smile", facing=-1, scale=0.82)
    ],
    "cam": cam(0.58, 0.60, 1.11),
    "texts": [narr("They went home lighter.", size=56)]
})

# B09 — the burden follows him into ordinary public space.
apply("b09", "scene", {
    "set": "city", "setArgs": {"sky": "dusk", "stage": True},
    "actors": [
        actor("hero", 0.48, "carry", "tired", facing=1, scale=1.03),
        actor("friend", 0.79, "open", "smile", facing=1, scale=0.75)
    ],
    "cam": cam(0.52, 0.56, 1.10),
    "texts": [narr("He carried every promise like it was small.", size=50)]
})

# B10 — a visible cost: he sits alone after the others have gone.
apply("b10", "scene", {
    "set": "cafe", "setArgs": {"sky": "night", "stage": True},
    "actors": [actor("hero", 0.50, "sit", "sad", facing=1, scale=0.98)],
    "cam": cam(0.50, 0.56, 1.10),
    "texts": [narr("He ate after everyone else left.", size=56)]
})

# B11 — his own deadline finally enters frame as a concrete consequence.
apply("b11", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.5, "y": 0.50,
    "w": 0.81, "h": 0.68, "subject": "PERSONAL PROJECT",
    "sender": "Submission Portal", "body": "Due tonight at 11:59 PM. Progress: 0%.",
    "hud": {"rows": [{"label": "FAVORS", "n": 9}, {"label": "HIS WORK", "n": 0}]},
    "cam": cam(0.5, 0.5, 1.10),
    "texts": [narr("His own deadline kept getting moved.", size=51)]
})

# B12 — the polite smile fails to hide the exhaustion.
apply("b12", "face", {
    "who": "hero", "face": "tired",
    "faceAt": [[0.0, "smile"], [2.15, "tired"]],
    "look": -0.12, "h": 1.22, "x": 0.5, "y": 0.50,
    "bg": "bedroom", "setArgs": room("night"),
    "cam": cam(0.5, 0.52, 1.08),
    "texts": [narr("He called it being dependable.", size=55)]
})

# B13 — let the friend hold the frame and notice him.
apply("b13", "scene", {
    "set": "cafe", "setArgs": {"sky": "night", "stage": True},
    "actors": [
        actor("hero", 0.35, "sit", "smile", facing=1, scale=0.95),
        actor("girl", 0.70, "sitpoint", "worried", facing=-1, scale=0.93)
    ],
    "cam": cam(0.52, 0.56, 1.08),
    "texts": [narr("When someone asked how he was, he smiled.", size=49)]
})

# B14 — a short, restrained overload beat. No monster and no exaggerated collapse.
apply("b14", "scene", {
    "set": "void", "setArgs": {"spot": 0.53, "gy": 0.81},
    "actors": [actor("hero", 0.49, "slump", "scared", facing=1, scale=1.04)],
    "hud": {"rows": [{"label": "REQUESTS", "n": 9}, {"label": "ENERGY", "n": 1}]},
    "cam": cam(0.50, 0.55, 1.14),
    "texts": [narr("Until his arms could not hold one more thing.", size=48)]
})

# B15 — the key beat is a stop; the film gives it air rather than spectacle.
apply("b15", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.44, "slump", "worried", facing=1, scale=1.04),
        actor("friend", 0.77, "stand", "worried", facing=-1, scale=0.86)
    ],
    "cam": cam(0.53, 0.57, 1.06, 4.45),
    "texts": [narr("For once, he stopped in the middle of yes.", size=49)]
})

# B16 — the friend changes posture to meet him at eye level.
apply("b16", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.39, "kneel", "sad", facing=1, scale=0.98),
        actor("friend", 0.65, "kneel", "worried", facing=-1, scale=0.88)
    ],
    "cam": cam(0.51, 0.61, 1.10),
    "texts": [narr("A friend noticed the silence.", size=56)]
})

# B17 — one last request arrives; show it as readable UI, not a scrolling feed.
apply("b17", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.5, "y": 0.50,
    "w": 0.80, "h": 0.68, "subject": "ONE LAST FAVOR?",
    "sender": "A friend", "body": "Can you cover for me again tonight?",
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("One more request arrived.", size=56)]
})

# B18 — his eyes move from their request to his own unfinished page.
apply("b18", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.43, "stand", "worried", facing=1, scale=1.00, look=-0.08),
        actor("girl", 0.75, "reach", "neutral", facing=-1, scale=0.86)
    ],
    "cam": cam(0.52, 0.56, 1.14),
    "texts": [narr("This time, he let the silence answer first.", size=49)]
})

# B19 — one calm, unmistakable boundary. Leave a clean text lane.
apply("b19", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.43, "arms", "determined", facing=-1, scale=1.00),
        actor("girl", 0.74, "reach", "neutral", facing=-1, scale=0.86)
    ],
    "cam": cam(0.52, 0.56, 1.07),
    "texts": [
        cap("big", "NO.", 0.70, 2.15, x=0.50, y=0.44, size=112, max_w=0.55),
        narr("Not today.", 3.02, 1.45, x=0.50, y=0.67, size=51, max_w=0.70)
    ]
})

# B20 — show the other person's response; no anger, punishment or instant applause.
apply("b20", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.42, "stand", "worried", facing=-1, scale=0.98),
        actor("girl", 0.72, "shrug", "smile", facing=1, scale=0.88)
    ],
    "cam": cam(0.52, 0.57, 1.05),
    "texts": [narr("She paused. Then she nodded.", size=58)]
})

# B21 — another pair of hands takes over, making the boundary practical.
apply("b21", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", "desk.seat", "sitdesk", "relaxed", facing=1, scale=0.96),
        actor("girl", 0.70, "carry", "neutral", facing=1, scale=0.91),
        actor("friend2", 0.86, "reach", "smile", facing=-1, scale=0.75)
    ],
    "cam": cam(0.56, 0.58, 1.10),
    "texts": [narr("The work found another pair of hands.", size=50)]
})

# B22 — visible completion, with a timed SENT confirmation after the click.
apply("b22", "laptop", {
    "bg": "bedroom", "setArgs": room("dawn"), "x": 0.5, "y": 0.50,
    "w": 0.81, "h": 0.68, "subject": "MY PROJECT",
    "sender": "Submission Portal", "body": "Submitted successfully. Thank you.",
    "sentAt": 2.25,
    "hud": {"rows": [{"label": "HIS WORK", "n": 1}, {"label": "FAVORS", "n": 9}]},
    "cam": cam(0.5, 0.5, 1.10),
    "texts": [narr("He kept the promise he had made himself.", size=49)]
})

# B23 — recovery is small and physical: he stands and clears his own space.
apply("b23", "scene", {
    "set": "bedroom",
    "setArgs": room("dawn", door=True, doorOpen=0.28, lamp=False),
    "actors": [
        actor("hero", 0.66, "open", "determined", facing=-1, scale=0.98,
              walk={"to": 0.48, "at": 0.28, "dur": 2.60, "speed": 0.74})
    ],
    "cam": cam(0.55, 0.55, 1.12),
    "texts": [narr("The first space he protected was his own.", size=49)]
})

# B24 — reciprocal care: the friend offers something and listens.
apply("b24", "scene", {
    "set": "cafe", "setArgs": {"sky": "dawn", "stage": True},
    "actors": [
        actor("hero", 0.36, "sit", "smile", facing=1, scale=0.96),
        actor("friend", 0.69, "sitpoint", "smile", facing=-1, scale=0.92)
    ],
    "cam": cam(0.52, 0.57, 1.08),
    "texts": [narr("Care began to move both ways.", size=58)]
})

# B25 — preserve generosity; the lesson is choice, not withdrawal.
apply("b25", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.42, "reach", "smile", facing=-1, scale=0.98),
        actor("girl", 0.70, "reach", "smile", facing=1, scale=0.88)
    ],
    "cam": cam(0.53, 0.57, 1.06),
    "texts": [narr("He still said yes when he meant it.", size=55)]
})

# B26 — a calm decline, followed by continued movement; no apology spiral.
apply("b26", "scene", {
    "set": "city", "setArgs": {"sky": "day", "stage": True},
    "actors": [
        actor("hero", 0.49, "open", "determined", facing=1, scale=0.99,
              walk={"to": 0.69, "at": 0.30, "dur": 2.60, "speed": 0.76}),
        actor("friend2", 0.22, "reach", "neutral", facing=1, scale=0.77)
    ],
    "cam": cam(0.51, 0.56, 1.08),
    "texts": [narr("And no when he had nothing left to give.", size=50)]
})

# B27 — the ledger is rebalanced: his work is done and rest has a place.
apply("b27", "calendar", {
    "month": "DEC", "from": 1, "to": 3, "at": 0.35, "dur": 4.2,
    "mode": "x", "color": "#d79b42", "s": 0.64,
    "hud": {"rows": [
        {"label": "HIS WORK", "n": 1},
        {"label": "FAVORS", "n": 9},
        {"label": "REST", "n": 1}
    ]},
    "cam": cam(0.5, 0.53, 1.08),
    "texts": [narr("His kindness stopped costing him everything.", size=50)]
})

# B28 — a designed end card, separate from the thumbnail treatment.
apply("b28", "card", {
    "word": "THE WEIGHT OF YES",
    "sub": "Kindness needs boundaries.",
    "sub2": "You can care without disappearing.",
    "at": 0.25, "typeDur": 1.35, "size": 0.145,
    "texts": []
}, {"type": "dip", "dur": 0.40})

# B29 — soft, in-world CTA; do not simulate fake platform controls.
apply("b29", "scene", {
    "set": "bedroom",
    "setArgs": room("dawn", door=True, doorOpen=0.7, lamp=False),
    "actors": [actor("hero", 0.53, "wave", "smile", facing=1, scale=0.94)],
    "cam": cam(0.52, 0.55, 1.04, 3.50),
    "texts": [narr("If this hit, like and subscribe.", 0.28, 3.45, size=48)]
})

# Strict storyboard gates: IDs, time, captions, visual turning point and payoff.
previous_end = 0.0
for shot in shots:
    start, end = float(shot["start"]), float(shot["end"])
    assert abs(start - previous_end) < 0.01, f"Gap/overlap before {shot['id']}"
    assert end > start, f"Invalid shot duration: {shot['id']}"
    duration = end - start
    for tx in shot.get("args", {}).get("texts", []):
        at = float(tx.get("at", 0.3))
        dur = float(tx.get("dur", duration - at - 0.1))
        assert at >= 0 and dur > 0 and at + dur <= duration + 0.02, (
            f"Caption outside shot: {shot['id']} / {tx.get('t')!r}"
        )
    previous_end = end

assert abs(previous_end - 143.0) < 0.02
assert by_id["b01"]["tpl"] == "black"
assert by_id["b05"]["tpl"] == "laptop"
assert by_id["b11"]["tpl"] == "laptop"
assert by_id["b14"]["args"]["set"] == "void"
assert any(t.get("t") == "NO." for t in by_id["b19"]["args"]["texts"])
assert len(by_id["b20"]["args"]["actors"]) == 2
assert by_id["b22"]["args"]["sentAt"] == 2.25
assert by_id["b28"]["tpl"] == "card"
assert by_id["b29"]["tpl"] == "scene"

story["duration"] = 143.0
path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ART-DIRECTION QA PASS: 29 shots, 143.0s, burden/request/overload/boundary/reaction/submit/reciprocity gates passed")
for sid in ("b01", "b03", "b05", "b08", "b10", "b11", "b14", "b15", "b19", "b20", "b21", "b22", "b24", "b26", "b27"):
    s = by_id[sid]
    print(f"  {sid}: {s['tpl']} / {s['start']:.1f}-{s['end']:.1f}s")
