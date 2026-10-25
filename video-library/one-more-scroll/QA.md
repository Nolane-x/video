# ONE MORE SCROLL — QA state

This documents the prior H2 delivery; re-verify against the actual MP4 before a new release.

## Reported technical output
- About 155 seconds, 1920×1080, 24 fps.
- H.264 video; AAC stereo 48 kHz.
- Loudness target about -14 LUFS; true peak reported about -2.4 dBFS.
- 31-shot story, generated music/SFX and intentional silence after the phone-down choice.

These are reported readings from the prior delivery, not a fresh probe of a binary currently in GitHub.

## Positive decisions to preserve
- Native H2 Canvas/Chromium renderer for delivered H2 master, not the earlier homemade SVG demo.
- Distinct location changes, not repeated generic exterior.
- Music arc: sad → dark → silence → hope → effort → resolution.
- Contact sheets and motion checks, not just “render success.”

## Defects/version distinction
The delivered master and later source-v2 are different versions. The prior master was flagged for an intense close-up expression, shoe-tying hands not clearly reaching the shoes, and a staircase camera that clipped the head. Source-v2 fixed these in code, but its full render was not verified because local Chromium navigation was blocked. Do not claim these fixes are in the canonical MP4 until a complete render proves it.

## Open release gates
- [ ] Archive the exact H2 master to durable GitHub storage.
- [ ] Record its SHA-256 and fresh ffprobe output.
- [ ] Re-render source-v2 with the real H2 engine.
- [ ] Inspect all fixed shots and transitions.
