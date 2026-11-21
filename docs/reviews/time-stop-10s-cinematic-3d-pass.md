# Time Stop 10s — Cinematic 3D pass

Date: 2026-11-21

## Why this pass exists

Run 32 cleared the caption defects and the technical release checks, but sampled review still showed that the 3D sequences looked too much like simple primitive figures in static layouts. The major weaknesses were oversized heads and narrow limbs, few clothing/face details, minimal body weight shifts, nearly locked-off cameras, and overly linear prop motion.

## Scope of the new candidate

This pass is isolated on `film/time-stop-10s-cinematic-3d-pass`; it does not mutate Run 30 or Run 32.

- Added an additive `figureCinematic()` character rig to the shared Three.js engine. The original `figure()` API remains untouched for compatibility.
- New characters use more balanced head/body proportions, a neck and pelvis, shaped shoulders, articulated upper/lower arms and legs, cuffs, hands, footwear, hoodie seams/zipper/pouch/strings, simple hair/headwear, and finer eyes/brows/mouth.
- Motion adds breathing, blink, head response, body lean, walk/run stride, knee recovery, and arm counter-swing. Existing `setPose()` entry points are preserved.
- Both custom 3D shot modules now opt into the new rig.
- Key-sequence camera motion has a restrained shot-length dolly and lateral arc; street rescue shots use a subject-aware pan/dolly rather than a locked camera.
- Basketball release now has a shaped drop/bounce/roll trajectory; falling books gain individual gravity/rotation and the book hand-off follows a shallow arc.
- Street-rescue bike pedals now animate with the wheel motion. The roadside shop sign has been re-anchored to its support foot so it tips around a plausible base rather than spinning around its centre.

## Render and review gate

- Render workflow: `.github/workflows/render-time-stop-10s.yml`.
- Candidate Run #35: https://github.com/Nolane-x/video/actions/runs/44918426729 — source commit `398b04e0b7d15df41f6f0c28878634a16dd96235`.
- VoiceStudio job completed successfully with all 84 Vietnamese narration segments and watermark verification. H2 initialized the full 84-shot story, placed voice, installed both new 3D modules, passed the all-shot renderer scan, rendered six contact sheets and a 30-second motion preview. The complete 1080p60 master is currently rendering; sound mix, package and upload are pending.
- Independent Run #35 inspection workflow prepared on `review/time-stop-10s-3d-fixes`: `.github/workflows/inspect-time-stop-run35.yml`, commit `7dddb9c0f02832e7fb6c22a7eaea906b3f5bc6fa`. Trigger marker `.github/workflows/enable-inspect-time-stop-run35.txt` only after the render candidate artifact is confirmed uploaded.
- The first gate is the built-in renderer scan, contact sheets, preview, full 1080p60 master and audio/QA package.
- The review must explicitly inspect s013–s022 (kitchen/cup), s026–s033 (basketball), s037–s042 (books), and s053–s072 (street rescue).
- Compare the new candidate with Run 32 on character proportions, pose legibility, camera movement, foot/ground contact, prop continuity, sign collapse pivot, and cross-shot visual consistency.
- Keep `visual_approval=false`; a rendered candidate and sampled frames are not a substitute for watching all 6m18s with sound.


## Visual review rubric (score each sequence 1–5)

| Dimension | What to verify |
|---|---|
| Character silhouette | Head/body ratio, shoulder width, visible neck, articulated elbows/knees, readable hands and footwear |
| Performance | Weight shift, anticipation, follow-through, arm counter-swing, stride cadence, crouch/reach/pull/hug readability |
| Prop physics | Ball release/bounce/roll, books falling and being caught, cup continuity, pedal/wheel relation, sign tipping around the foot |
| Camera | Shot has purpose; restrained push/pan follows action; subjects are not clipped; consecutive shots vary scale and angle |
| Lighting/material | Character separates from background; feet contact ground; faces/clothes retain shape; warm/cool palette stays consistent |
| Continuity | Character colors, scale, pose direction, prop position, screen direction and freeze logic remain consistent between adjacent shots |
| Stability | No renderer warnings, missing meshes, z-fighting, jitter, sudden teleports, one-frame pops or unexpected blank/black images |

Review each group at 0.75s, 2.25s and 3.75s per shot, and watch its motion preview with sound:
- Kitchen/cup s013–s022: release, falling cup, freeze, reaching/catching, re-entry.
- Basketball s026–s033: ball leaves the hand, rolls toward the road, protagonist runs, crouches, retrieves and hands back.
- Books s037–s042: stack falls, protagonist enters, catches/re-stacks and gives books back.
- Street rescue s053–s072: bike/mother establish geography, child runs, pulls mother/bike, billboard collapse, both recover and embrace.

A sequence is not accepted on screenshots alone: the motion must read continuously. Record scores and defects; any critical continuity/physics/cropping issue blocks the candidate. Keep visual_approval=false pending a continuous full-film viewing with audio.
