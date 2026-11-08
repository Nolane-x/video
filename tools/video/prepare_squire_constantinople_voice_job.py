#!/usr/bin/env python3
"""Prepare an eligible VoiceStudio English narration job for the 1453 film."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
from urllib.request import Request,urlopen
MANIFEST_URL="https://github.com/Nolane-x/VoiceStudio/releases/download/voice-library-latest/manifest.json"
PREFERRED_VOICE="en-vieneu-v3turbo-adam-3f0c9b"
COMMERCIAL_MARKERS={"upstream-model-card-permits-generated-audio","apache-2.0-model-and-voice-assets"}
def read_manifest(path):
    if path: data=json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        req=Request(MANIFEST_URL,headers={"Accept":"application/json","User-Agent":"Nolane-Squire-Production/1.0"})
        with urlopen(req,timeout=90) as res:data=json.loads(res.read().decode("utf-8"))
    if not isinstance(data,dict) or not isinstance(data.get("voices"),list):raise ValueError("VoiceStudio manifest missing voices")
    return data
def eligible(row):
    rights=row.get("rights") or {}; checks=row.get("signal_checks") or {}
    return row.get("language")=="en" and row.get("watermark")=="verified" and checks.get("status")=="passed" and rights.get("commercial_use") in COMMERCIAL_MARKERS
def choose_voice(manifest):
    rows=[r for r in manifest["voices"] if isinstance(r,dict) and eligible(r)]
    preferred=next((r for r in rows if r.get("id")==PREFERRED_VOICE),None)
    if preferred:return preferred,"Preferred Squire English voice; exact live manifest confirms eligibility."
    grades={"A":0,"A-":1,"B+":2,"B":3,"B-":4}
    kokoro=[r for r in rows if "kokoro" in str(r.get("engine","")).casefold() and r.get("upstream_quality_grade") in grades]
    if kokoro:
        kokoro.sort(key=lambda r:(grades[r["upstream_quality_grade"]],r.get("id","")))
        return kokoro[0],"Highest graded eligible English Kokoro voice in live manifest."
    vieneu=[r for r in rows if "vieneu" in str(r.get("engine","")).casefold()]
    if vieneu:return sorted(vieneu,key=lambda r:(r.get("display_name",""),r.get("id","")))[0],"Eligible English VieNeu fallback."
    raise RuntimeError("No eligible English voice passed rights, watermark and signal checks.")
def clean_script(path):
    raw=path.read_text(encoding="utf-8").replace("\r\n","\n").strip()
    raw=re.sub(r"\n+\d[\d,]* words\..*$","",raw,flags=re.S).strip()
    rows=[re.sub(r"\s+"," ",p).strip() for p in re.split(r"\n\s*\n",raw) if p.strip()]
    if not rows:raise ValueError("Empty script")
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--script",required=True);ap.add_argument("--output",required=True);ap.add_argument("--metadata",required=True);ap.add_argument("--manifest")
    a=ap.parse_args();manifest=read_manifest(a.manifest);voice,rationale=choose_voice(manifest);paras=clean_script(Path(a.script))
    segments=[{"id":f"p{i:03d}","text":p,"pause_ms_after":360 if i<len(paras) else 0} for i,p in enumerate(paras,1)]
    engine=str(voice.get("engine","")).casefold()
    engine="vieneu" if "vieneu" in engine else ("kokoro" if "kokoro" in engine else "")
    if not engine:raise RuntimeError(f"Unsupported voice engine: {voice.get('engine')!r}")
    chars=sum(len(x["text"]) for x in segments)
    if chars>30000:raise ValueError(f"Script exceeds 30,000 characters: {chars}")
    job={"schema_version":1,"job_id":"constantinople-1453-hfr-longform","title":"53 Days to the End of an Empire","language":"en","engine":engine,"voice_id":voice["id"],"segments":segments}
    meta={"schema_version":1,"manifest_built_at":manifest.get("built_at"),"voice_id":voice["id"],"display_name":voice.get("display_name"),"engine":voice.get("engine"),"upstream_quality_grade":voice.get("upstream_quality_grade"),"rights":voice.get("rights"),"signal_checks":voice.get("signal_checks"),"watermark":voice.get("watermark"),"rationale":rationale,"paragraph_count":len(segments),"script_characters":chars,"no_real_person_impersonation":True}
    Path(a.output).write_text(json.dumps(job,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    Path(a.metadata).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Voice contract ok: {voice['id']} | {len(segments)} paragraphs | {chars} chars")
if __name__=="__main__":
    try:raise SystemExit(main())
    except Exception as e:print(f"[constantinople-voice] {type(e).__name__}: {e}",file=sys.stderr);raise SystemExit(1)
