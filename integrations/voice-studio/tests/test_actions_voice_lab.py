from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from actions_voice_lab import (
    load_suite, master_candidates, run_lab, safe_audio_path,
    write_cross_scenario_audition,
)


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

    def test_cross_scenario_audition_groups_all_scripts_and_hides_voice_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = []
            for index, case_id in enumerate(
                ("tones-phonemes", "code-switch", "numbers-and-proper-nouns", "documentary-longform"),
                1,
            ):
                case_root = root / "cases" / case_id
                (case_root / "audio").mkdir(parents=True)
                candidates = []
                for candidate_index, candidate_id in enumerate(("private-voice-a", "private-voice-b"), 1):
                    filename = f"{candidate_index:03d}-Candidate-{candidate_index:02d}.wav"
                    (case_root / "audio" / filename).write_bytes(b"RIFF" + b"audio-data")
                    candidates.append({
                        "id": candidate_id,
                        "name": f"PRIVATE NAME {candidate_index}",
                        "blind_label": f"Candidate {candidate_index:02d}",
                        "status": "ready",
                        "audio_file": f"audio/{filename}",
                    })
                cases.append({
                    "id": case_id,
                    "title": f"Scenario {index}",
                    "text": "Xin chào Việt Nam.",
                    "candidates": candidates,
                })

            result = write_cross_scenario_audition(root, {"cases": cases})
            page = (root / result["page"]).read_text(encoding="utf-8")
            self.assertEqual(result["candidate_count"], 2)
            self.assertEqual(result["case_count"], 4)
            self.assertEqual(result["ready_track_count"], 8)
            self.assertFalse(result["candidate_identity_in_html"])
            self.assertEqual(result["identity_map_file"], "actions-voice-lab.json")
            self.assertTrue(result["identity_map_in_artifact"])
            self.assertIn("Candidate 01", page)
            self.assertIn("Candidate 02", page)
            self.assertIn("voice-human-ratings-all-scripts.json", page)
            self.assertIn("data-dimension=\"vietnamese\"", page)
            self.assertIn("Scenario 4", page)
            self.assertEqual(page.count("<audio controls"), 8)
            self.assertNotIn("private-voice-a", page)
            self.assertNotIn("PRIVATE NAME", page)

    def test_cross_scenario_audition_marks_missing_or_unsafe_samples_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case_root = root / "cases" / "tones-phonemes"
            (case_root / "audio").mkdir(parents=True)
            valid = case_root / "audio" / "001-Candidate-01.wav"
            valid.write_bytes(b"RIFF" + b"valid-audio")
            cases = [{
                "id": "tones-phonemes",
                "title": "Thanh điệu",
                "text": "Xin chào",
                "candidates": [
                    {
                        "id": "voice-good", "blind_label": "Candidate 01",
                        "status": "ready", "audio_file": "audio/001-Candidate-01.wav",
                    },
                    {
                        "id": "voice-unsafe", "blind_label": "Candidate 02",
                        "status": "ready", "audio_file": "../../outside.wav",
                    },
                ],
            }]
            result = write_cross_scenario_audition(root, {"cases": cases})
            page = (root / result["page"]).read_text(encoding="utf-8")
            self.assertEqual(result["ready_track_count"], 1)
            self.assertEqual(page.count("Không thể xác minh file audio."), 1)
            self.assertNotIn("../../outside.wav", page)
            self.assertNotIn("voice-unsafe", page)

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

    def test_mastering_is_applied_once_and_persisted_for_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audio = root / "audio" / "001-Candidate-01.wav"
            audio.parent.mkdir(parents=True)
            audio.write_bytes(b"RIFF" + b"raw-audio-payload")
            raw_sha = __import__("hashlib").sha256(audio.read_bytes()).hexdigest()
            report = {
                "status": "complete",
                "candidate_count": 1,
                "ready": 1,
                "failed": 0,
                "pending": 0,
                "catalogue_errors": [],
                "candidates": [{
                    "id": "voice-1",
                    "status": "ready",
                    "audio_file": "audio/001-Candidate-01.wav",
                    "sha256": raw_sha,
                    "bytes": audio.stat().st_size,
                }],
            }
            mastering_result = {
                "filter": "ffmpeg-loudnorm",
                "target_integrated_loudness_lufs": -20.0,
                "true_peak_ceiling_dbtp": -2.5,
            }
            def fake_master(path, **kwargs):
                path.write_bytes(b"RIFF" + b"mastered-audio-payload")
                return mastering_result

            with patch("actions_voice_lab.normalize_voice_file", side_effect=fake_master) as normalizer:
                mastered = master_candidates(root, report)
                normalizer.assert_called_once()
            row = mastered["candidates"][0]
            mastered_sha = __import__("hashlib").sha256(audio.read_bytes()).hexdigest()
            self.assertEqual(row["mastering"], mastering_result)
            self.assertEqual(row["sha256"], mastered_sha)
            self.assertNotEqual(row["sha256"], raw_sha)
            saved = json.loads((root / "provider-voice-benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["candidates"][0]["sha256"], mastered_sha)

            with patch("actions_voice_lab.normalize_voice_file") as normalizer:
                resumed = master_candidates(root, saved)
                normalizer.assert_not_called()
            self.assertEqual(resumed["status"], "complete")

    def test_mastering_failure_marks_benchmark_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audio = root / "audio" / "candidate.wav"
            audio.parent.mkdir(parents=True)
            audio.write_bytes(b"RIFF" + b"raw")
            import hashlib
            benchmark = {
                "candidate_count": 1,
                "ready": 1,
                "failed": 0,
                "pending": 0,
                "catalogue_errors": [],
                "candidates": [{
                    "id": "voice-1", "status": "ready",
                    "audio_file": "audio/candidate.wav",
                    "sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                }],
            }
            with patch("actions_voice_lab.normalize_voice_file", side_effect=RuntimeError("ffmpeg failed")):
                result = master_candidates(root, benchmark)
            self.assertEqual(result["status"], "partial")
            self.assertEqual(result["ready"], 0)
            self.assertEqual(result["failed"], 1)
            self.assertIn("Mastering failed", result["candidates"][0]["error"])

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
                audio = Path(root) / "case" / "audio" / "audio.wav"
                audio.parent.mkdir(parents=True)
                audio.write_bytes(b"audio")
                self.assertEqual(
                    safe_audio_path(Path(root) / "case", "audio/audio.wav"),
                    audio.resolve(),
                )
                with self.assertRaisesRegex(ValueError, "escapes benchmark output"):
                    safe_audio_path(Path(root) / "case", str(Path(outside) / "outside.wav"))


if __name__ == "__main__":
    unittest.main()
