# Video Studio — current state snapshot

## Asset library pipeline — 2026-10-30

This workstream is independent of the film render candidates recorded below.

- **Build 48** ([run #48](https://github.com/Nolane-x/video/actions/runs/41037407715), main commit `3d7050f3f0820d4f7daf5c38be449296c3f8b528`) completed its external-resource download step but **failed at ZIP packaging** because two USGS records with the same title generated the same target path: `third-party/usgs/images/aerial-image-of-the-southwest-rift-zone-eruption-of-k-lauea/...jpeg`. It did not publish a release. The follow-up fix in PR #16 adds a stable SHA-256 suffix from each exact USGS item URL to the folder/file slug.
- Build 48 measured results before packaging: **48,588 indexed assets** and **48,954 checksummed files**. Original generated content: 93 backgrounds, 80 overlays, 141 icons, 58 textures, 112 illustrations, 24 verified motion loops, 55 infographics and 196 SFX; 222 stickers, 80 meme templates and 64 caption overlays.
- Build 48 source counts: Kenney GitHub 6 packs; Poly Haven 54 packages / 338 files; ambientCG 122 packages / 981 files; The Met 59 images; Rijksmuseum 240 images; NASA 24 images / 17 videos / 0 audio; Library of Congress 90 images; Wikimedia 687 images / 23 SVG / 28 videos / 0 audio; Openverse 2 items; USGS 80 images / 40 videos / 24 audio; OpenGameArt 108 items / 35,608 files; Google Fonts 20 families / 36 files; OpenMoji 8,990 SVG; NOAA 5 images / 2 videos; Internet Archive 8 videos (663,709,055 bytes). Smithsonian returned 0 due HTTP 429 during that run. These are download/index counts, not a published ZIP size.
- **Last confirmed release remains Build 43:** `video-asset-library.zip` 1,095,394,051 bytes; SHA-256 `a03f02fcd6915361ed64c5ec1d0158837458ac2988adf300de33515b636bbe36`. Build 48 did not publish.
- **Build 49** ([run #49](https://github.com/Nolane-x/video/actions/runs/41048645254), merge commit `4391e74579ee78e13478dc3c0c9e10f1f5566221`) is now running after having queued behind Build 48. It contains the merged LazyTextures bounded public-API CC0 lane and optional Poly Pizza API importer (per-model CC0 only). Its actual download counts, package result and size are not known yet.
- LazyTextures caps: 10 models, 16 materials, 10 HDRIs, 18 texture archives and 8 other packages; 64 MiB per ZIP, 512 MiB total compressed, 128 MiB expanded per package and 1.5 GiB total expanded. Caps are not delivered counts. Poly Pizza is optional via `POLY_PIZZA_API_KEY`; only per-model CC0 1.0 records are accepted, with official HTTPS GLB URLs, GLB v2 validation, no remote sidecar dependencies and per-file SHA-256. Quaternius QAL v1.0 is source-only because current terms prohibit raw library redistribution.
- **Build 50** is in [PR #16](https://github.com/Nolane-x/video/pull/16): rights-filtered Kenney Godot SplashScreens derivative logos plus collision-resistant USGS output paths. The original Godot logo (CC-BY-4.0), Pixel and Pride paths are excluded; only README-confirmed Kenney CC0 Reimagined/Cog/Text derivatives are imported. The namespaced-SVG check validates XML root local-name rather than assuming `<svg>` byte spelling. [CI #108 passed](https://github.com/Nolane-x/video/actions/runs/41053587000) on PR head `10389c2043c2867a7f6d449a93c026b94a77d80e`.
- The asset workflow now uses `cancel-in-progress: false`, so later builds queue instead of cancelling an active three-hour resource build. This worked for Build 49 queuing behind Build 48. PR #16 still needs merge; its next Build 50 should include the USGS collision fix.
- Next: merge PR #16 after verifying the current head/CI; let Build 49 finish and inspect whether its older snapshot hits the USGS collision; Build 50 then reruns with the fix. Verify multi-volume ZIPs, complete manifest coverage, every archive checksum and only then publish measured release sizes/counts.
Snapshot updated 2026-10-28 after the latest First Hour caption-position correction. Current green candidates: **THE WEIGHT OF YES #31**, **ALMOST READY #34**, and **THE FIRST HOUR #55**. First Hour #55 passed all render, audio-mix, ffprobe, loudness and checksum gates; both contact sheets and targeted 1080p B27 frames are now reviewed. Caption fixes are technically verified and visually clear at sampled times. None is approved for final release yet: full-length video and perceptual audio review remain pending. The canonical ONE MORE SCROLL master remains unchanged.

## Current active candidate — THE WEIGHT OF YES
- QA: [manifest](../video-library/the-weight-of-yes/manifest.json), [QA ledger](../video-library/the-weight-of-yes/QA.md).
- Latest render: [run #31 — success](https://github.com/Nolane-x/video/actions/runs/40532086413), source [commit](https://github.com/Nolane-x/video/commit/58c95de849405b0ae5d1636851bb883ffa3870ec).
- Master: 143.000 s, H.264 1920×1080 @24 fps + AAC stereo 48 kHz; SHA-256 `cfc5882636f70e98ace6fc5263c2a60ee2100cf35a2b59351940453242951e9d`.
- Audio: −14.0 LUFS, LRA 9.2 LU, true peak −5.0 dBFS.
- Targeted visual QA: both sheets reviewed; B07 handwritten YES. is inside the page and B19’s boundary caption clears the actors/board. Full-length approval pending.

## Parallel H2 candidates
- **THE FIRST HOUR**: [run #55 — success](https://github.com/Nolane-x/video/actions/runs/40626868973), source [commit](https://github.com/Nolane-x/video/commit/9d86d9a4195982924868468887ff68a2fbcf1790). Master 172.000 s, H.264 1920×1080 @24 fps + AAC stereo 48 kHz; SHA-256 `67171131ab8ab539b82f992651ef6c5b3ce4e70efd91af92292e0da763a5bc6a`; −14.0 LUFS, LRA 6.6 LU, true peak −1.9 dBFS. Both sheets and B27 at 154.5, 157.2, 158.2 and 159.5 s inspected: whisper is below the calendar and fully readable; closing narration is inside the left safe lane. The actual override and post-merge gates are fixed; the downloaded artifact and all 24 checksums passed. Run #55 artifact is temporary and full-length approval remains pending.
- **ALMOST READY**: [run #34 — success](https://github.com/Nolane-x/video/actions/runs/40532086120). 172.000 s; master SHA-256 `aed4367abf31d0373d767856e4412bc96ce6be99a3210cc8e1abb3c0e1fac12a`; −14.1 LUFS, LRA 9.1 LU, true peak −1.8 dBFS. Both contact sheets and selected 1080p B27 frames were inspected; caption beats now have a readable dwell window.
- Green-run outputs are temporary Actions artifacts, not durable release archives. Full-length playback and perceptual listening are still pending for all three films.

## Shared H2 fix pushed to main
- Commit: [`1ab974acc2f8e0b268940fbf16f6b566884dace6`](https://github.com/Nolane-x/video/commit/1ab974acc2f8e0b268940fbf16f6b566884dace6).
- File: `integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit/packs/dem/templates.js`.
- Root cause: scheduled `walk`/`run` keyframe objects were passed to the character rig as numeric gait speeds when the actor was outside an active movement interval, corrupting limbs and occasionally detaching held props at first/last frames.
- Fix: strip scheduled movement descriptors outside active gait windows; three H2 projects rerendered successfully.
- Regression evidence: THE WEIGHT OF YES B08 proof sampled at opening/middle/end; THE FIRST HOUR B19 and ALMOST READY B19 sampled for coherent limbs.

## Caption readability revision — 2026-10-28
- Shared H2 handwritten-temptation renderer now caps the typewriter reveal at 30% of the caption’s hold, so the audience gets time to read the complete line.
- First Hour and Almost Ready source tuners add a regression gate requiring at least 1.2 seconds of full-text readability for temptation overlays, with timing kept inside the shot.
- Full-resolution review of #52/#53 caught two First Hour B27 defects (closing-caption edge clipping and whisper/calendar collision). Root cause: the workflow overwrote the tuner’s `args` with `shot-overrides.json`. The actual override was corrected in `1fc7a4c0e9fae34b2f1847204a63ad3a96e771f2`; post-merge checks were added in `9d86d9a4195982924868468887ff68a2fbcf1790`. Run #55 passed the gate, and targeted frames confirm both caption placement and timing. Full-length playback/perceptual audio review remains a separate gate.
- Preserve the canonical ONE MORE SCROLL master. Green CI is technical evidence, not artistic approval.

## Repository
- Repository: https://github.com/Nolane-x/video
- Default branch: `main`
- Root agent contract: `AGENTS.md`
- Persistent skill: `.agents/skills/video-production-master/SKILL.md`

## Canonical art direction
User rejected flat generic SVG/gradient visuals and photo-like AI humans. Preferred: symbolic stick figure (dark round head, pale rim, expressive face, colored shirt, slim limbs) in rich, staged environments; warm windows/practical lamps against plum/charcoal shadows; architecture, props, foreground/background depth, varied camera sizes, visible acting/contact and purposeful edits.

References: [Ifverse Tales](https://www.youtube.com/@IfverseTales), [Day One Films](https://www.youtube.com/@dayonefilmsofficial), and user-provided examples “The Words You Never Forgot” and “What If You Were a Mentalist?”. Read `docs/ART_DIRECTION_IFVERSE_DAYONE.md`. Their source links and a no-invented-observations study checklist are preserved in [`video-library/reference-clips.json`](../video-library/reference-clips.json).

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

### H2 SelfImprove Studio plugin and source mirror
- **Active private ChatGPT plugin: v1.1.0**, [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0), current release `pluginrel_6ade248942988191a57ff1059c818720`; Plugin Creator confirmed `status=updated` on 2026-10-25.
- GitHub build/validation: [Actions run 40207680206](https://github.com/Nolane-x/video/actions/runs/40207680206) succeeded for source commit `a58ed0a0ca85079435b61ef670fa62531cd7f502`. Plugin ZIP SHA-256: `84993b9eab1d61662cb5859214664b1ac93c1491d9dea6493886df2ab6914917`. [Release result](../integrations/h2-selfimprove-studio-production-overlay/RELEASE-RESULT-v1.1.0.md).
- The source mirror at `integrations/h2-selfimprove-studio/` intentionally preserves 51 UTF-8 files from the v1.0.2 base release (`pluginrel_6ade1c3ecb20819199def25125d2f89a`). The v1.1.0 production addendum/references are in `integrations/h2-selfimprove-studio-production-overlay/`; do not relabel the base manifest as v1.1.0.
- The active private `.plugin` package is managed in Plugin Creator; the canonical H2 master MP4 is now a binary in Git at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`. The H2 renderer source mirror is in GitHub; native rendering still requires the appropriate runtime/dependencies.
- This source is distinct from the Remotion project and from the complete upstream Remotion/Blender/Krita applications.
## Canonical H2 master (archived and verified in GitHub)
- File: `one-more-scroll-h2-final.mp4`
- Reported at delivery: about 155 seconds, 1920×1080, 24 fps, H.264 + AAC stereo 48 kHz.
- Audio target reported about -14 LUFS; reported true peak about -2.4 dBFS.
- Related session attachments: 30-second preview, thumbnail, two contact sheets, QA report, source ZIP (~115.9 MB) and source-v2 ZIP (~115.9 MB).
- **Storage truth:** the canonical H2 master is archived in Git and the original source plus source-v2 ZIPs are archived as verified [GitHub Release assets](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). Source-v2 has now been rendered fully and passed technical stream validation; candidate MP4, SHA-256, report and review bundle are recorded in `video-library/one-more-scroll/h2-source-release.json`. It remains a separate candidate until a human reviews the entire moving picture with audio and gives explicit artistic sign-off.
- Exact H2 master: `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, 31,547,778 bytes. GitHub Actions verified its SHA, codec, dimensions, FPS, duration and audio format in [run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143).
- The current Remotion reference render is `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`, SHA-256 `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`. This is a different video/renderer from the H2 master.
- An old chat sandbox path is not a durable GitHub URL.

## Historical CI evidence
Earlier in the conversation:
- Remotion render run 40186281738 succeeded for an earlier 31-shot Remotion version.
- H2 runtime packaging runs 40189690048 and 40189801017 succeeded.
These are historical identifiers, not proof about current HEAD. Check the live Actions page.

## Historical verified state — ONE MORE SCROLL source-v3
- **H2 source-v3 full render and Release packaging passed:** [workflow run 40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324), all required steps successful, including the previously failing review-bundle checksum/publish step.
- Candidate: [source-v3 H2 MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v3-shoelace-fix-candidate.mp4), SHA-256 `761d238ae019e6c39eca3a9c46bff88b02f6f96e332f35d6e5d6b0d41e29310f`, 33,409,690 bytes. Review ZIP: [source-v3 review package](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v3-shoelace-fix-review.zip), SHA-256 `56bf506a0ec63fbb9d99256ac1cc989186f6ddab12056c9cfb9f012b922d0745`, 33,709,840 bytes.
- Verified streams: 155.000s, 1920×1080 @24fps, H.264 + AAC stereo 48 kHz. EBU R128: −14.0 LUFS integrated, 6.9 LU LRA, −2.4 dBFS true peak.
- First attempt [40281627022](https://github.com/Nolane-x/video/actions/runs/40281627022) passed rendering/audio but omitted the pinned patch script from the review payload. The corrected workflow copies the patch before checksum generation, verifies required files and uploads the candidate/review assets separately.
- Portable skill package last passed in [run 40287442899](https://github.com/Nolane-x/video/actions/runs/40287442899): ZIP integrity, 176 entries, Remotion run-36 sample, canonical H2 master, H2 production overlay and plugin v1.1.0 all verified. That build's sidecar SHA-256 was `cf6257467655f73fedd715cf5ce2380c73aa30b855df1b6ae6605945d67f8635`; this manifest/docs change triggers a fresh package build, so recheck the newest run and sidecar.
- Canonical H2 master remains unchanged: `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`. Source-v2 and source-v3 are separate non-canonical candidates.
- Source-v3 is a **technical pass, not artistic sign-off**. I sampled the shot-b17 motion at 4 fps around 80–84 seconds: the forward crouch and alternating arm motion are visible, but the hand-to-shoe/lace contact remains ambiguous because the actor is too small in the wide shot. Treat this as a P1 visual defect. Next: build a source-v4 3–6 second focused preview with clearer composition and actual hand/lace contact; review that preview before any new full render. Full candidate playback with audio, pacing, transitions, sync and emotional arc still require review.

## Next priorities
1. Watch THE WEIGHT OF YES in full with audio, verifying pacing, transitions, captions, character acting, prop contacts and emotional arc.
2. Perform equivalent full-length audio/video reviews for THE FIRST HOUR and ALMOST READY; do not infer artistic approval from green CI.
3. After explicit sign-off, publish approved master and review ZIP to durable GitHub Release storage, verify remote URLs/checksums and update manifests. Actions artifacts expire.
4. Keep the ONE MORE SCROLL source-v4 shoe-tie/contact fix as a separate backlog item; do not replace the canonical master without full-motion review.

## Prior work catalog and reusable archive tooling
- The [previous-work catalog](../video-library/previous-works-catalog.json) records older H2/remotion/cinematic iterations, their exact checksums and whether they are available only in the production workspace or archived in GitHub.
- The prior-works import tool is `tools/video/archive_previous_works.py`. It stages matched video attachments by hash; GitHub workflow then verifies remote bytes and generates contact sheets.
- The H2 source publisher is `tools/video/publish_h2_source_release.ps1`; source ZIPs should be stored as verified GitHub Release assets, not huge regular Git blobs.
- The current portable skill ZIP includes both the Remotion reference MP4 and the checksum-verified canonical H2 MP4. It also includes `video-library/reference-clips.json`, which preserves your two reference-video URLs and study prompts; standalone copies of those third-party MP4s were not found in the current workspace/Library and are not embedded. It does not bundle every historical clip; use the catalog for availability and provenance.

## Historical H2 source-v2 render candidate
- Workflow: [40276064292](https://github.com/Nolane-x/video/actions/runs/40276064292) — full 155-second render, audio mix, stream validation and Release upload passed.
- Candidate: [download MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v2-render-candidate.mp4); review bundle: [ZIP](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v2-render-review.zip).
- SHA-256: `5f72e611c1257a4b31fa834c4b8d5481a8404b6becb50f41df7663cd2f7c96b7`; size 33,396,438 bytes; 155.000s; 1920×1080 @24fps; H.264 + AAC stereo 48 kHz.
- This is a technically validated candidate. Artistic approval remains open after contact-sheet sampling; full playback with audio and moving-action review are still needed.

## Latest archived Remotion render — run 36
- MP4: `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`
- Source commit: `e766c5f407cf4bbd175c28d306acc99c6d8aa609`; CI: [40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650).
- SHA-256: `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`; duration 155.100s; 1280x720 at 24/1.
- Audio measurement: -14.5 LUFS integrated; true peak -2.3 dBFS.
- Technical gates passed; contact sheets are available. Do not claim manual visual sign-off unless completed separately.



## Historical ALMOST READY candidate — run #14 technical pass
- Manifest: [video-library/almost-ready/manifest.json](../video-library/almost-ready/manifest.json); QA: [video-library/almost-ready/QA.md](../video-library/almost-ready/QA.md).
- Script: [01-PHIM-the-almost-ready.txt](../video-projects/h2-selfimprove/01-PHIM-the-almost-ready.txt); art-direction: [tune_story.py](../video-projects/h2-selfimprove/almost-ready/tune_story.py).
- Latest native H2 render: [run #14](https://github.com/Nolane-x/video/actions/runs/40429993482), all steps successful. 172.000 s, H.264 1920×1080 @24 fps + AAC 48 kHz stereo; −14.0 LUFS, −1.9 dBFS true peak.
- B19 turning-action sample shows coherent limbs during motion. Full contact-sheet review and full-length video/audio watch remain pending; the artifact expires 2026-11-26T01:05:34Z.
- Keep it separate from THE FIRST HOUR, THE WEIGHT OF YES and canonical ONE MORE SCROLL.
