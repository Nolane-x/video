# AI session handoff

## Asset-library handoff — 2026-10-30

Continue this workstream separately from the film projects below.

- Repository: `Nolane-x/video`. Main pipeline files: `tools/video/build_asset_library.py`, `tools/video/package_asset_bundles.py`, `.github/workflows/build-video-asset-library.yml`, `tools/video/test_asset_library_sources.py`, `video-library/assets/sources.json`.
- **Build 48** [run #48](https://github.com/Nolane-x/video/actions/runs/41037407715) completed external downloads but failed ZIP packaging due duplicate USGS image path for the Kilauea Southwest Rift Zone title. It indexed 48,588 assets, checksummed 48,954 files and did not publish. The fix is in merged PR #16: `usgs_asset_item_slug(title, item_url)` appends 12 hex chars of the exact item URL SHA-256 to prevent same-title collisions.
- Build 48 source counts are recorded in `docs/STATE.md`: e.g. Poly Haven 54 packages/338 files, ambientCG 122/981, OpenGameArt 108 items/35,608 files, Wikimedia 687 images/28 videos, USGS 80 images/40 videos/24 audio, OpenMoji 8,990 SVG. Smithsonian was rate-limited (HTTP 429). Do not confuse these successful downloads with a completed ZIP release.
- Last confirmed durable release is Build 43: 1,095,394,051-byte ZIP; SHA-256 `a03f02fcd6915361ed64c5ec1d0158837458ac2988adf300de33515b636bbe36`.
- **Build 49** [run #49](https://github.com/Nolane-x/video/actions/runs/41048645254) is in progress on merge commit `4391e74579ee78e13478dc3c0c9e10f1f5566221`. It adds bounded LazyTextures API categories plus optional Poly Pizza API downloads with exact per-item CC0 1.0 checks. Poly Pizza is skipped if `POLY_PIZZA_API_KEY` is absent. All published caps in source code are ceilings, not actual download counts.
- **Build 50** [run #50](https://github.com/Nolane-x/video/actions/runs/41054395607) is pending behind Build 49. PR #16 merged at `283a082587b28459737e25c805da784915d7a4f8`; it adds the Kenney splash-screen derivative subset (CC0 only), namespaced SVG root validation, and a deterministic USGS item-URL hash suffix to prevent path collisions. [CI #109](https://github.com/Nolane-x/video/actions/runs/41054098329) passed on the final PR head.
- Quaternius current QAL v1.0 is source-only because raw asset redistribution is prohibited. Poly Pizza is per-item licensed; only exact CC0 records are eligible. Never mark the full catalog CC0.
- Build workflow concurrency uses `cancel-in-progress: false`; this was verified by Build 49 queueing after Build 48 and Build 50 queueing after Build 49. Leave these runs intact; inspect them when they complete.
- **Smithsonian rate-limit follow-up — PR #17:** [PR](https://github.com/Nolane-x/video/pull/17), branch `fix/smithsonian-open-access-backoff`. It adds finite retries for 408/429/5xx, honors `Retry-After` seconds/HTTP dates and `X-RateLimit-Reset`, uses one-second spacing, and stops the remaining unit searches if 429 persists after retries. Both record and exact media must still say CC0; rights checks were not loosened. Validation run [#110](https://github.com/Nolane-x/video/actions/runs/41059088369) passed Python compilation and offline rights tests; the no-network original-asset smoke build was still running at the latest check. PR merged to main at [b0635e2](https://github.com/Nolane-x/video/commit/b0635e21dd0d66e42d0ef98846ba245dd5203801). Builds 49/50 were launched/queued from earlier source commits and do not contain the patch; subsequent main-branch builds will.
- The workflow maps the `SMITHSONIAN_API_KEY` repository secret into the builder. Without the secret the builder uses `DEMO_KEY`; do not commit API keys. A dedicated Actions secret is the correct configuration for a later high-volume Smithsonian run.
- Next: (1) inspect Build 49 logs/counts and package outcome; (2) inspect Build 50 outcome with the USGS collision fix; (3) verify ASSET_BUNDLES.json, every ZIP checksum and complete path coverage; (4) publish/claim only release sizes actually exposed by GitHub Releases.
## Current verified state — continue from these, not historical render numbers
- Primary candidate: **THE WEIGHT OF YES — render #31**, [workflow](https://github.com/Nolane-x/video/actions/runs/40532086413), source [commit](https://github.com/Nolane-x/video/commit/58c95de849405b0ae5d1636851bb883ffa3870ec), manifest/QA: `video-library/the-weight-of-yes/manifest.json` and `video-library/the-weight-of-yes/QA.md`.
- **THE FIRST HOUR #55** is now the current technical + targeted-visual candidate ([workflow](https://github.com/Nolane-x/video/actions/runs/40626868973)); manifest and QA ledger: `video-library/the-first-hour/manifest.json` and `video-library/the-first-hour/QA.md`. The downloaded artifact was checksum-verified. Full-resolution B27 frames at 154.5, 157.2, 158.2 and 159.5 s confirm the whisper is below the calendar and the final line sits inside the left safe area. The root cause was that the workflow overwrote `tune_story.py` args with `shot-overrides.json`; the actual override was fixed in `1fc7a4c0e9fae34b2f1847204a63ad3a96e771f2` and a post-merge regression gate was added in `9d86d9a4195982924868468887ff68a2fbcf1790`. Runs #52/#53 remain historical candidates with a known B27 placement issue; #54 was cancelled. Full-length viewing with audio and perceptual listening remain pending.
- **ALMOST READY #34** passed all render/validation steps ([run](https://github.com/Nolane-x/video/actions/runs/40532086120)); manifest/QA: `video-library/almost-ready/manifest.json` and `video-library/almost-ready/QA.md`.
- Downloaded artifacts for Weight of Yes #31, Almost Ready #34 and First Hour #55 were inspected. Metadata confirms H.264 1920×1080 @24 fps plus AAC 48 kHz stereo; durations are 143 s / 172 s / 172 s. SHA256SUMS ledgers passed (29 / 25 / 24 entries).
- Audio measurement: Weight of Yes −14.0 LUFS / 9.2 LU LRA / −5.0 dBFS peak; First Hour #55 −14.0 / 6.6 / −1.9; Almost Ready #34 −14.1 / 9.1 / −1.8.
- Shared handwritten-whisper reveal now completes within 30% of the caption hold. First Hour and Almost Ready source tuners assert at least 1.2 seconds of full-text readability; First Hour's workflow now repeats this check after `shot-overrides.json` is merged so overrides cannot silently erase the fix. Full-length playback and perceptual listening remain pending for every film; don't infer artistic approval from green CI or contact sheets.
- Preserve the canonical ONE MORE SCROLL master. Do not archive any new candidate as final until start-to-finish picture and audio review is completed.

## First reads
Read root `AGENTS.md`, `.agents/skills/video-production-master/SKILL.md`, `docs/STATE.md`, and `video-library/one-more-scroll/manifest.json`.

## Creative decisions to preserve
- User wants cinematic story-led stick-figure video, not generic AI-looking colors or flat repeated SVG backgrounds.
- Simple character; rich environment; warm practical lighting; motivated camera/editing; expressive action; visible contact; intentional sound arc.
- References: first consult `video-library/reference-clips.json` for the user's exact examples “The Words You Never Forgot” (https://www.youtube.com/watch?v=qyFUAlGMxSE) and “What If You Were a Mentalist?” (https://www.youtube.com/watch?v=XexSnQTMMhw), plus Ifverse Tales / Day One Films. Verify the sources are accessible and actually watch them before making timestamped claims; don't copy assets.
- The user expects honesty: “file exported” is not “visual QA passed.”
- Never confuse H2 Canvas/Chromium render with Remotion or Blender output.

## Project map
- Repo: https://github.com/Nolane-x/video
- Skill: `.agents/skills/video-production-master/SKILL.md`
- Remotion: `video-projects/remotion`
- Storyboard: `video-projects/remotion/public/story/shots.json`
- Audio generators: `video-projects/remotion/h2-audio`
- Blender: `tools/blender/render_h2_stage.py`
- Krita: `tools/krita/README.md`
- H2 source mirror: `integrations/h2-selfimprove-studio/` (51-file v1.0.2 base); v1.1.0 production overlay: `integrations/h2-selfimprove-studio-production-overlay/`.
- Active private ChatGPT plugin: [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) — v1.1.0, current release `pluginrel_6ade248942988191a57ff1059c818720` (Plugin Creator update confirmed 2026-10-25); see `docs/CHATGPT_PLUGIN.md` and `integrations/h2-selfimprove-studio-production-overlay/RELEASE-RESULT-v1.1.0.md`.
- Current film manifest: `video-library/the-weight-of-yes/manifest.json`; canonical ONE MORE SCROLL history remains in `video-library/one-more-scroll/manifest.json`.

## Tool and video inventory
- Read `docs/TOOL_INVENTORY.md`, `video-library/previous-works-catalog.json`, and `video-library/reference-clips.json` before assuming a tool, source archive, old clip, or reference MP4 is present.
- `tools/video/archive_previous_works.py` stages prior clips by fixed SHA; the GitHub verification workflow marks them permanent only after the remote files are checked.
- `tools/video/publish_h2_source_release.ps1` uploads the large H2 source packages to a versioned GitHub Release after checksum validation.

## Artifact truth
The exact 155-second Full HD H2 master is archived at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`, and verified by [workflow run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143). The original source ZIP and scene-fixes source-v2 ZIP are durable [GitHub Release assets](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). A full-length source-v2 candidate passed technical render/audio/ffprobe validation in [run 40276064292](https://github.com/Nolane-x/video/actions/runs/40276064292); candidate URL, SHA-256 and review bundle are in `video-library/one-more-scroll/h2-source-release.json`. Its artistic sign-off remains pending: watch the whole candidate with audio and review action contact/pacing before promoting it. The Remotion reference render at `video-library/one-more-scroll/renders/remotion-run-36/` is a different renderer/output. Never conflate them.

## Historical H2 source-v2 render review gate
- Candidate MP4: `https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v2-render-candidate.mp4`.
- Review ZIP: `https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v2-render-review.zip`.
- Technical pass: 155.000s, 1920×1080 @24fps, H.264 + AAC stereo 48 kHz; SHA-256 `5f72e611c1257a4b31fa834c4b8d5481a8404b6becb50f41df7663cd2f7c96b7`.
- Contact-sheet sampling suggests the staircase head crop is improved; shoe-to-hand contact and tight close-up pacing still need full-motion review. Do not replace the canonical H2 master until someone watches the full candidate with audio and explicitly approves it.

## Source-v3 shoe-tying fix — full render, stream/audio QA and release packaging passed
- Preview passed in [run 40280228327](https://github.com/Nolane-x/video/actions/runs/40280228327).
- Corrected full render and Release publication passed all required steps in [run 40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324); first attempt [40281627022](https://github.com/Nolane-x/video/actions/runs/40281627022) failed only because the patch script was missing from the review payload at checksum time.
- Candidate: [download source-v3 H2 MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v3-shoelace-fix-candidate.mp4); SHA-256 `761d238ae019e6c39eca3a9c46bff88b02f6f96e332f35d6e5d6b0d41e29310f`, 33,409,690 bytes.
- Review ZIP: [download source-v3 review bundle](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v3-shoelace-fix-review.zip); SHA-256 `56bf506a0ec63fbb9d99256ac1cc989186f6ddab12056c9cfb9f012b922d0745`, 33,709,840 bytes. Includes contact sheets, browser/render/mix/EBU logs, metadata report, pinned patch and SHA256SUMS.txt.
- Verified: 155s, 1920×1080 @24fps, H.264 + AAC stereo 48 kHz. EBU R128: −14.0 LUFS integrated, 6.9 LU LRA, −2.4 dBFS true peak.
- Base archive SHA-256 `b8db965db214bf0e37b307d3fe1aa663c55f29ee753fd9103a5972b5fe633014`; patch `tools/video/patch_h2_shoelace_scene.py` pinned to `05a2027cebdc83cedc1002992198d9404f253647`.
- Technical validation **passed**, but the shot-b17 motion spot-check found a P1 visual issue: Spot-check of frames at 0.25-second intervals around 80–84 seconds: the forward crouch and alternating arm motion are visible, but hand-to-shoe/lace contact remains ambiguous at the full-shot scale. The actor is small in frame; shot b17 needs a more legible medium/close composition and clearly visible contact with the lace prop. This is a visual QA finding, not a technical-render failure. Next action: build a source-v4 3–6 second focused preview with better action framing and clear hand/lace contact; only then decide whether to full-render. Also review the complete source-v3 candidate with audio for timing, close-up rhythm, transitions, synchronization and emotional arc. Do not replace the canonical H2 master.
- Canonical master SHA-256 remains `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`.

## End-of-session
Run checks; inspect contact sheets and motion proofs; record exact renderer, commit, run URL, artifact storage/expiry, audio measures, defects and next actions. Update `docs/STATE.md`, this file and the per-video manifest.


## Latest archived Remotion reference
- Video: `video-library/one-more-scroll/renders/remotion-run-36/one-more-scroll-remotion-master.mp4`
- Source commit: `e766c5f407cf4bbd175c28d306acc99c6d8aa609`; render CI: [40200152650](https://github.com/Nolane-x/video/actions/runs/40200152650).
- SHA-256: `cdccb836587093f2ab35d39b2ff229438ed947e6e5ccfc26f9f7e5fa13539765`; 155.100s, 1280x720, 24/1.
- This is a Remotion render, not the H2 Canvas/Chromium master. Inspect contact sheets and motion proof before accepting artistic quality.



## Historical ALMOST READY candidate — run #14 technical pass
- Project: 29 shots / 172 seconds about perfectionism and fear of being seen.
- Latest render: [run #14 — success](https://github.com/Nolane-x/video/actions/runs/40429993482), source commit `1ab974acc2f8e0b268940fbf16f6b566884dace6`; manifest and QA in `video-library/almost-ready/`.
- Master SHA-256: `67f0f483bf87c2cab16b333e8427e30a8445edf5120d9b08b1832dfba54806d2`; 1920×1080/24 fps H.264, AAC 48 kHz stereo, −14.0 LUFS, −1.9 dBFS true peak.
- B19 motion sample passed the targeted limb-coherence check. Contact sheets and complete 172-second audio/video review remain pending; artifact expires 2026-11-26T01:05:34Z.
- Do not mark artistically approved until full review. Keep it separate from THE FIRST HOUR, THE WEIGHT OF YES and canonical ONE MORE SCROLL.


## Asset library — distributed 50 GB target (2026-10-30)
- PR [#18](https://github.com/Nolane-x/video/pull/18) is merged to main at `6a44c974ba4be413a5b5006a720a5db5ee8e1b69`.
- The new workflow fans out 22 independent source lanes with `max-parallel: 16`; it streams each validated ZIP volume (<1.7 GB uncompressed) straight into a unique draft Release rather than staging the full collection or relying on Actions Artifact storage.
- Source worker: `tools/video/build_asset_library_shard.py`. Final merge/publish gate: `tools/video/finalize_asset_library_release.py`. Each lane manifest records provider report, asset license/provenance, byte size, SHA-256, per-file ledger and volume coverage.
- The finalizer requires all 22 manifests; unique asset IDs/paths; every packaged file in exactly one volume; exact remote Release asset names/sizes; and GitHub's SHA-256 digest for every volume, manifest and metadata file. It only publishes after every check passes.
- `gh release upload --clobber` supports reruns; raw files are removed only after a successful volume upload. Upload errors leave the original source files intact.
- Poly Haven has an 8 GiB aggregate lane cap to remain within a standard runner's 14 GB SSD. Provider-specific CC0/Public Domain and exact item-rights gates remain mandatory.
- Target is decimal **50,000,000,000 indexed resource bytes**, not a configured cap or a file-count proxy. Read actual finalizer output; never claim target reached before the published Release verifies.
- PR validation [run #131](https://github.com/Nolane-x/video/actions/runs/41066218856) passed all offline rights tests and generated-asset smoke tests.
- Current first distributed build [Build #52](https://github.com/Nolane-x/video/actions/runs/41066528335) was created after merge and is queued at this snapshot; no 50 GB output has yet been established. Old serial Build 49 remained in progress, Build 50 was cancelled, and Build 51 was pending; these are not evidence of completion.
- Existing last confirmed public library release remains Build 43 (1,095,394,051 bytes). Continue by inspecting every Build 52 source lane and improve source selection using measured bytes, not hypothetical caps.


## Video asset library — later 2026-10-30 handoff
- Latest source / cap changes are on main SHA `37fa3edaeab6cdbe992c754faac862ed9e779d4c`; CI #143 [passed](https://github.com/Nolane-x/video/actions/runs/41080103431).
- Build 62 [run](https://github.com/Nolane-x/video/actions/runs/41078978167) has 39 draft-release ZIP volumes (8,154,719,650 compressed bytes), 21/22 manifests, and the USGS lane still running at the snapshot. The finalizer has not published it.
- Completed Build 62 source logs account for 8,691,066,675 indexed resource bytes before USGS. Major totals: NASA 2.0306 GB, NOAA 1.9622 GB, OpenGameArt 1.4348 GB, Internet Archive 1.0923 GB, ambientCG 0.8693 GB, Wikimedia 0.5172 GB, Poly Haven 0.3850 GB. These are source file bytes from manifests, not ZIP sizes.
- USGS IDs now contain a SHA-256-derived item URL identity; NOAA IDs and filenames do too. Smithsonian will not burn ten minutes retrying a 429 if the provider's Retry-After is longer than 30 seconds.
- NASA adds 45 search topics with an 8 GiB aggregate ceiling; Wikimedia Commons adds 50 search topics, 1,600 image cap and 8 GiB ceiling; Internet Archive search depth is 5 pages × 100 and up to 220 item pages per collection; OpenGameArt has expanded category caps 60/60/48/36/36, 10 search pages and 120 item pages/category, 8 GiB total ceiling.
- ambientCG caps sum to 792 selections; Poly Haven limits are 120 HDRIs / 180 models / 480 textures; both retain 8 GiB aggregate runner-safe ceilings.
- Source matrix `max-parallel: 18` uses the 20 concurrent standard GitHub-hosted runner slots on Free, keeping a little room for CI and portable-skill packaging. Build 68 [run](https://github.com/Nolane-x/video/actions/runs/41080103332) is queued behind Build 62 and will pick up the latest caps.
- DVIDS is a future option only after a user API key is added and item-level media rights / privacy / publicity / DoD non-endorsement checks are designed; it is not currently bundled.
- The target remains exactly 50,000,000,000 indexed resource bytes. 50 GB is **not** yet achieved or published. Continue from Build 62's USGS lane, then inspect the newest distributed build's lane summaries, update caps based on actual yield and re-verify every Release asset SHA-256 before publication.

## Asset-library recovery — published Build 62 (2026-10-31)
- Published release: https://github.com/Nolane-x/video/releases/tag/video-asset-library-build-41078978167
- Recovery workflow [41149796885](https://github.com/Nolane-x/video/actions/runs/41149796885) succeeded after patching the finalizer to find draft releases through the release collection endpoint, not /releases/tags/{tag}.
- The release contains 73 assets: 44 ZIP volumes, 22 source manifests and 7 global metadata/catalog/license/checksum files. Every remote name, size and GitHub SHA-256 digest was verified.
- Final actual indexed resource total: **12,303,303,941 bytes = 12.303 GB (decimal) = 11.458 GiB**; 55,700 indexed assets. Compressed ZIP volume total 11,677,924,120 bytes. 50 GB target not yet reached (24.606%).
- USGS contributed 3,612,237,266 bytes / 196 assets; NASA 2,030,638,116 / 47; NOAA 1,962,159,985 / 340; OpenGameArt 1,434,785,584 / 42,030; Internet Archive 1,092,253,646 / 11; ambientCG 869,348,271 / 1,241; Wikimedia 517,246,544 / 660; Poly Haven 384,999,485 / 338. Exact aggregate is authoritative in ASSET_INDEX.json.
- Build workflow is manual + one explicit push sentinel .github/ASSET_LIBRARY_BUILD_REQUEST; do not restore a broad push trigger, because code edits otherwise restart costly full downloads. Matrix uses max-parallel 18, explicit contents: write at job level and a dedicated concurrency group.
- Recovery workflow .github/workflows/recover-video-asset-library-release.yml reuses existing 22 shard manifests and remote assets. For another draft, update .github/ASSET_LIBRARY_RECOVERY_REQUEST to the exact draft tag; finalizer rebuilds the metadata, verifies every remote asset, and publishes.
- Next step: run the next full build using expanded caps. Then create a cumulative cross-release index with SHA-256 deduplication so repeat source items aren't counted twice toward the 50 GB total.

## Time Stop 10s — continue native 60fps production (2026-11-19)

- Work only on branch `film/time-stop-10s-3d-cinema`. Read the project source: `video-projects/time-stop-10s/scripts/build_story.py`, `.github/workflows/render-time-stop-10s.yml`, `video-projects/time-stop-10s/scenes/shots/time-stop-3d.js`, and `.github/workflows/render-time-stop-60fps.yml`.
- Run #18 ([44511459706](https://github.com/Nolane-x/video/actions/runs/44511459706)) is the known-good baseline: 378 seconds, 1920×1080, 30fps, 84 shots, 26 freeze FX, AAC 48 kHz stereo, 84 VoiceStudio/VieNeu segments. Keep its artifact/master as fallback.
- Selected Three.js shots only: `s053`, `s054`, `s056`, `s058`, `s059`, `s061`–`s072` (18 total). Other 66 shots are H2 Canvas 2D. Do not claim fully 3D.
- The native-FPS renderer is selected by `.github/workflows/enable-time-stop-native-60fps.txt` containing exactly `native-60fps`. `build_story.py` accepts `--fps 30|60`. Run #19's self-referencing default argument defect was fixed in commit [6467af2](https://github.com/Nolane-x/video/commit/6467af2920503f6aeca6e9ee1e14e2d7fd4ea8d1). Native run #20 [44534851475](https://github.com/Nolane-x/video/actions/runs/44534851475) succeeded: 1920×1080, 60fps, 22,680 frames, 378 seconds, H.264 + AAC 48 kHz stereo; −14.3 LUFS / −2.1 dBFS; 84 Vietnamese VieNeu segments, AudioSeal watermark verified. Artifact ID `14542101968`, 301,241,502 bytes, expires 2026-12-19. `visual_approval` remains false pending full artistic review.
- Motion-interpolated run #5 [44533225246](https://github.com/Nolane-x/video/actions/runs/44533225246) used run #18 as input, BtbN FFmpeg 9.0.2 (archive and executable SHA-256 pinned), `minterpolate` MCI/AOBMC, scene-cut detection and a full decode pass. It failed only the exact frame count: output was 22,677 instead of 22,680. Native run #20 is the preferred 60fps edition; do not confuse the two.
- Permanent publication workflow is `.github/workflows/archive-time-stop-native-60fps.yml`. Archive run #1 [44662628970](https://github.com/Nolane-x/video/actions/runs/44662628970) passed download, QA gate and contact-sheet upload, but failed at `gh release create` because no repository had been checked out. The workflow now checks out `${{ github.sha }}` with persisted credentials before the release step. Marker `.github/workflows/archive-time-stop-native-60fps.txt` was updated, triggering archive run #2 [44662755247](https://github.com/Nolane-x/video/actions/runs/44662755247). Verify that run and then verify the actual GitHub Release and assets.
- Inspect all contact sheets and moving proof around hard actions/contact/recovery before artistic sign-off. A green Actions run only proves technical validation. Preserve the 30fps fallback and explicitly report that the current style is stylized stick-figure animation, with a limited 3D rescue section.

- Visual review in the current session: all six contact sheets and representative frames from the rescue/action/recovery sequence were inspected. The sampled progression is coherent; no full frame-by-frame artistic sign-off has been made. Do not change `visual_approval` to true solely because CI passed.

## Time Stop 10s — definitive delivery status (2026-11-20)

- The native H2 60fps run #20 [44534851475](https://github.com/Nolane-x/video/actions/runs/44534851475) succeeded and has been archived. Master: 1920×1080, 60fps, 22,680 frames, 378.0 seconds, H.264 + AAC 48 kHz stereo. QA: −14.3 LUFS / −2.1 dBFS; 84 shot-synced Vietnamese VieNeu segments with AudioSeal watermark verified.
- Permanent public Release: https://github.com/Nolane-x/video/releases/tag/time-stop-10s-native-60fps-run-20 . Assets: native master MP4, 30s preview, review ZIP and SHA256SUMS. Release run #2 [44662755247](https://github.com/Nolane-x/video/actions/runs/44662755247) completed successfully.
- The first release workflow run failed because the runner had no checked-out git repository for `gh release create`; the archive workflow now checks out `github.sha` first. Run #2 is green and the Release plus asset list have been independently fetched and verified.
- Local conversation copies: `/mnt/data/time-stop-10s-native-60fps-1080p.mp4`, `/mnt/data/time-stop-10s-native-60fps-preview-30s.mp4`, `/mnt/data/time-stop-10s-native-60fps-review.zip`, `/mnt/data/time-stop-10s-native-60fps-subtitles.srt`, `/mnt/data/time-stop-10s-native-60fps-QA.json`, `/mnt/data/time-stop-10s-native-60fps-contact-sheet.jpg`, `/mnt/data/time-stop-10s-native-60fps-rescue-highlight.mp4`. The master SHA-256 is `ddb197588298ccd258c350299f69ce112558a76f89f6da96558500f9ccd75cec`, matching the Release asset digest.
- The 30fps run #18 remains a fallback. Interpolated 60fps run #5 is not a deliverable: its output is 22,677 frames, three fewer than target. Prefer native H2 output.
- Visual review: all six contact sheets plus representative rescue frames have been inspected. A complete frame-by-frame artistic sign-off has not been done. Do not set `visual_approval: true` based on technical CI success alone.

## Time Stop 10s — next 3D expansion handoff (2026-11-20)

Continue on branch `film/time-stop-10s-3d-cinema`. The previous native 60fps master remains the known-good fallback and permanent Release: https://github.com/Nolane-x/video/releases/tag/time-stop-10s-native-60fps-run-20 .

The new file `video-projects/time-stop-10s/scenes/shots/time-stop-key-sequences-3d.js` registers Three.js versions of 24 additional timeline shots across three sequences: kitchen `s013–s022`, basketball court `s026–s033`, and school hallway `s037–s042`. Existing street rescue scenes remain in `time-stop-3d.js`; total 3D coverage is 42/84 shots, not the entire film. The H2 workflow copies both scene modules into the temporary project and runs `node --check` before H2's whole-timeline scan.

Relevant commits: `3acdaaea8d0af3d55c0f3a28e671e62f8a46f633`, `9d2987a71527ca31d3aaf91f067d641223db548e`, `332ef8ef0231d80022e9db73d5d25579ab4ba268`.

Check current Actions [run #23](https://github.com/Nolane-x/video/actions/runs/44666071523). VoiceStudio has since passed and uploaded `video-voice-assets-44666071523` (artifact ID `14597918199`, 52,459,735 bytes): 84 Vietnamese VieNeu segments, 199.84s PCM_24 mono at 48 kHz, AudioSeal verified (7 blocks; minimum confidence 0.9979; mean 0.9995), SHA-256 `9ff05535036814429493fce21c4abf62990ebf6934243b3d094ee707ba3544df`. The H2 render/sound-mix/QA job is now in progress. Run #21/#22 were superseded/cancelled by later pushes, so inspect #23 rather than treating those as render failures. After it completes:
1. Verify storyboard import, H2 scan, 60fps full render, audio mix, ffprobe frame count/duration and QA.
2. Download its artifact; inspect all contact sheets and motion clips across 54.0–99.0s (kitchen), 112.5–148.5s (court), and 162.0–189.0s (hallway).
3. Check prop contacts, hands/feet, character framing and mother hair silhouette; captions must not duplicate or overlap the acting.
4. If the scenes pass, package a candidate master and new review bundle, preserving all old release hashes and leaving artistic approval false until complete review.
5. Update the film QA ledger and only publish a new permanent release after the review. Never call the whole film fully 3D: only 42 shots use Three.js; 42 remain H2 Canvas 2D.


## Time Stop 10s — source-level visual blockers discovered during 3D expansion (2026-11-20)

Before promoting run #23 or publishing a new Release, address these code-level issues. This list is based on source geometry/camera projection, not yet on a full playback review:
1. `s027` ball close-up is framed incorrectly: ball projects at normalized x≈+1.73 (outside frame) with the current [−0.8,2.65,7] camera looking at [−0.7,1.25,1].
2. `s032–s033` friend faces +X while the ball is to the friend's left. Rotate to face the ball; add a proper carrying pose / hand contact.
3. `s040` book pile is near hero x≈0.75, not child x=2.0; animate it toward the child's forearms.
4. `s041–s042` six books overlap nearly exactly (0.13 thickness vs 0.015 vertical spacing) and sit near foot level. Build an actual separated, held stack.
5. Mother outfit requests `head:'bun'` but H2 Three.js figure rig only implements `cap` and `beanie`; author real bun/hair geometry.
6. `s018` narration says nine seconds while HUD says seven. Fix the script and regenerate the 84-segment voice job; a wrist-timer line should ideally have a visible wrist device rather than only the top-left HUD.

Candidate run #23 [Actions](https://github.com/Nolane-x/video/actions/runs/44666071523) is currently intended to finish unchanged as a first review candidate. Do not cancel it solely to fix the above. Inspect its contact sheets, then apply these repairs in a focused follow-up render. Preserve run-20 master/release and never set artistic approval from CI status alone.


## Time Stop 10s — corrected 3D candidate handoff (2026-11-20)

Current corrected source branch: `film/time-stop-10s-3d-review-fixes`, head `0b43d44d85a666d7b5df23e119bde2ca6badfaff`. The correction pass:
- Reframed `s027` around the ball; it now projects to screen center (x≈0) rather than x≈+1.73 outside frame.
- Resized the basketball court, added an asphalt access road beyond the right end line, and made the ball drop/roll toward that road.
- Added a shared H2 Three.js `carry` pose. Friend faces the ball during `s032–s033`; child uses carry pose for hallway book shots.
- Added explicit mother hair-cap/bun geometry. The former `head:'bun'` parameter was not a supported rig token.
- Reblocked books to transfer toward the child's forearms and form two visibly separated columns of three books at torso height.
- Corrected `s018` framing and changed voice line to “Vòng đếm ngược báo còn bảy giây.” so it agrees with the 7-second HUD.

Full corrected candidate Actions [run #26 / 44671416000](https://github.com/Nolane-x/video/actions/runs/44671416000). Its story request job passed. VoiceStudio passed and uploaded `video-voice-assets-44671416000` (artifact ID `14599653357`, 52,525,240 bytes): 84 Vietnamese VieNeu segments, 200.24s PCM_24 mono/48kHz, AudioSeal verified (7 blocks; minimum confidence 0.9992; mean 0.9997), SHA-256 `30d756206f9a35183d2cdd0b82d5f4ef669d7af5dcd004da6f875fc342ea86fe`. Transcript confirms `s018`: “Vòng đếm ngược báo còn bảy giây.” The H2 full render job has started. Wait for this run's H2 render, QA and uploaded artifact before treating it as a new master.

For early source/motion inspection, use separate branch `review/time-stop-10s-3d-fixes` and workflow [run #1 / 44671703847](https://github.com/Nolane-x/video/actions/runs/44671703847). It skips VoiceStudio and full master, renders the 24 selected 3D shot contact sheets plus three silent 960×540/60fps clips: kitchen 58.5–85.5s, court 117–148.5s, and hallway 175.5–189s. Artifact name will be `time-stop-10s-3d-motion-review-<run_id>`.

Keep run-20 native 60fps Release/master as the fallback. The old local MP4 SHA-256 remains `ddb197588298ccd258c350299f69ce112558a76f89f6da96558500f9ccd75cec`; it is not the corrected candidate. Do not set `visual_approval: true` from a green CI state. Inspect the targeted proof clips and then review the full-length new master/audio before publishing.


## Time Stop 10s — current review state after first 3D motion proof

Motion-review workflow [run #1 / 44671703847](https://github.com/Nolane-x/video/actions/runs/44671703847) passed. It rendered 24 selected 3D-shot contact sheets and three silent exact-length 960x540/60fps motion proofs (kitchen, court, hallway). I inspected the kitchen and court contact/motion sheets and the two full 24-shot contact sheets.

What improved in the sampled evidence:
- Basketball close-up now stays in-frame; a clear court/road boundary is visible; the friend faces toward the ball for the s032-s033 return.
- Hallway books are no longer a nearly flat pile on the floor; they are separated and raised toward the child's arms.
- Kitchen cup freeze sequence is legible, but the s018 insert still cropped the protagonist's head at left and pushed the cup too far right.

Source fix e82a7591d6676e68f38aaea1271e92e8789c567b widens/recentres s018 and moves the protagonist to keep the face and cup visible. It triggered full workflow [run #27 / 44736403329]. At the last check, story payload preparation had passed and the VoiceStudio job was in progress. Wait for H2 render and QA before considering this new source final.

Run #26 [44671416000](https://github.com/Nolane-x/video/actions/runs/44671416000) completed successfully and produced artifact ID 14604975960 (time-stop-10s-h2-26, 258,272,318 bytes). Separate independent master inspection [run #2 / 44736526771](https://github.com/Nolane-x/video/actions/runs/44736526771) is currently running: download artifact, full MP4 decode, exact metadata/frame-count/audio validation, SHA-256, 24 frame contact sheet, and 1080p60 clips with the original mixed audio for each key sequence.

Keep the original run-20 public Release untouched. Do not publish until run #27 passes and the new master inspection plus visual review of full-mix clips are complete. visual_approval remains false.


## Time Stop 10s — latest verified status and next actions (2026-11-20)

Independent run-26 master inspection [run #5 / 44737356101](https://github.com/Nolane-x/video/actions/runs/44737356101) passed. Downloaded the actual run-26 master, separately decoded video/audio with FFmpeg, recomputed ffprobe with exact frame count, validated streams, and created 24 representative master frames plus 3 full-mix 1080p60 clips. Artifact `time-stop-10s-run26-master-inspection` ID `14629461926` (12,853,588 bytes) includes `master-inspection.json`, SHA-256, contact sheet and kitchen/court/hallway clips.
Run #26 technical values: 1920x1080; native 60/1 fps; 22,680 frames; 378.0s; H.264 + AAC stereo 48kHz; −14.3 LUFS; −2.0 dBFS; 84 Vietnamese VieNeu segments; AudioSeal verified. CI technical pass is still not full artistic sign-off.

Second targeted 3D proof [run #2 / 44736908508](https://github.com/Nolane-x/video/actions/runs/44736908508) passed after syncing the s018 framing correction. Artifact ID `14629681532`, 2,725,831 bytes, contains selected 3D shot sheets and 3 silent exact-length 960x540/60fps clips. Its renderer and frame-count QA passed.

The newest full candidate is run #27 [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329), branch `film/time-stop-10s-3d-review-fixes`, source commit `e82a7591d6676e68f38aaea1271e92e8789c567b`. VoiceStudio passed; H2 storyboard, module install, full shot scan, 84-shot sheets and 30s preview passed. At last check it was rendering the complete 1080p60 master. Voice artifact ID `14628059443` (52,634,924 bytes). Once completed, download the new `time-stop-10s-h2-27` artifact and update the inspection workflow default source run ID to `44736403329`; then run independent master inspection and inspect its s018 frame.

Inspection workflow iteration [run #6 / 44738517112](https://github.com/Nolane-x/video/actions/runs/44738517112) is also running. It emits a compact montage as base64 in job logs so the image can be inspected without relying on the unavailable container runtime.

Keep the run-20 public Release immutable. Keep run-26 candidate as fallback. Do not publish a new Release or mark artistic approval true until run #27 passes independent QA and the full-mix clips/master visuals have been reviewed.


## Time Stop 10s — archive run-27 draft (prepared, not yet activated)

Workflow .github/workflows/archive-time-stop-10s-expanded-run28.yml has been added to film/time-stop-10s-3d-review-fixes. It is deliberately gated by .github/workflows/enable-time-stop-10s-expanded-draft.txt (or workflow_dispatch). It validates run-27's 1080p60 master, exact 22,680 frames / 378s, AAC 48kHz stereo, 84 Vietnamese VieNeu segments and AudioSeal. It then builds an immutable draft release tagged time-stop-10s-expanded-3d-review-run27, carrying master MP4, preview, review ZIP, QA, voice placement, SRT and hashes. The release stays a draft and visual_approval remains false.

Do NOT create the marker until run #27 succeeds and its own independent inspector passes. Preserve run-20 public release. Current run #27 is still at the full master render step; proof workflow #4 is running after adding the Pillow dependency for the compact visual montage.


### Exact checksum for run-26 master

Independent run #5 [44737356101](https://github.com/Nolane-x/video/actions/runs/44737356101) passed. The actual master inside artifact 14604975960 is 98,061,158 bytes with SHA-256 7184018d36b5dd28284a6621ba66802764e03c95bd7050efc350a3b7140f871a. It was fully decoded with FFmpeg: both video and audio return code 0. ffprobe: 1920x1080, H.264, 60/1 fps, 22,680 frames, 378.000s, AAC stereo 48kHz. Integrated loudness -14.3 LUFS; peak -2.0 dBFS; 84 Vietnamese VieNeu segments; watermark verified.
Inspector #6 [44738517112] passed and its artifact 14629966995 (12,853,637 bytes) contains the 24-frame contact sheet, sampled stills, full-mix clips and checksum. Proof run #4 [44739190519] is rerunning the selected 3D shots after installing Pillow for a compact visual montage.


## Time Stop 10s — visual proof after s018 reframe

Proof workflow [run #4 / 44739190519](https://github.com/Nolane-x/video/actions/runs/44739190519) passed (20/20 steps). Artifact ID `14630392510` contains 24 selected 3D-shot sheets, the 8-image montage and three exact-length silent 960x540/60fps clips.

I directly inspected the compact montage in its job log: the revised s018 now shows the protagonist's full head/face, suspended cup and readable 7-second HUD in frame. The ball close-up (s027), friend ball return (s032–s033), and elevated book stack/child interaction (s040–s042) also read within frame. This is targeted proof, not full-film artistic sign-off or proof of perfect physical contacts.

The full run-27 master [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) is still rendering at the native 1080p60 silent-master step. Once completed: verify sound mix, package, download artifact, update inspector source run ID to 44736403329, independently decode/measure the master and view its own s018 sample before activating the gated draft Release. Keep visual_approval false.


## Time Stop 10s — new s026 hand-contact fix; run-28 supersedes run-27

A further source audit found a visible prop-contact gap in s026: the friend rig's right-hand center is approximately x=2.60, y=1.47, z=1.10, but the basketball had started at x=2.5, y=1.08, z=1.1. Fixed in f630e863c2b118cdb3e6c7ecc28fb4479783059e by moving the friend to z=0.9 for this shot and starting the ball at [2.6,1.47,1.1] before its drop/bounce toward road x=7.45. Synced to review branch at 6fba5daf0d2285f1df3944cd8c1be4d13b30b040.

Run #27 [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) is not a deliverable: it was cancelled at the full silent master render step when the new contact fix was pushed. No mixed master or upload completed. Run #28 [44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) now includes both the s018 full-head/cup reframe and the s026 hand-aligned ball start. Story job passed; the VoiceStudio job is currently in progress. Wait for H2 master, QA and upload.

Proof run #5 [44740324018](https://github.com/Nolane-x/video/actions/runs/44740324018) is targeted 3D proof for the latest source. Inspect s026 at t=112.5–117s specifically (not only s027 at 117s), plus ball handoff, books and s018. Run-26 remains the only fully decoded and independently verified full candidate until run-28 completes and gets its own independent inspector.


## Run #28 latest checkpoint

Full candidate [run #28 / 44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) has passed storyboard payload and VoiceStudio. Voice artifact ID `14630746223` (51,951,746 bytes), 84 Vietnamese VieNeu segments, duration 198.00s, 7 AudioSeal blocks verified; ZIP SHA-256 `ecf9a37e67ec154ebad86eaaec24629448447d6a1fccb8e3bf20aa46aa43001a`. H2 render job has started and was installing H2/audio dependencies at this checkpoint.

The source includes both s018 full-face/cup reframe and s026 ball-to-hand start at x=2.6/y=1.47/z=1.1, friend z=0.9. Review proof [#6 / 44740517436](https://github.com/Nolane-x/video/actions/runs/44740517436) includes s026 frames 112.5s/114.75s and a court proof clip from 112.5–148.5s; it has installed the source modules and is scanning all 84 shots. Run #27 is cancelled and not a deliverable. Run #26 remains a technical fallback but predates s026 contact improvement and has the prior s018 framing.


## Inspector gate for run-28

Inspector run #7 [44740902252](https://github.com/Nolane-x/video/actions/runs/44740902252) failed before media checks: the run-28 artifact name did not exist yet because the full render was still active. The inspector workflow has been changed to require marker .github/workflows/enable-inspect-time-stop-run28.txt (or manual dispatch), so it cannot run before upload. Create that marker only after run #28 has successfully uploaded time-stop-10s-h2-28; then perform independent full decode, ffprobe/frame count, audio and checksum checks.


## Proof #6 result — latest s026 contact proof

Proof run #6 [44740517436](https://github.com/Nolane-x/video/actions/runs/44740517436) passed all 20 steps. Artifact 14632040618 (2,826,667 bytes) contains 24 shot sheets, a 10-image montage and three exact-length silent clips:
- kitchen 58.5–85.5s: 960x540, 60fps, 27.0s, 1,620 frames;
- court s026–s033 112.5–148.5s: 960x540, 60fps, 36.0s, 2,160 frames;
- hallway 175.5–189s: 960x540, 60fps, 13.5s, 810 frames.

I visually inspected the montage: s026 first sample (112.5s) places ball adjacent to the friend's extended hand; at 114.75s ball has moved toward the road; s027 at 117s shows ball close-up. s018 full face/cup/timer all remain visible. Handoff and book-rescue samples also stay inside frame. This is targeted proof only; leave visual_approval false. Run #28 44740306234 is still rendering the complete master and needs mix/QA/upload plus its own independent inspector.

## Handoff — Time Stop 10s run 28 (2026-11-20)

Latest source candidate: branch film/time-stop-10s-3d-review-fixes, follow-on commit f630e863c2b118cdb3e6c7ecc28fb4479783059e. It retains the s018 wider/recentered camera and adds a basketball start alignment fix: friend is moved to z=0.9, ball begins at y=1.47 near the friend's outstretched hand, then drops/rolls toward road. The updated motion proof's source bundle contains both fixes.

Run #27 [44736403329](https://github.com/Nolane-x/video/actions/runs/44736403329) was cancelled at 8,746 / 22,680 frames because a new commit triggered concurrency cancellation; it did not fail its renderer. Run #28 [44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) was triggered by the ball release change and has passed:
- Story request preparation
- VoiceStudio 84 Vietnamese narration segments (artifact ID 14630746223)
- H2 toolchain, 84-shot storyboard, voice placement, 3D module install
- Full shot scan
- 84-shot contact sheets and 30s motion preview

At last status check the H2 job was rendering the complete 1080p native-60fps master. No run-28 master artifact is uploaded yet. Do not claim run #28 is complete.

Targeted proof [run #6 / 44740517436](https://github.com/Nolane-x/video/actions/runs/44740517436) succeeded, artifact ID 14632040618. I extracted and inspected:
- Kitchen: cup fall/freeze, protagonist entrance, reaching/steadying close-up; s018 is now framed without cropping the character's head.
- Court: ball starts in friend's hand, leaves hand, rolls toward road edge; protagonist runs, retrieves and returns the ball; friend faces him at hand-off.
- Hallway: both arms receive the book stack at torso height and the hero steps back. No clip frame-count failures.
This is targeted sampled visual review only, not a full-length artistic sign-off.

The run-26 independent master artifact inspection [run #6 / 44738517112](https://github.com/Nolane-x/video/actions/runs/44738517112) passed technical full-decode, audio/video stream and exact frame validation; artifact ID 14629966995. Run-26 still has the prior s018 crop and pre-ball-start alignment, so it remains fallback, not preferred final.

Patched archive workflow file .github/workflows/archive-time-stop-10s-expanded-run28.yml at commit 49e80e9d to target run ID 44740306234, artifact time-stop-10s-h2-28, and tag time-stop-10s-expanded-3d-review-run28. The enabling marker has not been added: wait until run #28 master upload/QA exists, then trigger the archive draft workflow, verify the artifact and create draft release. Retain the existing public run-20 release.

Next steps:
1. Poll run #28; require all H2 QA and artifact time-stop-10s-h2-28.
2. In .github/workflows/inspect-time-stop-run.yml, change default/source run ID from 44671416000 to 44740306234 and artifact name from time-stop-10s-h2-26 to time-stop-10s-h2-28; trigger via the existing workflow path and inspect the new master.
3. Visually review full-mix kitchen/court/hallway clips plus s018/s026 contact frames.
4. Only then create a draft release through the updated archive workflow. Do not set visual_approval true.


Run #28 VoiceStudio artifact (ID 14630746223): 84 Vietnamese VieNeu segments; 198.00s PCM_24 mono 48kHz; checks passed; AudioSeal verified with 7 blocks, minimum confidence 0.9962 and mean 0.9993. WAV SHA-256 84ad2d365d1597a2414d3d2d9fdd458cbf2dd8ee13d31af1dcc542e2ffe9f92e matched the manifest. Subtitle cue s018 confirms “Vòng đếm ngược báo còn bảy giây.” User-facing copies are /mnt/data/time-stop-10s-run28-voice-assets.zip, /mnt/data/time-stop-10s-run28-subtitles-vi.srt and /mnt/data/time-stop-10s-run28-transcript-vi.txt. The voice track is verified; the full run-28 video master is still being rendered.


## Handoff — run 28 rendered, independent QA pending

Current corrected source branch: `film/time-stop-10s-3d-review-fixes`. Latest full render run [#28 / 44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) has completed with success:
- VoiceStudio 84-segment job: passed.
- H2 render/mix/QA: 24 steps passed.
- Full native 1080p60 master artifact `time-stop-10s-h2-28`, artifact ID `14636737019`, 258,555,982 bytes.

Confirmed run-28 QA values: 1920x1080, native 60/1 fps, 22,680 frames, 378.0s, H.264, AAC 48kHz stereo, −14.2 LUFS, peak −2.9 dBFS, 84 story shots, 26 time-freeze FX shots, 84 shot-synced Vietnamese VieNeu segments, AudioSeal watermark verified. `visual_approval` remains false.

Run-28 voice artifact ID 14630746223: 84 Vietnamese segments, 198s PCM_24 mono/48kHz; manifest SHA and WAV hash match; AudioSeal 7 blocks, min confidence 0.9962, mean 0.9993. WAV SHA-256: `84ad2d365d1597a2414d3d2d9fdd458cbf2dd8ee13d31af1dcc542e2ffe9f92e`. Transcript/srt s018 line matches “Vòng đếm ngược báo còn bảy giây.”

Latest selected-shot motion proof run #6 [44740517436](https://github.com/Nolane-x/video/actions/runs/44740517436) passed and sampled the corrected camera/ball/book blocking.

Independent run-28 inspection [44760145701](https://github.com/Nolane-x/video/actions/runs/44760145701) is running on `time-stop-10s-h2-28`; it separately decodes video/audio, checks ffprobe frame count and metadata, creates a contact sheet and three full-mix 1080p60 sequence clips. Wait for conclusion success and its inspection artifact before archiving.

Draft archive workflow path is now `.github/workflows/archive-time-stop-10s-expanded-run28.yml`; artifact target `time-stop-10s-h2-28`, run ID 44740306234, tag `time-stop-10s-expanded-3d-review-run28`. Do not create the enabling marker until independent inspection passes. Existing run-20 public Release is preserved and must not be overwritten.


## Handoff — run28 independently verified; draft archive is next

Run #28 [44740306234](https://github.com/Nolane-x/video/actions/runs/44740306234) completed successfully and uploaded time-stop-10s-h2-28 artifact ID 14636737019 (258,555,982 bytes). Independent master inspection [run #8 / 44760145701](https://github.com/Nolane-x/video/actions/runs/44760145701) also completed successfully and uploaded artifact ID 14641660047 (13,045,106 bytes).

Verified master SHA-256: d299ac9e74f0efcbb86822280f6d3baa5c0710647c0155405e37eb0180542fc0. Full MP4 decode succeeded. 1920x1080, 60/1 fps native H2 frames, 22,680 frames, 378 seconds, H.264 + AAC stereo 48kHz, −14.2 LUFS, −2.9 dBFS, 84 shot-synced Vietnamese VieNeu narration segments; AudioSeal verified. QA sets visual_approval false.

Visual review:
- Master contact sheet inspected; s018 framing now keeps the protagonist's head and reach arm visible; s027 ball is in frame; s032 hand-off is readable; s040–s042 book carry/transfer/recovery is legible.
- Full-mix clips extracted from the run28 master and fully decoded independently: kitchen 45s / 2,700 frames, court 36s / 2,160 frames, hallway 27s / 1,620 frames. All are 1080p60 with AAC stereo 48kHz.
- This is targeted visual inspection; do not represent it as an uninterrupted full-length screening.

User-facing local review ZIP: /mnt/data/time-stop-10s-run28-review-package.zip (65,369,947 bytes). Contains master-inspection evidence, 24 sampled frames, three full-mix clips, their sampled contact sheets, Vietnamese SRT/VTT/transcript, voice WAV and full voice-assets archive. Standalone files under /mnt/data/time-stop-10s-run28-*.

Next, trigger the QA-gated draft archive by creating .github/workflows/enable-time-stop-10s-expanded-draft.txt on film/time-stop-10s-3d-review-fixes. It runs .github/workflows/archive-time-stop-10s-expanded-run28.yml, downloads artifact time-stop-10s-h2-28 from run ID 44740306234, and creates draft tag time-stop-10s-expanded-3d-review-run28. Verify the archive workflow succeeds and its assets/checksums match. Do not publish the draft as a public release until an uninterrupted full-length watch; preserve run-20 release.


## Handoff — run28 archived as a verified draft release

Archive workflow [run #2 / 44761976792](https://github.com/Nolane-x/video/actions/runs/44761976792) completed successfully. It downloaded the run28 H2 artifact, validated the QA/narration/subtitle payload, uploaded archive artifact ID 14642261070 (462,018,811 bytes), and created draft GitHub Release ID 452849739.

Draft details:
- Tag: `time-stop-10s-expanded-3d-review-run28`
- Title: “Time Stop 10s — Expanded 3D Review Candidate (Run 28)”
- Draft URL currently returned by GitHub: https://github.com/Nolane-x/video/releases/tag/untagged-52cf422ee96cca7743e1
- The release remains `draft: true`, not public.

Release assets verified through GitHub API:
- `time-stop-10s-expanded-3d-review-1080p60.mp4`, 98,485,406 bytes, digest SHA-256 `d299ac9e74f0efcbb86822280f6d3baa5c0710647c0155405e37eb0180542fc0`, identical to independent inspection master hash.
- `time-stop-10s-expanded-3d-review-preview-30s.mp4`, 4,066,016 bytes, SHA-256 `f73d8e6942215c421c58c7ea57583567f96fd26b56544436ccd2bdd5cf79b17b`.
- `time-stop-10s-expanded-3d-review-bundle.zip`, 129,354,701 bytes, SHA-256 `825aae7342f085d8cd810929c3225f922345c941c2f8472303580fbbc0122952`.
- `SHA256SUMS.txt`, `REVIEW-NOTES.md`.

User-side full review package: `/mnt/data/time-stop-10s-run28-review-package.zip` (65,369,947 bytes); standalone SRT/VTT/transcript/WAV/master contact sheet/three 1080p60 mixed clips also at `/mnt/data/time-stop-10s-run28-*`.

Do not publish the draft release as public until uninterrupted full-length screening is done. Keep `visual_approval: false`. Preserve public run-20 release.

## Handoff — s002 camera correction; run 29 in progress (2026-11-21)

Repository: Nolane-x/video
Branch: film/time-stop-10s-3d-review-fixes
Latest source commit: 57c6ab294bba89acfdd0e79c20c9f817febf3aa9

### Why this change was made
A dense review of the Run-28 master sampled three instants (+0.75s, +2.25s, +3.75s) for every 4.5-second shot: 252 frames across all 84 shots. This was not an uninterrupted screening. A specific defect was found in s002: its written action is an alarm-clock insert, yet the current camera clipped the bedside digital clock, leaving only part of the character in frame.

The diagnosis was checked against the bedroom set in integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit/packs/dem/sets.js (clock at nx, gy - 97) and camera cropping in .../packs/dem/templates.js (center clamp plus zoom). The camera in only the s002 add(...) block of video-projects/time-stop-10s/scripts/build_story.py was changed:
- Before: camera(.62,.30,1.32,.63,.30,1.50)
- After: camera(.56,.44,1.16,.57,.44,1.25)
The scene caption, time 06:10, actor/pose, SFX and remaining shots were preserved.

### Current workflow
Full render Run #29: https://github.com/Nolane-x/video/actions/runs/44870641689
Source commit: 57c6ab294bba89acfdd0e79c20c9f817febf3aa9
At handoff snapshot, job 'Build per-shot Vietnamese narration request' passed; VoiceStudio was installing CPU inference/audio dependencies. H2 render, master artifact and QA are not yet confirmed. Check run status/jobs/artifacts before making claims.
Expected artifact name if the run succeeds: time-stop-10s-h2-29

### Next actions
1. Poll Run #29; require all jobs green and the time-stop-10s-h2-29 artifact.
2. Verify story/shots.json contains s002 camera from=[0.56,0.44,1.16], to=[0.57,0.44,1.25] (or equivalent generated fields), 84 shots and total 378s.
3. Inspect s002 at +0.75s/+2.25s/+3.75s (5.25s, 6.75s, 8.25s) from the actual run29 master and ensure the full alarm clock is clearly visible, readable at 1080p, without sacrificing the protagonist/scene context.
4. Generate 3 samples for each of the 84 shots (252 frames), inspect all six contact sheets, compare high-risk action sequences, and rerun full master FFmpeg decode + ffprobe, frame count, audio format, loudness and SHA-256 verification.
5. Only after successful run29 QA, create a separate run29 draft archive/release using a new tag/name. Preserve the run28 draft and run20 public release; never overwrite either. Keep visual_approval false until an uninterrupted full-length watch-through is performed.

Run28 remains a valid previous technical candidate (details immediately above in this handoff); it is superseded by source commit 57c6ab2 for the s002 framing issue, but its master/draft archive remain immutable and available for comparison.
