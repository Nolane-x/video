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
