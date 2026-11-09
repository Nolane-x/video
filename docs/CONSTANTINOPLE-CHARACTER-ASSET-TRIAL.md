# Constantinople 1453 — human asset trial

## Purpose
Replace the primitive block-figure artillery crew with anatomically proportioned, rigged human models. This is a supporting asset trial; it does not change the long-form master or approve the PBR bombardment sequence.

## Source and license
- Upstream: `kblood/CharacterCreator`, using its generated `output/` assets rather than bundling or executing its GPL-3.0 source code.
- The upstream `output/asset_licenses.json` and `LICENSE-NOTES.md` identify the selected generated body, hair and clothing assets as CC0 or project-original. The preparation job rejects any manifest entry outside those allowed values and records SHA-256 checksums.
- Source assets are downloaded in Actions and are not committed as binary files to this repository.

## First proof
- Actions run: [42577180745](https://github.com/Nolane-x/video/actions/runs/42577180745).
- Artifact: `constantinople-crew-character-proof-42577180745`.
- Result: Blender import, GLTF rebind and GLB export succeeded. Rig has 53 bones and the source GLB supplies 12 actions (idle, idle variants, walk/run, strafe, jump/fall/land).
- Geometry report: 30,854 vertices and 54,090 triangles across body, face, coat, trousers, boots, hair and wrap meshes.
- Visual review of v1: the face and skin texture are noticeably more human than the hand-built silhouettes, but the dark modern trenchcoat reads too contemporary, and the torus head-wrap read as a ring. Do not approve v1 for final use.

## Revision in progress
- Workflow re-renders after a revised costume script: fuller cloth cap with wrapped folds, brighter earth-brown coat/trousers/boots, leather belt and metal buckle, icosphere helper meshes hidden, full-body and face/torso preview cameras.
- The costume remains a generic illustrative adaptation, not authenticated 15th-century Ottoman clothing.
- Integration gate: review both previews, verify the 53-bone rig and animation tracks, check clothing/body intersections at idle and walk, then import into a separate PBR bombardment branch. Do not modify the long-form master until a representative shot is approved.

## Script and workflow
- `tools/blender/build_constantinople_crew_character.py`
- `.github/workflows/constantinople-human-asset-proof.yml`

## Next checks
1. Confirm the revised turban cap, belt, coat front and hands read cleanly in both full-body and close-up views.
2. Check imported `idle`, `walk` and `run` actions at 30 fps; final documentary renders will be sampled at 240 fps.
3. When integrated, keep character roots/armatures independent so each performer can use a different action and screen position.
4. Preserve the source license manifest and file checksums alongside any rendered proof.
