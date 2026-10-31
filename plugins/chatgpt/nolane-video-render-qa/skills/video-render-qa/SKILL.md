---
name: video-render-qa
description: Use when installing video tools, configuring GitHub Actions rendering, checking media integrity, captions, audio, motion continuity or release readiness.
---

# Video Render and Quality Supervisor

## CI runtime
- Read toolchain/manifest.json; exact-pin direct packages and keep package/license reports.
- Use Node 24, Python 3.12, Ubuntu 24.04, FFmpeg/ffprobe, Tesseract EN/VI and Playwright Chromium for CPU-first jobs.
- Cache npm downloads and Playwright browsers. Do not commit node_modules, browsers, Blender archives or renders into normal Git history.
- Blender is manual-only; verify official SHA-256 before extraction.
- Use least-privilege permissions, bounded concurrency and timeouts. Never touch asset-library workflow groups.

## Technical QA
Validate container, streams, duration, dimensions, FPS, codecs, sample rate, channels, loudness, true peak, black frames, silence, corrupt frames and checksums. Save ffprobe JSON, command, source commit and workflow run ID.

## Caption QA — release blocker
1. Treat transcript and timed text manifest as source of truth.
2. Confirm every spoken/important line is visible in the composition.
3. OCR representative frames with Tesseract EN/VI; compare to expected text, then manually review misses and false positives.
4. Verify safe margins, font size, contrast, line breaks, reading time, crop and occlusion.
5. Inspect text through motion and cuts, not a single screenshot.

## Visual QA
Generate per-shot and overview contact sheets. Play complete output or representative moving sections. Inspect anticipation, action, contact, follow-through, recovery, transitions, crop, set variety and visual consistency. A successful CLI exit and valid MP4 are technical gates, not artistic sign-off.

## Delivery and preservation
Render to a temporary candidate. Keep the last known-good master until the new candidate passes technical and visual gates. Store QA report, source hash, tool versions, manifest, metadata, contact sheets and known limitations.
