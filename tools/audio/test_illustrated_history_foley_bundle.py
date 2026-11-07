import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_illustrated_history_foley_bundle import build_bundle, safe_zip_extract


class IllustratedHistoryFoleyBundleTests(unittest.TestCase):
    def test_builds_provenance_rich_unapproved_catalog_and_zip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            downloads = root / "downloads"
            output = root / "output"
            source_id = "fixture-source"
            source_dir = downloads / source_id
            source_dir.mkdir(parents=True)
            archive_path = source_dir / "fixture.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("fixture/impact.wav", b"not-a-real-waveform-but-probe-is-mocked")
                archive.writestr("fixture/readme.txt", "not an audio file")
            manifest = {
                "collection": "Fixture CC0 Foley",
                "release_tag": "fixture-v0.0.1",
                "sources": [{
                    "source_id": source_id,
                    "title": "Fixture",
                    "creator": "Fixture Artist",
                    "source_page": "https://example.invalid/source",
                    "download_url": "https://example.invalid/fixture.zip",
                    "download_filename": "fixture.zip",
                    "archive_type": "zip",
                    "license": "CC0-1.0",
                    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                    "rights_class": "public_cc0_pd",
                    "tags": ["impact"],
                    "expected_sha256": None
                }]
            }

            def fake_probe(_path):
                return {
                    "duration_seconds": 0.5,
                    "container_format": "wav",
                    "codec": "pcm_s16le",
                    "sample_rate_hz": 48000,
                    "channels": 1,
                    "channel_layout": "mono",
                    "bits_per_sample": 16
                }

            report = build_bundle(manifest, downloads, output, probe=fake_probe)
            self.assertEqual(report["audio_asset_count"], 1)
            self.assertEqual(report["human_auditioned"], 0)
            self.assertEqual(report["approved_for_final_mix"], 0)
            catalog = json.loads((output / "package" / "catalog.json").read_text(encoding="utf-8"))
            asset = catalog["assets"][0]
            self.assertEqual(asset["license"], "CC0-1.0")
            self.assertEqual(asset["creator"], "Fixture Artist")
            self.assertFalse(asset["human_auditioned"])
            self.assertFalse(asset["approved_for_final_mix"])
            self.assertEqual(asset["duration_seconds"], 0.5)
            package = output / report["package"]
            self.assertTrue(package.is_file())
            with zipfile.ZipFile(package) as archive:
                self.assertIn("catalog.json", archive.namelist())
                self.assertIn("AUDIO_PREVIEW.html", archive.namelist())
                self.assertIn(asset["path"], archive.namelist())
                preview = archive.read("AUDIO_PREVIEW.html").decode("utf-8")
                self.assertIn("Foley + score audition & review console", preview)
                self.assertIn("Export decisions JSON", preview)
                self.assertIn("human_auditioned", preview)
                self.assertIn("approved_for_final_mix", preview)
                self.assertIn("localStorage", preview)
                self.assertIn("sha256", preview)
                self.assertIn("listen to this exact file", preview.lower())
                self.assertIn("reviewed", preview.lower())
                self.assertNotIn('approved_for_final_mix":true', preview)

    def test_review_console_contains_import_export_and_human_approval_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            downloads = root / "downloads"
            output = root / "output"
            source_id = "fixture-source"
            source_dir = downloads / source_id
            source_dir.mkdir(parents=True)
            with zipfile.ZipFile(source_dir / "fixture.zip", "w") as archive:
                archive.writestr("fixture/impact.wav", b"fixture-audio")
            manifest = {
                "collection": "Fixture CC0 Foley",
                "release_tag": "fixture-v0.0.2",
                "sources": [{
                    "source_id": source_id, "title": "Fixture", "creator": "Artist",
                    "source_page": "https://example.invalid/source",
                    "download_url": "https://example.invalid/file.zip",
                    "download_filename": "fixture.zip", "archive_type": "zip",
                    "license": "CC0-1.0",
                    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
                    "rights_class": "public_cc0_pd", "tags": ["impact"],
                    "expected_sha256": None
                }]
            }
            fake_probe = lambda _path: {
                "duration_seconds": 1.0, "container_format": "wav",
                "codec": "pcm_s16le", "sample_rate_hz": 48000,
                "channels": 1, "channel_layout": "mono", "bits_per_sample": 16
            }
            build_bundle(manifest, downloads, output, probe=fake_probe)
            preview = (output / "package" / "AUDIO_PREVIEW.html").read_text(encoding="utf-8")
            self.assertIn("Import previous review", preview)
            self.assertIn("Export decisions JSON", preview)
            self.assertIn("Next unreviewed", preview)
            self.assertIn("sha256", preview)
            self.assertIn("human_auditioned", preview)
            self.assertIn("approved_for_final_mix", preview)
            self.assertIn('disabled', preview)
            self.assertIn("listen to this exact file", preview.lower())

    def test_blocks_zip_path_traversal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            malicious = root / "bad.zip"
            with zipfile.ZipFile(malicious, "w") as archive:
                archive.writestr("../escape.wav", b"bad")
            with self.assertRaises(ValueError):
                safe_zip_extract(malicious, root / "out")


if __name__ == "__main__":
    unittest.main()
