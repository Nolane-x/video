import copy
import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_editorial_review import validate_review_data

ACTUAL_SHA = "a" * 64
DURATION = 10.0


def valid_review():
    return {
        "schemaVersion": 1,
        "candidate": {
            "sourceCommit": "1234567890abcdef",
            "videoPath": "out/candidate.mp4",
            "sha256": ACTUAL_SHA,
            "durationSeconds": DURATION,
        },
        "reviewer": {
            "reviewerId": "independent-reviewer-01",
            "role": "independent-editorial-reviewer",
            "contextIndependent": True,
            "reviewedAtUtc": "2026-10-31T12:00:00Z",
        },
        "method": {
            "fullPlaybackWithAudio": True,
            "normalPlaybackSpeed": True,
            "openEndedFindingsRecordedFirst": True,
            "checklistReviewedAfter": True,
            "checkedAtNativeDeliveryResolution": True,
        },
        "coverage": [
            {"start": 0, "end": 5, "visualReviewed": True, "audioReviewed": True},
            {"start": 5, "end": 10, "visualReviewed": True, "audioReviewed": True},
        ],
        "scores": {
            "storyClarity": 8,
            "pacing": 8,
            "visualVariety": 8,
            "motionContinuity": 8,
            "audioIntelligibility": 8,
            "captionLegibility": 8,
            "referenceFit": 8,
            "platformFit": 8,
        },
        "scoreEvidence": {
            key: "Reviewed the full sequence and recorded timecoded observations for this category."
            for key in (
                "storyClarity", "pacing", "visualVariety", "motionContinuity",
                "audioIntelligibility", "captionLegibility", "referenceFit", "platformFit",
            )
        },
        "openEndedFindings": [
            "Unaided first pass: no major issue; the ending could use a more distinct visual payoff."
        ],
        "findings": [],
        "decision": "PASS",
        "limitationsAcknowledged": True,
    }


class EditorialReviewContractTests(unittest.TestCase):
    def test_complete_review_attestation_passes(self):
        self.assertEqual(validate_review_data(valid_review(), ACTUAL_SHA, DURATION), [])

    def test_media_hash_mismatch_blocks_review(self):
        errors = validate_review_data(valid_review(), "b" * 64, DURATION)
        self.assertTrue(any("sha256 does not match" in e for e in errors))

    def test_missing_coverage_segment_blocks_review(self):
        review = valid_review()
        review["coverage"] = [review["coverage"][0]]
        errors = validate_review_data(review, ACTUAL_SHA, DURATION)
        self.assertTrue(any("coverage ends" in e for e in errors))

    def test_unresolved_p1_defect_blocks_pass_decision(self):
        review = valid_review()
        review["findings"] = [{
            "severity": "P1",
            "defectClass": "continuity",
            "timecodeStart": 4.2,
            "description": "The prop jumps across the cut.",
            "evidence": "At 00:04.2 the phone changes hands across the transition.",
            "resolved": False,
        }]
        errors = validate_review_data(review, ACTUAL_SHA, DURATION)
        self.assertTrue(any("unresolved P1" in e for e in errors))

    def test_non_independent_reviewer_is_rejected(self):
        review = valid_review()
        review["reviewer"]["contextIndependent"] = False
        errors = validate_review_data(review, ACTUAL_SHA, DURATION)
        self.assertTrue(any("contextIndependent" in e for e in errors))

    def test_low_editorial_score_blocks_release(self):
        review = valid_review()
        review["scores"]["pacing"] = 6
        errors = validate_review_data(review, ACTUAL_SHA, DURATION)
        self.assertTrue(any("below the release threshold" in e for e in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
