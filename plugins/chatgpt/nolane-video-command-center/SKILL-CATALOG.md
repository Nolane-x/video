# Nolane Video Command Center — skill catalog v0.4.0

The Command Center includes 23 internal skills. Use the one plugin as the normal entry point; the specialist plugins listed in `references/PLUGIN-REGISTRY.md` are optional focused entry points.

## Direction and story
- `video-command-center` — primary entry and route selection.
- `video-production-director` — end-to-end production direction and release lifecycle.
- `video-cinematic-director` — story, visual language, acting, camera and storyboard.
- `cinematic-storytelling` — story architecture and emotional progression.
- `video-production-master` — persistent repo workflow, H2/Remotion/Blender/Krita production gates and handoff.

## Motion, 2D/3D and explainers
- `motion-engineering` — Remotion, GSAP, Motion, Three.js and PixiJS.
- `video-motion-engineer` — engine selection, motion grammar and motion QA.
- `3d-vfx-engineering` — procedural 3D/VFX and compositing.
- `video-3d-vfx-engineer` — Blender/Three.js CPU-first 3D workflow.
- `manim-explainer-director` — mathematical/scientific explainer animation.
- `video-manim-explainer` — Manim implementation and validation.

## Audio, speech, text and accessibility
- `audio-postproduction-engineer` — voice, music/SFX and mastering.
- `video-audio-speech-engineer` — optional WhisperX/Demucs and stem workflows.
- `speech-caption-alignment-engineer` — speech alignment and captions.
- `video-caption-qa-engineer` — timed text manifest, bilingual OCR and caption legibility.

## Editorial, scene analysis and production QA
- `editorial-timeline-architect` — OTIO timeline interchange.
- `video-editorial-interchange` — frame-accurate OTIO and PySceneDetect handoff.
- `scene-detection-researcher` — scene boundaries, shot logs and contact sheets.
- `video-quality-assurance` — final technical/editorial release gate.
- `video-render-qa` — render runtime, dependencies and CI evidence.
- `video-render-ci-engineer` — reproducible Actions installs, caches, artifacts and SBOM.

## Toolchain, safety and licensing
- `video-toolchain-orchestrator` — route engines and profiles per shot/project.
- `video-production-license-auditor` — code/model/media license and provenance gates.
- `video-production-director` — overall coordination and project handoff.

All bundled skills remain distinct. Avoid duplicate work: route only the few skills that add value for the current job.
