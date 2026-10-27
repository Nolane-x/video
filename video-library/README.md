# Video library and visual memory

Read this folder before designing another video. It is the long-term catalog of films made by previous AI sessions.

User-selected external visual references are indexed in [`reference-clips.json`](reference-clips.json). The two standalone MP4 files were not found in the current workspace/Library snapshot, so the bundle keeps their source links and review protocol rather than rehosting the videos.

## Rules
- Each production needs a manifest, source commit/paths, story/shot data, master/preview links, contact sheets, QA notes, audio measurements and provenance.
- Keep master, preview, contact sheet, source package and reproducible build distinct.
- Use durable GitHub Releases for large masters where possible; Actions artifacts are temporary/test outputs. Do not put large MP4s into ordinary Git history by default.
- Never mark an artifact archived until its URL works and checksum/metadata are recorded.
- Inspect the actual video, not only its thumbnail or filename.

Current active candidate: [THE FIRST HOUR manifest](the-first-hour/manifest.json), with [QA notes](the-first-hour/QA.md). Its full-length H2 master passed technical QA in [Actions run #26](https://github.com/Nolane-x/video/actions/runs/40329265743), but remains awaiting a complete start-to-finish artistic watch with audio and durable release archival. Historical/canonical project: [ONE MORE SCROLL manifest](one-more-scroll/manifest.json), with [QA state](one-more-scroll/QA.md). The original H2 MP4 is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The Remotion output is a different build.


## Historical work and renderer-source preservation

[Previous work catalog](previous-works-catalog.json) inventories video iterations and their exact source-workspace checksums. Entries are *not* permanently archived unless their storage status says a GitHub verification workflow passed. The archive helper stages verified copies into `video-library/previous-works/<asset-id>/`; a workflow creates contact sheets/metadata and confirms the bytes after push.

The original H2 source and source-v2 scene-fixes ZIPs are published as checksum-verified assets in the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1); see [source release manifest](one-more-scroll/h2-source-release.json). They remain separate from Git history and from the portable skill ZIP. The repository does not vendor full upstream Remotion, Blender or Krita source trees; `docs/TOOL_INVENTORY.md` distinguishes Git files, release assets, and session-only attachments. A separate [source-v2 render candidate](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v2-render-candidate.mp4) passed technical validation; see [QA notes](one-more-scroll/QA.md). It is not promoted to canonical master until moving-picture review is approved. The source-v3 shoe-tying correction has a pinned patch and successful focused preview; its current [corrected full render rerun](https://github.com/Nolane-x/video/actions/runs/40286913324) and status are recorded in `one-more-scroll/h2-source-release.json`. Neither candidate is canonical until full-motion/audio QA is approved.



## ALMOST READY

A new H2 SelfImprove film is being built from original source: [script](../video-projects/h2-selfimprove/01-PHIM-the-almost-ready.txt), [project README](../video-projects/h2-selfimprove/almost-ready/README.md), [manifest](almost-ready/manifest.json), [QA ledger](almost-ready/QA.md), [publishing package](almost-ready/02-PACKAGE-almost-ready.md), and [thumbnail prompts](almost-ready/03-THUMB-PROMPT-almost-ready.txt). It targets 29 shots/172 seconds and currently requires a technical render plus full artistic review. See the dedicated workflow `.github/workflows/render-selfimprove-almost-ready.yml`.


## THE WEIGHT OF YES

A new 29-shot H2 short about people-pleasing and personal boundaries: [script](../video-projects/h2-selfimprove/01-PHIM-the-weight-of-yes.txt), [project README](../video-projects/h2-selfimprove/the-weight-of-yes/README.md), [art bible](../video-projects/h2-selfimprove/the-weight-of-yes/story/bible.md), [manifest](the-weight-of-yes/manifest.json), [QA ledger](the-weight-of-yes/QA.md), [publishing package](the-weight-of-yes/02-PACKAGE-the-weight-of-yes.md), and [thumbnail directions](the-weight-of-yes/03-THUMB-PROMPT-the-weight-of-yes.txt). The authored target is 143 seconds, 1920×1080 at 24 fps, English on-screen text and no voice-over. The newest preview-audio-validated render is [Actions run #6](https://github.com/Nolane-x/video/actions/runs/40425050181); run #5 reached the full silent-render stage before the preview-audio gate was added. It is not marked final until stream/loudness checks, contact-sheet/proof review and a full moving-picture/audio review are complete.
