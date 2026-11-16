#!/usr/bin/env python3
"""Prepare the Mua Thoi Gian Remotion project from the 90 stills and aligned VoiceStudio audio."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps, ImageEnhance

FPS = 30
WIDTH = 1920
HEIGHT = 1080


def normalize_token(value: str) -> str:
    return re.sub(r"[^\w']+", "", value.casefold(), flags=re.UNICODE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def extract_images(archive: Path, destination: Path) -> dict[str, Path]:
    temp = destination.parent / "_image_extract"
    shutil.rmtree(temp, ignore_errors=True)
    temp.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"Corrupt image archive member: {bad}")
        zf.extractall(temp)

    by_id: dict[str, Path] = {}
    for path in temp.rglob("*"):
        if not path.is_file():
            continue
        match = re.search(r"A(\d{3})", path.name, flags=re.IGNORECASE)
        if not match:
            continue
        asset_id = f"A{int(match.group(1)):03d}"
        if asset_id in by_id:
            raise RuntimeError(f"Duplicate source image for {asset_id}: {path} / {by_id[asset_id]}")
        by_id[asset_id] = path

    expected = {f"A{i:03d}" for i in range(1, 91)}
    missing = sorted(expected - set(by_id))
    unexpected = sorted(set(by_id) - expected)
    if missing or unexpected or len(by_id) != 90:
        raise RuntimeError(f"Image set mismatch: count={len(by_id)}, missing={missing}, unexpected={unexpected}")

    destination.mkdir(parents=True, exist_ok=True)
    output: dict[str, Path] = {}
    for asset_id in sorted(expected):
        source = by_id[asset_id]
        with Image.open(source) as im:
            im = im.convert("RGB")
            # Source images are 1376x768. Center-fit to exact 16:9 while preserving the original still.
            im = ImageOps.fit(im, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            im = ImageEnhance.Sharpness(im).enhance(1.06)
            target = destination / f"{asset_id}.jpg"
            im.save(target, "JPEG", quality=95, subsampling=0, optimize=True, progressive=True)
        output[asset_id] = target
    return output


def build_aligned_shots(base: dict, lines: list[dict], words: list[dict], duration_seconds: float) -> dict:
    line_by_block = {str(row.get("source_segment_id") or row["id"]): row for row in lines}
    words_by_line: dict[str, list[dict]] = defaultdict(list)
    for word in words:
        words_by_line[str(word["line"])].append(word)
    for rows in words_by_line.values():
        rows.sort(key=lambda row: (float(row["t"]), float(row["e"])))

    source_shots = list(base["shots"])
    by_voice: dict[str, list[dict]] = defaultdict(list)
    for index, shot in enumerate(source_shots):
        shot["_source_index"] = index
        by_voice[str(shot["voiceId"])].append(shot)

    aligned: list[dict] = []
    cursor_frame = 0
    alignment_stats = {"matched": 0, "interpolated": 0, "caption_word_mismatches": []}

    for voice_index in range(1, 91):
        voice_id = f"V{voice_index:03d}"
        line = line_by_block.get(voice_id)
        group = by_voice.get(voice_id, [])
        if not line or not group:
            raise RuntimeError(f"Missing line or shot group for {voice_id}")

        line_words = words_by_line.get(str(line["id"]), [])
        if not line_words:
            raise RuntimeError(f"No aligned words found for {voice_id} / {line['id']}")
        group.sort(key=lambda row: row["_source_index"])
        caption_tokens = []
        weights = []
        for shot in group:
            tokens = [token for token in str(shot.get("subtitle", "")).split() if normalize_token(token)]
            caption_tokens.append(tokens)
            weights.append(max(1, len(tokens)))

        total_weight = sum(weights)
        word_slices = []
        used = 0
        for index, weight in enumerate(weights):
            if index == len(weights) - 1:
                end = len(line_words)
            else:
                end = round(len(line_words) * (sum(weights[: index + 1]) / total_weight))
                end = max(used + 1, min(end, len(line_words) - (len(weights) - index - 1)))
            word_slices.append(line_words[used:end])
            used = end

        if used != len(line_words) or any(not chunk for chunk in word_slices):
            # Robust fallback for ASR tokenization edge cases: distribute all available words evenly.
            word_slices = []
            for index in range(len(group)):
                start = round(len(line_words) * index / len(group))
                end = round(len(line_words) * (index + 1) / len(group))
                word_slices.append(line_words[start:end])

        line_start = float(line["start"])
        line_end = float(line["end"])
        start_frame = max(cursor_frame, round(line_start * FPS))
        if start_frame > cursor_frame and aligned:
            # TTS inserts measured silences between voice blocks; hold the last shot over each pause.
            aligned[-1]["duration"] += start_frame - cursor_frame
            cursor_frame = start_frame
        end_frame = max(start_frame + len(group), round(line_end * FPS))
        boundaries = [start_frame]

        for index in range(len(group) - 1):
            current = word_slices[index]
            following = word_slices[index + 1]
            if current and following:
                boundary_seconds = (float(current[-1]["e"]) + float(following[0]["t"])) / 2
                proposed = round(boundary_seconds * FPS)
            else:
                proposed = round(start_frame + (end_frame - start_frame) * (index + 1) / len(group))
            min_frame = boundaries[-1] + 1
            max_frame = end_frame - (len(group) - index - 1)
            proposed = max(min_frame, min(proposed, max_frame))
            boundaries.append(proposed)
        boundaries.append(end_frame)

        for shot_index, shot in enumerate(group):
            item = dict(shot)
            item.pop("_source_index", None)
            item["from"] = boundaries[shot_index]
            item["duration"] = boundaries[shot_index + 1] - boundaries[shot_index]
            chunk = word_slices[shot_index]
            tokens = caption_tokens[shot_index]
            word_rows = []
            for token_index, token in enumerate(tokens):
                source_word = chunk[token_index] if token_index < len(chunk) else None
                if source_word is None:
                    word_rows.append({
                        "text": token,
                        "start": float(line_start),
                        "end": float(line_end),
                        "alignment": "fallback-line-window",
                    })
                    continue
                method = source_word.get("alignment", "unknown")
                if method == "asr-word-timestamp":
                    alignment_stats["matched"] += 1
                else:
                    alignment_stats["interpolated"] += 1
                word_rows.append({
                    "text": token,
                    "start": float(source_word["t"]),
                    "end": float(source_word["e"]),
                    "alignment": method,
                })
            if len(tokens) != len(chunk):
                alignment_stats["caption_word_mismatches"].append({
                    "shot_id": item["id"], "caption_tokens": len(tokens), "aligned_words": len(chunk)
                })
            item["captionWords"] = word_rows
            item["lineId"] = line["id"]
            aligned.append(item)
        cursor_frame = end_frame

    duration_frames = max(cursor_frame, round(duration_seconds * FPS))
    if duration_frames != round(duration_seconds * FPS):
        raise RuntimeError(
            f"Shot timeline ends at {cursor_frame} frames but audio duration implies {round(duration_seconds * FPS)}"
        )

    aligned.sort(key=lambda row: row["from"])
    previous_end = 0
    for shot in aligned:
        if shot["from"] != previous_end:
            raise RuntimeError(f"Timeline gap/overlap before {shot['id']}: {previous_end} -> {shot['from']}")
        if shot["duration"] < 1:
            raise RuntimeError(f"Invalid short shot: {shot['id']}")
        previous_end = shot["from"] + shot["duration"]
    if previous_end != duration_frames:
        raise RuntimeError(f"Timeline terminal mismatch: {previous_end} != {duration_frames}")

    result = dict(base)
    result["durationInFrames"] = duration_frames
    result["durationSeconds"] = round(duration_seconds, 4)
    result["audio"] = {
        "voiceEnabled": True,
        "musicEnabled": True,
        "sfxEnabled": True,
        "voiceAsset": "audio/narration.wav",
        "musicAsset": "audio/music-bed.wav",
        "voiceVolume": 1.0,
        "musicVolume": 0.36,
        "sfxVolume": 0.22,
    }
    result["shots"] = aligned
    result["alignment"] = alignment_stats
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-zip", type=Path, required=True)
    parser.add_argument("--voice-dir", type=Path, required=True)
    parser.add_argument("--project-dir", type=Path, required=True)
    args = parser.parse_args()

    project = args.project_dir.resolve()
    images_out = project / "public" / "images"
    source_images = extract_images(args.image_zip.resolve(), images_out)

    manifest = json.loads((args.voice_dir / "manifest.json").read_text(encoding="utf-8"))
    lines_path = args.voice_dir / "h2-timeline" / "timeline" / "lines.json"
    words_path = args.voice_dir / "h2-timeline" / "timeline" / "words.json"
    if not lines_path.is_file() or not words_path.is_file():
        raise FileNotFoundError("VoiceStudio word-alignment outputs are missing")
    lines = json.loads(lines_path.read_text(encoding="utf-8"))
    words = json.loads(words_path.read_text(encoding="utf-8"))
    duration = float(manifest["audio"]["duration_seconds"])
    if duration < 600 or duration > 900:
        raise RuntimeError(f"Unexpected narration duration for the 11-minute film: {duration:.2f}s")

    base_path = project / "src" / "storyboard.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    result = build_aligned_shots(base, lines, words, duration)
    (project / "src" / "shots.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    audio_dir = project / "public" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.voice_dir / "narration.wav", audio_dir / "narration.wav")
    shutil.copy2(args.voice_dir / "captions.srt", audio_dir / "captions.srt")
    shutil.copy2(args.voice_dir / "captions.vtt", audio_dir / "captions.vtt")
    shutil.copy2(args.voice_dir / "manifest.json", audio_dir / "voice-manifest.json")
    shutil.copy2(args.voice_dir / "h2-timeline" / "alignment-report.json", audio_dir / "alignment-report.json")

    image_hashes = {asset_id: sha256(path) for asset_id, path in sorted(source_images.items())}
    report = {
        "project": "neu-ban-co-the-mua-thoi-gian-bang-tien",
        "images": {"count": len(source_images), "source_archive_sha256": sha256(args.image_zip), "processed": image_hashes},
        "voice": {"duration_seconds": duration, "sha256": manifest["audio"]["sha256"], "voice_id": manifest.get("voice_id"), "engine": manifest.get("engine")},
        "timeline": {"shots": len(result["shots"]), "fps": FPS, "frames": result["durationInFrames"], "duration_seconds": result["durationSeconds"]},
        "alignment": result["alignment"],
    }
    (project / "public" / "production-manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "images": len(source_images),
        "shots": len(result["shots"]),
        "duration_seconds": result["durationSeconds"],
        "frames": result["durationInFrames"],
        "voice": manifest.get("voice_id"),
        "alignment": result["alignment"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
