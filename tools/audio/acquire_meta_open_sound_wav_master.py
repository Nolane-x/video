#!/usr/bin/env python3
"""Download one pinned Meta Open Sound WAV master and verify its release hash."""
from __future__ import annotations
import argparse, hashlib, json, shutil, urllib.request
from pathlib import Path
from urllib.parse import urlparse

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sources",type=Path,default=Path("audio-library/SOURCES.json"))
    p.add_argument("--collection",required=True,choices=("oculus-audio-pack","meta-piano","meta-nylon-guitar","meta-steel-guitar"))
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args()
    data=json.loads(a.sources.read_text(encoding="utf-8"))
    meta=next(x for x in data["external_sources"] if x["id"]=="meta-open-sound")
    item=next(x for x in meta["release_assets"] if x["collection"]==a.collection)
    url=item["wav_master_url"]; expected_size=int(item["wav_master_size_bytes"]); expected_sha=item["wav_master_sha256"].lower()
    filename=Path(urlparse(url).path).name
    a.output_dir.mkdir(parents=True,exist_ok=True)
    dest=a.output_dir/filename
    tmp=dest.with_suffix(dest.suffix+".part")
    req=urllib.request.Request(url,headers={"User-Agent":"Nolane-Audio-Library/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=240) as response,tmp.open("wb") as out:
            shutil.copyfileobj(response,out,length=1024*1024)
        if tmp.stat().st_size!=expected_size:
            raise ValueError(f"size mismatch: expected {expected_size}, got {tmp.stat().st_size}")
        digest=sha256(tmp)
        if digest!=expected_sha:
            raise ValueError(f"SHA-256 mismatch: expected {expected_sha}, got {digest}")
        tmp.replace(dest)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    print(json.dumps({
        "collection":a.collection,"archive":dest.name,"path":str(dest),
        "size_bytes":dest.stat().st_size,"sha256":digest,
        "license":item["license"],"license_url":item["license_url"],
        "source_url":url,"release_tag":meta["permanent_mirror_release"]["tag"]
    },indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
