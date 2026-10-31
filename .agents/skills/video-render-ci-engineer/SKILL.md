---
name: video-render-ci-engineer
description: Use when installing or upgrading video tools, building GitHub Actions render pipelines, optimizing CI caches, producing artifacts, version reports or reproducible renders.
---
# Video Render CI Engineer

## Safety
Read AGENTS.md and the target project handoff. Do not modify video-library/**, asset-library downloader/build files or the asset Release workflow unless explicitly assigned that workstream. Use a branch; do not cancel parallel asset runs.

## Runtime
- toolchain/manifest.json is the source of truth.
- Exact-pin direct npm versions in toolchain/node/package.json; never use latest, ^ or ~ in production manifests.
- Node 24 / Python 3.12 / Ubuntu 24.04. Install FFmpeg and Tesseract via apt; cache npm packages and Playwright Chromium by OS and manifest hash.
- Blender is manual-only. Verify the official checksum and render CPU-only unless a supported GPU runner is configured.
- Do not commit node_modules, browser binaries, Blender/Krita installers, model weights or rendered media into ordinary Git history.

## Workflow
Least privilege (contents:read by default), explicit path triggers, timeouts and concurrency. Never cancel the asset-release workflow group. Upload dependency lockfile, version report, checksum, SBOM/package inventory, render metadata and QA outputs. Keep toolchain smoke, film render and optional Blender jobs separate.

## Verification
Smoke-check actual commands: remotion --version, hyperframes --version, browser launch, FFmpeg/ffprobe and OCR languages. A config file is not proof that an install succeeded; a smoke pass is not artistic approval.
