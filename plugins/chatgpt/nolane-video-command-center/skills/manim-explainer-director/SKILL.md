---
name: manim-explainer-director
description: Use when creating mathematical, scientific, engineering, educational or diagram-led animation with Manim Community Edition.
---
# Manim Explainer Director

## Mission
Turn a concept into a mathematically correct, visually understandable, camera-aware animation. Use Manim CE 0.22.1 as the pinned optional renderer; never assume the package is present until the environment check passes.

## Preproduction
1. Identify the learner, prior knowledge, target misconception, language, runtime, aspect ratio and final learning outcome.
2. Reduce the explanation to one conceptual spine: question → intuition → representation → derivation/demonstration → application → recap.
3. Confirm equations, units, coordinate systems, diagrams and numerical examples before animating. For facts or current claims, preserve sources beside the scene.
4. Storyboard each scene with a visual purpose, narration segment, start/end state and intended camera crop.

## Scene engineering
- Prefer explicit mobject state and deterministic `Transform`, `ReplacementTransform`, `AnimationGroup`, `LaggedStart` and `Succession` choreography.
- Introduce an object before referring to it; preserve spatial continuity when changing axes or camera position.
- Use vector diagrams and mathematically meaningful motion. Never animate a graph/number merely for decoration.
- Keep equations readable at the final resolution; use line breaks, isolated equations and controlled transforms rather than shrinking everything.
- Use `MathTex` only after TeX/LaTeX system dependencies are available; fail clearly if compilation is unavailable.
- Use `ThreeDScene` only where depth clarifies the concept. Default to 2D for graph, algebra and geometry explanations.
- Use a custom color and typography system with contrast and safe margins. Avoid a generic slideshow of centered titles.

## Narration and timing
- Keep narration phrases aligned to scene beats and equation reveals.
- Leave pauses after a non-obvious transform or result.
- Render a low-quality animatic first; then a representative full-resolution segment; finally the full timeline.
- Captions and key terms are part of the composition, not an afterthought.

## QA
- Validate math, dimensions, units and labels with an independent check.
- Render representative sections and inspect the actual frames; verify no clipped formulas, overlapping labels, axes running off-screen or text that is too small.
- Check frame rate, duration, audio synchronization and final codec with FFmpeg/ffprobe.
- Preserve source, exact Manim version, requirements lock, render command and output checksum.

## Deliverables
Concept outline, scene map, Manim Python source, narration/caption timing, low-quality proof, final MP4, technical metadata and visual QA notes.
