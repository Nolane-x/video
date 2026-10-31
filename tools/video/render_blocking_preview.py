#!/usr/bin/env python3
"""Render low-resolution motion proofs for selected high-risk/story-critical shots."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREVIEW_IDS = ["s001", "s013", "s015", "s017", "s021", "s024", "s029"]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rendered_preview_digest(segments: list[dict[str, Any]]) -> str:
    ordered = [
        {"shotId": item["shotId"], "sha256": item["sha256"], "sizeBytes": item["sizeBytes"]}
        for item in sorted(segments, key=lambda item: item["shotId"])
    ]
    return sha256_bytes(canonical_bytes(ordered))


def plan_without_approval(plan: dict[str, Any]) -> dict[str, Any]:
    copy_plan = json.loads(json.dumps(plan))
    brief = copy_plan.get("creativeBrief")
    if isinstance(brief, dict):
        brief.pop("blockingPreviewApproval", None)
    return copy_plan


def build_preview_spec(
    plan: dict[str, Any],
    project_root: Path,
    tool_root: Path = ROOT,
) -> dict[str, Any]:
    fps = int(plan.get("fps") or 24)
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("plan needs a non-empty shots array")

    brief = plan.get("creativeBrief") if isinstance(plan.get("creativeBrief"), dict) else {}
    selected_ids = brief.get("blockingPreviewShotIds") or DEFAULT_PREVIEW_IDS
    if not isinstance(selected_ids, list) or not selected_ids:
        raise ValueError("creativeBrief.blockingPreviewShotIds must be a non-empty array")

    by_id = {str(shot.get("id")): shot for shot in shots if isinstance(shot, dict) and shot.get("id")}
    missing = [shot_id for shot_id in selected_ids if shot_id not in by_id]
    if missing:
        raise ValueError(f"blocking preview references unknown shot IDs: {missing}")

    segments = []
    for shot_id in selected_ids:
        shot = by_id[shot_id]
        start, end = shot.get("start"), shot.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            raise ValueError(f"invalid time range for blocking preview shot {shot_id}")
        start_frame = round(float(start) * fps)
        end_frame_exclusive = round(float(end) * fps)
        segments.append({
            "shotId": shot_id,
            "startSeconds": float(start),
            "endSeconds": float(end),
            "startFrame": start_frame,
            "endFrameExclusive": end_frame_exclusive,
            "durationFrames": end_frame_exclusive - start_frame,
            "framesArgument": f"{start_frame}-{end_frame_exclusive - 1}",
            "outputFile": f"{shot_id}.mp4",
            "requiresMotionProof": isinstance(shot.get("motionProof"), dict),
            "storyFunction": shot.get("storyFunction", ""),
        })

    tracked_files = [
        project_root / "src/OneMoreScroll.tsx",
        project_root / "src/Root.tsx",
        project_root / "h2-audio/packs/dem/audio.py",
        project_root / "h2-audio/requirements.txt",
        tool_root / "tools/video/render_blocking_preview.py",
    ]
    source_files = {}
    for path in tracked_files:
        if not path.is_file():
            raise FileNotFoundError(f"preview source dependency missing: {path}")
        source_files[str(path.relative_to(tool_root))] = sha256_file(path)

    base_plan = plan_without_approval(plan)
    spec = {
        "schemaVersion": 1,
        "compositionId": "OneMoreScroll",
        "fps": fps,
        "width": 1280,
        "height": 720,
        "previewScale": 0.5,
        "previewCodec": "h264",
        "sourcePlanSha256": sha256_bytes(canonical_bytes(base_plan)),
        "sourceFiles": source_files,
        "segments": segments,
    }
    spec["previewSpecSha256"] = sha256_bytes(canonical_bytes(spec))
    return spec


def render_segments(spec: dict[str, Any], project_root: Path, output_dir: Path) -> list[dict[str, Any]]:
    npx = shutil.which("npx")
    if not npx:
        raise RuntimeError("npx was not found; install the pinned Remotion dependencies first")
    output_dir.mkdir(parents=True, exist_ok=True)
    rendered = []
    for segment in spec["segments"]:
        output = output_dir / segment["outputFile"]
        command = [
            npx, "remotion", "render", "src/index.ts", spec["compositionId"], str(output),
            f"--frames={segment['framesArgument']}",
            f"--scale={spec['previewScale']}",
            f"--codec={spec['previewCodec']}",
            "--concurrency=2",
        ]
        subprocess.run(command, cwd=project_root, check=True)
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f"Remotion did not create a preview clip for {segment['shotId']}")
        rendered.append({
            **segment,
            "sizeBytes": output.stat().st_size,
            "sha256": sha256_file(output),
        })
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Storyboard JSON")
    parser.add_argument("--project-root", type=Path, default=ROOT / "video-projects/remotion")
    parser.add_argument("--output", type=Path, default=ROOT / "video-projects/remotion/out/blocking-preview")
    parser.add_argument("--dry-run", action="store_true", help="Write the preview spec without rendering clips")
    args = parser.parse_args()

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        spec = build_preview_spec(plan, args.project_root.resolve())
        if not args.dry_run:
            rendered = render_segments(spec, args.project_root.resolve(), args.output.resolve())
            spec["renderedSegments"] = rendered
            spec["previewArtifactSha256"] = rendered_preview_digest(rendered)
        args.output.mkdir(parents=True, exist_ok=True)
        manifest = args.output / "manifest.json"
        manifest.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("BLOCKING PREVIEW READY")
        print(f"- Preview spec SHA-256: {spec['previewSpecSha256']}")
        if not args.dry_run:
            print(f"- Rendered preview bundle SHA-256: {spec['previewArtifactSha256']}")
        print(f"- Selected shots: {', '.join(segment['shotId'] for segment in spec['segments'])}")
        print(f"- Manifest: {manifest}")
        if not args.dry_run:
            print(f"- Rendered clips: {len(spec.get('renderedSegments', []))}")
        return 0
    except Exception as exc:
        print(f"BLOCKING PREVIEW FAILED: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
