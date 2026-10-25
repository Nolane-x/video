# Setup on Windows 11

## Minimum tools

- Node.js 22 LTS (Remotion project and TypeScript checks)
- Git
- FFmpeg/ffprobe (for local media inspection; Remotion's pinned packages provide its rendering binaries)
- Optional: Blender for selected 2.5D/3D scenes; Krita for hand-authored art assets

Do not download the Blender, Krita, or Remotion application source archives into this repository. Install and update the tools separately.

## Remotion

Open PowerShell in the repository root:

```powershell
cd video-projects/remotion
npm install
npm run dev
```

Render the sample composition:

```powershell
npm run typecheck
npm run render
```

The MP4 will be written to `video-projects/remotion/out/one-more-scroll.mp4`.

## Optional artist tools

- Blender: https://www.blender.org/download/
- Krita: https://krita.org/en/download/
- Remotion docs: https://www.remotion.dev/docs

Use Blender for a scene only when depth, camera parallax, lighting, or rigging materially improves it. Use Krita for deliberate character/prop drawings and paint-overs. Keep the established flat H2 character style; avoid photorealistic or synthetic-looking human art unless a project explicitly calls for it.
