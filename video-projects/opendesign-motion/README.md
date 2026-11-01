# OpenDesign Motion — frame-indexed reference reconstruction (V13)

Reference profile: 37.312s, 1920×1080, 30fps. Output target: 1,119 frames at 37.300s, 1920×1080, H.264 with AAC stereo 48kHz.

Audio analysis measured approximately 114.84375 BPM and identified a lower-energy passage around 19–21s. The replacement soundtrack is newly synthesized using these structural cues; source audio is not reused.

Timeline is frame-indexed at 30fps:
- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted portfolio wall
- 316–585: 20-cut source-frame montage (269 frames)
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch film interface; source preview cuts at 780/795/810/825/840 and countdown 3/2 at 855/870, full-screen 1 at 885
- 897–933: MORRO type → purple extruded mark → app tile transition
- 933–1050: rounded camera-like cube/app tile
- 1050–1119: OpenDesign Motion end card

V13 rechecked the rendered output against exact source-frame pairs. The 20 montage cuts now follow the observed reference sequence and boundaries: 1952 comic, 1962 comic, infinity dots, optical refraction, pixel-game world, MIND, circular typography, editorial poster grid, point-cloud depth, EASE, OUT, green transition, IN, LINEAR, green wipe, illustrated clock, toggle, eye, repeated comic and metallic FUTURE. The launch preview has five distinct source-matched compositions; countdown 3/2 remains inside the app window and 1 takes over the full screen. Opening prompt, title scale and claim reveal were also rebuilt after side-by-side frame review. Artwork is independently authored SVG/CSS; without the original editable project, source fonts and proprietary art layers, it is not described as pixel-identical.

Render only through the dedicated GitHub Actions workflow. CI verifies typecheck, frame count, metadata, loudness and contact sheets. A green workflow is only a technical gate. The output must still be compared against the reference at the same native frame indices, with contact-sheet review and quantitative image similarity reported by segment.
