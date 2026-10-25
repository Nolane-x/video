# Source and asset policy

## Do commit

- Original project source, story JSON, documentation, rendering scripts, workflow configuration, and small assets we created or are licensed to redistribute.
- Small optimized reference sheets and thumbnails when useful.
- Exact dependency versions and reproducible build instructions.

## Do not commit

- Split upstream source archives such as `remotion-main.zip.001` through `.006`.
- Complete upstream Blender or Krita source trees just to make the applications available.
- `node_modules`, application binaries, secrets, API keys, local caches, or large rendered video/audio outputs.
- Assets that we do not own or cannot redistribute.

Store final videos in GitHub Actions artifacts or Releases. For large original assets, use Git LFS only where needed and review its storage/bandwidth limits first.

## Licensing

Installing or invoking an application is different from republishing its source code. Follow Remotion's current license and terms, and the respective Blender/Krita licenses. Track the origin and license for every third-party image, font, audio sample, and texture.
