# Illustrated-history Foley acquisition pack

Status: v0.1.0 is published; v0.2.0 added the offline audition console; v0.3.0 adds three CC0 orchestral score candidates.  
Current target release: nolane-illustrated-history-foley-v0.3.0

This is a targeted gap-filling pack for the illustrated/cartoon history route. It supplements, rather than duplicates, the broad Build 76 and Meta Open Sound catalogues. The sources are selected for concrete needs found in the Samurai reference study and historical Foley coverage audit.

## Source manifest

The canonical machine-readable register is tools/audio/illustrated_history_foley_sources.json. It records the exact source page, direct download URL, creator, per-item license class, purpose and minimum expected file size.

| Source | Main coverage | Rights |
|---|---|---|
| OpenGameArt — Medieval Weapon Textures, parts 1–2 | Katana draw/sheath/swing, bow handling, arrow release/pass and other weapon preparation | CC0 1.0 |
| OpenGameArt — Medieval Weapon Impacts, parts 1–2 | Blade-on-blade and weapon/haft/spear contact variations | CC0 1.0 |
| Wikimedia Commons — Six Horses Galloping By | A 25-second six-horse approach-and-pass gallop recording | CC0 1.0 |
| OpenGameArt — Crowd Shouting/Speaking Ambience | Human voice group/army-shout layer | CC0 1.0 |
| OpenGameArt — Blacksmith's Hammer | Hammer-to-anvil impact for forge/repair scenes | CC0 1.0 |
| OpenGameArt — Thwack Sounds | Generic impacts for layered action design | CC0 1.0 |
| OpenGameArt — Eye of the Storm | Orchestral warfare score candidate (WAV master) | CC0 1.0 |
| OpenGameArt — The Final Battle | Dramatic orchestral battle loop candidate | CC0 1.0 |
| OpenGameArt — Prepare to fight | Epic battle-intro score candidate | CC0 1.0 |

The weapon packs were created/recorded by Ben Jaszczak and Brian Nelson. The crowd cue is voice material recorded by its creator and siblings then edited into a crowd-like texture; it is not an authentic historical battle recording. The horse file is described by Wikimedia Commons as six horses galloping toward the listener and past. The hammer file is described as a hammer hitting an anvil. The thwack pack is a generic impact collection. Do not overstate their historical authenticity.

## Why these sources

The existing Build 76 + Meta Open Sound metadata audit found no credible direct hoofbeat/gallop match, weak direct battlefield crowd coverage, and no robust bow/arrow cue family. The targeted pack adds:
- a direct horse-gallop recording;
- weapon preparation and projectile actions;
- multiple weapon-on-weapon contact variations;
- a designed human crowd-shout layer;
- a forge-specific hammer/anvil hit;
- general impact variation;
- three CC0 orchestral score candidates, kept separate from Foley and still awaiting human audition.

It does not fully solve cavalry walk/trot/canter round-robins, horse tack/reins, shield-on-shield impact, armour/chainmail movement, distant battle-command layers or historically appropriate full music. Those remain acquisition/recording priorities.

## Acquisition and release

Run .github/workflows/build-illustrated-history-foley-library.yml on branch codex/samurai-cinematic-audio-v1. The workflow downloads only the listed source packs, verifies minimum sizes and optional pinned SHA-256 values, extracts and probes the media with FFprobe, keeps original media formats, writes a searchable JSON catalog and offline HTML audition page, and publishes the collection as a GitHub Release plus a workflow artifact.

Release assets are not committed into Git history. The bundle carries the source register, archive/member provenance, creator, license URL, source URL, file hash, codec, duration, sample rate and channel count.

## Approval state

Every newly acquired item starts with:
- human_auditioned: false
- approved_for_final_mix: false
- rights_class: public_cc0_pd only where the cited item-level page explicitly identifies CC0 1.0.

The workflow proves download integrity and decodability, not sound quality. Listen to the exact cue, inspect the waveform for clipping/loops, decide whether the sound fits the visible material and period, then record the audition decision in the project cue sheet. Do not use generated/placeholder sounds as a shortcut when a real recording exists.

## Future priorities

1. Recorded hoofbeats by surface (dirt, mud, grass, stone, timber), with walk/trot/canter/gallop round-robins and close/far passes.
2. Horse tack, reins, saddle leather, breath, snorts and whinnies.
3. Shield impacts, spear/shaft hits, armour/chainmail movement and formation handling.
4. Marching boots, group commands, distant battle ambience and panic/cheer layers.
5. Japanese environment beds: rain on tile/bamboo, temple/market/workshop, port, timber boats, oars, rigging and surf.
6. Music made from properly licensed performances/stems or recorded/sample-based instrument performances; multisampled piano/guitar notes are not complete scores.


## Verified build and published release — 2026-11-07

The final Actions build [42341596143](https://github.com/Nolane-x/video/actions/runs/42341596143) completed successfully, including tests, all eight source downloads, archive extraction, FFprobe/catalog validation, artifact upload and GitHub Release publication.

Release: https://github.com/Nolane-x/video/releases/tag/nolane-illustrated-history-foley-v0.1.0

- ZIP: `nolane-illustrated-history-foley-v0.1.0.zip`
- Size: 397,657,285 bytes
- SHA-256: `78e7136449d773456117f26a21e73d7e2cc00bb4709ea11d2c6ecc9f422a956e`
- Audio count: 115 files / 8 source entries
- Actions artifact: `illustrated-history-foley-cc0-3`, ID `13562295186`, 90-day retention.

The catalog intentionally remains at 0 human-auditioned and 0 approved-for-final-mix. Download/decode is not sonic QA; listen to each cue before use.


## Audition Edition v0.2.0 — human review console

The v0.2.0 pack upgrades AUDIO_PREVIEW.html from a simple search/list page into an offline review console:

- Search by cue title, filename or tags; filter by source pack and review state.
- Play each original file in-browser without converting or rewriting the source audio.
- Record a decision (keep candidate / reject), a 1–5 production-fit rating and notes.
- Explicitly mark that the exact file was listened to.
- Approve a cue for a final-mix shortlist only after the exact file is marked auditioned, is kept as a candidate and its item rights class is CC0/Public Domain.
- Persist decisions in that browser's local storage, export JSON, and import a prior review using asset ID plus SHA-256 matching.

The browser state is not sent automatically to GitHub. Export \`nolane-foley-review-decisions.json\` and keep that file with the project. Validate it against the exact pack catalog:

\`\`\`bash
python tools/audio/validate_foley_review_decisions.py \\
  --catalog package/catalog.json \\
  --review nolane-foley-review-decisions.json \\
  --output build/foley-review-report.json
\`\`\`

To block a final-mix shortlist unless at least one cue was genuinely approved, add \`--require-approved\`. The validator rejects unknown IDs, duplicate rows, SHA-256 mismatches, un-auditioned decisions, rejected cues marked approved, and assets outside the CC0 Public Domain rights class. It does not listen to audio or create a human decision; it validates the human-exported review record.

## Cannae 45-second audio cue map

\`docs/audio/CANNAE_45S_AUDIO_CUE_PLAN.json\` maps the existing five shots to required narration, ambience, Foley, impact and music layers. It intentionally contains no approved asset IDs. The 115-file Foley pack does not include a finished score, dedicated marching-foot bank, shield-on-shield bank or full ambience library. Search Build 76 and Meta Open Sound for direct matches, source any missing music/ambience under suitable item terms, and audition each exact file before adding an asset ID to a cue.

## Score candidates added in v0.3.0

Three item-level CC0 music recordings have been added to the audition pack:

| Track | Creator | Source | Editorial caution |
|---|---|---|---|
| Eye of the Storm | Indieteur | https://opengameart.org/content/eye-of-the-storm-0 | The creator describes an orchestral warfare cue; listen for modern game/fantasy coloration before using it in a documentary |
| The Final Battle | skrjablin | https://opengameart.org/content/the-final-battle | Generic dramatic orchestral loop; contains an audible restart/pause according to the source description |
| Prepare to fight | Basil | https://opengameart.org/content/prepare-to-fight | Epic battle-intro cue; test pacing and emotional fit |

These are real audio recordings, not code-generated music. They are CC0 per their item-level source pages, but are not automatically appropriate or approved. All three enter the console as un-auditioned candidates. Treat them as modern cinematic score options, not historically authentic ancient Roman music.

The exact source IDs are mapped in docs/audio/CANNAE_45S_AUDIO_CUE_PLAN.json. The five-shot map contains no approved music asset IDs until the exact recordings are auditioned.
