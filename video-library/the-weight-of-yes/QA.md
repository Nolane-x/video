# THE WEIGHT OF YES — QA ledger

## Current state — run #25 in progress
- Current workflow: [run #25](https://github.com/Nolane-x/video/actions/runs/40453637108), source commit `1bfb4abe2934cc36b239bb796013178f03cae5d5`.
- Progress verified: checkout, tool bootstrap, H2/audio dependencies, storyboard/art-direction assertions and timeline/contact-sheet checks have passed. The audio mix + 30-second preview step is running.
- Run #24 failed at the storyboard gate because a legacy assertion still expected separate `NO.` and `Not today.` captions after they were consolidated into `NO. NOT TODAY.`. Those stale assertions were replaced with the unified-caption check in run #25.
- No output from run #25 is claimed until its full render and audio/metadata/checksum gates finish.

## Latest available technical candidate — run #21
- Workflow: [run #21 — success](https://github.com/Nolane-x/video/actions/runs/40442985212), source commit `4a23abe4195133f319290f18fcccb4499dd48b5b`.
- Actions artifact: `the-weight-of-yes-h2-selfimprove-21`, ID `12706519055`, 61,842,849 bytes; SHA-256 `119d0c6a1428628a1757bf0fb15b75583c7719adfe3a48d04a569e026f79d377`; expires 2026-11-26.
- Master: 21,773,496 bytes; SHA-256 `c722d1e4363b42fff33d096f22b5b0da915e86d9b38e0c8a0b4d55863c7edb60`.
- Preview: 1,866,462 bytes; SHA-256 `c0d55b58e3b044660fdd1b994b4973036efedce12c4b5a1b399a8dbc29d4b893`.
- Original review ZIP: 30,907,384 bytes; SHA-256 `149dfa921fc58dfd7b0e9f52d22d184dfc232bb85fa420385c1fd5f0057b526a`.
- Master: 143.000 seconds, H.264 1920×1080 @24 fps + AAC stereo 48 kHz.
- Audio metrics on exact master: −14.0 LUFS integrated, LRA 9.2 LU, true peak −5.0 dBFS.
- Full run #21 artifact was downloaded; every entry in its checksum ledger passed `sha256sum -c`.

## Visual review
- [x] Both contact sheets covering all 29 shots inspected.
- [x] Three frames (start/mid/end) sampled from all 12 motion-proof clips; this is targeted frame sampling, not real-time playback of every clip.
- [x] B08 folder remains attached to the helper through the walk-away after the shared H2 gait fix.
- [x] B22 displays green SENT confirmation; B20's response is non-punitive; B24 reciprocal-care two-shot and B27 ledger are visible.
- [ ] Run #25 must confirm B08/B21 do not read as unsupported seated figures in the classroom.
- [ ] Run #25 must confirm unified “NO. NOT TODAY.” caption stays above faces/hands and remains readable.
- [ ] Full 143-second film start-to-finish review with sound remains pending.
- [ ] Perceptual listening to the full audio arc remains pending; loudness/true peak metrics are objective checks only.

## Required technical gates
- [x] Run #21 timeline QA: 29 shots, 143.000 seconds, no gaps or overlaps.
- [x] H.264 1920×1080 @24 fps + AAC 48 kHz stereo.
- [x] EBU R128 integrated −14.0 LUFS; true peak −5.0 dBFS below −1.0 dBFS ceiling.
- [x] Twelve audio/video motion proofs and all run #21 checksum entries validated.
- [ ] Run #25 full render, ffprobe, EBU R128, motion-proof and checksum gates must pass.
- [ ] Inspect corrected B08/B19/B21 proofs from run #25 before artistic sign-off.

**Status:** run #21 is a verified technical fallback candidate, not approved final. Full-length audiovisual sign-off remains pending.
