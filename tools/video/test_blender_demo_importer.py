#!/usr/bin/env python3
"""Offline tests for the item-level CC0 Blender demo importer."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blender_demo_importer as importer  # noqa: E402
import build_asset_library_shard as shard_builder  # noqa: E402
import package_asset_bundles as bundle_packager  # noqa: E402


class BlenderDemoImporterTests(unittest.TestCase):
    def test_allowlist_has_unique_official_https_urls_and_cc0_titles(self):
        ids = [item["id"] for item in importer.ASSETS]
        urls = [item["url"] for item in importer.ASSETS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(urls), len(set(urls)))
        self.assertGreaterEqual(len(ids), 18)
        for item in importer.ASSETS:
            self.assertTrue(importer.official_blender_url_is_allowed(item["url"]), item["url"])
            self.assertTrue(item["title"])
            self.assertTrue(item["creator"])

    def test_catalog_parser_extracts_only_https_official_download_links(self):
        html = b"""
        <html><body>
          <a href="/download/demo/sample.blend">Sample Project</a>
          <p>Sample Project</p><p>by Blender Studio</p><p>CC0</p>
          <a href="https://evil.example/payload.zip">Not Blender</a>
        </body></html>
        """
        text, links = importer.catalog_text_and_links(html)
        self.assertIn("Sample Project", text)
        self.assertIn("https://www.blender.org/download/demo/sample.blend", links)
        self.assertIn("https://evil.example/payload.zip", links)

    def test_current_item_license_evidence_is_local_and_fails_closed(self):
        self.assertIsNotNone(importer.catalog_cc0_evidence(
            "Human Base Meshes v1.4.1 by Blender Studio 49 MB – CC0. Cube Diorama CC0",
            "Human Base Meshes v1.4.1",
        ))
        self.assertIsNone(importer.catalog_cc0_evidence(
            "Ellie Pose Library v2.0.0 by Blender Studio 24 MB – CC-BY. Later Sample Scene CC0",
            "Ellie Pose Library v2.0.0",
        ))
        self.assertIsNone(importer.catalog_cc0_evidence(
            "Cube Diorama by Blender Studio, license not specified",
            "Cube Diorama",
        ))
        self.assertIsNone(importer.catalog_cc0_evidence(
            "Later Sample Scene CC0",
            "Missing Title",
        ))

    def test_host_and_redirect_allowlists_are_https_and_exact(self):
        self.assertTrue(importer.official_blender_url_is_allowed(
            "https://www.blender.org/download/demo/sample.blend"
        ))
        self.assertTrue(importer.official_blender_url_is_allowed(
            "https://download.blender.org/demo/sample.blend"
        ))
        for url in (
            "http://www.blender.org/download/demo/sample.blend",
            "https://blender.org/download/demo/sample.blend",
            "https://www.blender.org.evil.example/download/demo/sample.blend",
            "https://www.blender.org:443/download/demo/sample.blend",
            "https://user@www.blender.org/download/demo/sample.blend",
        ):
            self.assertFalse(importer.official_blender_url_is_allowed(url), url)

    def test_blend_file_requires_binary_signature(self):
        kind, count = importer._validate_project_blob(
            "https://www.blender.org/download/demo/sample.blend",
            b"BLENDER-v300",
        )
        self.assertEqual(kind, "blender-demo-cc0-project")
        self.assertEqual(count, 1)
        with self.assertRaisesRegex(ValueError, "signature"):
            importer._validate_project_blob(
                "https://www.blender.org/download/demo/sample.blend",
                b"<html>not a project</html>",
            )

    def test_zip_bundle_requires_safe_blend_project_members(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("Scene/Main.blend", b"BLENDER-v300")
            archive.writestr("Scene/README.txt", "CC0 demo project")
        kind, count = importer._validate_project_blob(
            "https://www.blender.org/download/demo/sample.zip",
            output.getvalue(),
        )
        self.assertEqual(kind, "blender-demo-cc0-bundle")
        self.assertEqual(count, 1)

    def test_zip_bundle_rejects_traversal_and_missing_blend(self):
        traversal = io.BytesIO()
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr("../escape.blend", b"BLENDER-v300")
        with self.assertRaisesRegex(ValueError, "unsafe"):
            importer._validate_project_blob(
                "https://www.blender.org/download/demo/unsafe.zip",
                traversal.getvalue(),
            )
        no_project = io.BytesIO()
        with zipfile.ZipFile(no_project, "w") as archive:
            archive.writestr("README.txt", "not a Blender project")
        with self.assertRaisesRegex(ValueError, "does not contain"):
            importer._validate_project_blob(
                "https://www.blender.org/download/demo/no-project.zip",
                no_project.getvalue(),
            )

    def test_source_lane_and_bundle_category_are_registered(self):
        self.assertEqual(
            shard_builder.SOURCE_LANES["blender-demo-cc0"],
            "download_blender_demo_assets",
        )
        self.assertEqual(
            bundle_packager.classify_asset({
                "type": "blender-demo-cc0-bundle",
                "path": "third-party/blender-demo-cc0/human-base-meshes.zip",
            }),
            "3d-models",
        )
        self.assertEqual(
            bundle_packager.classify_asset({
                "type": "blender-demo-cc0-project",
                "path": "third-party/blender-demo-cc0/sample.blend",
            }),
            "3d-models",
        )

    def test_source_registry_clearly_records_cc0_only_policy(self):
        source_path = Path(__file__).resolve().parents[2] / "video-library/assets/sources.json"
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        source = next(item for item in payload["sources"] if item["id"] == "blender-demo-cc0")
        self.assertEqual(source["license"], "CC0-1.0")
        self.assertTrue(source["verified_page_license"])
        self.assertIn("CC-BY", source["note"])
        self.assertIn("per-item", source["bundling"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
