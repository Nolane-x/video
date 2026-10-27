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
        x: float = 0.5, y: float = 0.20, size: int = 53,
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
    "texts": [narr("Before his own day began, someone else needed him.", 0.32, 4.25, x=0.26, y=0.29, size=48, max_w=0.30)]
})

# B03 — a request lands in physical space; he accepts before thinking.
apply("b03", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.43, "reach", "smile", facing=-1, scale=0.98),
        actor("friend", 0.69, "reach", "neutral", facing=-1, scale=0.91, hold="portfolio")
    ],
    "cam": cam(0.53, 0.56, 1.10),
    "texts": [narr("“Could you cover this?”", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B04 — second favor; keep both eye-lines and the handoff readable.
apply("b04", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.36, "carry", "neutral", facing=1, scale=0.96, hold="portfolio"),
        actor("girl", 0.70, "reach", "smile", facing=-1, scale=0.90),
        actor("friend2", 0.87, "point", "neutral", facing=-1, scale=0.70)
    ],
    "cam": cam(0.54, 0.56, 1.06),
    "texts": [narr("“Can you fix our part, too?”", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B05 — favors accumulate, but the hero's own board remains empty.
apply("b05", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.35, "y": 0.50,
    "w": 0.62, "h": 0.68, "subject": "TASK BOARD",
    "sender": "TEAM", "body": "6 favors accepted. Personal project: NOT STARTED.",
    "hud": {"rows": [{"label": "FAVORS", "n": 6}, {"label": "HIS WORK", "n": 0}]},
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("His own task list sat untouched.", 0.35, 4.0, x=0.85, y=0.49, size=48, max_w=0.26)]
})

# B06 — the pressure is social and face-to-face, not endless scrolling.
apply("b06", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.47, "carry", "worried", facing=1, scale=1.00, hold="portfolio"),
        actor("friend", 0.19, "reach", "neutral", facing=1, scale=0.76),
        actor("girl", 0.79, "reach", "smile", facing=-1, scale=0.79)
    ],
    "hud": {"rows": [{"label": "REQUESTS", "n": 3}]},
    "cam": cam(0.50, 0.57, 1.12),
    "texts": [narr("One more message. One more favor.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B07 — "YES" becomes a repeated, deliberate visual motif.
apply("b07", "note", {
    "text": "YES.", "at": 0.35, "cps": 5.2, "x": 0.5, "y": 0.51, "s": 1.10,
    "cam": cam(0.5, 0.52, 1.12),
    "hud": {"rows": [{"label": "FAVORS", "n": 7}, {"label": "HIS TIME", "n": 0}]},
    "texts": [narr("He answered before checking his own plans.", 0.32, 4.25, x=0.76, y=0.67, size=48, max_w=0.26, color="#302a24")]
})

# B08 — the hero remains grounded and visibly exhausted as the other helper carries the portfolio away.
apply("b08", "scene", {
    "set": "classroom", "setArgs": classroom("dusk", desks=[0.46]),
    "actors": [
        actor("hero", 0.49, "slump", "tired", facing=1, scale=1.00),
        actor("friend2", 0.70, "carry", "smile", facing=1, scale=0.82, hold="portfolio",
              walk={"to": 0.86, "at": 0.55, "dur": 2.85, "speed": 0.70})
    ],
    "cam": cam(0.56, 0.59, 1.05),
    "texts": [narr("They went home lighter.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B09 — the burden follows him into ordinary public space.
apply("b09", "scene", {
    "set": "city", "setArgs": {"sky": "dusk", "stage": True},
    "actors": [
        actor("hero", 0.48, "carry", "tired", facing=1, scale=1.03, hold="portfolio"),
        actor("friend", 0.79, "open", "smile", facing=1, scale=0.75)
    ],
    "cam": cam(0.52, 0.56, 1.10),
    "texts": [narr("He carried every promise like it was small.", size=50)]
})

# B10 — a visible cost: he sits alone after the others have gone.
apply("b10", "scene", {
    "set": "cafe", "setArgs": {"lampX": 0.50, "tableW": 0.28},
    "actors": [actor("hero", "table.left", "sit", "sad", facing=1, scale=0.88)],
    "cam": cam(0.50, 0.56, 1.10),
    "texts": [narr("He ate after everyone else left.", 0.32, 4.25, x=0.89, y=0.29, size=48, max_w=0.20)]
})

# B11 — his own deadline finally enters frame as a concrete consequence.
apply("b11", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.35, "y": 0.50,
    "w": 0.62, "h": 0.68, "subject": "PERSONAL PROJECT",
    "sender": "Submission Portal", "body": "Due tonight at 11:59 PM. Progress: 0%.",
    "hud": {"rows": [{"label": "FAVORS", "n": 9}, {"label": "HIS WORK", "n": 0}]},
    "cam": cam(0.5, 0.5, 1.10),
    "texts": [narr("His own deadline kept getting moved.", 0.35, 4.0, x=0.85, y=0.49, size=48, max_w=0.26)]
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
        actor("hero", "table.left", "sit", "smile", facing=1, scale=0.88),
        actor("girl", "table.right", "sitpoint", "worried", facing=-1, scale=0.88)
    ],
    "cam": cam(0.52, 0.56, 1.08),
    "texts": [narr("When someone asked how he was, he smiled.", 0.32, 4.25, x=0.89, y=0.29, size=48, max_w=0.20)]
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
    "texts": [narr("For once, he stopped in the middle of yes.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B16 — the friend changes posture to meet him at eye level.
apply("b16", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.39, "kneel", "sad", facing=1, scale=0.98),
        actor("friend", 0.65, "kneel", "worried", facing=-1, scale=0.88)
    ],
    "cam": cam(0.51, 0.61, 1.10),
    "texts": [narr("A friend noticed the silence.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B17 — one last request arrives; show it as readable UI, not a scrolling feed.
apply("b17", "laptop", {
    "bg": "bedroom", "setArgs": room("night"), "x": 0.35, "y": 0.50,
    "w": 0.62, "h": 0.68, "subject": "ONE LAST FAVOR?",
    "sender": "A friend", "body": "Can you cover for me again tonight?",
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("One more request arrived.", 0.35, 4.0, x=0.85, y=0.49, size=48, max_w=0.26)]
})

# B18 — his eyes move from their request to his own unfinished page.
apply("b18", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.43, "stand", "worried", facing=1, scale=1.00, look=-0.08),
        actor("girl", 0.75, "reach", "neutral", facing=-1, scale=0.86)
    ],
    "cam": cam(0.52, 0.56, 1.14),
    "texts": [narr("This time, he let the silence answer first.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B19 — one calm, unmistakable boundary, composed in the upper negative-space lane.
apply("b19", "scene", {
    "set": "classroom", "setArgs": classroom("dusk"),
    "actors": [
        actor("hero", 0.43, "arms", "determined", facing=-1, scale=1.00),
        actor("girl", 0.74, "reach", "neutral", facing=-1, scale=0.86)
    ],
    "cam": cam(0.52, 0.56, 1.07),
    "texts": [
        cap("big", "NO. NOT TODAY.", 0.70, 3.85, x=0.50, y=0.245, size=82, max_w=0.82)
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
    "texts": [narr("She paused. Then she nodded.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B21 — another pair of hands takes over; the hero stays upright and physically grounded.
apply("b21", "scene", {
    "set": "classroom", "setArgs": classroom("day", desks=[0.46]),
    "actors": [
        actor("hero", 0.43, "relaxed", "smile", facing=1, scale=0.96),
        actor("girl", 0.60, "reach", "neutral", facing=-1, scale=0.87),
        actor("friend2", 0.75, "carry", "smile", facing=-1, scale=0.83, hold="portfolio")
    ],
    "cam": cam(0.56, 0.58, 1.10),
    "texts": [narr("The work found another pair of hands.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
})

# B22 — visible completion, with a timed SENT confirmation after the click.
apply("b22", "laptop", {
    "bg": "bedroom", "setArgs": room("dawn"), "x": 0.35, "y": 0.50,
    "w": 0.62, "h": 0.68, "subject": "MY PROJECT",
    "sender": "Submission Portal", "body": "Submitted successfully. Thank you.",
    "sentAt": 2.25,
    "hud": {"rows": [{"label": "HIS WORK", "n": 1}, {"label": "FAVORS", "n": 9}]},
    "cam": cam(0.5, 0.5, 1.10),
    "texts": [narr("He kept the promise he had made himself.", 0.35, 4.0, x=0.85, y=0.49, size=48, max_w=0.26)]
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
    "texts": [narr("The first space he protected was his own.", 0.32, 4.25, x=0.20, y=0.29, size=48, max_w=0.26)]
})

# B24 — reciprocal care: the friend offers something and listens.
apply("b24", "scene", {
    "set": "cafe", "setArgs": {"lampX": 0.50, "tableW": 0.28},
    "actors": [
        actor("hero", "table.left", "sit", "smile", facing=1, scale=0.88),
        actor("friend", "table.right", "sitpoint", "smile", facing=-1, scale=0.88)
    ],
    "cam": cam(0.52, 0.57, 1.08),
    "texts": [narr("Care began to move both ways.", 0.32, 4.25, x=0.89, y=0.29, size=48, max_w=0.20)]
})

# B25 — preserve generosity; the lesson is choice, not withdrawal.
apply("b25", "scene", {
    "set": "classroom", "setArgs": classroom("day"),
    "actors": [
        actor("hero", 0.42, "reach", "smile", facing=-1, scale=0.98),
        actor("girl", 0.70, "reach", "smile", facing=1, scale=0.88)
    ],
    "cam": cam(0.53, 0.57, 1.06),
    "texts": [narr("He still said yes when he meant it.", 0.32, 4.25, x=0.41, y=0.28, size=48, max_w=0.34)]
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
    "mode": "x", "color": "#d79b42", "s": 0.56,
    "hud": {"rows": [
        {"label": "HIS WORK", "n": 1},
        {"label": "FAVORS", "n": 9},
        {"label": "REST", "n": 1}
    ]},
    "cam": cam(0.5, 0.53, 1.08),
    "texts": [
        narr("His kindness stopped costing him everything.", 0.35, 4.2,
             x=0.11, y=0.43, size=48, max_w=0.18)
    ]
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
    "texts": [narr("If this hit, like and subscribe.", 0.28, 3.45, x=0.22, y=0.29, size=50, max_w=0.30)]
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
        if tx.get("kind") in ("narr", "big") and tx.get("y") is not None:
            text_y = float(tx["y"])
            assert 0.16 <= text_y <= 0.84, (
                f"Caption falls in/too close to cinematic bars: {shot['id']} / "
                f"{tx.get('t')!r} at y={text_y}"
            )
    previous_end = end

assert abs(previous_end - 143.0) < 0.02
# Text coverage is a release gate: every shot carries story copy, except the designed card whose own fields are the copy.
for shot in shots:
    sid = shot["id"]
    args = shot.get("args", {})
    if sid == "b28":
        assert args.get("word") and args.get("sub") and args.get("sub2"), "B28 end card must contain all three text lines"
        continue
    captions = args.get("texts", [])
    story_captions = [tx for tx in captions if tx.get("kind", "narr") in ("narr", "big")]
    assert story_captions, f"Missing main narrative line: {sid}"
    for tx in story_captions:
        assert int(tx.get("size", 53)) >= 48, f"Caption too small to read at 1080p: {sid} / {tx.get('t')!r}"
    duration = float(shot["end"]) - float(shot["start"])
    sample_t = duration * 0.75
    active_story = [tx for tx in story_captions if float(tx.get("at", 0.3)) <= sample_t <= float(tx.get("at", 0.3)) + float(tx.get("dur", duration - float(tx.get("at", 0.3)) - 0.1))]
    assert active_story, f"No STORY narration active at 75% contact-sheet sample: {sid}"
    # A technically present caption is still a failure if its fade-out has begun at the review sample.
    tx = active_story[-1]
    at = float(tx.get("at", 0.3))
    fo = float(tx.get("fo", 0.45))
    tx["dur"] = max(float(tx.get("dur", duration - at - 0.1)), sample_t - at + fo + 0.12)
    assert at + float(tx["dur"]) <= duration - 0.05, f"{sid} narration cannot remain fully opaque at 75% without overrunning the shot"
assert by_id["b01"]["tpl"] == "black"
assert by_id["b05"]["tpl"] == "laptop"
assert by_id["b11"]["tpl"] == "laptop"
assert by_id["b14"]["args"]["set"] == "void"
assert any(t.get("t") == "NO. NOT TODAY." and abs(float(t.get("y", 0)) - 0.245) < 0.01 for t in by_id["b19"]["args"]["texts"])
assert by_id["b08"]["args"]["actors"][0]["pose"] == "slump"
assert by_id["b21"]["args"]["actors"][0]["pose"] == "relaxed"
assert all(a.get("pose") != "sitdesk" for a in by_id["b08"]["args"]["actors"] + by_id["b21"]["args"]["actors"])
assert len(by_id["b20"]["args"]["actors"]) == 2
# Only B07 uses the notebook insert; its narration must sit below the handwritten "YES." title.
tx = by_id["b07"]["args"]["texts"][0]
assert by_id["b07"]["tpl"] == "note" and tx["x"] >= 0.72 and tx["y"] >= 0.63 and tx["maxW"] <= 0.27 and tx.get("size", 53) >= 46 and tx.get("color") == "#302a24", "B07 narration must be dark, large and on the blank lower-right page"
classroom_lane = ("b03", "b04", "b06", "b08", "b15", "b16", "b18", "b20", "b21", "b25")
for sid in classroom_lane:
    tx = by_id[sid]["args"]["texts"][0]
    assert 0.38 <= tx["x"] <= 0.44 and 0.25 <= tx["y"] <= 0.31 and tx["maxW"] <= 0.35 and tx.get("size", 53) >= 46, (
        f"{sid} narration must be readable and stay in the upper classroom text lane"
    )
for sid in ("b10", "b13", "b24"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] >= 0.88 and 0.25 <= tx["y"] <= 0.33 and tx["maxW"] <= 0.21 and tx.get("size", 53) >= 46, (
        f"{sid} café narration must be large and stay in the clear right-side lane outside the window"
    )
for sid in ("b02", "b23"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] <= 0.30 and tx["maxW"] <= 0.32 and 0.25 <= tx["y"] <= 0.32 and tx.get("size", 53) >= 46, (
        f"{sid} opening/recovery narration must be large and remain left of the window/character"
    )
tx = by_id["b29"]["args"]["texts"][0]
assert tx["x"] <= 0.25 and tx["maxW"] <= 0.31 and 0.25 <= tx["y"] <= 0.33, "B29 CTA must stay left of the window"
for sid in ("b05", "b11", "b17", "b22"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] >= 0.84 and 0.40 <= tx["y"] <= 0.60 and tx["maxW"] <= 0.27 and tx.get("size", 53) >= 46, (
        f"{sid} laptop narration must be large and outside the resized laptop screen"
    )
    assert by_id[sid]["args"]["x"] <= 0.36 and by_id[sid]["args"]["w"] <= 0.63, f"{sid} laptop must leave a clean caption lane on the right"
    shot_duration = float(by_id[sid]["end"]) - float(by_id[sid]["start"])
    assert float(tx["at"]) + float(tx["dur"]) <= shot_duration + 0.02, f"{sid} narration overflows its shot"
assert by_id["b22"]["args"]["sentAt"] == 2.25
b27_caption = by_id["b27"]["args"]["texts"][0]
assert by_id["b27"]["tpl"] == "calendar"
assert by_id["b27"]["args"]["s"] <= 0.56 and b27_caption["x"] <= 0.12 and b27_caption["maxW"] <= 0.19 and 0.16 <= b27_caption["y"] <= 0.84 and b27_caption.get("size", 53) >= 46, "B27 calendar must leave a readable left caption lane"
assert by_id["b28"]["tpl"] == "card"
assert by_id["b29"]["tpl"] == "scene"
assert by_id["b10"]["args"]["actors"][0]["x"] == "table.left"
assert by_id["b08"]["args"]["actors"][0]["x"] == 0.49
assert by_id["b21"]["args"]["actors"][0]["x"] == 0.43
assert by_id["b08"]["args"]["actors"][0]["pose"] == "sitdesk"
assert by_id["b08"]["args"]["actors"][1]["walk"]["to"] >= 0.84
assert by_id["b08"]["args"]["actors"][1]["hold"] == "portfolio"
b19labels = {t.get("t"): t for t in by_id["b19"]["args"]["texts"]}
assert b19labels["NO."]["x"] == 0.29 and b19labels["NO."]["maxW"] <= 0.36
assert b19labels["Not today."]["x"] == 0.29 and b19labels["Not today."]["maxW"] <= 0.42
assert by_id["b21"]["args"]["actors"][2]["hold"] == "portfolio"
assert [a["x"] for a in by_id["b13"]["args"]["actors"]] == ["table.left", "table.right"]
assert [a["x"] for a in by_id["b24"]["args"]["actors"]] == ["table.left", "table.right"]

story["duration"] = 143.0
path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ART-DIRECTION QA PASS: 29 shots, 143.0s, burden/request/overload/boundary/reaction/submit/reciprocity gates passed")
for sid in ("b01", "b03", "b05", "b08", "b10", "b11", "b14", "b15", "b19", "b20", "b21", "b22", "b24", "b26", "b27"):
    s = by_id[sid]
    print(f"  {sid}: {s['tpl']} / {s['start']:.1f}-{s['end']:.1f}s")
