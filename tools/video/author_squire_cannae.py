#!/usr/bin/env python3
"""Author a historically cautious, visually varied Squire storyboard from real voice timings."""
from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

PRESETS = ("hastatus", "princeps", "triarius", "latin", "latinOld", "velites", "legionary", "senator", "consul")
VALID_TEMPLATES = {"scene", "close", "army", "top", "plan", "map", "board", "item", "split", "title", "black"}
ROMAN = "#9f4037"
CARTHAGE = "#3e5e82"
PAPER = "#d7c39b"


def load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def choose_template(text: str, index: int, progress: float, usage=None, last_at=None, last_template=None) -> str:
    """Choose a varied template with deliberate caps for repeated visual devices."""
    t = text.casefold()
    usage = usage or {}
    last_at = last_at or {}

    def available(name: str, cap: int, gap: int = 3) -> bool:
        return usage.get(name, 0) < cap and index - last_at.get(name, -999) >= gap and last_template != name

    if index == 0:
        return "title"

    geo = any(k in t for k in ("cannae", "apulia", "aufidus", "canusium", "southern italy", "river"))
    if geo and available("map", 2, 12):
        if (usage.get("map", 0) == 0 and progress < 0.30) or (usage.get("map", 0) == 1 and progress > 0.88):
            return "map"

    number_or_force = any(k in t for k in (
        "eighty thousand", "forty thousand", "six thousand", "ten thousand",
        "far more infantry", "more cavalry", "more infantry"
    ))
    if number_or_force and available("board", 2, 5):
        return "board"

    tactical = any(k in t for k in (
        "crescent", "double envelopment", "encirclement", "surrounded",
        "both flanks", "flanks", "folding inward", "folds inward",
        "give ground", "giving ground", "the centre", "the center",
        "the wings", "the rear"
    ))
    if tactical and available("top", 7, 4):
        return "top"

    if any(k in t for k in ("tactical victory", "strategic outcome", "the lesson", "remember one rule", "remember the rule")) and available("plan", 4, 5):
        return "plan"

    comparison = any(k in t for k in ("not one uniform block", "mixed force", "bigger hammer", "shape that can turn", "two different"))
    if comparison and available("split", 6, 4):
        return "split"

    if any(k in t for k in ("horsemen", "numidian", "hooves", "horse", "gallop", "riders")):
        return "scene"
    if "cavalry" in t and available("army", 26, 2):
        return "army"

    if any(k in t for k in ("hannibal", "varro", "paullus", "consul", "polybius")) and available("close", 16, 4):
        return "close"

    if any(k in t for k in ("shield", "spear", "weapon", "sword", "standard", "standards")) and available("item", 4, 6):
        return "item"

    if any(k in t for k in ("dead", "died", "wounded", "killed", "catastrophic", "disaster")):
        return "scene"

    sequence = ("scene", "army", "close", "scene", "split", "army", "plan", "scene", "top", "scene")
    choice = sequence[index % len(sequence)]
    if choice == last_template:
        choice = "scene" if last_template != "scene" else "army"
    return choice
def base_args(tpl: str, text: str, index: int, progress: float, sfx_root: Path) -> tuple[dict, list[dict]]:
    low = text.casefold()
    seed = index * 7919 + 216
    rng = random.Random(seed)
    time_of_day = "golden" if progress < 0.35 else ("day" if progress < 0.7 else "sunset")
    cues: list[dict] = []

    def cue(*names: str, gain: int = -10, at: float = 0.25):
        for name in names:
            if (sfx_root / f"{name}.wav").is_file():
                cues.append({"name": name, "at": at, "gain": gain})
                return

    if tpl == "map":
        args = {
            "view": [11.0, 39.5, 18.2, 43.3],
            "places": [
                {"text": "Rome", "lon": 12.496, "lat": 41.902},
                {"text": "Cannae", "lon": 16.13, "lat": 41.305},
                {"text": "Canusium", "lon": 16.07, "lat": 41.22},
                {"text": "Aufidus", "lon": 16.22, "lat": 41.26},
            ],
            "routes": [
                {"pts": [[14.85, 41.1], [15.35, 41.18], [15.8, 41.27], [16.13, 41.305]], "at": "Cannae", "dur": 1.3}
            ],
            "troops": [
                {"lon": 16.12, "lat": 41.34, "side": "red", "at": 0.2},
                {"lon": 16.18, "lat": 41.2, "side": "blue", "at": 0.8},
            ],
        }
        cue("page_turn", "sting_low", at=0.1)
    elif tpl == "board":
        if "cavalry" in low or "horse" in low:
            args = {
                "title": "CAVALRY",
                "bars": [
                    {"label": "ROME", "v": 0.62, "top": "≈6,000", "at": 0.2},
                    {"label": "CARTHAGE", "v": 1.0, "top": "≈10,000", "at": 0.7},
                ],
                "mult": {"text": "THE EDGE", "x": 0.5, "y": 0.34, "at": 0.9},
                "labels": [{"text": "POLYBIUS' ESTIMATE", "x": 0.5, "y": 0.2, "size": 30, "at": 0.2, "color": "#f0d9c8"}],
            }
        else:
            args = {
                "title": "INFANTRY",
                "bars": [
                    {"label": "ROME", "v": 1.0, "top": "≈80,000", "at": 0.2},
                    {"label": "CARTHAGE", "v": 0.5, "top": "≈40,000", "at": 0.7},
                ],
                "mult": {"text": "MORE MEN", "x": 0.5, "y": 0.34, "at": 0.9},
                "labels": [{"text": "POLYBIUS' ESTIMATE", "x": 0.5, "y": 0.2, "size": 30, "at": 0.2, "color": "#f0d9c8"}],
            }
        cue("drum_hit", "sting_low", at=0.15)
    elif tpl == "top":
        args = {
            "ground": {"color": "#c9ad7a", "grass": True, "rocks": True},
            "blocks": [
                {"x": 0.64, "y": 0.5, "w": 0.22, "h": 0.34, "cols": 10, "rows": 16, "cell": 0.016, "side": "red", "face": -1},
                {"x": 0.4, "y": 0.5, "w": 0.2, "h": 0.12, "cols": 9, "rows": 5, "cell": 0.018, "side": "blue", "face": 1, "path": [[0, 0.4, 0.5], [1.6, 0.49, 0.5]]},
                {"x": 0.34, "y": 0.27, "w": 0.17, "h": 0.1, "cols": 7, "rows": 4, "cell": 0.018, "side": "blue", "face": 1, "path": [[0, 0.34, 0.27], [2, 0.54, 0.32]]},
                {"x": 0.34, "y": 0.73, "w": 0.17, "h": 0.1, "cols": 7, "rows": 4, "cell": 0.018, "side": "blue", "face": 1, "path": [[0, 0.34, 0.73], [2, 0.54, 0.68]]},
            ],
            "zones": [
                {"x": 0.59, "y": 0.5, "w": 0.26, "h": 0.47, "color": "#8d382f", "at": 0.2, "dur": 0.5, "dashed": True},
            ],
            "arrows": [
                {"from": [0.49, 0.29], "to": [0.58, 0.4], "at": 0.9, "color": CARTHAGE},
                {"from": [0.49, 0.71], "to": [0.58, 0.6], "at": 1.4, "color": CARTHAGE},
            ],
        }
        if any(k in low for k in ("both flanks", "encirclement", "surrounded", "enclosure", "rear")):
            args["blocks"] = [
                {"x": 0.5, "y": 0.5, "w": 0.26, "h": 0.48, "cols": 9, "rows": 16, "cell": 0.016, "side": "red", "face": -1},
                {"x": 0.23, "y": 0.5, "w": 0.17, "h": 0.42, "cols": 6, "rows": 14, "cell": 0.018, "side": "blue", "face": 1, "path": [[0, 0.23, 0.5], [2.0, 0.39, 0.5]]},
                {"x": 0.77, "y": 0.5, "w": 0.17, "h": 0.42, "cols": 6, "rows": 14, "cell": 0.018, "side": "blue", "face": -1, "path": [[0, 0.77, 0.5], [2.0, 0.61, 0.5]]},
                {"x": 0.5, "y": 0.15, "w": 0.3, "h": 0.1, "cols": 10, "rows": 3, "cell": 0.018, "side": "blue", "face": -1, "path": [[0, 0.5, 0.15], [2.0, 0.5, 0.32]]},
            ]
            args["arrows"] = [
                {"from": [0.23, 0.5], "to": [0.39, 0.5], "at": 0.5, "color": CARTHAGE},
                {"from": [0.77, 0.5], "to": [0.61, 0.5], "at": 0.9, "color": CARTHAGE},
                {"from": [0.5, 0.15], "to": [0.5, 0.32], "at": 1.3, "color": CARTHAGE},
            ]
        cue("battle_roar", "battle_far", at=0.45)
    elif tpl == "plan":
        args = {
            "paper": "parchment",
            "zones": [
                {"x": 0.5, "y": 0.5, "w": 0.5, "h": 0.52, "color": "#9e8b68", "at": 0.2, "dur": 0.7},
                {"x": 0.5, "y": 0.5, "w": 0.22, "h": 0.3, "color": "#456789", "at": 0.7, "dur": 0.7, "dashed": True},
            ],
            "blocks": [
                {"x": 0.25, "y": 0.43, "w": 0.12, "h": 0.2, "side": "blue", "cols": 5, "rows": 8, "at": 0.25},
                {"x": 0.5, "y": 0.4, "w": 0.16, "h": 0.12, "side": "blue", "cols": 7, "rows": 4, "at": 0.5},
                {"x": 0.75, "y": 0.43, "w": 0.12, "h": 0.2, "side": "blue", "cols": 5, "rows": 8, "at": 0.75},
            ],
            "arrows": [
                {"from": [0.83, 0.4], "to": [0.61, 0.45], "at": 1.0, "color": CARTHAGE},
                {"from": [0.83, 0.6], "to": [0.61, 0.55], "at": 1.4, "color": CARTHAGE},
            ],
            "labels": [
                {"text": "FLEXIBLE CENTRE", "x": 0.5, "y": 0.19, "size": 52, "at": 0.4, "color": "#2a2117"},
                {"text": "WINGS", "x": 0.79, "y": 0.78, "size": 38, "at": 1.2, "color": "#2a2117"},
            ],
        }
        cue("page_turn", "drum_hit", at=0.1)
    elif tpl == "army":
        args = {
            "preset": "hastatus" if index % 2 else "latin",
            "presets": ["hastatus", "princeps", "triarius"],
            "rows": 4 if index % 2 else 3,
            "cols": 10 if index % 2 else 8,
            "march": 0.55,
            "flip": bool(index % 2),
            "face": "determined",
            "flags": [{"col": 0.5, "row": 0.8, "kind": "eagle", "color": ROMAN if index % 2 else CARTHAGE}],
            "enemy": "latin" if index % 2 else "hastatus",
            "bg": "plain",
            "bgOpts": {"volcano": False},
            "time": time_of_day,
            "move": "right",
        }
        cue("drum_march", "battle_far", at=0.35)
    elif tpl == "close":
        if any(k in low for k in ("hannibal", "carthaginian", "african", "iberian", "gallic", "numidian")):
            preset = "latinOld"  # blue-side generic commander, not authenticated Punic costume
        elif any(k in low for k in ("consul", "paullus", "varro")):
            preset = "consul"
        elif "polybius" in low:
            preset = "senator"
        else:
            preset = "hastatus"
        face = "worried" if any(k in low for k in ("trapped", "fear", "wounded", "crush", "confusing", "surrounded", "no clear front")) else "determined"
        pose = "point" if any(k in low for k in ("places", "shows", "orders", "points")) else ("push" if any(k in low for k in ("push", "advance", "press")) else "guard")
        others = [
            {"preset": "princeps", "x": 0.15, "y": 0.67, "R": 0.13, "face": "worried"},
            {"preset": "triarius", "x": 0.85, "y": 0.67, "R": 0.13, "face": "determined"},
        ]
        if "hannibal" in low:
            others = [{"preset": "latin", "x": 0.18, "y": 0.67, "R": 0.14, "face": "calm"}]
        args = {
            "preset": preset,
            "face": face,
            "pose": pose,
            "bg": "plain",
            "bgOpts": {"volcano": False},
            "time": time_of_day,
            "R": 0.23 + (0.01 if index % 2 else 0),
            "x": 0.46 if index % 3 else 0.55,
            "y": 0.52,
            "others": others,
            "fx": [{"kind": "dust", "at": 0.5}] if progress > 0.35 else [],
        }
        cue("armor_clank", "chainmail", at=0.3)
    elif tpl == "item":
        thing = "shield" if "shield" in low else ("spear" if "spear" in low else ("standard" if "standard" in low else "sword"))
        args = {
            "thing": {"kind": thing, "type": "scutum" if thing == "shield" else None, "s": 0.58, "anim": "grow" if index % 2 else "pop"},
            "props": [{"kind": "spear", "x": 0.22, "y": 0.76, "s": 0.22, "rot": -0.25}],
            "bg": "plain",
            "bgOpts": {"volcano": False},
            "time": time_of_day,
            "sway": True,
        }
        cue("sword_draw", "shield_bash", "armor_clank", at=0.35)
    elif tpl == "split":
        args = {
            "left": {
                "color": ROMAN,
                "people": [{"preset": "hastatus", "x": 0.26, "h": 0.62, "face": "determined", "pose": "push", "weapon": "pilum"}],
            },
            "right": {
                "color": CARTHAGE,
                "people": [{"preset": "latin", "x": 0.74, "h": 0.62, "face": "calm", "pose": "guard", "weapon": "spear", "flip": True}],
            },
            "labels": [
                {"text": "ROME", "x": 0.24, "y": 0.16, "size": 62, "at": 0.2},
                {"text": "CARTHAGE", "x": 0.75, "y": 0.16, "size": 54, "at": 0.7},
            ],
        }
        cue("sting_low", "war_horn", at=0.3)
    elif tpl == "title":
        args = {"text": "CANNAE\n216 BC", "sub": "THE TRAP THAT BEAT ROME", "bg": "plain", "bgOpts": {"volcano": False}, "time": "sunset", "dim": 0.15}
        cue("war_horn", "drum_hit", at=0.15)
    elif tpl == "black":
        args = {}
    else:
        carthage_focus = any(k in low for k in ("hannibal", "carthaginian", "african", "iberian", "gallic", "numidian"))
        roman_lead = {"preset": "hastatus", "x": 0.30 + (0.04 if index % 2 else 0), "h": 0.61, "face": "worried" if progress > 0.62 else "determined", "pose": "guard" if index % 3 else "push", "weapon": "pilum"}
        blue_lead = {"preset": "latinOld" if carthage_focus else "latin", "x": 0.70 - (0.04 if index % 2 else 0), "h": 0.58, "face": "determined" if progress < 0.7 else "worried", "pose": "stand" if index % 3 else "guard", "weapon": "spear", "flip": True}
        people = [blue_lead, roman_lead] if carthage_focus else [roman_lead, blue_lead]
        back_preset = "latin" if carthage_focus else "hastatus"
        args = {
            "bg": "plain",
            "time": time_of_day,
            "bgOpts": {"volcano": False, "trees": 3, "bushes": 5, "tents": 2, "flags": [{"x": 0.18, "color": ROMAN}, {"x": 0.82, "color": CARTHAGE}]},
            "back": [
                {"preset": back_preset, "rows": 2 + (index % 2), "cols": 9 + (index % 4), "x0": 0.04, "x1": 0.94, "yFront": 0.84, "yBack": 0.68, "hFront": 0.14, "hBack": 0.08, "advance": 0.003 + (0.001 if index % 2 else 0), "face": "determined", "weapon": "pilum" if not carthage_focus else "spear"},
            ],
            "people": people,
            "move": ("in" if index % 3 else "left") if progress < 0.72 else ("left" if index % 2 else "in"),
            "fx": [{"kind": "dust", "at": 0.5}] if progress > 0.25 else [],
        }
        if any(k in low for k in ("horse", "cavalry", "gallop", "horsemen", "numidian")):
            people[0 if carthage_focus else 1]["horse"] = {"color": "bay" if carthage_focus else "chestnut", "gait": "gallop"}
            cue("hooves_gallop", "horse_neigh", at=0.3)
        elif any(k in low for k in ("sword", "clash", "fight", "battle")):
            cue("sword_clash", "battle_far", at=0.4)
        elif any(k in low for k in ("drum", "march", "advance")):
            cue("drum_march", "war_horn", at=0.2)
        else:
            cue("battle_far", "wind_loop", at=0.2)

    if tpl not in VALID_TEMPLATES:
        raise ValueError(f"Unsupported Squire template: {tpl}")
    return args, cues[:1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    project = Path(args.project).resolve()
    shots_path = project / "story" / "shots.json"
    story = load(shots_path, {})
    shots = story.get("shots") or []
    if len(shots) < 20:
        raise ValueError(f"Voice-timed draft produced only {len(shots)} shots; expected a long-form sequence")
    duration = float(story.get("duration") or shots[-1]["end"])
    sfx_root = project.parents[1] / "audio" / "sfx"
    usage: dict[str, int] = {}
    last_at: dict[str, int] = {}
    last_template = None
    for index, shot in enumerate(shots):
        text = str(shot.get("line") or "")
        start, end = float(shot["start"]), float(shot["end"])
        if end <= start:
            raise ValueError(f"Non-positive shot duration in {shot.get('id')}")
        progress = ((start + end) / 2) / max(duration, 0.001)
        tpl = choose_template(text, index, progress, usage, last_at, last_template)
        visual, cues = base_args(tpl, text, index, progress, sfx_root)
        usage[tpl] = usage.get(tpl, 0) + 1
        last_at[tpl] = index
        last_template = tpl
        shot["tpl"] = tpl
        shot["args"] = visual
        shot["sfx"] = cues
        shot["notes"] = "Historical reconstruction; Squire generic ancient presets are visual shorthand, not authenticated uniforms."
        shot["in"] = {"type": "fade" if index == 0 else "cut"}
    # Keep a restrained, readable long-form score arc; all beds are generated by Squire's own audio pack.
    story["music"] = [
        {"start": 0, "end": round(duration * 0.14, 3), "bed": "ancient", "gainDb": -1},
        {"start": round(duration * 0.14, 3), "end": round(duration * 0.34, 3), "bed": "roman", "gainDb": 0},
        {"start": round(duration * 0.34, 3), "end": round(duration * 0.5, 3), "bed": "suspense", "gainDb": -1},
        {"start": round(duration * 0.5, 3), "end": round(duration * 0.76, 3), "bed": "war", "gainDb": 0},
        {"start": round(duration * 0.76, 3), "end": round(duration * 0.91, 3), "bed": "somber", "gainDb": -2},
        {"start": round(duration * 0.91, 3), "end": round(duration, 3), "bed": "mystery", "gainDb": -1},
    ]
    story["title"] = "How Hannibal Turned Rome's Army Into a Trap"
    story["genre"] = "historical-military-animation"
    story["engine"] = "Squire 2D/vector"
    story["historical_caution"] = "Force strengths and casualty totals are ancient estimates; tactical formation is an explanatory reconstruction."
    story["shots"] = shots
    shots_path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cfg_path = project / "config.json"
    cfg = load(cfg_path, {})
    cfg.update({
        "title": "How Hannibal Turned Rome's Army Into a Trap",
        "aspect": "16:9",
        "resolution": "1080p",
        "fps": 24,
        "style": "flat",
        "captions": False,
        "bars": "none",
        "pack": "squire",
        "lang": "en",
        "music": {"enabled": True, "gainDb": -13},
        "sfx": {"enabled": True, "gainDb": -7},
        "loudness": -14,
        "duration": round(duration, 3),
    })
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    templates = {shot["tpl"] for shot in shots}
    if len(templates) < 7:
        raise ValueError(f"Storyboard has only {len(templates)} visual templates: {sorted(templates)}")
    print(f"Authored {len(shots)} timed Squire shots across {len(templates)} templates; duration={duration:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
