# THE WEIGHT OF YES — QA ledger

## Current state — run #24 queued
- Current workflow: [run #24](https://github.com/Nolane-x/video/actions/runs/40453407914), source commit `4343b01d5265f89b1833a9e14d50fcf6b48976eb`.
- Run #22 failed because B21's authored X=0.43 disagreed with a stale assertion expecting 0.49. That gate was fixed in run #23.
- Run #23 then exposed a second, contradictory legacy assertion requiring B08's pose to be `sitdesk` after the new art direction deliberately changed B08 to `slump`. That redundant assertion was removed in run #24.
- These two runs failed before video rendering; no new MP4 was produced by them.

## Latest available technical candidate — run #21
- Workflow: [run #21 — success](https://github.com/Nolane-x/video/actions/runs/40442985212), source commit `4a23abe4195133f319290f18fcccb4499dd48b5b`.
- Actions artifact: `the-weight-of-yes-h2-selfimprove-21`, ID `12706519055`, 61,842,849 bytes; SHA-256 `119d0c6a1428628a1757bf0fb15b75583c7719adfe3a48d04a569e026f79d377`; expires 2026-11-26.
- Master: 21,773,496 bytes; SHA-256 `c722d1e4363b42fff33d096f22b5b0da915e86d9b38e0c8a0b4d55863c7edb60`.
- Preview: 1,866,462 bytes; SHA-256 `c0d55b58e3b044660fdd1b994b4973036efedce12c4b5a1b399a8dbc29d4b893`.
- Original review ZIP: 30,907,384 bytes; SHA-256 `149dfa921fc58dfd7b0e9f52d22d184dfc232bb85fa420385c1fd5f0057b526a`.
- Master: 143.000 seconds, H.264 1920×1080 @24 fps + AAC stereo 48 kHz.
- Audio metrics on exact master: −14.0 LUFS integrated, LRA 9.2 LU, true peak −5.0 dBFS.
- Full run #21 artifact was downloaded. Every entry in its checksum ledger passed `sha256sum -c`.

## Visual review
- [x] Both contact sheets covering all 29 shots inspected.
- [x] Three frames (start/mid/end) sampled from all 12 motion-proof clips. This is targeted frame sampling, not real-time playback of every clip.
- [x] B08's folder remains attached to the favor-giver through the walk-away after the shared H2 gait fix.
- [x] B22 shows the green SENT confirmation; B20's response is non-punitive; B24's reciprocal-care two-shot and B27's ledger are visible.
- [ ] Run #24 must confirm B08/B21 no longer read as unsupported seated figures in the classroom.
- [ ] Run #24 must confirm the unified “NO. NOT TODAY.” caption stays above faces/hands and is readable against the background.
- [ ] Full 143-second film start-to-finish review with sound remains pending.
- [ ] Perceptual listening to the full audio arc remains pending; LUFS/true-peak are objective checks only.

## Required technical gates
- [x] Run #21 timeline QA: 29 shots, 143.000 seconds, no gaps/overlaps.
- [x] H.264 1920×1080 @24 fps + AAC 48 kHz stereo.
- [x] EBU R128 integrated −14.0 LUFS; true peak −5.0 dBFS, below −1.0 dBFS ceiling.
- [x] Twelve audio/video motion proofs validated; all run #21 artifact checksum entries verified.
- [ ] Run #24: storyboard/caption/preset gates, contact sheets, audio preview, full render, ffprobe, EBU R128, motion-proof and checksum gates must pass.
- [ ] Review corrected B08/B19/B21 proofs from run #24 before artistic sign-off.

**Status:** run #21 is a verified technical fallback candidate, not an approved final. Full-length audiovisual approval remains pending.
