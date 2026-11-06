#!/usr/bin/env python3
"""Author context-specific, visually varied Cannae scenes from the measured voice timeline."""
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
    """Choose a varied template while protecting story beats from repetitive visual devices."""
    t = text.casefold()
    usage = usage or {}
    last_at = last_at or {}

    def available(name: str, cap: int, gap: int = 4) -> bool:
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
    if number_or_force and available("board", 2, 7):
        return "board"

    tactical = any(k in t for k in (
        "crescent", "double envelopment", "encirclement", "surrounded",
        "both flanks", "flanks", "folding inward", "folds inward",
        "give ground", "giving ground", "the centre", "the center",
        "the wings", "the rear"
    ))
    if tactical and available("top", 5, 7):
        return "top"

    if any(k in t for k in ("tactical victory", "strategic outcome", "the lesson", "remember one rule", "remember the rule")) and available("plan", 3, 8):
        return "plan"

    comparison = any(k in t for k in ("not one uniform block", "mixed force", "bigger hammer", "shape that can turn", "two different"))
    if comparison and available("split", 3, 10):
        return "split"

    if any(k in t for k in ("shield", "spear", "weapon", "sword", "standard", "standards")) and available("item", 7, 5):
        return "item"

    if any(k in t for k in ("hannibal", "varro", "paullus", "consul", "polybius")) and available("close", 12, 5):
        return "close"

    if any(k in t for k in ("horsemen", "numidian", "hooves", "horse", "gallop", "riders")):
        return "scene"
    if "cavalry" in t and available("army", 16, 4):
        return "army"

    if any(k in t for k in ("dead", "died", "wounded", "killed", "catastrophic", "disaster")):
        return "scene"

    sequence = ("scene", "army", "item", "scene", "close", "plan", "army", "scene", "top", "item", "scene", "split")
    choice = sequence[index % len(sequence)]
    if choice == last_template:
        choice = "scene" if last_template != "scene" else "army"
    if choice == "top" and not available("top", 5, 7):
        choice = "scene"
    if choice == "split" and not available("split", 3, 10):
        choice = "scene"
    if choice == "plan" and not available("plan", 3, 8):
        choice = "scene"
    if choice == "item" and not available("item", 7, 5):
        choice = "scene"
    if choice == "army" and not available("army", 16, 4):
        choice = "scene"
    if choice == "close" and not available("close", 12, 5):
        choice = "scene"
    return choice


def base_args(def base_args(tpl: str, text: str, index: int, progress: float, sfx_root: Path) -> tuple[dict, list[dict]]:
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
        base = {
            "ground": {"color": "#c9ad7a" if index % 2 else "#b99c70", "grass": True, "rocks": True},
            "blocks": [],
            "zones": [],
            "arrows": [],
        }
        envelopment = any(k in low for k in ("both flanks", "encirclement", "surrounded", "enclosure", "rear", "double envelopment"))
        yielding = any(k in low for k in ("crescent", "give ground", "giving ground", "folding inward", "folds inward", "centre", "center"))
        if envelopment:
            variant = index % 3
            if variant == 0:
                base["blocks"] = [
                    {"x": 0.5, "y": 0.5, "w": 0.26, "h": 0.48, "cols": 9, "rows": 16, "cell": 0.016, "side": "red", "face": -1},
                    {"x": 0.23, "y": 0.5, "w": 0.17, "h": 0.42, "cols": 6, "rows": 14, "cell": 0.018, "side": "blue", "face": 1, "path": [[0, 0.23, 0.5], [2.0, 0.39, 0.5]]},
                    {"x": 0.77, "y": 0.5, "w": 0.17, "h": 0.42, "cols": 6, "rows": 14, "cell": 0.018, "side": "blue", "face": -1, "path": [[0, 0.77, 0.5], [2.0, 0.61, 0.5]]},
                    {"x": 0.5, "y": 0.15, "w": 0.3, "h": 0.1, "cols": 10, "rows": 3, "cell": 0.018, "side": "blue", "face": -1, "path": [[0, 0.5, 0.15], [2.0, 0.5, 0.32]]},
                ]
                base["arrows"] = [
                    {"from": [0.23, 0.5], "to": [0.39, 0.5], "at": 0.5, "color": CARTHAGE},
                    {"from": [0.77, 0.5], "to": [0.61, 0.5], "at": 0.9, "color": CARTHAGE},
                    {"from": [0.5, 0.15], "to": [0.5, 0.32], "at": 1.3, "color": CARTHAGE},
                ]
            elif variant == 1:
                base["blocks"] = [
                    {"x": 0.5, "y": 0.52, "w": 0.32, "h": 0.48, "cols": 12, "rows": 18, "cell": 0.015, "side": "red", "face": -1},
                    {"x": 0.19, "y": 0.5, "w": 0.13, "h": 0.38, "cols": 6, "rows": 13, "cell": 0.018, "side": "blue", "path": [[0, 0.19, 0.5], [1.7, 0.37, 0.5]]},
                    {"x": 0.81, "y": 0.5, "w": 0.13, "h": 0.38, "cols": 6, "rows": 13, "cell": 0.018, "side": "blue", "path": [[0, 0.81, 0.5], [1.7, 0.63, 0.5]]},
                    {"x": 0.5, "y": 0.13, "w": 0.36, "h": 0.09, "cols": 12, "rows": 3, "cell": 0.018, "side": "blue"},
                ]
                base["arrows"] = [
                    {"from": [0.16, 0.5], "to": [0.37, 0.5], "at": 0.4, "color": CARTHAGE},
                    {"from": [0.84, 0.5], "to": [0.63, 0.5], "at": 0.8, "color": CARTHAGE},
                    {"from": [0.5, 0.12], "to": [0.5, 0.34], "at": 1.2, "color": CARTHAGE},
                ]
            else:
                base["blocks"] = [
                    {"x": 0.5, "y": 0.55, "w": 0.2, "h": 0.5, "cols": 8, "rows": 19, "cell": 0.016, "side": "red"},
                    {"x": 0.28, "y": 0.4, "w": 0.16, "h": 0.34, "cols": 7, "rows": 12, "cell": 0.018, "side": "blue", "path": [[0, 0.28, 0.4], [1.8, 0.43, 0.5]]},
                    {"x": 0.72, "y": 0.4, "w": 0.16, "h": 0.34, "cols": 7, "rows": 12, "cell": 0.018, "side": "blue", "path": [[0, 0.72, 0.4], [1.8, 0.57, 0.5]]},
                    {"x": 0.5, "y": 0.17, "w": 0.28, "h": 0.08, "cols": 10, "rows": 3, "cell": 0.018, "side": "blue"},
                ]
                base["arrows"] = [
                    {"from": [0.28, 0.35], "to": [0.42, 0.5], "at": 0.45, "color": CARTHAGE},
                    {"from": [0.72, 0.35], "to": [0.58, 0.5], "at": 0.85, "color": CARTHAGE},
                ]
            base["zones"] = [{"x": 0.5, "y": 0.5, "w": 0.58, "h": 0.62, "color": "#8d382f", "at": 0.2, "dur": 0.55, "dashed": True}]
        elif yielding:
            base["blocks"] = [
                {"x": 0.5, "y": 0.43, "w": 0.34, "h": 0.18, "cols": 15, "rows": 6, "cell": 0.017, "side": "blue", "path": [[0, 0.5, 0.43], [1.6, 0.5, 0.55]]},
                {"x": 0.5, "y": 0.75, "w": 0.2, "h": 0.28, "cols": 10, "rows": 9, "cell": 0.018, "side": "red", "path": [[0, 0.5, 0.75], [1.6, 0.5, 0.57]]},
                {"x": 0.21, "y": 0.54, "w": 0.15, "h": 0.24, "cols": 6, "rows": 8, "cell": 0.018, "side": "blue"},
                {"x": 0.79, "y": 0.54, "w": 0.15, "h": 0.24, "cols": 6, "rows": 8, "cell": 0.018, "side": "blue"},
            ]
            base["arrows"] = [
                {"from": [0.5, 0.78], "to": [0.5, 0.59], "at": 0.45, "color": ROMAN},
                {"from": [0.23, 0.52], "to": [0.38, 0.57], "at": 1.0, "color": CARTHAGE},
                {"from": [0.77, 0.52], "to": [0.62, 0.57], "at": 1.35, "color": CARTHAGE},
            ]
            base["zones"] = [{"x": 0.5, "y": 0.5, "w": 0.7, "h": 0.48, "color": "#456789", "at": 0.2, "dur": 0.7, "dashed": True}]
        else:
            base["blocks"] = [
                {"x": 0.68, "y": 0.5, "w": 0.17, "h": 0.44, "cols": 8, "rows": 16, "cell": 0.017, "side": "red"},
                {"x": 0.33, "y": 0.5, "w": 0.23, "h": 0.18, "cols": 11, "rows": 6, "cell": 0.018, "side": "blue"},
                {"x": 0.27, "y": 0.28, "w": 0.15, "h": 0.1, "cols": 7, "rows": 4, "cell": 0.018, "side": "blue"},
                {"x": 0.27, "y": 0.72, "w": 0.15, "h": 0.1, "cols": 7, "rows": 4, "cell": 0.018, "side": "blue"},
            ]
            base["arrows"] = [{"from": [0.44, 0.5], "to": [0.56, 0.5], "at": 0.8, "color": ROMAN}]
        base["labels"] = [{"text": "CARTHAGE", "x": 0.24, "y": 0.1, "size": 34, "at": 0.35, "color": CARTHAGE}, {"text": "ROME", "x": 0.76, "y": 0.1, "size": 34, "at": 0.65, "color": ROMAN}]
        args = base
        cue("battle_roar", "battle_far", at=0.45)
    elif tpl == "plan":    elif tpl == "plan":
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
        carthage_focus = any(k in low for k in ("hannibal", "carthaginian", "african", "iberian", "gallic", "numidian"))
        if "cavalry" in low or any(k in low for k in ("horse", "riders", "numidian")):
            args = {
                "bg": "hills" if index % 2 else "field",
                "bgOpts": {"volcano": False, "trees": 2, "flags": [{"x": 0.16, "color": ROMAN}, {"x": 0.84, "color": CARTHAGE}]},
                "time": time_of_day,
                "mid": [
                    {"preset": "latinOld" if carthage_focus else "hastatus", "rows": 2, "cols": 8, "x0": 0.03, "x1": 0.46, "yFront": 0.95, "yBack": 0.78, "hFront": 0.25, "hBack": 0.12, "march": 0.4, "flip": False, "face": "determined"},
                    {"preset": "latin" if carthage_focus else "princeps", "rows": 2, "cols": 7, "x0": 0.54, "x1": 0.97, "yFront": 0.9, "yBack": 0.75, "hFront": 0.23, "hBack": 0.12, "march": 0.35, "flip": True, "face": "determined"},
                ],
                "people": [
                    {"preset": "latinOld" if carthage_focus else "hastatus", "x": 0.30, "y": 0.67, "h": 0.39, "pose": "guard", "horse": {"color": "bay" if carthage_focus else "chestnut", "gait": "gallop", "travel": False}, "flip": False},
                    {"preset": "latin" if carthage_focus else "princeps", "x": 0.72, "y": 0.7, "h": 0.34, "pose": "guard", "horse": {"color": "dark" if carthage_focus else "bay", "gait": "gallop", "travel": False}, "flip": True},
                ],
                "fx": [{"kind": "dust", "at": 0.2, "x": 0.5, "y": 0.82, "s": 0.18}],
            }
            cue("hooves_gallop", "horse_neigh", "battle_far", at=0.25)
        else:
            args = {
                "bg": "plain" if index % 3 == 0 else ("hills" if index % 3 == 1 else "field"),
                "bgOpts": {"volcano": False, "trees": 3 + index % 3, "bushes": 4, "tents": 2, "flags": [{"x": 0.12, "color": ROMAN}, {"x": 0.86, "color": CARTHAGE}]},
                "time": time_of_day,
                "mid": [
                    {"preset": "hastatus" if not carthage_focus else "latinOld", "presets": ["hastatus", "princeps", "triarius"] if not carthage_focus else ["latin", "latinOld"], "rows": 3 + index % 2, "cols": 10 + index % 4, "x0": 0.03, "x1": 0.49, "yFront": 0.98, "yBack": 0.7, "hFront": 0.31, "hBack": 0.1, "march": 0.35, "flip": False},
                    {"preset": "latinOld" if not carthage_focus else "hastatus", "presets": ["latin", "latinOld"] if not carthage_focus else ["hastatus", "princeps"], "rows": 2 + index % 2, "cols": 9 + index % 3, "x0": 0.53, "x1": 0.97, "yFront": 0.94, "yBack": 0.72, "hFront": 0.27, "hBack": 0.1, "march": 0.25, "flip": True},
                ],
                "move": ("left", "right", "in", "out")[index % 4],
                "face": "determined",
            }
            cue("drum_march", "battle_far", at=0.35)
    elif tpl == "close":
        carthage_focus = any(k in low for k in ("hannibal", "carthaginian", "african", "iberian", "gallic", "numidian"))
        if carthage_focus:
            preset = "latinOld"  # blue-side generic commander; illustrative rather than authenticated Punic dress
        elif any(k in low for k in ("consul", "paullus", "varro")):
            preset = "consul"
        elif "polybius" in low:
            preset = "senator"
        else:
            preset = "hastatus"
        face = "worried" if any(k in low for k in ("trapped", "fear", "wounded", "crush", "confusing", "surrounded", "no clear front")) else "determined"
        pose = "point" if any(k in low for k in ("places", "shows", "orders", "points")) else ("push" if any(k in low for k in ("push", "advance", "press")) else "guard")
        bg_kind = ("tent" if "camp" in low or "command" in low else ("hills" if index % 3 == 0 else "field"))
        opponent = "hastatus" if carthage_focus else "latinOld"
        args = {
            "preset": preset,
            "face": face,
            "pose": pose,
            "bg": bg_kind,
            "bgOpts": {"volcano": False, "trees": 2 + index % 3, "flags": [{"x": 0.14, "color": ROMAN}, {"x": 0.86, "color": CARTHAGE}], "tents": 2 if bg_kind == "tent" else 0},
            "time": time_of_day,
            "R": 0.24 + (0.015 if index % 2 else 0),
            "x": 0.43 if index % 3 else 0.55,
            "y": 0.51,
            "others": [
                {"preset": opponent, "x": 0.82 if index % 2 else 0.16, "y": 0.69, "R": 0.15, "face": "worried" if face == "determined" else "determined", "pose": "guard", "flip": bool(index % 2)},
            ],
            "fx": [{"kind": "dust", "at": 0.35, "x": 0.78, "y": 0.78, "s": 0.1}] if progress > 0.35 else [],
            "move": ("in", "left", "out", "right")[index % 4],
        }
        if "hannibal" in low:
            args["props"] = [{"kind": "scroll", "x": 0.75, "y": 0.82, "s": 0.14, "anim": "float"}]
        cue("armor_clank", "chainmail", at=0.3)
    elif tpl == "item":    elif tpl == "item":
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
        roman_focus = any(k in low for k in ("roman", "rome", "varro", "paullus", "legion", "consul"))
        horse_focus = any(k in low for k in ("horse", "cavalry", "gallop", "horsemen", "numidian", "riders", "hooves"))
        camp_focus = any(k in low for k in ("camp", "supply", "stores", "river", "tent", "marching", "supplies"))
        ruins_focus = any(k in low for k in ("citadel", "ruins", "ruined", "town"))
        aftermath = any(k in low for k in ("dead", "died", "wounded", "killed", "catastrophic", "disaster", "aftermath", "losses", "blood"))
        crush = any(k in low for k in ("crush", "pressed", "pressing", "shield", "no clear front", "cannot turn", "crowded", "corridor", "packed"))
        red = "hastatus"
        blue = "latinOld"
        move = ("in", "left", "out", "right", "up", "still")[index % 6]

        if horse_focus:
            hero = blue if carthage_focus or "numidian" in low else red
            rival = red if hero == blue else blue
            args = {
                "bg": "hills" if index % 2 else "field",
                "time": time_of_day,
                "bgOpts": {"volcano": False, "trees": 4, "bushes": 3, "flags": [{"x": 0.12, "color": ROMAN}, {"x": 0.86, "color": CARTHAGE}]},
                "back": [{"preset": rival, "rows": 2, "cols": 12, "x0": 0.08, "x1": 0.92, "yFront": 0.78, "yBack": 0.68, "hFront": 0.12, "hBack": 0.07, "flip": True}],
                "mid": [{"preset": hero, "rows": 2, "cols": 7, "x0": 0.08, "x1": 0.92, "yFront": 0.95, "yBack": 0.81, "hFront": 0.19, "hBack": 0.11, "march": 0.25}],
                "people": [
                    {"preset": hero, "x": 0.28, "y": 0.68, "h": 0.39, "pose": "guard", "horse": {"color": "bay" if hero == blue else "chestnut", "gait": "gallop", "travel": False}},
                    {"preset": hero, "x": 0.69, "y": 0.73, "h": 0.33, "pose": "push", "horse": {"color": "dark" if hero == blue else "bay", "gait": "gallop", "travel": False}, "flip": True},
                ],
                "fx": [{"kind": "dust", "at": 0.15, "x": 0.5, "y": 0.83, "s": 0.2}],
                "move": move,
                "moveAmt": 0.025,
            }
            cue("hooves_gallop", "horse_neigh", "battle_far", at=0.25)
        elif aftermath:
            args = {
                "bg": "mud" if index % 2 else "field",
                "time": "dusk",
                "bgOpts": {"volcano": False, "trees": 2, "clouds": 2, "mud": True, "wet": True, "flags": [{"x": 0.12, "color": ROMAN}]},
                "back": [{"preset": red, "rows": 2, "cols": 11, "x0": 0.08, "x1": 0.92, "yFront": 0.73, "yBack": 0.64, "hFront": 0.1, "hBack": 0.06, "face": "worried"}],
                "people": [
                    {"preset": red, "x": 0.45, "y": 0.81, "h": 0.53, "pose": "guard", "face": "worried", "fall": 0.7},
                    {"preset": red, "x": 0.78, "y": 0.85, "h": 0.34, "pose": "guard", "face": "worried"},
                ],
                "props": [{"kind": "shield", "type": "scutum", "x": 0.22, "y": 0.82, "s": 0.22, "rot": -0.4}, {"kind": "spear", "x": 0.9, "y": 0.83, "s": 0.27, "rot": 0.9}],
                "fx": [{"kind": "smoke", "at": 0.2, "x": 0.7, "y": 0.45, "s": 0.2}, {"kind": "dust", "at": 0.35, "x": 0.5, "y": 0.85, "s": 0.16}],
                "move": ("out", "left", "in")[index % 3],
                "dark": 0.08,
            }
            cue("wind_loop", "sting_low", "battle_far", at=0.25)
        elif camp_focus:
            bg_kind = "tent" if "camp" in low or "tent" in low else ("hills" if index % 2 else "field")
            args = {
                "bg": bg_kind,
                "time": "golden" if progress < 0.5 else "day",
                "bgOpts": {"volcano": False, "tents": 4 if bg_kind != "tent" else 0, "trees": 3, "flags": [{"x": 0.18, "color": ROMAN}, {"x": 0.82, "color": CARTHAGE}]},
                "back": [{"preset": blue if carthage_focus else red, "rows": 2, "cols": 9, "x0": 0.08, "x1": 0.92, "yFront": 0.82, "yBack": 0.71, "hFront": 0.13, "hBack": 0.07}],
                "people": [
                    {"preset": blue if carthage_focus else red, "x": 0.34, "y": 0.72, "h": 0.43, "pose": "point", "face": "determined"},
                    {"preset": red if carthage_focus else blue, "x": 0.72, "y": 0.75, "h": 0.35, "pose": "guard", "face": "neutral", "flip": True},
                ],
                "props": [{"kind": "scroll", "x": 0.82, "y": 0.85, "s": 0.14, "anim": "float"}, {"kind": "barrel", "x": 0.16, "y": 0.86, "s": 0.13}],
                "move": move,
            }
            cue("page_turn", "drum_march", "wind_loop", at=0.2)
        elif ruins_focus:
            args = {
                "bg": "stone" if index % 2 else "castle",
                "time": "day" if index % 3 else "dawn",
                "bgOpts": {"volcano": False, "banner": {"color": ROMAN}, "window": False, "trees": 0},
                "back": [{"preset": red, "rows": 2, "cols": 10, "x0": 0.06, "x1": 0.94, "yFront": 0.8, "yBack": 0.72, "hFront": 0.12, "hBack": 0.07}],
                "people": [{"preset": red, "x": 0.28, "y": 0.76, "h": 0.42, "pose": "guard"}, {"preset": blue, "x": 0.72, "y": 0.74, "h": 0.38, "pose": "push", "flip": True}],
                "props": [{"kind": "rock", "x": 0.13, "y": 0.89, "s": 0.16}, {"kind": "standard", "x": 0.88, "y": 0.82, "s": 0.22, "color": CARTHAGE}],
                "move": move,
            }
            cue("wind_loop", "battle_far", at=0.2)
        elif crush and roman_focus:
            args = {
                "bg": "mud" if index % 2 else "field",
                "time": time_of_day,
                "bgOpts": {"volcano": False, "trees": 1, "bushes": 2, "mud": index % 2 == 0, "flags": [{"x": 0.12, "color": ROMAN}]},
                "back": [{"preset": red, "presets": ["hastatus", "princeps", "triarius"], "rows": 4, "cols": 18, "x0": 0.0, "x1": 1.0, "yFront": 0.83, "yBack": 0.58, "hFront": 0.23, "hBack": 0.1, "face": "worried"}],
                "mid": [{"preset": red, "presets": ["hastatus", "princeps"], "rows": 3, "cols": 12, "x0": 0.02, "x1": 0.98, "yFront": 0.98, "yBack": 0.8, "hFront": 0.28, "hBack": 0.14, "face": "worried", "march": 0.15}],
                "people": [{"preset": red, "x": 0.22 + (index % 3) * 0.08, "y": 0.68, "h": 0.48, "pose": "push", "face": "worried"}, {"preset": red, "x": 0.78, "y": 0.7, "h": 0.4, "pose": "guard", "face": "worried", "flip": True}],
                "props": [{"kind": "shield", "type": "scutum", "x": 0.87, "y": 0.86, "s": 0.18, "rot": 0.18}],
                "fx": [{"kind": "dust", "at": 0.2, "x": 0.54, "y": 0.81, "s": 0.18}],
                "move": move,
                "shake": 0.08,
            }
            cue("battle_roar", "shield_bash", "battle_far", at=0.25)
        elif carthage_focus:
            args = {
                "bg": "hills" if index % 2 else "field",
                "time": time_of_day,
                "bgOpts": {"volcano": False, "trees": 3, "flags": [{"x": 0.17, "color": CARTHAGE}, {"x": 0.83, "color": ROMAN}]},
                "back": [{"preset": blue, "presets": ["latin", "latinOld"], "rows": 2 + index % 2, "cols": 14, "x0": 0.04, "x1": 0.96, "yFront": 0.83, "yBack": 0.66, "hFront": 0.16, "hBack": 0.08, "flip": False}],
                "people": [{"preset": blue, "x": 0.63, "y": 0.66, "h": 0.51, "pose": "point", "face": "determined"}, {"preset": red, "x": 0.25, "y": 0.76, "h": 0.35, "pose": "guard", "face": "worried", "flip": True}],
                "props": [{"kind": "standard", "x": 0.9, "y": 0.79, "s": 0.23, "color": CARTHAGE}],
                "move": move,
            }
            cue("war_horn", "battle_far", at=0.2)
        else:
            # Rotate through deliberately different compositions instead of reusing the same face-off.
            mode = index % 4
            if mode == 0:
                args = {
                    "bg": "hills", "time": time_of_day,
                    "bgOpts": {"volcano": False, "trees": 5, "bushes": 4, "flags": [{"x": 0.1, "color": ROMAN}, {"x": 0.9, "color": CARTHAGE}]},
                    "back": [{"preset": red, "rows": 3, "cols": 16, "x0": 0.02, "x1": 0.48, "yFront": 0.84, "yBack": 0.66, "hFront": 0.17, "hBack": 0.08}, {"preset": blue, "rows": 3, "cols": 16, "x0": 0.52, "x1": 0.98, "yFront": 0.83, "yBack": 0.65, "hFront": 0.16, "hBack": 0.08, "flip": True}],
                    "people": [{"preset": red, "x": 0.22, "y": 0.72, "h": 0.41, "pose": "guard"}, {"preset": blue, "x": 0.78, "y": 0.72, "h": 0.42, "pose": "push", "flip": True}],
                    "move": "in",
                }
            elif mode == 1:
                args = {
                    "bg": "field", "time": "day",
                    "bgOpts": {"volcano": False, "trees": 2, "bushes": 6, "tents": 2, "flags": [{"x": 0.8, "color": ROMAN}]},
                    "back": [{"preset": red, "rows": 2, "cols": 20, "x0": 0.02, "x1": 0.98, "yFront": 0.83, "yBack": 0.68, "hFront": 0.15, "hBack": 0.08}],
                    "people": [{"preset": red, "x": 0.48, "y": 0.67, "h": 0.55, "pose": "point", "face": "determined"}, {"preset": red, "x": 0.78, "y": 0.78, "h": 0.31, "pose": "guard", "flip": True}],
                    "props": [{"kind": "eagle", "x": 0.16, "y": 0.82, "s": 0.25, "color": ROMAN}],
                    "move": "left",
                }
            elif mode == 2:
                args = {
                    "bg": "tent", "time": "golden",
                    "bgOpts": {"volcano": False, "lantern": True},
                    "people": [{"preset": blue, "x": 0.45, "y": 0.71, "h": 0.5, "pose": "guard", "face": "determined"}, {"preset": red, "x": 0.78, "y": 0.76, "h": 0.32, "pose": "guard", "flip": True}],
                    "props": [{"kind": "scroll", "x": 0.18, "y": 0.82, "s": 0.18, "anim": "float"}, {"kind": "campfire", "x": 0.86, "y": 0.91, "s": 0.16}],
                    "move": "out",
                }
            else:
                args = {
                    "bg": "mud", "time": "storm",
                    "bgOpts": {"volcano": False, "mud": True, "wet": True, "clouds": 1, "trees": 1},
                    "back": [{"preset": red, "rows": 4, "cols": 17, "x0": 0.0, "x1": 1.0, "yFront": 0.82, "yBack": 0.6, "hFront": 0.18, "hBack": 0.07, "face": "worried"}],
                    "people": [{"preset": red, "x": 0.33, "y": 0.73, "h": 0.48, "pose": "push", "face": "worried"}],
                    "props": [{"kind": "shield", "type": "scutum", "x": 0.78, "y": 0.85, "s": 0.2}],
                    "fx": [{"kind": "dust", "at": 0.25, "x": 0.5, "y": 0.85, "s": 0.16}],
                    "move": "right",
                }
            if any(k in low for k in ("sword", "clash", "fight", "battle")):
                cue("sword_clash", "battle_far", at=0.4)
            else:
                cue("battle_far", "wind_loop", at=0.2)

    if tpl not in VALID_TEMPLATES:
    args.setdefault("seed", seed)
    args.setdefault("move", ("in", "left", "out", "right", "up", "still")[index % 6])
    args.setdefault("moveAmt", 0.018 + (index % 4) * 0.006)
    if any(k in low for k in ("charge", "attack", "clash", "surrounded")):
        args.setdefault("shake", 0.035)
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
        "captions": True,
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
