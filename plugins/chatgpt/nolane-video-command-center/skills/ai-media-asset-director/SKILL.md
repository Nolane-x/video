---
name: ai-media-asset-director
description: Use when planning or producing AI-generated images, video clips, voice-over, music, sound effects, thumbnails or other synthetic media for a video.
---
# AI Media Asset Director

## Mission
Choose the smallest suitable media-generation workflow for a shot. Treat generation as a controlled production stage—not an invitation to run every model or service.

## Before execution
1. Identify the shot's visual/audio purpose, duration, aspect ratio, resolution, FPS, motion requirements, continuity constraints and exact text that must remain editable.
2. Select modality: still image, image edit, image-to-video, text-to-video, TTS, music, SFX, stem separation or deterministic vector/3D rendering.
3. Compare the user's existing tools and authorized endpoints before proposing a new provider. Record model/provider/version, hardware, disk, latency, cost, rate limits, data retention and terms.
4. Ask for explicit approval before any paid API request, cloud GPU provisioning, metered generation, voice cloning, model-weight download or checkpoint installation.
5. Do not download assets into `video-library/**` or start the resource-library workflow. That path is owned by the parallel resource agent; this skill only specifies the production use and review requirements.

## Generation contract
- Keep exact titles, UI, logos, charts, figures, numbers and captions as editable overlays in Remotion/HyperFrames; do not trust generated pixels for exact typography.
- Use deterministic seeds/settings when supported. Generate controlled variants and compare them against the art bible rather than accepting the first take.
- For video, inspect every frame range for identity drift, geometry warping, malformed anatomy, flicker, motion discontinuity, hallucinated text, unwanted marks and temporal instability.
- For audio, verify pronunciation, pauses, voice consent, duration, clipping, sample rate and alignment to the approved script.
- Preserve originals and prompts. Record prompt, negative prompt if supported, seed, workflow, model version, provider, output dimensions/FPS/duration, checksum, source path and review status.
- Do not remove watermarks to disguise ownership, imitate real people without authorization or generate copyrighted-character imitations on request.

## Deliverables
Shot-to-model routing table, cost/permission gate, versioned prompts/settings, candidate comparison, selected media manifest and rejection notes. No provider run is claimed until a returned asset or run record confirms it.
