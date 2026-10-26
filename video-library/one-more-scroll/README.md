# ONE MORE SCROLL — archive entry

Read [manifest.json](manifest.json) before using any output, and [QA.md](QA.md) before trusting the visual state.

## Durable Remotion render
The current archived sample is [`renders/remotion-run-31/one-more-scroll-remotion-master.mp4`](renders/remotion-run-31/one-more-scroll-remotion-master.mp4). The folder also contains per-shot contact sheets, overview, metadata, audio-loudness measurements, checksum manifest and the versioned skill ZIP. The latest pointer is [`latest-remotion-release.json`](latest-remotion-release.json). The archive job is [run 40197855575](https://github.com/Nolane-x/video/actions/runs/40197855575).

The portable top-level bundle is [`video-production-master-skill.zip`](../video-production-master-skill.zip); the packaging workflow is adding the current sample MP4 and source/docs to it so other agents can carry both the playbook and a reference film.

## Important: separate master files
The original 155-second 1920×1080 H2 Canvas/Chromium master is archived as `video-library/one-more-scroll/one-more-scroll-h2-final.mp4` and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The archive workflow stores a separate Remotion render at the path recorded by `latest-remotion-release.json`, plus contact sheets and the skill ZIP. That Remotion asset is not the H2 master.

When the exact H2 master becomes available through a supported binary upload path, add it as a Release asset, record SHA-256 + fresh ffprobe metadata, and update `manifest.json`. Never claim this happened until the asset URL works.
