from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from actions_voice_lab import load_suite, run_lab, safe_audio_path


class ActionsVoiceLabTests(unittest.TestCase):
    def test_suite_contains_unique_safe_vietnamese_scenarios(self):
        suite_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-benchmark-suite.json"
        )
        suite = load_suite(suite_path)
        self.assertEqual(suite["language"], "vi")
        self.assertEqual(len(suite["cases"]), 4)
        self.assertEqual(len({case["id"] for case in suite["cases"]}), 4)
        self.assertTrue(all(case["text"] for case in suite["cases"]))

    def test_duplicate_case_ids_are_rejected(self):
        data = {
            "schema_version": 1,
            "language": "vi",
            "cases": [
                {"id": "same-case", "title": "A", "purpose": "A", "text": "Xin chào"},
                {"id": "same-case", "title": "B", "purpose": "B", "text": "Tạm biệt"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "suite.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate benchmark case ID"):
                load_suite(path)

    def test_plan_only_does_not_load_models_or_call_providers(self):
        suite_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-benchmark-suite.json"
        )
        with tempfile.TemporaryDirectory() as tmp:
            report = run_lab(
                suite_path,
                Path(tmp),
                model_revision="a" * 40,
                plan_only=True,
            )
            saved = json.loads((Path(tmp) / "plan.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "plan_only")
        self.assertEqual(saved["model"]["revision"], "a" * 40)
        self.assertEqual(len(saved["voices"]), 10)
        self.assertEqual(saved["synthesis"]["device"], "cpu")

    def test_invalid_model_revision_is_rejected_before_download(self):
        suite_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-benchmark-suite.json"
        )
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "immutable Hugging Face commit SHA"):
                run_lab(suite_path, Path(tmp), model_revision="main")

    def test_audio_path_must_remain_inside_case_output(self):
        with tempfile.TemporaryDirectory() as root:
            with tempfile.TemporaryDirectory() as outside:
                audio = Path(root) / "case" / "audio.wav"
                audio.parent.mkdir()
                audio.write_bytes(b"audio")
                self.assertEqual(
                    safe_audio_path(Path(root) / "case", "audio/audio.wav"),
                    audio.resolve(),
                )
                with self.assertRaisesRegex(ValueError, "escapes benchmark output"):
                    safe_audio_path(Path(root) / "case", str(Path(outside) / "outside.wav"))


if __name__ == "__main__":
    unittest.main()
