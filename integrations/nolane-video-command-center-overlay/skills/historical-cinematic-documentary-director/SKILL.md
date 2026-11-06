---
name: historical-cinematic-documentary-director
description: Use for cinematic, motion-rich history documentaries with archival/real footage, 2.5D/3D worlds, motivated camera choreography, diverse editing grammar and detailed recorded sound. Do not route these projects into Squire by default.
---
# Historical Cinematic Documentary Director

## Route boundary
Use this route when the reference or brief asks for footage-led, richly layered, high-motion historical documentary craft. It is separate from H2 Squire. H2 Squire is used only when the user explicitly requests the Squire vector style or an existing Squire series. Select Remotion, Blender, Three.js/GSAP, Krita, archival footage, 2.5D and H2 per shot; never treat tool availability as art direction.

## Mandatory reference study
- Probe/hash the exact file and record duration, resolution, fps/timebase, codecs, audio layout and sample rate.
- Watch the full picture with sound at normal speed. Build a timestamped log for every cut and sustained moving shot.
- Detect candidate cuts with PySceneDetect; manually correct flashes, camera-motion false positives, fades and long shots whose action changes internally.
- Build a whole-film overview plus dense frame runs at 8–12 fps around camera moves, transitions, reveals, title beats and complex actor/prop actions.
- Analyze camera and subject movement separately using optical flow/motion vectors when available.
- Listen to the complete soundtrack and log music, ambience, Foley, impacts, whooshes, narration, silence, J/L cuts and spatial perspective.
- Separate observed facts from interpretation. If decoding/listening is impossible, record BLOCKED_NOT_WATCHED and do not invent timecodes.

## Three-pass edit
1. Paper edit: sourced claim ledger, script, evidence, estimates/contested interpretations and story turns.
2. Radio edit: narration, actual recorded ambience/Foley and licensed score. Cut the audio narrative first; preserve pauses and silence.
3. Picture edit: build each shot to the radio edit using archival/real footage, 3D, 2.5D, maps, animation, documents and motion typography only when each adds meaning.

## Shot grammar
Each shot records purpose, exact duration, scale, camera height/angle/lens intention/focus, start/end camera position, motion path/speed curve, screen direction, actor and prop blocking, anticipation/contact/reaction/follow-through/recovery, foreground/midground/background depth, lighting/materials, transition reason and sound cues.

Use wide geography, aerials, tracking, dolly push/pull, orbit, crane, pan/tilt, handheld drift, whip, rack focus, macro inserts, action cuts, graphic matches, match cuts, J/L cuts, speed ramps and deliberate holds. Motion must be motivated. Camera zoom alone over a static pose does not count as action. Show physical cause, contact, consequence and recovery. Test deterministic random frame seeking.

Avoid repeated generic faces, repeated weapon inserts, same army-row compositions and maps used as filler. Change spatial identity, scale, camera grammar, action and evidence. A shot should change information, relationship, place, action or emotional state.

## Existing resource library first
Search Build 76 asset indexes and bundles before generation or new download. Match historical photo, museum object, footage, model, texture, overlay and sound by actual metadata; inspect previews and per-item rights. Preserve source URL, license, attribution, hash and bundle location. Read the new audio-library source map. Do not modify video-library/** or its parallel downloader/build workflows.

## Recorded sound first
Search and audition the existing 1.14 GB audio bundles before any synthetic sound design or new downloads. Prefer real Foley, weapon/material contact, cloth, armor, footsteps, animals, crowds, weather, environmental recordings and actual licensed music or performed sample-based scores. Code should synchronize, layer, pan, duck, EQ, compress, reverb and master real audio. Do not use oscillator music or synthesized impacts as the normal final source. Keep stems separate and preserve intentional silence. Track exact source, license, attribution, checksum and human audition status. Sonniss/source-only packs must never be publicly mirrored.

## Preview and approval
Prototype the hardest motion, then build a representative 30–60 second visual/audio sample with multiple shot scales, a real camera path, physical action, layered depth and selected recordings. Review the moving clip and audio at normal speed before long renders. Full-film viewing/listening and a timecoded defect log remain mandatory. Technical success and contact sheets are not artistic approval.
