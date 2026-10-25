# Production workflow

This repository uses a gated, code-first pipeline rather than generating a new AI video clip for every shot.

## 1. Brief and art direction

Before writing animation code, specify:
- audience, takeaway, and emotional arc
- character bible and allowed pose/expression changes
- visual palette, shape language, lighting, and texture budget
- shot list with action verbs, framing, camera intention, duration, caption, and audio cues

## 2. Build assets

- Use SVG/React for simple repeatable H2 characters, props, titles, and diagrams.
- Use Krita for hand-authored expression sheets, props, paper textures, and paint-overs.
- Use Blender only for selected scenes needing 2.5D/3D camera, lighting, or a reusable rig.
- Preserve character silhouette and proportions between shots.

## 3. Animate

Every shot needs a readable action, not only a camera zoom. Favor anticipation, action, contact, follow-through, and recovery. Use deterministic frame-based values and easing; avoid random values at render time. Keep camera moves motivated and restrained.

## 4. Quality gates before a full render

- Render key frames at shot start, midpoint, and end.
- Build a contact sheet and inspect it visually.
- Check spatial continuity, contact points (hands/phone, fist/bag, feet/stairs), text-safe areas, visual variety, and character consistency.
- Render a short low-resolution proof before a full-quality export.
- Run typecheck/tests before rendering.
- Inspect final MP4 dimensions, FPS, duration, audio presence, clipping, and loudness.
- Keep intentional silence when the story calls for it.

## 5. GitHub rendering

A push that changes `video-projects/remotion/**` or the render workflow starts GitHub Actions. The job installs the pinned top-level packages, runs TypeScript checks, renders MP4, and uploads it as an Actions artifact. Do not commit rendered MP4 files into Git history.

The first workflow run is a practical environment test. If a package, browser, or codec fails, fix the workflow based on the actual log rather than declaring success based on a locally generated substitute.
