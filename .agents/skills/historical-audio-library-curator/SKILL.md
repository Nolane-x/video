---
name: historical-audio-library-curator
description: Curate and select recorded Foley, ambience, music and SFX for historical films with item-level license, provenance and audition records.
---
# Historical Audio Library Curator

Recorded/licensed sound is the default. Procedural WAV presets are placeholders or supplemental accents, not the main soundscape.

## Fast local search before downloads
- Search audio-library/generated/preview-catalog.json and audio-library/generated/meta-preview-catalog.json before unpacking archives.
- Use category/tags, title, creator, source and rights_class to shortlist. Metadata does not prove audible content; audition candidates before selection.
- Build 76 currently has 2,446 inventoried items: 2,331 redistribution candidates, 110 rights-review items and 5 source-specific-review items. Do not use the 115 review entries by default.
- Meta Open Sound has 1,583 OGG previews: 1,075 CC0 instrument samples and 508 CC BY 4.0 Oculus Foley/ambience samples. Keep the exact Oculus attribution. Instrument note samples are not finished music tracks.

## Unified search CLI
Use python tools/audio/search_audio_resources.py --query "katana sword clash". Filter with --kind foley or --kind instrument, --json for structured results, --direct-only for strict title/category/file matches and --include-review-required only to investigate quarantined candidates. Tag-assisted results are leads, not proof of historical fit.

## Historical coverage and targeted Foley acquisition
Read docs/audio/HISTORICAL_FOLEY_COVERAGE_AUDIT.md and docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md before designing battle sound.
The targeted acquisition workflow is .github/workflows/build-illustrated-history-foley-library.yml; its source manifest is tools/audio/illustrated_history_foley_sources.json. It is designed to package CC0 weapon handling/katana/bow/arrow sounds, weapon-on-weapon impacts, a six-horse gallop recording, a designed crowd-shout layer, a blacksmith hammer/anvil hit and generic impacts. Confirm that the Actions build succeeded and the release exists before relying on the pack.
This pack does not solve cavalry gait round-robins by surface, horse tack/reins, dedicated shield-on-shield Foley, chainmail movement, historical command layers or Japanese environmental beds.

## Search, audition and master selection
- Search by material, action, environment, distance and emotion: hooves on dirt/stone/timber, blade draw/clash, shield/spear, armour, bows/arrows, crowd/commands, rain/wind/fire/water, ships/rigging/oars, markets/workshops, scroll/paper and period-relevant music.
- Prefer direct item matches. Audition multiple candidates; filenames/tags do not prove what the sound contains.
- Record asset ID, title, creator, archive/member path, exact source page/file URL, license, attribution, SHA-256, duration, channel/sample-rate/bit-depth data, loudness/peak and human-audition state.
- Meta Open Sound previews map to original WAV members by source_wav_file, master archive, size and SHA-256. Audition OGG first; fetch only the chosen matching WAV master. Oculus is CC BY 4.0 and needs exact attribution; the piano/guitar note-sample collections are CC0, not complete compositions.

## Rights classes
- public_cc0_pd: redistributable only with exact item-level CC0/Public Domain proof and preserved provenance.
- project_use_only: synchronize into a finished video only where exact item terms permit; raw files cannot be redistributed.
- private_production_only: private licensed cache; never add raw files to public packs.
- blocked: unclear, conflicting or unsuitable rights; do not use.
NASA media uses government-specific media conditions and is not labelled CC0. Sonniss GDC 2026 is private_production_only; follow the live EULA, keep raw sources private and obey its AI/ML-training prohibition. Do not confuse a pack/repository license with an individual file's license.

## Editorial use
Separate narration, score, ambience, character Foley, prop Foley, spot SFX, transition and intentional-silence tracks. Sync transients to visible contact; layer near/far perspective; do not reuse one generic clang for every hit. Listen to the complete final mix at normal speed. Metadata and loudness checks do not replace audition.
