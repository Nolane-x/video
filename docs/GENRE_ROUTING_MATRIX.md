# Video genre and production routing matrix

This is a decision aid for the Command Center and Video Production Master skill. It is not a rigid template: use the user's brief and current project state as the source of truth, select only the smallest effective engine/skill set, and record any deliberate exception.

## 1. Brief contract — required before tool selection

Record or resolve:

- **Genre / purpose:** documentary, educational explainer, narrative film, product/software demo, tutorial/training, interview/podcast, music video, short-form social, advertisement, or hybrid.
- **Audience and platform:** who watches, what they know, where they watch, and the required aspect/resolution/frame rate.
- **Runtime and structure:** target duration, hook, sections/story beats, intro/outro, transitions and cutdown requirements.
- **Language and text:** narration policy, transcript source, subtitles/captions, on-screen labels, safe areas and required reading time.
- **Accuracy contract:** sourced claims, equations/data, actual product/UI behavior, scripted dialogue or fictional story.
- **Visual grammar:** live-action, authentic documentary footage, authorized screen capture, authored 2D, 3D, motion graphics, data visualization or mixed media.
- **Asset and release constraints:** provenance, license, privacy/publicity, commercial/monetized use, paid APIs, model weights, hardware, storage and delivery format.

If the user already supplied a field, do not ask them to repeat it. Mark unresolved assumptions; do not silently invent them.

## 2. Routing matrix

| Genre / deliverable | Primary creative owner | Typical engine mix | Required evidence before delivery |
|---|---|---|---|
| Documentary / factual story | Documentary research + fact-check, story architect, cinematography | Verified source footage/stills, authorized capture, Remotion/HyperFrames for maps/titles, FFmpeg for edit/master | Claim-source ledger; source timestamps; asset/license/credit records; factual review; footage continuity; full-picture and sound review |
| Science / mathematics / engineering explainer | Explainer director + research/fact-check + data visualization | Manim for equations/geometry; D3/SVG for source-backed charts; Remotion/HyperFrames for pacing, labels and composition; Blender only when 3D spatial reasoning adds value | Verified formula/data/units; reproducible chart inputs; equation/layout checks; timed text/labels; full playback and narration/audio review |
| Narrative animation / short film | Story architect + cinematic director + storyboard/animatic | H2 for the existing native rig/profile; Remotion or HyperFrames for frame-driven scenes; Blender/Three/Pixi for justified 3D/depth/effects; Krita for authored art | Script-to-shot coverage; character/art bible; shot variety; motion/contact proofs; text/subtitle completeness; sound sync; rights; full audiovisual review |
| Product / software demo | Product truth reviewer + browser-capture director + editor | Playwright or authorized screen capture for real states; Remotion/HyperFrames for callouts, zooms and transitions; FFmpeg for finishing | Verified product build/version; reproducible click path; unaltered proof of actual behavior; disclose mockups; redact private data; UI text/captions; full playback |
| Tutorial / training | Instructional designer + technical reviewer + editor | Real screen capture/browser capture; Remotion/HyperFrames for step labels; Manim/diagrams where explanation benefits; FFmpeg for chaptering/audio | Learning objective and step coverage; version-specific commands; tested steps; cursor/zoom readability; captions/transcript; sound intelligibility; full playback |
| Interview / podcast / narration-led video | Producer/editor + speech/caption alignment + audio postproduction | Camera/screen source; WhisperX or other approved ASR for draft transcript; OTIO for edit exchange; FFmpeg for cleanup/master; Remotion for lower thirds/captions | Consent/rights; source media preserved; transcript decisions reviewed by human/editor; speaker labels not inferred without evidence; caption-to-audio alignment; measured loudness/true peak; sync review |
| Music video / rhythm-led edit | Music-video editor + cinematography + motion designer | OTIO/EDL for editorial plan; PySceneDetect for candidate cuts; Remotion/HyperFrames/Blender for authored motion; FFmpeg for mastering | Music and footage rights; beat map; edit decisions tied to the track; no false claims of automatic beat correctness; sync and full audiovisual review |
| Short-form social / vertical | Retention editor + platform packaging + caption QA | Remotion/HyperFrames for kinetic text/cutdowns; authorized footage/screen capture; FFmpeg for delivery variants | Hook in opening seconds; 9:16 safe zones; mobile legibility; subtitle coverage; platform duration/codec; call-to-action; full mobile-size review |
| Advertisement / campaign | Creative director + product/legal reviewer + rights auditor | Remotion/HyperFrames for graphics; authored footage/2D/3D/AI media where licensed; FFmpeg finishing | Approved claims and offer terms; product truth; trademark/model/voice/media permissions; disclosure requirements; brand consistency; final legal/brand and audiovisual approval |
| Hybrid / AI-generated inserts | Director + AI media asset director + provenance/rights auditor | Choose generation/capture per shot; keep exact typography/data editable; compose in Remotion/Blender/HyperFrames; FFmpeg finishing | Model/provider/version and prompt provenance; input/output rights; likeness/privacy; artifacts reviewed for hallucinations; editable text; source/cost record; final composited shot QA |

## 3. Engine selection rules

- **Remotion:** preferred when the deliverable needs frame-accurate React composition, editable text/captions, transitions, data-driven scenes or repeatable render automation.
- **HyperFrames:** use for deterministic HTML/CSS/GSAP compositions, beat grids, motion snapshots and browser-based strict checks.
- **Manim:** reserve for mathematically meaningful equations, graphs, geometry and scientific transformations. Validate the math before animation; do not use it merely as a generic video editor.
- **H2 Studio:** use only when its native kit/schema is actually available and the brief calls for that established rig/profile. It is not the same renderer as Remotion.
- **Blender:** use when real spatial geometry, rigging, lighting, camera depth or 3D simulation materially improves a shot. Start with a small CPU proof; do not assume GPU on standard Actions runners.
- **Three.js / PixiJS:** browser-native 3D/2D, particles, shaders, depth and effects when these are simpler/lighter than a Blender render.
- **Krita:** authored 2D assets, paintovers, character/expression sheets, props and textures; not a headless video engine.
- **OpenTimelineIO:** frame-aware timeline interchange and editorial handoff. It does not contain media or render a film.
- **PySceneDetect:** candidate shot boundaries; an editor decides cut points and handles false positives.
- **Playwright / OCR:** authorized screen capture and machine-assisted text coverage. OCR is a detector/evidence source, not a replacement for visual inspection.
- **WhisperX / Demucs:** optional/manual audio-ML profile only. Verify language/model/weight licenses, hardware, cost and privacy before setup; do not download weights by default.
- **FFmpeg / ffprobe:** mastering, media transforms, frame extraction and technical verification. Record build flags and measure the actual final file.

Do not install or invoke every engine for every deliverable. Route by requirements, resource budget and available evidence.

## 4. Universal quality gates

1. **Brief fidelity:** the delivered film answers the requested purpose, audience, platform, duration, ratio, language and format.
2. **Information/story completeness:** no missing script sections, required steps, essential claims, dialogue, captions or on-screen information.
3. **Truth and provenance:** factual claims cite sources; product behavior is real; source media, generated media, fonts, music, voices and models have recorded permissions/terms.
4. **Visual craft:** deliberate hierarchy, composition, visual grammar, typography, contrast, shot variety and continuity. Do not substitute generic templates or random zooms for direction.
5. **Text/caption coverage:** a per-shot contract for subtitles and meaningful visible headings, labels, counters, kinetic words and end cards; explicit reason for shots intentionally containing no text; OCR detection in multiple samples (not a single hit); readable dwell time; safe-area placement; no overlap with important faces/product UI.
6. **Motion/editing:** action reads; camera movement has purpose; transitions, shot timing and beat alignment serve comprehension/story.
7. **Audio:** dialogue/narration is intelligible; music/SFX are licensed and synchronized; measure actual integrated loudness and true peak for the target platform.
8. **Technical:** verify stream count, codec, resolution, aspect ratio, FPS, duration, sample rate, channels, metadata and SHA-256.
9. **Visual review:** inspect the whole moving picture with audio; use contact sheets and targeted frame samples as supporting evidence, not substitutes.
10. **Handoff:** record source commit, exact engine, workflow/run, master/preview URLs, SHA-256, metadata, reports, unresolved defects and approval state.

## 5. Completion vocabulary

Keep these states separate in every report:

- `source updated`
- `static checks passed`
- `runtime/install proof passed`
- `preview rendered`
- `full render completed`
- `technical QC passed`
- `full video watched`
- `editorial/visual QA passed`
- `ready for user review`
- `published` / `archived` only when the permanent URL and checksum are independently verified

A green CI result does not imply the film is artistically approved. A plugin's existence does not prove that its upstream engine is installed or that it can silently invoke other private plugins.
