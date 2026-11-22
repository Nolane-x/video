# Time Stop 10s — Visual V4 plan from Run 41 evidence

Date: 2026-11-22

## Evidence that motivated V4

Independent review of Run #41 versus immutable Run #40 (44 matched 3D shot midpoints) found:
- Mean luma: 37.488 → 37.261 (almost unchanged).
- Median luma: 33.340 → 24.492 (darker midtones).
- P90 luma: 74.612 → 83.644 (brighter highlights).
- Luma standard deviation: 34.972 → 39.557 (more contrast).
- Mean saturation: 0.344 → 0.628; all 44 sampled scenes increased by +0.226 to +0.365.
- 36/44 scenes had lower median luminance.

This explains why V2's practical lights and highlights read more cinematic, but why the palette also became overly vivid and the middle tones too dark. The measurement is objective diagnostic evidence, not an artistic quality score.

## V4 source branch

- Branch: `story/time-stop-10s-visual-v4`
- Visual pass commit: `3b86bb96d2f18f04187cb5a80e1c2dba809bb467` (grade)
- Rig commit: `c1c2a44a6e96d9620693aec285478e1abb98d912` (world-space hand anchor)
- Rescue staging commit: `ca342573872d7e50b729b34cf9ad9295529bd285`
- Validation workflow commit: `1b456af2d34b0a7df52bbfc516b5e4d8e503b262`
- Validation run: [Visual V4 validation](https://github.com/Nolane-x/video/actions/runs/45030643152) — PASS.

## Changes

1. **Restrained grade**
   - Cinematic contrast 1.14 → 1.08.
   - Saturation 1.12 → 0.84.
   - Shadow lift strengthened slightly; vignette adjusted modestly.
   - Goal: keep the amber practicals, cool night separation and readable lighting while reducing the high saturation and dark midtones measured in V2.

2. **Explicit physical contact**
   - `figureCinematic` exposes a world-space hand anchor and `aimHandAtWorld`, which solves the upper-arm and forearm angles in the upper-body coordinate frame.
   - Rescue shots s064–s066 use a two-segment shoulder/elbow IK solve against the bicycle's actual handlebar point. The character root stays grounded; only shoulder and elbow angles change to reach the target.
   - Mother/child positions in s071–s072 are brought closer and rotated toward one another to make the embrace read as contact instead of two separate reaching poses.

3. **Story remains unchanged**
   - Keeps the Narrative V3 cold open, 84 shots, 378 seconds, 60fps, 22,680 frames, 29 freeze beats, 13 different shot durations, and 44 established 4.5s custom 3D local-clock shots.
   - Validation confirmed JS syntax, grounded IK contact wiring (three rescue beats), grade values and storyboard invariants.

## Promotion rule

Do not render V4 before the Run #42 Narrative V3 preview/contact sheets are available. If Run #42 shows the V3 story structure is sound but color or contact acting still reads poorly, promote V4 to a separate `film/time-stop-10s-visual-v4` branch and compare with Run #42. Never overwrite Run #40, Run #41 or Run #42. Keep visual approval false until the full master is watched continuously with sound.
