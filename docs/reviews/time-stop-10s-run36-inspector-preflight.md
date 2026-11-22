# Run 36 independent inspection preflight

Date: 2026-11-22  
Review branch: `review/time-stop-10s-3d-fixes`  
Candidate workflow: [Run 36](https://github.com/Nolane-x/video/actions/runs/44964684746)  
Inspection workflow: `.github/workflows/inspect-time-stop-run36.yml`

## Baseline artifact used to validate the inspection assumptions

- Run: #32, ID `44901911523`
- Artifact: `time-stop-10s-h2-32`
- Artifact ID: `14707913978`
- Downloaded archive size: 259,453,076 bytes
- The outer archive contains `time-stop-10s-review.zip`; its review root is `dist/time-stop-10s/`.
- The expected master, QA report, voice placement, subtitles, and contact sheets are present under that root.

## Checks completed against the real Run 32 artifact

| Check | Result |
|---|---|
| Outer artifact / inner review ZIP structure | Pass |
| SHA256 entries in the inner review manifest | 22 / 22 pass |
| Master resolution | 1920 × 1080 |
| Master frame rate | 60/1 |
| Decoded video frames | 22,680 |
| Duration | 378.000 seconds |
| Audio | AAC, 48 kHz, stereo |
| Subtitle cues | 84 |
| Voice placement segments | 84 |
| Subtitle start-time mismatches | 0 |
| Subtitle text mismatches | 0 |
| Subtitle overlaps | 0 |

The baseline validation confirms that the Run 36 inspection workflow's archive-root discovery, manifest verification, stream expectations, and exact subtitle-to-voice-placement checks match a previously delivered production artifact.

## Scope and limitations

- This is a preflight of the inspection assumptions using Run 32, not an inspection of Run 36.
- It does not establish that Run 36 has rendered, passed audio QA, or uploaded a movie artifact.
- It does not score visual quality or grant artistic approval.
- Keep `visual_approval=false` until the complete Run 36 master is watched continuously with audio and the 44 matched 3D shots are reviewed.

## Run 36 gate

At the time of this preflight, Run 36 had passed the all-shot renderer scan, full contact-sheet render, and 30-second preview. Its full 1080p/60fps master render was still in progress. The mix, package QA, artifact upload, and independent visual review remained pending.

## Run 36 result and next audio calibration (2026-11-22)

- Run #36 completed with failure in package QA, not in scene rendering or video mastering.
- The all-shot renderer scan, six contact-sheet render, 30-second motion preview, full 22,680-frame 1080p60 silent master, and procedural sound mix all succeeded.
- The package QA measured integrated loudness at **-15.7 LUFS**, below the accepted range of -15 to -13 LUFS. The assertion stopped before the script checked/reported the encoded AAC peak, so Run #36 does not prove whether the new peak limiter passed.
- The full candidate was not uploaded; Run #36 retains only its verified VoiceStudio narration artifact. Do not claim that a Run #36 film master was delivered or visually reviewed.
- The measured calibration workflow is running as [Run 37](https://github.com/Nolane-x/video/actions/runs/44979180178). It uses the exact 84-segment Run 36 narration, story/music/SFX inputs and measures decoded AAC output across 28 combinations of pre-AAC and final AAC limiter ceilings.
- Calibration is isolated on `review/time-stop-10s-3d-fixes`; it does not change production source or trigger the 378-second film render.
- Next production change must preserve both delivery gates: integrated loudness -15 to -13 LUFS and EBU peak <= -1.0 dBFS. The QA routine must print and persist both measurements before asserting, and its diagnostic package upload should run even if QA fails.
- Keep `visual_approval=false` until the full candidate is delivered and continuously watched with audio.

## Run 36 AAC loudness calibration and Run 38 rebuild (2026-11-22)

- Calibration workflow succeeded: [Run 4](https://github.com/Nolane-x/video/actions/runs/44979460350), artifact `time-stop-10s-audio-calibration-run36` (artifact ID `14737795599`).
- It rebuilt the exact 84-shot / 378-second Run 36 storyboard, placed all 84 verified Vietnamese narration segments, mixed the corresponding music/SFX, and encoded/measured 28 limiter combinations as AAC.
- 14 of 28 combinations passed both gates: integrated loudness -15 to -13 LUFS and decoded AAC EBU peak <= -1.0 dBFS.
- Selected production limits: pre-AAC limiter **0.70**, final AAC limiter **0.65**. The selected real-mix measurement was **-14.2 LUFS** and **-2.4 dBFS** peak. The previously failing 0.55/0.50 pair measured -15.7 LUFS / -4.0 dBFS: peak was safe, integrated loudness was too low.
- Production commit `9a8dc9f18057125b7054fbf26ca76207a9cce651` applies both selected limits and makes QA persist both audio measurements and all failures before returning a failing exit code. It also uploads a diagnostic artifact if technical QA fails, so the rendered master/contact sheets are not lost.
- A parser escaping issue in the first commit was corrected in `3be3a70835cb649fe7d24ec3dca22d96980b4163`. Run #37 was cancelled before its H2 render began; it did not consume a full film render.
- Current candidate: [Run #38](https://github.com/Nolane-x/video/actions/runs/44983218933), commit `3be3a70835cb649fe7d24ec3dca22d96980b4163`. Its narration/build is queued; do not treat it as delivered yet.
- Independent inspection workflow has been retargeted to Run #38. It will compare the new candidate against immutable Run #32 and inspect all 44 custom 3D shots after the production artifact is uploaded.
- Keep `visual_approval=false`; the new master still requires full technical checks, frame/motion review, and continuous full-film viewing with audio.

## Run 38 cancellation and current Run 39 (2026-11-22)

- Run #38 (`44983218933`) was cancelled before the H2 film render began after a second workflow-source audit found that the QA JSON writer emitted a literal escaped newline. No master or candidate artifact was produced by Run #38.
- The writer was corrected in production commit `112ed8b8b57af75173913cde60f7a7bd7dad516a`. Both JSON write sites now use a real newline terminator. The EBU parser was separately fixed in `3be3a70835cb649fe7d24ec3dca22d96980b4163`.
- Local parser/serialization smoke test passed on representative measurements: `-14.2 LUFS` and `-2.4 dBFS` are extracted correctly and the resulting QA JSON round-trips successfully.
- Current rebuild is [Run #39](https://github.com/Nolane-x/video/actions/runs/44983301715), source commit `112ed8b8b57af75173913cde60f7a7bd7dad516a`. Its storyboard job is starting; do not infer film render completion from workflow creation.
- Independent inspection workflow is now configured for Run #39 and immutable Run #32 baseline. Trigger it only when official artifact `time-stop-10s-h2-39` is uploaded after passing package QA.
- The chosen production audio settings remain pre-AAC 0.70 / final AAC 0.65; do not revert them or weaken the existing loudness/peak gates.
