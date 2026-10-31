import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_editorial_plan import evaluate_plan, requires_motion_proof

ROOT = Path(__file__).resolve().parents[2]


def valid_plan():
    return {
        "title": "A small change",
        "duration": 10,
        "fps": 24,
        "creativeBrief": {
            "audience": "Young adults building healthier digital habits",
            "platform": "YouTube",
            "language": "English",
            "aspectRatio": "16:9",
            "viewerPromise": "Show one practical way to regain attention",
            "hook": "A notification interrupts a quiet moment",
            "payoff": "The character chooses a meaningful offline action",
            "narrationPolicy": "none-by-design",
            "narrationRationale": "Dialogue-free short; clear visual actions and concise captions carry the meaning",
            "visualGrammar": "Warm hand-drawn 2D with varied staging and motivated camera movement",
            "pacingRationale": "Opening hold, faster middle actions and a quiet payoff",
            "storyArc": [
                {"name": "Setup", "purpose": "Establish the distraction"},
                {"name": "Choice", "purpose": "Show the decision and effort"},
                {"name": "Payoff", "purpose": "Demonstrate a visible change"},
            ],
        },
        "musicArc": [
            {"start": 0, "end": 4, "track": "quiet-bed"},
            {"start": 4, "end": 7, "track": "intentional-silence"},
            {"start": 7, "end": 10, "track": "resolve-bed"},
        ],
        "shots": [
            {
                "id": "s001", "start": 0, "end": 2, "tpl": "wide",
                "line": "A notification interrupts the quiet.",
                "emotion": "curiosity", "action": "The character notices a light.",
                "storyFunction": "Introduce the conflict",
                "shotLanguage": {
                    "shotSize": "wide", "cameraAngle": "eye-level",
                    "cameraMove": "slow push-in", "composition": "character right, negative space left",
                    "visualPurpose": "Establish isolation and the phone as a visual lure",
                },
                "soundCues": ["notification"], "args": {"subtitle": "A notification interrupts the quiet."},
            },
            {
                "id": "s002", "start": 2, "end": 7, "tpl": "insert",
                "line": "The phone keeps asking for attention.",
                "emotion": "temptation", "action": "A feed scrolls as messages arrive.",
                "storyFunction": "Escalate the temptation",
                "shotLanguage": {
                    "shotSize": "extreme close-up", "cameraAngle": "top-down",
                    "cameraMove": "locked", "composition": "phone centered with layered feed",
                    "visualPurpose": "Make the endless feed feel crowded",
                },
                "soundCues": ["notification", "soft pulse"], "args": {"subtitle": "The phone keeps asking for attention."},
            },
            {
                "id": "s003", "start": 7, "end": 10, "tpl": "profile",
                "line": "The character chooses to look up.",
                "emotion": "agency", "action": "The character raises their head and steps away.",
                "storyFunction": "Resolve the conflict with a visible choice",
                "shotLanguage": {
                    "shotSize": "medium", "cameraAngle": "three-quarter",
                    "cameraMove": "short lateral track", "composition": "open space revealed in front",
                    "visualPurpose": "Show agency through a change in gaze and screen direction",
                },
                "soundCues": ["footsteps"], "args": {"subtitle": "The character chooses to look up."},
            },
        ],
    }


class EditorialPlanTests(unittest.TestCase):
    def test_complete_plan_is_ready_for_blocking_not_release(self):
        report = evaluate_plan(valid_plan())
        self.assertEqual(report["status"], "PLAN_READY_FOR_RENDER", json.dumps({"severityCounts": report["severityCounts"], "findings": report["findings"]}, ensure_ascii=False))
        self.assertGreaterEqual(report["planReadinessScore"], 75)
        self.assertTrue(any("never a production release" in item for item in report["limitations"]))

    def test_missing_audience_language_and_story_payoff_blocks_plan(self):
        plan = valid_plan()
        del plan["creativeBrief"]["audience"]
        del plan["creativeBrief"]["language"]
        del plan["creativeBrief"]["payoff"]
        report = evaluate_plan(plan)
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("brief.audience", codes)
        self.assertIn("brief.language", codes)
        self.assertIn("brief.payoff", codes)

    def test_uniform_five_second_grid_without_rationale_is_flagged(self):
        plan = valid_plan()
        plan["shots"] = []
        for i in range(8):
            shot = copy.deepcopy(valid_plan()["shots"][0])
            shot["id"] = f"s{i:03d}"
            shot["start"] = i * 5
            shot["end"] = (i + 1) * 5
            plan["shots"].append(shot)
        plan["duration"] = 40
        plan["musicArc"] = [{"start": 0, "end": 40, "track": "music"}]
        del plan["creativeBrief"]["pacingRationale"]
        report = evaluate_plan(plan)
        self.assertTrue(report["metrics"]["uniformDurationGrid"])
        self.assertIn("pacing.uniform-grid", {x["code"] for x in report["findings"]})

    def test_template_dominance_requires_creative_rationale(self):
        plan = valid_plan()
        for shot in plan["shots"]:
            shot["tpl"] = "scene"
        report = evaluate_plan(plan)
        self.assertIn("visual.template-dominance", {x["code"] for x in report["findings"]})

    def test_contact_action_requires_motion_proof(self):
        plan = valid_plan()
        plan["shots"][1]["action"] = "The character punches the bag and it swings away."
        report = evaluate_plan(plan)
        self.assertIn("motion.contact-proof-missing", {x["code"] for x in report["findings"]})

    def test_no_voiceover_requires_story_rationale(self):
        plan = valid_plan()
        del plan["creativeBrief"]["narrationRationale"]
        report = evaluate_plan(plan)
        self.assertIn("audio.no-narration-rationale", {x["code"] for x in report["findings"]})

    def test_music_arc_gap_is_a_blocker(self):
        plan = valid_plan()
        plan["musicArc"] = [
            {"start": 0, "end": 3, "track": "opening"},
            {"start": 4, "end": 10, "track": "ending"},
        ]
        report = evaluate_plan(plan)
        self.assertIn("audio.music-arc-invalid", {x["code"] for x in report["findings"]})

    def test_shot_timeline_gap_is_a_hard_blocker(self):
        plan = valid_plan()
        plan["shots"][1]["start"] = 3
        plan["shots"][1]["end"] = 8
        plan["shots"][2]["start"] = 8
        report = evaluate_plan(plan)
        codes = {x["code"] for x in report["findings"]}
        self.assertIn("timeline.gap", codes)
        self.assertEqual(report["status"], "BLOCKED")

    def test_voiceover_requires_timed_audio_assets(self):
        plan = valid_plan()
        plan["creativeBrief"]["narrationPolicy"] = "voiceover"
        plan["creativeBrief"]["speechPlan"] = "Vietnamese narration, one phrase for each story beat"
        report = evaluate_plan(plan)
        self.assertIn("audio.missing-timed-narration", {x["code"] for x in report["findings"]})


    def test_remotion_renderer_uses_shot_plan_time_ranges_not_fixed_five_seconds(self):
        source = (
            ROOT / "video-projects/remotion/src/OneMoreScroll.tsx"
        ).read_text(encoding="utf-8")
        self.assertIn("startFrame: Math.round(entry.start * FPS)", source)
        self.assertIn("endFrame: Math.round(entry.end * FPS)", source)
        self.assertIn("candidate.endFrame", source)
        self.assertNotIn("SHOT_FRAMES", source)
        self.assertIn("shotSize.includes", source)
        self.assertIn("language?.cameraMove", source)
        self.assertIn("language?.cameraAngle", source)
        self.assertIn("language?.composition", source)
        self.assertIn("compositionOffset", source)
        self.assertIn("shotPlan.musicArc", source)
        self.assertIn("audioPlan?.narration", source)
        self.assertIn("plannedSoundCues", source)

    def test_revised_one_more_scroll_plan_is_ready_for_preview_not_release(self):
        path = ROOT / "video-projects/remotion/public/story/shots.json"
        plan = json.loads(path.read_text(encoding="utf-8"))
        report = evaluate_plan(plan)
        self.assertEqual(report["status"], "PLAN_READY_FOR_RENDER")
        self.assertEqual(report["severityCounts"]["P0"], 0)
        self.assertEqual(report["severityCounts"]["P1"], 0)
        self.assertEqual(report["metrics"]["shotCount"], 31)
        self.assertEqual(report["metrics"]["durationSeconds"], 155)
        self.assertFalse(report["metrics"]["uniformDurationGrid"])
        self.assertGreaterEqual(report["metrics"]["cameraLanguageCoverage"], 0.80)
        self.assertTrue(any("never a production release" in item for item in report["limitations"]))

    def test_message_state_word_open_is_not_a_physical_action(self):
        self.assertFalse(requires_motion_proof("The last message remains open on the phone; no reply appears."))

    def test_descriptive_lower_is_not_a_prop_contact_action(self):
        self.assertFalse(requires_motion_proof("Calendar sheets turn forward while the protagonist's posture drops lower."))
        self.assertTrue(requires_motion_proof("The hand lowers the phone onto the desk."))

    def test_opening_a_door_is_a_contact_action(self):
        self.assertTrue(requires_motion_proof("The protagonist opens the café door and steps inside."))


if __name__ == "__main__":
    unittest.main(verbosity=2)
