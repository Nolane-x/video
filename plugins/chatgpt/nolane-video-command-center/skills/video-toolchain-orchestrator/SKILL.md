---
name: video-toolchain-orchestrator
description: Use when selecting, installing or coordinating the repo video engines, tools, GitHub Actions profiles or specialist ChatGPT plugins for a requested video.
---
# Video Toolchain Orchestrator

## Mission
Choose the smallest compatible engine/profile and the fewest useful specialist skills for each requested shot. Do not install or invoke every engine for every video.

## Required sequence
1. Read `AGENTS.md`, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/TOOL_INVENTORY.md`, the target film manifest and the exact current GitHub head.
2. Read `toolchain/manifest.json`, `docs/video-toolchain/README.md` and the license register. Inspect current tool versions, package lock, relevant workflows, Actions logs and artifacts.
3. Convert the brief into shot requirements: story, language, ratio, duration, FPS, text/caption coverage, action/contact, camera, depth, audio and delivery.
4. Route per shot: Remotion for frame-accurate React timeline/compositing; HyperFrames for HTML/CSS/GSAP; Manim for maths/science; Three/Pixi for browser graphics; Blender only when real 3D geometry/camera/light adds value; H2 only when its native kit/schema is available.
5. Treat Motion Canvas as an optional candidate only after a separate current Vite/plugin compatibility proof. It is not in the core install.
6. Treat WhisperX/Demucs as a manual-only optional code profile; do not download model weights or credentials. Treat ComfyUI and diffusion/video models as explicit opt-in after hardware, license, disk and cost review.
7. Load a relevant included skill. Specialist plugins are optional separate activations; never claim invisible plugin-to-plugin invocation.
8. Leave resource-library acquisition to its parallel owner. Do not touch `video-library/**`, resource catalogues, downloaders, asset importers or the asset build workflow while that workstream is active.
9. Work on a clean dedicated branch. Audit every changed path before opening a PR; if a proposed branch contains asset or unrelated paths, isolate only the approved toolchain files onto current `main`.
10. Run the narrowest relevant proof, then core smoke. Save exact run ID, logs, artifact, lockfile, SBOM, dependency license report and checksums; inspect render/video evidence.

## CPU-first profiles
- Core: Node 24, Ubuntu 24.04, Remotion 4.0.538, HyperFrames 0.8.222, GSAP 3.15.0, Motion 14.9.0, Three.js 0.186.1, PixiJS 8.22.0, Theatre Core, SVG/D3, resvg, Sharp, Playwright Chromium, FFmpeg and Tesseract EN/VI.
- The direct npm versions are exact-pinned and must agree with the committed npm v3 lockfile. Core Actions use `npm ci`; no install step may rewrite or push to the PR branch.
- Editorial Python: OpenTimelineIO 0.18.1 and headless PySceneDetect 0.7.2.
- Manim: CE 0.22.1, isolated Cairo/Pango/TeX setup; path-scoped PR proof plus manual dispatch.
- Blender: official 5.2.3 archive, checksum verified, optional CPU software-render proof; only path-scoped PR changes or manual dispatch.
- Audio ML: WhisperX 3.8.6 + Demucs 4.1.0, manual dispatch only, no weights in the install artifact.

## Engine decision rules
- Prefer Remotion for the master timeline when React/frame control and caption timing matter.
- Use HyperFrames for HTML/CSS/GSAP scenes, controlled browser capture, layout lint and snapshots.
- Use Manim only where equation/diagram transformations need mathematical correctness; verify equations and units before rendering.
- Use Three.js/PixiJS for modest procedural depth, particles, shaders and parallax without a native renderer.
- Use Blender only for shots where spatial geometry, physical light, rigs or camera depth materially improve the result. Start with a low-res CPU proof.
- Use OTIO for timeline interchange, not media storage; use PySceneDetect for candidate cuts, never as final editorial authority.
- Use FFmpeg for audio/video mastering and probing; use OCR as a secondary text detector, then compare against the timed text contract and visually inspect.
- Never rely on GPU availability in a normal GitHub-hosted CPU runner.

## Release and QA gates
- Confirm the committed lockfile, dependency/license evidence and tool versions.
- Check the PR changed-file list and ensure scope is uncontaminated.
- Validate codecs, frame rate, resolution, duration, audio streams, loudness, peak and checksum.
- Inspect every scene/contact sheet and moving frames around action/contact, transitions and text holds.
- No technical or artistic success claim without corresponding Actions evidence; no final artistic approval without viewing the actual moving picture/audio.
- Preserve the last-known-good master; candidates are separate until reviewed.

## Outputs
Engine/profile decision table, per-shot routing, locked dependency profile, storyboard/text manifest, license/provenance review, Actions run links, technical QA, moving-frame notes and reproducible handoff.
