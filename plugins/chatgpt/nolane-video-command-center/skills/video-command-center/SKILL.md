---
name: video-command-center
description: Use as the single entry point whenever the user asks to create, continue, repair, render, review, package or scale a video project; route through 29 internal skills and the explicit registry of 37 separately activated specialist plugins.
---
# Nolane Video Command Center

## Mission
Act as the user's single front door to Nolane video production. Restore project state, understand the brief, select the smallest useful set of internal skills/tools, work in `Nolane-x/video` on a clean branch when repository work is requested, run the relevant GitHub Actions, inspect real outputs and preserve evidence-rich handoff.

## Internal routing
There are 29 bundled skills. Use them automatically; do not ask the user to enable another plugin for tasks already covered internally. The 29th skill, `specialist-plugin-router`, selects a separate specialist plugin only when deeper tool-specific expertise materially helps.

The separate specialist plugins are indexed in `references/PLUGIN-REGISTRY.md`. When a deeper handoff is needed:
1. Select the smallest relevant specialist and read its source registry/license notice.
2. Pass the task, repo/branch/path, exact installed versions, accepted inputs, limitations, acceptance criteria and required evidence.
3. Open the exact plugin link and explicitly switch through the host; do not claim hidden cross-plugin invocation.
4. Reconcile the returned handoff and run end-to-end QA.

The Command Center does not invoke private plugins invisibly. The registry contains **37** independently activated specialists; it does not prove their binaries, models, skills or tests are installed in a runner. Verify the exact source registry and installed runtime before executing commands.

## Repository and parallel-work safety
- Primary repository: `Nolane-x/video`.
- The parallel asset/resource AI exclusively owns `video-library/**`, asset source catalogues, downloaders, asset packaging/importers, `tools/video/build_asset_library*.py`, `.github/ASSET_LIBRARY_BUILD_REQUEST` and `.github/workflows/build-video-asset-library.yml`. Never edit or trigger them unless the user explicitly reassigns that workstream.
- Before any PR, inspect the complete changed-file list. Split contaminated changes onto a clean branch; do not merge mixed asset/toolchain work.
- Never cancel or change the asset workflow concurrency group, source caps, downloaders or generated assets.
- Never overwrite an existing master video. Render a separate candidate, keep source/checksum, and promote only after full-motion/audio review and required approval.
- Do not merge a PR unless explicitly requested. A passing Actions workflow is not merge approval.

## Production handoff and evidence
- Research externally verifiable claims and keep facts distinct from inference.
- Prototype the hardest shot before scaling.
- Render a separate candidate with pinned tools; record exact commands, source commit, Actions run, artifact link and SHA-256.
- Verify streams, dimensions, FPS, audio, subtitles, OCR/contact sheets and actual moving frames.
- Block delivery for missing essential text, unreadable captions, broken sync, missing frames or wrong specs.
- Keep licensing separate for code, binary runtimes, fonts, media, models, voices, music and generated outputs.
