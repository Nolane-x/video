# HyperFrames CPU proof — Nolane Video

This repository-owned 17-second, 1920×1080 sample verifies the pinned HyperFrames runtime and its production checks. It is self-contained: the workflow copies the exact pinned GSAP distribution into `vendor/`; no CDN, external footage, remote font or remote texture is needed. A small original ambient bed is synthesized deterministically during CI.

## What it demonstrates

- A visible first frame and readable title treatment.
- Four timed visual beats: story, motion, clarity and final delivery.
- Phrase-level on-screen text with comfortable reading holds and an original generated audio bed.
- Locally bundled GSAP timelines and a motion sidecar with time-based assertions.
- Deterministic CPU browser rendering.

## Quality gates

The workflow runs HyperFrames `check` with strict mode, snapshots, sampled frames and transition sampling. The generated JSON is passed to `tools/video/validate_hyperframes_report.py`, which fails on warnings/errors, disabled motion checks, missing motion samples or failed contrast/layout/runtime/craft sections. The final MP4 is independently checked for duration, dimensions, frame rate and codec.

The audio file is a procedural CI fixture, not a downloaded resource-library asset. A passing proof validates this sample/runtime integration only. It does not certify every future project or grant rights to assets, models, fonts or music.
