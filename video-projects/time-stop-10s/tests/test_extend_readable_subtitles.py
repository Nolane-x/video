from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "extend_readable_subtitles.py"
SPEC = importlib.util.spec_from_file_location("extend_readable_subtitles", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ExtendReadableSubtitlesTests(unittest.TestCase):
    def test_parse_srt_preserves_multiline_text(self):
        raw = (
            "1\n00:00:00,120 --> 00:00:01,500\n"
            "Một dòng\nDòng thứ hai\n\n"
            "2\n00:00:04,620 --> 00:00:05,900\n"
            "Cue tiếp theo\n"
        )
        cues = MODULE.parse_srt(raw)
        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0].text, "Một dòng\nDòng thứ hai")
        self.assertAlmostEqual(cues[0].start, 0.12)
        self.assertAlmostEqual(cues[1].start, 4.62)

    def test_build_extends_dwell_without_changing_text_or_starts(self):
        source_text = (
            "1\n00:00:00,120 --> 00:00:01,500\n"
            "Một ngày bình thường.\n\n"
            "2\n00:00:04,620 --> 00:00:05,900\n"
            "Thời gian vẫn trôi.\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.srt"
            output = root / "out"
            source.write_text(source_text, encoding="utf-8")
            report = MODULE.build(source, output, duration=9.0, gap=0.12, expected_cues=2)
            original = MODULE.parse_srt(source_text)
            extended = MODULE.parse_srt(
                (output / "time-stop-10s-readable-vi.srt").read_text(encoding="utf-8")
            )
            self.assertEqual([cue.start for cue in original], [cue.start for cue in extended])
            self.assertEqual([cue.text for cue in original], [cue.text for cue in extended])
            self.assertAlmostEqual(extended[0].end, 4.50)
            self.assertAlmostEqual(extended[1].end, 9.00)
            self.assertEqual(report["overlap_count"], 0)
            self.assertEqual(report["text_changes"], 0)
            self.assertTrue((output / "time-stop-10s-readable-vi.vtt").is_file())
            self.assertTrue((output / "subtitle-readability-qa.json").is_file())

    def test_vtt_omits_numeric_identifiers_and_keeps_webvtt_timing(self):
        cues = [MODULE.Cue(1, 0.12, 4.50, "Một ngày bình thường.")]
        rendered = MODULE.render_vtt(cues)
        self.assertTrue(rendered.startswith("WEBVTT" + chr(10) + chr(10)))
        self.assertIn("00:00:00.120 --> 00:00:04.500", rendered)
        self.assertNotIn(chr(10) + "1" + chr(10), rendered)

    def test_rejects_wrong_expected_cue_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.srt"
            source.write_text(
                "1\n00:00:00,120 --> 00:00:01,500\nOnly one cue\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Expected 2 cues"):
                MODULE.build(source, root / "out", duration=9.0, gap=0.12, expected_cues=2)


if __name__ == "__main__":
    unittest.main()
