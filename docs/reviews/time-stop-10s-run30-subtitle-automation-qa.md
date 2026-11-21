# Run 30 — readable subtitle automation QA

Date: 2026-11-21  
Repository: Nolane-x/video  
Review branch: review/time-stop-10s-3d-fixes

## Purpose

Make the already-reviewed extended-dwell Vietnamese subtitle alternative reproducible in GitHub Actions. This pipeline operates only on the subtitle files extracted from the immutable Run-30 render artifact. It does not change the master MP4, voice WAV, narration timing, canonical SRT/VTT or release state.

## Source of truth

- Render workflow run: https://github.com/Nolane-x/video/actions/runs/44873063135
- Source artifact: time-stop-10s-h2-30
- Master MP4 SHA-256: f4a7819429796c24393056240244b970c7fbb130445a4184fa60bbe8a03863b7
- Original SRT SHA-256: 7e0872b4fa958c089f9b44845530fb103a57eb25bd3527aacec16b9c1f1fefd4

## Reproducible implementation

- Builder: video-projects/time-stop-10s/tools/extend_readable_subtitles.py
- Unit tests: video-projects/time-stop-10s/tests/test_extend_readable_subtitles.py
- Workflow: .github/workflows/build-time-stop-run30-readable-subtitles.yml
- The builder uses only Python's standard library.
- The workflow tests parsing and cue invariants, downloads the immutable Run-30 artifact, generates SRT/VTT, checks golden SHA-256 values, creates an inner ZIP with its own manifest, and uploads the full output directory.
- The workflow is triggered by the marker file, its own workflow definition, and builder/test changes.

## CI verification — original compatible-actions run

- Run: https://github.com/Nolane-x/video/actions/runs/44890042017
- Result: completed / success.
- Main job: Rebuild and validate the alternate Vietnamese subtitle track
- All 8 functional steps succeeded: checkout, Python setup, unit tests, source artifact download, subtitle generation/invariant checks, summary, artifact upload.
- Artifact ID: 14701638125; 20,391 bytes.
- Artifact digest: f268443e02e93aa564ab4248be33ac6675036471d10c8c64909b82d7be206ba4

## CI verification — immutable Node 24 action pins

The workflow now pins four upstream actions to immutable commit SHAs and triggers when its own definition changes:

| Action | Pinned ref | Release |
|---|---|---|
| actions/checkout | 3d3c42e5aac5ba805825da76410c181273ba90b1 | v7.0.1 |
| actions/setup-python | 6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 | v7.1.0 |
| actions/download-artifact | 9000827ccba6bdab643e8b6fd33ac0654aef8333 | v8.0.2 |
| actions/upload-artifact | cf430e030ddbb5b0abf93d22962f4752f3646cd9 | v7.0.2 |

- Pin commit: 78cff3d71f8db80a5686e973fd8458704baf1d44
- CI run: https://github.com/Nolane-x/video/actions/runs/44892508009
- Result: completed / success; all 8 functional steps succeeded.
- Job ID: 136811168434
- Artifact ID: 14702017799; 20,390 bytes.
- Artifact server digest: f9f1752f6ec1ddd41f75a81e26d0cce2ff67f44d16c635bc1b2acef8eaadf71d
- Download: https://github.com/Nolane-x/video/actions/runs/44892508009/artifacts/14702017799
- The downloaded artifact's SHA-256 matches the artifact server digest exactly.
- Logs confirm that all four exact pinned SHAs were loaded. The prior Node.js 20 deprecation warning and punycode warning were absent from this run.

## Downloaded artifact integrity verification

The Run-44892508009 output was downloaded and inspected locally.

- Outer artifact ZIP: integrity test passed; 7 entries.
- Nested distribution ZIP: integrity test passed; 6 entries.
- Outer SHA-256 manifest: 5/5 entries verified.
- Nested SHA-256 manifest: 5/5 entries verified.
- Canonical and alternate subtitle files all match their approved golden SHA-256 values.
- Source SRT checksum is the expected Run-30 source checksum.
- The artifact server digest equals the locally calculated outer ZIP SHA-256.

## Subtitle QA

| Measure | Original | Extended dwell |
|---|---:|---:|
| Cue count | 84 | 84 |
| Median reading speed | 16.95 chars/s | 9.59 chars/s |
| P90 reading speed | 18.55 chars/s | 11.42 chars/s |
| Maximum reading speed | 20.09 chars/s | 13.70 chars/s |
| Minimum dwell | 1.20s | 4.38s |

Hard invariants:
- Source cue overlaps: 0.
- Output cue overlaps: 0.
- Changed cue text: 0.
- Changed cue start timestamps: 0.
- Voiceover timing changed: false.
- Final alternate cue ends at 378.0 seconds.
- Each alternate cue ends 0.12 seconds before the next narration cue begins, except the last cue, which ends at the master duration.

## Boundaries and remaining approval gates

This CI success establishes reproducible subtitle generation and artifact integrity only. It does not establish artistic approval of the film.

- Keep canonical voice-synchronous subtitles unchanged.
- Keep Run-30 release as a draft.
- Keep visual_approval: false.
- Do not publish until a human watches the full 6m18s master uninterrupted with sound.
- No video re-render was necessary for this subtitle-only work.


## Runtime and unit-test final audit

- The pinned action metadata was fetched from each exact SHA at its upstream repository. All four action.yml files explicitly declare runs.using: node24.
- The GitHub-hosted runner reported version 2.338.2, above the actions' Node-24 minimum runner requirement of 2.327.1.
- The final pinned CI job ran all 5 unit tests, all passed in 0.087s:
  1. Multiline SRT parsing.
  2. Extended dwell preserves cue starts and text.
  3. Source subtitle overlaps are rejected.
  4. Incorrect expected cue count is rejected.
  5. WebVTT omits numeric cue identifiers and preserves valid timestamps.
- Action metadata blob SHAs:
  - checkout action.yml: 5b0524f730db83f9513c18ab31a6c086c7239076
  - setup-python action.yml: 645de4f5108b28bcc7ed043ee171770b0754cc35
  - download-artifact action.yml: 8b8c65029ccad20750a29fecb438eca5a607fc57
  - upload-artifact action.yml: 7cb4d1e81db55320b41217e1a78a1a46e3d2baef

