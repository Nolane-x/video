---
name: 3d-vfx-engineering
description: Use when a video shot needs camera depth, parallax, procedural geometry, lighting, materials, shader effects, compositing or optional Blender headless rendering.
---

# Procedural 3D and VFX Engineer

## Choose smallest adequate engine
- Three.js for lightweight procedural 3D, cameras, geometry, WebGL/WebGPU and browser capture.
- PixiJS for 2D sprites, particles, trails and foreground effects.
- `postprocessing` for controlled glow, blur, depth-of-field and other browser effects.
- Blender only when geometry, rigging, real shadows or camera/lighting requires it. Use the repo's optional Blender 5.2.3 installation profile.
- FFmpeg for mastering/compositing and output validation.

## Procedural scene workflow
1. Define frame size, aspect ratio, frame rate, camera/lens, depth layers and final use of the shot.
2. Block with proxy geometry and low-resolution previews. Validate silhouette, horizon, scale, ground plane and object contact.
3. Lock camera before polishing materials. Avoid detail that the final camera never reveals.
4. Use a limited material palette, motivated light sources, believable shadow direction and consistent color response.
5. Split layers/passes for subject, background, practical light, shadow, particles, foreground and text.
6. Render a short proof on CPU before increasing samples, geometry or resolution.
7. Compare moving frames around cuts/contact; do not accept a scene based on one hero still.

## Runner budget
The standard Actions runner is CPU-first. Browser 3D and Blender Eevee CPU proof are appropriate for compact scenes; large fluid simulations, volumetrics, cycles path tracing and giant photogrammetry assets are not baseline CI tasks. Do not silently rely on a GPU.

## Safety and license
Use only the repo's checksum-verifying Blender installer. Do not copy third-party add-ons, fonts, models or textures without rights. Blender is GPL-3.0-or-later; each add-on has its own license.

## Outputs
Scene source, camera/material/lighting notes, render profile, short preview, output metadata, contact sheets and VFX QA.
