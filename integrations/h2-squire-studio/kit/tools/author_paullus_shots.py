#!/usr/bin/env python3
"""Assign a historically cautious, vertical Squire storyboard to the ASR-timed draft."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
a = ap.parse_args()
root = Path(a.project)
story_path = root / "story" / "shots.json"
cfg_path = root / "config.json"
story = json.loads(story_path.read_text(encoding="utf-8"))
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
shots = story.get("shots", [])
if not shots:
    raise SystemExit("No draft shots were generated from the aligned narration.")

ROMAN = "#c9473a"
BLUE = "#3e64a3"
GOLD = "#efc23f"
GROUND = {"color": "#c9ad7a", "grass": True, "rocks": False}

def close(face="determined", *, preset="consul", move="in", R=0.135, y=0.445, **extra):
    return {"tpl": "close", "args": {
        "preset": preset, "face": face, "bg": "plain", "time": "day",
        "R": R, "x": 0.5, "y": y, "move": move, "moveAmt": 0.025,
        "blur": 12, **extra
    }}

def top_centre(mode="push"):
    blocks = [
        {"x": 0.10, "y": 0.49, "w": 0.15, "h": 0.20, "cell": 0.020, "side": "red", "face": 1},
        {"x": 0.48, "y": 0.42, "w": 0.19, "h": 0.16, "cell": 0.020, "side": "blue", "face": -1},
        {"x": 0.48, "y": 0.61, "w": 0.19, "h": 0.15, "cell": 0.020, "side": "blue", "face": -1},
        {"x": 0.77, "y": 0.50, "w": 0.13, "h": 0.20, "cell": 0.020, "side": "red", "face": -1},
    ]
    arrows = [
        {"from": [0.20, 0.49], "to": [0.43, 0.49], "at": 0.15, "w": 8, "color": ROMAN}
    ]
    if mode in ("bend", "inward", "trap"):
        arrows = [
            {"from": [0.18, 0.45], "to": [0.43, 0.50], "at": 0.15, "w": 9, "color": BLUE},
            {"from": [0.82, 0.45], "to": [0.57, 0.50], "at": 0.35, "w": 9, "color": BLUE},
        ]
    if mode == "trap":
        blocks += [
            {"x": 0.28, "y": 0.32, "w": 0.18, "h": 0.08, "cell": 0.018, "side": "blue", "face": 1},
            {"x": 0.28, "y": 0.59, "w": 0.18, "h": 0.08, "cell": 0.018, "side": "blue", "face": 1},
        ]
        arrows += [
            {"from": [0.35, 0.30], "to": [0.48, 0.43], "at": 0.45, "w": 8, "color": BLUE},
            {"from": [0.35, 0.62], "to": [0.48, 0.58], "at": 0.65, "w": 8, "color": BLUE},
        ]
    return {"tpl": "top", "args": {
        "ground": GROUND, "blocks": blocks, "arrows": arrows,
        "dust": [{"x": 0.50, "y": 0.52, "s": 0.10, "at": 0.25, "a": 0.45}],
        "move": "in", "moveAmt": 0.018
    }}

def battle_scene(*, action="push", horse=False, face="determined"):
    people = [
        {"preset": "consul", "x": 0.50, "y": 0.61, "h": 0.36,
         "face": face, "pose": "guard", "flip": False}
    ]
    if horse:
        people[0]["pose"] = "hold"
        people[0]["horse"] = {
            "color": "chestnut", "gait": "gallop",
            "cloth": {"color": ROMAN, "charge": "eagle", "chargeColor": GOLD}
        }
        people[0]["h"] = 0.39
    return {"tpl": "scene", "args": {
        "bg": "plain", "time": "day", "bgOpts": {"groundY": 0.62, "trees": 2, "bushes": 3, "flags": False},
        "blur": 6,
        "back": [
            {"preset": "latin", "rows": 3, "cols": 9, "x0": 0.05, "x1": 0.95,
             "yFront": 0.58, "yBack": 0.43, "hFront": 0.12, "hBack": 0.07,
             "flip": True, "face": "determined"}
        ],
        "people": people,
        "fx": [{"kind": "dust", "x": 0.52, "y": 0.60, "n": 10}],
        "move": "in" if action == "push" else "right",
        "moveAmt": 0.035,
        "shake": 0.7 if action == "impact" else 0,
        "vignette": 0.22
    }}

for index, shot in enumerate(shots):
    line = re.sub(r"\s+", " ", shot.get("line", "")).strip().lower()
    shot["in"] = {"type": "cut"}
    shot["sfx"] = []
    shot["notes"] = ""

    # The last rear-cavalry movement must be identified before generic cavalry beats.
    if ("roman rear" in line or "reaches the rear" in line or "rear of the roman" in line):
        shot.update(battle_scene(action="impact", horse=True, face="shout"))
        shot["sfx"] = [
            {"name": "hooves_gallop", "at": 0.0, "gain": -3},
            {"name": "battle_roar", "at": 0.35, "gain": -8},
        ]
    elif ("falls in the thick" in line or "covered with wounds" in line or "dies after" in line or "severe wounds" in line):
        shot.update(close("pain", move="in", R=0.145, y=0.455, pose="kneel",
                          props=[{"kind": "shield", "type": "scutum", "color": ROMAN,
                                  "charge": "eagle", "chargeColor": GOLD, "x": 0.83, "y": 0.56, "s": 0.22, "rot": 0.25}]))
        shot["notes"] = "DROP"
        shot["sfx"] = [{"name": "sting_low", "at": 0.45, "gain": -5}]
    elif ("brutal cavalry" in line or "cavalry fight" in line or "cavalry clash" in line):
        shot.update(battle_scene(action="impact", horse=True, face="determined"))
        shot["sfx"] = [
            {"name": "hooves_gallop", "at": 0.0, "gain": -2},
            {"name": "sword_clash", "at": 0.45, "gain": -5},
        ]
    elif ("august second" in line or "two hundred and sixteen" in line):
        shot.update({"tpl": "title", "args": {
            "text": "CANNAE\n216 BCE", "sub": "SOUTHERN ITALY",
            "bg": "plain", "time": "day", "dim": 0.16, "y": 0.40
        }})
        shot["sfx"] = [{"name": "drum_hit", "at": 0.15, "gain": -7}]
    elif ("near cannae" in line or "southern italy" in line or "faces hannibal" in line):
        shot.update({"tpl": "map", "args": {
            "view": [11.9, 39.8, 17.3, 43.0],
            "places": [
                {"text": "ROME", "lon": 12.496, "lat": 41.903, "at": 0.1},
                {"text": "CANNAE", "lon": 15.59, "lat": 41.31, "at": 0.65},
                {"text": "AUFIDUS", "lon": 15.63, "lat": 41.35, "at": 1.0}
            ],
            "troops": [{"lon": 15.59, "lat": 41.31, "side": "red", "at": 1.25, "n": 6}],
            "move": "in", "moveAmt": 0.02
        }})
        shot["sfx"] = [{"name": "page_turn", "at": 0.0, "gain": -8}]
    elif ("both wings" in line or "turns inward" in line):
        shot.update(top_centre("inward"))
        shot["sfx"] = [{"name": "shield_bash", "at": 0.5, "gain": -7}]
    elif ("flanks are exposed" in line or "flanks exposed" in line):
        shot.update(top_centre("inward"))
        shot["args"]["marks"] = [{"kind": "circle", "x": 0.19, "y": 0.49, "r": 0.09, "at": 0.2},
                                 {"kind": "circle", "x": 0.81, "y": 0.49, "r": 0.09, "at": 0.4}]
    elif ("legions are trapped" in line or "formation" in line and "crowded" in line or "trap was closing" in line or "formation contracts" in line or "circle contracts" in line):
        shot.update(top_centre("trap"))
        shot["args"]["marks"] = [{"kind": "circle", "x": 0.50, "y": 0.50, "r": 0.22, "at": 0.3}]
    elif ("roman infantry pushes" in line or "pushes forward" in line or "surge deeper" in line):
        shot.update({"tpl": "army", "args": {
            "preset": "hastatus", "enemy": "latin", "rows": 5, "cols": 10,
            "march": 0.8, "flip": False, "face": "determined",
            "bg": "plain", "time": "day",
            "move": "in", "moveAmt": 0.025,
            "mid": [{"preset": "hastatus", "rows": 5, "cols": 10, "x0": 0.05, "x1": 0.95,
                      "yFront": 0.61, "yBack": 0.45, "hFront": 0.15, "hBack": 0.08,
                      "march": 0.8, "face": "determined",
                      "flags": [{"col": 0.30, "row": 0.75, "kind": "eagle", "color": GOLD}]}],
            "back": [{"preset": "latin", "rows": 4, "cols": 15, "x0": 0.0, "x1": 1.0,
                      "yFront": 0.45, "yBack": 0.34, "hFront": 0.08, "hBack": 0.05, "flip": True}]
        }})
        shot["sfx"] = [{"name": "drum_march", "at": 0.0, "gain": -7},
                       {"name": "battle_far", "at": 0.2, "gain": -12}]
    elif ("hannibal's centre" in line or "center gives ground" in line or "centre gives ground" in line):
        shot.update(top_centre("bend"))
        shot["sfx"] = [{"name": "battle_roar", "at": 0.15, "gain": -10}]
    elif ("cavalry danger" in line or "cavalry clash" in line or "on the roman right" in line or "roman right" in line):
        shot.update(battle_scene(action="right", horse=True))
        shot["args"]["signs"] = [{"text": "ROMAN RIGHT", "x": 0.50, "y": 0.13, "at": 0.25, "size": 40}]
        shot["sfx"] = [{"name": "hooves_gallop", "at": 0.1, "gain": -5}]
    elif ("rides toward the infantry" in line or "rides toward the centre" in line or "rides toward the center" in line):
        shot.update(battle_scene(action="right", horse=True, face="determined"))
        shot["args"]["signs"] = [{"text": "INTO THE CENTRE", "x": 0.50, "y": 0.13, "at": 0.3, "size": 42}]
        shot["sfx"] = [{"name": "hooves_gallop", "at": 0.0, "gain": -2},
                       {"name": "war_horn", "at": 0.4, "gain": -9}]
    elif ("hannibal" in line and ("fighting" in line or "commanders" in line)):
        shot.update(close("determined", preset="greek", move="in", R=0.135, y=0.445,
                          signs=[{"text": "HANNIBAL", "x": 0.50, "y": 0.13, "at": 0.2, "size": 44}]))
    elif ("paullus" in line or "lucius aemilius" in line or "roman consul" in line):
        face = "worried" if ("trap" in line or "could remain" in line) else "determined"
        shot.update(close(face, move="in", R=0.145 if index < 4 else 0.135, y=0.445,
                          signs=[{"text": "PAULLUS", "x": 0.50, "y": 0.13, "at": 0.2, "size": 44}]
                          if ("lucius" in line or "roman consul" in line) else []))
    elif ("did not ride" in line or "toward safety" in line):
        shot.update(close("determined", move="still", R=0.145, y=0.445))
        shot["notes"] = "DROP"
    elif ("he rode toward" in line or "point where rome" in line):
        shot.update(battle_scene(action="right", horse=True, face="determined"))
        shot["sfx"] = [{"name": "hooves_walk", "at": 0.0, "gain": -7}]
    else:
        # Keep a changing visual rhythm even when the narration line is a connective beat.
        if index % 4 == 0:
            shot.update(close("determined" if index % 2 == 0 else "worried"))
        elif index % 4 == 1:
            shot.update(top_centre("push"))
        elif index % 4 == 2:
            shot.update(battle_scene(action="push"))
        else:
            shot.update({"tpl": "army", "args": {
                "preset": "hastatus", "enemy": "latin", "rows": 4, "cols": 8,
                "march": 0.7, "bg": "plain", "time": "day", "move": "in",
                "mid": [{"preset": "hastatus", "rows": 4, "cols": 8, "x0": 0.08, "x1": 0.92,
                         "yFront": 0.60, "yBack": 0.45, "hFront": 0.14, "hBack": 0.08, "march": 0.7}],
                "back": [{"preset": "latin", "rows": 3, "cols": 14, "x0": 0.0, "x1": 1.0,
                          "yFront": 0.45, "yBack": 0.34, "hFront": 0.08, "hBack": 0.05, "flip": True}]
            }})

    shot["args"] = shot.get("args") or {}
    # Short captions occupy the lower third; keep titles, labels and tactical symbols above them.
    shot["args"].setdefault("move", "in")
    shot["args"].setdefault("moveAmt", 0.02)

duration = float(shots[-1]["end"])
story["title"] = cfg.get("title", "The Roman Consul Who Rode Into Hannibal's Trap")
story["duration"] = round(duration, 3)
story["music"] = [{"start": 0.0, "end": round(duration, 3), "bed": "war", "gainDb": -1.5}]
story_path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
cfg["duration"] = round(duration, 3)
cfg["aspect"] = "9:16"
cfg["resolution"] = "1080p"
cfg["fps"] = 24
cfg["captions"] = True
cfg["music"] = {"enabled": True, "gainDb": -13}
cfg["sfx"] = {"enabled": True, "gainDb": -4}
cfg["loudness"] = -14
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
missing = [s["id"] for s in shots if not s.get("tpl") or not s.get("args")]
if missing:
    raise SystemExit("Shots without authored visual template: " + ", ".join(missing))
for i in range(2, len(shots)):
    if shots[i]["tpl"] == shots[i-1]["tpl"] == shots[i-2]["tpl"]:
        # Keep the story beat's underlying visual meaning, but add a different framing by switching a generic scene.
        if shots[i]["tpl"] == "close":
            shots[i]["tpl"] = "scene"
            shots[i]["args"] = {
                "bg": "plain", "time": "day", "people": [
                    {"preset": "consul", "x": 0.5, "y": 0.61, "h": 0.36, "face": "determined", "pose": "guard"}
                ], "move": "in", "moveAmt": 0.03
            }
        elif shots[i]["tpl"] == "top":
            shots[i]["tpl"] = "army"
            shots[i]["args"] = {"preset": "hastatus", "enemy": "latin", "rows": 4, "cols": 8,
                                "march": 0.7, "bg": "plain", "time": "day", "move": "in",
                                "mid": [{"preset": "hastatus", "rows": 4, "cols": 8, "x0": 0.08, "x1": 0.92,
                                         "yFront": 0.60, "yBack": 0.45, "hFront": 0.14, "hBack": 0.08}],
                                "back": [{"preset": "latin", "rows": 3, "cols": 14, "x0": 0.0, "x1": 1.0,
                                          "yFront": 0.45, "yBack": 0.34, "hFront": 0.08, "hBack": 0.05, "flip": True}]}
story_path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Authored {len(shots)} Squire shots, {duration:.2f}s, 9:16 @24fps; one war bed and action-led SFX.")
