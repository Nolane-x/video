# OpenDesign Motion — frame-indexed reference reconstruction (V66 candidate)

Reference: `preview.mp4`, 1920×1080, 30fps, 1,119 decoded picture frames (0–1118), 37.312s source container. Output target: 37.300s picture, H.264, AAC stereo 48kHz.

This is an independently authored Remotion/SVG/CSS reconstruction, not the original editable project. Original editable layers/fonts are unavailable, so pixel identity is not claimed.

## Current focus: reference-led visual corrections across the whole film

Latest authored revision: V47. Latest technically verified render is V45 / Actions #104; V46 art changes are retained, with V47 repairing a stale validator check before the render can run.

The source-indexed timeline remains fixed; each revision below is recorded against actual rendered frames and the supplied native preview.

### Opening and gallery
- V35 removed the lingering continuous top wave line, retained more open blue sky, strengthened the irregular cream-white lower-left cloud mass, and added broad broken diagonal washes with peach/pink glazing and a low blue/teal shoreline. Its Actions render passed, but review at delivery size found the cloud bank still too diffuse and horizontal.
- V36 passed validator, typecheck, Remotion render, FFmpeg mastering and decoded-frame/metadata QA in [Actions run 41315006194](https://github.com/Nolane-x/video/actions/runs/41315006194). Direct comparison of native frame 0 against `preview.mp4` showed the larger lower-left cloud mass and horizontal bands still differed materially from the original. V36 is preserved as a technical-pass candidate, not approved.
- V37 passed all technical gates in [Actions run 41315724268](https://github.com/Nolane-x/video/actions/runs/41315724268), but frame 0/30 review still found repeated scallop-like clouds, an almost flat blue foreground band, an undersized title, over-advanced typing at frame 30 and a misplaced cursor.
- V38 passed full CI and its native 0/30/60 frames were directly compared with the source. Headline size, typewriter cadence and cursor travel are now close to the reference. The painted sky is still too smooth, and the directory control is inside the white field rather than a separate translucent shelf.
- V39 passed all CI gates and restored the translucent directory shelf. Its dry-brush texture improved the paint surface, but review found too many parallel high-contrast upper-sky lines.
- V40 reduces the upper-sky marks to a few broad irregular watercolor washes, while retaining the source-timed 0/30/60 typing and cursor choreography plus the separate directory shelf. Render [#99](https://github.com/Nolane-x/video/actions/runs/41318630418) passed the 1,119-frame, 1080p/30fps, audio and checksum gates; V40 remains a technical candidate pending full watch-through.
- V41 rendered successfully in [Actions #100](https://github.com/Nolane-x/video/actions/runs/41320461921). Native-frame review tightened S08 colors and the Any/model/agent order, but found the model type-on starts at frame645, the text must clear as the logo orbit forms at760, and Launch Film begins at769.
- V42 introduced the model type-on at645, dynamic capability typography, the provider-orbit replacement and Launch Film at769. Actions #101 stopped at a stale validator string that still expected V41's static layout; no render was produced. V43 updates that guard and rendered successfully in [Actions #102](https://github.com/Nolane-x/video/actions/runs/41321380345). Visual review confirmed the S08/Launch cut and countdown timing, then identified that the opening prompt typed too slowly, the pointer missed the send control, and its painted lower cloud/horizon still looked too geometric.
- V44 rendered successfully in [Actions #103](https://github.com/Nolane-x/video/actions/runs/41322081460), with 1,119 frames, 1080p/30fps, H.264/AAC and −14 LUFS mastering. Native frame comparison confirmed the frame30/60 prompt card still translated upward by roughly 62 px and expanded horizontally relative to the reference. V45 rendered successfully in [Actions #104](https://github.com/Nolane-x/video/actions/runs/41323121518). Its source-sized opening controls and pointer were verified; the remaining high-impact differences were the small kinetic poster scale, missing white iris bloom at frame511, abstract clock background, overly front-on late cube turns and small end-card lockup. V46 enlarges the EASE/IN/OUT/NEVER/LINEAR typography, adds the white iris disc, paints hills/trees/village around the 1889 clock, gives the cube more perspective and late-side exposure, and rebuilds the end logo ring with a delayed open-design.ai pill. Actions #105 stopped at a stale frame-510 shot-map phrase; V50 rendered successfully in [Actions #109](https://github.com/Nolane-x/video/actions/runs/41392928299). Frame345 improved versus V45 (SSIM −0.044 → 0.031), but direct review found the badge ~30 px too low and its speckles/dots too regular. V50 also showed V46's kinetic scale regressed the reference (frame456 SSIM 0.570 → 0.517), the frame420 rings lacked alternating paper/ink bands, and the 1889 backdrop remained geometric. V51 rendered successfully in [Actions #112](https://github.com/Nolane-x/video/actions/runs/41394247954). Native-frame review showed frame420's inner paths doubled their radius, frame456's EASE remained too narrow/tall, and frame461's metallic IN sat too low. V52 creates 12 consistent ring radii, scales EASE with non-uniform X/Y transforms, moves and stretches the metallic IN, and softens the clock's artificial halo rings. V52 passed CI and was rendered for manual review. V53 rendered successfully in [Actions #117](https://github.com/Nolane-x/video/actions/runs/41420760497), at 1920×1080, 30fps, 1,119 frames, plus AAC stereo 48kHz. Frame345 and frame420 are substantially closer; frame516 has a painted blue night and gold clock. Visual review of frames456/461 found duplicate title text and dark HUD on black; cube review showed the camera/100K/play panels were still reversed or duplicated. V55 corrects these visible-face assignments and improves HUD contrast/timecode. Actions #110 stopped before render because the validator still expected the removed `ring-v30-g` path; V52 updates that guard to the eight V51 ring IDs.
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
- 641–769: Any model / Any agent
- 769–897: Launch Film interface, preview zoom and countdown
- 897–933: MORRO typography/collage/ribbon/app-tile transition
- 933–1050: illustrated rounded camera cube
- 1050–1119: OpenDesign Motion end card

Output: 1,119 picture frames, 1920×1080, 30fps, H.264 + AAC stereo 48kHz.

## Quality control

Render only through `.github/workflows/render-opendesign-motion.yml`. Actions validates the timeline and source assertions, typechecks TypeScript, renders, masters with FFmpeg, checks frame count/metadata/loudness and uploads the MP4/contact sheets/metadata/checksums.

A green workflow is a technical gate, not artistic sign-off. Inspect the latest rendered candidate at the source-frame map above, watch the full moving sequence and compare with the supplied reference before changing PR #31 from Draft or promoting a release.
