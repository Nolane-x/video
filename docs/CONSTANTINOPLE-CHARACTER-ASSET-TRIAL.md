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

## Visual decisions
- v6 run [42580993765](https://github.com/Nolane-x/video/actions/runs/42580993765): 53 bones and 12 actions, but the coat remained dark and modern; the turban still read as a coiled tube. Not approved.
- v7 run [42581411336](https://github.com/Nolane-x/video/actions/runs/42581411336): the brighter coat and slimmer wrap did not fix the body proportions. Inspecting the exported GLB showed all 92 morph-target weights defaulting to 1, simultaneously enabling both male/female morphs, body extremes and blink/look targets.

## Visual decision (v9)
- Run [42582204551](https://github.com/Nolane-x/video/actions/runs/42582204551) succeeded: 53 bones, 12 actions, 30,869 vertices and 55,032 triangles. The hat no longer covers the eyes; the face is visible and the male morph defaults are correct.
- The exported GLB was parsed independently: 10 morph-bearing meshes all have `gender_male=1`, `gender_female=0`, `blink_left/right=0`, `look_down=0`, and `breast_cup_max=0`.
- Visual approval is limited: usable as a background/midground artillery crew asset. It is not a hero close-up asset or an authenticated Ottoman uniform; the coat/headwear remain generic historical adaptations.

## Integration handoff
- Use character artifact `constantinople-crew-character-proof-42582204551` (artifact ID `13657109082`).
- The 30 fps, four-second integration test is in branch `cinematic/constantinople-rigged-crew-integration`; the test duplicates six independent armatures and varies body morphs/actions.
- Do not replace the long-form master. Review the integration proof before upgrading any full-length 240 fps shots.
## Integration gate
Review the v9 previews, verify the 53-bone rig and animation tracks, check clothing/body intersections at idle and walk, then import into the separate PBR bombardment branch. Do not modify the long-form master until a representative shot is approved.

## Script and workflow
- `tools/blender/build_constantinople_crew_character.py`
- `.github/workflows/constantinople-human-asset-proof.yml`

## Next checks
1. Confirm the male outer garment, diagonal linen wrap, hands and boots read cleanly in both full-body and close-up views.
2. Check imported `idle`, `walk` and `run` actions at 30 fps; final documentary renders will be sampled at 240 fps.
3. When integrated, keep character roots/armatures independent so each performer can use a different action and screen position.
4. Preserve the source license manifest and file checksums alongside any rendered proof.
