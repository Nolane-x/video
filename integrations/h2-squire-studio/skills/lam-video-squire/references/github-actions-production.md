# GitHub Actions production mode — Nolane-x/video

Use this path when the production target is the public `Nolane-x/video` repository. Do not build the long-form master on the user's small local PC when the repository runner can do the work.

## Entrypoints

- Public engine integration: `integrations/h2-squire-studio/source.zip`
- First long-form pilot: `video-projects/squire/agincourt-project.zip`
- Workflow: `.github/workflows/squire-agincourt-longform.yml`
- Workflow run: https://github.com/Nolane-x/video/actions/workflows/squire-agincourt-longform.yml

## Pipeline contract

1. Validate the committed project ZIP and source ZIP against their SHA-256 checksums.
2. Validate `voice-job.json` and call `Nolane-x/VoiceStudio/.github/workflows/render-video-narration.yml` at a pinned commit.
3. For the Agincourt pilot, use English VieNeu v3 Turbo Adam: `en-vieneu-v3turbo-adam-3f0c9b`.
4. Download the VoiceStudio WAV and provenance manifest from the calling workflow run.
5. Extract the source archive, install the pinned Node renderer and Chromium, install Python audio/alignment libraries, and rebuild procedural music/SFX on the runner. Do not commit generated WAV caches or `node_modules`.
6. Create a new Squire project, prepare the voice timeline with `prep_voice.py`, produce shot timings with `draft_shots.py`, then author shot templates from the story plan.
7. Scan the timeline and every third frame; render contact sheets, a 30-second preview, thumbnail and the full 1920×1080 / 24 fps picture.
8. Mix narration, procedural score and motivated SFX with `tools/mix.py`; verify video/audio streams, dimensions, frame rate, duration, loudness and SHA-256.
9. Upload the MP4, thumbnail, contact sheets, voice manifest, shot timeline and QA report as a GitHub Actions artifact.

## Release gate

A green workflow proves deterministic project validation and technical render gates only. A person must still inspect the contact sheets and full video, listen to the narration/music/SFX mix, and confirm historical wording and timing before publication.

## Rights and attribution

The author has authorized public hosting in `Nolane-x/video`. Third-party packages, fonts, datasets and audio/model assets remain subject to their upstream terms. Use the VoiceStudio-generated voice manifest and its attribution notices with the final voice track. Do not claim all arrows penetrated plate armour, do not present Anne Curry's army totals as undisputed, and do not quote Shakespeare as Henry V's verbatim words.
