#!/usr/bin/env python3
"""Validate the machine-readable genre routing contract against the human matrix."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ROUTING_PATH = Path("tools/video/genre-routing.json")
MATRIX_PATH = Path("docs/GENRE_ROUTING_MATRIX.md")
EXPECTED_IDS = {
    "documentary-factual", "science-math-engineering", "narrative-animation",
    "product-software-demo", "tutorial-training", "interview-podcast",
    "music-video", "short-form-social", "advertisement-campaign", "hybrid-ai-generated",
}
ALLOWED_TOOLS = {
    "Authorized source media", "Remotion", "HyperFrames", "Manim", "D3/SVG",
    "Blender", "Three.js", "PixiJS", "Krita", "H2 Studio", "Playwright",
    "FFmpeg/ffprobe", "OpenTimelineIO", "PySceneDetect", "WhisperX", "Demucs",
    "Tesseract", "VideoDB (optional)", "AI media provider (opt-in)",
}
REQUIRED_FIELDS = (
    "intent", "creativeOwners", "primaryTools", "conditionalTools",
    "requiredEvidence", "criticalGuardrails", "qaChecks",
)
REQUIRED_CHECKS = {
    "documentary-factual": {"claim-source-ledger", "rights-and-release-check", "full-audiovisual-review"},
    "science-math-engineering": {"formula-and-units-check", "chart-data-reproducibility"},
    "narrative-animation": {"script-shot-coverage", "character-and-scene-continuity", "motion-contact-review"},
    "product-software-demo": {"product-version-and-path", "actual-ui-truth-check", "privacy-redaction-check"},
    "tutorial-training": {"learning-objective-coverage", "tested-step-proof"},
    "interview-podcast": {"consent-and-source-rights", "transcript-and-speaker-review", "caption-audio-alignment"},
    "music-video": {"music-and-footage-rights", "beat-map-review", "audio-visual-sync"},
    "short-form-social": {"vertical-safe-area", "mobile-caption-legibility", "platform-delivery-check"},
    "advertisement-campaign": {"approved-claims-check", "brand-and-likeness-rights", "legal-brand-approval"},
    "hybrid-ai-generated": {"model-and-prompt-provenance", "input-output-rights-check", "generated-media-artifact-check"},
}


def validate_data(data: dict[str, Any], matrix_text: str) -> list[str]:
    errors: list[str] = []
    if data.get("schemaVersion") != 1:
        errors.append("genre-routing schemaVersion must equal 1")
    universal = data.get("universalRules", {})
    required_universal = {
        "briefLedVisualDirection": True,
        "chooseSmallestEffectiveToolset": True,
        "h2IsDefaultStyle": False,
        "fullAudiovisualReviewRequiredForFinalApproval": True,
        "technicalPassEqualsArtisticApproval": False,
        "mutateParallelAssetLibrary": False,
    }
    for key, expected in required_universal.items():
        if universal.get(key) is not expected:
            errors.append(f"universalRules.{key} must be {str(expected).lower()}")
    profiles = data.get("profiles")
    if not isinstance(profiles, list):
        return errors + ["genre-routing profiles must be an array"]
    ids = [p.get("id") for p in profiles if isinstance(p, dict)]
    if len(ids) != len(profiles):
        errors.append("every genre profile must be an object")
    if len(ids) != len(set(ids)):
        errors.append("genre profile ids must be unique")
    if set(ids) != EXPECTED_IDS:
        errors.append(
            f"genre profile coverage mismatch; missing={sorted(EXPECTED_IDS-set(ids))}, "
            f"extra={sorted(set(ids)-EXPECTED_IDS)}"
        )
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        profile_id = profile.get("id", "<unknown>")
        for field in REQUIRED_FIELDS:
            value = profile.get(field)
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                errors.append(f"{profile_id}.{field} must be a non-empty string array")
        display_name = profile.get("displayName")
        if not isinstance(display_name, str) or display_name not in matrix_text:
            errors.append(f"{profile_id}.displayName must appear in {MATRIX_PATH}")
        tools = profile.get("primaryTools", []) + profile.get("conditionalTools", [])
        unknown = sorted(set(tools) - ALLOWED_TOOLS)
        if unknown:
            errors.append(f"{profile_id} contains unknown tools: {unknown}")
        if "H2 Studio" in set(profile.get("primaryTools", [])):
            errors.append(f"{profile_id} must not make H2 Studio a default primary tool")
        if "H2 Studio" in set(profile.get("conditionalTools", [])):
            if profile_id != "narrative-animation":
                errors.append("H2 Studio may only be conditional for narrative-animation")
            elif not any(token in " ".join(profile.get("criticalGuardrails", [])).lower()
                         for token in ("existing series", "explicit request", "do not impose")):
                errors.append("narrative-animation must guard H2 use behind series continuity or explicit request")
        missing_checks = REQUIRED_CHECKS.get(profile_id, set()) - set(profile.get("qaChecks", []))
        if missing_checks:
            errors.append(f"{profile_id} is missing QA checks: {sorted(missing_checks)}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    try:
        data = json.loads((root / ROUTING_PATH).read_text(encoding="utf-8"))
        matrix_text = (root / MATRIX_PATH).read_text(encoding="utf-8")
    except Exception as exc:
        return [f"Could not load genre routing contract/matrix: {exc}"]
    return validate_data(data, matrix_text)


def main() -> int:
    errors = validate()
    if errors:
        print("GENRE ROUTING VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    data = json.loads((ROOT / ROUTING_PATH).read_text(encoding="utf-8"))
    print("GENRE ROUTING VALIDATION: PASS")
    print(f"- Genre profiles: {len(data['profiles'])}")
    print("- Required ownership, tools, evidence, guardrails and QA checks present")
    print("- H2 is not a universal default; asset-library mutation remains prohibited")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
