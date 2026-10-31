from __future__ import annotations

import json
import sys
import tempfile
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

    def test_refuses_api_key_over_plain_http_to_remote_host(self):
        with patch("urllib.request.urlopen") as open_url:
            client = VoiceStudioClient(
                base_url="http://192.0.2.10:3900", api_key="secret-test-key"
            )
            with self.assertRaises(VoiceStudioError):
                client.health()
            open_url.assert_not_called()

    def test_allows_api_key_over_https(self):
        response = FakeResponse(b'{"status":"ok"}')
        with patch("urllib.request.urlopen", return_value=response) as open_url:
            result = VoiceStudioClient(
                base_url="https://voice.example.test", api_key="secret-test-key"
            ).health()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(open_url.call_args.args[0].get_header("Authorization"), "Bearer secret-test-key")

    def test_rejects_overlong_segment_before_network(self):
        with patch("urllib.request.urlopen") as open_url:
            with self.assertRaises(ValueError):
                VoiceStudioClient().synthesize("x" * 4097, "unused.wav")
            open_url.assert_not_called()

    def test_download_audio_preserves_mp3_content_type(self):
        response = FakeResponse(b"ID3" + b"\0" * 64, "audio/mpeg")
        with patch("urllib.request.urlopen", return_value=response):
            with tempfile.TemporaryDirectory() as tmp:
                path = VoiceStudioClient().download_audio(
                    "/archetypes/sample/preview", Path(tmp) / "sample.audio"
                )
                self.assertEqual(path.suffix, ".mp3")
                self.assertTrue(path.read_bytes().startswith(b"ID3"))

    def test_transcribe_posts_multipart_audio_and_returns_text(self):
        response = FakeResponse(b'{"text":"Xin chao Viet Nam"}', "application/json")
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sample.wav"
            source.write_bytes(b"RIFF" + b"\0" * 64)
            with patch("urllib.request.urlopen", return_value=response) as open_url:
                transcript = VoiceStudioClient().transcribe(source, language="vi")
            request = open_url.call_args.args[0]
            self.assertEqual(transcript, "Xin chao Viet Nam")
            self.assertIn("multipart/form-data; boundary=", request.get_header("Content-type"))
            self.assertIn(b'name="file"', request.data)
            self.assertIn(b'name="language"', request.data)
            self.assertIn(b'name="model"', request.data)

    def test_list_archetypes_passes_featured_filter_and_language(self):
        client = VoiceStudioClient()
        with patch.object(client, "_json", return_value={"items": []}) as request:
            result = client.list_archetypes(language="Vietnamese", featured=True, limit=20)
        self.assertEqual(result, [])
        self.assertEqual(request.call_args.kwargs["query"]["lang"], "Vietnamese")
        self.assertEqual(request.call_args.kwargs["query"]["featured"], "true")

    def test_create_design_profile_posts_native_recipe_and_returns_profile_id(self):
        response = FakeResponse(b'{"id":"profile-abc","name":"Nolane voice"}')
        with patch("urllib.request.urlopen", return_value=response) as open_url:
            result = VoiceStudioClient().create_design_profile(
                "Nolane voice",
                "Original fictional Vietnamese narrator, warm low-mid voice.",
                engine="voxcpm2", language="vi", seed=4201,
                sample_text="Xin chào.",
            )
        request = open_url.call_args.args[0]
        body = request.data
        self.assertEqual(result["id"], "profile-abc")
        self.assertIn("multipart/form-data; boundary=", request.get_header("Content-type"))
        for field in (b'name="name"', b'name="kind"', b'name="vd_states"',
                      b'name="design_recipe"', b'name="engine"', b'name="seed"'):
            self.assertIn(field, body)
        self.assertIn(b"Original fictional Vietnamese narrator", body)
        self.assertIn(b"voxcpm2", body)
        self.assertIn(b"4201", body)

    def test_create_design_profile_rejects_empty_or_oversize_description(self):
        with patch("urllib.request.urlopen") as open_url:
            with self.assertRaises(ValueError):
                VoiceStudioClient().create_design_profile(
                    "bad", " ", engine="voxcpm2"
                )
            with self.assertRaises(ValueError):
                VoiceStudioClient().create_design_profile(
                    "bad", "x" * 2001, engine="voxcpm2"
                )
            open_url.assert_not_called()

    def test_json_error_is_not_written_as_audio(self):
        response = FakeResponse(b'{"detail":"engine unavailable"}', "application/json")
        with patch("urllib.request.urlopen", return_value=response):
            with self.assertRaises(VoiceStudioError):
                VoiceStudioClient().synthesize("hello", "unused.wav")


if __name__ == "__main__":
    unittest.main()
