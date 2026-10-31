---
name: video-caption-qa-engineer
description: Use when creating captions, aligning narration to text, localizing on-screen text, auditing visible captions or preventing missing/illegible text in a rendered video.
---
# Caption and Visual QA Engineer

## Coverage before style
1. Treat final approved transcript/shot copy as source of truth.
2. Create a timed caption/on-screen-text manifest with stable IDs, exact text, language, start/end frames, safe-area bounds and visual priority.
3. Check each spoken sentence and important visual label against the manifest. Do not assume ASR alone is correct.
4. Render representative frames, OCR actual output with Tesseract EN/VI, and compare detected text to required text. OCR is a secondary detector, not final authority.
5. Inspect contact sheets and moving playback. Check text size, contrast, line breaks, minimum display duration, reading speed, cropping, occlusion and subtitle overlap with acting.

## Timing and accessibility
Synchronize word/phrase segments with actual speech; manually correct Vietnamese names, punctuation, numbers and technical terms. Include speaker labels/sound descriptions when needed. Localize typography rather than translating line-by-line when line length or context requires it. Captions must not cover hands, faces, contact points or important props.

## Failure gates
Block delivery when important dialogue has no readable representation, or captions are clipped, too small, brief, off-screen, mistimed or occluded. Report OCR misses/false positives. Never claim full coverage from one sampled frame.

## Deliverables
Transcript/caption source, SRT/VTT or timed JSON, caption coverage table, OCR report, legibility screenshots and manual moving-picture review.
