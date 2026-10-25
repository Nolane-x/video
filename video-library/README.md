# Video library and visual memory

Read this folder before designing another video. It is the long-term catalog of films made by previous AI sessions.

## Rules
- Each production needs a manifest, source commit/paths, story/shot data, master/preview links, contact sheets, QA notes, audio measurements and provenance.
- Keep master, preview, contact sheet, source package and reproducible build distinct.
- Use durable GitHub Releases for large masters where possible; Actions artifacts are temporary/test outputs. Do not put large MP4s into ordinary Git history by default.
- Never mark an artifact archived until its URL works and checksum/metadata are recorded.
- Inspect the actual video, not only its thumbnail or filename.

Current production: [ONE MORE SCROLL manifest](one-more-scroll/manifest.json), with [QA state](one-more-scroll/QA.md). The original H2 MP4 was delivered in a prior ChatGPT session but is not yet binary content in GitHub; the repository's Remotion output is a different build.
