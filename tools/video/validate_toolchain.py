#!/usr/bin/env python3
"""Validate the repo-owned, CPU-first video toolchain manifest."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXACT = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((root / "toolchain/manifest.json").read_text(encoding="utf-8"))
        package = json.loads((root / "toolchain/node/package.json").read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Could not load JSON manifests: {exc}"]
    if manifest.get("schemaVersion") != 1: errors.append("manifest.schemaVersion must equal 1")
    if manifest.get("platform", {}).get("node") != "24": errors.append("platform.node must be 24")
    if manifest.get("platform", {}).get("runner") != "ubuntu-24.04": errors.append("platform.runner must be ubuntu-24.04")
    if manifest.get("platform", {}).get("gpuRequired") is not False: errors.append("default toolchain must remain CPU-first")
    dependencies = package.get("dependencies", {})
    all_dependencies = {**dependencies, **package.get("devDependencies", {})}
    if not dependencies: errors.append("toolchain/node/package.json must include dependencies")
    for name, version in all_dependencies.items():
        if not isinstance(version, str) or not EXACT.fullmatch(version): errors.append(f"{name} must use exact x.y.z; found {version!r}")
    manifest_packages = {tool.get("package"): tool.get("version") for tool in manifest.get("tools", []) if tool.get("package")}
    for name, version in all_dependencies.items():
        if manifest_packages.get(name) != version: errors.append(f"manifest and package.json disagree for {name}")
    for name in manifest_packages:
        if name not in all_dependencies: errors.append(f"manifest lists npm package {name}, but package.json does not install it")
    core_packages = set(manifest.get("profiles", {}).get("core", {}).get("npmDependencies", []))
    if core_packages != set(dependencies): errors.append("profiles.core.npmDependencies must exactly match package.json dependencies")
    blender = manifest.get("profiles", {}).get("blender", {})
    if blender.get("required") is not False or blender.get("manualOnly") is not True: errors.append("Blender must remain optional and manual-only")
    if blender.get("version") != "5.2.3" or blender.get("archiveBytes", 0) > 400_000_000: errors.append("Blender profile version/size mismatch")
    if not blender.get("checksumUrl", "").endswith("blender-5.2.3.sha256"): errors.append("Blender must use official matching SHA-256 manifest")
    exclusions = {item.get("name") for item in manifest.get("excludedFromDefault", [])}
    for expected in ("ComfyUI and large diffusion/video weights", "Krita application"):
        if expected not in exclusions: errors.append(f"heavy tool must be excluded from default: {expected}")
    return errors

def main() -> int:
    errors = validate()
    if errors:
        print("VIDEO TOOLCHAIN VALIDATION: FAIL")
        for error in errors: print(f"- {error}")
        return 1
    manifest = json.loads((ROOT / "toolchain/manifest.json").read_text(encoding="utf-8"))
    package = json.loads((ROOT / "toolchain/node/package.json").read_text(encoding="utf-8"))
    print("VIDEO TOOLCHAIN VALIDATION: PASS")
    print(f"- Exact npm dependencies: {len(package['dependencies'])}")
    print(f"- Manifest tools: {len(manifest['tools'])}")
    print("- CPU-first core; optional checksum-verified Blender profile")
    return 0
if __name__ == "__main__": raise SystemExit(main())
