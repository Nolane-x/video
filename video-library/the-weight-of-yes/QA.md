# THE WEIGHT OF YES — QA ledger

## Current state
- Status: render attempt #2 is running on GitHub Actions after a prop-continuity refinement; the runner is still installing FFmpeg and no final MP4 is claimed yet.
- Project: 143 seconds, 29 shots, 1920×1080, 24 fps, English on-screen text, no voice-over.
- Engine: native H2 SelfImprove Studio Canvas/Chromium + FFmpeg mastering.
- Render workflow: [Render THE WEIGHT OF YES](https://github.com/Nolane-x/video/actions/workflows/render-selfimprove-weight-of-yes.yml).
- Source story: [01-PHIM-the-weight-of-yes.txt](../../video-projects/h2-selfimprove/01-PHIM-the-weight-of-yes.txt).
- Art direction: [tune_story.py](../../video-projects/h2-selfimprove/the-weight-of-yes/tune_story.py).

## Non-negotiable story/visual checks
- [ ] A rising favor count is contrasted with the hero's unfinished personal project.
- [ ] The overload beat is restrained; no villain or supernatural shadow is introduced.
- [ ] The “NO. Not today.” caption does not cover either character's face or hands.
- [ ] The friend’s response after the boundary is visible and non-punitive.
- [ ] Another person takes the task; the boundary has a believable practical outcome.
- [ ] A clear submitted/sent confirmation appears after the hero's action.
- [ ] The resolution shows both chosen help and a calm refusal.
- [ ] The 30-second preview, both contact sheets and all 12 motion proofs are inspected.

## Technical delivery gates
- [ ] Native H2 timeline check passes; all 29 shot IDs are present with no gaps/overlaps.
- [ ] Master MP4 has H.264 1920×1080 video at 24 fps and AAC 48 kHz stereo audio.
- [ ] Runtime is 143 seconds ±0.15 seconds.
- [ ] EBU R128 integrated loudness is -14 LUFS ±1.
- [ ] True peak is at or below -1.0 dBFS after AAC encoding.
- [ ] All proof clips contain both video and audio, are ~6 seconds, and have matching SHA-256 entries.
- [ ] The review bundle checksum validates against SHA256SUMS.txt.

## Honest sign-off policy
A successful CI run proves the build and automated checks passed. It does not by itself prove the film is artistically approved. Do not mark the film approved until the moving picture and sound arc have been reviewed from start to finish.
