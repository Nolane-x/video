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

## Visual decisions
- v5 run [42580571283](https://github.com/Nolane-x/video/actions/runs/42580571283): 53 bones, 12 actions, 31,167 vertices, 54,906 triangles; visually rejected because the female-derived dress bodice creates an implausible chest shape and the turban disappears when bone-parented. Do not use this costume.

## Current revision (v6)
- Restore male `clothing_trenchcoat.glb` as the long outer garment, recoloured to warm earth-red wool over the shirt, trousers and boots. This remains a generic adaptation, not an authenticated caftan.
- Replace direct bone parenting of the turban with a one-bone vertex group (`head`) and an Armature modifier so the wrap keeps its evaluated position and follows head motion.
- Remove duplicate animation setup that reset the selected pose to frame 1. Use the midpoint of `idle_look` for both previews, with eye-level cameras.
- Latest check: [42580993765](https://github.com/Nolane-x/video/actions/runs/42580993765), queued/in progress at last check. Script commit `f8b4f787ca961617328613c6edfb2415fd18fb96`; workflow asset-list commit `9edd39c6104702af65bf9b18f10acf90104065e9`.
- Do not approve this outfit until the new images are visually inspected.

## Integration gate
Review both v6 previews, verify the 53-bone rig and animation tracks, check clothing/body intersections at idle and walk, then import into the separate PBR bombardment branch. Do not modify the long-form master until a representative shot is approved.

## Script and workflow
- `tools/blender/build_constantinople_crew_character.py`
- `.github/workflows/constantinople-human-asset-proof.yml`

## Next checks
1. Confirm the male outer garment, diagonal linen wrap, hands and boots read cleanly in both full-body and close-up views.
2. Check imported `idle`, `walk` and `run` actions at 30 fps; final documentary renders will be sampled at 240 fps.
3. When integrated, keep character roots/armatures independent so each performer can use a different action and screen position.
4. Preserve the source license manifest and file checksums alongside any rendered proof.
