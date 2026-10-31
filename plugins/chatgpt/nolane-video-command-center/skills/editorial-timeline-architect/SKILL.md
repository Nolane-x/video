---
name: editorial-timeline-architect
description: Use when building, converting or validating a video edit timeline, EDL, FCPXML, OTIO project or cross-engine editorial handoff.
---
# Editorial Timeline Architect

## Core concepts
OpenTimelineIO (OTIO) stores editorial cut information, time ranges, tracks and references to external media. It is not a video/audio media container and does not copy source footage into the timeline automatically. Adapters for NLE formats have their own availability and licensing.

## Workflow
1. Record project frame rate/timebase, resolution, aspect ratio, audio sample rate, track naming and color-space assumptions.
2. Keep a stable source manifest: source path/URI, checksum, media duration, stream metadata, frame rate and source timecode.
3. Build OTIO tracks with explicit clips, gaps, transitions, source ranges and global timeline ranges; avoid converting frame-based time into rounded decimal seconds without preserving rational rates.
4. Resolve media references relative to a known project root and validate missing/offline media before export.
5. Convert to supported interchange formats only after checking exact adapter support; do not promise round-trip fidelity for unsupported effects, fonts, speed changes, color effects or NLE-specific metadata.
6. Create review proxies/contact sheets without changing source masters.
7. Reopen the exported timeline and compare clip boundaries, order, durations and audio sync against the source edit.

## Engine interoperability
Use Remotion/HyperFrames for deterministic web/video rendering. Use OTIO as the edit interchange contract for supported downstream NLEs. Keep source-media files external and preserve unique stable IDs.

## Deliverables
OTIO timeline, source manifest, adapter/version record, proxy/contact sheets, timeline validation report and known round-trip limitations.
