# Nếu Bạn Có Thể Dừng Thời Gian Trong 10 Giây?

An original 6-minute-18-second Vietnamese animated short built with the repository's H2 Canvas/Chromium renderer, a Three.js scene layer for selected action sequences, VoiceStudio narration and FFmpeg mastering. It is separate from the existing “Mua Thời Gian” film.

The project does not depend on paid generative-video APIs or paid image-generation APIs. Native H2, the bundled Three.js engine, locally executed procedural audio and the GitHub Actions workflow provide the render path.

## Current production target

- Runtime: 378 seconds (6 minutes 18 seconds).
- Story: 84 shots across 7 acts, each 4.5 seconds.
- Frame size: 1920 × 1080, 16:9.
- Current candidate branch: native 60 fps (22,680 frames).
- Rendering: H2 Canvas/Chromium + FFmpeg, with Three.js for selected 3D blocking/action.
- Visual split: 42 of 84 shots use Three.js 3D; the remaining 42 use H2 Canvas 2D.
- Vietnamese narration: 84 shot-aligned VieNeu/VoiceStudio segments, generated and AudioSeal-verified in GitHub Actions.
- Music/SFX: original procedural H2 audio, mixed to the film master.
- Signature visual language: restrained cyan time-freeze rings and suspended particles, warm practical lights against plum/charcoal environments, clear prop contact and purposeful camera changes.

The current branch's native-60fps switch is .github/workflows/enable-time-stop-native-60fps.txt with the exact content native-60fps. The render workflow supports both 30 and 60 fps; without that switch, it falls back to 30 fps. Do not remove or edit the switch when reproducing the current candidate.

## Render through GitHub Actions

Workflow: .github/workflows/render-time-stop-10s.yml.

A push to a matching film/time-stop-10s-* branch that changes the project, H2 renderer or workflow starts the production pipeline. The workflow builds the 84-shot story, creates the per-shot Vietnamese narration request, renders and verifies VoiceStudio audio, checks all H2 shots, creates contact sheets and a 30-second motion preview, renders the full master, mixes music/SFX, and packages the MP4, subtitle files and QA report.

Latest source and render status should always be checked from GitHub Actions rather than inferred from an older local copy.

## Compatible Linux runner / local reproduction

From the repository root:

    cd integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit
    npm install
    npx playwright install chromium
    python -m pip install numpy scipy soundfile pyloudnorm
    python audio/build_audio.py
    python ../../../../../video-projects/time-stop-10s/scripts/build_story.py --project-dir projects/time-stop-10s --fps 60
    node render.mjs --project projects/time-stop-10s --check --scale 0.25
    node render.mjs --project projects/time-stop-10s --sheet --scale 0.5 --at 0.45
    node render.mjs --project projects/time-stop-10s --workers 2 --crf 19
    python tools/mix.py --project projects/time-stop-10s

The master is written to kit/projects/time-stop-10s/out/time-stop-10s.mp4. These commands reproduce the H2 render/mix stage; VoiceStudio narration must also be rendered and placed onto the timeline using the repository's place_voiceover.py workflow step to reproduce the current fully narrated candidate.

## Review and approval gates

A green Actions run establishes technical completion, not artistic approval. The QA report deliberately keeps visual_approval: false until a human completes an uninterrupted full-length watch with audio.

Review at least:
- s002 alarm-clock close-up: the clock must be fully in frame and readable.
- s014–s019 cup fall, freeze and catch; verify the protagonist and suspended cup remain framed.
- s026–s033 basketball release, run, retrieval and return hand-off.
- s037–s042 hallway book rescue and transfer.
- s061–s072 final bicycle/sign rescue, impact, recovery and embrace.
- Narration/subtitle timing, intelligibility, music/SFX balance, transitions and any extended black or static intervals.

Use the independent run-specific inspection workflow and compare its SHA-256 with the exact render artifact. Keep draft candidates separate from published releases; never overwrite the preserved run-20 release or set visual_approval true based on CI alone.
