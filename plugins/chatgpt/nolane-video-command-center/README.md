# Nolane Video Command Center v0.8.0

One private front door for the Nolane video workflow. It retains **29 internal production skills** and routes to **37 focused specialist plugins**. v0.8.0 adds a blocking creative-plan preflight before rendering and an evidence-backed independent full audiovisual review gate before release.

## How to use
1. Start with the Command Center and describe the goal, audience, language, length and delivery format.
2. It restores current repository/project state and routes internally to the minimum necessary skills.
3. When deeper tool-specific work is justified, open the corresponding specialist link in `references/PLUGIN-REGISTRY.md` and explicitly switch to that plugin.
4. Return the specialist's handoff to the Command Center for project integration, full render and end-to-end QA.

The Command Center does not invisibly activate other private plugins. This host-controlled boundary is explicit in the router and registry.

## Safety and reproducibility
- The parallel asset AI owns `video-library/**`, catalogues, downloaders, asset packaging/importers and `.github/workflows/build-video-asset-library.yml`. Do not edit or trigger those paths unless explicitly reassigned.
- Inspect the full changed-file list before PR creation; keep mixed asset/toolchain changes separate.
- Do not overwrite master videos; deliver a separately rendered candidate with checksums and visual/audio review.
- Keep costs, model downloads, voice likeness, rights, production writes and PR merges behind explicit approval.
- A plugin's existence or source-backed skill does not prove its CLI, weights or runtime are installed. Check pinned versions and actual evidence.
- License boundaries are per component: aubio GPL-3.0-or-later; Inkscape GPL-family binary obligations; Rough.js/Rough Notation MIT; SVG.js MIT; Theatre Core Apache-2.0 and Theatre Studio AGPL-3.0-only. Confirm the exact version/build and separately audit fonts, assets, runtimes and linked dependencies.

See `SKILL-CATALOG.md`, `references/PLUGIN-REGISTRY.md` and `references/PLUGIN-RESEARCH-METHODOLOGY.md`.
