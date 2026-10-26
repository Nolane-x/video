# ALMOST READY — production project

A 172-second, 29-shot, English-language, no-voice-over animated short about perfectionism and fear of being seen. This project uses the repository's native H2 SelfImprove Studio Canvas/Chromium engine and FFmpeg mastering.

## Source of truth
- Script: video-projects/h2-selfimprove/01-PHIM-the-almost-ready.txt
- Project config: video-projects/h2-selfimprove/almost-ready/config.json
- Character/art bible: video-projects/h2-selfimprove/almost-ready/story/bible.md
- Hand-authored art direction and assertions: video-projects/h2-selfimprove/almost-ready/tune_story.py
- Publishing copy: video-library/almost-ready/02-PACKAGE-almost-ready.md
- Thumbnail prompts: video-library/almost-ready/03-THUMB-PROMPT-almost-ready.txt
- Manifest and gates: video-library/almost-ready/manifest.json, QA.md
- Render workflow: .github/workflows/render-selfimprove-almost-ready.yml

## Reproduce in GitHub Actions
The dedicated workflow installs the H2/Chromium render dependencies, parses the approved script, applies the explicit 29-shot art-direction pass, checks timeline/schema and text ranges, creates full contact sheets and a 30-second preview, renders the full film, mixes audio, exports 12 motion proofs, probes the final MP4, measures loudness/peak and uploads a review bundle. The workflow's output is technical evidence; a human must still watch all 172 seconds with audio for artistic sign-off.

## Visual target
Simple consistent H2 stick figure, staged bedroom/studio/classroom/café/city sets, amber practical light against plum/charcoal shadows, visible writing/typing and human reaction. Avoid flat repeated backdrops, zoom-only motion, captions over key action, and a shadow that remains dominant after the protagonist acts.

## Status
Source is prepared for the first CI render. Final runtime, output checksums, artifact ID and actual QA observations must be added to the manifest after the workflow result is verified.
