# OpenDesign Motion — frame-indexed reference reconstruction (V19)

Reference profile: 37.312s container, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118). Output target: 37.300s picture, H.264, AAC stereo 48kHz.

The supplied `preview.mp4` remains the visual source of truth. Artwork is independently authored Remotion/SVG/CSS. The original editable project, proprietary source fonts and original artwork layers were not supplied, so this is a reference-led reconstruction and is not claimed to be pixel-identical.

## V19 corrections from native-frame comparison

- The kinetic-type section now follows the original frame order: IN at frame 496, LINEAR reveal by frame 500, green dot during the hold, and the lime ring/play transition starting at frame 510. The clock remains anchored at frame 516, so the full 269-frame montage stays contiguous.
- Star History now uses the eight source-observed values, keyed to the eight frames rather than a linear approximation: 80K/Day88, 82K/Day96, 84K/Day104, 87K/Day111, 91K/Day119, 93K/Day126, 94K/Day132, and 96K/Day138.
- Enlarged and strengthened the concentric circular typography and metallic IN lettering; the toggle retains its isolated minimal form.
- Increased the dimensional layers on FUTURE, reduced the cube's rotation so more faces remain visible, and replaced the lens-only cube face with a camera-screen composition and illustrated portrait.
- The V18 Launch Film previews, optical poster, project wall, repeated MIND type, particle viewport, clock, eye readout and end card remain in the reconstruction.

## Verified source facts

- Source: 1,119 frames, 1920×1080, 30fps.
- Star History frames 523–530: 80K/Day88; 82K/Day96; 84K/Day104; 87K/Day111; 91K/Day119; 93K/Day126; 94K/Day132; 96K/Day138.
- Eye readout at frame 547: 3.7%.
- Launch Film preview states at 780/795/810/825/840: ink-wash mountain/play emblem; printed 1962 compass/comic panel; green OPEN DESIGN typography; black/white squiggle field; green EASE typography.
- Typography transition: frame496 IN, frame498 LINEAR reveal, frame500 LINEAR with green dot, frame510 green ring transition, frame511 inner ring/play mark, frame516 clock.

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

A green Actions run confirms technical validity only. The generated MP4 must still be compared side-by-side with the supplied reference at identical native frame indices and watched as a moving sequence. See `shot-map.json` for the source-frame ledger and V19 audit checkpoints.

## Exact-frame montage ledger

Absolute source frames: 316–318 gallery exit; 318–322 comic 1952; 322–338 comic 1962; 338–353 dots; 353–368 optical logo; 368–381 pixel game; 381–386 portfolio wall; 386–400 MIND; 400–430 circular typography; 430–446 editorial grid; 446–456 particle viewport; 456–461 EASE; 461–466 metallic IN; 466–471 IN.; 471–476 EASE; 476–486 OUT; 486–496 NEVER; 496–510 LINEAR; 510–516 green circular mark; 516–523 clock; 523–531 Star History; 531–539 toggle; 539–547 Motion Films; 547–555 eye; 555–563 Courses; 563–570 comic; 570–578 FUTURE; 578–585 Not.
