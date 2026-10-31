from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from caption_delivery import build_cues, write_subtitles


class CaptionDeliveryTests(unittest.TestCase):
    def make_timeline(self, root: Path):
        root.mkdir(parents=True, exist_ok=True)
        (root / "blocks.json").write_text(json.dumps([
            {"id": "V001", "slot": "NARRATOR", "char": "Người dẫn chuyện"}
        ]), encoding="utf-8")
        (root / "lines.json").write_text(json.dumps([
            {
                "id": "L001", "block": "V001", "slot": "NARRATOR",
                "char": "Người dẫn chuyện", "text": "Xin chào Việt Nam. Đây là câu chuyện.",
                "start": 0.5, "end": 2.8,
            }
        ], ensure_ascii=False), encoding="utf-8")
        (root / "words.json").write_text(json.dumps([
            {"w": "Xin", "t": 0.5, "e": 0.7},
            {"w": "chào", "t": 0.72, "e": 0.98},
            {"w": "Việt", "t": 1.0, "e": 1.24},
            {"w": "Nam", "t": 1.26, "e": 1.5},
            {"w": "Đây", "t": 1.6, "e": 1.82},
            {"w": "là", "t": 1.84, "e": 2.0},
            {"w": "câu", "t": 2.02, "e": 2.24},
            {"w": "chuyện", "t": 2.26, "e": 2.65},
        ], ensure_ascii=False), encoding="utf-8")

    def test_generates_srt_vtt_ass_and_json_with_vietnamese_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            timeline = root / "timeline"
            out = root / "delivery"
            self.make_timeline(timeline)
            report = write_subtitles(
                timeline, out, max_chars=25, max_duration_s=2.0,
                max_line_chars=20,
            )
            self.assertGreaterEqual(report["cue_count"], 2)
            for filename in ("captions.srt", "captions.vtt", "captions.ass", "captions.json"):
                self.assertTrue((out / filename).is_file())
            srt = (out / "captions.srt").read_text(encoding="utf-8")
            vtt = (out / "captions.vtt").read_text(encoding="utf-8")
            self.assertIn("Xin chào", srt)
            self.assertIn("Việt Nam.", srt)
            self.assertTrue(vtt.startswith("WEBVTT"))
            saved = json.loads((out / "captions.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["cue_count"], report["cue_count"])
            self.assertIn("not forced-alignment", saved["timing_method"])

    def test_all_cues_are_chronological_and_limited_to_two_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            timeline = root / "timeline"
            self.make_timeline(timeline)
            cues = build_cues(
                timeline, max_chars=25, max_duration_s=2.0,
                max_line_chars=20,
            )
            self.assertTrue(all(len(cue["text"].splitlines()) <= 2 for cue in cues))
            self.assertTrue(all(cue["end"] > cue["start"] for cue in cues))
            self.assertTrue(all(
                current["start"] >= previous["end"]
                for previous, current in zip(cues, cues[1:])
            ))

    def test_rejects_mismatch_between_line_text_and_h2_word_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            timeline = root / "timeline"
            self.make_timeline(timeline)
            words = json.loads((timeline / "words.json").read_text(encoding="utf-8"))
            words[0]["w"] = "Sai"
            (timeline / "words.json").write_text(json.dumps(words), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match text"):
                build_cues(timeline)

    def test_rejects_unmatched_extra_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            timeline = root / "timeline"
            self.make_timeline(timeline)
            words = json.loads((timeline / "words.json").read_text(encoding="utf-8"))
            words.append({"w": "thừa", "t": 3.0, "e": 3.2})
            (timeline / "words.json").write_text(json.dumps(words), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unmatched trailing"):
                build_cues(timeline)


if __name__ == "__main__":
    unittest.main()
