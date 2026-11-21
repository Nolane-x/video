# Run-30 caption burn-in defect audit and fix handoff

Date: 2026-11-21
Source master: Run 30, render run 44873063135
Fix branch: film/time-stop-10s-caption-safe-area-fixes

## Verified defects

The 1080p full-resolution samples s014 at 59.25s and s063 at 280s were inspected from the immutable Run-30 master.

1. Key-sequence 3D scenes (kitchen s013–s022, court s026–s033, hallway s037–s042) render their narration plate in the custom overlay. The plate was positioned from the full canvas bottom with a fixed offset. Because the project uses the dem pack's scope (2.39:1) letterbox, the plate extended below the active image and was partially hidden by the lower black bar.
2. Street rescue scenes s053–s072 had two copies of the same narration sentence: a camera-locked plane authored in makeStreet(info), plus a 2D canvas caption rendered by overlay(). The plane was in the visible active image; the canvas copy was lower and partially hidden by the letterbox. The result looked like one complete subtitle plus a clipped duplicate.

## Root cause and intentional architecture

- The dem pack intentionally disables generic karaoke captions. It does not disable story narration: 2D storyboard scenes populate args.texts and the scene template draws those directly.
- The 24 key-sequence 3D scenes have their own one-per-shot overlay and set timelineShot.captions=false to avoid a second generic word-group layer.
- The 20 street-rescue 3D scenes author a camera-space subtitle plate once in makeStreet(info). Their overlay must only add time-freeze rings/title effects, not duplicate narration text.
- Enabling global captions would be the wrong fix: it would alter the dem-pack no-karaoke design and could create duplicate text layers.

## Fix commits

On branch film/time-stop-10s-caption-safe-area-fixes:
- c746adc3b252aa42d991f35c011a1b1a39de9031 — key-sequence 3D captions now calculate safeBottom from the project's letterbox ratio and place the plate 28 logical pixels above the active picture boundary.
- d2b6bf694be2139400e58145ba263a140ee7c1e6 — remove the redundant canvas narration block in the street overlay; retain freeze rings and title, and keep the camera-locked caption plate created by makeStreet(info).

## Render verification state

- Workflow Run #31 (44901907125) on the fix branch was cancelled when the second source commit arrived; the workflow has cancel-in-progress concurrency enabled.
- Workflow Run #32 (44901911523), head commit d2b6bf694be2139400e58145ba263a140ee7c1e6, is the current full-render attempt.
- Completed successfully so far: storyboard/payload, VoiceStudio narration render and AudioSeal verification, renderer/toolchain setup, storyboard build, voice placement, module installation and Node syntax checks for both updated scene files.
- The all-shot H2 scan is still running at the time of this report. No render success or final visual verification is claimed yet.

## Remaining required verification

When Run #32 finishes:
1. Confirm the H2 all-shot scan and full master render completed successfully.
2. Download its new artifact and inspect full-resolution stills around s014, s026–s033, s037–s042 and s063–s072.
3. Verify key-sequence subtitle plates remain fully inside the scope-safe picture area.
4. Verify each street scene shows exactly one complete narration plate.
5. Check no caption plate overlaps the timer HUD or action subject.
6. Keep the new Run-32 candidate as a draft/unapproved until the full 6m18s screening with sound is completed.

Never edit or overwrite Run-30: it is an immutable comparison master. Do not mark visual approval true or publish a new candidate based on the code diff alone.
