import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_toolchain import validate
from validate_plugin_packages import validate as validate_plugins
from validate_genre_routing import validate as validate_genre_routing, validate_data as validate_genre_routing_data
from build_npm_sbom import build

ROOT = Path(__file__).resolve().parents[2]


class ToolchainManifestTests(unittest.TestCase):
    def test_manifest_and_npm_direct_pins_are_consistent(self):
        self.assertEqual(validate(ROOT), [])

    def test_plugin_manifests_and_skill_frontmatter_are_valid(self):
        self.assertEqual(validate_plugins(ROOT), [])

    def test_committed_npm_lockfile_matches_exact_direct_dependencies(self):
        package = json.loads(
            (ROOT / "toolchain/node/package.json").read_text(encoding="utf-8")
        )
        lock = json.loads(
            (ROOT / "toolchain/node/package-lock.json").read_text(encoding="utf-8")
        )
        root_lock = lock["packages"][""]
        self.assertEqual(lock["lockfileVersion"], 3)
        self.assertEqual(root_lock["name"], package["name"])
        self.assertEqual(root_lock["version"], package["version"])
        self.assertEqual(root_lock["dependencies"], package["dependencies"])
        for name, version in package["dependencies"].items():
            entry = lock["packages"][f"node_modules/{name}"]
            self.assertEqual(entry["version"], version)
            self.assertTrue(entry["resolved"].startswith("https://registry.npmjs.org/"))
            self.assertTrue(entry["integrity"].startswith("sha"))

    def test_optional_python_profiles_have_exact_direct_pins(self):
        manifest = json.loads(
            (ROOT / "toolchain/manifest.json").read_text(encoding="utf-8")
        )
        expected = {
            "editorialPython": (
                "toolchain/python/editorial/requirements.txt",
                ["opentimelineio==0.18.1", "scenedetect-headless==0.7.2"],
            ),
            "manim": (
                "toolchain/python/manim/requirements.txt",
                ["manim==0.22.1"],
            ),
            "audioML": (
                "toolchain/python/audio-ml/requirements.txt",
                ["whisperx==3.8.6", "demucs==4.1.0"],
            ),
        }
        for profile, (path, pins) in expected.items():
            self.assertEqual(manifest["profiles"][profile]["packages"], pins)
            requirements = [
                line.strip()
                for line in (ROOT / path).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(requirements, pins)

        profiles = manifest["profiles"]
        for name in ("manim", "blender"):
            profile = profiles[name]
            self.assertFalse(profile["required"])
            self.assertFalse(profile["manualOnly"])
            self.assertTrue(
                any(
                    item.startswith("pull_request paths:")
                    for item in profile["triggers"]
                )
            )
            self.assertIn("workflow_dispatch", profile["triggers"])
            self.assertTrue((ROOT / profile["workflow"]).is_file())

        audio_ml = profiles["audioML"]
        self.assertFalse(audio_ml["required"])
        self.assertTrue(audio_ml["manualOnly"])
        self.assertEqual(audio_ml["triggers"], ["workflow_dispatch"])

    def test_core_dependencies_are_exact_and_no_gpu_model_is_installed(self):
        package = json.loads(
            (ROOT / "toolchain/node/package.json").read_text(encoding="utf-8")
        )
        deps = package["dependencies"]
        self.assertEqual(deps["remotion"], "4.0.538")
        self.assertEqual(deps["hyperframes"], "0.8.222")
        self.assertEqual(deps["gsap"], "3.15.0")
        self.assertEqual(deps["motion"], "14.9.0")
        self.assertEqual(deps["typescript"], "5.9.3")
        self.assertNotIn("@motion-canvas/core", deps)
        forbidden = ("wan", "hunyuan", "ltx", "comfyui", "framepack", "diffusers")
        self.assertFalse(any(token in key.lower() for key in deps for token in forbidden))

    def test_sbom_includes_direct_and_nested_npm_packages(self):
        lock = {
            "name": "demo",
            "version": "1.0.0",
            "packages": {
                "": {"name": "demo", "version": "1.0.0"},
                "node_modules/react": {"version": "19.2.3", "license": "MIT"},
                "node_modules/@scope/tool": {
                    "version": "2.0.0",
                    "license": {"name": "Apache-2.0"},
                },
                "node_modules/a/node_modules/b": {"version": "3.0.0"},
            },
        }
        bom = build(lock)
        self.assertEqual(bom["bomFormat"], "CycloneDX")
        self.assertEqual(len(bom["components"]), 3)
        self.assertIn("@scope/tool", [component["name"] for component in bom["components"]])

    def test_blender_is_optional_and_size_gated(self):
        data = json.loads(
            (ROOT / "toolchain/manifest.json").read_text(encoding="utf-8")
        )
        blender = data["profiles"]["blender"]
        self.assertFalse(blender["required"])
        self.assertFalse(blender["manualOnly"])
        self.assertLess(blender["archiveBytes"], 400_000_000)
        self.assertTrue(
            str(blender["url"]).startswith(
                "https://download.blender.org/release/Blender5.2/"
            )
        )
        self.assertTrue(str(blender["checksumUrl"]).endswith("blender-5.2.3.sha256"))


class GenreRoutingContractTests(unittest.TestCase):
    def test_machine_readable_genre_routes_match_human_matrix(self):
        self.assertEqual(validate_genre_routing(ROOT), [])

    def test_genre_routing_rejects_missing_profile(self):
        data = json.loads(
            (ROOT / "tools/video/genre-routing.json").read_text(encoding="utf-8")
        )
        data["profiles"].pop()
        matrix = (ROOT / "docs/GENRE_ROUTING_MATRIX.md").read_text(encoding="utf-8")
        errors = validate_genre_routing_data(data, matrix)
        self.assertTrue(any("genre profile coverage mismatch" in error for error in errors))

    def test_genre_routing_requires_product_truth_and_privacy_checks(self):
        data = json.loads(
            (ROOT / "tools/video/genre-routing.json").read_text(encoding="utf-8")
        )
        product = next(p for p in data["profiles"] if p["id"] == "product-software-demo")
        product["qaChecks"].remove("actual-ui-truth-check")
        matrix = (ROOT / "docs/GENRE_ROUTING_MATRIX.md").read_text(encoding="utf-8")
        errors = validate_genre_routing_data(data, matrix)
        self.assertTrue(any("actual-ui-truth-check" in error for error in errors))

    def test_quality_assurance_skill_requires_independent_review(self):
        skill = (
            ROOT / "plugins/chatgpt/nolane-video-command-center/skills/video-quality-assurance/SKILL.md"
        ).read_text(encoding="utf-8").lower()
        for phrase in (
            "independent evaluation",
            "open-ended defect search",
            "technical defect",
            "creative defect",
            "continuity defect",
            "generation/model defect",
            "corrective-action protocol",
        ):
            self.assertIn(phrase, skill)


if __name__ == "__main__":
    unittest.main(verbosity=2)
