---
name: video-production-master
description: End-to-end workflow for cinematic code-driven YouTube animation: story, references, H2 Canvas, Remotion, Blender, Krita, sound design, rendering, quality gates, archival and AI handoff.
---

# Video Production Master

Persistent production memory for AI sessions in `Nolane-x/video`. This is a gated workflow, not a promise of automatic quality.

## ChatGPT Plugin Creator integration

The active private ChatGPT plugin [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) is **v1.1.0**, current release `pluginrel_6ade248942988191a57ff1059c818720`, confirmed by Plugin Creator on 2026-10-25. It preserves the native H2 rig, `dem`/`doodle` packs, renderer, scripts and audio helpers while adding the production pipeline, motion/contact QA gates and persistent handoff. The exact active release and CI evidence are documented in `docs/CHATGPT_PLUGIN.md`. The GitHub source mirror remains the v1.0.2 base; its v1.1.0 overlay is separate.

## ChatGPT H2 plugin and mirrored kit

The active private `h2-selfimprove-studio` ChatGPT plugin is available at https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 (v1.1.0, release `pluginrel_6ade248942988191a57ff1059c818720`). Its 51-file source mirror under `integrations/h2-selfimprove-studio/` is the v1.0.2 base snapshot, while `integrations/h2-selfimprove-studio-production-overlay/` records the production workflow enhancement used for v1.1.0. Read `docs/CHATGPT_PLUGIN.md` and `integrations/h2-selfimprove-studio/MIRROR-NOTES.md`. Keep the native H2 kit distinct from the repo's Remotion renderer and from the full upstream Blender/Krita applications.

## Read before acting
Read `AGENTS.md`, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/TOOL_INVENTORY.md`, `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, `video-library/README.md`, `video-library/previous-works-catalog.json`, `video-library/reference-clips.json`, the per-film manifest/QA, Remotion README, character bible and live shot plan. Inspect current HEAD, recent commits, Actions, logs and artifacts. The canonical H2 master MP4 is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`; the original source and source-v2 scene-fixes ZIPs are published at the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). Source-v2 is a candidate only until a new H2 render and full moving-picture QA pass. Then read these references: [visual language](references/visual-language.md), [engine selection](references/engine-selection.md), [production workflow](references/production-workflow.md), [animation QA](references/animation-qa.md), [audio/delivery](references/audio-delivery.md), [state restoration](references/state-restoration.md), [reusable prompts](references/reusable-prompts.md).

## Product target
Make a short film, not a motion-graphics slideshow. Use a simple symbolic stick figure (near-black round head, pale rim, readable face, colored shirt, slim dark limbs and shoes) inside a richly staged world. Distinct locations, architectural detail, warm practical light, plum/charcoal shadows, foreground/background depth, purposeful camera movement, visible acting and prop contact are central to the look.

User references:
- Ifverse Tales: https://www.youtube.com/@IfverseTales
- Day One Films: https://www.youtube.com/@dayonefilmsofficial
- Supplied examples: “The Words You Never Forgot” (https://www.youtube.com/watch?v=qyFUAlGMxSE) and “What If You Were a Mentalist?” (https://www.youtube.com/watch?v=XexSnQTMMhw). See `video-library/reference-clips.json` for source provenance and review checklist.
Open the source and actually watch it before recording timestamped observations; the standalone reference MP4s were not found in the current workspace/Library snapshot. Study the high-level visual grammar. Do not copy frames, characters, dialogue, scripts or music.

## Hard production gates
1. **Repository truth:** inspect code, storyboard, assets, commits, CI and storage status.
2. **Brief:** audience, platform, ratio, duration, language, voice-over policy, emotional outcome and constraints. Don't ask again for known details.
3. **Reference breakdown:** sample the whole video, not thumbnails alone. Record framing, angle, camera, characters, action, emotion, set, palette/light, props/contact, text, transitions and sound beats. Separate observation from inference.
4. **Story design:** every shot changes place, action, information, relationship, emotional state, scale or visual metaphor. Use meaningful holds, not filler.
5. **Art direction:** lock character proportions, palette, outlines, environment, light logic, camera and typography before detailed animation.
6. **Storyboard source of truth:** prefer `public/story/shots.json` in the Remotion project. H2 pack scenes may use `tpl + args`; inspect actual H2 schema, never invent fields.
7. **Assets:** document source/license. Use established H2 rig when suitable; Krita for authored art; Blender only when 2.5D/3D helps; code for repeatable shapes.
8. **Blocking:** prove scale, ground line, reach, layer order and camera-safe areas before detail.
9. **Acting:** anticipation → action → contact/impact → follow-through → recovery. Animate props with the actor. A camera move is not an action.
10. **Preview:** create a per-shot contact sheet, overview, moving proof of hard actions, and samples before/at/after contact.
11. **Audio:** music/SFX follow the story; preserve intentional silence; no synthetic voice-over unless requested.
12. **Render:** record exact engine, command, CI run and source commit. Use a temporary master and preserve last known-good output.
13. **QA:** validate shot variety, contact, continuity, crops, transitions, audio, duration, ratio, FPS and codecs. P0/P1 defects block release or must be disclosed.
14. **Delivery:** MP4, source/reproducible commit, manifest, contact sheets, QA, audio measurements, metadata and known limits.
15. **Truthfulness:** never say H2/Remotion/Blender ran unless logs support that exact claim.
16. **State transfer:** update state, handoff and film manifest at end of every session.

## Engine architecture
- **H2 Studio / Canvas rig / pack dem:** primary for established H2 work when the full source and packaged skill are available. Inspect engine entrypoint, `packs/dem`, templates, shot schema and required sheet/audio workflow.
- **Remotion:** frame-based timeline, sequences, type, 2D layers, compositing and CI render. Source lives at `video-projects/remotion`; it is not the H2 renderer.
- **Blender:** selected 2.5D/3D shots needing depth, camera, rigging or lighting. Start with proxies/Eevee.
- **Krita:** authored character/expression sheets, props, textures and paintovers.
- **FFmpeg/ffprobe:** mastering, frame extraction, contact sheets and validation.
- **Python audio:** existing generators under `video-projects/remotion/h2-audio` must be run to create WAVs; source files are not final audio assets.

## Acceptance
Accept only when the narrative progresses visually, backgrounds/shot sizes vary, actions read in silhouette, hand/foot contacts are believable, type supports action, sound aligns with beats, silence is intentional, contact sheets and moving proofs are reviewed, metadata matches the brief, and a new AI can reproduce the pipeline without relying on old chat history.
