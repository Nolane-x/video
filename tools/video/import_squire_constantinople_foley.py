#!/usr/bin/env python3
"""Import item-level CC0 recorded cues for the Constantinople candidate.
This checks provenance, decode and hashes; it does NOT constitute human audition.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
EXTS={".wav",".ogg",".mp3",".flac",".aiff",".m4a"}
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def audio_files(root):return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in EXTS)
def pick(root,*terms):
    rows=[]
    for p in audio_files(root):
        stem=p.stem.casefold();score=sum(3 for t in terms if t in stem)
        if score:rows.append((score,p.stat().st_size,p))
    if not rows:raise FileNotFoundError(f"No exact-ish cue match in {root}: {terms}")
    rows.sort(key=lambda x:(-x[0],-x[1],str(x[2])));return rows[0][2]

def source_definitions(root: Path):
    """Explicit CC0 cue map; never infer a cannon impact from a sword archive or arrow fletching."""
    impact_page="https://opengameart.org/content/battle-at-sea"
    weapon_page="https://opengameart.org/content/medieval-sound-effects-weapon-impacts"
    texture_page="https://opengameart.org/content/medieval-sound-effects-weapon-textures"
    return {
      "battle_roar":(root/"crowd"/"crowd_shouting.ogg",1,"StarNinjas","https://opengameart.org/content/crowd-shoutingspeaking-ambience","Designed group-voice layer; not a medieval field recording."),
      "wind_loop":(root/"wind"/"park_ambience_wind.wav",1,"Thimras","https://opengameart.org/content/park-ambiences","Modern open-field wind recording; not period-specific."),
      "bed_war":(root/"score"/"Eye_of_the_Storm.wav",2,"Indieteur","https://opengameart.org/content/eye-of-the-storm-0","Modern orchestral score candidate; not historically authentic music."),
      "sword_clash":(pick(root/"weapon-impact","clash","sword","blade"),1,"Ben Jaszczak & Brian Nelson",weapon_page,"Recorded weapon contact; exact take requires human audition."),
      "siege_impact":(root/"battle-at-sea"/"cannon_hit_wall_no_splash.ogg",1,"Thimras",impact_page,"CC0 recorded stone-wall impact candidate; not a recording of the 1453 siege."),
      "cannon_fire":(root/"battle-at-sea"/"cannon_fire_1.ogg",1,"Thimras",impact_page,"CC0 recorded cannon-fire effect candidate; not a historically exact 1453 artillery recording."),
      "arrow_whoosh":(pick(root/"weapon-textures","crossbow","bolt","pass","arrow"),1,"Ben Jaszczak & Brian Nelson",texture_page,"Recorded projectile pass/handling texture; not an arrow impact.")
    }

def convert(src,dst,channels=1):
    dst.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-vn","-ar","48000","-ac",str(channels),"-c:a","pcm_s16le",str(dst)],check=True)
    subprocess.run(["ffmpeg","-hide_banner","-v","error","-i",str(dst),"-f","null","-"],check=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--source-root",required=True,type=Path);ap.add_argument("--kit",required=True,type=Path);ap.add_argument("--project",required=True,type=Path);a=ap.parse_args()
    r=a.source_root.resolve();kit=a.kit.resolve();project=a.project.resolve();sfx=kit/"audio"/"sfx";music=kit/"audio"/"music"
    defs=source_definitions(r)
    rows=[]
    for alias,(src,ch,creator,url,note) in defs.items():
        if not src.is_file():raise FileNotFoundError(f"Missing source for {alias}: {src}")
        dst=(music/"bed_war_100bpm.wav") if alias=="bed_war" else (sfx/f"{alias}.wav")
        if alias=="bed_war":
            for old in music.glob("bed_war_*.wav"):old.unlink()
        convert(src,dst,ch)
        rows.append({"alias":alias,"source":src.name,"creator":creator,"source_url":url,"license":"CC0-1.0","source_sha256":sha(src),"converted_path":str(dst.relative_to(kit)),"converted_sha256":sha(dst),"sample_rate_hz":48000,"channels":ch,"human_auditioned":False,"approved_for_final_mix":False,"note":note})
    out=project/"story"/"FOLEY-SOURCE-MANIFEST.json";out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"status":"TECHNICAL_IMPORT_VERIFIED_HUMAN_AUDITION_PENDING","assets":rows,"review_required":True,"limitations":["Source files were technically decoded and hashed but were not human-auditioned in this workflow.","Crowd is a designed group-voice layer; the wind is a modern open-field recording; the score is modern orchestral.","Cannon fire and stone-wall impact are CC0 recorded effect candidates from Battle at Sea; they are not recordings of the 1453 siege.","Arrow source is a projectile pass/handling texture, not an arrow impact.","Do not describe any candidate as publication-approved until exact-file audition decisions are exported and validated."]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Imported {len(rows)} CC0 recorded cues; human auditions=0; publication approvals=0.")
if __name__=="__main__":main()
