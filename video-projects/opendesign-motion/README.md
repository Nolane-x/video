# OpenDesign Motion — frame-indexed reference reconstruction (V20)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are not available; no pixel-identical claim is made.

## V20 corrections after reviewing V19 output

V19 passed every technical gate but still had clear visual defects in the last 8 seconds:
- At frame 933 the source holds a large purple extruded MORRO symbol, while V19 showed a small unrelated dark play-button tile.
- At frames 960–1020 the source rotates a multi-faced rounded camera object through a portrait screen, black glyph/arrow face, blue clock artwork and lime EASE surface. V19 kept the play-mark face in front and showed an unrelated red OpenDesign side.
- V19's end-card group was visibly undersized against the source wordmark and domain capsule.

V20 replaces the MORRO transition with a larger ribbon-like purple mark, rebuilds the six cube faces with source-specific graphic surfaces, increases the cube's rotation so the observed face changes appear during the shot, and scales the end card logo, title and URL capsule to a more faithful visual hierarchy.

## Previously corrected facts retained

- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame 547: 3.7%.
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
- 779–897: Launch Film interface and countdown
- 897–933: MORRO typography → large purple extruded symbol
- 933–1050: rotating illustrated rounded camera object
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source map, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates frame count/metadata/audio loudness, computes checksums and produces 1fps/2fps contact sheets.

A successful workflow proves technical validity, not artistic similarity. The V20 MP4 must still be compared against the supplied reference at identical native frame indices, especially 897/925/933/945/960/990/1020/1050/1118, then watched as a moving sequence.
