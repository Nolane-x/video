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
    "GalleryPoster index={index%30}", "count=Math.round(84+12*progress)",
    "day=Math.round(111+27*progress)", "4.7%", "open-design.ai",
    "rotateY(180deg)", "BPM=114.84375"
]
for token in required:
    haystack=score if token == "BPM=114.84375" else source
    need(token in haystack, "missing required source token: " + token)

print("PASS: 12 source-indexed sections / 28 montage cuts / 30 gallery panels / 1119 frames / launch preview / countdown / MORRO tile / end card")
