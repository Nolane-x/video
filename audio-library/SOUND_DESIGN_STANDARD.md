# Cinematic historical sound design standard

## Layer palette

Every sequence should be considered against these layers, selecting only what is physically and editorially justified:

1. **Narration:** reviewed human or permitted synthetic voice; clear consonants, natural pauses, controlled dynamics.
2. **Score:** actual licensed composition or sampled/played instruments, arranged around the emotional arc. Don't rely on code-generated drone or loop as the main soundtrack.
3. **Location bed:** wind through a pass, rain on roofs, forest insects, surf, harbor, room tone, battlefield distance, temple/courtyard ambience.
4. **Foley:** footwear by surface, cloth, leather, armor, belts, scabbards, wood, rope, paper, doors, horses and movement.
5. **Action/impact:** blade unsheathing, metal contact, shield/wood impact, arrow handling, horse tack, fall, debris, gates and machinery—each selected for the material and scale shown.
6. **Crowd/animals:** distant murmur, shouted commands, crowd swell, horses, birds and other contextual sources; never assume a generic crowd loop is enough.
7. **Transitions/accents:** reverse swell, restrained whoosh, cut impact, bell, sub impact, tonal sting. Use only when edit or story needs it.

## Cue card

For each prominent cue record:
- shot ID and frame/time range;
- visual action and contact frame;
- distance/perspective (close, near, medium, far, off-screen);
- source asset ID + file name + SHA-256;
- license + required attribution;
- auditioned status and take number;
- gain, pan, EQ, dynamics, reverb/occlusion and fade envelope;
- music ducking sidechain or automation;
- reason for sound and expected emotional function.

## Editing rules

- Pre-lap and carry ambience across picture cuts to connect geography.
- Cut Foley on the actual movement/contact frame, not simply the shot boundary.
- Let weapons and armor have mass: a blade draw has friction and scabbard detail; a large clash needs distinct metal transients and body response; don't use one generic whoosh for all.
- Use layered distances and high/low-frequency loss for battlefield scale.
- A close step is present and transient-rich; distant ranks are softer and more diffuse.
- Don't add sound to every animated object. Sparse, meaningful effects read more cinematic than constant noise.
- Avoid identical repeated effects; rotate real takes, vary timing and perspective.
- Measure integrated loudness, loudness range, true peak and clipping. Preserve headroom and avoid limiter pumping.
- Listen to the full mix from beginning to end at normal speed and log issues with exact timecodes.

## Curated recorded-source priority

- Check Build 76 archives and the pinned Meta Open Sound preview bank before inventing or synthesizing replacement Foley.
- Meta Oculus Audio Pack 1 includes searchable 48 kHz recordings for sword contact/scrape, footsteps, cloth/gear, horse vocalizations, boats/oars, wind, water and ambience. The Oculus collection is CC BY 4.0 and requires its exact attribution line; its 3 instrument sample collections are CC0 1.0. Never merge those rights classes.
- Use OGG previews for selection; use the linked 48 kHz WAV masters for production where the cue is selected and legal terms are satisfied.
- A UCS category or file name is only a search hint. Its metadata may be machine-classified and every selected sound must still be heard for historical fit, quality, loop points, noise and perspective.

## Placeholder policy

Procedural sounds may fill a temporary gap in an animatic or test. The final candidate must replace them with an auditioned recording or document why no suitable legal recording exists. Never call an oscillator "realistic Foley".
