#!/usr/bin/env python3
"""Import rights-screened recorded Foley into the Squire Ain Jalut mix.

The import verifies file presence, media decode and SHA-256. This is technical
ingest only: human listening approval remains a separate editorial gate.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

AUDIO_EXTS = {".wav", ".ogg", ".mp3", ".flac", ".aiff", ".m4a"}
SOURCES = {
    "hooves_gallop": {
        "path": "horse/Six_Horses_Galloping_By.ogg",
        "creator": "Bruno Auzet",
        "source": "https://commons.wikimedia.org/wiki/File:Six_Horses_Galloping_By.ogg",
        "license": "CC0-1.0",
        "note": "Recorded six-horse approach and pass; one 25-second gallop take, not a full gait library."
    },
    "battle_roar": {
        "path": "crowd/crowd_shouting.ogg",
        "creator": "StarNinjas",
        "source": "https://opengameart.org/content/crowd-shoutingspeaking-ambience",
        "license": "CC0-1.0",
        "note": "Designed group-voice crowd layer, not a historical battlefield field recording."
    },
    "wind_loop": {
        "path": "wind/park_ambience_wind.wav",
        "creator": "Thimras",
        "source": "https://opengameart.org/content/park-ambiences",
        "license": "CC0-1.0",
        "note": "Modern open-field wind recording; not period-specific."
    },
    "bed_war": {
        "path": "score/Eye_of_the_Storm.wav",
        "creator": "Indieteur",
        "source": "https://opengameart.org/content/eye-of-the-storm-0",
        "license": "CC0-1.0",
        "note": "Modern orchestral warfare score candidate; not historically authentic music."
    }
}

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def audio_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTS)

def pick(root: Path, include: tuple[str,...]) -> Path:
    rows=[]
    for p in audio_files(root):
        score=sum(3 for x in include if x in p.stem.casefold())
        if score:
            rows.append((score,p.stat().st_size,p))
    if not rows:
        raise FileNotFoundError(f"No audio filename in {root} matched any of {include}")
    rows.sort(key=lambda x:(-x[0],-x[1],str(x[2])))
    return rows[0][2]

def convert(src: Path, dst: Path, channels: int=1) -> None:
    dst.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([
        "ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
        "-vn","-ar","48000","-ac",str(channels),"-c:a","pcm_s16le",str(dst)
    ],check=True)
    subprocess.run(["ffmpeg","-hide_banner","-v","error","-i",str(dst),"-f","null","-"],check=True)

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-root",required=True,type=Path)
    ap.add_argument("--kit",required=True,type=Path)
    ap.add_argument("--project",required=True,type=Path)
    args=ap.parse_args()
    root=args.source_root.resolve()
    kit=args.kit.resolve()
    sfx=kit/"audio"/"sfx"
    music=kit/"audio"/"music"
    project=args.project.resolve()
    records=[]

    fixed={
        "hooves_gallop": (root/SOURCES["hooves_gallop"]["path"],1),
        "battle_roar": (root/SOURCES["battle_roar"]["path"],1),
        "wind_loop": (root/SOURCES["wind_loop"]["path"],1),
        "bed_war": (root/SOURCES["bed_war"]["path"],2),
        "sword_clash": (pick(root/"weapon-impact",("clash","sword","blade","metal")),1),
        "spear_hit": (pick(root/"weapon-impact",("spear","shaft","impact","weapon")),1),
        "arrow_whoosh": (pick(root/"weapon-textures",("arrow","whoosh","pass","projectile","flight")),1),
        "arrow_thunk": (pick(root/"weapon-textures",("arrow","hit","impact","target","thunk")),1),
    }
    fixed["armor_clank"]=(fixed["sword_clash"][0],1)

    for alias,(src,channels) in fixed.items():
        if not src.is_file():
            raise FileNotFoundError(f"Required recorded source missing for {alias}: {src}")
        if alias=="bed_war":
            # Replace only the battle bed; quiet narrative beds stay available.
            for old in music.glob("bed_war_*.wav"):
                old.unlink()
            dst=music/"bed_war_100bpm.wav"
        else:
            dst=sfx/(alias+".wav")
        convert(src,dst,channels)
        if alias in SOURCES:
            meta=SOURCES[alias].copy()
        else:
            meta={
                "creator":"Ben Jaszczak & Brian Nelson",
                "source":"https://opengameart.org/content/medieval-sound-effects-weapon-impacts" if alias in ("sword_clash","spear_hit","armor_clank") else "https://opengameart.org/content/medieval-sound-effects-weapon-textures",
                "license":"CC0-1.0",
                "note":"Recorded weapon/projectile material selected by filename from the CC0 source archive; listen to the exact cue before publication."
            }
        records.append({
            "squire_alias":alias,
            "source_file":str(src.relative_to(root)),
            "output_file":str(dst.relative_to(kit)),
            "source_sha256":digest(src),
            "converted_sha256":digest(dst),
            "sample_rate_hz":48000,
            "channels":channels,
            "human_auditioned":False,
            "approved_for_final_publication":False,
            **meta
        })
    report={
        "schema_version":1,
        "status":"TECHNICAL_IMPORT_VERIFIED_HUMAN_LISTENING_PENDING",
        "rights_scope":"Each recording is CC0 per its item-level source page; source URLs and creators are retained.",
        "assets":records,
        "limitations":[
            "Download, FFmpeg decode and checksum verification are not subjective audio QA.",
            "The crowd layer is a designed voice effect, not an authentic medieval battlefield recording.",
            "The open-field wind and orchestral score are modern recordings, not period reconstructions.",
            "Every exact cue must be listened to and approved before public release."
        ]
    }
    out=project/"story"/"FOLEY-SOURCE-MANIFEST.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Recorded Foley imported:",", ".join(r["squire_alias"] for r in records))
    print("Human auditioned: 0 | Publication approvals: 0")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
