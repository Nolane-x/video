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
