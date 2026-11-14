#!/usr/bin/env python3
"""Author a character-led, event-specific H2 Squire film about the 1453 siege."""
from __future__ import annotations
import argparse, json
from pathlib import Path

# Actor-led scenes in this film must use the mature-proportion templates below.
STANDARD = {"top", "map", "plan", "board", "item", "title", "black"}
CUSTOM = {
    "final_night", "night_wall_watch", "night_camp", "night_camp_detail",
    "night_guns", "night_gun_crew", "night_gun_crew_detail",
    "assault_waves", "assault_first_wave", "assault_second_wave", "elite_reserve",
    "defender_identity", "defender_supply", "rewind_map",
    "city_panorama", "command_camp", "gun_crew", "wall_battery",
    "repair_wall", "golden_horn", "relief_galleys", "ship_portage",
    "tunnel_cutaway", "church_refuge", "city_interior", "last_assault", "aftermath_city",
    "actor_closeup", "city_detail"
}
BLUE, RED, GOLD = "#536b83", "#9c493c", "#d1ad68"
HERO = "byzantineYou"

def load(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def cue(root, names, at=.25, gain=-9):
    for name in names:
        if (root / f"{name}.wav").is_file():
            return [{"name": name, "at": at, "gain": gain}]
    return []

def sfx_for_shot(tpl, args, index, root):
    if tpl == "night_camp":
        return cue(root, ["battle_roar"], at=.16, gain=-19) + cue(root, ["wind_loop"], at=0, gain=-20)
    if tpl == "night_guns":
        return cue(root, ["cannon_fire"], at=.58, gain=-14)
    if tpl == "night_gun_crew":
        return cue(root, ["cannon_fire"], at=.92, gain=-12)
    if tpl == "night_gun_crew_detail":
        return cue(root, ["cannon_fire"], at=.92, gain=-15) + cue(root, ["wind_loop"], at=0, gain=-22)
    if tpl in {"night_wall_watch", "night_camp_detail"}:
        return cue(root, ["wind_loop"], at=0, gain=-20) + cue(root, ["battle_roar"], at=.24, gain=-23)
    if tpl == "defender_identity":
        return cue(root, ["wind_loop"], at=0, gain=-19) + cue(root, ["battle_roar"], at=.28, gain=-20)
    if tpl == "rewind_map":
        return cue(root, ["wind_loop"], at=0, gain=-24)
    if tpl in {"assault_waves", "assault_first_wave", "assault_second_wave", "elite_reserve"}:
        return cue(root, ["battle_roar"], at=.18, gain=-12) + cue(root, ["arrow_whoosh"], at=.56, gain=-17)
    if tpl == "defender_supply":
        return cue(root, ["battle_roar"], at=.25, gain=-23) + cue(root, ["wind_loop"], at=0, gain=-22)
    if tpl in {"wall_battery", "gun_crew"}:
        fire_at = float(args.get("fireAt", .52))
        return cue(root, ["cannon_fire"], at=fire_at, gain=-8) + cue(root, ["siege_impact"], at=fire_at + 1.02, gain=-7)
    if tpl == "repair_wall":
        return cue(root, ["siege_impact"], at=.38, gain=-10) if index % 2 == 0 else cue(root, ["battle_roar"], at=.32, gain=-15)
    if tpl in {"last_assault", "final_night"}:
        if index % 3 == 0:
            return cue(root, ["arrow_whoosh"], at=.28, gain=-10)
        if index % 3 == 1:
            return cue(root, ["sword_clash"], at=.62, gain=-8)
        return cue(root, ["battle_roar"], at=.18, gain=-13)
    if tpl in {"relief_galleys", "golden_horn"}:
        return cue(root, ["wind_loop"], at=0, gain=-16)
    if tpl == "ship_portage":
        return cue(root, ["battle_roar"], at=.36, gain=-16) if index % 4 == 0 else []
    if tpl in {"church_refuge", "city_interior", "tunnel_cutaway"}:
        return cue(root, ["wind_loop"], at=0, gain=-19) if index % 4 == 0 else []
    return cue(root, ["wind_loop"], at=0, gain=-19) if index % 5 == 0 else []

def opening_context(shots, index, max_gap=2.6):
    """Read the current cue and immediate neighbours; neighbours complete fragments only."""
    current = shots[index]
    midpoint = (float(current["start"]) + float(current["end"])) / 2
    nearby = []
    for j in range(max(0, index - 1), min(len(shots), index + 2)):
        item = shots[j]
        other_midpoint = (float(item["start"]) + float(item["end"])) / 2
        if j == index or abs(other_midpoint - midpoint) <= max_gap:
            line = str(item.get("line") or "").strip()
            if line:
                nearby.append(line)
    return " ".join(nearby)


def choose_opening_template(text, context_text, index):
    """Current narration cue wins; neighbours only complete syntactic fragments."""
    current = text.casefold()
    context = context_text.casefold()

    # Chronology hinge: move from the final night back to 6 April 1453.
    if any(k in current for k in ("to understand that night", "return to the morning",
                                  "sixth of april")):
        return "rewind_map"
    if any(k in context for k in ("return to the morning", "sixth of april")):
        return "rewind_map"

    # The order of the waves is explicit. Do not allow a future phrase to overwrite it.
    if any(k in current for k in ("second wave", "climb over what remains")):
        return "assault_second_wave"
    if any(k in current for k in ("first men may", "not be expected to survive", "first wave")):
        return "assault_first_wave"
    if any(k in current for k in ("largest assault", "assault will begin", "it will come in waves",
                                  "come in waves", "at dawn")):
        return "assault_waves"
    if any(k in current for k in ("sultan's best troops", "the sultan's best", "best troops")):
        return "elite_reserve"

    if "one defender among thousands" in current:
        return "defender_identity"
    if any(k in current for k in ("carrying water", "carry water", "water, stones",
                                  "stones, arrows", "arrows, and messages", "arrows and messages",
                                  "messages wherever", "wall is weakest")):
        return "defender_supply"
    if any(k in current for k in ("not a famous commander", "you have spent fifty-three days",
                                  "no longer certain", "almost run out of strength",
                                  "the question is no")):
        return "actor_closeup"
    if "make an empire pay" in current:
        return "city_detail"
    if "at midnight" in current:
        return "final_night"
    if any(k in current for k in ("walls are still standing", "the walls will hold")):
        return "night_wall_watch"

    if any(k in current for k in ("creak of carts", "cart wheels", "carts")):
        return "night_camp_detail"
    if any(k in current for k in ("horses shifting", "horses", "men calling", "calling to one another",
                                  "campfires", "camp fires", "fires beyond")):
        return "night_camp_detail"
    if any(k in current for k in ("distant thunder of guns", "thunder of guns", "guns in the darkness",
                                  "distant cannon", "artillery flash")):
        return "night_guns"
    if any(k in current for k in ("preparing the next shot", "prepare the next shot",
                                  "stone ball", "loading the gun", "rammer", "powder charge")):
        return "night_gun_crew_detail"
    if "cannon crew" in current or "gun crew" in current:
        return "night_gun_crew"
    if "ottoman camp" in current:
        return "night_camp"
    if any(k in current for k in ("beyond the dark", "dark fields", "fields:")):
        if any(k in context for k in ("horses", "carts", "men calling")):
            return "night_camp_detail"
        return "night_camp"
    if "somewhere in the darkness" in current or "somewhere in darkness" in current:
        if "cannon crew" in context or "preparing the next shot" in context:
            return "night_gun_crew"
    if any(k in current for k in ("tonight", "believing", "you are not", "you are one defender")):
        return "actor_closeup"
    if any(k in current for k in ("constantinople can win", "one city can", "one city")):
        return "city_panorama"

    # Use neighbouring lines only for incomplete fragments such as "of the siege will begin".
    if any(k in context for k in ("the sultan's best troops", "sultan's best", "best troops")):
        return "elite_reserve"
    if any(k in context for k in ("second wave", "climb over what remains")):
        return "assault_second_wave"
    if any(k in context for k in ("first men may", "not be expected to survive", "first wave")):
        return "assault_first_wave"
    if any(k in context for k in ("largest assault", "come in waves", "at dawn")):
        return "assault_waves"
    if any(k in context for k in ("carrying water", "carry water", "stones, arrows",
                                  "arrows and messages", "messages wherever", "wall is weakest")):
        return "defender_supply"
    if any(k in context for k in ("preparing the next shot", "prepare the next shot")):
        return "night_gun_crew_detail"
    if "cannon crew" in context or "gun crew" in context:
        return "night_gun_crew"
    if any(k in context for k in ("distant thunder of guns", "thunder of guns", "guns in the darkness")):
        return "night_guns"
    if any(k in context for k in ("horses shifting", "horses", "men calling", "creak of carts", "cart wheels")):
        return "night_camp_detail"
    if "ottoman camp" in context or "dark fields" in context:
        return "night_camp"
    if "no longer certain" in context or "not a famous commander" in context:
        return "actor_closeup"
    if "one defender among thousands" in context:
        return "defender_identity"
    if "walls are still standing" in context or "the walls will hold" in context:
        return "night_wall_watch"

    return "night_wall_watch" if index % 2 else "final_night"


def progress_phase(p, text):
    t = text.casefold()
    if any(k in t for k in (
        "final assault", "last assault", "largest assault", "first wave", "second wave",
        "third wave", "janissar", "ladder", "twenty-ninth of may", "twenty ninth of may",
        "just before dawn", "first men may not", "the sultan's best troops",
        "not be expected to survive", "climb over what remains", "it will come in waves"
    )):
        return "final"
    if p < .066 and "one defender among thousands" in t:
        return "defender_identity"
    if p < .066 and any(k in t for k in ("not a famous commander", "no longer certain",
                                         "you have spent fifty-three days", "almost run out of strength")):
        return "night_defender"
    if p < .066 and any(k in t for k in ("carrying water", "carry water", "stones, arrows",
                                         "arrows and messages", "wall is weakest")):
        return "defender_supply"
    if p < .066 and any(k in t for k in ("to understand that night", "return to the morning", "sixth of april")):
        return "rewind_map"
    if p < .066:
        # The film opens on the final night, but the narration already contains distinct
        # visual events. Give those events their own scenes instead of forcing every cue
        # into the same watchtower tableau until the first-day rewind.
        if any(k in t for k in (
            "cannon crew", "gun crew", "preparing the next shot", "prepare the next shot",
            "stone ball", "loading the gun", "rammer", "powder charge"
        )):
            return "night_gun_crew"
        if any(k in t for k in (
            "distant thunder of guns", "thunder of guns", "guns in the darkness",
            "cannon fire", "distant cannon", "bombard", "artillery"
        )):
            return "night_guns"
        if any(k in t for k in (
            "ottoman camp", "horses shifting", "horses", "men calling", "creak of carts",
            "carts", "dark fields", "tents spread", "campfires", "camp fires", "fires beyond"
        )):
            return "night_camp"
        return "night"

    # The final summary describes the operation retrospectively; do not stage it as a second portage.
    if p > .93:
        return "aftermath"

    # Strong event language wins over chapter windows, so explicit text always has priority.
    if any(k in t for k in ("hauled overland", "overland", "rollers", "ships are appearing inside",
                            "ships inside", "lowered into the inlet", "hauled across land",
                            "ships on rollers", "vessels overland")):
        return "portage"
    if any(k in t for k in ("four christian ships", "four ships", "relief ships", "convoy",
                            "ottoman fleet", "christian ships", "supply ships", "ships with supplies",
                            "ships close the distance", "ships fight their way", "reach the golden horn")):
        return "convoy"
    if any(k in t for k in ("countermin", "counter-min", "tunnel", "underground", "miners",
                            "digging below", "dig below", "earth being moved", "beneath the wall",
                            "counterminers")):
        return "tunnel"

    # Voice-aligned chapter windows in the approved 957.9-second narration fill split cue fragments.
    if 0.385 <= p < 0.433:
        return "convoy"
    if 0.437 <= p < 0.478:
        return "portage"
    if 0.505 <= p < 0.532:
        return "tunnel"
    if any(k in t for k in ("golden horn", "massive chain", "chain across", "harbour", "harbor", "sea lanes", "strait")):
        return "sea"
    if any(k in t for k in ("countermin", "counter-min", "tunnel", "underground", "miners", "digging below",
                            "dig below", "earth being moved", "beneath the wall", "counterminers")):
        return "tunnel"
    if any(k in t for k in ("repair crews", "repair team", "builders carry", "timber", "masonry", "repair the wall", "rebuild the wall", "breach is")):
        return "repair"
    if any(k in t for k in ("bombard", "cannon", "gun crew", "stone shot", "artillery", "powder", "wall is hit", "impact", "orban", "bombardment")):
        return "guns"
    if any(k in t for k in ("ration", "food", "churches", "praying", "wounded", "giustiniani", "constantine", "emperor", "civilians", "people who have never", "aid from the west")):
        return "inside"
    if any(k in t for k in ("mehmed", "rumeli", "bosporus", "bosphorus", "sultan", "ottoman army", "ottoman camp", "engineers measure")):
        return "camp"
    if any(k in t for k in ("city", "walls", "constantinople", "theodosian", "capital", "harbours", "harbors", "empire")):
        return "city"
    return ("city", "camp", "guns", "repair", "sea", "inside", "final")[int(p * 1000) % 7]

def choose_template(p, text, i, usage, last, context_text=None):
    phase = progress_phase(p, context_text or text)
    if p < .066:
        return choose_opening_template(text, context_text or text, i)
    # Hard cap wide city tableaux. Use a closer environmental shot after the limit.
    city_panorama_count = usage.get("city_panorama", 0)
    preferred = {
        "night": "final_night",
        "night_camp": "night_camp",
        "night_guns": "night_guns",
        "night_gun_crew": "night_gun_crew",
        "city": "city_detail" if city_panorama_count >= 50 else "city_panorama",
        "camp": "command_camp",
        "guns": "gun_crew" if i % 2 == 0 else "wall_battery",
        "repair": "repair_wall",
        "sea": "golden_horn" if usage.get("golden_horn", 0) < 58 else "city_detail",
        "convoy": "relief_galleys",
        "portage": "ship_portage",
        "tunnel": "tunnel_cutaway",
        "inside": "church_refuge" if any(k in text.casefold() for k in ("church", "pray", "food", "ration")) else "city_interior",
        "final": "last_assault",
        "defender_supply": "defender_supply",
        "aftermath": "aftermath_city"
    }
    custom = preferred[phase]

    # The dawn assault is a major narrative event, not a decorative insert.
    # Keep its first wave in the full battlefield composition even when the
    # deterministic insert cadence would otherwise choose "item" or a close-up.
    if phase == "final" and any(k in text.casefold() for k in (
        "largest assault", "first wave", "second wave", "third wave",
        "first men may not", "the sultan's best troops"
    )):
        return "last_assault"

    # Keep only diagrams/object inserts from the generic pack; never use its chibi actor templates.
    if phase in {"guns", "repair", "final", "inside"} and i % 8 in (2, 6):
        return "actor_closeup" if i % 8 == 2 else "item"
    if phase in {"city", "camp", "sea", "portage"} and i % 11 == 5:
        return "map" if phase in {"city", "camp", "portage"} else "top"
    if phase in {"guns", "repair", "final", "convoy", "portage"} and i % 13 == 9:
        return "top"
    if phase in {"city", "camp", "inside"} and i % 17 == 12:
        return "city_detail" if phase == "city" else "actor_closeup"
    if last == custom and i % 3 == 0:
        return "actor_closeup"
    return custom

def alternate_preset(phase, i, text):
    t = text.casefold()
    if phase in {"elite_reserve"}:
        return "ottomanElite"
    if phase in {"assault_waves", "assault_first_wave", "assault_second_wave", "night_guns", "night_gun_crew", "night_gun_crew_detail", "night_camp_detail"}:
        return "ottomanInfantry"
    if phase == "camp":
        return "ottomanCommander" if i % 2 == 0 else "ottomanElite"
    if phase in {"sea", "convoy"}:
        return "byzantineArcher" if i % 2 == 0 else "byzantineGuard"
    if phase == "portage":
        return "ottomanInfantry" if i % 2 == 0 else "ottomanElite"
    if phase == "tunnel":
        return "ottomanInfantry" if i % 2 == 0 else "byzantineGuard"
    if phase == "inside":
        if any(k in t for k in ("church", "pray", "priest")):
            return "monk"
        return "lady" if i % 3 == 0 else "peasant"
    if phase == "aftermath":
        return "peasant" if i % 2 == 0 else "lady"
    if phase == "guns" and any(k in t for k in ("orban", "gun crew", "cannon crew", "powder")):
        return "ottomanInfantry"
    if phase in {"city", "night", "guns", "repair", "final"}:
        return "byzantineGuard" if i % 2 == 0 else "byzantineArcher"
    return "byzantineGuard"


def scene_args(phase, i, p, text, hero_visible=True):
    t = text.casefold()
    lead_preset = HERO if hero_visible else alternate_preset(phase, i, text)
    motion = ("in", "left", "right", "out", "up", "down")[i % 6]
    cam = {"move": motion, "moveAmt": .035 if i % 3 else .055,
           "shake": .32 if phase in {"guns", "final", "repair"} and i % 4 == 0 else 0}
    hero = {"preset": lead_preset, "x": .32, "y": .96, "h": .63,
            "face": "tired" if phase in {"night", "inside"} else "determined",
            "pose": "guard", "weapon": "spear",
            "shield": {"type": "round", "color": BLUE, "charge": "cross", "chargeColor": GOLD}}
    if phase == "city":
        return {**cam, "bg": "castle", "time": "dawn" if p < .2 else "day",
                "bgOpts": {"window": False, "torch": False, "trees": 3, "bushes": 3, "banner": {"color": BLUE}},
                "blur": 6,
                "back": [{"preset": "byzantineGuard", "rows": 3, "cols": 16, "x0": .38, "x1": .98,
                          "yFront": .78, "yBack": .65, "hFront": .12, "hBack": .06, "seed": i + 5}],
                "people": [hero, {"preset": "peasant", "x": .76, "y": .94, "h": .38,
                                  "face": "worried", "pose": "walk", "walk": True, "dir": -1}],
                "props": [{"kind": "flag", "x": .84, "y": .74, "s": .22, "color": BLUE},
                          {"kind": "basket", "x": .64, "y": .93, "s": .14}],
                "fx": [{"kind": "dust", "at": .2, "x": .55, "y": .8, "s": .09}],
                "signs": [{"text": "YOU", "x": .32, "y": .19, "at": .2, "size": 34}] if i < 3 else []}
    if phase == "camp":
        return {**cam, "bg": "tent", "time": "golden",
                "bgOpts": {"tents": 5, "flags": [{"x": .14, "color": RED}, {"x": .84, "color": RED}]},
                "people": [{"preset": "ottomanCommander", "x": .48, "y": .88, "h": .65,
                            "face": "determined", "pose": "point"},
                           {"preset": "ottomanElite", "x": .74, "y": .9, "h": .43, "face": "neutral", "pose": "guard"},
                           {"preset": "ottomanElite", "x": .22, "y": .9, "h": .41, "face": "neutral", "pose": "guard", "flip": True}],
                "props": [{"kind": "scroll", "x": .8, "y": .92, "s": .2}, {"kind": "barrel", "x": .15, "y": .92, "s": .2}],
                "fx": [{"kind": "smoke", "at": .1, "x": .65, "y": .38, "s": .1}]}
    if phase in {"guns", "repair"}:
        return {**cam, "bg": "hills", "time": "day", "blur": 5,
                "bgOpts": {"volcano": False, "trees": 2, "bushes": 2},
                "mid": [{"preset": "byzantineGuard", "rows": 3, "cols": 12, "x0": .56, "x1": .98,
                         "yFront": .8, "yBack": .65, "hFront": .15, "hBack": .07, "seed": i}],
                "people": [hero, {"preset": "byzantineGuard", "x": .54, "y": .94, "h": .4,
                                  "face": "worried", "pose": "carry", "walk": True, "dir": 1}],
                "props": [{"kind": "cart", "x": .48, "y": .91, "s": .34},
                          {"kind": "barrel", "x": .65, "y": .93, "s": .17}],
                "fx": [{"kind": "smoke", "at": .4, "x": .42, "y": .6, "s": .15},
                       {"kind": "dust", "at": .5, "x": .71, "y": .82, "s": .16}]}
    if phase in {"sea", "convoy"}:
        return {**cam, "bg": "sea", "time": "dawn", "blur": 4,
                "people": [dict(hero, x=.28, y=.97, h=.55, pose="point"),
                           {"preset": "byzantineArcher", "x": .78, "y": .94, "h": .37,
                            "face": "worried", "pose": "point"}],
                "props": [{"kind": "flag", "x": .2, "y": .55, "s": .26, "color": BLUE},
                          {"kind": "flag", "x": .82, "y": .54, "s": .26, "color": RED}],
                "fx": [{"kind": "rain", "at": .1, "len": .06, "n": 26}]}
    if phase == "portage":
        return {**cam, "bg": "field", "time": "day", "blur": 5,
                "bgOpts": {"trees": 0, "bushes": 1, "clouds": 3},
                "people": [dict(hero, x=.25, y=.96, h=.58, pose="point"),
                           {"preset": "ottomanInfantry", "x": .76, "y": .94, "h": .42,
                            "face": "determined", "pose": "push", "walk": True, "dir": 1}],
                "props": [{"kind": "spear", "x": .55, "y": .78, "s": .4},
                          {"kind": "flag", "x": .82, "y": .55, "s": .22, "color": RED}],
                "fx": [{"kind": "dust", "at": .2, "x": .56, "y": .81, "s": .12}]}
    if phase == "tunnel":
        return {**cam, "bg": "trench", "time": "night", "blur": 4,
                "people": [dict(hero, x=.3, y=.96, h=.62, pose="kneel", face="worried"),
                           {"preset": "byzantineGuard", "x": .75, "y": .95, "h": .4,
                            "face": "worried", "pose": "hold", "weapon": "torch"}],
                "props": [{"kind": "torch", "x": .84, "y": .72, "s": .25},
                          {"kind": "pickaxe", "x": .58, "y": .9, "s": .25}],
                "fx": [{"kind": "smoke", "at": .2, "x": .62, "y": .39, "s": .12}]}
    if phase == "inside":
        return {**cam, "bg": "cathedral" if any(k in t for k in ("church", "pray", "priest")) else "castle",
                "time": "night" if i % 2 else "dusk", "blur": 5,
                "bgOpts": {"window": True, "torch": True, "floorY": .78},
                "people": [dict(hero, x=.3, y=.95, h=.62, pose="kneel" if any(k in t for k in ("pray", "church")) else "carry",
                                face="worried" if "wounded" in t else "tired"),
                           {"preset": "peasant", "x": .68, "y": .94, "h": .37,
                            "face": "worried", "pose": "run", "walk": True, "dir": 1},
                           {"preset": "monk", "x": .84, "y": .93, "h": .42, "face": "sad", "pose": "beg"}],
                "props": [{"kind": "torch", "x": .1, "y": .7, "s": .27},
                          {"kind": "basket", "x": .55, "y": .92, "s": .2}],
                "fx": [{"kind": "smoke", "at": .2, "x": .62, "y": .39, "s": .12}]}
    if phase == "night":
        return {**cam, "bg": "castle", "time": "night", "blur": 5,
                "bgOpts": {"window": True, "torch": True, "banner": {"color": BLUE}},
                "people": [dict(hero, x=.36, y=.97, h=.67, face="tired", pose="guard"),
                           {"preset": "byzantineGuard", "x": .76, "y": .95, "h": .46, "face": "worried", "pose": "look"}],
                "props": [{"kind": "torch", "x": .18, "y": .72, "s": .28}],
                "fx": [{"kind": "smoke", "at": .2, "x": .65, "y": .38, "s": .12}]}
    return {**cam, "bg": "hills", "time": "dusk", "blur": 5,
            "bgOpts": {"trees": 2, "flags": [{"x": .15, "color": BLUE}, {"x": .85, "color": RED}]},
            "people": [dict(hero, x=.28, y=.96, h=.63, face="worried"),
                       {"preset": "ottomanElite", "x": .74, "y": .94, "h": .51, "face": "determined", "pose": "guard", "flip": True}],
            "mid": [{"preset": "byzantineGuard", "rows": 3, "cols": 14, "x0": .02, "x1": .98,
                     "yFront": .78, "yBack": .62, "hFront": .14, "hBack": .06, "seed": i + 44}],
            "fx": [{"kind": "dust", "at": .2, "x": .5, "y": .83, "s": .12}]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    project = Path(args.project).resolve()
    path = project / "story" / "shots.json"
    story = load(path, {})
    shots = story.get("shots") or []
    if len(shots) < 350:
        raise ValueError(f"Expected at least 350 voice-timed shots, received {len(shots)}.")
    duration = float(story.get("duration") or shots[-1]["end"])
    if duration < 650:
        raise ValueError(f"Long-form narration must exceed 10:50; got {duration:.1f}s.")
    if len(shots) > 1100:
        raise ValueError(f"Shot count {len(shots)} is too high; avoid padding.")

    sfx_root = project.parents[1] / "audio" / "sfx"
    usage, last = {}, None
    hero_count = 0
    transitions = ("cut", "cut", "cut", "whip", "cut", "flash", "cut", "zoom", "cut", "dip")
    for i, shot in enumerate(shots):
        start, end = float(shot["start"]), float(shot["end"])
        if end <= start:
            raise ValueError(f"Bad timing in {shot.get('id')}")
        p = ((start + end) / 2) / duration
        text = str(shot.get("line") or "")
        context_text = opening_context(shots, i) if start < duration * .066 else text
        phase = progress_phase(p, text)
        tpl = choose_template(p, text, i, usage, last, context_text=context_text)
        # POV compositions are explicit in the opening; future Ottoman cues cannot suppress them.
        opening_pov = p < .066 and tpl in {
            "final_night", "night_wall_watch", "night_camp", "actor_closeup",
            "defender_identity", "defender_supply"
        }
        offensive = {
            "night_camp_detail", "night_guns", "night_gun_crew", "night_gun_crew_detail",
            "assault_waves", "assault_first_wave", "assault_second_wave", "elite_reserve"
        }
        hero_visible = opening_pov or (
            (i % 10 in {0, 3, 6, 8}) and phase not in {"camp", "night_guns", "night_gun_crew"}
        )
        if tpl in offensive or tpl == "rewind_map":
            hero_visible = False
        if tpl in {"defender_identity", "defender_supply", "actor_closeup", "night_wall_watch"} and p < .066:
            hero_visible = True
        lead_preset = HERO if hero_visible else alternate_preset(phase, i, text)

        if tpl in STANDARD:
            if tpl == "close":
                visual = {"preset": lead_preset,
                          "x": .5, "y": .5, "R": .255,
                          "face": "scared" if phase in {"final", "night"} else "worried",
                          "pose": "guard" if phase != "camp" else "point",
                          "bg": "castle" if phase in {"inside", "night", "repair"} else "hills",
                          "time": "night" if phase == "night" else ("dusk" if phase in {"final", "inside"} else "day"),
                          "others": [{"preset": "byzantineGuard", "x": .82, "y": .69, "R": .13, "face": "worried"}],
                          "move": "in", "moveAmt": .045}
                if i < 3 and phase == "night":
                    visual["signs"] = [{"text": "YOU", "x": .5, "y": .12, "at": .2, "size": 38}]
            elif tpl == "item":
                keywords = [("stone shot", "rock"), ("chain", "shield"), ("arrow", "arrow"),
                            ("helmet", "helmet"), ("shield", "shield"), ("sword", "sword"),
                            ("powder", "barrel"), ("torch", "torch"), ("ship", "flag"), ("gun", "spear")]
                thing = next((v for k, v in keywords if k in text.casefold()), "spear")
                visual = {"thing": {"kind": thing, "s": .64, "anim": "spin" if i % 2 else "drop"},
                          "bg": "castle" if phase in {"inside", "guns", "repair"} else "plain",
                          "time": "golden", "move": "in", "moveAmt": .06,
                          "props": [{"kind": "scroll", "x": .18, "y": .8, "s": .18}]}
            elif tpl == "top":
                visual = {"ground": {"color": "#b99f75", "grass": True, "rocks": True},
                          "blocks": [{"x": .48, "y": .57, "w": .26, "h": .28, "cols": 11, "rows": 10, "side": "blue",
                                      "path": [[0, .48, .57], [1.1, .52, .54]]},
                                     {"x": .18, "y": .45, "w": .16, "h": .3, "cols": 7, "rows": 12, "side": "red",
                                      "path": [[0, .18, .45], [1.4, .38, .5]]},
                                     {"x": .82, "y": .45, "w": .16, "h": .3, "cols": 7, "rows": 12, "side": "red",
                                      "path": [[0, .82, .45], [1.4, .62, .5]]}],
                          "arrows": [{"from": [.18, .45], "to": [.38, .5], "at": .35, "color": RED},
                                     {"from": [.82, .45], "to": [.62, .5], "at": .8, "color": RED}],
                          "labels": [{"text": "THE DEFENCE", "x": .5, "y": .12, "size": 31, "at": .25, "color": "#f5e5c6"}],
                          "move": "in"}
            elif tpl == "map":
                visual = {"view": [28.84, 40.96, 29.18, 41.22],
                          "places": [{"text": "CONSTANTINOPLE", "lon": 28.9784, "lat": 41.0082},
                                     {"text": "BOSPHORUS", "lon": 29.06, "lat": 41.16},
                                     {"text": "GOLDEN HORN", "lon": 28.96, "lat": 41.03},
                                     {"text": "RUMELI HISARI", "lon": 29.05, "lat": 41.08}],
                          "routes": [{"pts": [[29.05, 41.08], [29.0, 41.05], [28.98, 41.02]], "at": .4, "dur": 1.2}],
                          "move": "in", "moveAmt": .03}
            elif tpl == "plan":
                visual = {"paper": "parchment",
                          "zones": [{"x": .5, "y": .5, "w": .72, "h": .45, "color": "#9b876b", "at": .2, "dur": .7},
                                    {"x": .5, "y": .5, "w": .3, "h": .25, "color": BLUE, "at": .85, "dur": .55, "dashed": True}],
                          "blocks": [{"x": .5, "y": .55, "w": .2, "h": .18, "side": "blue", "cols": 9, "rows": 7, "at": .25},
                                     {"x": .2, "y": .47, "w": .14, "h": .24, "side": "red", "cols": 6, "rows": 10, "at": .6},
                                     {"x": .8, "y": .47, "w": .14, "h": .24, "side": "red", "cols": 6, "rows": 10, "at": .9}],
                          "arrows": [{"from": [.2, .65], "to": [.42, .55], "at": .85, "color": RED}],
                          "labels": [{"text": "THE DEFENCE", "x": .5, "y": .18, "size": 36, "at": .25, "color": "#2a2117"}]}
            elif tpl == "split":
                visual = {"left": {"color": BLUE, "people": [{"preset": lead_preset, "x": .26, "y": .78, "h": .55, "face": "determined"}]},
                          "right": {"color": RED, "people": [{"preset": "ottomanElite", "x": .74, "y": .78, "h": .55, "face": "determined"}]},
                          "labels": [{"text": "DEFENDERS", "x": .25, "y": .14, "size": 43, "at": .2, "color": BLUE},
                                     {"text": "SIEGE ARMY", "x": .75, "y": .14, "size": 43, "at": .8, "color": RED}],
                          "move": "in"}
            elif tpl == "army":
                visual = {"bg": "hills", "time": "day", "rows": 5, "cols": 18, "preset": "ottomanInfantry",
                          "enemy": lead_preset, "march": .28, "flags": [{"x": .2, "color": BLUE}, {"x": .8, "color": RED}],
                          "move": "right", "moveAmt": .055,
                          "fx": [{"kind": "dust", "at": .2, "x": .5, "y": .85, "s": .13}]}
            elif tpl == "frame":
                visual = {"bg": "castle", "people": [
                    {"preset": lead_preset, "x": .5, "y": .87, "h": .58, "face": "tired", "pose": "kneel"}],
                    "props": [{"kind": "torch", "x": .18, "y": .72, "s": .24}],
                    "arrows": [], "move": "in"}
            else:
                visual = scene_args(phase, i, p, text, hero_visible)
        else:
            visual = {"move": ("in", "left", "right", "out", "up", "down")[i % 6],
                      "moveAmt": .035 + (i % 3) * .012, "seed": i,
                      "hero": hero_visible, "variant": (i // 2) % 4,
                      "actorPreset": lead_preset}
            if tpl in {"wall_battery", "gun_crew"}:
                visual["fireAt"] = .35 + (i % 4) * .1
                visual["impactDelay"] = 1.02
            elif tpl == "last_assault":
                visual["moment"] = ("breach", "climb", "push", "counterattack")[i % 4]
            elif tpl == "relief_galleys":
                visual["label"] = "THE RELIEF CONVOY" if i % 4 == 0 else ""
                visual["beat"] = ("approach", "intercept", "breakthrough", "harbour")[i % 4]
            elif tpl == "golden_horn":
                visual["chain"] = True
                visual["beat"] = ("watch", "ships", "chain", "harbour")[i % 4]
            elif tpl == "ship_portage":
                visual["beat"] = ("rope_tension", "rollers", "haul", "arrival")[i % 4]
            elif tpl == "repair_wall":
                visual["beat"] = ("impact", "rubble", "brace", "rebuild")[i % 4]
            elif tpl == "tunnel_cutaway":
                visual["beat"] = ("listen", "dig", "countermine", "collapse")[i % 4]
            elif tpl == "church_refuge":
                visual["beat"] = ("prayer", "candle", "refuge", "departure")[i % 4]
            elif tpl == "final_night":
                visual["beat"] = ("watch", "torch", "dread", "dawn")[i % 4]
            elif tpl == "night_camp":
                visual["beat"] = ("horizon", "fires", "movement", "watch")[i % 4]
            elif tpl == "night_guns":
                visual["beat"] = ("distant_flash", "silhouette", "smoke", "thunder")[i % 4]
            elif tpl == "night_gun_crew":
                visual["beat"] = ("powder", "load", "brace", "match")[i % 4]
            elif tpl == "night_wall_watch":
                visual["beat"] = ("watch", "torch", "dread", "patrol")[i % 4]
            elif tpl == "night_camp_detail":
                visual["beat"] = ("carts" if "cart" in text.casefold() else
                                  "horses" if "horse" in text.casefold() else
                                  "signal" if "calling" in text.casefold() else
                                  "fires" if "fire" in text.casefold() else
                                  ("horses", "carts", "signal", "fires")[i % 4])
            elif tpl == "night_gun_crew_detail":
                visual["beat"] = ("stone" if "stone ball" in text.casefold() else
                                  "powder" if "powder" in text.casefold() else
                                  "match" if "match" in text.casefold() else
                                  "rammer" if any(k in text.casefold() for k in ("rammer", "preparing the next shot")) else
                                  ("powder", "stone", "rammer", "match")[i % 4])
            elif tpl == "assault_waves":
                visual["beat"] = ("approach", "drums", "ladders", "push")[i % 4]
            elif tpl == "assault_first_wave":
                visual["beat"] = ("arrows" if "arrows" in text.casefold() else
                                  "ladders" if any(k in text.casefold() for k in ("ladder", "climb")) else "first_rush")
            elif tpl == "assault_second_wave":
                visual["beat"] = ("breach" if "breach" in text.casefold() else
                                  "climb" if any(k in text.casefold() for k in ("climb", "what remains")) else "push")
            elif tpl == "elite_reserve":
                visual["beat"] = "command" if "behind them" in text.casefold() else "reserve"
            elif tpl == "defender_identity":
                visual["beat"] = "alone" if "not a famous commander" in text.casefold() else "among_thousands"
            elif tpl == "defender_supply":
                visual["beat"] = ("water" if "water" in text.casefold() else
                                  "stones" if "stone" in text.casefold() else
                                  "arrows" if "arrow" in text.casefold() else
                                  "messages" if "message" in text.casefold() else "wall")
            elif tpl == "rewind_map":
                visual["beat"] = "date" if any(k in text.casefold() for k in ("april", "morning")) else "route"
            elif tpl == "actor_closeup":
                visual["actorPreset"] = lead_preset
                visual["hero"] = hero_visible
                visual["expression"] = ("tired", "worried", "determined", "sad")[i % 4]
            elif tpl == "city_detail":
                visual["actorPreset"] = lead_preset
                visual["hero"] = hero_visible
                visual["variant"] = (i // 3) % 5
            elif tpl == "city_panorama":
                visual["chain"] = phase == "sea"
                visual["fall"] = p > .82
                visual["damage"] = min(.72, .08 + max(0,p-.25)*.72)

        shot["tpl"] = tpl
        shot["args"] = visual
        shot["in"] = {"type": "fade", "dur": .2} if i == 0 else (
            {"type": transitions[i % len(transitions)], "dur": .13, "dir": 1 if i % 2 else -1}
            if transitions[i % len(transitions)] != "cut" else {"type": "cut"})
        shot["sfx"] = sfx_for_shot(tpl, visual, i, sfx_root)
        shot["notes"] = "Character-led composite reconstruction; action beat is distinct and disputed details remain qualified."
        # Count the POV character only when the actor is actually selected for the shot.
        if (tpl in CUSTOM and tpl not in {"command_camp", "gun_crew"} and hero_visible)            or (tpl in STANDARD and HERO in json.dumps(visual)):
            hero_count += 1
        usage[tpl] = usage.get(tpl, 0) + 1
        last = tpl

    custom_count = sum(usage.get(x, 0) for x in CUSTOM)
    if custom_count < 260:
        raise ValueError(f"Insufficient bespoke siege shots: {custom_count}")
    for template, minimum in (("relief_galleys", 12), ("ship_portage", 8), ("tunnel_cutaway", 6)):
        actual = usage.get(template, 0)
        if actual < minimum:
            raise ValueError(f"Underrepresented historical set piece {template}: {actual} shots; require at least {minimum}.")
    panorama_cap = int(len(shots) * 0.15)
    if usage.get("city_panorama", 0) > panorama_cap:
        raise ValueError(f"City panorama overuse: {usage['city_panorama']} > {panorama_cap} shots (15% cap).")
    forbidden = {"scene", "close", "army", "split", "frame"}
    used_forbidden = sorted(name for name in forbidden if usage.get(name, 0))
    if used_forbidden:
        raise ValueError(f"Generic chibi Squire templates are forbidden in this film: {used_forbidden}")
    hero_ratio = hero_count / len(shots)
    if not (0.28 <= hero_ratio <= 0.42):
        raise ValueError(f"POV defender share must stay between 28% and 42%; got {hero_count}/{len(shots)} ({hero_ratio:.1%}).")

    story["title"] = "53 Days to the End of an Empire"
    story["genre"] = "historical-military-animation"
    story["engine"] = "H2 Squire 2D/vector — environment-led historical graphic reconstruction with mature-proportion actors"
    story["fps"] = 240
    story["hero_character"] = {"preset": HERO, "continuity": "fictional composite POV defender; appears in selected narrative beats, not a named historical person", "shot_count": hero_count, "ratio": round(hero_ratio, 4)}
    story["historical_caution"] = "Composite narrator; disputed ship-portage details, Giustiniani sequence and Constantine XI death circumstances are stated cautiously."
    story["shot_counts"] = usage
    story["shots"] = shots
    story["music"] = [
        {"start": 0, "end": round(duration * .055, 3), "bed": "mystery", "gainDb": -1},
        {"start": round(duration * .055, 3), "end": round(duration * .27, 3), "bed": "wonder", "gainDb": -1},
        {"start": round(duration * .27, 3), "end": round(duration * .46, 3), "bed": "curious", "gainDb": -1},
        {"start": round(duration * .46, 3), "end": round(duration * .72, 3), "bed": "tension", "gainDb": 0},
        {"start": round(duration * .72, 3), "end": round(duration * .91, 3), "bed": "war", "gainDb": 0},
        {"start": round(duration * .91, 3), "end": round(duration, 3), "bed": "emotional", "gainDb": -2}
    ]
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cfg_path = project / "config.json"
    cfg = load(cfg_path, {})
    cfg.update({"title": "53 Days to the End of an Empire", "aspect": "16:9", "resolution": "1080p",
                "fps": 240, "style": "dusk", "captions": True, "captionStyle": "squire", "bars": "none",
                "pack": "squire", "lang": "en", "music": {"enabled": True, "gainDb": -12},
                "sfx": {"enabled": True, "gainDb": -6}, "loudness": -14, "maxrate": "48M",
                "bufsize": "96M", "crf": 18, "renderPreset": "slow", "duration": round(duration, 3)})
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CONSTANTINOPLE HFR SHOTS: {len(shots)} | {duration:.1f}s | {custom_count} bespoke custom shots | {len(usage)} templates | POV hero {hero_count} ({hero_ratio:.1%}) | 240fps")
    print("SHOT COUNTS:", json.dumps(usage, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
