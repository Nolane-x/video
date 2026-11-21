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

- Render workflow: `.github/workflows/render-time-stop-10s.yml`, triggered by the final runtime commit on this branch.
- Run ID: pending final discovery from the Actions API.
- The first gate is the built-in renderer scan, contact sheets, preview, full 1080p60 master and audio/QA package.
- The review must explicitly inspect s013–s022 (kitchen/cup), s026–s033 (basketball), s037–s042 (books), and s053–s072 (street rescue).
- Compare the new candidate with Run 32 on character proportions, pose legibility, camera movement, foot/ground contact, prop continuity, sign collapse pivot, and cross-shot visual consistency.
- Keep `visual_approval=false`; a rendered candidate and sampled frames are not a substitute for watching all 6m18s with sound.
