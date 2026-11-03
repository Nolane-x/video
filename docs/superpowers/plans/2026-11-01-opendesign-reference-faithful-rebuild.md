# OpenDesign Motion Reference-Faithful Rebuild Plan

Goal: rebuild the 37.3-second short around the supplied reference's actual scene order, poster sequence, Launch film interface, single cube and end card.

Architecture: retain Remotion and the GitHub Actions-only renderer. The JSON shot map is the frame authority and a pre-render validator compares it with JSX. All artwork and audio remain independently authored.

Global constraints: 1920×1080, 30fps, 1,119 frames, H.264/AAC stereo 48kHz. Preserve main, the canonical H2 master and the previous V6 delivery. Do not use source-frame backgrounds or the embedded soundtrack. Render on Actions only.

Review focus: montage order and timing; fixed Launch film UI while the preview changes; one correctly oriented six-face cube; readable labels and URL; 114.84375 BPM with 19–21s energy reset.

Task 1: record 12 contiguous section ranges and 24 montage beats in shot-map.json. Add a validator that checks JSX order, cumulative frame counts, interface identifiers and soundtrack BPM.

Task 2: re-time the opening, hero, brand, positioning, gallery, montage and capabilities sequence. Add comic, prismatic sweep, pixel-game, poster grid, point cloud, 84K stats and course mascot designs. Rebuild the fixed Launch film window, preview states, countdown, MORRO transition, one cube and end card.

Task 3: replace the score with an original layered arrangement, add validator and decoded-frame-count checks to Actions, then render and inspect full motion, contact sheets and audio.
