---
name: video-voice-quality-auditor
description: Audit TTS samples and production voice-over for intelligibility, Vietnamese pronunciation, audio engineering defects, speaker identity drift and human-reviewed naturalness. Use after auditions, batch synthesis, dubbing or voice casting.
---

# Video Voice Quality Auditor

## Mission

Separate measurable defects from subjective vocal quality. A technically valid WAV is not automatically a good performance, and an ASR score is not a naturalness score. Evaluate pronunciation, stability, intelligibility, emotional fit and audio engineering without inventing an ElevenLabs-equivalence percentage.

## Execution policy: GitHub Actions is the render worker

For production benchmarks and audio generation, use the repository's
GitHub Actions workflows:

- `.github/workflows/voice-studio-actions-lab.yml` renders the ten KorvaTTS
  presets against four fixed Vietnamese scripts and performs FFprobe/FFmpeg QA.
- `.github/workflows/voice-studio-actions-project.yml` synthesizes a full
  multi-character project, audits individual WAVs, and runs the real H2
  `prep_voice.py` timing stage to produce the voice master and timestamps.

Inspect the resulting artifacts and workflow summaries; do not redirect model
inference to a developer PC just because an Actions lane is missing or
underpowered. The current CPU lanes use KorvaTTS's preset voices; they do not
exercise VoiceStudio custom voice design. Record that scope explicitly.

The separate `.github/workflows/voice-studio-headless-smoke.yml` builds the
pinned VoiceStudio fork and validates its FastAPI surface on a CPU runner. It
is a server/API contract check only: a healthy container and a non-empty engine
catalogue do not mean a Vietnamese model is installed or licensed, and do not
mean synthesis was performed. Require a separate rendered WAV artifact before
calling any VoiceStudio engine audio-tested.

For the project renderer, inspect the full delivery package, not just its
green job status: confirm each WAV hash, per-speaker identity fingerprint,
H2 block/line/word coverage, master audio peak/loudness, `captions.srt`,
`captions.vtt`, `captions.ass`, sentence-level caption alternatives,
`voice-cast-report.json`, and `artifact-manifest.json`. The artifact manifest
must exclude hidden internal caches that are not uploaded by Actions.

Caption timestamps produced by H2's proportional word/sentence heuristic are
estimated editing guides, not forced-alignment ground truth. Check every cue
against the spoken audio, especially sentence boundaries, numbers, code-
switching and short phrases, before publishing.

## Three distinct evidence layers

### A. Audio engineering signals

Use the repository checker:

```bash
python integrations/voice-studio/voice_quality.py \
  --report out/<project>-voice/voice-generation-report.json
```

Review codec, sample rate, channels, duration, peak/RMS, clipped-sample ratio, near-silence ratio and leading/trailing silence. Investigate:
- empty or truncated files;
- long silent tails;
- near-silence;
- clipping/peak headroom;
- inconsistent channel/rate handling;
- abrupt concatenation or bad fades;
- excessive loudness differences between characters.

Do not use a universal loudness target without considering the platform, soundtrack and mastering stage. Per-segment voice output is not the final mix.

### B. Pronunciation and intelligibility proxy

When VoiceStudio has a usable ASR engine installed, compare each generated sample to the exact script:

```bash
python integrations/voice-studio/voice_quality.py \
  --report out/<project>-voice/voice-generation-report.json \
  --asr --language vi
```

Or run the cross-provider same-script benchmark with `--asr`.

Interpret WER/CER carefully:
- NFC/diacritic-preserving comparison is essential for Vietnamese.
- Check initial consonants, final consonants, all six tones, vowel length, numbers, dates, proper names, abbreviations and English technical terms embedded in Vietnamese.
- An ASR can be wrong even when the speech is correct. Listen to every surprising mismatch.
- ASR can normalize punctuation/spacing. A low WER is not proof of good rhythm, naturalness or speaker similarity.
- A high WER can reflect ASR weakness, TTS pronunciation errors, text normalization mismatch or a clipped audio file.

WER/CER is an intelligibility/pronunciation proxy only. Never translate it into “x% of ElevenLabs”.

### C. Human performance and voice identity

Listen to full samples and review them in scene context. Evaluate each dimension separately:
1. naturalness: artifacts, breath/noise behaviour, smoothness, coarticulation;
2. Vietnamese articulation: tones, consonants, names, numbers and code-switching;
3. identity stability: same character across multiple lines and episodes;
4. expression: emphasis, emotion, pauses and delivery control;
5. character fit: does this sound like the correct narrator/host/expert/character?
6. cast separation: are voices distinct enough when heard back-to-back?
7. long-form stamina: does voice quality degrade or become repetitive over a long narration?

Use blind same-script audition pages so the listener does not know which provider/profile is playing. Rate each dimension 1–5 only after listening to the complete samples. Record why a voice wins; do not treat the arithmetic mean as an objective benchmark.

## Compare fairly

Use the same script, language, engine configuration, synthesis speed, reference conditions and post-processing wherever possible. Korva can share an explicit seed across preset comparisons. VoiceStudio designed profiles must retain their saved design seed; do not overwrite it during A/B. Google/ElevenLabs calls can incur cost and require explicit `--allow-cloud`.

Example:

```bash
python integrations/voice-studio/provider_voice_benchmark.py \
  --provider all --engine voxcpm2 --allow-cloud --asr \
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --language vi --limit 20 --output out/benchmark-all
```

The resulting benchmark is evidence about the selected engines, voices, script, settings and current revisions, not a universal ranking.

Before treating an `all` run as comparative evidence, inspect
`provider_catalogue` in the JSON report. Every selected provider must report
`available`; an empty or failed catalogue makes the run `partial` even if
other providers rendered audio.

The provider benchmark is restartable. In blind mode it shuffles candidates reproducibly with `--blind-seed`, checkpoints after every candidate and resumes only when the saved audio file still matches its SHA-256 and remains inside the benchmark output directory. Failed candidates are retried. After changing a remote service/model revision or any synthesis setting not represented in the cache key, use `--no-resume` to force a fresh comparison.

After listening, export the ratings JSON from the HTML page and join it to the benchmark's private identity map:

```bash
python integrations/voice-studio/analyze_voice_benchmark.py \
  --benchmark out/benchmark-all/provider-voice-benchmark.json \
  --ratings out/benchmark-all/voice-human-ratings.json \
  --min-ratings 3
```

Review rating coverage before comparing providers. The report includes per-dimension and provider means, with each eligible candidate weighted equally. A candidate needs at least 3 of 5 dimensions rated by default. ASR WER/CER remains a separate intelligibility proxy. Never interpret the average as a naturalness score or an ElevenLabs-equivalence percentage.

## Identity audit

Review the `speaker_identity_audit` in `voice-quality-report.json`. A character with one `speaker_id` must keep one provider/engine/profile identity fingerprint. Any “drift” is a release blocker until the casting change is intentional and documented. “not_recorded” means a legacy/third-party report lacks a fingerprint; do not silently claim that it was consistent.

## Acceptance gates

A voice can be:
- **Rejected:** wrong pronunciation, unstable identity, audible artifacts, unsuitable acting or unresolved rights.
- **Needs revision:** good core timbre but script, pacing, seed, instruction or mastering needs work.
- **Candidate:** usable sample but not yet approved for the series.
- **Approved for role:** passed full listening, benchmark and rights gates for a specific character/series. It is not an endorsement for impersonation or unrestricted reuse.

Do not accept a profile based only on its description, a successful API response, a model-card marketing claim or a blind rating average.

## Required QA package

- source script and stable cast manifest;
- engine/model revision and licence/consent gate;
- generated audio checksums;
- technical audio report;
- ASR transcript + WER/CER where available;
- blind human ratings and reviewer notes;
- identity drift report;
- explicit status per voice and per segment;
- known limitations and untested conditions.
