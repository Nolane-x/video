# AI session handoff

## First reads
Read root `AGENTS.md`, `.agents/skills/video-production-master/SKILL.md`, `docs/STATE.md`, and `video-library/one-more-scroll/manifest.json`.

## Creative decisions to preserve
- User wants cinematic story-led stick-figure video, not generic AI-looking colors or flat repeated SVG backgrounds.
- Simple character; rich environment; warm practical lighting; motivated camera/editing; expressive action; visible contact; intentional sound arc.
- References: user-provided videos and Ifverse Tales / Day One Films. Study techniques; don't copy assets.
- The user expects honesty: “file exported” is not “visual QA passed.”
- Never confuse H2 Canvas/Chromium render with Remotion or Blender output.

## Project map
- Repo: https://github.com/Nolane-x/video
- Skill: `.agents/skills/video-production-master/SKILL.md`
- Remotion: `video-projects/remotion`
- Storyboard: `video-projects/remotion/public/story/shots.json`
- Audio generators: `video-projects/remotion/h2-audio`
- Blender: `tools/blender/render_h2_stage.py`
- Krita: `tools/krita/README.md`
- H2 source mirror: `integrations/h2-selfimprove-studio/` (51-file v1.0.2 base); v1.1.0 production overlay: `integrations/h2-selfimprove-studio-production-overlay/`.
- Active private ChatGPT plugin: [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) — v1.1.0, current release `pluginrel_6ade248942988191a57ff1059c818720` (Plugin Creator update confirmed 2026-10-25); see `docs/CHATGPT_PLUGIN.md` and `integrations/h2-selfimprove-studio-production-overlay/RELEASE-RESULT-v1.1.0.md`.
- Film manifest: `video-library/one-more-scroll/manifest.json`

## Tool and video inventory
- Read `docs/TOOL_INVENTORY.md` and `video-library/previous-works-catalog.json` before assuming an app/source archive or old video is present.
- `tools/video/archive_previous_works.py` stages prior clips by fixed SHA; the GitHub verification workflow marks them permanent only after the remote files are checked.
- `tools/video/publish_h2_source_release.ps1` uploads the large H2 source packages to a versioned GitHub Release after checksum validation.

## Artifact truth
The exact 155-second Full HD H2 master is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4` and verified by workflow run 40271825143. The source ZIP remains external to GitHub until uploaded separately. The Remotion reference build under `video-library/one-more-scroll/renders/remotion-run-31/` is a separate renderer output. Never conflate them.

## End-of-session
Run checks; inspect contact sheets and motion proofs; record exact renderer, commit, run URL, artifact storage/expiry, audio measures, defects and next actions. Update `docs/STATE.md`, this file and the per-video manifest.


## Latest archived Remotion reference
- Video: `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`
- Source commit: `e766c5f407cf4bbd175c28d306acc99c6d8aa609`; render CI: [40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650).
- SHA-256: `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`; 155.100s, 1280x720, 24/1.
- This is a Remotion render, not the H2 Canvas/Chromium master. Inspect contact sheets and motion proof before accepting artistic quality.
