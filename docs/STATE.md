# Video Studio — current state snapshot

Snapshot authored 2026-10-25. Verify live GitHub state and Actions before relying on it.

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
- An old chat sandbox path is not a durable GitHub URL.

## Historical CI evidence
Earlier in the conversation:
- Remotion render run 40186281738 succeeded for an earlier 31-shot Remotion version.
- H2 runtime packaging runs 40189690048 and 40189801017 succeeded.
These are historical identifiers, not proof about current HEAD. Check the live Actions page.

## Next priorities
1. Verify current Remotion source and latest CI after skill/state additions.
2. Archive a reproducible Remotion output plus skill ZIP as permanent GitHub Release assets using the archive workflow; triggering render commit must include `[archive-video]`.
3. Add the exact original H2 MP4 to durable GitHub storage via a supported binary upload path. Do not confuse it with the Remotion release asset.
4. Re-render and inspect source-v2 with the actual H2 engine when its source/runtime is available; fix P0/P1 action/contact/crop issues.
5. Update state and film manifest after every verified render.
