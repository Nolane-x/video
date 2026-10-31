---
name: video-quality-assurance
description: Audit a video end-to-end for story completeness, caption coverage, visual quality, motion, continuity, audio, synchronization, technical media integrity and deliverable readiness. Use before every final video handoff or when asked to improve an existing video.
---

# Video Quality Assurance — evidence before approval

A render is only a candidate. The finished video must be watched and audited as a film.

## Audit sequence

1. Read the approved brief, script, storyboard, transcript, caption file, design bible, asset manifest and prior QA notes.
2. Probe the candidate with `ffprobe` or the project's real media probe. Record streams, codec, resolution, aspect, FPS, duration, pixel format, audio channels/sample rate and metadata.
3. Generate a contact sheet covering every shot and key text states. Include opening/middle/end samples for long shots and before/contact/after frames for complex actions.
4. Watch the full video with sound at normal speed. Then inspect complex sections frame-by-frame or at reduced speed. A contact sheet is not a replacement for playback.
5. Compare every scene against its purpose and source copy. Flag missing sections, repeated visual ideas, empty holds, incorrect data, mistranscribed words, poor transitions and contradictions.
6. Audit every caption/subtitle segment against the audio. Check exact wording, timing, punctuation, line length, reading duration, contrast, safe-area placement and overlap with important faces/objects. Captions must not silently omit key phrases.
7. Audit the visual story: visual hierarchy, framing variation, readable silhouettes, facial/action clarity, lighting motivation, depth, continuity, brand identity, consistency and restraint.
8. Audit movement: anticipation, action, contact, reaction, follow-through and recovery; check camera movement separately from subject movement. Check props, feet, shadows, intersections, temporal jitter and transition seams.
9. Audit sound: narration intelligibility, pronunciation, loudness, true peak, music ducking, SFX timing, channel balance, silence, clicks/pops and sync drift.
10. Log each issue with severity, timecode/frame range, evidence, impact and concrete fix. Re-render affected shots and repeat the relevant audit.

## Defect severity

- **P0 — release blocker:** corrupted/unplayable file, missing required stream, wrong deliverable, serious privacy/rights problem, checksum mismatch, or technical failure that prevents use.
- **P1 — major release blocker:** omitted/incorrect information, unreadable/missing important captions, major continuity/story failure, broken movement/contact, wrong product representation, obvious audio sync failure or an unusable section.
- **P2 — polish:** small spacing/easing/color/audio balance/transition problems that do not destroy comprehension but are perceptible.

Resolve every P0 and P1 before calling the video production-ready. Document accepted exceptions explicitly; do not silently downgrade severity.

## Audio measurement

Do not label the output as `-14 LUFS`, `-16 LUFS`, or any other target merely because an FFmpeg filter was configured. Measure the actual final file with an available loudness analyzer, record integrated loudness and true peak, and compare them with the platform/project target. Use the target appropriate to the content and platform, not a universal fixed number.

## Completion language

Use precise states:
- `source updated`
- `static checks passed`
- `preview rendered`
- `full render completed`
- `technical QC passed`
- `full video watched`
- `visual/editorial QA passed`
- `ready for user review`
- `published` / `archived` only with direct evidence.

Never collapse these states into a single word such as "done" when some gates remain unverified.
