#!/usr/bin/env python3
"""Strict 240fps technical QA for the Constantinople 1453 long-form master."""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess
from pathlib import Path
FPS=240
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def run(args,check=True):return subprocess.run(args,check=check,capture_output=True,text=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--project",required=True);ap.add_argument("--voice-assets",required=True);a=ap.parse_args()
    p=Path(a.project).resolve();assets=Path(a.voice_assets).resolve()
    cfg=json.loads((p/"config.json").read_text(encoding="utf-8"));story=json.loads((p/"story"/"shots.json").read_text(encoding="utf-8"))
    title=cfg["title"];safe=re.sub(r'[\\/:*?"<>|]',"",title).strip()
    final=p/"out"/(safe+".mp4");preview=p/"build"/"preview.mp4";thumb=p/"out"/"thumbnail.png"
    assert cfg.get("fps")==FPS,f"Project config must be {FPS} fps"
    assert final.is_file() and final.stat().st_size>300_000,f"Missing/undersized final: {final}"
    assert preview.is_file() and preview.stat().st_size>50_000,"Missing 240fps moving proof"
    assert thumb.is_file() and thumb.stat().st_size>10_000,"Missing thumbnail"
    assert any((p/"build"/"sheets").glob("sheet_*.jpg")),"Contact sheets missing"
    shots=story.get("shots") or [];duration=float(story.get("duration",0))
    assert duration>650,f"Film too short: {duration:.1f}s"
    assert 350<=len(shots)<=1100,f"Unexpected shot count: {len(shots)}"
    custom={"city_panorama","command_camp","city_interior","wall_battery","relief_galleys","ship_portage","last_assault","aftermath_city"}
    custom_count=sum(1 for s in shots if s.get("tpl") in custom)
    assert custom_count>=220,f"Not enough bespoke siege animation shots: {custom_count}"
    for s in shots:
        assert s.get("args") is not None,f"No authored args: {s.get('id')}"
        assert float(s["end"])>float(s["start"]),f"Bad shot timing: {s.get('id')}"
        assert float(s["end"])-float(s["start"])<=8.2,f"Overlong static shot: {s.get('id')}"
    voice=json.loads((assets/"manifest.json").read_text(encoding="utf-8"));selection=json.loads((assets/"voice-selection.json").read_text(encoding="utf-8"))
    wav=assets/"narration.wav";timeline=p/"timeline"/"voice.wav"
    assert voice["voice_id"]==selection["voice_id"]
    aud=voice["audio"]
    assert aud["checks"]=="passed" and aud["watermark"]["status"]=="verified"
    assert aud["sample_rate"]==48000 and aud["channels"]==1 and aud["subtype"]=="PCM_24"
    assert sha(wav)==aud["sha256"] and sha(timeline)==aud["sha256"]
    assert (assets/"captions.srt").stat().st_size>100 and (assets/"captions.vtt").stat().st_size>100
    words=json.loads((p/"timeline"/"words.json").read_text(encoding="utf-8"))
    alignment=json.loads((p/"story"/"alignment-report.json").read_text(encoding="utf-8"))
    assert len(words)>=1800,f"Narration word timeline short: {len(words)}"
    assert float(alignment["alignment"]["matched_ratio"])>=.65
    probe=json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(final)]).stdout)
    vs=[x for x in probe["streams"] if x.get("codec_type")=="video"];aas=[x for x in probe["streams"] if x.get("codec_type")=="audio"]
    assert vs and aas,"Both audio and video streams are required"
    v,audstream=vs[0],aas[0]
    assert (int(v["width"]),int(v["height"]))==(1920,1080)
    assert v.get("r_frame_rate")==f"{FPS}/1",f"Not native 240fps: {v.get('r_frame_rate')}"
    assert v.get("avg_frame_rate")==f"{FPS}/1",f"Average frame rate mismatch: {v.get('avg_frame_rate')}"
    frames=int(v.get("nb_frames") or 0)
    expected=int(duration*FPS*.995)
    assert frames>=expected,f"Only {frames} frames; expected at least {expected}"
    assert audstream.get("codec_name")=="aac" and int(audstream.get("sample_rate",0))==48000 and int(audstream.get("channels",0))==2
    assert abs(float(probe["format"]["duration"])-duration)<=1.5
    decode=run(["ffmpeg","-hide_banner","-v","error","-i",str(final),"-f","null","-"],check=False)
    assert decode.returncode==0 and not decode.stderr.strip(),f"Decode failure: {decode.stderr[-1000:]}"
    # Detect accidental 24fps frame duplication: sampled adjacent frames must not all collapse to the same image.
    sample=run(["ffmpeg","-hide_banner","-v","error","-i",str(final),"-vf","select='not(mod(n,24))',scale=96:54,format=gray","-frames:v","100","-f","framemd5","-"],check=False)
    assert sample.returncode==0,f"Frame-difference probe failed: {sample.stderr[-500:]}"
    hashes=[x.split(",")[-1].strip() for x in sample.stdout.splitlines() if x and not x.startswith("#")]
    unique=len(set(hashes))
    assert unique>=max(20,int(len(hashes)*.70)),f"Too many identical sampled frames: {unique}/{len(hashes)}"
    loud=run(["ffmpeg","-hide_banner","-nostats","-i",str(final),"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"])
    hits=re.findall(r'\{\s*"input_i"[\s\S]*?\}',loud.stderr)
    assert hits,"Loudness measurement missing"
    measurement=json.loads(hits[-1]);integrated=float(measurement["input_i"]);peak=float(measurement["input_tp"])
    assert -15.7<=integrated<=-12.3,f"LUFS outside target: {integrated}"
    assert peak<=-1.0,f"True peak too high: {peak}"
    report={"status":"technical_pass","artistic_signoff":"pending complete human watch/listen","title":title,"duration_seconds":round(float(probe["format"]["duration"]),3),"resolution":"1920x1080","fps":FPS,"frames":frames,"expected_frames":int(duration*FPS),"video_codec":v.get("codec_name"),"audio_codec":audstream.get("codec_name"),"shot_count":len(shots),"bespoke_shots":custom_count,"templates":sorted({s.get("tpl") for s in shots}),"sampled_unique_frame_hashes":unique,"sampled_frame_hash_count":len(hashes),"lufs":integrated,"true_peak_dbtp":peak,"narrator":voice["voice_id"],"voice_sha256":aud["sha256"],"final_sha256":sha(final),"final_bytes":final.stat().st_size,"limitations":["240 fps is verified from native output time samples; monitor refresh may display fewer frames.","Automated QA is technical, not artistic sign-off.","A human must watch the full film at normal speed and audition every final audio stem before public release."]}
    (p/"story"/"QA-REPORT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Constantinople 1453 — 240 fps technical report","",f"- Status: {report['status']}","- Artistic sign-off: pending full human review",f"- Duration: {report['duration_seconds']:.2f}s","- Picture: 1920×1080 / native 240 fps / {frames} frames",f"- Shots: {len(shots)} total; {custom_count} bespoke scene shots",f"- Unique sampled frames: {unique}/{len(hashes)}",f"- Sound: AAC stereo / 48 kHz / {integrated:.2f} LUFS / {peak:.2f} dBTP",f"- SHA-256: {report['final_sha256']}","","240 fps is verified in the encoded stream. A 60 Hz display cannot show 240 distinct refreshes per second; the master preserves the additional temporal samples for supported playback and slow-motion editorial use."]
    (p/"story"/"QA-REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"TECHNICAL PASS: {final} | {duration:.1f}s | 1920x1080@240 | {frames} frames | {len(shots)} shots | {custom_count} custom")
    return 0
if __name__=="__main__":raise SystemExit(main())
