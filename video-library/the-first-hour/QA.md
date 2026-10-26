# THE FIRST HOUR — QA and handoff

## Build identity
- Source commit: `6eba384b4babde94f030371d5c9904c483fcbef3`
- Engine: H2 SelfImprove Studio Canvas/Chromium + FFmpeg audio mastering.
- CI run #26: [passed](https://github.com/Nolane-x/video/actions/runs/40329265743); [temporary Actions artifact](https://github.com/Nolane-x/video/actions/runs/40329265743), artifact ID `12653272820`.
- All workflow steps passed, including storyboard checks, full render, audio mix, motion proof generation, metadata/loudness checks and artifact upload.

## Master metadata
- File: `the-first-hour-h2-selfimprove.mp4`
- Duration: 172.000 s; 29 curated shots.
- Video: H.264, 1920×1080, 24 fps.
- Audio: AAC, 48 kHz stereo.
- FFmpeg EBU R128 on the exact final MP4: −14.1 LUFS integrated, 6.8 LU loudness range, −2.5 dBFS true peak.
- MP4 size: 26,696,094 bytes.
- MP4 SHA-256: `75b4172e47735368bb0070b50273ce12fb0248a460a5930c78cd19abb26e82a8`.

## Review package integrity
- ZIP size: 36,695,188 bytes; SHA-256: `e0e514ee6cd048ad2d389a536c6c899297f77755e7d551cfd303193435dbfa3f`.
- The embedded `SHA256SUMS.txt` was independently checked; all 24 listed files matched.
- Includes the master, 30-second preview, two contact sheets, storyboard/overrides, bible, metadata and audio logs, plus 12 six-second motion proofs with audio.
- Each of the 12 motion proofs passed ffprobe checks for both audio/video streams and ~6 s duration.

## Visual review actually performed
- Reviewed both contact sheets covering all 29 shots.
- Inspected motion frames from b20 (notebook writing): the prior negative-slice issue is fixed; no early text from the next line appears in the sampled frames. The pen follows the current line.
- Inspected frames across b25 (punch bag): the gym set now passes the authored impact timestamps, recoil amount and spark color through to the bag renderer. The bag visibly tilts/recoils around the two timed impacts.
- The other ten proof clips were generated and technically checked, but were not all individually watched.
- **Important limit:** a full 172-second start-to-finish playback with audio has not yet been performed. Therefore visual QA is a targeted pass, not complete artistic sign-off.

## Release/storage status
- CI artifact name: `the-first-hour-h2-selfimprove-26`, artifact ID `12653272820`, 73,426,295 bytes, ZIP SHA-256 `f7b6c6b6cac7ac0f76d10856d8a6e0c62d9351f9ba249ed3162feab9c2acef2a`.
- GitHub Actions artifacts are temporary. This render is **not yet archived to a durable GitHub Release**, so do not label it permanently archived.
- The verified local download can be served from this conversation as a file attachment; the repo keeps its exact checksums and source/run provenance.

## Remaining gates
- [ ] Watch all 172 seconds with audio, start to finish.
- [ ] Verify all action/contact/transition and caption issues discovered during playback.
- [ ] Publish the candidate and review ZIP to durable release storage; verify remote assets against these checksums.
- [ ] Only then update the manifest to durable archive / artistic approval status.
