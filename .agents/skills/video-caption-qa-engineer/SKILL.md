---
name: video-caption-qa-engineer
description: Use when creating captions, aligning narration to text, localizing on-screen text, auditing visible captions or preventing missing/illegible text in a rendered video.
---
# Caption and Visual QA Engineer

## Coverage before style
1. Treat final approved transcript/shot copy as source of truth.
2. Create a timed caption/on-screen-text manifest with stable IDs, exact text, language, start/end frames, safe-area bounds and visual priority.
3. Every shot must have a text contract: include subtitles plus every meaningful visible heading, label, counter, kinetic word or end-card title. For Remotion shots, the auditor infers known subtitle, day-counter, red-word and fixed scene-label fields; use `requiredOnScreenText` for additional or genre-specific overlays.
4. A shot intentionally containing no text must declare `noTextRequired: true` and a specific `noTextReason`. An unexplained empty shot is a missing-contract blocker, not an automatic pass.
5. Check each spoken sentence and important visual label against the manifest. Do not assume ASR alone is correct.
6. Render representative frames, OCR actual output with Tesseract EN/VI, and compare detected text to required text. The current audit samples three points per shot and requires readable detection in at least two; a single lucky OCR hit is not enough. When whole-frame OCR misses a known overlay, run a tight composition-aware crop (for example the day-counter badge, calendar heading, bus-stop sign or lower-third subtitle), enlarge it with a high-quality scaler, apply restrained grayscale/contrast/sharpness preprocessing, and record crop OCR separately. Use language models appropriate to the expected string (for example English-only on English labels; retain EN/VI for bilingual subtitles). Exact compact alphanumeric matches such as `DAY14` for `DAY 14` are acceptable when no characters are lost. For known small overlays, use a per-region binary threshold tuned to the foreground/background palette (for example light text on dark badges versus dark text on warm calendar panels); do not reuse one threshold indiscriminately. Crops must target the actual rendered element and must not lower the acceptance threshold. OCR is a secondary detector, not final authority.
7. Inspect contact sheets and moving playback. Check text size, contrast, line breaks, minimum display duration, reading speed, cropping, occlusion and subtitle overlap with acting.

## Timing and accessibility
Synchronize word/phrase segments with actual speech; manually correct Vietnamese names, punctuation, numbers and technical terms. Include speaker labels/sound descriptions when needed. Localize typography rather than translating line-by-line when line length or context requires it. Captions must not cover hands, faces, contact points or important props.

## Failure gates
Block delivery when important dialogue has no readable representation, or captions are clipped, too small, brief, off-screen, mistimed or occluded. In particular, never place kinetic words across faces or let small labels depend on visual guessing. Report OCR misses/false positives and inspect crop evidence before deciding whether a miss is visual or detector-related. Never claim full coverage from one sampled frame.

## Deliverables
Transcript/caption source, SRT/VTT or timed JSON, caption coverage table, OCR report, legibility screenshots and manual moving-picture review.
