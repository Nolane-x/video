import json
import tempfile
import unittest
from pathlib import Path

from search_audio_resources import search_catalogs


class UnifiedAudioSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.build76 = self.root / "preview-catalog.json"
        self.meta = self.root / "meta-preview-catalog.json"
        self.build76.write_text(json.dumps({
            "assets": [
                {
                    "asset_id": "b76-1",
                    "title": "Metal blade clash",
                    "archive_name": "video-assets-opengameart-audio-001.zip",
                    "archive_member": "weapons/blade_clash.wav",
                    "rights_status": "redistributable_candidate",
                    "auditioned_by_human": False,
                    "tags": ["sword", "impact", "metal"],
                    "category": "weapon foley",
                },
                {
                    "asset_id": "b76-review",
                    "title": "Unknown battle sound",
                    "rights_status": "review_required",
                    "tags": ["sword", "battle"],
                },
            ]
        }), encoding="utf-8")
        self.meta.write_text(json.dumps({
            "assets": [
                {
                    "asset_id": "meta-1",
                    "title": "Sword strike and armor ring",
                    "collection": "oculus-audio-pack",
                    "collection_kind": "foley",
                    "license": "CC-BY-4.0",
                    "rights_class": "cc_by_4_attribution_required",
                    "tags": ["sword", "katana", "metal", "clash"],
                    "auditioned_by_human": False,
                    "attribution_text": "Oculus Audio Pack 01 by Oculus VR, LLC",
                    "archive_member": "WEAP/sword-clash.ogg",
                    "source_wav_file": "WEAPSwrd_SwordClash_OS_01.wav",
                    "wav_master_download_url": "https://github.com/Nolane-x/video/releases/download/nolane-historical-audio-library-v0.1.0/meta-open-sound-oculus-audio-pack-wav.zip",
                    "wav_master_sha256": "cc9dcf42d20c339e82ca9dcaa976553179ee4d1951f011ea31eeed93ac43e93c",
                },
                {
                    "asset_id": "meta-piano-1",
                    "title": "Piano C4 multisample",
                    "collection_kind": "instrument",
                    "license": "CC0-1.0",
                    "rights_class": "cc0_public_domain",
                    "tags": ["piano", "instrument", "note"],
                    "auditioned_by_human": False,
                },
                {
                    "asset_id": "false-bow-hit",
                    "title": "Elbow body collision",
                    "collection_kind": "foley",
                    "license": "CC-BY-4.0",
                    "rights_class": "cc_by_4_attribution_required",
                    "tags": ["body", "elbow", "impact"],
                    "auditioned_by_human": False,
                },
                {
                    "asset_id": "real-bow",
                    "title": "Bowstring release",
                    "collection_kind": "foley",
                    "license": "CC-BY-4.0",
                    "rights_class": "cc_by_4_attribution_required",
                    "tags": ["bow", "string", "release"],
                    "auditioned_by_human": False,
                },
            ]
        }), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_searches_both_sources_and_excludes_review_by_default(self):
        items = search_catalogs([self.build76, self.meta], "sword clash")
        self.assertEqual({item["asset_id"] for item in items}, {"b76-1", "meta-1"})
        self.assertTrue(all(item["audition_status"] == "NOT_AUDITIONED" for item in items))
        self.assertNotIn("b76-review", {item["asset_id"] for item in items})

    def test_cc_by_attribution_is_carried_through(self):
        items = search_catalogs([self.build76, self.meta], "katana sword")
        self.assertEqual(len(items), 1)
        self.assertIn("Oculus Audio Pack 01", items[0]["attribution_text"])
        self.assertEqual(items[0]["rights_status_normalized"], "cc_by_4_attribution_required")

    def test_search_result_exposes_exact_wav_master(self):
        items = search_catalogs([self.build76, self.meta], "katana sword")
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0]["wav_master_download_url"].endswith("-wav.zip"))
        self.assertEqual(items[0]["source_wav_file"], "WEAPSwrd_SwordClash_OS_01.wav")
        self.assertEqual(len(items[0]["wav_master_sha256"]), 64)

    def test_kind_filter_separates_instrument_samples_from_foley(self):
        foley = search_catalogs([self.build76, self.meta], "sword clash", kind="foley")
        instruments = search_catalogs([self.build76, self.meta], "piano note", kind="instrument")
        self.assertEqual([item["asset_id"] for item in foley], ["meta-1"])
        self.assertEqual([item["asset_id"] for item in instruments], ["meta-piano-1"])

    def test_whole_token_search_avoids_false_positive_substrings(self):
        items = search_catalogs([self.build76, self.meta], "bow")
        ids = {item["asset_id"] for item in items}
        self.assertIn("real-bow", ids)
        self.assertNotIn("false-bow-hit", ids)

    def test_generic_foley_synonyms_are_tag_assisted_not_direct(self):
        matches = search_catalogs([self.build76, self.meta], "march")
        self.assertTrue(matches)
        self.assertTrue(all(item["match_quality"] == "tag_assisted" for item in matches))
        self.assertEqual(search_catalogs([self.build76, self.meta], "march", direct_only=True), [])

    def test_search_never_promotes_unauditioned_assets(self):
        items = search_catalogs([self.build76, self.meta], "sword clash")
        self.assertTrue(all(item["final_use_gate"].startswith("human_audition") for item in items))
        self.assertEqual(search_catalogs([self.build76, self.meta], "sword clash", only_auditioned=True), [])


if __name__ == "__main__":
    unittest.main()
