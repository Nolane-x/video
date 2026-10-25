# ONE MORE SCROLL — archive entry

Read [manifest.json](manifest.json) before using any output, and [QA.md](QA.md) before trusting the visual state.

## Durable Remotion render
[latest-remotion-release.json](latest-remotion-release.json) is updated by `.github/workflows/archive-video-showcase.yml` after a successful archive-marked render. It points to the permanent GitHub Release containing:
- the repo's Remotion MP4,
- contact sheets,
- ffprobe metadata and audio measurements,
- `video-production-master-skill.zip`,
- SHA-256 checksums.

If this pointer does not exist yet, inspect [GitHub Releases](https://github.com/Nolane-x/video/releases) and [Actions](https://github.com/Nolane-x/video/actions) for the latest successful run.

## Important: separate master files
The original 155-second 1920×1080 H2 Canvas/Chromium master was delivered as a ChatGPT attachment but was not imported as a durable binary in this repo. The archive workflow stores a separate Remotion render at the path recorded by `latest-remotion-release.json`, plus contact sheets and the skill ZIP. That Remotion asset is not the H2 master.

When the exact H2 master becomes available through a supported binary upload path, add it as a Release asset, record SHA-256 + fresh ffprobe metadata, and update `manifest.json`. Never claim this happened until the asset URL works.
