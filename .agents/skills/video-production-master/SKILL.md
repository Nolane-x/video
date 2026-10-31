---
name: video-production-master
description: Genre-aware end-to-end video production across story, documentary research, explainers, cinematography, animation, editing, audio, rendering, QA, archival and AI handoff.
---

# Video Production Master

Persistent production memory for AI sessions in `Nolane-x/video`. This is a gated workflow, not a promise of automatic quality.

## Active multi-engine command center

The active private [Nolane Video Command Center](https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc) is **v0.7.9**, release `pluginrel_6ae5b448d6948191a011fc39d2ec282d`. It contains 29 internal skills and routes to a registry of 37 separately activated specialist plugins. Read `plugins/chatgpt/nolane-video-command-center/SKILL-CATALOG.md` and `plugins/chatgpt/nolane-video-command-center/references/PLUGIN-REGISTRY.md` for the exact responsibilities and links.

The separate [Nolane Video Production Studio](https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd) v0.4.0 contains a broader 32-skill production library. [H2 SelfImprove Studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) v1.1.0 is a specialised H2 renderer/workflow. They are independent private plugins; the host/user controls activation. Never claim hidden cross-plugin invocation.

## ChatGPT Plugin Creator integration

The active private ChatGPT plugin [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) is **v1.1.0**, current release `pluginrel_6ade248942988191a57ff1059c818720`, confirmed by Plugin Creator on 2026-10-25. It preserves the native H2 rig, `dem`/`doodle` packs, renderer, scripts and audio helpers while adding the production pipeline, motion/contact QA gates and persistent handoff. The exact active release and CI evidence are documented in `docs/CHATGPT_PLUGIN.md`. The GitHub source mirror remains the v1.0.2 base; its v1.1.0 overlay is separate.

## ChatGPT H2 plugin and mirrored kit

The active private `h2-selfimprove-studio` ChatGPT plugin is available at https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 (v1.1.0, release `pluginrel_6ade248942988191a57ff1059c818720`). Its 51-file source mirror under `integrations/h2-selfimprove-studio/` is the v1.0.2 base snapshot, while `integrations/h2-selfimprove-studio-production-overlay/` records the production workflow enhancement used for v1.1.0. Read `docs/CHATGPT_PLUGIN.md` and `integrations/h2-selfimprove-studio/MIRROR-NOTES.md`. Keep the native H2 kit distinct from the repo's Remotion renderer and from the full upstream Blender/Krita applications.

## Read before acting
Read `AGENTS.md`, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/TOOL_INVENTORY.md`, `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, `video-library/README.md`, `video-library/previous-works-catalog.json`, `video-library/reference-clips.json`, the per-film manifest/QA, Remotion README, character bible and live shot plan. Inspect current HEAD, recent commits, Actions, logs and artifacts. The canonical H2 master MP4 is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`; the original source and source-v2 scene-fixes ZIPs are published at the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). Source-v2 has passed technical rendering, but remains non-canonical until full-motion review. Source-v3 is the focused shoe-tying correction: inspect `video-library/one-more-scroll/h2-source-v3-render-request.json`, `tools/video/patch_h2_shoelace_scene.py`, preview workflow `.github/workflows/preview-h2-source-v3-shoelace.yml`, and full-render workflow `.github/workflows/verify-h2-source-v3.yml`; current run/status is recorded in `docs/STATE.md` and `video-library/one-more-scroll/h2-source-release.json`. Require the full render's technical/audio gates and a complete moving-picture review before any promotion. Then read these references: [visual language](references/visual-language.md), [engine selection](references/engine-selection.md), [production workflow](references/production-workflow.md), [animation QA](references/animation-qa.md), [audio/delivery](references/audio-delivery.md), [state restoration](references/state-restoration.md), [reusable prompts](references/reusable-prompts.md).

## Genre-aware production routing

Use the versioned [Genre and Production Routing Matrix](../../docs/GENRE_ROUTING_MATRIX.md) as the full format/engine/acceptance reference. The checklist below is the working summary; the matrix records the deeper routing and evidence contract.

Choose the genre, delivery format and production grammar before choosing an engine. Do not assume every request is a short cinematic animation or inherits the visual style of an earlier project.

At the start of each task, resolve from the brief and existing project state:
- Genre and purpose: documentary, science/math explainer, narrative animation, product demo, tutorial/screen recording, interview, music video, short-form social, advertisement or hybrid.
- Audience, platform, runtime, aspect ratio, language, narration policy, caption/subtitle requirements and call to action.
- The information contract: factual claims and citations, exact product/UI behavior, equations/data, scripted dialogue, or emotional story beats.
- Visual grammar: live-action, documentary footage, authored 2D, 3D, motion graphics, screen capture, mixed media or the user's established series style.
- Asset provenance, licenses, privacy, model/API costs, hardware and delivery constraints.

Route only the needed stages:
- Documentary/science: research and fact-check claims first; keep a claim/source ledger; use Manim or data-visualization skills when mathematical or quantitative accuracy benefits.
- Product/software demos: use authorized browser capture and real UI state; never fabricate product behavior or imply a mockup is a live product.
- Narration/interview: separate script decisions, transcript observations, timing, subtitle generation, audio cleanup and mastering. Verify exact text and speech coverage.
- Narrative/2D/3D animation: storyboard, art bible, blocking, acting, contact/motion proofs and engine-specific QA.
- Short-form/social: front-load the hook and enforce mobile-safe typography, pacing and platform-specific cutdowns.
- Hybrid/AI media: select media tools per shot, preserve editable text and deterministic finishing, and independently audit generated-asset provenance/rights.

Use the Command Center's internal skills first. Switch explicitly to an independently activated specialist plugin only when its tool-specific depth materially helps. Do not install every engine, download model weights, or invoke paid services by default.

The established cinematic stick-figure/H2 style below is a **conditional project profile**, not a universal style rule. Preserve it when continuing that series or when the user explicitly requests it; otherwise follow the new brief's visual grammar.

## Established cinematic/H2 visual profile (conditional)
When this profile applies, make a short film rather than a motion-graphics slideshow. Use a simple symbolic stick figure (near-black round head, pale rim, readable face, colored shirt, slim dark limbs and shoes) inside a richly staged world. Distinct locations, architectural detail, warm practical light, plum/charcoal shadows, foreground/background depth, purposeful camera movement, visible acting and prop contact are central to this particular series. Do not impose these character, palette, duration or voice-over choices on unrelated genres.

User references:
- Ifverse Tales: https://www.youtube.com/@IfverseTales
- Day One Films: https://www.youtube.com/@dayonefilmsofficial
- Supplied examples: “The Words You Never Forgot” (https://www.youtube.com/watch?v=qyFUAlGMxSE) and “What If You Were a Mentalist?” (https://www.youtube.com/watch?v=XexSnQTMMhw). See `video-library/reference-clips.json` for source provenance and review checklist.
Open the source and actually watch it before recording timestamped observations; the standalone reference MP4s were not found in the current workspace/Library snapshot. Study the high-level visual grammar. Do not copy frames, characters, dialogue, scripts or music.

## Hard production gates

0. **Editorial readiness before render:** complete the audience/platform/language/aspect/voice-policy/hook/promise/payoff brief. Run `python tools/video/evaluate_editorial_plan.py <shot-plan.json> --output <report.json> --strict`; a blocked plan must be revised before rendering. Do not use uniform shot timing or a dominant scene template by default. Every shot needs a story function and explicit framing/angle/camera/composition; physical contacts need an action/contact/follow-through proof. A plan-ready report permits only blocking/animatic and preview, never final release.
0.5. **Blocking preview before full render:** after editorial preflight passes, render the selected motion-proof clips with `tools/video/render_blocking_preview.py`. The full render is prohibited until `tools/video/validate_preview_approval.py` confirms the exact preview-spec and clip-bundle hashes, all selected segments reviewed, explicit reviewer identity/timestamp and concrete notes. Any storyboard/renderer change invalidates approval.
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
    - For a problematic H2 action, use a focused 3–6 second preview before a full render. Preserve the previous source archive and master; pin the patch commit and preview run; then reapply the exact same patch to an immutable source extraction for the full candidate. A green CI status proves technical processing, not artistic approval.
11. **Audio:** music/SFX follow the story; preserve intentional silence; no synthetic voice-over unless requested.
12. **Render:** record exact engine, command, CI run and source commit. Use a temporary master and preserve last known-good output.
13. **QA:** validate shot variety, contact, continuity, crops, transitions, audio, duration, ratio, FPS and codecs. P0/P1 defects block release or must be disclosed.
14. **Delivery:** MP4, source/reproducible commit, manifest, contact sheets, QA, audio measurements, metadata and known limits.
15. **Truthfulness:** never say H2/Remotion/Blender ran unless logs support that exact claim. A 100% text OCR score or technical render pass does not demonstrate story quality, visual variety, pacing, sound design or emotional impact.
16. **State transfer:** update state, handoff and film manifest at end of every session.

## Engine architecture
- **H2 Studio / Canvas rig / pack dem:** primary for established H2 work when the full source and packaged skill are available. Inspect engine entrypoint, `packs/dem`, templates, shot schema and required sheet/audio workflow.
- **Remotion:** frame-based timeline, sequences, type, 2D layers, compositing and CI render. Source lives at `video-projects/remotion`; it is not the H2 renderer.
- **Blender:** selected 2.5D/3D shots needing depth, camera, rigging or lighting. Start with proxies/Eevee.
- **HyperFrames:** HTML/CSS/GSAP scenes, beat-based motion, deterministic browser capture and snapshot QA.
- **Manim:** equations, geometry, graphs and mathematically precise science explainers; verify the underlying facts/formulas before rendering.
- **Three.js / PixiJS:** browser-based 3D, 2D graphics, particles, shaders and lightweight effects where they add value.
- **Krita:** authored 2D character sheets, props, textures and paintovers.
- **OpenTimelineIO:** editorial timeline interchange, not a video container; media remains externally referenced.
- **PySceneDetect:** candidate cut boundaries and logs; a human/editor decides the final cut.
- **Playwright / OCR:** authorized browser capture and timed on-screen-text/caption checks; OCR is evidence, not a substitute for visual review.
- **FFmpeg/ffprobe:** mastering, frame extraction, contact sheets and technical validation.
- **WhisperX / Demucs:** optional manual-only speech alignment and source separation; validate language/model terms and do not download weights by default.
- **Python audio:** existing generators under `video-projects/remotion/h2-audio` must be run to create WAVs; source files are not final audio assets.

## Acceptance
Accept only when the deliverable fulfills its brief: information is complete and accurate, visual grammar is coherent, pacing serves the audience, text/captions are readable and complete where required, audio is intelligible and measured, asset rights are documented, technical metadata matches the target, and the actual moving picture/audio has been reviewed. For the established stick-figure profile, additionally verify readable silhouettes, believable hand/foot contact and actor/prop follow-through. A new AI must be able to reproduce the pipeline from the repository state without relying on old chat history.
