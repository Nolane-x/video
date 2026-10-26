# Video Studio — current state snapshot

Snapshot updated 2026-10-26 after **THE FIRST HOUR** H2 render candidate passed the complete CI pipeline (run #26). Technical QA and targeted visual/motion spot-checks passed. The complete 172-second film has **not** yet had a real-time, start-to-finish artistic review with audio; keep artistic sign-off pending. The previously archived ONE MORE SCROLL canonical master remains unchanged.

## Latest active film — THE FIRST HOUR

- Manifest: [video-library/the-first-hour/manifest.json](../video-library/the-first-hour/manifest.json); QA notes: [video-library/the-first-hour/QA.md](../video-library/the-first-hour/QA.md).
- Engine: native H2 SelfImprove Studio Canvas/Chromium render + FFmpeg mix/master; not Remotion.
- Source commit: `6eba384b4babde94f030371d5c9904c483fcbef3`.
- CI: [run #26 — passed](https://github.com/Nolane-x/video/actions/runs/40329265743), every workflow step green.
- Master: 172.000 s, H.264 1920×1080 @24/1, AAC 48 kHz stereo; integrated loudness −14.1 LUFS, LRA 6.8 LU, true peak −2.5 dBFS.
- MP4 SHA-256: `75b4172e47735368bb0070b50273ce12fb0248a460a5930c78cd19abb26e82a8`; 26,696,094 bytes.
- Review ZIP SHA-256: `e0e514ee6cd048ad2d389a536c6c899297f77755e7d551cfd303193435dbfa3f`; includes the master, preview, two full shot sheets, reports and 12 six-second audio/video motion proofs. All 24 checksums listed inside the review bundle were verified locally.
- Actions artifact: [the-first-hour-h2-selfimprove-26](https://github.com/Nolane-x/video/actions/runs/40329265743), artifact ID `12653272820`, ZIP SHA-256 `f7b6c6b6cac7ac0f76d10856d8a6e0c62d9351f9ba249ed3162feab9c2acef2a`. This is temporary Actions storage, **not** a durable release archive yet.
- Visual sampling: both 29-shot contact sheets reviewed; notebook writing (b20) and punch-bag (b25) motion proofs inspected. The notebook no longer leaks characters from the next line; the bag visibly tilts/recoils at timed impacts after the gym-set wiring fix. The other 10 proof files are stream/duration validated, not all individually watched.
- Next gate: full 172-second playback with audio, checking transitions, text readability, acting, all prop contacts and sound/story pacing; then archive the candidate to a durable release and update its status. Do not mark fully artistically approved based on CI or contact sheets alone.

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

## Verified latest state
- **H2 source-v3 full render and Release packaging passed:** [workflow run 40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324), all required steps successful, including the previously failing review-bundle checksum/publish step.
- Candidate: [source-v3 H2 MP4](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/one-more-scroll-h2-source-v3-shoelace-fix-candidate.mp4), SHA-256 `761d238ae019e6c39eca3a9c46bff88b02f6f96e332f35d6e5d6b0d41e29310f`, 33,409,690 bytes. Review ZIP: [source-v3 review package](https://github.com/Nolane-x/video/releases/download/h2-production-assets-v1/h2-source-v3-shoelace-fix-review.zip), SHA-256 `56bf506a0ec63fbb9d99256ac1cc989186f6ddab12056c9cfb9f012b922d0745`, 33,709,840 bytes.
- Verified streams: 155.000s, 1920×1080 @24fps, H.264 + AAC stereo 48 kHz. EBU R128: −14.0 LUFS integrated, 6.9 LU LRA, −2.4 dBFS true peak.
- First attempt [40281627022](https://github.com/Nolane-x/video/actions/runs/40281627022) passed rendering/audio but omitted the pinned patch script from the review payload. The corrected workflow copies the patch before checksum generation, verifies required files and uploads the candidate/review assets separately.
- Portable skill package last passed in [run 40287442899](https://github.com/Nolane-x/video/actions/runs/40287442899): ZIP integrity, 176 entries, Remotion run-36 sample, canonical H2 master, H2 production overlay and plugin v1.1.0 all verified. That build's sidecar SHA-256 was `cf6257467655f73fedd715cf5ce2380c73aa30b855df1b6ae6605945d67f8635`; this manifest/docs change triggers a fresh package build, so recheck the newest run and sidecar.
- Canonical H2 master remains unchanged: `video-library/one-more-scroll/one-more-scroll-h2-final.mp4`, SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`. Source-v2 and source-v3 are separate non-canonical candidates.
- Source-v3 is a **technical pass, not artistic sign-off**. I sampled the shot-b17 motion at 4 fps around 80–84 seconds: the forward crouch and alternating arm motion are visible, but the hand-to-shoe/lace contact remains ambiguous because the actor is too small in the wide shot. Treat this as a P1 visual defect. Next: build a source-v4 3–6 second focused preview with clearer composition and actual hand/lace contact; review that preview before any new full render. Full candidate playback with audio, pacing, transitions, sync and emotional arc still require review.

## Next priorities
1. **P1:** create and inspect a source-v4 focused shoe-tie preview; make the hand/lace contact legible at actual viewing size before full render.
2. Watch the complete source-v3 candidate with audio and review close-up rhythm, transitions, synchronization and emotional arc.
3. Verify the newest portable bundle run and SHA-256 sidecar after manifest sync.
4. Preserve canonical master hash until an explicitly approved candidate exists.

## Prior work catalog and reusable archive tooling
- The [previous-work catalog](../video-library/previous-works-catalog.json) records older H2/remotion/cinematic iterations, their exact checksums and whether they are available only in the production workspace or archived in GitHub.
- The prior-works import tool is `tools/video/archive_previous_works.py`. It stages matched video attachments by hash; GitHub workflow then verifies remote bytes and generates contact sheets.
- The H2 source publisher is `tools/video/publish_h2_source_release.ps1`; source ZIPs should be stored as verified GitHub Release assets, not huge regular Git blobs.
- The current portable skill ZIP includes both the Remotion reference MP4 and the checksum-verified canonical H2 MP4. It also includes `video-library/reference-clips.json`, which preserves your two reference-video URLs and study prompts; standalone copies of those third-party MP4s were not found in the current workspace/Library and are not embedded. It does not bundle every historical clip; use the catalog for availability and provenance.

## Latest H2 source-v2 render candidate
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
