# Time Stop 10s — Run 30 post-render QA addendum

Date: 2026-11-21

## Sustained-black scan

- Run 30 master: 44873063135; immutable artifact `time-stop-10s-h2-30`.
- Full 378.0-second timeline was scanned at 4 samples/second after downscaling to 160×90 grayscale.
- Detector parameters: `blackdetect=d=0.5:pix_th=0.06:pic_th=0.985`.
- One near-black interval was detected: **373.50–374.75s (1.25s)**.
- This is expected, not a missing-image defect: `video-projects/time-stop-10s/scripts/build_story.py` defines shot s084 as the `black` location, with the explicit direction “Thẻ kết nền than chì; vòng sáng xanh nhỏ co lại thành một chấm rồi tắt.” Its entry transition is a 0.7-second dip and the final on-screen text is “HÃY SỐNG TRỌN VẸN TỪNG GIÂY.”
- No unexpected black interval of 1.5 seconds or longer was found.
- Audit workflow: https://github.com/Nolane-x/video/actions/runs/44886988249
- Audit artifact: `time-stop-10s-run30-black-scan`, ID `14700104314`.
- The audit workflow now explicitly classifies the 373.5–378.0s end-card interval as `designed-dark-end-card`.

## Subtitle readability addendum

The original voice-synchronous subtitle track has 84 cues, no overlaps, and preserves the narration timing. The cue ends currently follow the spoken audio durations, giving a median 16.95 characters/second and a maximum 20.09 characters/second.

A supplementary extended-dwell subtitle variant was generated without changing the master MP4, original SRT/VTT, narration WAV, voiceover manifest, or shot timing:

- Retains all 84 cue texts and all original cue start times.
- Each cue now remains visible until 0.12 seconds before the next shot's cue begins; the final cue ends at 378.0s.
- Minimum dwell is 4.38 seconds.
- Median reading speed improves from 16.95 to 9.59 characters/second.
- Maximum reading speed improves from 20.09 to 13.70 characters/second.
- No cue overlaps and no text changes.

The add-on is a separate downloadable package in the ChatGPT work session named `time-stop-10s-run30-readable-subtitles.zip`. It must remain an alternate subtitle track; do not overwrite the canonical voice-synchronous subtitle files unless the user approves the choice.

## Visual review scope

The six dense-sampling sheets cover all 84 shots (252 time samples total), plus a 32-frame key-beat sheet. Main action beats—cup rescue, basketball retrieval/hand-off, corridor book transfer, final bicycle/sign rescue and embrace—remain legible in the sampled moments. Freeze-beat shots are intentionally static; do not treat repeated poses within a time-freeze shot as a defect without checking the scene design.

This is sampled visual QA, not a continuous uninterrupted 6m18s screening. Keep `visual_approval: false`; a human still needs to watch the full master with audio before the Draft Release can be published.

## Candidate and release safety

- Draft Release Run 30 stays at https://github.com/Nolane-x/video/releases/tag/untagged-6d2b148e20b9aadb6662.
- Master SHA-256 remains `f4a7819429796c24393056240244b970c7fbb130445a4184fa60bbe8a03863b7`.
- Preserve Run-28 draft and public Run-20 release.
- Do not rerender for this QA addendum: no change to the video source, scene graph, narration, or master is required.
