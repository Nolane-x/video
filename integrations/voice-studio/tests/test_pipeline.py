from __future__ import annotations

import ast
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate_voiceover
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
        self.assertEqual(segments[0]["engine"], "korva-onnx")
        self.assertEqual(segments[1]["engine"], "omnivoice")

    def test_cast_is_applied_and_identity_fingerprint_is_stable(self):
        data = {
            "language": "vi",
            "cast": {
                "narrator": {
                    "provider": "voicestudio",
                    "engine": "voxcpm2",
                    "voice": "profile-123",
                    "language": "vi",
                    "seed": 42,
                    "instruct": "warm, calm delivery",
                }
            },
            "segments": [
                {"speaker_id": "narrator", "text": "Câu thứ nhất."},
                {"speaker_id": "narrator", "text": "Câu thứ hai."},
            ],
        }
        segments = validate_manifest(data)
        self.assertEqual(segments[0]["voice"], "profile-123")
        self.assertEqual(segments[0]["engine"], "voxcpm2")
        self.assertEqual(
            segments[0]["voice_identity_fingerprint"],
            segments[1]["voice_identity_fingerprint"],
        )

    def test_rejects_voice_identity_drift_for_same_speaker(self):
        with self.assertRaisesRegex(ValueError, "Voice identity drift"):
            validate_manifest({
                "segments": [
                    {
                        "speaker_id": "host", "text": "A",
                        "provider": "voicestudio", "engine": "voxcpm2",
                        "voice": "profile-a", "language": "vi"
                    },
                    {
                        "speaker_id": "host", "text": "B",
                        "provider": "voicestudio", "engine": "voxcpm2",
                        "voice": "profile-b", "language": "vi"
                    },
                ]
            })

    def test_rejects_duplicate_id_and_unsupported_provider(self):
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [
                {"id": "V001", "text": "a"},
                {"id": "V001", "text": "b"},
            ]})
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [{"text": "a", "provider": "unknown"}]})

    def test_sanitizes_voice_block_metadata(self):
        segments = validate_manifest({"segments": [{
            "text": "Xin chào", "character": "A | B = C · D\nline 2"
        }]})
        self.assertEqual(segments[0]["character"], "A / B - C - D line 2")

    def test_rejects_invalid_speed(self):
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [{"text": "Xin chào", "speed": 9}]})

    def test_rejects_oversized_text(self):
        with self.assertRaises(ValueError):
            validate_manifest({"segments": [{"text": "x" * 4097}]})

    def test_plan_only_does_not_call_a_provider_or_write_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(generate_voiceover, "_synthesize") as synthesize:
                report = generate(
                    {"project": "unit-test", "segments": [
                        {"text": "Xin chào", "provider": "korva", "voice": "khanh_vy"}
                    ]},
                    Path(tmp), plan_only=True,
                )
            synthesize.assert_not_called()
            self.assertEqual(report["status"], "plan_only")
            self.assertFalse((Path(tmp) / "voice").exists())
            self.assertFalse((Path(tmp) / "voice-generation-report.json").exists())

    def test_batch_continues_after_one_provider_failure(self):
        def fake_synth(item, output, _client):
            if item["id"] == "V001":
                raise RuntimeError("simulated provider failure")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(b"RIFF" + b"\0" * 64)
            return output

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(generate_voiceover, "_synthesize", side_effect=fake_synth):
                report = generate(
                    {"project": "partial-test", "segments": [
                        {"id": "V001", "text": "Câu lỗi", "provider": "korva", "voice": "khanh_vy"},
                        {"id": "V002", "text": "Câu tốt", "provider": "korva", "voice": "khanh_vy"},
                    ]},
                    Path(tmp),
                )
            self.assertEqual(report["status"], "partial")
            self.assertEqual(report["failed_segments"], 1)
            self.assertEqual(report["generated_segments"], 1)
            self.assertFalse((Path(tmp) / "voice" / "V001.wav").exists())
            self.assertTrue((Path(tmp) / "voice" / "V002.wav").is_file())
            saved = (Path(tmp) / "02-VOICE-partial-test-TTS.txt").read_text(encoding="utf-8")
            self.assertNotIn("V001", saved)
            self.assertIn("V002", saved)

    def test_h2_voice_script_uses_actual_prep_voice_block_grammar(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(generate_voiceover, "_synthesize") as synthesize:
                def fake(item, output, _client):
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_bytes(b"RIFF" + b"\0" * 64)
                    return output
                synthesize.side_effect = fake
                generate(
                    {"project": "parser-test", "segments": [{
                        "id": "V001", "slot": "NARRATOR",
                        "character": "Người kể chuyện",
                        "text": "Xin chào Việt Nam.",
                        "provider": "korva", "voice": "khanh_vy",
                    }]},
                    Path(tmp),
                )
            script = (Path(tmp) / "02-VOICE-parser-test-TTS.txt").read_text(encoding="utf-8")
            repo_root = Path(__file__).resolve().parents[3]
            parser_path = (
                repo_root / "integrations/h2-selfimprove-studio/skills/"
                "lam-video-selfimprove/kit/tools/prep_voice.py"
            )
            parser_ast = ast.parse(parser_path.read_text(encoding="utf-8-sig"))
            parser_pattern = None
            for node in ast.walk(parser_ast):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "finditer"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and node.args[0].value.startswith("^===")
                ):
                    parser_pattern = node.args[0].value
                    break
            self.assertIsNotNone(parser_pattern, "Could not find the actual H2 parse_voice_txt regex")
            match = re.search(parser_pattern, script, re.S | re.M)
            self.assertIsNotNone(match)
            self.assertEqual(match.group(1), "V001")
            self.assertIn("NARRATOR", match.group(2))
            self.assertIn("Người kể chuyện", match.group(2))
            self.assertIn("Xin chào Việt Nam.", match.group(3))
            self.assertTrue((Path(tmp) / "voice" / "V001.wav").is_file())


if __name__ == "__main__":
    unittest.main()
