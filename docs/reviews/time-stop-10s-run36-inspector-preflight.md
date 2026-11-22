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

## Run 39 voice asset verification and active master render (2026-11-22)

- Production run: [Run #39](https://github.com/Nolane-x/video/actions/runs/44983301715), source commit `112ed8b8b57af75173913cde60f7a7bd7dad516a`.
- VoiceStudio job completed successfully and uploaded artifact `video-voice-assets-44983301715` (artifact ID `14738338133`). The downloaded archive was inspected directly: 84 Vietnamese segments, 48 kHz / 24-bit / mono PCM, 200 seconds, and `clipped_ratio=0`.
- AudioSeal watermark reports `verified`, 7 blocks, minimum confidence 0.9946 and mean confidence 0.999. The outer and nested copies of the narration WAV match the manifest SHA-256.
- Both SRT and VTT contain 84 cues. Every SRT cue was compared to its manifest segment: zero text mismatches, zero start-time mismatches, and zero end-time mismatches. The segment text SHA-256 matches the newline-joined manifest text. This verifies machine-readable alignment, not subjective voice quality; listening review remains outstanding.
- H2 render preparation, storyboard generation, voice placement, 3D module installation, all-shot renderer scan, six contact sheets and the 30-second motion preview completed successfully.
- At the latest check, the H2 job remains in progress at **Render the complete 1080p native-FPS silent master**. The 1080p/60fps, 22,680-frame master is not yet reported complete; mix, package QA and film upload remain pending. Only the verified voice artifact is currently uploaded for Run #39; do not describe this as a delivered film.
- Immutable Run #32 baseline artifact `time-stop-10s-h2-32` (artifact ID `14707913978`, about 259 MB) remains available and unexpired.
- The Run #39 independent-inspection workflow is configured against the Run #32 baseline. Trigger it only after the official `time-stop-10s-h2-39` artifact is uploaded following successful package QA.
- Keep `visual_approval=false` until the complete film is watched continuously with sound and the 44 matched 3D shots are visually reviewed.

## Run 39 root-cause analysis and Run 40 rerender (2026-11-22)

- Run #39 completed its full H2 render and mix, but package QA failed with a Python `IndentationError: unexpected indent` at the first `print(json.dumps(report, indent=2))` inside the no-stream defensive branch. This was a workflow-script indentation defect, not a media or audio measurement failure.
- Downloaded diagnostic artifact: `time-stop-10s-diagnostic-39` (artifact ID `14740333359`, 131,323,445 bytes). It contains the complete 100,284,438-byte H.264 master, 30-second preview, six contact sheets, story and voice manifests, subtitles and EBU log. The candidate is not an official release artifact because package QA did not complete.
- Independent inspection of the actual MP4 metadata and QA inputs confirmed: 1920x1080, 60/1 fps, 22,680 frames, 378.000 seconds; AAC 48 kHz stereo; integrated loudness `-14.3 LUFS`; EBU true peak `-2.3 dBFS`; 84-shot storyboard; voice placement status `passed`, 84 Vietnamese segments, engine `vieneu`, and watermark status `verified`. Every measurable technical gate represented in the existing QA code passed when checked independently.
- A separate full-file FFmpeg decode was attempted in this inspection environment but exceeded the execution time limit; this decode check is therefore still delegated to the independent GitHub inspection workflow and must not be marked complete from the local attempt.
- Visual contact-sheet review shows all six sheets and the story progression are present. The film intentionally mixes flat graphic story beats with stylized 3D sequences; this is only a sampled still-image review. The 44 custom 3D shots and full audiovisual pacing still require matched before/after inspection and continuous watching.
- Production fix committed as `42d23953e252b79f36dd7dd09834a19fbf934de6`: moved the defensive branch's `qa-report.json` write into the same conditional block as its report creation, print and exit, removing the malformed indentation.
- GitHub automatically queued [Run #40](https://github.com/Nolane-x/video/actions/runs/44987846626) from the corrected workflow. At the first check, storyboard preparation succeeded and VoiceStudio was running; H2 full render has not yet started.
- Run #39's measured audio settings and gates remain unchanged. Do not lower or bypass the QA checks to force publication.
- The independent inspection workflow still targets Run #39 and must be retargeted to the successful Run #40 artifact once it exists. Keep `visual_approval=false` until full decode, all 44 matched 3D comparisons, subtitle/audio alignment and continuous viewing with sound have passed.

## Run 40 inspection preflight and sampled visual review (2026-11-22)

- Run #40 voice artifact `video-voice-assets-44987846626` (artifact ID `14740058876`) independently verified: 84/84 narration segments, 84 SRT cues and 84 VTT cues; every SRT cue matches manifest text, start and end to the millisecond; transcript SHA-256 matches the manifest. Audio is 48 kHz mono PCM_24, 199.68 seconds, clipped_ratio 0; AudioSeal watermark verified in 7 blocks, minimum confidence 0.9987 and mean confidence 0.9997.
- The six Run 39 contact sheets were examined as sampled visual evidence. The story order and key actions are present across the kitchen, basketball, hallway and street-rescue blocks; captions appear inside dark high-contrast plates in the custom 3D action shots at this thumbnail scale. The 3D models remain intentionally stylized/low-poly relative to photoreal animation; contact sheets cannot establish motion quality, facial animation, continuity, or full-frame caption safety. This is not artistic approval.
- The independent inspection workflow has been retargeted to Run #40 by commit `589402a4699c65f0378f10ca09382e725c780792`. It now waits for marker `.github/workflows/enable-inspect-time-stop-run40.txt`, downloads artifact `time-stop-10s-h2-40`, compares all 44 custom 3D shot midpoints against immutable Run #32, decodes the full master, checks 84 narration/subtitle cues, extracts 32 key frames and 252 dense stills, and verifies four full-mix action clips.
- Do not create the trigger marker until official candidate artifact `time-stop-10s-h2-40` has been uploaded after successful package QA.
- At the latest poll, Run #40 is still in progress at its full 1080p/60fps master render step. VoiceStudio and all pre-render checks succeeded; sound mix, package QA and upload are pending. No official Run #40 movie artifact exists yet.
- Keep `visual_approval=false` until the independent inspection passes and the complete film is watched continuously with sound.

## Run 40 official master and independent inspection retry (2026-11-22)

- Official production [Run #40](https://github.com/Nolane-x/video/actions/runs/44987846626) completed with success from source commit `42d23953e252b79f36dd7dd09834a19fbf934de6`. Official artifact `time-stop-10s-h2-40` is ID `14741738853` (262,628,497 bytes).
- The downloaded artifact's `qa-report.json` reports `technical-pass`, 1920x1080, 60fps, 22,680 frames, 378s, H.264 + AAC 48kHz stereo; integrated loudness -14.3 LUFS, true peak -1.8 dBFS; all 84 Vietnamese narration segments placed, watermark verified, and zero QA failures. Both audio gates passed. Artistic approval remains false.
- Independent Run #40 inspection run #1 ([45005825494](https://github.com/Nolane-x/video/actions/runs/45005825494)) passed artifact downloads, SHA256 manifest verification, full MP4 FFmpeg decode, stream/frame checks, exact 84 subtitle cue count, no overlaps, and exact subtitle text/start matching; 32 key frames extracted. It failed only because `BASELINE_MASTER` was appended to `GITHUB_ENV` but read by Python in the same step (GitHub applies that file only to later steps).
- Fixed the inspector at commit `70131e2aa55e58c2ea37492076e5487b41829874` by exporting `BASELINE_MASTER="$BASELINE"` immediately in the same shell. Retry triggered by marker update commit `c5cd5d8366845751259bf0829e2aa5a56f49215e`; independent inspection run #2 is [45006109601](https://github.com/Nolane-x/video/actions/runs/45006109601).
- Additional direct archive inspection verified all 84 SRT cues against voice-placement: zero text, start, or end mismatches; no cue overlaps; manifest transcript SHA-256 matches. The official artifact's nested review archive contains 22 SHA256 manifest entries; the independent CI check validated that manifest against the source artifact.
- Six official Run #40 contact sheets have been visually inspected. All 84 shots and the kitchen, basketball, hallway/books, street rescue, and ending sequences are present. Caption plates remain within the visible scope in the sampled 3D rescue and key-sequence stills. Style is deliberately stylized / low-poly rather than photorealistic. Static contact sheets do not assess motion continuity, character animation or subjective audio quality.
- The independent retry must finish matched Run 32 vs Run 40 midpoint comparison for all 44 custom 3D shots, 252 still sampling, and four full-mix action clips. Do not mark artistic approval until those outputs are reviewed and the entire 6m18s master is watched continuously with audio.
