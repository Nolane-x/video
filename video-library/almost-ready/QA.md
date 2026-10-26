# ALMOST READY — QA ledger

## Status at source authoring
- [ ] H2 schema/JS runtime check on the actual project
- [ ] Exactly 29 shots, 172.000 seconds and no timeline gaps/overlaps
- [ ] Full contact sheets viewed
- [ ] 30-second preview with audio reviewed
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
