#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[2]
data=json.loads((root/"video-projects/opendesign-motion/shot-map.json").read_text())
source=(root/"video-projects/remotion/src/OpenDesignMotion.tsx").read_text()
score=(root/"tools/video/generate_opendesign_score.py").read_text()
def need(ok,msg):
 if not ok: raise SystemExit("FAIL: "+msg)
need(data["output"]["durationFrames"]==1119,"wrong master frame count")
need(data["output"]["fps"]==30,"wrong master fps")
shots=data["shots"]; need(len(shots)==12,"expected 12 sections")
cursor=0
for s in shots:
 need(s["startFrame"]==cursor,s["id"]+" is not contiguous"); need(s["endFrame"]>s["startFrame"],s["id"]+" is empty"); cursor=s["endFrame"]
need(cursor==1119,"root timeline must end at frame 1119")
beats=next(s for s in shots if s["id"]=="S06")["posterBeats"]
need(len(beats)==20,"expected 20 source-matched poster beats"); need(sum(b[1] for b in beats)==269,"poster beat duration must total 269")
block=source.split("const PosterSequence =",1)[1].split("\nconst ",1)[0]
actual=[(int(a),int(b),c) for a,b,c in re.findall(r"<Sequence from=\{(\d+)\} durationInFrames=\{(\d+)\}><([A-Za-z0-9]+)",block)]
expected=[]; frame=0
for comp,dur in beats: expected.append((frame,dur,comp)); frame+=dur
need(actual==expected,"nested montage order/timing differs from shot map")
root=source.split("export const OpenDesignMotion",1)[1]
actualRoot=[(int(a),int(b),c) for a,b,c in re.findall(r"<Sequence from=\{(\d+)\} durationInFrames=\{(\d+)\}><([A-Za-z0-9]+)",root)]
expectedRoot=[(s["startFrame"],s["endFrame"]-s["startFrame"],s["component"]) for s in shots]
need(actualRoot==expectedRoot,"root JSX differs from shot map")
for x in ["Launch film","Make a 10s launch film for our app.","GPT-6-Astra","Claude Opus 5.5","MorroCubeIntro","const ProjectCube=","open-design.ai","rotateY(180deg)","const Comic1952","const Comic1962","const DotPoster","const GreenGhostTransition","80K","Day 88","96K","Day 138","const CoursesPoster"]:
 need(x in source,"missing required source token: "+x)
need("BPM=114.84375" in score,"score BPM does not match source tempo")
print("PASS: 12 source-indexed sections / 20 poster beats / 1119 frames / launch preview states / countdown / MORRO tile / end card")
