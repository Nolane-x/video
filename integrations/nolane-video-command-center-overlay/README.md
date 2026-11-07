# Nolane Video Command Center v1.0.3

One private front door for Nolane video production. It includes **33 internal skills**, **37 core specialist plugins**, and **1 genre-specific H2 Squire specialist** (38 separately activated specialist plugins total).

## What's new in v1.0.3

- Adds a dedicated **illustrated-history-animation-director** for expressive 2D/cartoon history: character rigs, pose-led acting, prop choreography, moving environments, parallax, motivated camera paths, animated maps and information graphics.
- Adds **historical-audio-library-curator** with source-first recorded Foley/ambience/music, rights separation, exact attribution, SHA-256 and human audition gates.
- Adds a detailed illustrated-history motion reference covering character/prop/environment/camera/graphic channels, camera grammar, action cycles, uniqueness checks and full-motion QA.
- Adds the CC0 illustrated-history Foley + Score Audition Edition v0.3.0 with an offline console for listening to individual recordings, filtering, fit ratings, keep/reject notes, browser-local review persistence and JSON export/import.
- Adds a SHA-256-bound review validator that rejects un-auditioned approvals, rejected cues, unknown IDs, duplicate rows and rights-class mismatches before cue-sheet inclusion.
- Adds a five-shot Cannae audio cue map that separates narration, score, ambience, Foley, impacts, transitions and intentional silence without pre-approving any asset.
- Adds searchable metadata indexes for the 2,331 Build 76 redistribution candidates and 1,583 pinned Meta Open Sound samples, then an offline playable audio preview bank.
- Routes sound selection through lightweight catalogs before unpacking source archives, preserving Oculus CC BY 4.0 attribution and CC0 instrument rights.
- Links each Meta OGG preview to its exact WAV master source member, size and SHA-256. The Oculus WAV master is mirrored in the permanent Release; instrument masters can be acquired one collection at a time through GitHub Actions.
- Routes illustrated/cartoon history, footage-led cinematic documentaries and H2 Squire vector history as three separate visual languages.
- Keeps H2 Squire as a separate route only when the user explicitly asks for its symbolic/vector military-history style or an established Squire series.
- Makes full-motion sampling, explicit inspection-scope reporting, source provenance and timecoded audiovisual review mandatory. No workflow success or contact sheet is treated as artistic approval.
- Makes recorded SFX, Foley, ambience and licensed music the default; code synchronizes, layers and masters recordings rather than replacing the soundscape with oscillators.

## Unified audio search

Use `python tools/audio/search_audio_resources.py --query "katana sword clash"` to search Build 76 and Meta Open Sound together. Add `--kind foley` or `--kind instrument` to separate effects from note samples, `--direct-only` to hide tag-only suggestions and `--json` for structured results. Rights-review candidates are excluded by default; no search result bypasses human audition.

## Lossless audio workflow

The Meta catalog maps each OGG preview to `source_wav_file`, WAV archive, download URL and SHA-256. Oculus WAV is in the permanent Nolane audio Release. For Piano/Nylon/Steel, run `.github/workflows/acquire-meta-open-sound-wav-master.yml` and select only the collection required; it verifies file size and SHA-256 before publishing.

## Private production sound sources

The source map also tracks the Sonniss GDC 2026 bundle as `private_production_only`. Its current EULA allows film/video synchronization but prohibits raw-file sale and AI/ML training. Because the main repository is public, never upload Sonniss source archives or loose recordings to public branches, Releases or preview artifacts; only retain sanitized cue metadata. The licensee must accept the EULA before downloading.

## Historical Foley coverage

The plugin bundles `references/HISTORICAL_FOLEY_COVERAGE_AUDIT.md`: current direct matches, broad tag-only suggestions and gaps such as hoofbeats/cavalry, bow/arrow, shield/spear and battlefield crowd cues. For historical Foley searches prefer `--direct-only` and inspect the candidate audio yourself.

The CC0 Foley + Score Audition Edition v0.3.0 adds `AUDIO_PREVIEW.html`. Listen to each exact file, mark it heard and choose keep/reject, fit rating and notes. Export `nolane-foley-review-decisions.json`; browser decisions are local until exported. Validate against the exact package catalog before making a final-mix shortlist:

```bash
python tools/audio/validate_foley_review_decisions.py \
  --catalog package/catalog.json \
  --review nolane-foley-review-decisions.json \
  --output build/foley-review-report.json
```

The Cannae shot-by-shot cue map is `references/CANNAE_45S_AUDIO_CUE_PLAN.json`. It deliberately leaves approved asset IDs empty until human audition.

## How to use

1. Start with the Command Center and describe the story, audience, platform, language, duration and reference.
2. It restores repository/project state and selects the visual route before choosing an engine.
3. For illustrated/cartoon history, use expressive rigs, varied environments, action/prop blocking, parallax and progressive map/graphic reveals. Read the timecoded Samurai reference study.
4. For footage-led cinematic documentaries, it selects real/archive footage, 2.5D/3D reconstruction, camera paths and motion typography per shot.
5. For explicitly requested H2 Squire/vector historical animation, it selects the separate Squire director and host-controlled H2 Squire specialist.
6. Search `audio-library/generated/preview-catalog.json` and `meta-preview-catalog.json` first; audition OGG candidates, then retrieve the exact hash-verified WAV master for a selected cue. Fetch instrument master collections only as needed.
7. Prototype the hardest moving shot and a 30–60 second picture/sound sample, then scale after human review.
8. Full-length viewing/listening and a timecoded defect log remain required before approval.

The Command Center does not invisibly activate other private plugins. Host-controlled activation is explicit in the router and registries.

## Safety and reproducibility

- The parallel asset-library agent exclusively owns video-library/**, global resource catalogs, downloaders, asset packaging/importers and the Build 76 resource release. Production may read/pull published resources but must not mutate that workstream.
- Inspect the complete changed-file list before PR creation; keep mixed asset/toolchain work separate.
- Do not overwrite master videos; deliver a separately rendered candidate with checksums and visual/audio review.
- Keep production writes, raw licensed audio, voice likeness, model downloads, costs and PR merges behind explicit approval.
- A plugin's existence or source-backed skill does not prove its CLI, weights or runtime are installed. Check pinned versions and actual evidence.
- License boundaries remain per component and per media record. Preserve third-party notices and verify fonts, assets, runtimes, music and sound files separately.

See `references/ILLUSTRATED_HISTORY_MOTION_SYSTEM.md` for the complete shot/motion standard. See SKILL-CATALOG.md and the plugin registries for internal skills and explicit specialist handoffs.


The v0.3.0 source pack includes three item-level CC0 music candidates: Eye of the Storm (WAV), The Final Battle (OGG) and Prepare to fight (MP3). They are modern orchestral/game-style recordings, not period-authentic music; audition them in edit context and keep them unapproved until a person chooses them.


The v0.3.0 pack contains 118 audio files from 11 item-level CC0 sources, including three orchestral candidates: Eye of the Storm (WAV), The Final Battle (OGG) and Prepare to fight (MP3). These are modern cinematic/game-style recordings, not period-authentic music. They remain un-auditioned.

The v0.3.0 acquisition, decode and catalog checks passed. Its 432 MB Actions artifact (ID 13563793933) expires 2027-02-05; persistent Release publication was denied by GitHub with HTTP 403. Use the [successful Actions run](https://github.com/Nolane-x/video/actions/runs/42347935721) to download it. Inner package SHA-256: `c5dbb1f639b6a96c0533657e983994ba99eb67ce9b86c2605f2f9de11eeced40`.


## Verified Foley + score v0.3.0 delivery

The v0.3.0 acquisition and decode/catalog checks passed: **118 audio files from 11 item-level CC0 sources**. The ZIP is delivered as Actions artifact `illustrated-history-foley-cc0-18` (ID `13563793933`) in [run 42347935721](https://github.com/Nolane-x/video/actions/runs/42347935721), available until **2027-02-05 06:38:50 UTC**. Inner package SHA-256: `c5dbb1f639b6a96c0533657e983994ba99eb67ce9b86c2605f2f9de11eeced40`. Outer artifact SHA-256: `37dade9eddadb006c03779de5a98edacc8f824d396c8ceafdb1a0c9acec5d3a5`.

The persistent GitHub Release upload was denied with HTTP 403 from the Actions integration token. Do not treat `/releases/tag/nolane-illustrated-history-foley-v0.3.0` as published; use the Actions run/artifact while it remains available. A repository maintainer must add `NOLANE_RELEASE_TOKEN` with Contents: write and rerun to create a permanent Release.


The v0.3.0 build, catalog checks and permanent GitHub Release succeeded in [Actions run 42348053901](https://github.com/Nolane-x/video/actions/runs/42348053901). [Download the 431.8 MB ZIP](https://github.com/Nolane-x/video/releases/download/nolane-illustrated-history-foley-v0.3.0/nolane-illustrated-history-foley-v0.3.0.zip) or [open the Release](https://github.com/Nolane-x/video/releases/tag/nolane-illustrated-history-foley-v0.3.0). It contains 118 files from 11 CC0 source entries. ZIP SHA-256: `d6eb13df0ebd4f17084d95993708f26bfb4fd86e9c4e9776e6454e04b190a7bd`. An Actions fallback artifact (ID 13563804097) expires 2027-02-05. All 118 entries are still un-auditioned and unapproved for final mix.


The next CC0 pack v0.4.0 expands the source pool with five modern environment recordings: Adelaide park birds-before-rain, a small park river with wildlife, open-field wind, Vistula River waves and indoor howling wind. Their original context is retained; they are not period-authentic sound reconstructions. Birds are not a default battle bed, Vistula waves are river rather than ocean, and indoor wind is for interiors. The v0.4.0 GitHub Actions acquisition/build is being validated before a permanent Release is available.
