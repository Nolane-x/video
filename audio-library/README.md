# Nolane Audio Library — curated, searchable and rights-aware

This folder is the production-facing map for sound resources. It does not duplicate the global video-library asset pipeline and does not publish third-party binary assets by default.

## Existing sound resources already published

The Build 76 asset-library Release already contains these audio archives:

| Archive | Size (bytes) | Source family / role | Distribution note |
|---|---:|---|---|
| video-assets-kenney-audio-001.zip | 1,724,247 | Kenney recorded game/UI/impact/ambience SFX | Per-source record; Kenney audio packs are generally CC0 |
| video-assets-opengameart-audio-001.zip | 462,854,835 | OpenGameArt SFX/music/foley | License is per item; do not infer one license for the complete ZIP |
| video-assets-originals-audio-001.zip | 33,910,385 | Original assets made for this repo | Repository provenance and asset-specific terms |
| video-assets-usgs-audio-001.zip | 456,076,826 | USGS environmental/geological recordings | Public-domain/source-use checks are per item |
| video-assets-nasa-audio-001.zip | 165,256,750 | NASA-origin space/mission/environmental audio | NASA media guidance applies; not labelled CC0 automatically |
| video-assets-wikimedia-audio-001.zip | 17,840,331 | Wikimedia audio | Exact file license and attribution per record |

Total published audio archive size: **1,137,? bytes (about 1.14 GB)**. These files are already in the public [Build 76 Release](https://github.com/Nolane-x/video/releases/tag/video-asset-library-build-41184526545). The asset library's cumulative deduplicated index is much larger; do not download or repackage it wholesale for every film.

The URLs and exact byte counts are machine-readable in [SOURCES.json](SOURCES.json). This source map is a starting point, not proof that every sound is appropriate for a specific film. Before a sound enters a final mix, resolve its exact source record, rights, attribution, identity, technical properties and audition status.

## Production-first policy

**Audition the recordings before synthesizing.** The library is searched first for every shot. A new web download is justified only when the library lacks a suitable recording or the match is materially poor.

1. Search by sound function and physical material, not only by the script's noun: for example samurai armor cloth movement, metal blade unsheathe, wooden geta footsteps, horse tack, rain on castle roof, crowd distant, arrow flight, temple bell.
2. Find multiple candidates and inspect their metadata. Listen to each candidate; tags and filenames are not enough.
3. Use different takes/layers for repeated actions, and do not reuse one generic whoosh/impact through an entire battle.
4. Align spot Foley to the action's anticipation, contact, consequence and recovery. Place sound in perspective with distance, stereo width, reverb and occlusion.
5. Keep voice, score, ambience, Foley, weapons/impacts, crowd/animals and transitions as separate stems until final mastering.
6. Silence is intentional. Do not fill every gap with procedural drone or generic music.

## License classes

- **Redistributable:** exact record says CC0 or an otherwise verified license permitting raw-file redistribution; keep the license notice and attribution.
- **Use-in-final-film / source-only:** terms allow synchronization into the finished video but prohibit redistributing the raw audio as a sound library. Keep the source file private and only include the finished mix in the video output.
- **Attribution required:** exact CC BY notice and attribution text travel with the project and publication package.
- **Review required:** unclear, mixed, conflicting, NC, ND, missing or unverified rights. Do not use until resolved.

Sonniss GDC packs are not a public-library source: their current license permits use synced to films/videos but restricts standalone redistribution as a sound library and prohibits AI training. Keep files private and use only under the actual current terms. Mixkit/Pixabay can be source-only for final creative works where the relevant license allows; never mirror their files as a public downloadable library. Freesound requires per-record license/attribution checks.

## External source candidates

See [SOURCES.json](SOURCES.json) for:
- Meta Open Sound: CC0 instrument sample sets and an Oculus Audio Pack whose license is CC BY 4.0.
- Open Game SFX Index: a curated index of 1,451 CC0 SFX from Kenney/OpenGameArt. It overlaps with the repo's existing libraries, so deduplicate before importing.
- Sonniss GDC: private source-only use; no public mirror and no AI-training use.
- Mixkit/Pixabay: use only in the finished film under the applicable terms, never as raw downloadable library distribution.
- Freesound: per-file licensing and attribution; do not batch-import without record checks.

## Required record schema

Each final audio cue must carry: asset_id, title, category, tags, archive_name, archive_member or exact download URL, source_url, license_id, license_url, attribution_text, redistributable, sha256, duration, sample rate, bit depth, channels, peak/RMS/loudness, and audition status. Missing rights or missing audition is a blocker for final publication.

## What this library is not

- It is not a claim that the entire 1.14 GB collection has been auditioned.
- It is not a single blanket CC0 grant for all Build 76 archives.
- It is not a collection of oscillator-generated placeholder WAVs.
- It does not modify the parallel global asset-library workflow or its ownership boundary.
