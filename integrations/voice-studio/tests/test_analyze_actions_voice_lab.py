from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze_actions_voice_lab import analyze_actions_voice_lab, write_markdown


class AnalyzeActionsVoiceLabTests(unittest.TestCase):
    def benchmark(self):
        def row(voice_id, label, name, true_peak=-3.0):
            return {
                "id": voice_id,
                "name": name,
                "provider": "korva",
                "engine": "korva-onnx",
                "blind_label": label,
                "status": "ready",
                "technical_status": "pass",
                "technical_findings": [],
                "audio_file": "audio.wav",
                "audio_sha256_verified": True,
                "audio_metrics": {"duration_s": 12.0, "peak_dbfs": -3.0},
                "mastering": {
                    "output_integrated_loudness_lufs": -20.0,
                    "output_true_peak_dbtp": true_peak,
                },
            }
        return {
            "status": "complete",
            "provider": "korva",
            "language": "vi",
            "model": {"revision": "a" * 40},
            "runner": {"run_id": "12345"},
            "cases": [
                {
                    "id": "tones-phonemes",
                    "title": "Thanh điệu",
                    "candidates": [
                        row("voice-a", "Candidate 01", "Khánh Vy", -3.0),
                        row("voice-b", "Candidate 02", "Quang Huy", -2.8),
                    ],
                },
                {
                    "id": "documentary-longform",
                    "title": "Lời dẫn dài",
                    "candidates": [
                        row("voice-a", "Candidate 01", "Khánh Vy", -3.2),
                        row("voice-b", "Candidate 02", "Quang Huy", -2.7),
                    ],
                },
            ],
        }

    def test_joins_blind_ratings_and_selects_only_fully_reviewed_voices(self):
        ratings = {
            "ratings": [
                {
                    "candidate": "Candidate 01",
                    "ratings": {
                        "naturalness": 5,
                        "vietnamese": 5,
                        "identity": 4,
                        "expression": 4,
                        "character_fit": 5,
                    },
                    "notes": "Phát âm rõ, giọng kể ổn định.",
                },
                {
                    "candidate": "Candidate 02",
                    "ratings": {"naturalness": 5, "vietnamese": 5},
                    "notes": "Chưa nghe đủ các tiêu chí.",
                },
            ],
        }
        report = analyze_actions_voice_lab(self.benchmark(), ratings, min_ratings=3)
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["fully_rendered_voice_count"], 2)
        self.assertEqual(report["rated_voice_count"], 2)
        self.assertEqual(report["eligible_voice_count"], 1)
        self.assertEqual(report["human_rating_winner"]["id"], "voice-a")
        self.assertEqual(report["human_rating_winner"]["name"], "Khánh Vy")
        self.assertEqual(report["shortlist"][0]["human_mean_rating"], 4.6)
        self.assertEqual(
            report["candidates"][0]["listener_notes"],
            "Phát âm rõ, giọng kể ổn định.",
        )
        self.assertEqual(report["shortlist"][0]["mastering_summary"]["maximum_true_peak_dbtp"], -3.0)
        self.assertIsNone(report["methodology"].get("objective_naturalness_score"))

    def test_voice_missing_from_one_scenario_is_not_shortlist_eligible(self):
        benchmark = self.benchmark()
        benchmark["cases"][1]["candidates"] = benchmark["cases"][1]["candidates"][:1]
        ratings = {
            "ratings": [{
                "candidate": "Candidate 01",
                "ratings": {
                    "naturalness": 5,
                    "vietnamese": 5,
                    "identity": 5,
                },
            }],
        }
        report = analyze_actions_voice_lab(benchmark, ratings)
        voice = next(row for row in report["candidates"] if row["id"] == "voice-b")
        self.assertFalse(voice["scenario_coverage_complete"])
        self.assertFalse(voice["eligible_for_human_shortlist"])
        self.assertEqual(report["status"], "partial")

    def test_unknown_or_duplicate_blind_labels_are_rejected(self):
        benchmark = self.benchmark()
        with self.assertRaisesRegex(ValueError, "Unknown blind candidate"):
            analyze_actions_voice_lab(
                benchmark,
                {"ratings": [{"candidate": "Candidate 99", "ratings": {}}]},
            )
        with self.assertRaisesRegex(ValueError, "Duplicate ratings entry"):
            analyze_actions_voice_lab(
                benchmark,
                {"ratings": [
                    {"candidate": "Candidate 01", "ratings": {}},
                    {"candidate": "Candidate 01", "ratings": {}},
                ]},
            )

    def test_invalid_human_scores_are_rejected(self):
        benchmark = self.benchmark()
        for invalid in (0, 6, True, float("nan"), float("inf"), "5"):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "finite number from 1 to 5"):
                    analyze_actions_voice_lab(
                        benchmark,
                        {"ratings": [{
                            "candidate": "Candidate 01",
                            "ratings": {"naturalness": invalid},
                        }]},
                    )

    def test_blind_label_must_not_change_between_scenarios(self):
        benchmark = self.benchmark()
        benchmark["cases"][1]["candidates"][0]["blind_label"] = "Candidate 02"
        with self.assertRaisesRegex(ValueError, "Blind label changed"):
            analyze_actions_voice_lab(benchmark, {"ratings": []})

    def test_markdown_report_uses_real_newlines_and_hides_no_identity_after_reveal(self):
        benchmark = self.benchmark()
        ratings = {
            "ratings": [{
                "candidate": "Candidate 01",
                "ratings": {
                    "naturalness": 5, "vietnamese": 4, "identity": 4,
                },
                "notes": "Good stable narrator.",
            }],
        }
        report = analyze_actions_voice_lab(benchmark, ratings)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "voice-shortlist.md"
            write_markdown(report, path)
            text = path.read_text(encoding="utf-8")
        self.assertIn("\n## Important interpretation\n", text)
        self.assertNotIn("\\n## Important interpretation", text)
        self.assertIn("Khánh Vy", text)


if __name__ == "__main__":
    unittest.main()
