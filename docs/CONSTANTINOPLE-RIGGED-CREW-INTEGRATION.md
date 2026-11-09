# Constantinople 1453 — rigged crew integration proof

## Objective
Replace the primitive crew silhouettes in the 3D bombardment stage with independent copies of the verified CC0 human rig. This is a short staging/motion test, not a replacement for the 240 fps PBR bombardment master.

## Inputs
- Character source: `kblood/CharacterCreator` generated outputs, CC0/project-original per the upstream `asset_licenses.json` and `LICENSE-NOTES.md`.
- Character artifact expected from run [42582204551](https://github.com/Nolane-x/video/actions/runs/42582204551), smoke build passed and the morph weights were independently checked.
- Cannon/fortress models and textures: verified Poly Haven CC0 asset artifact from run [42578951674](https://github.com/Nolane-x/video/actions/runs/42578951674).

## Scene integration
- Six copies of the same 53-bone character rig, each with its own armature object and action.
- Four Ottoman artillery crew positions around the cannon: breathing/idle-look and in-place walking actions.
- Two Byzantine defenders on the wall, facing the cannon.
- Each copy can use separate body morphs (age, weight, muscle, facial shape) and a different animation without sharing armature pose state.
- Short proof: 1920×1080, 30 fps, 120 frames (4 seconds). This is only a composition and deformation test; the target documentary render remains 1920×1080 at native 240 fps.

## Workflow
- Script: `tools/blender/render_constantinople_rigged_crew_integration.py`.
- Workflow: `.github/workflows/constantinople-rigged-crew-integration.yml`.
- The push trigger is gated by `tools/blender/run-crew-integration.trigger` so the proof is not launched until the character artifact exists.
- First premature attempt [42581475804](https://github.com/Nolane-x/video/actions/runs/42581475804) failed only because the v7 character artifact had not finished uploading; the render job was skipped. It did not run Blender.

## Release gate
Inspect the four-second clip/contact sheet for correct placement, orientation, clothing deformations, foot contact, clipping and independent motion. Only after a pass should these characters be integrated into a 240 fps PBR shot. The long-form Squire master remains unchanged and is not artistically approved.
