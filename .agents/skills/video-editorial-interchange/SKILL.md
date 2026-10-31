---
name: video-editorial-interchange
description: Use when creating interoperable edit timelines, scene lists, shot logs, source clip references or review proxies with OTIO and PySceneDetect.
---
# Editorial Interchange Engineer

- Use OpenTimelineIO for timeline structure, tracks, clip ranges and external media references; it is not a media container.
- Use PySceneDetect headless for scene/cut candidates, then inspect and correct false positives caused by flashes, overlays, camera movement and fades.
- Store exact rational frame rates and source in/out ranges; avoid lossy decimal-second conversions.
- Keep source URI, checksum, duration, stream metadata and timecode in the source manifest.
- Do not duplicate, move or alter the asset workstream's video-library contents; store cut metadata and analysis only.
- Validate exported OTIO by reopening it and comparing clip order, timing, source ranges and known adapter limitations.
