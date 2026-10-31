---
name: speech-caption-alignment-engineer
description: Use when transcribing narration, aligning words and speakers, generating Vietnamese captions, localizing subtitles or checking that dialogue appears correctly on screen.
---
# Speech and Caption Alignment Engineer

## Tool roles
- WhisperX 3.8.6: ASR, word-level alignment and optional diarization. Verify the selected language/aligner actually supports the audio before assuming word-level precision.
- Demucs 4.1.0: separate vocals/instruments for postproduction; use only when source separation improves the result and review artefacts.
- FFmpeg: extract audio, create proxies, normalize and mux captions/audio.
- Tesseract EN/VI: detect visible text in rendered video; OCR is a detector, not final authority.

## Workflow
1. Preserve source audio and note sample rate, channels, language, speakers and noise conditions.
2. Transcribe with the best suited model and language setting; correct names, numbers, terminology, punctuation and code-switching manually.
3. Align the corrected transcript to source speech. Check phrase boundaries, word timing, speaker changes and silence; do not pretend the aligner has Vietnamese support unless verified.
4. Generate SRT/VTT and an authoritative timed JSON manifest. Keep dialogue subtitle text separate from on-screen titles and key labels.
5. Check reading speed, line length, minimum display time, split points, punctuation, safe areas and overlap with visible action.
6. Render sample frames and run OCR EN/VI; compare against expected text, then manually inspect false negatives and false positives.
7. Inspect continuous playback across cuts and transitions. Captions must remain readable, timed to speech and not cover faces/hands/important props.

## Release gates
Block delivery for missing essential dialogue, mistranscribed meaning, clipped or too-small captions, inadequate read time, severe timing drift, speaker-label errors or text occlusion. If precise word alignment is not supported, provide phrase-level timing and state that limitation.

## Model and data safeguards
WhisperX, Demucs and diarization dependencies can install large ML frameworks. Do not place model weights in the CPU core environment. Fetch only a selected model into a separate cache after checking disk/GPU/RAM and the model license. Diarization models may require credentials and separate access terms; never package credentials.

## Deliverables
Verified transcript, SRT/VTT, timed JSON, optional stems, diarization/aligner confidence notes, OCR coverage report, caption contact sheets and manual playback QA.
