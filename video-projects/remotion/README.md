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

The Remotion workflow uploads video/QA as a temporary artifact. A commit message containing `[archive-video]` triggers the archive workflow, which copies the resulting Remotion render and the skill ZIP to a permanent GitHub Release. That release is still not the original H2 Canvas/Chromium master.


## Persistent archive

A render commit with `[archive-video]` in its commit message triggers the archive workflow after CI succeeds. It stores a versioned MP4, contact sheets, metadata/checksums and a skill ZIP under `video-library/one-more-scroll/renders/` and updates the folder's latest-render pointer. The archived MP4 is the Remotion pipeline output; it is not the original H2 Canvas/Chromium master.
