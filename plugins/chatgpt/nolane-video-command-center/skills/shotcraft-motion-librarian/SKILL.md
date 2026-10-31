---
name: shotcraft-motion-librarian
description: Use when searching reusable Shotcraft motion recipes and exact Remotion demo implementations for cinematic shots, transitions, typography, camera, UI motion or data graphics.
---
# Shotcraft Motion Librarian

## Source
Upstream repository: `https://github.com/Vincentwei1021/video-shotcraft` (Apache-2.0 source code). The source has 152 recipe cards and a large Remotion demo collection. Check the current repo and license at the time of use; snapshots can be stale.

## Retrieval workflow
1. Search recipe categories by visual purpose: opening, camera, UI entrance, interaction, typography, data, effects, rhythm, transitions and outro.
2. Read the full recipe. Extract purpose, duration, frame grammar, composition, movement curve, parameters, dependencies and pitfalls.
3. Follow the source demo index to the exact TSX implementation. Read imports and shared fixtures; never invent the demo filename from the recipe title.
4. Compare candidate recipe against the shot's story purpose, visual bible, target aspect ratio and timeline engine. Do not stack effects without a narrative reason.
5. Adapt design tokens and all copy/branding. Preserve Apache notices and attribution, while checking any media and audio files independently.
6. Render a standalone low-resolution moving proof at target FPS. Inspect easing, frame boundaries, parallax, text hold, transition and mobile legibility.
7. Record recipe slug, upstream commit/version, source path, modified files, dependency versions and attribution.

## Boundaries
- A repository license does not automatically license preview footage, sound effects, music, fonts or embedded external assets.
- Do not bulk-copy the Shotcraft repository into the user's resource library. Do not modify `video-library/**` or trigger asset work; the parallel agent owns that.
- Treat Talkcraft as a different project with a PolyForm Noncommercial 1.0.0 license. Do not use its recipes/demos/audio/templates/code for monetized or commercial output without written commercial permission.
- Prefer a small selected set of implementations over copying every recipe.

## Output
Recipe shortlist, exact source/demo references, dependency map, adapted shot plan, attribution note and proof-render review.
