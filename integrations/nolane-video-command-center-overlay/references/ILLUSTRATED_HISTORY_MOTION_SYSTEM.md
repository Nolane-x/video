# Illustrated History Motion System

Version: 1.1  
Purpose: turn the Samurai reference study into repeatable production rules for original illustrated/cartoon history films.

## 0. Reference-derived visual strategy

The Samurai reference demonstrates a multi-form illustrated history language, not a single animation trick. The sampled film moves between character acting, mounted action, opposing formations, ships and invasion geography, calligraphy, route maps, workshop/social life, period transitions, historical artwork and legacy/museum framing.

Use this as a reusable vocabulary, not as a storyboard template. Original work must create its own characters, art direction, locations, symbols and compositions.

### Sequence modes to rotate with narrative purpose

- **Embodied action:** character close-ups, gesture, walk/run/ride, archery, weapon handling, impact and group reaction.
- **Geography and scale:** maps, coastline/terrain, fleet/army markers, routes, formations and overhead views.
- **Human stakes:** family, loyalty, political negotiation, fear, grief, celebration and civilian life.
- **World building:** markets, workshops, smithies, training, architecture, ships, roads and material culture.
- **Evidence and explanation:** scrolls, calligraphy, portraits, date/rank cards, diagrams, myth/fact comparisons and historical artwork.
- **Change and legacy:** costume/institution shifts, timelines, ruins, museum/painting frames and returning motifs.

A good sequence changes the kind of information the viewer receives. Do not make every paragraph a face close-up, battle panorama or map. Do not insert a new location without a narrative reason.

### Reference observations to apply

- The opening sampled passage moves from a horse/rider action to commander/formation scale and close action. Build a clear action hook, then expand context.
- Invasion passages move between ship/landing imagery and strategic geography; show both the human event and the route/scale.
- Calligraphy and a wind/map motif create an information transition across eras. Use symbols/typography as narrative devices, not decoration.
- Social/workshop passages communicate the economic and material world beyond battles.
- Later-era and museum/legacy passages provide temporal distance and a visual payoff to earlier motifs.

The exact sampled timecodes and limitations are in docs/SAMURAI_REFERENCE_STUDY.md and docs/reference-studies/samurai-history-animation-review-2026-11-06.md.

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
Use hierarchical rigs with a stable silhouette and readable joints. Include head/gaze, torso, shoulders, upper/lower arms, hands, pelvis, upper/lower legs, feet and optional secondary pieces (hair, sleeves, armour straps, cloak). Reuse rigs, but author character-specific proportions, costume, facial design and acting.

Plan anticipation, action, contact, follow-through, recovery and settle. Include weight shifts, balance corrections, eye-lines and reactions. Avoid floating hands, feet sliding across ground, weapons detached from grip or riders that do not follow horse movement.

### Prop / physical interaction
Props have state and weight. A sword draw, bow shot, shield block, oar stroke, rope pull, gate opening, brush stroke or object hand-off should show a visible causal chain. Keep attachment points stable. The prop must respond at the same contact frame as the actor.

### Environment
Animate only the layers that serve the shot: parallax hills/rooflines, clouds, wind-blown banners, smoke, rain, waves, dust, fire, crowds, foliage, ship bob or atmospheric particles. Give foreground/midground/background different rates and directions when the camera moves. Do not apply parallax to every shot by default.

### Camera
Choose one motivated move: locked, pan, tilt, lateral track, push, pull, orbit, crane, handheld drift or reframing. Specify start and end values, duration, easing and why the move reveals information. Camera movement does not replace subject action. Avoid applying the same slow zoom to every static illustration.

### Graphics / information
Reveal routes, borders, labels, portraits, dates, ranks, stats, diagrams, timelines, handwritten calligraphy and myth/fact comparisons in narrative order. A map reveal can follow:
1. establish geography;
2. reveal the relevant place/actor/group;
3. draw the route or show the movement;
4. show arrival, resistance or consequence;
5. transition to the human-scale scene.

Animate timeline progression, chart fills, count-ups and callout anchors only when the narration supports them. Keep labels legible and on screen long enough to read.

A motion-led shot normally uses at least two independent channels. Hero moments may use three or more. Some shots should deliberately hold still.

## 3. Character, environment and asset investment

Build reusable, original asset families rather than generating one-off generic inserts.

### Character and acting kit
- role silhouettes and costume layers for leaders, retainers, soldiers, civilians, artisans, merchants, monks, sailors and officials;
- expression sheet: neutral, alert, suspicious, anger, fear, grief, relief, resolve and joy;
- gesture set: speak, point, command, bow, look back, draw, aim, hold, strike, block, recoil, carry and work;
- rig pivots, ground-contact points, hand/prop attachment points and costume secondary motion.

### Environment and prop kit
- distinct environment families: castle exterior/interior, village street, mountain road, coast/harbour, ship deck, market, forge/workshop, training ground, political chamber, shrine/temple, battlefield and later-era city;
- period-specific prop families: armour, blades, bows, arrows, banners, scrolls, maps, tools, boats, timber architecture, signs, work objects and documents;
- layered foreground/midground/background plates for camera parallax and occlusion.

### Graphic language
- map/route animation with a consistent symbol grammar;
- portrait/rank/name cards and statistics;
- timelines and era transitions;
- calligraphy/scroll/document reveals;
- myth/fact and claim/evidence/correction panels;
- archival-art/museum framing where historically supported.

Every family needs source/provenance or original-creation status, rights, resolution, style consistency and a working preview. Search the existing 50 GB+ asset library before making new assets; do not grow it indiscriminately.

## 4. Reusable action and cycle library

Build reusable, frame-seek-safe cycles as small components:
- idle, look, speak, point, turn, walk, march, run, kneel, fall, stand, group cheer/panic;
- horse walk/trot/canter/gallop/rear with linked rider bounce, rein/tack response and hoof contact;
- draw, aim, release, projectile travel, arrow pass, impact, recoil, block, parry and recovery;
- rowing, sailing, ship bob, boarding, ladder climb, rope/rigging movement;
- wind cloth, flag wave, rain, smoke, fire, water/waves, cloud drift, dust, foliage and crowd phase offsets;
- map route draw, marker travel, location highlight, portrait card, timeline, stat panel and myth/fact reveal.

Cycles must support arbitrary frame seeking. Store explicit phase/time state; do not depend on previous-frame mutation. Stagger repeated crowd/horse cycles to avoid a synchronized army.

## 5. Camera and edit grammar

Use a changing shot-scale ladder:
- establishing wide for geography and scale;
- wide/medium for group blocking;
- close reaction for identity/emotion;
- insert/macro for a decisive object or contact;
- over-shoulder/profile for point of view;
- high-angle/overhead for formations and maps;
- graphic/tableau for claims, rank, timelines and comparisons.

Build screen direction before action cuts. Use match cuts, graphic matches, wipes, map-to-location transitions and sound J/L cuts with a reason. Let camera paths reveal or withhold information: a lateral track can expose a formation, a pull-back can reveal a fleet, a push-in can isolate a character's decision, and a top-down move can clarify geography. Do not stack arbitrary camera moves in one shot.

Vary shot scale, angle, camera path, visual mode, location and emotional energy over a sequence. No universal cut rate is required. A long hold is valid when the picture has readable internal progression or deliberate emotional weight.

## 6. Audio belongs to the physical action

Use the audio-library source map and playable preview packs first. Search by action + material + surface + distance, not broad tags alone.

- Build 76 and Meta Open Sound are the broad existing catalogues.
- The targeted illustrated-history CC0 pack is specified by docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md and tools/audio/illustrated_history_foley_sources.json; its GitHub Actions workflow downloads and packages weapon handling/impacts, horse gallop, crowd shouts, smithy hammer and generic impacts.
- The source audit still identifies missing horse surface round-robins, tack/reins, shield impacts, chainmail/armour, distant commands and Japanese environment beds. Do not claim a full cavalry Foley bank yet.
- Every new source must carry source page, creator, exact license, file hash and technical metadata. Keep source-only/private assets out of the public release.
- Every acquired sound starts un-auditioned. A successful FFprobe/catalog build does not approve the sound.

For every shot, plan ambience, music, Foley, spot effect and intentional silence separately. Sync the transient to the visible event: hoof landing, blade contact, bow release, arrow impact, rope/wood creak, footstep or graphic reveal. Use close/medium/far perspective and different takes for repeated actions.

Code should select, sync, layer, loop, pan, EQ, compress, duck, reverberate and master recordings. Procedural tones/noise are temporary placeholders or occasional designed accents, not the default soundscape.

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
- accurate aspect ratio, fps, frame count, audio sync and loudness/true-peak checks;
- every audio item has a source/license/hash record and a human audition state.

### Motion/artistic
Review moving picture at normal speed. A contact sheet is not sufficient. Check foot/hand contact, balance, pose arcs, prop attachment, cause/contact/reaction, camera motivation, readable information and composition repetition. Record exact timecodes.

### Audio
Listen to the full soundtrack at normal speed. Log narration, score, ambience, Foley, impact, distortion, noise, clipping, abrupt loop points and bad synchronization. Keep stems and rights/attribution records.

Technical pass is not visual approval or publication approval. The final report must separate machine QA, sampled review and full human review.
