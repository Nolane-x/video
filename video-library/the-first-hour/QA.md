# THE FIRST HOUR — QA and handoff

## Latest build — render #30 technical pass
- Workflow: [run #30 — success](https://github.com/Nolane-x/video/actions/runs/40429993407); all 17 steps passed.
- Source/render commit: [`1ab974acc2f8e0b268940fbf16f6b566884dace6`](https://github.com/Nolane-x/video/commit/1ab974acc2f8e0b268940fbf16f6b566884dace6), including the shared H2 scheduled-motion fix.
- Temporary Actions artifact: `the-first-hour-h2-selfimprove-30`, ID `12702200246`, 73,535,367 bytes; expires 2026-11-26T01:07:01Z. Not durable release storage.
- Master: 172.000 s, H.264 1920×1080 @24 fps, AAC 48 kHz stereo; 26,743,126 bytes.
- Master SHA-256: `f08c9afad88034b1ce7a0e57438f48391aa0a43ffcb3f59c8bbbc4339d25126b`.
- EBU R128: −14.1 LUFS integrated, 6.8 LU LRA, −2.5 dBFS true peak.
- Preview SHA-256: `cb0d5abe68a91bc3e1bf0fe34aea19594055d66f8ebd2780baea56feb9d56d8b`; 30.000 s, video and audio present.
- Review ZIP SHA-256: `e3b3c700d8f2cd585db8a889981370aa7412f9daf38acc9376398aa92eb37672`; every listed checksum passed after download.

## Targeted visual review
- [x] Both current-run contact sheets reviewed; all 29 authored shots appear.
- [x] B19 walk-to-desk proof sampled at 0.15, 1, 2.8 and 5.5 seconds: the character keeps coherent limbs through movement.
- [x] Existing targeted checks for B20 notebook line reveal and B25 punch-bag recoil remain represented in the current contact sheets.
- [ ] Individually watch all 12 proof clips with audio; the other ten were not all individually watched.
- [ ] Watch the complete 172-second master start-to-finish with audio.

## Technical gates
- [x] All 17 Actions steps passed; native H2 timeline, storyboard and contact-sheet generation completed.
- [x] Master H.264 1920×1080/24 fps + AAC 48 kHz stereo; duration 172.000 s.
- [x] EBU R128 −14.1 LUFS / 6.8 LU LRA / −2.5 dBFS true peak.
- [x] Twelve ~6-second motion proofs contain audio/video; checksum ledger passed after download.

**Technical pass; full-length artistic review pending.** The Actions artifact is temporary and this candidate is not yet archived to a durable GitHub Release. Do not replace the canonical ONE MORE SCROLL H2 master.
