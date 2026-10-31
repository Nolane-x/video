---
name: video-command-center
description: Use as the single entry point whenever the user asks to create, continue, repair, render, review, package or scale a video project; route through 29 internal skills and the explicit registry of 37 separately activated specialist plugins.
---
# Nolane Video Command Center

## Mission
Act as the user's single front door to Nolane video production. Restore project state, understand the brief, select the smallest useful set of internal skills/tools, work in `Nolane-x/video` on a clean branch when repository work is requested, run the relevant GitHub Actions, inspect real outputs and preserve evidence-rich handoff.

## Internal routing
There are 29 bundled skills. Use them automatically; do not ask the user to enable another plugin for tasks already covered internally. The 29th skill, `specialist-plugin-router`, selects a separate specialist plugin only when deeper tool-specific expertise materially helps.

Before selecting engines for a video project, read `docs/GENRE_ROUTING_MATRIX.md` and, when the repository workspace is available, `tools/video/genre-routing.json`. Treat the JSON as the machine-readable routing contract: choose the closest primary profile, then follow its creative owners, primary versus conditional tools, required evidence, guardrails and `qaChecks`. For a deliberate hybrid, name the primary profile and explain the specific secondary route. Conditional tools are not mandatory dependencies. H2/stick-figure style is not a global house style; only consider it inside the narrative-animation route when the brief or an established series explicitly calls for it. The route must never mutate the parallel asset-library workstream.

Before rendering a storyboard, require a completed creative brief and run `python tools/video/evaluate_editorial_plan.py <shot-plan.json> --output <report.json> --strict`. A blocked plan must be revised, not bypassed. The preflight checks audience/promise/hook/payoff, explicit narration policy, story-function coverage, shot size/angle/camera/composition, motion/contact proof, pacing variation, template concentration and planned text/audio coverage. `PLAN_READY_FOR_RENDER` permits only a low-resolution blocking preview; render the specified motion proofs with `python tools/video/render_blocking_preview.py <shot-plan.json> --project-root <remotion-dir> --output <preview-dir>`. A full render is blocked until `python tools/video/validate_preview_approval.py <shot-plan.json> --manifest <preview-dir>/manifest.json --project-root <remotion-dir>` verifies explicit reviewer approval, every selected segment, preview-spec SHA-256 and exact preview-clip bundle SHA-256. After preview approval and full render, complete `tools/video/editorial-review.template.json` and run `python tools/video/validate_editorial_review.py <review.json> --video <candidate.mp4>`. Do not claim a rendered film is production-ready until an independent reviewer has watched the full moving picture with audio, inspected captions and logged defects/timecodes. A machine-readable plan score is not a quality score for the finished video.

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
