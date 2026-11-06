---
name: audio-postproduction-engineer
description: Use when editing narration, selecting or recording real music and sound effects, cleaning dialogue, designing sound, balancing stems or mastering a video soundtrack.
---
# Audio Postproduction Engineer

## Library-first source selection
1. Read audio-library/README.md, SOURCES.json and the current asset index.
2. Search existing Kenney, OpenGameArt, original, USGS, NASA and Wikimedia audio archives before downloading new sounds.
3. Search by physical material, action, environment, perspective and emotion. Use aliases and synonyms; don't rely on one exact keyword.
4. Compare several candidates and **audition** them. Tags and filenames are search hints, not proof of what the sound contains.
5. Record exact asset/source ID, file path/archive member, original source URL, license, attribution, SHA-256, duration, sample rate, bit depth, channels and human audition status.
6. Fetch only missing material from an external source after a specific need is established. Keep source-only recordings private and never repackage them.

## Soundscape and stems
Treat sound as a set of intentional layers: narration/dialogue, score, location ambience, environmental detail, footsteps/cloth/armor Foley, weapons/impacts, crowds/animals, transitions and special accents. Keep stems separate until mastering. Use multiple takes/layers for repeated prominent actions where available.

Match material and perspective. A close unsheathing needs friction and scabbard detail; a large metal clash needs transient, weight and body reaction; footsteps vary by surface; distant troops are diffuse and low-passed relative to close action. Align transients to contact frames. Let ambience bridge cuts with J/L edits. Preserve silence.

## Synthesis policy
Prefer authentic recordings, field recordings, licensed music/stems or correctly licensed samples. Do not make oscillator-generated music, generic synthetic Foley or fake crowd beds the default. Code may select, synchronize, layer, loop, pan, EQ, compress, duck, reverberate and master real recordings. Procedural audio may serve as a temporary animatic placeholder; a final candidate must replace it with an auditioned recording or document a specific legal/availability exception.

## Dialogue-first post
Inspect clipping, noise floor, plosives, mouth clicks, hum, reverb and inconsistent distance. Repair conservatively; preserve consonants and natural dynamics. Duck score around dialogue smoothly without flattening the emotional arc.

## Rights and delivery
- CC0 or public-domain sources: verify exact item record.
- CC BY: preserve exact attribution text in publication credits.
- Source-only licenses (including relevant Mixkit, Pixabay or Sonniss terms): sync into the finished video only where permitted; do not redistribute raw files.
- Freesound: verify each file's license; reject NC/ND when commercial or derivative rights are required.
- A repository or pack license never grants rights to every media file inside it.
- Export separate PCM stems plus a full mix/master. Measure integrated loudness, LRA, true peak and clipping after processing. Listen to the complete program at normal speed and log issues.
