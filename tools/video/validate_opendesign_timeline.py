#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path

root=Path(__file__).resolve().parents[2]
data=json.loads((root/"video-projects/opendesign-motion/shot-map.json").read_text())
source=(root/"video-projects/remotion/src/OpenDesignMotion.tsx").read_text()
score=(root/"tools/video/generate_opendesign_score.py").read_text()

def need(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit("FAIL: " + msg)

need(data["output"]["durationFrames"] == 1119, "wrong master frame count")
need(data["output"]["fps"] == 30, "wrong master fps")
shots=data["shots"]
need(len(shots) == 12, "expected 12 sections")
cursor=0
for shot in shots:
    need(shot["startFrame"] == cursor, shot["id"] + " is not contiguous")
    need(shot["endFrame"] > shot["startFrame"], shot["id"] + " is empty")
    cursor=shot["endFrame"]
need(cursor == 1119, "root timeline must end at frame 1119")

beats=next(shot for shot in shots if shot["id"] == "S06")["posterBeats"]
need(len(beats) == 28, "expected 28 native-frame montage cuts")
need(sum(beat[1] for beat in beats) == 269, "poster beat duration must total 269")

poster_start=source.index("const PosterSequence")
poster_end=source.index("\nconst ", poster_start + len("const PosterSequence"))
poster_block=source[poster_start:poster_end]
actual=[(int(a), int(b), name) for a,b,name in re.findall(
    r"<Sequence from=\{(\d+)\} durationInFrames=\{(\d+)\}><([A-Za-z0-9]+)", poster_block
)]
expected=[]
frame=0
for name,duration in beats:
    expected.append((frame, duration, name))
    frame += duration
need(actual == expected, "nested montage order/timing differs from shot map")

root_start=source.index("export const OpenDesignMotion")
root_block=source[root_start:]
actual_root=[(int(a), int(b), name) for a,b,name in re.findall(
    r"<Sequence from=\{(\d+)\} durationInFrames=\{(\d+)\}><([A-Za-z0-9]+)", root_block
)]
expected_root=[(shot["startFrame"], shot["endFrame"]-shot["startFrame"], shot["component"]) for shot in shots]
need(actual_root == expected_root, "root JSX differs from shot map")

# Every scene referenced by the authoritative shot map must actually exist.
missing=[]
for shot in shots:
    if not re.search(rf"^const\s+{re.escape(shot['component'])}\s*=", source, re.M):
        missing.append(shot["component"])
for name,_duration in beats:
    if not re.search(rf"^const\s+{re.escape(name)}\s*=", source, re.M):
        missing.append(name)
need(not missing, "components referenced by shot map / montage are missing: " + ", ".join(sorted(set(missing))))

required=[
    "Launch film", "Make a 10s launch film", "for our app.",
    "DeepSeek V4.1", "Claude Opus 5.5", "CountdownOne",
    "GalleryPoster index={index%30}", "const counts=[80,82,84,87,91,93,94,96]",
    "days=[88,96,104,111,119,126,132,138]", "3.7%", "open-design.ai",
    "rotateY(180deg)", "squiggle-preview-v18", "BPM=114.84375"
]
for token in required:
    haystack=score if token == "BPM=114.84375" else source
    need(token in haystack, "missing required source token: " + token)

# Lock source-observed values and preview art against silent regressions.
audit = data.get("visualAudit", [])
need(any(item.get("frame") == 523 and item.get("content") == "80K / Day 88" for item in audit), "frame 523 must record 80K / Day 88")
need(any(item.get("frame") == 510 and "ring transition" in item.get("content", "") for item in audit), "frame 510 ring transition observation is missing")
need(any(item.get("frame") == 933 and "rounded-square emblem" in item.get("content", "") for item in audit), "frame 933 standalone logo-tile observation is missing")
need(any(item.get("frame") == 1118 and "domain capsule" in item.get("content", "") for item in audit), "frame 1118 branded end card observation is missing")
need(any(item.get("frame") == 547 and "3.7%" in item.get("content", "") for item in audit), "frame 547 must record 3.7%")
need("const counts=[80,82,84,87,91,93,94,96]" in source, "Star History source value sequence is missing")
need("days=[88,96,104,111,119,126,132,138]" in source, "Star History day sequence is missing")
need("3.7%" in source and "4.7%" not in source, "eye readout must match 3.7%")
need("squiggle-preview-v18" in source, "black/white squiggle launch preview is missing")
need("f<15?-90+128*e(f,0,15):f<45?38+49*e(f,15,45):87+93*e(f,45,75)" in source, "camera cube face order / rotation timing is missing")
need("if(f<12)return <AbsoluteFill" in source, "separate app-mark lead-in is missing")
need("THE FUTURE / 100K" in source, "yellow 100K cube face is missing")
need("cubeClock-v22" in source, "blue/gold clock face must be on the top surface")
need("rotateX=18+44*Math.sin(Math.min(1,f/75)*Math.PI)" in source, "cube pitch schedule for top/underside faces is missing")
need('rotateX(-90deg) translateZ("+z+"px)' in source, "blue clock must occupy the top face")
need('rotateX(90deg) translateZ("+z+"px)' in source, "lime EASE must occupy the underside")
need("MORRO / FORM STUDY" in source, "large purple MORRO transition is missing")
need("OpenDesign Motion" in source and "open-design.ai" in source, "full branded end card is missing")
need("resolve=e(f,0,2)" in source, "IN to LINEAR transition timing is missing")
need("r=420-70*e(f,0,1)" in source, "green ring transition timing is missing")
need("durationInFrames={14}><LinearPoster" in source and "from={194} durationInFrames={6}><GreenCircleTransition" in source, "source-frame 510 typography/ring boundary is incorrect")
need("MORRO / 01" in source, "illustrated camera cube face artwork is missing")

print("PASS: 12 source-indexed sections / 28 montage cuts / 30 gallery panels / 1119 frames / launch preview / countdown / MORRO tile / end card")
