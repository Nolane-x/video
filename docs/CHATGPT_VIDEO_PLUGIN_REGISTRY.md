# ChatGPT video plugin registry

Last verified against Plugin Creator: **2026-10-31**.

## Main entry point

**Nolane Video Command Center v0.7.9** is the primary routing plugin. Its active private release is `pluginrel_6ae5b448d6948191a011fc39d2ec282d`.

- 29 internal production skills.
- 37 separately activated specialist plugins with a source/provenance registry.
- The authoritative list, versions, links and routing boundaries live in `plugins/chatgpt/nolane-video-command-center/references/PLUGIN-REGISTRY.md`.
- Activation of another private plugin is controlled by ChatGPT and the user. The Command Center does not silently invoke another private plugin.

[Open Nolane Video Command Center](https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc).

## Other distinct private video plugins

| Plugin | Active version | Role | Link |
|---|---:|---|---|
| Nolane Video Production Studio | 0.4.0 | Broad multi-engine production library with 32 top-level specialist skills and bundled source snapshots | https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd |
| H2 SelfImprove Studio | 1.1.0 | Native H2 renderer, rigs, dem/doodle packs, procedural audio and a focused self-improvement animation workflow | https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 |

These are not interchangeable:
- Command Center is the normal orchestration entry point.
- Video Production Studio is an independent broader skill library; it is not silently called by Command Center.
- H2 is a specialised engine/workflow, not a universal video editor or the repository's Remotion renderer.

**Rights warning:** the Video Production Studio contains a Talkcraft snapshot under PolyForm Noncommercial 1.0.0. Do not use that snapshot's code, cards, templates, demos or embedded sounds in monetized/commercial deliverables without prior written commercial authorization. Check `resources/UPSTREAM-LICENSE-MATRIX.md` before using any included third-party material.

## Repository toolchain

The CPU-first runtime, pinned package profile, CI proofs and helper tools are maintained in:
- `toolchain/manifest.json`
- `toolchain/node/package.json` and `package-lock.json`
- `docs/video-toolchain/README.md`
- `docs/video-toolchain/THIRD-PARTY-LICENSES.md`

A tool listed in a plugin or manifest is not proof that it is installed on a user's computer. Use the corresponding clean-runner or project-specific proof, and distinguish a technical smoke render from artistic approval.

## Workstream boundary

The parallel asset workstream owns `video-library/**`, asset-source catalogues, downloaders, asset importers/packaging and the asset-library workflow. Video-toolchain changes must stay isolated from those paths unless ownership is explicitly reassigned.
