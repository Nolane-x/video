# THE FIRST HOUR — QA and handoff

## Latest render — #55 technical pass with targeted visual review
- Workflow: [run #55 — success](https://github.com/Nolane-x/video/actions/runs/40626868973); all render, mix, stream and loudness checks passed.
- Source commit: [`9d86d9a4195982924868468887ff68a2fbcf1790`](https://github.com/Nolane-x/video/commit/9d86d9a4195982924868468887ff68a2fbcf1790).
- Temporary Actions artifact: `the-first-hour-h2-selfimprove-55`, ID `12789354772`, 74,398,229 bytes; expires 2026-11-27 03:35:04 UTC. Not a durable release.
- Downloaded artifact SHA-256: `02fd88d1ecf76010453d2ea3e37c0f2f00f600219d888b7bf8b18ff791cb6d5c`.
- Master: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo; 26,866,550 bytes.
- Master SHA-256: `67171131ab8ab539b82f992651ef6c5b3ce4e70efd91af92292e0da763a5bc6a`.
- EBU R128: −14.0 LUFS integrated, 6.6 LU LRA, −1.9 dBFS true peak.
- Preview SHA-256: `cedabafa48eedf397d09a02dcf11245baef461f3fc2b88bdcd868c042512c879`; 30.000 s.
- Review ZIP SHA-256: `8685bf5217a458e954401f3c461214ace167444257e36b55248175e124b89ae8`; all 24 entries in `SHA256SUMS.txt` passed.
- All 24 checksum-ledger files were recomputed after downloading the artifact; no missing files or hash mismatches.

## Targeted visual review — run #55
- [x] Both 29-shot contact sheets inspected.
- [x] B20 notebook-writing caption remains on the right page, clear of the pen and bottom/page edge.
- [x] B27 whisper at 154.5 s: “just one more scroll.” fully displayed in the right-side safe lane below the calendar.
- [x] B27 closing line at 157.2, 158.2 and 159.5 s: “But it sounded smaller now.” is fully within the left safe lane, not clipped, and no longer overlaps the whisper.
- [x] Final merged storyboard confirms the B27 whisper holds for 2.85 s; closing narration begins after it and has 3.15 s inside the 9 s shot.
- [x] Post-override regression gates passed; the workflow now checks the final merged storyboard so `shot-overrides.json` cannot silently replace the corrected coordinates/timing.
- [x] Timeline, contact-sheet, motion-proof stream/duration, ffprobe, audio-loudness and checksum gates passed.
- [x] Six-point visual frame sweep of all 12 motion proofs; no sampled caption/crop regression found. This is a visual-only pass; perceptual listening of the proof clips remains pending.
- [ ] Individually watch all 12 motion-proof clips with audio.
- [ ] Watch the complete 172-second master start-to-finish with audio, checking pacing, transitions, acting, prop contact, sound arc and emotional payoff.

## Caption-regression history
- Run #52 was technically successful but full-resolution review found the B27 closing narration clipped at the left edge and the whisper crossing the hanging calendar.
- Run #53 was also technically successful but still rendered the old positions. Root cause: the workflow replaces each shot's full `args` from `shot-overrides.json` after `tune_story.py` runs.
- Corrected the actual B27 source in `video-projects/h2-selfimprove/the-first-hour/shot-overrides.json` and added safe-lane, non-overlap and minimum-readable-dwell assertions immediately after the override merge in `.github/workflows/render-selfimprove-film.yml`. Run #55 passed these gates and the resulting frames were rechecked.

## Critical motion checks
- B03: alarm-hand hesitation must remain distinct from the “five more minutes” temptation.
- B19: walk to desk — review foot placement and limbs through the full movement, not only endpoints.
- B20: notebook-writing reveal must not leak the next line or collide with the pen.
- B25: punch-bag impact/recoil must stay visible and timed to sound.
- Caption safe-area rule: no text clipped by the frame or competing with eyes, hands, pen, screen UI or important props.

**Status: technical pass + targeted visual review. Full-length artistic and perceptual audio approval remain pending.**
