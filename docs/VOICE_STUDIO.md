# Voice Studio integration

The video repo consumes the pinned user fork of VoiceStudio as an independent
application submodule. It is the voice-management and TTS core; the video repo
adds voice-casting, batch orchestration, audition and audio-QA workflows.

Start with the full integration guide:
[integrations/voice-studio/README.md](../integrations/voice-studio/README.md).

## GitHub Actions execution

Production audio render/QA runs are orchestrated by
[Voice Studio Actions CPU lab](../.github/workflows/voice-studio-actions-lab.yml).
It renders ten KorvaTTS Vietnamese presets across four scripts, performs
FFprobe/FFmpeg checks, and uploads WAVs, blind audition pages and reports as a
GitHub Actions artifact. No local workstation is required for this baseline.

This CPU lane is explicitly a preset-voice baseline, not the full VoiceStudio
voice-design service. Custom VoiceStudio engines need a separate Actions lane
with compute/storage matching their actual model requirements.

## Core workflows

- Create a reusable original Vietnamese voice set:
  integrations/voice-studio/design_voice_library.py
- Audition saved profiles and compare them blind with a fixed script:
  integrations/voice-studio/voice_audition.py
- Generate a cast-locked per-line package for the existing H2 voice timing
  stage: integrations/voice-studio/generate_voiceover.py
- Inspect audio engineering signals and optionally ASR WER/CER:
  integrations/voice-studio/voice_quality.py
- Resume provider benchmarks and aggregate blind listener ratings:
  integrations/voice-studio/provider_voice_benchmark.py and
  integrations/voice-studio/analyze_voice_benchmark.py

## Agent skills

- [Voice design director](../.agents/skills/video-voice-design-director/SKILL.md)
- [Character voice casting engineer](../.agents/skills/video-character-voice-casting-engineer/SKILL.md)
- [Voice quality auditor](../.agents/skills/video-voice-quality-auditor/SKILL.md)

## Guardrails

Do not add model weights, reference recordings, API keys, cloned human voices,
or generated audio to Git. Use the external VoiceStudio model cache and local
secret stores. Profile cloning requires the speaker's permission. Each model
and its required components must be reviewed independently from the app's
AGPL-3.0 licence. Asset-library acquisition remains a separate completed
workstream and is not changed by voice development.
