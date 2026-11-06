#!/usr/bin/env python3
"""Offline integration test for the pinned Meta Open Sound preview-bank builder."""
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"/"audio"))
import build_meta_open_sound_preview as preview

def main():
    old=preview.COLLECTIONS
    preview.COLLECTIONS=[{
      "id":"oculus-audio-pack","archive":"meta-open-sound-oculus-audio-pack-ogg.zip",
      "tag":"fixture","sha256":"0"*64,"size":1,"license":"CC-BY-4.0",
      "license_url":"https://creativecommons.org/licenses/by/4.0/","kind":"foley",
      "wav_master_url":"https://example.invalid/master.zip","wav_master_size":1234,"wav_master_sha256":"abc123"
    }]
    try:
      with tempfile.TemporaryDirectory(prefix="meta-open-sound-test-") as temp:
        root=Path(temp); downloads=root/"downloads"; output=root/"output"
        downloads.mkdir()
        wav=root/"sample.wav"
        subprocess.run([
          "ffmpeg","-v","error","-f","lavfi","-i","sine=frequency=700:duration=0.2",
          "-c:a","libvorbis","-y",str(root/"SwordClash.ogg")
        ],check=True)
        archive=downloads/preview.COLLECTIONS[0]["archive"]
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
          z.write(root/"SwordClash.ogg","ogg/SwordClash.ogg")
        preview.fetch_metadata=lambda:(
          {"swordclash":{"summary":"Use for: two swords clashing.","keywords":["sword","katana"],"index_category":"WEAP","ucs":{"category":"WEAPONS"}}},
          {"oculus-audio-pack":{"samples":[{"file":"SwordClash.wav"}]}},
          {"oculus-attribution":preview.ATTRIBUTION}
        )
        records,licenses=preview.extract_bank(downloads,output)
        assert len(records)==1
        assert records[0]["rights_class"]=="cc_by_4_attribution_required"
        assert "katana" in records[0]["tags"]
        assert records[0]["auditioned_by_human"] is False
        assert records[0]["source_wav_file"] == "SwordClash.wav"
        assert records[0]["wav_master_archive_name"] == "master.zip"
        assert records[0]["wav_master_download_url"].endswith("/meta-open-sound-oculus-audio-pack-wav.zip")
        summary=preview.write_bank(output,records,licenses)
        assert summary["cc_by_files"]==1
        assert (output/"media"/(records[0]["asset_id"]+".ogg")).is_file()
        assert "Oculus Audio Pack 01" in (output/"ATTRIBUTION.md").read_text()
        catalog=json.loads((output/"meta-preview-catalog.json").read_text())
        assert catalog["summary"]["approved_for_final_mix"]==0
      print("PASS: Meta OGG ZIP, source manifest, metadata tags, CC-BY attribution and preview catalog.")
    finally:
      preview.COLLECTIONS=old

if __name__=="__main__": main()
