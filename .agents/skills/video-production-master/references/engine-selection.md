# Engine selection

## What's really in this repo

The native H2 SelfImprove Studio plugin source has now been mirrored under `integrations/h2-selfimprove-studio/` from Plugin Creator release `pluginrel_6ade1c3ecb20819199def25125d2f89a` (v1.0.2). This includes the H2 skills, renderer scripts, rig, `dem`/`doodle` packs, and procedural audio/helpers. See `integrations/h2-selfimprove-studio/SOURCE-MANIFEST.json`. The `.plugin` binary archive itself remains outside Git; the source files are present.
The repo is `Nolane-x/video`, not a complete copy of all upstream apps or the full H2 source. It contains:
- Remotion project: `video-projects/remotion`
- Python music/SFX generators: `video-projects/remotion/h2-audio`
- Blender proof: `tools/blender/render_h2_stage.py`
- Krita authoring guidance: `tools/krita/README.md`
- State/skill/catalog: `.agents/skills`, `docs`, `video-library`

A source ZIP from a previous ChatGPT session is separate unless the manifest says it was copied here.

## Select by task
- **H2 Studio:** first choice for established H2 scenes if full source and bundled skill are available. Inspect actual entrypoint, `packs/dem`, template names, `tpl + args` schema and required sheet/audio gates.
- **Remotion:** React/frame timeline, sequences, titles, 2D motion, composition and reproducible CI. Key files: package.json, `src/Root.tsx`, `src/OneMoreScroll.tsx`, `public/story/shots.json`, `public/story/bible.md`.
- **Blender:** use when depth/parallax/lighting/3D rig genuinely benefits a scene. Start with low-poly/proxy scene and a 3–5 second proof. Script: `tools/blender/render_h2_stage.py`; workflow: `.github/workflows/render-blender-preview.yml`.
- **Krita:** use for authored expression sheets, pose/prop sheets, texture and paintovers. Export named transparent assets with stable anchors. Not a runtime dependency unless a workflow explicitly opens a `.kra` file.
- **FFmpeg:** mastering, proxies, frame capture, contact sheets and file validation; it cannot fix bad staging.

## Environment checks
Check `node`, `npm`, `python`, `ffmpeg`, `ffprobe`, `blender`, Krita and browser availability. A README/ZIP does not prove a tool is installed. GitHub Actions is a separate machine; its logs prove only the runner's result.
