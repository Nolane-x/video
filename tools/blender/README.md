# Blender in the H2 pipeline

Blender is an optional renderer for shots that benefit from depth, real shadows, camera parallax, or a reusable 3D rig. It is **not** the default style for every scene.

The initial style study is a short, procedural 2.5D scene: a simple cream mascot, charcoal stage, restrained red shadow, orthographic camera, and keyed movement. It is designed as a technical proof, not as a finished film.

## Local render

Install Blender from https://www.blender.org/download/ and FFmpeg if needed, then run from the repository root:

```powershell
$env:BLENDER_OUTPUT = "$PWD/out/blender/h2-style-study.mp4"
blender -b --python tools/blender/render_h2_stage.py
```

The script reads `BLENDER_OUTPUT`; if it is missing, it writes to `out/blender/h2-style-study.mp4`.

## CI render

The GitHub Actions workflow `.github/workflows/render-blender-preview.yml` renders the scene on a GitHub-hosted runner and stores the MP4 as an artifact. This allows a Blender render to be executed even when Blender is not installed on the current workstation.

## Style constraints

- Prefer a symbolic mascot to realistic human anatomy.
- Keep surfaces matte, lighting restrained, and the palette coherent with H2.
- Use Blender selectively; Remotion remains responsible for the main edit, typography, timing, and repeatable 2D motion.
