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
| Hoofbeats / trot / gallop | No credible direct match found | No credible direct match found | **Critical gap** for cavalry/history scenes |
| Cavalry movement | No credible direct match found | No credible direct match found | **Critical gap** |
| Armor / chain | 2 generic armor-light records; 4 chainmail records in prior Build76 text search included duplicate AppleDouble metadata | Some chains/metal; no clear historical armor set | Needs audition and source hygiene |
| Shield impact / spear impact | No clearly suitable direct match | No clearly suitable shield/spear direct match | **Gap**; Sonniss track list is a promising private-only source |
| Bowstring / arrow release / flight / impact | No credible direct match | No credible direct match | **Critical gap** |
| Battlefield crowd / commands | 4 crowd records, e.g. station / cheer / stylized murmur | No direct battle-crowd bed surfaced | Needs dedicated crowd / command recordings |
| Boats / oars / water | No strong rowing direct match | 5 distinct rowing takes | Useful for historical ship scenes after audition |
| Wind / rain / forest beds | Several generic ambience records | Small set of wind/rain/forest ambiences | Useful bed candidates; check setting and recording quality |
| Fire / destruction | Mixed fire/game effects | Some door/hatch and non-period machine cues | Weak historical fit unless manually auditioned |

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
