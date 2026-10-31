from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import provider_voice_benchmark as benchmark


class FakeClient:
    pass


class ProviderVoiceBenchmarkTests(unittest.TestCase):
    def test_cloud_benchmark_requires_explicit_allow_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates") as candidates:
                with self.assertRaisesRegex(ValueError, "can incur charges"):
                    benchmark.run_benchmark(
                        "elevenlabs", "Xin chào", Path(tmp),
                        allow_cloud=False,
                    )
                candidates.assert_not_called()

    def test_blind_benchmark_hides_voice_names_and_keeps_mapping_in_report(self):
        candidates = [
            {"id": "secret-voice-a", "name": "Private Voice A", "language": "vi", "type": "preset"},
            {"id": "secret-voice-b", "name": "Private Voice B", "language": "vi", "type": "preset"},
        ]
        seen = []

        def fake_synthesize(provider, candidate, text, destination, **kwargs):
            seen.append((candidate["id"], text, kwargs["seed"], kwargs["client"]))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"RIFF" + b"\0" * 64)
            return destination

        client = FakeClient()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates", return_value=candidates):
                with patch.object(benchmark, "_synthesize", side_effect=fake_synthesize):
                    report = benchmark.run_benchmark(
                        "korva", "Cùng một câu thử.", Path(tmp),
                        language="vi", limit=10, seed=1234,
                        blind=True, client=client, delay=0,
                    )
            page = (Path(tmp) / "index.html").read_text(encoding="utf-8")
            saved = json.loads((Path(tmp) / "provider-voice-benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(report["ready"], 2)
            self.assertIn("Candidate 01", page)
            self.assertIn("Naturalness", page)
            self.assertIn("Export human ratings JSON", page)
            self.assertNotIn("Private Voice A", page)
            self.assertNotIn("secret-voice-a", page)
            self.assertEqual(saved["candidates"][0]["id"], "secret-voice-a")
            self.assertEqual([row[1] for row in seen], ["Cùng một câu thử."] * 2)
            self.assertEqual([row[2] for row in seen], [1234, 1234])
            self.assertTrue(all(row[3] is client for row in seen))

    def test_voice_studio_keeps_the_profile_saved_seed(self):
        calls = {}
        class Client:
            def synthesize(self, text, destination, **kwargs):
                calls.update(kwargs)
                destination.write_bytes(b"RIFF" + b"\\0" * 64)
                return destination
        with tempfile.TemporaryDirectory() as tmp:
            benchmark._synthesize(
                "voicestudio", {"id": "profile-123"}, "Same Vietnamese script",
                Path(tmp) / "voice.wav", engine="voxcpm2", language="vi",
                seed=9999, client=Client(),
            )
        self.assertEqual(calls["voice"], "profile-123")
        self.assertNotIn("seed", calls)

    def test_all_benchmarks_local_providers_without_cloud_permission(self):
        catalog = {
            "voicestudio": [{"id": "profile-1", "name": "Studio voice"}],
            "korva": [{"id": "khanh_vy", "name": "Khánh Vy"}],
        }
        calls = []
        def fake_synthesize(provider, candidate, text, destination, **kwargs):
            calls.append((provider, text, kwargs["seed"]))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"RIFF" + b"\\0" * 64)
            return destination
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates", side_effect=lambda p, language, client: catalog[p]):
                with patch.object(benchmark, "_synthesize", side_effect=fake_synthesize):
                    report = benchmark.run_benchmark(
                        "all", "Cùng một kịch bản.", Path(tmp), engine="voxcpm2",
                        language="vi", limit=5, seed=4200, allow_cloud=False,
                        blind=True, client=FakeClient(), delay=0,
                    )
            self.assertEqual(report["providers_included"], ["voicestudio", "korva"])
            self.assertEqual(report["ready"], 2)
            self.assertEqual([call[1] for call in calls], ["Cùng một kịch bản."] * 2)
            self.assertEqual({call[0] for call in calls}, {"voicestudio", "korva"})
            page = (Path(tmp) / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("Studio voice", page)
            self.assertNotIn("Khánh Vy", page)

    def test_all_adds_cloud_catalogues_only_after_explicit_allow_flag(self):
        catalogue_calls = []
        def fake_catalogue(provider, language, client):
            catalogue_calls.append(provider)
            return [{"id": f"{provider}-voice", "name": f"{provider} voice"}]
        def fake_synthesize(provider, candidate, text, destination, **kwargs):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"RIFF" + b"\\0" * 64)
            return destination
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates", side_effect=fake_catalogue):
                with patch.object(benchmark, "_synthesize", side_effect=fake_synthesize):
                    report = benchmark.run_benchmark(
                        "all", "Same text.", Path(tmp), engine="voxcpm2",
                        language="vi", limit=2, allow_cloud=True,
                        client=FakeClient(), delay=0,
                    )
            self.assertEqual(
                catalogue_calls,
                ["voicestudio", "korva", "google", "elevenlabs"],
            )
            self.assertEqual(report["providers_included"], catalogue_calls)
            self.assertTrue(report["cloud_enabled"])
            self.assertEqual(report["ready"], 4)

    def test_optional_asr_uses_same_voice_studio_client_and_adds_wer_cer(self):
        candidate = {"id": "khanh_vy", "name": "Khánh Vy"}
        class AsrClient:
            def transcribe(self, audio_path, language=None):
                self.last_path = audio_path
                self.last_language = language
                return "Xin chào Việt Nam."
        client = AsrClient()
        def fake_synthesize(provider, candidate, text, destination, **kwargs):
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"RIFF" + b"\\0" * 64)
            return destination
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates", return_value=[candidate]):
                with patch.object(benchmark, "_synthesize", side_effect=fake_synthesize):
                    report = benchmark.run_benchmark(
                        "korva", "Xin chào Việt Nam.", Path(tmp),
                        language="vi", seed=99, asr=True, client=client, delay=0,
                    )
            row = report["candidates"][0]
            self.assertEqual(row["asr_intelligibility_proxy"]["wer"], 0)
            self.assertEqual(row["asr_intelligibility_proxy"]["cer"], 0)
            self.assertEqual(client.last_language, "vi")
            page = (Path(tmp) / "index.html").read_text(encoding="utf-8")
            self.assertIn("ASR proxy WER 0.0%", page)

    def test_interrupted_benchmark_resumes_valid_audio_without_rerendering(self):
        calls = {"voice-a": 0, "voice-b": 0}

        def fake_synthesize(provider, candidate, text, destination, **kwargs):
            voice_id = candidate["id"]
            calls[voice_id] += 1
            if voice_id == "voice-b" and calls[voice_id] == 1:
                raise RuntimeError("simulated interrupted provider call")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"RIFF" + b"\\0" * 64)
            return destination

        candidates = [
            {"id": "voice-b", "name": "Voice B", "language": "vi"},
            {"id": "voice-a", "name": "Voice A", "language": "vi"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates", return_value=candidates):
                with patch.object(benchmark, "_synthesize", side_effect=fake_synthesize):
                    first = benchmark.run_benchmark(
                        "korva", "Cùng một kịch bản.", Path(tmp),
                        language="vi", seed=4200, blind=True, blind_seed=71,
                        client=FakeClient(), delay=0,
                    )
                    self.assertEqual(first["status"], "partial")
                    self.assertEqual(first["ready"], 1)
                    self.assertEqual(first["failed"], 1)

                    second = benchmark.run_benchmark(
                        "korva", "Cùng một kịch bản.", Path(tmp),
                        language="vi", seed=4200, blind=True, blind_seed=71,
                        client=FakeClient(), delay=0,
                    )

            self.assertEqual(second["status"], "complete")
            self.assertEqual(second["ready"], 2)
            self.assertEqual(second["failed"], 0)
            self.assertEqual(second["cache_hits"], 1)
            self.assertEqual(calls, {"voice-a": 1, "voice-b": 2})
            saved = json.loads(
                (Path(tmp) / "provider-voice-benchmark.json").read_text(encoding="utf-8")
            )
            self.assertEqual(saved["status"], "complete")
            self.assertEqual(saved["pending"], 0)

    def test_report_audio_path_cannot_escape_benchmark_output_directory(self):
        with tempfile.TemporaryDirectory() as output_tmp:
            with tempfile.TemporaryDirectory() as outside_tmp:
                outside_audio = Path(outside_tmp) / "outside.wav"
                outside_audio.write_bytes(b"audio")
                self.assertIsNone(
                    benchmark._safe_report_audio_path(
                        Path(output_tmp), str(outside_audio)
                    )
                )

    def test_all_requires_voice_studio_engine_for_fair_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates") as candidates:
                with self.assertRaisesRegex(ValueError, "Provider-wide benchmark"):
                    benchmark.run_benchmark(
                        "all", "Xin chào", Path(tmp), engine=None
                    )
                candidates.assert_not_called()

    def test_voice_studio_requires_exact_engine_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(benchmark, "_candidates") as candidates:
                with self.assertRaisesRegex(ValueError, "exact installed --engine ID"):
                    benchmark.run_benchmark(
                        "voicestudio", "Xin chào", Path(tmp), engine=None
                    )
                candidates.assert_not_called()


if __name__ == "__main__":
    unittest.main()
