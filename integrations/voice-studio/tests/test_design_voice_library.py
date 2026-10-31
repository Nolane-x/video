from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from design_voice_library import create_library, validate_design_set


def sample_set():
    return {
        "engine": "voxcpm2",
        "language": "vi",
        "sample_text": "Xin chào, đây là mẫu thử.",
        "voices": [
            {
                "name": "Narrator A",
                "description": "Original fictional Vietnamese female narrator, warm low-mid timbre.",
                "seed": 4201
            },
            {
                "name": "Expert B",
                "description": "Original fictional Vietnamese male expert, calm medium-low timbre.",
                "seed": 4202
            },
        ],
    }


class FakeVoiceStudio:
    def __init__(self):
        self.created = []
        self.previews = []

    def create_design_profile(self, name, description, **kwargs):
        profile_id = f"profile-{kwargs['seed']}"
        self.created.append((name, description, kwargs))
        return {"id": profile_id, "name": name}

    def profile_audio(self, profile_id, output_path):
        path = Path(output_path).with_suffix(".wav")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"RIFF" + b"\0" * 64)
        self.previews.append(profile_id)
        return path


class VoiceDesignLibraryTests(unittest.TestCase):
    def test_validates_engine_and_unique_voice_seeds(self):
        engine, language, voices = validate_design_set(sample_set())
        self.assertEqual(engine, "voxcpm2")
        self.assertEqual(language, "vi")
        self.assertEqual(len(voices), 2)
        bad = sample_set()
        bad["voices"][1]["seed"] = bad["voices"][0]["seed"]
        with self.assertRaisesRegex(ValueError, "distinct seed"):
            validate_design_set(bad)

    def test_plan_only_never_calls_voice_studio(self):
        client = FakeVoiceStudio()
        with tempfile.TemporaryDirectory() as tmp:
            report = create_library(sample_set(), Path(tmp), create=False, client=client)
        self.assertEqual(report["status"], "plan_only")
        self.assertEqual(client.created, [])
        self.assertEqual(client.previews, [])

    def test_creates_profiles_renders_previews_and_resumes_without_duplicates(self):
        client = FakeVoiceStudio()
        with tempfile.TemporaryDirectory() as tmp:
            first = create_library(
                sample_set(), Path(tmp), create=True, render_previews=True,
                delay=0, client=client,
            )
            self.assertEqual(first["created_or_reused"], 2)
            self.assertEqual(first["failed"], 0)
            self.assertEqual(len(client.created), 2)
            self.assertEqual(len(client.previews), 2)
            cast_path = Path(tmp) / "voice-cast.json"
            cast = __import__("json").loads(cast_path.read_text(encoding="utf-8"))
            self.assertEqual(cast["cast"]["narrator_a"]["voice"], "profile-4201")
            self.assertEqual(cast["cast"]["expert_b"]["engine"], "voxcpm2")

            second = create_library(
                sample_set(), Path(tmp), create=True, render_previews=True,
                delay=0, client=client,
            )
            self.assertEqual(second["created_or_reused"], 2)
            self.assertEqual(len(client.created), 2)
            self.assertEqual(len(client.previews), 4)
            self.assertTrue((Path(tmp) / "voice-design-library.json").is_file())
            self.assertTrue(cast_path.is_file())


if __name__ == "__main__":
    unittest.main()
