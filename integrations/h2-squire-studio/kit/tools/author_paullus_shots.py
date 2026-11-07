#!/usr/bin/env python3
"""Create a shot-specific illustrated Cannae storyboard from ASR-timed narration."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
args = ap.parse_args()
root = Path(args.project)
story_path = root / "story" / "shots.json"
cfg_path = root / "config.json"
story = json.loads(story_path.read_text(encoding="utf-8"))
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
shots = story.get("shots", [])
source_lines = json.loads((root / "timeline" / "lines.json").read_text(encoding="utf-8"))
if not shots or not source_lines:
    raise SystemExit("Storyboard draft and aligned source lines are both required.")

ROMAN = "#c9473a"
CARTHAGE = "#3e64a3"
GOLD = "#efc23f"
GROUND = {"color": "#c9ad7a", "grass": True, "rocks": False}

def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()

def source_for(shot):
    start, end = float(shot["start"]), float(shot["end"])
    candidates = []
    for row in source_lines:
        overlap = max(0.0, min(end, float(row["end"])) - max(start, float(row["start"])))
        if overlap > 0:
            candidates.append((overlap, row))
    if not candidates:
        return min(source_lines, key=lambda row: abs(float(row["start"]) - start))
    return max(candidates, key=lambda item: item[0])[1]

source_rows = [source_for(shot) for shot in shots]
source_indices = {}
for index, row in enumerate(source_rows):
    source_indices.setdefault(row["id"], []).append(index)

def beat_index(index, row):
    return source_indices[row["id"]].index(index)

def close(face="determined", *, preset="consul", move="in", R=0.135, y=0.445, **extra):
    return {"tpl": "close", "args": {
        "preset": preset, "face": face, "bg": "plain", "time": "golden",
        "R": R, "x": 0.5, "y": y, "move": move, "moveAmt": 0.035,
        "blur": 13, **extra
    }}

def top_centre(mode="push"):
    # Schematic Cannae plan: Roman mass in red, Carthaginian centre and wings in blue.
    roman = {
        "x": 0.50, "y": 0.66, "w": 0.34, "h": 0.22,
        "cell": 0.018, "rows": 11, "cols": 16, "side": "red",
        "face": -1, "spears": True, "tired": True
    }
    carth_center = {
        "x": 0.50, "y": 0.39, "w": 0.28, "h": 0.105,
        "cell": 0.018, "rows": 5, "cols": 13, "side": "blue",
        "face": 1, "spears": True
    }
    left_wing = {
        "x": 0.18, "y": 0.56, "w": 0.105, "h": 0.28,
        "cell": 0.018, "rows": 13, "cols": 5, "side": "blue",
        "face": 1, "spears": True
    }
    right_wing = {
        "x": 0.82, "y": 0.56, "w": 0.105, "h": 0.28,
        "cell": 0.018, "rows": 13, "cols": 5, "side": "blue",
        "face": -1, "spears": True
    }
    blocks = [roman, carth_center, left_wing, right_wing]
    arrows = []
    if mode == "push":
        roman["path"] = [[1.65, 0.50, 0.54]]
        arrows = [{"from": [0.50, 0.82], "to": [0.50, 0.53], "at": 0.2, "w": 10, "color": ROMAN}]
    elif mode == "bend":
        roman["path"] = [[1.1, 0.50, 0.58]]
        carth_center["path"] = [[0.9, 0.50, 0.33]]
        arrows = [
            {"from": [0.50, 0.40], "to": [0.50, 0.26], "at": 0.25, "w": 8, "color": CARTHAGE},
            {"from": [0.50, 0.78], "to": [0.50, 0.59], "at": 0.25, "w": 8, "color": ROMAN},
        ]
    elif mode in ("inward", "trap"):
        left_wing["path"] = [[1.6, 0.36, 0.59]]
        right_wing["path"] = [[1.6, 0.64, 0.59]]
        arrows = [
            {"from": [0.22, 0.54], "to": [0.39, 0.59], "at": 0.2, "w": 9, "color": CARTHAGE},
            {"from": [0.78, 0.54], "to": [0.61, 0.59], "at": 0.45, "w": 9, "color": CARTHAGE},
        ]
    if mode == "trap":
        roman["path"] = [[1.3, 0.50, 0.61]]
        blocks.append({
            "x": 0.50, "y": 0.91, "w": 0.25, "h": 0.08,
            "cell": 0.018, "rows": 4, "cols": 12, "side": "blue",
            "face": -1, "path": [[1.7, 0.50, 0.76]], "spears": True
        })
        arrows.append({"from": [0.50, 0.89], "to": [0.50, 0.72], "at": 0.55, "w": 10, "color": CARTHAGE})
    return {"tpl": "top", "args": {
        "ground": GROUND, "blocks": blocks, "arrows": arrows,
        "dust": [
            {"x": 0.50, "y": 0.59, "s": 0.12, "at": 0.25, "a": 0.42},
            {"x": 0.38, "y": 0.58, "s": 0.08, "at": 0.8, "a": 0.25}
        ],
        "move": "in", "moveAmt": 0.025,
        "signs": [
            {"text": "ROME", "x": 0.50, "y": 0.14, "at": 0.2, "size": 39},
            {"text": "CARTHAGE", "x": 0.50, "y": 0.94, "at": 0.5, "size": 34}
        ]
    }}

def battle_scene(*, action="push", horse=False, face="determined",
                 rider_preset="consul", horse_color="chestnut",
                 cloth_color=ROMAN, pair=False):
    people = []
    def mounted(preset, x0, x1, color, cloth, expression, flip=False, seed=0):
        return {
            "preset": preset, "x": x0, "from": x0, "to": x1,
            "dur": 1.75, "y": 0.76, "h": 0.38,
            "face": expression, "pose": "ride", "seed": seed,
            "horse": {
                "color": color, "gait": "gallop", "h": 0.88,
                "cloth": {"color": cloth, "charge": "eagle", "chargeColor": GOLD},
                "riderH": 0.67
            },
            "flip": flip
        }
    if horse and pair:
        people = [
            mounted("consul", 0.10, 0.53, "chestnut", ROMAN, face, seed=2),
            mounted("greek", 0.90, 0.57, "bay", CARTHAGE, "angry", flip=True, seed=5)
        ]
    elif horse:
        end = 0.88 if action != "retreat" else 0.14
        start = 0.12 if action != "retreat" else 0.88
        people = [mounted(rider_preset, start, end, horse_color, cloth_color, face, flip=action=="retreat")]
    else:
        people = [{
            "preset": "consul", "x": 0.50, "y": 0.68, "h": 0.42,
            "face": face, "pose": "guard", "walk": False
        }]
    return {"tpl": "scene", "args": {
        "bg": "plain", "time": "golden",
        "bgOpts": {"groundY": 0.67, "trees": 5, "bushes": 5, "flags": True, "clouds": 2},
        "blur": 5,
        "back": [
            {"preset": "latin", "rows": 3, "cols": 17, "x0": 0.0, "x1": 1.0,
             "yFront": 0.56, "yBack": 0.42, "hFront": 0.13, "hBack": 0.07,
             "flip": True, "face": "determined", "march": 0.55},
            {"preset": "hastatus", "rows": 2, "cols": 10, "x0": 0.08, "x1": 0.92,
             "yFront": 0.72, "yBack": 0.63, "hFront": 0.09, "hBack": 0.06,
             "face": "determined", "march": 0.4}
        ],
        "people": people,
        "front": [
            {"preset": "legionary", "x": 0.94, "y": 1.05, "h": 0.68, "flip": True}
        ],
        "fx": [
            {"kind": "dust", "x": 0.52, "y": 0.66, "n": 14, "a": 0.65},
            {"kind": "rays", "x": 0.25, "n": 3, "a": 0.07}
        ],
        "move": "right" if action in ("right", "retreat") else "in",
        "moveAmt": 0.035,
        "shake": 0.7 if action == "impact" else 0,
        "vignette": 0.24
    }}

def paullus_fall_scene():
    return {"tpl": "scene", "args": {
        "bg": "mud", "time": "dusk",
        "bgOpts": {"groundY": 0.72, "trees": 2, "bushes": 3, "mud": True, "wet": True},
        "blur": 6,
        "back": [
            {"preset": "latin", "rows": 3, "cols": 15, "x0": 0.0, "x1": 1.0,
             "yFront": 0.53, "yBack": 0.40, "hFront": 0.12, "hBack": 0.07,
             "flip": True, "march": 0.55}
        ],
        "people": [
            {"preset": "consul", "x": 0.48, "y": 0.79, "h": 0.43,
             "face": "pain", "pose": "kneel", "fall": 1.05, "tremble": True}
        ],
        "props": [
            {"kind": "shield", "type": "scutum", "color": ROMAN,
             "charge": "eagle", "chargeColor": GOLD, "x": 0.76, "y": 0.87,
             "s": 0.24, "rot": 0.45, "at": 0.4, "anim": "drop"}
        ],
        "fx": [{"kind": "dust", "x": 0.51, "y": 0.79, "n": 9, "a": 0.4}],
        "move": "in", "moveAmt": 0.04, "vignette": 0.28
    }}

for index, shot in enumerate(shots):
    source = source_rows[index]
    line = clean(source.get("text", shot.get("line", "")))
    fragment = clean(shot.get("line", ""))
    sub_index = beat_index(index, source)
    shot["source_line_id"] = source["id"]
    shot["caption_text"] = shot.get("line", "")
    shot["in"] = {"type": "cut"}
    shot["sfx"] = []
    shot["notes"] = ""

    if "cavalry fight" in line or "cavalry clash" in line:
        shot.update(battle_scene(action="impact", horse=True, pair=True, face="shout"))
        shot["sfx"] = [
            {"name": "hooves_gallop", "at": 0.0, "gain": -2},
            {"name": "sword_clash", "at": 0.45, "gain": -4},
            {"name": "battle_roar", "at": 0.6, "gain": -9}
        ]
    elif "survives it" in line or "roman consul" in line or "lucius aemilius" in line:
        shot.update(close("determined", move="in", R=0.145, y=0.445,
                          signs=[{"text": "PAULLUS", "x": 0.50, "y": 0.13, "at": 0.2, "size": 43}]))
    elif "rides into the centre" in line or "rides toward the infantry" in line or "he rode toward" in line:
        if "hannibal's trap" in line and sub_index > 0:
            shot.update(top_centre("trap"))
        else:
            shot.update(battle_scene(action="right", horse=True, face="determined"))
            shot["args"]["signs"] = [{"text": "INTO THE CENTRE", "x": 0.50, "y": 0.13, "at": 0.25, "size": 40}]
            shot["sfx"] = [
                {"name": "hooves_gallop", "at": 0.0, "gain": -2},
                {"name": "war_horn", "at": 0.45, "gain": -9}
            ]
    elif "august second" in line or "two hundred and sixteen" in line:
        shot.update({"tpl": "title", "args": {
            "text": "CANNAE\n216 BCE", "sub": "2 AUGUST 216 BCE",
            "bg": "plain", "time": "golden", "dim": 0.12, "y": 0.40,
            "size": 118
        }})
        shot["sfx"] = [{"name": "drum_hit", "at": 0.15, "gain": -7}]
    elif "near cannae" in line or "southern italy" in line or "faces hannibal" in line:
        shot.update({"tpl": "map", "args": {
            "view": [10.8, 39.5, 17.1, 43.2],
            "places": [
                {"text": "ROME", "lon": 12.496, "lat": 41.903, "at": 0.1, "dx": 0.025, "size": 42},
                {"text": "CANNAE", "lon": 15.59, "lat": 41.31, "at": 0.55, "dx": -0.015, "dy": 0.01, "size": 42},
                {"text": "AUFIDUS", "lon": 15.63, "lat": 41.35, "at": 1.0, "dx": 0.06, "dy": 0.045, "size": 34}
            ],
            "routes": [
                {"pts": [[12.496, 41.903], [13.9, 41.7], [15.59, 41.31]], "at": 0.8, "dur": 1.1, "color": ROMAN}
            ],
            "troops": [{"lon": 15.59, "lat": 41.31, "side": "red", "at": 1.35, "n": 6}],
            "move": "in", "moveAmt": 0.035
        }})
        shot["sfx"] = [{"name": "page_turn", "at": 0.0, "gain": -8}]
    elif "rome's right" in line or "roman right" in line:
        shot.update(battle_scene(action="right", horse=True, face="determined"))
        shot["args"]["signs"] = [{"text": "ROMAN RIGHT", "x": 0.50, "y": 0.13, "at": 0.2, "size": 42}]
        shot["sfx"] = [{"name": "hooves_gallop", "at": 0.0, "gain": -5}]
    elif "decisive struggle" in line or "forming in the centre" in line:
        shot.update(top_centre("push"))
        shot["args"]["signs"] = [{"text": "THE CENTRE", "x": 0.50, "y": 0.13, "at": 0.2, "size": 42}]
    elif "roman infantry pushes" in line or "pushes forward" in line:
        shot.update({"tpl": "army", "args": {
            "bg": "plain", "time": "golden",
            "mid": [
                {"preset": "hastatus", "rows": 6, "cols": 11, "x0": 0.05, "x1": 0.95,
                 "yFront": 0.61, "yBack": 0.43, "hFront": 0.16, "hBack": 0.08,
                 "march": 1.1, "advance": 0.025,
                 "flags": [{"col": 0.28, "row": 0.78, "kind": "eagle", "color": GOLD}]}
            ],
            "back": [
                {"preset": "latin", "rows": 4, "cols": 17, "x0": 0.0, "x1": 1.0,
                 "yFront": 0.42, "yBack": 0.30, "hFront": 0.08, "hBack": 0.05,
                 "flip": True, "march": 0.35}
            ],
            "move": "in", "moveAmt": 0.035
        }})
        shot["sfx"] = [
            {"name": "drum_march", "at": 0.0, "gain": -7},
            {"name": "battle_far", "at": 0.2, "gain": -12}
        ]
    elif "hannibal's centre gives ground" in line or "centre gives ground" in line:
        shot.update(top_centre("bend"))
        shot["sfx"] = [{"name": "battle_roar", "at": 0.15, "gain": -10}]
    elif "romans surge deeper" in line or "surge deeper" in line:
        shot.update({"tpl": "army", "args": {
            "bg": "plain", "time": "golden",
            "mid": [
                {"preset": "hastatus", "rows": 6, "cols": 12, "x0": 0.02, "x1": 0.98,
                 "yFront": 0.63, "yBack": 0.43, "hFront": 0.17, "hBack": 0.09,
                 "march": 1.2, "advance": 0.03}
            ],
            "back": [
                {"preset": "latin", "rows": 3, "cols": 18, "x0": 0.0, "x1": 1.0,
                 "yFront": 0.42, "yBack": 0.30, "hFront": 0.08, "hBack": 0.05,
                 "flip": True, "march": 0.25}
            ],
            "move": "in", "moveAmt": 0.04
        }})
    elif "turns inward from both wings" in line or "both wings" in line:
        shot.update(top_centre("inward"))
        shot["sfx"] = [{"name": "shield_bash", "at": 0.5, "gain": -7}]
    elif "flanks are exposed" in line or "flanks exposed" in line:
        shot.update(top_centre("inward"))
        shot["args"]["marks"] = [
            {"kind": "circle", "x": 0.31, "y": 0.59, "r": 0.09, "at": 0.2},
            {"kind": "circle", "x": 0.69, "y": 0.59, "r": 0.09, "at": 0.45}
        ]
    elif "could remain on the right" in line:
        shot.update(close("worried", move="still", R=0.145, y=0.445,
                          signs=[{"text": "HOLD THE RIGHT?", "x": 0.50, "y": 0.13, "at": 0.2, "size": 37}]))
    elif "battle will be decided" in line:
        shot.update(battle_scene(action="push", horse=False))
        shot["args"]["signs"] = [{"text": "THE CENTRE", "x": 0.50, "y": 0.13, "at": 0.2, "size": 42}]
    elif "hannibal is fighting" in line or "hannibal" in line and "centre too" in line:
        shot.update(close("determined", preset="greek", move="in", R=0.14, y=0.445,
                          signs=[{"text": "HANNIBAL", "x": 0.50, "y": 0.13, "at": 0.2, "size": 44}]))
    elif "cavalry strikes the roman rear" in line or "roman rear" in line:
        shot.update(battle_scene(action="impact", horse=True, rider_preset="greek",
                                 horse_color="bay", cloth_color=CARTHAGE, face="angry"))
        shot["args"]["signs"] = [{"text": "THE REAR", "x": 0.50, "y": 0.13, "at": 0.2, "size": 42}]
        shot["sfx"] = [
            {"name": "hooves_gallop", "at": 0.0, "gain": -3},
            {"name": "battle_roar", "at": 0.35, "gain": -8}
        ]
    elif "legions are trapped" in line or "packed ranks" in line:
        shot.update(top_centre("trap"))
        shot["args"]["marks"] = [{"kind": "circle", "x": 0.50, "y": 0.61, "r": 0.23, "at": 0.3}]
    elif "ranks fall" in line or "circle contracts" in line:
        shot.update(top_centre("trap"))
        shot["args"]["marks"] = [{"kind": "circle", "x": 0.50, "y": 0.61, "r": 0.23, "at": 0.2}]
    elif "falls in the thick" in line or "covered with wounds" in line or "severe wounds" in line:
        shot.update(paullus_fall_scene())
        shot["notes"] = "DROP"
        shot["sfx"] = [{"name": "sting_low", "at": 0.45, "gain": -5}]
    elif "did not ride toward safety" in line or "toward safety" in line:
        shot.update(close("determined", move="still", R=0.145, y=0.445))
        shot["notes"] = "DROP"
    elif "trap was closing around him" in line or "hannibal's trap" in line:
        shot.update(top_centre("trap"))
        shot["args"]["marks"] = [{"kind": "circle", "x": 0.50, "y": 0.61, "r": 0.24, "at": 0.25}]
    elif "point where rome needed him most" in line or "rome needed him most" in line:
        shot.update(battle_scene(action="right", horse=True, face="determined"))
        shot["sfx"] = [{"name": "hooves_walk", "at": 0.0, "gain": -7}]
    else:
        # Fallback still preserves the subject and moves the camera; it avoids a generic tactical plate.
        if index % 3 == 0:
            shot.update(close("determined", R=0.14))
        elif index % 3 == 1:
            shot.update(battle_scene(action="push", horse=False))
        else:
            shot.update(top_centre("push"))

    shot["args"] = shot.get("args") or {}
    if sub_index > 0:
        shot["args"]["move"] = "left" if sub_index % 2 else "in"
        shot["args"]["moveAmt"] = 0.035
    else:
        shot["args"].setdefault("move", "in")
        shot["args"].setdefault("moveAmt", 0.03)

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
cfg["captionStyle"] = "squire"
cfg["music"] = {"enabled": True, "gainDb": -13}
cfg["sfx"] = {"enabled": True, "gainDb": -4}
cfg["loudness"] = -14
cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
invalid = [shot["id"] for shot in shots if not shot.get("tpl") or not isinstance(shot.get("args"), dict)]
if invalid:
    raise SystemExit("Shots without a valid visual template: " + ", ".join(invalid))
stats = {}
for shot in shots:
    stats[shot["tpl"]] = stats.get(shot["tpl"], 0) + 1
print(f"Authored {len(shots)} Squire shots, {duration:.2f}s, 9:16 @24fps.")
print("Template distribution: " + ", ".join(f"{key}={value}" for key, value in sorted(stats.items())))
