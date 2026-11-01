from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from providers import elevenlabs, google_cloud


class ProviderCatalogueTests(unittest.TestCase):
    def test_google_short_language_codes_expand_to_region_codes(self):
        self.assertEqual(google_cloud._normalize_language("vi"), "vi-VN")
        self.assertEqual(google_cloud._normalize_language("en"), "en-US")
        self.assertEqual(google_cloud._normalize_language("vi-VN"), "vi-VN")

    def test_elevenlabs_catalogue_paginates_and_filters_verified_language(self):
        page_one = {
            "voices": [{
                "voice_id": "voice-vi",
                "name": "Vietnamese voice",
                "category": "professional",
                "verified_languages": [{"language": "Vietnamese"}],
                "labels": {"accent": "Northern Vietnamese"}
            }],
            "next_page_token": "page-2"
        }
        page_two = {
            "voices": [{
                "voice_id": "voice-en",
                "name": "English voice",
                "category": "premade",
                "verified_languages": [{"language": "English"}]
            }],
            "next_page_token": None
        }
        responses = [
            (json.dumps(page_one).encode("utf-8"), "application/json"),
            (json.dumps(page_two).encode("utf-8"), "application/json")
        ]
        with patch.object(elevenlabs, "_request", side_effect=responses) as request:
            voices = elevenlabs.list_voices(language="vi", page_size=1, max_pages=3)
        self.assertEqual([voice["id"] for voice in voices], ["voice-vi"])
        self.assertEqual(voices[0]["verified_languages"], ["Vietnamese"])
        self.assertEqual(request.call_count, 2)
        self.assertEqual(request.call_args_list[1].kwargs["query"]["next_page_token"], "page-2")

    def test_elevenlabs_catalogue_accepts_language_code_metadata(self):
        page = {
            "voices": [{
                "voice_id": "voice-vicode",
                "name": "Vietnamese code voice",
                "verified_languages": [{"language": "vi"}]
            }]
        }
        with patch.object(
            elevenlabs, "_request",
            return_value=(json.dumps(page).encode("utf-8"), "application/json")
        ):
            voices = elevenlabs.list_voices(language="Vietnamese")
        self.assertEqual([voice["id"] for voice in voices], ["voice-vicode"])


if __name__ == "__main__":
    unittest.main()
