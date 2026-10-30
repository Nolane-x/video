#!/usr/bin/env python3
"""Fast offline regression tests for source rights gates and generated asset families."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_asset_library as library  # noqa: E402



class ExternalSourceExpansionTests(unittest.TestCase):
    def test_external_source_ceilings_remain_expanded(self):
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["hdris"], 20)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["models"], 28)
        self.assertGreaterEqual(library.POLYHAVEN_SELECTION_LIMITS["textures"], 48)
        self.assertGreaterEqual(library.MET_OPEN_ACCESS_IMAGE_CAP, 110)
        self.assertGreaterEqual(library.RIJKSMUSEUM_OPEN_ACCESS_IMAGE_CAP, 90)
        self.assertGreaterEqual(library.WIKIMEDIA_PUBLIC_DOMAIN_IMAGE_CAP, 240)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_SVG_CAP, 60)
        self.assertGreaterEqual(library.WIKIMEDIA_CC0_AUDIO_VIDEO_CAP, 36)
        self.assertEqual(sum(library.AMBIENTCG_SELECTION_CAPS.values()), 30)
        self.assertEqual(set(library.AMBIENTCG_SELECTION_CAPS), {"Material", "HDRI", "3DModel", "Decal", "Atlas", "PlainTexture", "Brush", "Substance"})
        self.assertGreaterEqual(library.AMBIENTCG_MAX_ARCHIVE_BYTES, 20 * 1024 * 1024)
        self.assertGreaterEqual(library.AMBIENTCG_MAX_TOTAL_UNPACKED_BYTES, 250 * 1024 * 1024)
        self.assertEqual(library.USGS_GALLERY_PAGE_SCAN_LIMIT, 4)
        self.assertEqual(library.USGS_SELECTION_CAPS, {"images": 24, "videos": 8, "audio": 8})
        self.assertGreaterEqual(library.USGS_TOTAL_MAX_BYTES, 100 * 1024 * 1024)

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
