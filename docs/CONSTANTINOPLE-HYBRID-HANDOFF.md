# Constantinople 1453 — production handoff

Updated: 2026-11-08 (UTC)

## Current deliverable paths

This production is being developed in independent branches so the existing Squire work is not overwritten.

### 1. Squire native 240fps master

- Run: https://github.com/Nolane-x/video/actions/runs/42449792684
- Branch: `squire/constantinople-1453-240fps`
- Current state at handoff: full 1080p native-240fps render and audio mix completed; strict HFR QA / delivery-bundle assembly still in progress.
- Only the short motion-proof artifact is published so far. Do not report the full master as delivered until the final upload artifact exists and is checked.

### 2. Squire redesign proof

- Run: https://github.com/Nolane-x/video/actions/runs/42459027169
- Branch: `squire/constantinople-1453-redesign`
- Technical proof: 37.383 seconds, 1920x1080, CFR 240fps, 8,969 frames; complete decode passed.
- This is a technical proof, not artistic approval. The inspected contact sheet still reads as simplified vector/cartoon imagery and is not the final visual target.

### 3. Original Blender full-native render experiment

- Run: https://github.com/Nolane-x/video/actions/runs/42461960154
- Branch: `cinematic/constantinople-bombard-proof`
- Scene: illustrative 3D bombard loading, firing, stone flight, wall impact and repair; 39.14 seconds; 9,394 frames.
- The one-frame smoke test succeeded. Full Eevee render on the CPU runner was too slow: latest observed progress was frame 445 / 9,394 (4.7%) at 2026-11-08 09:33:39Z. This route is not a viable delivery path under the 180-minute job timeout. Do not claim completion or wait on this path as the primary deliverable.

## Optimized hybrid 240fps branch

- Branch: `cinematic/constantinople-hybrid-240fps`
- Workflow: https://github.com/Nolane-x/video/actions/workflows/constantinople-hybrid-240fps.yml
- Run: https://github.com/Nolane-x/video/actions/runs/42467823008
- Current state at handoff: queued; waiting for available GitHub Actions capacity.
- Commit includes static mesh consolidation (same parent/material groups) and a deterministic keyframe export mode. This reduces per-frame Eevee object synchronization while preserving the authored 3D scene and all animation poses.
- Planned path: render evaluated 3D poses at 30fps (every 8th frame of the 240fps animation timeline), then use FFmpeg `minterpolate` to produce a 1920x1080 CFR 240fps delivery file, mux the verified VoiceStudio narration, recorded CC0 score and cannon effects, export captions, run full decode/stream QA and upload a provenance bundle.
- Be explicit in metadata and delivery notes: **the picture is rendered at 30fps and motion-compensated to 240fps; it is not 9,394 independently ray/scene-rendered Blender frames.** The Squire path remains the native-240fps alternative.
- Audio asset audition is still required. Candidate recordings are CC0, but their suitability has not been human-approved.
- The 39.14-second bombard sequence is only a proof segment, not the complete 53-day film.

## Delivery gate

A run being green is not enough. Before calling a proof complete:
1. Confirm artifact upload exists and download the artifact.
2. Check FFprobe metadata, decoded frame count, 1920x1080, CFR 240/240, 48kHz stereo and full-file FFmpeg decode.
3. Inspect the contact sheet and representative frames at start, middle, every cut, muzzle flash, projectile flight, impact and aftermath.
4. Inspect motion at normal playback speed, especially the cannon recoil, ball trajectory, camera moves, debris and interpolation around fast action.
5. Listen to the complete mix and verify narration clarity, music balance, cannon timing and caption sync.
6. Keep technical pass, visual review and artistic approval as separate statuses.

Do not merge or replace the existing Squire branch based only on technical QA. Preserve both alternatives until the visual comparison is complete.
