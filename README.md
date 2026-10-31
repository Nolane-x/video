# Nolane Video Studio

A genre-aware, code-first production workspace for story-led video, explainers, documentary, product demos, tutorials, interviews, short-form, animation and hybrid media. Select visual grammar and engines from the brief; do not assume every video uses the same style.

## Start here for every new AI session

**Read [AGENTS.md](AGENTS.md) first**, then the [Video Production Master skill](.agents/skills/video-production-master/SKILL.md), [Genre and Production Routing Matrix](docs/GENRE_ROUTING_MATRIX.md), [current project state](docs/STATE.md), [AI handoff](docs/AI_HANDOFF.md), and the relevant project's brief/manifest/shot plan. These files are the persistent creative and technical memory; don't rely on previous chat history alone.

## Main AI entry point

[**Nolane Video Command Center v0.7.9**](https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc) is the primary private routing plugin:
- 29 internal production skills.
- A registry of 37 separately activated specialist plugins with source/provenance notes.
- Explicit routing and handoff rules. The Command Center does not silently invoke another private plugin; ChatGPT/user controls plugin activation.

Other independent private plugins:
- [Nolane Video Production Studio v0.4.0](https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd) — broader 32-skill multi-engine production library with source snapshots and its own licensing boundaries.
- [H2 SelfImprove Studio v1.1.0](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) — native H2 rig/renderer and focused self-improvement animation workflow.

These plugins are independent. See [the video plugin registry](docs/CHATGPT_VIDEO_PLUGIN_REGISTRY.md) and the [Command Center registry](plugins/chatgpt/nolane-video-command-center/references/PLUGIN-REGISTRY.md). In particular, the Talkcraft snapshot bundled in Video Production Studio is PolyForm Noncommercial 1.0.0; commercial/monetized use requires prior written authorization. Check its license matrix before use.

## Genre-aware production policy

Read [docs/GENRE_ROUTING_MATRIX.md](docs/GENRE_ROUTING_MATRIX.md) before selecting a workflow. It maps documentary, science/math explainers, narrative animation, product demos, tutorials, interviews, music videos, vertical shorts, advertising and AI/hybrid formats to the relevant specialists, engines and QA evidence.

The canonical [stick-figure visual reference](docs/ART_DIRECTION_IFVERSE_DAYONE.md) is a **conditional direction for the established self-improvement/H2 series**, not a universal visual style. New projects should follow their own audience, purpose and visual grammar.

- [Reusable production skill](.agents/skills/video-production-master/SKILL.md)
- [Current state](docs/STATE.md)
- [Video catalog](video-library/README.md)
- [Verified tools/source inventory](docs/TOOL_INVENTORY.md)
- [Prior video catalog](video-library/previous-works-catalog.json)

## Production architecture

Route per deliverable/shot; don't install every tool for every job.

- **H2 Studio:** the native H2 rig/packs for the established self-improvement animation profile. Keep it distinct from Remotion.
- **Remotion:** frame-accurate React timeline, text/captions, transitions, composition and reproducible CI. Project: [video-projects/remotion](video-projects/remotion).
- **HyperFrames:** HTML/CSS/GSAP compositions, beat grids, deterministic browser capture and motion/layout QA.
- **Manim:** mathematically meaningful science, math and engineering explainers; verify formulas and units before rendering.
- **Blender:** selected 2.5D/3D shots where geometry, depth, camera, light or rigging adds value. [tools/blender](tools/blender).
- **Three.js / PixiJS:** procedural browser 3D/2D, particles, shaders, depth and lightweight effects.
- **Krita:** deliberately authored 2D assets and paintovers. [tools/krita](tools/krita).
- **OpenTimelineIO / PySceneDetect:** editorial interchange and candidate shot-boundary analysis, not automatic final editorial authority.
- **Playwright / Tesseract:** authorized browser capture and assisted text/caption coverage.
- **FFmpeg / ffprobe:** mastering and technical validation.

The CPU-first runtime pins dependencies in `toolchain/manifest.json` and `toolchain/node/package-lock.json`. Blender, Manim and audio-ML are separate/optional profiles; a plugin entry does not mean a runtime or model is installed.

## Canonical video and archive truth

- The canonical Full HD H2 master is stored at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`; its SHA-256 and technical verification are recorded in the film manifest and [tool inventory](docs/TOOL_INVENTORY.md).
- The separate Remotion run-36 sample is 155.1 seconds at 1280×720/24 fps. It is not the H2 render.
- H2 source ZIPs are published as checksum-verified assets in the [H2 production Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1).
- Source-v2/source-v3 are separate candidates, not canonical replacements. Technical render success does not equal full-motion/audio or artistic approval.
- Keep large masters in durable GitHub Releases where appropriate; do not call an Actions artifact permanent storage. Check its URL, metadata and SHA-256.

## Workflows and references

- [Remotion render](.github/workflows/render-remotion.yml) — generates music/SFX, typechecks, renders, masters audio, validates metadata and uploads QA.
- [Blender preview proof](.github/workflows/render-blender-preview.yml)
- [H2 runtime package](.github/workflows/prepare-h2-runtime.yml)
- [Video Showcase archive](.github/workflows/archive-video-showcase.yml)
- [Install/restore guide](docs/INSTALL_VIDEO_SKILL.md)
- [Plugin release evidence](docs/CHATGPT_PLUGIN.md)

Large video masters should be kept as Release assets, not ordinary Git blobs. Always distinguish source-only changes, successful build, rendered candidate, technical QC, full visual/audio review and approved publication.
