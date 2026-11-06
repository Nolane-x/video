---
name: historical-audio-library-curator
description: Curate and select recorded Foley, ambience, music and SFX for historical films with item-level license, provenance and audition records.
---
# Historical Audio Library Curator

Recorded/licensed sound is the default. Procedural WAV presets are placeholders or supplemental accents, not the main soundscape.

## Fast local search before downloads

- Search `audio-library/generated/preview-catalog.json` for Build 76 playable candidates and `audio-library/generated/meta-preview-catalog.json` for Meta Open Sound samples before unpacking archives.
- Use category/tags, title, creator, source and `rights_class` to shortlist. These records do not prove a sound fits the film; audition candidates before selection.
- Build 76 currently has 2,446 inventoried items; 2,331 are redistributable candidates with playable previews, 110 require rights review and 5 require source-specific review. Do not use the 115 review entries by default.
- Meta Open Sound currently has 1,583 OGG previews: 1,075 CC0 instrument samples and 508 CC BY 4.0 Oculus Foley/ambience samples. Preserve the exact Oculus attribution. A sample bank is not 1,583 complete music tracks.
- Download the entire audio preview artifact only when broad listening is necessary; otherwise fetch the relevant source pack/member to save bandwidth.

## Unified search CLI

Use `python tools/audio/search_audio_resources.py --query "katana sword clash"` for both generated catalogs. Use `--kind foley` or `--kind instrument` to separate recorded effects from multisampled notes, `--json` for structured results, and `--include-review-required` only for investigating quarantined candidates. Results with `match_quality=direct` match the title/category/file; `tag_assisted` are broader keyword suggestions. Add `--direct-only` when the context must match exactly. Search never grants approval: every returned item still has an audition and rights gate.
## Historical coverage audit

Before designing a historical battle soundscape, read `docs/audio/HISTORICAL_FOLEY_COVERAGE_AUDIT.md`. It separates direct catalogue matches from generic tag suggestions and lists the missing hoofbeat, cavalry, bow/arrow, armor and battlefield-crowd families.

## Search and audition
- Read audio-library/README.md, audio-library/SOURCES.json and docs/audio/HISTORICAL_SOUND_LIBRARY.md.
- Search by material, action, environment, distance and emotion. Prioritise horses/hooves/tack, blades/armor/shields/bows/arrows, crowds/commands, rain/wind/fire/water, ships/rigging/oars, steps, markets/workshops, paper/wood/metal and historically appropriate music textures.
- Inspect exact per-item source and license metadata. Audition several candidates; filenames and tags are not evidence of sound quality.
- Record asset ID, title, creator, semantic tags, archive/member path, source page, exact file URL, SHA-256, duration, channel/sample-rate/bit-depth data, loudness/peak, rights class and human audition status.

## OGG preview to verified WAV master

The Meta Open Sound catalog links each OGG preview to its exact WAV member through `source_wav_file`, master archive name, size and SHA-256. Search and audition OGG first; fetch a master only after choosing a cue. Oculus WAV is mirrored in the permanent Nolane release. Fetch Piano/Nylon/Steel masters only as needed using `.github/workflows/acquire-meta-open-sound-wav-master.yml`; the workflow verifies archive bytes and SHA-256. Extract the exact original WAV member, retain its metadata and apply the collection-level rights correctly (Oculus CC BY 4.0; instrument collections CC0).

## Rights classes
- public_cc0_pd: redistributable only after exact item-level CC0/Public Domain proof and required attribution is retained.
- project_use_only: may be synchronized into a finished film under exact item terms; raw source cannot be redistributed.
- private_production_only: private licensed cache; never add raw media to public GitHub packs.
- blocked: unclear, conflicting or unsuitable rights; do not use.

NASA media belongs in government_media_conditions: apply item-level NASA Media Usage Guidelines, retain credit and do not imply endorsement; it is not labelled CC0. Sonniss GDC 2026 is private_production_only. Its current EULA v2.0 permits film/TV synchronization, commercial projects and modifications in the production, but prohibits selling raw files as supplied and all AI/ML training. The licensee must review and accept the EULA before downloading. Never upload Sonniss ZIPs or extracted WAVs to this public repo, public Releases, public Actions artifacts or redistributable preview packs; keep the raw source in private production storage and retain only sanitized metadata/cue decisions here. Mixkit is item/license-specific and source-only by default. Do not confuse software or collection licenses with an individual media file's license.

## Editorial use
Create separate narration, score, ambience, character Foley, prop Foley, spot SFX, transition and intentional-silence tracks. Sync transients to visible contact; layer near/far perspective; do not reuse one generic clang for every hit. Listen to the complete final film at normal speed. Loudness/metadata checks do not replace human audition.
