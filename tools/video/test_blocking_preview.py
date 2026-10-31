import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_blocking_preview import build_preview_spec, rendered_preview_digest, sha256_file
from validate_preview_approval import validate_approval

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "video-projects/remotion"
PLAN_PATH = PROJECT / "public/story/shots.json"


def load_plan():
    return json.loads(PLAN_PATH.read_text(encoding="utf-8"))


def rendered_manifest(plan, output_dir: Path):
    spec = build_preview_spec(plan, PROJECT)
    output_dir.mkdir(parents=True, exist_ok=True)
    rendered = []
    for segment in spec["segments"]:
        path = output_dir / segment["outputFile"]
        path.write_bytes(("deterministic test clip " + segment["shotId"]).encode("utf-8"))
        rendered.append({
            **segment,
            "sizeBytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    spec["renderedSegments"] = rendered
    spec["previewArtifactSha256"] = rendered_preview_digest(rendered)
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return spec, manifest_path


class BlockingPreviewTests(unittest.TestCase):
    def test_preview_spec_selects_story_and_motion_critical_segments(self):
        plan = load_plan()
        spec = build_preview_spec(plan, PROJECT)
        ids = [segment["shotId"] for segment in spec["segments"]]
        self.assertEqual(ids, ["s001", "s013", "s015", "s017", "s021", "s024", "s029"])
        self.assertEqual(spec["fps"], 24)
        self.assertEqual(spec["previewScale"], 0.5)
        self.assertTrue(all(segment["durationFrames"] > 0 for segment in spec["segments"]))
        self.assertTrue(any(segment["requiresMotionProof"] for segment in spec["segments"]))

    def test_approval_metadata_does_not_change_preview_spec_hash(self):
        plan = load_plan()
        first = build_preview_spec(plan, PROJECT)["previewSpecSha256"]
        plan["creativeBrief"]["blockingPreviewApproval"] = {
            "approved": True,
            "reviewerId": "owner",
            "reviewedAtUtc": "2026-10-31T13:00:00Z",
        }
        second = build_preview_spec(plan, PROJECT)["previewSpecSha256"]
        self.assertEqual(first, second)

    def test_storyboard_timing_change_invalidates_preview_spec(self):
        plan = load_plan()
        first = build_preview_spec(plan, PROJECT)["previewSpecSha256"]
        plan["shots"][12]["end"] += 0.25
        second = build_preview_spec(plan, PROJECT)["previewSpecSha256"]
        self.assertNotEqual(first, second)

    def test_unknown_preview_shot_is_rejected(self):
        plan = load_plan()
        plan["creativeBrief"]["blockingPreviewShotIds"] = ["missing-shot"]
        with self.assertRaisesRegex(ValueError, "unknown shot IDs"):
            build_preview_spec(plan, PROJECT)

    def test_pending_approval_blocks_full_render(self):
        plan = load_plan()
        spec = build_preview_spec(plan, PROJECT)
        plan["creativeBrief"]["blockingPreviewApproval"] = {"approved": False}
        errors = validate_approval(plan, spec, PROJECT, PROJECT / "out/blocking-preview/manifest.json")
        self.assertTrue(any("must be true" in item for item in errors))

    def test_exact_approved_preview_bundle_is_accepted(self):
        plan = load_plan()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            manifest, manifest_path = rendered_manifest(plan, output)
            approval = {
                "approved": True,
                "reviewerId": "human-owner",
                "reviewedAtUtc": "2026-10-31T13:00:00Z",
                "previewSpecSha256": manifest["previewSpecSha256"],
                "previewArtifactSha256": manifest["previewArtifactSha256"],
                "reviewedSegmentIds": [segment["shotId"] for segment in manifest["segments"]],
                "reviewNotes": "Reviewed every selected motion clip and their audio; framing, contacts and story clarity are acceptable.",
            }
            plan["creativeBrief"]["blockingPreviewApproval"] = approval
            self.assertEqual(validate_approval(plan, manifest, PROJECT, manifest_path), [])

    def test_modified_preview_clip_invalidates_approval(self):
        plan = load_plan()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            manifest, manifest_path = rendered_manifest(plan, output)
            approval = {
                "approved": True,
                "reviewerId": "human-owner",
                "reviewedAtUtc": "2026-10-31T13:00:00Z",
                "previewSpecSha256": manifest["previewSpecSha256"],
                "previewArtifactSha256": manifest["previewArtifactSha256"],
                "reviewedSegmentIds": [segment["shotId"] for segment in manifest["segments"]],
                "reviewNotes": "Reviewed every selected motion clip and their audio; framing, contacts and story clarity are acceptable.",
            }
            plan["creativeBrief"]["blockingPreviewApproval"] = approval
            (output / manifest["segments"][0]["outputFile"]).write_bytes(b"modified after review")
            errors = validate_approval(plan, manifest, PROJECT, manifest_path)
            self.assertTrue(any("changed since manifest creation" in item for item in errors))

    def test_approval_is_invalidated_if_renderer_source_changes(self):
        plan = load_plan()
        spec = build_preview_spec(plan, PROJECT)
        self.assertIn("video-projects/remotion/src/OneMoreScroll.tsx", spec["sourceFiles"])
        self.assertIn("tools/video/render_blocking_preview.py", spec["sourceFiles"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
