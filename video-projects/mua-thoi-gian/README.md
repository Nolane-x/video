# Nếu Bạn Có Thể Mua Thời Gian Bằng Tiền — Remotion Film

Standalone 1080p/30fps image-led production for the 90 user-created stills.

## Production inputs
- Image source: 90 JPEG stills, IDs A001–A090, supplied by the user.
- Narration: VoiceStudio GitHub Actions artifact from run 43893822013.
- Voice: Vietnamese VieNeu narrator, preserved as 48 kHz mono PCM-24 WAV with provenance and watermark checks.
- Timing: H2-compatible word timeline generated with faster-whisper; captions retain the original Vietnamese punctuation.
- Shot plan: 273 editorial shot instances built from the 90 unique images.

## Render pipeline
The workflow `.github/workflows/render-mua-thoi-gian.yml` downloads the exact image ZIP and v4 storyboard package, converts image stills to 1920x1080 JPEG, aligns the 273 shots to the actual narration timeline, creates an original procedural underscore and cue-specific sound effects, then renders through Remotion.

The Remotion project uses:
- Ken Burns camera moves with restrained push, pan and detail reframing.
- Foreground/background separation using blurred ambience layers, vignette and film texture.
- Freeze-time particles and restrained light sweeps at the story's time-stop beats.
- Independent, editable Vietnamese title/data/rule/ledger overlays.
- Word-timed karaoke-style captions driven by the actual aligned voice timestamps.
- Original procedural music and 21 sound-effect cues.

## Run locally
1. Install Node.js 22+, Python 3.12+, FFmpeg and Noto Sans fonts.
2. Download/extract the v4 production package and 90-image archive.
3. Place the VoiceStudio artifact under `voiceover-assets/`.
4. Run the preparation and audio-generation scripts shown in the GitHub Actions workflow.
5. Run `npm install`, `npm run typecheck`, `npm run validate`, then `npm run render`.

## QA notes
The source images are 1376x768 and are fitted to exact 1920x1080. The video uses 30 fps. The final render is mastered to approximately -14 LUFS integrated with a -1.5 dBTP ceiling. The artifact includes the MP4, preview, contact sheet, thumbnail, captions, voice manifest, alignment report and production manifest.

The visual source images are AI-generated stills; Remotion's camera motion is 2D reframing and does not claim true 3D depth reconstruction. No AI-generated text is used for important captions, prices or story data; those are rendered as editable graphics.
