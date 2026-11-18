# Nếu Bạn Có Thể Dừng Thời Gian Trong 10 Giây?

A standalone, original H2 Canvas/Chromium production for the time-stop story. It is deliberately separate from the existing “Mua Thời Gian” film and does not call Higgsfield, Runway, paid image APIs, or paid video APIs.

## Target master

- Runtime: 6 minutes 18 seconds
- Storyboard: 84 shots across 7 acts
- Frame rate: 30 fps
- Frame size: 1920 × 1080 (16:9 cinematic scope)
- Rendering: H2 Studio Canvas + Chromium + FFmpeg
- Audio: procedural H2 music beds and SFX; no synthetic narrator is generated
- Story-specific visuals: reusable cyan time-freeze overlay, suspended-particle treatment, bicycle and tilting billboard props for the rescue sequence

The project uses the repository’s existing H2 character rig and environment system. It does not use the paid 3D Jutsu renderer.

## Run locally or in a compatible Linux runner

From the repository root, run these commands:

    cd integrations/h2-selfimprove-studio/skills/lam-video-selfimprove/kit
    npm install
    npx playwright install chromium
    python -m pip install numpy scipy soundfile pyloudnorm
    python audio/build_audio.py
    python ../../../../../video-projects/time-stop-10s/scripts/build_story.py --project-dir projects/time-stop-10s
    node render.mjs --project projects/time-stop-10s --check --scale 0.25
    node render.mjs --project projects/time-stop-10s --sheet --scale 0.5 --at 0.45
    node render.mjs --project projects/time-stop-10s --workers 4 --crf 19
    python tools/mix.py --project projects/time-stop-10s

The master is written to kit/projects/time-stop-10s/out/time-stop-10s.mp4. The workflow archives the master, a 30-second preview, contact sheets, metadata, and QA results as a GitHub Actions artifact.

## GitHub Actions

The workflow is .github/workflows/render-time-stop-10s.yml. A push to this feature branch that changes the project, H2 renderer, or workflow starts a render. It can also be started manually from the Actions tab using the workflow_dispatch event.

## Review gates

A successful Actions run proves the build and export completed; it does not prove the film is artistically approved. Review all contact sheets and moving frames around:
- the first accidental freeze and cup catch
- the basketball save
- the mother's bicycle approaching the falling sign
- the final 10-second rescue, sign impact, and recovery/embrace

Do not replace an approved master with a candidate until visual and audio QA has been reviewed.
