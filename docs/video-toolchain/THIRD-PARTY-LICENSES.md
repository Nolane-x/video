# Third-party license register (toolchain)

Engineering notice only, not legal advice. Re-check exact package metadata and notices at every upgrade and before distribution.

| Component | Version | License / condition | Handling |
|---|---:|---|---|
| Remotion + CLI | 4.0.538 | Special Remotion license; qualifying individual/small/non-profit use may be free; some larger for-profit organizations need a company license | Check current official license for the legal entity and deployment. |
| HyperFrames | 0.8.222 | Apache-2.0 | Preserve license and notices. |
| GSAP | 3.15.0 | GreenSock standard license | Check current terms; do not call it MIT. |
| Motion | 14.8.0 | MIT | Preserve notice. |
| Three.js | 0.186.1 | MIT | Preserve notice. |
| PixiJS | 8.22.0 | MIT | Preserve notice. |
| Motion Canvas packages | 3.17.2 | MIT | Preserve notices; validate the older stable release against current Node/Chromium. |
| Theatre.js Core | 0.7.2 | Apache-2.0 | Core only. Do not bundle Theatre Studio (AGPL-3.0) by default. |
| SVG.js / Rough.js | 3.2.8 / 4.6.6 | MIT | Preserve notices. |
| D3 | 7.9.0 | ISC | Preserve notice. |
| postprocessing | 6.39.5 | MIT | Preserve notice. |
| resvg-js | 2.6.2 | MPL-2.0 | Keep MPL notice; modified MPL files can create source availability obligations for those files. |
| Sharp | 0.35.4 | Apache-2.0 | Preserve notices; use supported platform prebuilt binaries. |
| Playwright | 1.64.1 | Apache-2.0 | Browser binaries have separate notices; use the official Playwright installer. |
| FFmpeg | Ubuntu 24.04 apt package | LGPL/GPL depends on build options/codecs | Upload ffmpeg -buildconf; don't claim LGPL-only without checking the exact build. |
| Tesseract | Ubuntu 24.04 apt package | Apache-2.0 | Language data packages may have separate notices. |
| Blender binary | 5.2.3 | GPL-3.0-or-later | Optional runner installation; comply with redistribution terms if ever bundling the binary. |

## Provenance

Exact direct package versions and upstream links are in toolchain/manifest.json. The Actions-generated license report covers the actual transitive packages resolved at install time.
