# Time Stop 10s — Run 32 caption-fix candidate QA

Date: 2026-11-21

## Candidate and render result

- Source branch: `film/time-stop-10s-caption-safe-area-fixes`
- Source commit: `d2b6bf694be2139400e58145ba263a140ee7c1e6`
- Render workflow: [Run 32](https://github.com/Nolane-x/video/actions/runs/44901911523) — all three jobs completed successfully, including the full H2 render, sound mix, package and upload.
- Master artifact: `time-stop-10s-h2-32`, artifact ID `14707913978`, 259,453,076 bytes.
- Voice artifact: `video-voice-assets-44901911523`, artifact ID `14706377147`, 52,173,940 bytes.
- Master MP4: 1920×1080, H.264, 60fps, 22,680 frames, 378.000s; AAC stereo, 48kHz.
- Master size: 98,846,712 bytes.
- Master SHA-256: `c55b883070448d526cffeb5525cec8c9ee1583704d245dd31f239a1db878a641`.
- Render QA report: `technical-pass`; integrated loudness −14.2 LUFS, true peak −3.1 dBFS, 84 story shots, 26 freeze-FX shots; `visual_approval=false`.

## Fixes present in the rendered candidate

1. `time-stop-key-sequences-3d.js`: caption plate bottom position is calculated against the active image area after accounting for `scope`, `wide` or numeric letterbox bars. This corrects the clipping seen in key-sequence shots such as s014.
2. `time-stop-3d.js`: removed the redundant canvas subtitle draw from street-scene `overlay()`; retained the camera-space subtitle plate and the remaining visual overlays. This removes the duplicate caption previously seen in s063.

Both source changes are included in the Run 32 source SHA above. The 60 H2 Canvas 2D scenes were not changed by these fixes.

## Artifact integrity and independent spot checks

- Downloaded outer artifact ZIP size: 259,453,076 bytes. GitHub artifact digest: `sha256:28a20708dab3aa4b07f39cb2b5535941894706d4d735a9cd572fbc1ebb381b9a`.
- Extracted render package and nested review ZIP successfully; all 20 entries in the review package SHA256SUMS manifest verify.
- MP4 checksum recomputed locally and matches the release candidate hash above.
- All six contact sheets cover shots s001–s084 and were visually inspected.
- Direct 1080p frame spot checks:
  - s014 at 59.25s: caption plate is entirely inside the active image region above the lower letterbox bar.
  - s063 at 280.0s: one caption plate remains; the redundant bottom canvas caption is gone.
- The same 3D shot groups across the six sheets (kitchen s013–s022, basketball s026–s033, hallway s037–s042 and street/rescue s053–s072) show caption plates inside the image area. No repeat/clipped bottom caption was apparent in this sampled review.
- Canonical SRT: 84 cues, zero overlaps; first cue starts at 0.12s and final cue ends at 375.46s, before the 378s master end.
- Voice manifest: 84 Vietnamese VieNeu segments, 198.96s narration, 48kHz PCM24 source WAV; AudioSeal verified (7 blocks, min confidence 0.9953, mean 0.9988), clipped ratio 0.0. Source WAV SHA-256: `cf0b29daba7306ed9521af450d4613322cf278a5c1999f619f87ec2ac6e0b63a`.
- Independent FFmpeg full-master decode passed in GitHub Actions with no errors and verified all 22,680 frames; this supersedes the local all-frame decode timeout. Audio metadata, complete video and audio streams and exact SHA-256 were independently checked. The render's EBU R128 analysis processed the full video/audio at 14.1×, with I = −14.2 LUFS, LRA = 5.2 LU and true peak = −3.1 dBFS.
- Independent inspection: [Run 32 independent inspection](https://github.com/Nolane-x/video/actions/runs/44914373793) — success. Its complete FFmpeg decode, exact stream/frame/hash checks, subtitle validation, 252 per-shot stills (three per shot), four full-mix clips, ZIP packaging and upload all passed. Independent artifact `time-stop-10s-run32-independent-inspection`, ID `14711346655`, 58,746,924 bytes, digest `sha256:15e31ac571fa986b098218cf8a252d371174f9a9bee02c9089348d6e9a156080`.

- Additional cross-track verification: all 84 SRT cue start timestamps match the corresponding `voice-placement.json` `video_start` values exactly (zero start-time mismatches), and all 84 subtitle texts match the corresponding placed narration text exactly (zero text mismatches).

## Approval and release gate

- This is a rendered and technically validated candidate, not an approved release.
- Keep `visual_approval=false`. No uninterrupted human watch-through of all 6m18s with sound has been completed.
- Do not publish or overwrite Run 30 / existing release assets. Run 32 is a separate candidate for final review.
- The independent bundle has 32 key frames, all six dense motion sheets covering s001–s084, 252 samples total (3 per shot), and four full-mix sequence clips. Each clip passed independent probe/full decode: kitchen 54–99s (45s / 2,700 frames), basketball 112.5–148.5s (36s / 2,160), hallway/books 162–189s (27s / 1,620), final bicycle/sign rescue 270–324s (54s / 3,240). All four are 1920×1080/60fps with AAC 48kHz stereo. The nested ZIP passed integrity and every outer-package SHA256SUMS entry verified.
- All six dense sheets were visually inspected. Sampling confirms the caption safe-area fix across modified 3D scene groups and removal of the s063 duplicate. This is still sampled visual evidence, not a continuous full-length artistic review.
- The remaining release gate is a complete continuous watch-through with sound, including narration clarity, music balance, timing, action continuity and the end card.
