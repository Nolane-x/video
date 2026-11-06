# H2 Squire Studio — repository integration

This directory mirrors the current source of the user's private h2-squire-studio plugin so that Squire productions can be reproduced by GitHub Actions in Nolane-x/video.

## Pinned source
- Plugin: h2-squire-studio
- Current private user release: v1.2.2
- Plugin ID: plugins_6aec6edf62248191b2eb6333f7620cbc
- Release ID: pluginrel_6aed0f69052c8191b54a5e97c5422f75
- Engine package: h2-2d-studio-kit v0.5.1
- Current skills mirrored: lam-video-squire and kich-ban-squire
- Full source manifest: SOURCE-MANIFEST.json

The uploaded ZIP in this conversation was v1.2.1 (SHA-256 668b98bff0187748513a15bc7025ff76ac8aea401b49523224e68ba61c2900f7). It was inspected, but not used to downgrade the newer v1.2.2 plugin. The mirror follows the current v1.2.2 private plugin source.

## Structure
- kit/ — renderer, engine, Squire/Doodle packs, tools, audio synthesizers.
- skills/lam-video-squire/ — production skill and operational references.
- skills/kich-ban-squire/ — scriptwriting skill and structure/title references.
- plugin-manifest.json — source plugin manifest copied for provenance.
- SOURCE-MANIFEST.json — exact source/version and output routing.

## Production route
The Cannae pilot lives in video-projects/squire/cannae-216bc and uses .github/workflows/squire-cannae-longform.yml. VoiceStudio is called as a separate reusable workflow; the WAV, captions, alignment report and provenance remain sidecar artifacts. Generated MP4/WAV outputs are not stored in Git history by default.

## Engine boundary
Squire is its own code-drawn 2D/vector canvas renderer. It is not Remotion and it is not the established H2 Canvas/Chromium engine. The existing H2, Remotion, Blender and Krita lanes remain intact.
