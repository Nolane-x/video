# Time Stop 10s — Cinematic V2 improvement pass

Date: 2026-11-22

## Why V2 exists

Run #40 is a technically valid delivery candidate, but its sampled presentation still reads too much like a flat low-poly illustration. The root cause was verified in `video-projects/time-stop-10s/scripts/build_story.py`: the generated project config selected `style: "flat"`, which maps to `STYLES.flat.grade = null` in the H2 player. That explicitly bypassed global contrast, saturation, vignette and film-grain processing. A 2.39:1 scope bar further reduced the active picture height.

V2 is an artistic pass, not a replacement of the known-good release baseline. Run #40 remains immutable.

## V2 source branch and commit

- Branch: `film/time-stop-10s-cinematic-v2`
- Commit: `671ee442dfb7d6ce60c12ec62a77232956c4ed92`
- Production workflow: [Run #41](https://github.com/Nolane-x/video/actions/runs/45014668552)
- Baseline: official Run #40 artifact `time-stop-10s-h2-40` (run ID `44987846626`, artifact ID `14741738853`).

## Changes in this pass

1. **Global image treatment**
   - Add a cinematic grade in `core.js` with measured contrast/saturation lift, controlled shadow lift, restrained vignette and fine grain.
   - Set storyboard output to `style: cinematic` instead of the ungraded `flat` profile.
   - Change letterbox profile from 2.39:1 scope to 2:1 wide so more of the 16:9 source image remains visible.

2. **3D renderer and lighting**
   - Use ACES filmic tone mapping and a consistent sRGB output path.
   - Enable soft shadow mapping.
   - Move shared scene materials to physically based MeshStandardMaterial with conservative roughness/metalness and substantially lower emissive fill.
   - Add motivated key, rim and practical bounce lights; cinematic scene mode is additive and legacy mode remains available.
   - Prepare shadow casting/receiving once per cinematic scene, skipping transparent overlays.

3. **Composition and staging**
   - Increase motivated dolly and parallax for 24 kitchen/court/hallway shots.
   - Retarget close-ups for cup, basketball retrieval, books and character interaction.
   - Add kitchen pendant/practical lights and countertop dressing, a court scoreboard/crowd silhouette, and hallway lighting/posters.
   - Replace repeated target-reticle circles during frozen time with fine suspended particles/streaks and subtle elliptical temporal distortion.
   - Strengthen street rescue tracking/impact camera motion and improve character presence in frame.

## Validation gates

Do not relax existing production gates:
- 1920x1080, native 60 fps, 22,680 decoded frames, 378 seconds.
- Integrated loudness -15 to -13 LUFS.
- EBU peak <= -1.0 dBFS.
- 84 Vietnamese narration segments with watermark verification.
- Full master FFmpeg decode and manifest SHA256.
- 84 subtitle cues: exact text/start/end, no overlap.
- Four full-mix action clips: kitchen, basketball, hallway/books, street rescue.

Inspect the actual V2 contact sheets and master before considering the pass an improvement. Compare identical midpoints across all 44 custom 3D shots against Run #40, not the older Run #32 baseline. The dedicated comparison workflow is `.github/workflows/inspect-time-stop-run41-vs-run40.yml`; trigger marker `.github/workflows/enable-inspect-time-stop-run41.txt` only after official Run #41 candidate artifact `time-stop-10s-h2-41` exists.

## Artistic review remains separate

Static frames cannot establish motion quality, character acting, pacing, visual continuity or voice/music balance. Keep `visual_approval=false` until the complete six-minute-eighteen-second master has been watched continuously with sound and the 44 matched 3D scenes have been reviewed. If V2 looks too dark, too flat, or too game-like after actual render, revise the grade/light/camera with the rendered proof rather than declaring success from source edits.
