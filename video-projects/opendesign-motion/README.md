# OpenDesign Motion — frame-indexed reference reconstruction (V16)

Reference profile: 37.312s, 1920×1080, 30fps. Output target: 1,119 frames at 37.300s, 1920×1080, H.264 with AAC stereo 48kHz.

Audio analysis measured approximately 114.84375 BPM and identified a lower-energy passage around 19–21s. The replacement soundtrack is newly synthesized using these structural cues; source audio is not reused.

Timeline is frame-indexed at 30fps:
- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted portfolio wall
- 316–585: 28-cut source-frame montage (269 frames)
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch film interface; source preview cuts at 780/795/810/825/840 and countdown 3/2 at 855/870, full-screen 1 at 885
- 897–933: MORRO type → purple extruded mark → app tile transition
- 933–1050: rounded camera-like cube/app tile
- 1050–1119: OpenDesign Motion end card

V13 rechecked the rendered output against exact source-frame pairs. The 20 montage cuts now follow the observed reference sequence and boundaries: 1952 comic, 1962 comic, infinity dots, optical refraction, pixel-game world, MIND, circular typography, editorial poster grid, point-cloud depth, EASE, OUT, green transition, IN, LINEAR, green wipe, illustrated clock, toggle, eye, repeated comic and metallic FUTURE. The launch preview has five distinct source-matched compositions; countdown 3/2 remains inside the app window and 1 takes over the full screen. Opening prompt, title scale and claim reveal were also rebuilt after side-by-side frame review. Artwork is independently authored SVG/CSS; without the original editable project, source fonts and proprietary art layers, it is not described as pixel-identical.

Render only through the dedicated GitHub Actions workflow. CI verifies typecheck, frame count, metadata, loudness and contact sheets. A green workflow is only a technical gate. The output must still be compared against the reference at the same native frame indices, with contact-sheet review and quantitative image similarity reported by segment.


## V16 exact-frame cut ledger

Absolute source frames: 316-318 gallery exit; 318-322 comic 1952; 322-338 comic 1962; 338-353 dots; 353-368 prism; 368-381 pixel game; 381-386 World/Wide; 386-400 MIND; 400-430 circular typography; 430-446 editorial grid; 446-456 particles; 456-461 EASE; 461-466 metallic IN; 466-471 IN.; 471-476 EASE; 476-486 OUT; 486-496 NEVER; 496-511 LINEAR; 511-516 green icon transition; 516-523 clock; 523-531 stats; 531-539 toggle; 539-547 Motion Films; 547-555 eye; 555-563 Courses; 563-570 comic; 570-578 FUTURE; 578-585 Not.
