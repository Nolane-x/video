# Video library and visual memory

Read this folder before designing another video. It is the long-term catalog of films made by previous AI sessions.

User-selected external visual references are indexed in [`reference-clips.json`](reference-clips.json). The two standalone MP4 files were not found in the current workspace/Library snapshot, so the bundle keeps their source links and review protocol rather than rehosting the videos.

## Rules
- Each production needs a manifest, source commit/paths, story/shot data, master/preview links, contact sheets, QA notes, audio measurements and provenance.
- Keep master, preview, contact sheet, source package and reproducible build distinct.
- Use durable GitHub Releases for large masters where possible; Actions artifacts are temporary/test outputs. Do not put large MP4s into ordinary Git history by default.
- Never mark an artifact archived until its URL works and checksum/metadata are recorded.
- Inspect the actual video, not only its thumbnail or filename.

Current active candidate: [THE WEIGHT OF YES manifest](the-weight-of-yes/manifest.json), with [QA ledger](the-weight-of-yes/QA.md). Native H2 [run #8](https://github.com/Nolane-x/video/actions/runs/40429993390) passed all technical gates; full-length artistic review remains pending. Parallel technical-pass candidates after the shared engine fix: [THE FIRST HOUR #30](https://github.com/Nolane-x/video/actions/runs/40429993407) and [ALMOST READY #14](https://github.com/Nolane-x/video/actions/runs/40429993482). Actions artifacts are temporary, not durable archives. Historical/canonical project: [ONE MORE SCROLL manifest](one-more-scroll/manifest.json), with [QA state](one-more-scroll/QA.md). Its canonical H2 MP4 remains unchanged at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`; verified by [run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The Remotion output is a different build.


## Historical work and renderer-source preservation

[Previous work catalog](previous-works-catalog.json) inventories video iterations and their exact source-workspace checksums. Entries are *not* permanently archived unless their storage status says a GitHub verification workflow passed. The archive helper stages verified copies into `video-library/previous-works/<asset-id>/`; a workflow creates contact sheets/metadata and confirms the bytes after push.

The original H2 source and source-v2 scene-fixes ZIPs are published as checksum-verified assets in the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1); see [source release manifest](one-more-scroll/h2-source-release.json). They remain separate from Git history and from the portable skill ZIP. The repository does not vendor full upstream Remotion, Blender or Krita source trees; `docs/TOOL_INVENTORY.md` distinguishes Git files, release assets, and session-only attachments. A separate [source-v2 render candidate](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v2-render-candidate.mp4) passed technical validation; see [QA notes](one-more-scroll/QA.md). It is not promoted to canonical master until moving-picture review is approved. The source-v3 shoe-tying correction has a pinned patch and successful focused preview; its current [corrected full render rerun](https://github.com/Nolane-x/video/actions/runs/40286913324) and status are recorded in `one-more-scroll/h2-source-release.json`. Neither candidate is canonical until full-motion/audio QA is approved.



## ALMOST READY

ALMOST READY is a technical-pass H2 candidate: [manifest](almost-ready/manifest.json), [QA ledger](almost-ready/QA.md), [script](../video-projects/h2-selfimprove/01-PHIM-the-almost-ready.txt), [publishing package](almost-ready/02-PACKAGE-almost-ready.md), and [thumbnail prompts](almost-ready/03-THUMB-PROMPT-almost-ready.txt). [Run #14](https://github.com/${repo}/actions/runs/${ra}) passed; full contact-sheet and start-to-finish audio review remain pending.


## THE WEIGHT OF YES

Current render: [Actions run #22](https://github.com/Nolane-x/video/actions/runs/40452825177). Run #21 passed technical QA; full-length audiovisual sign-off is pending.



A new 29-shot H2 short about people-pleasing and personal boundaries: [script](../video-projects/h2-selfimprove/01-PHIM-the-weight-of-yes.txt), [project README](../video-projects/h2-selfimprove/the-weight-of-yes/README.md), [art bible](../video-projects/h2-selfimprove/the-weight-of-yes/story/bible.md), [manifest](the-weight-of-yes/manifest.json), [QA ledger](the-weight-of-yes/QA.md), [publishing package](the-weight-of-yes/02-PACKAGE-the-weight-of-yes.md), and [thumbnail directions](the-weight-of-yes/03-THUMB-PROMPT-the-weight-of-yes.txt). The authored target is 143 seconds, 1920×1080 at 24 fps, English on-screen text and no voice-over. The newest candidate is [Actions run #8](https://github.com/Nolane-x/video/actions/runs/40429993390), which passed all technical gates after a shared H2 scheduled-motion fix. Both contact sheets and the B08 motion proof were reviewed; full-length audio/video sign-off remains pending. The Actions artifact is temporary, not durable release storage.
