# Nolane Video Actions Toolchain

The repository owns exact pins, installers, profiles, skills, tests and workflows. GitHub Actions installs into isolated runner storage and caches downloads. It does not commit node_modules, browser binaries, model weights or desktop installers into normal Git history.

## Profiles

| Profile | Contents | Trigger | Hardware |
|---|---|---|---|
| Core | Node 24, Remotion, HyperFrames, GSAP, Motion, Three.js, PixiJS, Theatre Core, SVG/D3, resvg, Sharp, Playwright Chromium, FFmpeg, Tesseract EN/VI | PR/push smoke | CPU |
| Editorial | OpenTimelineIO 0.18.1 and PySceneDetect headless 0.7.2 | PR and manual proof | CPU |
| Manim | Manim CE 0.22.1, Cairo/Pango and TeX | PR proof on Manim profile/source changes; manually dispatchable | CPU |
| Audio ML | WhisperX 3.8.6 and Demucs 4.1.0 | Manual install/import only | CPU import; model inference may need GPU |
| Blender | Blender 5.2.3 official Linux x64 archive verified against official SHA-256, EGL/Mesa software GL | PR proof on Blender/script/installer changes; manually dispatchable | CPU |

The existing Remotion film remains pinned at 4.0.538. Optional Python profiles have separate exact direct requirements and are not installed into the Node core environment.

## Workflows

1. **Video toolchain smoke** validates manifests, plugin/skill contracts and the committed npm lockfile; installs exactly from that lockfile with `npm ci`, typechecks the existing Remotion app, tests CLIs/modules and uploads checksums, license inventory, SBOM and runtime-version evidence.
2. **HyperFrames render proof** scaffolds a sample, runs doctor/lint/browser/layout/motion/contrast checks, renders an MP4 and uploads snapshots.
3. **Editorial interchange proof** generates synthetic two-scene media, detects the hard cut and round-trips a frame-accurate OTIO timeline. It never reads the separate asset library.
4. **Manim proof** runs for PR changes to the Manim profile, smoke scene or skill; installs Cairo/Pango/TeX and renders a short equations/graph scene.
5. **Audio ML runtime** is manual-only; installs/imports WhisperX/Demucs code but does not fetch models or access credentials.
6. **Blender proof** runs for PR changes to Blender scripts/installer/profile; downloads the official binary on demand, verifies SHA-256, installs EGL/Mesa for software rendering, then renders a five-second 640×360 proof.

## Engine routing

- Remotion: primary React timeline, captions, typography, transitions and compositing.
- HyperFrames: HTML/CSS/GSAP, deterministic browser capture, lint/check/snapshots and render.
- GSAP/Motion: kinetic typography, transition choreography and spring motion.
- Three.js/PixiJS: browser 3D, particles, depth, filters and effects.
- Manim: mathematical/scientific/engineering explainers.
- OpenTimelineIO: timeline interchange data, not a media container.
- PySceneDetect: shot/cut candidates; humans review false positives.
- WhisperX: speech recognition/alignment; validate Vietnamese aligner support before claiming word precision.
- Demucs: optional source separation; inspect artefacts and keep model-weight terms separate from code license.
- Blender: optional 3D stage only when actual geometry, light, camera or rigging helps. The CI proof is intentionally 640×360/24fps on software GL; final project renders use their own quality settings.
- FFmpeg/Tesseract/Playwright: mastering, probing, OCR/caption coverage and visual QA.

## Reproducibility and boundaries

- Node direct dependencies and the v3 package-lock are committed and validated together. CI uses `npm ci` only; it never writes commits back to a pull-request branch.
- Python profiles pin direct dependencies. Their workflows upload resolved pip-freeze evidence for review.
- Core smoke workflow has `contents: read` permission; the runtime install is reproducible without a CI write token.
- Cache npm, pip and Playwright downloads by OS and manifest hash.
- Blender is fetched only for the explicit Blender proof workflow; never commit the ~385 MB binary.
- GPU model weights are never part of default CI. The audio ML workflow installs packages only, not model checkpoints.
- This workstream does not modify video-library/**, video-library/assets/**, resource downloaders, SFX/music acquisition or the asset builder workflow. The parallel asset AI retains ownership.

## License gates

Read THIRD-PARTY-LICENSES.md. A package-code license does not grant rights to model weights, voices, footage, fonts, music or presets. Remotion and GSAP have special terms; check commercial eligibility before publishing.
