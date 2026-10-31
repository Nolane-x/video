#!/usr/bin/env python3
"""Validate repository-owned ChatGPT plugin manifests and Agent Skill frontmatter."""
from __future__ import annotations
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"^[a-z0-9][a-z0-9.-]{0,63}$")

def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifests = sorted((root / "plugins/chatgpt").glob("*/plugin.json"))
    if not manifests:
        errors.append("No plugin source manifests found")
    for path in manifests:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        if data.get("$schema") != SCHEMA:
            errors.append(f"{path}: invalid schema")
        if data.get("name") != path.parent.name or not NAME.fullmatch(str(data.get("name", ""))):
            errors.append(f"{path}: plugin name must match its directory")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", str(data.get("version", ""))):
            errors.append(f"{path}: invalid semantic version")
        interface = data.get("extensions", {}).get("com.openai", {}).get("interface", {})
        short = interface.get("shortDescription", "")
        if not isinstance(short, str) or not short.strip() or len(short) > 30:
            errors.append(f"{path}: shortDescription must be 1–30 characters")
        seen: set[str] = set()
        for skill in sorted(path.parent.glob("skills/*/SKILL.md")):
            lines = skill.read_text(encoding="utf-8").splitlines()
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
    return errors

if __name__ == "__main__":
    failures = validate()
    if failures:
        print("PLUGIN PACKAGE VALIDATION: FAIL")
        print("\n".join(f"- {x}" for x in failures))
        raise SystemExit(1)
    print("PLUGIN PACKAGE VALIDATION: PASS")
