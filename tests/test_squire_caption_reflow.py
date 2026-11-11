from __future__ import annotations
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("reflow", Path(__file__).with_name("reflow_squire_captions.py"))
reflow = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reflow
assert SPEC.loader
SPEC.loader.exec_module(reflow)

class CaptionReflowTests(unittest.TestCase):
    def test_split_long_cue_preserves_words_and_two_line_limit(self):
        text = "You can hear the Ottoman camp beyond the dark fields horses shifting men calling to one another the creak of carts and the distant thunder of guns."
        groups = reflow.partition_words(text, 42, 2)
        self.assertGreater(len(groups), 1)
        self.assertEqual(" ".join(w for group in groups for w in group).split(), text.split())
        for group in groups:
            lines = reflow.wrap_words(group, 42)
            self.assertLessEqual(len(lines), 2)
            self.assertTrue(all(len(line) <= 42 for line in lines))

    def test_preserves_outer_timing_and_no_overlap(self):
        source = [
            reflow.Cue(0.0, 5.0, "One very long caption that should be split into two short balanced cards without losing a single word."),
            reflow.Cue(5.2, 7.0, "Then the next sentence begins."),
        ]
        output, report = reflow.reflow(source)
        self.assertEqual(output[0].start, source[0].start)
        self.assertEqual(output[-1].end, source[-1].end)
        self.assertGreater(report["output_cues"], report["source_cues"])
        for a, b in zip(output, output[1:]):
            self.assertLessEqual(a.end, b.start + 0.001)

    def test_parse_and_write_srt_vtt_roundtrip(self):
        src = [reflow.Cue(0.0, 2.25, "The walls are still standing."), reflow.Cue(2.5, 4.0, "But the city is exhausted.")]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            srt, vtt = root / "source.srt", root / "source.vtt"
            reflow.write_subtitles(src, srt, "srt")
            reflow.write_subtitles(src, vtt, "vtt")
            parsed_srt = reflow.parse_subtitles(srt, "srt")
            parsed_vtt = reflow.parse_subtitles(vtt, "vtt")
            self.assertEqual([(x.start, x.end, x.text) for x in parsed_srt], [(x.start, x.end, x.text) for x in parsed_vtt])

    def test_rejects_word_wider_than_line(self):
        with self.assertRaises(ValueError):
            reflow.wrap_words(["x" * 43], 42)

if __name__ == "__main__":
    unittest.main()
