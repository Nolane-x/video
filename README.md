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
