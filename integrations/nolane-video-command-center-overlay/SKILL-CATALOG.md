# Nolane Video Command Center — internal skill catalog v0.9.6

The Command Center contains **33 internal skills**, a directory of **37 core specialist plugins**, and **1 genre-specific Squire specialist (38 separately activated specialists total)**. Internal skills are the normal entry path. Specialist plugins require explicit host activation; they are not silently invoked. Rendering and release remain evidence-gated.

## Direction and orchestration
- `video-command-center` — single entry point, genre routing and safe execution.
- `video-production-director` — end-to-end production planning, pre-render editorial gate and release lifecycle.
- `video-production-master` — persistent repo memory, engine choice and handoff.
- `video-toolchain-orchestrator` — tool/runner selection and capability gates.
- `specialist-plugin-router` — explicit handoff to source-backed specialist plugins.

## Creative direction
- `video-cinematic-director` — story, visual language, acting, camera and storyboard.
- `cinematic-storytelling` — emotional arc and narrative progression.
- `historical-cinematic-documentary-director` — footage-led, archival/2.5D/3D historical documentary direction.
- `illustrated-history-animation-director` — original cartoon/2D history animation: expressive acting, changing historical settings, animated maps/infographics, layered camera and motion QA.
- `historical-military-animation-director` — opt-in H2 Squire/vector route for researched military-history animation.
- `motion-engineering` — cross-engine motion system selection and choreography.
- `video-motion-engineer` — timing, typography, transitions and browser scenes.
- `shotcraft-motion-librarian` — reusable motion patterns and provenance.

## Graphics and 3D
- `3d-vfx-engineering` — procedural 3D/VFX, camera, lighting and compositing.
- `video-3d-vfx-engineer` — Blender/Three.js CPU-first 3D workflow.
- `manim-explainer-director` — mathematical/scientific explainer direction.
- `video-manim-explainer` — Manim implementation and validation.

## AI media, browser and provenance
- `ai-media-asset-director` — choose AI media tools and plan generated inserts.
- `comfyui-graph-orchestrator` — inspect/plan ComfyUI graphs without silently downloading weights.
- `browser-capture-director` — authorized product/site capture with Playwright.
- `asset-provenance-rights-auditor` — verify licenses and attribution without weakening item-level rules.

## Audio, subtitles and editorial
- `historical-audio-library-curator` — search and audition OGG previews, retrieve hash-verified WAV masters, and separate public redistributable from private licensed Sonniss source tiers.
- `audio-postproduction-engineer` — recorded-sound-first dialogue, Foley/ambience/music, stems, mix and mastering.
- `video-audio-speech-engineer` — optional local speech/audio-ML lane.
- `speech-caption-alignment-engineer` — speech alignment and subtitle timing.
- `video-caption-qa-engineer` — timed-text manifests and EN/VI readability.
- `editorial-timeline-architect` — OTIO interchange and exact frame ranges.
- `video-editorial-interchange` — frame-accurate editorial handoff.
- `scene-detection-researcher` — candidate scene boundaries, camera/subject motion analysis and shot logs.

## CI, licensing and quality
- `video-render-qa` — runtime, dependency and CI evidence.
- `video-render-ci-engineer` — reproducible Actions installs, caches, SBOM and artifacts.
- `video-production-license-auditor` — code/model/media license checks.
- `video-quality-assurance` — plan-to-master QA, independent audiovisual review and release attestation.

See `references/PLUGIN-REGISTRY.md` for 37 core specialist plugins and `references/GENRE-PLUGIN-REGISTRY.md` for the separately activated Squire specialist, versions and links. See `references/PLUGIN-RESEARCH-METHODOLOGY.md` for source/verification semantics.
