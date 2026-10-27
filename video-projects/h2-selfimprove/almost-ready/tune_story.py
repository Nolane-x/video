#!/usr/bin/env python3
"""Idempotent, schema-checked art-direction pass for ALMOST READY."""
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
shots[-1]["end"] = 172.0
story["duration"] = 172.0

def cap(kind: str, text: str, at: float = 0.3, dur: float = 5.25,
        x: float = 0.5, y: float = 0.20, size: int = 55,
        max_w: float = 0.82, **extra: Any) -> dict[str, Any]:
    return {"kind": kind, "t": text, "at": at, "dur": dur,
            "x": x, "y": y, "size": size, "maxW": max_w, **extra}

def narr(text: str, at: float = 0.3, dur: float = 5.25, **extra: Any) -> dict[str, Any]:
    return cap("narr", text, at, dur, **extra)

def tempting(text: str, at: float = 0.5, dur: float = 4.5, **extra: Any) -> dict[str, Any]:
    return cap("tempt", text, at, dur, y=extra.pop("y", 0.31),
               size=extra.pop("size", 46), max_w=extra.pop("max_w", 0.65), **extra)

def actor(who: str, x: Any, pose: str = "stand", face: str = "neutral", **extra: Any) -> dict[str, Any]:
    return {"who": who, "x": x, "pose": pose, "face": face, **extra}

def cam(x: float, y: float, z1: float = 1.08, dur: float = 5.4) -> dict[str, Any]:
    return {"from": [x, y, 1.0], "to": [x, y, z1], "at": 0.25, "dur": dur}

def bedroom(sky: str = "night", **extra: Any) -> dict[str, Any]:
    return {"sky": sky, "stage": True, "bedX": 0.12, "bedW": 0.25,
            "windowX": 0.42, "deskX": 0.72, "laptop": True,
            "lamp": True, "calendar": False, "clock": False, **extra}

def apply(sid: str, tpl: str, args: dict[str, Any], transition: dict[str, Any] | None = None) -> None:
    s = by_id[sid]
    s["tpl"] = tpl
    s["args"] = args
    if transition is not None:
        s["in"] = transition
    else:
        s["in"] = {"type": "cut"}

# B01 — a sparse hook, not a busy title graphic.
apply("b01", "black", {
    "dust": True, "line": False,
    "texts": [cap("big", "He was always one revision away.", 0.25, 3.45,
                  y=0.47, size=86, max_w=0.86)]
})

# B02 — establish a consistent, richly staged bedroom studio.
apply("b02", "scene", {
    "set": "bedroom", "setArgs": bedroom("night", door=True, doorOpen=0.08),
    "actors": [actor("hero", "desk.seat", "sitdesk", "determined", facing=1, look=0.12)],
    "hud": {"rows": [{"label": "DAYS LEFT", "n": 5}]},
    "cam": cam(0.60, 0.57, 1.08),
    "texts": [narr("The deadline was five days away.", 0.35, 4.25, x=0.25, y=0.28, size=42, max_w=0.24)]
})

# B03 — native notebook drawing with a visible, timed pen contact.
apply("b03", "note", {
    "text": "FIRST DRAFT", "at": 0.45, "cps": 5.0, "x": 0.5, "y": 0.52, "s": 0.88,
    "cam": cam(0.5, 0.52, 1.07),
    "texts": [narr("The first draft felt alive.", 0.35, 4.25, x=0.70, y=0.67, size=50, max_w=0.27, color="#302a24")]
})

# B04 — face reaction after the first flaw; the screen/page light cools the mood.
apply("b04", "face", {
    "who": "hero", "face": "worried", "faceAt": [[0.0, "neutral"], [2.4, "worried"]],
    "look": -0.12, "h": 1.22, "x": 0.5, "y": 0.50,
    "bg": "bedroom", "setArgs": bedroom("night"),
    "cam": cam(0.5, 0.52, 1.06),
    "texts": [narr("Then he found one imperfect line.", 0.35, 5.3)]
})

# B05 — the temptation has a physical position behind the hero, not just text.
apply("b05", "scene", {
    "set": "bedroom", "setArgs": bedroom("night"),
    "actors": [
        actor("hero", "desk.seat", "type", "worried", facing=1),
        actor("voice", 0.89, "reach", "grin", facing=-1, at=0.35, scale=0.70)
    ],
    "cam": cam(0.68, 0.58, 1.12),
    "texts": [
        narr("He traded progress for another correction.", 0.35, 5.15, x=0.18, y=0.28, size=50, max_w=0.34),
        tempting("just one small correction.", 0.45, 4.95)
    ]
})

# B06 — actual laptop insert for the deadline, never a fake phone screen.
apply("b06", "laptop", {
    "bg": "bedroom", "setArgs": bedroom("night"), "x": 0.35, "y": 0.50,
    "w": 0.62, "h": 0.66, "subject": "PORTFOLIO APPLICATION",
    "sender": "Studio Review", "body": "Final submissions close Friday at 11:59 PM.",
    "cam": cam(0.5, 0.5, 1.04),
    "texts": [narr("The deadline was already real.", 0.35, 4.55, x=0.85, y=0.49, size=50, max_w=0.26)]
})

# B07 — a tighter over-shoulder staging; keep the shadow away from the text lane.
apply("b07", "scene", {
    "set": "bedroom", "setArgs": bedroom("night"),
    "actors": [
        actor("hero", "desk.seat", "type", "tired", facing=1, look=0.1),
        actor("voice", 0.91, "reach", "grin", facing=-1, at=0.2, scale=0.76)
    ],
    "hud": {"rows": [{"label": "EDITS", "n": 12}]},
    "cam": cam(0.70, 0.60, 1.24),
    "texts": [
        narr("He hid the work from everyone.", 0.35, 5.15, x=0.18, y=0.28, size=50, max_w=0.34),
        tempting("nobody needs to see it yet.", 0.45, 4.95, x=0.78, y=0.32)
    ]
})

# B08 — the revision counter grows while the shared count stays at zero.
apply("b08", "calendar", {
    "month": "NOV", "from": 1, "to": 12, "at": 0.3, "dur": 5.1,
    "mode": "x", "color": "#d79b42", "s": 0.61,
    "hud": {"rows": [
        {"label": "EDITS", "from": 1, "to": 12, "at": 0.3, "dur": 5.1},
        {"label": "SHARED", "n": 0}
    ]},
    "cam": cam(0.5, 0.53, 1.08),
    "texts": [narr("One correction became twelve.", 0.35, 4.25, x=0.20, y=0.60, size=42, max_w=0.24)]
})

# B09 — an insert of version 19, with correct page/pen staging.
apply("b09", "note", {
    "text": "VERSION 19", "at": 0.4, "cps": 5.1, "s": 0.90,
    "cam": cam(0.5, 0.52, 1.13),
    "hud": {"rows": [{"label": "EDITS", "n": 19}, {"label": "SHARED", "n": 0}]},
    "texts": [narr("Every fix uncovered another flaw.", 0.35, 4.25, x=0.70, y=0.67, size=50, max_w=0.27, color="#302a24")]
})

# B10 — peers visibly share; the protagonist stays in the less-lit foreground.
apply("b10", "scene", {
    "set": "classroom",
    "setArgs": {"sky": "dusk", "board": "SHOWCASE FRIDAY", "desks": [0.20, 0.45, 0.70]},
    "actors": [
        actor("hero", 0.31, "stand", "worried", facing=1, scale=0.96, z=1, look=0.05),
        actor("girl", 0.72, "reach", "smile", facing=-1, scale=0.92, at=0.15, hold="portfolio")
    ],
    "cam": cam(0.49, 0.57, 1.04),
    "texts": [narr("Everyone else had something to show.", 0.35, 4.25, x=0.41, y=0.28, size=44, max_w=0.34)]
})

# B11 — a readable phone feed establishes comparison without overloading the screen.
apply("b11", "phone", {
    "screen": "feed", "posts": ["mountain", "city", "sneakers"],
    "x": 0.38, "y": 0.53, "h": 0.90, "hands": True, "tilt": -0.10,
    "bg": "bedroom", "setArgs": bedroom("night"),
    "cam": cam(0.5, 0.55, 1.04),
    "texts": [narr("Their finished work appeared everywhere.", 0.3, 5.3, x=0.80, y=0.49, size=49, max_w=0.31)]
})

# B12 — autosave is not submission.
apply("b12", "laptop", {
    "bg": "bedroom", "setArgs": bedroom("night"), "x": 0.35, "y": 0.5,
    "w": 0.62, "h": 0.68, "subject": "MY PORTFOLIO — DRAFT 47",
    "sender": "Autosave", "body": "Last saved at 11:38 PM. Not submitted.",
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("He kept saving instead of sending.", 0.35, 4.55, x=0.85, y=0.49, size=50, max_w=0.26)]
})

# B13 — preserve the clock insert and time transition as a separate action.
apply("b13", "clock", {
    "time": "11:58", "timeAt": [[3.0, "11:59"]], "ring": False,
    "s": 0.64, "x": 0.5, "y": 0.53, "cam": cam(0.5, 0.52, 1.08),
    "texts": [narr("The minutes began to sprint.", 0.35, 5.15, x=0.16, y=0.28, size=50, max_w=0.28)]
})

# B14 — the voice is close and dominant at the low point.
apply("b14", "scene", {
    "set": "void", "setArgs": {"spot": 0.53, "gy": 0.81},
    "actors": [
        actor("hero", 0.38, "slump", "scared", facing=1, scale=1.02),
        actor("voice", 0.69, "reach", "grin", facing=-1, at=0.15, scale=1.06, glow="#cf9747")
    ],
    "cam": cam(0.52, 0.55, 1.13),
    "texts": [
        narr("Fear made every mistake feel permanent.", 0.35, 5.15, x=0.18, y=0.28, size=50, max_w=0.34),
        tempting("they'll notice every mistake.", 0.45, 4.9, x=0.75, y=0.31)
    ]
})

# B15 — deadline count reaches zero; the two lines do not collide.
apply("b15", "black", {
    "dust": False, "line": False, "cy": 0.43,
    "hud": {"rows": [{"label": "MINUTES LEFT", "from": 1, "to": 0, "at": 0.25, "dur": 1.6}]},
    "texts": [
        cap("narr", "At 11:59, the window closed.", 0.3, 2.25, y=0.36, size=65, max_w=0.85),
        cap("big", "His draft was still open.", 2.85, 2.75, y=0.57, size=82, max_w=0.88)
    ]
}, {"type": "dip", "dur": 0.25})

# B16 — a closed portal, visibly legible on the computer.
apply("b16", "laptop", {
    "bg": "bedroom", "setArgs": bedroom("night"), "x": 0.35, "y": 0.5,
    "w": 0.62, "h": 0.70, "subject": "SUBMISSION WINDOW CLOSED",
    "sender": "Portfolio Portal", "body": "This application is no longer accepting files.",
    "cam": cam(0.5, 0.5, 1.09),
    "texts": [narr("He had polished it for no one.", 0.35, 4.55, x=0.85, y=0.49, size=50, max_w=0.26)]
})

# B17 — intentional silence after the emotional reveal.
apply("b17", "black", {
    "dust": False, "line": False, "cy": 0.43,
    "texts": [
        cap("narr", "He wasn't afraid of bad work.", 0.25, 2.4, y=0.35, size=66, max_w=0.87),
        cap("big", "He was afraid of being seen.", 3.05, 2.55, y=0.57, size=80, max_w=0.88)
    ]
}, {"type": "dip", "dur": 0.3})

# B18 — the human connection is a real message and a new sound bed.
apply("b18", "phone", {
    "screen": "chat", "name": "Mina",
    "messages": [{"text": "still want to see what you made?", "me": False, "at": 0.55}],
    "x": 0.43, "y": 0.53, "h": 0.91, "hands": True, "tilt": -0.04,
    "bg": "bedroom", "setArgs": bedroom("dawn"),
    "cam": cam(0.5, 0.53, 1.04),
    "texts": [narr("Someone still wanted to see it.", 0.35, 5.2, x=0.80, y=0.5, size=49, max_w=0.32)]
}, {"type": "dip", "dur": 0.4})

# B19 — stand and walk to the desk; the turn is visible in body and light.
apply("b19", "scene", {
    "set": "bedroom", "setArgs": bedroom("dawn", door=True, doorOpen=0.4),
    "actors": [actor("hero", 0.30, "stand", "determined", facing=1,
                     walk={"to": "desk.seat", "at": 0.35, "dur": 2.8, "speed": 0.78})],
    "cam": cam(0.53, 0.57, 1.12),
    "texts": [narr("He opened the file one last time.", 0.35, 4.25, x=0.22, y=0.28, size=42, max_w=0.24)]
})

# B20 — the written rule is the action; the hand must track the current line.
apply("b20", "note", {
    "text": "GOOD ENOUGH\nTO SHARE.", "at": 0.45, "cps": 6.2,
    "x": 0.5, "y": 0.52, "s": 0.92, "cam": cam(0.5, 0.52, 1.10),
    "texts": [narr("He made one rule for himself.", 0.35, 4.25, x=0.70, y=0.67, size=50, max_w=0.27, color="#302a24")]
})

# B21 — deliberate desk composition, real typing posture; sent count is still zero.
apply("b21", "scene", {
    "set": "bedroom", "setArgs": bedroom("dawn", phoneOnDesk={"x": 0.82}),
    "actors": [actor("hero", "desk.seat", "type", "determined", facing=1, look=0.10)],
    "hud": {"rows": [{"label": "EDITS", "n": 47}, {"label": "SHARED", "n": 0}]},
    "cam": cam(0.69, 0.60, 1.24),
    "texts": [narr("He chose the version he had.", 0.35, 4.25, x=0.80, y=0.28, size=42, max_w=0.25)]
})

# B22 — the outgoing email is visible on laptop; sent is now one.
apply("b22", "laptop", {
    "bg": "bedroom", "setArgs": bedroom("dawn"), "x": 0.35, "y": 0.5,
    "w": 0.62, "h": 0.70, "subject": "Portfolio — first look",
    "sender": "To: Mina", "body": "It's not finished. I wanted you to see it.",
    "sentAt": 2.25,
    "hud": {"rows": [{"label": "EDITS", "n": 47}, {"label": "SHARED", "n": 1}]},
    "cam": cam(0.5, 0.5, 1.08),
    "texts": [narr("He sent it before he could retreat.", 0.35, 4.55, x=0.85, y=0.49, size=50, max_w=0.26)]
})

# B23 — response arrives after send; the notification is not the ending by itself.
apply("b23", "phone", {
    "screen": "chat", "name": "Mina",
    "messages": [{"text": "it's rough. it's interesting. keep going.", "me": False, "at": 0.55}],
    "x": 0.43, "y": 0.53, "h": 0.91, "hands": True,
    "bg": "bedroom", "setArgs": bedroom("dawn"),
    "hud": {"rows": [{"label": "SHARED", "n": 1}]},
    "cam": cam(0.5, 0.52, 1.05),
    "texts": [narr("A real person answered the work.", 0.35, 5.2, x=0.80, y=0.5, size=49, max_w=0.32)]
})

# B24 — true two-person café geography and reciprocal eye-lines.
apply("b24", "scene", {
    "set": "cafe", "setArgs": {"lampX": 0.50, "tableW": 0.28},
    "actors": [
        actor("hero", "table.left", "sit", "worried", facing=1, scale=0.88,
              faceAt=[[0.0, "worried"], [1.8, "neutral"], [3.7, "smile"]], look=0.1),
        actor("girl", "table.right", "sit", "smile", facing=-1, scale=0.88, at=0.12,
              poseAt=[[0.0, "sit"], [2.0, "sitpoint"]])
    ],
    "cam": cam(0.5, 0.55, 1.06),
    "texts": [narr("Her first question was about the idea.", 0.35, 4.25, x=0.82, y=0.28, size=50, max_w=0.30)]
})

# B25 — studio critique; hero is no longer hidden at the back of the room.
apply("b25", "scene", {
    "set": "classroom",
    "setArgs": {"sky": "dawn", "board": "MAKE  /  SHARE  /  LEARN", "desks": [0.20, 0.46, 0.72]},
    "actors": [
        actor("hero", 0.40, "stand", "determined", facing=1, scale=0.97),
        actor("girl", 0.72, "stand", "smile", facing=-1, scale=0.92, at=0.12)
    ],
    "cam": cam(0.54, 0.56, 1.08),
    "texts": [narr("The room didn't collapse around him.", 0.35, 4.5, x=0.38, y=0.28, size=44, max_w=0.30)]
})

# B26 — motivated lateral walk through the city at dawn, not zoom-only movement.
apply("b26", "scene", {
    "set": "city", "setArgs": {"time": "dawn", "scroll": 1.0, "birds": True, "lamps": [0.18, 0.84]},
    "actors": [actor("hero", 0.18, "stand", "neutral", facing=1,
                     walk={"to": 0.78, "at": 0.25, "dur": 4.3, "speed": 0.78})],
    "cam": cam(0.5, 0.56, 1.05),
    "texts": [narr("A few flaws survived the journey.", 0.35, 4.5)]
})

# B27 — the old voice returns small; the hero keeps working.
apply("b27", "scene", {
    "set": "bedroom", "setArgs": bedroom("dawn"),
    "actors": [
        actor("hero", "desk.seat", "type", "determined", facing=1, look=0.1),
        actor("voice", 0.93, "reach", "grin", facing=-1, at=0.25,
              scale=0.40, out=4.8, fade=0.85, glow="#8f724d")
    ],
    "cam": cam(0.69, 0.60, 1.20, 8.35),
    "texts": [
        narr("He still heard the old voice.", 0.25, 2.2, x=0.18, y=0.20, size=46, max_w=0.30),
        tempting("one more tiny fix.", 2.65, 1.8, x=0.80, y=0.30, size=42),
        narr("He didn't have to obey it.", 4.65, 3.0, x=0.18, y=0.20, size=46, max_w=0.30)
    ]
})

# B28 — distinct end-card hierarchy, no copied thumbnail text treatment.
apply("b28", "card", {
    "word": "RELEASE.", "sub": "Finished can find its people.",
    "sub2": "Let it leave your hands.", "at": 0.3,
    "typeDur": 1.25, "size": 0.15,
    "texts": []
}, {"type": "dip", "dur": 0.45})

# B29 — natural in-world CTA rather than simulated Like/Subscribe buttons.
apply("b29", "scene", {
    "set": "bedroom", "setArgs": bedroom("dawn", door=True, doorOpen=0.7),
    "actors": [actor("hero", 0.53, "wave", "smile", facing=1, scale=0.94)],
    "cam": cam(0.52, 0.55, 1.04),
    "texts": [narr("If this hit, like and subscribe.", 0.35, 5.1, x=0.22, y=0.29, size=50, max_w=0.30)]
})

# Validate captions and global timing after the authored pass.
# Readability/coverage gate: raise story captions to a usable Full-HD floor, then require both narrative coverage and visible text at 75% of each shot.
for shot in shots:
    sid = shot["id"]
    args = shot.get("args", {})
    if sid == "b28":
        assert args.get("word") and args.get("sub") and args.get("sub2"), "B28 card must contain all three end-card lines"
        continue
    texts = args.get("texts", [])
    story_texts = [tx for tx in texts if tx.get("kind", "narr") in ("narr", "big")]
    assert story_texts, f"{sid} is missing its main narrative line"
    for tx in story_texts:
        tx["size"] = max(50, int(tx.get("size", 58)))
    duration = float(shot["end"]) - float(shot["start"])
    sample_t = duration * 0.75
    active_story = [tx for tx in story_texts if float(tx.get("at", 0.3)) <= sample_t <= float(tx.get("at", 0.3)) + float(tx.get("dur", duration - float(tx.get("at", 0.3)) - 0.1))]
    assert active_story, f"{sid} has no STORY narration active at the 75% contact-sheet sample"
    # Keep the selected narration fully opaque at the exact contact-sheet sample.
    tx = active_story[-1]
    at = float(tx.get("at", 0.3))
    fo = float(tx.get("fo", 0.45))
    tx["dur"] = max(float(tx.get("dur", duration - at - 0.1)), sample_t - at + fo + 0.12)
    assert at + float(tx["dur"]) <= duration - 0.05, f"{sid} narration cannot remain fully opaque at 75% without overrunning the shot"

previous_end = 0.0
for s in shots:
    assert abs(float(s["start"]) - previous_end) < 0.01, f"Gap/overlap before {s['id']}"
    assert float(s["end"]) > float(s["start"]), f"Invalid shot duration: {s['id']}"
    d = float(s["end"]) - float(s["start"])
    for tx in s.get("args", {}).get("texts", []):
        at = float(tx.get("at", 0.3))
        dur = float(tx.get("dur", d - at - 0.1))
        assert at >= 0 and dur > 0 and at + dur <= d + 0.02, (
            f"{s['id']} text outside shot: {tx.get('t')!r}; at={at}, dur={dur}, shot={d}"
        )
        if tx.get("kind") in ("narr", "big") and tx.get("y") is not None:
            text_y = float(tx["y"])
            assert 0.16 <= text_y <= 0.84, (
                f"Caption falls in/too close to cinematic bars: {s['id']} / "
                f"{tx.get('t')!r} at y={text_y}"
            )
    previous_end = float(s["end"])
assert abs(previous_end - 172.0) < 0.02, f"Expected 172.0 s, got {previous_end}"
assert by_id["b03"]["tpl"] == "note" and by_id["b03"]["args"]["text"] == "FIRST DRAFT"
assert by_id["b13"]["tpl"] == "clock" and "11:59" in str(by_id["b13"]["args"].get("timeAt"))
assert by_id["b15"]["args"]["hud"]["rows"][0]["to"] == 0
assert by_id["b22"]["tpl"] == "laptop" and by_id["b22"]["args"]["hud"]["rows"][1]["n"] == 1 and by_id["b22"]["args"]["sentAt"] == 2.25
assert by_id["b10"]["args"]["actors"][1]["pose"] == "reach" and by_id["b10"]["args"]["actors"][1]["hold"] == "portfolio"
assert by_id["b24"]["args"]["set"] == "cafe" and len(by_id["b24"]["args"]["actors"]) == 2
assert by_id["b24"]["args"]["actors"][1]["poseAt"] == [[0.0, "sit"], [2.0, "sitpoint"]]
assert by_id["b27"]["args"]["actors"][1]["scale"] < 0.5
b27_text = {tx.get("t"): tx for tx in by_id["b27"]["args"].get("texts", [])}
assert b27_text["He still heard the old voice."]["dur"] >= 2.0
assert b27_text["one more tiny fix."]["dur"] >= 1.7
assert by_id["b25"]["args"]["texts"][0]["dur"] <= 4.6
assert by_id["b26"]["args"]["texts"][0]["dur"] <= 4.6
for sid in ("b06", "b12", "b16", "b22"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] >= 0.84 and 0.40 <= tx["y"] <= 0.60 and tx["maxW"] <= 0.30 and tx.get("size", 53) >= 48, (
        f"{sid} laptop narration must remain in the right-side message-safe area"
    )
    shot_duration = float(by_id[sid]["end"]) - float(by_id[sid]["start"])
    assert float(tx["at"]) + float(tx["dur"]) <= shot_duration + 0.02, f"{sid} narration overflows its shot"
b25_caption = by_id["b25"]["args"]["texts"][0]
assert 0.30 <= b25_caption["x"] <= 0.45 and 0.22 <= b25_caption["y"] <= 0.34 and b25_caption["maxW"] <= 0.31
for sid in ("b10", "b25"):
    tx = by_id[sid]["args"]["texts"][0]
    assert 0.30 <= tx["x"] <= 0.44 and 0.22 <= tx["y"] <= 0.34 and tx["maxW"] <= 0.35 and tx.get("size", 53) >= 48, f"{sid} narration must avoid the TEAM WORK/SHOWCASE board"
for sid in ("b03", "b09", "b20"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] == 0.70 and tx["y"] >= 0.63 and tx["maxW"] <= 0.28 and tx.get("size", 53) >= 48 and tx.get("color") == "#302a24", f"{sid} notebook narration must be dark, readable and inside the blank right page"
for sid in ("b02", "b19", "b29"):
    tx = by_id[sid]["args"]["texts"][0]
    assert tx["x"] <= 0.26 and tx["maxW"] <= 0.31 and 0.25 <= tx["y"] <= 0.33 and tx.get("size", 53) >= 48, f"{sid} caption must stay left of the window/character and remain readable"
tx = by_id["b21"]["args"]["texts"][0]
assert tx["x"] >= 0.76 and tx["maxW"] <= 0.30 and 0.25 <= tx["y"] <= 0.33 and tx.get("size", 53) >= 48, "B21 caption must stay in the right-side bedroom wall lane"
tx = by_id["b13"]["args"]["texts"][0]
assert tx["x"] <= 0.18 and 0.25 <= tx["y"] <= 0.32 and tx["maxW"] <= 0.30 and tx.get("size", 53) >= 48 and by_id["b13"]["args"]["s"] <= 0.66, "B13 clock must leave a readable left narration lane"
tx = by_id["b08"]["args"]["texts"][0]
assert tx["x"] <= 0.22 and tx["y"] >= 0.55 and tx["maxW"] <= 0.25, "B08 calendar caption must stay left of the calendar"
tx = by_id["b24"]["args"]["texts"][0]
assert tx["x"] >= 0.80 and 0.24 <= tx["y"] <= 0.32 and tx["maxW"] <= 0.31 and tx.get("size", 53) >= 48, "B24 cafe narration must stay above the seated characters and remain readable"
assert by_id["b27"]["args"]["texts"][0]["x"] <= 0.25 and by_id["b27"]["args"]["texts"][2]["x"] <= 0.25
assert b27_text["He didn't have to obey it."]["dur"] >= 3.0
assert abs(float(by_id["b27"]["end"]) - float(by_id["b27"]["start"]) - 9.0) < 0.02
story["duration"] = 172.0
path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ART-DIRECTION QA PASS: 29 shots, 172.0s, desk/pen/clock/deadline/send/reply/cafe/voice gates passed")
for sid in ("b03", "b05", "b10", "b13", "b15", "b16", "b18", "b20", "b21", "b22", "b23", "b24", "b27"):
    s = by_id[sid]
    print(f"  {sid}: {s['tpl']} / {s['start']:.1f}-{s['end']:.1f}s / {s.get('scene', '')[:60]}")
