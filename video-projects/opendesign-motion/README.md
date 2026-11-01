# OpenDesign Motion — frame-indexed reference reconstruction (V22)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V22 correction: cube timing and face assignment

V21 added the separate emblem tile before the camera cube, but its cube animation incorrectly restarted its keyframe clock after the 12-frame lead-in. V22 keeps the logo tile at frames 933–944 and uses the cube-local clock so source timing aligns:
- frame 945, cube local frame 0: cube enters;
- frame 960, local frame 15: portrait face forward, black glyph on adjacent side;
- frame 990, local frame 45: blue/gold clock top and lime EASE underside;
- frame 1005, local frame 60: yellow 100K editorial side;
- frame 1020, local frame 75: black glyph face forward, editorial face adjacent;
- frame 1050: move to the final brand lockup.

The six graphic surfaces are now assigned by physical orientation: portrait front, black symbol side, yellow 100K side, blue clock top, green EASE underside and black symbol rear. The 3D pitch is increased through the middle of the turn so both top and underside surfaces can read.

## Verified content carried forward

- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame 547: 3.7%.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.
- Launch Film preview states at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.
- MORRO transition: repeated type resolves into a large purple extruded ribbon mark before the app emblem.

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

A successful workflow proves technical validity, not artistic similarity. Compare the rendered MP4 with the supplied reference at native frame indices 933/945/960/975/990/1005/1020/1050/1118 and watch the complete sequence for motion and transitions.
