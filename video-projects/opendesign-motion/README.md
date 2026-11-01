# OpenDesign Motion — frame-indexed reference reconstruction (V23)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V23 cube alignment

V22 corrected the cube-local clock after the separate 12-frame logo tile, and assigned the clock, 100K and EASE artwork to distinct faces. V23 adjusts the yaw landmarks and swaps the top/underside CSS face normals to align the source camera-angle changes:
- frame 933–944: standalone rounded-square blue emblem;
- frame 945 / cube local f0: camera cube begins at -90° yaw;
- frame 960 / local f15: +38° yaw; portrait screen is intended to face camera, black emblem on adjacent side;
- frame 990 / local f45: +87° yaw; blue/gold clock face above, lime EASE underside below;
- frame 1005 / local f60: +133° yaw; yellow 100K side face moves into view;
- frame 1020 / local f75: +180° yaw; black glyph face dominates;
- frame 1050: transition to the final logo lockup.

## Verified content carried forward

- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame 547: 3.7%.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.
- Launch Film preview states at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.
- MORRO transition resolves into the large purple extruded symbol before the separate app-logo tile.

## Timeline

- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted 30-panel project wall
- 316–585: 28-cut source-indexed montage
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch Film interface and countdown
- 897–933: MORRO typography → large purple extruded symbol
- 933–945: standalone blue logo tile
- 945–1050: rotating illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source map, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates frame count/metadata/audio loudness, computes checksums and produces 1fps/2fps contact sheets.

A successful workflow proves technical validity, not artistic similarity. Compare the candidate at frames 933/945/960/975/990/1005/1020/1050/1080/1118 and watch the full moving sequence.
