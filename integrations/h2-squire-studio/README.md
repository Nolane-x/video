# H2 Squire — Paullus at Cannae

An independent H2 Squire Studio production project for a vertical English history short.

- Story: **The Roman Consul Who Rode Into Hannibal's Trap**
- Output: 1080 × 1920, 24 fps, English narration, 9:16.
- Production: GitHub Actions. VoiceStudio generates a watermarked 48 kHz PCM-24 narration artifact; Squire renders the animation through Chromium and FFmpeg on the runner.
- Output artifact: `squire-paullus-cannae-short-<run_id>` containing the MP4, preview, visual contact sheets, thumbnail, storyboard, aligned narration, captions and QA reports.
- Source project: `video-projects/squire/paullus-cannae-short/`.

The visuals follow H2 Squire's vector-history language: a recurring Paullus character, mounted cavalry movement, deep battlefield staging, parchment geography and animated overhead tactics. Roman units are red and Carthaginian units blue as a viewer-facing diagram convention, not a claim of uniform historical livery. The encirclement graphics are schematic, not a surveyed reconstruction.

The historical account is grounded in Polybius, *Histories* Book III, sections 113–116. The video omits disputed army and casualty totals. The final MP4 must still receive a full moving-picture and audio review before public release; passing technical CI is not artistic approval.
