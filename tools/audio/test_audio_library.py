#!/usr/bin/env python3
"""Offline tests for rights classification and manifest-to-archive matching."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_audio_library_index as audio

class AudioRightsTests(unittest.TestCase):
    def test_cc0_is_redistributable_candidate(self):
        self.assertEqual(audio.rights_status("CC0-1.0", None), "redistributable_candidate")
    def test_cc_by_requires_attribution(self):
        self.assertEqual(audio.rights_status("CC-BY-4.0", None), "attribution_required")
    def test_nc_and_nd_are_not_default_commercial_assets(self):
        self.assertEqual(audio.rights_status("CC-BY-NC-4.0", None), "not_approved_for_default_commercial_use")
        self.assertEqual(audio.rights_status("CC-BY-ND-4.0", None), "not_approved_for_default_commercial_use")
    def test_share_alike_is_not_mislabeled_as_plain_attribution(self):
        self.assertEqual(audio.rights_status("CC-BY-SA-4.0", None), "share_alike_required")
        self.assertEqual(audio.rights_status("Creative Commons Attribution-ShareAlike 4.0", None), "share_alike_required")

    def test_unknown_license_fails_closed(self):
        self.assertEqual(audio.rights_status(None, None), "review_required")
        self.assertEqual(audio.rights_status("royalty free", None), "review_required")
    def test_explicit_non_redistributable_overrides_cc0_label(self):
        self.assertEqual(audio.rights_status("CC0-1.0", False), "source_only_or_not_redistributable")
    def test_audio_extension_filter(self):
        self.assertTrue(audio.is_audio_path("battle/impact.wav"))
        self.assertTrue(audio.is_audio_path("voice/line.ogg"))
        self.assertFalse(audio.is_audio_path("footage/scene.mp4"))
    def test_manifest_exact_path_match(self):
        record = {"path": "source/metal/blade.wav", "license": "CC0-1.0", "source_url": "https://example.invalid"}
        by_path, by_base = audio.build_asset_registry({"assets": [record]})
        found, method = audio.match_rights("source/metal/blade.wav", by_path, by_base)
        self.assertEqual(method, "exact_path")
        self.assertEqual(found["rights_status"], "redistributable_candidate")
    def test_ambiguous_basename_is_not_guessed(self):
        records = [
            {"path": "one/impact.wav", "license": "CC0-1.0"},
            {"path": "two/impact.wav", "license": "CC-BY-4.0"}
        ]
        by_path, by_base = audio.build_asset_registry({"assets": records})
        found, method = audio.match_rights("archive/impact.wav", by_path, by_base)
        self.assertIsNone(found)
        self.assertEqual(method, "ambiguous")

if __name__ == "__main__":
    unittest.main()
