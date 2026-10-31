import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_toolchain import validate
from build_npm_sbom import build
ROOT = Path(__file__).resolve().parents[2]

class ToolchainManifestTests(unittest.TestCase):
    def test_manifest_and_npm_direct_pins_are_consistent(self):
        self.assertEqual(validate(ROOT), [])
    def test_core_dependencies_are_exact_and_no_gpu_model_is_installed(self):
        package = json.loads((ROOT / "toolchain/node/package.json").read_text(encoding="utf-8"))
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
        lock = {"name":"demo","version":"1.0.0","packages":{
            "":{"name":"demo","version":"1.0.0"},
            "node_modules/react":{"version":"19.2.3","license":"MIT"},
            "node_modules/@scope/tool":{"version":"2.0.0","license":{"name":"Apache-2.0"}},
            "node_modules/a/node_modules/b":{"version":"3.0.0"}}}
        bom = build(lock)
        self.assertEqual(bom["bomFormat"], "CycloneDX")
        self.assertEqual(len(bom["components"]), 3)
        self.assertIn("@scope/tool", [component["name"] for component in bom["components"]])
    def test_blender_is_optional_and_size_gated(self):
        data = json.loads((ROOT / "toolchain/manifest.json").read_text(encoding="utf-8"))
        blender = data["profiles"]["blender"]
        self.assertFalse(blender["required"])
        self.assertTrue(blender["manualOnly"])
        self.assertLess(blender["archiveBytes"], 400_000_000)
if __name__ == "__main__": unittest.main(verbosity=2)
