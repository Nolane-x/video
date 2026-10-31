---
name: specialist-plugin-router
description: Use when a production task requires tool-specific depth beyond the Command Center’s internal skills; select one specialist plugin, create an explicit handoff and never claim hidden cross-plugin invocation.
---

# Specialist Plugin Router

## Purpose
Use the internal 29-skill Command Center first. Route to a separate specialist plugin only when tool-specific detail, a dedicated source pack or a specialized QA workflow materially improves the task.

## Routing procedure
1. Classify the work: engine, graphics/motion, vector/SVG, media processing, speech/audio, editorial, browser capture, CI correctness or CI security.
2. Choose the smallest effective specialist from `references/PLUGIN-REGISTRY.md`.
3. Confirm the plugin's current version and source registry. The registry is a directory, not a substitute for reading the specialist's skill.
4. Prepare a concise handoff: goal, audience, format/duration/FPS, language, exact repo/branch/paths, current tool versions, source media/asset IDs already approved, known constraints, tests to run and expected output/evidence.
5. Open the exact plugin link and explicitly switch/activate it. The host controls plugin activation. Do not claim that another private plugin was silently called.
6. After the specialist returns, reconcile its changes with the current repo and re-run the end-to-end production QA before delivery.

## When not to hand off
- The internal skill already covers the task adequately.
- The specialist would duplicate analysis without adding new evidence.
- The project is on a weak runner where the specialized engine is unavailable; use a proven alternative and report the limitation.
- The requested action crosses the parallel asset-library boundary, costs money, downloads large weights, merges a PR or writes to production without explicit approval.

## Never infer from registry labels
A source-backed plugin can still contain only adapted instructions and no upstream executable/test suite. Inspect its source registry and files. Do not claim a tool is installed, tested on GitHub Actions or executed merely because a plugin is available.
