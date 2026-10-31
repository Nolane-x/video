#!/usr/bin/env python3
"""Generate an original beat-led score for the OpenDesign Motion study.

Uses Python's standard library only. It deliberately does not sample or reuse
the soundtrack embedded in the user's reference video.
"""
from __future__ import annotations

import argparse
import math
import os
import wave
from array import array
from pathlib import Path

SR = 48_000
DURATION = 37.3
BPM = 115.0
TAU = math.tau


def smoothstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="public/audio/opendesign-motion-score.wav")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = int(DURATION * SR)
    left = array("h")
    right = array("h")

    # A bright, modern tech pulse: D-minor colour with suspended upper notes.
    scale = [146.83, 174.61, 220.00, 261.63, 293.66, 349.23, 392.00, 440.00]
    beat_seconds = 60.0 / BPM
    transition_times = [0.0, 3.0, 4.5, 5.5, 7.5, 10.5, 19.5, 21.0, 25.5, 30.5, 32.5, 35.3]

    # Pre-compute transition swells and UI ticks so each frame remains deterministic.
    cues = []
    for cue in transition_times:
        cues.append((cue, 0.42, "whoosh"))
    for beat in range(int(DURATION / beat_seconds) + 1):
        t = beat * beat_seconds
        cues.append((t, 0.10, "kick"))
        if beat % 4 in (1, 3):
            cues.append((t, 0.16, "clap"))
        if beat % 2 == 1:
            cues.append((t, 0.07, "tick"))

    # Event windows indexed by integer sample, avoiding a search through every cue.
    starts: dict[int, list[tuple[int, str]]] = {}
    for t, duration, kind in cues:
        start = max(0, int(t * SR))
        length = max(1, int(duration * SR))
        starts.setdefault(start, []).append((length, kind))

    active: list[list[float | int | str]] = []
    for i in range(frames):
        t = i / SR

        # Bring the groove in immediately, with a short controlled fade.
        fade_in = smoothstep(t / 0.16)
        fade_out = smoothstep((DURATION - t) / 0.65)
        master = min(fade_in, fade_out) * 0.74

        if i in starts:
            for length, kind in starts[i]:
                active.append([length, 0, kind])

        # Harmonic bed slowly changes every four bars to keep a clear arc.
        bar = int(t / (beat_seconds * 4.0))
        chord_roots = [73.42, 65.41, 87.31, 98.00, 73.42]
        root = chord_roots[min(len(chord_roots) - 1, bar // 4)]
        pad = (
            math.sin(TAU * root * t) * 0.040
            + math.sin(TAU * root * 1.5 * t + 0.4) * 0.020
            + math.sin(TAU * root * 2.0 * t + 0.8) * 0.012
        )
        step = int(t / (beat_seconds / 2.0))
        note = scale[(step + (step // 8)) % len(scale)]
        pulse = 0.5 + 0.5 * math.sin(TAU * (1.0 / (beat_seconds * 2.0)) * t)
        arp_env = 0.22 + 0.18 * pulse
        arp = (
            math.sin(TAU * note * t) * 0.040
            + math.sin(TAU * note * 2.0 * t + 0.2) * 0.012
        ) * arp_env

        beat_phase = (t / beat_seconds) % 1.0
        kick_env = math.exp(-beat_phase * 22.0) if beat_phase < 0.24 else 0.0
        kick_freq = 53.0 - beat_phase * 48.0
        kick = math.sin(TAU * kick_freq * t) * kick_env * 0.15

        # A tight offbeat hat texture, intentionally quieter than the kick.
        eighth_phase = (t / (beat_seconds / 2.0)) % 1.0
        hat_env = math.exp(-eighth_phase * 55.0) if eighth_phase < 0.09 else 0.0
        hat = math.sin(TAU * 7_200.0 * t) * hat_env * 0.012

        hit = 0.0
        keep = []
        for event in active:
            length, age, kind = int(event[0]), int(event[1]), str(event[2])
            x = age / SR
            if age < length:
                if kind == "whoosh":
                    q = x / (length / SR)
                    env = math.sin(math.pi * q) ** 1.4
                    wavelet = math.sin(TAU * (170.0 + 520.0 * q) * x)
                    hit += env * wavelet * 0.035
                elif kind == "kick":
                    env = math.exp(-x * 27.0)
                    hit += math.sin(TAU * (76.0 - 26.0 * x) * x) * env * 0.075
                elif kind == "clap":
                    env = math.exp(-x * 31.0)
                    noise = math.sin(TAU * 1_913.0 * x) * math.sin(TAU * 2_771.0 * x)
                    hit += noise * env * 0.035
                elif kind == "tick":
                    env = math.exp(-x * 62.0)
                    hit += math.sin(TAU * 2_100.0 * x) * env * 0.018
                event[1] = age + 1
                keep.append(event)
        active = keep

        mono = (pad + arp + kick + hat + hit) * master
        # Tiny stereo decorrelation keeps the mix centred and mono-compatible.
        l = max(-0.92, min(0.92, mono + 0.0015 * math.sin(TAU * 0.17 * t)))
        r = max(-0.92, min(0.92, mono - 0.0015 * math.sin(TAU * 0.17 * t)))
        left.append(int(l * 32767))
        right.append(int(r * 32767))

    interleaved = array("h")
    for l, r in zip(left, right):
        interleaved.append(l)
        interleaved.append(r)
    if os.sys.byteorder != "little":
        interleaved.byteswap()

    with wave.open(str(out), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(interleaved.tobytes())

    print(f"Generated original score: {out} ({DURATION:.1f}s, {BPM:.0f} BPM, {SR} Hz stereo; reference-aligned original composition)")


if __name__ == "__main__":
    main()
