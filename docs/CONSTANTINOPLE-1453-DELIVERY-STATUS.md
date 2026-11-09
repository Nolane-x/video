# Constantinople 1453 — production handoff (2026-11-09)

## Long-form Squire master

- GitHub Actions run: https://github.com/Nolane-x/video/actions/runs/42449792684
- Artifact: `squire-constantinople-1453-240fps-42449792684` (2,023,692,938 bytes; artifact ID `13611674134`).
- Automated technical QA: PASS — 957.9 seconds, 1920×1080, native CFR 240/1, 229,896 frames, 586 shots, 434 custom shots; AAC 48 kHz stereo; full decode and loudness checks passed.
- Do not equate this with artistic approval. The complete contact sheet was inspected: the Squire film still relies on flat cartoon/vector-like figures, repeated formations and simplified backgrounds. It is not yet at the requested cinematic visual standard.

## Blender 3D bombardment proof

- Branch: `cinematic/constantinople-bombard-proof`.
- Earlier unchunked run `42461960154` was cancelled after the single long render step exceeded the available job window.
- Chunked run: https://github.com/Nolane-x/video/actions/runs/42487879116
- All six render jobs succeeded and uploaded artifacts (frame ranges 1–1566, 1567–3132, 3133–4698, 4699–6264, 6265–7830, 7831–9394). Each chunk passed 1920×1080 and CFR 240/1 metadata checks.
- The package job failed because the generated FFmpeg concat list contained a literal backslash-n between file entries. This was a packaging bug, not a render failure.
- The six already-rendered chunks were downloaded and joined locally with a corrected concat list. Output: 39.141667 seconds, 1920×1080, 240/1, 9,394 frames, AAC 48 kHz stereo. Full decode passed.
- Audio measurement: -15.0 LUFS integrated, -1.27 dBTP true peak. A sampled 10 Hz motion check found 392/392 distinct video-frame hashes.
- The 3D contact sheet was visually inspected. Cannon, carriage, wall masonry, scaffolding and debris have real scene depth and more dimensional lighting than the Squire proof, but human models remain stylized low-poly. This remains a technical/visual proof, not release-approved footage.
- Narration is a verified excerpt from VoiceStudio run `42448341267`, starting at 220.760 seconds; source audio and downloaded CC0 score/effects were checksum-verified. Human listening/audition is still pending.

## Latest source fixes not yet rendered

- Commit `b28b10a989747b08e091d4895064b6f63d6200d7`: increased Eevee render samples from 2 to 4, raised video bitrate to 48 Mbps, and added role-specific crew bracing/recoil gestures plus camera response at the cannon and wall impacts.
- Commit `c27b762bef0775309b3f787d2dd700e4c0ad0f6a`: fixes the concat-list newline escaping in the chunked workflow.
- Important: run `42487879116` rendered the earlier source commit `faab1f5ef0973a9ddc668c75c10b5f098de17a00`; it did not include the later camera/crew/sample-quality changes. The updated source and workflow fix still need a fresh Actions render to validate them end-to-end.

## Next work

1. Trigger the chunked Blender workflow on the latest branch tip and confirm package job succeeds.
2. Inspect the new 3D result at normal speed, not just a contact sheet; improve human anatomy/poses, environmental detail, camera composition and impact follow-through before expanding beyond the bombardment sequence.
3. Watch the full Squire master at normal speed and audition every music/Foley stem before any public-release sign-off.
