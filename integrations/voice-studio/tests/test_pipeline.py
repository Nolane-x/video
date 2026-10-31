from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_voiceover import generate, validate_manifest


class VoiceoverPipelineTests(unittest.TestCase):
    def test_validates_speaker_segments(self):
        segments = validate_manifest({
            "language": "vi",
            "segments": [
                {"text": "Xin chào", "slot": "NARRATOR", "provider": "korva"},
                {"id": "V002", "text": "Chào mọi người", "provider": "voicestudio"},
            ],
        })
        self.assertEqual([s["id"] for s in segments], ["V001", "V002"])
        self.assertEqual(segments[0]["language"], "vi")
        self.assertEqual(segments[1]["engine"], "omnivoice")

    def test_rejects_duplicate_id_and_unsupported_provider(self):
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [
                {"id": "V001", "text": "a"},
                {"id": "V001", "text": "b"},
            ]})
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [{"text": "a", "provider": "unknown"}]})

    def test_rejects_oversized_text(self):
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [{"text": "x" * 4097}]})

    def test_plan_only_does_not_call_a_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = generate(
                {"project": "unit-test", "segments": [
                    {"text": "Xin chào", "provider": "korva", "voice": "khanh_vy"}
                ]},
                Path(tmp), plan_only=True,
            )
            self.assertEqual(report["status"], "plan_only")
            self.assertFalse((Path(tmp) / "voice").exists())
            self.assertFalse((Path(tmp) / "02-VOICE-unit-test-TTS.txt").exists())


if __name__ == "__main__":
    unittest.main()
