---
name: video-render-qa
description: Use when installing video tools, configuring GitHub Actions rendering, checking media integrity, captions, audio, motion continuity or release readiness.
---

# Video Render and Quality Supervisor

## CI runtime
- Read `toolchain/manifest.json`; exact-pin direct packages and keep the package/license report.
- Use Node 24, Python 3.12, Ubuntu 24.04, FFmpeg/ffprobe, Tesseract EN/VI and Playwright Chromium for CPU-first jobs.
- Cache npm package downloads and Playwright browser binaries. Do not commit `node_modules`, browser binaries, Blender archives or render output in normal Git history.
- Keep Blender in its manual profile; verify official SHA-256 before extraction.
- Use least-privilege workflow permissions, bounded concurrency and timeouts. Never touch asset-library workflow groups.

## Technical QA
Validate container, video/audio streams, duration, dimensions, FPS, codecs, sample rate, channels, loudness, true peak, black frames, silence, corrupt frames and file checksum. Save ffprobe JSON and exact render command, source commit and workflow run ID.

## Caption QA — release blocker
1. Treat transcript and timed text manifest as source of truth.
2. Confirm all spoken/important lines are visible in the composition, not only burned into notes or metadata.
3. OCR representative rendered frames with Tesseract EN/VI; compare against expected text, then manually review misses/false positives.
4. Verify safe margins, font size, contrast, line breaks, reading time, positioning, cropping and overlap with action.
5. Inspect text across motion and cuts, not a single screenshot.

## Visual QA
Generate per-shot and overview contact sheets. Play the complete output or at least representative moving sections. Inspect anticipation, action, prop contact, follow-through, recovery, transitions, crop, set variety and visual consistency. A successful CLI exit and valid MP4 are technical gates, not artistic sign-off.

## Delivery and preservation
Render to a temporary candidate. Keep the last known-good master until the new candidate passes all technical and visual gates. Store QA report, source hash, tool versions, manifest, metadata, contact sheets and known limits.
