# OpenDesign Motion — reference-led reconstruction

Reference profile: 37.312s, 1920×1080, 30fps. Output target: 1,119 frames at 37.300s, 1920×1080, H.264 with AAC stereo 48kHz.

Audio analysis measured approximately 114.84375 BPM and identified a lower-energy passage around 19–21s. The replacement soundtrack is newly synthesized using these structural cues; source audio is not reused.

Timeline:
- 0.00–2.77 cloud prompt and send
- 2.77–5.77 OpenDesign MOTION hero
- 5.77–6.97 Claude Motion brand mark
- 6.97–8.13 open-source positioning
- 8.13–10.70 deep project gallery
- 10.70–20.00 24-beat motion-design montage
- 20.00–21.37 Not just Opus 5.5
- 21.37–25.97 Any model / Any agent
- 25.97–29.83 Launch film interface, preview changes and countdown
- 29.83–31.10 MORRO-to-app-tile transition
- 31.10–35.30 one rotating 3D cube
- 35.30–37.30 OpenDesign Motion end card

The shot map is the authoritative source for exact frame ranges. CI validates the map against JSX sequence order before rendering. Art is independently authored and does not use source frames as backgrounds. The Launch film frame stays fixed while its preview viewport changes. The cube is a single rounded six-face object, resolving into the final icon.

Render only through the dedicated GitHub Actions workflow. CI verifies typecheck, frame count, metadata, loudness and contact sheets. A green workflow is a technical gate; full motion playback and audio listening are still needed for artistic approval.
