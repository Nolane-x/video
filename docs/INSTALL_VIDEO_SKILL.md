# Installing/restoring the video-production skill

This repo itself is the canonical skill workspace. Start by cloning/opening `Nolane-x/video`, then tell the agent to follow root `AGENTS.md`.

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

Read `video-library/one-more-scroll/manifest.json`, `QA.md`, and `latest-remotion-release.json` first. The latest Remotion video stored in the repo is not interchangeable with the original H2 Canvas/Chromium master. Verify every path and renderer label before use.

## Import the exact H2 master file

The original H2 master is distinct from the Remotion reference video. Its expected checksum and technical metadata are recorded in the manifest. To move it from the prior ChatGPT attachment into durable GitHub storage:

1. Download the exact file named one-more-scroll-h2-final.mp4 from the previous chat.
2. From the root of a clone of this repository, run this PowerShell command (adjust the Downloads path if needed):

   python tools/video/archive_h2_master.py "$env:USERPROFILE\Downloads\one-more-scroll-h2-final.mp4"

3. The importer verifies SHA-256, file size, duration, resolution, FPS, codecs and audio format before copying it into video-library/one-more-scroll/. It also generates contact sheets and updates manifest/QA/state.
4. Review the generated files, then commit and push the binary, checksum, contact sheets and updated documentation. The package workflow will update the portable skill ZIP to include the H2 master as well as the Remotion reference sample.

Do not rename the Remotion render as the H2 master. If the checksum fails, stop; the input is not the exact canonical H2 file.


## Archive previous videos and the H2 source code

The repository catalog lists older render iterations and their checksums in `video-library/previous-works-catalog.json`. If the corresponding attachments are downloaded into one folder, run:

```powershell
python tools/video/archive_previous_works.py --source-dir "$env:USERPROFILE\Downloads\video-previous-works-import-pack\assets"
```

Review the staged files, commit and push them. Wait for the “Verify previous AI video assets” workflow to pass before relying on the recorded repository paths.

The full H2 renderer/source ZIP is larger than a sensible Git blob. To preserve it as a durable Release asset, download the exact `one-more-scroll-h2-source.zip` and related files to a local folder, then run:

```powershell
.	oolsideopublish_h2_source_release.ps1 -AssetsDir "$env:USERPROFILE\Downloads\h2-production-assets"
```

The publisher requires GitHub CLI authentication, checks each file against a fixed SHA-256 allow-list, creates a versioned GitHub Release and stages `h2-source-release.json`. Commit/push that manifest after reviewing it. The source-v2 archive has extra scene fixes that were not verified by a complete render; do not treat that archive as a new final master.
