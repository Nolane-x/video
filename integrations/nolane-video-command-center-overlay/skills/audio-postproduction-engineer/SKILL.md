---
name: audio-postproduction-engineer
description: Edit narration, select and mix real music/sound recordings, design shot-synced Foley, manage stems and master a finished video soundtrack.
---
# Audio Postproduction Engineer

## Source-first workflow
1. Read audio-library/README.md, SOURCES.json, the Build 76 preview catalogue and Meta Open Sound preview catalogue.
2. Search with python tools/audio/search_audio_resources.py by action, material, surface, distance and emotion. Use --kind foley or --kind instrument and --direct-only for strict matching.
3. Consult the historical Foley coverage audit and the illustrated-history CC0 acquisition record.
4. Compare and listen to multiple exact files. A filename, source tag or FFprobe result is not a listening approval.
5. Use the original WAV/source master for selected high-value cues when available; retain source path/member, creator, license, attribution, hash and technical metadata.
6. Keep source-only/private raw assets out of public releases. Never treat a pack-wide license as proof for every file.

## Targeted historical sources
The workflow .github/workflows/build-illustrated-history-foley-library.yml builds the CC0 release from item-level sources recorded in tools/audio/illustrated_history_foley_sources.json. It covers weapon draw/sheath and bow/arrow handling, weapon-on-weapon impacts, a six-horse approach/pass gallop, a designed crowd shout, a forge hammer/anvil hit and generic impacts. Confirm that the Actions run succeeded and the release exists before use.
Do not claim this source pack includes surface-specific cavalry gait round-robins, horse tack, shield-on-shield impacts or chainmail Foley; those remain gaps. Keep all pack entries marked not human-auditioned until reviewed.

## Cue architecture and physical sync
Separate:
- narration/dialogue;
- score;
- location ambience and room/air tone;
- environmental layers (wind, rain, water, fire, birds);
- character Foley (steps, clothing, breathing, armour);
- prop Foley (leather, wood, paper, metal, tools);
- action spot effects (weapons, arrows, impacts, boats);
- transition accents and intentional silence.

Match material and perspective. A close unsheathing needs friction and scabbard detail. A blade contact needs transient, weight and a response/recoil. Footsteps vary by surface. Distant troops are diffuse and filtered relative to a foreground action. Align transients to the exact contact frame. Use ambience J/L edits to bridge cuts; preserve screen-space perspective and silence.

## Mix and mastering
- Keep stems separate through editorial and mix.
- Use volume automation and gentle ducking around narration; do not flatten score dynamics.
- Vary repeated prominent sounds with alternate takes, timing and perspective.
- Measure integrated loudness, loudness range, true peak and clipping, but treat those as technical checks only.
- Export a full mix and separate PCM stems with cue and rights sheets.
- Review the complete soundtrack at normal speed and log every audible issue with timecode.

## Synthesis policy
Prefer field/foley recordings, licensed stems and properly licensed sample performances. Code should select, synchronize, layer, loop, pan, EQ, compress, duck, reverberate and master recordings. Do not make oscillator music, generic synthetic Foley or generated crowd beds the default. Procedural audio is an animatic placeholder or documented creative exception; replace it before final delivery unless no lawful, suitable recording exists.

## License handling
- CC0/Public Domain: verify the exact source page and retain its creator/provenance record.
- CC BY: include the exact attribution in end credits/description.
- Project-use/private stock: follow exact terms and do not redistribute raw assets.
- Sonniss GDC: private cache only under the current EULA; never place raw files in public GitHub releases or shared asset packs.
- NASA: follow item-specific NASA Media Usage Guidelines and credit; not CC0.
