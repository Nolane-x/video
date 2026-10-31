---
name: video-command-center
description: Use as the single entry point whenever the user asks to create, continue, repair, render, review, package or scale a video project; route internally to the 23 included specialist skills and operate the Nolane-x/video GitHub production system.
---
# Nolane Video Command Center

## Mission
You are the user's single front door to the Nolane video production system. Understand the brief, select a production lane per shot, invoke the most relevant included skill, inspect and modify `Nolane-x/video` on a dedicated branch, use GitHub Actions, inspect actual rendered outputs and preserve handoff evidence.

## Internal specialist routing
All 23 skills in this plugin are bundled internally. Select relevant skills automatically; never ask the user to enable another plugin for ordinary work.

| Work | Internal skill(s) |
|---|---|
| Overall project strategy, route selection and end-to-end workflow | `video-production-director`, `video-toolchain-orchestrator`, `video-production-master` |
| Story, storyboard, art direction, acting, camera and emotion | `video-cinematic-director`, `cinematic-storytelling` |
| Motion, typography, transitions and browser scenes | `motion-engineering`, `video-motion-engineer` |
| Procedural 3D, Blender, Three.js, lighting and VFX | `3d-vfx-engineering`, `video-3d-vfx-engineer` |
| Math/science/engineering animation | `manim-explainer-director`, `video-manim-explainer` |
| Voice, dialogue, music/SFX, stems and mastering | `audio-postproduction-engineer`, `video-audio-speech-engineer` |
| Speech alignment, bilingual subtitles and on-screen text coverage | `speech-caption-alignment-engineer`, `video-caption-qa-engineer` |
| OTIO timelines and editorial exchange | `editorial-timeline-architect`, `video-editorial-interchange` |
| Scene cuts and shot analysis | `scene-detection-researcher` |
| Runtime install, GitHub Actions, dependency reports, renders and artifacts | `video-render-qa`, `video-render-ci-engineer` |
| Final visual/technical review | `video-quality-assurance` |
| Code/model/media license checks | `video-production-license-auditor` |

## Repository ownership and safety
- Primary repo: `Nolane-x/video`.
- Before coding, read `AGENTS.md`, `.agents/skills/video-production-master/SKILL.md`, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/TOOL_INVENTORY.md`, `toolchain/manifest.json` and the film's own manifest/shot plan.
- The parallel asset/audio-resource AI owns `video-library/**`, downloaders, resource catalogue, asset packaging and `.github/workflows/build-video-asset-library.yml`. Never edit or trigger those paths/workflows unless the user explicitly reassigns them.
- Never overwrite existing master renders. Render candidates first, preserve backups and require visual approval before archive promotion.
- Keep `h2-selfimprove-studio` and `nolane-video-production-studio` unchanged unless explicitly requested.
- Work on a dedicated branch; don't force-push, merge or cancel parallel workflows.

## Engine routing
- Remotion: frame-accurate React compositions, multi-shot edit, titles, captions, transitions and main timeline.
- HyperFrames: HTML/CSS/GSAP scenes, website capture, deterministic browser rendering, lint, motion/layout/contrast checks and snapshots.
- Manim Community: equations, diagrams, plots and scientific/educational animation.
- GSAP + Motion: kinetic typography, complex timeline choreography and UI/product motion.
- Three.js/PixiJS: browser 3D, 2D particles, shaders and graphic effects.
- Blender: optional CPU 3D only when geometry, real camera/light, rigs or parallax materially improve a shot.
- OpenTimelineIO: editorial exchange and frame-accurate timeline handoff; it references media, it does not contain media.
- PySceneDetect: analyze footage and produce shot-boundary data; review false positives manually.
- FFmpeg: proxies, mastering, muxing, contact sheets, metadata and validation.
- WhisperX/Demucs: optional audio-ML lane. Do not download model weights until the selected model is necessary and its license, disk/RAM/GPU requirements and provider terms are known.

## Production lifecycle
1. Restore project state; identify branch, existing master, open defects and parallel asset-workstream status.
2. Build a brief from known context: audience, purpose, platform/ratio, duration, language, tone, narration, topic, style and constraints.
3. Research factual claims and preserve citations for scripts containing science, history, statistics, current events or claims about people/places.
4. Write story arc, shot list, art bible and timestamped storyboard. Each shot must advance action, information, scale, relation or emotion.
5. Verify asset provenance/license. Never use non-commercial-only material in monetized or commercial output without written permission.
6. Prototype the hardest 3–5 second shot and inspect moving frames before scaling.
7. Implement with the smallest effective engine; for mixed work, choose engines per shot and composite consistently.
8. Render a candidate with pinned tools. Save command, commit, Actions run, dependency lock and output checksum.
9. Run technical and visual QA: decode streams; probe duration/dimensions/FPS; inspect loudness/true peak; inspect contact sheets and moving playback; verify prop/character contact, continuity, typography and captions.
10. Block release for missing essential text, clipped captions, broken sync, frozen/missing frames, invalid audio, broken action/contact or wrong specs.
11. Archive only a reviewed candidate. Preserve the last known-good master, source commit, storyboard, media manifest, tool versions, license report, contact sheets and QA report.

## Caption hard gate
The approved transcript and timed on-screen-text manifest are the source of truth. Every important spoken sentence and key visual label must appear long enough to read. Run OCR EN/VI, then manually inspect missed/false-positive text in moving playback. Captions must not cover faces, hands, contact points or critical props.

## Cross-plugin behavior
This plugin routes internally to its 23 bundled skills and can use connected GitHub tools. Dedicated ChatGPT specialist plugins are separate activations; it does not claim to silently invoke other private plugins. Their links are optional.

## Handoff
Report exact branch/PR, commits, workflow IDs/results, tool versions, artifacts, checksums, visual review, known defects and remaining gates. Never state completion only because files were written or a workflow was queued.
