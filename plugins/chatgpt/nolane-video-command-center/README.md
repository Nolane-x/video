# Nolane Video Command Center v0.4.0

**One private ChatGPT plugin for the normal Nolane video workflow.** It now bundles 23 internal skills across story/direction, cinematography, animation, Remotion/HyperFrames, Blender/Three.js, Manim, audio/speech, captions, scene analysis, editorial exchange, CI and licensing.

## How to use
1. Start with this plugin and describe the video goal, audience, format and constraints.
2. The Command Center selects a small internal skill set for the job; it does not activate every tool on every request.
3. It can use connected GitHub tools to inspect and change `Nolane-x/video` on a dedicated branch, then follow Actions evidence and render artifacts.
4. Dedicated specialist plugins remain optional direct entry points. ChatGPT does not guarantee invisible plugin-to-plugin invocation, so the Command Center carries the core workflows it needs internally.

## Repository safety
- The parallel asset agent owns `video-library/**`, asset downloaders/catalogue and the asset-library workflow. Do not edit or trigger those paths while that workstream is active.
- Do not overwrite existing master videos; create a candidate, verify it and request review before promotion.
- A successful build/render is not artistic approval. Full playback, motion/contact, captions, audio and legal provenance are separate gates.

## Toolchain profiles
- Core: Node 24, Remotion 4.0.538, HyperFrames, GSAP/Motion, Three.js/PixiJS, Playwright Chromium, FFmpeg/ffprobe and Tesseract EN/VI.
- Editorial: OpenTimelineIO + PySceneDetect headless.
- Manim: separate Manim CE + Cairo/Pango/TeX profile.
- Audio ML: optional WhisperX/Demucs code profile; model weights and credentials are not bundled.
- Blender 5.2.3: official archive, checksum-verified, installed on demand for headless 3D proof.

See `SKILL-CATALOG.md` for all internal skills and `references/PLUGIN-REGISTRY.md` for optional specialist plugins.
