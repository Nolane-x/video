# Cannae — Illustrated-history 45-second motion proof

## Purpose and status

This is an isolated 45-second proof of the new illustrated-history visual route. It is rendered by a dedicated Remotion composition, `CannaeIllustrated45s`, and does not modify the existing `OneMoreScroll` composition or the archived H2 master.

The proof is intentionally **picture-only**. No music, ambience or battle Foley is included because the relevant catalogue samples have not been human-auditioned. A green render job establishes technical output only; it is not artistic approval.

## Historical basis

The narrative is limited to the central tactical explanation:
- Cannae was fought in 216 BCE beside the River Aufidus in Apulia.
- Polybius describes the initial cavalry engagement and the infantry battle; the commonly explained manoeuvre has Hannibal's centre yield under Roman pressure while the wings and cavalry create an enveloping movement.
- The five scenes here are an original teaching schematic. They are not a surveyed map, a minute-by-minute reconstruction, or a claim that exact unit positions and strengths are known. In particular, the African infantry wings turn against the exposed Roman flanks while the Carthaginian cavalry movement reaches the rear; the artwork does not depict two symmetrical cavalry wings closing a literal circle.

Sources:
- Polybius, *Histories*, Book III, battle of Cannae: https://www.fordham.edu/halsall/ancient/polybius-cannae.asp
- Oxford Classical Dictionary, “Cannae”: https://doi.org/10.1093/acrefore/9780199381135.013.1340

Ancient casualty and force-strength figures are omitted. Ancient accounts and modern scholarship differ; this short visual proof does not need a numerical claim.

## Shot map

| Time | Shot | Visual purpose | Motion focus |
|---|---|---|---|
| 00:00–00:09 | Apulia, Aufidus and Cannae | Orient the audience geographically | Progressive river/terrain reveal and camera push |
| 00:09–00:18 | Roman infantry mass | Establish the forward pressure and formation scale | Staggered march cycles, dust, standards and lateral camera track |
| 00:18–00:27 | The centre gives ground | Show the centre bending rather than treating the battle as generic fighting | Shield contact, body weight shift, recoil, dust and motivated push-in |
| 00:27–00:36 | The wings turn | Explain the enveloping movement | Overhead geometry, two differentiated cavalry paths and progressive arrows |
| 00:36–00:45 | The trap closes | Resolve the tactical geometry and place/date | Pull back, narrowing perimeter and readable end title |

## Motion and technical gates

Shot plan:
- `docs/animation/CANNAE_ILLUSTRATED_45S_SHOT_PLAN.json`
- Schema: `docs/animation/ILLUSTRATED_HISTORY_SHOT_PLAN.schema.json`
- Validator: `tools/video/validate_illustrated_history_shot_plan.py`
- Regression tests: `tests/video/test_illustrated_history_shot_plan.py`

The validator requires a continuous frame timeline, unique shot IDs, motivated cameras, independent channels on motion-led shots, causal action phases, no three consecutive identical compositions, valid contact frames and explicit audio audition/rights gates. The sample is 5 × 9 seconds = 1,080 frames at 24 fps.

Dedicated workflow:
- `.github/workflows/render-cannae-illustrated-45s.yml`
- Output: `CannaeIllustrated45s`, 1920×1080, 24 fps, H.264.
- Artifact: `cannae-illustrated-history-45s-proof`.

The workflow runs the Python regression tests, validates the plan, installs Remotion dependencies, typechecks both compositions, renders, probes the MP4, generates a contact sheet and stores a SHA-256 record.

## Open review gates

1. Review the actual 45-second MP4 at normal speed, not only the contact sheet.
2. Check the map labels, shield/hand contact, centre's controlled retreat, differentiated cavalry paths, the final enclosing geometry and safe text margins.
3. Inspect the five timecodes and intermediate frames for jumps, foot/horse rig disconnection, clipping and visual repetition.
4. Audio remains intentionally absent. Do not add an unreviewed sample to the final mix; obtain and audition suitable hoofbeats, shield/spear impacts, bow/arrow cues and battle-crowd layers first.
5. Only after picture review should a separate sound pass and second proof be rendered.

Do not replace or relabel the archived H2 master or the existing One More Scroll Remotion output with this new proof.
