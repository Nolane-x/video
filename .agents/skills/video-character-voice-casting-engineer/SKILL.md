---
name: video-character-voice-casting-engineer
description: Turn a video script into a stable multi-character voice cast and per-line audio package. Use when generating narration, dialogue, dubbing, interviews or recurring characters with VoiceStudio and other TTS providers.
---

# Video Character Voice Casting Engineer

## Mission

Convert the approved script into a reliable voice-over package while preserving each character's vocal identity, the exact dialogue text and the H2 timing handoff. Casting is a production decision; synthesis is only one stage.

## Read and inspect

Before editing a manifest:
- Read the voice integration guide and current project manifest.
- Inspect actual saved VoiceStudio profiles and their exact profile IDs.
- Check provider/engine availability; do not assume the documented engine has been installed.
- Confirm each selected model and all required components have passed the project's rights gate.
- Locate the existing H2 `prep_voice.py` and preserve its parser contract. The current parser reads blocks such as `=== V001 | NARRATOR · Character ===` and expects matching `V001.wav` / `V001.mp3` files in the voice directory.

## Build a role map before generating audio

Break the script into speaker turns, not arbitrary equal-length chunks. Each row should have:
- stable `id` such as `V001`;
- stable `speaker_id` used across the full series;
- `slot`/role for editorial grouping and speaker-gap timing;
- character name;
- exact approved text, preserving Vietnamese diacritics, names, numbers and intentional punctuation;
- engine/provider, saved voice ID, language, speed, seed and any engine-specific settings;
- optional acting notes that are supported by the selected engine.

A top-level `cast` is the source of truth. Define each speaker once and reference it in every segment:

```json
{
  "language": "vi",
  "cast": {
    "narrator": {
      "provider": "voicestudio",
      "engine": "voxcpm2",
      "voice": "SAVED_PROFILE_ID",
      "language": "vi",
      "seed": 4201
    }
  },
  "segments": [
    {
      "id": "V001",
      "speaker_id": "narrator",
      "slot": "NARRATOR",
      "character": "Người dẫn chuyện",
      "text": "Lời dẫn đã được biên tập và duyệt."
    }
  ]
}
```

The generator fingerprints provider, engine, voice/profile ID, language, style/instruct, seed and settings. If the same `speaker_id` changes voice identity, stop and resolve the casting change explicitly. Do not “fix” this validator by removing the speaker ID or bypassing the identity check.

## Select engines honestly

- VoiceStudio profile ID is preferred for a character that needs continuity across shots/episodes.
- KorvaTTS presets are useful for Vietnamese local rendering; they are fixed presets, not user-created clones.
- Google Cloud and ElevenLabs account voices are discovered dynamically and should be stored by exact provider voice ID.
- Provider libraries may contain voices that do not support the requested language. Use the verified-language metadata; do not infer capability from a display name.
- Keep engine settings fixed within a character's profile. A seed helps reproducibility but does not guarantee identical prosody on every line or identical identity across different engines.

## Generate the line package

First validate the manifest without connecting to a provider:

```bash
python integrations/voice-studio/generate_voiceover.py \
  --manifest projects/<project>/voice-cast-and-lines.json \
  --output out/<project>-voice --plan-only
```

After review, synthesize:

```bash
python integrations/voice-studio/generate_voiceover.py \
  --manifest projects/<project>/voice-cast-and-lines.json \
  --output out/<project>-voice
```

The batch generator:
- writes one audio file per dialogue block;
- caches by script + provider + engine + profile + language + seed + settings;
- writes progress after each segment so failures can resume;
- removes partial/corrupt target files after a failed segment;
- continues after individual provider failures unless `--stop-on-error` is requested;
- writes a generation report with expected text, voice identity fingerprint, byte count and SHA-256;
- exports `02-VOICE-<project>-TTS.txt` for the existing H2 timing parser.

Do not use output audio from a failed segment. Do not mark the batch complete if the report says partial.

## H2 handoff

The voice package is not the final timeline or audio master. Run the actual repository H2 timing tool from the repo root:

```bash
python integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit/tools/prep_voice.py \
  --project projects/<project> \
  --voice-dir out/<project>-voice/voice \
  --voice-txt out/<project>-voice/02-VOICE-<project>-TTS.txt \
  --lang vi
```

The H2 tool owns concatenation, silence trimming, block/line/word timestamp output and the master `voice.wav`. Use the same script and audio directory as the report. Check that every `V###` block has a corresponding playable WAV/MP3. Preserve the generated blocks/lines/words/transcript files in the project's QA package.

Do not silently rewrite text after synthesis. If a script changes, invalidate its cache and regenerate the affected segment, then rerun timing and subtitle alignment.

## Error recovery

- VoiceStudio unavailable: keep the report and retry after the service is healthy; do not silently switch to another provider.
- Engine unavailable or licence unaccepted: stop and resolve the model installation/acceptance path.
- Profile preview pending: preserve the profile ID, but do not call it audition-ready.
- Provider failure: inspect the exact failed segment and cache; retry only after correcting the cause.
- Identity drift: check `speaker_id` cast entry and profile mapping; do not patch only the filename.
- ASR mismatch: listen to the actual clip before rewriting dialogue. It may be ASR error, TTS pronunciation error or both.

## Required outputs

- approved cast manifest;
- line-level generation report and audio checksums;
- H2 `voice.wav`, blocks, lines, words and transcript;
- subtitle alignment review;
- clear record of failed/partial segments;
- human sign-off for each core character.

Generated audio, reference recordings, secrets and personal voice-consent documents stay out of Git unless explicitly approved for private archival.
