---
name: illustrated-history-animation-director
description: Use when the user requests polished illustrated/cartoon history films with lively 2D character acting, animated maps and infographics, historical set changes, layered camera motion and varied editorial grammar; especially when a supplied reference is the target for study.
---
# Illustrated History Animation Director

## Purpose and route
This is a distinct route for animated historical explainers (samurai, Japan, empires, military history, biographies, inventions and social history). It is **not automatically the H2 Squire style** and is not the footage-led cinematic documentary route. Analyse the reference and select an engine and asset strategy per shot. Never assume that the source video's exact software, budget or production method is known.

## Production reference

For shot schemas, the five independent motion channels, camera grammar, repeatability gates and full moving QA, follow `references/ILLUSTRATED_HISTORY_MOTION_SYSTEM.md`. The exact Samurai sample map and honest evidence scope live in `docs/reference-studies/samurai-history-animation-review-2026-11-06.md` in the repository.

## Reference study: required evidence
1. Probe the source file: duration, resolution, frame rate, codecs, audio layout and variable-frame-rate status.
2. Sample the full runtime at a repeatable interval (normally every 1–2 seconds) to map the complete visual arc. Create contact sheets with timecodes.
3. Select representative action-heavy intervals and sample them densely (normally 4–8 fps; 10–15 fps for especially fast motion). Inspect start, anticipation, midpoint, contact, follow-through, recovery and transition.
4. Record shot size, angle, camera path, subject action, prop interaction, environment movement, graphic overlays, transition, colour/light, sound cue and confidence for each observation.
5. Separate direct observation from inference. A still/contact sheet cannot prove a moving action, camera path or soundtrack detail. Never claim every source frame was inspected unless that was actually done.
6. Do not copy the reference's characters, exact compositions, scripts, narration, music, SFX or copyrighted frames. Extract visual grammar and produce original designs.

## Visual grammar to adapt, not imitate
Mix these forms with narrative intent:
- Character-led scenes: distinct poses, gaze, facial acting, walk/run cycles, riding, bow/weapon handling, recoil, group reactions and prop interaction.
- Environment-led scenes: castle interiors, roads, villages, ports, ships, markets, training grounds, temples, battlefields and weathered terrain, staged with foreground/midground/background depth.
- Story graphics: animated maps, routes that draw progressively, moving troop/ship markers, timeline reveals, stat/portrait cards, hierarchy diagrams, split comparisons, myth/fact cards and annotated historical art.
- Editorial variety: establishing wides, medium group action, close reaction, object inserts, over-shoulder, profile/tracking, overhead/map, tableaux and brief graphic transitions.
- Motif callbacks: bring back a character, object, map symbol, camera composition or visual metaphor when it creates a meaningful narrative echo.

Do not turn this into a mandatory checklist for every shot. Each shot needs one dominant story purpose and a clear visual hierarchy. Variety means meaningful changes in visual information, not random scene changes.

## Motion design and character performance
For each important shot define separate channels:
1. Actor/body performance (pose, limbs, face, gaze, weight and timing).
2. Props and physical response (weapon path, bowstring/arrow, shield recoil, cloth, horse tack, boat/vehicle response, debris and contact).
3. Environment (rain, wind, smoke, waves, banners, fire, crowds and parallax layers).
4. Camera (locked, pan, track, push, pull, tilt, orbit, crane or motivated reframing).
5. Information graphics (route drawing, labels, markers, chart fills, card entrances and wipes).

At least two channels should create independent, story-motivated motion in a motion-led shot; three or more may be used for a hero shot. Camera movement alone does not count as character action. Avoid motion clutter: keep a primary focal action, secondary motion and a readable settle.

For physical action, plan anticipation → action → contact/impact → follow-through → recovery. Make the prop respond at contact, keep hands/feet connected to objects and ground, and keep gaze aligned. For cycles, design reusable walk/march/run, horse gait, rowing, sailing, idle and crowd loops with phase variation so copied cycles do not look synchronized. Use held poses and limited animation where they help readability; do not make every part move continuously.

## Camera and editing rules
- Build a shot-scale ladder: establishing wide → medium action → close reaction/insert → geography or return to the environment as appropriate.
- State why the camera moves and what information it reveals.
- Use lateral tracking for travel/progression, push-ins for recognition/threat, pull-backs for scale/context, top-down for geography and inserts for important evidence/objects.
- Use match cuts, direction continuity, graphic matches and motivated wipes. Keep screen direction coherent across action cuts.
- Vary shot length to narration and action beats. Do not force a fixed shot duration or cut rate.
- Reuse a visual motif only when it pays off story meaning.

## Engine and asset routing
- **H2 Squire/H2 Canvas**: only when its established symbolic vector/rig grammar is intended and the current rig can execute the shot.
- **Remotion**: frame-accurate timeline, multi-layer 2D compositions, animated titles/maps/charts and editorial transitions; separate from H2 renderer.
- **Blender**: conditional for camera depth, ship/horse/weapon mechanics, layered 2.5D, real lighting or physics that materially improve a shot.
- **Krita**: authored character sheets, hand-painted environments, historic-art paintovers and frame-by-frame animation.
- **Motion Canvas**: evaluate for voice-synchronized vector graphics, diagrams, map paths and infographic sequences; verify current license/runtime and benchmark before adoption.
- **FFmpeg/ffprobe**: source inspection, audio finishing, frame extraction and technical QC.

Prefer real, licensed source assets and authored artwork for environments, objects, music and sound. Use procedural graphics for story information, not to replace every visual and audio asset with code-generated approximations. Prototype the hardest action/transition as a 3–8 second moving proof before scaling.

## Per-shot manifest contract
Record: id; story beat; duration/frame range; location; shot size; viewpoint; camera path/easing; screen direction; character IDs/key poses; action phases; props/contact; environment layers/motion; lighting/palette; graphics; transition; asset IDs/rights; narration segment; music/SFX/ambience cue IDs; text/subtitles; risk; motion-proof status.

## Quality gates
- Contact sheet covers every shot; overview alone is insufficient for detailed action review.
- For hero actions, inspect actual motion at start/contact/follow-through/recovery at normal speed and selected frame-by-frame points.
- Verify silhouette, prop/hand/foot contact, layer depth, safe crop, text legibility and transition continuity.
- Flag repeated camera/scene/pose/template reuse. If many shots share composition, explain why and show intentional counter-variation.
- Review the complete render with sound before release. A technical render and a still contact sheet never equal artistic approval.

## Deliverables
Reference breakdown with exact evidence scope/timecodes; original style bible; story beat/shot manifest; character/environment rig plan; selected reusable motion recipes with exact sources; sound cue sheet and rights ledger; blocking/motion proofs; final QA and unresolved gates.
