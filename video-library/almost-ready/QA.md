# ALMOST READY — QA ledger

## Current status — render in progress
- [x] H2 schema/runtime check and authored 29-shot timeline passed in Actions run [#1](https://github.com/Nolane-x/video/actions/runs/40346315405)
- [x] Exactly 29 shots, 172.000 seconds and no timeline gaps/overlaps
- [ ] Full contact sheets viewed manually
- [ ] 30-second preview with audio reviewed manually
- [ ] 12 moving proofs with audio rendered and reviewed
- [ ] Exact final MP4 passes ffprobe: 1920×1080, 24 fps, H.264, AAC 48 kHz stereo
- [ ] EBU R128 on the exact final MP4: integrated loudness −14 LUFS ±1; true peak ≤ −1 dBFS
- [ ] All files in the review ZIP have checksums and validate after packaging
- [ ] Full 172-second playback with audio and artistic sign-off

## Critical motion checks
- b03 and b20: pen tip aligns to the current written line; text reveal never leaks into a later line.
- b05/b07/b14/b27: temptation enters for a story reason, stays out of the hero's hands/face, becomes smaller at the end.
- b10/b24/b25: different character eye-lines; café positions must resolve to the table anchors and feet touch the floor.
- b13/b15/b16: clock, deadline reset and closed portal read as a single cause-and-effect chain.
- b21/b22: typing precedes sending; sending is a visible narrative event, not merely a camera zoom.
- b23: the reply is legible and follows the send.
- Captions: stay in safe areas and avoid eyes, hands and phone/laptop UI.

## Gate semantics
A green CI build does not establish artistic approval. Contact sheets do not establish motion or prop contact. Record any unresolved P1 defect explicitly; do not quietly promote the master.


## Latest technical pass — render #3 (baseline before visible-send fix)
- Workflow: [run #3](https://github.com/Nolane-x/video/actions/runs/40349359432), source commit `563a1d5c30fcffec5e0efc0be7c98bc092afee33`.
- Master: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo.
- EBU R128 on the exported MP4: integrated `-14.0 LUFS`; peak `-1.9 dBFS`. This passed the enforced `-14 LUFS ±1` / `≤ -1 dBFS` gates.
- The 12 motion proof clips were all verified to contain audio/video and be approximately six seconds. All 25 checksums in the delivered manifest validated.
- Master SHA-256: `dfb78ba804919e03771055e456fb216c058f5a02ef1f477ac0fd0c5a1cfc7d2f`.
- Review bundle SHA-256: `bbbf830a58492f12eab914dd2d84f97498d0615bef5ba5f39f876f7b3212ba54`.
- Temporary artifact: [run #3 artifact](https://github.com/Nolane-x/video/actions/runs/40349359432), artifact ID `12663396507`, available until 2026-11-25.
- Contact sheets and a frame-by-frame sampled montage were inspected. Improvements identified and applied to the next render: the student should physically reach with a held book while showing work; the laptop must show an animated SENT confirmation after the message is submitted.
- Artistic sign-off remains pending until the final improved master has its targeted proofs reviewed and the whole film is watched end-to-end with audio.





## Final candidate — render #13
- Workflow: [run #13](https://github.com/Nolane-x/video/actions/runs/40417564202), source commit `cf3050b81bab6163ea8793c641b21d98e4eead84`.
- Added a larger, illustrated portfolio folder hand prop for the classroom-sharing beat (B10), while preserving the seated pointing pose in the café (B24) and timed SENT confirmation (B22). Final render and QA are pending.
- The last confirmed technical baseline is run #11: [workflow](https://github.com/Nolane-x/video/actions/runs/40354490453), artifact `12664834346`. Full-length artistic sign-off still requires a start-to-finish watch with audio.


## Technical pass — render #11, before the larger portfolio-folder prop
- Workflow: [run #11](https://github.com/Nolane-x/video/actions/runs/40354490453), source commit `e9e92b631855fac2b72379e4442bb6c0873f9e44`, artifact ID `12664834346` (retained until 2026-11-25).
- Master SHA-256: `a4cc565fca9a6aa39ace0b0e5a4f9c71a81264ce12b99515ba832638ba34522a`. Review bundle SHA-256: `2fc9d40c93266111b75108e9002cba975681a31df39e229f68cd53f742d2aaf9`. Preview SHA-256: `74cfecb8c7795f306410bdfad75133b0017aa91d00ad2be295dd0c561f4e9f92`.
- Final MP4 gates passed: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo; integrated loudness `-14.0 LUFS`, true peak `-1.9 dBFS`.
- All 25 entries in `SHA256SUMS.txt` validated. The 12 motion proof clips all have audio/video and are approximately six seconds.
- Targeted motion review confirms: the SENT toast appears in B22; B10 shows a peer physically holding out a folder-like object; the two participants stay seated during B24 feedback; the old voice remains small in B27.
- A further refinement adds a larger illustrated portfolio folder prop to B10 because the prior held object was too small to read clearly. Full-length artistic sign-off remains pending.
