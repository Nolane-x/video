# OpenDesign Motion — frame-indexed reference reconstruction (V26)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Source-specific fonts and original layered artwork are unavailable; no pixel-identical claim is made.

## V26 cube correction after comparing V24 and V25

V24 was stronger than V25 on the key cube frames (SSIM: 960 0.8604 vs 0.8415; 990 0.8187 vs 0.7984; 1005 0.8536 vs 0.8240). V25's more extreme negative camera pitch made the main clock face turn away from the viewer. V26 restores a shallow pitch while keeping the better frame-keyed front/side artwork:
- frame960 / local f15: portrait front, black symbol adjacent;
- frame990 / local f45: clock stays dominant on the front; blue side graphic remains adjacent; EASE becomes a narrow 10%-height lower fold;
- frame1005 / local f60: yellow 100K face comes forward with the blue graphic side retained;
- frame1020 / local f75: black glyph returns to the front.

Pitch is now approximately 4° at local f15, 10° at f45, 4° at f60 and 0° at f75. The EASE strip is at 84% vertical position and 10% height to prevent covering the clock.

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

A successful workflow proves technical validity, not artistic similarity. Compare the V26 candidate at frames 933/945/960/975/990/1005/1020/1035/1049/1050/1080/1118 and watch the moving sequence.
