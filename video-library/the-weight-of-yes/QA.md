# THE WEIGHT OF YES — QA ledger

## Latest render — run #25 passed
- Workflow: [run #25 — all 19 steps successful](https://github.com/Nolane-x/video/actions/runs/40453637108).
- Source commit: 1bfb4abe2934cc36b239bb796013178f03cae5d5.
- Renderer: native H2 SelfImprove Studio Canvas/Chromium + FFmpeg mastering; not Remotion.
- Spec: 143.000 seconds, 29 shots, H.264 1920×1080 @24 fps, AAC stereo 48 kHz, English on-screen text, no voice-over.
- Master: 21,776,467 bytes; SHA-256 73737805d180b218fd7e6fe4b0d008fb9f6672152579b80971c5ce98aab187e6.
- Preview: 30.000 seconds; SHA-256 539866c06ebed0580384d00ad29ca93f4425b7e2b32677c7b3da33d4679b0093.
- Inner review bundle: 30,922,811 bytes; SHA-256 e64a6adbb81f41f43a7ff2f70e8d161872fd8134eefd1a6bf7e3b4f66b90f70f.
- Actions artifact: the-weight-of-yes-h2-selfimprove-25, ID 12711996632, 61,873,149 bytes; archive SHA-256 318561c6296339feff95aa2afbf31553dd3d85d15f57875ecfc2ba0568d2410d; expires 2026-11-26.
- Audio: −14.0 LUFS integrated; LRA 9.2 LU; true peak −5.0 dBFS.
- Artifact downloaded successfully; every entry in SHA256SUMS.txt passed sha256sum -c. ffprobe confirmed streams, resolution, frame rate, sample rate, channels and duration. All 12 motion proofs had audio/video and were approximately six seconds.

## Targeted visual review — run #25
- [x] Both contact sheets inspected across all 29 shots.
- [x] Three frames (start, midpoint and end) from all 12 proof clips sampled. This is targeted motion sampling, not a real-time start-to-finish watch.
- [x] B08: hero remains upright/slumped while the helper carries the portfolio away; sampled frames show coherent limbs and held folder.
- [x] B19: unified “NO. NOT TODAY.” caption is in the upper negative-space lane and no longer collides with the hero in sampled frames.
- [x] B21: hero stays upright as another helper takes the folder; sampled handoff is understandable.
- [x] B22: green SENT confirmation is visible.
- [x] B20: response remains non-punitive.
- [x] B24: reciprocal-care café two-shot is present in contact sheet.
- [x] B27: rebalanced ledger/end arc is present.
- [ ] Full 143-second film must still be watched start-to-finish with audio, checking transitions, pacing, acting, prop contacts and emotional arc.
- [ ] Full perceptual listening remains pending. Objective loudness/true-peak measurements are not a substitute for listening.

## Sound arc spot-check
- [x] Master has audio; integrated loudness −14.0 LUFS and true peak −5.0 dBFS.
- [x] FFmpeg silencedetect at −45 dB found a 4.917-second quiet interval between approximately 69.12 and 74.04 seconds, matching the intended silence around the overload/turning point.
- [ ] Full start-to-finish listening remains pending.

## Historical validation failures and fixes
- Run #22 failed before rendering because a stale assertion expected B21 X=0.49 instead of authored X=0.43.
- Run #23 failed before rendering because a legacy assertion still required B08 sitdesk after its pose was changed to slump.
- Run #24 failed before rendering because stale checks expected two B19 captions after they were unified.
- Run #25 removed the contradictory checks; all 19 steps passed and the resulting artifact was downloaded and verified.

## Status and sign-off
**Technical pass + targeted motion review passed. Full-length artistic approval remains pending.** Do not call this the approved final until the complete 143-second master has been watched with sound and any remaining P0/P1 issues are resolved.
