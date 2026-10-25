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

The user's H2 plugin has been created privately through ChatGPT Plugin Creator: [Open h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0). Its source/version and scope are documented in [docs/CHATGPT_PLUGIN.md](docs/CHATGPT_PLUGIN.md). This is the original H2 kit/plugin, distinct from the repo's Remotion renderer.

## Downloads and current reference

- **[Download the portable Video Production Master ZIP](video-library/video-production-master-skill.zip)** — reusable agent skill, cross-agent entrypoints, project/source map, tool inventory, state/handoff, Remotion source, storyboard and the archived reference render.
- **[Open the latest archived Remotion MP4](video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4)** — 155.1 seconds, 1280×720, 24 fps. See [the current manifest](video-library/one-more-scroll/latest-remotion-release.json) and [QA notes](video-library/one-more-scroll/QA.md).
- **[Current art-direction/production skill](.agents/skills/video-production-master/SKILL.md)** — canonical source for future AI sessions.
- **[Tool inventory](docs/TOOL_INVENTORY.md)** — explicitly distinguishes checked-in projects from full app/source archives and older session-only video outputs.
- **[Prior AI video catalog](video-library/previous-works-catalog.json)** — tracks historical MP4s by checksum and archive status.

The portable ZIP contains the Remotion reference render, not the original H2 Canvas/Chromium master until that exact binary is downloaded and pushed through `tools/video/archive_h2_master.py`. See [the installation/import guide](docs/INSTALL_VIDEO_SKILL.md). Full H2 source ZIPs are published separately as verified GitHub Release assets by `tools/video/publish_h2_source_release.ps1`.
