# Historical Foley Coverage Audit

Date: 2026-11-06  
Catalog inputs: `audio-library/generated/preview-catalog.json` (Build 76) and `audio-library/generated/meta-preview-catalog.json` (Meta Open Sound).  
Method: whole-token searches over title, description, file name, archive member, categories and tags. Results are metadata leads only; they have not been listened to in this audit. Direct title/file/description matches are distinguished from broad tags. Counts below are search hits, not unique sound designs or proof of historical accuracy.

## What the public/redistributable catalogs actually cover

| Historical cue family | Build 76 metadata | Meta Open Sound metadata | Assessment |
|---|---|---|---|
| Sword clash | 11 broadly labelled sword files, including unsheathes | 1 direct sword-on-sword clash | Useful starting point; audition before use |
| Sword scrape / unsheathing | Sword-unsheathe files; scrape not clearly described | 2 sword-blade scrape takes | Good real Foley candidate; CC BY 4.0 |
| Sword handling / swing | Generic sound/swing candidates | 2 handling/swing candidates | Candidate only; some are game/VR oriented |
| Human footsteps | 26 records; mixed game footsteps | 72 records, mostly shoes on concrete/metal | Plenty of generic steps, but material is often modern |
| Horse vocalization | No clear horse record | 2 horse-neigh takes | Useful animal vocalization; not a hoofbeat |
| Hoofbeats / trot / gallop | No credible direct match found | No credible direct match found | Targeted CC0 pack now adds one six-horse gallop approach/pass recording; surface-specific hoofbeat layers and gait round-robins remain missing |
| Cavalry movement | No credible direct match found | No credible direct match found | One gallop pass is now available; walk/trot/canter cycles, tack, rider coupling and varied surfaces remain a gap |
| Armor / chain | 2 generic armor-light records; 4 chainmail records in prior Build76 text search included duplicate AppleDouble metadata | Some chains/metal; no clear historical armor set | Needs audition and source hygiene |
| Shield impact / spear impact | No clearly suitable direct match | No clearly suitable shield/spear direct match | The new OGA packs add several weapon-on-weapon/spear contacts, but no dedicated shield-on-shield or shield-block Foley; Sonniss remains private-only |
| Bowstring / arrow release / flight / impact | No credible direct match | No credible direct match | New OGA Weapon Textures provides bow handling/release and arrow travel/pass cues; target-impact variants still require targeted review/acquisition |
| Battlefield crowd / commands | 4 crowd records, e.g. station / cheer / stylized murmur | No direct battle-crowd bed surfaced | New CC0 crowd-shouting cue is a designed group-voice layer, not a historical field recording; commands and near/mid/far layers remain missing |
| Boats / oars / water | No strong rowing direct match | 5 distinct rowing takes | Useful for historical ship scenes after audition |
| Wind / rain / forest beds | Several generic ambience records | Small set of wind/rain/forest ambiences | Useful bed candidates; check setting and recording quality |
| Fire / destruction | Mixed fire/game effects | Some door/hatch and non-period machine cues | Weak historical fit unless manually auditioned |


## Targeted CC0 illustrated-history acquisition — 2026-11-07

The first GitHub Actions build verified a new targeted source pack from eight item-level CC0 source entries. Download, extraction, FFprobe, catalog validation and the two Python safety/provenance tests passed in run [42341098346](https://github.com/Nolane-x/video/actions/runs/42341098346). It produced **115 distinct audio files** in a ZIP of **397,657,285 bytes** (SHA-256 `5be9ea8cbcf5daf9e848e190447a4c79480045c164b2ba9a8ce9f173f5b1257b`).

| Source family | Audio files |
|---|---:|
| Medieval Weapon Textures, part 1 | 25 |
| Medieval Weapon Textures, part 2 | 19 |
| Medieval Weapon Impacts, part 1 | 29 |
| Medieval Weapon Impacts, part 2 | 19 |
| Six Horses Galloping By | 1 |
| Crowd Shouting/Speaking Ambience | 1 |
| Blacksmith's Hammer | 1 |
| Thwack Sounds | 20 |
| **Total** | **115** |

The first build reached package creation and passed the content checks, but its Release-upload step failed because the workflow's `GH_TOKEN` interpolation contained an erroneous literal escape character. That was corrected in commit `e074b689f5046d195b31dc4b41a6d886d758380e`; retry run [42341335341](https://github.com/Nolane-x/video/actions/runs/42341335341) is the release-publication attempt. Until that run succeeds, treat the source ZIP as built in Actions but **not yet published as a GitHub Release**.

The current catalog state is `ACQUIRED_AND_PROBED_NOT_HUMAN_AUDITIONED`: **0/115** human-auditioned and **0/115** approved for a final mix. FFprobe confirms decodability/metadata, not quality or suitability. The 25-second horse file is one gallop pass, not a cavalry gait library. The crowd sample is a designed group-voice effect, not a historical battlefield recording. Weapon packs provide useful handling, bow/arrow and weapon-contact variety, but do not close the shield/armour/tack gaps.

Manifest: `tools/audio/illustrated_history_foley_sources.json`  
Build workflow: `.github/workflows/build-illustrated-history-foley-library.yml`  
Acquisition notes: `docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md`

## Avoid false confidence from metadata tags

The Meta Oculus catalog uses broad thesaurus keywords. For example, generic footsteps may carry tags such as “march”, “cavalry-adjacent” terms or many walking synonyms despite the description saying shoes on concrete. Do not interpret such a tag as evidence of a horse, military boot or historical surface.

The search CLI therefore reports:
- `match_quality=direct`: token appears in title/category/file name/description;
- `match_quality=tag_assisted`: result depends on broad tags or source metadata;
- `--direct-only`: excludes tag-assisted suggestions.

Neither match type proves audible content or historical suitability. Listen to the exact sample before use and record the human audition decision.

## Priority gaps for future acquisitions / commissioned recordings

1. Horses: isolated hoofbeats on dirt, mud, grass, stone and wood; walk/trot/canter/gallop round-robins; tack/leather/reins; hooves mixed with rider movement; horse breaths/snorts/whinnies.
2. Weapons: shield-on-shield, spear shaft impact, sword-on-helmet/armor, blade parry, scabbard draw, bowstring release, arrow flight, arrow impact on wood/shield/earth.
3. Army movement: marching boots on dirt/grass/stone, shield wall movement, armor/chain rustle, formation turns, distant ranks, shouted command layers, crowd swell/panic/cheer in near/mid/far perspective.
4. Historical environments: wooden ships, oar stroke/rowlock, sail/rigging, hull creak, deck footsteps, harbor surf, campfires, rain on canvas/leather/wood, wind on banners.
5. Music: source real licensed/recorded/performed instruments or finished compositions; instrument note samples are building blocks, not finished scores. Avoid asserting historical authenticity unless researched.

## Private-only candidate: Sonniss GDC 2026

The official track list includes **Historical Weapons Vol. 2** cues for shield spin, wooden spear/stick impact and metallic sword slide/cuts. This may close some weapon gaps, but the current bundle license is source-only: EULA v2.0 allows synchronization into films/videos and commercial projects, but prohibits raw-file sale and AI/ML training. It must stay in a private production store and must never be uploaded as raw files to this public repository. The licensee must accept the current EULA before downloading.

- Bundle: https://gdc.sonniss.com/
- EULA: https://sonniss.com/gdc-bundle-license/
- Track list: https://docs.google.com/spreadsheets/d/1MkoGwA6FfgNXhye9wLnY0gNLvjEp4H2iYXM1YxMI6Qs/edit?usp=sharing

Acquisition status: **not downloaded**. Do not claim the repository currently contains Sonniss audio.

## Approval rule

No item in either generated catalog is human-auditioned merely because it appears in a preview bank. For final production, keep the preview OGG separate from the selected WAV/master, verify exact item rights, listen to the selected file, record a cue-sheet entry, and only then mark it approved for a final mix.


## Verified release publication — 2026-11-07

The final artifact-first workflow completed successfully in run [42341596143](https://github.com/Nolane-x/video/actions/runs/42341596143). All test, acquisition, FFprobe/catalog validation, Actions artifact upload and GitHub Release steps passed.

- GitHub Release: https://github.com/Nolane-x/video/releases/tag/nolane-illustrated-history-foley-v0.1.0
- Actions artifact: `illustrated-history-foley-cc0-3` (90-day retention; artifact ID `13562295186`)
- ZIP size: 397,657,285 bytes
- ZIP SHA-256: `78e7136449d773456117f26a21e73d7e2cc00bb4709ea11d2c6ecc9f422a956e`
- Catalog: 115 distinct audio files from 8 source entries
- Human auditioned: 0/115
- Approved for final mix: 0/115

The release is now published. The previous two failed attempts are superseded by this final successful run. The pack is acquired, decoded and indexed, but remains **not human-auditioned**; do not treat it as a production-approved sound library until cues are listened to and selected.


## Audition console and approval validation — v0.2.0

The Foley pack now has an offline human-review console in \`AUDIO_PREVIEW.html\`. It supports per-file listening, decision, fit rating, notes, audition state, and a final-mix approval checkbox. The browser stores reviews locally; export the JSON and validate it against the exact matching \`catalog.json\` using:

\`\`\`bash
python tools/audio/validate_foley_review_decisions.py \\
  --catalog package/catalog.json \\
  --review nolane-foley-review-decisions.json \\
  --output foley-review-report.json
\`\`\`

The validator checks the asset ID and SHA-256 pair, license/right class, listened state and keep/reject decision. A final-mix shortlist is emitted only from human-approved CC0 cues. This is an approval-record validator, not an automated audio quality classifier.

The Cannae shot-by-shot requirements are mapped in \`docs/audio/CANNAE_45S_AUDIO_CUE_PLAN.json\`. Its asset IDs are intentionally empty until the exact sounds have been auditioned.


## v0.3.0 score additions

The audio source manifest now includes three item-level CC0 orchestral score candidates:
- Eye of the Storm — Indieteur, WAV source, creator describes it as orchestral music for warfare scenes.
- The Final Battle — skrjablin, OGG source, generic dramatic orchestral loop with a restart pause noted on the source page.
- Prepare to fight — Basil, MP3 source, epic battle-intro cue.

All three are modern cinematic/game-style recordings, not period-authentic music. Their availability in the pack does not imply they fit Cannae or any historical scene. They start un-auditioned and not approved for final mix; use the review console and SHA-256 validator.




## Verified v0.3.0 release — 2026-11-07

The final build and permanent GitHub Release succeeded in [Actions run 42348053901](https://github.com/Nolane-x/video/actions/runs/42348053901). This supersedes the earlier run whose Release upload was denied with HTTP 403.

- GitHub Release: https://github.com/Nolane-x/video/releases/tag/nolane-illustrated-history-foley-v0.3.0
- ZIP: [nolane-illustrated-history-foley-v0.3.0.zip](https://github.com/Nolane-x/video/releases/download/nolane-illustrated-history-foley-v0.3.0/nolane-illustrated-history-foley-v0.3.0.zip)
- Source entries: 11
- Catalogued audio files: 118 (115 Foley/weapon/environment cues + 3 orchestral score candidates)
- ZIP size: 431,804,481 bytes
- ZIP SHA-256: `d6eb13df0ebd4f17084d95993708f26bfb4fd86e9c4e9776e6454e04b190a7bd`
- Actions fallback artifact: ID `13563804097`, `illustrated-history-foley-cc0-19`
- Artifact size: 432,234,335 bytes; expires 2027-02-05 06:40:33 UTC
- Artifact SHA-256: `015768fdbda68af42dbec23ddedfb60b2e0f3e6ae32d9d42a0e873e3ab9cf15e`
- Human-auditioned: **0/118**
- Approved for final mix: **0/118**

The Release contains the ZIP, build report, download manifest and SHA256SUMS. The package includes the per-file catalog, source register, original audio and offline audition/review console. All recordings remain un-auditioned until a human listens and records a decision.
