from __future__ import annotations

import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from providers import korva
from providers.korva import list_voices


class KorvaCatalogueTests(unittest.TestCase):
    def test_exposes_ten_preset_voices_without_model_install(self):
        voices = list_voices("vi")
        self.assertEqual(len(voices), 10)
        self.assertEqual(sum(v["gender"] == "female" for v in voices), 5)
        self.assertEqual(sum(v["gender"] == "male" for v in voices), 5)
        self.assertEqual(list_voices("en"), [])

    def test_synthesis_uses_official_cpu_api_seed_and_quality_steps(self):
        class FakeTTS:
            def __init__(self):
                self.kwargs = None
                self.saved = None
            def synthesize(self, text, **kwargs):
                self.kwargs = kwargs
                return b"audio", 1.0
            def save_audio(self, wav, path):
                self.saved = (wav, path)
                Path(path).write_bytes(b"RIFF" + b"\\0" * 64)

        engine = FakeTTS()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(korva, "_engine", return_value=engine) as loader:
                output = korva.synthesize(
                    "Xin chào", "khanh_vy", Path(tmp) / "voice.wav",
                    settings={"total_steps": 32, "num_threads": 4}, seed=123,
                )
                loader.assert_called_once_with(4)
                self.assertTrue(output.is_file())
        self.assertEqual(engine.kwargs["lang"], "vi")
        self.assertEqual(engine.kwargs["total_steps"], 32)
        self.assertEqual(engine.kwargs["seed"], 123)

    def test_rejects_quality_steps_above_upstream_maximum(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(korva, "_engine") as loader:
                with self.assertRaises(ValueError):
                    korva.synthesize(
                        "Xin chào", "khanh_vy", Path(tmp) / "voice.wav",
                        settings={"total_steps": 33},
                    )
                loader.assert_not_called()


if __name__ == "__main__":
    unittest.main()
