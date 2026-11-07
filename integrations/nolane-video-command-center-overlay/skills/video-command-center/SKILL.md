---
name: video-command-center
description: Use as the single entry point whenever the user asks to create, continue, repair, render, review, package or scale a video project; route by genre and reference language.
---
# Nolane Video Command Center

## Mission
Restore project state, understand the brief, route through the 33 internal skills, use the smallest useful toolset, inspect real outputs and preserve evidence-rich handoff.

## Route before renderer
Read repository state, genre routing, tool inventory and asset policy first. Search the existing resource pool before AI media generation or external downloads. The Build 76 resource release is already above 50 GB globally unique and contains about 1.14 GB of category-level audio ZIPs (some recordings, some synthetic). Its exact asset/source manifests separate creators and rights; do not infer suitability from an archive name.

### Illustrated/cartoon history route
For polished illustrated/cartoon historical explainers with expressive character acting, distinct locations, horse/weapon/world cycles, animated maps, portrait/stat cards, historical-art and legacy framing, route first to illustrated-history-animation-director. This is separate from footage-led historical documentary and H2 Squire. Use the reference study and v1.1 motion system. Build a changing visual vocabulary: embodied action, geography, relationships, work/economy, evidence graphics, period change and legacy. Plan actor/prop/environment/camera/graphics as independent motion channels. Select H2 rigs, Remotion, Motion Canvas, Krita or Blender per shot; keep original art and composition. Prototype difficult actions before scaling.

### Cinematic historical documentary route
For sweeping cinematic history, footage-led documentary craft, archival evidence, 2.5D/3D reconstruction or live-action-inspired references, route first to historical-cinematic-documentary-director. Use a paper edit → radio edit → picture edit workflow. Pick Remotion, Blender, Three.js/GSAP, Krita, archival footage and compositing per shot. Require timecoded camera/motion/audio notes; full normal-speed playback/listening is required for final artistic approval.

### Historical military animation / Squire route
Only when the user explicitly asks for H2 Squire/vector style or an existing Squire series (symbolic round-headed characters, vector formations and tactical diagrams), route to historical-military-animation-director and the separately activated private h2-squire-studio specialist. Do not default to Squire just because the subject is a historic battle or the engine is available.

### Other video routes
Use the established cinematic stick-figure narrative style only when that style is selected by the user or belongs to the existing series. Match documentary, product, explainer, social and motion-graphic formats to their actual purpose; do not impose one universal look.

## Audio policy
Search Build 76 and Meta Open Sound before unpacking broad archives. Use the direct/tag-assisted confidence in search_audio_resources.py; exact file names and tags do not prove sound content. The dedicated CC0 illustrated-history pack v0.2.0 is defined by docs/audio/ILLUSTRATED_HISTORY_FOLEY_ACQUISITION.md and tools/audio/illustrated_history_foley_sources.json, and built by .github/workflows/build-illustrated-history-foley-library.yml. Its release contains weapon handling/impacts, a six-horse gallop, crowd shouts, a forge hammer and generic impacts, plus an offline review console. Check the actual Actions run and release before use. Export review JSON and validate asset IDs/SHA-256/human approval with tools/audio/validate_foley_review_decisions.py before creating a final-mix cue sheet. The pack does not include a finished score.
Use recorded/licensed sound as the foundation. Code may select, synchronize, layer, loop, pan, EQ, compress, duck, reverberate and master recordings. Procedural synthesis is a temporary placeholder or documented exception, not the default soundtrack. Keep score, ambience, Foley, impacts, narration, transitions and stems separate until mix. Route acquisition through historical-audio-library-curator and mixing through audio-postproduction-engineer.

## Motion and QA
Every key shot names camera path, subject/prop action, depth layers and edit motivation. Camera zoom alone is not action. Prototype the hardest action/transition and a representative picture/sound sample before scaling. Motion must be deterministic under arbitrary frame seeking. Require continuous full-length picture and soundtrack review with timecoded defect logs before final artistic approval. CI and contact sheets do not prove artistic approval.

## Repository safety
- Primary repo: Nolane-x/video.
- The asset library has already exceeded the 50 GB unique-resource target. Prioritize category coverage, curated discovery and actual shot diversity, not indiscriminate byte growth.
- Keep changes limited to the assigned production lane.
- Separate public CC0/Public Domain redistribution from item-specific project-use and private production-only sources. Never put unredistributable raw media in public GitHub Releases.
- Never overwrite an existing master. Render a distinct candidate, preserve source/checksum and require explicit approval before merge or promotion.
- Plugin activation is host-controlled. Do not claim hidden plugin-to-plugin calls.
