# Genre routing matrix

This matrix distinguishes **content genre** from **render engine**. A genre selects a production recipe; it does not rename or replace existing renderers.

| Genre | Primary route | Engine | Typical delivery | Key QA |
|---|---|---|---|---|
| Cinematic stick-figure narrative | Existing H2 / Remotion route | H2 Canvas/Chromium for native H2 projects; Remotion for its own timeline | Story-led short and long-form films | Character continuity, action contact, motivated camera, caption legibility, audio arc, full-motion review |
| Historical military animation | Squire route | H2 Squire 2D/vector canvas engine with Squire character, army, horse, map and tactical packs | English 16:9 long-form films and 9:16 Shorts | Historical claim ledger, tactical legibility, exact voice ID/provenance, narration alignment, scene variety, sound, full-film review |
| Mathematical/scientific explainer | Manim route | Manim / Remotion as selected by the brief | Formula-led and data-led explainers | Mathematical correctness, readable equations, pacing, accessibility |
| 2.5D / 3D sequence | Shot-specific specialist route | Blender / Three.js / compositing | Selected depth-rich shots inside a larger edit | Geometry, camera, lighting, render passes, integration |
| Product/UI walkthrough | Browser-capture / Remotion route | Playwright capture plus Remotion | Real product walkthrough and feature film | Actual app state, privacy, readable text, interaction truthfulness |

## Squire historical-military route

- **Specialist plugin:** h2-squire-studio v1.2.2, private user plugin plugins_6aec6edf62248191b2eb6333f7620cbc.
- **Command Center route:** internal skill historical-military-animation-director; specialist activation remains explicit through the host.
- **GitHub integration:** integrations/h2-squire-studio/ contains the current plugin's engine and both Squire skills.
- **Projects:** video-projects/squire/<slug>/.
- **Voice service:** VoiceStudio reusable Actions workflow, pinned by the immutable commit SHA recorded in each production workflow.
- **Reference pilot:** [Cannae — How Hannibal Turned Rome's Army Into a Trap](../video-projects/squire/cannae-216bc/README.md).
- **Workflow:** [.github/workflows/squire-cannae-longform.yml](../.github/workflows/squire-cannae-longform.yml).
- **Delivery:** Actions artifact first. Release archiving and public approval are separate explicit steps.

## Routing rules

1. Explicit requests for animated ancient, medieval, samurai, Viking or other military history in the Squire look route to Squire unless the user names a different engine.
2. Requests for the established cinematic stick-figure narrative look stay on the existing H2/Remotion route.
3. Blender, Krita, Playwright, Remotion and FFmpeg can support a Squire project, but they do not silently replace Squire as the primary renderer.
4. Keep the current master and historical renders unchanged. A new Squire film is a separate candidate and project folder.
5. Never claim rendered, technical pass, human approval or permanent archive without the corresponding workflow output, measurements and review evidence.
6. Historical force strengths and casualty numbers require explicit attribution and uncertainty language. Distinguish source fact from visual reconstruction.
