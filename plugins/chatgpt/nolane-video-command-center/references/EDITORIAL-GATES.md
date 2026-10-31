# Editorial gates — Command Center v0.8.0

A technically valid export is a candidate, not a finished film. The production path has two independent gates.

## Gate A — editorial plan preflight (before rendering)

From the repository root:

```bash
python tools/video/evaluate_editorial_plan.py path/to/shots.json --output out/editorial-plan-report.json --strict
```

The preflight requires a named audience, platform, language, aspect ratio, viewer promise, hook, payoff, narration policy and visual grammar. It also checks:
- a story arc with purpose, and a story function for each shot;
- shot size, camera angle/movement, composition and visual purpose;
- explicit motion/contact/follow-through planning for physical actions;
- non-mechanical pacing, justified long holds and visible variation when a template repeats heavily;
- planned subtitle/transcript and music coverage.

A blocked plan must be revised. A plan-ready result authorizes only blocking/animatic and a low-cost preview. It is not a subjective quality score and never grants final release approval.

## Gate A.5 — rendered blocking preview and approval (before full render)

Once Gate A is ready, render the seven selected story/action proofs:

```bash
python tools/video/render_blocking_preview.py video-projects/remotion/public/story/shots.json --project-root video-projects/remotion --output video-projects/remotion/out/blocking-preview
```

The preview consists of low-resolution motion clips, not contact sheets alone. Inspect the hook, phone release, writing/action contacts, shoe tying, café door, listening reaction and shared two-shot. The owner/reviewer must add a `creativeBrief.blockingPreviewApproval` object with reviewer ID, ISO-8601 UTC time, exact `previewSpecSha256`, exact `previewArtifactSha256`, all `reviewedSegmentIds` and concrete `reviewNotes`.

The full render workflow verifies approval with:

```bash
python tools/video/validate_preview_approval.py video-projects/remotion/public/story/shots.json --project-root video-projects/remotion --manifest video-projects/remotion/out/blocking-preview/manifest.json
```

A missing/stale approval blocks the full render. Changes to the shot plan, renderer source, selected segments or preview clips invalidate it. CI only verifies the attestation and hashes; it cannot attest that the reviewer genuinely watched the clips.

## Gate B — independent full audiovisual review (after rendering)

Start from `tools/video/editorial-review.template.json`, fill it for the exact candidate, then run:

```bash
python tools/video/validate_editorial_review.py out/editorial-review.json --video out/candidate.mp4
```

A release-ready review requires:
- independent reviewer context;
- full playback with audio at normal speed;
- contiguous timecoded visual + audio coverage from first frame through the final frame;
- open-ended findings recorded before the checklist;
- evidence for separate scores covering story, pacing, visual variety, motion/continuity, intelligibility, captions, reference fit and platform fit;
- all scores at least 7/10 and average at least 7.5/10;
- no unresolved P0/P1 defects;
- exact MP4 SHA-256 and duration matching the reviewed file.

The validator checks the record and the media identity. It cannot prove that the reviewer genuinely watched the video; this is an accountable reviewer attestation, not an automated truth oracle.

## What must never be conflated

| Evidence | It proves | It does not prove |
|---|---|---|
| JSON/schema + timeline validator | Plan is structurally valid | Story is compelling |
| OCR coverage | Required text appears in sampled frames | Text is important, well-written or readable in motion |
| ffprobe + loudness | Streams/specs and measured levels | Sound design, clarity or emotional fit |
| Contact sheets | Staging and visual variety at sampled frames | Motion, timing, continuity or full narrative |
| Plan preflight | Creative brief and shot-plan completeness | Final rendered quality |
| Independent full review attestation | A reviewer records full audiovisual inspection and evidence | The validator itself cannot verify the reviewer's honesty |

Never report "production-ready", "approved", "published" or "archived" from a render/checksum/OCR pass alone.

## Renderer contract

The Remotion timeline now consumes each shot's explicit `start` and `end` seconds, rather than assigning every scene a fixed five-second frame budget. The preflight requires a continuous timeline from 0 to the declared duration, with no gaps/overlaps. It also reads the music arc and checks that voiceover/dialogue plans include timed audio-file references. The renderer can read optional `audioPlan.narration` clips from `public/audio/narration/` and `audioPlan.soundCues` from `public/audio/`; a file must actually be generated/staged before a full render can succeed.

A dynamic renderer only enables meaningful timing; it does not design the story or guarantee that varied durations are artistically correct. Those decisions still need to be made in the storyboard and checked in an animatic.
