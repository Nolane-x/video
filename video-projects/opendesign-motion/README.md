# OpenDesign Motion — frame-indexed reference reconstruction (V11)

Reference profile: 37.312s, 1920×1080, 30fps. Output target: 1,119 frames at 37.300s, 1920×1080, H.264 with AAC stereo 48kHz.

Audio analysis measured approximately 114.84375 BPM and identified a lower-energy passage around 19–21s. The replacement soundtrack is newly synthesized using these structural cues; source audio is not reused.

Timeline is frame-indexed at 30fps:
- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion mark reveal
- 170–240: open-source claim
- 240–316: tilted portfolio wall
- 316–585: 20-beat cut montage (269 frames)
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch film interface; source preview cuts at 780/795/810/825/840 and countdown 3/2/GO at 855/870/885
- 897–933: MORRO type → purple extruded mark → app tile transition
- 933–1050: rounded camera-like cube/app tile
- 1050–1119: OpenDesign Motion end card

V11 uses native decoded frame indices, with a corrected 20-beat montage: comic 1952/1962, 1965 dots, optical prism, pixel game, portfolio flash, MIND, rings, editorial grid, EASE/OUT/NEVER/LINEAR typography, transition, 80K→96K Star History, Motion Films, eye, Courses and metallic Future. The launch preview now matches the five observed artwork states and the countdown geometry; the MORRO transition now changes from large typographic repeats through a lilac extruded lettermark into the blue app tile. CI validates exact root/nested sequence ranges and technical output. Artwork remains independent vector/CSS/SVG work; without the original editable project, fonts and artwork layers, it is not described as pixel-identical.

Render only through the dedicated GitHub Actions workflow. CI verifies typecheck, frame count, metadata, loudness and contact sheets. A green workflow is only a technical gate. The output must still be compared against the reference at the same native frame indices, with contact-sheet review and quantitative image similarity reported by segment.
