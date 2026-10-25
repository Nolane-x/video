# Animation and visual QA

Technical success isn't artistic success. TypeScript passing or an MP4 export proves the tool ran, not that the film is good.

## Per-shot checks
Review start, midpoint, contact peak, recovery and end:
- character is inside frame, no accidental head/foot crop;
- same head/body proportions, face layout, outline and shirt hue;
- feet contact bed/floor/stair;
- hand reaches actual prop, props move/recoil appropriately;
- head/eyes aim at object/person;
- distinct acting for walk, listen, drink, tie shoes, write, punch and reach;
- foreground/background parallax and light sources are plausible;
- captions don't cover face/hands/props;
- location and composition change when story beat changes.

## Required contact tests
- Phone: hand/wrist aligns with device; released device rests on its surface.
- Writing: pen tip touches page; supporting arm has a believable pose.
- Drinking: cup reaches mouth, arm/head react; no floating cup.
- Shoe tying: body bends and both hands approach shoe/laces; no shadow graphic pretending to be contact.
- Stairs: leading foot lands on visible tread, torso rises per step, wide camera avoids clipping.
- Punch bag: draw back, strike, visible contact, bag swings, fist recovers; static bag reads as a miss.
- Friend: characters orient toward each other; listening differs from speaking/walking.

## Contact sheets and motion proof
Make numbered sheet for every shot plus overview; map frame/time to shot. For hard motion, create a clip including anticipation/contact/recovery and inspect samples 2–4 frames apart. A poster frame cannot prove motion.

## Defect severity
- **P0:** corrupt MP4, wrong duration/ratio, missing required audio, false engine claim, severe continuity, inaccessible deliverable.
- **P1:** repeated generic locations, floating prop, clipped face/feet, false contact, static action, missing key cue.
- **P2:** small spacing, transition or color issue.
Fix P0/P1 or disclose before calling final.
