# Nolane Video Studio

Code-first production workspace for cinematic, story-led YouTube animation.

## Start here for every new AI session

**Read [AGENTS.md](AGENTS.md) first**, then the [Video Production Master skill](.agents/skills/video-production-master/SKILL.md), [current project state](docs/STATE.md), [AI handoff](docs/AI_HANDOFF.md), and [video library](video-library/README.md). These files are the persistent creative and technical memory; don't rely on previous chat history alone.

## Canonical visual direction
Simple reusable stick-figure characters staged in rich, cinematic environments. Warm practical windows against plum/charcoal shadow; architecture and props; varied shot sizes; motivated camera; visible acting/contact; purposeful sound design. The user rejected generic gradient/flat-SVG output and pseudo-real AI humans.

- [Visual reference analysis](docs/ART_DIRECTION_IFVERSE_DAYONE.md)
- [Reusable skill](.agents/skills/video-production-master/SKILL.md)
- [Current state](docs/STATE.md)
- [Video catalog](video-library/README.md)
- [Verified tools/source inventory](docs/TOOL_INVENTORY.md)
- [Prior video catalog](video-library/previous-works-catalog.json)

## H2 SelfImprove Studio in ChatGPT

[Open/activate the private H2 SelfImprove Studio plugin](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0). The active Plugin Creator release is **v1.1.0** (`pluginrel_6ade248942988191a57ff1059c818720`), updated and confirmed on 2026-10-25. The 51-file source mirror under [integrations/h2-selfimprove-studio/](integrations/h2-selfimprove-studio/) intentionally preserves the v1.0.2 base source; the production overlay is versioned separately under [integrations/h2-selfimprove-studio-production-overlay/](integrations/h2-selfimprove-studio-production-overlay/). See the [source manifest](integrations/h2-selfimprove-studio/SOURCE-MANIFEST.json), [release result](integrations/h2-selfimprove-studio-production-overlay/RELEASE-RESULT-v1.1.0.md) and [activation notes](docs/CHATGPT_PLUGIN.md).

## Production architecture
- **H2 Studio:** primary for the established H2 rig/renderer when its full source and bundled skill are available.
- **Remotion:** timeline, text, frame-driven composition, compositing and CI. Project: [video-projects/remotion](video-projects/remotion).
- **Blender:** selected 2.5D/3D shots when depth, camera, light or rigging adds value. [tools/blender](tools/blender).
- **Krita:** deliberately authored art assets and paintovers. [tools/krita](tools/krita).
- **FFmpeg/ffprobe:** mastering and technical validation.

## Important distinction
The Full HD H2 master previously delivered in ChatGPT is noted in the manifest but is not yet committed as a binary file in this repository. The Remotion pipeline generates a separate reproducible render. Do not conflate engines or claim an asset is archived until its permanent URL/checksum is verified.

## Workflows
- [Remotion render](.github/workflows/render-remotion.yml) — generates music/SFX, typechecks, renders, masters audio, validates metadata and uploads QA.
- [Blender proof](.github/workflows/render-blender-preview.yml)
- [H2 runtime package](.github/workflows/prepare-h2-runtime.yml)
- [Video Showcase archive](.github/workflows/archive-video-showcase.yml) — creates a tagged Release with Remotion video and skill ZIP when the triggering render commit includes `[archive-video]`.

Large video masters should be kept as Release assets, not ordinary Git blobs. The skill and manifest preserve a distinction between source-only changes, rendered output and visually reviewed output.

## Reusable ChatGPT plugin

The active private H2 plugin is v1.1.0: [Open h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0). Its current release ID, CI evidence, checksum and base-source/overlay distinction are documented in [docs/CHATGPT_PLUGIN.md](docs/CHATGPT_PLUGIN.md). The native H2 kit remains distinct from the repo's Remotion renderer.

## Voice Studio and narration

The full [Nolane VoiceStudio fork](https://github.com/Nolane-x/VoiceStudio) is
pinned under `vendor/VoiceStudio/` as an independent AGPL-3.0 submodule.
The video repo adds a lightweight multi-provider adapter for saved VoiceStudio
profiles/archetypes, KorvaTTS, Google Cloud TTS and ElevenLabs.

- [Voice Studio integration guide](docs/VOICE_STUDIO.md)
- [Provider adapters, voice casting and H2 handoff](integrations/voice-studio/README.md)
- [Original Vietnamese synthetic voice set](integrations/voice-studio/examples/vietnamese-original-voice-set.json)
- [Stable Vietnamese documentary cast](integrations/voice-studio/examples/vietnamese-documentary.json)
- [Repeatable Vietnamese pronunciation benchmark](integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt)
- [Voice profile factory, blind audition and audio QA](integrations/voice-studio/README.md)

The integration can create reusable fictional voice-design profiles in VoiceStudio, audition saved profiles blindly with a common script, lock a cast by speaker_id, resume failed audio batches and run technical/ASR QA. It does not add weights or output audio to Git. Model rights and real-speaker consent remain separate gates.

## Downloads and current reference

- **[Download the portable Video Production Master ZIP](video-library/video-production-master-skill.zip)** — reusable agent skill, cross-agent entrypoints, project/source map, tool inventory, state/handoff, Remotion source, storyboard and the archived reference render.
- **[Open the latest archived Remotion MP4](video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4)** — 155.1 seconds, 1280×720, 24 fps. See [the current manifest](video-library/one-more-scroll/latest-remotion-release.json) and [QA notes](video-library/one-more-scroll/QA.md).
- **[Current art-direction/production skill](.agents/skills/video-production-master/SKILL.md)** — canonical source for future AI sessions.
- **[Tool inventory](docs/TOOL_INVENTORY.md)** — explicitly distinguishes checked-in projects from full app/source archives and older session-only video outputs.
- **[Prior AI video catalog](video-library/previous-works-catalog.json)** — tracks historical MP4s by checksum and archive status.

The portable ZIP includes both the checksum-verified canonical H2 Canvas/Chromium master and a separate Remotion run-36 reference render; they are distinct outputs. Large H2 source ZIPs and the technically validated source-v2 candidate are published separately in the [H2 production Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). A deterministic source-v3 shoe-tying patch now has a focused preview pass; corrected full render [run 40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324) is underway after the first render passed video/audio checks but failed review-payload checksum packaging. See [the install/restore guide](docs/INSTALL_VIDEO_SKILL.md), [current state](docs/STATE.md), and [QA log](video-library/one-more-scroll/QA.md).
