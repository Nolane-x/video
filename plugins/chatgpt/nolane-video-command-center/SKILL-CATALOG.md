# Nolane Video Command Center — internal skill catalog v0.7.8

The Command Center contains **29 internal skills** and an explicit directory of **37 separate specialist plugins**. Use the internal skills as the normal entry path. Specialist plugins require an explicit switch through the host; they are not silently invoked.

## Direction and orchestration
- `video-command-center` — single entry point and safe execution.
- `video-production-director` — end-to-end production planning and release lifecycle.
- `video-production-master` — persistent repo memory, engine choice and handoff.
- `video-toolchain-orchestrator` — tool/runner selection and capability gates.
- `specialist-plugin-router` — explicit handoff to source-backed specialist plugins.

## Creative direction
- `video-cinematic-director` — story, visual language, acting, camera and storyboard.
- `cinematic-storytelling` — emotional arc and narrative progression.
- `motion-engineering` — cross-engine motion system selection and choreography.
- `video-motion-engineer` — timing, typography, transitions and browser scenes.
- `shotcraft-motion-librarian` — research reusable motion patterns and provenance.

## Graphics and 3D
- `3d-vfx-engineering` — procedural 3D, lighting and compositing.
- `video-3d-vfx-engineer` — Blender/Three.js CPU-first 3D workflow.
- `manim-explainer-director` — mathematical/scientific explainer direction.
- `video-manim-explainer` — Manim implementation and validation.

## AI media, browser and provenance
- `ai-media-asset-director` — choose AI media tools and plan generated inserts.
- `comfyui-graph-orchestrator` — inspect/plan ComfyUI graphs without silently downloading weights.
- `browser-capture-director` — authorized product/site capture with Playwright.
- `asset-provenance-rights-auditor` — verify licenses and attribution without owning acquisition.

## Audio, subtitles and editorial
- `audio-postproduction-engineer` — dialogue, music/SFX and mastering.
- `video-audio-speech-engineer` — optional local speech/audio-ML lane.
- `speech-caption-alignment-engineer` — speech alignment and subtitle timing.
- `video-caption-qa-engineer` — timed-text manifests and EN/VI OCR readability.
- `editorial-timeline-architect` — OTIO interchange and exact frame ranges.
- `video-editorial-interchange` — frame-accurate editorial handoff.
- `scene-detection-researcher` — candidate scene boundaries and shot logs.

## CI, licensing and quality
- `video-render-qa` — runtime, dependency and CI evidence.
- `video-render-ci-engineer` — reproducible Actions installs, caches, SBOM and artifacts.
- `video-production-license-auditor` — code/model/media license checks.
- `video-quality-assurance` — final technical and visual gate.

See `references/PLUGIN-REGISTRY.md` for all 37 specialist names, current versions and explicit links; see `references/PLUGIN-RESEARCH-METHODOLOGY.md` for source/verification semantics.
