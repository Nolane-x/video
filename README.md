# Nolane Video Studio

Code-first video production workspace for H2 SelfImprove Studio.

## Goals

- Use Remotion for timeline, typography, SVG/2D rig animation, composition, and final MP4 rendering.
- Keep the H2 minimalist character style: simple cream character, charcoal backgrounds, restrained red accent, intentional negative space, and text-driven storytelling.
- Use Blender only where a scene benefits from 2.5D/3D camera, lighting, or rigged motion.
- Use Krita for hand-authored character sheets, expressions, props, textures, and paint-over assets.
- Prefer local/open-source tools and deterministic rendering over paid per-clip AI video generation.
- Validate output using rendered stills, contact sheets, frame checks, audio checks, and an explicit QA checklist.

## Important scope decision

This repository should store **our own project code, production scripts, configurations, story assets, and setup instructions**. It should not vendor entire upstream Remotion, Blender, or Krita source repositories or commit huge split archives. Install those tools through their official package/install mechanisms instead. This keeps licensing, repository size, updates, and CI manageable.

## Production architecture

1. **Story & art direction** — premise, character bible, shot list, emotional beats, palette, camera intention.
2. **Asset creation** — SVG/React for deterministic shapes; Krita for hand-authored assets; Blender for selected 2.5D/3D shots.
3. **Animation** — Remotion frame-driven timeline, explicit keyframes, easing, anticipation, follow-through, and contact checks.
4. **Audio** — dedicated music/SFX tracks; planned silence where dramaturgically useful; loudness and clipping checks.
5. **Quality gates** — render a contact sheet, inspect keyframes and transitions, run typecheck/tests, validate MP4 metadata and audio.
6. **Delivery** — render MP4 and publish it as a GitHub Actions artifact, not as a large binary committed into Git.

## Render pipelines

- **Remotion:** [video-projects/remotion](video-projects/remotion) is the main text/2D animation timeline. Push changes there to start the render workflow; the resulting MP4 is uploaded as a GitHub Actions artifact.
- **Blender:** [tools/blender](tools/blender) contains an optional headless 2.5D/3D style study. The Blender workflow renders a short proof to an artifact.
- **Krita:** [tools/krita](tools/krita) documents the hand-authored asset workflow. Krita source files and exports should only be committed when intentionally created and licensed for the project.

## Local setup

See [docs/SETUP.md](docs/SETUP.md), [docs/WORKFLOW.md](docs/WORKFLOW.md), and [docs/ASSET_POLICY.md](docs/ASSET_POLICY.md).

## Rights & attribution

Follow each tool's license and only commit assets that we created or are authorized to redistribute. See [docs/ASSET_POLICY.md](docs/ASSET_POLICY.md).
