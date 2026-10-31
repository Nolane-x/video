---
name: audio-postproduction-engineer
description: Use when editing narration, music and sound effects, cleaning dialogue, balancing a mix, designing sound or mastering a video soundtrack.
---
# Audio Postproduction Engineer

## Session plan
Define delivery platform, language, target loudness, true-peak ceiling, stems, sample rate, channel layout and required mix versions before editing. Preserve original recordings and work on copies.

## Dialogue-first workflow
1. Inspect waveform, clipping, noise floor, room tone, plosives, mouth clicks, hum, reverb and inconsistent distance.
2. Repair conservatively: high-pass only when appropriate, de-click/de-plosive, gentle denoise, subtractive EQ, controlled compression and de-essing.
3. Preserve natural voice dynamics and consonants; avoid over-denoising, metallic artefacts and aggressive pitch correction.
4. Keep dialogue, music, ambience and spot SFX as separate stems until final mix.
5. Duck music around narration with smooth attack/release and story-sensitive automation; protect important quiet moments.
6. Use silence intentionally. Never fill every gap with music or effects.

## Sound design
Use sound to clarify action, distance, material, environment or emotion. Match transient timing to visible contact. Check stereo image and mono compatibility. Maintain licensed-source records for every external recording, sample, loop or preset.

## Mastering and verification
- Use FFmpeg `loudnorm` for measured integrated loudness and true-peak control; measure after processing with `ebur128` or an equivalent meter.
- Avoid hard clipping and limiter pumping. Listen to full programme and inspect difficult transitions.
- Export a full mix and separated stems at the agreed PCM sample rate/bit depth; encode delivery AAC/Opus only after mastering.
- Keep original WAV/FLAC masters; never recompress intermediate generations unnecessarily.

## Commercial and model rights
A software-code license does not automatically license bundled model weights, voice samples or generated voice identities. Check each model/provider's terms and consent requirements. Do not imitate a real person's voice without authorization.

## Deliverables
Session/stem map, processing chain, measured LUFS/true peak, mix/master renders, source/rights ledger and listening QA report.
