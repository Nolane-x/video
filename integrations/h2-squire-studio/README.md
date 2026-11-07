# H2 Squire — Paullus at Cannae

Independent Squire Studio integration and production project for a vertical English history short.

- Project: `video-projects/squire/paullus-cannae-short/`
- Output: `1080 × 1920`, 24 fps, English narration, 9:16.
- Production: GitHub Actions only. The reusable VoiceStudio workflow generates a verified narration artifact; the H2 Squire kit renders the animation with Chromium and FFmpeg on the runner.
- Final MP4 and review bundle are delivered as the GitHub Actions artifact `squire-paullus-cannae-short-<run_id>`.
- The workflow keeps this separate from the existing Remotion Cannae 45-second picture-only proof.

The integrated kit is copied from the installed H2 Squire Studio 0.5.1 bundle. The vertical parchment-map layout is adjusted to reserve the lower caption band. This is an original Squire-style rendering, not an attempt to reproduce another creator's exact film.

Technical CI checks do not equal artistic approval. Watch the complete MP4 with sound and review pronunciation, pacing, captions and motion before public release.
