# Remotion sample: One More Scroll

This is the first executable Remotion composition in the repository. It is a **silent 60-second motion prototype**, not yet a finished YouTube master: the purpose of this baseline is to prove that real Remotion can typecheck, render on a GitHub-hosted runner, and produce a downloadable MP4 artifact.

## Local run

```powershell
npm install
npm run typecheck
npm run dev
npm run render
```

Output: `out/one-more-scroll.mp4`.

## Character and visual direction

The character is a symbolic mascot (cream round head, slate body, simple eyes and line limbs) rather than a realistic person. The palette is charcoal, warm cream, muted slate, a restrained red temptation accent, and a warmer dawn ending. Eight 7.5-second shots form a 60-second timeline.

See `public/story/bible.md` for the character rules and `public/story/shots.json` for the shot plan.

## Before using as a published video

- Add approved music and SFX to `public/audio/` and place them on distinct timeline tracks.
- Replace placeholder actions with reviewed, continuous poses (hand/phone contact, alternating feet on stairs, contact/recovery in action beats).
- Render and visually inspect a contact sheet, including every shot boundary.
- Verify voice/caption timing, audio loudness and peaks, final metadata, and license/attribution records.
- Keep the H2 visual style restrained; don't add realistic human characters or glossy AI gradients by default.

The GitHub Actions job renders this composition and uploads the MP4 as an artifact. Artifact retention is temporary (7 days), so download any render you want to keep.
