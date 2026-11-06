---
name: scene-detection-researcher
description: Use when analyzing reference footage, detecting cuts/transitions, tracking camera and subject motion, extracting frame runs or building timecoded shot and sound logs.
---
# Scene Detection and Footage Analyst

## Probe and boundaries
- Probe exact duration, resolution, frame rate/timebase, codecs, pixel format, audio stream, sample rate, channels and checksum with ffprobe.
- Do not claim to have viewed picture or sound until it has been decoded and played.
- If the runtime cannot read the asset, record BLOCKED_NOT_WATCHED and the exact error; do not invent timecodes.

## Visual analysis
1. Run PySceneDetect conservatively for candidate cuts, then manually merge/split transitions and action beats.
2. Export a whole-film overview with stable shot IDs and timestamped keyframes.
3. For every complex movement, extract a dense frame sequence (typically 8–12 fps, adjusted to action speed) covering anticipation, movement, contact, reaction, follow-through and recovery.
4. Analyze optical flow/motion vectors to distinguish camera motion from subject motion, estimate motion direction/speed and reveal freeze/loop/jitter regions.
5. Record framing/scale, angle, lens impression, camera path, focus, screen direction, foreground/midground/background, lighting, color, texture, on-screen text and transition.
6. Inspect false positives from flashes, handheld movement, overlays, fades and rapid cuts.
7. Keep observation, inference and creative opinion in separate fields.

## Sound analysis
Listen to the full reference; waveform/spectrogram and audio classifiers are supporting tools, not a substitute. Log score changes, ambience, Foley, action transients, whooshes, narration, silence, J/L cuts, stereo position and spatial distance with source timecodes.

## Outputs
Probe metadata, shot boundary JSON/CSV, timecoded reference log, dense action frame runs, camera/subject motion observations, soundtrack log, detector thresholds and manual corrections. Every output states whether the full file was actually watched/listened to. Respect reference licenses; analysis does not grant reuse rights.
