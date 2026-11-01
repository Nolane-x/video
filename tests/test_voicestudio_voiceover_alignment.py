from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "video" / "align_voicestudio_voiceover.py"
SPEC = importlib.util.spec_from_file_location("voiceover_aligner", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_vietnamese_words_keep_diacritics_and_ignore_punctuation_tokens():
    assert MODULE.normalize_token("ĐỪNG") == "đừng"
    assert MODULE.tokens("Xin chào — thế giới!") == ["Xin", "chào", "thế", "giới"]


def test_asr_words_are_mapped_to_h2_schema_and_keep_line_ownership():
    lines = [
        {"id": "L0001", "start": 0.0, "end": 0.8},
        {"id": "L0002", "start": 1.0, "end": 1.8},
    ]
    expected = [
        ("Xin", 0), ("chào.", 0),
        ("Thế", 1), ("giới!", 1),
    ]
    asr = [
        {"word": "Xin", "start": 0.08, "end": 0.24},
        {"word": " chào.", "start": 0.27, "end": 0.66},
        {"word": " Thế", "start": 1.08, "end": 1.30},
        {"word": " giới!", "start": 1.34, "end": 1.67},
    ]
    words, report = MODULE.format_words(expected, asr, lines)
    assert report["matched_ratio"] == 1.0
    assert [word["w"] for word in words] == ["Xin", "chào", "Thế", "giới"]
    assert [word["line"] for word in words] == ["L0001", "L0001", "L0002", "L0002"]
    assert all(word["alignment"] == "asr-word-timestamp" for word in words)
    assert all(word["t"] < word["e"] for word in words)


def test_unmatched_words_are_interpolated_inside_their_sentence():
    lines = [{"id": "L0001", "start": 0.0, "end": 1.0}]
    expected = [("Xin", 0), ("chào", 0), ("bạn", 0)]
    asr = [
        {"word": "Xin", "start": 0.05, "end": 0.20},
        {"word": "bạn", "start": 0.75, "end": 0.93},
    ]
    words, report = MODULE.format_words(expected, asr, lines)
    assert report["matched_word_count"] == 2
    assert report["interpolated_word_count"] == 1
    assert words[1]["alignment"] == "interpolated"
    assert words[0]["t"] <= words[1]["t"] <= words[2]["t"]
    assert 0 <= words[1]["t"] < words[1]["e"] <= 1.0


def test_interpolation_does_not_cross_segment_boundaries():
    lines = [
        {"id": "L0001", "start": 0.0, "end": 0.4},
        {"id": "L0002", "start": 0.8, "end": 1.2},
    ]
    expected = [("Xin", 0), ("chào", 0), ("thế", 1), ("giới", 1)]
    asr = [
        {"word": "Xin", "start": 0.05, "end": 0.15},
        {"word": "giới", "start": 1.0, "end": 1.1},
    ]
    words, _ = MODULE.format_words(expected, asr, lines)
    assert all(0 <= word["t"] <= 0.4 for word in words[:2])
    assert all(0.8 <= word["t"] <= 1.2 for word in words[2:])
