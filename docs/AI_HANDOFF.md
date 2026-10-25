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
- Film manifest: `video-library/one-more-scroll/manifest.json`

## Tool and video inventory
- Read `docs/TOOL_INVENTORY.md` and `video-library/previous-works-catalog.json` before assuming an app/source archive or old video is present.
- `tools/video/archive_previous_works.py` stages prior clips by fixed SHA; the GitHub verification workflow marks them permanent only after the remote files are checked.
- `tools/video/publish_h2_source_release.ps1` uploads the large H2 source packages to a versioned GitHub Release after checksum validation.

## Artifact truth
The prior 155-second Full HD H2 master and source ZIP were delivered as attachments in an earlier ChatGPT session; metadata, SHA-256 and ffprobe results are recorded in the manifest. The exact H2 binary is still not committed here. The Remotion reference build has been persisted under `video-library/one-more-scroll/renders/remotion-run-31/`; this is a separate renderer output. Never conflate them.

## End-of-session
Run checks; inspect contact sheets and motion proofs; record exact renderer, commit, run URL, artifact storage/expiry, audio measures, defects and next actions. Update `docs/STATE.md`, this file and the per-video manifest.


## Latest archived Remotion reference
- Video: `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`
- Source commit: `e766c5f407cf4bbd175c28d306acc99c6d8aa609`; render CI: [40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650).
- SHA-256: `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`; 155.100s, 1280x720, 24/1.
- This is a Remotion render, not the H2 Canvas/Chromium master. Inspect contact sheets and motion proof before accepting artistic quality.
