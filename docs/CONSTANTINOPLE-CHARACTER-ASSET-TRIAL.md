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

## Iteration history and visual decision
- v1 run [42577180745](https://github.com/Nolane-x/video/actions/runs/42577180745): import/rebind/export succeeded, but the face, clothes and animation still needed visual review.
- v2 run [42577611981](https://github.com/Nolane-x/video/actions/runs/42577611981): 53-bone model rendered. The first full-body image had a ring-like cap and modern coat; not approved.
- v3 run [42578085824](https://github.com/Nolane-x/video/actions/runs/42578085824): leather apron and straps were too blocky/large; not approved.
- v4 run [42579017921](https://github.com/Nolane-x/video/actions/runs/42579017921): 53 bones, 12 actions, 31,874 vertices, 56,114 triangles; the apron read as a flat shield and the modern coat remained; not approved. The full-body preview was inspected.

## Current revision (v5)
- Replace the modern trenchcoat with the CC0-derived `clothing_dress.glb` (long tunic/skirt assembly), recoloured as muted wool, layered with shirt, trousers and boots.
- Remove the flat procedural apron, the cube powder pouch and the extra leather belt; the selected tunic asset includes its own belt.
- Replace stacked torus rings with a fuller cloth cap and one diagonal wrap strip, convert the wrap curve to mesh for GLB export, and parent headwear to the head bone.
- Sample a midpoint idle pose and use eye-level full-body/close-up cameras.
- Latest check: [42580571283](https://github.com/Nolane-x/video/actions/runs/42580571283), still building the character proof at last check. Script commit `b55aacb913971b6533d98796ed1cab15260180c0`; workflow commit `fb925cd608d2c3c772857558c84f88afae6225e9`.
- The outfit remains an illustrative historical adaptation, not authenticated 15th-century Ottoman clothing.

## Integration gate
Review both v5 previews, verify the 53-bone rig and animation tracks, check clothing/body intersections at idle and walk, then import into the separate PBR bombardment branch. Do not modify the long-form master until a representative shot is approved.

## Script and workflow
- `tools/blender/build_constantinople_crew_character.py`
- `.github/workflows/constantinople-human-asset-proof.yml`

## Next checks
1. Confirm the male outer garment, diagonal linen wrap, hands and boots read cleanly in both full-body and close-up views.
2. Check imported `idle`, `walk` and `run` actions at 30 fps; final documentary renders will be sampled at 240 fps.
3. When integrated, keep character roots/armatures independent so each performer can use a different action and screen position.
4. Preserve the source license manifest and file checksums alongside any rendered proof.
