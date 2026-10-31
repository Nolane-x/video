---
name: motion-engineering
description: Use when designing or implementing procedural 2D/3D motion, transitions, kinetic typography, particles, browser scenes or deterministic video compositions.
---

# Motion Engineering Director

## Purpose
Create motion that serves story and information, not motion for its own sake. Use the repo's pinned dependencies and preserve frame determinism.

## Engine routing
- Remotion: frame-accurate React composition, typography, multi-shot timeline, captions and final edit.
- HyperFrames: HTML/CSS/GSAP scenes, timeline capture, lint, snapshots and CLI rendering.
- Motion Canvas: vector/explainer motion and narration-synchronised scenes.
- GSAP: custom timelines, advanced easing, stagger, split text and complex sequences.
- Motion: React spring/physics transitions and layout movement.
- Three.js + postprocessing: camera, geometry, particles in 3D, shader effects and DOF.
- PixiJS: efficient 2D particles, glows, trails, sprites and layered effects.
- Theatre Core: reusable keyframe choreography. Use Core in production; keep the AGPL Studio out of shipped runtime.

## Workflow
1. Read the video brief, storyboard schema, art direction and timing rules.
2. For every shot, define a frame range, dominant action, motion arc, coordinate space, layer order, camera path, safe text area and transition.
3. Build a reusable motion-token set: durations, easing curves, spacing, scale, stagger, camera movement and text hierarchy.
4. Animate anticipation → action → contact → follow-through → recovery. Add secondary motion only after the main action reads.
5. Keep animations deterministic: derive all movement from `frame`, seeded randomness and fixed shot data; avoid wall-clock timing.
6. Render a 3–5 second representative moving proof and an overview/contact sheet before expanding to the full video.
7. Check motion at the actual rendered frame rate. A still image cannot prove continuous motion.

## Quality bar
- Use varied rhythms: short accents, medium transitions, slow reveals and intentional holds.
- Avoid stacking bloom/glow/glitch on every scene; keep depth and contrast purposeful.
- Never use camera zoom as a substitute for character/prop animation.
- Captions and key words must remain legible and must not cover faces, hands, props or contact points.
- Browser effects must degrade gracefully on CPU-only runner; no hidden GPU requirement.

## Outputs
Engine decision table, per-shot frame/motion plan, reusable helpers/components, render command, preview, contact sheet and QA evidence.
