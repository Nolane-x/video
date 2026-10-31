# Nolane Video Command Center v0.6.0

**One private ChatGPT plugin for the normal Nolane video workflow.** It bundles 28 internal skills across creative direction, story, cinematography, motion, Remotion/HyperFrames, Manim, 3D/VFX, AI media planning, ComfyUI graphs, browser capture, audio/speech, bilingual caption QA, editorial interchange, CI, licensing and final review.

## How to use

1. Start with this plugin and describe the video goal, audience, language, duration, visual style and delivery constraints.
2. The Command Center restores the current repository/film state and routes only to the internal skills that materially help the requested work.
3. It selects the smallest compatible engine/profile per shot rather than installing or running every tool.
4. It operates on a dedicated clean GitHub branch, reads Actions logs/artifacts and verifies the resulting candidate before handoff.
5. Specialist plugins remain optional direct entry points. ChatGPT does not silently activate another private plugin, so the Command Center contains the core production skills it needs internally.

## Production toolchain

- **Core CPU lane:** Node 24, Remotion 4.0.538, HyperFrames 0.8.222, GSAP 3.15.0, Motion 14.9.0, Three.js 0.186.1, PixiJS 8.22.0, Theatre Core, SVG/D3, resvg, Sharp, Playwright Chromium, FFmpeg/ffprobe and Tesseract EN/VI.
- **Editorial:** OpenTimelineIO 0.18.1 + PySceneDetect headless 0.7.2.
- **Educational animation:** Manim CE 0.22.1 with isolated Cairo/Pango/TeX dependencies.
- **3D/VFX:** Blender 5.2.3 from the official host with SHA-256 verification; optional, path-scoped CPU proof and manual dispatch.
- **Audio ML:** WhisperX 3.8.6 + Demucs 4.1.0 in an isolated manual-only profile. It does not download model weights or credentials.
- **Optional lanes:** Motion Canvas stays outside core until its current Vite/plugin compatibility proof passes. ComfyUI and large diffusion/video weights are not installed on ordinary CPU Actions runners.

## Repository safety and reproducibility

- The parallel asset agent owns `video-library/**`, source catalogues, downloaders, `tools/video/build_asset_library*.py`, CDC/asset importers and `.github/workflows/build-video-asset-library.yml`. Do not modify or trigger these paths unless the user explicitly reassigns that workstream.
- Before opening a PR, audit the complete changed-file list. A toolchain PR must not contain asset-library paths; split contaminated work onto a clean branch from current `main`.
- Do not overwrite master videos. Render a candidate, verify checksums/streams/audio, inspect contact sheets and moving footage, then promote only after visual approval.
- The Node package manifest and committed v3 lockfile must match. Core CI uses `npm ci`, has `contents: read` permission, and never commits back to a PR branch.
- Preserve dependency pins, license inventory, CycloneDX SBOM, FFmpeg build configuration and runtime checksums. Re-check special Remotion/GSAP terms, model/weight terms, fonts and media provenance.
- A passing CI/render proves only the technical gate. Artistic approval requires actual moving-picture and audio review.

See `SKILL-CATALOG.md` for the 28 internal skills and `references/PLUGIN-REGISTRY.md` for optional specialist plugins.
