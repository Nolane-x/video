import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "video"))
from validate_illustrated_history_shot_plan import validate_plan


def good_shot(shot_id="shot-01"):
    return {
        "shot_id": shot_id,
        "start_frame": 0,
        "end_frame": 72,
        "story_purpose": "Show the first clash and establish the opposing lines.",
        "location": "Cannae river plain",
        "scale": "medium_wide",
        "angle": "low",
        "composition_key": "frontline-clash-a",
        "template_id": "combat-rig-a",
        "motion_led": True,
        "motion_channels": ["actor", "prop", "camera"],
        "visual_state_change": "The shield rises, the sword strikes, and the front rank recoils.",
        "camera": {"move": "track", "motivation": "Track with the shield advance to reveal the contact."},
        "action_type": "impact",
        "action_phases": ["anticipation", "action", "contact", "reaction", "follow_through", "recovery"],
        "characters": [{"character_id": "roman-01", "role": "frontline infantry", "blocking": "advances left to right"}],
        "props": [{"prop_id": "shield-01", "state": "raised", "contact_frame": 42, "reaction": "recoils at impact"}],
        "environment_layers": [{"layer_id": "dust-bg", "depth": "background", "motion": "dust drifts right"}],
        "audio_cues": [{
            "cue_id": "shield-hit-01", "track": "prop_foley", "sync_event": "shield_contact",
            "asset_id": "meta-audio-01", "license": "CC-BY-4.0",
            "rights_class": "cc_by_4_attribution_required", "audition_status": "not_auditioned",
            "approved_for_final_mix": False
        }]
    }


class IllustratedHistoryShotPlanTests(unittest.TestCase):
    def test_motion_led_shot_with_two_channels_passes(self):
        plan = {
            "schema_version": "1.0.0",
            "project": {"project_id": "cannae-sample", "fps": 24, "style": "illustrated_history"},
            "shots": [good_shot()]
        }
        result = validate_plan(plan)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["summary"]["motion_channels_used"], ["actor", "camera", "prop"])

    def test_motion_led_shot_with_one_channel_fails(self):
        shot = good_shot()
        shot["motion_channels"] = ["camera"]
        plan = {"schema_version": "1.0.0", "project": {"project_id": "x", "fps": 24, "style": "illustrated_history"}, "shots": [shot]}
        result = validate_plan(plan)
        self.assertTrue(any("at least two independent channels" in error for error in result["errors"]))

    def test_unauditioned_audio_cannot_be_final_approved(self):
        shot = good_shot()
        shot["audio_cues"][0]["approved_for_final_mix"] = True
        plan = {"schema_version": "1.0.0", "project": {"project_id": "x", "fps": 24, "style": "illustrated_history"}, "shots": [shot]}
        result = validate_plan(plan)
        self.assertTrue(any("unauditioned cue cannot be approved" in error for error in result["errors"]))

    def test_physical_action_requires_causal_phases(self):
        shot = good_shot()
        shot["action_phases"] = ["action", "contact"]
        plan = {"schema_version": "1.0.0", "project": {"project_id": "x", "fps": 24, "style": "illustrated_history"}, "shots": [shot]}
        result = validate_plan(plan)
        self.assertTrue(any("missing phases" in error for error in result["errors"]))

    def test_three_consecutive_same_compositions_fail(self):
        shots = []
        for i in range(3):
            shot = good_shot(f"shot-{i}")
            shot["composition_key"] = "same-crowd-row"
            shots.append(shot)
        plan = {"schema_version": "1.0.0", "project": {"project_id": "x", "fps": 24, "style": "illustrated_history"}, "shots": shots}
        result = validate_plan(plan)
        self.assertTrue(any("repeats three or more shots consecutively" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
