---
name: motion-engineering
description: Use when designing or implementing procedural 2D/3D motion, transitions, kinetic typography, particles, browser scenes or deterministic video compositions.
---

# Motion Engineering Director

Create motion that serves story and information, not motion for its own sake. Use the repository's pinned dependencies and preserve frame determinism.

## Engine routing
- Remotion: frame-accurate React composition, typography, multi-shot timeline, captions and final edit.
- HyperFrames: HTML/CSS/GSAP scenes, timeline capture, lint, snapshots and CLI rendering.
- Motion Canvas: optional vector/explainer motion only when a project-specific compatible runtime is supplied; it is not installed in the core runner.
- GSAP: custom timelines, advanced easing, stagger, split text and complex sequences.
- Motion: React spring/physics transitions and layout movement.
- Three.js + postprocessing: camera, geometry, 3D particles, shader effects and DOF.
- PixiJS: efficient 2D particles, glows, trails, sprites and layered effects.
- Theatre Core: reusable keyframe choreography; keep AGPL Studio out of production runtime.

## Workflow
1. Read the brief, storyboard schema, art direction and timing rules.
2. For every shot define frame range, dominant action, motion arc, coordinate space, layer order, camera path, safe text area and transition.
3. Build reusable tokens for durations, easing curves, spacing, scale, stagger, camera movement and typography hierarchy.
4. Animate anticipation → action → contact → follow-through → recovery. Add secondary motion only after the main action reads.
5. Keep animation deterministic: derive movement from frame, seeded randomness and fixed shot data; avoid wall-clock timing.
6. Render a 3–5 second representative moving proof and contact sheet before expanding to full video.
7. Inspect at actual frame rate. Still images cannot prove continuous motion.

## Quality bar
- Vary rhythm: short accents, medium transitions, slow reveals and intentional holds.
- Avoid stacking glow/glitch/bloom indiscriminately.
- Camera zoom is not a substitute for character or prop animation.
- Captions must not cover faces, hands, props or contact points.
- Browser effects must degrade gracefully on CPU-only runners; no hidden GPU requirement.

## Outputs
Engine decision table, per-shot frame/motion plan, reusable helpers/components, render command, preview, contact sheet and QA evidence.
