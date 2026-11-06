# Instructions for AI agents in this repository

## Mandatory start sequence
Read in order: (1) `.agents/skills/video-production-master/SKILL.md`, (2) `docs/STATE.md`, (3) `docs/AI_HANDOFF.md`, (4) `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, (5) `video-library/README.md`, (6) `video-library/reference-clips.json`, (7) `video-library/one-more-scroll/manifest.json` and `QA.md`, (8) `video-projects/remotion/README.md`, (9) `video-projects/remotion/public/story/bible.md`, (10) `video-projects/remotion/public/story/shots.json`. Then inspect current HEAD, relevant Actions/logs/artifacts, and the actual files.

## Non-negotiable requirements

## Genre routing and recorded-sound policy
- The preferred stick-figure house style remains the default only when the brief or existing series calls for it. A supplied illustrated/cartoon history reference routes to `.agents/skills/illustrated-history-animation-director/SKILL.md`; use expressive acting, varied environments, prop choreography, animated maps/graphics and multi-plane motion rather than repeating the same vector board. A footage-led cinematic historical brief routes to `historical-cinematic-documentary-director`. Do not force either route into H2 Squire.
- H2 Squire is an opt-in route for the explicitly requested Squire/vector language or an established Squire series. Historical subject matter alone does not select Squire.
- For cinematic documentary production, complete a full-length reference watch with sound and a timestamped camera/action/audio study. If decoding or playback is blocked, state BLOCKED_NOT_WATCHED rather than inventing an analysis.
- Search and audition the existing Build 76 media pool before generating or downloading new material. The Build 76 release already includes about 1.14 GB of separate audio archives; use the source map in audio-library/SOURCES.json, then verify each item's license and attribution.
- Prefer real recorded sound and licensed music. Procedural audio is a temporary placeholder or documented exception; code should arrange, synchronize, process and master genuine recordings.
- Do not mutate video-library/**, global asset source manifests, downloaders, packagers or the parallel asset-library workflow from a production route. Read and consume its Releases with per-item rights.
- See docs/HISTORICAL_CINEMATIC_DOCUMENTARY_PLAYBOOK.md and docs/SAMURAI_REFERENCE_STUDY.md for the cinematic-documentary route and reference-review status.

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

## Audio discovery
Search `audio-library/generated/preview-catalog.json` and `audio-library/generated/meta-preview-catalog.json` before unpacking archives. Check source and rights metadata, audition the selected preview, and fetch only the required source/member.

Sonniss GDC 2026 is tracked as `private_production_only`: the licensee must accept current EULA v2.0, raw archives/WAVs must never be pushed into this public repo, its public Releases or its public Actions artifacts, and the sound files must never be used for AI/ML training. Keep only sanitized metadata and production cue decisions here.
