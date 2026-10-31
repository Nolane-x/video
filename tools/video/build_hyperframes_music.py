#!/usr/bin/env python3
"""Generate a deterministic original ambient bed for the HyperFrames CI proof."""
from __future__ import annotations
import argparse, math, struct, wave
from pathlib import Path

SAMPLE_RATE = 48_000
DURATION = 17.0
CHORDS = (
    (146.83, 174.61, 220.00, 261.63),
    (116.54, 146.83, 174.61, 220.00),
    (130.81, 164.81, 196.00, 233.08),
    (130.81, 164.81, 196.00, 261.63),
)

def _envelope(t: float, duration: float) -> float:
    return min(1.0, t / 1.15) * min(1.0, max(0.0, (duration - t) / 1.7))

def synth_sample(t: float, duration: float = DURATION) -> tuple[float, float]:
    bar = duration / len(CHORDS)
    chord = CHORDS[min(len(CHORDS) - 1, int(t / bar))]
    env = _envelope(t, duration)
    pad = 0.0
    for index, frequency in enumerate(chord):
        phase = 2.0 * math.pi * frequency * t
        level = (0.026 if index == 0 else 0.017) / (1.0 + index * 0.18)
        pad += level * math.sin(phase)
        pad += level * 0.18 * math.sin(phase * 2.0 + index * 0.13)
    bass = 0.035 * math.sin(2.0 * math.pi * (chord[0] / 2.0) * t)
    beat_pos = t % 0.85
    pluck_frequency = chord[(int(t / 0.85) % 3) + 1]
    pluck = 0.0
    if beat_pos < 0.38:
        pluck_env = math.exp(-beat_pos * 8.0) * min(1.0, t / 0.3)
        pluck = 0.045 * pluck_env * math.sin(2.0 * math.pi * pluck_frequency * beat_pos)
    left = (pad + bass + pluck) * env
    right = (pad * 0.94 + bass * 0.92 + pluck * 0.82) * env
    return max(-0.6, min(0.6, left)), max(-0.6, min(0.6, right))

def write_music_bed(output: Path, duration: float = DURATION, sample_rate: int = SAMPLE_RATE) -> None:
    if duration <= 0 or sample_rate < 8_000:
        raise ValueError("duration must be positive and sample_rate at least 8000 Hz")
    output.parent.mkdir(parents=True, exist_ok=True)
    frame_count = int(round(duration * sample_rate))
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(2); wav.setsampwidth(2); wav.setframerate(sample_rate)
        chunk = bytearray()
        for frame in range(frame_count):
            left, right = synth_sample(frame / sample_rate, duration)
            chunk.extend(struct.pack("<hh", int(left * 32767), int(right * 32767)))
            if len(chunk) >= 128 * 1024:
                wav.writeframesraw(chunk); chunk.clear()
        if chunk:
            wav.writeframesraw(chunk)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=DURATION)
    args = parser.parse_args()
    write_music_bed(args.output, duration=args.duration)
    print(f"Generated original ambient bed: {args.output} ({args.duration:.2f}s @ {SAMPLE_RATE}Hz stereo)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
