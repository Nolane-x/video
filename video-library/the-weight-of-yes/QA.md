# THE WEIGHT OF YES — QA ledger

## Current status — render #8 technical pass
- Workflow: [run #8 — success](https://github.com/Nolane-x/video/actions/runs/40429993390); all 19 workflow steps passed.
- Source/render commit: [`1ab974acc2f8e0b268940fbf16f6b566884dace6`](https://github.com/Nolane-x/video/commit/1ab974acc2f8e0b268940fbf16f6b566884dace6) — shared H2 scheduled-motion fix.
- Temporary Actions artifact: `the-weight-of-yes-h2-selfimprove-8`, ID `12701373173`, 58,464,627 bytes; expires 2026-11-26T01:05:42Z. This is not a durable release.
- Project: 143.000 s, 29 shots, H.264 1920×1080 @24 fps, AAC 48 kHz stereo, English on-screen text, no voice-over.
- Master: 20,652,791 bytes; SHA-256 `87f3fb490289d3bb34527dc49821c3d9cdbb0cb12ff8c2af6a36e7803e2691a9`.
- Audio on the exact MP4: −14.0 LUFS integrated, LRA 9.2 LU, true peak −5.0 dBFS.
- Preview: 30.000 s with video + AAC sound; SHA-256 `ad1351737a2e10a926f6ae96713412bbf07a761a3b8e4ef016bf505019180f97`.
- Review ZIP: 29,218,876 bytes; SHA-256 `3d786efda871f5185043aad20eb27c0d8432a7db5973ddfefcbd4061509a9378`; every entry in its checksum file passed after download.

## Targeted visual review
- [x] Both contact sheets reviewed across all 29 shots.
- [x] B08 proof sampled at opening, middle and end: limbs remain coherent and the portfolio stays attached to the favor-giver during departure.
- [x] B19 boundary caption sits in negative space; B20's response is visible and non-punitive.
- [x] B21 shows another helper taking the folder; B22 shows SENT; B24 reciprocal-care two-shot and B27 rebalanced ledger are present in the contact sheets.
- [ ] Watch the entire 143-second film start-to-finish with audio, checking transitions, pacing, acting, prop contacts and emotional arc.
- [ ] Individually watch the 30-second preview and all 12 motion proofs with audio; the eleven proofs other than B08 were not all individually watched.

## Technical gates
- [x] Native H2 timeline / authored story QA passed: 29 shot IDs, 143.000 s, no gaps/overlaps.
- [x] Master H.264 1920×1080 @24 fps + AAC 48 kHz stereo.
- [x] Runtime 143.000 s; EBU R128 −14.0 LUFS; true peak −5.0 dBFS (below −1.0 dBFS ceiling).
- [x] Twelve ~6-second motion proofs contain audio/video; packaged checksum ledger validates.
- [x] All entries in `SHA256SUMS.txt` passed `sha256sum -c`.

## Root cause and fix
The earlier B08 proof exposed an engine bug: a scheduled `walk: {to, at, dur, speed}` object remained on the actor while movement was idle, and the character rig treated the object as a numeric gait speed. That could corrupt limb coordinates and detach held props at the first/last frames. The shared native H2 renderer now strips scheduled `walk`/`run` descriptor objects outside the active gait window in `integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit/packs/dem/templates.js`. The new B08 proof was checked at the beginning, middle and end; the portfolio remains held and limbs are coherent.

**Technical pass; artistic sign-off pending.** CI and targeted motion checks do not replace a full-length review with audio. Do not mark this an approved final or replace the canonical ONE MORE SCROLL master until the complete viewing is finished.
