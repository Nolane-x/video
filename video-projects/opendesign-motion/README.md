# OpenDesign Motion — frame-indexed reference reconstruction (V29)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s source container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Original editable layers and typeface files are not available; do not claim pixel identity.

## V29 source-frame rebuild

V29 moves beyond the countdown/cube-only pass and fixes several high-error sections from V28 after checking source frames at native resolution.

### Poster sequence
- Frame300: camera scale and tilt increase on the 30-card project wall, so the composition is cropped/perspective-led rather than showing the entire grid uniformly.
- Frame330: rebuild the 1962 pop-art comic with two narrow side rails (yellow “ONE IDEA...” panel and pink halftone panel on the left; pink dots and yellow panel on the right), a central blue radial burst, yellow dotted halo, red rounded D-shaped play mark, black arrow, “MEANWHILE, IN 1962...” banner, “1962 POP ART” header, and yellow CLICK starburst.
- Frame345: 1965 Infinity dots is redrawn as a dense, irregular cream-white dot field, with a scalloped cream 1965 label and a yellow D-shaped play icon with black speckles.
- Frame420: concentric typography is scaled to about 1.88 so the circular type rings and large rotated words crop through the frame edges like the source.

### Launch Film UI and countdown
The app shell keeps its source-like window geometry, then animates the Preview panel using explicit frame landmarks:
- Frame780: outer application shell x118–1800, y72–1000; 586px left chat pane, preview card x≈732–1490 and y≈215–803.
- Frame885: preview card x≈528–1508, y≈128–882; countdown 1 remains inside the Preview.
- Frame889: preview card expands to x≈307–1784, y≈12–1080.
- Frame890: preview card expands to x≈196–1795, y≈0–1080.
- Frame891: full takeover card x≈117–1800, y≈0–1080 with the notched blue extruded numeral, near-horizontal orange/blue orbit rings and blue lower-right wedge.

These are frame-specific layout keyframes, not a generic scale-up. The 1 prism has a lower-left notch and bevelled top/right extrusion.

### MORRO ending
- Frame897: four staggered rows of oversized MORRO wordforms alternate solid black and outlined letters, cropped by the frame; a pale layered form appears in the center.
- Frame905: large centered cream rounded-square tile filled by overlapping MORRO letterforms.
- Frame915: blue/cream letter fragments and tall folded lavender ribbon shapes.
- Frame925: the blue/cream tile holds with the pink-violet folded form crossing the center.
- Frame933: the tile gives way to a glossy blue/black rounded application icon with a large white outlined play/camera mark.

The V26 camera cube remains carried forward: portrait front at frame960, blue/gold clock at frame990, yellow 100K at frame1005, black glyph at frame1020; shallow pitch and narrow EASE lower fold.

## Verified facts retained

- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame547: 3.7%.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.
- Launch Film preview states at 780/795/810/825/840 remain the ink-wash mountain, printed compass/comic panel, green OPEN DESIGN typography, black/white squiggle field and green EASE typography.
- MORRO frame map is explicitly audited at 897/905/915/925/933.

## Timeline

- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: project wall
- 316–585: 28-cut source-indexed poster montage
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch Film interface, Preview zoom and countdown
- 897–933: MORRO typography/collage/ribbon/app-tile transition
- 933–1050: illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

## Render and quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the frame map and source assertions, typechecks TypeScript, renders 1080p30, masters audio with FFmpeg, validates picture frame count/metadata/loudness, computes checksums and uploads the review bundle.

A successful workflow is a technical gate, not artistic sign-off. Inspect actual output frames at 300/330/345/420/780/885/889/890/891/897/905/915/925/933 and watch the whole moving sequence before any PR promotion.
