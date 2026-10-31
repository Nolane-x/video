#!/usr/bin/env python3
"""Validate the repo-owned, CPU-first video toolchain manifest."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXACT = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def _validate_optional_profile(
    profile_name: str,
    profile: dict,
    root: Path,
    errors: list[str],
    *,
    expected_manual_only: bool,
) -> None:
    if profile.get("required") is not False:
        errors.append(f"{profile_name} must remain optional (required=false)")
    if profile.get("manualOnly") is not expected_manual_only:
        errors.append(
            f"{profile_name}.manualOnly must be {str(expected_manual_only).lower()}"
        )

    workflow = profile.get("workflow")
    if not isinstance(workflow, str) or not workflow.startswith(".github/workflows/"):
        errors.append(f"{profile_name} must declare its repository workflow")
    elif not (root / workflow).is_file():
        errors.append(f"{profile_name} workflow does not exist: {workflow}")

    triggers = profile.get("triggers", [])
    if expected_manual_only:
        if triggers != ["workflow_dispatch"]:
            errors.append(
                f"{profile_name} must expose workflow_dispatch only; "
                "manual-only profiles must not run automatically"
            )
    else:
        has_scoped_pr = any(
            isinstance(item, str) and item.startswith("pull_request paths:")
            for item in triggers
        )
        has_manual_dispatch = "workflow_dispatch" in triggers
        if not (has_scoped_pr and has_manual_dispatch):
            errors.append(
                f"{profile_name} must use path-scoped pull_request triggers "
                "and remain manually dispatchable"
            )


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(
            (root / "toolchain/manifest.json").read_text(encoding="utf-8")
        )
        package = json.loads(
            (root / "toolchain/node/package.json").read_text(encoding="utf-8")
        )
    except Exception as exc:
        return [f"Could not load JSON manifests: {exc}"]

    if manifest.get("schemaVersion") != 1:
        errors.append("manifest.schemaVersion must equal 1")
    if manifest.get("platform", {}).get("node") != "24":
        errors.append("platform.node must be 24")
    if manifest.get("platform", {}).get("runner") != "ubuntu-24.04":
        errors.append("platform.runner must be ubuntu-24.04")
    if manifest.get("platform", {}).get("gpuRequired") is not False:
        errors.append("default toolchain must remain CPU-first")

    dependencies = package.get("dependencies", {})
    all_dependencies = {
        **dependencies,
        **package.get("devDependencies", {}),
    }
    if not dependencies:
        errors.append("toolchain/node/package.json must include dependencies")
    for name, version in all_dependencies.items():
        if not isinstance(version, str) or not EXACT.fullmatch(version):
            errors.append(f"{name} must use exact x.y.z; found {version!r}")

    manifest_packages = {
        tool.get("package"): tool.get("version")
        for tool in manifest.get("tools", [])
        if tool.get("package")
    }
    for name, version in all_dependencies.items():
        if manifest_packages.get(name) != version:
            errors.append(f"manifest and package.json disagree for {name}")
    for name in manifest_packages:
        if name not in all_dependencies:
            errors.append(
                f"manifest lists npm package {name}, but package.json does not install it"
            )

    core_packages = set(
        manifest.get("profiles", {}).get("core", {}).get("npmDependencies", [])
    )
    if core_packages != set(dependencies):
        errors.append(
            "profiles.core.npmDependencies must exactly match package.json dependencies"
        )

    profiles = manifest.get("profiles", {})
    blender = profiles.get("blender", {})
    _validate_optional_profile(
        "blender", blender, root, errors, expected_manual_only=False
    )
    if (
        blender.get("version") != "5.2.3"
        or not isinstance(blender.get("archiveBytes"), int)
        or blender.get("archiveBytes", 0) > 400_000_000
    ):
        errors.append("Blender profile version/size mismatch")
    if not str(blender.get("url", "")).startswith(
        "https://download.blender.org/release/Blender5.2/"
    ):
        errors.append("Blender must use the official version-matched download host")
    if not str(blender.get("checksumUrl", "")).endswith(
        "blender-5.2.3.sha256"
    ):
        errors.append("Blender must use official matching SHA-256 manifest")

    manim = profiles.get("manim", {})
    _validate_optional_profile(
        "manim", manim, root, errors, expected_manual_only=False
    )
    audio_ml = profiles.get("audioML", {})
    _validate_optional_profile(
        "audioML", audio_ml, root, errors, expected_manual_only=True
    )

    exclusions = {
        item.get("name")
        for item in manifest.get("excludedFromDefault", [])
    }
    for expected in (
        "ComfyUI and large diffusion/video weights",
        "Krita application",
    ):
        if expected not in exclusions:
            errors.append(f"heavy tool must be excluded from default: {expected}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("VIDEO TOOLCHAIN VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    manifest = json.loads(
        (ROOT / "toolchain/manifest.json").read_text(encoding="utf-8")
    )
    package = json.loads(
        (ROOT / "toolchain/node/package.json").read_text(encoding="utf-8")
    )
    print("VIDEO TOOLCHAIN VALIDATION: PASS")
    print(f"- Exact npm dependencies: {len(package['dependencies'])}")
    print(f"- Manifest tools: {len(manifest['tools'])}")
    print("- CPU-first core; optional path-scoped Manim/Blender proof profiles")
    print("- Audio ML remains manual-only; no model weights are installed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
