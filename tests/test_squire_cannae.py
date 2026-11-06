#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREP = load_module("prepare_squire_voice_job", ROOT / "tools/video/prepare_squire_voice_job.py")
AUTHOR = load_module("author_squire_cannae", ROOT / "tools/video/author_squire_cannae.py")
QA = load_module("qa_squire_output", ROOT / "tools/video/qa_squire_output.py")


class SquireCannaeTests(unittest.TestCase):
    def test_long_form_script_is_within_squire_target(self):
        path = ROOT / "video-projects/squire/cannae-216bc/01-SCRIPT.md"
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\n+\d[\d,]* words\..*$", "", text, flags=re.S).strip()
        words = len(text.split())
        self.assertGreaterEqual(words, 1700)
        self.assertLessEqual(words, 2000)
        self.assertNotIn("|", text)
        self.assertIn("double envelopment", text.casefold())
        self.assertIn("Polybius", text)

    def test_voice_picker_prefers_exact_live_adam_id(self):
        rows = [
            {
                "id": "en-vieneu-v3turbo-adam-3f0c9b",
                "language": "en",
                "engine": "VieNeu-TTS v3 Turbo",
                "watermark": "verified",
                "signal_checks": {"status": "passed"},
                "rights": {"commercial_use": "upstream-model-card-permits-generated-audio"},
            },
            {
                "id": "en-kokoro-v1-af_heart",
                "language": "en",
                "engine": "Kokoro-82M",
                "watermark": "verified",
                "signal_checks": {"status": "passed"},
                "upstream_quality_grade": "A",
                "rights": {"commercial_use": "apache-2.0-model-and-voice-assets"},
            },
        ]
        selected, reason = PREP.choose_voice({"voices": rows})
        self.assertEqual(selected["id"], "en-vieneu-v3turbo-adam-3f0c9b")
        self.assertIn("Preferred VieNeu", reason)

    def test_voice_picker_falls_back_to_highest_curated_kokoro_grade(self):
        rows = [
            {
                "id": "en-kokoro-v1-af_bella",
                "language": "en",
                "engine": "Kokoro-82M",
                "watermark": "verified",
                "signal_checks": {"status": "passed"},
                "upstream_quality_grade": "A-",
                "rights": {"commercial_use": "apache-2.0-model-and-voice-assets"},
            },
            {
                "id": "en-kokoro-v1-af_heart",
                "language": "en",
                "engine": "Kokoro-82M",
                "watermark": "verified",
                "signal_checks": {"status": "passed"},
                "upstream_quality_grade": "A",
                "rights": {"commercial_use": "apache-2.0-model-and-voice-assets"},
            },
        ]
        selected, _ = PREP.choose_voice({"voices": rows})
        self.assertEqual(selected["id"], "en-kokoro-v1-af_heart")

    def test_squire_director_uses_registered_visual_templates(self):
        cases = [
            ("The river near Cannae becomes the key landmark.", 1, 0.2, "map"),
            ("The Roman infantry numbers eighty thousand.", 2, 0.3, "board"),
            ("The Carthaginian wings attack both flanks.", 3, 0.7, "top"),
            ("Hannibal studies the line.", 4, 0.4, "close"),
        ]
        for text, index, progress, expected in cases:
            self.assertEqual(AUTHOR.choose_template(text, index, progress), expected)
        self.assertEqual(AUTHOR.VALID_TEMPLATES, {"scene", "close", "army", "top", "plan", "map", "board", "item", "split", "title", "black"})

    def test_squire_top_down_geometry_is_normalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            args, cues = AUTHOR.base_args("top", "The centre is surrounded on both flanks.", 12, 0.7, Path(tmp))
        self.assertEqual(len(args["blocks"]), 4)
        for block in args["blocks"]:
            self.assertGreater(block["w"], 0)
            self.assertGreater(block["h"], 0)
            self.assertIn(block["side"], {"red", "blue", "grey", "purple", "gold", "green"})

    def test_safe_output_name(self):
        self.assertEqual(QA.safe_title('How Hannibal Turned Rome: "Trap"'), "How Hannibal Turned Rome Trap")


if __name__ == "__main__":
    unittest.main(verbosity=2)
