import unittest

from validate_foley_review_decisions import PACK_ID, validate_review


def fixture_catalog():
    return {
        "release_tag": "nolane-illustrated-history-foley-v0.2.0",
        "assets": [{
            "asset_id": "ihf-abc123",
            "title": "Sword impact",
            "path": "assets/weapon/sword.wav",
            "sha256": "a" * 64,
            "creator": "Artist",
            "source_page": "https://example.invalid/source",
            "license": "CC0-1.0",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "rights_class": "public_cc0_pd",
            "duration_seconds": 1.25,
            "codec": "pcm_s16le",
            "sample_rate_hz": 48000,
            "channels": 1,
        }]
    }


def fixture_review(**overrides):
    row = {
        "asset_id": "ihf-abc123",
        "sha256": "a" * 64,
        "human_auditioned": True,
        "approved_for_final_mix": True,
        "decision": "keep_candidate",
        "rating": "4",
        "notes": "Listened; fits the shield contact after layering.",
    }
    row.update(overrides)
    return {
        "schema_version": "1.0.0",
        "pack": PACK_ID,
        "decisions": [row],
    }


class FoleyReviewValidationTests(unittest.TestCase):
    def test_allows_only_a_matching_human_auditioned_cc0_approval(self):
        report = validate_review(fixture_catalog(), fixture_review())
        self.assertEqual(report["human_auditioned_count"], 1)
        self.assertEqual(report["approved_for_final_mix_count"], 1)
        self.assertEqual(report["status"], "VALIDATED_WITH_HUMAN_APPROVALS")
        self.assertEqual(report["approved_for_final_mix"][0]["asset_id"], "ihf-abc123")

    def test_blocks_approval_without_human_audition(self):
        with self.assertRaisesRegex(ValueError, "before human audition"):
            validate_review(fixture_catalog(), fixture_review(human_auditioned=False))

    def test_blocks_approval_of_rejected_cue(self):
        with self.assertRaisesRegex(ValueError, "decision=keep_candidate"):
            validate_review(fixture_catalog(), fixture_review(decision="reject"))

    def test_blocks_sha256_mismatch(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            validate_review(fixture_catalog(), fixture_review(sha256="b" * 64))

    def test_blocks_unknown_or_duplicate_asset_ids(self):
        with self.assertRaisesRegex(ValueError, "Unknown asset_id"):
            validate_review(fixture_catalog(), fixture_review(asset_id="not-in-catalog"))
        review = fixture_review()
        review["decisions"].append(dict(review["decisions"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate review decision"):
            validate_review(fixture_catalog(), review)

    def test_no_approval_is_a_valid_non_final_review(self):
        report = validate_review(
            fixture_catalog(),
            fixture_review(approved_for_final_mix=False, human_auditioned=False, decision="unreviewed"),
        )
        self.assertEqual(report["approved_for_final_mix_count"], 0)
        self.assertEqual(report["status"], "VALIDATED_NO_FINAL_MIX_APPROVALS")


if __name__ == "__main__":
    unittest.main()
