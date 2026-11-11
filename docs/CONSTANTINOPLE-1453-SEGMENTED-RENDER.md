# Constantinople 1453 — segmented master render

## Why the original full render was replaced

The first full-length GitHub Actions attempt (run `42982265108`) was cancelled at the hosted-job six-hour execution limit. Its renderer had produced `161,153 / 229,896` frames (70.1%) at a stable approximately `8.02 fps`; the runner was then terminated before the working directory could be uploaded. No complete master was produced by that attempt.

## New render architecture

Workflow: `.github/workflows/squire-constantinople-segmented-master.yml`

The project is authored and validated once, then archived as a prepared-project bundle. Four independent hosted runners restore the same project and render fixed, non-overlapping intervals at native 240 fps:

| Shard | Start | End | Expected frames |
|---|---:|---:|---:|
| 0 | 0.000 s | 239.475 s | 57,474 |
| 1 | 239.475 s | 478.950 s | 57,474 |
| 2 | 478.950 s | 718.425 s | 57,474 |
| 3 | 718.425 s | 957.900 s | 57,474 |
| **Total** | **0.000 s** | **957.900 s** | **229,896** |

Each shard has its own frame-count, resolution, native-frame-rate, duration and SHA-256 gate. A final assembly job checks all four manifests, concatenates the segments without re-encoding, verifies the 229,896-frame silent master, produces a short audio preview, mixes narration/score/Foley, renders the thumbnail, and runs the existing strict long-form QA before uploading the master artifact.

The workflow uses a unique concurrency group per run and cancels superseded attempts at startup, preventing an older render attempt from occupying the runners.

## Delivery and review gates

- The master artifact keeps the existing name pattern so the readable-caption workflow can attach its separate subtitle artifact after a successful run.
- Original SRT/VTT captions remain in the master package. The post-run caption workflow also emits reflowed sidecars, with source originals preserved, a 42-character line cap, a two-line cue cap, source-word preservation, reading-speed measurements and SHA-256 manifests.
- Automated technical QA is not artistic approval. A complete human watch-through and audio audition are still required before public release or merge to the default branch.
