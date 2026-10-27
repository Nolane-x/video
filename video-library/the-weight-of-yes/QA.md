# THE WEIGHT OF YES — QA ledger

## Latest render — #30 technical pass with targeted visual review
- Workflow: [run #30 — success](https://github.com/Nolane-x/video/actions/runs/40461365610); all 19 steps passed.
- Source commit: [`9214fb3ce0765c38d4169be917099a75a8e53442`](https://github.com/Nolane-x/video/commit/9214fb3ce0765c38d4169be917099a75a8e53442).
- Renderer: native H2 SelfImprove Studio Canvas/Chromium + FFmpeg mastering; not Remotion.
- Spec: 143.000 seconds, 29 shots, H.264 1920×1080 @24 fps, AAC stereo 48 kHz, English on-screen text, no voice-over.
- Master: 21,783,919 bytes; SHA-256 `cfc5882636f70e98ace6fc5263c2a60ee2100cf35a2b59351940453242951e9d`.
- Preview: 30.000 seconds; SHA-256 `d963785ac2e8b9c486e866373622a59a7a6c6486b9bcab4defd21cdc0ae92965`.
- Review bundle SHA-256: `c4325fe0044f89ff3a031baa7386c4a9e0bb693e23d28966dffdd73f8b5a0455`.
- Actions artifact: `the-weight-of-yes-h2-selfimprove-30`, ID `12714602184`, 61,869,228 bytes; expires 2026-11-26. Archive SHA-256: `21810fde7a704eea5c70454c8032935631f44f2b957edd9da3e5b6ace89d515e`.
- Audio: −14.0 LUFS integrated; LRA 9.2 LU; true peak −5.0 dBFS.
- All 29 entries in `SHA256SUMS.txt` passed; ffprobe confirms duration, codecs, resolution, frame rate and audio format.

## Targeted visual review — run #30
- [x] Both contact sheets inspected across all 29 shots.
- [x] 1080p B07 frame at 32.75 s: handwritten “YES.” stays inside the left page; narration stays on the right page and clear of the outer edge.
- [x] B19 “NO. NOT TODAY.” sits in upper-left negative space, clear of actors and the classroom board on the current contact sheet.
- [x] Latest storyboard and caption-safe-area gates passed.
- [ ] Individually review all 12 motion-proof clips with audio.
- [ ] Watch the complete 143-second master start-to-finish with audio, checking pacing, transitions, hand/prop contacts, emotional arc and sound design.

## Sound arc spot-check
- [x] AAC audio present; −14.0 LUFS integrated and −5.0 dBFS true peak measured on the exact master.
- [ ] Full perceptual listening remains pending; objective loudness is not a substitute for listening.

## Historical validation failures
- Run #22 failed before rendering because a stale assertion expected B21 X=0.49 instead of authored X=0.43.
- Run #23 failed because a legacy assertion expected B08 sitdesk after its pose changed to slump.
- Run #24 failed because stale checks expected two B19 captions after they were unified.
- Run #25 passed after contradictory assertions were removed. Subsequent renders focused on caption placement and notebook framing; run #30 is the current targeted-reviewed candidate.

**Status: technical pass + targeted visual review. Full-length artistic approval remains pending.**
