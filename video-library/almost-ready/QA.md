# ALMOST READY — QA ledger

## Latest render — #34 technical pass with targeted visual review
- Workflow: [run #34 — success](https://github.com/Nolane-x/video/actions/runs/40532086120); all 19 workflow steps passed.
- Source commit: [`58c95de849405b0ae5d1636851bb883ffa3870ec`](https://github.com/Nolane-x/video/commit/58c95de849405b0ae5d1636851bb883ffa3870ec).
- Temporary Actions artifact: `almost-ready-h2-selfimprove-34`, ID `12745749609`, 64,348,173 bytes; expires 2026-11-26 15:36:32 UTC. Not a durable release.
- Downloaded artifact SHA-256: `c6854df2b2f8451365882abc02c2ef71c1d63cb5bf9c4b84b549eec6fa7a80ea`.
- Master: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo; 24,066,531 bytes.
- Master SHA-256: `aed4367abf31d0373d767856e4412bc96ce6be99a3210cc8e1abb3c0e1fac12a`.
- EBU R128: −14.1 LUFS integrated, 9.1 LU LRA, −1.8 dBFS true peak.
- Preview SHA-256: `e0c264462036a8e55799b4dd21ff584c259dc38bedc86933a9429f2b73454e9f`; 30.000 s.
- Review ZIP SHA-256: `21d6431cd5f6df57daf6321d4aa6924f8fb19b76c0196d3a3b2adcff1f2d68bc`; all 25 entries in `SHA256SUMS.txt` passed.

## Targeted visual review — run #34
- [x] Both 29-shot contact sheets inspected.
- [x] B03/B09/B20 notebook captions sit inside the right-hand paper region, clear of the pen and page edges.
- [x] B13 narration sits above the reduced 11:59 clock; SNOOZE and digits remain clear.
- [x] B27 “one more tiny fix.” is fully revealed and readable; the follow-up “He didn't have to obey it.” is present in the sampled 1080p frame.
- [x] Timeline, contact-sheet, motion-proof stream/duration, ffprobe and checksum-ledger gates passed.
- [ ] Individually watch all 12 motion-proof clips with audio.
- [ ] Watch the complete 172-second master start-to-finish and sign off sound, transitions, timing, prop contact and emotional arc.

## Critical motion checks
- B03 and B20: pen tip should align to the written line; no later-line text leakage.
- B05/B07/B14/B27: temptation enters for a story reason, stays clear of the hero’s hands/face, then recedes.
- B10/B24/B25: preserve eye-lines, café table anchors and floor contact.
- B13/B15/B16: clock, deadline collapse and reset read as a cause/effect chain.
- B21/B22: typing precedes sending; sending must be a visible narrative event.
- B23: reply legible and follows the send.
- Captions: readable at 1080p and clear of eyes, hands, pen, phone/laptop UI and the outer frame.

## Gate semantics
A green CI build does not establish artistic approval. Contact sheets do not establish full motion, prop contact or sound quality. Record unresolved defects explicitly; never quietly promote a candidate to final.

**Status: technical pass + targeted visual review. Full-length artistic approval and perceptual listening remain pending.**
