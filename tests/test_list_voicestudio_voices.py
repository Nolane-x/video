from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "video" / "list_voicestudio_voices.py"
SPEC = importlib.util.spec_from_file_location("voicestudio_voice_selector", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def sample_manifest():
    return {
        "built_at": "2026-11-01T00:00:00+00:00",
        "counts": {"en": 933, "vi": 25, "unique_voice_identities": 933},
        "voices": [
            {
                "id": "en-piper-libritts-high-0000",
                "display_name": "English Speaker 001",
                "language": "en",
                "engine": "Piper TTS 1.8.0",
                "sample_rate": 22050,
                "duration_seconds": 10.0,
                "sample_text": "Hello.",
                "rights": {
                    "rights_status": "restricted-evidence",
                    "commercial_use": "not-cleared-by-this-build",
                    "attribution_required": True,
                    "notice": "Voice terms vary.",
                },
            },
            {
                "id": "en-vieneu-v3turbo-adam-123456",
                "display_name": "VieNeu Adam",
                "language": "en",
                "engine": "VieNeu-TTS v3 Turbo 3.8.3",
                "sample_rate": 48000,
                "duration_seconds": 8.0,
                "sample_text": "Welcome.",
                "rights": {
                    "rights_status": "upstream-preset-consent-stated",
                    "commercial_use": "upstream-model-card-permits-generated-audio",
                    "attribution_required": True,
                    "notice": "Upstream model card permits commercial generated audio.",
                },
            },
            {
                "id": "en-kokoro-v1-af_heart",
                "display_name": "English (US) · Heart · Grade A",
                "language": "en",
                "engine": "Kokoro-82M 0.9.4",
                "sample_rate": 24000,
                "duration_seconds": 8.0,
                "sample_text": "Welcome.",
                "upstream_quality_grade": "A",
                "quality_grade_source": "Kokoro upstream VOICES.md",
                "rights": {
                    "rights_status": "upstream-apache-2.0-model-voice-assets",
                    "commercial_use": "apache-2.0-model-and-voice-assets",
                    "attribution_required": True,
                    "notice": "Apache-2.0 model and packaged voice assets; upstream grade is subjective."
                },
            },
            {
                "id": "vi-vieneu-v3turbo-adam-123456",
                "display_name": "VieNeu Adam",
                "language": "vi",
                "engine": "VieNeu-TTS v3 Turbo 3.8.3",
                "sample_rate": 48000,
                "duration_seconds": 8.0,
                "sample_text": "Xin chào.",
                "rights": {
                    "rights_status": "upstream-preset-consent-stated",
                    "commercial_use": "upstream-model-card-permits-generated-audio",
                    "attribution_required": True,
                    "notice": "Upstream model card permits commercial generated audio.",
                },
            },
        ],
    }


class VoiceCatalogSelectorTests(unittest.TestCase):
    def test_language_filter_returns_only_matching_locale(self):
        rows = MODULE.select_voices(sample_manifest(), language="vi")
        self.assertEqual([row["voice_id"] for row in rows], ["vi-vieneu-v3turbo-adam-123456"])

    def test_engine_filter_matches_case_insensitively(self):
        rows = MODULE.select_voices(sample_manifest(), engine="vieneu")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all("VieNeu" in row["engine"] for row in rows))

    def test_commercial_filter_excludes_piper_restricted_evidence(self):
        rows = MODULE.select_voices(sample_manifest(), commercial_permitted_only=True)
        self.assertEqual(len(rows), 3)
        self.assertFalse(any("piper" in row["voice_id"] for row in rows))
        self.assertEqual({row["commercial_use"] for row in rows}, upstream-model-card-permits-generated-audioS)

    def test_combined_filter_and_limit_are_deterministic(self):
        rows = MODULE.select_voices(
            sample_manifest(),
            language="en",
            engine="vieneu",
            commercial_permitted_only=True,
            limit=1,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["voice_id"], "en-vieneu-v3turbo-adam-123456")

    def test_kokoro_engine_and_upstream_grade_are_exposed(self):
        rows = MODULE.select_voices(sample_manifest(), language="en", engine="kokoro")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["voice_id"], "en-kokoro-v1-af_heart")
        self.assertEqual(rows[0]["upstream_quality_grade"], "A")
        self.assertEqual(rows[0]["quality_grade_source"], "Kokoro upstream VOICES.md")

    def test_empty_manifest_selection_is_empty_not_fabricated(self):
        self.assertEqual(MODULE.select_voices({"voices": []}), [])


if __name__ == "__main__":
    unittest.main()
