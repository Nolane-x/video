---
name: historical-audio-library-curator
description: Use when finding, downloading, curating, indexing, licensing or selecting real music, ambience, Foley and sound effects for historical, military, documentary, illustrated-history or cinematic video; especially when a reusable sound bank is needed instead of mostly synthetic SFX.
---
# Historical Audio Library Curator

## Principle
Use real recorded/licensed audio as the default foundation. Code-generated tones/noise are a last-mile supplement for designed UI ticks, stylized transitions or genuinely unavailable sounds—not a replacement for horses, footsteps, weapons, crowds, weather, water, room tone, instruments or cinematic music.

## Fast local search before downloads

- Search `audio-library/generated/preview-catalog.json` for Build 76 playable candidates and `audio-library/generated/meta-preview-catalog.json` for Meta Open Sound samples before unpacking archives.
- Use category/tags, title, creator, source and `rights_class` to shortlist. These records do not prove a sound fits the film; audition candidates before selection.
- Build 76 currently has 2,446 inventoried items; 2,331 are redistributable candidates with playable previews, 110 require rights review and 5 require source-specific review. Do not use the 115 review entries by default.
- Meta Open Sound currently has 1,583 OGG previews: 1,075 CC0 instrument samples and 508 CC BY 4.0 Oculus Foley/ambience samples. Preserve the exact Oculus attribution. A sample bank is not 1,583 complete music tracks.
- Download the entire audio preview artifact only when broad listening is necessary; otherwise fetch the relevant source pack/member to save bandwidth.

## Existing library first
The verified Build 76 GitHub Release contains separate audio-category volumes. Read the item-level source manifests and the `docs/audio/HISTORICAL_SOUND_LIBRARY.md` map before building anything new. The current archive families include OpenGameArt, USGS, NASA, Wikimedia Commons, Kenney and a distinct procedural-originals pack. Treat filename/category and rights class as separate facts; an audio ZIP is not proof every item inside is a historical Foley recording.

## Asset taxonomy
Tag each file with controlled terms:
- **People:** crowd walla, cheers, chants, panic, command, distant voices, footsteps, clothing/armor movement, breathing.
- **Historical combat:** sword draw, blade clash, metal armour, shield impact, spear/shaft, arrow release, arrow flight/impact, bowstring, reload, distant melee, cavalry charge, horse gallop/trot/walk/whinny/snort, cannon/gunfire where historically appropriate.
- **World/transport:** wind, rain, thunder, fire, forest, birds/insects, river, surf, harbor, wood creak, ship hull/rigging/sails, oars, wheels, carts, doors, interior room tone.
- **Materials/objects:** leather, cloth, wood, stone, metal, paper, scroll, ceramics, glass, tools, food preparation and market stalls.
- **Music:** period-relevant instruments/textures, ceremonial, tense drone, pulse, action ostinato, grief, reflection, resolve, stingers and transitions. Avoid claiming a track is historically authentic without evidence.
- **Editorial:** whooshes, impacts, risers, reverse swells, transition tails, UI accents and logo cues.

## Source tiers and legal separation
1. **Redistributable library:** accept only verified CC0 or Public Domain items whose exact item record proves that status. Preserve creator, source landing page, exact file URL, license URL/version, date, hash, size, duration, sample rate, channel count, format and notice. Validate file signature and safe archive paths.
2. **Project-use tier:** licensed stock can be synchronized into a finished video when item-specific terms allow it, but the raw file stays out of a public asset pack/repository release if redistribution is prohibited.
3. **Private production tier:** Sonniss #GameAudioGDC can be used under its current EULA for synchronized personal/commercial film projects, but raw sounds may not be resupplied/sold and may not be used for AI/ML training. Store the exact EULA version and download date. Do not upload the pack to a public GitHub release or shared redistributable collection.
4. **Blocked/unverified:** mixed, missing, conflicting or unclear rights are not downloaded into the redistributable pool. Never infer a license from a provider, collection or repository-wide default.

Source routes (re-verify current item terms at acquisition): OpenGameArt CC0 item-page results; Openverse audio API with exact `license=cc0`; Wikimedia Commons file-level CC0/Public Domain metadata; USGS items whose own Sources/Usage block explicitly says Public Domain; Kenney packs whose individual page identifies CC0. Mixkit and Sonniss are project-use/private-source routes, not raw-library redistribution routes under their standard terms.

## Acquisition and catalogue
1. Search specific scene/action/material and synonyms: `horse hoofbeats cobblestone`, `chainmail movement`, `katana sheath draw`, `sword blade ring`, `wooden ship rigging creak`, `rain bamboo roof`, `taiko ensemble`, `crowd battle distant`.
2. Query multiple trusted sources; respect API quotas, rate limits and download controls.
3. Check item page rights and actual file. Keep evidence and original filename; deduplicate by SHA-256 without discarding distinct provenance records.
4. Store source files losslessly; create processed working copies, not destructive edits to archival masters.
5. Index duration, peak, LUFS, true peak, sample rate, channels, bit depth, clipping, silence and a waveform/spectral preview.
6. Automated tags are search hints only. Preview-listen to every selected file before marking it production-ready; record human audition status.
7. Maintain an offline playable catalogue; keep public CC0/PD assets physically and logically separate from project-use/private assets.

## Historical sound editing
- Build a per-shot cue map: ambience bed, specific Foley/action, distant world, transitions and music, each with an exact cue ID and timing.
- Synchronize attacks/transients with visible contact; add body and tail only when distance/material supports it; vary near/far perspective.
- Use perspective layers: close detail dry/intimate; distant combat filtered/reverberant; interiors with short room response; outdoors with spatial width and restrained tails.
- Avoid one generic sword clang repeated for every action. Draw, swing, contact, armor scrape, shield hit and recovery are distinct.
- Make music evolve across narrative acts; create tension/release and deliberate silence. Duck under narration with smooth automation; do not push SFX/music above dialogue.
- Keep music, ambience, spot Foley, designed transitions and narration as separate stems.

## Quality and rights gates
- No public release until every raw file is cleared for that exact use and attribution is preserved.
- Do not use licensed SFX for AI training where the license forbids it; never clone an identifiable voice without authorization.
- Do not claim full listening from metadata or automated classification. A human must listen to the full mix and spot-check critical cues.
- Deliver source register, asset IDs/hashes, category index, rights separation report, cue sheet, stem map, loudness/true-peak measure and listening QA log.
