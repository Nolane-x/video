#!/usr/bin/env python3
"""Fast offline regression tests for source rights gates and generated asset families."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_asset_library as library  # noqa: E402


class RightsGateTests(unittest.TestCase):
    def test_smithsonian_requires_cc0_for_record_and_exact_media(self):
        self.assertTrue(library.smithsonian_rights_are_cc0("CC0", "CC0"))
        self.assertTrue(library.smithsonian_rights_are_cc0(" cc0 ", " CC0 "))
        self.assertFalse(library.smithsonian_rights_are_cc0("CC0", "Usage conditions apply"))
        self.assertFalse(library.smithsonian_rights_are_cc0("Usage conditions apply", "CC0"))
        self.assertFalse(library.smithsonian_rights_are_cc0(None, "CC0"))
        self.assertFalse(library.smithsonian_rights_are_cc0("CC0", None))

    def test_rijksmuseum_resolver_rejects_nonofficial_hosts_without_network_access(self):
        self.assertEqual(library.resolve_rijksmuseum_iiif("https://example.com/123"), "")
        self.assertEqual(library.resolve_rijksmuseum_iiif("https://data.rijksmuseum.nl/123"), "")

    def test_rijksmuseum_only_accepts_explicit_cc0_or_public_domain_mark(self):
        self.assertEqual(
            library.rijksmuseum_license_from_rights(
                "https://creativecommons.org/publicdomain/zero/1.0/"
            ),
            "CC0-1.0",
        )
        self.assertEqual(
            library.rijksmuseum_license_from_rights(
                "https://creativecommons.org/publicdomain/mark/1.0/"
            ),
            "Public Domain Mark 1.0",
        )
        self.assertIsNone(
            library.rijksmuseum_license_from_rights(
                "https://creativecommons.org/licenses/by/4.0/"
            )
        )
        self.assertIsNone(library.rijksmuseum_license_from_rights(""))
        self.assertIsNone(library.rijksmuseum_license_from_rights("rights unknown"))

    def test_library_of_congress_requires_positive_nonconflicting_statement(self):
        good, statement = library.loc_rights_are_eligible(
            "No known restrictions on publication."
        )
        self.assertTrue(good)
        self.assertIn("No known", statement)
        self.assertTrue(library.loc_rights_are_eligible("Public Domain")[0])
        self.assertTrue(
            library.loc_rights_are_eligible(
                {"Rights Information": "No known copyright restrictions"}
            )[0]
        )
        self.assertFalse(library.loc_rights_are_eligible("Copyrighted")[0])
        self.assertFalse(
            library.loc_rights_are_eligible(
                "Public Domain; possible restrictions may apply"
            )[0]
        )
        self.assertFalse(library.loc_rights_are_eligible(None)[0])

    def test_svg_sanitizer_removes_active_content_and_remote_refs(self):
        raw = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script><rect onclick="alert(2)" fill="red"/><image href="https://evil.example/pixel.png"/></svg>'
        cleaned = library.sanitize_cc0_svg(raw)
        lowered = cleaned.lower()
        self.assertIn(b"svg", lowered)
        self.assertNotIn(b"<script", lowered)
        self.assertNotIn(b"onclick", lowered)
        self.assertNotIn(b"evil.example", lowered)
        with self.assertRaises(RuntimeError):
            library.sanitize_cc0_svg(b'<!DOCTYPE svg [<!ENTITY x "bad">]><svg>&x;</svg>')

    def test_wikimedia_media_accepts_only_explicit_cc0_or_public_domain_labels(self):
        self.assertTrue(library.wikimedia_license_is_eligible("CC0"))
        self.assertTrue(library.wikimedia_license_is_eligible("CC0-1.0"))
        self.assertTrue(library.wikimedia_license_is_eligible("Public domain"))
        self.assertTrue(library.wikimedia_license_is_eligible("Public domain (United States)"))
        self.assertTrue(library.wikimedia_license_is_eligible("Public Domain Mark"))
        self.assertFalse(library.wikimedia_license_is_eligible("CC BY 4.0"))
        self.assertFalse(library.wikimedia_license_is_eligible("CC BY-SA 4.0"))
        self.assertFalse(library.wikimedia_license_is_eligible("CC BY-NC"))
        self.assertFalse(library.wikimedia_license_is_eligible("rights unclear"))
        self.assertFalse(library.wikimedia_license_is_eligible(None))

    def test_nasa_screen_accepts_known_center_and_skips_explicit_restrictions(self):
        ok, _ = library.nasa_item_is_eligible(
            {"center": "JPL", "title": "Mars surface landscape", "keywords": ["Mars", "rover"]}
        )
        self.assertTrue(ok)
        ok, _ = library.nasa_item_is_eligible(
            {"center": "NASA Goddard", "title": "Galaxy", "keywords": ["astronomy"]}
        )
        self.assertTrue(ok)
        self.assertFalse(
            library.nasa_item_is_eligible(
                {"center": "NASA", "title": "Copyrighted third-party photograph"}
            )[0]
        )
        self.assertFalse(
            library.nasa_item_is_eligible(
                {"center": "NASA", "title": "A mission", "keywords": ["crew portrait"]}
            )[0]
        )
        self.assertFalse(
            library.nasa_item_is_eligible({"center": "Unknown", "title": "Landscape"})[0]
        )


class GeneratedAssetFamilyTests(unittest.TestCase):
    def test_asset_families_have_enough_unique_ids(self):
        self.assertGreaterEqual(len(library.PALETTES), 90)
        self.assertGreaterEqual(len(library.OVERLAYS), 75)
        self.assertGreaterEqual(len(library.ICONS), 110)
        self.assertGreaterEqual(len(library.TEXTURES), 55)
        self.assertGreaterEqual(len(library.ILLUSTRATIONS), 105)
        self.assertGreaterEqual(len(library.INFO), 50)

        for entries, family in [
            ([x[0] for x in library.PALETTES], "palettes"),
            ([x[0] for x in library.OVERLAYS], "overlays"),
            ([x[0] for x in library.TEXTURES], "textures"),
            ([x[0] for x in library.ILLUSTRATIONS], "illustrations"),
            ([x[0] for x in library.INFO], "infographics"),
        ]:
            with self.subTest(family=family):
                self.assertEqual(len(entries), len(set(entries)))

    def test_original_motion_loops_have_unique_ids_and_valid_filter_chains(self):
        self.assertEqual(len(library.MOTION_LOOPS), 24)
        ids = [row[0] for row in library.MOTION_LOOPS]
        self.assertEqual(len(ids), len(set(ids)))
        styles = [row[4] for row in library.MOTION_LOOPS]
        self.assertEqual(len(styles), len(set(styles)))
        for style in styles:
            with self.subTest(style=style):
                chain = library.motion_loop_filters(style)
                self.assertTrue(chain)
                self.assertIn("drawbox=", chain)
                self.assertNotIn("http://", chain)

    def test_illustrations_reference_existing_original_icons(self):
        missing = [row[3] for row in library.ILLUSTRATIONS if row[3] not in library.ICONS]
        self.assertEqual(missing, [])

    def test_generated_vector_texture_and_illustration_are_self_contained_svg(self):
        texture_id, texture_title = library.TEXTURES[0]
        texture = library.make_texture_svg(texture_id, texture_title, 0)
        self.assertIn("<svg ", texture)
        self.assertIn('width="1024"', texture)
        self.assertNotIn("http://www.w3.org/1999/xlink", texture)

        illustration_id, title, category, icon_id = library.ILLUSTRATIONS[0]
        illustration = library.make_illustration_svg(
            illustration_id, title, category, icon_id, 0
        )
        self.assertIn("<svg ", illustration)
        self.assertIn(title.upper(), illustration)
        self.assertIn("viewBox=", illustration)


    def test_original_sound_bank_is_large_unique_and_categorized(self):
        import generate_sfx_library
        ids = [row[0] for row in generate_sfx_library.SFX_PRESETS]
        self.assertGreaterEqual(len(ids), 175)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row[1] and row[2] > 0 for row in generate_sfx_library.SFX_PRESETS))

    def test_overlay_and_icon_ids_are_unique_and_illustrations_resolve(self):
        overlay_ids = [row[0] for row in library.OVERLAYS]
        icon_ids = list(library.ICONS)
        self.assertGreaterEqual(len(overlay_ids), 75)
        self.assertEqual(len(overlay_ids), len(set(overlay_ids)))
        self.assertEqual(len(icon_ids), len(set(icon_ids)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
