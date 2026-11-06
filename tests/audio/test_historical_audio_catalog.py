"""Offline integration check for the historical audio catalog builder."""
import hashlib
import json
import shutil
import subprocess
import sys
import wave
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "audio" / "build_historical_audio_catalog.py"
FIXTURE = Path("/tmp/nolane-audio-catalog-fixture")


def test_catalog_builder():
    shutil.rmtree(FIXTURE, ignore_errors=True)
    archives = FIXTURE / "archives"
    manifests = FIXTURE / "manifests"
    output = FIXTURE / "output"
    for folder in (archives, manifests, output):
        folder.mkdir(parents=True, exist_ok=True)

    source = FIXTURE / "sample.wav"
    with wave.open(str(source), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(48000)
        wav.writeframes(b"\x00\x00" * 48000)

    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    with zipfile.ZipFile(archives / "video-assets-test-audio-001.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(source, "video-asset-library/sample/sample.wav")

    manifest = {
        "lane": "test",
        "assets": [{
            "id": "fixture-001",
            "path": "sample/sample.wav",
            "title": "Fixture sample",
            "creator": "Test",
            "provider": "Test provider",
            "category": "test",
            "license": "CC0-1.0",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "source_page": "https://example.invalid/fixture",
            "sha256": digest,
            "redistributable": True,
        }],
    }
    (manifests / "asset-shard--test.json").write_text(json.dumps(manifest), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(SCRIPT), "--archive-dir", str(archives),
         "--manifest-dir", str(manifests), "--output-dir", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    catalog = json.loads((output / "audio-catalog.json").read_text(encoding="utf-8"))
    assert catalog["summary"]["catalogued_audio_files"] == 1
    assert catalog["summary"]["human_auditioned"] == 0
    assert catalog["assets"][0]["rights_class"] == "public_cc0_pd"
    assert catalog["assets"][0]["audition_status"] == "not_auditioned"
    assert (output / "ASSET_CATALOG.html").is_file()


if __name__ == "__main__":
    test_catalog_builder()
    print("PASS: fixture audio extracted, ffprobed, SHA-256 and rights checked, then catalogued.")
