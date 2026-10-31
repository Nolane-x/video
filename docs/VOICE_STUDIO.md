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

For actual video narration, the separate
[Voice Studio Actions production renderer](../.github/workflows/voice-studio-actions-project.yml)
takes a committed multi-character manifest, creates per-line audio, checks and
loudness-normalizes the files, and runs the real H2 `prep_voice.py` timing
stage to export `voice.wav`, `blocks.json`, `lines.json`, `words.json`
and `transcript.txt`. It also exports word-timed SRT/VTT/ASS captions,
sentence-level and speaker-labelled variants, a per-character voice-cast
report, and an artifact SHA-256 manifest. The example project includes four
stable characters and ten dialogue segments. Audio and timeline files are
uploaded as a workflow artifact.

Caption times use H2's estimated word/sentence boundaries rather than ASR
forced alignment. Review subtitles against the audio before publishing.

These Actions CPU lanes intentionally use KorvaTTS's released Vietnamese
presets; they are not the full VoiceStudio custom voice-design service. A
custom VoiceStudio engine still needs its own Actions lane with compute and
storage matched to its model requirements. It must not silently fall back to a
developer's workstation.

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
