# THE WEIGHT OF YES — QA ledger

## Latest render — #31 technical pass with targeted visual review
- Workflow: [run #31 — success](https://github.com/Nolane-x/video/actions/runs/40532086413); all 19 workflow steps passed.
- Source commit: [`58c95de849405b0ae5d1636851bb883ffa3870ec`](https://github.com/Nolane-x/video/commit/58c95de849405b0ae5d1636851bb883ffa3870ec).
- Renderer: native H2 SelfImprove Studio Canvas/Chromium + FFmpeg mastering; not Remotion.
- Temporary Actions artifact: `the-weight-of-yes-h2-selfimprove-31`, ID `12746292555`, 61,868,285 bytes; expires 2026-11-26 15:36:18 UTC. Not a durable release.
- Downloaded artifact SHA-256: `ddfbc5100354b0cd881632767649faf075605bd3ee560938f22cbd4d0a367b3f`.
- Master: 143.000 s, H.264 1920×1080 @24 fps, AAC stereo 48 kHz; 21,783,919 bytes.
- Master SHA-256: `cfc5882636f70e98ace6fc5263c2a60ee2100cf35a2b59351940453242951e9d`.
- Preview SHA-256: `d963785ac2e8b9c486e866373622a59a7a6c6486b9bcab4defd21cdc0ae92965`; 30.000 s.
- Review bundle SHA-256: `dcd222468bd915cf202b6fb46f55eb945d382b062c16986a41692db90ed311d5`; all 29 entries in `SHA256SUMS.txt` passed.
- Audio: −14.0 LUFS integrated; LRA 9.2 LU; true peak −5.0 dBFS.

## Targeted visual review — run #31
- [x] Both contact sheets inspected across all 29 shots.
- [x] B07 at 29 s: handwritten “YES.” remains within the left notebook page and its narration stays in the right page lane.
- [x] B19 at 89 s: “NO. NOT TODAY.” remains readable in upper negative space, clear of the actors and classroom board.
- [x] Downloaded master matches the manifest SHA-256; ffprobe confirms duration, codecs, resolution, frame rate and audio format.
- [x] All 29 entries in the downloaded checksum ledger passed.
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
