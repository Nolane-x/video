#!/usr/bin/env python3
import hashlib
import importlib.util
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "video" / "build_squire_review_pack.py"
spec = importlib.util.spec_from_file_location("build_squire_review_pack", SCRIPT)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class SquireReviewPackTests(unittest.TestCase):
    def test_master_report_must_match_verified_240fps_contract_and_media_hash(self):
        with tempfile.TemporaryDirectory() as td:
            video = Path(td) / "master.mp4"
            video.write_bytes(b"verified-master-fixture")
            valid = {
                "status": "technical_pass",
                "fps": 240,
                "frames": 229896,
                "resolution": "1920x1080",
                "duration_seconds": 957.9,
                "final_bytes": video.stat().st_size,
                "final_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
                "artistic_signoff": "pending complete human watch/listen",
            }
            actual_probe = {
                "streams": [
                    {"codec_type": "video", "width": 1920, "height": 1080,
                     "r_frame_rate": "240/1", "avg_frame_rate": "240/1", "nb_frames": "229896"},
                    {"codec_type": "audio", "codec_name": "aac", "sample_rate": "48000", "channels": 2},
                ],
                "format": {"duration": "957.9"},
            }
            with patch.object(review, "ffprobe_json", return_value=actual_probe):
                review.validate_master_report(valid, video)
                for field, value in (("fps", 30), ("frames", 229895), ("resolution", "1280x720"),
                                     ("status", "failed"), ("final_sha256", "0" * 64)):
                    bad = dict(valid)
                    bad[field] = value
                    with self.subTest(field=field):
                        with self.assertRaises(ValueError):
                            review.validate_master_report(bad, video)

    def test_srt_parser_preserves_cue_timing_and_multiline_text(self):
        srt = """1
00:00:01,200 --> 00:00:03,500
The walls are still standing.

2
00:00:03,500 --> 00:00:05,000
But the city has almost
run out of strength.
"""
        cues = review.parse_srt(srt)
        self.assertEqual(len(cues), 2)
        self.assertAlmostEqual(cues[0]["start"], 1.2)
        self.assertAlmostEqual(cues[0]["end"], 3.5)
        self.assertEqual(cues[1]["text"], "But the city has almost run out of strength.")

    def test_shot_index_maps_timecoded_captions_to_each_shot(self):
        shots = [
            {"id": "s001", "start": 0.0, "end": 2.0, "tpl": "final_night", "args": {"beat": "wall"}},
            {"id": "s002", "start": 2.0, "end": 4.0, "tpl": "gun_crew", "args": {"moment": "load"}},
        ]
        cues = [
            {"start": 0.5, "end": 1.5, "text": "The walls are still standing."},
            {"start": 2.2, "end": 3.8, "text": "A crew prepares the next shot."},
        ]
        rows = review.build_shot_index(shots, cues)
        self.assertEqual([row["shot_id"] for row in rows], ["s001", "s002"])
        self.assertEqual(rows[0]["caption"], "The walls are still standing.")
        self.assertEqual(rows[1]["beat"], "load")
        self.assertAlmostEqual(rows[1]["duration_seconds"], 2.0)

    def test_master_actual_stream_metadata_must_match_240fps_delivery_contract(self):
        with tempfile.TemporaryDirectory() as td:
            video = Path(td) / "master.mp4"
            video.write_bytes(b"verified-master-fixture")
            report = {
                "status": "technical_pass", "fps": 240, "frames": 229896,
                "resolution": "1920x1080", "duration_seconds": 957.9,
                "final_bytes": video.stat().st_size,
                "final_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
            }
            good = {
                "streams": [
                    {"codec_type": "video", "width": 1920, "height": 1080,
                     "r_frame_rate": "240/1", "avg_frame_rate": "240001/1000", "nb_frames": "229896"},
                    {"codec_type": "audio", "codec_name": "aac", "sample_rate": "48000", "channels": 2},
                ], "format": {"duration": "957.9"},
            }
            with patch.object(review, "ffprobe_json", return_value=good):
                review.validate_master_report(report, video)
            for stream in (
                {**good["streams"][0], "r_frame_rate": "30/1"},
                {**good["streams"][0], "nb_frames": "229895"},
                {**good["streams"][0], "width": 1280},
            ):
                bad = {"streams": [stream, good["streams"][1]], "format": {"duration": "957.9"}}
                with patch.object(review, "ffprobe_json", return_value=bad):
                    with self.assertRaises(ValueError):
                        review.validate_master_report(report, video)

    def test_selected_master_run_artifact_and_commit_must_be_bound_together(self):
        valid = (43718146698, 14167018401,
                 "squire-constantinople-1453-redesign-240fps-43718146698", "a" * 40)
        review.validate_source_identity(*valid)
        invalid = [
            (0, valid[1], valid[2], valid[3]),
            (valid[0], 0, valid[2], valid[3]),
            (valid[0], valid[1], "stale-artifact-name", valid[3]),
            (valid[0], valid[1], valid[2], "short-sha"),
        ]
        for args in invalid:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    review.validate_source_identity(*args)

    def test_contact_sheet_count_is_derived_from_video_duration_and_tile_geometry(self):
        self.assertEqual(review.expected_contact_sheets(957.9), 60)
        self.assertEqual(review.expected_contact_sheets(16.0), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
