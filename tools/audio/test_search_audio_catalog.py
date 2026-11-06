from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_audio_catalog import search_assets


class AudioSearchTests(unittest.TestCase):
    def test_search_ranks_matching_title(self):
        catalog = {"assets": [
            {"title": "distant rain", "rights_status": "redistributable_candidate", "auditioned_by_human": False, "approved_for_final_mix": False},
            {"title": "metal blade draw", "rights_status": "redistributable_candidate", "auditioned_by_human": False, "approved_for_final_mix": False}
        ]}
        found = search_assets(catalog, "metal blade", limit=5)
        self.assertEqual(found[0]["title"], "metal blade draw")

    def test_review_required_is_hidden_by_default(self):
        catalog = {"assets": [
            {"title": "approved candidate", "rights_status": "redistributable_candidate"},
            {"title": "unknown recording", "rights_status": "review_required"}
        ]}
        found = search_assets(catalog, "recording", limit=5)
        self.assertEqual([x["title"] for x in found], ["approved candidate"])

    def test_search_never_promotes_unheard_audio_to_final(self):
        catalog = {"assets": [
            {"title": "footstep", "rights_status": "redistributable_candidate", "auditioned_by_human": False, "approved_for_final_mix": False}
        ]}
        found = search_assets(catalog, "footstep")
        self.assertEqual(found[0]["final_use_gate"], "requires_human_audition_and_project_license_review")


if __name__ == "__main__":
    unittest.main()
