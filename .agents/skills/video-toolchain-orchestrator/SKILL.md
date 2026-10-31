---
name: video-toolchain-orchestrator
description: Use when selecting, installing or coordinating the repo video engines, tools, GitHub Actions profiles or specialist ChatGPT plugins for a requested video.
---
# Video Toolchain Orchestrator

## Mission
Choose the smallest compatible set of engines and specialists that can deliver the requested look and motion. Do not install or invoke every engine for every video.

## Required sequence
1. Read AGENTS.md, current project state/handoff and target film manifest before changing a film.
2. Read toolchain/manifest.json and docs/video-toolchain/README.md; check actual installed versions or run the CPU toolchain workflow.
3. Convert the brief into shot requirements: story, style, ratio, duration, FPS, text/caption coverage, action/contact, camera, depth, audio and delivery.
4. Route by shot: Remotion for frame-accurate React timeline/compositing; HyperFrames for HTML/CSS/GSAP; Motion Canvas for explanatory vector motion; Three/Pixi for browser graphics; Blender only when actual 3D geometry/camera/light adds value; H2 only when its real kit and schema are available.
5. Load the specialist in docs/CHATGPT_VIDEO_PLUGIN_REGISTRY.md. Plugins are separately activated; do not claim invisible plugin-to-plugin invocation. Use repo skill fallback if specialist is not active.
6. Leave media/resource-library work to the parallel asset workstream; it owns video-library/** and its Actions pipeline.
7. Run the relevant workflow, save run ID, logs, artifact links and dependency manifest; review motion and contact sheets.

## CPU-first routing
- Prefer deterministic code-driven motion and small npm packages on ubuntu-24.04.
- Core includes Remotion, HyperFrames, Motion Canvas packages, GSAP, Motion, Three.js, PixiJS, Theatre Core, SVG/D3 and browser QA.
- Blender is manual/on-demand and CPU-rendered in the default runner; its 385 MB archive is not part of every CI run.
- Reject GPU-heavy diffusion/video models for ordinary Actions jobs. Ask for a GPU only when procedural techniques cannot meet the shot and a supported runner/budget exists.

## Outputs and gates
Per-video engine plan, locked dependency profile, shot/asset manifest, Actions run links, technical QA, moving-frame notes and reproducible handoff. No success claim without workflow logs. No artistic sign-off from build success alone. Never overwrite a last-known-good master before a candidate passes technical and visual review.
