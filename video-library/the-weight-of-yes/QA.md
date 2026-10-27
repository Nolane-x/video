# THE WEIGHT OF YES — QA ledger

## Current state — run #23 queued
- Current workflow: [run #23](https://github.com/Nolane-x/video/actions/runs/40453130871), source commit `9f7b94ef60bc0dc1733e262aa7992264a2e03e48`.
- Goal: confirm the revised B08/B21 grounded poses and single-line B19 “NO. NOT TODAY.” caption.
- Previous run #22 failed at the storyboard gate (no final video was produced). Root cause: the new B21 blocking moved the hero's X coordinate from 0.49 to 0.43, while one old assertion in `tune_story.py` still expected 0.49. The source and workflow assertions now agree on 0.43.
- Current work is not complete while run #23 is queued/in progress.

## Latest available technical candidate — run #21
- Workflow: [run #21 — success](https://github.com/Nolane-x/video/actions/runs/40442985212), source commit `4a23abe4195133f319290f18fcccb4499dd48b5b`.
- Actions artifact: `the-weight-of-yes-h2-selfimprove-21`, ID `12706519055`, 61,842,849 bytes; SHA-256 `119d0c6a1428628a1757bf0fb15b75583c7719adfe3a48d04a569e026f79d377`; expires 2026-11-26.
- Master: 21,773,496 bytes; SHA-256 `c722d1e4363b42fff33d096f22b5b0da915e86d9b38e0c8a0b4d55863c7edb60`.
- Preview: 1,866,462 bytes; SHA-256 `c0d55b58e3b044660fdd1b994b4973036efedce12c4b5a1b399a8dbc29d4b893`.
- Review bundle: 30,907,384 bytes; SHA-256 `149dfa921fc58dfd7b0e9f52d22d184dfc232bb85fa420385c1fd5f0057b526a`.
- Master: 143.000 seconds, H.264 1920×1080 @24 fps + AAC stereo at 48 kHz.
- Audio on the exact MP4: −14.0 LUFS integrated, LRA 9.2 LU, true peak −5.0 dBFS.
- Full run #21 artifact downloaded. Every entry in its checksum ledger passed `sha256sum -c`.

## Visual review
- [x] Both contact sheets covering all 29 shots inspected.
- [x] Three frames (start/mid/end) sampled from all 12 motion-proof clips. This is targeted frame sampling, not real-time playback of each clip.
- [x] B08 portfolio stayed attached to the favor-giver through the walk-away after the shared H2 gait fix.
- [x] B22 displays the green SENT confirmation; B20's response is non-punitive; B24 reciprocal-care two-shot and B27 ledger are visible.
- [ ] Run #23 must verify B08/B21 do not read as unsupported seated figures without visible chairs.
- [ ] Run #23 must verify the unified B19 caption stays above faces and hands and can be read over the set.
- [ ] Full 143-second start-to-finish audiovisual review remains pending.
- [ ] Perceptual listening to the full audio arc remains pending; LUFS/true-peak measurements are objective checks only.

## Required technical gates
- [x] Run #21 timeline QA: 29 shots, 143.000 seconds, no gaps or overlaps.
- [x] H.264 1920×1080 @24 fps + AAC 48 kHz stereo.
- [x] EBU R128 integrated −14.0 LUFS; true peak −5.0 dBFS below −1.0 dBFS ceiling.
- [x] Twelve audio/video motion proofs validated; all artifact checksum entries verified.
- [ ] Run #23: storyboard/caption/preset gates, contact sheets, audio preview, full render, FFmpeg mastering, ffprobe and EBU R128 checks must pass.
- [ ] Refresh artifact checksums and inspect corrected B08/B19/B21 motion proofs from run #23.

**Status:** run #21 is a technically verified fallback candidate, not approved final. Run #22 was a pre-render validation failure. Run #23 is queued to validate the visual revisions. Never claim artistic approval without full-length review with sound.
