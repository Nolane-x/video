# Remotion sample: One More Scroll

This is the repository's reproducible Remotion composition. It is a separate pipeline from the H2 Canvas/Chromium master, not a relabeling of that file.

## Local run
```powershell
npm install
npm run typecheck
npm run dev
npm run render
```
Output: `out/one-more-scroll.mp4`.

## Current plan
The data-driven shot plan in `public/story/shots.json` is the source of truth. The current intended plan is 31 shots × 5 seconds = 155 seconds at 24 fps and 1280×720, with procedural H2-style music/SFX generation. Check current JSON and CI logs before relying on these values.

## Required production QA
- Read root `AGENTS.md` and `.agents/skills/video-production-master/SKILL.md`.
- Inspect the full contact sheet and moving tests around hard contacts.
- Check hand/phone and pen/page, cup/mouth, feet/stairs, fist/bag, and shot/crop continuity.
- Check audio peaks, loudness and intentional-silence segments.
- A passing export is only a technical gate.

The Remotion workflow uploads video/QA as an Actions artifact, then the archive workflow commits the rendered MP4 (force-added despite the global media ignore rule), contact sheets, metadata, checksums and skill ZIP to `video-library/one-more-scroll/`. Keep this pipeline output clearly distinguished from the prior H2 Canvas/Chromium master. That release is still not the original H2 Canvas/Chromium master.


## Persistent archive

A render commit with `[archive-video]` in its commit message triggers the archive workflow after CI succeeds. It stores a versioned MP4, contact sheets, metadata/checksums and a skill ZIP under `video-library/one-more-scroll/renders/` and updates the folder's latest-render pointer. The archived MP4 is the Remotion pipeline output; it is not the original H2 Canvas/Chromium master.


## Prior-work preservation

The current reference render is embedded in `video-library/one-more-scroll/renders/`. Older iterations are indexed in `video-library/previous-works-catalog.json`. A later AI must check whether an entry is a committed repository file, a GitHub Release asset, or only an attachment from an older ChatGPT session. Don't claim to have watched a video if only its catalog entry/contact sheet was available.
