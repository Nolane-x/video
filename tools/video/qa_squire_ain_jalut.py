#!/usr/bin/env python3
"""Strict technical QA and evidence report for the Squire Ain Jalut candidate."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, capture_output=True, text=True)


def safe_title(value: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", value).strip() or "video"


def measure_loudness(path: Path) -> dict:
    p = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ], check=True)
    matches = re.findall(r"\{\s*\"input_i\"[\s\S]*?\}", p.stderr)
    if not matches:
        raise RuntimeError("FFmpeg loudnorm did not return input measurements")
    return json.loads(matches[-1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice-assets", required=True)
    args = ap.parse_args()
    project = Path(args.project).resolve()
    assets = Path(args.voice_assets).resolve()
    config = json.loads((project / "config.json").read_text(encoding="utf-8"))
    story = json.loads((project / "story" / "shots.json").read_text(encoding="utf-8"))
    shots = story.get("shots") or []
    title = config["title"]
    final = project / "out" / (safe_title(title) + ".mp4")
    preview = project / "build" / "preview.mp4"
    thumbnail = project / "out" / "thumbnail.png"
    contact_sheets = sorted((project / "build" / "sheets").glob("sheet_*.jpg"))
    voice_manifest = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    selection = json.loads((assets / "voice-selection.json").read_text(encoding="utf-8"))
    voice = assets / "narration.wav"
    timeline_voice = project / "timeline" / "voice.wav"
    captions_srt = assets / "captions.srt"
    captions_vtt = assets / "captions.vtt"
    foley_manifest_path = project / "story" / "FOLEY-SOURCE-MANIFEST.json"
    foley_manifest = json.loads(foley_manifest_path.read_text(encoding="utf-8")) if foley_manifest_path.is_file() else {}

    assert final.is_file() and final.stat().st_size > 100_000, f"Final MP4 missing or too small: {final}"
    assert preview.is_file() and preview.stat().st_size > 50_000, "45-second preview missing"
    assert thumbnail.is_file() and thumbnail.stat().st_size > 10_000, "Thumbnail missing"
    assert contact_sheets, "No Squire contact sheets were rendered"
    assert voice.is_file() and timeline_voice.is_file(), "Narration WAV or Squire timeline copy missing"
    assert captions_srt.is_file() and captions_srt.stat().st_size > 100, "SRT missing"
    assert captions_vtt.is_file() and captions_vtt.stat().st_size > 100, "VTT missing"
    assert foley_manifest.get("status") == "TECHNICAL_IMPORT_VERIFIED_HUMAN_LISTENING_PENDING", "Recorded Foley manifest missing or not verified"
    foley_assets = foley_manifest.get("assets") or []
    assert len(foley_assets) >= 8, f"Expected recorded CC0 Foley set, got {len(foley_assets)} assets"
    assert all(row.get("license") == "CC0-1.0" for row in foley_assets), "A Foley item lacks item-level CC0 rights metadata"
    assert all(row.get("human_auditioned") is False for row in foley_assets), "Do not silently mark imported recordings as human-auditioned"

    audio = voice_manifest["audio"]
    assert voice_manifest["voice_id"] == selection["voice_id"], "Rendered voice does not match selected voice"
    assert audio["checks"] == "passed", "VoiceStudio signal checks did not pass"
    assert audio["watermark"]["status"] == "verified", "VoiceStudio watermark not verified"
    assert audio["sample_rate"] == 48000 and audio["channels"] == 1 and audio["subtype"] == "PCM_24", "VoiceStudio master format mismatch"
    assert sha(voice) == audio["sha256"], "VoiceStudio WAV SHA-256 mismatch"
    assert sha(timeline_voice) == audio["sha256"], "Squire timeline changed the source narration bytes"

    duration = float(story["duration"])
    assert duration > 600, f"Long-form target must exceed ten minutes: {duration:.1f}s"
    assert 50 <= len(shots) <= 500, f"Unexpected shot count: {len(shots)}"
    templates = sorted({str(s.get("tpl")) for s in shots})
    assert len(templates) >= 7, f"Not enough Squire visual variation: {templates}"
    for shot in shots:
        assert shot.get("tpl") in {"scene", "close", "army", "top", "plan", "map", "board", "item", "split", "title", "black"}, f"Unknown template {shot.get('tpl')}"
        assert float(shot["end"]) > float(shot["start"]), f"Invalid shot {shot.get('id')}"
        assert float(shot["end"]) - float(shot["start"]) <= 8.2, f"Static/overlong shot {shot.get('id')}"
        assert shot.get("args") is not None, f"Shot has no authored args: {shot.get('id')}"

    words = sum(1 for row in json.loads((project / "timeline" / "words.json").read_text(encoding="utf-8")))
    alignment = json.loads((project / "story" / "alignment-report.json").read_text(encoding="utf-8"))
    match_ratio = float(alignment["alignment"]["matched_ratio"])
    assert words >= 1400, f"Narration timeline unexpectedly short: {words} words"
    assert match_ratio >= 0.65, f"ASR word-timeline match ratio too low: {match_ratio:.1%}"

    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(final)
    ]).stdout)
    vstreams = [s for s in probe["streams"] if s.get("codec_type") == "video"]
    astreams = [s for s in probe["streams"] if s.get("codec_type") == "audio"]
    assert vstreams and astreams, "Final MP4 must contain both video and audio streams"
    v, a = vstreams[0], astreams[0]
    assert (int(v["width"]), int(v["height"])) == (1920, 1080), f"Unexpected resolution: {v.get('width')}x{v.get('height')}"
    assert v.get("codec_name") == "h264", f"Unexpected video codec: {v.get('codec_name')}"
    assert v.get("r_frame_rate") == "24/1", f"Unexpected frame rate: {v.get('r_frame_rate')}"
    assert a.get("codec_name") == "aac" and int(a.get("sample_rate", 0)) == 48000 and int(a.get("channels", 0)) == 2, "Final audio stream format mismatch"
    video_duration = float(probe["format"]["duration"])
    assert abs(video_duration - duration) <= 1.3, f"Final video duration differs from storyboard: {video_duration:.2f}s vs {duration:.2f}s"
    frame_count = int(v.get("nb_frames") or 0)
    assert frame_count == 0 or frame_count >= int(duration * 24 * 0.99), f"Final frame count too low: {frame_count}"

    loudness = measure_loudness(final)
    integrated = float(loudness["input_i"])
    true_peak = float(loudness["input_tp"])
    assert -15.7 <= integrated <= -12.3, f"Integrated loudness outside target: {integrated} LUFS"
    assert true_peak <= -1.0, f"True peak too high: {true_peak} dBTP"

    decode = run(["ffmpeg", "-hide_banner", "-v", "error", "-i", str(final), "-f", "null", "-"], check=False)
    assert decode.returncode == 0 and not decode.stderr.strip(), f"Decode errors: {decode.stderr[-1000:]}"

    report = {
        "status": "technical_pass",
        "visual_approval": "pending human full-motion review",
        "title": title,
        "project": "ain-jalut-1260",
        "engine": "Squire 2D/vector",
        "duration_seconds": round(video_duration, 3),
        "resolution": "1920x1080",
        "fps": "24/1",
        "video_codec": v["codec_name"],
        "audio_codec": a["codec_name"],
        "audio_sample_rate": int(a["sample_rate"]),
        "audio_channels": int(a["channels"]),
        "recorded_foley": {"asset_count": len(foley_assets), "human_auditioned": 0, "approved_for_final_publication": 0, "manifest_status": foley_manifest["status"]},
        "integrated_loudness_lufs": integrated,
        "true_peak_dbtp": true_peak,
        "shot_count": len(shots),
        "visual_templates": templates,
        "voice_id": voice_manifest["voice_id"],
        "voice_engine": voice_manifest["engine"],
        "voice_audioseal": audio["watermark"],
        "voice_sha256": audio["sha256"],
        "asr_word_alignment_ratio": match_ratio,
        "word_count": words,
        "contact_sheets": [p.name for p in contact_sheets],
        "thumbnail_bytes": thumbnail.stat().st_size,
        "preview_bytes": preview.stat().st_size,
        "final_mp4_bytes": final.stat().st_size,
        "final_mp4_sha256": sha(final),
        "mix_wav_sha256": sha(project / "build" / "mix.wav"),
        "captions": {"srt_bytes": captions_srt.stat().st_size, "vtt_bytes": captions_vtt.stat().st_size},
        "limitations": [
            "Ancient force and casualty totals are estimates attributed to Polybius.",
            "Tactical movement is an explanatory reconstruction, not an exact second-by-second record.",
            "Squire ancient character presets are stylized generic representations, not authenticated uniforms.",
            "Recorded CC0 Foley passed download, decode and checksum checks, but the exact cues still require human listening approval.",
            "Automated checks do not replace human review of every scene and the full soundtrack.",
        ],
    }
    (project / "story" / "QA-REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Ain Jalut — technical QA report",
        "",
        f"- Status: {report['status']}",
        f"- Human audiovisual approval: {report['visual_approval']}",
        f"- Duration: {video_duration:.2f}s",
        "- Picture: 1920×1080, 24 fps, H.264",
        f"- Sound: AAC stereo / 48 kHz, {integrated:.2f} LUFS, {true_peak:.2f} dBTP",
        f"- Shots: {len(shots)} across {len(templates)} Squire templates",
        f"- Narrator: {voice_manifest['voice_id']} ({voice_manifest['engine']})",
        f"- ASR word timestamp match: {match_ratio:.1%}",
        f"- Final MP4 SHA-256: {report['final_mp4_sha256']}",
        "",
        "## Open review gate",
        "A human must watch the complete film with audio, inspect the contact sheets and selected action/recovery frames, and record defects/timecodes before public release.",
    ]
    (project / "story" / "QA-REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"TECHNICAL PASS: {final} | {video_duration:.1f}s | {len(shots)} shots | {integrated:.2f} LUFS | SHA256 {report['final_mp4_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
