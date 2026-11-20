# Video Studio — current state snapshot

## Verified asset-library state — 50 GB target reached (2026-10-31)

- **The global unique-resource target is complete.** The SHA-256-deduplicated cumulative index reports **53,975,967,320 unique resource bytes (53.976 GB decimal / 50.260 GiB)** across **9 published asset-library Releases** — **107.95%** of the exact 50,000,000,000-byte goal, exceeding it by **3,975,967,320 bytes (3.976 GB)**.
- The cumulative index counts **47,519 unique resources** after deduplicating identical resource bytes across releases. It records 571,731 release-origin occurrences and removes 524,212 repeated occurrences; the summed per-release resource total before deduplication is 264,031,249,154 bytes. Repeated copies never count again toward the target.
- Cumulative SHA-256 workflow [run #3](https://github.com/Nolane-x/video/actions/runs/41189496556) completed successfully. It validated all 9 requested published Release tags, downloaded their indexes/manifests, merged provenance, deduplicated exact resource bytes, and uploaded the cumulative index/download map to the latest Release.
- Latest source build is **Build 76**, not Build 77: [Actions run #76](https://github.com/Nolane-x/video/actions/runs/41184526545) completed successfully and published the [Build 76 Release](https://github.com/Nolane-x/video/releases/tag/video-asset-library-build-41184526545). Its individual per-release index contains **48,788,442,684 bytes**, **64,828 indexed resource records** and **66 ZIP volumes**; the finalizer validated the release assets and remote SHA-256 values before publication.
- The Build 76 Release now also contains [CUMULATIVE_ASSET_INDEX.json](https://github.com/Nolane-x/video/releases/download/video-asset-library-build-41184526545/CUMULATIVE_ASSET_INDEX.json) and [CUMULATIVE_ASSET_DOWNLOADS.json](https://github.com/Nolane-x/video/releases/download/video-asset-library-build-41184526545/CUMULATIVE_ASSET_DOWNLOADS.json). The index is the authoritative content-addressed record; the downloads file maps resources to the Release ZIP volumes containing them.
- Build 76's important additions were NASA SVS (9,422,982,075 indexed bytes / 90 silent videos), ESO (9,513,714,763 bytes / 42 silent videos), NASA (4,360,279,993 bytes / 102 resources), NOAA Ocean Exploration (3,904,839,727 bytes / 491 resources), NPS B-roll (4,177,273,822 bytes / 31 videos), NPS NPGallery photography (1,726,488,088 bytes / 229 photos) and USGS (913,394,519 bytes / 71 resources). All registered source-lane jobs completed successfully; source-specific rights, attribution, official-host, file-signature, size and SHA-256 checks remain in force.
- **Do not queue Build 77 merely to increase the byte count.** The 50 GB target has already been exceeded after global SHA-256 deduplication. Keep the current Releases intact; future asset work should focus on a specific missing media category or demonstrable quality gap, not repeated downloads. Keep all existing per-item redistribution and provenance checks strict. The toolchain workstream remains separate.

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
- Build 69 [run](https://github.com/Nolane-x/video/actions/runs/41149972764) completed successfully. Its [published Release](https://github.com/Nolane-x/video/releases/tag/video-asset-library-build-41149972764) contains 73 assets: 44 ZIP volumes, 22 shard manifests and 7 global metadata files. The finalizer reports **15,825,356,549 indexed resource bytes (15.825 GB decimal)** and **64,485 indexed assets**; total compressed ZIP bytes are 14,997,640,229. The 50 GB target remains incomplete. Use indexed resource bytes, not compressed archive bytes.
- Build 70 [run](https://github.com/Nolane-x/video/actions/runs/41155773940) is now running on the merged 23-lane matrix. At the latest check, **22/23 source shards have completed successfully**; only USGS remains in progress. The release is still a draft until finalization verifies every manifest, ZIP, byte count and GitHub SHA-256 digest.
- NASA SVS limits: 17 science-topic searches, up to 170 page inspections, at most 36 downloaded videos, 300 MiB per file and 4 GiB total. The importer only downloads complete SVS visualizations; accepts exact-host `/vis/` media after HTTPS normalization; rejects redirects that downgrade to HTTP or leave the exact resource; screens page/item music and rights notes; skips non-empty audio-track metadata; and retains attribution, data sets, dimensions, dates, keywords, item URL, file URL and SHA-256. NASA SVS media is labelled Public Domain under its own default, not CC0.
- Build 70's NASA SVS shard completed successfully: **36 unique indexed videos**, **3,942,780,430 source bytes (~3.943 GB)**, 36 files in 3 ZIP volumes (3,941,124,395 compressed archive bytes). Its 157,202-byte `asset-shard--nasa-svs.json` manifest is uploaded to the Build 70 draft Release. The other 21 source shards that completed have also uploaded their manifests; only USGS remains in progress. Do not count these new bytes toward cumulative growth until Build 70's 23 manifests are merged, all Release assets/checksums are verified, the Release is published, and a cross-release SHA-256 comparison removes byte-identical repeats.

## ESO video archive expansion research — 2026-10-31

- Official ESO public video pages expose RSS category feeds, direct H.264 4K/1080p media links, page-level metadata, full credit text and SHA-256 checksums in the download controls. ESO's public default is CC BY 4.0 unless an item explicitly says otherwise; the full unaltered credit must be visible to viewers, not only in a YouTube description. Music is explicitly excluded from the usual CC BY grant, so a first importer should conservatively skip any page with a music credit, preserve the complete non-music credit, and create a visible end-card/overlay.
- Research confirmed category feeds such as `https://www.eso.org/public/videos/feed/category/esocast/` and `.../cosmology/`; 4K preview/Full HD formats and per-item SHA-256 are available on item pages. Some pages have third-party footage credits or non-ESO materials, so page-level rights screening is mandatory.
- Branch `feature/eso-video-archive-lane` has been created from main for isolated work, but at this checkpoint no ESO importer or source-shard code has yet been committed. Do not present ESO as an implemented or downloaded source until code, tests, CI and a real shard run are complete.
- Official sources: https://www.eso.org/public/copyright/ and https://www.eso.org/public/videoformats/.

## Time Stop 10s film — native 60fps upgrade checkpoint (2026-11-19 13:40 UTC)

This film is separate from the ONE MORE SCROLL / Remotion reference render. Project branch: `film/time-stop-10s-3d-cinema`.

- **Verified 30fps base master:** Actions run [#18 / 44511459706](https://github.com/Nolane-x/video/actions/runs/44511459706) completed successfully. Artifact `time-stop-10s-h2-18` (artifact ID `14527463068`) contains the 378-second / 6m18s, 1920×1080, 30fps H.264 + AAC stereo master, preview, contact sheets, 84-shot story package, subtitles, QA and VoiceStudio narration provenance. Artifact ZIP size reported by GitHub: 265,161,441 bytes. It is an Actions artifact (30-day retention), not a permanent Release yet.
- **Story facts:** 84 shots × 4.5 seconds = 378 seconds; 7 acts; 26 time-freeze FX shots. Vietnamese VoiceStudio / VieNeu narration is generated in 84 segments, with audio watermark verification and shot-synced placement. This is the verified 30fps source used by the subsequent 60fps workflows.
- **Important artistic scope:** the Three.js rainy-rescue module `video-projects/time-stop-10s/scenes/shots/time-stop-3d.js` is registered on 18 selected shots (`s053`, `s054`, `s056`, `s058`, `s059`, and `s061`–`s072`). The other 66 shots remain in the H2 Canvas 2D renderer. Never label the whole film as fully 3D or photorealistic. Target style is a stylized cinematic stick-figure film with selected 3D rescue shots.
- **Motion-interpolated 60fps candidate:** workflow run [#5 / 44533225246](https://github.com/Nolane-x/video/actions/runs/44533225246) completed interpolation and full-decode steps but failed the final frame-count assertion: 22,677 frames instead of 22,680 (three frames short). Do not use this as the primary 60fps master. Native H2 60fps below is preferred. The interpolation workflow can be repaired independently with a terminal 3-frame pad if a second edition remains useful.
- **Native 60fps path:** commit [7b96260](https://github.com/Nolane-x/video/commit/7b96260b6eb4408df1c47fd78890945b03e769da) introduced the FPS-selectable story/workflow; the default-argument defect was corrected in [6467af2](https://github.com/Nolane-x/video/commit/6467af2920503f6aeca6e9ee1e14e2d7fd4ea8d1). Run [#20 / 44534851475](https://github.com/Nolane-x/video/actions/runs/44534851475) completed successfully and generated the native H2 60fps master: 1920×1080, 60/1, 22,680 frames, 378 seconds, H.264 + AAC 48 kHz stereo. QA: −14.3 LUFS integrated, −2.1 dBFS peak; 84 shot-synced Vietnamese VieNeu segments, AudioSeal watermark verified. Artifact `time-stop-10s-h2-20`, ID `14542101968`, 301,241,502 bytes, expires 2026-12-19. The master MP4 itself is 119,265,280 bytes. Technical QA passed; `visual_approval` remains false.
- Run #19 failed in the initial Python storyboard setup because of the self-referencing default argument; this is fixed in commit 6467af2 and run #20 has successfully passed that stage. Do not describe run #19 as a render.
- **Permanent archive workflow:** `.github/workflows/archive-time-stop-native-60fps.yml` verifies run #20's artifact and uploaded a compact visual-QA artifact (ID `14596510571`). Archive run [#1 / 44662628970](https://github.com/Nolane-x/video/actions/runs/44662628970) passed artifact download, QA and contact-sheet upload, then failed because `gh release create` ran without a checked-out Git repository. The workflow now checks out the marker commit before the release step. Marker `.github/workflows/archive-time-stop-native-60fps.txt` has been updated to trigger archive run #2; publication is not confirmed until the run succeeds and the release/tag/assets are verified.
- Earlier interpolation attempts are diagnostic only: run #1 failed when Ubuntu APT mirrors returned HTTP 503; run #4 downloaded and checksum-verified the pinned FFmpeg archive but failed while selecting its internal paths. Run #5 uses full archive extraction and passed the binary-check step. Runs #2/#3 are older queued attempts; do not use their state as evidence for the current candidate.
- Preserve run #18's 30fps master. A passing render/metadata check is technical validation, not artistic sign-off. Review the complete contact sheets and moving action/contact/recovery frames before calling the film approved.

- Visual review checkpoint: all six contact sheets and representative frames from the rescue/action/recovery sequence were inspected. The sampled rescue progression is coherent, but no full frame-by-frame artistic approval has been given; keep `visual_approval: false`.

## Time Stop 10s — final native 60fps master and permanent release (2026-11-20)

- **Native master:** Actions run [#20 / 44534851475](https://github.com/Nolane-x/video/actions/runs/44534851475) succeeded. Technical QA passed at 1920×1080, 60/1 FPS, exactly 22,680 frames, exactly 378.0 seconds, H.264 + AAC 48 kHz stereo. Loudness: −14.3 LUFS integrated, −2.1 dBFS peak. 84 shot-synced Vietnamese VieNeu segments; AudioSeal watermark verified. `visual_approval` is deliberately still false.
- **Permanent GitHub Release:** [time-stop-10s-native-60fps-run-20](https://github.com/Nolane-x/video/releases/tag/time-stop-10s-native-60fps-run-20) is published (not draft). Release workflow run [#2 / 44662755247](https://github.com/Nolane-x/video/actions/runs/44662755247) succeeded after adding checkout before `gh release create`. Assets: `time-stop-10s-native-60fps-1080p.mp4` (119,265,280 bytes; SHA-256 `ddb197588298ccd258c350299f69ce112558a76f89f6da96558500f9ccd75cec`), 30-second preview (4,056,209 bytes), full `time-stop-10s-review.zip` (150,687,746 bytes) and SHA256SUMS.
- The six contact sheets and representative time points from the 3D rescue sequence were visually inspected in the working session. The rescue progression is coherent in the sampled images. Do not claim a full frame-by-frame artistic sign-off; keep QA `visual_approval: false`.
- **Motion-interpolated 60fps** is not the delivery master. Its run #5 completed the encode/decode steps but failed the exact frame-count gate by three frames (22,677 vs 22,680). Native H2 is better and already published.
- Local verified copies created for this conversation: `/mnt/data/time-stop-10s-native-60fps-1080p.mp4`, `...-preview-30s.mp4`, `...-review.zip`, `...-subtitles.srt`, `...-QA.json`, `...-contact-sheet.jpg`, `...-rescue-highlight.mp4`. Master local SHA-256 was recomputed and matches the GitHub Release asset digest.

## Time Stop 10s — expanded 3D story sequences candidate (2026-11-20)

- Preserve the existing published native-60fps master and Release as the known-good fallback: [time-stop-10s-native-60fps-run-20](https://github.com/Nolane-x/video/releases/tag/time-stop-10s-native-60fps-run-20). Do not replace it until the new candidate passes technical QA and motion/visual review.
- New isolated Three.js scene module: `video-projects/time-stop-10s/scenes/shots/time-stop-key-sequences-3d.js`. It adds 24 shots: kitchen/cup freeze `s013–s022` (10), basketball rescue `s026–s033` (8), and school hallway/books rescue `s037–s042` (6). The existing street-rescue module remains unchanged. Coverage is now 42 of 84 shots using Three.js; the remaining 42 shots still use H2 Canvas 2D. The film is not fully 3D.
- Source commits: `3acdaaea8d0af3d55c0f3a28e671e62f8a46f633` (new scenes), `9d2987a71527ca31d3aaf91f067d641223db548e` (pose/contact corrections), and `332ef8ef0231d80022e9db73d5d25579ab4ba268` (render workflow installs both Three.js modules and syntax-checks them).
- The 84-shot / 378-second timeline and native-60fps selection remain unchanged. Current candidate workflow [run #23 / 44666071523](https://github.com/Nolane-x/video/actions/runs/44666071523) was accepted on the branch. Its storyboard/narration-request preparation job passed, and VoiceStudio subsequently completed and uploaded artifact `video-voice-assets-44666071523` (ID `14597918199`, 52,459,735 bytes): 84 Vietnamese VieNeu segments, 199.84s PCM_24 mono at 48 kHz, AudioSeal verified (7 blocks; min confidence 0.9979; mean 0.9995), SHA-256 `9ff05535036814429493fce21c4abf62990ebf6934243b3d094ee707ba3544df`. The H2 render/sound-mix/QA job is now in progress. Earlier intermediate runs #21 and #22 were cancelled by the branch's cancel-in-progress policy when newer commits arrived; they are not failures of the candidate.
- The new visual candidate is not yet approved. After render completion, inspect the 84-shot contact sheets and create motion proofs for the three new 3D sequences (kitchen, court, hallway), including anticipation, contact, follow-through and recovery. Recheck Vietnamese subtitles against the action safe area. Keep `visual_approval: false` until the full moving picture/audio review is complete.
- Do not publish a new Release or overwrite the old master on the basis of source commits or a green syntax check. Record the new Actions run, artifact IDs, exact MP4 metadata, loudness and SHA-256 only after the corresponding job artifacts exist and are independently verified.


## Time Stop 10s — source-level visual blocking audit for 3D candidate (2026-11-20)

This is a source/projection audit, not a claim that contact sheets or the new master have been visually approved. Candidate run #23 is still the in-flight render for commit `332ef8ef0231d80022e9db73d5d25579ab4ba268`. Do not cancel or replace that run simply to apply these findings; use it as a render candidate, then make a focused follow-up patch and render after collecting its artifact.

Blocking / P1 review items to inspect and repair before a new Release:
- `s027` basketball close-up: current camera at `[-0.8, 2.65, 7]`, looking at `[-0.7, 1.25, 1]`, FOV 30°, while the ball is at `[4.55, 0.3, 1.1]`. A perspective projection using the 16:9 camera gives normalized horizontal coordinate about **+1.73**, outside the visible [-1,+1] frame. Reframe the close-up around the ball/boundary.
- `s032–s033` ball hand-off: the 3D figure faces +X by default; friend is to the right of the ball (`s032`: friend x=3.0, ball x=2.05; `s033`: friend x=2.4, ball x=2.05). The friend currently reaches toward +X, away from the ball. Turn the friend to face -X and use a carrying/receiving pose that actually supports the ball.
- `s040` book hand-off: child remains at x=2.0, but the books are reset around x=0.85–0.97, beside the hero at x=0.75. They do not meet the child's arms. Interpolate the stack from the falling position toward the child's forearms.
- `s041–s042` book hold: six book objects are placed at the same x/z and y values separated by only 0.015 while each book is 0.13 units thick. They overlap almost completely, and the stack sits at foot-level rather than in the child's arms. Arrange a visibly separated stack and bring it to chest/forearm height with a suitable supported pose.
- Mother hairstyle: `makeKitchen` asks `T3.figure` for `head: 'bun'`, but the current rig only has special geometry for `cap` and `beanie`. Add explicit bun/hair geometry or choose a supported hairstyle; do not assume the `bun` token is implemented.
- Countdown continuity: the spoken line for `s018` says “con số chín giây”, while the shot HUD is configured with `timer=7` (the sequence already shows 10, 9, 8 in `s015–s017`). Correct the spoken line / corresponding cue and regenerate the affected narration job so voice and timer agree. The line also describes a wrist display, but the current timer overlay is fixed at the upper-left; consider a visible wrist device for a stronger visual match.

These findings do not invalidate the technical pipeline pass; they do block artistic approval and permanent publication of the expanded candidate until addressed. Keep the existing run-20 release/master untouched. Re-run source checks and motion QA after fixes, then leave `visual_approval: false` until full-length viewing is complete.


## Time Stop 10s — focused 3D source corrections and rerender (2026-11-20)

- Kept the initial 42-shot 3D expansion render [run #23 / 44666071523](https://github.com/Nolane-x/video/actions/runs/44666071523) intact as the first candidate; it was still at the full native-60fps master step at the last status query. Do not confuse it with the later corrected source.
- Created a follow-up source branch `film/time-stop-10s-3d-review-fixes`. Final source changes in the initial correction pass: `101547139501d908ff2aba710bca835ac3e9962e` (ball/camera and prop blocking), `2ad3f03bce89f3e8d752299837a54322fbda1687` (new articulated `carry` pose in the Three.js rig), `0b43d44d85a666d7b5df23e119bde2ca6badfaff` (countdown narration correction and full corrected source head).
- Fixes: `s027` ball close-up now frames the ball inside the 16:9 shot (projected x changed from +1.73 off-screen to 0.0); court narrowed to show a real asphalt access road beyond the end line; ball path now drops from the friend's hand and rolls to the road edge; friend turns toward the ball in `s032–s033` and uses the new two-arm `carry` pose; mother has explicit hair-cap + bun geometry instead of unsupported `head:'bun'`; hallway books now interpolate to the child's forearms and form two separated three-book columns at chest level rather than six overlapping floor-level objects. `s018` scene now centers on the protagonist and narration reads “Vòng đếm ngược báo còn bảy giây.” to match the 7-second HUD.
- Corrected full-film workflow [run #26 / 44671416000](https://github.com/Nolane-x/video/actions/runs/44671416000) has started on the corrected branch. Storyboard preparation passed. VoiceStudio passed and uploaded `video-voice-assets-44671416000` (artifact ID `14599653357`, 52,525,240 bytes): 84 Vietnamese VieNeu segments, 200.24s PCM_24 mono/48kHz, AudioSeal verified (7 blocks; minimum confidence 0.9992; mean 0.9997), SHA-256 `30d756206f9a35183d2cdd0b82d5f4ef669d7af5dcd004da6f875fc342ea86fe`. Transcript confirms `s018`: “Vòng đếm ngược báo còn bảy giây.” The H2 full render job has started.
- A separate low-cost silent proof workflow is on branch `review/time-stop-10s-3d-fixes`: [.github/workflows/preview-time-stop-10s-3d.yml](https://github.com/Nolane-x/video/blob/review/time-stop-10s-3d-fixes/.github/workflows/preview-time-stop-10s-3d.yml). Run [#1 / 44671703847](https://github.com/Nolane-x/video/actions/runs/44671703847) is rendering selected-shot contact sheets and 60fps motion proofs for 58.5–85.5s (kitchen), 117–148.5s (court), and 175.5–189s (hallway). These clips are silent 960×540 review evidence, not a release master.
- The corrected source branch intentionally does not overwrite the permanent run-20 Release. The file currently at `/mnt/data/time-stop-10s-native-60fps-1080p.mp4` hashes to the old known-good SHA-256 `ddb197588298ccd258c350299f69ce112558a76f89f6da96558500f9ccd75cec`; it is not the expanded candidate.
- Next gates: complete targeted proof rendering; inspect selected stills and the full motion clips for hand contact, ball/road relation, book-hold continuity and character crop; then inspect the corrected full master and audio. Keep `visual_approval: false` and do not publish until full-length review.


## Time Stop 10s — motion-proof visual review and final camera correction (2026-11-20)

- Targeted motion proof workflow [run #1 / 44671703847](https://github.com/Nolane-x/video/actions/runs/44671703847) completed successfully. It generated 24-shot Three.js contact sheets plus three exact-length silent 960x540 / 60fps motion clips for kitchen, court and hallway. ffprobe validated the requested frame counts for all clips.
- Inspected the generated contact sheets and kitchen/court motion-frame sheets. Corrections read well in the samples: the court ball close-up is now inside frame; the road edge is visible; the friend faces the incoming ball for the hand-off; the book pile is separated and moved to the child's upper-body/forearm area. These are promising targeted checks, not a complete full-film artistic approval.
- One remaining composition flaw was visible in kitchen insert s018: the protagonist's head was still cropped by the left frame edge and the cup sat too far right. Fixed by source commit e82a7591d6676e68f38aaea1271e92e8789c567b: hero repositioned to x=-1.7 and camera widened/recentered. New full candidate is [run #27 / 44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329); narration-request prep passed and VoiceStudio is generating the matching narration.
- Run #26 [44671416000](https://github.com/Nolane-x/video/actions/runs/44671416000) completed all 24 render/QA steps with success and uploaded artifact time-stop-10s-h2-26 (ID 14604975960, 258,272,318 bytes). Its corrected story includes the 7-second HUD wording and the 42/84 3D-shot expansion. A dedicated master-inspection workflow [run #2 / 44736526771](https://github.com/Nolane-x/video/actions/runs/44736526771) is downloading it to independently full-decode the MP4, verify 1920x1080/60fps/22,680 frames/378s + AAC 48kHz stereo, compute SHA-256, and export three full-mix action clips plus 24 sampled master frames. This independent inspection is separate from the original pipeline QA.
- Run #27 supersedes run #26 only for the corrected s018 camera framing. Preserve run #20's public Release and run #26's artifact until run #27 passes and its master is inspected. Do not create a new Release yet; keep visual_approval: false.


## Time Stop 10s — independent master QA and second 3D proof pass (2026-11-20)

- Run #26 corrected 42-shot 3D candidate [44671416000](https://github.com/Nolane-x/video/actions/runs/44671416000) completed successfully; artifact ID `14604975960`, size 258,272,318 bytes.
- Independent inspection [run #5 / 44737356101](https://github.com/Nolane-x/video/actions/runs/44737356101) completed successfully. It downloaded the actual master, decoded video and audio separately with FFmpeg, recomputed ffprobe metadata/frame count, and checked narration placement. It then created a 24-frame master contact sheet, full-mix 1080p60 clips for kitchen/court/hallway, and a checksum report. Artifact: `time-stop-10s-run26-master-inspection`, ID `14629461926`, 12,853,588 bytes.
- The independent check confirms 1920x1080, native 60/1 fps, 22,680 video frames, 378.0s, H.264 + AAC stereo 48kHz; QA loudness −14.3 LUFS, peak −2.0 dBFS; 84 shot-synced Vietnamese VieNeu segments; AudioSeal verified. The master SHA-256 and all detailed measurements are in the inspection artifact's `master-inspection.json` and `master-sha256.txt`.
- The second targeted 3D proof [run #2 / 44736908508](https://github.com/Nolane-x/video/actions/runs/44736908508) completed successfully after syncing the s018 reframe. It regenerated 24 selected-shot contact sheets and all three silent 960x540 / 60fps motion clips; artifact ID `14629681532`, name `time-stop-10s-3d-motion-review-44736908508`, size 2,725,831 bytes. No renderer/ffprobe/clip-count failure was reported.
- Full corrected candidate [run #27 / 44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) has passed both VoiceStudio and H2 setup/storyboard/renderer scan/contact sheets/30s preview; it was at the full native 1080p60 render step at last check. Its voice artifact ID is `14628059443` (52,634,924 bytes). This candidate differs from run #26 by the final s018 camera/hero placement correction.
- A new inspection iteration [run #6 / 44738517112](https://github.com/Nolane-x/video/actions/runs/44738517112) is underway to expose a compact frame montage in workflow logs for direct visual inspection; this avoids reliance on the container runtime, which was unavailable during this session.
- Do not publish a new Release until run #27 has finished and its own master is independently inspected. Preserve run-20's public release and run-26's passing candidate. Keep `visual_approval: false` until review of the full-mix clips/master frames and a full-length review.


## Time Stop 10s — permanent draft archive workflow prepared (2026-11-20)

- Added .github/workflows/archive-time-stop-10s-expanded-run27.yml on the candidate branch. It is gated by marker .github/workflows/enable-time-stop-10s-expanded-draft.txt or workflow_dispatch. It downloads run #27 artifact time-stop-10s-h2-27, validates 1080p60 / 22,680 frames / 378s / AAC 48kHz, 84 Vietnamese VieNeu segments and AudioSeal watermark, then creates a draft release at tag time-stop-10s-expanded-3d-review-run27.
- The workflow stores master MP4, 30s preview, full review bundle, QA, voice placement, Vietnamese SRT and SHA256SUMS. It explicitly keeps visual_approval: false and says the archive is a review candidate, not full artistic approval.
- The workflow is prepared but NOT activated yet. Do not add the marker until run #27 has completed and independent verification of run #27 succeeds. This prevents archiving an incomplete or unverified master.
- Existing run-20 public Release remains untouched. Run-26 independent inspection passed; run-27 full render and proof #4 remain pending at this checkpoint.


### Run-26 exact master checksum and independent decode result

- Independent inspection [run #5 / 44737356101](https://github.com/Nolane-x/video/actions/runs/44737356101) passed. The master file inside artifact 14604975960 is 98,061,158 bytes and has SHA-256: 7184018d36b5dd28284a6621ba66802764e03c95bd7050efc350a3b7140f871a.
- ffprobe counted exactly 22,680 H.264 frames at 60/1, 1920x1080, 378.000s; AAC audio 48kHz, 2 channels. FFmpeg video and audio full decodes both returned code 0. Reported loudness -14.3 LUFS, peak -2.0 dBFS; 84 Vietnamese VieNeu segments, watermark verified.
- Inspector run #6 [44738517112](https://github.com/Nolane-x/video/actions/runs/44738517112) completed successfully and created a compact montage in logs; it also generated the three full-mix clips, checksum and 24 sampled frames in artifact 14629966995 (12,853,637 bytes).
- Proof run #4 [44739190519](https://github.com/Nolane-x/video/actions/runs/44739190519) is active after adding Pillow to the compact montage step. Earlier run #3 passed storyboard scan and still rendering but failed only because Pillow was missing on the runner; no H2 source/render error was reported.


## Time Stop 10s — corrected s018 proof verified visually (2026-11-20)

- Proof workflow [run #4 / 44739190519](https://github.com/Nolane-x/video/actions/runs/44739190519) completed successfully (20/20 steps), including full 84-shot scan, 24 selected 3D contact sheets, eight key stills, and 3 exact-duration silent 960x540 / 60fps motion clips. Artifact: `time-stop-10s-3d-motion-review-44739190519`, ID `14630392510`, 2,723,201 bytes.
- Its compact montage was inspected from job logs. The corrected `s018` at 76.5s now keeps the protagonist's head/face in frame, the suspended cup visible, and the 7-second HUD readable. This resolves the left-edge crop seen in run-26's master sample.
- The same montage confirms `s027` ball close-up stays in frame; `s032–s033` ball hand-off and recovery remain visible; `s040–s042` books are raised from floor level into the child's upper-body/forearm area. This is a targeted visual check, not full-length sign-off or proof that every hand contact is perfect.
- Run #27 [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) remains the new full candidate with the corrected `s018` camera; at last check its H2 job was rendering the complete 1080p native 60fps silent master. After it finishes, mix, upload and independent-inspect the actual run-27 master before drafting the archive.


## Time Stop 10s — basketball release contact correction and run-28 handoff (2026-11-20)

- While reviewing the source blocking, confirmed the friend's right-hand contact point in 3D is approximately x=2.60, y=1.47, z=1.10 from friend root [2.0,0,0.9]. Previous s026 ball start [2.5,1.08,1.1] was materially low and too far back from the hand.
- Corrected s026 in commit f630e863c2b118cdb3e6c7ecc28fb4479783059e: friend moves to z=0.9 for the release shot; basketball starts at [2.6,1.47,1.1] aligned with the hand, then drops/bounces toward the road edge x=7.45. Synced this source to review branch in commit 6fba5daf0d2285f1df3944cd8c1be4d13b30b040.
- Full workflow run #27 [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) was superseded and cancelled while rendering its master (render step conclusion cancelled; no sound mix/package/upload). Do not treat run #27 as a deliverable.
- New full candidate run #28 [44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) is now running with s018 reframing and s026 hand-aligned basketball release. Story payload preparation passed; VoiceStudio has started the 84-segment render. A fresh master will be produced only after that succeeds.
- Proof run #5 [44740324018](https://github.com/Nolane-x/video/actions/runs/44740324018) is rebuilding the targeted 3D proof on the current source. After it completes, inspect the s026 first frame to confirm hand contact, then verify s027 close-up and hand-off/recovery; preserve run-26 as the only independently verified full master until run #28 is complete and independently inspected.
