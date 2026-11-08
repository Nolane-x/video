# Constantinople 1453 — master review and artistic hold

Review date: 2026-11-08  
Repository: `Nolane-x/video`  
Master branch: `squire/constantinople-1453-240fps`  
Master run: [42449792684](https://github.com/Nolane-x/video/actions/runs/42449792684)  
Fast visual review run: [42471038668](https://github.com/Nolane-x/video/actions/runs/42471038668)

## Verified master facts

The Squire master render and automated technical QA completed successfully.

- Duration: 957.9 seconds (15:57.9)
- Picture: 1920×1080, H.264, CFR 240/1
- Frames: 229,896 (229,896 expected)
- Audio: AAC, 48 kHz, stereo
- Shot count: 586 total, 434 bespoke/template-authored siege shots
- Unique sampled-frame hashes in the QA probe: 564 / 564
- Integrated loudness: −14.06 LUFS
- True peak: −3.06 dBTP
- Master SHA-256: `3422e13689551c9e411d7924cd17712133777adfba1042f794be2c4431a45b3e`
- Artifact: `squire-constantinople-1453-240fps-42449792684`, 2,023,692,938 bytes, artifact ID `13611674134`

The full automated QA report says `technical_pass`; it explicitly keeps `artistic_signoff` pending. The six music beds and Foley candidates are not human-auditioned or approved for final mix. Technical QA does not imply artistic acceptance.

## Visual review evidence

The master was reviewed using a 30-moment contact sheet sampled across the full duration and three original 4-second 1080p/240fps excerpts taken from the opening, middle and ending.

Review package: artifact `squire-constantinople-master-fast-review`, ID `13613268510`, produced by run [42471038668](https://github.com/Nolane-x/video/actions/runs/42471038668).

### Findings — artistic hold

The master is not yet at the requested cinematic quality.

- The project config remains `style: "flat"`.
- The contact sheet shows simplified vector/cartoon soldiers, repeated army rows, block-like city silhouettes, flat sea/wall plates and recurring compositions.
- The opening excerpt holds almost the same army-and-wall tableau across 0–3.0 seconds; visible pose/action change is small.
- The middle excerpt repeats a largely static two-guard composition for the first 1.5 seconds, then returns to repeated rows and a flat ship/wall diagram.
- The ending excerpt reuses a flat city backdrop and largely static characters across the first 1.5 seconds, then moves to another simple repeated crowd tableau.
- The output's verified 240fps stream is real CFR 240, but frame rate alone does not create dense, purposeful motion. The 564/564 unique hashes in the one-second sampled QA probe only rule out literal duplication in those sampled points; they do not prove meaningful action or strong choreography.
- The film lacks enough cinematic depth, varied shot families, character acting, material detail, motivated camera movement and readable cause/effect action in the reviewed samples.

This is a technical pass and an artistic reject/hold, not a finished release. Do not market or describe the current Squire master as a polished cinematic film.

## Pending audio review

The WAV/encoded technical data passes QA, but subjective audio approval remains open.

- Voice source integrity, PCM-24/48k mono provenance and AudioSeal verification passed.
- Mix is measured at −14.06 LUFS and −3.06 dBTP.
- The six CC0 music beds and recorded Foley are still marked `human_auditioned: false` / `approved_for_final_mix: false`.
- A complete listen of the narration, music transitions, ambience, individual Foley cues, synchronization and final stereo mix is still required before public release.

## Parallel 3D proof work

Two isolated 39.14-second Blender proof routes are being evaluated:

1. Native Blender 240fps branch: [run 42461960154](https://github.com/Nolane-x/video/actions/runs/42461960154), branch `cinematic/constantinople-bombard-proof`. The narration excerpt, recorded CC0 music/effects, Blender compile and one-frame smoke render passed. At last inspection, the full 9,394-frame render was still running and no proof artifact had been uploaded.
2. 30fps evaluated 3D keyframes → FFmpeg motion-compensated CFR 240fps branch: [run 42467823008](https://github.com/Nolane-x/video/actions/runs/42467823008), branch `cinematic/constantinople-hybrid-240fps`. Blender smoke render and narration/audio preparation passed; keyframe rendering was still running and no proof artifact had been uploaded.

The current Blender scene is explicitly an illustrative reconstruction, not archival footage and not a verified replica of Orban's exact bombard. It uses a generic bombard, primitive geometry, composite simplified crew, Theodosian-style wall, 6 camera shots, projectile/recoil/impact/repair animation and smoke/debris proxies. It is a useful technical experiment, but its visual quality must be judged from the uploaded frames before being promoted. It is only a 39.14-second proof, not a full film.

## Release gate and next steps

Do not start another 16-minute master render yet.

1. Finish and inspect the Blender proofs at normal speed. Check the contact sheet plus all action beats: loading, ramming, recoil, projectile flight, impact, debris, defender reaction, dust and repair.
2. Reject any proof that still looks like primitive low-poly/cartoon assets or has no visible acting/action. Raise material/geometry detail, environment layers, lighting, camera choreography, character silhouettes/rigs, crowd staging and secondary motion before continuing.
3. Use the existing asset library only after checking the exact item index, source page, license, path and checksum. Do not indiscriminately import unvetted models.
4. Produce a visually reviewed 30–60-second proof with at least four genuinely distinct shot families and clear foreground/midground/background depth; watch it at normal speed before expanding.
5. Only after the proof meets the visual bar should the full film be rebuilt. Keep native 240fps where feasible; if a keyframe/interpolation route is used, measure optical-flow artifacts on fast-moving debris, camera cuts and limbs instead of assuming CFR 240 alone proves smoothness.
6. Complete a full film watch and audio audition. Mark artistic approval separately from automated technical status.

## Review files

- Full-film master run: [Actions run 42449792684](https://github.com/Nolane-x/video/actions/runs/42449792684)
- Full-film sampled contact sheet and QA: artifact `squire-constantinople-master-fast-review`, [review workflow](https://github.com/Nolane-x/video/actions/runs/42471038668)
- Earlier 14-scene redesign proof: [run 42459027169](https://github.com/Nolane-x/video/actions/runs/42459027169)
- Native Blender proof: [run 42461960154](https://github.com/Nolane-x/video/actions/runs/42461960154)
- Hybrid Blender proof: [run 42467823008](https://github.com/Nolane-x/video/actions/runs/42467823008)
