# Nolane Video Actions Toolchain

The repo owns the recipes, pins, wrappers, skills, tests and workflows. GitHub Actions installs runtime packages into ephemeral runner storage and caches downloads. This is intentionally not a node_modules or desktop-installer commit to Git history.

## Profiles

| Profile | Contents | When it runs |
|---|---|---|
| core | Node 24, Remotion, HyperFrames, Motion Canvas libraries, GSAP, Motion, Three.js, PixiJS, Theatre Core, SVG/D3, resvg, Sharp, postprocessing, Playwright Chromium, FFmpeg and Tesseract EN/VI | Toolchain smoke workflow, CPU-first |
| blender | Blender 5.2.3 official Linux x64 archive, verified with the official SHA-256 manifest | Manual workflow only; ~385 MB download and CPU render |

The existing Remotion film stays pinned at 4.0.538. Do not bump it as part of routine toolchain refreshes. Runtime packages install under toolchain/node; the scripts expose the binary directory and the Actions workflow links the runtime into the existing Remotion workspace for Node module resolution.

## Actions workflow

1. Run Video toolchain smoke manually or by changing toolchain/skill files. It installs dependencies and Chromium, checks module imports/CLIs, records version data, transitive dependencies, licenses and a CycloneDX SBOM.
2. Run HyperFrames render proof manually to verify a scaffold → lint → MP4 → snapshot path on a CPU runner.
3. Run Blender CPU proof only when a planned shot benefits from actual 3D depth, camera parallax, lighting or geometry. The binary is downloaded from the official host and verified against the official checksum file.

## Engine routing

- Remotion: primary deterministic React timeline/compositing.
- HyperFrames: HTML/CSS/GSAP scenes, lint, render, snapshot and CLI diagnostics.
- Motion Canvas: vector/explanatory animation; 3.17.2 is a specialist lane and must be smoke-tested before use in a film.
- GSAP / Motion / Theatre Core: timeline choreography, springs and authored keyframes.
- Three.js / PixiJS / postprocessing: procedural 3D, 2D particles, depth, filters, glow, blur and compositing.
- SVG.js / Rough.js / D3 / resvg / Sharp: vector scenes, illustrative accents, data motion, rasterization and image transforms.
- FFmpeg / Tesseract / Playwright: mastering, media inspection, OCR/caption coverage and browser capture.
- Blender: optional 3D stage. Start with a low-res 3–5 second proof.

## Reproducibility and size

- Every direct npm dependency is exact-pinned in toolchain/node/package.json and duplicated in toolchain/manifest.json.
- Actions creates package-lock.json and uploads it with install evidence. The first transitive lock must be reviewed and promoted into source only after CI resolves successfully.
- Cache npm and Playwright Chromium by OS + package manifest hash.
- Blender is fetched only when the manual 3D workflow runs; do not commit its 385 MB binary.
- No GPU models or giant native SDK stacks are in the default toolchain.

## Existing project boundaries

This workstream does not edit video-library/**, video-library/assets/**, asset downloaders, SFX/music generation or the asset-release workflow. Existing H2 and Remotion render workflows are preserved. The toolchain smoke workflow does not render or overwrite any film master.

## License gates

Read THIRD-PARTY-LICENSES.md and package notices before redistribution or commercial use. Remotion has a tiered license; Theatre Core is Apache-2.0 while Theatre Studio is AGPL-3.0; resvg-js is MPL-2.0. FFmpeg's effective license depends on build flags and enabled codecs.
