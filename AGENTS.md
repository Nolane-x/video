# Instructions for AI agents in this repository

## Mandatory start sequence
Read in order: (1) `.agents/skills/video-production-master/SKILL.md`, (2) `docs/STATE.md`, (3) `docs/AI_HANDOFF.md`, (4) `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, (5) `video-library/README.md`, (6) `video-library/reference-clips.json`, (7) `video-library/one-more-scroll/manifest.json` and `QA.md`, (8) `video-projects/remotion/README.md`, (9) `video-projects/remotion/public/story/bible.md`, (10) `video-projects/remotion/public/story/shots.json`. Then inspect current HEAD, relevant Actions/logs/artifacts, and the actual files.

## Historical military animation — Squire route

When a task explicitly asks for animated historical military history in the Squire look, read `docs/GENRE_ROUTING_MATRIX.md` and `tools/video/genre-routing.json`, then use the dedicated route under `integrations/h2-squire-studio/`. The current mirrored source is the private `h2-squire-studio` v1.2.2 plugin. This is a separate code-drawn vector/canvas engine; do not call it Remotion or H2 Canvas/Chromium.

- Squire projects live in `video-projects/squire/<slug>/`.
- The first reference production is `video-projects/squire/cannae-216bc/`.
- Use VoiceStudio's pinned reusable Actions workflow for requested synthetic narration. Select exact voice IDs from the live manifest and retain the complete voice metadata, generated WAV, captions and provenance.
- Use the Squire engine's real registered templates and presets. Never invent unsupported names.
- Attribute historical claims, label ancient force/casualty counts as estimates, and label tactical diagrams as reconstructions.
- Render to a separate Actions candidate and keep its artifact, preview, contact sheets, QA, checksum and review log. Never overwrite the existing H2/Remotion masters.
- A green Actions run is only a technical gate. Human full-motion/audio review is still required before publication.
- Keep this work separate from the parallel asset-library ownership boundary below.

## Non-negotiable requirements
- Preferred look: cinematic, story-led stick-figure animation. Character simple and reusable; environments, light, camera, props and action carry richness.
- Do not regress to flat slides, generic gradients, repeated sets, excessive HUDs, pseudo-real AI humans, or zoom-only “motion.”
- Do not replace H2 Studio with a homemade SVG renderer without explicit approval. Remotion is a separate timeline/compositing pipeline; never call it the H2 renderer.
- Choose per shot: H2 Canvas/rig, Remotion, Blender, Krita and FFmpeg each have distinct roles.
- Never claim a program ran unless its command/workflow log proves it. Distinguish code written, build passed, render succeeded, and visual QA passed.
- A successful export is only a technical gate. Inspect every scene in contact sheets and actual moving frames around contact/action/recovery.
- Save storyboard JSON, asset provenance, contact sheets, audio measurements, render metadata, QA report and handoff.
- Synthetic voice-over is opt-in. When explicitly requested, use `.github/workflows/render-voicestudio-voiceover.yml` and read `docs/VOICEOVER_WORKFLOW.md`; don't wire TTS into normal render commits by default. Review the full WAV before publishing, and don't fabricate word-level alignment from SRT cues.
- Preserve the last known-good master. Don't overwrite it before the next render passes QA.
- Do not commit secrets, API keys, copyrighted reference footage, or assets without redistribution rights.

See `docs/STATE.md` and `video-library/one-more-scroll/manifest.json` for current status. The exact Full HD H2 master is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, verified by [Actions run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The separate H2 source ZIPs are published in the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1); hashes and URLs are recorded in `video-library/one-more-scroll/h2-source-release.json`. Source-v2 has passed a full technical render and stream validation in [run 40276064292](https://github.com/Nolane-x/video/actions/runs/40276064292); it remains a separate candidate pending full-motion review. A focused source-v3 shoe-tying preview passed in [run 40280228327](https://github.com/Nolane-x/video/actions/runs/40280228327). Corrected full-render rerun [40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324) passed render, ffprobe, EBU R128, review-bundle checksum and publication. The separate [candidate MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v3-shoelace-fix-candidate.mp4) has SHA-256 `761d238ae019e6c39eca3a9c46bff88b02f6f96e332f35d6e5d6b0d41e29310f`; the [review ZIP](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v3-shoelace-fix-review.zip) has SHA-256 `56bf506a0ec63fbb9d99256ac1cc989186f6ddab12056c9cfb9f012b922d0745`. Technical pass is not artistic approval: review the complete moving picture/audio and keep the canonical H2 master unchanged. Check `docs/STATE.md`, `docs/AI_HANDOFF.md`, `video-library/one-more-scroll/QA.md`, and `video-library/one-more-scroll/h2-source-release.json`; do not overwrite the canonical H2 master. Consult `video-library/reference-clips.json` for the two user-selected reference-video links; do not claim to have watched them until reviewed.
