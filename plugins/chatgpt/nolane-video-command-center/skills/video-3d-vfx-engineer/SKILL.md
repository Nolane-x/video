---
name: video-3d-vfx-engineer
description: Use when a shot needs procedural 3D geometry, camera parallax, physical depth, lighting, environment modelling, shader effects, compositing or Blender/Three.js.
---
# 3D and VFX Engineer

## Select the smallest sufficient engine
- Three.js for lightweight procedural 3D, camera moves, geometry and browser-rendered scene layers.
- PixiJS for 2D foreground particles and compositing where full 3D is unnecessary.
- Blender 5.2.3 only for shots that need geometry, real light/shadow, rigs or depth that browser geometry cannot express cleanly.
- FFmpeg for final compositing. Keep OpenFX/Natron/OpenUSD/OpenVDB/OCIO native builds out of the default runner unless a shot requires them.

## Blender CPU workflow
1. Start with a proxy scene and 3–5 second proof.
2. Use headless blender --background; don't assume a GPU exists.
3. Specify exact scene dimensions, frame rate, frame range, camera, render engine and output format.
4. Cache geometry/simulation only when reusable and affordable; prefer deterministic low-poly/procedural scenes for CI.
5. Download Blender only through toolchain/scripts/install-blender.sh, which verifies the official checksum.

## VFX and compositing
Separate background, subject, shadow, practical light, particles, foreground props and type into passes/layers. Preserve alpha and color-space metadata. Review composited action/contact at motion frames.

## License
Blender is GPL-3.0-or-later. Do not copy proprietary add-ons, fonts, textures or models into the repository without redistribution rights.

## Deliverables
Scene file/script, provenance, camera/light/material notes, render settings, low-res moving proof, composite preview and QA report.
