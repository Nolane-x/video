# ONE MORE SCROLL — archive entry

Read [manifest.json](manifest.json) before using any output, and [QA.md](QA.md) before trusting the visual state.

## Durable Remotion render
The current archived Remotion sample is [`renders/remotion-run-36/one-more-scroll-remotion-master.mp4`](renders/remotion-run-36/one-more-scroll-remotion-master.mp4), from render CI [run 40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650). The folder contains the render, contact sheets, metadata, audio-loudness measurements, checksums, and the versioned portable skill ZIP.

The portable top-level bundle is [`video-production-master-skill.zip`](../video-production-master-skill.zip); packaging run [40272019747](https://github.com/Nolane-x/video/actions/runs/40272019747) verified 167 entries, including the Remotion reference film, original H2 master, source/docs and H2 production overlay.

## Important: separate master files
The original 155-second 1920×1080 H2 Canvas/Chromium master is archived as `video-library/one-more-scroll/one-more-scroll-h2-final.mp4` and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The archive workflow stores a separate Remotion render at the path recorded by `latest-remotion-release.json`, plus contact sheets and the skill ZIP. That Remotion asset is not the H2 master.

The archive and its SHA-256/ffprobe evidence are now recorded in `manifest.json`, `QA.md`, and `original-h2-master-metadata.json`. Remaining open gates concern visual sign-off, a fresh H2 source-v2 render, and separately archiving the H2 source ZIPs. The portable package includes the H2 master but does not include these still-missing source ZIPs.
