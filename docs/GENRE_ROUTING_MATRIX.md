# Video genre routing matrix

The repo supports multiple visual genres. The default cinematic stick-figure style remains the established route for narrative explainers. H2 Squire is an explicit opt-in genre and must not become the global house style.

| Profile | Trigger | Primary renderer | Supporting systems | Required evidence |
|---|---|---|---|---|
| Cinematic stick-figure narrative | User requests the established Ifverse / Day One-style story animation or an existing series in that look | Existing H2-dem or Remotion route, chosen per project | Blender/Krita only for specific shots; FFmpeg for mastering | Character bible, shot plan, contact sheets, moving action/contact proof, full AV review |
| Historical military animation — Squire | User explicitly requests animated military history in the Squire visual grammar, or continues an established Squire project | H2 Squire Canvas/Chromium renderer | VoiceStudio for authorized synthetic narration; procedural Squire music/SFX; FFmpeg/ffprobe; Blender only for a shot with a clear 3D need | Research ledger, script, art bible, scene plan, generated voice manifest, Squire contact sheets, 30-second preview, full MP4 technical QA, human full-length AV review |
| Data / science explainer | User asks for data, charts, mathematical or scientific explanation | Remotion or Manim, depending on whether the shot needs a timeline composition or mathematical scene | D3/SVG and audio systems as needed | Source ledger, chart/data contracts, scene timing, OCR/text checks, full AV review |
| Product / UI walkthrough | User asks to show a real product, web UI or workflow | Playwright capture for actual UI; Remotion for deterministic composition around it | FFmpeg, caption/OCR QA | Authorized capture, privacy review, source/state provenance, visual/text QA |
| Hybrid cinematic sequence | The brief requires two distinct kinds of shots and names the reason | Explicit primary renderer plus only the justified secondary engine | Shot-level handoff; never merge engines by assumption | Per-shot engine map, synchronized timing, one coherent audio master, full AV review |

## Squire profile guardrails

- Squire is the genre-specific renderer for code-drawn military-history animation. It is not the Remotion renderer.
- It does not require AI-generated stills; characters, horses, formations, maps, diagrams, score and SFX can be code generated.
- Use the exact Squire source archive and checksum in `integrations/h2-squire-studio/`; regenerate build-time audio on the runner and do not commit `node_modules` or transient WAV caches.
- Synthetic narration must use a canonical VoiceStudio voice ID with a recorded rights/attribution notice. The VoiceStudio job is a separate reusable workflow and its artifact must be verified before rendering.
- Long-form default: English 16:9, 1080p/24fps, 9–11 minutes. Shorts: 9:16, 60–75 seconds. These are defaults, not immutable requirements.
- Historical facts, troop estimates and quotations must be sourced and disputed estimates must be labelled.
- Do not promote a candidate to master until a human reviewer has watched the full moving picture with audio.

## Ownership boundary

Never edit or trigger the parallel asset-library workflow or write under `video-library/**` as part of ordinary genre routing. Squire integration and projects belong under `integrations/h2-squire-studio/` and `video-projects/squire/`.
