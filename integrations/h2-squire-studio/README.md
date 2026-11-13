# H2 Squire Studio — public integration

This directory contains the public Squire source archive used by the new animated military-history production lane in `Nolane-x/video`.

- `source.zip` contains the skill pair (`kich-ban-squire`, `lam-video-squire`), references, 2D vector engine, Squire character/horse/army packs, renderer, voice preparation, scene planner and audio synthesis source.
- `source.sha256` records the release archive digest.
- The source archive omits the former personalized purchase-license file and omits generated WAVs and `node_modules`; GitHub Actions rebuilds the procedural audio library from source.
- `PUBLIC-RELEASE-NOTICE.md` records the author's authorization to host and use this source publicly in this repository. Third-party dependencies retain their own upstream licensing.

## Production entry point

`video-projects/squire/agincourt-project.zip` is the first long-form project. `.github/workflows/squire-agincourt-longform.yml` calls VoiceStudio's reusable TTS workflow, downloads the verified Adam narration, installs Squire on `ubuntu-24.04`, rebuilds music/SFX, aligns the voice, authors shots, renders 1080p/24fps, mixes and uploads the final MP4 plus review evidence as a GitHub Actions artifact.

Run history: [Squire — Agincourt longform production](../../actions/workflows/squire-agincourt-longform.yml).