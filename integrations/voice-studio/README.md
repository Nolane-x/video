# Nolane Voice Studio Integration

This directory connects the video-production pipeline to the user's pinned
VoiceStudio fork and to optional direct speech providers. It is an adapter and
workflow layer, not a second desktop studio.

## VoiceStudio application

The complete application is pinned as a Git submodule:

- Repository: https://github.com/Nolane-x/VoiceStudio
- Upstream parent: https://github.com/debpalash/VoiceStudio
- Pinned commit: faa5294359f23c911972ffe6d27785c50c67097b
- Application license: AGPL-3.0
- VoiceStudio's nested omnivoice-gallery submodule is not initialized by
  default. The video repo does not need to recursively clone it for the API
  adapter to work.

Initialize only the application submodule:

    git submodule update --init vendor/VoiceStudio

VoiceStudio is a separate app/service. Start its desktop app or its documented
local Docker service yourself, then keep its API on loopback. The default
adapter target is http://127.0.0.1:3900.

Optional connection environment:

- VOICESTUDIO_BASE_URL — defaults to http://127.0.0.1:3900.
- VOICESTUDIO_API_KEY — optional for local loopback; required when the
  service is configured for API-key access. Never commit this value.

The adapter uses VoiceStudio's documented API:

- GET /health
- GET /engines/tts
- GET /v1/models
- GET /v1/audio/voices
- GET /profiles
- GET /archetypes
- POST /archetypes/{id}/use
- POST /v1/audio/speech

A profile ID or an engine preset can be used as the voice. Use the actual
engine ID returned by /engines/tts; do not assume that an engine is installed
just because it appears in VoiceStudio's documentation.

## Provider adapters

| Provider | Voice catalogue | Generation | Notes |
|---|---|---|---|
| VoiceStudio | Saved profiles, installed engine information and built-in archetypes | Local API | Preferred orchestration layer; the UI handles voice design/cloning |
| KorvaTTS | 10 Vietnamese preset voices | Local ONNX/CPU | Presets only today; upstream voice cloning/training is not treated as shipped |
| Google Cloud TTS | Live voice discovery through Google API | Cloud | Uses Google Application Default Credentials |
| ElevenLabs | Paginated account voice library and verified-language metadata | Cloud | Requires ELEVENLABS_API_KEY; not every library voice supports Vietnamese |

This allows the video repo to use the same segment manifest across providers.
Provider selection is per speaker/line, so a narrator, interview guest and
character can each use a different authorized voice. New cloud voices are
discovered at runtime rather than hardcoded into the repo.

Optional installs (only install the provider you use):

    python -m pip install korvatts
    python -m pip install google-cloud-texttospeech

Google Cloud credentials should be configured using Application Default
Credentials, for example GOOGLE_APPLICATION_CREDENTIALS pointing to a
local, untracked service-account file. ElevenLabs credentials must be set in
ELEVENLABS_API_KEY. Do not put credentials in manifests, logs, or GitHub
files.

## Generate a voice-over package

Start with the example manifest and replace the placeholder IDs with actual
voice IDs from your connected catalogue.

    python integrations/voice-studio/voice_catalog.py --provider voicestudio
    python integrations/voice-studio/voice_catalog.py --provider korva --language vi
    python integrations/voice-studio/voice_catalog.py --provider google --language vi-VN
    python integrations/voice-studio/voice_catalog.py --provider elevenlabs --language vi

Create an audio generation plan without connecting to a TTS provider:

    python integrations/voice-studio/generate_voiceover.py \
      --manifest integrations/voice-studio/examples/vietnamese-documentary.json \
      --output out/voiceover --plan-only

Generate the selected segments:

    python integrations/voice-studio/generate_voiceover.py \
      --manifest integrations/voice-studio/examples/vietnamese-documentary.json \
      --output out/voiceover

The output contains:

- voice/V001.wav, voice/V002.wav, etc. (ElevenLabs uses MP3).
- 02-VOICE-<project>-TTS.txt, formatted for the existing H2
  prep_voice.py block parser.
- voice-generation-report.json, with provider/voice/model metadata,
  output file checksums and cache status.

Then hand those files to the current H2 timing/assembly stage. The script
does not silently re-time or alter the narration. Existing prep_voice.py
continues to create the timeline/blocks/lines/words and transcript files.

Generated audio and cache folders are outputs, not source files. Keep them
outside Git. Voice cache keys include text, provider, voice, model and settings,
so changing the voice or text causes a new render while unchanged lines can be
reused.

## Model and voice rights

The app license and every model/voice license are separate:

- VoiceStudio's application is AGPL-3.0. If you redistribute a modified
  network-served VoiceStudio application, the AGPL corresponding-source
  obligations apply. Keep the application as a submodule rather than copying
  it into the video repo.
- VoiceStudio's default OmniVoice weights are disclosed as non-commercial
  (CC-BY-NC family) and include additional tokenizer/component terms. Do not
  select it for monetized/commercial videos unless the full current component
  chain and intended use have been cleared.
- Other VoiceStudio engines also have individual model/component restrictions.
  VoiceStudio's own model-acceptance dialog and its model licence inventory
  should be checked before installation/use. A code licence alone is not model
  or generated-voice permission.
- KorvaTTS's upstream project publishes Apache-2.0 code/weights for its ten
  shipped presets. Re-check upstream before redistribution or commercial use.
- Google Cloud and ElevenLabs are governed by their current service terms,
  voice-specific permissions and plan/API conditions. A public voice library
  entry is not blanket permission to impersonate a real person.

Only clone/use voices for which the speaker has given the necessary permission.
Keep source audio consent records private and outside the public repository.

## Tests and limits

The adapter tests use mocks and standard-library unittest. They do not download
model weights, invoke paid APIs, run the full desktop app, or claim a naturalness
quality score. End-to-end acceptance still requires a real VoiceStudio service,
an installed/licence-accepted TTS engine, valid provider credentials where
needed, and playback review of Vietnamese and English samples.
