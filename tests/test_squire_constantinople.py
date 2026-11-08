#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"tools"/"video"/"author_squire_constantinople.py"
spec=importlib.util.spec_from_file_location("author_squire_constantinople",P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
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
if __name__=="__main__":unittest.main()
