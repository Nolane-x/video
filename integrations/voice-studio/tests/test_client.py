from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from client import VoiceStudioClient, VoiceStudioError


class FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class FakeResponse:
    def __init__(self, body: bytes, content_type: str = "application/json"):
        self.body = body
        self.headers = FakeHeaders({"Content-Type": content_type})

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, *args):
        return self.body


class VoiceStudioClientTests(unittest.TestCase):
    def test_health_uses_loopback_default(self):
        response = FakeResponse(b'{"status":"ok"}')
        with patch("urllib.request.urlopen", return_value=response) as open_url:
            result = VoiceStudioClient().health()
        self.assertEqual(result["status"], "ok")
        self.assertIn("127.0.0.1:3900/health", open_url.call_args.args[0].full_url)

    def test_synthesize_posts_selected_engine_and_voice(self):
        response = FakeResponse(b"RIFF" + b"\0" * 80, "audio/wav")
        with patch("urllib.request.urlopen", return_value=response) as open_url:
            out = Path("test-voice.wav")
            try:
                client = VoiceStudioClient(api_key="secret-test-key")
                client.synthesize(
                    "Xin chào", out, engine="voxcpm2",
                    voice="voice-profile-123", language="vi",
                )
                request = open_url.call_args.args[0]
                payload = json.loads(request.data.decode("utf-8"))
                self.assertEqual(payload["model"], "voxcpm2")
                self.assertEqual(payload["voice"], "voice-profile-123")
                self.assertEqual(request.get_header("Authorization"), "Bearer secret-test-key")
                self.assertEqual(out.read_bytes()[:4], b"RIFF")
            finally:
                out.unlink(missing_ok=True)

    def test_rejects_overlong_segment_before_network(self):
        with patch("urllib.request.urlopen") as open_url:
            with self.assertRaises(ValueError):
                VoiceStudioClient().synthesize("x" * 4097, "unused.wav")
            open_url.assert_not_called()

    def test_json_error_is_not_written_as_audio(self):
        response = FakeResponse(b'{"detail":"engine unavailable"}', "application/json")
        with patch("urllib.request.urlopen", return_value=response):
            with self.assertRaises(VoiceStudioError):
                VoiceStudioClient().synthesize("hello", "unused.wav")


if __name__ == "__main__":
    unittest.main()
