---
name: motion-graphics-production
description: Reference-led, code-driven motion design production for kinetic typography, launch films, UI showcases, poster reels, logo animation and graphic 3D. Use this for motion-design genres; do not route it through H2 narrative-film rules.
---

# Motion Graphics Production

## Scope

This is a specialist genre skill in the multi-genre Nolane Video engine. It is not the global production master and it is not the H2 SelfImprove skill. Choose it for kinetic typography, product / launch motion, poster reels, graphic UI showcases, logo animation and code-driven motion design.

## Upstream practice

Informed by the MIT-licensed [Mort1d/motion-graphics-skills](https://github.com/Mort1d/motion-graphics-skills), version 1.4.1. The upstream project owns its own source and implementation. This skill records our adapted production contract; it does not vendor the upstream scripts.

## Reference-first method

1. Probe the source: exact duration, dimensions, frame rate, codec, audio properties and shot boundaries.
2. Sample the entire reference at 1 fps or faster; create a separate 2 fps sheet for rapid cuts.
3. Write a shot map with source time windows, focal hierarchy, palette, type, motion, transitions and sound beats.
4. Separate measured observation from interpretation. Never invent assets, text, fonts or motion that cannot be seen.
5. Rebuild motion grammar and timing with newly authored assets; do not copy source frames, audio or unlicensed media.
6. Build four key stills first (opening, hero title, densest poster frame, ending) and assess composition before filling all transitions.
7. Create scenes in modular components. Every parameter is deterministic from frame/time; no random state or wall-clock animation.
8. Review the complete moving render, not only a poster frame or green CI check.

## Motion craft contract

- The opening moves from frame 0; avoid dead air before the first visual read.
- One primary read at a time. Keep supporting labels subordinate and never cover the hero.
- Use a readable scale hierarchy. At 1080p, hero words should generally dominate at roughly 150–260 px; supporting labels should remain comfortably readable (normally 28 px or larger).
- Enter with intent: out-cubic / out-expo for typography and cards; use a spring only for UI chips, controls and physical-feeling objects. Do not bounce large editorial type.
- Exit with acceleration, a mask, wipe, whip, match cut or perspective push. Avoid generic cross-fades on every scene.
- Use stagger for groups, but preserve reading order. Secondary motion can continue during a hold; the primary message should not move so much that it cannot be read.
- Fast motion should communicate travel and direction. Use motion blur only where the object actually travels; avoid blurring text during its reading window.
- Keep the frame alive through restrained parallax, background motion and camera drift. Avoid replacing purposeful animation with a permanent HUD.
- Use a consistent spatial logic for perspective, shadows and layer depth. CSS 3D is suitable for simple geometric forms; move to Blender only when real geometry, rigging, complex lighting or shadows justify it.
- Cut to the beat where it helps, not on every beat. The score and sound effects must be authored for the timeline; visible taps, card slams and transitions need deliberate audio decisions.
- Give all important type enough dwell time. The end card should be held for at least 2.5 seconds when the length permits.

## Technical architecture

- Remotion is preferred for frame-deterministic typography, SVG, UI, timelines and 2D/2.5D composition.
- Use Three.js / PixiJS only when their real-time scene capability adds value; do not add engines without a shot-level reason.
- Use Blender for shots requiring true 3D scene authoring, rigging, real lighting or simulation.
- Use FFmpeg / ffprobe for mastering, metadata, frame sampling, audio loudness and checksum validation.
- Run renders through GitHub Actions. Do not silently depend on a local GPU, local desktop application, API key or binary file absent from the workflow.
- Keep reference media out of public repo history unless its licence explicitly allows this exact redistribution.

## Quality gates

1. Composition and shot map are consistent in duration / frame count.
2. Text spelling, position, clipping, safe margins and actual reading time are checked.
3. Transitions have continuous motion direction and do not expose blank frames.
4. 3D elements keep believable perspective, shadows, face orientation and timing.
5. Audio contains no clipping, pops, abrupt truncation or unintentional silence; loudness / true peak are measured.
6. All nine shot groups are visible in contact sheets; rapid shots additionally receive 2 fps sampling.
7. Inspect moving clips at each shot boundary and on all signature motions.
8. Preserve the previous known-good project outputs. Technical pass is not artistic approval.
9. Publish source commit, workflow run, checksums, contact sheets, metadata and a concise QA ledger.

## Handoff

Record the chosen engine, exact workflow run, artifact name, output metadata, checksum, QA defects and remaining work. Use the source shot map and skill, not chat memory alone, to resume the project.
