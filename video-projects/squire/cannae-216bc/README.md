# Cannae — Squire long-form production

**Title:** How Hannibal Turned Rome's Army Into a Trap  
**Genre:** Historical military animation  
**Target:** 16:9 · 1920×1080 · 24 fps · English long-form film  
**Engine:** H2 Squire 2D/vector animation (not Remotion)

## Production flow

1. The workflow reads the current VoiceStudio manifest and resolves a suitable English narrator by exact current voice ID and eligibility metadata.
2. VoiceStudio renders narration on GitHub Actions, verifies the PCM master and AudioSeal provenance, and emits SRT/VTT sidecars.
3. Faster-Whisper aligns the spoken narration to line and word timelines. Interpolated timestamps remain identified in the alignment report.
4. Squire creates voice-timed shots; the Cannae director script authors maps, troop diagrams, character close-ups, formations, objects and tactical sequences.
5. Procedural Squire music and battle effects are mixed beneath the verified narration. FFmpeg measures loudness and true peak and checks final streams.
6. The workflow uploads the MP4, 45-second preview, contact sheets, thumbnail, master WAV, captions, alignment report, script, research ledger and QA evidence as one Actions artifact.

## Historical method

Force strengths are attributed to Polybius and treated as ancient estimates. Casualty counts are not presented as settled fact. Formation animations are explanatory reconstructions, not claims of exact archaeological reconstruction. The Squire character pack does not contain historically authenticated Punic/Iberian/Celtic uniforms; its generic ancient presets are visual shorthand and are labelled as such in the production bible.

## Review gate

A machine QA pass does not equal artistic approval. A person must watch the complete moving film, listen to the narration/music/SFX, inspect representative contact/action/recovery moments and check caption timing before publication.
