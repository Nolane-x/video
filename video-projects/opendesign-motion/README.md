# OpenDesign Motion — reconstruction study

This is a genre-specific motion-design project inside the wider Nolane Video production ecosystem. It is **not** the H2 SelfImprove Studio pipeline and does not replace the existing One More Scroll Remotion composition.

## Reference analysis

User-supplied reference: `preview.mp4`, 37.312 seconds, 1920×1080, 30 fps. The source video, extracted frames, soundtrack and third-party logos are intentionally not committed to this public repository.

The reconstruction follows the reference's shot rhythm and motion vocabulary: pastel prompt opening, oversized typographic reveal, brand/positioning card, perspective poster wall, high-energy kinetic poster sequence, model/agent carousel, UI showcase, 3D countdown and rotating-cube end lockup. All artwork and the score in this project are newly authored.

## Render

The project shares the existing Remotion 4.0.538 installation but registers its own composition:

- Composition ID: `OpenDesignMotion`
- 1920×1080, 30 fps
- 1,119 frames / 37.3 seconds
- Source of truth: `shot-map.json`
- Composition: `../remotion/src/OpenDesignMotion.tsx`
- Original generated score: `../remotion/public/audio/opendesign-motion-score.wav` (created during Actions)

The dedicated workflow is `.github/workflows/render-opendesign-motion.yml`. It runs on pushes to `feature/opendesign-motion-rebuild` and can be manually re-run from the Actions UI. It typechecks, synthesizes audio, renders, masters, probes, creates contact sheets and uploads a review artifact. It does not change the existing `render-remotion.yml` or H2 workflows.

## Production decisions

- Remotion is the primary renderer for deterministic frame-driven typography, poster composition, vector graphics, UI and transitions.
- The final rotating cubes use CSS 3D transforms. Blender is not forced into this short CPU-friendly piece because the reference's 3D forms are simple, graphic and controllable in CSS.
- The soundtrack is original procedural audio generated in Python's standard library. The reference audio is not reused.
- The reference's visual structure is studied, but the original uploaded frames, soundtrack and source logos are not copied into the repository.

## Review

Start with `shot-map.json`. Review both contact sheets and the complete MP4. Check type legibility, motion continuity, timing, transition quality, colour balance, audio/music sync, end-card hold and technical metadata. Do not call the piece finished merely because Actions is green.

## Upstream skill reference

The workflow was informed by the MIT-licensed `motion-graphics` skill from [Mort1d/motion-graphics-skills](https://github.com/Mort1d/motion-graphics-skills), version 1.4.1. We use its public craft ideas (beat-grid direction, frame-first motion, motion blur awareness, readable kinetic type, original score and critique gates) while implementing an independent Remotion composition. No upstream script or copyrighted media is copied into this project.
