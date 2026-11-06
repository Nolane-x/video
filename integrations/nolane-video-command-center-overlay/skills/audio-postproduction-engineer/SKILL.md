---
name: audio-postproduction-engineer
description: Use when editing narration, selecting or recording real music and sound effects, cleaning dialogue, designing sound, balancing stems or mastering a video soundtrack.
---
# Audio Postproduction Engineer

## Library-first source selection
1. Read `audio-library/README.md`, `audio-library/SOURCES.json`, `audio-library/generated/preview-catalog.json` and `audio-library/generated/meta-preview-catalog.json` before downloading or unpacking media.
2. Search the generated indexes for Build 76 and Meta Open Sound candidates; inspect rights class, source, hash, tags and technical metadata, then audition suitable previews.
3. For Build 76, use the 2,331 playable redistribution candidates first; do not default to 110 rights-review entries or 5 source-specific items.
4. Meta Open Sound has 1,075 CC0 instrument samples and 508 CC BY 4.0 Oculus Foley/ambience samples. The latter require the exact Oculus Audio Pack attribution in publication credits. The instruments are individual note samples, not finished music tracks.
5. Use OGG samples for discovery/listening and the linked WAV masters for high-quality production when selected and legally eligible.
6. Search the existing Build 76 Kenney, OpenGameArt, USGS, NASA, Wikimedia and original-audio archives before downloading new sounds.
7. Search by physical material, action, environment, perspective and emotion. Use aliases and synonyms; don't rely on one exact keyword.
8. Compare several candidates and **audition** them. Tags and filenames are search hints, not proof of what the sound contains.
9. Record exact asset/source ID, file path/archive member, original source URL, license, attribution, SHA-256, duration, sample rate, bit depth, channels and human audition status.
10. Fetch only genuinely missing material from an external source after a specific need is established. Keep source-only/private recordings outside public redistribution bundles.
1. Read the repository audio-library README, source catalogue, asset index and the focused historical audio map when available.
2. Search the existing Build 76 Kenney, OpenGameArt, USGS, NASA, Wikimedia and original-audio archives before downloading new sounds.
3. Search by physical material, action, environment, perspective and emotion. Use aliases and synonyms; don't rely on one exact keyword.
4. Compare several candidates and **audition** them. Tags and filenames are search hints, not proof of what the sound contains.
5. Record exact asset/source ID, file path/archive member, original source URL, license, attribution, SHA-256, duration, sample rate, bit depth, channels and human audition status.
6. Fetch only genuinely missing material from an external source after a specific need is established. Keep source-only/private recordings outside public redistribution bundles.

## Soundscape and stems
Treat sound as intentional separate layers: narration/dialogue, score, location ambience, environmental detail, footsteps/cloth/armor Foley, weapons/impacts, crowds/animals, transitions and special accents. Keep stems separate until mastering. Use multiple takes/layers for repeated prominent actions where available.

Match material and perspective. A close unsheathing needs friction and scabbard detail; a large metal clash needs transient, weight and body reaction; footsteps vary by surface; distant troops are diffuse and low-passed relative to close action. Align transients to contact frames. Let ambience bridge cuts with J/L edits. Preserve silence.

For historical films, search specifically for horse gaits/hoof surfaces/tack, sword draw/clash/scrape, chainmail/armor, shields, bows/arrows, commands/crowds, rain/wind/fire, ship timber/rigging/oars, market/workshop sounds, paper/scroll, doors and period-context music. Distinguish a real historical field recording from modern Foley and from an evocative score; do not claim historical authenticity without evidence.

## Synthesis policy
Prefer authentic recordings, field recordings, licensed music/stems or correctly licensed samples. Do not make oscillator-generated music, generic synthetic Foley or fake crowd beds the default. Code may select, synchronize, layer, loop, pan, EQ, compress, duck, reverberate and master real recordings. Procedural audio may serve as a temporary animatic placeholder or a documented creative exception; a final candidate must replace it with an auditioned recording or document a specific legal/availability exception.

## Dialogue-first post
Inspect clipping, noise floor, plosives, mouth clicks, hum, reverb and inconsistent distance. Repair conservatively; preserve consonants and natural dynamics. Duck score around dialogue smoothly without flattening the emotional arc.

## Rights and delivery
- CC0 or Public Domain sources: verify exact item record and retain provenance.
- CC BY: preserve exact attribution text in publication credits.
- Source-only/project-use licenses (including relevant Mixkit stock): synchronize into the finished video only where permitted; do not redistribute raw files.
- Private bundles such as Sonniss GDC: follow the exact current EULA; do not publicly mirror/resupply raw sounds, and obey any AI/ML-training prohibition.
- Freesound: verify each file's license; reject NC/ND when commercial or derivative rights are required.
- A repository or pack license never grants rights to every media file inside it.
- Export separate PCM stems plus a full mix/master. Measure integrated loudness, LRA, true peak and clipping after processing. Listen to the complete programme at normal speed and log issues.
