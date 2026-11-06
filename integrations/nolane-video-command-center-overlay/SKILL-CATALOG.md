# Nolane Video Command Center — internal skill catalog v0.8.3

The Command Center contains **31 internal skills**, a directory of **37 core specialist plugins**, and **1 genre-specific Squire specialist (38 separately activated specialists in total)**. Use internal skills as the normal entry path. Specialist plugins require explicit host activation; they are not silently invoked. Rendering and release remain evidence-gated.

## Direction and orchestration
- video-command-center — single entry point and safe execution.
- video-production-director — end-to-end production planning, pre-render editorial gate and release lifecycle.
- video-production-master — persistent repo memory, engine choice and handoff.
- video-toolchain-orchestrator — tool/runner selection and capability gates.
- specialist-plugin-router — explicit handoff to source-backed specialist plugins.

## Creative direction
- video-cinematic-director — story, visual language, acting, camera and storyboard.
- cinematic-storytelling — emotional arc and narrative progression.
- historical-cinematic-documentary-director — high-motion, footage-led and 2.5D/3D historical documentaries; reference study, shot grammar, asset matching and recorded-sound-first direction.
- historical-military-animation-director — opt-in H2 Squire route for researched English military-history animation in its vector style.
- motion-engineering — cross-engine motion system selection and choreography.
- video-motion-engineer — timing, typography, transitions and browser scenes.
- shotcraft-motion-librarian — reusable motion patterns and provenance.

## Graphics and 3D
- 3d-vfx-engineering — procedural 3D/VFX, camera, lighting and compositing.
- video-3d-vfx-engineer — Blender/Three.js CPU-first 3D workflow.
- manim-explainer-director — mathematical/scientific explainer direction.
- video-manim-explainer — Manim implementation and validation.

## AI media, browser and provenance
- ai-media-asset-director — choose AI media tools and plan generated inserts.
- comfyui-graph-orchestrator — inspect/plan ComfyUI graphs without silently downloading weights.
- browser-capture-director — authorized product/site capture with Playwright.
- asset-provenance-rights-auditor — verify licenses and attribution without owning acquisition.

## Audio, subtitles and editorial
- audio-postproduction-engineer — dialogue, recorded Foley/ambience/music, stems and mastering.
- video-audio-speech-engineer — optional local speech/audio-ML lane.
- speech-caption-alignment-engineer — speech alignment and subtitle timing.
- video-caption-qa-engineer — timed-text manifests and EN/VI OCR readability.
- editorial-timeline-architect — OTIO interchange and exact frame ranges.
- video-editorial-interchange — frame-accurate editorial handoff.
- scene-detection-researcher — candidate scene boundaries, camera/subject motion analysis and shot logs.

## CI, licensing and quality
- video-render-qa — runtime, dependency and CI evidence.
- video-render-ci-engineer — reproducible Actions installs, caches, SBOM and artifacts.
- video-production-license-auditor — code/model/media license checks.
- video-quality-assurance — plan-to-master QA, independent audiovisual review and release attestation.

The historical cinematic route is a new **internal skill**, not a new third-party specialist plugin. The 37 core specialist count and separate Squire specialist count remain unchanged.
