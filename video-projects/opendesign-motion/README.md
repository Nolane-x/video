# OpenDesign Motion — frame-indexed reference reconstruction (V39 candidate)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s source container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Original editable layers/fonts are unavailable, so pixel identity is not claimed.

## Current focus: reference-led visual corrections across the whole film

The source-indexed timeline remains fixed; each revision below is recorded against actual rendered frames and the supplied native preview.

### Opening and gallery
- V35 removed the lingering continuous top wave line, retained more open blue sky, strengthened the irregular cream-white lower-left cloud mass, and added broad broken diagonal washes with peach/pink glazing and a low blue/teal shoreline. Its Actions render passed, but review at delivery size found the cloud bank still too diffuse and horizontal.
- V36 passed validator, typecheck, Remotion render, FFmpeg mastering and decoded-frame/metadata QA in [Actions run 41315006194](https://github.com/Nolane-x/video/actions/runs/41315006194). Direct comparison of native frame 0 against `preview.mp4` showed the larger lower-left cloud mass and horizontal bands still differed materially from the original. V36 is preserved as a technical-pass candidate, not approved.
- V37 passed all technical gates in [Actions run 41315724268](https://github.com/Nolane-x/video/actions/runs/41315724268), but frame 0/30 review still found repeated scallop-like clouds, an almost flat blue foreground band, an undersized title, over-advanced typing at frame 30 and a misplaced cursor.
- V38 passed full CI and its native 0/30/60 frames were directly compared with the source. Headline size, typewriter cadence and cursor travel are now close to the reference. The painted sky is still too smooth, and the directory control is inside the white field rather than a separate translucent shelf.
- V39 adds dry-brush displacement, stronger pigment/paper texture, richer low cloud paint and separates the translucent directory shelf. It keeps the source-timed typing and cursor choreography; its Actions render is still required.
- The project wall has a stronger camera angle and diagonal crop, instead of appearing nearly front-on.
- The 1962 comic target is a circular red/cream pop-art mark with a yellow radial halo, replacing the rounded-square center.
- The 1965 Infinity dots mark is circular with yellow/red rings and black speckling on the irregular cream-white dot field.
- The 1973 optical study now separates a visible rainbow spectrum from the white diagonal prism beam.
- The 1985 pixel-game scene contains a hollow golden portal and a large white cursor sprite, not a generic D-shaped play icon.
- The MIND poster gains a translucent faceted glass prism at its center; the concentric-ring poster adds seven nested text paths to create the optical tunnel.

### Motion typography and data posters
- Kinetic words EASE / IN / OUT / NEVER / LINEAR are scaled to crop beyond the canvas edges at their source frame beats.
- The lime-green iris transition grows to a source-scale ring radius.
- The clock gains a tree silhouette, village edge and painterly water/sky strokes around the gold mechanism.
- Star History remains frame-keyed across all eight labels, with a slightly larger chart inset.
- The 3.7% eye is an angular blue-grid optical field with radial iris detail, on black, with the number bottom-right. It no longer uses a large white sclera.

### Launch Film, cube and MORRO
- Launch Film preview variant 0 now uses textured ink-wash mountains and an imperfect circular play mark.
- The cube's blue/gold 1889 clock remains on the top plane at source frame990 while a black glyph side faces the camera and the EASE underside is exposed. The black face is kept camera-facing during the clock beat; the mint/yellow 100K GitHub-stars face rotates forward at 1005.
- V32 fixes the cube's CSS plane mapping: the blue/gold 1889 clock is visibly on the top plane at frame990 while the black glyph faces the camera and the EASE fold sits below. At frame1005 the mint/yellow 100K halftone face becomes camera-facing and the clock moves to the adjacent side; at frame1020 the black glyph face returns.
- MORRO V31 now reaches a fully opaque 1,120px cream collage tile at frame905, contracts to a 720px blue/cream letter tile by frame915, then holds the broader lavender folded ribbons at frame925 before the glossy app mark.
- The end lockup is enlarged: a larger app tile, 96px class OpenDesign Motion wordmark, and prominent open-design.ai capsule.

## Source frame map

Key source-frame checks: 0/30/60 (opening); 300/330/345/353/368/386/420 (project wall and poster art); 456/461/466/471/476/486/496/498/500/510/511/516/523/530/547 (typography and data); 641/700 (Any/model); 780/885/889/890/891 (Launch Film/counter); 897/905/915/925/933 (MORRO); 960/990/1005/1020 (camera cube); 1118 (end card).

## Fixed timeline and technical output

- 0–83: painterly prompt intro
- 83–140: OpenDesign MOTION title
- 140–170: Claude Motion brand reveal
- 170–240: open-source claim
- 240–316: project wall
- 316–585: 28-cut source-indexed poster montage
- 585–641: Not just Opus 5.5
- 641–779: Any model / Any agent
- 779–897: Launch Film interface, preview zoom and countdown
- 897–933: MORRO typography/collage/ribbon/app-tile transition
- 933–1050: illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

Output: 1,119 picture frames, 1920×1080, 30fps, H.264 + AAC stereo 48kHz.

## Quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source assertions, typechecks TypeScript, renders, masters with FFmpeg, checks frame count/metadata/loudness and uploads the MP4/contact sheets/metadata/checksums.

A green workflow is a technical gate, not artistic sign-off. Inspect the latest rendered candidate at the source-frame map above, watch the full moving sequence and compare with the supplied reference before changing PR #31 from Draft or promoting a release.
