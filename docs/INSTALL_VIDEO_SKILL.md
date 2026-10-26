# Installing/restoring the video-production skill

This repo itself is the canonical skill workspace. Start by cloning/opening `Nolane-x/video`, then tell the agent to follow root `AGENTS.md`.

## ChatGPT Plugin Creator

The private plugin [h2-selfimprove-studio](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) is active at **v1.1.0**, current release `pluginrel_6ade248942988191a57ff1059c818720` (confirmed by Plugin Creator on 2026-10-25). Open the link in ChatGPT and ensure it is available to the current workspace. See `docs/CHATGPT_PLUGIN.md` for release evidence and contents. The GitHub mirror preserves the v1.0.2 base source and keeps the v1.1.0 production overlay separately. The cross-engine master skill in this repository remains the production policy of record.

## Recommended use by agent family

- **Codex / OpenCode / agents honoring AGENTS.md:** read `AGENTS.md`, then `.agents/skills/video-production-master/SKILL.md`. Copy the complete `.agents/skills/video-production-master/` directory, not just the entrypoint.
- **Claude Code:** also read `CLAUDE.md` and `.claude/skills/video-production-master/SKILL.md`. The adapter points back to the canonical skill; it should not fork policy.
- **Other AI workspaces:** provide `AGENTS.md`, the entire `.agents/skills/video-production-master/` tree, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/ART_DIRECTION_IFVERSE_DAYONE.md`, and `video-library/`. Preserve the folder paths because references are relative.

## Do not copy only the prompt

The skill needs the real assets/source maps and state files to avoid losing context:
- Remotion source + storyboard: `video-projects/remotion/`
- generated-audio source: `video-projects/remotion/h2-audio/`
- Blender example: `tools/blender/`
- Krita authoring workflow: `tools/krita/`
- video catalog and per-film manifest/QA: `video-library/`

The current skill ZIP is intended as a convenient bundle of agent instructions, state, catalog, and helper tooling. For reproducible rendering, clone the repo as well; a skill ZIP is not a substitute for dependencies, the H2 source bundle, or the application's runtime.

## Restoring a particular video

Read `video-library/one-more-scroll/manifest.json`, `QA.md`, `latest-remotion-release.json`, and `video-library/reference-clips.json` first. The repo contains the exact H2 master and a separate Remotion sample; never interchange their paths or renderer labels. The reference map keeps your two named video links and study checklist; don't claim timestamped findings unless the linked source was actually viewed.

## Canonical H2 master — already archived

The exact H2 master is already stored at `video-library/one-more-scroll/one-more-scroll-h2-final.mp4` (31,547,778 bytes), SHA-256 `be0608239a374cf10c89b2c9b16e642de962cdd8f1b177de1a173219413a940f`. GitHub Actions [run 40271825143](https://github.com/Nolane-x/video/actions/runs/40271825143) validated the checksum, duration, dimensions, frame rate, codecs and audio format, and generated metadata/contact sheets. The current portable skill ZIP includes this H2 master and a separate Remotion run-36 reference render. Do not repeat the import to restore current state, and never label the Remotion render as H2.

The large H2 source archives and separate source-v2 render candidate are published at the [h2-production-assets-v1 GitHub Release](https://github.com/Nolane-x/video/releases/tag/h2-production-assets-v1). Exact source/candidate SHA-256 values and URLs are recorded in `video-library/one-more-scroll/h2-source-release.json`. The portable skill ZIP links to the manifest rather than duplicating the 230+ MB source packages. A focused source-v3 shoe-tying preview passed [run 40280228327](https://github.com/Nolane-x/video/actions/runs/40280228327), and the first candidate rendered but review packaging failed; corrected rerun [40286913324](https://github.com/Nolane-x/video/actions/runs/40286913324) is active. Both source-v2 and source-v3 remain non-canonical until human full-motion/audio review and explicit artistic sign-off pass.

## Archive previous videos and the H2 source code

The repository catalog lists older render iterations and their checksums in `video-library/previous-works-catalog.json`. If the corresponding attachments are downloaded into one folder, run:

```powershell
python tools/video/archive_previous_works.py --source-dir "$env:USERPROFILE\Downloads\video-previous-works-import-pack\assets"
```

Review the staged files, commit and push them. Wait for the “Verify previous AI video assets” workflow to pass before relying on the recorded repository paths.

The full H2 renderer/source ZIP is larger than a sensible Git blob. To preserve it as a durable Release asset, download the exact `one-more-scroll-h2-source.zip` and related files to a local folder, then run:

```powershell
   .\tools\video\publish_h2_source_release.ps1 -AssetsDir "$env:USERPROFILE\Downloads\h2-production-assets"
```

The publisher requires GitHub CLI authentication, checks each file against a fixed SHA-256 allow-list, creates a versioned GitHub Release and stages `h2-source-release.json`. Commit/push that manifest after reviewing it. The source-v2 archive has been rendered and technically stream-validated, but it is not the final master. Source-v3 adds the reproducible shoe-tying fix from `tools/video/patch_h2_shoelace_scene.py`; see `video-library/one-more-scroll/h2-source-v3-render-request.json`, `docs/STATE.md` and `docs/AI_HANDOFF.md`. Do not promote a candidate until its full-length video and audio have been reviewed.
