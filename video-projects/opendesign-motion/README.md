# OpenDesign Motion — frame-indexed reference reconstruction (V18)

Reference profile: 37.312s container, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118). Output target: 37.300s picture, H.264, AAC stereo 48kHz.

The supplied `preview.mp4` remains the visual source of truth. The output is independently authored Remotion/SVG/CSS artwork; the original editable source project, proprietary fonts and original art layers were not supplied, so this is a reconstruction and is not claimed to be pixel-identical.

## V18 corrections from native-frame review

This iteration replaces the obviously mismatched Launch Film preview artwork at source frames 795/810/825/840, rebuilds the 1973 optical poster, the portfolio-wall cutaway, repeated MIND typography and the particle-vortex app viewport, and increases the scale/motion treatment of the EASE / IN / OUT / NEVER / LINEAR typography. The cube face that previously contained an unrelated portrait is now a designed camera/lens face with a play-marked side, clock artwork and graphic surfaces.

Specific source values have been checked against the uploaded video:
- Star History frames 523–530: 80K / Day 88; 82K / Day 96; 84K / Day 104; 87K / Day 111; 91K / Day 119; 93K / Day 126; 94K / Day 132; 96K / Day 138.
- Eye readout at frame 547: 3.7%.
- The 531–539 toggle is a small isolated switch, not a large settings card.
- Launch Film preview at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.

## Timeline

- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted 30-panel project wall
- 316–585: 28-cut source-frame montage (269 frames)
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch Film interface, five source-matched preview states and 3/2/full-screen 1 countdown
- 897–933: MORRO typography → geometric mark → app tile
- 933–1050: rotating rounded camera-like multi-face object
- 1050–1119: OpenDesign Motion end card

## Render and review

Render only through `.github/workflows/render-opendesign-motion.yml`. CI performs timeline/map validation, TypeScript typecheck, 1080p30 rendering, FFmpeg audio mastering, stream/frame-count checks, loudness measurement, checksum generation and contact-sheet upload.

A green Actions run confirms technical validity only. It does not certify visual similarity. Review the generated MP4 side-by-side with the supplied reference at identical native frame indices, then watch the full moving sequence for transitions, timing and motion. The current source-frame ledger and key review points are in `shot-map.json`.

## Exact-frame montage ledger

Absolute source frames: 316–318 gallery exit; 318–322 comic 1952; 322–338 comic 1962; 338–353 dots; 353–368 optical logo; 368–381 pixel game; 381–386 portfolio wall; 386–400 MIND; 400–430 circular typography; 430–446 editorial grid; 446–456 particle viewport; 456–461 EASE; 461–466 metallic IN; 466–471 IN.; 471–476 EASE; 476–486 OUT; 486–496 NEVER; 496–511 LINEAR; 511–516 green circular mark; 516–523 clock; 523–531 Star History; 531–539 toggle; 539–547 Motion Films; 547–555 eye; 555–563 Courses; 563–570 comic; 570–578 FUTURE; 578–585 Not.
