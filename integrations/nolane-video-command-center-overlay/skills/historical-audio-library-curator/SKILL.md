---
name: historical-audio-library-curator
description: Curate, acquire and select real/licensed music, ambience, Foley and effects for history films with per-item rights, source hashes and human-audition records.
---
# Historical Audio Library Curator

## Principle
Recorded/licensed audio is the default foundation. Procedural tones/noise are last-mile supplements for stylized ticks or temporary animatics, not replacements for horses, weapons, footsteps, crowds, weather, water, workshop ambience, instruments or score.

## Search existing catalogues first
- Search Build 76 preview-catalog.json and Meta Open Sound meta-preview-catalog.json before unpacking large archives.
- Use python tools/audio/search_audio_resources.py --query "horse hooves dirt" --kind foley --direct-only for strict matches; use tag-assisted results only as leads.
- Inspect item-level rights, file hash, duration, channels/sample rate and creator. Listen to the exact preview before choosing a cue.
- Build 76 currently indexes 2,446 items (2,331 redistribution candidates, 110 rights-review and 5 source-specific-review). Meta has 1,583 OGG previews: 1,075 CC0 instrument notes and 508 CC BY 4.0 Oculus Foley/ambience samples; preserve Oculus attribution and do not mistake note samples for finished music.

## Targeted illustrated-history CC0 pack
The source map and acquisition status are in docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md and tools/audio/illustrated_history_foley_sources.json.
The workflow .github/workflows/build-illustrated-history-foley-library.yml downloads and indexes the listed CC0 sources: Medieval Weapon Textures (katana/bow/arrow handling), Weapon Impacts, Six Horses Galloping By, Crowd Shouting/Speaking Ambience, Blacksmith's Hammer and Thwack Sounds. Confirm the Actions result and the release tag nolane-illustrated-history-foley-v0.3.0 before claiming it has been published.
The crowd cue is edited group voice material, not a field recording of a historical army. The six-horse recording is the direct gallop candidate. The weapon pack provides weapon handling and weapon-to-weapon contacts, not a complete shield/armour/cavalry Foley library. Every new item is initially un-auditioned.

## Coverage gaps and next sourcing
The metadata audit still calls for hoofbeat surface round-robins, tack/reins, shield impacts, chainmail/armour handling, distant command/crowd beds, Japanese rain/temple/port/workshop ambience and period-appropriate recorded music. Search exact sources and licenses; don't infer these from broad tags.

## Lossless Meta preview-to-master mapping

The Meta Open Sound catalog carries each OGG preview's exact original WAV path as `source_wav_file`, together with `wav_master_archive_name`, `wav_master_download_url`, `wav_master_size_bytes` and `wav_master_sha256`. Use OGG for discovery/audition, then retrieve only the selected source WAV member through `.github/workflows/acquire-meta-open-sound-wav-master.yml`. Verify the collection archive size and SHA-256 before extraction. Oculus samples are CC BY 4.0 and require attribution; Piano/Nylon/Steel Guitar entries are CC0 note samples, not finished scores.

Sonniss GDC 2026 is a private production source. never upload Sonniss raw archives or extracted files into this public repository, public Releases or shared preview packs. Follow the live EULA and its AI/ML-training prohibition.

## OGG preview to WAV master
The Meta catalog links each OGG preview to a WAV member and collection archive with size/SHA-256. Search/listen to OGG first; only then fetch the exact matching WAV master. Oculus Audio Pack WAV requires CC BY 4.0 attribution. Piano/Nylon/Steel Guitar masters contain CC0 instrument note samples, not complete scores.

## Source rights tiers
1. public_cc0_pd: exact item-level CC0/Public Domain proof, source page, creator, license URL and hash retained.
2. project_use_only: use in the finished video only when exact terms permit; do not redistribute raw files.
3. private_production_only: private licensed store only. Sonniss GDC 2026 is private-only; check current EULA, never public-mirror raw assets and obey the AI/ML-training prohibition.
4. government_media_conditions: apply NASA item-level rules, retain credit and do not imply endorsement.
5. blocked: unclear or conflicting rights; do not download/use.

## Cue design and post
Build shot-level ambience, near/mid/far world, character/prop Foley, impacts, transitions and music separately. Sync transients to visible contact and vary takes/perspective. Keep stems separated until mix. Preserve silence and narration headroom. Every new entry has human_auditioned=false and approved_for_final_mix=false until a person listens and records the decision.


## Human audition workflow — v0.3.0

Open the pack's offline \`AUDIO_PREVIEW.html\` after extracting the release. It is a review console, not just a player: search and filter all cues, listen to the exact original file, record keep/reject, score 1–5, write notes and explicitly mark the audition checkbox. Final-mix approval is disabled until the cue has been heard, kept as a candidate and has CC0/Public Domain item-level rights.

Export \`nolane-foley-review-decisions.json\` from the browser. Decisions are local to that browser until exported; they are not automatically sent to GitHub. Validate the export against the exact catalog and SHA-256 values:

\`\`\`bash
python tools/audio/validate_foley_review_decisions.py \\
  --catalog package/catalog.json \\
  --review nolane-foley-review-decisions.json \\
  --output build/foley-review-report.json
\`\`\`

The validator rejects duplicate/unknown IDs, changed file hashes, un-auditioned keep/reject decisions and final-mix approval that bypasses the human/rights gate. A valid report is an auditable shortlist, not an automatic mix decision.


## Score candidate coverage — v0.3.0

The audition pack also includes three real CC0 orchestral score candidates: Eye of the Storm (WAV), The Final Battle (OGG) and Prepare to fight (MP3). These are modern cinematic/game-style recordings, not historically authentic ancient Roman music. Listen to each exact source, compare its emotional arc and loop behavior with the edit, and keep the music track separate from Foley. A CC0 license permits use under its terms; it does not make the track artistically appropriate. No score candidate is pre-approved.
