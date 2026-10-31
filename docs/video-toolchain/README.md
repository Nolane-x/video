# Nolane Video Actions Toolchain

The repository owns exact pins, installers, profiles, skills, tests and workflows. GitHub Actions installs into isolated runner storage and caches downloads. It does not commit node_modules, browser binaries, model weights or desktop installers into normal Git history.

## Profiles

| Profile | Contents | Trigger | Hardware |
|---|---|---|---|
| Core | Node 24, Remotion, HyperFrames, GSAP, Motion, Three.js, PixiJS, Theatre Core, SVG/D3, resvg, Sharp, Playwright Chromium, FFmpeg, Tesseract EN/VI | PR/push smoke | CPU |
| Editorial | OpenTimelineIO 0.18.1 and PySceneDetect headless 0.7.2 | PR and manual proof | CPU |
| Manim | Manim CE 0.22.1, Cairo/Pango and TeX | PR proof on Manim profile/source changes; manually dispatchable | CPU |
| Audio ML | WhisperX 3.8.6 and Demucs 4.1.0 | Manual install/import only | CPU import; model inference may need GPU |
| Blender | Blender 5.2.3 official Linux x64 archive verified against official SHA-256, EGL/Mesa software GL | Path-scoped PR proof or manual dispatch | CPU |

The existing Remotion film remains pinned at 4.0.538. Optional Python profiles have separate exact direct requirements and are not installed into the Node core environment.

## Workflows

1. **Video toolchain smoke** validates manifests, plugin/skill contracts and the committed npm lockfile; installs exactly from that lockfile with `npm ci`, typechecks the existing Remotion app, tests CLIs/modules and uploads checksums, license inventory, SBOM and runtime-version evidence.
2. **HyperFrames render proof** uses a repository-owned, 17-second 1920×1080 sample with local pinned GSAP, phrase-level captions, a motion sidecar and an original procedural test score. It runs strict browser/layout/motion/contrast/craft/audio checks, preserves five sampled PNG frames plus a contact sheet, renders H.264, muxes AAC 48 kHz stereo and independently probes the final MP4.
3. **Editorial interchange proof** generates synthetic two-scene media, detects the hard cut and round-trips a frame-accurate OTIO timeline. It never reads the separate asset library.
4. **Manim proof** installs Cairo/Pango/TeX and renders a short equations/graph scene with Manim CE.
5. **Audio ML runtime** is manual-only; installs/imports WhisperX/Demucs code but does not fetch models or access credentials.
6. **Blender proof** runs a short EEVEE CPU preview using the official Blender 5.2.3 archive and verified SHA-256. The CI preview is intentionally 2 seconds at 320×180/24 fps to exercise headless render/encoding on a CPU runner; it is not a final-quality render preset.

## Verified clean-branch CI evidence — 2026-10-31

All runs below completed successfully on clean PR commit `bf443d8738b1326502efdbbb6f4ab81ab668eb19`:

| Gate | Actions run | Verified result |
|---|---:|---|
| Core toolchain smoke | [41175570073](https://github.com/Nolane-x/video/actions/runs/41175570073) | Exact lockfile install, Remotion typecheck, CLI/module smoke, SBOM/license/version/checksum artifact |
| HyperFrames strict proof | [41175570008](https://github.com/Nolane-x/video/actions/runs/41175570008) | Strict report clean; 300 motion samples; contrast 37/37; five PNG snapshots and six-frame contact sheet; final 17.000s H.264 1920×1080/24p + AAC stereo 48 kHz |
| Blender EEVEE CPU preview | [41175570037](https://github.com/Nolane-x/video/actions/runs/41175570037) | 2.000s H.264 320×180/24p; official archive checksum verified |
| Manim CE proof | [41175570007](https://github.com/Nolane-x/video/actions/runs/41175570007) | 6.800s H.264 854×480/15p; TeX/Cairo/Pango runtime and resolved requirements |
| Caption OCR EN/VI | [41175570021](https://github.com/Nolane-x/video/actions/runs/41175570021) | Bilingual timed-text fixture and visual text coverage audit passed |
| Editorial interchange | [41175570038](https://github.com/Nolane-x/video/actions/runs/41175570038) | Synthetic hard-cut detection and OTIO timing round-trip passed |

The HyperFrames proof artifact also stores the exact QA JSON, five individual frame samples, contact sheet, source demo, video-only render, mastered MP4 and original procedural WAV. The report sections `lint`, `runtime`, `layout`, `motion`, `contrast`, `craft` and `audio` each returned `ok=true` with zero errors and warnings. The motion checker evaluated 300 samples. These are technical/fixture-level proofs, not artistic approval of a future film.

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
- Blender: optional 3D stage only when actual geometry, light, camera or rigging helps. The CI proof is a deliberately small EEVEE CPU preview; final project renders use their own quality settings.
- FFmpeg/Tesseract/Playwright: mastering, probing, OCR/caption coverage and visual QA.

## Reproducibility and boundaries

- Node direct dependencies and the v3 package-lock are committed and validated together. CI uses `npm ci` only; it never writes commits back to a pull-request branch.
- Python profiles pin direct dependencies. Their workflows upload resolved pip-freeze evidence for review.
- Core smoke workflow has `contents: read` permission; the runtime install is reproducible without a CI write token.
- Cache npm, pip and Playwright downloads by OS and manifest hash.
- Blender is fetched only for its explicit proof workflow; never commit the ~385 MB binary.
- GPU model weights are never part of default CI. The audio ML workflow installs packages only, not model checkpoints.
- This workstream does not modify `video-library/**`, `video-library/assets/**`, resource downloaders, SFX/music acquisition or the asset builder workflow. The parallel asset AI retains ownership.

## License gates

Read `THIRD-PARTY-LICENSES.md`. A package-code license does not grant rights to model weights, voices, footage, fonts, music or presets. Remotion and GSAP have special terms; check commercial eligibility before publishing.
