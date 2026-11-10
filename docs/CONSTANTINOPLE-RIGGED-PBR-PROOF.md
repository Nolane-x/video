# Constantinople 1453 — rigged PBR bombardment proof

Updated: 2026-11-09

## Purpose and scope

This is a separate, short production-quality experiment for the artillery sequence. It does not replace the existing 15m57s Squire master and must not modify that render. The target proof is 16 seconds, 1920×1080, constant 240 fps (3,840 frames), with the verified English narration excerpt, a recorded music bed, cannon fire/impact effects, and an SRT sidecar.

The reconstruction is illustrative. The Poly Haven cannon is a generic CC0 asset, not an authenticated reconstruction of Orban's great bombard. The modular fortress geometry is a visual stand-in, not a measured reconstruction of the Theodosian walls. The rigged crew are CC0-derived character assets with an illustrative period-workwear adaptation, not authenticated portraits or uniforms.

## Existing outputs

- PBR chunked master, run [42578951674](https://github.com/Nolane-x/video/actions/runs/42578951674): all eight chunks and packaging passed. The artifact is 16 seconds, 1920×1080, 240/1 fps, 3,840 frames, AAC 48 kHz stereo. This is a **technical proof only**. It still has primitive crew silhouettes and is not the target visual result.
- Rigged character proof v16, run [42589082600](https://github.com/Nolane-x/video/actions/runs/42589082600): 53 bones, 12 animation actions, 30,389 vertices and 54,088 triangles; standalone preview and GLB export passed. The character asset is not yet approved for hero close-ups; the linen headwrap still reads as stacked bands.
- Rigged PBR integration smoke, run [42621643523](https://github.com/Nolane-x/video/actions/runs/42621643523): asset checksums, two Blender smoke frames, and artifact upload passed. Visual inspection found white low-poly lower-body volumes that swallow the performers; this was rejected for full render.
- Texture tint and canonical morph-state correction, run [42641180829](https://github.com/Nolane-x/video/actions/runs/42641180829): CI passed, but the white lower-body volumes remained. No full render was started.
- Current isolation run [42642846845](https://github.com/Nolane-x/video/actions/runs/42642846845): renders the two baseline frames plus two selective diagnostics (hide the trousers mesh; hide the Body mesh) to identify which imported mesh creates the lower-body volume. It must be visually reviewed before another integration change.

## Visual gate

Do not start the full 3,840-frame PBR render until:
1. The lower-body volumes are identified and corrected.
2. A full-body crew still shows feet, boots, hands and headwrap without mesh intersections or ground clipping.
3. The camera clearly reads the actual crew and the bombard instead of burying the crew behind the weapon.
4. Fire, recoil, projectile, impact dust and debris read at normal speed; one-frame stills alone are not sufficient for motion approval.
5. The complete 16-second proxy and sound are reviewed. The human audition/sign-off of the score and effects remains separate from CI validation.

## Asset provenance

- Cannon and modular-fort model inputs: Poly Haven, CC0-1.0; checksums are verified by the workflow before rendering.
- Rigged character output: generated from MakeHuman-derived CC0 assets; see `LICENSE-NOTES.md` and the character `manifest.json` packaged with the proof.
- Voice excerpt, music and effects: reused from the verified prepared-media artifact; checksums are verified in the prepare job. Human audio approval is still required.

## Workflow safety

The PBR branch is isolated as `cinematic/constantinople-pbr-rigged-crew`. Pushes to the smoke trigger run only the bounded still-image checks. The eight-chunk 240fps render and packaging jobs are gated behind an explicit full-render dispatch/trigger. Keep that gate closed until the visual gate above is met.


## Latest integration correction — 2026-11-10

- Root cause of the white lower-body blocks: the imported crew GLB contained an unmaterialed `Icosphere` helper mesh (1.902 × 2.0 × 2.0 units). It was duplicated with each performer. Hiding the body, trousers, caftan, tunic and boots independently did not remove it.
- `tools/blender/crew_mesh_policy.py` now rejects named Icosphere leftovers and oversized material-free helper meshes. The PBR renderer applies this policy before duplicating the performer. Four regression tests pass in the PBR workflow.
- Character build run [42770651003](https://github.com/Nolane-x/video/actions/runs/42770651003) succeeded: 53 bones, 12 actions, 30,389 vertices, 54,088 triangles. The new GLB contains 12 named render meshes and no Icosphere; the manifest records an empty rejected-mesh list. The standalone stills remain pending artistic approval; use this asset only for background/midground figures, not hero close-ups.
- PBR integration smoke [42770641096](https://github.com/Nolane-x/video/actions/runs/42770641096) passed with the renderer-side filter. Log evidence shows the unwanted Icosphere was dropped before the six performers were duplicated; each performer was assembled from 12 meshes. The reviewed 900-frame still no longer contains the large white blocks. Frame 1500 also renders the cannon firing flash.
- A clean-artifact integration smoke is running in [42771291837](https://github.com/Nolane-x/video/actions/runs/42771291837), using the output of character run 42770651003. Do not begin the 3,840-frame render until this run passes and its two stills are reviewed.
- Packaging now validates the four cue times and burns readable captions into the MP4 while keeping the SRT sidecar. A local FFmpeg filter test preserved 1920×1080, 240/1 fps and 240 frames for a one-second sample; the full 16-second package step has not yet been run.
- The next full candidate is still a technical proof, not an approved film. After the smoke gate, inspect the 30fps proxy, 4 caption-check stills, 10fps unique-frame motion sample and full audio/video before any release decision.


## Runtime reliability correction — 2026-11-10

- Full-render run [42772227982](https://github.com/Nolane-x/video/actions/runs/42772227982) passed preparation and smoke, but the 8-chunk matrix and package were skipped because the trigger predicate checked only modified paths. The predicate now checks both added and modified paths.
- Runs [42788001530](https://github.com/Nolane-x/video/actions/runs/42788001530) and [42788666145](https://github.com/Nolane-x/video/actions/runs/42788666145) did not reach Blender rendering: apt stalled while downloading the 35.9 MB Blender data archive as part of a 225 MB / 183-package install, then exited with timeout 124.
- To avoid repeating that large install on the smoke and eight render runners, the workflow now downloads the official Blender 4.0.2 Linux x64 archive once in `prepare`, verifies its SHA-256 against the official release checksum, checks the xz archive, and uploads it as a run-scoped runtime artifact. Smoke and each render chunk download and extract that same immutable runtime.
- Package only attempts FFmpeg installation if the hosted runner does not already provide `ffmpeg` and `ffprobe`; this occurs once after all chunks, not once per render worker.
- The portable-runtime workflow has not yet passed a new run. Its first smoke is the verification gate; do not describe the full video as rendered until all eight chunks and the package artifact are present and validated.


### Portable runtime integration note

- Run [42791870324](https://github.com/Nolane-x/video/actions/runs/42791870324) verified and uploaded the official 277.6 MB Blender 4.0.2 Linux archive; smoke downloaded/extracted it, imported `bpy` and NumPy, and passed the four mesh-policy tests.
- The first render attempt reached full scene assembly and loaded all six performers with 12 meshes each, then aborted because the hosted runner did not have `libEGL.so.1`. The workflow now installs only the small headless EGL/OpenGL/X11 runtime libraries on smoke and render workers, rather than reinstalling Blender and its 225 MB dependency tree.
- The EGL-library fix has not yet passed a new smoke run. Full render remains gated until it does.
