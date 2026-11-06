#!/usr/bin/env python3
"""Integration tests for the offline audio preview bank builder."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import wave
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "audio"))
import build_audio_preview_bundle as preview


def test_cc0_candidate_is_extracted_and_playable() -> None:
    with tempfile.TemporaryDirectory(prefix="nolane-audio-preview-test-") as temporary:
        root = Path(temporary)
        download_dir = root / "downloads"
        output_dir = root / "output"
        download_dir.mkdir()

        wav_bytes_path = root / "sample.wav"
        with wave.open(str(wav_bytes_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(48000)
            wav.writeframes(b"\x00\x00" * 4800)
        media_bytes = wav_bytes_path.read_bytes()
        digest = hashlib.sha256(media_bytes).hexdigest()
        invalid_path = root / "invalid.wav"
        invalid_bytes = b"not an audio stream"
        invalid_path.write_bytes(invalid_bytes)
        invalid_digest = hashlib.sha256(invalid_bytes).hexdigest()

        archive_name = "video-assets-test-audio-001.zip"
        with zipfile.ZipFile(download_dir / archive_name, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(wav_bytes_path, "fixture/soft-step.wav")
            archive.write(invalid_path, "fixture/._bad-metadata.wav")

        catalog = {
            "assets": [
                {
                    "asset_id": "cc0-fixture",
                    "archive_name": archive_name,
                    "archive_member": "fixture/soft-step.wav",
                    "license": "CC0-1.0",
                    "rights_status": "redistributable_candidate",
                    "rights_match_method": "exact_path",
                    "sha256": digest,
                    "size_bytes": len(media_bytes),
                    "title": "Soft step fixture",
                    "attribution_text": "Fixture Author",
                    "source_url": "https://example.invalid/fixture",
                },
                {
                    "asset_id": "bad-audio-fixture",
                    "archive_name": archive_name,
                    "archive_member": "fixture/._bad-metadata.wav",
                    "license": "CC0-1.0",
                    "rights_status": "redistributable_candidate",
                    "rights_match_method": "exact_path",
                    "sha256": invalid_digest,
                    "size_bytes": len(invalid_bytes),
                    "title": "Invalid metadata WAV",
                    "source_url": "https://example.invalid/bad",
                },
                {
                    "asset_id": "nasa-fixture",
                    "archive_name": archive_name,
                    "archive_member": "fixture/soft-step.wav",
                    "license": "NASA Media Usage Guidelines",
                    "rights_status": "source_specific_review_required",
                    "rights_match_method": "exact_path",
                    "size_bytes": len(media_bytes),
                },
            ]
        }

        assets, rejected = preview.extract_preview_bank(catalog, download_dir, output_dir)
        preview.write_catalog(output_dir, assets, rejected)
        assert len(assets) == 1
        assert assets[0]["asset_id"] == "cc0-fixture"
        assert len(rejected) == 1
        assert rejected[0]["asset_id"] == "bad-audio-fixture"
        assert "ffprobe rejected source audio" in rejected[0]["reason"]
        assert assets[0]["computed_sha256"] == digest
        assert assets[0]["source_sha256_verified"] is True
        assert assets[0]["auditioned_by_human"] is False
        assert (output_dir / assets[0]["preview_path"]).is_file()
        page = (output_dir / "AUDIO_PREVIEW_BANK.html").read_text(encoding="utf-8")
        assert "Soft step fixture" in page
        assert "NOT AUDITIONED" in page
        assert "example.invalid/fixture" in page


if __name__ == "__main__":
    test_cc0_candidate_is_extracted_and_playable()
    print("PASS: eligible audio is extracted, hashed, probed and indexed; NASA/review items are excluded.")
