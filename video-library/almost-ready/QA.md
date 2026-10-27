# ALMOST READY — QA ledger

## Latest render — #33 technical pass with targeted visual review
- Workflow: [run #33 — success](https://github.com/Nolane-x/video/actions/runs/40462284021); all 19 steps passed.
- Source commit: [`263e855a675b451f799ee684d66515b23a0dded7`](https://github.com/Nolane-x/video/commit/263e855a675b451f799ee684d66515b23a0dded7).
- Temporary Actions artifact: `almost-ready-h2-selfimprove-33`, ID `12714493740`, 64,227,290 bytes; expires 2026-11-26. Not durable release storage.
- Master: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo; 24,016,274 bytes.
- Master SHA-256: `1b55dc7dda017d7f9869c2b3b5e5492a2c97d471e51ac958e019a031c7af5fc9`.
- EBU R128: −14.1 LUFS integrated, 9.1 LU LRA, −1.8 dBFS true peak.
- Preview SHA-256: `099f8bfdc31f3f3fa4adbe67e1534d2bbe8fe8721c68a797a80b671901dad59b`; 30.000 s.
- Review ZIP SHA-256: `db80d442367b89d42558021658b0b5787acaf6706e84954f4262adffdcb27b63`; all 25 entries in `SHA256SUMS.txt` passed.

## Targeted visual review — run #33
- [x] Both 29-shot contact sheets inspected.
- [x] B03/B09/B20 notebook captions sit inside the right-hand paper region rather than overflowing the page edge.
- [x] 1080p B13 frame extracted at 74.5 s: narration sits above the reduced 11:59 clock, with SNOOZE and digits clear.
- [x] B05/B07/B14 retain the separate temptation layer and explanatory narration.
- [x] Timeline/contact-sheet gates, motion-proof exports, stream checks and checksum ledger passed.
- [ ] Individually watch all 12 motion-proof clips with audio.
- [ ] Watch the complete 172-second master start-to-finish and sign off audio, transitions, timing, prop contact and emotional arc.

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
