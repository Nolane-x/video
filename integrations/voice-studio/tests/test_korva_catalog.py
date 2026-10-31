from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from providers.korva import list_voices


class KorvaCatalogueTests(unittest.TestCase):
    def test_exposes_ten_preset_voices_without_model_install(self):
        voices = list_voices("vi")
        self.assertEqual(len(voices), 10)
        self.assertEqual(sum(v["gender"] == "female" for v in voices), 5)
        self.assertEqual(sum(v["gender"] == "male" for v in voices), 5)
        self.assertEqual(list_voices("en"), [])


if __name__ == "__main__":
    unittest.main()
