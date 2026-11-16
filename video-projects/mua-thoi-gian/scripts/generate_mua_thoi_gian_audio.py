#!/usr/bin/env python3
"""Generate original, royalty-free procedural underscore and story SFX for the film."""
from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np

SR = 48000
TAU = 2.0 * math.pi


def midi(note: int) -> float:
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def write_wav(path: Path, audio: np.ndarray, sample_rate: int = SR) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    audio = np.asarray(audio, dtype=np.float32)
    audio = np.nan_to_num(audio, nan=0.0, posinf=0.0, neginf=0.0)
    audio = np.clip(audio, -0.98, 0.98)
    pcm = (audio * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1 if pcm.ndim == 1 else pcm.shape[1])
        out.setsampwidth(2)
        out.setframerate(sample_rate)
        out.writeframes(pcm.tobytes())


def adsr(seconds: float, attack: float = 0.04, release: float = 0.5) -> np.ndarray:
    n = max(1, int(seconds * SR))
    t = np.arange(n, dtype=np.float32) / SR
    env = np.ones(n, dtype=np.float32)
    if attack > 0:
        env *= np.clip(t / attack, 0.0, 1.0)
    if release > 0:
        env *= np.clip((seconds - t) / release, 0.0, 1.0)
    return env


def pinkish_noise(n: int, rng: np.random.Generator) -> np.ndarray:
    white = rng.normal(0.0, 1.0, n).astype(np.float32)
    # A compact one-pole low-pass gives a softer, less brittle noise bed.
    out = np.empty_like(white)
    state = 0.0
    for i, sample in enumerate(white):
        state = 0.84 * state + 0.16 * float(sample)
        out[i] = state
    peak = max(1e-6, float(np.max(np.abs(out))))
    return out / peak


def make_sfx(name: str, rng: np.random.Generator) -> np.ndarray:
    specs = {
        "soft_impact": 0.75, "phone_vibrate": 0.72, "ui_click": 0.16,
        "time_freeze": 1.75, "whoosh_reverse": 1.2, "time_resume": 1.35,
        "paper_flick": 0.22, "clock_tick": 0.12, "cash_register": 0.8,
        "whoosh_mid": 0.92, "idea_ding": 0.9, "game_click": 0.13,
        "downer": 1.0, "plate_clink": 0.55, "low_pulse": 0.65,
        "glitch": 0.58, "room_tone": 2.4, "soft_click": 0.14,
        "chair_slide": 0.7, "street_ambience": 2.5, "end_bell": 1.7,
    }
    duration = specs[name]
    n = int(duration * SR)
    t = np.arange(n, dtype=np.float32) / SR
    env = adsr(duration, 0.008, min(0.65, duration * 0.65))
    noise = pinkish_noise(n, rng)
    out = np.zeros(n, dtype=np.float32)

    if name == "soft_impact":
        f = 88.0 - 42.0 * (t / duration)
        phase = TAU * np.cumsum(f) / SR
        out = 0.50 * np.sin(phase) + 0.16 * noise * np.exp(-t * 8)
    elif name == "phone_vibrate":
        gate = (np.sin(TAU * 24.0 * t) > 0).astype(np.float32)
        out = (0.22 * np.sin(TAU * 132.0 * t) + 0.12 * noise) * gate
    elif name in {"ui_click", "soft_click", "game_click"}:
        f = {"ui_click": 1450.0, "soft_click": 920.0, "game_click": 1850.0}[name]
        out = 0.42 * np.sin(TAU * f * t) + 0.15 * noise
        env = np.exp(-t * (36 if name != "soft_click" else 24))
    elif name in {"time_freeze", "whoosh_reverse", "time_resume", "whoosh_mid"}:
        if name == "whoosh_reverse":
            shape = (t / duration) ** 2
        elif name == "time_resume":
            shape = np.clip(1.0 - np.abs(t - duration * 0.32) / (duration * 0.38), 0, 1)
        else:
            shape = np.sin(np.pi * np.clip(t / duration, 0, 1)) ** 1.7
        sweep = np.sin(TAU * (180.0 * t - 100.0 * t * t))
        out = 0.58 * noise * shape + 0.23 * sweep * shape
        if name == "time_freeze":
            out += 0.16 * np.sin(TAU * 1174.0 * t) * np.exp(-np.maximum(0, t - 0.45) * 4)
    elif name == "paper_flick":
        out = noise * np.exp(-t * 24) * 0.36
    elif name == "clock_tick":
        out = 0.35 * np.sin(TAU * 2100.0 * t) + 0.12 * noise
        env = np.exp(-t * 42)
    elif name == "cash_register":
        out = 0.20 * np.sin(TAU * 784.0 * t) + 0.18 * np.sin(TAU * 1175.0 * t) + 0.12 * np.sin(TAU * 1568.0 * t)
        env = np.exp(-t * 4.2) * np.clip(t / 0.015, 0, 1)
    elif name == "idea_ding":
        out = 0.24 * np.sin(TAU * 880.0 * t) + 0.16 * np.sin(TAU * 1320.0 * t) + 0.10 * np.sin(TAU * 1760.0 * t)
        env = np.exp(-t * 3.7)
    elif name == "downer":
        f = 190.0 - 115.0 * (t / duration)
        phase = TAU * np.cumsum(f) / SR
        out = 0.32 * np.sin(phase) + 0.08 * noise
    elif name == "plate_clink":
        out = 0.24 * np.sin(TAU * 1180.0 * t) + 0.16 * np.sin(TAU * 1670.0 * t) + 0.06 * noise
        env = np.exp(-t * 6)
    elif name == "low_pulse":
        gate = np.sin(TAU * 2.7 * t) ** 8
        out = 0.40 * np.sin(TAU * 48.0 * t) * gate
    elif name == "glitch":
        gate = (np.sin(TAU * 31.0 * t) > 0.65).astype(np.float32)
        out = 0.55 * noise * gate + 0.13 * np.sin(TAU * 460.0 * t)
        env = np.exp(-t * 2.6)
    elif name == "room_tone":
        out = 0.065 * noise + 0.018 * np.sin(TAU * 58.0 * t) + 0.009 * np.sin(TAU * 117.0 * t)
        env = np.ones(n, dtype=np.float32)
    elif name == "chair_slide":
        ramp = np.clip(t / duration, 0, 1)
        out = 0.31 * noise * (0.45 + 0.55 * np.sin(np.pi * ramp))
        out += 0.04 * np.sin(TAU * 72.0 * t)
    elif name == "street_ambience":
        distant = 0.055 * np.sin(TAU * (52.0 * t + 2.0 * np.sin(TAU * 0.18 * t)))
        breeze = 0.09 * noise
        passing = np.clip(1.0 - np.abs(t - duration * 0.62) / (duration * 0.34), 0, 1)
        out = breeze + distant + 0.12 * passing * np.sin(TAU * 92.0 * t)
        env = np.ones(n, dtype=np.float32)
    elif name == "end_bell":
        out = (
            0.24 * np.sin(TAU * 659.25 * t)
            + 0.18 * np.sin(TAU * 987.77 * t)
            + 0.12 * np.sin(TAU * 1318.51 * t)
        )
        env = np.exp(-t * 2.5)
    else:
        raise ValueError(name)

    return np.clip(out * env * 0.55, -0.95, 0.95)


def section_chord(progress: float, index: int) -> tuple[list[int], float]:
    # Note numbers are MIDI. Each region moves through a small, coherent chord set.
    sections = [
        (0.00, 0.08, [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 60], [52, 55, 59, 64]], 0.72),
        (0.08, 0.18, [[53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67], [57, 60, 64, 69]], 0.54),
        (0.18, 0.32, [[57, 60, 64, 69], [50, 53, 57, 62], [52, 55, 59, 64], [57, 60, 64, 67]], 0.76),
        (0.32, 0.43, [[57, 60, 64, 67], [55, 59, 62, 67], [53, 57, 60, 65], [52, 55, 59, 64]], 0.58),
        (0.43, 0.56, [[48, 52, 55, 60], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], 0.62),
        (0.56, 0.68, [[50, 53, 57, 62], [45, 48, 52, 57], [52, 55, 59, 64], [57, 60, 64, 67]], 0.66),
        (0.68, 0.78, [[45, 48, 52, 57], [52, 55, 59, 64], [50, 53, 57, 62], [45, 48, 52, 57]], 0.74),
        (0.78, 0.90, [[53, 57, 60, 65], [57, 60, 64, 69], [50, 53, 57, 62], [55, 59, 62, 67]], 0.62),
        (0.90, 1.01, [[48, 52, 55, 60], [53, 57, 60, 65], [55, 59, 62, 67], [48, 52, 55, 60]], 0.58),
    ]
    for start, end, chords, gain in sections:
        if start <= progress < end:
            return chords[index % len(chords)], gain
    return [48, 52, 55, 60], 0.55


def generate_music(output: Path, duration: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    frames_total = int(math.ceil(duration * SR))
    chunk = 4 * SR
    chord_seconds = 10.5
    rng = np.random.default_rng(20261116)
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        for start in range(0, frames_total, chunk):
            count = min(chunk, frames_total - start)
            idx = np.arange(start, start + count, dtype=np.float32)
            t = idx / SR
            progress = np.minimum(1.0, t / max(1.0, duration))
            chord_index = np.floor(t / chord_seconds).astype(int)
            section = np.zeros(count, dtype=np.float32)
            left = np.zeros(count, dtype=np.float32)
            right = np.zeros(count, dtype=np.float32)

            # Group contiguous samples by chord to keep the oscillator phase stable.
            changes = np.r_[0, np.where(np.diff(chord_index) != 0)[0] + 1, count]
            for a, b in zip(changes[:-1], changes[1:]):
                if b <= a:
                    continue
                cidx = int(chord_index[a])
                chord, gain = section_chord(float(progress[a]), cidx)
                local_t = t[a:b]
                tone = np.zeros(b - a, dtype=np.float32)
                for note_i, note in enumerate(chord):
                    f = midi(note - (12 if note_i == 0 else 0))
                    phase = TAU * f * local_t
                    base = np.sin(phase)
                    overtone = 0.17 * np.sin(phase * 2.0 + 0.2)
                    slow = 0.78 + 0.22 * np.sin(TAU * (0.055 + note_i * 0.007) * local_t + note_i)
                    tone += (base + overtone) * slow * (0.012 if note_i == 0 else 0.008)
                section[a:b] = tone * gain

            # A gentle, sparse upper-register motif; no hard percussion under the narration.
            beat = np.floor(t / 4.7).astype(int)
            motif_notes = np.array([72, 76, 79, 76, 74, 72, 67, 71], dtype=int)
            motif = np.zeros(count, dtype=np.float32)
            for beat_id in np.unique(beat):
                mask = beat == beat_id
                note = motif_notes[int(beat_id) % len(motif_notes)]
                local = t[mask] - beat_id * 4.7
                f = midi(note)
                pluck = np.sin(TAU * f * local) + 0.23 * np.sin(TAU * f * 2.01 * local)
                motif[mask] += 0.018 * pluck * np.exp(-local * 2.6)

            fade_in = np.clip(t / 6.0, 0, 1)
            fade_out = np.clip((duration - t) / 10.0, 0, 1)
            master_env = np.minimum(fade_in, fade_out)
            pulse = 0.96 + 0.04 * np.sin(TAU * 0.22 * t)
            mono = (section + motif) * master_env * pulse

            # Slight stereo width without phase cancellation.
            side = 0.16 * np.sin(TAU * 0.07 * t) * section
            left = mono + side
            right = mono - side
            stereo = np.stack([left, right], axis=1)
            peak = float(np.max(np.abs(stereo)))
            if peak > 0.22:
                stereo *= 0.22 / peak
            pcm = (np.clip(stereo, -0.95, 0.95) * 32767).astype("<i2")
            wav.writeframes(pcm.tobytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, required=True)
    args = parser.parse_args()
    project = args.project_dir.resolve()
    data = json.loads((project / "src" / "shots.json").read_text(encoding="utf-8"))
    duration = float(data["durationSeconds"])
    audio_dir = project / "public" / "audio"
    generate_music(audio_dir / "music-bed.wav", duration)
    sfx_dir = audio_dir / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    names = sorted({str(s["sfx"]) for s in data["shots"] if s.get("sfx")})
    rng = np.random.default_rng(20261116)
    for name in names:
        write_wav(sfx_dir / f"{name}.wav", make_sfx(name, rng))
    print(json.dumps({
        "duration_seconds": duration,
        "music": str(audio_dir / "music-bed.wav"),
        "sfx_count": len(names),
        "sfx": names,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
