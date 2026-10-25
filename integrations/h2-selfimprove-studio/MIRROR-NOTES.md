# H2 SelfImprove Studio — source mirror

This folder mirrors the 51 UTF-8 source files reported by ChatGPT Plugin Creator for the private `h2-selfimprove-studio` release v1.0.2.

- [Open/activate the private ChatGPT plugin](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0)
- Plugin ID: `plugins_6ade1c3ca8d0819188070ae20f2792d0`
- Plugin release ID: `pluginrel_6ade1c3ecb20819199def25125d2f89a`
- Includes H2 scripts/skills, the renderer, rig, `dem` and `doodle` packs, audio generators and helper tools.
- Source file list and Git blob IDs are tracked in `SOURCE-MANIFEST.json`.

## Active plugin vs. mirrored source version

As verified on 2026-10-25, the active private ChatGPT plugin has been updated to **v1.1.0**, current release ID `pluginrel_6ade248942988191a57ff1059c818720`. The 51-file mirror in this folder remains the exact **v1.0.2 base-source snapshot** (release `pluginrel_6ade1c3ecb20819199def25125d2f89a`), by design. The production overlay used to build v1.1.0 is stored separately at `integrations/h2-selfimprove-studio-production-overlay/`; see [the verified release report](../h2-selfimprove-studio-production-overlay/RELEASE-RESULT-v1.1.0.md) and [the canonical plugin record](../../docs/CHATGPT_PLUGIN.md). Do not change the source snapshot's version or checksums to imply it was originally exported from v1.1.0.

This is the original H2 plugin package source, not a full checkout of the Remotion, Blender or Krita upstream applications. It should be used alongside this repo's cross-engine production skill and video library. The private ChatGPT plugin remains the activation point; this folder makes the same source files reviewable/versionable in GitHub.
