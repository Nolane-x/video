---
name: video-voice-design-director
description: Design, curate and create original synthetic character voices using VoiceStudio, KorvaTTS and approved TTS providers. Use when a project needs a new narrator, host, expert, character voice set or reusable series cast.
---

# Video Voice Design Director

## Mission

Create a small, distinctive, reusable cast of voices that serves the story. Do not maximize voice count for its own sake. Every designed voice needs a clear dramatic function, an audible distinction from the other cast members, a repeatable identity and a lawful source/model path.

VoiceStudio is the voice-management and rendering core. The video repo owns the casting brief, original profile manifests, audition records, usage notes and continuity across episodes. Do not recreate VoiceStudio's desktop studio or duplicate its internal backend.

## Mandatory source and rights gate

1. Read `integrations/voice-studio/README.md` and `integrations/voice-studio/VOICE_STUDIO_LOCK.json`.
2. Discover the actual installed engines with `voice_catalog.py --provider voicestudio`. Documentation alone is not proof that an engine is installed or available on the current machine.
3. Check the exact installed model and all required components in VoiceStudio's model acceptance/licence registry before creating profiles or generating any audio.
4. Treat the VoiceStudio app licence, model weights, tokenizers/codecs, reference recordings, voice identity, generated outputs and commercial use as separate rights questions.
5. Do not claim commercial/monetization clearance for VoxCPM2 while its component closure/output terms remain unresolved in the current reviewed inventory. Do not use default OmniVoice CC-BY-NC weights for monetized work without an independent clearance.
6. Cloning a real speaker requires documented authorization for the reference and the intended use. Never clone a public figure, creator, colleague, celebrity or private person merely because a clip is available. For a character, prefer an original fictional design.

## Choose the right source

- **VoiceStudio native Voice Design:** original fictional identities from a descriptive recipe; choose only an installed engine declaring voice-design support.
- **VoiceStudio reference cloning:** preserve a consenting speaker's voice; use only a clean, authorized reference recording and keep its consent record private.
- **VoiceStudio archetypes:** fast starting points for curated or combinatorial profiles. Do not describe the current catalogue as hundreds of ready-made Vietnamese voices; its combinatorial coverage is mainly English and Chinese with a smaller multilingual subset.
- **KorvaTTS:** ten Vietnamese presets for low-resource local use. They are useful baselines, not unlimited custom voices. Upstream cloning/training is not shipped in the reviewed version.
- **Google Cloud / ElevenLabs:** provider libraries discovered at runtime. Verify voice language and account permissions; some calls may incur cost.

## Design a voice identity

For each character, write a private casting brief with:
- story role and point of view;
- age *as a fictional vocal performance descriptor*, not a guess about a real speaker;
- register and timbre (low/medium/high, warm/bright/airy/rough/rounded);
- articulation and Vietnamese dialect/pronunciation target;
- pace, pause behaviour, energy and emotional range;
- what the voice must not sound like (for example: not a commercial announcer, not theatrical, not exaggerated);
- scenes where the voice must stay calm, become tense, or soften.

Use descriptions that control several independent dimensions, not adjective piles. A useful design brief distinguishes the voice through both sound and performance: e.g. “warm low-mid register, grounded resonance, measured documentary pacing, precise final consonants, restrained confidence.” Avoid contradictory instructions such as “very low, very high, soft, forceful, slow and extremely fast.”

Prefer 3–8 strong core characters per series over a huge undifferentiated catalogue. Make two voices differ on at least two audible dimensions (register/timbre, rhythm, articulation, energy). Do not rely on gender labels alone.

## Create the native profile set

Start with a plan. It must not contact the synthesis API:

```bash
python integrations/voice-studio/design_voice_library.py \
  --manifest integrations/voice-studio/examples/vietnamese-original-voice-set.json \
  --output out/voice-library
```

Inspect:
- engine is installed and supports Voice Design;
- language is supported by that exact engine;
- each name is unique;
- seed values are distinct;
- each sample script is identical for direct comparisons;
- descriptions are clearly fictional and not requests to emulate a named person.

Only after those gates pass, create profiles:

```bash
python integrations/voice-studio/design_voice_library.py \
  --manifest integrations/voice-studio/examples/vietnamese-original-voice-set.json \
  --output out/voice-library --create
```

To create profile records but defer model/sample rendering, use `--create --no-preview`. If the preview fails, the report must say partial/pending; never label an unrendered profile as audition-ready. The factory persists a `voice-design-library.json` report and exports `voice-cast.json` containing the real saved profile IDs, engine, language and seed. Re-running with the same output directory reuses recorded profiles rather than creating duplicates.

## Audition and curate

Use a single fixed benchmark script for every candidate. Do not compare two voices using different text, speed, language, engine settings or emotional instruction and then attribute the difference to timbre.

Build a VoiceStudio profile gallery:

```bash
python integrations/voice-studio/voice_audition.py \
  --source profiles --language vi --limit 40 --output out/voice-auditions
```

Compare profiles with the same script and engine:

```bash
python integrations/voice-studio/voice_audition.py \
  --source profiles --language vi --engine voxcpm2 \
  --text-file integrations/voice-studio/examples/vietnamese-pronunciation-benchmark.txt \
  --blind --output out/voice-a-b
```

The profile's stored seed should be respected; do not overwrite it merely to make the audition deterministic. Blind listening hides profile names/IDs from the listener. Keep the identity mapping in the private report until selection is complete.

## Acceptance before adding a voice to the series cast

A candidate is not “approved” just because VoiceStudio returned HTTP 200 or audio bytes exist. Require:
- a playable sample;
- correct Vietnamese tone/initial/final consonant pronunciation;
- natural rhythm and phrase endings;
- audible distinction from the existing cast;
- a suitable emotional range for the intended scenes;
- acceptable long-phrase stability;
- profile ID, engine, model revision/rights notes and seed recorded;
- human listening sign-off.

Store a short voice-cast card: profile ID, character ID, intended use, pronunciation notes, allowed performance range, model/source, rights status and approval date. Keep real-speaker consent records private and outside Git.

## Output

Deliver:
1. voice design manifest;
2. profile factory report and generated `voice-cast.json`;
3. audition samples and blind human ratings;
4. selected/declined candidate rationale;
5. model/voice rights gate status;
6. a short note identifying anything not tested on real hardware.

Never invent profile IDs, claim a preview rendered if it did not, or declare a model cleared because the app itself is AGPL/Apache licensed.
