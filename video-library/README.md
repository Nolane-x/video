# Video library and visual memory

Read this folder before designing another video. It is the long-term catalog of films made by previous AI sessions.

User-selected external visual references are indexed in [`reference-clips.json`](reference-clips.json). The two standalone MP4 files were not found in the current workspace/Library snapshot, so the bundle keeps their source links and review protocol rather than rehosting the videos.

## Rules
- Each production needs a manifest, source commit/paths, story/shot data, master/preview links, contact sheets, QA notes, audio measurements and provenance.
- Keep master, preview, contact sheet, source package and reproducible build distinct.
- Use durable GitHub Releases for large masters where possible; Actions artifacts are temporary/test outputs. Do not put large MP4s into ordinary Git history by default.
- Never mark an artifact archived until its URL works and checksum/metadata are recorded.
- Inspect the actual video, not only its thumbnail or filename.

Current production: [ONE MORE SCROLL manifest](one-more-scroll/manifest.json), with [QA state](one-more-scroll/QA.md). The original H2 MP4 is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The Remotion output is a different build.


## Historical work and renderer-source preservation

[Previous work catalog](previous-works-catalog.json) inventories video iterations and their exact source-workspace checksums. Entries are *not* permanently archived unless their storage status says a GitHub verification workflow passed. The archive helper stages verified copies into `video-library/previous-works/<asset-id>/`; a workflow creates contact sheets/metadata and confirms the bytes after push.

The canonical H2 source ZIP is too large for ordinary Git history. Use `tools/video/publish_h2_source_release.ps1` to upload checksum-verified H2 source assets as a GitHub Release after downloading the matching files. The repository does not vendor full upstream Remotion, Blender or Krita source trees; `docs/TOOL_INVENTORY.md` separates what is in Git from session-only attachments.
