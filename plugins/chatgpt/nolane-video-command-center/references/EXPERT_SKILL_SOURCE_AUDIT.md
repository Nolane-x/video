# Expert skill source audit — video production

**Scope:** research and adaptation references for the Command Center and toolchain. This is not a statement that every upstream repository is installed, executable, or copied into this repository.

**Audit date:** 2026-10-31  
**Rule:** pin every inspected source to an immutable commit; preserve its exact license and notices; distinguish upstream code/tests from local adaptations; never download weights, use paid providers, or import media assets implicitly.

## Selected source references

| Upstream project | Inspected commit | License | Useful contribution | Local status / boundary |
|---|---|---|---|---|
| [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | [1266a3ec4831289c4d893d42dd5102723658039a](https://github.com/Vincentwei1021/video-shotcraft/commit/1266a3ec4831289c4d893d42dd5102723658039a) | Apache-2.0 | Product-video shot grammar, actual Remotion demos, transitions, camera moves, typography and beat-aware editing. | Existing Shotcraft integration remains a reference. Upstream README at this commit reports **124 recipe cards / 150 shots**; do not repeat the older 152-card count. SFX/music and Remotion runtime have separate terms; do not import those assets by default. |
| [video-production-skills](https://github.com/sb-dev/video-production-skills) | [5e82bb9a188d3cfc83cae0979cc39737011411b9](https://github.com/sb-dev/video-production-skills/commit/5e82bb9a188d3cfc83cae0979cc39737011411b9) | Apache-2.0 | Human approval states, bounded retry/spend, artifact lineage, independent evaluation and diagnosis by owning layer. | Concepts adapted into the QA protocol. Upstream TypeScript scripts/runtime were **not** copied or claimed as installed; its video-evaluate contract requires Node.js 24.12+ plus FFmpeg/ffprobe. Local checks continue to use this repository's pinned tools. |
| [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | [eddb488a093064f1be59cc3c6977684c2672a495](https://github.com/digitalsamba/claude-code-video-toolkit/commit/eddb488a093064f1be59cc3c6977684c2672a495) | MIT | Modular skill/command registry, voice/audio pipeline, scene-oriented workflow, project state, QC and reusable templates. | Reference for modularity and integration seams only. Do not import provider credentials, cloud GPU setup, weights, templates or third-party assets as defaults. |
| [claude-video-skills](https://github.com/imtamiliniyan/claude-video-skills) | [69b8f5f3447f569002cf71acd89eefe7965b2bee](https://github.com/imtamiliniyan/claude-video-skills/commit/69b8f5f3447f569002cf71acd89eefe7965b2bee) | MIT | Distinct workflows for talking-head shorts, long-form edits and faceless narration reels; brand setup and recurring-series contracts. | Routing reference only. Its paper-reel look is an optional style, never a universal house style. No bundled media/assets imported. |
| [video-pipeline-skills](https://github.com/arnans/video-pipeline-skills) | [4394273a3152b68dbc584f8fa28dde039ac72cfc](https://github.com/arnans/video-pipeline-skills/commit/4394273a3152b68dbc584f8fa28dde039ac72cfc) | MIT | Three distinct edit spines: demo-action-led, verbatim-script-led and outline/transcript-led; gap repair for ASR; editable FCP7 XML handoff. | Optional NLE/narration reference. Its GPU guidance and FCP7 import assumptions are not default toolchain requirements; no fonts or sample media imported. |
| [VideoDB skills](https://github.com/video-db/skills) | [583c70b9e847bfce104931cabe50e68e034398e2](https://github.com/video-db/skills/commit/583c70b9e847bfce104931cabe50e68e034398e2) | MIT | Search, query, transcribe and clip existing footage with a provider-backed video index. | Optional external integration only. Requires a VideoDB account/API and may consume credits; not part of core CI or default production. |
| [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | Current upstream license inspected 2026-10-31 | PolyForm Noncommercial 1.0.0 | Word-synchronized narration and motion-recipe ideas. | **Restricted:** do not copy/bundle its skill, cards, templates, code or media into a commercial workflow without separate written authorization. Existing local snapshot remains noncommercial-only. |

## Explicitly excluded from direct adaptation

| Project | License / issue | Decision |
|---|---|---|
| [OpenMontage](https://github.com/calesthio/OpenMontage) | AGPL-3.0; broad system with substantial code/skill corpus. | May be inspected as a public architecture reference, but do not copy or merge its code/skills into this repository without an explicit compatibility decision. |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | Official upstream skill repository; a permissive reuse license was not verified during this audit. | Use official Remotion documentation as a technical reference; do not copy skill text until license and exact commit are verified. |

## Integration and validation rules

1. A source link is not an integration. A plugin package is not proof that an upstream CLI, script or model is installed.
2. An adaptation must say which behaviour was derived, which code was copied (if any), which files were excluded, and which local test proves the result.
3. Preserve upstream LICENSE, required notices and third-party asset notices whenever files are copied.
4. Keep commercial eligibility separate from rights to model weights, voices, fonts, music, footage, SFX and example media.
5. Keep external services opt-in. Confirm account, privacy, cost, regional access and data-transfer implications before use.
6. For user work in Nolane-x/video, the separate asset-library workstream retains ownership. This toolchain track must not mutate its library, downloader, importer or builder files.
