#!/usr/bin/env python3
"""Generate original CC0 sticker, meme-layout and caption-overlay packs for video editors."""
from __future__ import annotations

import html
import math
from pathlib import Path

CC0 = "CC0-1.0"
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"

STICKERS = [
    ("wow", "WOW", "surprise", "burst"),
    ("mind-blown", "MIND BLOWN", "surprise", "burst"),
    ("plot-twist", "PLOT TWIST", "story", "burst"),
    ("no-way", "NO WAY", "reaction", "bubble"),
    ("really", "REALLY?", "reaction", "bubble"),
    ("wait-a-minute", "WAIT A MINUTE", "reaction", "bubble"),
    ("hmm", "HMM…", "thinking", "bubble"),
    ("big-brain", "BIG BRAIN", "thinking", "badge"),
    ("idea", "IDEA!", "thinking", "badge"),
    ("aha", "AHA!", "thinking", "burst"),
    ("oops", "OOPS", "reaction", "badge"),
    ("bruh", "BRUH", "reaction", "bubble"),
    ("awkward", "AWKWARD", "reaction", "bubble"),
    ("sus", "SUS", "reaction", "badge"),
    ("cringe", "CRINGE", "reaction", "badge"),
    ("facepalm", "FACEPALM", "reaction", "bubble"),
    ("nice", "NICE!", "praise", "burst"),
    ("legend", "LEGEND", "praise", "badge"),
    ("respect", "RESPECT", "praise", "badge"),
    ("clap", "CLAP CLAP", "praise", "burst"),
    ("bravo", "BRAVO", "praise", "burst"),
    ("clean", "CLEAN!", "praise", "badge"),
    ("fail", "FAIL", "outcome", "burst"),
    ("win", "WIN", "outcome", "burst"),
    ("mission-complete", "MISSION COMPLETE", "outcome", "badge"),
    ("game-over", "GAME OVER", "outcome", "badge"),
    ("level-up", "LEVEL UP", "outcome", "burst"),
    ("loading", "LOADING…", "status", "badge"),
    ("error", "ERROR", "status", "badge"),
    ("success", "SUCCESS", "status", "badge"),
    ("warning", "WARNING", "status", "burst"),
    ("important", "IMPORTANT", "editorial", "badge"),
    ("fact-check", "FACT CHECK", "editorial", "badge"),
    ("true", "TRUE", "editorial", "badge"),
    ("false", "FALSE", "editorial", "badge"),
    ("myth", "MYTH", "editorial", "burst"),
    ("busted", "BUSTED", "editorial", "burst"),
    ("did-you-know", "DID YOU KNOW?", "editorial", "bubble"),
    ("quick-tip", "QUICK TIP", "editorial", "badge"),
    ("pro-tip", "PRO TIP", "editorial", "badge"),
    ("breaking", "BREAKING", "news", "banner"),
    ("live", "LIVE", "news", "badge"),
    ("exclusive", "EXCLUSIVE", "news", "badge"),
    ("update", "UPDATE", "news", "banner"),
    ("new", "NEW", "news", "burst"),
    ("hot-take", "HOT TAKE", "editorial", "burst"),
    ("versus", "VS", "editorial", "burst"),
    ("before", "BEFORE", "comparison", "badge"),
    ("after", "AFTER", "comparison", "badge"),
    ("part-one", "PART 01", "navigation", "badge"),
    ("part-two", "PART 02", "navigation", "badge"),
    ("step-one", "STEP 01", "navigation", "badge"),
    ("step-two", "STEP 02", "navigation", "badge"),
    ("step-three", "STEP 03", "navigation", "badge"),
    ("subscribe", "SUBSCRIBE", "social", "banner"),
    ("like", "LIKE", "social", "badge"),
    ("share", "SHARE", "social", "badge"),
    ("comment", "COMMENT", "social", "bubble"),
    ("follow", "FOLLOW", "social", "banner"),
    ("watch-next", "WATCH NEXT", "social", "banner"),
    ("save-this", "SAVE THIS", "social", "badge"),
    ("turn-on-notifications", "NOTIFICATIONS", "social", "badge"),
    ("đỉnh", "ĐỈNH!", "vietnamese", "burst"),
    ("không-thể-tin", "KHÔNG THỂ TIN!", "vietnamese", "bubble"),
    ("bất-ngờ", "BẤT NGỜ!", "vietnamese", "burst"),
    ("sự-thật", "SỰ THẬT", "vietnamese", "badge"),
    ("mẹo-hay", "MẸO HAY", "vietnamese", "badge"),
    ("lưu-ý", "LƯU Ý", "vietnamese", "burst"),
    ("thử-thách", "THỬ THÁCH", "vietnamese", "banner"),
    ("thành-công", "THÀNH CÔNG", "vietnamese", "badge"),
    ("thất-bại", "THẤT BẠI", "vietnamese", "badge"),
    ("hết-hồn", "HẾT HỒN!", "vietnamese", "burst"),
    ("xem-tiếp", "XEM TIẾP", "vietnamese", "banner"),
    ("đừng-bỏ-lỡ", "ĐỪNG BỎ LỠ", "vietnamese", "banner"),
]

PALETTES = [
    ("coral", "#ff705d", "#fff0e8", "#2a1820"),
    ("ocean", "#24b6c8", "#e9fcff", "#102b3b"),
    ("violet", "#9276ff", "#f5efff", "#241d45"),
    ("lime", "#b7d84b", "#f4fbdc", "#24301c"),
    ("amber", "#ffbd4a", "#fff5d9", "#392819"),
    ("pink", "#f277b8", "#fff0f7", "#3a1d32"),
    ("ice", "#76b9ef", "#edf8ff", "#1a2e45"),
    ("mono", "#252a35", "#ffffff", "#151922"),
]

MEME_LAYOUTS = [
    ("top-bottom", "Top / bottom caption", "Two bold caption bars framing an image placeholder."),
    ("expectation-reality", "Expectation vs reality", "Split comparison layout with two caption zones."),
    ("two-panel", "Two-panel reaction", "Setup and response panels with a center divider."),
    ("three-beat", "Three-beat story", "A three-frame setup, escalation and payoff layout."),
    ("zoom-reaction", "Zoom reaction frame", "Inset reaction window and a large caption band."),
    ("quote-reaction", "Quote and reaction", "Quote card beside a reaction window."),
    ("before-after", "Before and after", "Paired transformation panels with clear labels."),
    ("tiny-big", "Small problem / big reaction", "Scale contrast with a small prompt and large reaction panel."),
    ("plot-twist", "Plot twist", "A reveal panel with a turn marker and caption area."),
    ("choose-one", "Choose one", "Two competing options with a central choice marker."),
    ("timeline", "Timeline punchline", "Three time cards connected by a line."),
    ("chat-screenshot", "Chat conversation", "Two original message bubbles and response space."),
    ("ranking", "Ranking board", "Three ranked cards with editable labels."),
    ("myth-fact", "Myth / fact", "Two contrasting statement areas."),
    ("freeze-frame", "Freeze-frame caption", "A cinematic still placeholder with a large caption band."),
    ("editorial-cutaway", "Editorial cutaway", "Image window, side annotation and source note area."),
    ("mood-switch", "Mood switch", "A vertical split with contrasting scene and caption areas."),
    ("one-more-thing", "One more thing", "A main statement and a small reveal callout."),
    ("mini-comic", "Mini comic strip", "Four sequential comic cells."),
    ("scoreboard", "Scoreboard", "Two competitor panels and a result strip."),
]

CAPTION_LAYOUTS = [
    ("lower-third", "Lower third", "Name and role bar"),
    ("speaker-id", "Speaker identification", "Name, title and affiliation"),
    ("chapter-card", "Chapter marker", "Numbered chapter title"),
    ("source-note", "Source note", "Source and date attribution"),
    ("fact-callout", "Fact callout", "One key fact and supporting detail"),
    ("definition", "Definition", "Term and concise explanation"),
    ("quote-panel", "Quotation", "Quoted statement and speaker"),
    ("stat-card", "Statistic", "Large number and descriptive label"),
    ("warning-strip", "Warning", "Safety or accuracy notice"),
    ("tip-panel", "Practical tip", "One actionable recommendation"),
    ("map-label", "Map label", "Location and context"),
    ("timeline-label", "Timeline event", "Date, event and context"),
    ("data-label", "Data label", "Metric and unit"),
    ("section-title", "Section title", "Large chapter heading"),
    ("end-card", "End card", "Next action and follow-up prompt"),
    ("subtitle-emphasis", "Subtitle emphasis", "Short phrase with a highlighted keyword"),
]


def _star_points(cx, cy, outer, inner, count=12, rotation=-90):
    points = []
    for i in range(count * 2):
        angle = math.radians(rotation + i * 180 / count)
        radius = outer if i % 2 == 0 else inner
        points.append(f"{cx + math.cos(angle) * radius:.1f},{cy + math.sin(angle) * radius:.1f}")
    return " ".join(points)


def _sticker_svg(slug, label, palette, style, variant):
    accent, paper, ink = palette
    safe = html.escape(label)
    if style == "burst":
        backdrop = f'<polygon points="{_star_points(256,256,224,194,14,variant*7)}" fill="{accent}" stroke="{ink}" stroke-width="18" stroke-linejoin="round"/>'
        inner = f'<polygon points="{_star_points(256,256,188,168,14,variant*7)}" fill="{paper}" opacity=".98"/>'
        detail = '<path d="M115 150l-28-38m340 40 30-40M96 350l-34 24m380-18 34 28" stroke="'+ink+'" stroke-width="12" stroke-linecap="round"/>'
    elif style == "bubble":
        backdrop = f'<path d="M72 96Q72 58 112 58H400Q442 58 442 100V330Q442 370 400 370H260L178 447V370H112Q72 370 72 330Z" fill="{paper}" stroke="{ink}" stroke-width="18" stroke-linejoin="round"/>'
        inner = f'<path d="M93 110Q93 82 122 82H390Q420 82 420 112V316Q420 346 390 346H252L194 400V346H122Q93 346 93 316Z" fill="{accent}" opacity=".2"/>'
        detail = f'<circle cx="144" cy="124" r="10" fill="{accent}"/><circle cx="176" cy="124" r="10" fill="{accent}"/><circle cx="208" cy="124" r="10" fill="{accent}"/>'
    elif style == "banner":
        backdrop = f'<path d="M36 112L72 80H440L476 112V360L440 392H72L36 360Z" fill="{accent}" stroke="{ink}" stroke-width="18" stroke-linejoin="round"/>'
        inner = f'<path d="M58 128H454V344H58Z" fill="{paper}" opacity=".18"/>'
        detail = f'<path d="M72 176H408M72 320H408" stroke="{paper}" stroke-width="7" opacity=".55"/>'
    else:
        backdrop = f'<circle cx="256" cy="256" r="205" fill="{accent}" stroke="{ink}" stroke-width="18"/>'
        inner = f'<circle cx="256" cy="256" r="164" fill="{paper}" stroke="{ink}" stroke-width="7"/>'
        detail = f'<path d="M155 120L130 82M358 126L392 82" stroke="{ink}" stroke-width="12" stroke-linecap="round"/>'
    font_size = 62 if len(label) < 10 else 45 if len(label) < 15 else 34
    y = 270 if len(label) < 16 else 252
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(slug.replace("-", " ").title())}</title><desc id="desc">Original decorative video sticker: {safe}</desc>
<defs><filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="8" flood-color="#000" flood-opacity=".24"/></filter></defs>
<g filter="url(#shadow)">{backdrop}{inner}{detail}</g>
<text x="256" y="{y}" text-anchor="middle" dominant-baseline="middle" fill="{ink}" font-family="Arial,sans-serif" font-size="{font_size}" font-weight="900" letter-spacing="-1">{safe}</text>
<path d="M130 430Q256 462 382 430" fill="none" stroke="{accent}" stroke-width="8" stroke-linecap="round"/>
</svg>'''


def _meme_svg(slug, title, description, palette, layout, variant):
    accent, paper, ink = palette
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    top = f'<rect x="38" y="32" width="1204" height="108" rx="20" fill="{ink}"/><text x="640" y="101" fill="{paper}" text-anchor="middle" font-family="Arial,sans-serif" font-size="44" font-weight="900">TOP CAPTION — EDIT ME</text>'
    bottom = f'<rect x="38" y="580" width="1204" height="108" rx="20" fill="{ink}"/><text x="640" y="650" fill="{paper}" text-anchor="middle" font-family="Arial,sans-serif" font-size="44" font-weight="900">BOTTOM CAPTION — EDIT ME</text>'
    panel_bg = f'<rect x="38" y="160" width="1204" height="400" rx="26" fill="{paper}" stroke="{ink}" stroke-width="8"/>'
    if layout in {"expectation-reality", "before-after", "mood-switch", "scoreboard", "myth-fact"}:
        panel_bg = (
            f'<rect x="38" y="160" width="586" height="400" rx="24" fill="{paper}" stroke="{ink}" stroke-width="8"/>'
            f'<rect x="656" y="160" width="586" height="400" rx="24" fill="{paper}" stroke="{ink}" stroke-width="8"/>'
            f'<path d="M640 172V550" stroke="{accent}" stroke-width="12" stroke-dasharray="18 14"/>'
            f'<text x="331" y="205" fill="{accent}" text-anchor="middle" font-family="Arial" font-size="30" font-weight="bold">LEFT / SETUP</text>'
            f'<text x="949" y="205" fill="{accent}" text-anchor="middle" font-family="Arial" font-size="30" font-weight="bold">RIGHT / PAYOFF</text>'
        )
    elif layout in {"three-beat", "timeline", "mini-comic"}:
        panel_bg = "".join(
            f'<rect x="{38+i*407}" y="160" width="380" height="400" rx="22" fill="{paper}" stroke="{ink}" stroke-width="8"/>'
            f'<circle cx="{228+i*407}" cy="208" r="24" fill="{accent}"/><text x="{228+i*407}" y="218" fill="{ink}" text-anchor="middle" font-family="Arial" font-size="28" font-weight="bold">{i+1}</text>'
            for i in range(3)
        )
    elif layout == "chat-screenshot":
        panel_bg = (
            f'<rect x="70" y="160" width="1140" height="420" rx="30" fill="{paper}" stroke="{ink}" stroke-width="8"/>'
            f'<path d="M120 260Q120 225 158 225H670Q708 225 708 263V335Q708 372 670 372H240L178 425V372H158Q120 372 120 335Z" fill="{accent}" opacity=".9"/>'
            f'<path d="M450 410Q450 375 488 375H1040Q1078 375 1078 413V480Q1078 518 1040 518H950L890 564V518H488Q450 518 450 480Z" fill="{ink}" opacity=".9"/>'
            f'<text x="420" y="300" fill="{ink}" font-family="Arial" font-size="28" font-weight="bold">MESSAGE 01</text>'
            f'<text x="760" y="450" fill="{paper}" font-family="Arial" font-size="28" font-weight="bold">REPLY / REACTION</text>'
        )
    else:
        panel_bg += f'<rect x="85" y="205" width="1110" height="310" rx="20" fill="{accent}" opacity=".12" stroke="{accent}" stroke-width="4" stroke-dasharray="18 12"/>'
        panel_bg += f'<text x="640" y="385" fill="{accent}" text-anchor="middle" font-family="Arial" font-size="38" font-weight="bold">DROP IMAGE / REACTION HERE</text>'
    if layout in {"zoom-reaction", "quote-reaction", "one-more-thing"}:
        panel_bg += f'<circle cx="1020" cy="430" r="130" fill="{accent}" stroke="{ink}" stroke-width="12"/><text x="1020" y="420" text-anchor="middle" fill="{ink}" font-family="Arial" font-size="26" font-weight="bold">REACTION</text><text x="1020" y="455" text-anchor="middle" fill="{ink}" font-family="Arial" font-size="20">INSERT</text>'
    if layout == "plot-twist":
        panel_bg += f'<path d="M560 250L770 250L710 210M770 250L710 292" fill="none" stroke="{accent}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><text x="640" y="455" text-anchor="middle" fill="{accent}" font-size="54" font-family="Arial" font-weight="900">PLOT TWIST</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
<title id="title">{safe_title}</title><desc id="desc">{safe_description}. Original editable meme layout; replace caption placeholders and insert your own licensed footage.</desc>
<rect width="1280" height="720" fill="{accent}" opacity=".12"/>{top}{panel_bg}{bottom}
<text x="52" y="708" fill="{ink}" opacity=".68" font-family="Arial" font-size="12">ORIGINAL NOLANE TEMPLATE • {html.escape(layout.upper())} • VARIANT {variant+1}</text></svg>'''


def _caption_svg(slug, title, description, palette, layout, variant):
    accent, paper, ink = palette
    title_safe = html.escape(title)
    if layout in {"lower-third", "speaker-id", "source-note"}:
        shape = f'<rect x="40" y="535" width="900" height="140" rx="14" fill="{ink}" opacity=".94"/><rect x="40" y="535" width="18" height="140" fill="{accent}"/><text x="88" y="592" fill="{paper}" font-family="Arial" font-size="38" font-weight="bold">NAME / TITLE</text><text x="88" y="638" fill="{paper}" opacity=".84" font-family="Arial" font-size="22">ROLE • SOURCE • DATE</text>'
    elif layout in {"chapter-card", "section-title", "end-card"}:
        shape = f'<rect x="70" y="70" width="1140" height="580" rx="28" fill="{ink}" opacity=".94"/><rect x="70" y="70" width="1140" height="16" fill="{accent}"/><text x="130" y="240" fill="{accent}" font-family="Arial" font-size="30" font-weight="bold">CHAPTER / SECTION</text><text x="130" y="360" fill="{paper}" font-family="Arial" font-size="70" font-weight="bold">YOUR TITLE</text><text x="130" y="430" fill="{paper}" opacity=".8" font-family="Arial" font-size="28">Supporting subtitle or next action</text>'
    elif layout in {"quote-panel", "definition", "fact-callout"}:
        shape = f'<path d="M64 110H1100Q1200 110 1200 210V500Q1200 600 1100 600H64Z" fill="{ink}" opacity=".95"/><path d="M64 110H82V600H64Z" fill="{accent}"/><text x="140" y="245" fill="{accent}" font-family="Arial" font-size="30" font-weight="bold">KEY IDEA</text><text x="140" y="350" fill="{paper}" font-family="Arial" font-size="46" font-weight="bold">YOUR QUOTE / DEFINITION</text><text x="140" y="425" fill="{paper}" opacity=".82" font-family="Arial" font-size="24">Source / speaker / context</text>'
    elif layout in {"stat-card", "data-label"}:
        shape = f'<rect x="70" y="150" width="500" height="420" rx="36" fill="{ink}" opacity=".95"/><circle cx="170" cy="250" r="48" fill="{accent}"/><text x="260" y="275" fill="{accent}" font-family="Arial" font-size="34" font-weight="bold">METRIC</text><text x="125" y="420" fill="{paper}" font-family="Arial" font-size="110" font-weight="bold">00%</text><text x="130" y="490" fill="{paper}" opacity=".86" font-family="Arial" font-size="25">LABEL AND UNIT</text>'
    elif layout in {"warning-strip", "tip-panel"}:
        shape = f'<path d="M60 200H1190L1140 520H110Z" fill="{ink}" opacity=".95"/><circle cx="180" cy="360" r="78" fill="{accent}"/><text x="180" y="385" text-anchor="middle" fill="{ink}" font-family="Arial" font-size="62" font-weight="900">!</text><text x="300" y="330" fill="{accent}" font-family="Arial" font-size="35" font-weight="bold">IMPORTANT NOTE</text><text x="300" y="410" fill="{paper}" font-family="Arial" font-size="30">Add the fact, tip or safety reminder here</text>'
    elif layout in {"timeline-label", "map-label"}:
        shape = f'<path d="M80 530H1180" stroke="{accent}" stroke-width="14" stroke-linecap="round"/><circle cx="420" cy="530" r="27" fill="{paper}" stroke="{ink}" stroke-width="8"/><rect x="210" y="280" width="420" height="190" rx="22" fill="{ink}" opacity=".95"/><text x="250" y="345" fill="{accent}" font-family="Arial" font-size="32" font-weight="bold">DATE / LOCATION</text><text x="250" y="405" fill="{paper}" font-family="Arial" font-size="25">Event or place description</text>'
    else:
        shape = f'<rect x="50" y="500" width="1180" height="160" rx="18" fill="{ink}" opacity=".94"/><rect x="50" y="500" width="16" height="160" fill="{accent}"/><text x="100" y="568" fill="{paper}" font-family="Arial" font-size="42" font-weight="bold">EMPHASIZED SUBTITLE</text><text x="100" y="615" fill="{accent}" font-family="Arial" font-size="23">Highlight the essential phrase</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-labelledby="title desc">
<title id="title">{title_safe}</title><desc id="desc">{html.escape(description)}. Original transparent caption graphic; edit all placeholder copy.</desc>
{shape}
<text x="1220" y="700" text-anchor="end" fill="{ink}" opacity=".55" font-family="Arial" font-size="14">NOLANE • EDITABLE VECTOR • {variant+1:02d}</text></svg>'''


def generate_assets(root: Path, index: list[dict]) -> dict[str, int]:
    """Create a large, original and license-clean pack; no copyrighted meme characters/templates."""
    root = Path(root)
    sticker_dir = root / "originals" / "stickers"
    meme_dir = root / "originals" / "meme-templates"
    caption_dir = root / "originals" / "caption-presets"
    sticker_dir.mkdir(parents=True, exist_ok=True)
    meme_dir.mkdir(parents=True, exist_ok=True)
    caption_dir.mkdir(parents=True, exist_ok=True)
    sticker_count = 0
    for slug, label, category, preferred_style in STICKERS:
        for variant, palette_row in enumerate(PALETTES[:3]):
            palette_name, accent, paper, ink = palette_row
            palette = (accent, paper, ink)
            style = preferred_style if variant == 0 else ("bubble" if variant == 1 else "badge")
            filename = f"{slug}-{palette_name}.svg"
            path = sticker_dir / filename
            path.write_text(_sticker_svg(slug, label, palette, style, variant), encoding="utf-8")
            index.append({
                "id": f"sticker-{slug}-{palette_name}",
                "path": path.relative_to(root).as_posix(),
                "type": "original-video-sticker",
                "title": f"{label} — {palette_name.title()} sticker",
                "category": f"stickers / {category}",
                "keywords": [slug, label.lower(), category, "reaction", "transparent-background"],
                "license": CC0, "license_url": CC0_URL, "redistributable": True,
                "original_artwork": True, "format": "SVG", "canvas": "512x512",
                "note": "Original generic vector reaction sticker. No franchise character, brand logo, or copied meme image."
            })
            sticker_count += 1

    meme_count = 0
    for layout_index, (slug, title, description) in enumerate(MEME_LAYOUTS):
        for palette_index, palette_row in enumerate(PALETTES[:4]):
            palette_name, accent, paper, ink = palette_row
            palette = (accent, paper, ink)
            filename = f"{slug}-{palette_name}.svg"
            path = meme_dir / filename
            path.write_text(_meme_svg(slug, title, description, palette, slug, palette_index), encoding="utf-8")
            index.append({
                "id": f"meme-layout-{slug}-{palette_name}",
                "path": path.relative_to(root).as_posix(),
                "type": "original-meme-layout-template",
                "title": f"{title} — {palette_name.title()}",
                "category": "meme templates / editable reaction layout",
                "keywords": [slug, title.lower(), "meme", "reaction", "caption placeholder", "editable"],
                "license": CC0, "license_url": CC0_URL, "redistributable": True,
                "original_artwork": True, "format": "SVG", "canvas": "1280x720",
                "description": description,
                "note": "Original generic layout, not a reproduction of a copyrighted meme image or character. Replace all placeholder text and use footage you have rights to."
            })
            meme_count += 1

    caption_count = 0
    for layout_index, (slug, title, description) in enumerate(CAPTION_LAYOUTS):
        for palette_index, palette_row in enumerate(PALETTES[:4]):
            palette_name, accent, paper, ink = palette_row
            palette = (accent, paper, ink)
            filename = f"{slug}-{palette_name}.svg"
            path = caption_dir / filename
            path.write_text(_caption_svg(slug, title, description, palette, slug, palette_index), encoding="utf-8")
            index.append({
                "id": f"caption-preset-{slug}-{palette_name}",
                "path": path.relative_to(root).as_posix(),
                "type": "original-caption-overlay",
                "title": f"{title} — {palette_name.title()}",
                "category": "caption presets / lower thirds / editorial graphics",
                "keywords": [slug, title.lower(), "caption", "subtitle", "lower third", "overlay", "title card"],
                "license": CC0, "license_url": CC0_URL, "redistributable": True,
                "original_artwork": True, "format": "SVG", "canvas": "1280x720",
                "description": description,
                "note": "Original transparent vector overlay with editable placeholder copy."
            })
            caption_count += 1
    return {
        "stickers": sticker_count,
        "meme_templates": meme_count,
        "caption_overlays": caption_count,
        "total": sticker_count + meme_count + caption_count
    }


if __name__ == "__main__":
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="nolane-sticker-library-"))
    entries = []
    result = generate_assets(tmp, entries)
    print(result)
    print(f"Generated {len(entries)} original, independently indexed SVG assets in {tmp}")
