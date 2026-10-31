#!/usr/bin/env python3
"""Require a human approval attestation for the exact blocking-preview spec."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from render_blocking_preview import build_preview_spec, rendered_preview_digest, sha256_file

ROOT = Path(__file__).resolve().parents[2]


def validate_approval(plan: dict, manifest: dict, project_root: Path, manifest_path: Path) -> list[str]:
    errors = []
    current_spec = build_preview_spec(plan, project_root)
    approved_spec = manifest.get("previewSpecSha256")
    if not isinstance(approved_spec, str) or approved_spec != current_spec["previewSpecSha256"]:
        errors.append("preview manifest does not match the current storyboard/renderer spec; review the new preview")
    rendered_segments = manifest.get("renderedSegments")
    expected_ids = [segment["shotId"] for segment in current_spec["segments"]]
    if not isinstance(rendered_segments, list) or {item.get("shotId") for item in rendered_segments if isinstance(item, dict)} != set(expected_ids):
        errors.append("preview manifest must contain a rendered clip for every selected shot")
    else:
        for segment in rendered_segments:
            if not isinstance(segment, dict):
                errors.append("rendered preview segment entry must be an object")
                continue
            filename = segment.get("outputFile")
            if not isinstance(filename, str) or Path(filename).name != filename:
                errors.append(f"invalid preview filename for {segment.get('shotId')}")
                continue
            clip_path = manifest_path.parent / filename
            if not clip_path.is_file() or clip_path.stat().st_size <= 0:
                errors.append(f"rendered preview clip missing or empty: {filename}")
            elif sha256_file(clip_path) != segment.get("sha256") or clip_path.stat().st_size != segment.get("sizeBytes"):
                errors.append(f"rendered preview clip changed since manifest creation: {filename}")
        actual_digest = rendered_preview_digest(rendered_segments)
        if manifest.get("previewArtifactSha256") != actual_digest:
            errors.append("previewArtifactSha256 does not match the rendered preview clips")
    approval = plan.get("creativeBrief", {}).get("blockingPreviewApproval")
    if not isinstance(approval, dict):
        return errors + ["creativeBrief.blockingPreviewApproval is missing; full render is not authorised"]
    if approval.get("approved") is not True:
        errors.append("blockingPreviewApproval.approved must be true after the preview is watched")
    reviewer = approval.get("reviewerId")
    if not isinstance(reviewer, str) or not reviewer.strip() or reviewer.startswith("REPLACE_"):
        errors.append("blockingPreviewApproval.reviewerId is required")
    reviewed_at = approval.get("reviewedAtUtc")
    if not isinstance(reviewed_at, str) or not reviewed_at.endswith("Z"):
        errors.append("blockingPreviewApproval.reviewedAtUtc must be an ISO-8601 UTC timestamp ending in Z")
    else:
        try:
            datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("blockingPreviewApproval.reviewedAtUtc is not a valid ISO-8601 timestamp")
    if approval.get("previewSpecSha256") != current_spec["previewSpecSha256"]:
        errors.append("blockingPreviewApproval.previewSpecSha256 does not match the exact preview spec")
    if approval.get("previewArtifactSha256") != manifest.get("previewArtifactSha256"):
        errors.append("blockingPreviewApproval.previewArtifactSha256 does not match the exact rendered preview clips")
    ids = [segment["shotId"] for segment in current_spec["segments"]]
    reviewed_ids = approval.get("reviewedSegmentIds")
    if not isinstance(reviewed_ids, list) or set(reviewed_ids) != set(ids) or len(reviewed_ids) != len(ids):
        errors.append("reviewedSegmentIds must include every selected preview shot exactly once")
    notes = approval.get("reviewNotes")
    if not isinstance(notes, str) or len(notes.strip()) < 30:
        errors.append("blockingPreviewApproval.reviewNotes must include specific observations (at least 30 characters)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Storyboard JSON with approval metadata")
    parser.add_argument("--manifest", type=Path, required=True, help="Rendered blocking-preview manifest")
    parser.add_argument("--project-root", type=Path, default=ROOT / "video-projects/remotion")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors = validate_approval(plan, manifest, args.project_root.resolve(), args.manifest.resolve())
    except Exception as exc:
        print(f"PREVIEW APPROVAL VALIDATION: ERROR — {exc}")
        return 2
    if errors:
        print("PREVIEW APPROVAL: BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PREVIEW APPROVAL: PASS")
    print("- Exact storyboard and renderer preview spec verified")
    print("- Every selected preview segment was reviewed")
    print("- Explicit reviewer attestation recorded; full render may proceed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
