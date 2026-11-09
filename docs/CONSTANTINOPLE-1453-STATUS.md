# Constantinople 1453 — production status and handoff

## Current truth

The long-form Squire master exists and passed automated technical QA, but it is **not artistically approved**.

- Master: 957.9 seconds, 1920×1080, native CFR 240 fps, 229,896 frames.
- Timeline: 586 shots, including 434 custom shots across 15 templates.
- Voice: verified PCM-24/48 kHz narration provenance and AudioSeal.
- Delivery artifact: Actions run 42449792684, artifact 13611674134 (~2.02 GB).
- QA status: `technical_pass`; a human watch-through and final audio audition are still required.
- Visual review: whole-film contact sheet reviewed. The dominant look is still flat vector/cartoon; formations and character designs repeat. Do not describe this as cinematic final or publish it as the approved master.

Review proxy and contact sheet were extracted locally during the review session:
- `whole-film-review-proxy-30fps.mp4`
- `whole-film-contact-sheet.jpg`

## Earlier Blender proof

The first Blender 3D bombardment branch produced six successful chunks. Its FFmpeg concat/package step failed because the concat list contained literal escaped newlines. The chunks were recovered and packaged separately.

- Recovered proof: 39.14 seconds, 1920×1080, native CFR 240 fps, 9,394 frames.
- It includes gun/crew staging, shot flight, wall impact and repair aftermath.
- Visual review: it has real 3D depth and camera motion, but primitive character geometry still reads as low-poly/toy-like. Technical proof only, not art approval.
- Recovery workflow: `.github/workflows/constantinople-package-cached-chunks.yml`.

## PBR scene direction

Branch: `cinematic/constantinople-pbr-proof`.

The next proof uses:
- Poly Haven CC0 cannon mesh and modular-fort PBR material maps, downloaded from a separately verified asset artifact.
- SHA-256 verification of the imported model and texture files before render.
- 16-second English narration excerpt from the gun/bombard section, with a matching SRT sidecar.
- 1920×1080 native 240 fps, 3,840 frames, divided into eight resumable 480-frame chunks; Eevee TAA is 8 samples. The earlier 960-frame chunks progressed too slowly for a safe 120-minute job limit.
- Camera grammar: bronze/cannon macro reveal → crew/wall wide → recoil and smoke → projectile flight → wall impact/debris.
- Loose accessory cannonballs embedded in the asset are hidden; the live projectile, muzzle flame and powder smoke are positioned from the imported barrel's evaluated world-space bounds instead of hard-coded screen coordinates.
- Human figures remain distant silhouettes; no close-up toy faces. The PBR cannon still uses the generic Poly Haven field-cannon mesh, so it is not visually equivalent to Orban's colossal bronze bombard.
- The cannon is a generic visual stand-in, not an authenticated replica of Orban's great bombard. The wall is an illustrative composite, not a measured reconstruction of the Theodosian walls.

Workflow: `.github/workflows/constantinople-pbr-proof.yml`.
Scene script: `tools/blender/render_constantinople_bombardment_pbr.py`.
Latest run: [42578951674](https://github.com/Nolane-x/video/actions/runs/42578951674) — source preparation and PBR smoke frame passed; eight 240 fps chunks are being rendered, with the first four active. Latest log samples show chunk 01 at frame 130 and chunks 02–04 around frames 543, 1023 and 1502. These are still rendering; no packaged 16-second movie exists yet.
Latest scene commit: `1c8cb59d25e7a1cc8b395c11eae08331f176cbdf`; workflow commit: `82714c6453d09e1b7f9159b56d420adcafda26c5`.

## Release gates

1. Smoke frame must show the cannon oriented toward the wall, with visible imported PBR materials and no composition breakage.
2. All four chunks must render and concatenate; verify exact frame count, 240/1 CFR, 1920×1080, 48 kHz stereo and complete decode.
3. Review contact sheet and normal-speed 30 fps proxy; do not judge motion from stills alone.
4. Human visual review and audio audition remain separate gates.
5. Only after the PBR proof is visually acceptable should its style be expanded to the Golden Horn, ship portage, mining, final assault and aftermath sequences. Do not silently swap the entire long-form master to this branch.

## Known engineering lessons

- Ubuntu 24.04's Blender package needs `python3-numpy` for the glTF importer.
- Use `Vector((x, y, z))` when later adding mathutils vectors; do not add a tuple directly to a Vector.
- Avoid unnecessary Weighted Normal modifiers unless Auto Smooth is enabled.
- FFmpeg concat lists must be written with actual newline characters, e.g. `printf "file '%s'\\n" "$f"`.
- Keep chunk ranges deterministic and independently verifiable before packaging.
