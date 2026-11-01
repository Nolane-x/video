# OpenDesign Motion — frame-indexed reference reconstruction (V25)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V25 cube refinement

V24 improved source-frame similarity across the cube sequence (SSIM gains against V23: +0.034 at frame960, +0.023 at frame990, +0.054 at frame1005, +0.019 at frame1020), but the full-size review showed an oversized EASE panel obscuring too much of the clock at frame990.

V25 keeps the source-indexed front artwork and changes the surface hierarchy:
- frame960 / local f15: portrait front, black emblem on the left side;
- frame990 / local f45: blue/gold 1889 clock remains the main front face; EASE becomes a narrow folded lower-edge strip rather than a large green panel;
- frame1005 / local f60: yellow 100K artwork comes forward; adjacent side also switches to the yellow 100K visual;
- frame1020 / local f75: black glyph face returns to the front.

The camera pitch is now near level at frame960, rises through frame990, then reduces again through frame1020. The neighboring side artwork is frame-keyed to the reference's fast turn: black → blue clock motif → yellow 100K.

## Verified content carried forward

- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame 547: 3.7%.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.
- Launch Film preview states at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.
- MORRO transition resolves into the large purple extruded symbol before the separate app emblem.

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

A successful workflow proves technical validity, not artistic similarity. Compare V25 with the supplied source at frames 933/945/960/975/990/1005/1020/1035/1049/1050/1080/1118 and watch the moving sequence.
