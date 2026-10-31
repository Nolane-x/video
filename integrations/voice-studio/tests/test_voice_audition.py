from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from voice_audition import collect_auditions


class FakeVoiceStudio:
    def list_profiles(self):
        return [
            {"id": "profile-1", "name": "<script>alert(1)</script>", "language": "Auto"},
        ]

    def list_archetypes(self, **kwargs):
        return [
            {
                "id": "archetype-1", "name": "Vietnamese Narrator",
                "language": "Vietnamese", "instruct": "female, middle-aged, low pitch",
                "facets": {"gender": "female", "age": "middle-aged", "pitch": "low pitch"},
            }
        ]

    def profile_audio(self, profile_id, output_path):
        path = Path(output_path).with_suffix(".wav")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"RIFF" + b"\0" * 64)
        return path

    def archetype_preview_state(self, archetype_id):
        return {"source": "gallery", "message": "cached"}

    def preview_archetype(self, archetype_id, output_path):
        path = Path(output_path).with_suffix(".mp3")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"ID3" + b"\0" * 64)
        return path


class VoiceAuditionTests(unittest.TestCase):
    def test_combined_gallery_keeps_both_sources_and_escapes_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = collect_auditions(
                FakeVoiceStudio(), Path(tmp),
                source="both", language="vi", limit=5, delay=0,
            )
            self.assertEqual(result["total"], 2)
            self.assertEqual(result["ready"], 2)
            page = (Path(tmp) / "index.html").read_text(encoding="utf-8")
            self.assertIn("Vietnamese Narrator", page)
            self.assertNotIn("<script>alert(1)</script>", page)
            self.assertIn("&lt;script&gt;", page)
            self.assertTrue((Path(tmp) / "audio").is_dir())

    def test_language_filter_includes_auto_profile_for_cross_language_voice(self):
        self.assertTrue(
            __import__("voice_audition")._language_matches("Auto", "vi")
        )
        self.assertTrue(
            __import__("voice_audition")._language_matches("vi-VN", "vi")
        )
        self.assertFalse(
            __import__("voice_audition")._language_matches("English", "vi")
        )


if __name__ == "__main__":
    unittest.main()
