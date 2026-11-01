#!/usr/bin/env python3
"""Build an H2-compatible voice timeline from a VoiceStudio Actions artifact.

The original 48 kHz PCM-24 WAV is copied byte-for-byte. faster-whisper adds
ASR-assisted word timestamps; unmatched words receive clearly labelled,
interpolated estimates so consumers can decide whether to use them.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import unicodedata
import zipfile
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_token(value: str) -> str:
    value = unicodedata.normalize("NFC", value).casefold()
    return re.sub(r"[^\w']+", "", value, flags=re.UNICODE)


def tokens(text: str) -> list[str]:
    return [match.group(0) for match in re.finditer(r"\S+", text, flags=re.UNICODE) if normalize_token(match.group(0))]


def display_token(value: str) -> str:
    return value.strip(" \t\r\n.,!?;:…\"'“”‘’()[]{}<>").strip()


def format_words(
    expected: list[tuple[str, int]],
    asr_words: list[dict],
    lines: list[dict],
) -> tuple[list[dict], dict]:
    expected_norm = [normalize_token(token) for token, _ in expected]
    asr_norm = [normalize_token(str(item.get("word", ""))) for item in asr_words]
    matcher = difflib.SequenceMatcher(None, expected_norm, asr_norm, autojunk=False)
    assigned: dict[int, tuple[float, float, str]] = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            expected_index = block.a + offset
            asr_index = block.b + offset
            token, line_index = expected[expected_index]
            word = asr_words[asr_index]
            start = max(float(lines[line_index]["start"]), float(word["start"]))
            end = min(float(lines[line_index]["end"]), float(word["end"]))
            if end > start:
                assigned[expected_index] = (start, end, "asr-word-timestamp")

    by_line: dict[int, list[int]] = {}
    for index, (_, line_index) in enumerate(expected):
        by_line.setdefault(line_index, []).append(index)

    for line_index, indices in by_line.items():
        anchors = [index for index in indices if index in assigned]
        cursor = 0
        while cursor < len(indices):
            if indices[cursor] in assigned:
                cursor += 1
                continue
            run_start = cursor
            while cursor < len(indices) and indices[cursor] not in assigned:
                cursor += 1
            run = indices[run_start:cursor]
            prev_index = indices[run_start - 1] if run_start > 0 else None
            next_index = indices[cursor] if cursor < len(indices) else None
            left_time = assigned[prev_index][1] if prev_index is not None and prev_index in assigned else float(lines[line_index]["start"])
            right_time = assigned[next_index][0] if next_index is not None and next_index in assigned else float(lines[line_index]["end"])
            if right_time < left_time:
                right_time = left_time
            weights = [max(1, len(expected[index][0].strip())) for index in run]
            total = sum(weights)
            elapsed = 0
            span = right_time - left_time
            for index, weight in zip(run, weights):
                start = left_time + span * elapsed / total
                elapsed += weight
                end = left_time + span * elapsed / total
                if end <= start:
                    end = min(float(lines[line_index]["end"]), start + 0.025)
                assigned[index] = (start, end, "interpolated")

    output: list[dict] = []
    matched = 0
    estimated = 0
    for index, (token, line_index) in enumerate(expected):
        start, end, method = assigned[index]
        matched += method == "asr-word-timestamp"
        estimated += method == "interpolated"
        output.append({
            "w": display_token(token),
            "t": round(start, 3),
            "e": round(max(start, end), 3),
            "alignment": method,
            "line": lines[line_index]["id"],
        })
    denominator = max(1, len(expected))
    return output, {
        "expected_word_count": len(expected),
        "asr_word_count": len(asr_words),
        "matched_word_count": matched,
        "interpolated_word_count": estimated,
        "matched_ratio": round(matched / denominator, 4),
        "method": "faster-whisper ASR word timestamps + interpolation for unmatched words",
    }


def build_timeline(artifact: Path, model_name: str) -> Path:
    from faster_whisper import WhisperModel

    manifest_path = artifact / "manifest.json"
    wav_path = artifact / "narration.wav"
    if not manifest_path.is_file() or not wav_path.is_file():
        raise FileNotFoundError("Expected narration.wav and manifest.json in the VoiceStudio artifact")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    language = manifest.get("language")
    if language not in {"en", "vi"}:
        raise ValueError(f"Unsupported voice-over language: {language!r}")
    audio = manifest["audio"]
    if audio.get("sample_rate") != 48000 or audio.get("subtype") != "PCM_24" or audio.get("channels") != 1:
        raise ValueError("VoiceStudio master must be mono 48 kHz PCM-24")
    if audio.get("watermark", {}).get("status") != "verified":
        raise ValueError("VoiceStudio manifest does not report a verified watermark")
    if sha256_file(wav_path) != audio.get("sha256"):
        raise ValueError("VoiceStudio WAV checksum does not match manifest")

    segments = manifest.get("segments") or []
    if not segments:
        raise ValueError("VoiceStudio manifest contains no narration segments")

    line_rows: list[dict] = []
    expected: list[tuple[str, int]] = []
    transcript_lines: list[str] = []
    for index, segment in enumerate(segments, 1):
        text = str(segment.get("text", "")).strip()
        if not text:
            raise ValueError(f"Empty narration chunk in manifest: {segment}")
        start = float(segment["start_seconds"])
        end = float(segment["end_seconds"])
        if end <= start:
            raise ValueError(f"Invalid segment timing: {segment}")
        line_id = f"L{index:04d}"
        line_rows.append({
            "id": line_id,
            "block": "V001",
            "slot": "NARRATOR",
            "char": "",
            "text": text,
            "start": round(start, 3),
            "end": round(end, 3),
            "drop": False,
            "source_segment_id": segment.get("id"),
        })
        transcript_lines.append(text)
        expected.extend((token, index - 1) for token in tokens(text))

    print(f"[voiceover-align] Loading {model_name!r} on CPU for {language} word alignment", flush=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4, num_workers=1)
    result_segments, info = model.transcribe(
        str(wav_path),
        language=language,
        word_timestamps=True,
        beam_size=3,
        vad_filter=True,
        condition_on_previous_text=True,
    )
    asr_words: list[dict] = []
    for row in result_segments:
        for item in row.words or []:
            asr_words.append({
                "word": str(item.word).strip(),
                "start": float(item.start),
                "end": float(item.end),
            })

    words, alignment = format_words(expected, asr_words, line_rows)
    timeline = artifact / "h2-timeline"
    (timeline / "timeline").mkdir(parents=True, exist_ok=True)
    target_wav = timeline / "timeline" / "voice.wav"
    shutil.copy2(wav_path, target_wav)
    if sha256_file(target_wav) != audio["sha256"]:
        raise RuntimeError("Timeline WAV copy changed bytes; watermark/provenance must be preserved")

    duration = float(audio["duration_seconds"])
    blocks = [{
        "id": "V001",
        "slot": "NARRATOR",
        "char": "",
        "drop": False,
        "text": "\n".join(transcript_lines),
        "start": 0.0,
        "end": round(duration, 3),
        "file": "voice.wav",
    }]
    (timeline / "timeline" / "blocks.json").write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (timeline / "timeline" / "lines.json").write_text(
        json.dumps(line_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (timeline / "timeline" / "words.json").write_text(
        json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (timeline / "timeline" / "transcript.txt").write_text(
        "\n\n".join(transcript_lines) + "\n", encoding="utf-8"
    )
    report = {
        "schema_version": 1,
        "language": language,
        "model": model_name,
        "model_runtime": "faster-whisper / CTranslate2 CPU int8",
        "detected_language": getattr(info, "language", None),
        "language_probability": round(float(getattr(info, "language_probability", 0.0)), 4),
        "audio_sha256": audio["sha256"],
        "alignment": alignment,
        "limitations": [
            "Word timestamps are ASR-assisted, not a phoneme-level forced alignment.",
            "Unmatched words receive interpolated estimates; review them before word-synchronous animation.",
            "The original narration WAV is copied byte-for-byte and is not re-encoded or trimmed.",
        ],
    }
    (timeline / "alignment-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    archive = artifact / "h2-timeline.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=4) as zf:
        for path in sorted(timeline.rglob("*")):
            if not path.is_file():
                continue
            zf.write(path, path.relative_to(timeline).as_posix())
    print(
        f"[voiceover-align] {alignment['matched_word_count']}/{alignment['expected_word_count']} "
        f"words matched ({alignment['matched_ratio']:.1%}); bundle={archive}",
        flush=True,
    )
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", type=Path, default=Path("voiceover-assets"))
    parser.add_argument("--model", default="small", choices=["base", "small", "medium"])
    args = parser.parse_args()
    archive = build_timeline(args.artifact_dir.resolve(), args.model)
    print(f"Timeline bundle ready: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
