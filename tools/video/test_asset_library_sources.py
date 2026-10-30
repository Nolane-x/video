#!/usr/bin/env python3
"""Fast offline regression tests for source rights gates and generated asset families."""
from __future__ import annotations

import io
import sys
import tempfile
import tarfile
import unittest
import urllib.parse
from unittest import mock
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_asset_library as library  # noqa: E402
import generate_sticker_meme_library as sticker_meme  # noqa: E402
import package_asset_bundles as bundle_packager  # noqa: E402
import generate_sfx_library as sfx_library  # noqa: E402
import json



class ExternalSourceExpansionTests(unittest.TestCase):
    def test_external_source_ceilings_remain_expanded(self):
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["hdris"], 48)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["models"], 72)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["textures"], 160)
        self.assertGreaterEqual(library.MAX_POLY_FILE, 60 * 1024 * 1024)
        self.assertGreaterEqual(library.MAX_MEDIA_FILE, 12 * 1024 * 1024)
        self.assertGreaterEqual(library.MET_OPEN_ACCESS_IMAGE_CAP, 300)
        self.assertGreaterEqual(library.RIJKSMUSEUM_OPEN_ACCESS_IMAGE_CAP, 240)
        self.assertGreaterEqual(library.WIKIMEDIA_PUBLIC_DOMAIN_IMAGE_CAP, 800)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_SVG_CAP, 100)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_AUDIO_VIDEO_CAP, 100)
        self.assertEqual(sum(library.AMBIENTCG_SELECTION_CAPS.values()), 140)
        self.assertEqual(set(library.AMBIENTCG_SELECTION_CAPS), {"Material", "HDRI", "3DModel", "Decal", "Atlas", "PlainTexture", "Brush", "Substance"})
        self.assertGreaterEqual(library.AMBIENTCG_MAX_ARCHIVE_BYTES, 50 * 1024 * 1024)
        self.assertGreaterEqual(library.AMBIENTCG_MAX_TOTAL_UNPACKED_BYTES, 5 * 1024 * 1024 * 1024)
        self.assertEqual(library.LAZYTEXTURES_ASSET_CAPS, {"models": 10, "materials": 16, "hdris": 10, "textures": 18, "other": 8})
        self.assertEqual(library.LAZYTEXTURES_API_TYPES["other"]["endpoint"], "previewsOther")
        self.assertEqual(library.LAZYTEXTURES_MAX_ZIP_MEMBERS, 2500)
        self.assertEqual(library.LAZYTEXTURES_MAX_ARCHIVE_BYTES, 64 * 1024 * 1024)
        self.assertEqual(library.LAZYTEXTURES_MAX_TOTAL_ARCHIVE_BYTES, 512 * 1024 * 1024)
        self.assertGreaterEqual(library.LAZYTEXTURES_MAX_TOTAL_UNPACKED_BYTES, 1024 * 1024 * 1024)
        self.assertEqual(library.USGS_GALLERY_PAGE_SCAN_LIMIT, 18)
        self.assertEqual(library.USGS_SELECTION_CAPS, {"images": 80, "videos": 40, "audio": 24})
        self.assertGreaterEqual(library.USGS_TOTAL_MAX_BYTES, 6 * 1024 * 1024 * 1024)
        self.assertEqual(library.OPENGAMEART_SELECTION_CAPS, {"2d": 24, "3d": 24, "textures": 20, "sfx": 20, "music": 20})
        self.assertEqual(library.OPENGAMEART_SEARCH_PAGES_PER_TYPE, 5)
        self.assertEqual(library.OPENGAMEART_MAX_ITEM_PAGES_PER_TYPE, 48)
        self.assertGreaterEqual(library.OPENGAMEART_MAX_TOTAL_BYTES, 4 * 1024 * 1024 * 1024)
        self.assertEqual(library.NOAA_MEDIA_PAGE_SCAN_LIMIT, 20)
        self.assertEqual(library.NOAA_MEDIA_SELECTION_CAPS, {"image": 200, "video": 120})
        self.assertEqual(library.OPENMOJI_VERSION, "17.0.0")
        self.assertEqual(library.OPENMOJI_EXPECTED_FILE_COUNT, 11539)
        self.assertGreaterEqual(library.OPENMOJI_MAX_ARCHIVE_BYTES, 80 * 1024 * 1024)
        self.assertGreaterEqual(library.OPENMOJI_MAX_EXTRACTED_BYTES, 100 * 1024 * 1024)
        self.assertGreaterEqual(library.NOAA_TOTAL_MAX_BYTES, 8 * 1024 * 1024 * 1024)

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
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-models-asset-file", "path": "third-party/lazytextures/models/SpaceKit/model.fbx"}), "3d-models")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-materials-asset-file", "path": "third-party/lazytextures/materials/Concrete01/Color.png"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-hdris-asset-file", "path": "third-party/lazytextures/hdris/Studio/lighting.exr"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-textures-asset-file", "path": "third-party/lazytextures/textures/Rust/overlay.png"}), "3d-textures")
        self.assertEqual(bundle_packager.classify_asset({"type": "lazytextures-other-asset-file", "path": "third-party/lazytextures/other/Brush01/brush.png"}), "miscellaneous")

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
