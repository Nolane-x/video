# Third-party license register

Engineering inventory, not legal advice. Re-check versions and terms before upgrades, redistribution, downloading model weights or commercial publishing.

| Component | Version | License / condition | Handling |
|---|---:|---|---|
| Remotion + CLI | 4.0.538 | Special tiered Remotion license | Check current eligibility for creator/entity and commercial scale. |
| HyperFrames | 0.8.222 | Apache-2.0 | Preserve notice. |
| GSAP | 3.15.0 | GreenSock standard license | Not MIT; check current terms for actual use. |
| Motion | 14.9.0 | MIT | Preserve notice. |
| Three.js / PixiJS | 0.186.1 / 8.22.0 | MIT | Preserve notices. |
| Theatre.js Core | 0.7.2 | Apache-2.0 | Core only; do not bundle Theatre Studio (AGPL-3.0). |
| SVG.js / Rough.js / D3 | 3.2.8 / 4.6.6 / 7.9.0 | MIT / MIT / ISC | Preserve notices. |
| postprocessing | 6.39.5 | MIT | Preserve notice. |
| resvg-js | 2.6.2 | MPL-2.0 | Retain MPL notice; modified covered files may have source obligations. |
| Sharp / Playwright | 0.35.4 / 1.64.1 | Apache-2.0 | Preserve notices; browser binaries have separate notices. |
| FFmpeg | Ubuntu 24.04 apt | LGPL/GPL depends on build flags/codecs | Archive ffmpeg -buildconf; do not assume LGPL-only. |
| Tesseract | Ubuntu 24.04 apt | Apache-2.0 | Language data may have separate notices. |
| Blender | 5.2.3 | GPL-3.0-or-later | Optional runner install; comply with redistribution if bundling. |
| OpenTimelineIO | 0.18.1 | Apache-2.0 | Timeline data/interchange only; adapters have separate limits. |
| PySceneDetect headless | 0.7.2 | BSD-3-Clause | Headless package uses opencv-python-headless. |
| Manim CE | 0.22.1 | MIT with upstream copyright/license notices | Retain notices; Cairo/Pango/TeX system packages are separate. |
| WhisperX | 3.8.6 | BSD-2-Clause | Package code only; model weights and diarization/provider terms are separate. |
| Demucs | 4.1.0 | MIT | Package code only; pretrained weights have separate terms. |

## Model, voice and media rights

- Package license is not a license for pretrained checkpoints or training data.
- Diarization may require credentials and separate model/provider terms. Never commit tokens or upload secrets in CI artifacts.
- Voice samples and identity rights are separate; do not imitate a real person's voice without authorization.
- Footage/music rights remain in the separate asset library's provenance register.

## Dependency evidence

Core Actions uploads the resolved npm license inventory and CycloneDX SBOM. Optional Python workflows upload package evidence for the profile they execute.
