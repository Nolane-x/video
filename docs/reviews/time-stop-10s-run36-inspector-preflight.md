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
