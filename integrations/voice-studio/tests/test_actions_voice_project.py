from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import actions_voice_project as project


class ActionsVoiceProjectTests(unittest.TestCase):
    def manifest(self):
        return {
            "project": "actions-test",
            "language": "vi",
            "cast": {
                "narrator": {
                    "provider": "korva",
                    "voice": "khanh_vy",
                    "language": "vi",
                    "seed": 42,
                    "settings": {"total_steps": 32, "num_threads": 4},
                }
            },
            "segments": [
                {
                    "id": "V001",
                    "speaker_id": "narrator",
                    "slot": "NARRATOR",
                    "character": "Người dẫn chuyện",
                    "text": "Xin chào Việt Nam.",
                }
            ],
        }

    def test_repository_actions_documentary_manifest_validates_for_all_cast_roles(self):
        manifest_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-vietnamese-documentary.json"
        )
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        segments = project.validate_actions_project(data)
        self.assertEqual(len(data["cast"]), 4)
        self.assertEqual(len(segments), 10)
        self.assertEqual({item["provider"] for item in segments}, {"korva"})
        self.assertEqual({item["engine"] for item in segments}, {"korva-onnx"})

    def test_actions_project_rejects_non_korva_provider(self):
        data = self.manifest()
        data["cast"]["narrator"]["provider"] = "voicestudio"
        with self.assertRaisesRegex(ValueError, "only runs KorvaTTS"):
            project.validate_actions_project(data)

    def test_actions_project_requires_high_quality_cpu_profile(self):
        data = self.manifest()
        data["cast"]["narrator"]["settings"]["total_steps"] = 8
        with self.assertRaisesRegex(ValueError, "total_steps=32"):
            project.validate_actions_project(data)

    def test_actions_project_requires_stable_speaker_id(self):
        data = self.manifest()
        data["segments"][0].pop("speaker_id")
        with self.assertRaisesRegex(ValueError, "stable speaker_id"):
            project.validate_actions_project(data)

    def test_actions_project_executes_h2_handoff_and_emits_evidence_report(self):
        data = self.manifest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
            out = root / "out"
            audio_dir = out / "voice"
            audio_dir.mkdir(parents=True)
            audio = audio_dir / "V001.wav"
            audio.write_bytes(b"RIFF" + b"\0" * 64)
            digest = hashlib.sha256(audio.read_bytes()).hexdigest()

            def fake_generate(manifest, output_dir, **kwargs):
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "02-VOICE-actions-test-TTS.txt").write_text(
                    "=== V001 | NARRATOR · Người dẫn chuyện ===\nXin chào Việt Nam.\n",
                    encoding="utf-8",
                )
                (output_dir / "voice-generation-report.json").write_text(
                    json.dumps({
                        "project": "actions-test",
                        "status": "generated",
                        "generated_segments": 1,
                        "failed_segments": 0,
                        "voice_script": "02-VOICE-actions-test-TTS.txt",
                        "segments": [{
                            "id": "V001", "speaker_id": "narrator",
                            "voice": "khanh_vy", "status": "generated",
                            "provider": "korva", "engine": "korva-onnx",
                            "file": "voice/V001.wav", "sha256": digest,
                        }],
                    }),
                    encoding="utf-8",
                )
                return {"status": "generated"}

            def fake_h2(output_dir, voice_txt, audio_path):
                timeline = output_dir / "h2-project" / "timeline"
                timeline.mkdir(parents=True, exist_ok=True)
                (timeline / "voice.wav").write_bytes(b"RIFF" + b"\0" * 64)
                (timeline / "blocks.json").write_text('[{"id":"V001"}]', encoding="utf-8")
                (timeline / "lines.json").write_text('[{"id":"L001"}]', encoding="utf-8")
                (timeline / "words.json").write_text('[{"w":"Xin"}]', encoding="utf-8")
                (timeline / "transcript.txt").write_text("Xin chào Việt Nam.\n", encoding="utf-8")
                return {"timeline_dir": "h2-project/timeline", "outputs": {}}

            with patch.object(project.importlib.metadata, "version", return_value="0.1.3"):
                with patch.object(project, "_download_model", return_value=root / "assets"):
                    with patch.object(project.korva, "_engine") as engine:
                        engine.return_value.list_voices.return_value = ["khanh_vy"]
                        with patch.object(project, "generate", side_effect=fake_generate):
                            with patch.object(project, "audit_report", return_value={"technical_pass": 1}):
                                with patch.object(project, "_probe_audio", return_value={
                                    "sample_rate_hz": 44100,
                                    "duration_s": 2.0,
                                    "peak_dbfs": -2.0,
                                    "rms_dbfs": -18.0,
                                    "clipped_sample_ratio": 0.0,
                                    "trailing_silence_s": 0.1,
                                    "silence_ratio_below_minus_40_db": 0.05,
                                }):
                                    with patch.object(project, "_technical_findings", return_value=[]):
                                        with patch.object(project, "_run_h2_timing", side_effect=fake_h2) as h2:
                                            report = project.run_project(
                                                manifest_path,
                                                out,
                                                model_revision="a" * 40,
                                            )
            h2.assert_called_once()
            self.assertEqual(report["status"], "complete")
            self.assertEqual(report["generated_segments"], 1)
            self.assertIsNotNone(report["h2_timing"])
            self.assertEqual(report["technical_pass"], 1)
            self.assertEqual(report["h2_timing"]["block_count"], 1)
            self.assertEqual(report["h2_timing"]["line_count"], 1)
            self.assertEqual(report["h2_timing"]["word_count"], 1)
            self.assertTrue((out / "project-manifest.json").is_file())
            saved = json.loads((out / "actions-voice-project-report.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["model"]["revision"], "a" * 40)
            self.assertEqual(saved["elevenlabs_equivalence"], None)


if __name__ == "__main__":
    unittest.main()
