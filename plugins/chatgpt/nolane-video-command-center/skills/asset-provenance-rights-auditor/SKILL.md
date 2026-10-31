---
name: asset-provenance-rights-auditor
description: Use when selecting or using third-party images, video, audio, fonts, models, checkpoints, custom nodes, templates, code, voice or visual references in a video project.
---
# Asset Provenance and Rights Auditor

## Per-item register
For each selected item, record asset ID, creator/rights holder, source URL, exact version/commit, retrieval date, file checksum, license/permission, attribution requirements, modification, commercial-use status, model/voice consent and the shot in which it is used.

## Status vocabulary
- `ALLOW`: use is supported for the specified output/use.
- `ALLOW_WITH_NOTICE`: use is allowed when required notice/attribution is preserved.
- `RESTRICTED`: allowed only under stated scope or with conditions.
- `UNVERIFIED`: insufficient evidence; do not publish until resolved.
- `BLOCKED`: license or permission prohibits this use.

## Check separately
- Software/code and embedded media are separate licensed works.
- Model package code, weights/checkpoints, training datasets, generated outputs and provider terms are separate.
- Voice synthesis/model access does not grant voice identity rights; cloning a real person requires authorization.
- Fonts, footage, music, SFX, logos, screenshots and public references have distinct terms.
- An open-source license on the repo does not grant rights to customer data, commercial marks or third-party stock media.

## Mandatory project-specific gates
- `video-shotcraft`: Apache-2.0 code; check external/embedded media and attribution files separately.
- `claude-code-video-toolkit`: MIT code; product marks, demo/customer content and voice samples are not automatically cleared.
- `video-talkcraft`: PolyForm Noncommercial 1.0.0 and requires prior written permission for commercial use. Monetized YouTube, sponsorship, client work and paid promotion are commercial unless written permission explicitly covers them. Never port its code/cards/demos/SFX as a workaround.
- `ComfyUI`: GPL-3.0 application; each custom node, model and weight has its own license/terms.
- `Remotion`: tiered special license; confirm the user's commercial eligibility.

## Workflow
1. Review the exact asset and intended use (personal, public, monetized, sponsored, client/commercial).
2. Inspect the applicable license and exact version; preserve notices and source links.
3. Resolve conflicting or unclear terms with a written permission from the rights holder; otherwise substitute a clean-source alternative.
4. Keep license/provenance data with the production project. Do not upload private account data, credentials or private content into public logs.
5. Report blockers before render/publish. Do not downgrade a blocked item to unverified silently.

## Resource workstream boundary
This auditor checks items already selected or referenced for use. It does not own bulk acquisition, downloaders, media catalogue or `video-library/**`; the assigned asset agent owns those paths. Never overwrite or reorganize its work.

## Deliverable
An itemized rights table with status, proof, attribution text, conditions, replacement recommendations and release blockers.
