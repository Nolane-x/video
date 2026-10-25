# Instructions for AI agents in this repository

## Mandatory start sequence
Read in order: (1) `.agents/skills/video-production-master/SKILL.md`, (2) `docs/STATE.md`, (3) `docs/AI_HANDOFF.md`, (4) `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, (5) `video-library/README.md`, (6) `video-projects/remotion/README.md`, (7) `video-projects/remotion/public/story/bible.md`, (8) `video-projects/remotion/public/story/shots.json`. Then inspect current HEAD, relevant Actions/logs/artifacts, and the actual files.

## Non-negotiable requirements
- Preferred look: cinematic, story-led stick-figure animation. Character simple and reusable; environments, light, camera, props and action carry richness.
- Do not regress to flat slides, generic gradients, repeated sets, excessive HUDs, pseudo-real AI humans, or zoom-only “motion.”
- Do not replace H2 Studio with a homemade SVG renderer without explicit approval. Remotion is a separate timeline/compositing pipeline; never call it the H2 renderer.
- Choose per shot: H2 Canvas/rig, Remotion, Blender, Krita and FFmpeg each have distinct roles.
- Never claim a program ran unless its command/workflow log proves it. Distinguish code written, build passed, render succeeded, and visual QA passed.
- A successful export is only a technical gate. Inspect every scene in contact sheets and actual moving frames around contact/action/recovery.
- Save storyboard JSON, asset provenance, contact sheets, audio measurements, render metadata, QA report and handoff.
- Preserve the last known-good master. Don't overwrite it before the next render passes QA.
- Do not commit secrets, API keys, copyrighted reference footage, or assets without redistribution rights.

See `docs/STATE.md` and `video-library/one-more-scroll/manifest.json` for current status. The previous Full HD H2 master was delivered as a prior ChatGPT attachment; it is not yet a permanent binary file in this repository.
