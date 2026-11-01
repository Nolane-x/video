# OpenDesign Motion — frame-indexed reference reconstruction (V28)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V28 countdown artwork and handoff

V27 corrected the early cut but the 1 inside Preview was still typographic and too small, while the full-screen cut became an unrounded black canvas. V28 now uses one reusable, original SVG prism for both states: blue front, violet top bevel, dark extruded side, strong 3D edge and a matching source-scale silhouette.

The UI handoff is frame-locked:
- source frame 885: number 1 inside the Launch Film Preview; app/window still present;
- frame 889: scale the app around the center-right Preview anchor so the left prompt UI crops away;
- frame 890: Preview becomes near full frame;
- frame 891: swap to a rounded black takeover card with the same blue prism, orange/blue orbit rings, diagonal light line and blue bottom-right wedge;
- frame 897: cut to MORRO.

The takeover card has 5.5% horizontal margins and slightly oversized top/bottom crop, creating the rounded, near-edge-to-edge visual area seen in the source.

## Other key corrections retained

- V26 cube camera sequence: portrait front at frame960, blue/gold clock at frame990, yellow 100K at frame1005, black glyph at frame1020; shallow pitch and narrow EASE lower fold.
- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame547: 3.7%.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.
- Launch Film preview states at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.

## Timeline

- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted 30-panel project wall
- 316–585: 28-cut source-indexed montage
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch Film interface, countdown preview and takeover
- 897–933: MORRO typography → large purple extruded symbol
- 933–945: standalone blue logo tile
- 945–1050: rotating illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source map, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates frame count/metadata/audio loudness, computes checksums and produces 1fps/2fps contact sheets.

A successful workflow proves technical validity, not artistic similarity. Compare the V28 candidate at frames 780/795/810/825/840/855/870/885/889/890/891/896/897, then the later cube frames and end card.
