# Video Studio — current state snapshot

## Asset library pipeline — 2026-10-30

This workstream is independent of the film render candidates recorded below.

- **Build 48** ([run #48](https://github.com/Nolane-x/video/actions/runs/41037407715), main commit `3d7050f3f0820d4f7daf5c38be449296c3f8b528`) completed external-source downloads but **failed at ZIP packaging** because two USGS records with the same title generated the same target path. It did not publish a release. PR #16 fixes this by appending a stable SHA-256 suffix from each exact USGS item-page URL to the output folder/file slug.
- Build 48 measured results before packaging: **48,588 indexed assets** and **48,954 checksummed files**. Generated content: 93 backgrounds, 80 overlays, 141 icons, 58 textures, 112 illustrations, 24 verified motion loops, 55 infographics, 196 SFX, 222 stickers, 80 meme templates and 64 caption overlays.
- Build 48 external-source results: Kenney GitHub 6 packs; Poly Haven 54 packages / 338 files; ambientCG 122 packages / 981 files; The Met 59 images; Rijksmuseum 240 images; NASA 24 images / 17 videos / 0 audio; Library of Congress 90 images; Wikimedia 687 images / 23 SVG / 28 videos / 0 audio; Openverse 2 items; USGS 80 images / 40 videos / 24 audio; OpenGameArt 108 items / 35,608 files; Google Fonts 20 families / 36 files; OpenMoji 8,990 SVG; NOAA 5 images / 2 videos; Internet Archive 8 videos (663,709,055 bytes). Smithsonian returned 0 after HTTP 429 responses. These are actual download/index counts, not a published archive size.
- **Last confirmed release remains Build 43:** `video-asset-library.zip` 1,095,394,051 bytes; SHA-256 `a03f02fcd6915361ed64c5ec1d0158837458ac2988adf300de33515b636bbe36`. Build 48 did not publish.
- **PR #15 / Build 49 is merged** at `4391e74579ee78e13478dc3c0c9e10f1f5566221`. [Build 49 run #49](https://github.com/Nolane-x/video/actions/runs/41048645254) is in progress at the resource-download step. It includes LazyTextures five-category bounded CC0 API ingestion and optional Poly Pizza API ingestion that accepts exact per-model CC0 1.0 only, validates GLB v2, rejects remote/sidecar dependencies and records SHA-256. The Poly Pizza lane is skipped unless `POLY_PIZZA_API_KEY` is configured.
- LazyTextures caps: 10 models, 16 materials, 10 HDRIs, 18 texture archives and 8 other packages; 64 MiB per ZIP, 512 MiB total compressed, 128 MiB expanded per package and 1.5 GiB expanded total. Poly Pizza caps: 48 models, 128 MiB each, 4 GiB aggregate. These are ceilings, not downloaded counts. Current Quaternius QAL v1.0 remains source-only because it prohibits raw asset-library redistribution.
- **PR #16 / Build 50 is merged** at `283a082587b28459737e25c805da784915d7a4f8`. It adds the rights-filtered Kenney Godot SplashScreens CC0 subset (Reimagined/Cog/Text derivatives only; original Godot CC-BY-4.0, Pixel and Pride excluded), accepts correctly namespaced sanitized SVG roots, and fixes USGS same-title output collisions. [CI #109 passed](https://github.com/Nolane-x/video/actions/runs/41054098329) on the final PR head. [Build 50 run #50](https://github.com/Nolane-x/video/actions/runs/41054395607) is pending behind Build 49.
- The workflow uses `cancel-in-progress: false`. This was verified: Build 49 queued after Build 48 finished; Build 50 then queued behind Build 49. Do not cancel either active build merely because a later run is pending.
- Next: inspect Build 49 download counts and whether its pre-USGS-fix snapshot fails at packaging; then inspect Build 50, which contains the USGS path fix. Require multi-volume ZIP integrity, full extraction coverage, SHA-256 and release metadata before claiming a new downloadable release.

- **2026-10-30 live follow-up:** PR [#17](https://github.com/Nolane-x/video/pull/17) (branch `fix/smithsonian-open-access-backoff`) adds finite Smithsonian HTTP 429/transient-error retries, `Retry-After`/rate-limit-reset handling, one-second query pacing and a stop condition after persistent 429. Its strict record-level + exact-media CC0 gate is unchanged. PR validation run [#110](https://github.com/Nolane-x/video/actions/runs/41059088369): Python compilation and offline source-rights tests have passed; generated-asset smoke build was still running at the last check. PR merged to main at commit [b0635e2](https://github.com/Nolane-x/video/commit/b0635e21dd0d66e42d0ef98846ba245dd5203801). Builds 49/50 were already launched or queued from earlier source commits and do not contain this patch; later builds from main will use the updated importer.
- At the same check, Build 49 [run #49](https://github.com/Nolane-x/video/actions/runs/41048645254) remained in the resource-download step after compile/offline tests passed; Build 50 [run #50](https://github.com/Nolane-x/video/actions/runs/41054395607) had not started and remained queued behind it. No new asset-library release or artifact was confirmed. Keep both runs intact; inspect the final bundle manifest, all ZIP checksums and exact file coverage before publishing any size/count claim.
- The asset workflow maps the repository secret `SMITHSONIAN_API_KEY` into the importer. If this secret is absent, the importer currently falls back to `DEMO_KEY`; add a dedicated Actions secret for higher-volume future runs, and never commit the key.
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


## Distributed 50 GB asset-library pipeline — 2026-10-30

- PR [#18](https://github.com/Nolane-x/video/pull/18) merged to `main` at commit [`6a44c974`](https://github.com/Nolane-x/video/commit/6a44c974ba4be413a5b5006a720a5db5ee8e1b69). It replaces the single serial source-download job with 22 independent lanes (original assets + 21 providers), up to 16 simultaneous GitHub-hosted runners.
- Latest PR validation [run #131](https://github.com/Nolane-x/video/actions/runs/41066218856) passed: Python compilation, the full offline rights/source regression suite, and generated-asset smoke build.
- New distributed workflow [Build #52](https://github.com/Nolane-x/video/actions/runs/41066528335) was created on the merge commit. At this snapshot it is **queued**; the source jobs were created but no asset volume has yet been confirmed uploaded by this run.
- Source sharder: `tools/video/build_asset_library_shard.py`. Each lane runs its existing source importer, requires a license and `redistributable: true` for every indexed asset, validates paths/bytes/SHA-256, packages independent category volumes under 1.7 GB uncompressed, uploads directly into a unique draft Release, and deletes local copies only after successful upload. Failed uploads preserve raw files; reruns can overwrite same-name assets.
- Finalizer: `tools/video/finalize_asset_library_release.py`. Merges all 22 manifests, rejects duplicate asset IDs/paths and incomplete volume coverage, builds the global offline catalog/index/license ledger/checksum list, then verifies exact Release asset names, sizes and GitHub-computed SHA-256 digests before publishing.
- Poly Haven lane now has an 8 GiB aggregate download ceiling so a large model/texture selection does not exceed a standard runner's 14 GB SSD. Matrix concurrency is limited to 16 to remain within standard GitHub Actions concurrency.
- The new workflow uses concurrency group `video-asset-library-distributed-v2` so it is not blocked behind the legacy serial build queue.
- 50 GB is defined as **50,000,000,000 actual indexed media bytes**. The finalizer reports the exact measured value and never rounds a partial build up to 50 GB.
- Legacy state at the time of merge: Build 49 [run](https://github.com/Nolane-x/video/actions/runs/41048645254) remained in progress in the old serial download step; Build 50 [run](https://github.com/Nolane-x/video/actions/runs/41054395607) was cancelled; Build 51 [run](https://github.com/Nolane-x/video/actions/runs/41059475106) remained pending behind the old queue. Do not count any of these as a completed release.
- Last confirmed published library remains Build 43 at 1,095,394,051 bytes. **No new 50 GB release has been published yet.** Next: inspect Build 52's 22 lane jobs as runners become available; use actual per-lane byte counts and upload status to improve any slow/failing importer. Only announce 50 GB once the final Release and its remote digests are verified.


## Asset-library sprint update — 2026-10-30 evening

- CI #143 [passed](https://github.com/Nolane-x/video/actions/runs/41080103431) on main SHA `37fa3edaeab6cdbe992c754faac862ed9e779d4c`. It includes the expanded Poly Haven / ambientCG caps, new NASA and Wikimedia search coverage, source-ID fixes, and expanded offline test expectations.
- Build 62 [run](https://github.com/Nolane-x/video/actions/runs/41078978167) is still in progress at this snapshot. Its draft Release currently contains 39 ZIP volumes totaling **8,154,719,650 compressed bytes**, with 21 of 22 source shard manifests uploaded. The USGS shard is the only remaining source lane; finalizer and publication have not run yet.
- The 21 completed shard manifests/log summaries account for **8,691,066,675 indexed resource bytes** (decimal 8.691 GB) before USGS. This is measured from the `indexed_resource_bytes` summary in each completed lane, not inferred from ZIP size.
- Largest completed contributors in Build 62: NASA 2,030,638,116 bytes (47 assets); NOAA Ocean Exploration 1,962,159,985 bytes (340 assets); OpenGameArt 1,434,785,584 bytes (42,030 indexed files); Internet Archive 1,092,253,646 bytes (11 videos); ambientCG 869,348,271 bytes (1,241 files); Wikimedia Commons 517,246,544 bytes (660 images); Poly Haven 384,999,485 bytes (338 assets).
- Other Build 62 indexed contributions: original assets 48,483,095 bytes; Kenney 15,574,258; Kenney Splash 1,487,986; Met 6,409,505; Rijksmuseum 55,225,720; OpenMoji 23,888,144; Wikimedia audio/video 185,955,412; Wikimedia SVG 5,799,922; Google Fonts 25,394,876; LOC 31,416,126. Poly Pizza, LazyTextures, Openverse and Smithsonian produced 0 resource bytes in this run.
- USGS source IDs now use the exact source URL hash rather than a truncated page slug, preventing similar-titled source pages from colliding. NOAA item IDs and filenames also include a source-URL hash.
- Smithsonian rate-limit handling now stops rather than retrying before a provider-requested wait longer than 30 seconds; this avoids tying up a runner for ten minutes only to receive another 429.
- New source coverage: NASA query list expanded by 45 topic searches (still bounded to 8 GiB aggregate); Wikimedia Commons search scope expanded by 50 topics, with a strict 8 GiB byte ceiling; Wikimedia image ceiling 1,600; Internet Archive searches 5 pages × 100 and up to 220 item pages per collection; OpenGameArt category caps 60/60/48/36/36, 10 search pages and up to 120 item pages per category, with its 8 GiB ceiling.
- CC0 material intake: ambientCG caps are now 792 total category selections (Material 240, HDRI 64, 3DModel 80, Decal 64, Atlas 64, PlainTexture 120, Brush 80, Substance 80), with 8 GiB aggregate extraction ceiling. Poly Haven caps are 120 HDRIs / 180 models / 480 textures, with 8 GiB aggregate limit.
- Source matrix concurrency is now 18, leaving headroom within the GitHub Free standard-runner account limit of 20 for validation / packaging jobs. Workflow file: `.github/workflows/build-video-asset-library.yml`.
- Build 68 [run](https://github.com/Nolane-x/video/actions/runs/41080103332) is queued and will use these latest caps/concurrency once Build 62 leaves the distributed-build concurrency group. Older queued Build 65–67 attempts were superseded before their source matrices began.
- DVIDS was investigated as a possible public-media lane but is not integrated: API access requires a user API key, and the item-level copyright / privacy / publicity / non-endorsement terms need stricter verification than the current API search payload alone provides.
- **The 50 GB target has not been reached or published.** Do not count compressed bytes, configured caps or unverified sources as target progress. Next: allow Build 62 USGS to finish, verify its manifest and Release SHA-256s, then inspect Build 68's actual per-lane indexed byte counts and improve the largest yielding lanes.

## Build 62 recovery and published baseline — 2026-10-31

- Build 62 source run: [41078978167](https://github.com/Nolane-x/video/actions/runs/41078978167). All 22 source lanes completed and produced 44 ZIP volumes plus 22 shard manifests.
- The original finalizer attempt failed only at its lookup of a draft release by tag. The source shards and 7 global metadata files were already uploaded; no media had to be downloaded again.
- Fixed tools/video/finalize_asset_library_release.py to resolve draft/published releases using the release collection (GET /repos/{owner}/{repo}/releases?per_page=100) and added regression tests for draft selection / missing tags. This avoids the integration-context failure from the by-tag draft endpoint.
- Recovery workflow: [run 41149796885](https://github.com/Nolane-x/video/actions/runs/41149796885) — **success**. It downloaded the 22 existing manifests, rebuilt the global index/catalog/license ledger/checksum files, verified all remote Release asset names, sizes and GitHub SHA-256 digests, and published the draft.
- Published Release: https://github.com/Nolane-x/video/releases/tag/video-asset-library-build-41078978167. Release is no longer a draft and contains **73 assets**: 44 volumes, 22 shard manifests and 7 global metadata files.
- Final measured library size: **12,303,303,941 indexed resource bytes** (12.303 GB decimal / 11.458 GiB), **55,700 indexed assets**, **44 download volumes**. The 50,000,000,000-byte target remains incomplete; progress = 24.606%.
- Total compressed size of the 44 ZIP volumes: **11,677,924,120 bytes**. This is not the target metric; use indexed resource bytes only.
- Highest-yield lanes: USGS 3,612,237,266 bytes / 196 assets; NASA 2,030,638,116 / 47; NOAA 1,962,159,985 / 340; OpenGameArt 1,434,785,584 / 42,030; Internet Archive 1,092,253,646 / 11; ambientCG 869,348,271 / 1,241; Wikimedia 517,246,544 / 660; Poly Haven 384,999,485 / 338. Other lanes add the remaining bytes; exact aggregate is authoritative in ASSET_INDEX.json.
- The next full library build is deliberately gated by .github/ASSET_LIBRARY_BUILD_REQUEST; code edits and documentation no longer relaunch a full 22-lane download. The build workflow uses group video-asset-library-distributed-v4, job-level contents: write permissions, and max-parallel: 18.
- Recovery-specific workflow: .github/workflows/recover-video-asset-library-release.yml; future recovery runs can republish already-uploaded draft assets without re-running the source matrix.
- Next build should use the latest caps on main. Measure its actual per-lane bytes and compare against Build 62 via SHA-256 / asset IDs before counting cumulative library growth. Do not simply add repeated downloads as unique assets. After another incremental build, produce a cumulative index across published releases using content hashes to deduplicate.


## NASA SVS production asset lane — 2026-10-31

- Branch: `feature/nasa-svs-asset-library-lane`; implementation adds a dedicated `nasa-svs` shard using the official NASA Scientific Visualization Studio Search and Page APIs.
- The metadata-only probe inspected 40/40 pages and found 206 movie items but zero allowlisted videos because NASA's API emitted official `http://svs.gsfc.nasa.gov/vis/...` links while the probe required HTTPS. The corrected policy upgrades only the exact official host/path to HTTPS and rejects credentials, alternate hosts, ports, query/fragment URLs and non-`/vis/` paths.
- The importer searches 17 science-topic areas and requests at most 170 visualization pages; it indexes at most 36 videos, 300 MiB per file and 4 GiB per lane build. It selects one best-resolution video per complete SVS page, verifies final URL, MIME, container signature and SHA-256, and preserves credits, datasets, categories, missions, keywords, dates, dimensions and source URLs.
- Rights: NASA SVS says its visualizations are public domain unless otherwise noted. It specifically says licensed-music visualizations may be reused without their audio tracks. This importer conservatively skips page-level music/copyright/permission notes and non-empty `audio_track` metadata rather than copying uncertain soundtracks. Assets are labelled NASA SVS Public Domain default, not CC0.
- The source is wired into the builder, shard registry, distributed matrix and `sources.json`. This branch does not edit `.github/ASSET_LIBRARY_BUILD_REQUEST`, so code review will not relaunch the large distributed library build.
- Validation is pending CI on this branch. Do not count additional bytes toward 50 GB until the new shard completes, the release finalizer verifies remote hashes and the cumulative index deduplicates by SHA-256.
- Official sources: https://svs.gsfc.nasa.gov/help/ and https://www.nasa.gov/nasa-brand-center/images-and-media/.

## NASA SVS lane merged and Build 70 queued — 2026-10-31

- PR [#19](https://github.com/Nolane-x/video/pull/19) was merged by squash at `e69715989daa6467ce170d5f7d4e8776a00bba5f` after validation [run #177](https://github.com/Nolane-x/video/actions/runs/41155520706) passed. The run compiled the changed Python modules, passed the offline rights/asset regression suite, and completed the generated original-family FFmpeg smoke build.
- Main now contains the NASA SVS video importer, source registry and metadata catalog entry, `nasa-svs` sharder/matrix lane, redirect-safe HTTPS enforcement, per-file/container/hash checks, creator/dataset provenance, and the source/rights tests.
- The distributed asset workflow now has **23 source lanes including originals**. The finalizer's expected manifest count is derived from `build_asset_library_shard.SOURCE_LANES` instead of a hard-coded 22, and a regression test asserts that the workflow matrix exactly matches the registered lanes.
- Build 69 [run](https://github.com/Nolane-x/video/actions/runs/41149972764) is still in progress on the USGS shard. Its Release remains a draft; at the latest check it held 44 ZIP volumes and 22 shard manifests, about 14.998 GB compressed. This is not a verified published library size and must not be counted toward the 50 GB indexed-resource target.
- Build 70 [run](https://github.com/Nolane-x/video/actions/runs/41155773940) was queued after the merge and is waiting behind Build 69 in the non-cancelling distributed-build concurrency group. It will use the merged 23-lane matrix including NASA SVS.
- NASA SVS limits: 17 science-topic searches, up to 170 page inspections, at most 36 downloaded videos, 300 MiB per file and 4 GiB total. The importer only downloads complete SVS visualizations; accepts exact-host `/vis/` media after HTTPS normalization; rejects redirects that downgrade to HTTP or leave the exact resource; screens page/item music and rights notes; skips non-empty audio-track metadata; and retains attribution, data sets, dimensions, dates, keywords, item URL, file URL and SHA-256. NASA SVS media is labelled Public Domain under its own default, not CC0.
- Do not count NASA SVS bytes until Build 70's `nasa-svs` shard completes, the 23 manifests are merged, every uploaded Release asset and checksum is verified, and the Release is published. After publication, update the cumulative SHA-256 index using all published releases so byte-identical resources are counted only once.
