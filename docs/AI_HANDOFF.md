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

## Artifact truth
The prior 155-second Full HD H2 master and source ZIP were delivered as attachments in an earlier ChatGPT session but are not binary files in this repository. The Remotion output is a separate reproducible build. Check the manifest before claiming otherwise.

## End-of-session
Run checks; inspect contact sheets and motion proofs; record exact renderer, commit, run URL, artifact storage/expiry, audio measures, defects and next actions. Update `docs/STATE.md`, this file and the per-video manifest.
