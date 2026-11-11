# Constantinople 1453 — visual proof review

Review date: 2026-11-11  
Repository: `Nolane-x/video`  
Branch under render: `squire/constantinople-1453-redesign`  
Render run: [42982265108](https://github.com/Nolane-x/video/actions/runs/42982265108)  
Source commit: `fe332aa89f60849a48fecdabbe6f5c1e18a30294`  
Proof artifact: `squire-constantinople-redesign-proof-42982265108`  
Proof SHA-256: `56772d7fbff8c004888d34e5c1f4d32c5aaef95a4ab8e8ca107bedd3f4e527e9`

## What passed in the proof

- The 37.38-second proof file probes as H.264, 1920×1080, constant 240/1 fps, with AAC stereo 48 kHz audio.
- The on-frame Squire captions are present and visually readable in the sampled contact sheet.
- All 14 required bespoke templates produced moving proof segments.
- The proof is technical evidence only. It is not the 15:57.9 master and is not an artistic sign-off.

## Shotbook profile

The generated shotbook contains 583 shots over 957.9 seconds (15:57.9). The 14 bespoke templates account for 444 shots (76.2%). Average shot length is about 1.64 seconds, median 1.66 seconds, with observed lengths from 0.54 to 3.96 seconds.

| Bespoke template | Shots | Share of all shots |
|---|---:|---:|
| city_panorama | 94 | 16.1% |
| golden_horn | 63 | 10.8% |
| command_camp | 59 | 10.1% |
| repair_wall | 51 | 8.7% |
| last_assault | 37 | 6.3% |
| city_interior | 32 | 5.5% |
| wall_battery | 29 | 5.0% |
| aftermath_city | 25 | 4.3% |
| final_night | 22 | 3.8% |
| gun_crew | 17 | 2.9% |
| church_refuge | 8 | 1.4% |
| relief_galleys | 3 | 0.5% |
| ship_portage | 2 | 0.3% |
| tunnel_cutaway | 2 | 0.3% |

## Issues visible in the contact sheets / proof

1. **Character language is too toy-like for the intended cinematic history film.** The large-head stock Squire character silhouettes dominate the frame. The recurring defender works for continuity, but needs more restrained human proportions, richer period clothing/armor detail, and a more believable scale against the city.
2. **Backgrounds are graphic stage sets rather than deep environments.** Several skyline, wall, and sea scenes have flat horizon bands. Add stronger foreground / mid-ground / far-background separation, atmospheric perspective, texture, practical light sources, and parallax that serves the action.
3. **Shot variety is uneven.** The panorama template is used 94 times, while ship portage (2), tunnel cutaway (2), and relief galleys (3) are underrepresented. Each of those key story beats needs a coherent multi-shot sequence, not a single token visual.
4. **Action cause-and-effect needs to read in the edit.** The cannon sequence should visibly connect crew loading, ignition, recoil, projectile travel, wall impact, masonry collapse, defender reaction, and repair. The portage sequence should show ropes under strain, rollers turning, hauling teams moving, and the ship actually progressing. The final assault needs distinct waves, ladder contact, climbing, fighting at the parapet, breach, and withdrawal/line collapse.
5. **Audio is not yet human-approved.** The proof mix is a technical mix from recorded candidate music and Foley. Keep its source manifest, but do not claim the beds or Foley have passed a human audition.

## Required visual-redesign gates before artistic approval

- Replace oversized/chibi foreground people with a coherent, more mature illustrated character system. Keep the recurring defender identifiable, but preserve human proportions and consistent costume details.
- Create at least three visually distinct compositions for each currently underused story beat: relief galleys, overland ship portage, and tunnel/countermine.
- Reduce panorama reuse: any repeated template must change camera angle, scale, lighting/time-of-day, focal subject, and foreground/mid-ground staging; avoid merely changing the caption.
- Build deeper city, wall, harbour, artillery, and siege-camp environments with layered depth, material texture, atmospheric haze, smoke/light interaction, and meaningful camera movement.
- Review contact sheets by chapter and inspect representative motion clips at normal speed. A 240 fps stream alone does not make animation cinematic.
- Keep captions readable, away from focal action and faces, with sensible line breaks and safe margins.
- Human-watch the full master and audition the complete final mix before public-release approval.

## Decision

**Technical proof: passed. Artistic approval: not granted.**  
The current 16-minute master render must complete its strict technical QA first. Preserve the existing previous master as a rollback artifact. Do not merge or replace the release/default branch on the strength of this proof alone.


## Additional subtitle and audio measurement

- Local ffprobe verification of the downloaded proof confirms 37.383 seconds, 8,969 encoded frames, 1920×1080, H.264 at constant 240/1 fps, plus AAC stereo 48 kHz.
- Proof mix measurement: -14.30 LUFS integrated, -3.24 dBTP true peak, 2.10 LU loudness range. This is a safe technical level for the proof, not approval of the music or Foley choices.
- The delivered SRT sidecar has 238 cues. In its text payload, 113 lines exceed 56 characters and the longest line is 154 characters. Reflow sidecar cues to a maximum of two balanced lines (target roughly 42–48 characters per line), preserve original cue timing, and verify no overlaps before final delivery. This is a sidecar formatting issue; it does not by itself prove that the burn-in caption renderer overflowed.


## Implemented caption-sidecar repair

Added `tools/video/reflow_squire_captions.py` and `tests/test_squire_caption_reflow.py` on this branch. The utility verifies SRT/VTT source parity, splits long paragraph captions at word boundaries, balances the resulting cue groups, and preserves each original cue's outer start/end time and the gaps between source cues.

Measured against the VoiceStudio subtitle sidecars used for this film:
- Source cues: 238; reflowed cues: 294
- Longest source line: 154 characters; longest output line: 42 characters
- Every output cue: at most 2 lines
- All 2,473 words preserved, in source order
- No overlaps; original timeline endpoints and inter-cue gaps retained
- Minimum output cue duration: 0.88 seconds
- Four unit tests pass locally

Command:
`python tools/video/reflow_squire_captions.py --srt voice-assets/captions.srt --vtt voice-assets/captions.vtt --output-dir reflowed-captions`

This is a sidecar fix and does not require re-encoding the video. The in-flight GitHub Actions render uses the commit it checked out at start; this newly added utility is for the next delivery assembly/review and did not modify the active render workflow.
