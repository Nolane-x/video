# Audio and delivery

## ONE MORE SCROLL sound arc
Reflective/sad piano → dark drone → intentional silence after the phone-down choice → gentle hope → rising effort → resolution. SFX punctuate notification, clock, page, footsteps, door, breath, gym/punch impact and shadow resolution. Sync SFX to action/contact frames.

## Source generators
- `video-projects/remotion/h2-audio/audio/synth.py`
- `video-projects/remotion/h2-audio/audio/music.py`
- `video-projects/remotion/h2-audio/audio/build_audio.py`
- `video-projects/remotion/h2-audio/packs/dem/audio.py`
- `video-projects/remotion/h2-audio/requirements.txt`

These are code which generate WAVs, not prerecorded audio. Generate in a clean environment, confirm expected files/sample rate/duration, and don't “fix” intentional silence by filling it.

## Default delivery target
- Stereo AAC 48 kHz.
- Around -14 LUFS integrated for YouTube-type delivery unless the creative brief justifies another target.
- Conservative true peak ≤ -1.5 dBTP.
- Measure actual loudness/peak; a filter argument is not a measurement.
- Current film uses text/music/SFX, no synthetic voice-over.

## Mastering order
Picture lock → create/place tracks → mix and check peaks/silence → encode to temporary file → ffprobe and audio measurement → inspect/listen to representative intervals → atomic rename to master → record codecs/resolution/FPS/duration/audio/loudness/peak in manifest.
