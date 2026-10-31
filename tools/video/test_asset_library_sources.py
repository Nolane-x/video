#!/usr/bin/env python3
"""Fast offline regression tests for source rights gates and generated asset families."""
from __future__ import annotations

import io
import sys
import tempfile
import tarfile
import unittest
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from unittest import mock
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_asset_library as library  # noqa: E402
import generate_sticker_meme_library as sticker_meme  # noqa: E402
import package_asset_bundles as bundle_packager  # noqa: E402
import build_asset_library_shard as shard_builder  # noqa: E402
import finalize_asset_library_release as release_finalizer  # noqa: E402
import build_cumulative_asset_library_index as cumulative_index  # noqa: E402
import probe_nara_bulk_dataset as nara_probe  # noqa: E402
import probe_nasa_svs as nasa_svs_probe  # noqa: E402
import nasa_svs_importer as nasa_svs_importer  # noqa: E402
import generate_sfx_library as sfx_library  # noqa: E402
import json
import hashlib



class KenneyGodotSplashScreenCC0Tests(unittest.TestCase):
    def _readme(self):
        return (
            "# Godot SplashScreens\n"
            "1. The original Godot logo is made by Andrea Calabro and is CC-BY-4.0 licensed.\n"
            "2. Other derivative logos (reimagined logo, cog logo, text logo) featured in this pack "
            "are made by Kenney and are CC0 licensed.\n"
        )

    def test_official_github_archive_root_names_are_recognized(self):
        self.assertTrue(library.kenney_godot_splash_archive_root_is_allowed("KenneyNL-Godot-SplashScreens-deadbeef"))
        self.assertTrue(library.kenney_godot_splash_archive_root_is_allowed("Godot-SplashScreens-main"))
        self.assertFalse(library.kenney_godot_splash_archive_root_is_allowed("attacker-Godot-SplashScreens-main"))

    def test_scope_requires_explicit_mixed_license_readme(self):
        self.assertTrue(library.kenney_godot_splash_readme_confirms_cc0(self._readme()))
        self.assertFalse(library.kenney_godot_splash_readme_confirms_cc0(
            "The images are CC0 licensed, but no folder-specific license statement is available."
        ))
        self.assertFalse(library.kenney_godot_splash_readme_confirms_cc0(
            self._readme().replace("CC0 licensed", "CC-BY licensed")
        ))

    def test_allowlist_includes_only_explicit_kenney_cc0_subpaths(self):
        allowed = [
            "Logo/reimagined-horizontal-dark.svg",
            "Logo/text-dark.svg",
            "Screen/Cog logo/cog-blue.png",
            "Screen/Reimagined logo/blue-gradient.png",
            "Screen/Text logo/text-light.png",
        ]
        denied = [
            "Logo/original-horizontal-dark.svg",
            "Logo/Pixel/original-large.png",
            "Screen/Original logo/icon-dark.png",
            "Screen/Pixel logo/reimagined-large.png",
            "Screen/Pride logo/pride-light-a.png",
            "../Screen/Reimagined logo/escape.png",
            "/Screen/Cog logo/absolute.png",
            "Screen/Cog logo/unsafe.exe",
            "Screen/Cog logo/animation.gif",
        ]
        for path in allowed:
            self.assertTrue(library.kenney_godot_splash_path_is_allowed(path), path)
        for path in denied:
            self.assertFalse(library.kenney_godot_splash_path_is_allowed(path), path)

    def test_download_imports_only_cc0_paths_from_mixed_license_repository(self):
        import io
        buffer = io.BytesIO()
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><rect width="8" height="8"/></svg>'
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 24
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/README.md", self._readme())
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Logo/reimagined-horizontal-dark.svg", svg)
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Screen/Cog logo/cog-blue.png", png)
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Screen/Original logo/icon-dark.png", png)
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Screen/Pixel logo/reimagined-large.png", png)
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Screen/Pride logo/pride-light-a.png", png)
            archive.writestr("KenneyNL-Godot-SplashScreens-deadbeef/Logo/original-horizontal-dark.svg", svg)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = []
            with mock.patch.object(
                library,
                "request_bytes",
                return_value=(
                    buffer.getvalue(),
                    "application/zip",
                ),
            ):
                report = library.download_kenney_godot_splashscreens(root, index)
            self.assertEqual(len(report), 1)
            self.assertEqual(report[0]["status"], "downloaded")
            self.assertEqual(report[0]["file_count"], 2)
            self.assertEqual(len(index), 2)
            svg_asset = next(asset for asset in index if asset["path"].endswith(".svg"))
            sanitized_svg = (root / svg_asset["path"]).read_bytes()
            import xml.etree.ElementTree as ET
            svg_root = ET.fromstring(sanitized_svg)
            self.assertEqual(svg_root.tag.rsplit("}", 1)[-1].lower(), "svg")
            paths = {asset["path"] for asset in index}
            self.assertIn("third-party/kenney/godot-splashscreens/Logo/reimagined-horizontal-dark.svg", paths)
            self.assertIn("third-party/kenney/godot-splashscreens/Screen/Cog logo/cog-blue.png", paths)
            self.assertFalse(any(
                "Original logo" in path or "Pixel logo" in path or "Pride logo" in path
                for path in paths
            ))
            for asset in index:
                self.assertEqual(asset["license"], "CC0-1.0")
                self.assertTrue(asset["license_verified_from_repository_readme"])
                self.assertTrue(asset["redistributable"])
                asset_path = root / asset["path"]
                self.assertTrue(asset_path.is_file())
                self.assertEqual(asset["sha256"], library.sha256_path(asset_path))
            self.assertTrue((root / "third-party/kenney/godot-splashscreens/SOURCE_AND_LICENSE.md").is_file())


class ExternalSourceExpansionTests(unittest.TestCase):
    def test_external_source_ceilings_remain_expanded(self):
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["hdris"], 120)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["models"], 180)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["textures"], 480)
        self.assertGreaterEqual(library.MAX_POLY_FILE, 60 * 1024 * 1024)
        self.assertGreaterEqual(library.MAX_MEDIA_FILE, 12 * 1024 * 1024)
        self.assertGreaterEqual(library.MET_OPEN_ACCESS_IMAGE_CAP, 300)
        self.assertGreaterEqual(library.RIJKSMUSEUM_OPEN_ACCESS_IMAGE_CAP, 360)
        self.assertGreaterEqual(library.WIKIMEDIA_PUBLIC_DOMAIN_IMAGE_CAP, 1600)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_SVG_CAP, 200)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_AUDIO_VIDEO_CAP, 200)
        self.assertLessEqual(library.WIKIMEDIA_PUBLIC_DOMAIN_TOTAL_MAX_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertGreaterEqual(library.WIKIMEDIA_PUBLIC_DOMAIN_MAX_IMAGE_BYTES, 24 * 1024 * 1024)
        self.assertEqual(sum(library.AMBIENTCG_SELECTION_CAPS.values()), 792)
        self.assertEqual(set(library.AMBIENTCG_SELECTION_CAPS), {"Material", "HDRI", "3DModel", "Decal", "Atlas", "PlainTexture", "Brush", "Substance"})
        self.assertGreaterEqual(library.AMBIENTCG_MAX_ARCHIVE_BYTES, 50 * 1024 * 1024)
        self.assertGreaterEqual(library.AMBIENTCG_MAX_TOTAL_UNPACKED_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertEqual(library.LAZYTEXTURES_ASSET_CAPS, {"models": 10, "materials": 16, "hdris": 10, "textures": 18, "other": 8})
        self.assertEqual(library.LAZYTEXTURES_API_TYPES["other"]["endpoint"], "previewsOther")
        self.assertEqual(library.POLY_PIZZA_MAX_MODELS, 48)
        self.assertEqual(library.POLY_PIZZA_MAX_PAGES_PER_TERM, 2)
        self.assertEqual(library.POLY_PIZZA_MAX_MODEL_BYTES, 128 * 1024 * 1024)
        self.assertEqual(library.POLY_PIZZA_TOTAL_MAX_BYTES, 4 * 1024 * 1024 * 1024)
        self.assertEqual(library.POLY_PIZZA_API_BASE, "https://api.poly.pizza/v1.1")
        self.assertEqual(library.KENNEY_GODOT_SPLASHSCREEN_MAX_FILES, 40)
        self.assertEqual(library.KENNEY_GODOT_SPLASHSCREEN_ALLOWED_EXTS, {".png", ".svg"})
        self.assertEqual(library.LAZYTEXTURES_MAX_ZIP_MEMBERS, 2500)
        self.assertEqual(library.LAZYTEXTURES_MAX_ARCHIVE_BYTES, 64 * 1024 * 1024)
        self.assertEqual(library.LAZYTEXTURES_MAX_TOTAL_ARCHIVE_BYTES, 512 * 1024 * 1024)
        self.assertGreaterEqual(library.LAZYTEXTURES_MAX_TOTAL_UNPACKED_BYTES, 1024 * 1024 * 1024)
        self.assertEqual(library.USGS_GALLERY_PAGE_SCAN_LIMIT, 32)
        self.assertEqual(library.USGS_SELECTION_CAPS, {"images": 120, "videos": 64, "audio": 40})
        self.assertGreaterEqual(library.USGS_TOTAL_MAX_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertEqual(library.OPENGAMEART_SELECTION_CAPS, {"2d": 60, "3d": 60, "textures": 48, "sfx": 36, "music": 36})
        self.assertEqual(library.OPENGAMEART_SEARCH_PAGES_PER_TYPE, 10)
        self.assertEqual(library.OPENGAMEART_MAX_ITEM_PAGES_PER_TYPE, 120)
        self.assertGreaterEqual(library.OPENGAMEART_MAX_TOTAL_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertEqual(library.NOAA_MEDIA_PAGE_SCAN_LIMIT, 40)
        self.assertEqual(library.NOAA_MEDIA_SELECTION_CAPS, {"image": 300, "video": 180})
        self.assertEqual(library.OPENMOJI_VERSION, "17.0.0")
        self.assertEqual(library.OPENMOJI_EXPECTED_FILE_COUNT, 11539)
        self.assertGreaterEqual(library.OPENMOJI_MAX_ARCHIVE_BYTES, 80 * 1024 * 1024)
        self.assertGreaterEqual(library.OPENMOJI_MAX_EXTRACTED_BYTES, 100 * 1024 * 1024)
        self.assertGreaterEqual(library.NOAA_TOTAL_MAX_BYTES, 9 * 1024 * 1024 * 1024)
        self.assertGreaterEqual(library.NASA_IMAGE_MAX_BYTES, 48 * 1024 * 1024)
        self.assertGreaterEqual(library.NASA_VIDEO_MAX_BYTES, 250 * 1024 * 1024)
        self.assertGreaterEqual(library.NASA_AUDIO_MAX_BYTES, 48 * 1024 * 1024)
        self.assertLessEqual(library.NASA_TOTAL_MAX_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertGreaterEqual(library.SMITHSONIAN_MAX_RETRIES, 1)
        self.assertGreaterEqual(library.INTERNET_ARCHIVE_TOTAL_MAX_BYTES, 8 * 1024 * 1024 * 1024)
        self.assertEqual(library.INTERNET_ARCHIVE_SEARCH_PAGES, 5)
        self.assertGreaterEqual(library.INTERNET_ARCHIVE_MAX_ITEM_PAGES_PER_COLLECTION, 220)
        self.assertEqual(library.INTERNET_ARCHIVE_COLLECTION_CAPS, {"prelinger": 120, "nasa": 120})

    def test_nara_bulk_catalog_is_research_only_until_item_rights_schema_is_verified(self):
        catalog = json.loads(library.SOURCES_PATH.read_text(encoding="utf-8"))
        nara = next(
            row for row in catalog["sources"]
            if row.get("id") == "nara-national-archives-catalog-aws-open-data"
        )
        self.assertIn("research-only", nara["bundling"])
        self.assertIn("Unrestricted", nara["note"])
        self.assertNotIn("nara", shard_builder.SOURCE_LANES)

    def test_poly_pizza_source_catalog_requires_optional_key_and_item_level_cc0(self):
        catalog = json.loads(library.SOURCES_PATH.read_text(encoding="utf-8"))
        entry = next(row for row in catalog["sources"] if row.get("id") == "poly-pizza-cc0-api")
        self.assertIn("per-model-cc0", entry["bundling"])
        self.assertIn("POLY_PIZZA_API_KEY", entry["authentication"])
        self.assertIn("optional", entry["authentication"].lower())
        self.assertEqual(entry["api"], "https://api.poly.pizza/v1.1")
        self.assertFalse(entry["verified_page_license"])
        self.assertIn("CC0 1.0 only", entry["license"])
        self.assertEqual(entry["license_url"], "https://creativecommons.org/publicdomain/zero/1.0/")

    def test_quaternius_current_qal_is_catalogued_source_only(self):
        catalog = json.loads(library.SOURCES_PATH.read_text(encoding="utf-8"))
        entry = next(
            row for row in catalog["sources"]
            if row.get("id") == "quaternius-current-qal-source-only"
        )
        self.assertIn("QAL", entry["license"])
        self.assertIn("v1.0", entry["license"])
        self.assertIn("source-only", entry["bundling"])
        self.assertIn("redistributing the assets themselves", entry["note"])
        self.assertEqual(entry["license_url"], "https://quaternius.com/license.html")

    def test_ambientcg_download_url_rejects_untrusted_hosts_and_paths(self):
        self.assertTrue(library.ambientcg_download_url_is_allowed("https://ambientcg.com/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("http://ambientcg.com/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://ambientcg.com.evil.example/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://example.com/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://ambientcg.com/api/v2/full_json?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://ambientcg.com/get?file=../payload.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://ambientcg.com:8443/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://user@ambientcg.com/get?file=Wood096_1K-JPG.zip"))
        self.assertFalse(library.ambientcg_download_url_is_allowed("https://ambientcg.com/get?file=Wood096_1K-JPG.zip#fragment"))

    def test_ambientcg_download_picker_prefers_small_official_zip(self):
        # Fixture mirrors the live official v2 full_json schema: filetype, fileName,
        # downloadLink, size and attribute inside downloadFolders/default/.../downloads.
        asset = {"assetId": "Wood096", "tags": ["wood", "pbr"], "downloadFolders": {"default": {"downloadFiletypeCategories": {"zip": {"downloads": [
            {"attribute": "2K-JPG", "filetype": "zip", "fileName": "Wood096_2K-JPG.zip", "size": 8_000_000, "downloadLink": "https://ambientcg.com/get?file=Wood096_2K-JPG.zip"},
            {"attribute": "1K-JPG", "filetype": "zip", "fileName": "Wood096_1K-JPG.zip", "size": 2_000_000, "downloadLink": "https://ambientcg.com/get?file=Wood096_1K-JPG.zip"},
            {"attribute": "1K-JPG", "filetype": "zip", "fileName": "Other_1K-JPG.zip", "size": 1_000_000, "downloadLink": "https://evil.example/get?file=Other_1K-JPG.zip"}
        ]}}}}}
        choice = library.ambientcg_choose_download(asset)
        self.assertEqual(choice["attribute"], "1K-JPG")
        self.assertTrue(library.ambientcg_download_url_is_allowed(choice["url"]))
        self.assertEqual(len(library.ambientcg_download_candidates(asset)), 2)

    def test_ambientcg_api_response_handles_documented_asset_lists(self):
        self.assertEqual(library.ambientcg_response_assets({"foundAssets": [{"assetId": "Wood096"}]}), [{"assetId": "Wood096"}])
        self.assertEqual(library.ambientcg_response_assets({"assets": [{"id": "Concrete001"}]}), [{"id": "Concrete001"}])
        self.assertEqual(library.ambientcg_response_assets({"other": []}), [])


class PolyPizzaCC0APITests(unittest.TestCase):
    def _model(self):
        return {
            "ID": "TreeOne",
            "Title": "Low Poly Tree",
            "Creator": {"Username": "ExampleArtist", "PURL": "https://poly.pizza/u/ExampleArtist"},
            "Licence": "CC0 1.0",
            "URL": "https://poly.pizza/m/TreeOne",
            "Download": "https://cdn.poly.pizza/models/TreeOne.glb",
            "Tags": ["tree", "nature"],
            "Tri Count": 1200,
        }

    def test_api_and_asset_url_allowlists_are_https_and_host_pinned(self):
        self.assertTrue(library.poly_pizza_api_url_is_allowed("https://api.poly.pizza/v1.1/search/tree"))
        self.assertFalse(library.poly_pizza_api_url_is_allowed("https://api.poly.pizza.evil.example/v1.1/search/tree"))
        self.assertFalse(library.poly_pizza_api_url_is_allowed("http://api.poly.pizza/v1.1/search/tree"))
        self.assertTrue(library.poly_pizza_asset_url_is_allowed("https://cdn.poly.pizza/models/tree.glb"))
        self.assertTrue(library.poly_pizza_asset_url_is_allowed("https://poly.pizza/m/TreeOne"))
        self.assertTrue(library.poly_pizza_download_url_is_allowed("https://cdn.poly.pizza/models/tree.glb"))
        self.assertFalse(library.poly_pizza_download_url_is_allowed("https://cdn.poly.pizza/models/tree.zip"))
        self.assertFalse(library.poly_pizza_download_url_is_allowed("https://evil.example/models/tree.glb"))
        self.assertFalse(library.poly_pizza_asset_url_is_allowed("https://evil.example/models/tree.glb"))
        self.assertFalse(library.poly_pizza_asset_url_is_allowed("http://cdn.poly.pizza/models/tree.glb"))
        self.assertFalse(library.poly_pizza_asset_url_is_allowed("https://user@cdn.poly.pizza/models/tree.glb"))

    def test_model_parser_accepts_exact_cc0_and_fails_closed_on_other_licenses(self):
        parsed, reason = library.poly_pizza_parse_model(self._model(), require_download=True)
        self.assertIsNone(reason)
        self.assertEqual(parsed["license"], "CC0-1.0")
        self.assertEqual(parsed["model_id"], "TreeOne")
        self.assertEqual(parsed["creator"], "ExampleArtist")
        self.assertTrue(parsed["source_page"].startswith("https://poly.pizza/m/"))
        self.assertEqual(parsed["download_url"], "https://cdn.poly.pizza/models/TreeOne.glb")

        numeric_cc0 = self._model()
        numeric_cc0["Licence"] = 1
        self.assertEqual(library.poly_pizza_parse_model(numeric_cc0)[0]["license"], "CC0-1.0")
        nested_cc0 = self._model()
        nested_cc0["Licence"] = {"ID": 1, "Name": "CC0"}
        self.assertEqual(library.poly_pizza_parse_model(nested_cc0)[0]["license"], "CC0-1.0")
        numeric_by = self._model()
        numeric_by["Licence"] = 0
        self.assertEqual(library.poly_pizza_parse_model(numeric_by)[1], "license_not_cc0_or_unrecognized")

        by_model = self._model()
        by_model["Licence"] = "CC-BY 4.0"
        self.assertEqual(library.poly_pizza_parse_model(by_model)[1], "license_not_cc0_or_unrecognized")
        unknown = self._model()
        unknown.pop("Licence")
        self.assertEqual(library.poly_pizza_parse_model(unknown)[1], "license_not_cc0_or_unrecognized")
        hostile = self._model()
        hostile["Download"] = "https://evil.example/tree.glb"
        self.assertEqual(library.poly_pizza_parse_model(hostile, require_download=True)[1], "download_url_not_official_glb")
        wrong_extension = self._model()
        wrong_extension["Download"] = "https://cdn.poly.pizza/tree.zip"
        self.assertEqual(library.poly_pizza_parse_model(wrong_extension, require_download=True)[1], "download_url_not_official_glb")
        wrong_source = self._model()
        wrong_source["URL"] = "https://poly.pizza/m/AnotherModel"
        self.assertEqual(library.poly_pizza_parse_model(wrong_source)[1], "source_url_not_official")

    def test_glb_validator_checks_magic_version_json_chunk_and_declared_length(self):
        payload = json.dumps({"asset": {"version": "2.0"}}).encode("utf-8")
        payload += b" " * ((4 - len(payload) % 4) % 4)
        total = 12 + 8 + len(payload)
        valid = b"glTF" + (2).to_bytes(4, "little") + total.to_bytes(4, "little") + len(payload).to_bytes(4, "little") + b"JSON" + payload
        self.assertTrue(library.poly_pizza_glb_is_valid(valid))
        bin_data = b"1234"
        bin_chunk = len(bin_data).to_bytes(4, "little") + b"BIN\x00" + bin_data
        with_bin = b"glTF" + (2).to_bytes(4, "little") + (len(valid) + len(bin_chunk)).to_bytes(4, "little") + valid[12:] + bin_chunk
        self.assertTrue(library.poly_pizza_glb_is_valid(with_bin))
        self.assertFalse(library.poly_pizza_glb_is_valid(b"<html>blocked</html>"))
        self.assertFalse(library.poly_pizza_glb_is_valid(b"glTF" + (1).to_bytes(4, "little") + total.to_bytes(4, "little") + valid[12:]))
        self.assertFalse(library.poly_pizza_glb_is_valid(b"glTF" + (2).to_bytes(4, "little") + (total + 4).to_bytes(4, "little") + valid[12:]))
        invalid_json = b"not-json".ljust(8, b" ")
        bad = b"glTF" + (2).to_bytes(4, "little") + (28).to_bytes(4, "little") + (8).to_bytes(4, "little") + b"JSON" + invalid_json
        self.assertFalse(library.poly_pizza_glb_is_valid(bad))

        remote_payload = json.dumps({
            "asset": {"version": "2.0"},
            "buffers": [{"byteLength": 4, "uri": "https://evil.example/model.bin"}],
        }).encode("utf-8")
        remote_payload += b" " * ((4 - len(remote_payload) % 4) % 4)
        remote_total = 12 + 8 + len(remote_payload)
        remote_glb = b"glTF" + (2).to_bytes(4, "little") + remote_total.to_bytes(4, "little") + len(remote_payload).to_bytes(4, "little") + b"JSON" + remote_payload
        self.assertFalse(library.poly_pizza_glb_is_valid(remote_glb))

        no_bin_payload = json.dumps({
            "asset": {"version": "2.0"},
            "buffers": [{"byteLength": 16}],
        }).encode("utf-8")
        no_bin_payload += b" " * ((4 - len(no_bin_payload) % 4) % 4)
        no_bin_total = 12 + 8 + len(no_bin_payload)
        no_bin_glb = b"glTF" + (2).to_bytes(4, "little") + no_bin_total.to_bytes(4, "little") + len(no_bin_payload).to_bytes(4, "little") + b"JSON" + no_bin_payload
        self.assertFalse(library.poly_pizza_glb_is_valid(no_bin_glb))

    def test_importer_skips_without_secret_and_does_not_attempt_network(self):
        with mock.patch.dict(library.os.environ if hasattr(library, "os") else __import__("os").environ,
                             {"POLY_PIZZA_API_KEY": ""}, clear=False):
            with mock.patch.object(library, "poly_pizza_api_json", side_effect=AssertionError("network must not run")):
                report = library.download_poly_pizza(Path("."), [])
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]["status"], "skipped_missing_api_key")

    def test_importer_rechecks_detail_and_records_glb_receipt(self):
        model = self._model()
        gltf_json = json.dumps({"asset": {"version": "2.0"}}).encode("utf-8")
        gltf_json += b" " * ((4 - len(gltf_json) % 4) % 4)
        glb_length = 12 + 8 + len(gltf_json)
        glb = b"glTF" + (2).to_bytes(4, "little") + glb_length.to_bytes(4, "little") + len(gltf_json).to_bytes(4, "little") + b"JSON" + gltf_json
        def fake_api(path, params, token):
            if path == "/model/TreeOne":
                return model
            if "/search/tree" in path:
                return {"results": [model]}
            return {"results": []}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = []
            with mock.patch.dict(__import__("os").environ, {"POLY_PIZZA_API_KEY": "test-token"}, clear=False), \
                 mock.patch.object(library, "poly_pizza_api_json", side_effect=fake_api), \
                 mock.patch.object(library, "poly_pizza_download_glb", return_value=(glb, model["Download"])), \
                 mock.patch.object(library.time, "sleep", return_value=None):
                report = library.download_poly_pizza(root, index)
            downloaded = [row for row in report if row.get("status") == "downloaded"]
            self.assertEqual(len(downloaded), 1)
            self.assertEqual(len(index), 1)
            asset = index[0]
            self.assertEqual(asset["license"], "CC0-1.0")
            self.assertTrue(asset["license_verified_from_item_metadata"])
            path = root / asset["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_bytes(), glb)
            self.assertEqual(asset["sha256"], library.sha256_path(path))
            self.assertTrue((path.parent / "SOURCE_AND_LICENSE.md").is_file())
            self.assertEqual(path.parent.parent.name, "models")
            self.assertRegex(path.parent.name, r"^treeone-[0-9a-f]{10}$")


class LazyTexturesCC0APITests(unittest.TestCase):
    def test_asset_names_and_detail_urls_are_pinned(self):
        self.assertTrue(library.lazytextures_asset_name_is_allowed("Concrete01"))
        self.assertTrue(library.lazytextures_asset_name_is_allowed("Oak Wood 02"))
        self.assertTrue(library.lazytextures_asset_name_is_allowed("Árbol de Navidad"))
        self.assertFalse(library.lazytextures_asset_name_is_allowed("../payload"))
        self.assertFalse(library.lazytextures_asset_name_is_allowed("folder/model"))
        self.assertFalse(library.lazytextures_asset_name_is_allowed("bad\\name"))
        self.assertFalse(library.lazytextures_asset_name_is_allowed(""))

        detail = library.lazytextures_detail_url("materials", "Concrete01")
        self.assertEqual(
            detail,
            "https://lazytextures.net:3000/Asset/materials/Concrete01",
        )
        self.assertTrue(library.lazytextures_detail_url_is_allowed(detail, "materials", "Concrete01"))
        self.assertFalse(library.lazytextures_detail_url_is_allowed(
            "https://evil.example:3000/Asset/materials/Concrete01", "materials", "Concrete01"
        ))
        self.assertFalse(library.lazytextures_detail_url_is_allowed(
            "https://lazytextures.net:3000/Asset/models/Concrete01", "materials", "Concrete01"
        ))
        with self.assertRaises(ValueError):
            library.lazytextures_detail_url("unknown", "Concrete01")

    def test_zip_download_allowlist_rejects_untrusted_hosts_paths_and_formats(self):
        good = "https://lazytextures.net:3000/Assets/Materials/Concrete01/Mat/1k/Concrete01_1k.zip"
        self.assertTrue(library.lazytextures_download_url_is_allowed(good))
        self.assertEqual(library.lazytextures_download_url("/Assets/Models/SpaceKit/1k/SpaceKit_1k.zip"),
                         "https://lazytextures.net:3000/Assets/Models/SpaceKit/1k/SpaceKit_1k.zip")
        for bad in [
            "http://lazytextures.net:3000/Assets/Materials/a.zip",
            "https://lazytextures.net/Assets/Materials/a.zip",
            "https://lazytextures.net:3000.evil.example/Assets/Materials/a.zip",
            "https://evil.example:3000/Assets/Materials/a.zip",
            "https://lazytextures.net:3000/Asset/materials/a.zip",
            "https://lazytextures.net:3000/Assets/Materials/../escape.zip",
            "https://lazytextures.net:3000/Assets/Materials/a.exe",
            "https://lazytextures.net:3000/Assets/Materials/a.zip?redirect=1",
            "https://user@lazytextures.net:3000/Assets/Materials/a.zip",
        ]:
            self.assertFalse(library.lazytextures_download_url_is_allowed(bad), bad)
        self.assertEqual(library.lazytextures_download_url("/Assets/../../escape.zip"), "")

    def test_api_browse_parser_requires_success_and_documented_asset_list(self):
        expected = [{"name": "Concrete01", "category": "Concrete"}]
        self.assertEqual(
            library.lazytextures_response_assets({"success": True, "PreviewMaterials": expected}, "materials"),
            expected,
        )
        self.assertEqual(
            library.lazytextures_response_assets({"success": True, "data": {"PreviewModels": [{"name": "SpaceKit"}]}}, "models"),
            [{"name": "SpaceKit"}],
        )
        self.assertEqual(library.lazytextures_response_assets({"success": True, "data": [{"name": "Brush01"}]}, "other"), [{"name": "Brush01"}])
        self.assertEqual(library.lazytextures_response_assets({"success": True, "PreviewOthers": [{"name": "Preset01"}]}, "other"), [{"name": "Preset01"}])
        self.assertEqual(library.lazytextures_response_assets({"success": False, "PreviewMaterials": expected}, "materials"), [])
        self.assertEqual(library.lazytextures_response_assets({"success": True, "PreviewMaterials": expected}, "models"), [])

    def test_provider_wide_cc0_policy_accepts_absent_or_exact_cc0_and_rejects_conflicts(self):
        self.assertTrue(library.lazytextures_license_detail({"name": "Concrete01"})["verified"])
        self.assertEqual(library.lazytextures_license_detail({"name": "Concrete01"})["license"], "CC0-1.0")
        self.assertTrue(library.lazytextures_license_detail({"license": "CC0 1.0 Universal"})["verified"])
        self.assertTrue(library.lazytextures_license_detail({
            "licenseUrl": "https://creativecommons.org/publicdomain/zero/1.0/"
        })["verified"])
        self.assertFalse(library.lazytextures_license_detail({"license": "CC BY 4.0"})["verified"])
        self.assertFalse(library.lazytextures_license_detail({"license_url": "unknown"})["verified"])
        self.assertFalse(library.lazytextures_license_detail(None)["verified"])

    def test_archive_picker_prefers_smallest_available_resolution_and_checks_path_size(self):
        detail = {
            "archiveFiles": {
                "4k": [{"name": "Concrete01_4k.zip",
                         "path": "/Assets/Materials/Concrete01/Mat/4k/Concrete01_4k.zip",
                         "size": 22_020_096}],
                "1k": [{"name": "Concrete01_1k.zip",
                         "path": "/Assets/Materials/Concrete01/Mat/1k/Concrete01_1k.zip",
                         "size": 2_000_000}],
                "unsafe": [{"name": "escape.zip", "path": "/Assets/../../escape.zip", "size": 1_000}],
                "huge": [{"name": "huge.zip", "path": "/Assets/Materials/huge.zip",
                          "size": library.LAZYTEXTURES_MAX_ARCHIVE_BYTES + 1}],
                "wrong": [{"name": "not-a-zip.exe", "path": "/Assets/Materials/not-a-zip.exe", "size": 1000}],
            },
            "textureFiles": {
                "1k": [{"name": "Texture_Rust_1k.zip",
                        "path": "/Assets/Textures/Rust/1k/Texture_Rust_1k.zip",
                        "size": 3_500_000}],
            }
        }
        candidates = library.lazytextures_archive_candidates(detail)
        self.assertEqual(len(candidates), 3)
        self.assertTrue(any(row["name"] == "Texture_Rust_1k.zip" for row in candidates))
        choice = library.lazytextures_choose_archive(detail)
        self.assertEqual(choice["name"], "Concrete01_1k.zip")
        self.assertEqual(choice["size_bytes"], 2_000_000)
        self.assertEqual(library.lazytextures_archive_candidates({"archiveFiles": [], "textureFiles": []}), [])

    def test_zip_preflight_bounds_paths_members_expansion_and_compression_ratio(self):
        safe = io.BytesIO()
        with zipfile.ZipFile(safe, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("model/scene.obj", "o Example\nv 0 0 0\n")
            archive.writestr("model/material.mtl", "newmtl Example\nKd 1 1 1\n")
        count, unpacked = library.lazytextures_validate_zip_archive(safe.getvalue())
        self.assertEqual(count, 2)
        self.assertGreater(unpacked, 0)

        traversal = io.BytesIO()
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr("../escape.obj", "v 0 0 0\n")
        with self.assertRaises(RuntimeError):
            library.lazytextures_validate_zip_archive(traversal.getvalue())

        too_many = io.BytesIO()
        with zipfile.ZipFile(too_many, "w") as archive:
            for i in range(library.LAZYTEXTURES_MAX_ZIP_MEMBERS + 1):
                archive.writestr(f"item-{i}.txt", "x")
        with self.assertRaises(RuntimeError):
            library.lazytextures_validate_zip_archive(too_many.getvalue())

    def test_lazytextures_file_signatures_accept_supported_assets_and_reject_mislabeled_files(self):
        self.assertTrue(library.lazytextures_media_signature_is_valid(b"\x89PNG\r\n\x1a\n" + b"x" * 32, ".png"))
        self.assertTrue(library.lazytextures_media_signature_is_valid(b"Kaydara FBX Binary  \x00\x1a\x00", ".fbx"))
        self.assertTrue(library.lazytextures_media_signature_is_valid(b"BLENDER-v300", ".blend"))
        self.assertTrue(library.lazytextures_media_signature_is_valid(b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 8, ".wav"))
        self.assertFalse(library.lazytextures_media_signature_is_valid(b"<html>blocked</html>", ".png"))
        self.assertFalse(library.lazytextures_media_signature_is_valid(b"PK\x03\x04", ".fbx"))

    def test_bounded_importer_records_only_verified_files_and_source_provenance(self):
        buffer = io.BytesIO()
        payload = b"Kaydara FBX Binary  \x00\x1a\x00"
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("SpaceKit.fbx", payload)
        archive_blob = buffer.getvalue()
        expected_size = len(archive_blob)

        browse_payloads = {
            "models": [{"name": "SpaceKit", "tags": ["space", "vehicle"]}],
            "materials": [], "hdris": [], "textures": [], "other": [],
        }
        responses = {}
        for asset_type, spec in library.LAZYTEXTURES_API_TYPES.items():
            responses[library.LAZYTEXTURES_API_BASE + "/" + spec["endpoint"]] = {
                "success": True, spec["list_key"]: browse_payloads[asset_type]
            }
        detail_url = library.lazytextures_detail_url("models", "SpaceKit")
        responses[detail_url] = {
            "success": True, "name": "SpaceKit", "assetType": "models",
            "tags": ["space", "vehicle"],
            "archiveFiles": {"1k": [{
                "name": "SpaceKit_1k.zip",
                "path": "/Assets/Models/SpaceKit/1k/SpaceKit_1k.zip",
                "size": expected_size,
            }]},
        }

        def fake_request_json(url, timeout=25):
            return responses[url]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = []
            with mock.patch.object(library, "request_json", side_effect=fake_request_json), \
                 mock.patch.object(library, "lazytextures_download_bytes", return_value=(archive_blob, "application/zip")), \
                 mock.patch.object(library.time, "sleep", return_value=None):
                report = library.download_lazytextures(root, index)

            downloaded = [row for row in report if row.get("status") == "downloaded"]
            self.assertEqual(len(downloaded), 1)
            self.assertEqual(downloaded[0]["asset_type"], "models")
            self.assertEqual(downloaded[0]["extracted_files"], 1)
            self.assertEqual(len(index), 1)
            item = index[0]
            self.assertEqual(item["provider"], "LazyTextures")
            self.assertEqual(item["license"], "CC0-1.0")
            self.assertTrue(item["license_verified_from_provider_api_policy"])
            self.assertEqual(item["source_page"], detail_url)
            self.assertEqual(item["download_archive_sha256"], downloaded[0]["archive_sha256"])
            path = root / item["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_bytes(), payload)
            self.assertEqual(item["sha256"], library.sha256_path(path))

    def test_download_helper_rejects_redirects_outside_the_official_host(self):
        response = mock.MagicMock()
        response.__enter__.return_value.geturl.return_value = "https://evil.example/payload.zip"
        response.__enter__.return_value.read.return_value = b"PK\\x03\\x04"
        response.__enter__.return_value.headers.get.return_value = "application/zip"
        with mock.patch.object(library.urllib.request, "urlopen", return_value=response):
            with self.assertRaises(RuntimeError):
                library.lazytextures_download_bytes(
                    "https://lazytextures.net:3000/Assets/Materials/Concrete01/1k/a.zip",
                    limit=1024,
                )

class OpenMojiCCBYSAAssetTests(unittest.TestCase):
    def test_openmoji_npm_metadata_requires_pinned_version_and_sharealike_license(self):
        good = {
            "version": "17.0.0",
            "license": "CC-BY-SA-4.0",
            "repository": {"url": "git+https://github.com/hfg-gmuend/openmoji.git"},
            "dist": {
                "tarball": "https://registry.npmjs.org/openmoji/-/openmoji-17.0.0.tgz",
                "shasum": "ee8094c5c0de0d2126b77ceb074d62b6fe2071d0",
                "integrity": "sha512-EBnYrNGdcdw+OSXmENeNE1yBNRu6tOraTmoOyUbJkTmvT/+XETp8RZLSJFzD3lrPc5N9CzsyPnRTk0Vp4UaI9w==",
                "fileCount": 11539,
                "unpackedSize": 43405090,
            },
        }
        self.assertTrue(library.openmoji_metadata_is_eligible(good))
        bad = json.loads(json.dumps(good))
        bad["license"] = "CC0-1.0"
        self.assertFalse(library.openmoji_metadata_is_eligible(bad))
        bad = json.loads(json.dumps(good))
        bad["dist"]["fileCount"] = 11538
        self.assertFalse(library.openmoji_metadata_is_eligible(bad))
        bad = json.loads(json.dumps(good))
        bad["dist"]["unpackedSize"] = library.OPENMOJI_MAX_EXTRACTED_BYTES + 1
        self.assertFalse(library.openmoji_metadata_is_eligible(bad))
        bad = json.loads(json.dumps(good))
        bad["version"] = "latest"
        self.assertFalse(library.openmoji_metadata_is_eligible(bad))
        bad = json.loads(json.dumps(good))
        bad["dist"]["tarball"] = "https://evil.example/openmoji-17.0.0.tgz"
        self.assertFalse(library.openmoji_metadata_is_eligible(bad))

    def test_openmoji_tarball_and_asset_path_allowlists_are_strict(self):
        self.assertTrue(library.openmoji_tarball_url_is_allowed(
            "https://registry.npmjs.org/openmoji/-/openmoji-17.0.0.tgz"))
        self.assertFalse(library.openmoji_tarball_url_is_allowed(
            "http://registry.npmjs.org/openmoji/-/openmoji-17.0.0.tgz"))
        self.assertFalse(library.openmoji_tarball_url_is_allowed(
            "https://registry.npmjs.org/openmoji/-/openmoji-16.0.0.tgz"))
        self.assertFalse(library.openmoji_tarball_url_is_allowed(
            "https://user@registry.npmjs.org/openmoji/-/openmoji-17.0.0.tgz"))
        self.assertEqual(library.openmoji_selected_archive_path("package/color/svg/1F600.svg"), "color/svg/1F600.svg")
        self.assertEqual(library.openmoji_selected_archive_path("package/black/618x618/1F600.png"), "black/618x618/1F600.png")
        self.assertEqual(library.openmoji_selected_archive_path("package/data/openmoji.json"), "data/openmoji.json")
        self.assertIsNone(library.openmoji_selected_archive_path("package/helpers/install.js"))
        self.assertIsNone(library.openmoji_selected_archive_path("package/src/generator.py"))
        self.assertIsNone(library.openmoji_selected_archive_path("package/color/svg/../../outside.svg"))

    def test_openmoji_extractor_keeps_only_safe_svg_png_and_central_metadata(self):
        stream = io.BytesIO()
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(1)</script><rect width="10" height="10"/></svg>'
        png = b"\x89PNG\r\n\x1a\n" + b"valid-png-fixture"
        metadata = json.dumps([{"hexcode": "1F600", "annotation": "grinning face"}]).encode()
        with tarfile.open(fileobj=stream, mode="w:gz") as archive:
            def add_file(name, payload):
                info = tarfile.TarInfo(name)
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            add_file("package/color/svg/1F600.svg", svg)
            add_file("package/black/618x618/1F600.png", png)
            add_file("package/data/openmoji.json", metadata)
            add_file("package/helpers/install.js", b"console.log('do not extract')")
            add_file("package/color/svg/unsafe.png", b"<html>not a png</html>")
            link = tarfile.TarInfo("package/color/svg/symlink.svg")
            link.type = tarfile.SYMTYPE
            link.linkname = "../outside.svg"
            archive.addfile(link)
            add_file("package/../outside.svg", svg)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "openmoji"
            selected, rows = library.openmoji_extract_selected_assets(stream.getvalue(), target)
            self.assertEqual(len(selected), 2)
            self.assertEqual(len(rows), 1)
            self.assertTrue((target / "color/svg/1F600.svg").is_file())
            self.assertTrue((target / "black/618x618/1F600.png").is_file())
            self.assertFalse((target / "helpers/install.js").exists())
            self.assertFalse((Path(tmp) / "outside.svg").exists())
            cleaned = (target / "color/svg/1F600.svg").read_text(encoding="utf-8")
            self.assertNotIn("<script", cleaned.lower())
            self.assertNotIn("onload=", cleaned.lower())


class GoogleFontsOFLTests(unittest.TestCase):
    def test_google_fonts_api_endpoint_is_pinned_to_official_family_directory(self):
        self.assertTrue(library.google_fonts_api_url_is_allowed(
            "https://api.github.com/repos/google/fonts/contents/ofl/inter?ref=main", "inter"))
        self.assertFalse(library.google_fonts_api_url_is_allowed(
            "https://api.github.com/repos/other/fonts/contents/ofl/inter?ref=main", "inter"))
        self.assertFalse(library.google_fonts_api_url_is_allowed(
            "https://api.github.com/repos/google/fonts/contents/ofl/roboto?ref=main", "inter"))
        self.assertFalse(library.google_fonts_api_url_is_allowed(
            "https://api.github.com/repos/google/fonts/contents/ofl/inter?ref=dev", "inter"))

    def test_google_fonts_raw_files_must_match_family_path(self):
        self.assertTrue(library.google_fonts_raw_url_is_allowed(
            "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
            "inter", "Inter[opsz,wght].ttf"))
        self.assertTrue(library.google_fonts_raw_url_is_allowed(
            "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt", "inter", "OFL.txt"))
        self.assertFalse(library.google_fonts_raw_url_is_allowed(
            "https://evil.example/google/fonts/main/ofl/inter/Inter.ttf", "inter", "Inter.ttf"))
        self.assertFalse(library.google_fonts_raw_url_is_allowed(
            "https://raw.githubusercontent.com/google/fonts/main/ofl/roboto/Roboto.ttf", "inter", "Roboto.ttf"))

    def test_google_fonts_requires_real_sil_ofl_1_1_text(self):
        good = "Copyright 2024 A Font Author\nSIL OPEN FONT LICENSE Version 1.1\nPermission is hereby granted."
        self.assertTrue(library.google_fonts_ofl_is_valid(good))
        self.assertFalse(library.google_fonts_ofl_is_valid("Copyright 2024. CC0 1.0 public domain."))
        self.assertFalse(library.google_fonts_ofl_is_valid("SIL OPEN FONT LICENSE Version 1.0"))

    def test_google_fonts_accepts_sfnt_ttf_and_rejects_html(self):
        self.assertTrue(library.google_fonts_ttf_signature_is_valid(b"\x00\x01\x00\x00" + b"x" * 5000))
        self.assertTrue(library.google_fonts_ttf_signature_is_valid(b"OTTO" + b"x" * 5000))
        self.assertFalse(library.google_fonts_ttf_signature_is_valid(b"<html>" + b"x" * 5000))
        self.assertEqual(len(library.GOOGLE_FONTS_FAMILY_SLUGS), library.GOOGLE_FONTS_MAX_FAMILIES)
        self.assertEqual(library.GOOGLE_FONTS_MAX_TTF_PER_FAMILY, 2)
        self.assertGreaterEqual(library.GOOGLE_FONTS_MAX_TOTAL_BYTES, 50 * 1024 * 1024)


class SafeArchiveExtractionTests(unittest.TestCase):
    def _archive(self, filename, payload=b"not-executable"):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr(filename, payload)
        return stream.getvalue()

    def test_safe_extract_rejects_posix_and_windows_traversal(self):
        for member in ("../escape.png", "folder\\\\..\\\\escape.png", "C:\\\\Windows\\\\escape.png"):
            with self.subTest(member=member), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    library.safe_extract(self._archive(member), Path(tmp) / "bundle", max_bytes=1024)
                self.assertFalse((Path(tmp) / "escape.png").exists())

    def test_safe_extract_rejects_symlink_members(self):
        stream = io.BytesIO()
        info = zipfile.ZipInfo("linked.png")
        info.external_attr = (0o120777 << 16)
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr(info, "../outside.png")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                library.safe_extract(stream.getvalue(), Path(tmp) / "bundle", max_bytes=1024)

    def test_safe_extract_keeps_normal_nested_media(self):
        payload = self._archive("Textures/stone.png", b"safe-image-data" * 10)
        with tempfile.TemporaryDirectory() as tmp:
            count, size = library.safe_extract(payload, Path(tmp) / "bundle", max_bytes=1024)
            self.assertEqual(count, 1)
            self.assertGreater(size, 0)
            self.assertTrue((Path(tmp) / "bundle" / "Textures" / "stone.png").is_file())


class OpenGameArtRightsAndParsingTests(unittest.TestCase):
    ZIP_URL = "https://opengameart.org/sites/default/files/sample-pack.zip"
    PNG_URL = "https://opengameart.org/sites/default/files/sample.png"

    def test_opengameart_search_requires_official_cc0_and_known_art_type_taxonomy(self):
        good = "https://opengameart.org/art-search-advanced?field_art_licenses_tid%5B0%5D=4&field_art_type_tid%5B0%5D=13&sort_by=count&sort_order=DESC&items_per_page=24&page=0"
        self.assertTrue(library.opengameart_search_page_is_allowed(good))
        self.assertFalse(library.opengameart_search_page_is_allowed(good.replace("=4&", "=2&")))
        self.assertFalse(library.opengameart_search_page_is_allowed(good.replace("%5B0%5D=13", "%5B0%5D=999")))
        self.assertFalse(library.opengameart_search_page_is_allowed("https://evil.example/art-search-advanced?field_art_licenses_tid%5B0%5D=4&field_art_type_tid%5B0%5D=13"))

    def test_opengameart_item_page_requires_single_exact_cc0_license(self):
        self.assertTrue(library.opengameart_item_page_is_allowed("https://opengameart.org/content/rpg-sound-pack"))
        self.assertFalse(library.opengameart_item_page_is_allowed("http://opengameart.org/content/rpg-sound-pack"))
        self.assertFalse(library.opengameart_item_page_is_allowed("https://opengameart.org/content/rpg-sound-pack/extra"))
        self.assertTrue(library.opengameart_cc0_link_is_valid("http://creativecommons.org/publicdomain/zero/1.0/"))
        self.assertFalse(library.opengameart_cc0_link_is_valid("https://creativecommons.org/licenses/by/4.0/"))
        cc0 = """<div class="field-name-field-art-licenses"><div><a href="http://creativecommons.org/publicdomain/zero/1.0/"><div class="license-name">CC0</div></a></div></div>"""
        parsed = library.opengameart_parse_item_page(cc0)
        self.assertTrue(parsed["cc0_verified_from_item_page"])
        non_cc0 = """<div class="field-name-field-art-licenses"><div><a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0</a></div></div>"""
        self.assertFalse(library.opengameart_parse_item_page(non_cc0)["cc0_verified_from_item_page"])
        mixed = """<div class="field-name-field-art-licenses"><div><a href="http://creativecommons.org/publicdomain/zero/1.0/">CC0</a><a href="https://creativecommons.org/licenses/by/4.0/">CC BY</a></div></div>"""
        self.assertFalse(library.opengameart_parse_item_page(mixed)["cc0_verified_from_item_page"])

    def test_opengameart_parser_extracts_only_file_section_and_creator(self):
        page = f"""<html><head><meta property="og:title" content="Sample game asset pack"></head><body>
        <div class="field-name-title"><div><h2>Sample game asset pack</h2></div></div>
        <div class="field-name-author-submitter"><div><span>Maker One</span><a href="https://opengameart.org/users/maker-one">Maker One</a></div></div>
        <div class="field-name-field-art-licenses"><div><a href="http://creativecommons.org/publicdomain/zero/1.0/">CC0</a></div></div>
        <a href="https://opengameart.org/sites/default/files/preview.png">Not an attachment</a>
        <div class="field-name-field-art-files"><div><span class="file"><a type="application/zip; length=1234" download="sample-pack.zip" href="{self.ZIP_URL}">sample-pack.zip</a></span></div></div>
        </body></html>"""
        parsed = library.opengameart_parse_item_page(page)
        self.assertTrue(parsed["cc0_verified_from_item_page"])
        self.assertEqual(parsed["title"], "Sample game asset pack")
        self.assertIn("Maker One", parsed["creator"])
        self.assertEqual(len(parsed["files"]), 1)
        self.assertEqual(parsed["files"][0]["url"], self.ZIP_URL)
        self.assertEqual(parsed["files"][0]["declared_size"], 1234)

    def test_opengameart_search_parser_reads_only_result_view_not_sidebar(self):
        page = """<html><body>
        <div class="view view-art view-id-art view-display-id-search_art_advanced">
          <div class="view-content"><div class="views-row">
            <a href="https://opengameart.org/content/rpg-sound-pack">RPG Sound Pack</a>
          </div></div>
          <a href="https://opengameart.org/art-search-advanced?page=1">next page</a>
        </div>
        <div class="sidebar"><a href="https://opengameart.org/content/not-a-search-result">sidebar link</a></div>
        </body></html>"""
        self.assertEqual(
            library.opengameart_parse_search_page(page),
            ["https://opengameart.org/content/rpg-sound-pack"],
        )

    def test_opengameart_file_allowlist_requires_official_file_host_and_path(self):
        self.assertTrue(library.opengameart_file_url_is_allowed(self.ZIP_URL))
        self.assertTrue(library.opengameart_file_url_is_allowed(self.PNG_URL))
        self.assertFalse(library.opengameart_file_url_is_allowed("https://opengameart.org/sites/default/files/unsafe.svg"))
        self.assertFalse(library.opengameart_file_url_is_allowed("https://opengameart.org/sites/default/files/project.blend"))
        self.assertFalse(library.opengameart_file_url_is_allowed("https://example.com/sites/default/files/sample.zip"))
        self.assertFalse(library.opengameart_file_url_is_allowed("https://opengameart.org/other/sample.zip"))
        self.assertFalse(library.opengameart_file_url_is_allowed("http://opengameart.org/sites/default/files/sample.zip"))
        self.assertFalse(library.opengameart_file_url_is_allowed("https://user@opengameart.org/sites/default/files/sample.zip"))

    def test_opengameart_signature_gate_rejects_html_and_bad_media_bytes(self):
        self.assertTrue(library.opengameart_file_signature_is_valid(b"PK\x03\x04" + b"x" * 64, ".zip", "application/zip"))
        self.assertTrue(library.opengameart_file_signature_is_valid(b"\x89PNG\r\n\x1a\n" + b"x" * 64, ".png", "image/png"))
        self.assertTrue(library.opengameart_file_signature_is_valid(b"OggS" + b"x" * 64, ".ogg", "audio/ogg"))
        self.assertTrue(library.opengameart_file_signature_is_valid(b"wOF2" + b"x" * 64, ".woff2", "font/woff2"))
        self.assertTrue(library.opengameart_file_signature_is_valid(b"\x1a\x45\xdf\xa3" + b"x" * 64, ".webm", "video/webm"))
        self.assertFalse(library.opengameart_file_signature_is_valid(b"<html>not a zip</html>", ".zip", "text/html"))
        self.assertFalse(library.opengameart_file_signature_is_valid(b"<html>not a png</html>", ".png", "text/html"))

class ScalableBundlePackagingTests(unittest.TestCase):
    def _create_library(self, root, asset_sizes):
        library_root = root / "video-asset-library"
        library_root.mkdir(parents=True)
        assets = []
        for i, size in enumerate(asset_sizes):
            rel = f"originals/stickers/sticker-{i}.svg"
            path = library_root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((f"<svg id='{i}'>" + "x" * (size - 20) + "</svg>").encode("utf-8"))
            assets.append({
                "id": f"sticker-{i}", "path": rel, "type": "original-video-sticker",
                "license": "CC0-1.0", "redistributable": True
            })
        (library_root / "ASSET_INDEX.json").write_text(json.dumps({
            "built_at": "2026-10-30T00:00:00Z", "assets": assets, "summary": {}
        }), encoding="utf-8")
        (library_root / "ASSET_CATALOG.html").write_text("<html>catalog</html>", encoding="utf-8")
        (library_root / "SOURCES_AND_LICENSES.md").write_text("# rights", encoding="utf-8")
        (library_root / "SHA256SUMS.txt").write_text("", encoding="utf-8")
        return library_root

    def test_compact_library_keeps_one_click_legacy_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            root = self._create_library(output, [128, 128])
            manifest = bundle_packager.package_library(output)
            self.assertEqual(manifest["mode"], "single-archive")
            self.assertEqual(manifest["bundle_count"], 1)
            self.assertTrue((output / "video-asset-library.zip").is_file())
            self.assertFalse((output / "video-assets-catalog.zip").exists())
            bundle_packager.verify_manifest(output, root, manifest)

    def test_large_library_splits_by_family_and_extracts_into_same_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            root = self._create_library(output, [35_000, 35_000, 35_000])
            with mock.patch.object(bundle_packager, "MAX_BUNDLE_UNCOMPRESSED_BYTES", 50_000):
                manifest = bundle_packager.package_library(output)
                self.assertEqual(manifest["mode"], "multi-volume")
                self.assertGreaterEqual(manifest["bundle_count"], 3)
                names = {row["name"] for row in manifest["bundles"]}
                self.assertIn("video-assets-catalog.zip", names)
                self.assertTrue(any(name.startswith("video-assets-original-graphics-") for name in names))
                self.assertFalse((output / "video-asset-library.zip").exists())
                self.assertTrue((output / "ASSET_BUNDLES.json").is_file())
                bundle_packager.verify_manifest(output, root, manifest)

    def test_packager_classifies_stickers_textures_audio_footage_and_fonts(self):
        self.assertEqual(bundle_packager.classify_asset({"type": "original-video-sticker", "path": "originals/stickers/wow.svg"}), "original-graphics")
        self.assertEqual(bundle_packager.classify_asset({"type": "original-meme-layout-template", "path": "originals/meme-templates/two-panel.svg"}), "original-graphics")
        self.assertEqual(bundle_packager.classify_asset({"type": "original-svg-texture", "category": "texture / surface", "path": "originals/textures/grid.svg"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "original-procedural-sfx", "path": "originals/audio/cue.wav"}), "audio")
        self.assertEqual(bundle_packager.classify_asset({"type": "original-procedural-video-loop", "path": "originals/video-loops/loop.mp4"}), "footage")
        self.assertEqual(bundle_packager.classify_asset({"type": "google-font-ttf", "path": "third-party/google-fonts/inter/Inter.ttf"}), "typography")
        self.assertEqual(bundle_packager.classify_asset({"type": "openmoji-cc-by-sa-svg", "path": "third-party/openmoji/color/svg/1F600.svg"}), "original-graphics")
        self.assertEqual(bundle_packager.classify_asset({"type": "openmoji-cc-by-sa-png", "path": "third-party/openmoji/color/618x618/1F600.png"}), "original-graphics")
        self.assertEqual(bundle_packager.classify_asset({"type": "kenney-godot-splashscreens-cc0-asset-file", "path": "third-party/kenney/godot-splashscreens/Screen/Reimagined logo/blue.png"}), "original-graphics")
        self.assertEqual(bundle_packager.classify_unindexed_path("third-party/kenney/godot-splashscreens/SOURCE_AND_LICENSE.md"), "original-graphics")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-models-asset-file", "path": "third-party/lazytextures/models/SpaceKit/model.fbx"}), "3d-models")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-materials-asset-file", "path": "third-party/lazytextures/materials/Concrete01/Color.png"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-hdris-asset-file", "path": "third-party/lazytextures/hdris/Studio/lighting.exr"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-textures-asset-file", "path": "third-party/lazytextures/textures/Rust/overlay.png"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-other-asset-file", "path": "third-party/lazytextures/other/Brush01/brush.png"}), "miscellaneous")
        self.assertEqual(bundle_packager.classify_asset({"type": "poly-pizza-cc0-model", "path": "third-party/poly-pizza/models/TreeOne/model.glb"}), "3d-models")
        self.assertEqual(bundle_packager.classify_unindexed_path("third-party/poly-pizza/models/TreeOne/SOURCE_AND_LICENSE.md"), "3d-models")
        self.assertEqual(bundle_packager.classify_unindexed_path("third-party/lazytextures/models/SpaceKit/SOURCE_AND_LICENSE.md"), "3d-models")
        self.assertEqual(bundle_packager.classify_unindexed_path("third-party/lazytextures/materials/Concrete01/SOURCE_AND_LICENSE.md"), "3d-textures")
        self.assertEqual(bundle_packager.classify_unindexed_path("third-party/lazytextures/other/Brush01/SOURCE_AND_LICENSE.md"), "miscellaneous")

    def test_bundle_manifest_detects_missing_or_modified_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            root = self._create_library(output, [128])
            manifest = bundle_packager.package_library(output)
            first = output / manifest["bundles"][0]["name"]
            first.write_bytes(first.read_bytes() + b"tamper")
            with self.assertRaises(RuntimeError):
                bundle_packager.verify_manifest(output, root, manifest)


class InternetArchiveVideoRightsAndParsingTests(unittest.TestCase):
    def test_internet_archive_identifier_and_item_endpoints_are_pinned(self):
        self.assertTrue(library.internet_archive_identifier_is_allowed("AboutBan1935"))
        self.assertFalse(library.internet_archive_identifier_is_allowed("../AboutBan1935"))
        self.assertFalse(library.internet_archive_identifier_is_allowed("has space"))
        self.assertTrue(library.internet_archive_item_url_is_allowed(
            "https://archive.org/details/AboutBan1935", "AboutBan1935"))
        self.assertTrue(library.internet_archive_metadata_url_is_allowed(
            "https://archive.org/metadata/AboutBan1935", "AboutBan1935"))
        self.assertFalse(library.internet_archive_item_url_is_allowed(
            "https://evil.example/details/AboutBan1935", "AboutBan1935"))
        self.assertFalse(library.internet_archive_metadata_url_is_allowed(
            "https://archive.org/metadata/OtherItem", "AboutBan1935"))

    def test_internet_archive_accepts_only_exact_cc0_or_public_domain_item_rights(self):
        self.assertEqual(
            library.internet_archive_license_from_item_metadata(
                "http://creativecommons.org/publicdomain/zero/1.0/", ""),
            "CC0-1.0")
        self.assertEqual(
            library.internet_archive_license_from_item_metadata(
                "https://creativecommons.org/licenses/cc0/3.0/", ""),
            "CC0-3.0")
        self.assertEqual(
            library.internet_archive_license_from_item_metadata(
                "http://creativecommons.org/licenses/publicdomain/", "Public Domain"),
            "Public Domain (item-level Internet Archive rights statement)")
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "http://creativecommons.org/licenses/publicdomain/", ""))
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "http://creativecommons.org/licenses/publicdomain/", "Public Domain with restrictions"))
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "https://creativecommons.org/licenses/by/4.0/", "Public Domain"))
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "http://creativecommons.org/publicdomain/mark/1.0/", "Public Domain"))
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "https://user@creativecommons.org/publicdomain/zero/1.0/", ""))
        self.assertIsNone(library.internet_archive_license_from_item_metadata(
            "https://creativecommons.org/publicdomain/zero/1.0/?redirect=1", ""))

    def test_internet_archive_metadata_normalizer_and_license_detail(self):
        payload = {
            "metadata": {
                "identifier": "Doctorin1946", "mediatype": "movies",
                "licenseurl": "http://creativecommons.org/licenses/publicdomain/",
                "rights": "Public Domain", "collection": ["prelinger", "opensource_movies"]
            },
            "files": [{"name": "Doctorin1946.mp4", "size": "117249712", "source": "derivative"}]
        }
        metadata, files = library.internet_archive_parse_payload(payload)
        self.assertEqual(metadata["identifier"], "Doctorin1946")
        self.assertEqual(len(files), 1)
        detail = library.internet_archive_license_detail(metadata)
        self.assertTrue(detail["verified"])
        self.assertIn("Public Domain", detail["license"])

    def test_internet_archive_video_picker_prefers_largest_safe_mp4(self):
        rows = [
            {"name": "film.mpeg", "size": 30000000, "length": 120},
            {"name": "film-512kb.mp4", "size": 20000000, "length": 120, "source": "derivative"},
            {"name": "film-hd.mp4", "size": 90000000, "length": 120, "source": "original"},
            {"name": "too-large.mp4", "size": library.INTERNET_ARCHIVE_MAX_VIDEO_BYTES + 1, "length": 120},
            {"name": "too-long.mp4", "size": 90000000, "length": 7200},
            {"name": "../unsafe.mp4", "size": 1000000, "length": 30},
        ]
        picked = library.internet_archive_choose_video_file(rows)
        self.assertEqual(picked["file"]["name"], "film-hd.mp4")
        self.assertEqual(picked["duration_seconds"], 120)
        self.assertIsNone(library.internet_archive_choose_video_file([
            {"name": "unknown-duration.mp4", "size": 90000000, "source": "original"}
        ]))
        self.assertIsNone(library.internet_archive_choose_video_file([
            {"name": "malformed-duration.mp4", "size": 90000000, "length": "not-a-duration"}
        ]))
        self.assertIsNone(library.internet_archive_choose_video_file([
            {"name": "too-long.mp4", "size": 90000000,
             "length": library.INTERNET_ARCHIVE_MAX_DURATION_SECONDS + 0.01}
        ]))
        self.assertIsNotNone(library.internet_archive_choose_video_file([
            {"name": "at-limit.mp4", "size": 90000000,
             "length": library.INTERNET_ARCHIVE_MAX_DURATION_SECONDS}
        ]))

    def test_internet_archive_direct_download_is_pinned_to_identifier_and_filename(self):
        self.assertTrue(library.internet_archive_file_url_is_allowed(
            "https://archive.org/download/AboutBan1935/AboutBan1935.mp4",
            "AboutBan1935", "AboutBan1935.mp4"))
        self.assertFalse(library.internet_archive_file_url_is_allowed(
            "https://archive.org/download/OtherItem/AboutBan1935.mp4",
            "AboutBan1935", "AboutBan1935.mp4"))
        self.assertFalse(library.internet_archive_file_url_is_allowed(
            "https://archive.org/download/AboutBan1935/../escape.mp4",
            "AboutBan1935", "../escape.mp4"))
        self.assertFalse(library.internet_archive_file_url_is_allowed(
            "https://evil.example/download/AboutBan1935/AboutBan1935.mp4",
            "AboutBan1935", "AboutBan1935.mp4"))

    def test_internet_archive_duration_and_mp4_signature_validation(self):
        self.assertEqual(library.internet_archive_parse_duration("18:47"), 1127)
        self.assertEqual(library.internet_archive_parse_duration("664.03"), 664.03)
        self.assertIsNone(library.internet_archive_parse_duration("unknown"))
        self.assertTrue(library.internet_archive_media_signature_is_valid(
            b"\x00\x00\x00\x18ftypisom" + b"x" * 20000, ".mp4", "video/mp4"))
        self.assertFalse(library.internet_archive_media_signature_is_valid(
            b"<html>blocked</html>" + b"x" * 20000, ".mp4", "text/html"))

    def test_internet_archive_search_url_uses_bounded_collection_and_start_offset(self):
        url = library.internet_archive_search_url("prelinger", 100)
        parsed = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "archive.org")
        self.assertIn("collection:prelinger", query["q"][0])
        self.assertIn("licenseurl:http*publicdomain*", query["q"][0])
        self.assertIn("licenseurl:http*cc0*", query["q"][0])
        self.assertEqual(query["start"], ["100"])
        with self.assertRaises(ValueError):
            library.internet_archive_search_url("unknown", 0)
        with self.assertRaises(ValueError):
            library.internet_archive_search_url("nasa", -1)
        self.assertEqual(query["rows"], [str(library.INTERNET_ARCHIVE_SEARCH_ROWS)])

class NOAAMultimediaRightsAndParsingTests(unittest.TestCase):
    IMAGE_URL = "https://oceanexplorer.noaa.gov/wp-content/uploads/2025/08/sample-image.jpg"
    VIDEO_URL = "https://oceanexplorer.noaa.gov/wp-content/uploads/2025/08/sample-video-1280x720.mp4"

    def test_noaa_listing_parser_reads_only_official_multimedia_card_links(self):
        page = f"""<html><body>
        <div class="component-cards-posts__main">
          <div class="component-cards-posts__initial">
            <div class="element-card-compact"><a href="https://oceanexplorer.noaa.gov/multimedia/octopus-dive/">Octopus</a></div>
            <div class="element-card-compact"><a href="/multimedia/deep-sea-coral/">Coral</a></div>
          </div>
        </div>
        <div class="sidebar"><a href="https://oceanexplorer.noaa.gov/multimedia/not-a-card/">Sidebar</a></div>
        <a href="https://example.com/multimedia/external/">External</a>
        </body></html>"""
        self.assertEqual(
            library.noaa_parse_listing_page(page),
            [
                "https://oceanexplorer.noaa.gov/multimedia/octopus-dive/",
                "https://oceanexplorer.noaa.gov/multimedia/deep-sea-coral/",
            ],
        )

    def test_noaa_detail_parser_extracts_title_caption_credit_and_hd_download(self):
        page = f"""<html><head><meta property="og:title" content="Deep Ocean Discovery"></head><body>
        <div class="component-multimedia-post__type eyebrow">video</div>
        <div class="component-multimedia-post__heading h2">Deep Ocean Discovery</div>
        <div class="component-multimedia-post__content content-formatted">An ROV explores a deep-sea coral habitat.</div>
        <div class="component-multimedia-post__details"><div class="content-stack">
          <div class="meta-pair"><div class="eyebrow">Credit</div><p>NOAA Ocean Exploration, Example Expedition</p></div>
          <div class="meta-pair"><div class="eyebrow">Download</div><p>
            <a class="text-download" href="{self.VIDEO_URL}">HD version (mp4)</a>
          </p></div>
        </div></div></body></html>"""
        detail = library.noaa_parse_detail_page(page)
        self.assertEqual(detail["title"], "Deep Ocean Discovery")
        self.assertEqual(detail["media_type"], "video")
        self.assertIn("ROV explores", detail["caption"])
        self.assertEqual(detail["credit"], "NOAA Ocean Exploration, Example Expedition")
        self.assertEqual(detail["downloads"][0]["url"], self.VIDEO_URL)
        self.assertFalse(detail["copyright_marker"])

    def test_noaa_copyright_marker_is_case_insensitive_and_blocks_item(self):
        page = """<html><body>
        <div class="component-multimedia-post__heading">Partner Footage</div>
        <div class="component-multimedia-post__type">video</div>
        <div class="component-multimedia-post__content content-formatted">Copyright © Partner Studio. Used by permission.</div>
        <div class="component-multimedia-post__details"><div class="meta-pair">
        <div class="eyebrow">Credit</div><p>NOAA Ocean Exploration</p></div></div>
        </body></html>"""
        detail = library.noaa_parse_detail_page(page)
        self.assertTrue(detail["copyright_marker"])

    def test_noaa_download_allowlist_is_official_and_media_type_specific(self):
        self.assertTrue(library.noaa_detail_page_is_allowed("https://oceanexplorer.noaa.gov/multimedia/octopus-dive/"))
        self.assertFalse(library.noaa_detail_page_is_allowed("https://example.com/multimedia/octopus-dive/"))
        self.assertTrue(library.noaa_media_download_url_is_allowed(self.IMAGE_URL, "image"))
        self.assertTrue(library.noaa_media_download_url_is_allowed(self.VIDEO_URL, "video"))
        self.assertFalse(library.noaa_media_download_url_is_allowed("https://example.com/wp-content/uploads/a.jpg", "image"))
        self.assertFalse(library.noaa_media_download_url_is_allowed("http://oceanexplorer.noaa.gov/wp-content/uploads/a.mp4", "video"))
        self.assertFalse(library.noaa_media_download_url_is_allowed(self.VIDEO_URL, "image"))

    def test_noaa_magic_bytes_reject_html_and_accept_jpeg_mp4(self):
        self.assertTrue(library.noaa_media_signature_is_valid(b"\xff\xd8\xff" + b"x" * 64, "image", "image/jpeg", ".jpg"))
        self.assertTrue(library.noaa_media_signature_is_valid(b"\x00\x00\x00\x18ftypisom" + b"x" * 20000, "video", "video/mp4", ".mp4"))
        self.assertFalse(library.noaa_media_signature_is_valid(b"<html>blocked</html>", "image", "text/html", ".jpg"))
        self.assertFalse(library.noaa_media_signature_is_valid(b"<html>blocked</html>", "video", "text/html", ".mp4"))

    def test_usgs_singular_type_map_keeps_audio_correct(self):
        self.assertEqual(library.usgs_singular_media_type("images"), "image")
        self.assertEqual(library.usgs_singular_media_type("videos"), "video")
        self.assertEqual(library.usgs_singular_media_type("audio"), "audio")
        with self.assertRaises(ValueError):
            library.usgs_singular_media_type("unknown")


class OriginalSFXIntegrityTests(unittest.TestCase):
    def test_sfx_index_digest_matches_complete_wav_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            index = []
            count = sfx_library.generate_original_audio(root, index, library.CC0_URL)
            self.assertGreater(count, 0)
            self.assertEqual(count, len(index))
            for item in index:
                audio_path = root / item["path"]
                self.assertTrue(audio_path.is_file())
                self.assertEqual(item["sha256"], library.sha256_path(audio_path), item["path"])
                self.assertEqual(item["size_bytes"], audio_path.stat().st_size)


class OriginalStickerMemeLibraryTests(unittest.TestCase):
    def test_sticker_meme_and_caption_packs_generate_large_original_cc0_families(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = []
            counts = sticker_meme.generate_assets(Path(tmp), index)
            self.assertGreaterEqual(counts["stickers"], 200)
            self.assertGreaterEqual(counts["meme_templates"], 70)
            self.assertGreaterEqual(counts["caption_overlays"], 60)
            self.assertEqual(counts["total"], len(index))
            self.assertGreaterEqual(len(index), 330)
            self.assertTrue(all(item.get("license") == "CC0-1.0" and item.get("original_artwork") is True for item in index))
            for item in index:
                path = Path(tmp) / item["path"]
                self.assertTrue(path.is_file())
                xml = path.read_text(encoding="utf-8")
                ET.fromstring(xml)
                self.assertNotIn("<script", xml.lower())
                self.assertNotRegex(xml.lower(), r"\s(?:href|src)\s*=\s*['\"](?:https?:|//|data:)")
            self.assertTrue(any("meme" in item["category"] for item in index))
            self.assertTrue(any("caption" in item["category"] for item in index))
            self.assertTrue(any("stickers" in item["category"] for item in index))


class USGSGalleryRightsAndParsingTests(unittest.TestCase):
    IMAGE_URL = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/sample.jpg"
    AUDIO_URL = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/audio/sample.mp3"
    VIDEO_URL = "https://usgs-ocapsv2-public-input-media.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/video/sample.mp4"

    def test_usgs_rights_gate_requires_exact_item_level_public_domain_label(self):
        self.assertTrue(library.usgs_rights_are_public_domain("Public Domain."))
        self.assertTrue(library.usgs_rights_are_public_domain(" public domain "))
        self.assertFalse(library.usgs_rights_are_public_domain(""))
        self.assertFalse(library.usgs_rights_are_public_domain("Copyrighted"))
        self.assertFalse(library.usgs_rights_are_public_domain("Public Domain. Third-party material used with permission."))
        self.assertFalse(library.usgs_rights_are_public_domain("Public Domain with restrictions"))
        self.assertFalse(library.usgs_rights_are_public_domain("CC BY 4.0"))

    def test_usgs_same_title_items_get_stable_distinct_output_slugs(self):
        title = "Aerial Image of the Southwest Rift Zone Eruption of Kilauea"
        item_a = "https://www.usgs.gov/media/images/southwest-rift-zone-01"
        item_b = "https://www.usgs.gov/media/images/southwest-rift-zone-02"
        slug_a = library.usgs_asset_item_slug(title, item_a)
        slug_a_again = library.usgs_asset_item_slug(title, item_a)
        slug_b = library.usgs_asset_item_slug(title, item_b)
        self.assertEqual(slug_a, slug_a_again)
        self.assertNotEqual(slug_a, slug_b)
        self.assertRegex(slug_a, r"^aerial-image-of-the-southwest-rift-zone-eruption-of-kilauea-[0-9a-f]{12}$")

    def test_usgs_item_ids_are_url_hashed_and_type_scoped(self):
        item_a = "https://www.usgs.gov/media/images/southwest-rift-zone-01"
        item_a_with_slash = item_a + "/"
        item_b = "https://www.usgs.gov/media/images/southwest-rift-zone-02"
        image_id = library.usgs_asset_item_id("images", item_a)
        self.assertEqual(image_id, library.usgs_asset_item_id("images", item_a_with_slash))
        self.assertNotEqual(image_id, library.usgs_asset_item_id("images", item_b))
        self.assertNotEqual(image_id, library.usgs_asset_item_id("videos", item_a))
        self.assertRegex(image_id, r"^usgs-images-[0-9a-f]{16}$")

    def test_usgs_direct_media_allowlist_binds_exact_host_and_type_path(self):
        self.assertTrue(library.usgs_media_detail_url_is_allowed(self.IMAGE_URL, "images"))
        self.assertTrue(library.usgs_media_detail_url_is_allowed(self.AUDIO_URL, "audio"))
        self.assertTrue(library.usgs_media_detail_url_is_allowed(self.VIDEO_URL, "videos"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed("https://example.com/media/images/sample.jpg", "images"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed("https://d9-wret.s3.us-west-2.amazonaws.com/styles/large/media/images/sample.jpg", "images"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed("http://d9-wret.s3.us-west-2.amazonaws.com/assets/media/images/sample.jpg", "images"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed(self.AUDIO_URL, "images"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed(self.VIDEO_URL, "audio"))
        self.assertFalse(library.usgs_media_detail_url_is_allowed("https://user@d9-wret.s3.us-west-2.amazonaws.com/media/images/sample.jpg", "images"))

    def test_usgs_detail_parser_requires_section_label_and_extracts_original_media(self):
        page = f"""<html><head><meta property="og:title" content="USGS sample item"><meta name="description" content="A sample science image"></head>
        <body><h1>USGS sample item</h1><section class="source"><h3>Sources/Usage</h3><p>Public Domain.</p></section>
        <a href="{self.IMAGE_URL}">Original</a></body></html>"""
        detail = library.usgs_parse_media_detail(page, "images")
        self.assertEqual(detail["title"], "USGS sample item")
        self.assertEqual(detail["rights_statement"], "Public Domain.")
        self.assertTrue(library.usgs_rights_are_public_domain(detail["rights_statement"]))
        self.assertEqual(detail["direct_media_urls"], [self.IMAGE_URL])

    def test_usgs_gallery_parser_only_accepts_official_media_item_paths(self):
        page = """<html><a href="/media/images/volcano-image">image</a>
        <a href="/media/videos/volcano-video">video</a>
        <a href="https://example.com/media/images/nope">external</a></html>"""
        image_candidates = library.usgs_page_detail_candidates(page, "images")
        video_candidates = library.usgs_page_detail_candidates(page, "videos")
        audio_candidates = library.usgs_page_detail_candidates(page, "audio")
        self.assertEqual(image_candidates, ["https://www.usgs.gov/media/images/volcano-image"])
        self.assertEqual(video_candidates, ["https://www.usgs.gov/media/videos/volcano-video"])
        self.assertEqual(audio_candidates, [])

    def test_usgs_media_signatures_reject_html_and_accept_expected_magic(self):
        self.assertTrue(library.usgs_media_signature_is_valid(b"\xff\xd8\xff" + b"x" * 64, "images", "image/jpeg", ".jpg"))
        self.assertTrue(library.usgs_media_signature_is_valid(b"RIFF" + b"x" * 4 + b"WAVE" + b"x" * 32, "audio", "audio/wav", ".wav"))
        self.assertTrue(library.usgs_media_signature_is_valid(b"\x00\x00\x00\x18ftypisom" + b"x" * 20000, "videos", "video/mp4", ".mp4"))
        self.assertFalse(library.usgs_media_signature_is_valid(b"<html>blocked</html>", "images", "text/html", ".jpg"))
        self.assertFalse(library.usgs_media_signature_is_valid(b"<html>blocked</html>", "videos", "text/html", ".mp4"))


class RightsGateTests(unittest.TestCase):
    def test_smithsonian_requires_cc0_for_record_and_exact_media(self):
        self.assertTrue(library.smithsonian_rights_are_cc0("CC0", "CC0"))
        self.assertTrue(library.smithsonian_rights_are_cc0(" cc0 ", " CC0 "))
        self.assertFalse(library.smithsonian_rights_are_cc0("CC0", "Usage conditions apply"))
        self.assertFalse(library.smithsonian_rights_are_cc0("Usage conditions apply", "CC0"))
        self.assertFalse(library.smithsonian_rights_are_cc0(None, "CC0"))
        self.assertFalse(library.smithsonian_rights_are_cc0("CC0", None))

    def test_smithsonian_retry_delay_honors_retry_after_and_rate_limit_reset(self):
        self.assertEqual(
            library.smithsonian_retry_delay_seconds({"Retry-After": "9"}, 0, 429),
            9.0,
        )
        now = datetime(2026, 10, 30, 12, 0, tzinfo=timezone.utc)
        reset = str(int(now.timestamp() + 17))
        self.assertEqual(
            library.smithsonian_retry_delay_seconds(
                {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": reset},
                0, 429, now=now,
            ),
            18.0,
        )
        self.assertEqual(library.smithsonian_retry_delay_seconds({}, 1, 429), 120.0)
        self.assertEqual(library.smithsonian_retry_delay_seconds({}, 1, 503), 10.0)

    def test_smithsonian_request_retries_429_then_recovers_without_network(self):
        url = "https://api.si.edu/openaccess/api/v1.0/search?q=unit_code%3ANMNH"
        limited = urllib.error.HTTPError(
            url, 429, "Too Many Requests", {"Retry-After": "7"}, None
        )
        expected = {"response": {"rows": []}}
        with mock.patch.object(library, "request_json", side_effect=[limited, expected]) as request:
            with mock.patch.object(library.time, "sleep") as sleep:
                self.assertEqual(library.smithsonian_request_json(url), expected)
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(7.0)

    def test_smithsonian_request_does_not_retry_permanent_http_errors(self):
        url = "https://api.si.edu/openaccess/api/v1.0/search?q=unit_code%3ANMNH"
        denied = urllib.error.HTTPError(url, 401, "Unauthorized", {}, None)
        with mock.patch.object(library, "request_json", side_effect=denied):
            with mock.patch.object(library.time, "sleep") as sleep:
                with self.assertRaises(urllib.error.HTTPError):
                    library.smithsonian_request_json(url)
        sleep.assert_not_called()

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
        self.assertGreaterEqual(len(library.ICONS), 125)
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


class ParallelAssetSourceLaneTests(unittest.TestCase):
    def test_source_lanes_run_concurrently_and_merge_indexes_in_declared_order(self):
        import threading

        barrier = threading.Barrier(2)
        shared_index = []

        def make_lane(source_name):
            def run(_root, local_index):
                barrier.wait(timeout=5)
                local_index.append({"id": source_name})
                return [{"id": source_name, "status": "downloaded"}]

            return run

        lanes = [
            ("first", make_lane("first")),
            ("second", make_lane("second")),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            reports = library.run_parallel_source_lanes(
                Path(tmp), shared_index, lanes, max_workers=2
            )

        self.assertEqual(reports["first"][0]["status"], "downloaded")
        self.assertEqual(reports["second"][0]["status"], "downloaded")
        self.assertEqual([entry["id"] for entry in shared_index], ["first", "second"])




class DistributedAssetLibraryTests(unittest.TestCase):
    def _asset(self, root, relative, asset_id):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((asset_id + "-verified-content").encode("utf-8"))
        return {
            "id": asset_id,
            "path": relative,
            "type": "nasa-video",
            "title": asset_id,
            "license": "Public Domain",
            "license_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
            "redistributable": True,
            "size_bytes": path.stat().st_size,
            "sha256": library.sha256_path(path),
        }

    def test_volume_is_uploaded_before_source_files_are_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "video-asset-library"
            root.mkdir()
            assets = [
                self._asset(root, "third-party/nasa/video/one.mp4", "nasa-one"),
                self._asset(root, "third-party/nasa/video/two.mp4", "nasa-two"),
            ]
            volume_dir = Path(tmp) / "volumes"
            with mock.patch.object(shard_builder, "upload_release_asset") as upload:
                rows = shard_builder.create_source_volumes(
                    root, volume_dir, "nasa", assets, bundle_packager, release_tag="test-release"
                )

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["source_lane"], "nasa")
            self.assertEqual(rows[0]["category"], "footage")
            self.assertTrue(rows[0]["uploaded_to_release"])
            self.assertEqual(len(rows[0]["sha256"]), 64)
            upload.assert_called_once()
            self.assertFalse((root / assets[0]["path"]).exists())
            self.assertFalse((root / assets[1]["path"]).exists())
            self.assertFalse((volume_dir / rows[0]["name"]).exists())

    def test_failed_volume_upload_keeps_original_source_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "video-asset-library"
            root.mkdir()
            asset = self._asset(root, "third-party/nasa/video/one.mp4", "nasa-one")
            volume_dir = Path(tmp) / "volumes"
            with mock.patch.object(
                shard_builder, "upload_release_asset", side_effect=RuntimeError("upload rejected")
            ):
                with self.assertRaisesRegex(RuntimeError, "upload rejected"):
                    shard_builder.create_source_volumes(
                        root, volume_dir, "nasa", [asset], bundle_packager, release_tag="test-release"
                    )
            self.assertTrue((root / asset["path"]).is_file())

    def test_global_catalog_renders_metadata_for_volumes_already_uploaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "video-asset-library"
            root.mkdir()
            asset = {
                "id": "mars-rover-shot",
                "path": "third-party/nasa/video/mars-rover.mp4",
                "type": "nasa-video",
                "title": "Mars rover exploration footage",
                "license": "Public Domain",
                "source_page": "https://images.nasa.gov/",
                "license_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
                "size_bytes": 123456,
                "sha256": "a" * 64,
                "redistributable": True,
            }
            library.make_asset_catalog(root, [asset], {"indexed_asset_count": 1})
            catalog = (root / "ASSET_CATALOG.html").read_text(encoding="utf-8")
            self.assertIn("Mars rover exploration footage", catalog)
            self.assertIn("third-party/nasa/video/mars-rover.mp4", catalog)
            self.assertIn("121 KB", catalog)

    def test_shard_merge_verifies_volume_coverage_and_exact_license_metadata(self):
        def make_shard(lane, asset_id, relative, payload):
            digest = hashlib.sha256(payload).hexdigest()
            asset = {
                "id": asset_id,
                "path": relative,
                "type": "original-svg-background",
                "license": "CC0-1.0",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "redistributable": True,
                "size_bytes": len(payload),
                "sha256": digest,
            }
            return {
                "lane": lane,
                "summary": {"indexed_asset_count": 1},
                "source_report": [],
                "assets": [asset],
                "file_checksums": [{"path": relative, "size_bytes": len(payload), "sha256": digest}],
                "bundles": [{
                    "name": f"video-assets-{lane}-original-graphics-001.zip",
                    "sha256": "b" * 64,
                    "archive_bytes": 1024,
                    "uncompressed_bytes": len(payload),
                    "file_count": 1,
                    "paths": [relative],
                    "source_lane": lane,
                }],
            }

        merged = release_finalizer.merge_shard_manifests(
            [
                make_shard("one", "asset-one", "originals/one.svg", b"one"),
                make_shard("two", "asset-two", "originals/two.svg", b"two"),
            ],
            expected_lanes={"one", "two"},
        )
        self.assertEqual(merged["summary"]["indexed_asset_count"], 2)
        self.assertEqual(merged["summary"]["indexed_resource_bytes"], 6)
        self.assertEqual(len(merged["bundles"]), 2)
        self.assertEqual(merged["assets"][0]["license"], "CC0-1.0")

    def test_shard_merge_rejects_duplicate_resource_paths(self):
        digest = "a" * 64
        asset = {
            "id": "same-asset",
            "path": "third-party/shared/asset.bin",
            "license": "CC0-1.0",
            "redistributable": True,
            "size_bytes": 3,
            "sha256": digest,
        }
        shard = {
            "lane": "one",
            "summary": {},
            "source_report": [],
            "assets": [asset],
            "file_checksums": [{"path": asset["path"], "size_bytes": 3, "sha256": digest}],
            "bundles": [{
                "name": "video-assets-one-misc-001.zip",
                "sha256": "b" * 64,
                "archive_bytes": 1024,
                "uncompressed_bytes": 3,
                "file_count": 1,
                "paths": [asset["path"]],
            }],
        }
        second_shard = {
            **shard,
            "lane": "two",
            "assets": [{**asset, "id": "other-asset"}],
            "bundles": [{
                    "name": "video-assets-two-misc-001.zip",
                    "sha256": "c" * 64,
                    "archive_bytes": 1024,
                    "uncompressed_bytes": 3,
                    "file_count": 1,
                    "paths": [asset["path"]],
                }],
        }
        with self.assertRaisesRegex(RuntimeError, "Duplicate asset path"):
            release_finalizer.merge_shard_manifests(
                [shard, second_shard], expected_lanes={"one", "two"}
            )



class ReleaseLookupTests(unittest.TestCase):
    def test_release_lookup_finds_draft_in_release_collection(self):
        releases = [
            {"id": 5, "tag_name": "older", "draft": False, "assets": []},
            {"id": 42, "tag_name": "draft-build", "draft": True, "assets": []},
        ]
        with mock.patch.object(release_finalizer, "_run_gh_json", return_value=releases) as gh:
            release = release_finalizer.release_by_tag("Nolane-x/video", "draft-build")
        self.assertEqual(release["id"], 42)
        self.assertTrue(release["draft"])
        gh.assert_called_once_with([
            "gh", "api", "repos/Nolane-x/video/releases?per_page=100"
        ])

    def test_release_lookup_fails_clearly_when_tag_is_not_listed(self):
        with mock.patch.object(
            release_finalizer, "_run_gh_json",
            return_value=[{"id": 5, "tag_name": "other", "draft": True, "assets": []}],
        ):
            with self.assertRaisesRegex(RuntimeError, "not found in the first 100"):
                release_finalizer.release_by_tag("Nolane-x/video", "missing-tag")


class ReleaseAssetVerificationTests(unittest.TestCase):
    def test_release_verification_requires_all_uploaded_asset_hashes_and_sizes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundle_path = root / "video-assets-nasa-footage-001.zip"
            manifest_path = root / "asset-shard--nasa.json"
            metadata_path = root / "ASSET_INDEX.json"
            bundle_path.write_bytes(b"zip-like-bundle-payload")
            manifest_path.write_bytes(b'{"lane":"nasa"}')
            metadata_path.write_bytes(b'{"assets":[]}')

            expected_rows = [
                (bundle_path.name, bundle_path.stat().st_size, hashlib.sha256(bundle_path.read_bytes()).hexdigest()),
                (manifest_path.name, manifest_path.stat().st_size, hashlib.sha256(manifest_path.read_bytes()).hexdigest()),
                (metadata_path.name, metadata_path.stat().st_size, hashlib.sha256(metadata_path.read_bytes()).hexdigest()),
            ]
            remote_assets = [
                {"name": name, "size": size, "digest": "sha256:" + digest}
                for name, size, digest in expected_rows
            ]
            with mock.patch.object(
                release_finalizer, "_run_gh_json",
                return_value=[{"id": 42, "tag_name": "draft-build", "draft": True, "assets": remote_assets}],
            ):
                result = release_finalizer.verify_release_assets(
                    "Nolane-x/video",
                    "draft-build",
                    {"bundles": [{"name": expected_rows[0][0], "archive_bytes": expected_rows[0][1], "sha256": expected_rows[0][2]}]},
                    [metadata_path],
                    [manifest_path],
                )

            self.assertEqual(result["verified_assets"], 3)
            self.assertTrue(result["all_remote_names_exact"])
            self.assertTrue(result["github_sha256_verified"])

    def test_release_verification_rejects_stale_or_unexpected_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "asset-shard--nasa.json"
            metadata_path = root / "ASSET_INDEX.json"
            manifest_path.write_bytes(b'{"lane":"nasa"}')
            metadata_path.write_bytes(b'{"assets":[]}')
            expected = [
                (path.name, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
                for path in (manifest_path, metadata_path)
            ]
            remote_assets = [
                {"name": name, "size": size, "digest": "sha256:" + digest}
                for name, size, digest in expected
            ]
            remote_assets.append({"name": "video-assets-stale.zip", "size": 1, "digest": "sha256:" + "0" * 64})
            with mock.patch.object(
                release_finalizer, "_run_gh_json",
                return_value=[{"id": 42, "tag_name": "draft-build", "draft": True, "assets": remote_assets}],
            ):
                with self.assertRaisesRegex(RuntimeError, "unexpected/stale"):
                    release_finalizer.verify_release_assets(
                        "Nolane-x/video",
                        "draft-build",
                        {"bundles": []},
                        [metadata_path],
                        [manifest_path],
                    )

    def test_release_verification_rejects_missing_github_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "asset-shard--nasa.json"
            metadata_path = root / "ASSET_INDEX.json"
            manifest_path.write_bytes(b'{"lane":"nasa"}')
            metadata_path.write_bytes(b'{"assets":[]}')
            remote_assets = [
                {"name": path.name, "size": path.stat().st_size, "digest": ""}
                for path in (manifest_path, metadata_path)
            ]
            with mock.patch.object(
                release_finalizer, "_run_gh_json",
                return_value=[{"id": 42, "tag_name": "draft-build", "draft": True, "assets": remote_assets}],
            ):
                with self.assertRaisesRegex(RuntimeError, "SHA-256 digest is missing"):
                    release_finalizer.verify_release_assets(
                        "Nolane-x/video",
                        "draft-build",
                        {"bundles": []},
                        [metadata_path],
                        [manifest_path],
                    )



class ExactDuplicateAssetRecordTests(unittest.TestCase):
    def test_identical_duplicate_asset_records_are_deduplicated_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            relative = "originals/icons/map-route.svg"
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"<svg>original map route</svg>")
            asset = {
                "id": "map-route",
                "path": relative,
                "type": "original-svg-icon",
                "license": "CC0-1.0",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "redistributable": True,
            }

            with mock.patch.object(library, "sha256_path", wraps=library.sha256_path):
                validated, checksums, deduplicated = shard_builder._validate_and_hash_assets(
                    library, root, [dict(asset), dict(asset)]
                )

            self.assertEqual(len(validated), 1)
            self.assertEqual(len(checksums), 1)
            self.assertEqual(deduplicated, 1)
            self.assertEqual(validated[0]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_conflicting_path_reuse_is_still_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            relative = "third-party/source/asset.bin"
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"verified bytes")
            first = {
                "id": "asset-one",
                "path": relative,
                "type": "source-file",
                "license": "CC0-1.0",
                "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                "redistributable": True,
            }
            second = {**first, "id": "asset-two"}
            with self.assertRaisesRegex(RuntimeError, "Conflicting duplicate"):
                shard_builder._validate_and_hash_assets(library, root, [first, second])



class OriginalAssetNamespaceTests(unittest.TestCase):
    def test_original_asset_families_have_unique_namespaced_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "library"
            root.mkdir()
            entries = []
            library.generate_originals(root, entries)
            ids = [entry["id"] for entry in entries]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertIn("overlay-map-route", ids)
            self.assertIn("icon-map-route", ids)
            self.assertTrue(all(entry.get("redistributable") is True for entry in entries))



class NARABulkDatasetProbeTests(unittest.TestCase):
    def test_nara_video_url_allowlist_requires_exact_s3_bucket_and_mopix_mp4(self):
        allowed = "https://s3.amazonaws.com/NARAprodstorage/lz/mopix/111/lc/111-lc-53870.mp4"
        self.assertTrue(nara_probe.nara_video_object_url_is_allowed(allowed))
        self.assertFalse(nara_probe.nara_video_object_url_is_allowed("https://example.com/NARAprodstorage/lz/mopix/a.mp4"))
        self.assertFalse(nara_probe.nara_video_object_url_is_allowed("https://s3.amazonaws.com/other-bucket/lz/mopix/a.mp4"))
        self.assertFalse(nara_probe.nara_video_object_url_is_allowed("https://s3.amazonaws.com/NARAprodstorage/lz/stillpix/a.jpg"))
        self.assertFalse(nara_probe.nara_video_object_url_is_allowed("http://s3.amazonaws.com/NARAprodstorage/lz/mopix/a.mp4"))

    def test_nara_range_probe_reads_only_a_small_mp4_header(self):
        url = "https://s3.amazonaws.com/NARAprodstorage/lz/mopix/111/lc/111-lc-53870.mp4"
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 206
        response.headers = {
            "Content-Type": "video/mp4",
            "Content-Range": "bytes 0-63/292897920",
            "Content-Length": "64",
        }
        response.read.return_value = bytes.fromhex("000000186674797069736f6d") + b"x" * 52
        with mock.patch.object(nara_probe.urllib.request, "urlopen", return_value=response):
            result = nara_probe.probe_nara_mp4_range(url, 292897920)
        self.assertEqual(result["status"], "range-verified")
        self.assertEqual(result["http_status"], 206)
        self.assertTrue(result["mp4_ftyp_signature"])
        self.assertEqual(result["bytes_read"], 64)
        self.assertTrue(result["metadata_size_matches_remote"])
        self.assertEqual(result["remote_size_bytes"], 292897920)
        response.read.assert_called_once_with(65)

    def test_restriction_status_reads_only_an_explicit_status(self):
        self.assertEqual(nara_probe._restriction_status({"status": "Unrestricted"}), "Unrestricted")
        self.assertEqual(nara_probe._restriction_status({"restrictionStatus": "Unrestricted"}), "Unrestricted")
        self.assertEqual(nara_probe._restriction_status("Unrestricted"), "Unrestricted")
        self.assertEqual(nara_probe._restriction_status({"note": "unrestricted in a note"}), "")

    def test_iter_records_reads_record_objects_from_bulk_json_envelopes(self):
        document = {
            "body": {
                "hits": {
                    "hits": [
                        {"_source": {"record": {"levelOfDescription": "item", "title": "Test film"}}},
                        {"record": {"levelOfDescription": "item", "title": "Second film"}},
                    ]
                }
            }
        }
        records = list(nara_probe.iter_records(document))
        self.assertEqual([row["title"] for row in records], ["Test film", "Second film"])

    def test_summary_counts_only_items_with_both_unrestricted_rights_and_digital_objects(self):
        document = {
            "body": {
                "hits": {
                    "hits": [
                        {
                            "_source": {
                                "record": {
                                    "levelOfDescription": "item",
                                    "title": "Public-domain aviation film",
                                    "useRestriction": {"status": "Unrestricted"},
                                    "accessRestriction": {"status": "Unrestricted"},
                                    "audiovisual": "True",
                                    "generalRecordsTypes": ["Moving Images"],
                                    "digitalObjects": [{
                                        "objectFilename": "aviation-film.mp4",
                                        "objectUrl": "https://catalog.archives.gov/medialz/test/aviation-film.mp4",
                                        "objectFileSize": 123456789,
                                    }],
                                }
                            }
                        },
                        {
                            "record": {
                                "levelOfDescription": "item",
                                "title": "Restricted donor footage",
                                "useRestriction": {"status": "Restricted - Possibly"},
                                "accessRestriction": {"status": "Unrestricted"},
                                "generalRecordsTypes": ["Moving Images"],
                                "digitalObjects": [{
                                    "objectFilename": "restricted.mp4",
                                    "objectUrl": "https://catalog.archives.gov/medialz/test/restricted.mp4",
                                    "objectFileSize": 1000,
                                }],
                            }
                        },
                    ]
                }
            }
        }
        summary = nara_probe.summarize_metadata_file(
            json.dumps(document).encode("utf-8"), "342", "rg_342-0.json"
        )
        self.assertEqual(summary["records_seen"], 2)
        self.assertEqual(summary["item_records"], 2)
        self.assertEqual(summary["both_unrestricted"], 1)
        self.assertEqual(summary["item_records_with_both_rights_and_objects"], 1)
        self.assertEqual(summary["eligible_audiovisual_item_records"], 1)
        self.assertEqual(summary["eligible_audiovisual_items_with_objects"], 1)
        self.assertEqual(summary["eligible_video_objects"], 1)
        self.assertEqual(summary["eligible_video_object_bytes"], 123456789)
        self.assertEqual(summary["candidate_media_count"], 2)
        self.assertEqual(summary["sample_eligible_video_objects"][0]["object_url_host"], "catalog.archives.gov")
        self.assertNotIn("restricted.mp4", [x.get("object_filename") for x in summary["sample_eligible_video_objects"]])
        self.assertFalse("media_downloaded" in summary)




class NASASVSPublicDomainProbeTests(unittest.TestCase):
    def test_svs_movie_url_requires_the_official_vis_path_and_supported_video_type(self):
        self.assertTrue(
            nasa_svs_probe.svs_movie_url_is_allowed(
                "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/movie.mp4"
            )
        )
        self.assertTrue(
            nasa_svs_probe.svs_movie_url_is_allowed(
                "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/movie.webm"
            )
        )
        self.assertFalse(nasa_svs_probe.svs_movie_url_is_allowed("https://example.com/vis/movie.mp4"))
        self.assertFalse(nasa_svs_probe.svs_movie_url_is_allowed("https://svs.gsfc.nasa.gov/api/5101/"))
        self.assertTrue(nasa_svs_probe.svs_movie_url_is_allowed("http://svs.gsfc.nasa.gov/vis/movie.mp4"))
        self.assertEqual(nasa_svs_importer.normalize_svs_media_url("http://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/movie.mp4"), "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/movie.mp4")
        self.assertFalse(nasa_svs_probe.svs_movie_url_is_allowed("https://svs.gsfc.nasa.gov/vis/frame.tif"))
        self.assertIsNone(nasa_svs_importer.normalize_svs_media_url("https://svs.gsfc.nasa.gov.evil.example/vis/movie.mp4"))
        self.assertIsNone(nasa_svs_importer.normalize_svs_media_url("https://user@svs.gsfc.nasa.gov/vis/movie.mp4"))
        self.assertIsNone(nasa_svs_importer.normalize_svs_media_url("https://svs.gsfc.nasa.gov:444/vis/movie.mp4"))
        self.assertIsNone(nasa_svs_importer.normalize_svs_media_url("https://svs.gsfc.nasa.gov/api/5687/movie.mp4"))
        self.assertIsNone(nasa_svs_importer.normalize_svs_media_url("https://svs.gsfc.nasa.gov/vis/movie.mp4?redirect=1"))

    def test_svs_page_parser_finds_movies_and_detects_explicit_licensed_music_notes(self):
        page = {
            "id": 5101,
            "page_type": "Visualization",
            "progress": "Complete",
            "title": "Earth ocean visualization",
            "description": "An animated view of global ocean temperatures.",
            "studio": "SVS",
            "credits": [{"role": "Visualizer", "people": [{"name": "Test Author", "employer": "NASA/GSFC"}]}],
            "media_groups": [{
                "widget": "Video player",
                "description": "The animation shows sea surface temperature.",
                "items": [{
                    "instance": {
                        "url": "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/ocean.mp4",
                        "filename": "ocean.mp4",
                        "media_type": "Movie",
                        "width": 3840,
                        "height": 2160,
                    }
                }],
            }],
        }
        with mock.patch.object(nasa_svs_probe, "fetch_json", return_value=(page, 2048)):
            result, size = nasa_svs_probe.inspect_page(5101)
        self.assertEqual(size, 2048)
        self.assertEqual(result["status"], "inspected")
        self.assertEqual(result["allowlisted_movie_count"], 1)
        self.assertFalse(result["exception_flagged"])
        self.assertEqual(result["movie_samples"][0]["width"], 3840)
        self.assertTrue(result["movie_samples"][0]["url"].startswith("https://svs.gsfc.nasa.gov/"))

        page["media_groups"][0]["description"] = (
            "Music credit: this track is from a third-party production library."
        )
        with mock.patch.object(nasa_svs_probe, "fetch_json", return_value=(page, 2048)):
            flagged, _ = nasa_svs_probe.inspect_page(5101)
        self.assertTrue(flagged["exception_flagged"])
        self.assertTrue(flagged["public_domain_exception_markers"])

    def test_svs_mp4_range_probe_checks_magic_and_reads_only_header_bytes(self):
        url = "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/ocean.mp4"
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 206
        response.headers = {
            "Content-Type": "video/mp4",
            "Content-Range": "bytes 0-63/78000000",
        }
        response.read.return_value = bytes.fromhex("000000186674797069736f6d") + b"x" * 52
        with mock.patch.object(nasa_svs_probe.urllib.request, "urlopen", return_value=response):
            result = nasa_svs_probe.probe_movie_header(url)
        self.assertEqual(result["status"], "header-verified")
        self.assertTrue(result["signature_ok"])
        self.assertEqual(result["remote_size_bytes"], 78000000)
        self.assertEqual(result["bytes_read"], 64)
        response.read.assert_called_once_with(65)


    def test_nasa_svs_chooses_highest_resolution_and_rejects_music_notes(self):
        page = {
            "page_type": "Visualization", "progress": "Complete", "studio": "SVS",
            "main_video": {
                "url": "http://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/1080.mp4",
                "media_type": "Movie", "width": 1920, "height": 1080, "audio_track": None,
            },
            "media_groups": [{
                "caption": "A global science visualization.",
                "items": [
                    {"instance": {
                        "url": "http://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/4k.mp4",
                        "media_type": "Movie", "width": 3840, "height": 2160,
                    }},
                    {"instance": {
                        "url": "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005101/music.webm",
                        "media_type": "Movie", "width": 3840, "height": 2160, "audio_track": {"name": "licensed"},
                    }},
                ],
            }],
        }
        chosen, reason = nasa_svs_importer.choose_video_candidate(page)
        self.assertIsNotNone(chosen)
        self.assertTrue(chosen["url"].endswith("/4k.mp4"))
        self.assertIn("no page-level", reason)
        page["media_groups"][0]["items"][0]["caption"] = "Music credit: licensed soundtrack."
        chosen, reason = nasa_svs_importer.choose_video_candidate(page)
        self.assertIsNone(chosen)
        self.assertIn("third-party-music", reason)

    def test_nasa_svs_json_respects_per_request_byte_ceiling(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.headers = {"Content-Length": "11"}
        with mock.patch.object(nasa_svs_importer.urllib.request, "urlopen", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "exceeds response ceiling"):
                nasa_svs_importer._json("https://svs.gsfc.nasa.gov/api/search/", 10)
        response.read.assert_not_called()

    def test_nasa_svs_shard_lane_is_registered_and_packaged_as_footage(self):
        self.assertEqual(shard_builder.SOURCE_LANES["nasa-svs"], "download_nasa_svs_media")
        self.assertEqual(bundle_packager.classify_asset({
            "type": "nasa-svs-video",
            "path": "third-party/nasa-svs/video/5687-ocean.mp4",
        }), "footage")


class CumulativeAssetLibraryIndexTests(unittest.TestCase):
    def _release(self, tag, repository, assets, bundle_name):
        bundle_paths = [asset["path"] for asset in assets]
        bundle = {
            "name": bundle_name,
            "sha256": hashlib.sha256((tag + bundle_name).encode("utf-8")).hexdigest(),
            "archive_bytes": 1024,
            "uncompressed_bytes": sum(asset["size_bytes"] for asset in assets),
            "file_count": len(bundle_paths),
            "paths": bundle_paths,
        }
        return {
            "release_tag": tag,
            "repository": repository,
            "summary": {"indexed_resource_bytes": sum(asset["size_bytes"] for asset in assets)},
            "assets": assets,
            "bundles": [bundle],
        }

    def _asset(self, asset_id, path, payload, license_name="CC0-1.0"):
        return {
            "id": asset_id,
            "path": path,
            "type": "test-image",
            "provider": "Test Provider",
            "title": asset_id,
            "license": license_name,
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "source_page": "https://example.test/item/" + asset_id,
            "redistributable": True,
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }

    def test_identical_bytes_count_once_but_preserve_each_origin_and_license(self):
        payload_shared = b"same image content"
        payload_new = b"new unique footage payload"
        release_a = self._release(
            "video-asset-library-build-A",
            "Nolane-x/video",
            [
                self._asset("same-a", "third-party/a/shared.jpg", payload_shared, "CC0-1.0"),
                self._asset("old-only", "third-party/a/old.mp4", payload_new, "Public Domain"),
            ],
            "video-assets-a-media-001.zip",
        )
        release_b = self._release(
            "video-asset-library-build-B",
            "Nolane-x/video",
            [
                self._asset("same-b", "third-party/b/copy.jpg", payload_shared, "CC-BY-4.0"),
            ],
            "video-assets-b-media-001.zip",
        )

        merged = cumulative_index.merge_published_release_indexes([release_a, release_b])
        shared_digest = hashlib.sha256(payload_shared).hexdigest()
        shared = next(row for row in merged["assets"] if row["sha256"] == shared_digest)

        self.assertEqual(merged["summary"]["unique_resource_bytes"], len(payload_shared) + len(payload_new))
        self.assertEqual(merged["summary"]["unique_asset_count"], 2)
        self.assertEqual(merged["summary"]["release_asset_occurrences"], 3)
        self.assertEqual(merged["summary"]["duplicate_resource_occurrences"], 1)
        self.assertEqual(len(shared["origins"]), 2)
        self.assertEqual({origin["license"] for origin in shared["origins"]}, {"CC0-1.0", "CC-BY-4.0"})
        self.assertTrue(all(origin["download_url"].startswith("https://github.com/Nolane-x/video/releases/download/") for origin in shared["origins"]))
        self.assertEqual(merged["summary"]["source_release_count"], 2)

    def test_cumulative_index_rejects_same_sha_with_inconsistent_sizes(self):
        digest = hashlib.sha256(b"abc").hexdigest()
        first = {
            "id": "a", "path": "one/a.bin", "license": "CC0-1.0",
            "redistributable": True, "size_bytes": 3, "sha256": digest,
        }
        second = {
            "id": "b", "path": "two/b.bin", "license": "CC0-1.0",
            "redistributable": True, "size_bytes": 4, "sha256": digest,
        }
        a = self._release("release-a", "Nolane-x/video", [first], "bundle-a.zip")
        b = self._release("release-b", "Nolane-x/video", [second], "bundle-b.zip")
        with self.assertRaisesRegex(RuntimeError, "inconsistent byte sizes"):
            cumulative_index.merge_published_release_indexes([a, b])

    def test_cumulative_index_rejects_asset_not_covered_by_any_volume(self):
        asset = self._asset("a", "orphan/file.jpg", b"orphan")
        release = self._release("release-a", "Nolane-x/video", [asset], "bundle-a.zip")
        release["bundles"][0]["paths"] = ["different/file.jpg"]
        with self.assertRaisesRegex(RuntimeError, "does not package indexed asset"):
            cumulative_index.merge_published_release_indexes([release])

    def test_cumulative_index_rejects_duplicate_release_tags(self):
        asset = self._asset("a", "one/file.jpg", b"one")
        release = self._release("release-a", "Nolane-x/video", [asset], "bundle-a.zip")
        with self.assertRaisesRegex(RuntimeError, "Duplicate source release index"):
            cumulative_index.merge_published_release_indexes([release, release])

    def test_cumulative_index_writer_emits_index_and_download_map(self):
        asset = self._asset("a", "one/file.jpg", b"one")
        release = self._release("video-asset-library-build-A", "Nolane-x/video", [asset], "bundle-a.zip")
        merged = cumulative_index.merge_published_release_indexes([release])
        with tempfile.TemporaryDirectory() as tmp:
            index_path, downloads_path = cumulative_index.write_cumulative_index(merged, Path(tmp))
            index_doc = json.loads(index_path.read_text(encoding="utf-8"))
            downloads_doc = json.loads(downloads_path.read_text(encoding="utf-8"))
        self.assertEqual(index_doc["summary"]["unique_resource_bytes"], 3)
        self.assertEqual(downloads_doc["bundles"][0]["download_url"], "https://github.com/Nolane-x/video/releases/download/video-asset-library-build-A/bundle-a.zip")


if __name__ == "__main__":
    unittest.main(verbosity=2)
