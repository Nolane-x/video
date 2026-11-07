---
name: illustrated-history-animation-director
description: Direct polished illustrated/cartoon history films with character acting, world-building, multi-form motion graphics, camera choreography, licensed asset use and motion/audio QA.
---
# Illustrated History Animation Director

Use for original illustrated/cartoon history films. This is distinct from H2 Squire/vector military animation and footage-led historical documentary. The supplied Samurai reference is an illustrated-history example; use it as evidence of visual grammar, not as a design to copy.

## Reference study and honesty
- Probe and hash the exact source. Map the full runtime with repeatable samples and inspect representative action passages densely.
- Record timecodes, sample rate and scope. Separate what was directly seen from inference.
- A contact sheet cannot prove camera motion, acting continuity or a soundtrack cue. Do not claim a normal-speed full watch/listen unless it actually happened.
- The current Samurai study and its limitations are in docs/SAMURAI_REFERENCE_STUDY.md and docs/reference-studies/samurai-history-animation-review-2026-11-06.md.
- Do not copy protected characters, exact compositions, script, narration, music, SFX or frames.

## Visual storytelling modes
Rotate, with a narrative reason:
- character-led acting and physical action;
- geography, maps, coastlines, routes, fleets and formations;
- human relationships, domestic/political decisions and civilian stakes;
- world-building through streets, markets, workshops, smithies, ships, castles and landscapes;
- evidence/explanation through scrolls, calligraphy, portraits, timelines, rank cards, diagrams and myth/fact comparisons;
- time-change and legacy through uniforms, institutions, historical artwork, museum framing and recurring motifs.

The reference uses more than battle scenes: its sampled passages alternate mounted action, invasion geography, calligraphy/map transitions, craft/economic life, period change and museum/legacy framing. Transfer the variety principle, not the original character designs or shot compositions.

## Motion architecture
Every motion-led shot defines separate channels for actor, prop, environment, camera and graphics. At least two channels should move independently. Hero shots may use three or more, while some shots intentionally hold.
For physical action, show anticipation → action → contact → reaction → follow-through → recovery. The camera must not substitute for character/object action.
Build reusable walk/march/run/idle/gesture/group cycles; horse gait with linked rider bounce and visible hoof contact; draw/sheath/aim/release; projectile travel and target response; sword/spear/shield contact and recovery; ship/rowing/boarding; weather/cloth/water/smoke; and map/infographic reveals. Vary timing and phase to avoid synchronized repetition.

## Camera and editing language
Use establishing wides, medium group/action, close reactions, object inserts, profile/over-shoulder, tracking/travel, overhead geography and graphic tableaux. Specify camera start/end, angle/height, speed curve and narrative motivation. Use pull-backs to reveal scale, tracks to expose movement, push-ins for character decisions, and top-down views for spatial explanation when they actually help.
Keep screen direction coherent. Use match cuts, map-to-location transitions, graphic matches, wipes and sound J/L cuts for a reason. Avoid repeating the same slow zoom or map/face/army template.

## Engines and assets
Select H2 rigs, Remotion, Motion Canvas, Krita, Blender and FFmpeg by shot needs. Motion Canvas is a candidate for infographic work, not an assumed installed dependency. Benchmark a short moving shot and validate dependencies before scaling.
Search the existing 50 GB+ pool before external acquisition or AI generation. Invest in distinct environments, character/prop rigs, pose/expression sheets, historical art/document cards, map graphics, camera recipes and real source audio. Grow the library through curated gaps rather than bulk downloads.

## Audio: recordings first
- Search Build 76 and Meta Open Sound through audio-library/generated indexes and tools/audio/search_audio_resources.py.
- Consult docs/audio/HISTORICAL_FOLEY_COVERAGE_AUDIT.md and docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md.
- The dedicated CC0 pack workflow is .github/workflows/build-illustrated-history-foley-library.yml. It targets weapon handling/impacts, six-horse gallop, crowd shout, forge hammer and generic impacts; only use the versioned release after the workflow actually publishes it.
- Search by material, surface, action, environment and perspective. Prefer direct item-level matches over broad tag-assisted matches.
- Preserve the exact original recording, creator, source page, CC0/PD or project-use tier, file hash and technical metadata. Never place source-only/private raw media in public releases.
- Every acquired cue begins human_auditioned=false and approved_for_final_mix=false. FFprobe success is not a listening decision.
- Code is for editing real audio: synchronization, layering, looping, perspective, EQ, compression, ducking, reverb and mastering. Synthetic sounds are placeholders or documented exceptions, not the soundtrack default.

## Quality gates
- Prototype the hardest action and transition before a long render.
- Test deterministic output at arbitrary frame seeks.
- Review actual moving footage at normal speed, including contact/follow-through and camera changes.
- Review the full soundtrack at normal speed; keep separate stems and a timecoded defect/cue log.
- Render success is not artistic approval. Report technical pass, sampled review, complete human picture review and complete human audio review separately.


## Audio direction and audition gate

Use the Cannae five-shot cue plan in \`docs/audio/CANNAE_45S_AUDIO_CUE_PLAN.json\` as the reference for keeping narration, score, ambience, character Foley, prop Foley, impacts and intentional silence separate. The CC0 Foley v0.3.0 pack has an offline audition console; export and validate human decisions with \`tools/audio/validate_foley_review_decisions.py\` before adding asset IDs to a shot cue. Keep approved asset IDs empty while audition is outstanding. This pack does not contain a finished score or a complete battle ambience library.


The CC0 v0.3.0 pack includes modern orchestral score candidates. Treat them as optional music beds that still require human audition and historical/style review; do not imply they are period-authentic. The Cannae cue map lists candidates but leaves asset approvals empty.


## Environmental sound coverage — v0.4.0

The v0.4.0 CC0 pack adds five modern field-recorded environment beds: birds-before-rain in an Adelaide park, a small park river with wildlife, open-field wind, Vistula River waves and indoor howling wind. The recording context is part of the asset metadata and must guide use. These are not historical reconstructions; choose them only as neutral ambience when the scene matches. Do not imply they were recorded at the historical location. Human audition and the review validator remain required before cue approval.


## Cannae 45-second narration — generated, pending approval

The shot-aligned English narration is documented in `docs/audio/CANNAE_45S_NARRATION_SCRIPT.md`. An AI voiceover was generated in a deep, measured documentary style. [Open the generated full voiceover](https://www.aidocmaker.com/g0/audio?name=45ad22e901854f05b5b25b60aea6b6e6). It is split across the five CAN-01…CAN-05 shots in the cue map. Before final render, listen to the complete audio, check the pronunciations of “Cannae” and “Aufidus”, verify timing against the 45-second edit, and record human approval. The generated voice is a separate narration stem; it does not approve or replace the Foley/score review gates.
