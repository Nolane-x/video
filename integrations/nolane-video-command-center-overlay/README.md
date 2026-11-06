# Nolane Video Command Center v0.9.6

One private front door for Nolane video production. It includes **33 internal skills**, **37 core specialist plugins**, and **1 genre-specific H2 Squire specialist** (38 separately activated specialist plugins total).

## What's new in v0.9.6

- Adds a dedicated **illustrated-history-animation-director** for expressive 2D/cartoon history: character rigs, pose-led acting, prop choreography, moving environments, parallax, motivated camera paths, animated maps and information graphics.
- Adds **historical-audio-library-curator** with source-first recorded Foley/ambience/music, rights separation, exact attribution, SHA-256 and human audition gates.
- Adds a detailed illustrated-history motion reference covering character/prop/environment/camera/graphic channels, camera grammar, action cycles, uniqueness checks and full-motion QA.
- Adds searchable metadata indexes for the 2,331 Build 76 redistribution candidates and 1,583 pinned Meta Open Sound samples, then an offline playable audio preview bank.
- Routes sound selection through lightweight catalogs before unpacking source archives, preserving Oculus CC BY 4.0 attribution and CC0 instrument rights.
- Links each Meta OGG preview to its exact WAV master source member, size and SHA-256. The Oculus WAV master is mirrored in the permanent Release; instrument masters can be acquired one collection at a time through GitHub Actions.
- Routes illustrated/cartoon history, footage-led cinematic documentaries and H2 Squire vector history as three separate visual languages.
- Keeps H2 Squire as a separate route only when the user explicitly asks for its symbolic/vector military-history style or an established Squire series.
- Makes full-motion sampling, explicit inspection-scope reporting, source provenance and timecoded audiovisual review mandatory. No workflow success or contact sheet is treated as artistic approval.
- Makes recorded SFX, Foley, ambience and licensed music the default; code synchronizes, layers and masters recordings rather than replacing the soundscape with oscillators.

## Unified audio search

Use `python tools/audio/search_audio_resources.py --query "katana sword clash"` to search Build 76 and Meta Open Sound together. Add `--kind foley` or `--kind instrument` to separate effects from note samples, and `--json` for structured results. Rights-review candidates are excluded by default; no search result bypasses human audition.

## Lossless audio workflow

The Meta catalog maps each OGG preview to `source_wav_file`, WAV archive, download URL and SHA-256. Oculus WAV is in the permanent Nolane audio Release. For Piano/Nylon/Steel, run `.github/workflows/acquire-meta-open-sound-wav-master.yml` and select only the collection required; it verifies file size and SHA-256 before publishing.

## Private production sound sources

The source map also tracks the Sonniss GDC 2026 bundle as `private_production_only`. Its current EULA allows film/video synchronization but prohibits raw-file sale and AI/ML training. Because the main repository is public, never upload Sonniss source archives or loose recordings to public branches, Releases or preview artifacts; only retain sanitized cue metadata. The licensee must accept the EULA before downloading.

## How to use

1. Start with the Command Center and describe the story, audience, platform, language, duration and reference.
2. It restores repository/project state and selects the visual route before choosing an engine.
3. For illustrated/cartoon history, use expressive rigs, varied environments, action/prop blocking, parallax and progressive map/graphic reveals. Read the timecoded Samurai reference study.
4. For footage-led cinematic documentaries, it selects real/archive footage, 2.5D/3D reconstruction, camera paths and motion typography per shot.
5. For explicitly requested H2 Squire/vector historical animation, it selects the separate Squire director and host-controlled H2 Squire specialist.
6. Search `audio-library/generated/preview-catalog.json` and `meta-preview-catalog.json` first; audition OGG candidates, then retrieve the exact hash-verified WAV master for a selected cue. Fetch instrument master collections only as needed.
7. Prototype the hardest moving shot and a 30–60 second picture/sound sample, then scale after human review.
8. Full-length viewing/listening and a timecoded defect log remain required before approval.

The Command Center does not invisibly activate other private plugins. Host-controlled activation is explicit in the router and registries.

## Safety and reproducibility

- The parallel asset-library agent exclusively owns video-library/**, global resource catalogs, downloaders, asset packaging/importers and the Build 76 resource release. Production may read/pull published resources but must not mutate that workstream.
- Inspect the complete changed-file list before PR creation; keep mixed asset/toolchain work separate.
- Do not overwrite master videos; deliver a separately rendered candidate with checksums and visual/audio review.
- Keep production writes, raw licensed audio, voice likeness, model downloads, costs and PR merges behind explicit approval.
- A plugin's existence or source-backed skill does not prove its CLI, weights or runtime are installed. Check pinned versions and actual evidence.
- License boundaries remain per component and per media record. Preserve third-party notices and verify fonts, assets, runtimes, music and sound files separately.

See `references/ILLUSTRATED_HISTORY_MOTION_SYSTEM.md` for the complete shot/motion standard. See SKILL-CATALOG.md and the plugin registries for internal skills and explicit specialist handoffs.
