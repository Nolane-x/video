# Video Studio — current state snapshot

Snapshot updated 2026-10-25 after successful render/archive. Verify live GitHub state and Actions before relying on it.

## Repository
- Repository: https://github.com/Nolane-x/video
- Default branch: `main`
- Root agent contract: `AGENTS.md`
- Persistent skill: `.agents/skills/video-production-master/SKILL.md`

## Canonical art direction
User rejected flat generic SVG/gradient visuals and photo-like AI humans. Preferred: symbolic stick figure (dark round head, pale rim, expressive face, colored shirt, slim limbs) in rich, staged environments; warm windows/practical lamps against plum/charcoal shadows; architecture, props, foreground/background depth, varied camera sizes, visible acting/contact and purposeful edits.

References: [Ifverse Tales](https://www.youtube.com/@IfverseTales), [Day One Films](https://www.youtube.com/@dayonefilmsofficial), and user-provided examples “The Words You Never Forgot” and “What If You Were a Mentalist?”. Read `docs/ART_DIRECTION_IFVERSE_DAYONE.md`.

## Current projects

### Remotion
- Project: `video-projects/remotion`
- Main composition: `src/OneMoreScroll.tsx`
- Root: `src/Root.tsx`
- Story source: `public/story/shots.json`
- Character bible: `public/story/bible.md`
- Procedural audio code: `h2-audio`
- Workflow: `.github/workflows/render-remotion.yml`
- Intended plan: 31 shots × 5 seconds = 155 seconds, 1280×720 at 24 fps with generated music/SFX. Verify live source and latest CI.

### Blender
- Script: `tools/blender/render_h2_stage.py`
- Workflow: `.github/workflows/render-blender-preview.yml`
- Use selectively for shots that benefit from depth/rig/lighting; inspect live workflow status.

### Krita
- Workflow: `tools/krita/README.md`
- Use for hand-authored expression sheets, props, texture and paintovers. It isn't a render dependency unless a workflow invokes it.

### H2 Studio
The full H2 source and its packed skill were used in the prior ChatGPT session but aren't a complete source checkout in this repo. This repository contains the separate Remotion project and procedural audio source. A new agent must locate the actual H2 archive/repository and read its bundled skill before claiming to use the native H2 renderer.

## Previously delivered H2 master (outside Git history)
- File: `one-more-scroll-h2-final.mp4`
- Reported at delivery: about 155 seconds, 1920×1080, 24 fps, H.264 + AAC stereo 48 kHz.
- Audio target reported about -14 LUFS; reported true peak about -2.4 dBFS.
- Related session attachments: 30-second preview, thumbnail, two contact sheets, QA report, source ZIP (~115.9 MB) and source-v2 ZIP (~115.9 MB).
- **Storage truth:** these were delivered as ChatGPT attachments; they are not committed binary files in this repo. Source-v2 includes fixes that had not been verified by a new full render due to local Chromium navigation restrictions. Do not claim those fixes are in the master.
- The exact H2 master SHA-256 is `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, size 31,547,778 bytes. It has been freshly probed in the current workspace, but the binary itself is not yet committed to GitHub. Use `tools/video/archive_h2_master.py` after downloading that exact attachment to import it with checksum validation.
- The repository's Remotion reference render **is now persisted** at `video-library/one-more-scroll/renders/remotion-run-31/one-more-scroll-remotion-master.mp4`. Its SHA-256 is `cba900cebb306acc42fa3f741f7c7d008e9a04400a867a87402dcdf8090ac3e3`. This is a different video/renderer from the H2 master.
- An old chat sandbox path is not a durable GitHub URL.

## Historical CI evidence
Earlier in the conversation:
- Remotion render run 40186281738 succeeded for an earlier 31-shot Remotion version.
- H2 runtime packaging runs 40189690048 and 40189801017 succeeded.
These are historical identifiers, not proof about current HEAD. Check the live Actions page.

## Verified latest state
- Remotion render CI: [run 40197641208](https://github.com/Nolane-x/video/actions/runs/40197641208) — passed schema validation, TypeScript, rendering, audio normalization, metadata and contact-sheet generation.
- Archive CI: [run 40197855575](https://github.com/Nolane-x/video/actions/runs/40197855575) — passed and committed the video plus skill ZIP.
- Permanent Remotion sample: `video-library/one-more-scroll/renders/remotion-run-31/one-more-scroll-remotion-master.mp4`.
- Portable skill bundle: `video-library/video-production-master-skill.zip`, which the new packaging workflow is updating to include the current video and the instructions/source.

## Prior work catalog and reusable archive tooling
- The [previous-work catalog](../video-library/previous-works-catalog.json) records older H2/remotion/cinematic iterations, their exact checksums and whether they are available only in the production workspace or archived in GitHub.
- The prior-works import tool is `tools/video/archive_previous_works.py`. It stages matched video attachments by hash; GitHub workflow then verifies remote bytes and generates contact sheets.
- The H2 source publisher is `tools/video/publish_h2_source_release.ps1`; source ZIPs should be stored as verified GitHub Release assets, not huge regular Git blobs.
- The current portable skill ZIP intentionally includes the Remotion reference video and, after checksum-verified import, the canonical H2 MP4. It does not bundle every historical video clip to avoid exceeding GitHub's single-file size limit. Clone the repo or inspect the catalog for the rest.

## Next priorities
1. Complete the portable skill package workflow and verify the ZIP contains the actual MP4 as well as skill/source docs.
2. Import the exact H2 master binary using `tools/video/archive_h2_master.py` once the attachment is downloaded to a local path, then commit/push the resulting video, checksum and contact sheets.
3. Visually review the persisted Remotion contact sheets and short moving proofs; technical CI passed, but this archive turn did not sign off the video on artistic criteria. Consider an audio-only remaster because measured true peak is -1.2 dBFS, slightly above the conservative -1.5 dBTP target.
4. Re-render and inspect source-v2 with the actual H2 engine when its source/runtime is available; fix P0/P1 action/contact/crop issues.
5. Update state and film manifest after every verified render.


## Latest archived Remotion render — run 36
- MP4: `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`
- Source commit: `e766c5f407cf4bbd175c28d306acc99c6d8aa609`; CI: [40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650).
- SHA-256: `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`; duration 155.100s; 1280x720 at 24/1.
- Audio measurement: -14.5 LUFS integrated; true peak -2.3 dBFS.
- Technical gates passed; contact sheets are available. Do not claim manual visual sign-off unless completed separately.
