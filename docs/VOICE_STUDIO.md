# Voice Studio integration

The video repo consumes the pinned user fork of VoiceStudio as an independent
application submodule. It is the voice-management and TTS core; the video repo
adds voice-casting, batch orchestration, audition and audio-QA workflows.

Start with the full integration guide:
[integrations/voice-studio/README.md](../integrations/voice-studio/README.md).

## Core workflows

- Create a reusable original Vietnamese voice set:
  integrations/voice-studio/design_voice_library.py
- Audition saved profiles and compare them blind with a fixed script:
  integrations/voice-studio/voice_audition.py
- Generate a cast-locked per-line package for the existing H2 voice timing
  stage: integrations/voice-studio/generate_voiceover.py
- Inspect audio engineering signals and optionally ASR WER/CER:
  integrations/voice-studio/voice_quality.py

## Guardrails

Do not add model weights, reference recordings, API keys, cloned human voices,
or generated audio to Git. Use the external VoiceStudio model cache and local
secret stores. Profile cloning requires the speaker's permission. Each model
and its required components must be reviewed independently from the app's
AGPL-3.0 licence. Asset-library acquisition remains a separate completed
workstream and is not changed by voice development.
