---
name: video-manim-explainer
description: Use when creating mathematically rigorous scientific, engineering or educational animations and visual explanations with Manim Community Edition.
---
# Manim Explainer Engineer

- Use the pinned optional Manim CE profile in `toolchain/python/manim/requirements.txt`; do not mix its dependencies into the Node core runtime.
- Verify concepts, equations, dimensions, units, graph scales and worked examples before animation.
- Storyboard concept progression as question → intuition → diagram → derivation → application → recap.
- Use MathTex only when the LaTeX system is installed; otherwise use a tested text/vector fallback and disclose the limitation.
- Animate mathematical transformations with explicit object state and frame timing; do not use meaningless decorative movement.
- Render a low-quality sample, inspect formulas and graph labels at delivery resolution, and then render final.
- Deliver Manim source, narration/caption timing, command, pinned version, MP4 and ffprobe evidence.
