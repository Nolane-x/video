---
name: video-command-center
description: Use whenever the user requests a video, asks to continue a film project, wants production tools/skills routed, or needs a GitHub Actions video build orchestrated.
---
# Nolane Video Command Center

## Mission
Single entry point for AI-first video production in Nolane-x/video. Turn the creative brief into an executable plan, choose an efficient toolchain, route specialist skills/plugins, work on an isolated branch, run GitHub Actions, inspect the real output and preserve handoff.

## Repository ownership
- Read AGENTS.md, the canonical video-production-master skill, docs/STATE.md, docs/AI_HANDOFF.md, docs/TOOL_INVENTORY.md and the target film manifest/shot plan.
- The parallel asset/audio AI owns video-library/**, video-library/assets/**, asset downloaders, SFX/music acquisition and .github/workflows/build-video-asset-library.yml. Never edit or trigger those paths/workflows as part of this work.
- Keep h2-selfimprove-studio v1.1.0 and nolane-video-production-studio v0.4.0 unchanged.
- Work on a dedicated branch. Do not force-push, merge or cancel other workflows. Preserve existing masters; render candidates first.

## Intake and routing
1. Reuse known project state; ask only if an essential artistic constraint cannot be sensibly defaulted.
2. Capture audience, purpose, platform/aspect ratio, duration, language, tone, narration, message, desired style and delivery constraints.
3. Route per shot:
   - Remotion: frame-driven React timeline, typography, captions and compositing.
   - HyperFrames: HTML/CSS/GSAP scenes, data graphics and HTML capture/render.
   - Motion Canvas: optional only with a separately validated compatible runtime; not in core CI.
   - GSAP/Motion/Theatre Core: animation choreography.
   - Three.js/PixiJS: browser 3D, particles and graphic effects.
   - Blender: manual CPU proof only when depth, geometry, camera/light or rigging materially helps.
   - H2: use only when the real kit, source and schema are available; never replace with a homemade renderer.
4. Open the matching specialist plugin from PLUGIN-REGISTRY.md when appropriate. ChatGPT plugins are separately activated; do not claim invisible cross-plugin invocation. Use repo Agent Skills as fallback.
5. For mixed-genre work, combine engines per shot rather than forcing the whole film through one engine.

## Production lifecycle
1. Restore state and inspect source, branch, latest render and open QA defects.
2. Research factual/contemporary content before scripting; retain source citations in research pack.
3. Build narrative arc, shot design, character/art bible and timed shot JSON.
4. Use only approved library assets or original code; respect source/license registry.
5. Prototype a difficult 3–5 second shot and inspect moving output.
6. Render using exact toolchain pins; default to CPU-first Actions profile.
7. Run technical QA, contact sheets, continuous motion review, contact/action, continuity and caption OCR/legibility.
8. Block release for missing important text, clipped captions, broken sync, missing/frozen frames, invalid audio, bad contact or wrong aspect/FPS.
9. Archive a new candidate without overwriting last approved master. Update manifest, QA ledger, hashes, Actions evidence and handoff.

## Caption hard gate
The transcript and timed on-screen-text manifest are the source of truth. Every important spoken sentence and essential visual label must appear long enough to read. OCR is a detector, not final authority; inspect moving frames. Record expected text, frames, OCR result, legibility review and blocker status.

## Toolchain policy
- Core: Node 24, Remotion 4.0.538, HyperFrames, GSAP, Motion 14.9.0, Three.js, PixiJS, Theatre Core, SVG/D3, Sharp/resvg, TypeScript, Playwright Chromium, FFmpeg and Tesseract EN/VI.
- Blender 5.2.3 is optional/manual, checksum verified and about 385 MB; never download for every 2D render.
- Motion Canvas is optional and not installed in the core profile until compatibility is demonstrated.
- Keep ComfyUI, giant video models, weights, OpenUSD/Natron native stacks and GPU-only frameworks out of standard CPU jobs.
- Never commit node_modules, browser binaries, Blender binary or render outputs into ordinary Git history.

## Evidence and handoff
Report branch/PR, exact workflow run IDs, versions, artifacts, hashes, visual review, known defects and remaining work. Never claim success solely because files were written or a job was queued.
