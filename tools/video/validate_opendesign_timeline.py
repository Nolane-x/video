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

s08=next(shot for shot in shots if shot["id"] == "S08")
s09=next(shot for shot in shots if shot["id"] == "S09")
need((s08["startFrame"],s08["endFrame"],s08["endFrame"]-s08["startFrame"]) == (641,769,128), "S08 must end on the source-frame-769 Launch Film handoff")
need((s09["startFrame"],s09["endFrame"],s09["endFrame"]-s09["startFrame"]) == (769,897,128), "S09 must begin at source frame769 and preserve the MORRO cut")
need("const frame=useCurrentFrame()-10;" in source, "Launch Film 10-frame pre-roll must preserve countdown source landmarks")
need("<Sequence from={0} durationInFrames={4}><Phrase phase={0}/></Sequence>" in source, "Any-only opening beat must hold through source frame644")
need("<Sequence from={4} durationInFrames={65}><Phrase phase={1}/></Sequence>" in source, "Any model type-on must start at source frame645 and resolve by 650")
need("<Sequence from={69} durationInFrames={30}><Phrase phase={2}/></Sequence>" in source, "Any agent must enter at source frame710")
need("<Sequence from={99} durationInFrames={30}>" in source and "const orbitProgress=e(f,109,119)" in source, "provider logos must form the reference-timed orbit by source frame760")
need('left:"10%",right:"10%",top:rowTop' in source and "const textSize=phase===2?210+30*(1-e(f,69,79)):210" in source, "Any agent typography must span the source layout")
need("if(frame>=112)return <CountdownOne frame={frame-112}/>" in source, "full-screen countdown must begin at source frame891")
need("frame<76?-1:frame<91?3:frame<106?2:1" in source, "number 1 must remain inside the Launch Film preview at frame885")
need("const CountdownPrism=" in source, "blue extruded countdown prism artwork is missing")
need("wc-cloud-edge-v40" in source and "wc-paper-v40" in source and "wc-pigment-v40" in source and "wc-wash-texture-v40" in source and "const lowerPaint=Array.from({length:132}" in source, "V44 expanded watercolor wash, paper-grain and pigment treatment are missing")
need("wc-cloud-light-v40" in source and "wc-cloud-coral-v40" in source and "wc-ridge-near-v40" in source and "wc-ridge-far-v40" in source and "M-120 1018C-8 1003" in source, "V44 low painted cloud bank and near-bottom blue horizon are missing")
need("left:290,right:290,top:390,height:345" in source and 'translateY("+(55-3*e(f,0,30))+"px) scale("+(0.99-0.05*e(f,0,30)-pressed*.008)+")' in source, "V45 frame0/frame30 prompt card position and width are source-matched")
need("right:40,bottom:87" in source and "width:68,height:68" in source, "V45 submit control size and position are source-matched")
need('fontSize:370,fontWeight:1000,letterSpacing:"-.02em"' in source, "V34 MOTION letter scale and tracking are missing")
need("fontSize:132,fontWeight:850" in source and 'fontSize:40,fontWeight:650,color:"#fff"' in source, "V34 OpenDesign/Introducing title hierarchy is missing")
need("wc-wash-white-v40" in source and "wc-wash-blue-v40" in source and "wc-wash-peach-v40" in source, "V40 broken organic diagonal sky washes are missing")
need("source1973-spectrum-v30" in source, "V30 rainbow optical dispersion is missing")
need("M-132 178V-72C-132 -205 132 -205 132 -72V178" in source, "V30 gold pixel-game portal is missing")
need("mind-prism-v30" in source, "V30 translucent MIND polyhedron is missing")
need('const rings=[540,475,410,345,280,215,150,85,28]' in source and 'id={"ring-v53-"+i}' in source and 'sizes=[76,64,54,46,38,31,25,19,14]' in source, "V53 nine-band concentric tunnel is incomplete")
need("eye-field-v30" in source and "3.7%" in source, "V30 angular blue-grid eye is missing")
need("stars-grid-v31" in source, "V30 yellow/mint 100K stars face is missing")
need("ink-mtn-texture-v30" in source, "V30 ink-wash Launch Film preview is missing")
need("fontSize:116,fontWeight:950" in source, "V46 end-card wordmark scale is missing")
need("zoom=1.0+.28*e(f,36,77)" in source, "V29 enlarged project-wall camera is missing")
need("Array.from({length:26*44}" in source and "row*43+((seed%11)-5)*2.2,r:9+(seed%6)*1.15" in source and "translate(960 540)" in source, "V53 dense 1965 dot field and centred D-shaped badge are incomplete")
need("ONE IDEA..." in source and "MEANWHILE, IN 1962..." in source and "POP ART" in source and "CLICK!" in source, "V29 source-matched 1962 comic panels are missing")
need("1.92+0.04*Math.sin(f/7)" in source, "V30 oversized concentric typography crop is missing")
need("shellLeft=118*(1-zoomExit)" in source and "sidebarWidth=frame<106?586-86*zoomExit" in source, "V29 Launch Film original-window-to-Preview morph is missing")
need("paneRight=frame<106?285*(1-zoomExit):frame<110?109*e(frame,106,110):109+16*e(frame,110,111)" in source, "V29 Preview right-edge frame landmarks are missing")
need("cardTop=frame<106?89+39*zoomExit:frame<110?128-116*e(frame,106,110):12-12*e(frame,110,111)" in source, "V29 Preview top-edge frame landmarks are missing")
need("Array.from({length:5},(_,k)=><Word key={k}" in source and "blueTile=e(f,8,16)" in source, "V29 repeated MORRO / collage transition is missing")
need("glossy-play-ring-v29" in source, "V29 glossy app-tile material is missing")
need('width="34.5%" height="76%"' in source, "V29 full-countdown prism scale is missing")
need('isOne?<CountdownPrism width="42%" height="74%" scale={.98+.04*p}/>' in source, "countdown 1 Preview artwork is not source-scaled")
need("shellLeft=118*(1-zoomExit)" in source and "paneRight=frame<106?285*(1-zoomExit):frame<110?109*e(frame,106,110):109+16*e(frame,110,111)" in source, "source-frame keyframed Preview pane geometry is missing")
need('left:"6.1%",right:"6.25%",top:0,bottom:0' in source, "frame-891 rounded takeover bounds are missing")
need('stroke="#df884c"' in source and 'stroke="#5a6dff"' in source and 'background:"#f2f0e9"' in source, "countdown takeover ring/card colours are missing")

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
need(any(item.get("frame") == 933 and "glossy blue/black rounded app tile" in item.get("content", "") for item in audit), "frame 933 glossy app-tile observation is missing")
need(any(item.get("frame") == 1118 and "domain capsule" in item.get("content", "") for item in audit), "frame 1118 branded end card observation is missing")
need(any(item.get("frame") == 547 and "3.7%" in item.get("content", "") for item in audit), "frame 547 must record 3.7%")
need("const counts=[80,82,84,87,91,93,94,96]" in source, "Star History source value sequence is missing")
need("days=[88,96,104,111,119,126,132,138]" in source, "Star History day sequence is missing")
need("3.7%" in source and "4.7%" not in source, "eye readout must match 3.7%")
need("squiggle-preview-v18" in source, "black/white squiggle launch preview is missing")
need("f<15?-90+128*e(f,0,15):f<45?38+49*e(f,15,45):f<60?87+48*e(f,45,60):135+25*e(f,60,75)" in source and "perspective:1500" in source, "V53 cube yaw and perspective landmarks are missing")
need("if(f<12)return <AbsoluteFill" in source, "separate app-mark lead-in is missing")
need("GITHUB STARS" in source and "stars-grid-v31" in source, "yellow/mint 100K GitHub-stars cube face is missing")
need("cubeClock-v24" in source, "blue/gold clock face must be on the top surface")
need("f<15?18-14*e(f,0,15):f<45?4-26*e(f,15,45):f<60?-22+4*e(f,45,60):-18+10*e(f,60,75)" in source, "V53 cube pitch landmarks are missing")
need("const dynamicFront=frame<27?portrait:frame<55?blackSide:frame<72?archiveFace:blackMark" in source, "V53 source-indexed cube front artwork is missing")
need("const dynamicSide=frame<27?blackSide:frame<55?clock:frame<72?yellow:archive1923" in source, "V53 source-indexed cube side artwork is missing")
need("kind===3?(frame<55?clock:blackSide)" in source, "V32 clock must move from top to adjacent face after frame990")
need('top:"84%"' in source and 'height:"10%"' in source and "opacity:e(f,38,42)*(1-e(f,54,58))" in source, "V25 lower-edge EASE fold timing is missing")
need('rotateX(90deg) translateZ("+z+"px)' in source, "blue clock must occupy the top face")
need('rotateX(-90deg) translateZ("+z+"px)' in source, "lime EASE must occupy the underside")
need("MORRO / FORM STUDY" in source, "large purple MORRO transition is missing")
need("OpenDesign Motion" in source and "open-design.ai" in source, "full branded end card is missing")
need("resolve=e(f,0,2)" in source, "IN to LINEAR transition timing is missing")
need("r=860-100*e(f,0,1)" in source and "r={bloom} fill=\"#f8faf5\"" in source, "green ring transition must bloom into the source white inner disc")
need("durationInFrames={14}><LinearPoster" in source and "from={194} durationInFrames={6}><GreenCircleTransition" in source, "source-frame 510 typography/ring boundary is incorrect")
need("MORRO / 01" in source, "illustrated camera cube face artwork is missing")

need("Array.from({length:26*44}" in source and "row*43+((seed%11)-5)*2.2,r:9+(seed%6)*1.15" in source and "translate(960 540)" in source, "V53 dense 1965 dot field and centred D-shaped badge are incomplete")
need('const rings=[540,475,410,345,280,215,150,85,28]' in source and 'id={"ring-v53-"+i}' in source and 'sizes=[76,64,54,46,38,31,25,19,14]' in source, "V53 nine-band concentric tunnel is incomplete")
need("const sky=Array.from({length:1050}" in source and "const halo=Array.from({length:330}" in source and "clock-gold-v53" in source, "V53 painterly 1889 clock scene is incomplete")
need("const x=1195+Math.cos(angle)*230" in source and "Array.from({length:11},(_,i)" in source, "V51 provider orbit must retain the source-sized ellipse")
need('scaleX(1.9) scaleY(.6)' in source, "V52 EASE poster must preserve the source's wide, shallow word geometry")
need('top:"31%"' in source and 'Array.from({length:10},(_,i)' in source and "scale(1.02,1.08)" in source, "V53 metallic IN extrusion and position are missing")
need('const rings=[540,475,410,345,280,215,150,85,28]' in source and 'id={"ring-v53-"+i}' in source and 'sizes=[76,64,54,46,38,31,25,19,14]' in source, "V53 nine-band concentric tunnel is incomplete")
need("length:26*44" in source and "r:9+(seed%6)*1.15" in source, "V53 1965 dot grid must match the source's density and dot scale")
need('const rings=[540,475,410,345,280,215,150,85,28]' in source and 'id={"ring-v53-"+i}' in source and 'sizes=[76,64,54,46,38,31,25,19,14]' in source, "V53 nine-band concentric tunnel is incomplete")
need("const sky=Array.from({length:1050}" in source and "const halo=Array.from({length:330}" in source and "clock-gold-v53" in source, "V53 painted night clock with dense sky/halo brushwork is missing")
need("const archiveFace=" in source and "const archive1923=" in source and "frame<55?clock:frame<72?yellow:archive1923" in source, "V53 cube side faces must vary with the source-indexed frame sequence")
need("const treeMarks=Array.from({length:250}" in source and "townStrokes=Array.from({length:160}" in source, "V53 clock painting tree/village brush textures are missing")
print("PASS: 12 source-indexed sections / 28 montage cuts / 30 gallery panels / 1119 frames / launch preview / countdown / MORRO tile / end card")

need('fontSize:100,fontWeight:700,letterSpacing:"-.055em"' in source, "V38 opening headline scale is missing")
need('const firstPhaseCount=Math.round(Math.max(0,Math.min(1,(f-14)/16))*introLength)' in source and 'const finalPhaseCount=introLength+Math.round(Math.max(0,Math.min(1,(f-30)/30))*(text.length-introLength))' in source, "typed prompt must reach Introducing at frame30 and the full line at frame60")
need("left:1875-337*e(f,42,60)" in source and "top:955-315*e(f,42,60)" in source, "V45 cursor motion must land on the submit control")
need('height:278,background:"rgba(255,255,255,.97)",borderRadius:24' in source and 'bottom:87,left:-12' in source and "▱ Working directory⌄" in source, "V45 source-sized prompt field and toolbar are missing")
