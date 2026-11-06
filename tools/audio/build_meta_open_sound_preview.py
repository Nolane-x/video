#!/usr/bin/env python3
"""Download, verify and index Meta Open Sound OGG collections for offline preview."""
from __future__ import annotations
import argparse, hashlib, html, json, shutil, stat, subprocess, urllib.request, zipfile
from pathlib import Path, PurePosixPath
from typing import Any

REPOSITORY = "facebookincubator/Meta-open-sound"
REVISION = "251c0be57d5d1b3242b91f53e0cde62ab1cb42d9"
BASE_RAW = f"https://raw.githubusercontent.com/{REPOSITORY}/{REVISION}"
ATTRIBUTION = (
    '"Oculus Audio Pack 01" by Oculus VR, LLC '
    "(https://developers.meta.com/vr/downloads/package/oculus-audio-pack-1/), "
    "licensed under CC BY 4.0. Files renamed to the UCS naming convention; "
    "OGG previews transcoded from the original WAVs."
)
COLLECTIONS = [
    {"id":"oculus-audio-pack","archive":"meta-open-sound-oculus-audio-pack-ogg.zip","tag":"oculus-audio-pack-v1.0.0","sha256":"d807c8f4a09512f506f5a6170ef291b2ff4a9783b87dcddf2f458538d25afcb4","size":44626986,"license":"CC-BY-4.0","license_url":"https://creativecommons.org/licenses/by/4.0/","kind":"foley"},
    {"id":"meta-piano","archive":"meta-open-sound-meta-piano-ogg.zip","tag":"meta-piano-v1.0.0","sha256":"4ba8095f5c2a70396d14f3b9c563f6c9010a093893159bad50e83145e1c35d40","size":48182243,"license":"CC0-1.0","license_url":"https://creativecommons.org/publicdomain/zero/1.0/","kind":"instrument"},
    {"id":"meta-nylon-guitar","archive":"meta-open-sound-meta-nylon-guitar-ogg.zip","tag":"meta-nylon-guitar-v1.0.0","sha256":"2ff8f6296cfdb1a98f67116c5091a4f9f01c0c46ac538dd1c5756acc8b76889b","size":16483193,"license":"CC0-1.0","license_url":"https://creativecommons.org/publicdomain/zero/1.0/","kind":"instrument"},
    {"id":"meta-steel-guitar","archive":"meta-open-sound-meta-steel-guitar-ogg.zip","tag":"meta-steel-guitar-v1.0.0","sha256":"a06baf193497ba36f20ccb67018e9f106155ad5e4f81d8a672530498038f68ed","size":25440465,"license":"CC0-1.0","license_url":"https://creativecommons.org/publicdomain/zero/1.0/","kind":"instrument"},
]

def sha256_file(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""): digest.update(block)
    return digest.hexdigest()

def fetch_json(url: str) -> Any:
    req=urllib.request.Request(url,headers={"User-Agent":"Nolane-Audio-Library/1.0"})
    with urllib.request.urlopen(req,timeout=30) as response: return json.loads(response.read().decode())

def fetch_text(path: str) -> str:
    req=urllib.request.Request(f"{BASE_RAW}/{path}",headers={"User-Agent":"Nolane-Audio-Library/1.0"})
    with urllib.request.urlopen(req,timeout=30) as response: return response.read().decode()

def fetch_metadata():
    tree=fetch_json(f"https://api.github.com/repos/{REPOSITORY}/git/trees/{REVISION}?recursive=1")
    if tree.get("truncated"): raise RuntimeError("Meta Open Sound tree listing is truncated")
    paths={entry["path"] for entry in tree.get("tree",[])}
    required=[
      "corpora/oculus-audio-pack/manifest.json","corpora/oculus-audio-pack/README.md",
      "corpora/oculus-audio-pack/LICENSE","corpora/oculus-audio-pack/ATTRIBUTION.md",
      "systems/instruments/meta-piano/manifest.json","systems/instruments/meta-piano/LICENSE",
      "systems/instruments/meta-nylon-guitar/manifest.json","systems/instruments/meta-nylon-guitar/LICENSE",
      "systems/instruments/meta-steel-guitar/manifest.json","systems/instruments/meta-steel-guitar/LICENSE",
    ]
    indexes=sorted(p for p in paths if p.startswith("corpora/oculus-audio-pack/index/") and p.endswith(".json"))
    if not indexes: raise RuntimeError("Oculus search index files missing")
    metadata={}
    for p in required+indexes:
        if p not in paths: raise FileNotFoundError("Missing pinned metadata: "+p)
        metadata[p]=json.loads(fetch_text(p)) if p.endswith(".json") else fetch_text(p)
    sound_map={}
    for p in indexes:
        category=metadata[p]
        for sound in category.get("sounds",[]):
            for take in sound.get("takes",[]):
                file_name=str(take.get("file") or "")
                if file_name:
                    sound_map[Path(file_name).stem.casefold()]={**sound,"index_category":category.get("cat_short"),"take":take}
    manifests={"oculus-audio-pack":metadata["corpora/oculus-audio-pack/manifest.json"]}
    for cid in ("meta-piano","meta-nylon-guitar","meta-steel-guitar"):
        manifests[cid]=metadata[f"systems/instruments/{cid}/manifest.json"]
    licenses={
      "oculus-attribution":metadata["corpora/oculus-audio-pack/ATTRIBUTION.md"],
      "oculus-license":metadata["corpora/oculus-audio-pack/LICENSE"],
      "oculus-readme":metadata["corpora/oculus-audio-pack/README.md"],
      "meta-piano-license":metadata["systems/instruments/meta-piano/LICENSE"],
      "meta-nylon-guitar-license":metadata["systems/instruments/meta-nylon-guitar/LICENSE"],
      "meta-steel-guitar-license":metadata["systems/instruments/meta-steel-guitar/LICENSE"],
    }
    return sound_map,manifests,licenses

def download_archives(download_dir: Path):
    download_dir.mkdir(parents=True,exist_ok=True)
    for c in COLLECTIONS:
        path=download_dir/c["archive"]
        if not path.exists() or path.stat().st_size!=c["size"]:
            path.unlink(missing_ok=True)
            url=f"https://github.com/{REPOSITORY}/releases/download/{c['tag']}/{c['archive']}"
            req=urllib.request.Request(url,headers={"User-Agent":"Nolane-Audio-Library/1.0"})
            with urllib.request.urlopen(req,timeout=180) as response,path.open("wb") as dst:
                shutil.copyfileobj(response,dst,1024*1024)
        if path.stat().st_size!=c["size"]: raise ValueError("Archive size mismatch: "+c["archive"])
        if sha256_file(path)!=c["sha256"]: raise ValueError("Archive SHA-256 mismatch: "+c["archive"])

def probe(path: Path):
    cmd=["ffprobe","-v","error","-select_streams","a:0","-show_entries","stream=codec_name,sample_rate,channels,channel_layout","-show_entries","format=duration,bit_rate","-of","json",str(path)]
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=20,check=False)
    if result.returncode: raise ValueError((result.stderr or "ffprobe failed")[-300:])
    data=json.loads(result.stdout or "{}"); streams=data.get("streams") or []
    if not streams: raise ValueError("No audio stream")
    s,f=streams[0],data.get("format") or {}
    return {"codec":s.get("codec_name"),"sample_rate_hz":int(s["sample_rate"]) if str(s.get("sample_rate","")).isdigit() else None,"channels":s.get("channels"),"channel_layout":s.get("channel_layout"),"duration_seconds":float(f["duration"]) if f.get("duration") else None,"bit_rate_bps":int(f["bit_rate"]) if str(f.get("bit_rate","")).isdigit() else None}

def extract_bank(download_dir: Path, output_dir: Path):
    sound_map,manifests,licenses=fetch_metadata()
    media_dir=output_dir/"media"; media_dir.mkdir(parents=True,exist_ok=True)
    records=[]; seen_hashes=set()
    for c in COLLECTIONS:
        sample_map={Path(str(x["file"])).stem.casefold():x for x in manifests[c["id"]].get("samples",[])}
        with zipfile.ZipFile(download_dir/c["archive"]) as archive:
            bad=archive.testzip()
            if bad: raise ValueError(f"ZIP CRC failure: {c['archive']}::{bad}")
            members=[x for x in archive.infolist() if not x.is_dir() and Path(x.filename).suffix.casefold()==".ogg"]
            if not members: raise ValueError("No OGG files in "+c["archive"])
            for info in members:
                p=PurePosixPath(info.filename)
                if p.is_absolute() or ".." in p.parts or "\\\\" in info.filename: raise ValueError("Unsafe member path: "+info.filename)
                if ((info.external_attr>>16)&0o170000)==stat.S_IFLNK: raise ValueError("Symlink member blocked")
                if info.file_size<1 or info.file_size>128*1024*1024: raise ValueError("OGG size out of range")
                stem=Path(info.filename).stem.casefold()
                if stem not in sample_map: raise ValueError("OGG sample absent from pinned manifest: "+info.filename)
                sound=sound_map.get(stem) if c["id"]=="oculus-audio-pack" else None
                asset_id=f"meta-{c['id']}-{stem}"
                destination=media_dir/(asset_id+".ogg")
                digest=hashlib.sha256()
                with archive.open(info) as src,destination.open("wb") as dst:
                    for block in iter(lambda:src.read(1024*1024),b""):
                        digest.update(block); dst.write(block)
                digest_hex=digest.hexdigest()
                if digest_hex in seen_hashes:
                    destination.unlink(missing_ok=True); continue
                seen_hashes.add(digest_hex)
                tags=[]; summary=""
                if sound:
                    tags=list(dict.fromkeys([str(x) for x in sound.get("keywords",[])]+[str(sound.get("index_category") or ""),str(sound.get("ucs",{}).get("category") or "")]))
                    summary=str(sound.get("summary") or "")
                else:
                    tags=["instrument",c["id"],Path(info.filename).stem]
                    summary=f"Multisampled {c['id']} instrument sample."
                records.append({
                  "asset_id":asset_id,"title":summary or Path(info.filename).stem,
                  "file_name":Path(info.filename).name,"archive_name":c["archive"],
                  "archive_member":info.filename,"collection":c["id"],"collection_kind":c["kind"],
                  "tags":tags,"license":c["license"],"license_url":c["license_url"],
                  "rights_class":"cc_by_4_attribution_required" if c["license"]=="CC-BY-4.0" else "cc0_public_domain",
                  "source_url":f"https://github.com/{REPOSITORY}/tree/{REVISION}/"+("corpora/oculus-audio-pack" if c["id"]=="oculus-audio-pack" else f"systems/instruments/{c['id']}"),
                  "attribution_text":ATTRIBUTION if c["license"]=="CC-BY-4.0" else "",
                  "source_sha256":c["sha256"],"computed_sha256":digest_hex,
                  "size_bytes":destination.stat().st_size,"preview_path":f"media/{destination.name}",
                  "auditioned_by_human":False,"approved_for_final_mix":False,**probe(destination)
                })
    return records,licenses

def write_bank(output_dir: Path,records,licenses):
    summary={"files":len(records),"total_bytes":sum(x["size_bytes"] for x in records),"cc0_files":sum(x["rights_class"]=="cc0_public_domain" for x in records),"cc_by_files":sum(x["rights_class"]=="cc_by_4_attribution_required" for x in records),"human_auditioned":0,"approved_for_final_mix":0}
    payload={"schema_version":"1.0.0","source_repository":REPOSITORY,"source_revision":REVISION,"summary":summary,"assets":records,"policy":"Each collection keeps its own license; all samples still require human audition before final mix."}
    (output_dir/"meta-preview-catalog.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    (output_dir/"ATTRIBUTION.md").write_text("# Attribution\\n\\n"+ATTRIBUTION+"\\n\\nOculus Audio Pack 1 is CC BY 4.0. Meta Piano, Meta Nylon Guitar and Meta Steel Guitar are CC0 1.0. Retain this attribution when using or redistributing the Oculus collection.\\n",encoding="utf-8")
    for name,text in licenses.items(): (output_dir/f"{name}.txt").write_text(text,encoding="utf-8")
    cards=[]
    for item in records:
        esc=html.escape
        search=esc(" ".join([item["title"],item["file_name"],item["collection"]," ".join(item["tags"]),item["license"]]).casefold(),quote=True)
        meta=esc(f'{item["collection"]} · {item["license"]} · {item["codec"]} · {item["sample_rate_hz"]} Hz · {item["channels"]} ch · {item["duration_seconds"]:.2f}s')
        license_link=f'<a href="{esc(item["license_url"],quote=True)}" target="_blank" rel="noreferrer">License</a>'
        source_link=f'<a href="{esc(item["source_url"],quote=True)}" target="_blank" rel="noreferrer">Source</a>'
        attribution=f'<p class="attr">{esc(item["attribution_text"])}</p>' if item["attribution_text"] else ""
        cards.append(f'<article class="card" data-search="{search}"><b>{esc(item["title"])}</b><p>{meta}</p><p>{esc(item["file_name"])}</p><audio controls preload="none" src="{esc(item["preview_path"],quote=True)}"></audio><p>NOT AUDITIONED · NOT APPROVED FOR FINAL MIX · {license_link} · {source_link}</p>{attribution}</article>')
    page="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Meta Open Sound — Nolane Audio Bank</title><style>
:root{color-scheme:dark}body{font:15px system-ui;background:#101820;color:#eef3f7;margin:24px}input{box-sizing:border-box;width:100%;padding:12px;background:#202b35;color:inherit;border:1px solid #52616e;border-radius:8px;margin:12px 0 18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}.card{background:#1c2832;border:1px solid #3e4d58;border-radius:10px;padding:14px}.card p{font-size:12px;color:#becbd5;overflow-wrap:anywhere}audio{width:100%;margin:8px 0}a{color:#9addd0}.attr{color:#e5c985}.hidden{display:none}.note{padding:12px;border-left:3px solid #d7aa57;background:#202a32}</style>
<h1>Meta Open Sound — Nolane Audio Bank</h1><p id="count"></p><p class="note">Oculus Audio Pack is CC BY 4.0; its attribution must be retained. The three instrument collections are CC0. All samples remain NOT AUDITIONED and NOT APPROVED FOR FINAL MIX until reviewed by a human.</p>
<input id="q" type="search" placeholder="Search sword, katana, footsteps, horse, rowing, rain, wind, instrument..."><div class="grid">"""+ "".join(cards)+"""</div><script>
const q=document.getElementById('q'),cards=[...document.querySelectorAll('.card')];function update(){let n=0;const t=q.value.toLowerCase();for(const c of cards){const ok=c.dataset.search.includes(t);c.classList.toggle('hidden',!ok);if(ok)n++}document.getElementById('count').textContent=n+' / '+cards.length+' playable samples'}q.addEventListener('input',update);update();
</script></html>"""
    (output_dir/"META_AUDIO_PREVIEW_BANK.html").write_text(page,encoding="utf-8")
    (output_dir/"README.md").write_text("# Meta Open Sound preview bank\\n\\nOpen META_AUDIO_PREVIEW_BANK.html in a browser and search/play the local OGG files. meta-preview-catalog.json records tags, sources, hashes and technical metadata. Oculus requires CC BY 4.0 attribution; the three instrument collections are CC0. All files require human audition before final use.\\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--download-dir",type=Path,default=Path("/tmp/meta-open-sound"))
    p.add_argument("--output-dir",type=Path,default=Path("build/audio-preview-bank/meta-open-sound"))
    a=p.parse_args()
    download_archives(a.download_dir)
    a.output_dir.mkdir(parents=True,exist_ok=True)
    records,licenses=extract_bank(a.download_dir,a.output_dir)
    print(json.dumps(write_bank(a.output_dir,records,licenses),indent=2))

if __name__=="__main__": main()
