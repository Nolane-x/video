# Voice-over generation through VoiceStudio Actions

This is an **opt-in** voice-over workflow for video projects. The normal render
workflows remain unchanged and do not add synthetic narration automatically.
Use it when the user or approved storyboard explicitly requests a narrator,
character dialogue or spoken explanation.

## What it does

The video repository sends a structured JSON narration job to the public
`Nolane-x/VoiceStudio` reusable GitHub Actions workflow. VoiceStudio performs
CPU/ONNX synthesis, audio mastering, provenance marking and post-write checks.
The video repository then downloads and verifies the result.

No Electron app, local model install, self-hosted GPU, paid voice API or binary
audio commit is required.

## Run it

Open **Actions → Render AI voice-over with VoiceStudio → Run workflow** and
paste the JSON job into `job_json`. The schema and bilingual examples live in
[VoiceStudio's video-job contract](https://github.com/Nolane-x/VoiceStudio/tree/main/voice-library).

A valid Vietnamese request looks like this:

```json
{
  "schema_version": 1,
  "job_id": "the-first-hour-vi-narrator",
  "title": "The First Hour — Vietnamese narration",
  "language": "vi",
  "engine": "vieneu",
  "voice_id": "vi-vieneu-v3turbo-adam-bua-87e364",
  "segments": [
    {
      "id": "opening",
      "text": "Xin chào. Hôm nay, chúng ta sẽ cùng bắt đầu câu chuyện này.",
      "pause_ms_after": 350
    },
    {
      "id": "turning-point",
      "text": "Đôi khi, thay đổi lớn nhất bắt đầu từ một lựa chọn rất nhỏ.",
      "pause_ms_after": 500
    },
    {
      "id": "closing",
      "text": "Cảm ơn bạn đã theo dõi. Hẹn gặp lại trong câu chuyện tiếp theo.",
      "pause_ms_after": 0
    }
  ]
}
```

Use an exact language-specific `voice_id` from the current VoiceStudio
`voice-library-latest` manifest. The ID above is an example only; always
confirm it exists in the manifest before production. VieNeu preset voices are
the recommended starting point for public/monetized videos because the
upstream model card documents preset consent and commercial use of generated
audio. Piper LibriTTS High is a separate English option with restricted rights
evidence and must not be treated as blanket commercially cleared.

## Artifacts

The workflow publishes two artifacts to the same run:

- `video-voice-assets-<run_id>` — the original VoiceStudio result
- `video-voiceover-ready-<run_id>` — the same package plus `ffprobe.json`,
  after the video repository verifies format, SHA-256, duration metadata,
  captions and VoiceStudio AudioSeal watermark status

Each package contains:

- `narration.wav` — mono 48 kHz PCM-24 voice master, mastered to -18 LUFS
  integrated and -1.5 dBTP true-peak ceiling
- `captions.srt` and `captions.vtt` — captions timed to the measured audio
  chunks
- `transcript.txt` — the narration text
- `manifest.json` — speaker/model provenance, segment timing, audio metrics,
  checksum and watermark verification
- `build-summary.txt` and `video-voice-assets.zip`

Download `video-voiceover-ready-<run_id>` from the successful Actions run.
For the H2 kit, copy `narration.wav` to the target project's
`timeline/voice.wav`; use the manifest's segment timings and the SRT/VTT
captions when placing lines. The historic `prep_voice.py` path expects
`blocks.json`, `lines.json` and `words.json`; those are not synthesized by
this first integration. Do not fabricate word-level alignment from subtitle
timings. Use a dedicated forced-alignment/ASR pass before any project feature
that needs word-by-word animation.

## Quality and release gate

The workflow is configured to reject non-mono/non-48 kHz/non-PCM-24 output,
failed SHA-256 checks, failed watermark detection, non-finite samples,
unexpected RMS/clipping, or missing captions. It also retains the selected
voice ID and model revisions in the manifest.

These are technical checks, not artistic sign-off. Before using the voice in a
published film, listen to the full narration and review pronunciation,
Vietnamese tones, pacing, emotional fit, pauses, names, and synchronization.
Fix the script and rerender rather than hiding a pronunciation problem with
video cuts. Do not assume a green Action means a voice-over is artistically
approved.
