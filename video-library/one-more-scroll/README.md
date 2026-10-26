# ONE MORE SCROLL — archive entry

Read [manifest.json](manifest.json) before using any output, and [QA.md](QA.md) before trusting the visual state.

## Durable Remotion render
The current archived Remotion sample is [`renders/remotion-run-36/one-more-scroll-remotion-master.mp4`](renders/remotion-run-36/one-more-scroll-remotion-master.mp4), from render CI [run 40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650). The folder contains the render, contact sheets, metadata, audio-loudness measurements, checksums, and the versioned portable skill ZIP.

The portable top-level bundle is [`video-production-master-skill.zip`](../video-production-master-skill.zip); packaging run [40278816724](https://github.com/Nolane-x/video/actions/runs/40278816724) verified 172 entries, including the Remotion reference film, canonical H2 master, source-release manifest, candidate QA metadata, cross-agent instructions, H2 production overlay and source-v2 render/Release-sync workflows.

## Important: separate master files
The original 155-second 1920×1080 H2 Canvas/Chromium master is archived as `video-library/one-more-scroll/one-more-scroll-h2-final.mp4` and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The archive workflow stores a separate Remotion render at the path recorded by `latest-remotion-release.json`, plus contact sheets and the skill ZIP. That Remotion asset is not the H2 master.

The source-v2 candidate render is also available as [MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v2-render-candidate.mp4), with [review ZIP/contact sheets/logs](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v2-render-review.zip). It passed technical render and stream checks in [run 40276064292](https://github.com/Nolane-x/video/actions/runs/40276064292), but is not artistically approved or canonical until a complete motion/audio review passes. The source-v3 shoe-tying fix is driven by `tools/video/patch_h2_shoelace_scene.py`, has a focused-preview pass [40280228327](https://github.com/Nolane-x/video/actions/runs/40280228327), and is being rendered in [first attempt 40281627022](https://github.com/Nolane-x/video/actions/runs/40281627022); follow `docs/STATE.md` for the live result. The original master and source-v2 candidate stay unchanged.

The archive and its SHA-256/ffprobe evidence are recorded in `manifest.json`, `QA.md`, and `original-h2-master-metadata.json`. The original source and source-v2 scene-fixes packages are published in the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1), with checksums and asset URLs in `h2-source-release.json`. The portable package contains the instructions and release manifest, not duplicate 230+ MB ZIP assets. The source-v2 candidate has passed full render/stream checks; the remaining gate is full moving-picture/audio review and explicit artistic sign-off.


Corrected source-v3 full render rerun: [40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324). The first render passed technical video/audio checks but the review ZIP checksum step failed because the patch script was not copied into its payload. The rerun fixes this packaging step; canonical H2 master remains untouched.
