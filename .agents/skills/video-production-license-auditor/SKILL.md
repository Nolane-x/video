---
name: video-production-license-auditor
description: Use when selecting, downloading, vendoring, installing, redistributing or commercially publishing code, fonts, models, effects, footage, audio or presets in the video toolchain.
---
# Video Production License Auditor

## Review each exact version
Record package/repo, version or commit, source URL, SPDX/license label, copyright holder, redistribution terms, attribution needs, model-weight terms, restrictions and checksum.

## Important cases
- Remotion has a tiered special license. Some individual, small or non-profit usage qualifies for a free tier; some larger for-profit organizations need a company license. Check current terms for the legal entity.
- Theatre Core is Apache-2.0; Theatre Studio is AGPL-3.0. Keep Studio out of production bundle by default.
- resvg-js is MPL-2.0. Preserve notices and comply with modified-file source obligations.
- Blender is GPL-3.0-or-later. Respect redistribution and add-on licensing.
- FFmpeg's effective license depends on build flags/codecs; record ffmpeg -buildconf.
- An npm package license does not license separate fonts, models, footage, audio, plugins or model weights.

## Required outcome
Produce allow / allow-with-notice / restricted / blocked. Never weaken a license gate to finish a build. Reject non-commercial-only resources for monetized/commercial deliverables unless permission is documented.
