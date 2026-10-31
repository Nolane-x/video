---
name: comfyui-graph-orchestrator
description: Use when authoring, inspecting, importing, validating or running node-based ComfyUI workflows for image, video, audio, masking, upscaling or 3D generation.
---
# ComfyUI Graph Orchestrator

## Environment gate
- Check whether ComfyUI is local, remote or hosted and record the exact version/commit, Python runtime, PyTorch/CUDA, VRAM, disk and custom-node registry.
- Treat ComfyUI itself (GPL-3.0), each custom node, each model/checkpoint/LoRA/VAE, workflow JSON, prompt and generated output as separate provenance/licensing objects.
- Never download multi-GB checkpoints, install custom nodes, expose an endpoint or launch a GPU job without the user's explicit approval and a resource/cost review.
- Do not modify `video-library/**`, resource downloader code or the other agent's asset catalog.

## Graph workflow
1. Inspect graph JSON and node classes. Build a dependency table of required custom nodes, exact versions, model names and input/output dimensions.
2. Reject unknown nodes, embedded executable scripts, suspicious URLs, shell commands or arbitrary code execution until reviewed.
3. Validate model filenames, hashes and license/usage terms. A node package license does not cover weights or datasets.
4. Define a small smoke graph first: load one authorized input, perform one transform, save one output and record node versions.
5. Keep all critical text, chart labels and UI in deterministic vector/video layers rather than a generative model output.
6. Pin seeds, sampler, scheduler, steps, CFG, denoise, dimensions, FPS, frames, batch size and motion settings where available.
7. Run on isolated paths/endpoints. Keep outputs outside the resource-library root unless the resource owner explicitly requests ingestion.
8. Compare output against the shot brief and reject flicker, face/character drift, broken hands, temporal jumps, watermarks, warped objects and false text.

## Security and operations
- Do not expose ComfyUI's unauthenticated API to the public internet.
- Use trusted extensions and least-privilege filesystem/network access; isolate custom-node installation.
- Keep API tokens outside graph JSON and repository files; redact secrets from logs/artifacts.
- Record endpoint URL type, access control and data-retention policy, but never echo secrets.

## Deliverables
Workflow JSON, required node/version manifest, model license/checksum register, execution parameters, output provenance and visual QA. Distinguish graph validity, execution success and artistic approval.
