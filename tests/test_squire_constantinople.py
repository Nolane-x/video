#!/usr/bin/env python3
import importlib.util
import unittest
import tempfile
import json
import sys
from unittest.mock import patch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

mod=load_module("author_squire_constantinople",ROOT/"tools"/"video"/"author_squire_constantinople.py")
foley=load_module("import_squire_constantinople_foley",ROOT/"tools"/"video"/"import_squire_constantinople_foley.py")

class ConstantinopleAuthorTests(unittest.TestCase):
    def test_chapter_classifier(self):
        self.assertEqual(mod.progress_phase(.01,"The final assault begins"),"final")
        self.assertEqual(mod.progress_phase(.02,"At midnight, the walls are still standing"),"night")
        self.assertEqual(mod.progress_phase(.52,"Four Christian ships approach the Golden Horn"),"convoy")
        self.assertEqual(mod.progress_phase(.68,"Ships are hauled overland on rollers"),"portage")
        self.assertEqual(mod.progress_phase(.38,"The cannon fires against the wall"),"guns")
        self.assertEqual(mod.progress_phase(.40,"Repair crews carry timber and masonry"),"repair")
        self.assertEqual(mod.progress_phase(.62,"Defenders listen beneath the wall as miners dig"),"tunnel")
        self.assertEqual(mod.progress_phase(.50,"The chain across the Golden Horn blocks the harbour"),"sea")
    def test_custom_templates_are_registered_in_author(self):
        for name in ("final_night","city_panorama","wall_battery","gun_crew","repair_wall","golden_horn","relief_galleys","ship_portage","tunnel_cutaway","church_refuge","last_assault","aftermath_city"):
            self.assertIn(name,mod.CUSTOM)
    def test_story_phase_changes(self):
        self.assertEqual(mod.choose_template(.3,"Rumeli Hisarı rises",20,{},"none"),"command_camp")
        self.assertEqual(mod.choose_template(.40,"Four ships break through",42,{},"none"),"relief_galleys")
        self.assertEqual(mod.choose_template(.455,"Mehmed hauls ships overland on rollers",41,{},"none"),"ship_portage")
        self.assertEqual(mod.choose_template(.515,"The miners dig under the wall",70,{},"none"),"tunnel_cutaway")
        self.assertEqual(mod.choose_template(.64,"The miners dig under the wall",70,{},"none"),"tunnel_cutaway")

    def test_full_authoring_stays_character_led_and_avoids_long_template_runs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            project=root/"work"/"kit"/"projects"/"constantinople"
            (project/"story").mkdir(parents=True)
            (root/"work"/"kit"/"audio"/"sfx").mkdir(parents=True)
            lines=[
                "At midnight, the walls are still standing",
                "The Ottoman army approaches from the hills",
                "The city walls have protected the capital for centuries",
                "The cannon fires and stone strikes the wall",
                "Repair crews carry timber and masonry",
                "The chain across the Golden Horn blocks the harbour",
                "Four Christian ships break through the Ottoman fleet",
                "Ships are hauled overland on rollers",
                "Miners dig beneath the wall as defenders listen",
                "Families pray inside the churches",
                "The final assault begins before dawn",
                "The city falls and the people flee through the streets",
            ]
            shots=[{"id":f"s{i+1:03d}","start":i*2.0,"end":(i+1)*2.0,"line":lines[i%len(lines)]} for i in range(350)]
            (project/"story"/"shots.json").write_text(json.dumps({"duration":700,"shots":shots}),encoding="utf-8")
            with patch.object(sys,"argv",["author_squire_constantinople.py","--project",str(project)]):
                self.assertEqual(mod.main(),0)
            result=json.loads((project/"story"/"shots.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(result["hero_character"]["shot_count"],int(len(result["shots"])*.28))
            self.assertLessEqual(result["hero_character"]["shot_count"],int(len(result["shots"])*.42))
            self.assertGreaterEqual(sum(result["shot_counts"].get(x,0) for x in mod.CUSTOM),260)
            self.assertGreaterEqual(result["shot_counts"].get("relief_galleys",0),12)
            self.assertGreaterEqual(result["shot_counts"].get("ship_portage",0),8)
            self.assertGreaterEqual(result["shot_counts"].get("tunnel_cutaway",0),6)
            self.assertLessEqual(result["shot_counts"].get("city_panorama",0),int(len(result["shots"])*.15))
            self.assertFalse({"scene","close","army","split","frame"} & set(result["shot_counts"]))
            run=1; longest=1
            for prev,cur in zip(result["shots"],result["shots"][1:]):
                run=run+1 if cur["tpl"]==prev["tpl"] else 1
                longest=max(longest,run)
            self.assertLessEqual(longest,3)
            self.assertEqual(result["hero_character"]["preset"],"byzantineYou")
            self.assertIn("actor_closeup",mod.CUSTOM)
            self.assertIn("city_detail",mod.CUSTOM)
            self.assertTrue(any(s["args"].get("hero") is False for s in result["shots"] if s["tpl"] in mod.CUSTOM and s["tpl"] not in {"command_camp","gun_crew"}))
            cfg=json.loads((project/"config.json").read_text(encoding="utf-8"))
            self.assertEqual(cfg["style"],"dusk")
            self.assertTrue(cfg["captions"])
            self.assertEqual(cfg["captionStyle"],"squire")

    def test_siege_audio_source_is_real_cc0_cannon_wall_impact(self):
        root=Path("/fixtures")
        defs=foley.source_definitions(root)
        self.assertEqual(defs["siege_impact"][0],root/"battle-at-sea"/"cannon_hit_wall_no_splash.ogg")
        self.assertEqual(defs["cannon_fire"][0],root/"battle-at-sea"/"cannon_fire_1.ogg")
    def test_fletching_is_not_mislabeled_as_arrow_impact(self):
        self.assertNotIn("arrow_thunk",foley.source_definitions(Path("/fixtures")))
    def test_cannon_fire_and_wall_impact_are_synced_to_animation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"cannon_fire.wav").touch()
            (root/"siege_impact.wav").touch()
            cues=mod.sfx_for_shot("wall_battery",{"fireAt":.47},0,root)
            self.assertEqual([(c["name"],c["at"]) for c in cues],[("cannon_fire",.47),("siege_impact",1.49)])
    def test_last_assault_uses_close_combat_cues_not_cannon_wall_impact(self):
        root=Path("/fixtures/sfx")
        cues=mod.sfx_for_shot("last_assault",{},0,root)
        self.assertNotIn("siege_impact",[c["name"] for c in cues])
    def test_siege_impact_uses_actual_cc0_wall_impact_not_sword_clash_search(self):
        root=Path("/fixtures")
        defs=foley.source_definitions(root)
        self.assertEqual(defs["siege_impact"][0],root/"battle-at-sea"/"cannon_hit_wall_no_splash.ogg")
        self.assertEqual(defs["cannon_fire"][0],root/"battle-at-sea"/"cannon_fire_1.ogg")
    def test_arrow_impact_is_not_mislabeled_from_fletching_texture(self):
        defs=foley.source_definitions(Path("/fixtures"))
        self.assertNotIn("arrow_thunk",defs)
    def test_every_story_music_bed_uses_an_exact_cc0_recording(self):
        root=Path("/fixtures")
        defs=foley.source_definitions(root)
        expected={
            "bed_mystery":"esa_0.ogg",
            "bed_wonder":"Loop_The_Bards_Tale.wav",
            "bed_curious":"Exploration_0.mp3",
            "bed_tension":"war theme ver 2_0.ogg",
            "bed_war":"Eye_of_the_Storm.wav",
            "bed_emotional":"emotional_piano_2.ogg",
        }
        self.assertTrue(set(expected).issubset(defs))
        for alias,filename in expected.items():
            src,channels,creator,url,note=defs[alias]
            expected_path=root/"score"/filename if alias=="bed_war" else root/"music"/filename
            self.assertEqual(src,expected_path)
            self.assertEqual(channels,2)
            self.assertTrue(creator)
            self.assertIn("opengameart.org/content/",url)
    def test_recorded_beds_replace_procedural_files_with_unique_aliases(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);music=root/"music";sfx=root/"sfx"
            music.mkdir();sfx.mkdir()
            generated=music/"bed_mystery_Em_80bpm.wav"
            generated.touch()
            dst=foley.destination_for("bed_mystery",music,sfx)
            self.assertEqual(dst,music/"bed_mystery_recorded_cc0.wav")
            self.assertFalse(generated.exists())
            self.assertEqual(foley.destination_for("cannon_fire",music,sfx),sfx/"cannon_fire.wav")

if __name__=="__main__":unittest.main()
