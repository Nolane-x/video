---
name: illustrated-history-animation-director
description: Direct polished illustrated/cartoon history films with character acting, world-building, multi-form motion graphics, camera choreography, licensed asset use and motion/audio QA; study supplied references without copying them.
---
# Illustrated History Animation Director

## Purpose and route
Use this route for original illustrated/cartoon history films. It is distinct from H2 Squire/vector military animation and footage-led historical documentary. The supplied Samurai example demonstrates an illustrated-history visual vocabulary, not a design to copy.

## Required reference study
1. Probe/hash the exact source and record video/audio stream metadata.
2. Map the whole runtime with repeatable samples; create timecoded contact sheets.
3. Inspect action-heavy intervals densely. Record anticipation, motion path, contact, follow-through, recovery, camera movement, transition and secondary motion.
4. Record shot scale/angle, character action, prop interaction, environment, camera, graphics, palette/light and timecode.
5. Separate direct observation from interpretation. Still frames do not prove motion or subjective sound; never claim a full normal-speed watch/listen unless performed.
6. Do not copy protected characters, frames, exact compositions, scripts, narration, music or SFX.
The Samurai source record is docs/SAMURAI_REFERENCE_STUDY.md; the detailed sample map is docs/reference-studies/samurai-history-animation-review-2026-11-06.md.

## Visual storytelling modes
Rotate these modes according to the story:
- character-led acting and physical action;
- geography, routes, coastline, fleet and formation explanation;
- relationships, politics, family, civilian stakes and aftermath;
- world-building through markets, workshops, smithies, ships, roads, castles and landscapes;
- evidence/explanation through scrolls, calligraphy, portraits, timelines, rank cards, diagrams, myth/fact comparisons and historical artwork;
- time changes and legacy through costumes, institutions, museum frames and recurring motifs.

The Samurai sample changes visual mode: mounted action and group scale; invasion/fleet geography; brush/calligraphy and map transitions; social/workshop life; institutional change; museum/legacy imagery. Transfer the variety principle, not the exact scene compositions or character designs.

## Five motion channels
For each important shot define separate channels:
1. Actor/body performance: pose, limbs, face, gaze, weight shift and timing.
2. Prop/physical response: weapon path, bowstring/arrow, shield, cloth, horse tack, boat, debris and contact.
3. Environment: rain, wind, smoke, waves, banners, fire, crowds, water and parallax layers.
4. Camera: locked, pan, track, push, pull, tilt, orbit, crane or motivated reframing.
5. Information graphics: route drawing, labels, markers, chart fills, card entrances, timelines and wipes.

At least two channels should create independent, story-motivated motion in a motion-led shot; three or more may be used for hero beats. Keep one primary focal action, secondary movement and a readable settle. Camera movement alone is not character action.

For physical action, plan anticipation → action → contact/impact → follow-through → recovery. The prop must respond at the same contact frame. Check hand/foot grounding, balance, rider/horse coupling, gaze and screen direction.

## Reusable animation and scene systems
Build deterministic, frame-seek-safe cycles for:
- idle, look, speak, point, turn, walk, march, run, kneel, fall, stand, group cheer/panic;
- horse walk/trot/canter/gallop/rear with rider bounce, rein/tack response and hoof contacts;
- weapon draw/sheath, bow nock/draw/release, arrow travel/pass/impact, sword/spear/shield contact, recoil and recovery;
- rowing, ship bob, boarding, ladder climb, rope/rigging and sail motion;
- banners, cloth, rain, smoke, fire, water, clouds, dust, foliage and asynchronous crowd loops;
- map route drawing, marker travel, location highlight, portrait/rank cards, timelines and myth/fact reveals.

Use stable rig pivots and named attachment points. Stagger repeated cycles so crowds and cavalry do not move in synchrony. Use holds when they support emotion or reading.

## Camera and edit grammar
Use establishing wides, medium group/action, close reactions, object inserts, profile/over-shoulder, tracking/travel, overhead geography and graphic tableaux. Specify camera start/end, angle/height, duration, easing and narrative motivation. Pull back to reveal scale, track to expose movement, push in for a decision, and use top-down views to clarify spatial relations when useful.
Keep screen direction coherent. Use match cuts, map-to-location transitions, graphic matches, wipes and sound J/L cuts for a reason. Avoid repeating the same slow zoom or map/face/army template. Combat should be balanced by people, places, craft, trade, politics, training and aftermath.

## Art, engines and asset strategy
- Search the existing 50 GB+ asset pool before new acquisition or AI generation.
- Invest in original character/expression sheets, costume and prop variants, distinct environment plates, historical document/art cards, map/infographic components, camera recipes and real sound.
- Use Remotion for editorial timing, maps, text and layered compositions; Krita for authored/painted assets; Blender for shots where depth, mechanics or lighting add real value; evaluate Motion Canvas only after dependency/license and sample-shot tests; use H2 rigs only when the Squire visual language is explicitly desired.
- Prototype the hardest motion or transition as a 3–8 second moving proof before scaling.

## Audio: recordings first
- Search Build 76 and Meta Open Sound with tools/audio/search_audio_resources.py; direct matches outrank broad tag-assisted candidates.
- Consult docs/audio/HISTORICAL_FOLEY_COVERAGE_AUDIT.md and docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md.
- The targeted public CC0 acquisition workflow is .github/workflows/build-illustrated-history-foley-library.yml. It acquires bow/katana handling, weapon impacts, six-horse gallop, crowd shout, forge hammer and generic impacts. Use the versioned release only after its GitHub Actions run actually publishes it.
- Retain creator, exact source page, license, source hash, duration, sample rate and channels. Never place private/project-use raw sources in a public release.
- All new items start human_auditioned=false and approved_for_final_mix=false. FFprobe success does not approve the sound.
- Code should select, synchronize, layer, loop, pan, EQ, compress, duck, reverberate and master recordings. Synthesized audio is a temporary placeholder or a documented exception, not the main soundscape.

## Per-shot manifest
Record: shot ID; story beat; duration/frame range; location/time; shot size; viewpoint; camera path/easing; screen direction; character IDs/key poses; action phases; prop/contact; environment layers/motion; palette/light; graphics; transition; asset IDs/rights; narration segment; music/SFX/ambience cue IDs; on-screen text/subtitles; risks; motion-proof status.

## Quality gates
- Contact sheet covers every shot; detailed action needs moving proof.
- Inspect hero action at normal speed and selected frames around contact/follow-through/recovery.
- Verify silhouette, hand/foot contact, prop attachment, depth layers, crop, text legibility, cut continuity and visual repetition.
- Review complete picture and soundtrack before release; log defects and cues with timecodes.
- Report technical pass, sampled review, full picture review and full audio audition as separate states.
