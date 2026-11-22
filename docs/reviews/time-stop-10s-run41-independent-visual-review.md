# Run 41 Cinematic V2 — independent visual/technical review

Date: 2026-11-22

## Source and integrity

- Production run: [Run #41](https://github.com/Nolane-x/video/actions/runs/45014668552)
- Source branch: `film/time-stop-10s-cinematic-v2`
- Source commit: `671ee442dfb7d6ce60c12ec62a77232956c4ed92`
- Official render artifact: `time-stop-10s-h2-41` (artifact ID `14755196342`, 347,050,097 bytes)
- Independent inspection run: [Run #1 inspection](https://github.com/Nolane-x/video/actions/runs/45029673274)
- Inspection artifact: `time-stop-10s-run41-independent-inspection` (artifact ID `14757740461`, 96,357,946 bytes)
- Immutable technical baseline: Run #40 / `time-stop-10s-h2-40`.
- Full master independently decoded; 1080p60, 378s, 22,680 frames, AAC 48k stereo. 84 narration segments and subtitles were cross-checked. Four full-mix action clips passed FFmpeg decode and stream validation.

## Technical result

Run #41 passed all technical gates:
- 1920×1080, 60fps, exactly 22,680 frames over 378 seconds.
- Integrated loudness: -14.2 LUFS.
- EBU peak: -2.6 dBFS.
- 84 verified Vietnamese narration segments, AudioSeal watermark verified.
- No package QA failures.
- `visual_approval=false` remains mandatory.

## Matched-shot grade measurements

44 custom 3D shot midpoints were measured using the same time positions in Run #40 and Run #41 (160×90 RGB samples per frame).

| Metric | Run 40 | Run 41 | Delta |
|---|---:|---:|---:|
| Mean luma (0–255) | 37.488 | 37.261 | -0.227 |
| Median luma | 33.340 | 24.492 | -8.848 |
| P90 luma | 74.612 | 83.644 | +9.032 |
| Luma standard deviation | 34.972 | 39.557 | +4.585 |
| Mean saturation (0–1) | 0.344 | 0.628 | +0.284 |

Additional distribution facts:
- 44/44 matched shots increased in saturation, by +0.226 to +0.365.
- 36/44 matched shots had a lower median luminance.
- 36/44 matched shots had higher luminance standard deviation.

Interpretation: V2 did add contrast and a stronger highlight/shadow separation, but the global exposure is not higher. Midtones became substantially darker and saturation is close to twice the baseline average. The new look is richer, but it risks looking oversaturated/toy-like and burying details in the middle tones. Do not increase saturation further. A next image pass should test a more restrained sat multiplier (~0.90–0.96), slightly lower contrast (~1.08–1.10), and exposure compensation based on actual contact sheets; judge the rendered evidence, not these suggested numbers alone.

## Acting / continuity findings from the moving proof

The full-mix rescue excerpt and matched frames show a stronger 3D street environment and improved lighting, but the mother/bicycle and protagonist interaction still lacks unmistakable hand-to-handlebar / body-contact acting. The final “hug” reads more like two upright characters reaching toward one another than a fully committed embrace in some sampled moments. This is a staging/rig/animation problem, not an encoder or color problem.

The 3D character model also departs from the flat mascot language used by most non-3D scenes: more toy-like/chibi anatomy, skin-toned face detail, while 2D scenes use simple outlined figures. This style seam remains visible. Richer environments are a good direction; further refinement should make the 3D characters feel like the same designed cast rather than a different animation product.

## Next visual pass

1. Reduce oversaturation and protect midtones while keeping the practical amber light pools and cool rain/night separation.
2. Improve contact acting in the rescue: explicit hand-on-handlebar, grip/weight transfer, bicycle momentum, mother's balance shift, and an actual closing embrace.
3. Align the 3D mascot proportions/face language with the 2D cast; avoid adding more face details or plastic shine just to make the model look “more 3D”.
4. Preserve the V3 story improvements (cold-open, variable pace, mother/child beats), and review actual rendered footage before approval.

## Current production continuation

- Narrative V3 source branch: `story/time-stop-10s-narrative-v3`.
- V3 validation run: [PASS](https://github.com/Nolane-x/video/actions/runs/45030008851); 84 shots, 378s, 60fps, 22,680 frames, 13 distinct shot durations, hook freeze beat at 9.6s, voice-slot smoke test passed (84 segments, max atempo 1.03).
- V3 3D cold-open shots `s001–s006` are registered in `time-stop-3d.js` and share the street/bicycle/billboard set with the rescue.
- Production branch: `film/time-stop-10s-narrative-v3`.
- Production run #42: https://github.com/Nolane-x/video/actions/runs/45030100930. At time of this note, story preparation passed and VoiceStudio is generating fresh Vietnamese narration. H2 render has not yet started.
- The latest production workflow validates 29 freeze shots, variable shot durations, the six V3 cold-open durations, and 44 legacy custom 3D shots remaining on their 4.5s local clock.
- Do not overwrite Run #40 or Run #41. Keep visual approval false until the complete V3 master is watched continuously with sound.
