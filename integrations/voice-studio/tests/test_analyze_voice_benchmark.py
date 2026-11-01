from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze_voice_benchmark import analyze_benchmark


class AnalyzeVoiceBenchmarkTests(unittest.TestCase):
    def test_joins_blind_ratings_and_keeps_asr_separate(self):
        benchmark = {
            "provider": "all",
            "language": "vi",
            "script_sha256": "abc",
            "candidates": [
                {
                    "blind_label": "Candidate 01", "id": "korva-a",
                    "name": "Voice A", "provider": "korva", "status": "ready",
                    "asr_intelligibility_proxy": {
                        "status": "available", "wer": 0.1, "cer": 0.02,
                    },
                },
                {
                    "blind_label": "Candidate 02", "id": "studio-b",
                    "name": "Voice B", "provider": "voicestudio", "status": "ready",
                    "asr_intelligibility_proxy": {"status": "unavailable"},
                },
            ],
        }
        ratings = {
            "ratings": [
                {
                    "candidate": "Candidate 01",
                    "ratings": {
                        "naturalness": 5, "vietnamese": 4, "identity": 4,
                        "expression": 5, "character_fit": 4,
                    },
                    "notes": "Clear tones and confident documentary delivery.",
                },
                {
                    "candidate": "Candidate 02",
                    "ratings": {
                        "naturalness": 4, "vietnamese": 5, "identity": 4,
                    },
                },
            ],
        }
        report = analyze_benchmark(benchmark, ratings, min_ratings=3)
        self.assertEqual(report["eligible_candidate_count"], 2)
        self.assertEqual(report["human_rating_winner"]["id"], "korva-a")
        self.assertEqual(
            report["candidates"][0]["listener_notes"],
            "Clear tones and confident documentary delivery.",
        )
        korva = next(row for row in report["providers"] if row["provider"] == "korva")
        self.assertEqual(korva["mean_candidate_rating"], 4.4)
        self.assertEqual(korva["mean_wer"], 0.1)
        studio = next(row for row in report["providers"] if row["provider"] == "voicestudio")
        self.assertIsNone(studio["mean_wer"])
        self.assertEqual(report["methodology"]["asr"].split(" ")[0], "WER/CER")

    def test_candidates_below_rating_coverage_are_not_ranked(self):
        benchmark = {
            "candidates": [{
                "blind_label": "Candidate 01", "id": "voice-1",
                "provider": "korva", "status": "ready",
            }],
        }
        ratings = {
            "ratings": [{
                "candidate": "Candidate 01",
                "ratings": {"naturalness": 5, "vietnamese": 5},
            }],
        }
        report = analyze_benchmark(benchmark, ratings, min_ratings=3)
        self.assertEqual(report["eligible_candidate_count"], 0)
        self.assertIsNone(report["human_rating_winner"])
        self.assertIsNone(report["providers"][0]["mean_candidate_rating"])

    def test_unknown_or_duplicate_rating_labels_are_rejected(self):
        benchmark = {
            "candidates": [{
                "blind_label": "Candidate 01", "id": "voice-1", "provider": "korva",
            }],
        }
        with self.assertRaisesRegex(ValueError, "Unknown candidate"):
            analyze_benchmark(
                benchmark,
                {"ratings": [{"candidate": "Candidate 99", "ratings": {}}]},
            )
        with self.assertRaisesRegex(ValueError, "Duplicate ratings"):
            analyze_benchmark(
                benchmark,
                {"ratings": [
                    {"candidate": "Candidate 01", "ratings": {}},
                    {"candidate": "Candidate 01", "ratings": {}},
                ]},
            )

    def test_invalid_scores_are_rejected(self):
        benchmark = {
            "candidates": [{
                "blind_label": "Candidate 01", "id": "voice-1", "provider": "korva",
            }],
        }
        with self.assertRaisesRegex(ValueError, "number from 1 to 5"):
            analyze_benchmark(
                benchmark,
                {"ratings": [{
                    "candidate": "Candidate 01",
                    "ratings": {"naturalness": 6},
                }]},
            )


if __name__ == "__main__":
    unittest.main()
