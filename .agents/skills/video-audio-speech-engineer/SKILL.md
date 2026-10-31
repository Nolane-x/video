---
name: video-audio-speech-engineer
description: Use when producing voice-over, aligning Vietnamese speech, separating stems, designing sound, mastering dialogue/music or auditing caption coverage.
---
# Audio, Speech and Caption Engineer

- Keep the CPU video core separate from optional WhisperX/Demucs dependencies in `toolchain/python/audio-ml/requirements.txt`.
- Preserve original recordings and masters; work on copies and keep dialogue, music, ambience and spot effects as separate stems.
- Use WhisperX only after confirming that the selected language aligner supports the actual speech. Do not claim Vietnamese word-level accuracy without verification; use manually checked phrase timing when needed.
- Demucs source separation is optional; use it only when it improves the mix and inspect artefacts. Package licensing does not automatically cover model weights.
- Check diarization provider/model terms and credentials separately; never store credentials in repo files or CI artifacts.
- Measure final loudness/true peak after mastering; inspect synchronization and intentional silence.
- Ensure essential speech and key labels are readable on-screen long enough. OCR is a detector, followed by manual moving-picture review.
