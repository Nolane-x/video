## Follow-through update — 2026-11-08, after full-film visual review

- The Squire master remains a **technical pass, not an approved film**: run [42449792684](https://github.com/Nolane-x/video/actions/runs/42449792684), 957.9 s, 1920×1080, 240/240 fps, 229,896 frames, 586 shots / 434 custom shots. The full-film contact sheet has now been visually inspected; repeated flat vector characters, formations and template backgrounds remain unacceptable for the requested cinematic look.
- The separate 3D bombardment workflow has been split into six native-240fps frame chunks. Run [42487879116](https://github.com/Nolane-x/video/actions/runs/42487879116) has chunks 01 and 06 completed (1,566 and 1,564 frames, each about 6.5 s); chunks 02–05 were still rendering at the latest check. A prior run [42485801702](https://github.com/Nolane-x/video/actions/runs/42485801702) is also still active and is a duplicate attempt. Do not claim the 39.14 s sequence is assembled until all six chunks, concat, audio mix and QA finish.
- First available Blender chunk previews have been inspected. They are 1920×1080 CFR 240/240, but the people and much of the environment still read as low-poly/stylized models, not cinematic realism. This is a useful technical 3D proof only; do not approve it as the film's visual target. Use detailed CC0 models/materials for cannon, fort and ship, keep human figures distant/silhouetted unless better rigs are obtained, and add more convincing lighting, atmosphere, debris and motivated action.
- The asset discovery workflow is [run 42492813906](https://github.com/Nolane-x/video/actions/runs/42492813906), currently processing the pinned asset-library manifests and Poly Haven models. It uses the official Poly Haven model /files API and only the three model IDs cannon_01, modular_fort_01, and ship_pinnace. The current code selects the glTF branch and imports glTF with Blender; the .blend path was rejected by Blender 4.0.2 despite the API URL suffix. Preserve each model's CC0/license/hash and include manifest in any downstream bundle. Wait for preview artifact before integrating models into the active Blender scene.
- The master-inspection workflow is [run 42492431821](https://github.com/Nolane-x/video/actions/runs/42492431821). It has downloaded the 2 GB Squire artifact and is generating FFprobe report, whole-film contact sheet and 30fps review proxy. The source-path bug was fixed in commit b5fec029abf7f7d5e3f4dae532fe2a8a9a19097b; wait for inspection artifact before claiming this job is done.
- Public-domain visual reference: Jean Le Tavernier's *Le siège de Constantinople (1453)*, created after 1455, is preserved by the BnF and listed as Public Domain on Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Le_si%C3%A8ge_de_Constantinople_(1453)_by_Jean_Le_Tavernier_after_1455.jpg. Treat it as a contemporary medieval miniature / period visual evidence, not a literal camera record.
- Next gate: review the Poly Haven model previews and the remaining Blender chunks; integrate only models that materially improve close-up detail; produce a 10–20 s polished proof with distinct action and a normal-speed review before starting another long-form render. Keep the Squire master as backup, not final. Audio beds/Foley are still not human-auditioned or approved.

# AI session handoff

## Current active film work — Constantinople 1453 (2026-11-08 latest)

User wants a substantially better cinematic historical documentary, not a flat vector explainer. Requirements retained: English narration/captions, 1920×1080, very high frame-rate output (target 240fps), stronger and more detailed movement, historical accuracy and delivery through GitHub Actions. Do not render on the user's low-spec local PC, do not use Remote Desktop Commander, and do not claim a successful render is artistically approved.

- **Squire master complete, but not accepted creatively:** [run 42449792684](https://github.com/Nolane-x/video/actions/runs/42449792684), branch `squire/constantinople-1453-240fps`, source commit `a65d369ae07984469306dd80839c7d96f74bbb1d`. All render/mix/strict-HFR-QA/upload steps passed. Master artifact ID `13611674134`, 2,023,692,938 bytes; review artifact ID `13604509897`. 12-second proof metadata is 1920×1080, 240/240 fps, 2,880 frames.
- **Visual inspection rejects it as final:** project sets `style: "flat"`; Squire pack is intentionally cartoon/vector-history animation. Full master contact sheets show repeated army rows, simplistic characters and flat map/prop inserts. Retain as a working technical reference/backup, not the final film.
- Master inspection workflow is active on `inspect/squire-master-artifact`, [run 42477549638](https://github.com/Nolane-x/video/actions/runs/42477549638). It downloads the 2 GB artifact within GitHub Actions and generates a compact output: QA report, ffprobe, whole-film contact sheet and a normal-speed 30fps low-resolution review proxy. Check its artifact after completion.
- Voice artifact [run 42448341267](https://github.com/Nolane-x/video/actions/runs/42448341267) has a verified 15:56 PCM-24 / 48 kHz mono narration with SHA-256, AudioSeal and narrator-selection checks. Reuse that exact source.
- Squire redesign proof [run 42459027169](https://github.com/Nolane-x/video/actions/runs/42459027169), artifact `13609059158`, is CFR 240/240 and technically decodes; it remains visually flat and is not artistic approval.
- Blender proof [run 42461960154](https://github.com/Nolane-x/video/actions/runs/42461960154) passed the one-frame smoke render but the full 9,394-frame 1080p pass was cancelled at the workflow's 180-minute ceiling; no proof artifact. Its generated primitive scene should not be treated as acceptable 3D quality.
- Historical asset discovery is active on `inspect/constantinople-asset-candidates`, [run 42478240580](https://github.com/Nolane-x/video/actions/runs/42478240580). It reads the repo's pinned asset library (Wikimedia, The Met, Rijksmuseum, LOC, Poly Haven, ambientCG and Kenney) for relevant 1453/Byzantine/Ottoman assets and inspects model archive contents. Preserve exact source/license/hash information for every selected asset.
- **Next production direction:** use real rights-cleared archival/historical imagery, museum objects, maps and manuscript illustrations as evidence-led source material; make them cinematic with layered depth, parallax, motivated camera moves, light/shadow and strong action choreography. Use detailed 3D for only the shots that need spatial reconstruction (bombard, wall breach, ships hauled overland, Golden Horn geography and final assault). Label 3D as illustrative. Avoid static repeated army rows, generic iconography and generic map slides.
- Render a 10–20s representative proof first, with actual movement and all key visual layers, and validate the normal-speed proxy before rendering the full 15–16 minute film. Optimize Blender by scene complexity, chunked rendering or a lower source sampling rate followed by a documented interpolation stage only if native 240fps full rendering is prohibitively slow; do not silently pretend interpolated frames are native-rendered frames.
- Audio source manifest verifies CC0 rights and checksums, but all music and Foley candidates remain `human_auditioned=false` and `approved_for_final_mix=false`. The full mix needs a real human listen-through.
- Final approval requires full start-to-finish picture/audio review, timecoded defects, subtitle/credits/rights checks and an explicitly accepted artistic review. No artifact should be called final merely because CI is green.

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

## AI handoff — 2026-11-13, final-night sequence and parallel PBR proof

### Source changes already committed

- Branch: `squire/constantinople-1453-redesign`.
- Scene/authoring change: `24872b21de69cdc01853bf7ab1fc79ee74baac1b`.
- Dawn-assault selection correction: `b1bd36e1f2882b8093159dbe4e7bfeb92fd21977`.
- Files changed: `tools/video/author_squire_constantinople.py`, `tests/test_squire_constantinople.py`, `video-projects/squire/constantinople-1453/scenes/shots/constantinople-cinematic.js`, and `video-projects/squire/constantinople-1453/story/03-VISUAL-DIRECTION.md`.
- New custom templates: `night_camp`, `night_guns`, `night_gun_crew`. The classifier prioritizes the final assault and the Ottoman camp/artillery beats over the generic first-5.5%-of-film night rule. SFX cues use existing recorded battle/wind/cannon sources where present. The protagonist is not staged in the Ottoman gun crew.
- Static production suite run [43448502521](https://github.com/Nolane-x/video/actions/runs/43448502521) passed. Cinematic proof run [43448502373](https://github.com/Nolane-x/video/actions/runs/43448502373) was at scene/contact-sheet scanning at last observation; then it must mix proof audio and render the moving 240fps montage. Inspect its artifact rather than assuming visual quality from CI.

### Immediate next actions

1. Finish run 43448502373 and inspect its contact sheets / moving proof. Verify the three new night templates are represented and visually distinct.
2. Extend `tools/video/render_squire_constantinople_redesign_proof.py`'s `CUSTOM` list with the three new templates. Add a contiguous native-240fps opening preview (target 65 seconds) and a 4×4 contact sheet sampled about every four seconds; copy both into the review artifact. Keep this a proof, not a full-master render.
3. Extend `progress_phase` to classify “To understand that night, we have to return to the morning of the sixth of April” as the first-day `camp` chapter, and add a regression test that `choose_template` produces `command_camp` for that rewind cue.
4. Inspect the assembled PBR v4 result from [run 43439300571](https://github.com/Nolane-x/video/actions/runs/43439300571), compare to v3 [run 43437648364](https://github.com/Nolane-x/video/actions/runs/43437648364), and decide whether the 16-second 3D proof is useful or needs a narrower close-up / less empty foreground. Both are parallel technical candidates and neither replaces the Squire master.
5. Keep the Supertonic voice set from [run 43438201324](https://github.com/Nolane-x/video/actions/runs/43438201324) as an audition only. It contains Adam, Kokoro Heart/Bella and M1–M5/F1–F5; the model is OpenRAIL-licensed. Do not switch the actual narration without explicit human selection and a full voice review.

### Non-negotiable review status

The existing long-form 240fps master remains the known-good technical archive, not an artistic approval. Do not trigger `[full-render]`, overwrite the master, or declare the redesigned film complete until the contiguous opening preview, every custom scene's motion/contact behavior, the full sound mix and the complete film have been reviewed.
