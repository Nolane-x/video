from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import voicestudio_engine_actions_benchmark as bench


class FakeApi:
    def __init__(self, states):
        self.states = list(states)
        self.posts = []
        self.gets = []

    def get_json(self, path):
        self.gets.append(path)
        self.last_get = path
        return self.states.pop(0)

    def post_json(self, path, payload):
        self.posts.append((path, payload))
        return {"ok": True, "engine_id": "supertonic3", "accepted": True}


class VoiceStudioEngineActionsBenchmarkTests(unittest.TestCase):
    def test_acceptance_is_not_written_without_explicit_manual_confirmation(self):
        api = FakeApi([{"engine_id": "supertonic3", "accepted": False}])
        with self.assertRaisesRegex(PermissionError, "manually dispatch"):
            bench.verify_or_accept_license(api, accept_model_license=False)
        self.assertEqual(api.posts, [])
        self.assertEqual(api.last_get, "/api/settings/license/supertonic3")

    def test_benchmark_stops_before_output_or_synthesis_without_model_consent(self):
        api = FakeApi([{"engine_id": "supertonic3", "accepted": False}])
        suite = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-benchmark-suite.json"
        )
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "must-not-exist"
            with patch.object(api, "synthesize", side_effect=AssertionError("synthesis must not run")) as synthesize:
                with self.assertRaises(PermissionError):
                    bench.run_benchmark(
                        suite, output, api, accept_model_license=False,
                    )
            synthesize.assert_not_called()
            self.assertFalse(output.exists())
            self.assertEqual(api.posts, [])

    def test_explicit_confirmation_accepts_license_and_records_provenance(self):
        api = FakeApi([
            {"engine_id": "supertonic3", "accepted": False},
            {"engine_id": "supertonic3", "accepted": True},
            {"backends": [{
                "id": "supertonic3", "available": True, "license_accepted": True,
                "reason": "ready (CPU-only via onnxruntime)",
            }]},
        ])
        receipt = bench.verify_or_accept_license(api, accept_model_license=True)
        self.assertEqual(
            api.posts,
            [("/api/settings/license", {"engine_id": "supertonic3", "accepted": True})],
        )
        self.assertTrue(receipt["accepted"])
        self.assertTrue(receipt["accepted_in_this_run"])
        self.assertEqual(receipt["model_license"], "OpenRAIL-M")
        self.assertEqual(receipt["model_revision"], bench.MODEL_REVISION)
        self.assertTrue(receipt["engine_available"])
        self.assertEqual(api.last_get, "/engines/tts")

    def test_previously_accepted_license_is_not_reaccepted(self):
        api = FakeApi([
            {"engine_id": "supertonic3", "accepted": True},
            {"backends": [{
                "id": "supertonic3", "available": True, "license_accepted": True,
                "reason": "ready (CPU-only via onnxruntime)",
            }]},
        ])
        receipt = bench.verify_or_accept_license(api, accept_model_license=False)
        self.assertEqual(api.posts, [])
        self.assertTrue(receipt["accepted"])
        self.assertFalse(receipt["accepted_in_this_run"])
        self.assertTrue(receipt["engine_available"])

    def test_engine_must_be_available_after_license_is_accepted(self):
        api = FakeApi([
            {"engine_id": "supertonic3", "accepted": False},
            {"engine_id": "supertonic3", "accepted": True},
            {"backends": [{
                "id": "supertonic3", "available": False, "license_accepted": True,
                "reason": "supertonic package missing in runtime",
            }]},
        ])
        with self.assertRaisesRegex(bench.VoiceStudioApiError, "still unavailable"):
            bench.verify_or_accept_license(api, accept_model_license=True)
        self.assertEqual(len(api.posts), 1)
        self.assertEqual(api.gets[-1], "/engines/tts")

    def test_only_loopback_voice_studio_api_urls_are_allowed(self):
        for url in (
            "https://127.0.0.1:3900",
            "http://example.com:3900",
            "http://user:pass@127.0.0.1:3900",
            "http://127.0.0.1:3900?token=secret",
        ):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    bench.VoiceStudioApi(url, "ephemeral-key")

    def test_suite_uses_four_fixed_vietnamese_scenarios(self):
        suite_path = (
            Path(__file__).resolve().parents[1]
            / "examples"
            / "actions-benchmark-suite.json"
        )
        suite = bench.load_suite(suite_path)
        self.assertEqual(suite["language"], "vi")
        self.assertEqual(len(suite["cases"]), 4)
        self.assertEqual(
            [item["id"] for item in suite["cases"]],
            ["tones-phonemes", "code-switch", "numbers-and-proper-nouns", "documentary-longform"],
        )

    def test_speech_request_uses_supertonic_vi_and_quality_steps(self):
        class FakeResponse:
            def __enter__(self):
                return self
            def __exit__(self, *_):
                return None
            def read(self):
                return b"RIFF" + b"\0" * 4 + b"WAVE" + b"payload"
            headers = {"Content-Type": "audio/wav"}

        api = bench.VoiceStudioApi("http://127.0.0.1:3900", "ephemeral-key")
        with tempfile.TemporaryDirectory() as tmp:
            with patch("urllib.request.urlopen", return_value=FakeResponse()) as opener:
                path = Path(tmp) / "candidate.wav"
                result = api.synthesize("Xin chào Việt Nam.", "F3", path)
                self.assertTrue(path.is_file())
                self.assertEqual(result["content_type"], "audio/wav")
                self.assertEqual(result["sha256"], bench._sha256(path))
        request = opener.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["model"], "supertonic3")
        self.assertEqual(payload["language"], "vi")
        self.assertEqual(payload["voice"], "F3")
        self.assertEqual(payload["num_step"], 12)
        self.assertEqual(payload["response_format"], "wav")


if __name__ == "__main__":
    unittest.main()
