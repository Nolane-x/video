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
