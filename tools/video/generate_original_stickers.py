#!/usr/bin/env python3
"""Generate original CC0 sticker art and editable meme-layout templates."""
from __future__ import annotations

import html
import math
from pathlib import Path


REACTION_WORDS = [
    "WOW", "LOL", "OMG", "YES", "NOPE", "BRUH", "YAY", "OOPS", "RIP", "GG",
    "SUS", "WAIT", "WHAT", "FACTS", "YIKES", "EPIC", "VIBE", "HYPE", "NICE",
    "COOL", "FIRE", "REAL", "MOOD", "SAME", "HUH", "OOF", "WILD", "TRUE",
    "CAP", "BASED", "SLAY", "ICONIC", "PLOT TWIST", "BIG BRAIN", "GENIUS",
    "FAIL", "WIN", "CLAP", "THANKS", "SORRY", "LOVE IT", "NO WAY", "BRAVO",
    "LET'S GO", "SAVAGE", "RELAX", "FOCUS", "LEGEND", "HELP", "BONK", "SHEESH",
    "TOO MUCH", "MIC DROP", "CONFIRMED", "BREAKING", "HOT TAKE", "FACT CHECK",
]
REACTION_PALETTES = [
    ("#ffcf33", "#ff6b35", "#271d33"),
    ("#85e7ff", "#4378ed", "#101d46"),
    ("#ff91c8", "#a74be0", "#30133e"),
    ("#8ff0a4", "#18a878", "#103c35"),
    ("#ff8c7d", "#ed3658", "#421a35"),
    ("#f5f2e8", "#b6c4d6", "#1d2938"),
    ("#b9a4ff", "#6452d8", "#211a4a"),
    ("#ffdd9a", "#f48a3d", "#49233a"),
]
DOODLE_TYPES = [
    "arrow-up", "arrow-down", "arrow-left", "arrow-right", "curved-arrow",
    "double-arrow", "check-mark", "cross-mark", "question-mark", "exclamation",
    "sparkle", "sparkle-cluster", "lightning", "heart", "broken-heart",
    "star", "crown", "fire", "target", "location-pin", "speech-bubble",
    "thought-bubble", "swipe", "tap", "click", "zoom", "highlight-circle",
    "underline-swoosh", "bracket-left", "bracket-right", "sound-lines",
    "confetti", "burst", "ribbon", "bookmark", "notification-dot",
    "loading-spinner", "play-button", "pause-button", "rewind",
]
MEME_LAYOUTS = [
    ("classic-top-bottom", "Classic top and bottom caption"),
    ("two-panel-compare", "Two-panel comparison"),
    ("four-panel-story", "Four-panel story grid"),
    ("vertical-reaction", "Vertical reaction / response"),
    ("side-by-side", "Side-by-side contrast"),
    ("quote-card", "Quote and reaction card"),
    ("timeline", "Before / during / after timeline"),
    ("choice-split", "This or that choice split"),
    ("progress-bars", "Expectation versus reality"),
    ("chat-screenshot", "Conversation / chat parody"),
    ("headline-card", "Headline and image card"),
    ("ranking-list", "Top five / ranking list"),
]


def _svg(body: str, width: int = 512, height: int = 512) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>Original CC0 video sticker</title>'
        f'<defs><filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feDropShadow dx="0" dy="12" stdDeviation="8" flood-color="#101522" flood-opacity=".24"/>'
        f'</filter><linearGradient id="shine" x1="0" y1="0" x2="1" y2="1">'
        f'<stop stop-color="#ffffff" stop-opacity=".42"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
        f'</linearGradient></defs>{body}</svg>'
    )


def _burst_points(cx: float, cy: float, outer: float, inner: float, points: int, offset: float = -math.pi / 2) -> str:
    out = []
    for i in range(points * 2):
        angle = offset + math.pi * i / points
        radius = outer if i % 2 == 0 else inner
        out.append(f"{cx + math.cos(angle)*radius:.1f},{cy + math.sin(angle)*radius:.1f}")
    return " ".join(out)


def _word_sticker(word: str, idx: int, variant: int) -> str:
    c1, c2, ink = REACTION_PALETTES[(idx + variant * 3) % len(REACTION_PALETTES)]
    label = html.escape(word, quote=False)
    font_size = 86 if len(word) <= 5 else 60 if len(word) <= 9 else 43
    rotation = ((idx * 13 + variant * 11) % 17) - 8
    if variant == 0:
        shape = f'<rect x="38" y="126" width="436" height="258" rx="88" fill="{c1}" stroke="#fff" stroke-width="22" filter="url(#shadow)"/>'
        detail = f'<path d="M100 166 Q256 110 410 165" fill="none" stroke="{c2}" stroke-width="12" stroke-linecap="round" opacity=".7"/>'
    elif variant == 1:
        shape = f'<polygon points="{_burst_points(256,256,222,188,16,idx*.07)}" fill="{c2}" stroke="#fff" stroke-width="22" stroke-linejoin="round" filter="url(#shadow)"/>'
        detail = f'<circle cx="256" cy="256" r="142" fill="{c1}" opacity=".42"/>'
    else:
        shape = f'<path d="M80 110 Q65 70 130 68 L380 68 Q449 73 436 140 L418 330 Q410 398 342 390 L268 386 L190 440 L190 382 L118 390 Q54 390 68 314Z" fill="{c1}" stroke="#fff" stroke-width="22" stroke-linejoin="round" filter="url(#shadow)"/>'
        detail = f'<path d="M108 128 Q165 100 220 122" fill="none" stroke="{c2}" stroke-width="12" stroke-linecap="round"/>'
    return _svg(
        f'<g transform="rotate({rotation} 256 256)">{shape}{detail}'
        f'<text x="256" y="282" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="Impact,Arial,sans-serif" font-size="{font_size}" font-weight="900" '
        f'letter-spacing="-2" fill="{ink}" stroke="#fff" stroke-width="8" paint-order="stroke" '
        f'stroke-linejoin="round">{label}</text>'
        f'<path d="M105 330 Q250 370 400 324" fill="none" stroke="{c2}" stroke-width="7" '
        f'stroke-linecap="round" opacity=".6"/></g>'
    )


def _face_sticker(idx: int) -> str:
    c1, c2, ink = REACTION_PALETTES[idx % len(REACTION_PALETTES)]
    eye_style = idx % 5
    mouth_style = idx % 6
    if eye_style == 0:
        eyes = '<circle cx="202" cy="218" r="19" fill="#20263a"/><circle cx="310" cy="218" r="19" fill="#20263a"/>'
    elif eye_style == 1:
        eyes = '<path d="M172 220 Q205 178 238 220 M280 220 Q313 178 346 220" fill="none" stroke="#20263a" stroke-width="18" stroke-linecap="round"/>'
    elif eye_style == 2:
        eyes = '<path d="M182 224 L222 188 L242 224 Z M290 224 L330 188 L350 224 Z" fill="#20263a"/>'
    elif eye_style == 3:
        eyes = '<circle cx="202" cy="218" r="25" fill="#fff"/><circle cx="310" cy="218" r="25" fill="#fff"/><circle cx="205" cy="220" r="11" fill="#20263a"/><circle cx="307" cy="220" r="11" fill="#20263a"/>'
    else:
        eyes = '<path d="M170 216 Q205 236 240 216 M280 216 Q315 236 350 216" fill="none" stroke="#20263a" stroke-width="17" stroke-linecap="round"/>'
    mouths = [
        '<path d="M190 310 Q256 375 322 310" fill="none" stroke="#20263a" stroke-width="20" stroke-linecap="round"/>',
        '<ellipse cx="256" cy="314" rx="26" ry="39" fill="#20263a"/>',
        '<path d="M190 315 Q255 275 322 315" fill="none" stroke="#20263a" stroke-width="19" stroke-linecap="round"/>',
        '<path d="M190 310 Q255 355 322 310 L308 343 Q256 376 205 343Z" fill="#20263a"/>',
        '<path d="M194 320 Q255 320 318 320" fill="none" stroke="#20263a" stroke-width="19" stroke-linecap="round"/>',
        '<path d="M202 310 Q256 360 310 310" fill="none" stroke="#20263a" stroke-width="12" stroke-linecap="round"/>',
    ]
    blush = '<ellipse cx="145" cy="275" rx="27" ry="13" fill="#ed6c87" opacity=".65"/><ellipse cx="367" cy="275" rx="27" ry="13" fill="#ed6c87" opacity=".65"/>'
    accents = '<path d="M100 115 L72 84 M408 115 L438 84" stroke="#fff" stroke-width="13" stroke-linecap="round"/>'
    return _svg(
        f'<circle cx="256" cy="256" r="211" fill="{c1}" stroke="#fff" stroke-width="25" filter="url(#shadow)"/>'
        f'<circle cx="256" cy="256" r="177" fill="url(#shine)"/>'
        f'{accents}{blush}{eyes}{mouths[mouth_style]}'
        f'<path d="M136 370 Q256 418 376 370" fill="none" stroke="{c2}" stroke-width="10" stroke-linecap="round"/>'
    )


def _doodle_sticker(kind: str, idx: int) -> str:
    c1, c2, ink = REACTION_PALETTES[(idx * 3) % len(REACTION_PALETTES)]
    common = 'fill="none" stroke="#fff" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"'
    inner = f'fill="none" stroke="{c2}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"'
    drawings = {
        "arrow-up": '<path d="M256 420 V105 M120 240 L256 95 L392 240"/>',
        "arrow-down": '<path d="M256 90 V405 M120 270 L256 415 L392 270"/>',
        "arrow-left": '<path d="M420 256 H100 M235 120 L90 256 L235 392"/>',
        "arrow-right": '<path d="M92 256 H412 M277 120 L422 256 L277 392"/>',
        "curved-arrow": '<path d="M110 300 Q90 110 270 125 Q420 130 390 320 M292 245 L395 345 L455 220"/>',
        "double-arrow": '<path d="M90 256 H420 M190 150 L82 256 L190 362 M320 150 L428 256 L320 362"/>',
        "check-mark": '<path d="M95 265 L210 365 L420 145"/>',
        "cross-mark": '<path d="M135 135 L377 377 M377 135 L135 377"/>',
        "question-mark": '<path d="M160 185 Q168 85 275 90 Q380 95 368 194 Q365 252 256 278 V310 M256 382 V390"/>',
        "exclamation": '<path d="M256 85 V300 M256 388 V395"/>',
        "sparkle": '<path d="M256 48 L291 214 L458 256 L291 292 L256 462 L220 292 L52 256 L220 214Z"/>',
        "sparkle-cluster": '<path d="M170 80 L192 180 L292 205 L192 230 L170 330 L148 230 L48 205 L148 180Z M360 260 L376 330 L446 346 L376 362 L360 432 L344 362 L274 346 L344 330Z"/>',
        "lightning": '<path d="M286 42 L132 265 H246 L208 468 L384 215 H267Z"/>',
        "heart": '<path d="M256 420 C35 265 65 100 182 104 C224 105 250 135 256 165 C270 118 312 98 357 106 C470 128 475 285 256 420Z"/>',
        "broken-heart": '<path d="M256 420 C35 265 65 100 182 104 C224 105 250 135 256 165 C270 118 312 98 357 106 C470 128 475 285 256 420Z M274 170 L230 260 L286 290 L246 372"/>',
        "star": '<polygon points="256,45 315,192 474,200 352,306 390,462 256,376 122,462 160,306 38,200 197,192"/>',
        "crown": '<path d="M75 365 L95 155 L205 245 L255 95 L310 245 L418 155 L438 365Z M95 410 H418"/>',
        "fire": '<path d="M256 450 C70 400 145 250 220 165 C230 250 280 242 285 85 C400 215 442 375 256 450Z"/>',
        "target": '<circle cx="256" cy="256" r="180"/><circle cx="256" cy="256" r="110"/><circle cx="256" cy="256" r="40"/>',
        "location-pin": '<path d="M256 455 C150 330 100 255 115 185 C130 85 215 60 256 60 C330 60 398 115 398 196 C398 275 335 360 256 455Z"/><circle cx="256" cy="194" r="47"/>',
        "speech-bubble": '<path d="M75 110 Q75 70 125 70 H390 Q438 70 438 120 V310 Q438 350 395 350 H220 L135 440 V350 H122 Q75 350 75 305Z"/>',
        "thought-bubble": '<circle cx="255" cy="205" r="145"/><circle cx="128" cy="395" r="35"/><circle cx="80" cy="465" r="18"/>',
        "swipe": '<path d="M90 270 Q250 80 420 260 M315 150 L430 260 L310 370"/>',
        "tap": '<path d="M215 400 V200 Q215 165 250 165 Q285 165 285 200 V270 L330 240 Q365 222 382 252 Q396 278 370 303 L298 404Z"/>',
        "click": '<path d="M256 60 V130 M256 382 V452 M60 256 H130 M382 256 H452 M118 118 L168 168 M344 344 L394 394 M394 118 L344 168 M168 344 L118 394"/>',
        "zoom": '<circle cx="220" cy="220" r="120"/><path d="M310 310 L430 430 M175 220 H265 M220 175 V265"/>',
        "highlight-circle": '<ellipse cx="256" cy="256" rx="190" ry="140" transform="rotate(-18 256 256)"/>',
        "underline-swoosh": '<path d="M55 330 Q230 260 440 310"/>',
        "bracket-left": '<path d="M330 85 H150 V425 H330"/>',
        "bracket-right": '<path d="M180 85 H360 V425 H180"/>',
        "sound-lines": '<path d="M155 170 Q70 256 155 342 M230 110 Q105 256 230 402 M310 70 Q140 256 310 442"/>',
        "confetti": '<path d="M130 100 L170 145 M330 70 L350 125 M415 215 L365 235 M90 320 L145 300 M260 390 L280 445 M390 370 L350 405"/>',
        "burst": '<polygon points="256,45 290,170 420,80 350,205 475,255 350,305 420,430 290,342 256,465 222,342 92,430 162,305 37,255 162,205 92,80 222,170"/>',
        "ribbon": '<path d="M130 95 H385 V345 L320 300 L255 350 L190 300 L130 345Z"/>',
        "bookmark": '<path d="M150 70 H365 V445 L256 365 L150 445Z"/>',
        "notification-dot": '<circle cx="256" cy="256" r="150"/><circle cx="385" cy="125" r="64" fill="#ff425e" stroke="#fff" stroke-width="18"/>',
        "loading-spinner": '<path d="M256 70 A186 186 0 1 1 86 180" />',
        "play-button": '<polygon points="150,75 420,256 150,437"/>',
        "pause-button": '<rect x="135" y="90" width="82" height="332" rx="20"/><rect x="295" y="90" width="82" height="332" rx="20"/>',
        "rewind": '<path d="M250 100 L70 256 L250 412Z M440 100 L260 256 L440 412Z"/>',
    }
    drawing = drawings.get(kind, drawings["sparkle"])
    return _svg(
        f'<g {common}>{drawing}</g>'
        f'<g transform="scale(.86) translate(41 41)" {inner}>{drawing}</g>'
    )


def _meme_template_svg(layout: str, title: str, index: int) -> str:
    width, height = (1080, 1920) if index % 4 == 0 else (1080, 1350) if index % 4 == 1 else (1080, 1080) if index % 4 == 2 else (1920, 1080)
    pad = int(min(width, height) * .055)
    ink = ["#f7f3e8", "#182232", "#ffffff", "#111827"][index % 4]
    accent = ["#f15b4a", "#33b5a4", "#6655d9", "#f2b84b", "#2575d8"][index % 5]
    outer = f'<rect x="0" y="0" width="{width}" height="{height}" fill="{ink}"/>'
    def box(x, y, w, h, label, fill="#d9e0eb"):
        return (
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" '
            f'stroke="{accent}" stroke-width="8" stroke-dasharray="20 14"/>'
            f'<text x="{x+w/2}" y="{y+h/2}" text-anchor="middle" dominant-baseline="middle" '
            f'font-family="Arial,sans-serif" font-size="{max(24,min(56,int(h*.13)))}" '
            f'font-weight="700" fill="#46546a">{label}</text>'
        )
    top_h = int(height * .17)
    bottom_h = int(height * .17)
    if layout == "classic-top-bottom":
        content = box(pad, top_h + pad, width-2*pad, height-top_h-bottom_h-2*pad, "DROP IMAGE / CLIP HERE")
        content += f'<text x="{width/2}" y="{top_h/2}" font-size="{int(top_h*.28)}" text-anchor="middle" dominant-baseline="middle" font-family="Impact,Arial" fill="{accent}">TOP CAPTION</text>'
        content += f'<text x="{width/2}" y="{height-bottom_h/2}" font-size="{int(bottom_h*.28)}" text-anchor="middle" dominant-baseline="middle" font-family="Impact,Arial" fill="{accent}">BOTTOM CAPTION</text>'
    elif layout in {"two-panel-compare", "side-by-side", "choice-split"}:
        gap = pad//2
        half = (width-2*pad-gap)//2
        content = box(pad, top_h+pad, half, height-top_h-bottom_h-2*pad, "PANEL A")
        content += box(pad+half+gap, top_h+pad, half, height-top_h-bottom_h-2*pad, "PANEL B")
        content += f'<text x="{width/2}" y="{top_h/2}" font-size="{int(top_h*.25)}" text-anchor="middle" dominant-baseline="middle" font-family="Impact,Arial" fill="{accent}">CAPTION / COMPARISON</text>'
        content += f'<text x="{width/2}" y="{height-bottom_h/2}" font-size="{int(bottom_h*.24)}" text-anchor="middle" dominant-baseline="middle" font-family="Arial" fill="{accent}">YOUR TAKE</text>'
    elif layout == "four-panel-story":
        gap = pad//2
        halfw = (width-2*pad-gap)//2
        halfh = (height-2*pad-gap-top_h-bottom_h)//2
        for row in range(2):
            for col in range(2):
                x = pad + col*(halfw+gap)
                y = top_h + pad + row*(halfh+gap)
                content += box(x,y,halfw,halfh,f"PANEL {row*2+col+1}")
        content += f'<text x="{width/2}" y="{top_h/2}" font-size="{int(top_h*.25)}" text-anchor="middle" dominant-baseline="middle" font-family="Impact,Arial" fill="{accent}">4-PANEL STORY</text>'
    elif layout == "vertical-reaction":
        content = box(pad, top_h+pad, width-2*pad, int(height*.50), "MAIN IMAGE / VIDEO")
        content += box(pad, int(height*.67), width-2*pad, int(height*.17), "REACTION / PUNCHLINE")
        content += f'<text x="{width/2}" y="{top_h/2}" font-size="{int(top_h*.25)}" text-anchor="middle" dominant-baseline="middle" font-family="Impact,Arial" fill="{accent}">REACTION FORMAT</text>'
    elif layout in {"quote-card", "headline-card"}:
        content = box(pad, int(height*.30), width-2*pad, int(height*.42), "IMAGE / QUOTE BACKDROP")
        content += f'<rect x="{pad}" y="{int(height*.72)}" width="{width-2*pad}" height="{int(height*.18)}" rx="24" fill="{accent}"/>'
        content += f'<text x="{width/2}" y="{int(height*.81)}" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="{int(height*.035)}" font-weight="700" fill="#fff">HEADLINE / QUOTE TEXT</text>'
    elif layout == "timeline":
        content = box(pad, int(height*.18), width-2*pad, int(height*.22), "BEFORE")
        content += box(pad, int(height*.44), width-2*pad, int(height*.22), "DURING")
        content += box(pad, int(height*.70), width-2*pad, int(height*.22), "AFTER")
    elif layout == "progress-bars":
        content = box(pad, int(height*.18), width-2*pad, int(height*.28), "EXPECTATION")
        content += box(pad, int(height*.54), width-2*pad, int(height*.28), "REALITY")
    elif layout == "chat-screenshot":
        for row in range(4):
            y = pad + row*int((height-2*pad)/4)
            x = pad if row%2==0 else width*.34
            w = width*.62
            content += f'<rect x="{x}" y="{y}" width="{w}" height="{int(height*.13)}" rx="36" fill="{accent if row%2 else "#d9e0eb"}"/>'
            content += f'<text x="{x+w/2}" y="{y+height*.065}" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="{int(height*.024)}" fill="{ "#fff" if row%2 else "#273247"}">MESSAGE {row+1}</text>'
    elif layout == "ranking-list":
        content = box(pad, int(height*.1), width-2*pad, int(height*.78), "TOP 5 / RANKING LIST")
    else:
        content = box(pad, int(height*.2), width-2*pad, int(height*.6), "DROP IMAGE / CLIP HERE")
    title_text = html.escape(title)
    footer = (
        f'<rect x="0" y="{height-28}" width="{width}" height="28" fill="{accent}"/>'
        f'<text x="{pad}" y="{height-48}" font-family="Arial" font-size="{max(20,int(height*.018))}" fill="{accent}">{title_text}</text>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><title>{title_text} — original editable meme template</title>'
        f'{outer}{content}{footer}</svg>'
    )


def generate_original_stickers(root: Path, index: list, cc0_url: str) -> tuple[int, int]:
    sticker_dir = root / "originals" / "stickers"
    meme_dir = root / "originals" / "meme-templates"
    sticker_dir.mkdir(parents=True, exist_ok=True)
    meme_dir.mkdir(parents=True, exist_ok=True)
    sticker_count = 0
    for i, word in enumerate(REACTION_WORDS):
        for variant in range(2):
            asset_id = f"reaction-{i+1:03d}-{variant+1}"
            path = sticker_dir / f"{asset_id}.svg"
            path.write_text(_word_sticker(word, i, variant), encoding="utf-8")
            index.append({
                "id": asset_id, "path": path.relative_to(root).as_posix(),
                "type": "original-sticker-reaction", "title": f"{word} reaction sticker",
                "category": "Stickers / reaction words / transparent SVG",
                "license": "CC0-1.0", "license_url": cc0_url, "redistributable": True,
                "editable_vector": True, "transparent_background": True
            })
            sticker_count += 1
    for i in range(48):
        asset_id = f"reaction-face-{i+1:03d}"
        path = sticker_dir / f"{asset_id}.svg"
        path.write_text(_face_sticker(i), encoding="utf-8")
        index.append({
            "id": asset_id, "path": path.relative_to(root).as_posix(),
            "type": "original-sticker-face", "title": f"Reaction face sticker {i+1}",
            "category": "Stickers / expressive faces / transparent SVG",
            "license": "CC0-1.0", "license_url": cc0_url, "redistributable": True,
            "editable_vector": True, "transparent_background": True
        })
        sticker_count += 1
    for i, kind in enumerate(DOODLE_TYPES):
        asset_id = f"doodle-{kind}"
        path = sticker_dir / f"{asset_id}.svg"
        path.write_text(_doodle_sticker(kind, i), encoding="utf-8")
        index.append({
            "id": asset_id, "path": path.relative_to(root).as_posix(),
            "type": "original-sticker-doodle", "title": kind.replace("-", " ").title(),
            "category": "Stickers / arrows / doodles / annotation SVG",
            "license": "CC0-1.0", "license_url": cc0_url, "redistributable": True,
            "editable_vector": True, "transparent_background": True
        })
        sticker_count += 1
    meme_count = 0
    for layout_index, (layout, title) in enumerate(MEME_LAYOUTS):
        for variant in range(4):
            asset_id = f"meme-{layout}-{variant+1}"
            path = meme_dir / f"{asset_id}.svg"
            path.write_text(_meme_template_svg(layout, title, layout_index*4+variant), encoding="utf-8")
            index.append({
                "id": asset_id, "path": path.relative_to(root).as_posix(),
                "type": "original-meme-layout-template", "title": title,
                "category": "Meme templates / editable SVG / image and caption placeholders",
                "layout": layout, "license": "CC0-1.0", "license_url": cc0_url,
                "redistributable": True, "editable_vector": True,
                "note": "Original generic layout template; replace placeholders with media you own or are licensed to use."
            })
            meme_count += 1
    return sticker_count, meme_count


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as directory:
        sample = []
        stickers, memes = generate_original_stickers(Path(directory), sample, "https://creativecommons.org/publicdomain/zero/1.0/")
        print(f"generated {stickers} stickers and {memes} meme templates")
