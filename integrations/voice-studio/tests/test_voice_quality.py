from __future__ import annotations

import sys
import unicodedata
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from voice_quality import audit_speaker_identities, compare_text, normalize_text


class VoiceQualityTests(unittest.TestCase):
    def test_vietnamese_normalization_is_unicode_stable(self):
        self.assertEqual(
            normalize_text("Tiếng Việt"),
            normalize_text("Tie\u0302\u0301ng Vie\u0323\u0302t"),
        )

    def test_exact_transcript_has_zero_error(self):
        result = compare_text(
            "Trời trở lạnh, trời trăng sáng.",
            "Trời trở lạnh, trời trăng sáng!",
        )
        self.assertEqual(result["wer"], 0)
        self.assertEqual(result["cer"], 0)

    def test_tone_and_word_errors_are_not_silently_erased(self):
        result = compare_text(
            "má mà mả mã mạ",
            "ma ma ma ma ma",
        )
        self.assertGreater(result["wer"], 0)
        self.assertGreater(result["cer"], 0)
        self.assertEqual(result["expected_word_count"], 5)

    def test_speaker_identity_audit_confirms_stable_cast(self):
        result = audit_speaker_identities([
            {
                "speaker_id": "narrator", "provider": "voicestudio",
                "engine": "voxcpm2", "voice": "profile-1",
                "voice_identity_fingerprint": "abc"
            },
            {
                "speaker_id": "narrator", "provider": "voicestudio",
                "engine": "voxcpm2", "voice": "profile-1",
                "voice_identity_fingerprint": "abc"
            },
        ])
        self.assertEqual(result[0]["status"], "consistent")
        self.assertEqual(result[0]["segment_count"], 2)

    def test_speaker_identity_audit_detects_voice_drift(self):
        result = audit_speaker_identities([
            {
                "speaker_id": "host", "provider": "voicestudio",
                "engine": "voxcpm2", "voice": "profile-1",
                "voice_identity_fingerprint": "abc"
            },
            {
                "speaker_id": "host", "provider": "voicestudio",
                "engine": "voxcpm2", "voice": "profile-2",
                "voice_identity_fingerprint": "def"
            },
        ])
        self.assertEqual(result[0]["status"], "drift")
        self.assertEqual(result[0]["distinct_provider_engine_voice"], 2)

    def test_legacy_report_without_fingerprint_is_not_claimed_consistent(self):
        result = audit_speaker_identities([
            {"speaker_id": "guest", "provider": "korva", "engine": None, "voice": "khanh_vy"}
        ])
        self.assertEqual(result[0]["status"], "not_recorded")

    def test_empty_recognition_is_a_full_error(self):
        result = compare_text("xin chào", "")
        self.assertEqual(result["wer"], 1.0)
        self.assertEqual(result["cer"], 1.0)


if __name__ == "__main__":
    unittest.main()
