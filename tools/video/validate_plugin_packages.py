#!/usr/bin/env python3
"""Validate repository-owned ChatGPT plugin manifests, skills and versioned registries."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"^[a-z0-9][a-z0-9.-]{0,63}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
PLUGIN_ROW = re.compile(r"^\|\s*[^|]+\s*\|\s*\d+\.\d+\.\d+\s*\|\s*https://chatgpt\.com/plugins/[^|]+\|", re.M)


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            errors.append(f"{path}: expected a JSON object")
            return None
        return value
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"{path}: cannot read UTF-8 text: {exc}")
        return ""


def validate_command_center(path: Path, manifest: dict, errors: list[str]) -> None:
    root = path.parent
    version = str(manifest.get("version", ""))
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    actual_names: set[str] = set()

    for skill in skills:
        lines = read_text(skill, errors).splitlines()
        if len(lines) < 4 or lines[0] != "---" or lines[3] != "---":
            errors.append(f"{skill}: malformed first four frontmatter lines")
            continue
        if not lines[1].startswith("name: ") or not lines[2].startswith("description: "):
            errors.append(f"{skill}: requires name and description")
            continue
        name = lines[1][6:].strip()
        if name:
            actual_names.add(name)

    if len(skills) != 29:
        errors.append(f"{root}: expected 29 bundled skills, found {len(skills)}")
    if len(actual_names) != len(skills):
        errors.append(f"{root}: skill frontmatter names are missing or duplicated")

    codex_path = root / ".codex-plugin/plugin.json"
    codex = load_json(codex_path, errors)
    if codex:
        if codex.get("name") != manifest.get("name"):
            errors.append(f"{codex_path}: plugin name differs from plugin.json")
        if codex.get("version") != version:
            errors.append(f"{codex_path}: version differs from plugin.json")
        codex_interface = codex.get("interface", {})
        public_interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
        if codex_interface.get("shortDescription") != public_interface.get("shortDescription"):
            errors.append(f"{codex_path}: shortDescription differs from plugin.json")

    readme = read_text(root / "README.md", errors)
    catalog = read_text(root / "SKILL-CATALOG.md", errors)
    registry = read_text(root / "references/PLUGIN-REGISTRY.md", errors)
    methodology = read_text(root / "references/PLUGIN-RESEARCH-METHODOLOGY.md", errors)

    for label, content in (
        ("README.md", readme),
        ("SKILL-CATALOG.md", catalog),
        ("PLUGIN-REGISTRY.md", registry),
        ("PLUGIN-RESEARCH-METHODOLOGY.md", methodology),
    ):
        header = re.search(r"^#.*?v(\d+\.\d+\.\d+)", content, re.M)
        if not header or header.group(1) != version:
            errors.append(f"{root}/{label}: version header must match {version}")

    catalog_names = set(re.findall(r"^- `([a-z0-9-]+)` —", catalog, re.M))
    if catalog_names != actual_names:
        missing = sorted(actual_names - catalog_names)
        stale = sorted(catalog_names - actual_names)
        errors.append(f"{root}/SKILL-CATALOG.md: skill index mismatch; missing={missing}, stale={stale}")

    readme_skills = re.search(r"\*\*(\d+) internal production skills\*\*", readme)
    readme_specialists = re.search(r"\*\*(\d+) focused specialist plugins\*\*", readme)
    catalog_skills = re.search(r"\*\*(\d+) internal skills\*\*", catalog)
    catalog_specialists = re.search(r"\*\*(\d+) separate specialist plugins\*\*", catalog)
    methodology_specialists = re.search(r"\*\*(\d+) separate specialist plugins\*\*", methodology)
    claims = [
        ("README.md internal skill count", readme_skills, len(skills)),
        ("README.md specialist count", readme_specialists, 37),
        ("SKILL-CATALOG.md internal skill count", catalog_skills, len(skills)),
        ("SKILL-CATALOG.md specialist count", catalog_specialists, 37),
        ("PLUGIN-RESEARCH-METHODOLOGY.md specialist count", methodology_specialists, 37),
    ]
    for label, match, expected in claims:
        if not match or int(match.group(1)) != expected:
            errors.append(f"{root}/{label}: expected {expected}")

    registry_count = len(PLUGIN_ROW.findall(registry))
    if registry_count != 37:
        errors.append(f"{root}/PLUGIN-REGISTRY.md: expected 37 specialist entries, found {registry_count}")

    description = str(manifest.get("description", ""))
    if "29 internal skills" not in description or "37 separately activated specialist plugins" not in description:
        errors.append(f"{path}: description must declare 29 internal skills and 37 separately activated specialist plugins")


def validate_genre_routing(root: Path, errors: list[str]) -> None:
    matrix_path = root / "docs/GENRE_ROUTING_MATRIX.md"
    master_path = root / ".agents/skills/video-production-master/SKILL.md"
    agents_path = root / "AGENTS.md"
    matrix = read_text(matrix_path, errors)
    master = read_text(master_path, errors)
    agents = read_text(agents_path, errors)

    required_genres = (
        "Documentary / factual story",
        "Science / mathematics / engineering explainer",
        "Narrative animation / short film",
        "Product / software demo",
        "Tutorial / training",
        "Interview / podcast / narration-led video",
        "Music video / rhythm-led edit",
        "Short-form social / vertical",
        "Advertisement / campaign",
        "Hybrid / AI-generated inserts",
    )
    for genre in required_genres:
        if genre not in matrix:
            errors.append(f"{matrix_path}: missing genre route {genre!r}")

    required_engines = (
        "Remotion", "HyperFrames", "Manim", "H2 Studio", "Blender",
        "Three.js / PixiJS", "OpenTimelineIO", "PySceneDetect",
        "Playwright / OCR", "WhisperX / Demucs", "FFmpeg / ffprobe",
    )
    for engine in required_engines:
        if engine not in matrix:
            errors.append(f"{matrix_path}: missing engine route {engine!r}")

    if "Genre and Production Routing Matrix" not in master:
        errors.append(f"{master_path}: must link the genre-routing matrix")
    if "conditional project profile" not in master or "not a universal style rule" not in master:
        errors.append(f"{master_path}: established H2 style must remain explicitly conditional")
    if "Do not impose this profile on other genres" not in agents:
        errors.append(f"{agents_path}: H2 style scope must be limited to its established series")

    plan_validator = root / "tools/video/evaluate_editorial_plan.py"
    review_validator = root / "tools/video/validate_editorial_review.py"
    review_template = root / "tools/video/editorial-review.template.json"
    if not plan_validator.is_file():
        errors.append(f"{plan_validator}: editorial plan preflight is required")
    if not review_validator.is_file():
        errors.append(f"{review_validator}: final audiovisual review validator is required")
    if not review_template.is_file():
        errors.append(f"{review_template}: final audiovisual review contract template is required")

    command_center = read_text(
        root / "plugins/chatgpt/nolane-video-command-center/skills/video-command-center/SKILL.md",
        errors,
    )
    director = read_text(
        root / "plugins/chatgpt/nolane-video-command-center/skills/video-production-director/SKILL.md",
        errors,
    )
    qa = read_text(
        root / "plugins/chatgpt/nolane-video-command-center/skills/video-quality-assurance/SKILL.md",
        errors,
    )
    for source, required in (
        (command_center, "evaluate_editorial_plan.py"),
        (command_center, "validate_editorial_review.py"),
        (director, "evaluate_editorial_plan.py"),
        (qa, "validate_editorial_review.py"),
        (qa, "Watch the complete video with sound at normal speed."),
    ):
        if required not in source:
            errors.append("Command Center/Director/QA skills must reference required editorial gate: " + required)


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifests = sorted((root / "plugins/chatgpt").glob("*/plugin.json"))
    if not manifests:
        errors.append("No plugin source manifests found")

    validate_genre_routing(root, errors)

    for path in manifests:
        data = load_json(path, errors)
        if data is None:
            continue
        if data.get("$schema") != SCHEMA:
            errors.append(f"{path}: invalid schema")
        if data.get("name") != path.parent.name or not NAME.fullmatch(str(data.get("name", ""))):
            errors.append(f"{path}: plugin name must match its directory")
        if not SEMVER.fullmatch(str(data.get("version", ""))):
            errors.append(f"{path}: invalid semantic version")

        interface = data.get("extensions", {}).get("com.openai", {}).get("interface", {})
        short = interface.get("shortDescription", "")
        if not isinstance(short, str) or not short.strip() or len(short) > 30:
            errors.append(f"{path}: shortDescription must be 1–30 characters")

        seen: set[str] = set()
        for skill in sorted(path.parent.glob("skills/*/SKILL.md")):
            lines = read_text(skill, errors).splitlines()
            if len(lines) < 4 or lines[0] != "---" or lines[3] != "---":
                errors.append(f"{skill}: malformed first four frontmatter lines")
                continue
            if not lines[1].startswith("name: ") or not lines[2].startswith("description: "):
                errors.append(f"{skill}: requires name and description")
                continue
            name, description = lines[1][6:].strip(), lines[2][13:].strip()
            if not name or not description:
                errors.append(f"{skill}: blank frontmatter name/description")
            if name in seen:
                errors.append(f"{skill}: duplicate skill name {name!r} in plugin")
            seen.add(name)

        if data.get("name") == "nolane-video-command-center":
            validate_command_center(path, data, errors)

    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        print("PLUGIN PACKAGE VALIDATION: FAIL")
        print("\n".join(f"- {x}" for x in failures))
        raise SystemExit(1)
    print("PLUGIN PACKAGE VALIDATION: PASS")
