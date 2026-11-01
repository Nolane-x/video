# OpenDesign Motion — frame-indexed reference reconstruction (V27)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V27 countdown timing fix

Native-frame inspection of the reference around frames 880–900 showed that the large extruded number 1 remains inside the Launch Film Preview pane at frame885; the app/window UI is still present. The preview then expands to a near-full-screen view around frames889–890, and the full-screen countdown shot follows around frame891. V27 corrects the timing:
- frame855: 3 inside Preview
- frame870: 2 inside Preview
- frames885–890: 1 inside Preview while the Launch Film UI scales/crops away
- frame891: full-screen CountdownOne begins
- frame897: cut to the MORRO transition

The V26 camera cube changes remain: portrait at frame960, blue clock at frame990, yellow 100K at frame1005 and black glyph at frame1020, with the shallow camera pitch and narrow EASE lower fold.

## Verified content carried forward

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
- 779–897: Launch Film interface, preview countdown and transition
- 897–933: MORRO typography → large purple extruded symbol
- 933–945: standalone blue logo tile
- 945–1050: rotating illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source map, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates frame count/metadata/audio loudness, computes checksums and produces 1fps/2fps contact sheets.

A successful workflow proves technical validity, not artistic similarity. Compare candidate frames 855/870/885/890/891/897 and the later cube frames against the same indices in the source, then watch the whole sequence.
