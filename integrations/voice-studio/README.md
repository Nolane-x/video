# Nolane Voice Studio Integration

This is the voice-production layer for \`Nolane-x/video\`. It reuses the user's
pinned VoiceStudio application as the voice-management and synthesis core; it
does not rebuild another desktop studio or duplicate the upstream backend.

## 1. VoiceStudio application

The application is pinned as an independent Git submodule:

- Repository: https://github.com/Nolane-x/VoiceStudio
- Parent: https://github.com/debpalash/VoiceStudio
- Commit: \`faa5294359f23c911972ffe6d27785c50c67097b\`
- Application license: AGPL-3.0
- Model weights and local voice assets are not committed to this repository.

Initialize the submodule:

\`\`\`bash
git submodule update --init vendor/VoiceStudio
\`\`\`

Start VoiceStudio locally (desktop app or its documented Docker service).
The adapter defaults to \`http://127.0.0.1:3900\`.

- \`VOICESTUDIO_BASE_URL\` — optional service URL.
- \`VOICESTUDIO_API_KEY\` — optional on loopback; required if the remote
  service is configured for API-key access. Remote API keys require HTTPS.
  Never commit the value.

The adapter uses VoiceStudio's documented health, TTS engine/model, profile,
archetype, preview and OpenAI-compatible speech/transcription APIs. A voice
profile ID is the stable identifier to keep in a video cast.

## 2. Where the voices come from

| Source | What it contributes | Important limit |
|---|---|---|
| VoiceStudio saved profiles | Reusable cloned or designed voices, preview samples, profile IDs | Cloning requires the speaker's authorization and a legally usable reference recording |
| VoiceStudio archetypes | Several hundred combinatorial designs, plus a curated multilingual subset | Most generated combinations are English/Chinese; it is not a Vietnamese-only catalogue |
| VoxCPM2 through VoiceStudio | Native text-description voice design and zero-shot reference cloning; supports Vietnamese | Model and component licence review is still required; design descriptions do not guarantee the same identity quality as ElevenLabs |
| OmniVoice through VoiceStudio | Very broad language coverage and reference cloning/design | The current default weights are in a CC-BY-NC family with extra component terms; do not assume commercial use |
| KorvaTTS | 10 Vietnamese preset voices (5 female, 5 male), 44.1 kHz ONNX/CPU, code-switching | Preset voices only today; voice cloning/training is still on the upstream roadmap |
| Google Cloud TTS | Live provider voice catalogue | Cloud account/billing/service terms apply |
| ElevenLabs | Account library, verified-language metadata and TTS | API key, account plan, voice-specific rights and language support apply |

**Important catalogue distinction:** VoiceStudio's language support is not the
same as its number of ready-made speaker identities. Its current built-in
combinatorial archetype catalogue is mainly English and Chinese, with a small
curated subset in other languages; do not claim hundreds of ready-made
Vietnamese archetypes. For Vietnamese original synthetic profiles, use an
engine that supports Vietnamese voice design (for example VoxCPM2, subject to
engine availability and rights review) and save the result as a VoiceStudio
profile.

KorvaTTS is installed only when selected:

\`\`\`bash
python -m pip install "korvatts==0.1.3"
\`\`\`

Its official API loads one CPU model, exposes the ten bundled IDs through
\`list_voices()\`, and supports a fixed seed, 1–32 inference steps and speed
from 0.5 to 2.0. The adapter pins CPU inference and caches the model object for
the batch, rather than reloading it for every utterance.

Other optional provider installs:

\`\`\`bash
python -m pip install google-cloud-texttospeech
\`\`\`

Google credentials use Application Default Credentials. ElevenLabs reads
\`ELEVENLABS_API_KEY\`. Keep all credentials in local secret stores, never in
manifests or Git.

## 3. Create a reusable Nolane voice set

The repository includes an original Vietnamese voice-design set:
\`examples/vietnamese-original-voice-set.json\`. It defines five fictional
speaker identities with different timbre, delivery, and seed settings. It uses
the exact engine ID \`voxcpm2\`; change that only to an installed engine that
declares native voice-design support.

First create a plan. This makes no API calls and changes nothing in VoiceStudio:

\`\`\`bash
python integrations/voice-studio/design_voice_library.py \\
  --manifest integrations/voice-studio/examples/vietnamese-original-voice-set.json \\
  --output out/nolane-vietnamese-voices
\`\`\`

After reviewing the plan, create the profiles and render their sample clips:

\`\`\`bash
python integrations/voice-studio/design_voice_library.py \\
  --manifest integrations/voice-studio/examples/vietnamese-original-voice-set.json \\
  --output out/nolane-vietnamese-voices --create
\`\`\`

This calls VoiceStudio's native \`POST /profiles\` design path with a validated
recipe, exact engine ID, language and seed. The service stores a reusable
profile ID. The first profile-audio request lazily renders the identity sample.
The local \`voice-design-library.json\` records names, profile IDs, description
fingerprints, preview status and failures. Rerunning against the same output
directory reuses profiles already recorded there; it does not recreate them.

To create the profiles but defer expensive preview/model loading:

\`\`\`bash
python integrations/voice-studio/design_voice_library.py \\
  --manifest integrations/voice-studio/examples/vietnamese-original-voice-set.json \\
  --output out/nolane-vietnamese-voices --create --no-preview
\`\`\`

The profile IDs from the report are the values to put in the cast. A seed
provides reproducible sampling; it does not by itself guarantee perfect
speaker identity, naturalness or identical prosody on every long passage.

## 4. Audition and choose voices

List the current VoiceStudio engines, saved profiles and archetypes:

\`\`\`bash
python integrations/voice-studio/voice_catalog.py --provider voicestudio --language vi
python integrations/voice-studio/voice_catalog.py --provider korva --language vi
python integrations/voice-studio/voice_catalog.py --provider google --language vi-VN
python integrations/voice-studio/voice_catalog.py --provider elevenlabs --language vi
\`\`\`

Build a local gallery from saved profiles and previews:

\`\`\`bash
python integrations/voice-studio/voice_audition.py \\
  --source profiles --language vi --limit 40 \\
  --output out/voice-auditions
\`\`\`

For an A/B comparison, use the exact same script and engine across saved
profiles, and hide their names while listening:

\`\`\`bash
python integrations/voice-studio/voice_audition.py \\
  --source profiles --language vi \\
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \\
  --engine voxcpm2 --blind \\
  --output out/voice-a-b
\`\`\`

Open \`out/voice-a-b/index.html\` locally. The blind page labels candidates
rather than revealing profile names/IDs. The JSON report retains the mapping
so the listener can reveal the selected voice after the comparison. A blind
listening test is a selection aid, not an automatic quality score.

The benchmark includes Vietnamese initial consonants, tone contrasts, numbers,
names and English terms embedded in Vietnamese. Use the *same text* when
comparing models or voice profiles; otherwise the A/B result is confounded by
different scripts.

Compare a whole provider's catalogue on that same benchmark script:

```bash
python integrations/voice-studio/provider_voice_benchmark.py \
  --provider korva --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --language vi --limit 10 --output out/benchmark-korva

python integrations/voice-studio/provider_voice_benchmark.py \
  --provider voicestudio --engine voxcpm2 \
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --language vi --limit 20 --output out/benchmark-voicestudio

python integrations/voice-studio/provider_voice_benchmark.py \
  --provider google --allow-cloud \
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --language vi-VN --limit 20 --output out/benchmark-google

python integrations/voice-studio/provider_voice_benchmark.py \
  --provider elevenlabs --allow-cloud \
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --language vi --limit 20 --output out/benchmark-elevenlabs
```

Google and ElevenLabs calls can incur charges; the explicit `--allow-cloud`
flag is mandatory. Each run exports an identity-mapped JSON report and a
blind listening page. Rate naturalness, Vietnamese clarity/tones, identity,
expressiveness and character fit from 1–5, then click **Export human ratings
JSON**. The ratings are subjective review evidence, not a validated
ElevenLabs-equivalence percentage.

## 5. Lock a cast and generate the voice-over

Use a top-level \`cast\` object to declare each character's voice once. Every
line references a \`speaker_id\`. The generator fingerprints provider, engine,
voice/profile ID, language, description/instruct, seed and settings; it stops
if the same speaker ID silently changes voice identity.

\`examples/voice-casting-template.json\` shows the structure. A shortened
example:

\`\`\`json
{
  "language": "vi",
  "cast": {
    "narrator": {
      "provider": "korva",
      "voice": "khanh_vy",
      "language": "vi",
      "seed": 4201
    },
    "expert": {
      "provider": "voicestudio",
      "engine": "voxcpm2",
      "voice": "PASTE_SAVED_PROFILE_ID",
      "language": "vi",
      "seed": 4202
    }
  },
  "segments": [
    {"id": "V001", "speaker_id": "narrator", "slot": "NARRATOR", "text": "Lời dẫn..."},
    {"id": "V002", "speaker_id": "expert", "slot": "EXPERT", "text": "Lời chuyên gia..."},
    {"id": "V003", "speaker_id": "narrator", "slot": "NARRATOR", "text": "Lời dẫn tiếp..."}
  ]
}
\`\`\`

Plan without calling a provider:

\`\`\`bash
python integrations/voice-studio/generate_voiceover.py \\
  --manifest integrations/voice-studio/examples/vietnamese-documentary.json \\
  --output out/voiceover --plan-only
\`\`\`

Generate:

\`\`\`bash
python integrations/voice-studio/generate_voiceover.py \\
  --manifest integrations/voice-studio/examples/vietnamese-documentary.json \\
  --output out/voiceover
\`\`\`

The batch:

- Generates one MP3/WAV per dialogue segment.
- Caches by text + provider + model + voice + seed + synthesis settings.
- Writes progress after each segment; on one failed segment it records the
  error and continues with the rest. Re-running reuses successful cache items.
- Writes \`voice-generation-report.json\` with profile identity, expected text,
  audio path, byte count and SHA-256.
- Writes \`02-VOICE-<project>-TTS.txt\` in the exact block format read by the
  existing H2 \`prep_voice.py\`. That tool remains responsible for creating
  \`voice.wav\`, \`blocks.json\`, \`lines.json\`, \`words.json\` and
  \`transcript.txt\`.

## 6. Audio and intelligibility QA

Run technical analysis on the generated report:

\`\`\`bash
python integrations/voice-studio/voice_quality.py \\
  --report out/voiceover/voice-generation-report.json
\`\`\`

For an ASR round-trip (requires a working ASR engine already configured in
VoiceStudio):

\`\`\`bash
python integrations/voice-studio/voice_quality.py \\
  --report out/voiceover/voice-generation-report.json --asr --language vi
\`\`\`

The quality report measures technical signals such as duration, sample rate,
peak/RMS, clipping and near-silence. Optional WER/CER compares the generated
audio's ASR transcript with the expected script. **WER/CER is only an
intelligibility/pronunciation proxy**; it does not grade timbre, naturalness,
emotion, acting, speaker similarity or whether a voice fits a scene.

Human listening remains mandatory. Review Vietnamese tones, final consonants,
proper names, numbers, pauses, emotional arc, long-form identity consistency
and differences between characters. Keep a human-approved voice-cast manifest
for each series.

## 7. Connect to the H2 / Remotion production pipeline

The generator outputs a ready-to-use H2 voice block file and individual
segment audio. Run the existing H2 timing stage with the actual tool path
recorded in the report:

\`integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit/tools/prep_voice.py\`.

The video renderer still owns the final timing, subtitle alignment, sound mix
and master. TTS generation is not the final audio master.

## 8. Rights, licensing and consent

- VoiceStudio application code is AGPL-3.0. Keep it as a separate submodule
  and comply with AGPL obligations if you distribute a modified network
  service.
- VoiceStudio model rights are separate from the app license. The current
  fork's registry shows OmniVoice weights in a CC-BY-NC family with additional
  tokenizer/component terms. Do not assume it is cleared for monetized video.
- VoxCPM2 is a promising Vietnamese voice-design/clone engine. Its upstream
  model card identifies Apache-2.0, but VoiceStudio's own audit marks component
  closure incomplete and generated-output terms not specifically granted in
  the reviewed evidence. Verify the installed revision, every required
  component, attribution/NOTICE and intended distribution before commercial use.
- KorvaTTS source and model weights are published under Apache-2.0. Its ten
  shipped voices are presets; custom cloning/training is not yet part of the
  released upstream implementation.
- Google Cloud and ElevenLabs are subject to current service plans, voice
  permissions and provider terms. A public voice-library item is not blanket
  permission to impersonate a real person.
- Do not clone a real person's voice without documented consent and the rights
  needed for the intended output. Store consent evidence and source recordings
  privately, outside Git and outside public Releases.

## 9. Tests and honest limits

CI checks the integration logic, API request formatting, cast identity locks,
batch recovery, H2 handoff grammar, audition page escaping and Vietnamese
text-comparison logic using mocks. CI does **not** download weights, call paid
APIs, render audio or claim a naturalness score.

A live acceptance pass still requires a reachable VoiceStudio service, an
installed/licence-accepted engine, actual profile creation, rendered Vietnamese
samples, ASR checks and human listening. No claim is made that this matches
ElevenLabs; this workflow creates a measurable, repeatable path to improve
and compare each voice set.
