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
