#!/usr/bin/env python3
"""Acquire and package a small, provenance-rich CC0 Foley collection.

Raw media stays out of Git history. Every item remains un-auditioned until a
human listens to it; successful probing is not creative or legal approval.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import stat
import subprocess
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

AUDIO_EXTENSIONS = {".wav", ".wave", ".ogg", ".oga", ".mp3", ".flac", ".m4a", ".aac", ".aiff", ".aif", ".opus"}
USER_AGENT = "Nolane-Video-Illustrated-History-Foley/1.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_zip_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            name = PurePosixPath(item.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"Unsafe ZIP member path: {item.filename}")
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError(f"ZIP symlink member is not allowed: {item.filename}")
            target = (destination / Path(*name.parts)).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"ZIP member escapes extraction directory: {item.filename}")
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(item) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def download_source(source: dict[str, Any], destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(source["download_url"], headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    size = destination.stat().st_size
    minimum = int(source.get("minimum_bytes", 1))
    if size < minimum:
        raise ValueError(f"{source['source_id']} download too small: {size} < {minimum}")
    digest = sha256_file(destination)
    expected = source.get("expected_sha256")
    if expected and digest.lower() != expected.lower():
        raise ValueError(f"{source['source_id']} SHA-256 mismatch: {digest}")
    return {
        "source_id": source["source_id"],
        "download_url": source["download_url"],
        "download_filename": source["download_filename"],
        "download_size_bytes": size,
        "download_sha256": digest,
        "expected_sha256_pinned": bool(expected),
    }


def extract_source(source: dict[str, Any], archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    kind = source["archive_type"]
    if kind == "7z":
        executable = shutil.which("7z") or shutil.which("7zz")
        if not executable:
            raise RuntimeError("7z/7zz is required to extract OpenGameArt .7z packs")
        subprocess.run(
            [executable, "x", "-y", f"-o{destination}", str(archive_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    elif kind == "zip":
        safe_zip_extract(archive_path, destination)
    elif kind == "file":
        shutil.copy2(archive_path, destination / source["download_filename"])
    else:
        raise ValueError(f"Unsupported archive type: {kind}")

    root = destination.resolve()
    for path in destination.rglob("*"):
        if path.is_file() and not path.resolve().is_relative_to(root):
            raise ValueError(f"Extracted path escapes source directory: {path}")


def probe_audio(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,format_name:stream=codec_name,codec_type,sample_rate,channels,channel_layout,bits_per_sample,bits_per_raw_sample",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = [stream for stream in data.get("streams", []) if stream.get("codec_type") == "audio"]
    if not streams:
        raise ValueError(f"No audio stream detected in {path}")
    stream = streams[0]
    duration = float(data.get("format", {}).get("duration", 0) or 0)
    if duration <= 0:
        raise ValueError(f"Invalid or missing duration for {path}")
    return {
        "duration_seconds": round(duration, 6),
        "container_format": data.get("format", {}).get("format_name"),
        "codec": stream.get("codec_name"),
        "sample_rate_hz": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
        "channels": int(stream["channels"]) if stream.get("channels") is not None else None,
        "channel_layout": stream.get("channel_layout"),
        "bits_per_sample": stream.get("bits_per_sample") or stream.get("bits_per_raw_sample"),
    }


def build_bundle(manifest: dict[str, Any], download_root: Path, output_root: Path, probe=probe_audio) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    package_root = output_root / "package"
    if package_root.exists():
        shutil.rmtree(package_root)
    assets_root = package_root / "assets"
    assets_root.mkdir(parents=True)

    acquisition_records: list[dict[str, Any]] = []
    asset_by_hash: dict[str, dict[str, Any]] = {}
    source_counts: Counter[str] = Counter()

    for source in manifest["sources"]:
        source_id = source["source_id"]
        archive_path = download_root / source_id / source["download_filename"]
        if not archive_path.is_file():
            raise FileNotFoundError(f"Missing acquired source: {archive_path}")
        archive_sha = sha256_file(archive_path)
        expected = source.get("expected_sha256")
        if expected and archive_sha.lower() != expected.lower():
            raise ValueError(f"{source_id} archive SHA-256 mismatch")

        extracted_root = download_root / source_id / "extracted"
        extract_source(source, archive_path, extracted_root)
        acquisition_records.append({
            "source_id": source_id,
            "title": source["title"],
            "creator": source["creator"],
            "source_page": source["source_page"],
            "download_url": source["download_url"],
            "download_filename": source["download_filename"],
            "archive_sha256": archive_sha,
            "archive_size_bytes": archive_path.stat().st_size,
            "license": source["license"],
            "license_url": source["license_url"],
            "rights_class": source["rights_class"],
        })

        for audio_path in sorted(extracted_root.rglob("*")):
            if not audio_path.is_file() or audio_path.suffix.lower() not in AUDIO_EXTENSIONS:
                continue
            if "__MACOSX" in audio_path.parts or audio_path.name.startswith("._") or audio_path.name == ".DS_Store":
                continue
            relative = audio_path.relative_to(extracted_root)
            digest = sha256_file(audio_path)
            if digest in asset_by_hash:
                existing = asset_by_hash[digest]
                if source_id not in existing["source_ids"]:
                    existing["source_ids"].append(source_id)
                continue

            metadata = probe(audio_path)
            rel_posix = PurePosixPath(relative.as_posix())
            target_rel = PurePosixPath("assets") / source_id / rel_posix
            target = package_root.joinpath(*target_rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(audio_path, target)
            source_counts[source_id] += 1
            asset_by_hash[digest] = {
                "asset_id": f"ihf-{digest[:16]}",
                "title": audio_path.stem.replace("_", " ").replace("-", " "),
                "path": target_rel.as_posix(),
                "original_filename": audio_path.name,
                "source_ids": [source_id],
                "creator": source["creator"],
                "source_page": source["source_page"],
                "license": source["license"],
                "license_url": source["license_url"],
                "rights_class": source["rights_class"],
                "sha256": digest,
                "size_bytes": audio_path.stat().st_size,
                **metadata,
                "tags": source.get("tags", []),
                "human_auditioned": False,
                "approved_for_final_mix": False,
                "review_note": "Metadata/codec probe only. Human listening and contextual approval still required.",
            }

    assets = sorted(asset_by_hash.values(), key=lambda item: (item["source_ids"][0], item["original_filename"].lower()))
    if not assets:
        raise RuntimeError("No audio assets were discovered in the acquired source packs")

    catalog = {
        "schema_version": 1,
        "collection": manifest["collection"],
        "release_tag": manifest["release_tag"],
        "generated_by": "tools/audio/build_illustrated_history_foley_bundle.py",
        "assets": assets,
        "summary": {
            "source_count": len(acquisition_records),
            "audio_asset_count": len(assets),
            "source_audio_counts": dict(source_counts),
            "unique_audio_bytes": sum(item["size_bytes"] for item in assets),
            "human_auditioned": 0,
            "approved_for_final_mix": 0,
        },
    }
    (package_root / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_root / "source-register.json").write_text(json.dumps(acquisition_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_root / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme = f"""# {manifest['collection']}

This is a curated CC0 1.0 source pack for historical/illustrated video production.

- Original audio files are preserved in their downloaded formats.
- Per-file source pages, creators, license URLs and SHA-256 hashes are in catalog.json and source-register.json.
- Every item is initially marked human_auditioned=false and approved_for_final_mix=false.
- A successful download and FFprobe check is not a listening/quality approval.
- The crowd file is a creator-edited voice-group effect, not an authentic historical field recording.
- The six-horse file is described as a horse approach-and-pass recording.
- Weapon-impact and generic thwack files must be matched to the material and visual contact, not reused indiscriminately.

Open AUDIO_PREVIEW.html in a browser to audition the extracted files offline. Retain the CC0 and provenance records with the media.
"""
    (package_root / "README.md").write_text(readme, encoding="utf-8")

    rows = []
    for item in assets:
        asset_id = html.escape(item["asset_id"], quote=True)
        title = html.escape(item["title"])
        rel_path = html.escape(item["path"], quote=True)
        meta = html.escape(
            f"{item['duration_seconds']:.2f}s · {item.get('codec') or 'audio'} · "
            f"{item.get('sample_rate_hz') or '?'} Hz · {item.get('channels') or '?'} ch"
        )
        creator = html.escape(item["creator"])
        source_id = html.escape(item["source_ids"][0])
        source_page = html.escape(item["source_page"], quote=True)
        license_name = html.escape(item["license"])
        license_url = html.escape(item["license_url"], quote=True)
        digest = html.escape(item["sha256"])
        tags = html.escape(", ".join(item["tags"]))
        search_value = html.escape(
            (item["title"] + " " + " ".join(item["tags"]) + " " + item["original_filename"]).lower(),
            quote=True,
        )
        rows.append(
            f'<article class="cue" data-id="{asset_id}" data-search="{search_value}" '
            f'data-source="{source_id}" data-rights="{html.escape(item["rights_class"], quote=True)}" '
            f'data-sha="{digest}">'
            f'<header><div><span class="eyebrow">{source_id}</span><h2>{title}</h2></div>'
            f'<span class="status">NOT HEARD</span></header>'
            f'<p class="meta">{meta} · {item["size_bytes"]:,} bytes</p>'
            f'<div class="provenance"><span>Creator: {creator}</span>'
            f'<span>License: <a href="{license_url}" target="_blank" rel="noreferrer">{license_name}</a></span>'
            f'<span>SHA-256: <code>{digest}</code></span>'
            f'<span>Tags: {tags}</span>'
            f'<a href="{source_page}" target="_blank" rel="noreferrer">Open original source page ↗</a></div>'
            f'<audio controls preload="none" src="{rel_path}"></audio>'
            f'<div class="review-grid">'
            f'<label>Listening decision<select class="decision">'
            f'<option value="unreviewed">Not reviewed</option>'
            f'<option value="keep_candidate">Keep as candidate</option>'
            f'<option value="reject">Reject</option>'
            f'</select></label>'
            f'<label>Production fit<select class="rating">'
            f'<option value="">Not rated</option><option value="1">1 — Poor</option>'
            f'<option value="2">2 — Weak</option><option value="3">3 — Usable</option>'
            f'<option value="4">4 — Good</option><option value="5">5 — Excellent</option>'
            f'</select></label>'
            f'<label class="note">Reviewer notes<textarea class="notes" rows="2" '
            f'placeholder="Material, distance, quality, loop/clicks, period fit, best shot…"></textarea></label>'
            f'<label class="check"><input class="heard" type="checkbox"> I listened to this exact file</label>'
            f'<label class="check"><input class="approved" type="checkbox" disabled> Approved for final mix</label>'
            f'</div><p class="gate">Downloaded and decoded; not yet human-auditioned.</p></article>'
        )
    source_options = "".join(
        f'<option value="{html.escape(source["source_id"], quote=True)}">'
        f'{html.escape(source["title"])}'
        f'</option>'
        for source in manifest["sources"]
    )
    preview_template = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Illustrated History Foley — Audition & Review Console</title>
<style>
:root{color-scheme:dark;--bg:#101114;--panel:#1a1d22;--line:#343943;--muted:#a7afba;--ink:#f1eee6;--accent:#d8b77c;--green:#87b99b;--red:#d88e87}
*{box-sizing:border-box}body{font:15px/1.5 Inter,ui-sans-serif,system-ui,sans-serif;max-width:1180px;margin:0 auto;padding:28px 18px 80px;background:var(--bg);color:var(--ink)}
h1{font-size:clamp(27px,4vw,42px);line-height:1.08;margin:4px 0 12px;letter-spacing:-.04em}
h2{font-size:19px;line-height:1.2;margin:4px 0 0}.sub{color:var(--muted);max-width:850px}
.warning{border:1px solid #755d38;background:#2b2418;padding:14px 16px;border-radius:12px;margin:20px 0}
.toolbar,.stats,.review-grid{display:grid;gap:10px}.stats{grid-template-columns:repeat(4,minmax(0,1fr));margin:18px 0}
.stat,.panel,.cue{background:var(--panel);border:1px solid var(--line);border-radius:14px}
.stat{padding:12px 14px}.stat strong{display:block;font-size:25px}.stat span,.meta,.eyebrow,.gate,small{color:var(--muted)}
.toolbar{grid-template-columns:2fr 1.3fr 1.3fr auto auto;align-items:end;margin:20px 0}
label{display:block;font-size:12px;color:var(--muted)}input[type=search],select,textarea,button{font:inherit}
input[type=search],select,textarea{width:100%;background:#111317;color:var(--ink);border:1px solid #444a55;border-radius:8px;padding:9px 10px;margin-top:5px}
button{padding:10px 13px;border:1px solid #5a606a;border-radius:9px;background:#252a31;color:var(--ink);cursor:pointer}
button.primary{background:#d8b77c;color:#211c15;border-color:#d8b77c;font-weight:700}button:disabled{opacity:.45;cursor:not-allowed}
.cue{padding:16px;margin:13px 0}.cue header{display:flex;justify-content:space-between;gap:15px;align-items:flex-start}
.eyebrow{text-transform:uppercase;font-size:10px;letter-spacing:.14em}.status{font-size:10px;letter-spacing:.1em;padding:4px 8px;border:1px solid var(--line);border-radius:99px;white-space:nowrap}
.meta{font-size:12px;margin:7px 0 12px}.provenance{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px 14px;color:var(--muted);font-size:12px;margin-bottom:12px;overflow-wrap:anywhere}
a{color:var(--accent)}code{font-size:11px;overflow-wrap:anywhere}audio{width:100%;height:42px;margin:3px 0 10px}
.review-grid{grid-template-columns:1fr 1fr 1.5fr 1fr 1.2fr;align-items:start}.review-grid .note{grid-column:span 1}.check{display:flex;gap:8px;align-items:center;padding-top:27px}.check input{width:17px;height:17px;accent-color:var(--green)}
.gate{font-size:12px;margin:8px 0 0}.cue.reviewed .status{border-color:var(--green);color:var(--green)}.cue.approved-card .gate{color:var(--green)}.cue.rejected .status{border-color:var(--red);color:var(--red)}
.empty{padding:24px;text-align:center;color:var(--muted)}.footer{margin-top:28px;color:var(--muted);font-size:12px}
@media(max-width:900px){.toolbar{grid-template-columns:1fr 1fr}.review-grid{grid-template-columns:1fr 1fr}.review-grid .note{grid-column:span 2}.stats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.review-grid,.provenance{grid-template-columns:1fr}.review-grid .note{grid-column:span 1}.toolbar{grid-template-columns:1fr}.check{padding-top:5px}}
</style>
</head>
<body>
<p class="eyebrow">NOLANE · HISTORICAL AUDIO LIBRARY</p>
<h1>Foley + score audition & review console</h1>
<p class="sub">Listen to the exact source file, assess whether it fits the visible action, then record a decision. This page works offline after you extract the ZIP. Review decisions are saved in this browser and can be exported/imported as JSON.</p>
<div class="warning"><strong>Important approval gate.</strong> Every recording starts unreviewed. FFprobe confirms that a file decodes; it does not confirm sound quality, historical suitability or final-mix approval. A cue cannot be approved for a final mix until you have listened to that exact file and marked it as a candidate.</div>
<div class="stats">
 <div class="stat"><strong id="total">0</strong><span>Total cue files</span></div>
 <div class="stat"><strong id="heard">0</strong><span>Human-auditioned</span></div>
 <div class="stat"><strong id="approved">0</strong><span>Approved for final mix</span></div>
 <div class="stat"><strong id="rejected">0</strong><span>Rejected after listening</span></div>
</div>
<div class="panel" style="padding:15px">
 <div class="toolbar">
  <label>Search<input id="search" type="search" placeholder="horse, katana, arrow, impact, metal…"></label>
  <label>Source<select id="source"><option value="">All source packs</option>{{SOURCE_OPTIONS}}</select></label>
  <label>Review status<select id="status"><option value="">All statuses</option><option value="unreviewed">Not reviewed</option><option value="heard">Listened</option><option value="approved">Approved</option><option value="rejected">Rejected</option></select></label>
  <button id="next">Next unreviewed</button>
  <button id="export" class="primary">Export decisions JSON</button>
 </div>
 <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
  <label style="display:flex;gap:8px;align-items:center"><input id="import" type="file" accept="application/json" style="max-width:250px"> Import previous review</label>
  <button id="clear">Clear this browser's review</button>
  <span id="visible" class="meta"></span>
 </div>
</div>
<div id="cues">{{ASSET_ROWS}}</div>
<p class="footer">Rights class for this pack: CC0 1.0 as recorded in the per-item source manifest. Keep the source register and license links with the files. Approval means your human audition found this particular take suitable for this project; it does not create rights beyond the stated license.</p>
<script>
const PACK_ID="nolane-illustrated-history-foley-review-v0.3.0";
const STORAGE_KEY=PACK_ID+":decisions";
const cards=[...document.querySelectorAll(".cue")];
const byId=new Map(cards.map(card=>[card.dataset.id,card]));
const el=id=>document.getElementById(id);
let decisions=load();
function blank(){return {human_auditioned:false,approved_for_final_mix:false,decision:"unreviewed",rating:"",notes:""}}
function load(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}")}catch{return {}}}
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(decisions));render()}
function state(card){return decisions[card.dataset.id]||blank()}
function apply(card){
 const s=state(card);
 card.querySelector(".decision").value=s.decision||"unreviewed";
 card.querySelector(".rating").value=s.rating||"";
 card.querySelector(".notes").value=s.notes||"";
 card.querySelector(".heard").checked=!!s.human_auditioned;
 const approve=card.querySelector(".approved");
 approve.checked=!!s.approved_for_final_mix;
 approve.disabled=!(s.human_auditioned&&s.decision==="keep_candidate"&&card.dataset.rights==="public_cc0_pd");
 card.classList.toggle("reviewed",!!s.human_auditioned);
 card.classList.toggle("approved-card",!!s.approved_for_final_mix);
 card.classList.toggle("rejected",s.decision==="reject");
 card.querySelector(".status").textContent=s.approved_for_final_mix?"APPROVED":s.decision==="reject"?"REJECTED":s.human_auditioned?"LISTENED":"NOT HEARD";
 card.querySelector(".gate").textContent=s.approved_for_final_mix?"Human audition recorded; approved for this project's final-mix shortlist.":s.human_auditioned?"Listened. Check candidate decision and notes; not approved for final mix.":"Downloaded and decoded; not yet human-auditioned.";
}
function render(){
 cards.forEach(card=>{
  const s=state(card);apply(card);
  const q=el("search").value.trim().toLowerCase();
  const source=el("source").value,status=el("status").value;
  const searchMatch=!q||card.dataset.search.includes(q)||card.dataset.id.includes(q);
  const sourceMatch=!source||card.dataset.source===source;
  const statusMatch=!status||(status==="unreviewed"?!s.human_auditioned:status==="heard"?s.human_auditioned:status==="approved"?s.approved_for_final_mix:status==="rejected"?s.decision==="reject":true);
  card.hidden=!(searchMatch&&sourceMatch&&statusMatch);
 });
 const heard=cards.filter(c=>state(c).human_auditioned).length;
 const approved=cards.filter(c=>state(c).approved_for_final_mix).length;
 const rejected=cards.filter(c=>state(c).decision==="reject"&&state(c).human_auditioned).length;
 el("total").textContent=cards.length;el("heard").textContent=heard;el("approved").textContent=approved;el("rejected").textContent=rejected;
 el("visible").textContent=cards.filter(c=>!c.hidden).length+" of "+cards.length+" shown";
}
function update(card,patch){decisions[card.dataset.id]={...blank(),...state(card),...patch};save()}
cards.forEach(card=>{
 card.querySelector(".decision").addEventListener("change",e=>{
  const s=state(card);let decision=e.target.value;
  if(decision!=="unreviewed"&&!s.human_auditioned){alert("Listen to this exact file and tick the audition checkbox first.");e.target.value="unreviewed";return}
  if(decision==="reject")update(card,{decision,approved_for_final_mix:false});
  else update(card,{decision});
 });
 card.querySelector(".rating").addEventListener("change",e=>update(card,{rating:e.target.value}));
 card.querySelector(".notes").addEventListener("change",e=>update(card,{notes:e.target.value}));
 card.querySelector(".heard").addEventListener("change",e=>{
  if(!e.target.checked){update(card,{human_auditioned:false,approved_for_final_mix:false,decision:"unreviewed"});return}
  update(card,{human_auditioned:true});
 });
 card.querySelector(".approved").addEventListener("change",e=>{
  const s=state(card);
  if(e.target.checked&&!(s.human_auditioned&&s.decision==="keep_candidate"&&card.dataset.rights==="public_cc0_pd")){
   alert("Approval requires an auditioned CC0/PD cue marked Keep as candidate.");e.target.checked=false;return
  }
  update(card,{approved_for_final_mix:e.target.checked});
 });
});
["search","source","status"].forEach(id=>el(id).addEventListener("input",render));
el("next").addEventListener("click",()=>{
 const card=cards.find(c=>!c.hidden&&!state(c).human_auditioned);
 if(!card){alert("No unreviewed cue in the current filter.");return}
 card.scrollIntoView({behavior:"smooth",block:"center"});card.querySelector("audio").focus();
});
el("export").addEventListener("click",()=>{
 const rows=cards.map(c=>({asset_id:c.dataset.id,sha256:c.dataset.sha,...state(c)}));
 const payload={schema_version:"1.0.0",pack:PACK_ID,exported_at:new Date().toISOString(),summary:{total:rows.length,human_auditioned:rows.filter(x=>x.human_auditioned).length,approved_for_final_mix:rows.filter(x=>x.approved_for_final_mix).length},decisions:rows};
 const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="nolane-foley-review-decisions.json";a.click();URL.revokeObjectURL(url);
});
el("import").addEventListener("change",async e=>{
 const file=e.target.files?.[0];if(!file)return;
 try{
  const incoming=JSON.parse(await file.text());
  if(!Array.isArray(incoming.decisions))throw new Error("Missing decisions array");
  const next={...decisions};
  for(const row of incoming.decisions){
   const card=byId.get(row.asset_id);if(!card||row.sha256!==card.dataset.sha)continue;
   const heard=!!row.human_auditioned;
   const keep=heard&&row.decision==="keep_candidate"&&card.dataset.rights==="public_cc0_pd";
   next[row.asset_id]={human_auditioned:heard,decision:heard?row.decision:"unreviewed",rating:row.rating||"",notes:String(row.notes||""),approved_for_final_mix:keep&&!!row.approved_for_final_mix};
  }
  decisions=next;save();alert("Review imported. Only matching asset IDs and SHA-256 hashes were applied.");
 }catch(err){alert("Could not import review JSON: "+err.message)}
 e.target.value="";
});
el("clear").addEventListener("click",()=>{
 if(!confirm("Clear all review decisions saved in this browser for this pack? Export first if you need a backup."))return;
 decisions={};localStorage.removeItem(STORAGE_KEY);render();
});
render();
</script>
</body>
</html>"""
    preview = preview_template.replace("{{SOURCE_OPTIONS}}", source_options).replace("{{ASSET_ROWS}}", "".join(rows))
    (package_root / "AUDIO_PREVIEW.html").write_text(preview, encoding="utf-8")

    package_name = f"{manifest['release_tag']}.zip"
    package_path = output_root / package_name
    if package_path.exists():
        package_path.unlink()
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(package_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(package_root).as_posix())

    report = {
        "collection": manifest["collection"],
        "release_tag": manifest["release_tag"],
        "package": package_name,
        "package_size_bytes": package_path.stat().st_size,
        "package_sha256": sha256_file(package_path),
        "source_count": len(acquisition_records),
        "audio_asset_count": len(assets),
        "source_audio_counts": dict(source_counts),
        "human_auditioned": 0,
        "approved_for_final_mix": 0,
        "status": "ACQUIRED_AND_PROBED_NOT_HUMAN_AUDITIONED",
    }
    (output_root / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_root / "SHA256SUMS.txt").write_text(f"{report['package_sha256']}  {package_name}\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--download", action="store_true", help="Download all sources before building")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.download_dir.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.download:
        records = []
        for source in manifest["sources"]:
            destination = args.download_dir / source["source_id"] / source["download_filename"]
            records.append(download_source(source, destination))
        (args.output_dir / "download-manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = build_bundle(manifest, args.download_dir, args.output_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
