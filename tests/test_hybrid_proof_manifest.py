from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.video.build_hybrid_proof_manifest import build_manifest


class HybridProofManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.video = self.root / "hybrid.mp4"
        self.metadata = self.root / "metadata.json"
        self.voice = self.root / "voice.json"
        self.score = self.root / "score.wav"
        self.fire = self.root / "fire.ogg"
        self.impact = self.root / "impact.ogg"

        self.video.write_bytes(b"test-video-data")
        self.score.write_bytes(b"score")
        self.fire.write_bytes(b"cannon-fire")
        self.impact.write_bytes(b"cannon-impact")
        self.voice.write_text(json.dumps({
            "voice_id": "voice-test",
            "audio": {"sha256": "a" * 64},
        }), encoding="utf-8")
        self.metadata.write_text(json.dumps({
            "streams": [
                {
                    "codec_type": "video",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "240/1",
                    "avg_frame_rate": "240/1",
                    "nb_read_frames": "9394",
                    "codec_name": "h264",
                },
                {
                    "codec_type": "audio",
                    "sample_rate": "48000",
                    "channels": 2,
                    "codec_name": "aac",
                },
            ],
            "format": {"duration": "39.141667"},
        }), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build(self) -> dict:
        return build_manifest(
            video_path=self.video,
            metadata_path=self.metadata,
            voice_manifest_path=self.voice,
            score_path=self.score,
            cannon_fire_path=self.fire,
            cannon_impact_path=self.impact,
            source_run_id="123456",
            source_sha="b" * 40,
        )

    def test_manifest_hashes_video_and_records_provenance(self) -> None:
        result = self.build()
        self.assertEqual(result["decoded_frames"], 9394)
        self.assertEqual(result["output_fps"], "240/1")
        self.assertEqual(result["source_run_id"], "123456")
        self.assertEqual(result["source_commit_sha"], "b" * 40)
        self.assertEqual(
            result["sha256_video"],
            hashlib.sha256(self.video.read_bytes()).hexdigest(),
        )
        self.assertEqual(len(result["audio_assets"]), 3)
        self.assertFalse(result["audio_assets"][0]["human_auditioned"])

    def test_rejects_wrong_frame_count(self) -> None:
        data = json.loads(self.metadata.read_text(encoding="utf-8"))
        data["streams"][0]["nb_read_frames"] = "9393"
        self.metadata.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "decoded frames"):
            self.build()

    def test_rejects_variable_or_wrong_rate(self) -> None:
        data = json.loads(self.metadata.read_text(encoding="utf-8"))
        data["streams"][0]["avg_frame_rate"] = "239/1"
        self.metadata.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "constant 240/1"):
            self.build()

    def test_rejects_missing_video_file(self) -> None:
        self.video.unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()

    def test_rejects_missing_narrator_attestation(self) -> None:
        self.voice.write_text(json.dumps({"voice_id": "voice-test", "audio": {}}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "source SHA-256"):
            self.build()


if __name__ == "__main__":
    unittest.main()
