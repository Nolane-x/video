#!/usr/bin/env python3
"""Render one real moving 240fps sample from every bespoke Constantinople scene."""
from __future__ import annotations
import argparse, json, shutil, subprocess
from pathlib import Path

CUSTOM = [
    "final_night", "city_panorama", "command_camp", "gun_crew",
    "wall_battery", "repair_wall", "golden_horn", "relief_galleys",
    "ship_portage", "tunnel_cutaway", "church_refuge", "city_interior",
    "last_assault", "aftermath_city", "actor_closeup", "city_detail",
]

def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return p.stdout

def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",type=Path,required=True)
    ap.add_argument("--kit",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--workers",type=int,default=2)
    a=ap.parse_args()
    project=a.project.resolve()
    kit=a.kit.resolve()
    output=a.output.resolve()
    story=json.loads((project/"story"/"shots.json").read_text(encoding="utf-8"))
    shots=story.get("shots") or []
    if len(shots)<350: raise SystemExit(f"Expected a longform shotbook, received {len(shots)} shots.")
    selected=[]
    for template in CUSTOM:
        matches=[s for s in shots if s.get("tpl")==template]
        if not matches: raise SystemExit(f"No authored shot for required template: {template}")
        # Prefer a longer example so anticipation, action and follow-through have room to read.
        s=max(matches,key=lambda x:float(x["end"])-float(x["start"]))
        start=float(s["start"]); end=float(s["end"])
        if end-start<.55: raise SystemExit(f"Shot too short to prove motion: {s.get('id')} ({template})")
        selected.append({"template":template,"shot_id":s["id"],"line":s.get("line",""),
                         "start":round(start,4),"end":round(end,4),"duration":round(end-start,4),
                         "args":s.get("args",{})})
    proof_dir=project/"build"/"redesign-proof-segments"
    proof_dir.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,item in enumerate(selected,1):
        segment=proof_dir/f"{i:02d}-{item['template']}.mp4"
        print(f"[{i}/{len(selected)}] {item['template']} — {item['shot_id']} {item['start']:.2f}s–{item['end']:.2f}s",flush=True)
        run(["node",str(kit/"render.mjs"),"--project",str(project),"--style","dusk",
             "--from",str(item["start"]),"--to",str(item["end"]),
             "--workers",str(a.workers),"--crf","18","--maxrate","48M","--bufsize","96M","--preset","veryfast"])
        rendered=project/"build"/"preview.mp4"
        if not rendered.is_file() or rendered.stat().st_size<20_000:
            raise SystemExit(f"Renderer failed to produce a usable preview for {item['template']}")
        shutil.copy2(rendered,segment)
        meta=probe(segment)
        streams=meta.get("streams",[])
        video=next((x for x in streams if x.get("codec_type")=="video"),None)
        audio=next((x for x in streams if x.get("codec_type")=="audio"),None)
        if not video or not audio: raise SystemExit(f"Missing audio/video in {segment.name}")
        if video.get("r_frame_rate")!="240/1": raise SystemExit(f"{segment.name} is not native 240fps: {video.get('r_frame_rate')}")
        item["segment"]=segment.name
        item["width"]=int(video["width"]); item["height"]=int(video["height"])
        item["r_frame_rate"]=video["r_frame_rate"]
        item["avg_frame_rate"]=video.get("avg_frame_rate")
        item["frame_count"]=int(video.get("nb_frames") or 0)
        item["encoded_duration"]=float(meta["format"]["duration"])
        item["audio_codec"]=audio["codec_name"]
        clips.append(segment)
    concat=proof_dir/"concat.txt"
    concat.write_text("".join(f"file '{p.as_posix().replace(chr(39),chr(39)+chr(92)+chr(39)+chr(39))}'\n" for p in clips),encoding="utf-8")
    output.parent.mkdir(parents=True,exist_ok=True)
    run(["ffmpeg","-hide_banner","-v","error","-y","-f","concat","-safe","0","-i",str(concat),
         "-vf","fps=240","-r","240","-fps_mode","cfr","-c:v","libx264","-preset","veryfast","-crf","18",
         "-pix_fmt","yuv420p","-video_track_timescale","240000","-c:a","aac","-b:a","192k","-ar","48000",
         "-ac","2","-movflags","+faststart",str(output)])
    final=probe(output)
    video=next(x for x in final["streams"] if x.get("codec_type")=="video")
    audio=next(x for x in final["streams"] if x.get("codec_type")=="audio")
    if video.get("r_frame_rate")!="240/1" or video.get("avg_frame_rate")!="240/1":
        raise SystemExit(f"Montage is not constant 240fps: r={video.get('r_frame_rate')} avg={video.get('avg_frame_rate')}")
    decode=subprocess.run(["ffmpeg","-hide_banner","-v","error","-i",str(output),"-f","null","-"],capture_output=True,text=True)
    if decode.returncode or decode.stderr.strip(): raise SystemExit(f"Proof decode error: {decode.stderr[-1200:]}")
    report={
        "status":"RENDERED_TECHNICAL_PROOF_NOT_ARTISTIC_APPROVAL",
        "project":"53 Days to the End of an Empire",
        "render_engine":"H2 Squire",
        "style":"dusk",
        "captions":True,
        "resolution":[int(video["width"]),int(video["height"])],
        "fps":video["r_frame_rate"],
        "avg_frame_rate":video.get("avg_frame_rate"),
        "frame_count":int(video.get("nb_frames") or 0),
        "duration_seconds":float(final["format"]["duration"]),
        "audio":{"codec":audio["codec_name"],"sample_rate":audio.get("sample_rate"),"channels":audio.get("channels")},
        "templates":selected,
        "limitations":["This is a montage of one selected moving shot from each custom template, not the complete film.","No human full-length artistic approval is claimed.","CC0 music and Foley remain pending human audition."],
    }
    report_path=output.with_suffix(".json")
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"PROOF READY: {output} | {len(selected)} templates | {report['duration_seconds']:.2f}s | {report['frame_count']} frames @ 240fps",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
