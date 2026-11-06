# Illustrated History Motion System

Version: 1.0  
Purpose: turn the Samurai reference study into repeatable production rules for original illustrated/cartoon history films.

## 1. The unit of design is a shot, not a template

A paragraph or narration sentence is not automatically one shot. Break the story at changes in:
- place or time;
- action and physical cause/consequence;
- character relationship or emotional state;
- information (geography, scale, evidence, comparison, claim);
- point of view or dramatic emphasis.

Each shot needs one dominant story purpose. Avoid changing the background only to create superficial variety. A shot must reveal new action, information, relationship, place, scale or emotional state.

The storyboard must include:
- shot ID and narrative beat;
- exact in/out frame or time;
- location and time of day/weather;
- shot size, angle, height, screen direction and focus;
- camera start/end position and motivated path;
- character blocking, gaze and body performance;
- prop state and physical contact;
- foreground/midground/background layers;
- graphic layer and reveal sequence;
- edit/transition motivation;
- source asset IDs and rights class;
- sound cue IDs and exact sync event.

## 2. Five independent motion channels

Treat each channel separately in the shot plan and timeline.

### Actor / character
Use hierarchical rigs with a stable silhouette and readable joints. Include head/gaze, torso, shoulders, upper/lower arms, hands, pelvis, upper/lower legs, feet and optional secondary pieces (hair, sleeves, armor straps, cloak). Reuse rigs, but author character-specific proportions, costume, facial design and acting.

Plan anticipation, action, contact, follow-through, recovery and settle. Include weight shifts, balance corrections, eye-lines and reactions. Avoid floating hands, feet sliding across ground, weapons detached from grip or riders that do not follow horse movement.

### Prop / physical interaction
Props have state and weight. A sword draw, bow shot, shield block, oar stroke, rope pull, gate opening or object hand-off should show a visible causal chain. Keep attachment points stable. The prop must respond at the same contact frame as the actor.

### Environment
Animate only the layers that serve the shot: parallax hills/rooflines, clouds, wind-blown banners, smoke, rain, waves, dust, fire, crowds, foliage, ship bob or atmospheric particles. Give foreground/midground/background different rates and directions when the camera moves. Do not apply parallax to every shot by default.

### Camera
Choose one motivated move: locked, pan, tilt, lateral track, push, pull, orbit, crane, handheld drift or reframing. Specify start and end values, duration, easing and why the move reveals information. Camera movement does not replace subject action. Avoid applying the same slow zoom to every static illustration.

### Graphics / information
Reveal routes, borders, labels, portraits, dates, ranks, stats and diagrams in narrative order. Examples:
1. establish geography;
2. reveal the relevant place/actor/group;
3. draw the route or show the movement;
4. reveal the result/consequence.
Animate timeline progression, chart fills, count-ups and callout anchors only when the narration supports them. Keep labels legible and on screen long enough to read.

A motion-led shot normally uses at least two independent channels. Hero moments may use three or more. Some shots should deliberately hold still.

## 3. Reusable action and cycle library

Build reusable, frame-seek-safe cycles as small components:
- idle, look, speak, point, turn, walk, march, run, kneel, fall, stand, group cheer/panic;
- horse walk/trot/gallop/rear with linked rider bounce, rein/tack response and hoof contact;
- draw, aim, release, projectile travel, impact, recoil, block, parry and recovery;
- rowing, sailing, ship bob, boarding, ladder climb, rope/rigging movement;
- wind cloth, flag wave, rain, smoke, fire, water/waves, cloud drift, dust, foliage and crowd phase offsets;
- map route draw, marker travel, location highlight, portrait card, timeline, stat panel and myth/fact reveal.

Cycles must support arbitrary frame seeking. Store explicit phase/time state; do not depend on previous-frame mutation. Stagger repeated crowd/horse cycles to avoid a synchronized army.

## 4. Camera and edit grammar

Use a changing shot-scale ladder:
- establishing wide for geography and scale;
- wide/medium for group blocking;
- close reaction for identity/emotion;
- insert/macro for a decisive object or contact;
- over-shoulder/profile for point of view;
- high-angle/overhead for formations and maps;
- graphic/tableau for claims, rank, timelines and comparisons.

Build screen direction before action cuts. Use match cuts, graphic matches, wipes, map-to-location transitions and sound J/L cuts with a reason. Alternate movement-heavy scenes with human, social, political, training, travel, economic and aftermath beats. Do not let battle imagery dominate all historical sections.

## 5. Original art and resource strategy

Use original character design and scene composition. Never copy a reference's exact characters, frames, script, narration, music or SFX.

Search the existing 50 GB+ library by category before creating or acquiring new assets. Prioritize missing location packs, historical props, character poses, cloth/armor variations, maps, ship/horse/environment sets and real recordings. The global library has already surpassed its byte target; improve retrieval and actual shot diversity rather than indiscriminate bulk.

Per shot, record source IDs, exact source page, creator, file hash and rights class. Keep CC0/Public Domain, attribution-required and project-use/private media separate.

Select render technology per shot:
- Remotion: editorial timing, captioning, graphic composition and deterministic scene sequencing;
- Motion Canvas: vector animation/infographic candidate, only after dependency and sample-shot validation;
- Krita: authored character/environment artwork and painted frames;
- Blender: depth, camera, lighting, physical interactions and shots where 3D provides real value;
- FFmpeg: media probes, mix/assembly, transcodes and final mastering.
Do not choose a renderer just because it is available. Prototype the hardest action before scaling.

## 6. Sound belongs to the physical action

Use the audio-library source map and playable preview packs first. For every shot, plan ambience, music, Foley, spot effect and intentional silence separately. Sync the transient to the visible event: hoof landing, blade contact, bow release, arrow impact, rope/wood creak, footstep, graphic reveal.

Use close/medium/far perspective and different takes for repeated actions. OGG previews are for audition; use the matching high-quality source masters for production. Do not call an audio file production-ready until a person has listened to it and verified the exact rights record.

Code should select, sync, layer, loop, pan, EQ, compress, duck, reverberate and master recordings. Procedural tones/noise are temporary placeholders or occasional designed accents.

## 7. Diversity and repetition gates

Before a long render, generate a shot-contact sheet and a timeline overview. Detect repeated backgrounds, character blocking, camera moves, props and scene templates. A recurring motif is intentional only when it creates a meaningful narrative callback.

For a representative 30–60 second sample, aim to demonstrate:
- at least 5 meaningfully different shot scales/angles;
- at least 3 distinct visual spaces or environmental states where story permits;
- at least 3 kinds of character/prop action;
- at least 2 independent environment/camera/graphic motion treatments;
- at least 1 geography or information reveal if the story needs it;
- audible narration, ambience, Foley/spot sound and score layers where appropriate.

These are sample targets, not an inflexible checklist for every sequence. Do not fake variety by flashing shots too quickly. A shot lasting over ~6 seconds needs an intentional hold or visible internal progression; it need not always be moving.

## 8. QA gates

### Technical
- deterministic rendering under random frame seeking;
- no missing layers, broken fonts, out-of-frame props, unintended clipping or alpha issues;
- no repeated frame freezes unless intentionally held;
- accurate aspect ratio, fps, frame count, audio sync and loudness/true-peak checks.

### Motion/artistic
Review moving picture at normal speed. A contact sheet is not sufficient. Check foot/hand contact, balance, pose arcs, prop attachment, cause/contact/reaction, camera motivation, readable information and composition repetition. Record exact timecodes.

### Audio
Listen to the full soundtrack at normal speed. Log narration, score, ambience, Foley, impact, distortion, noise, clipping, abrupt loop points and bad synchronization. Keep stems and rights/attribution records.

Technical pass is not visual approval or publication approval. The final report must separate machine QA, sampled review and full human review.
