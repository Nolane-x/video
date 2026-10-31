---
name: video-quality-assurance
description: Audit a video end-to-end for story completeness, caption coverage, visual quality, motion, continuity, audio, synchronization, technical media integrity and deliverable readiness. Use before every final video handoff or when asked to improve an existing video.
---

# Video Quality Assurance — evidence before approval

A render is a candidate, not a finished film. Separate technical validity, creative readiness and user approval.

## Audit sequence

1. Read the approved brief, script, storyboard, transcript, caption file, design bible, asset manifest, upstream provenance and prior QA notes.
2. Probe the candidate with ffprobe or the project's real media probe. Record streams, codec, resolution, aspect, FPS, duration, pixel format, audio channels/sample rate and metadata.
3. Build a frame pack covering every shot and meaningful text/action state. Include opening/middle/end samples for long shots and before/contact/after frames for complex actions.
4. Watch the complete video with sound at normal speed. Then inspect complex sections frame-by-frame or at reduced speed. A contact sheet, OCR result or a set of keyframes is supporting evidence, never a substitute for full moving-picture review.
5. Compare each section with its purpose and approved sources. Flag omitted sections, repeated visual ideas, empty holds, incorrect data, misheard speech, poor transitions and contradictions.
6. Audit every caption/subtitle against the audio. Check wording, timing, punctuation, language, line length, reading duration, contrast, safe areas and overlap with faces/key objects. Do not silently omit key phrases or explanatory on-screen text.
7. Audit visual craft: hierarchy, composition, framing variety, silhouette/readability, lighting motivation, depth, continuity, brand identity and restraint.
8. Audit motion/editing: anticipation, action, contact, reaction, follow-through and recovery; inspect camera and subject movement separately. Check props, feet, shadows, intersections, temporal jitter, frozen ranges and transition seams.
9. Audit sound: intelligibility, pronunciation, measured loudness and true peak, music ducking, SFX timing, channel balance, silence, clicks/pops and sync drift.
10. Record each issue with severity, timecode/frame range, evidence, impact, owning layer and a concrete corrective action.

## Blocking preview — required before a full render

A plan-ready report authorizes only the selected low-resolution motion previews. Use `tools/video/render_blocking_preview.py` and inspect the exact clips for the hook, every physical contact proof, prop continuity, high-risk acting, emotional reaction/listening and final payoff. Record explicit approval against both `previewSpecSha256` (the storyboard + renderer source contract) and `previewArtifactSha256` (the exact rendered clip set), plus reviewer identity, UTC timestamp, all reviewed shot IDs and actionable notes. Validate with `tools/video/validate_preview_approval.py`. If any source, timeline, renderer or preview clip changes, the approval is stale and the preview must be reviewed again. The existence of a successful preview render is not approval.

## Independent evaluation — required for final candidates

Use a reviewer context that did not create or edit the candidate. Give it only:
- the candidate frame pack or video and its approved parent references;
- the technical requirements that can be objectively checked;
- the applicable evaluation criteria.

Do not give the reviewer the producer's prompt rationale, rejected alternatives or explanation of what the scene was "supposed" to mean before its first pass. Start with an open-ended defect search (for example: "Describe anything that looks, sounds or behaves wrong"). Only after the reviewer records its unaided findings should it receive the structured checklist. This reduces confirmation bias and prevents a checklist from becoming a false detector.

The independent reviewer must return:
- open-ended findings first;
- PASS/FAIL for each applicable criterion, with evidence;
- defect class and severity;
- usable time range for motion-heavy/generated shots;
- a concrete fix and the layer responsible.

Still frames resolve staging, not temporal integrity. For motion-heavy/generated footage, inspect the full moving range for frozen sections, looping, drift, seams, identity/prop changes and plausible action. Report the longest usable range; do not call a shot usable for its full duration if only part of it survives review.

## Defect classes and ownership

Classify findings separately; do not compress them into one overall score:

| Class | Typical owner |
|---|---|
| Technical defect | Renderer, media pipeline, codec, timing, audio or delivery configuration |
| Creative defect | Brief, story, visual direction, composition or editorial decision |
| Continuity defect | Character/product identity, prop, environment, screen direction or adjacent-shot relationship |
| Generation/model defect | Input asset, prompt, model capability, temporal artifact or provider execution |

A generation defect is not fixed by rewriting an editorial checklist. A creative defect is not fixed by swapping models. Diagnose the owning layer before changing anything.

## Defect severity

- **P0 — release blocker:** corrupt/unplayable file, missing required stream, wrong deliverable, serious privacy/rights issue, checksum mismatch or failure that prevents use.
- **P1 — major release blocker:** omitted/incorrect information, missing/unreadable important captions, major continuity/story failure, broken action/contact, false product representation, obvious audio sync failure or unusable section.
- **P2 — polish:** small spacing/easing/color/audio-balance/transition problems that remain perceptible but do not destroy comprehension.

Resolve all P0 and P1 defects before calling a candidate production-ready. Document accepted exceptions with rationale and an explicit owner; never silently downgrade severity.

## Corrective-action protocol

Recommend one next action and identify its owner:
- accept
- refine-current
- retry-execution
- revise-reference
- revise-shot-plan
- revise-storyboard
- revise-edit
- change-capability
- reject

Diagnose in order: source/asset mismatch → overloaded brief or prompt → unclear action/end state → camera/blocking error → continuity gap → capability mismatch. Avoid repeated retries at the same layer with unchanged inputs; stop when the agreed attempt or cost ceiling is reached.

## Audio measurement

Do not label output as -14 LUFS, -16 LUFS or any other target merely because a filter was configured. Measure the actual final file, record integrated loudness and true peak, and compare them with the target appropriate to the platform/project. A numeric result does not prove intelligibility or artistic balance.

## Completion language

Keep these states separate:
- source updated
- static checks passed
- preview rendered
- full render completed
- technical QC passed
- full video watched
- independent review passed
- ready for user review
- published / archived only with direct evidence.

A plugin release, CI pass, or successful export is not artistic approval.

## Final release attestation — mandatory

After the candidate passes the full review above, complete `tools/video/editorial-review.template.json` with:
- exact source commit, candidate MP4 path, SHA-256 and ffprobe duration;
- an independent reviewer context/identifier;
- full-playback-at-normal-speed and audio-review confirmations;
- contiguous timecoded visual/audio coverage from 0 to the end;
- scores and timecoded evidence for every category;
- open-ended findings recorded before the checklist;
- every P0/P1 finding either resolved and rechecked or the decision remains REVISE/REJECT.

Validate the attestation against the exact MP4:
`python tools/video/validate_editorial_review.py <review.json> --video <candidate.mp4>`

All category scores must be at least 7/10 and the mean at least 7.5/10; no unresolved P0/P1 defects are allowed. A passing validator confirms that the media identity and review record are complete and consistent. It **cannot prove** that the reviewer actually watched or listened; the independent reviewer is accountable for that attestation. A plan-readiness score is not an artistic quality score and never replaces this final gate.

## Source provenance

This protocol adapts high-level evaluation practices from sb-dev/video-production-skills at commit 5e82bb9a188d3cfc83cae0979cc39737011411b9 (Apache-2.0). No upstream TypeScript evaluator scripts are bundled or claimed as locally runnable here. See docs/EXPERT_SKILL_SOURCE_AUDIT.md for source scope, licensing and adaptation boundaries.
