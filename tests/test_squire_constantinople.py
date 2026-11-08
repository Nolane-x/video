#!/usr/bin/env python3
import importlib.util
import unittest
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
        self.assertEqual(mod.progress_phase(.52,"Four Christian ships approach the Golden Horn"),"sea")
        self.assertEqual(mod.progress_phase(.68,"Ships are hauled overland on rollers"),"portage")
        self.assertEqual(mod.progress_phase(.38,"The cannon fires against the wall"),"guns")
    def test_custom_templates_are_registered_in_author(self):
        for name in ("city_panorama","wall_battery","relief_galleys","ship_portage","last_assault","aftermath_city"):
            self.assertIn(name,mod.CUSTOM)
    def test_story_phase_changes(self):
        self.assertEqual(mod.choose_template(.3,"Rumeli Hisarı rises",20,{},"scene"),"command_camp")
        self.assertEqual(mod.choose_template(.57,"Four ships break through",42,{},"scene"),"relief_galleys")
    def test_siege_impact_uses_actual_cc0_wall_impact_not_sword_clash_search(self):
        root=Path("/fixtures")
        defs=foley.source_definitions(root)
        self.assertEqual(defs["siege_impact"][0],root/"battle-at-sea"/"cannon_hit_wall_no_splash.ogg")
        self.assertEqual(defs["cannon_fire"][0],root/"battle-at-sea"/"cannon_fire.ogg")
    def test_arrow_impact_is_not_mislabeled_from_fletching_texture(self):
        defs=foley.source_definitions(Path("/fixtures"))
        self.assertNotIn("arrow_thunk",defs)

if __name__=="__main__":unittest.main()
