# Reference study — The Entire History of the Samurai

Study date: 2026-11-06  
Source: user-supplied MP4. The video, extracted frames and audio are not copied into this repository.  
Purpose: learn reusable visual grammar for original illustrated-history films, not reconstruct copyrighted frames or assets.

## Evidence scope

The supplied file probes as 700.267 seconds, 1280×720, AV1 at 30 fps (21,008 frames), with AAC stereo audio at 44.1 kHz. I mapped the full runtime with 350 stills sampled every 2 seconds and reviewed 13 high-motion intervals at 4 fps. The intervals cover 00:00–00:06, 00:14–00:20, 00:33–00:39, 00:44–00:52, 01:06–01:12, 01:20–01:26, 03:20–03:26, 04:10–04:16, 05:50–05:56, 07:55–08:05, 09:00–09:08, 10:20–10:30 and 11:00–11:12.

This is a systematic whole-runtime sample plus dense action sampling. It is not a claim that every frame was inspected or that the complete film and soundtrack were perceptually watched/listened to at normal speed. Audio was technically measured but not fully auditioned; instrument and individual Foley identification remain unverified.

## Visual grammar observed

### Character acting and props
- Compact stylised 2D characters use stable proportions, costume silhouettes and readable facial expressions to separate leaders, soldiers and civilians.
- Acting is pose-led: looking, pointing, walking, running, aiming, climbing, boarding, reacting, cheering and expression changes.
- Horse/rider motion uses a repeatable gait and linked rider bounce. The horse image later returns as a motif callback to the opening.
- Weapons and tools are staged as actions, not icons: preparation, movement/release, contact or reveal, reaction and settle.
- Crowd life comes from staggered silhouettes, spacing and camera changes; every background figure need not be independently animated.

### Environments and secondary motion
- Locations change with the historical beat: battlefield, road, rain-soaked settlement, ship/port/sea, market, training hall, political room, map/tableau and landscape.
- Walls, rooftops, lanterns, flags, trees, hills, ships and terrain explain where the story happens.
- Secondary motion includes horse legs, rider bounce, boat bob, water, smoke, rain, banners, clouds and foreground parallax.
- Strong shots separate foreground, actor/prop, environment and graphics into layers with different movement.

### Camera, cut and information design
- Shot sizes alternate: establishing wide, medium action, close reaction, insert, overhead map/formation and graphic panel.
- Camera scale changes with the information. Close-up for identity/emotion; overhead for geography; broad framing for fleet/army scale; inserts for actions that are unclear in a wide.
- Reframing and lateral tracking accompany action; a universal slow zoom is not the motion language.
- Story graphics include portrait/rank cards, banners/nameplates, timelines, route paths, marker icons, highlighted ship groups, comparison panels and myth/fact call-outs.
- A recurring horse/rider image connects distant parts of the film.

## Timecoded observations

| Time | Observation | Lesson |
|---|---|---|
| 00:00–00:06 | Horse/rider cold open with cyclic leg motion, rider bounce and smoke/environment layers; then a tighter pointing beat. | Open with an action and recurring visual motif; animate rider and horse as linked systems. |
| 00:14–00:20 | New character/formation and contextual change. | Establish visual variety early; do not hold one establishing tableau. |
| 00:33–00:39 | Parchment Japan map; markers and tokens appear; highlighted leader arrives; a red route progressively draws north; cut to a rainy street group. | Build maps in causal order: context, tokens, route, then human consequence. |
| 00:44–00:52 | Mounted archer changes pose; bow/arrow action; target insert. | Animate the prop path and target response; use an insert when a wide shot cannot explain the action. |
| 01:06–01:12 | Opposing formations, flags and close reactions form a face-off. | Establish sides and screen direction before battle. |
| 01:20–01:26 | Another action/context change breaks up the battle sequence. | Alternate combat with travel, social and political history. |
| 03:20–03:26 | Boat with figures, deck/ladder action, fleet-wide composition, highlighted units and question marker. | Move from human-scale action to strategic geography, then point to the relevant unit. Animate water and ship as well as people. |
| 04:10–04:16 | Human relationship beat provides a pacing contrast. | History needs emotional/human beats, not just fighting and leaders. |
| 05:50–05:56 | Portrait/rank reveal, red hero composition, sunset/nameplate, then a street walk scene. | Let identity graphics become a transition into the scene, not a detached slide. |
| 07:55–08:05 | Family/domestic emotional material. | Show civilian life and stakes between conflicts. |
| 09:00–09:08 | Market/economic staging with merchants, goods and explanatory board graphics. | Show social/economic causes with props, groups and data graphics. |
| 10:20–10:30 | “THE MYTH” treatment, archival-style artwork, comparison bubbles, red cross-out, then cannon/formation imagery. | State a claim, visualise it, correct it and show the consequence. |
| 11:00–11:12 | Timeline/map and training lead back to the horse/rider motif; expression close-up and historical artwork follow. | Pay off motifs and bridge original animation with source-era art. |

## Motion grammar to implement

Each motion-led shot must author separate channels:
1. Actor — pose, limbs, face, gaze, weight shift and timing.
2. Prop — held object, weapon/arrow, bowstring, shield/armor, rigging or horse tack.
3. Environment — rain, smoke, sea, flags, fire, dust, clouds, crowd offset and foreground parallax.
4. Camera — lock, track, pan, push/pull, tilt or reframe with an explicit narrative reason.
5. Graphics — route reveal, marker travel, portrait/name reveal, statistic count, timeline, callout or myth/fact wipe.

At least two channels should move independently in motion-led shots; selected hero beats may use three or more. Holds are valid. Motion everywhere is not the goal.

Build reusable cycles for walk, march, run, idle, talk/gesture, group reactions, horse gaits, rider bounce, draw/aim/release, arrow travel/impact, sword contact/recoil/recovery, rowing/boarding, smoke/fire/rain/wind cloth/water, crowd offsets, map route reveals, portrait cards and data graphics. Stagger cycle phases to prevent a mechanically synchronized crowd.

## Audio facts and limits

A PCM working conversion measured approximately −14.2 LUFS integrated, 2.9 LU LRA and −1.6 dBTP true peak. A silence detector at −38 dB found only a final interval of about 0.63 seconds. This does not identify instruments, specific SFX or music structure. Do not claim a subjective listening review based on those measurements.

A future cue sheet must be verified while listening at normal speed. Separate narration, score, atmosphere/room tone, character Foley, object/weapon impacts, transitions and intentional silence. Sync transients to visible contact: hoof landing, blade contact, arrow release, rope/boat contact and graphic reveal.

## Production implications

- This is an illustrated-history route, distinct from the existing H2 Squire vector route and from footage-led documentary.
- Select engines per shot: established rigs, Remotion or Motion Canvas for timeline/infographic work, Krita for authored 2D art, Blender for shots that truly need 3D depth/physics, and FFmpeg for assembly/mastering. Motion Canvas is a candidate, not an assumed installed dependency.
- Build 76 already exceeded the 50 GB globally unique resource target. The next investment is curated sound selection, better search tags, historical character/prop cycles, diverse environments and camera choreography—not another indiscriminate bulk download.
- Do not store the user's supplied video, audio or extracted frames in public repository history.
- A new film is not approved until its full moving picture and soundtrack have been reviewed at normal speed and defects logged with timecodes.
