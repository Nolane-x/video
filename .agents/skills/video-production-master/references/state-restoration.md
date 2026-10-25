# Restore state in a fresh AI session

1. Read AGENTS, this skill, state/handoff, video-library README and per-video manifest.
2. Inspect current HEAD, latest commits, Actions and artifacts; dated docs are snapshots.
4. Identify exact renderer for each artifact: H2 Canvas/Chromium, Remotion CLI, Blender, or FFmpeg assembly.
5. Verify whether each artifact is a permanent repo file, GitHub Release asset, expiring Actions artifact or old ChatGPT attachment. Check URL/checksum.
6. Read live story JSON, character bible, source and audio workflow.
7. Reconstruct environment from real manifests; don't assume packages/apps are installed.
7. Render a small proof before full render.

At session end update STATE, HANDOFF and video manifest with UTC time, commit, files changed, relevant CI URLs/conclusions, artifact URLs/storage/expiry, what was actually inspected, fixed/open defects and next action. Separate rendered change from source-only change.
