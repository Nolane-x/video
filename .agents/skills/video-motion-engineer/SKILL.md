---
name: video-motion-engineer
description: Use when creating high-quality 2D motion graphics, kinetic typography, transitions, procedural particles, vector animation, HTML video or browser-based 3D for a video.
---
# Video Motion Engineer

## Engine selection
- Remotion for frame-driven React scenes, repeatable timing, captions and composition.
- HyperFrames for HTML/CSS/GSAP scenes, deterministic browser capture, lint and CLI rendering.
- GSAP for timelines, sequencing, custom easing, text splitting and morph-style transitions.
- Motion for React springs, gestures and layout movement.
- Motion Canvas for vector/explainer animation synced to narration.
- Three.js + postprocessing for geometry, depth, cameras and shader-driven atmosphere.
- PixiJS for 2D particles, sprites, filters, glow and moving graphic elements.
- Theatre Core for tightly choreographed keyframes; keep AGPL Studio out of bundles.

## Design motion before code
Define the motion grammar: anticipation, acceleration, primary action, contact/impact, follow-through, recovery, secondary motion and hold. Assign every animated object a purpose, start/end pose, coordinate system, easing family and depth/layer order. Avoid a generic all-purpose ease-in-out on every layer.

## Build discipline
1. Convert each shot to explicit frame ranges and safe areas.
2. Prototype one representative 3–5 second shot at low resolution.
3. Implement reusable tokens for spacing, typography, easing, motion duration and camera.
4. Prefer deterministic math and seeded randomness. Avoid time-based animations whose output changes across render runs.
5. Use composition-specific render concurrency and isolate GPU-only effects from CPU lanes.
6. Render a moving proof plus contact sheets; inspect frames around transitions and contact.

## Quality bar
Motion must communicate action, emotion, spatial relationships or information. A camera zoom alone is not character animation. Titles/captions must remain readable and must not obscure the acting.

## Deliverables
Engine choice, shot timing table, reusable motion helpers, source composition, low-res preview, final render metadata and motion QA notes.
