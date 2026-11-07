#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, re, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

AUTHOR=load("author_squire_ain_jalut",ROOT/"tools/video/author_squire_ain_jalut.py")
QA=load("qa_squire_ain_jalut",ROOT/"tools/video/qa_squire_ain_jalut.py")
PREP=load("prepare_squire_ain_jalut_voice_job",ROOT/"tools/video/prepare_squire_ain_jalut_voice_job.py")

class AinJalutTests(unittest.TestCase):
    def test_script_is_long_form_and_over_ten_minutes(self):
        path=ROOT/"video-projects/squire/ain-jalut-1260/01-SCRIPT.md"
        text=path.read_text(encoding="utf-8")
        text=re.sub(r"\n+\d[\d,]* words\..*$","",text,flags=re.S).strip()
        words=len(text.split())
        self.assertGreaterEqual(words,1900)
        self.assertLessEqual(words,2100)
        self.assertGreater(words/185*60,600)
        self.assertNotIn("|",text)
        self.assertIn("feigned retreat",text.casefold())
        self.assertIn("accounts",text.casefold())
        self.assertIn("Qutuz",text)
        self.assertIn("Kitbuqa",text)
        self.assertIn("Baybars",text)

    def test_voice_picker_selects_only_eligible_english_voice(self):
        rows=[
            {"id":"en-kokoro-v1-af_heart","language":"en","engine":"Kokoro-82M","watermark":"verified",
             "signal_checks":{"status":"passed"},"upstream_quality_grade":"A",
             "rights":{"commercial_use":"apache-2.0-model-and-voice-assets"}},
            {"id":"fr-kokoro-v1-test","language":"fr","engine":"Kokoro-82M","watermark":"verified",
             "signal_checks":{"status":"passed"},"upstream_quality_grade":"A",
             "rights":{"commercial_use":"apache-2.0-model-and-voice-assets"}}
        ]
        selected,_=PREP.choose_voice({"voices":rows})
        self.assertEqual(selected["id"],"en-kokoro-v1-af_heart")

    def test_director_uses_specific_templates_for_story_beats(self):
        cases=[
            ("The route from Cairo reaches Gaza and Acre.",1,.35,"map"),
            ("Hulegu withdraws with his main army east.",2,.30,"board"),
            ("The Mamluk reserve commits as the line has opened.",3,.75,"top"),
            ("Qutuz rallies the men.",4,.80,"close"),
            ("The horse archer checks his bowstring and arrows.",5,.60,"item")
        ]
        for text,index,progress,expected in cases:
            self.assertEqual(AUTHOR.choose_template(text,index,progress,{}, {},None),expected)
        self.assertEqual(AUTHOR.VALID_TEMPLATES,{"scene","close","army","top","plan","map","board","item","split","title","black"})

    def test_map_uses_levant_places_and_mamluk_visuals(self):
        with tempfile.TemporaryDirectory() as tmp:
            args,_=AUTHOR.base_args("map","The army reaches Gaza and Ayn Jalut.",1,.4,Path(tmp))
        names={p["text"] for p in args["places"]}
        self.assertIn("Cairo",names)
        self.assertIn("Ayn Jalut (approx.)",names)
        self.assertIn("Gaza",names)

    def test_mamluk_closeup_uses_turban_and_mail_shorthand(self):
        with tempfile.TemporaryDirectory() as tmp:
            args,_=AUTHOR.base_args("close","Qutuz rallies the Mamluk line.",8,.8,Path(tmp))
        self.assertEqual(args["preset"],"knight12")
        self.assertEqual(args["helmet"],"turban")
        self.assertEqual(args["body"],"mail")
        self.assertEqual(args["tunicColor"],AUTHOR.MAMLUK)

    def test_mongol_closeup_is_mounted_archer_shorthand(self):
        with tempfile.TemporaryDirectory() as tmp:
            args,_=AUTHOR.base_args("close","Kitbuqa watches the Mongol horse archers.",9,.5,Path(tmp))
        self.assertEqual(args["preset"],"englishArcher")
        self.assertEqual(args["helmet"],"cap")
        self.assertEqual(args["weapon"],"bow")
        self.assertEqual(args["tunicColor"],AUTHOR.MONGOL)

    def test_top_down_geometry_has_both_factions(self):
        with tempfile.TemporaryDirectory() as tmp:
            args,_=AUTHOR.base_args("top","The Mamluk reserve counterattacks the Mongol line.",12,.8,Path(tmp))
        sides={b["side"] for b in args["blocks"]}
        self.assertIn("blue",sides)
        self.assertIn("red",sides)
        self.assertTrue(args["arrows"])

    def test_qa_requires_more_than_ten_minutes(self):
        qa_source=(ROOT/"tools/video/qa_squire_ain_jalut.py").read_text(encoding="utf-8")
        self.assertIn("duration > 600",qa_source)
        self.assertEqual(QA.safe_title("The Day the Mongols Were Stopped: Ain Jalut"),"The Day the Mongols Were Stopped Ain Jalut")

if __name__=="__main__":
    unittest.main(verbosity=2)
