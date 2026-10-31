import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from caption_coverage import expected_text_for_shot, normalize_text, targeted_ocr_region, text_coverage


class CaptionCoverageTests(unittest.TestCase):
    def test_vietnamese_accent_normalization(self):
        self.assertEqual(normalize_text("Đừng bỏ cuộc!"), "dung bo cuoc")

    def test_text_coverage_is_case_and_punctuation_tolerant(self):
        self.assertGreaterEqual(text_coverage("The feed can wait.", "THE FEED can wait"), 0.99)

    def test_text_coverage_accepts_ocr_that_collapses_label_spacing(self):
        self.assertEqual(text_coverage("DAY 14", "DAY14"), 1.0)
        self.assertEqual(text_coverage("6:12 AM", "6:12AM"), 1.0)

    def test_ocr_single_word_error_is_reported_as_partial_not_zero(self):
        score = text_coverage("The feed always has one more thing", "The feed always has one more think")
        self.assertGreaterEqual(score, 0.8)
        self.assertLess(score, 1.0)

    def test_coverage_fails_when_subtitle_is_not_detected(self):
        self.assertLess(text_coverage("Bạn có thể bắt đầu lại", "background only"), 0.67)

    def test_default_manifest_contract_is_subtitle_plus_final_title(self):
        first = {"line": "First subtitle", "args": {"title": "Scene title", "subtitle": "First subtitle"}}
        final = {"line": "Final subtitle", "args": {"title": "Final card", "subtitle": "Final subtitle"}}
        self.assertEqual(expected_text_for_shot(first, 0, 2), [{"kind": "subtitle", "text": "First subtitle"}])
        self.assertEqual(expected_text_for_shot(final, 1, 2), [
            {"kind": "subtitle", "text": "Final subtitle"},
            {"kind": "end-card-title", "text": "Final card"}
        ])

    def test_explicit_on_screen_text_contract_wins(self):
        shot = {"args": {"title": "Not used"}, "requiredOnScreenText": ["Visible heading", "Required label"]}
        self.assertEqual(expected_text_for_shot(shot, 0, 1), [
            {"kind": "required", "text": "Visible heading"},
            {"kind": "required", "text": "Required label"}
        ])

    def test_dynamic_day_and_red_word_overlays_are_included(self):
        shot = {
            "line": "The voice starts sounding like your own.",
            "args": {
                "subtitle": "The voice starts sounding like your own.",
                "setting": "mirror",
                "day": "DAY 03",
                "redWords": ["TOMORROW", "LATER"]
            }
        }
        self.assertEqual(expected_text_for_shot(shot, 0, 1), [
            {"kind": "subtitle", "text": "The voice starts sounding like your own."},
            {"kind": "day-counter", "text": "DAY 03"},
            {"kind": "red-word", "text": "TOMORROW"},
            {"kind": "red-word", "text": "LATER"}
        ])

    def test_fixed_scene_labels_are_included(self):
        shot = {"line": "One day becomes a habit.", "args": {"setting": "calendar", "subtitle": "One day becomes a habit."}}
        self.assertEqual(expected_text_for_shot(shot, 0, 1)[-1], {"kind": "scene-label", "text": "THIS MONTH"})

    def test_targeted_ocr_regions_cover_small_day_counter_and_lower_third(self):
        shot = {"args": {"day": "DAY 14", "setting": "library"}}
        day_region = targeted_ocr_region({"kind": "day-counter", "text": "DAY 14"}, shot)
        subtitle_region = targeted_ocr_region({"kind": "subtitle", "text": "Your attention belongs to you."}, shot)
        self.assertEqual(day_region, ("top-left-day-counter", (25, 12, 140, 68)))
        self.assertEqual(subtitle_region, ("lower-third-subtitle", (80, 575, 1120, 145)))

    def test_targeted_ocr_region_tracks_calendar_and_bus_stop_signs(self):
        calendar = targeted_ocr_region(
            {"kind": "scene-label", "text": "THIS MONTH"}, {"args": {"setting": "calendar"}}
        )
        bus_stop = targeted_ocr_region(
            {"kind": "scene-label", "text": "BUS"}, {"args": {"setting": "busStop"}}
        )
        self.assertEqual(calendar, ("calendar-heading", (570, 65, 520, 115)))
        self.assertEqual(bus_stop, ("bus-stop-sign", (890, 148, 90, 70)))

    def test_multiword_kinetic_phrases_use_distinct_clear_regions(self):
        shot = {"args": {"setting": "void", "redWords": ["ONE MORE", "TOMORROW", "JUST ONCE", "LATER"]}}
        one_more = targeted_ocr_region({"kind": "red-word", "text": "ONE MORE"}, shot)
        just_once = targeted_ocr_region({"kind": "red-word", "text": "JUST ONCE"}, shot)
        self.assertEqual(one_more, ("red-word-1", (330, 95, 260, 70)))
        self.assertEqual(just_once, ("red-word-3", (330, 160, 260, 70)))
        self.assertNotEqual(one_more[1][1], just_once[1][1])

    def test_untracked_no_text_shot_fails_closed(self):
        from caption_coverage import resolve_text_contract
        items, status, reason = resolve_text_contract({"id": "blank-shot", "args": {"setting": "park"}}, 0, 1)
        self.assertEqual(items, [])
        self.assertEqual(status, "missing-text-contract")
        self.assertEqual(reason, "")

    def test_explicit_no_text_exemption_requires_a_reason(self):
        from caption_coverage import resolve_text_contract
        _, status_without_reason, _ = resolve_text_contract({"noTextRequired": True}, 0, 1)
        _, status_with_reason, reason = resolve_text_contract({
            "id": "visual-pause", "noTextRequired": True, "noTextReason": "Intentional silent visual hold"
        }, 0, 1)
        self.assertEqual(status_without_reason, "missing-text-contract")
        self.assertEqual(status_with_reason, "approved-no-text")
        self.assertEqual(reason, "Intentional silent visual hold")

    def test_text_must_be_readable_in_two_of_three_samples(self):
        from caption_coverage import evaluate_text_samples
        one_hit = evaluate_text_samples("Choose where it goes", [
            "Choose where it goes", "", ""
        ])
        two_hits = evaluate_text_samples("Choose where it goes", [
            "Choose where it goes", "Choose where it goes", ""
        ])
        self.assertFalse(one_hit["passed"])
        self.assertEqual(one_hit["readable_samples"], 1)
        self.assertTrue(two_hits["passed"])
        self.assertEqual(two_hits["readable_samples"], 2)

    def test_current_remotion_manifest_has_complete_text_contracts(self):
        from caption_coverage import resolve_text_contract
        repository_root = Path(__file__).resolve().parents[2]
        manifest_path = repository_root / "video-projects/remotion/public/story/shots.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        shots = manifest["shots"]
        self.assertGreater(len(shots), 0)

        counts = {}
        for index, shot in enumerate(shots):
            items, status, reason = resolve_text_contract(shot, index, len(shots))
            self.assertEqual(status, "tracked", f"{shot.get('id')}: {reason}")
            self.assertTrue(items, shot.get("id"))
            for item in items:
                counts[item["kind"]] = counts.get(item["kind"], 0) + 1

        self.assertEqual(counts.get("subtitle", 0), len(shots))
        self.assertGreater(counts.get("day-counter", 0), 0)
        self.assertGreater(counts.get("red-word", 0), 0)
        self.assertGreater(counts.get("scene-label", 0), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
