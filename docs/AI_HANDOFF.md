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
