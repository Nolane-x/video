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
hybrid_splice=load_module("splice_constantinople_hybrid_insert",ROOT/"tools"/"video"/"splice_constantinople_hybrid_insert.py")

class ConstantinopleAuthorTests(unittest.TestCase):
    def test_hybrid_bombard_insert_is_frame_exact_across_two_shards(self):
        self.assertEqual(hybrid_splice.START_FRAME, 52982)
        self.assertEqual(hybrid_splice.END_FRAME, 62376)
        self.assertEqual(hybrid_splice.INSERT_FRAMES, 9394)
        self.assertEqual(hybrid_splice.FIRST_SHARD_INSERT, 4492)
        self.assertEqual(hybrid_splice.SECOND_SHARD_INSERT, 4902)
        self.assertEqual(hybrid_splice.SECOND_SHARD_SUFFIX, 52572)
        self.assertEqual(hybrid_splice.FIRST_SHARD_INSERT + hybrid_splice.SECOND_SHARD_INSERT, 9394)

    def test_blender_insert_cannon_sfx_use_verified_cc0_assets_and_are_idempotent(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            kit=root/"kit"
            project=kit/"projects"/"demo"
            (project/"story").mkdir(parents=True)
            (kit/"audio"/"sfx").mkdir(parents=True)
            rows=[]
            for alias in ("cannon_fire","siege_impact"):
                path=kit/"audio"/"sfx"/f"{alias}.wav"
                path.write_bytes((alias+"-fixture").encode())
                rows.append({
                    "alias":alias,
                    "license":"CC0-1.0",
                    "source":alias+".ogg",
                    "source_url":"https://opengameart.org/content/battle-at-sea",
                    "converted_path":f"audio/sfx/{alias}.wav",
                    "converted_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                    "human_auditioned":False,
                    "approved_for_final_mix":False,
                })
            (project/"story"/"AUDIO-SOURCE-MANIFEST.json").write_text(
                json.dumps({"assets":rows}),encoding="utf-8")
            story_path=project/"story"/"shots.json"
            story_path.write_text(json.dumps({"shots":[]}),encoding="utf-8")
            result=hybrid_splice.add_insert_sound_cues(project)
            self.assertEqual([c["name"] for c in result["cues"]],["cannon_fire","siege_impact"])
            self.assertEqual([c["t"] for c in result["cues"]],[239.760,246.060])
            story=json.loads(story_path.read_text(encoding="utf-8"))
            self.assertEqual(len(story["sfx"]),2)
            hybrid_splice.add_insert_sound_cues(project)
            story=json.loads(story_path.read_text(encoding="utf-8"))
            self.assertEqual(len(story["sfx"]),2)

    def test_hybrid_caption_excerpt_clips_start_and_end_without_losing_cues(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/"source.srt"
            output=root/"excerpt.srt"
            source.write_text(
                "1\n00:03:40,000 --> 00:03:41,000\nOpening cannon crew\n\n"
                "2\n00:04:19,000 --> 00:04:21,000\nWall impact and debris\n\n"
                "3\n00:04:21,000 --> 00:04:22,000\nOutside the insert\n",
                encoding="utf-8"
            )
            count=hybrid_splice.extract_caption_excerpt(source,output)
            self.assertEqual(count,2)
            excerpt=output.read_text(encoding="utf-8")
            self.assertIn("Opening cannon crew",excerpt)
            self.assertIn("Wall impact and debris",excerpt)
            self.assertNotIn("Outside the insert",excerpt)
            self.assertIn("00:00:00,000 --> 00:00:00,242",excerpt)
            self.assertIn("00:00:39,142",excerpt)

    def test_custom_scene_function_boundaries_remain_runtime_loadable(self):
        scene = (ROOT / "video-projects" / "squire" / "constantinople-1453" /
                 "scenes" / "shots" / "constantinople-cinematic.js")
        source = scene.read_text(encoding="utf-8")
        self.assertIn("function drawNightCampDetail(g,t,info,a){", source)
        self.assertIn("function drawNightGunCrewDetail(g,t,info,a){", source)
        self.assertNotIn("function drawNightGunCrewDetail\n  const", source)

    def test_chapter_classifier(self):
        self.assertEqual(mod.progress_phase(.01,"The final assault begins"),"final")
        self.assertEqual(mod.progress_phase(.02,"At midnight, the walls are still standing"),"night")
        self.assertEqual(mod.progress_phase(.52,"Four Christian ships approach the Golden Horn"),"convoy")
        self.assertEqual(mod.progress_phase(.68,"Ships are hauled overland on rollers"),"portage")
        self.assertEqual(mod.progress_phase(.38,"The cannon fires against the wall"),"guns")
        self.assertEqual(mod.progress_phase(.35,"Repair crews carry timber and masonry"),"repair")
        self.assertEqual(mod.progress_phase(.62,"Defenders listen beneath the wall as miners dig"),"tunnel")
        self.assertEqual(mod.progress_phase(.50,"The chain across the Golden Horn blocks the harbour"),"sea")
    def test_opening_context_prioritizes_current_cue_over_future_events(self):
        cues = [
            ("the creak of carts,", "night_camp_detail"),
            ("the distant thunder of guns.", "night_guns"),
            ("Tonight, you are no longer certain.", "actor_closeup"),
            ("It will come in waves.", "assault_waves"),
            ("not be expected to survive.", "assault_first_wave"),
            ("You are not a famous commander.", "actor_closeup"),
            ("You are one defender among thousands,", "defender_identity"),
            ("To understand that night,", "rewind_map"),
        ]
        for index, (line, expected) in enumerate(cues, start=1):
            with self.subTest(line=line):
                self.assertEqual(mod.choose_template(.02, line, index, {}, None, context_text=line), expected)

    def test_opening_event_context_preserves_split_clauses(self):
        samples = [
            ([{"start":0.0,"end":1.0,"line":"At dawn, the largest assault"},
              {"start":1.0,"end":2.0,"line":"of the siege will begin."}], 1, "assault_waves"),
            ([{"start":0.0,"end":1.0,"line":"The first men may"},
              {"start":1.0,"end":2.0,"line":"not be expected to survive."}], 1, "assault_first_wave"),
            ([{"start":0.0,"end":1.0,"line":"A cannon crew is"},
              {"start":1.0,"end":2.0,"line":"preparing the next shot."}], 1, "night_gun_crew_detail"),
            ([{"start":0.0,"end":1.0,"line":"Behind them will come"},
              {"start":1.0,"end":2.0,"line":"the sultan's best troops."}], 1, "elite_reserve"),
            ([{"start":0.0,"end":1.0,"line":"carrying water, stones,"},
              {"start":1.0,"end":2.0,"line":"arrows, and messages wherever"}], 1, "defender_supply"),
        ]
        for shots, index, expected in samples:
            with self.subTest(expected=expected):
                context=mod.opening_context(shots,index)
                self.assertEqual(mod.choose_template(.02,shots[index]["line"],index,{},None,context_text=context),expected)

    def test_opening_camp_sequence_uses_distinct_cinematic_inserts(self):
        shots=[
            {"start":0.0,"end":1.0,"line":"You can hear the Ottoman camp"},
            {"start":1.0,"end":2.0,"line":"beyond the dark fields"},
            {"start":2.0,"end":3.0,"line":"fields: horses shifting,"},
            {"start":3.0,"end":4.0,"line":"men calling to one another,"},
            {"start":4.0,"end":5.0,"line":"the creak of carts,"},
        ]
        actual=[]
        details=[]
        for i,s in enumerate(shots):
            context=mod.opening_context(shots,i)
            tpl=mod.choose_template(.02,s["line"],i,{},None,context_text=context)
            actual.append(tpl)
            if tpl=="night_camp_detail":
                details.append({"tpl":tpl,"args":{"beat":mod.opening_camp_detail_beat(s["line"],i)}})
        self.assertEqual(actual,["night_camp","night_camp_detail","night_camp_detail",
                                 "night_camp_detail","night_camp_detail"])
        self.assertEqual([s["args"]["beat"] for s in details],["fires","horses","signal","carts"])
        self.assertEqual(mod.max_consecutive_visual_signature_run(details),1)

    def test_visual_signature_audit_preserves_caption_split_holds(self):
        shots=[
            {"tpl":"assault_first_wave","args":{"beat":"first_rush"}},
            {"tpl":"assault_first_wave","args":{"beat":"first_rush"}},
            {"tpl":"assault_second_wave","args":{"beat":"climb"}},
            {"tpl":"assault_second_wave","args":{"beat":"push"}},
        ]
        self.assertEqual(mod.max_consecutive_visual_signature_run(shots),2)

    def test_opening_final_night_uses_event_specific_scenes(self):
        cases = [
            ("At midnight, the walls are still standing.", "night", "final_night"),
            ("You can hear the Ottoman camp beyond the dark fields.", "night_camp", "night_camp"),
            ("The distant thunder of guns.", "night_guns", "night_guns"),
            ("A cannon crew is preparing the next shot.", "night_gun_crew", "night_gun_crew_detail"),
            ("At dawn, the largest assault of the siege will begin.", "final", "assault_waves"),
            ("The first men may not be expected to survive.", "final", "assault_first_wave"),
            ("The sultan's best troops.", "final", "elite_reserve"),
            ("carrying water, stones, arrows, and messages.", "defender_supply", "defender_supply"),
        ]
        for index, (line, expected_phase, expected_template) in enumerate(cases, start=1):
            with self.subTest(line=line):
                self.assertEqual(mod.choose_template(.02, line, index, {}, None, context_text=line), expected_template)

    def test_custom_templates_are_registered_in_author(self):
        for name in (
            "final_night","night_wall_watch","night_camp","night_camp_detail",
            "night_guns","night_gun_crew","night_gun_crew_detail",
            "assault_waves","assault_first_wave","assault_second_wave","elite_reserve",
            "artillery_haul","defender_identity","defender_supply","rewind_map",
            "city_panorama","wall_battery","gun_crew","repair_wall","golden_horn","relief_galleys",
            "ship_portage","tunnel_cutaway","church_refuge","last_assault","aftermath_city"
        ):
            self.assertIn(name,mod.CUSTOM)
    def test_first_day_encampment_and_artillery_train_are_not_misclassified(self):
        cases = [
            ("Tents spread across the land.", "camp", "command_camp"),
            ("Standards move in the wind.", "camp", "command_camp"),
            ("Engineers measure the ground.", "camp", "command_camp"),
            ("The road to the city is filling with an army assembled for one purpose.", "camp", "command_camp"),
            ("Oxen pull heavy guns into position.", "artillery_haul", "artillery_haul"),
            ("The artillery train drags the gun carriage into position.", "artillery_haul", "artillery_haul"),
        ]
        for index, (line, phase, template) in enumerate(cases, start=1):
            with self.subTest(line=line):
                self.assertEqual(mod.progress_phase(.072, line), phase)
                self.assertEqual(mod.choose_template(.072, line, index, {}, None), template)

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
