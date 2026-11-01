# OpenDesign Motion — frame-indexed reference reconstruction (V21)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V21 fixes after V20 source-frame review

V20's cube still revealed the portrait face at frame 945 instead of holding it for source frame 960, then brought the blue clock face forward too early. V21 now stages the end sequence as:
- frames 933–944: separate blue rounded-square emblem tile;
- frame 945: rounded camera cube begins to rotate;
- frame 960: portrait screen is the intended front face, black emblem on the adjacent side;
- frame 975: three-quarter blue/black/lime composition;
- frame 990: blue/gold clock surface with lime underside;
- frame 1005: yellow 100K editorial face;
- frame 1020: black emblem face and cream editorial side;
- frame 1050 onward: end-card logo and wordmark.

The V20 enlarged end card was slightly less similar in the exact-frame comparison, so V21 restores the previous smaller group sizing while preserving the enlarged V20 MORRO purple symbol.

## Verified content carried forward

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
- 933–945: standalone blue logo tile
- 945–1050: rotating illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source map, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates frame count/metadata/audio loudness, computes checksums and produces 1fps/2fps contact sheets.

A successful workflow proves technical validity, not artistic similarity. The rendered MP4 must still be compared with the supplied reference at identical native frame indices and watched as a moving sequence. Key V21 frame checks are 933/945/960/975/990/1005/1020/1050/1118.
