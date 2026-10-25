
## Production-grade workflow and persistent memory (H2 SelfImprove Studio v1.1.0)

Before any full render, read the companion references: references/production-pipeline.md, references/quality-gates.md, references/state-handoff.md, references/one-more-scroll-case-study.md and the existing references/kiem-tra.md.

### Non-negotiable contract
- Preserve the native H2 engine, rig, real template/set schema and the dem/doodle packs. Do not silently replace H2 with a handmade SVG stand-in.
- Use cinematic grammar: simple repeatable stick-figure characters, richly staged environments, specific props, practical light, motivated camera, diverse shot sizes, legible expressions and visible action. Avoid generic AI gradients/people and repeated static backgrounds.
- Design action as anticipation → action → contact/impact → follow-through → recovery. If a prop interaction is unclear, fix blocking/rigging before polish.
- Run schema/doctor and duration checks, render all-shot contact sheets, then a short motion proof for every difficult interaction. No P0/P1 unresolved before final export.
- Verify actual MP4 with ffprobe and measure audio loudness/true peak. A configured filter is not a measurement.
- Record exact engine, source commit, workflow run, artifact URL/storage, SHA-256, metadata, QA results and open defects.
- Distinguish H2 Canvas/Chromium output from the separate Remotion pipeline. Never report a render engine that did not run.
- Keep prior known-good master; render to a temporary path and replace it only after technical and visual gates pass.

### Shared production repository
Use https://github.com/Nolane-x/video as persistent production memory. Read its AGENTS.md, .agents/skills/video-production-master/SKILL.md, docs/STATE.md, docs/AI_HANDOFF.md, docs/TOOL_INVENTORY.md, H2 source mirror and film manifest. The H2 plugin is the native render kit; Remotion/Blender/Krita are complementary tools, not synonyms for H2.
