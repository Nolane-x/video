# H2 Character Bible — Cinematic Stick-Figure Story Style

## The reference videos were reviewed shot-by-shot

- **The Words You Never Forgot**: locker/hallway, character close-ups, mirror/shadow, bedroom, invading words, school/bus stop, statistics and an emotional recovery arc.
- **What If You Were a Mentalist?**: many location changes, multiple characters, over-the-shoulder/reaction shots, inserts of relevant props, and wide/medium/close-up variation.

The target is not to copy frames or storylines. Learn the visual grammar: simple repeatable characters, but rich environments, clear actions, varied shot sizes, motivated camera movement and a story that progresses through pictures.

## Character

- Symbolic stick figure: near-black round head, high-contrast eyes/mouth, warm pale outline, slim dark limbs, colored shirt and readable shoes/hands.
- Keep the silhouette, head-to-body ratio, line thickness and facial placement consistent.
- The protagonist's muted rose shirt represents the loop; muted ochre begins during recovery as a deliberate change.
- Avoid photorealistic people, AI-looking gradients, pseudo-real skin and glossy synthetic materials.

## Environment and camera

- Purpose-built sets: bedroom, phone insert, street, bus stop, classroom, calendar, bathroom/mirror, word-storm, desk, kitchen, stairs, park, gym, cafe, bus, library, dawn and end card.
- The environment carries the production value: architectural perspective, doors, windows, mullions, shelves, tables, lamps, plants, practical light and grounded shadows.
- Contrast cool plum/charcoal surroundings with warm amber windows. Bloom and vignette remain restrained.
- Vary wide establishing shots, medium actions, close reactions, inserts, silhouettes and holds. No repeating one backdrop across every shot.
- Pan/zoom must be motivated by the action; do not use it as a substitute for animation.

## Action principles

Every action should read through anticipation -> action -> contact -> follow-through -> recovery:
- Phone: hand and screen must align; eyes/head point at the device.
- Writing: hand/pen meet the page; the other hand stabilizes the paper or desk.
- Drinking: the cup reaches the mouth and the head reacts.
- Tying shoes: bent posture and hands approach the laces.
- Stairs: alternating feet land on visible treads; body height advances.
- Punching: draw back, strike the bag, show contact, bag reacts, fist recovers.
- Friend interaction: both characters orient toward one another; listener's body language differs from the speaker.

## H2 workflow

`public/story/shots.json` is the source of truth. Each shot defines `id`, time range, `tpl`, caption line, emotion, action, sound cues and animation `args`. Remotion renders the timeline; H2 procedural audio builds music/SFX; FFmpeg masters levels and validates output. The music arc is sad -> dark -> intentional silence -> hope -> rise -> resolve.

## QA gates

1. Inspect a contact sheet with all 31 shots, not a handful of frames.
2. Inspect action start/contact/recovery at actual motion frames.
3. Check hands against props, feet against surfaces, shot variety, background hierarchy and transitions.
4. Confirm subtitles do not cover the acting and that shadow intensity changes with the story.
5. Validate 155s, 1280x720, 24fps, audio track, loudness and peaks.
6. A successful render is a technical gate, not proof of artistic quality.
