# Gated production workflow

## Gate 0 — restore state
Read AGENTS, skill, state/handoff, target manifest; inspect HEAD, relevant Actions/logs and artifact storage. Distinguish source-only changes from changes already rendered.

## Gate 1 — brief
Record audience, platform, ratio, duration, language, voice-over policy, emotional result and constraints. Preserve already-known user choices.

## Gate 2 — references
Break videos down across their full length. For each sample record time, size, angle, camera, pose/action, emotion, location, color/light, props/contact, text, transition and sound beat. Separate observation from assumptions.

## Gate 3 — story
Create logline, emotional arc, turning points and a purpose for each shot. Every shot changes at least one of space, action, information, relationship, emotion, scale or metaphor. Avoid filler.

## Gate 4 — art direction
Lock character sheet, outline/proportions, palette, environment, practical-light logic, type and camera rules.

## Gate 5 — storyboard schema
Each shot should define `id`, duration/start/end, `tpl`, line, emotion, action, setting, framing, camera rationale, props, contact, transition, sound cues and engine-specific args. Validate missing templates/assets, illegal values, duplicated actions and total duration. Keep the H2 `tpl + args` contract if using H2.

## Gate 6 — block and asset
Record asset origin/license. Confirm ground line, prop location, anchors, scale, layers and safe areas before decoration.

## Gate 7 — animate
Plan anticipation → action → contact/impact → follow-through → recovery. Animate character and prop as one interaction. Secondary motion comes only after the main action reads.

## Gate 8 — preview
Render one contact sheet per shot plus overview, a 5–10 second moving proof for difficult actions, samples around contact, and first/last frames around cuts. Inspect actual output.

## Gate 9 — audio
Place music/SFX to story beats. Preserve planned silence. Keep tracks separate until mix. Don't add TTS by default.

## Gate 10 — render/master
Run intended engine, log exact command/run ID/commit, render to temp and keep prior master until new one passes.

## Gate 11 — QA
Inspect frame composition, motion/contact, set variety, continuity, type, transition, sound, duration, ratio, FPS/codecs. P0/P1 defects block release or must be explicitly disclosed.

## Gate 12 — archive/handoff
Store master, source commit, storyboard, assets manifest, contact sheets, audio measurement, ffprobe JSON and QA report. Update state, handoff and video manifest.
