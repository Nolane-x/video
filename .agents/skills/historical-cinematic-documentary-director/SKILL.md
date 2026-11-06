---
name: historical-cinematic-documentary-director
description: Use when creating or upgrading cinematic, high-motion historical documentaries with rich live-action/archival/3D/2.5D imagery, dynamic camera language and detailed production sound; distinct from H2 Squire vector animation.
---

# Historical Cinematic Documentary Director

## Route boundary

This is the preferred route for a historical documentary whose desired look is cinematic, richly animated, footage-led, 2.5D/3D, archival, or hybrid—such as a sweeping history of the samurai. It is **not** the Squire/H2 vector route.

- Use documentary footage, historical objects/photography, 2.5D projection, Blender/Three.js scenes, real camera paths, motion-graphic maps and carefully staged reenactment when they materially clarify the story.
- Use H2 Squire only when the user explicitly asks for the established symbolic round-headed/vector military style or an existing Squire series. Do not force every historical battle into repeated vector close-ups, maps and tactical boards.
- Remotion is an editorial/compositing timeline, not the H2 renderer. Blender is for real 3D staging, lighting, camera, rigging and depth. Krita is for authored illustrations, paintovers, maps and hand-drawn texture. FFmpeg is for media handling, proxies, finishing and QC.
- Choose the best engine per shot; name one primary pipeline and the specific secondary pipeline(s).

## Non-negotiable reference study

When the user supplies a film:
1. Hash and probe the exact file; record duration, resolution, timebase, frame rate, video/audio codecs, channel layout and sample rate.
2. Watch the complete reference at normal speed with sound. Build a time-coded scene log covering every cut and every sustained moving shot. Do not substitute thumbnails or contact sheets for the full watch.
3. Use PySceneDetect/FFmpeg for candidate boundaries, then correct false cuts from flashes, camera movement, overlays and fades.
4. Extract a low-rate overview across the whole runtime, then dense frame sequences around every complex action, transition, camera move, reveal, impact and text beat. Use optical flow/motion vectors to locate motion direction, speed changes, camera movement and frozen/looped footage.
5. Analyze audio separately: listen from start to finish; log music changes, ambiences, Foley, impacts, whooshes, silence, narration pauses, transitions and spatial distance. Use waveform/spectrogram analysis as supporting evidence only.
6. Record **observed facts** separately from hypotheses and taste judgments. Every technical observation must have a source timecode.
7. If the video cannot be decoded or auditioned in the current environment, set the review state to **BLOCKED_NOT_WATCHED**, preserve the exact reason and continue only with metadata/research. Never invent a timestamp log or claim full review.

Reference-study fields for each shot:
- shot ID, source in/out and duration;
- framing/scale (extreme wide, wide, medium, close, extreme close, insert);
- camera angle, lens impression, perspective and screen direction;
- camera motion (static, push, pull, track, pan, tilt, orbit, crane, handheld, whip, aerial, parallax);
- subject motion and action phase (anticipation, action, contact, reaction, follow-through, recovery);
- foreground/midground/background layers and depth cues;
- lighting direction, contrast, palette, atmosphere, texture and focus;
- edit/transition type, speed ramp, match cut or hold;
- text/graphics and their temporal behavior;
- audio layers and exact sound beats;
- what the technique achieves editorially.

Do not copy exact frames, characters, narration, script, music or proprietary footage. Translate high-level craft into original scenes, designs and timing.

## Three-pass editorial architecture

1. **Paper edit:** research ledger, claim-evidence map, script, chapter logic and emotional escalation. Separate accepted fact, estimate, disputed interpretation and illustrative reconstruction.
2. **Radio edit:** record/approve narration; cut the full narration and real sound bed before deciding the final picture duration. Let silence, breath, emphasis and music transitions shape the visual beats. Do not write a full visual montage before the spoken story has a coherent rhythm.
3. **Picture edit:** build the shot plan against the radio edit. Each shot must introduce a new action, place, scale, viewpoint, evidence, emotional state or visual metaphor. Use footage/photography, 3D, 2.5D, maps, archival documents, animation and typography as different visual instruments rather than repeating one template.

## Shot design and motion grammar

Each production shot must declare:
- narrative purpose and visual claim;
- exact duration and editorial in/out;
- shot scale, camera height/angle, lens/focal-length intention and focus plane;
- camera path with start/end position, orientation, speed curve and motivated destination;
- subject blocking, screen direction, staging, silhouette and prop interaction;
- foreground, subject plane and background/parallax depth;
- lighting, atmosphere, material response and palette;
- motion phases and the visible final state;
- transition to the next shot and its reason;
- narration phrase, music beat, ambience and spot-SFX cues.

Choose motion for the storytelling job, not to make every frame busy:
- camera moves: push/pull, lateral track, arc/orbit, crane/jib, pan/tilt, handheld drift, aerial top-down, reveal from behind foreground, dolly-through, rack-focus, whip-pan and locked-off contrast;
- subject/prop movement: gait, turn, draw, strike, parry, recoil, stumble, grip, release, cloth/armor follow-through, horse acceleration, formation compression, environmental reaction;
- layered animation: depth parallax, light sweeps, smoke/embers/dust, weather, moving shadows, cloth/flags, particles, map routes, typography timed to evidence;
- edit grammar: hard cut, motivated match cut, graphic match, J/L cut, action cut, cut-on-impact, dissolve for time/association, speed ramp for a defined kinetic beat, hold for weight, and occasional silence/black.

Camera movement alone is not character animation. A slow zoom over a static pose is not a motion shot. Show cause, contact, consequence and recovery. Motion must be frame-seek-safe and deterministic: frame N must not depend on wall-clock timers or previous renders. Test random seeks and temporal continuity.

Variety controls:
- avoid consecutive shots with the same scale, angle, camera path and composition unless the repetition deliberately communicates a pattern;
- no long sequence of generic faces, sword props, repeated army rows or interchangeable overhead diagrams;
- alternate broad geography, embodied action, material inserts, human reaction, evidence detail and visual metaphor;
- maps are used only where geography is the point;
- every sequence has a distinct spatial/lighting identity, not just a different caption over the same set.

## Use the existing 50 GB resource pool first

Before generating new media or writing procedural stand-ins:
1. Search the current Build 76 release indexes and the asset-to-bundle map for the shot's required material, footage, photographs, 3D models, textures, overlays and sound.
2. Search by multiple synonyms, period/region/material/action, not only by the exact narration word.
3. Review candidate metadata, original source URL, per-item license, attribution, resolution/duration/format, SHA-256 and package location.
4. Preview/audition the chosen asset. A filename or tags alone do not prove it is suitable.
5. Prefer existing resources where quality and context match. Generate or source something new only for a specific uncovered need.
6. Keep the global library workstream separate: do not modify video-library/**, source catalogues, downloaders, packagers or its workflows from this production route.

The Build 76 Release already exposes separate audio archives for Kenney, OpenGameArt, originals, USGS, NASA and Wikimedia. See audio-library/SOURCES.json. These are inventory starting points, not a blanket license: every selected file still needs its source record and rights status.

## Audio: recordings first, code second

The soundscape is a core part of the film, not a late garnish.
- Search and audition the existing recording library before synthesizing, generating or downloading more material.
- Use recorded ambience, Foley, weapons, animals, crowds, footsteps, cloth, armor, fire, wind, water, room tone and impacts. Use licensed musical recordings/stems or genuinely performed sample-based music.
- Do not use oscillator-generated melodies, synthetic sword clashes, procedural crowd beds or generic whooshes as the default. Code may arrange, synchronize, pan, EQ, compress, reverberate, duck and master real recordings; it should not replace them.
- Keep separate stems: narration/dialogue, score, location ambience, environmental detail, footsteps/cloth/armor Foley, weapons/impacts, crowd/animals, transitions and designed accents.
- Sound effects must correspond to visible material, distance, mass, timing and perspective. Sync transients to contact, not merely to the start of a shot.
- Use at least two or three distinct takes/layers for repeated prominent events where available. Avoid the same sword/impact sound on every cut.
- Respect room tone and sound perspective across edits. Use J/L cuts to bridge locations when appropriate. Silence is an intentional layer.
- Mix music under dialogue with story-sensitive automation; don't fill every pause.
- Every external file keeps exact source URL, rights/attribution, SHA-256, original file, sample rate, channel count, loudness and audition status. A file not auditioned is a candidate, not approved sound.
- Never publish Sonniss or other source-only/licensed pack files as a standalone archive. Use only under the actual terms and keep raw files private when required.

## Engine and shot allocation

- **Remotion:** main editorial timeline, narration, captions, compositing, timecoded media, 2D overlays and render sequencing.
- **Blender:** cinematic 3D reconstructions, camera choreography, architecture, terrain, large formations, physically motivated lighting, atmosphere, depth of field and selected high-impact inserts.
- **Three.js/GSAP:** seek-safe 2D/3D camera and title animation when the scene is better as browser-rendered graphics; test non-linear frame seeking.
- **Krita:** painted maps, historical illustration, textured overlays, cleanup and frame-by-frame additions.
- **H2 Squire:** only for explicitly requested Squire/vector sequences or a planned visual insert.
- **FFmpeg/PySceneDetect/OpenTimelineIO:** reference analysis, scene logging, proxy generation, retiming, edit interchange, sound processing and QC.

Do not assume a binary, model, font, rig or plugin is installed because its skill exists. Verify the pinned dependency and an actual smoke render before planning around it.

## Preview and approval gates

1. Prototype the most difficult action and camera move as a short sequence before a full film.
2. Review the actual moving clip at normal speed and frame-by-frame around the key action; review the complete sound.
3. Render an animatic, then a representative 30–60 second picture/sound sample with final style, camera variety, real assets and layered audio before committing to a long render.
4. Inspect scene coverage, camera path, depth, temporal artifacts, repeated composition, character continuity, evidence readability, transitions, captions and sync.
5. Technical QC: ffprobe, duration/FPS/codec, missing frames, black/freeze segments, audio stream, loudness, true peak, clipping, caption coverage, file hash.
6. Artistic QA requires uninterrupted full-length viewing with sound and a time-coded defect log. Contact sheets are secondary evidence, never a substitute.
7. Keep last-known-good masters. New output stays a candidate until human review and user approval.

## Deliverables

Research/claim ledger, exact reference study, script/radio edit, film bible, timecoded shot JSON, asset/rights manifest, source-audio manifest, separate audio stems, project files, preview, contact sheets, motion QA, full render, SHA-256, technical QA and handoff. Explicitly list all open approval gates.
