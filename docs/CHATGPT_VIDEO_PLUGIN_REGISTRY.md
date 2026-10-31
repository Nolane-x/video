# ChatGPT video plugin registry

The **Nolane Video Command Center v0.6.0** is the single normal entry point. It bundles 28 internal production skills; specialist plugins are optional direct entry points for focused work.

| Plugin | Version | ID | Private ChatGPT link | Responsibility |
|---|---:|---|---|---|
| Nolane Video Command Center | 0.6.0 | `plugins_6ae55f28fb148191b2eb6333f7620cbc` | https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc | Main router; 28 internal skills; story-to-delivery workflow and GitHub coordination |
| Nolane Motion Lab | 0.1.0 | `plugins_6ae55edab2a881919d80ab5cc7a54dfe` | https://chatgpt.com/plugins/plugins_6ae55edab2a881919d80ab5cc7a54dfe | Remotion, HyperFrames, GSAP, Motion, Three.js, PixiJS and motion engineering |
| Nolane Story Studio | 0.1.0 | `plugins_6ae55ee6e0588191a2d0542ed0235781` | https://chatgpt.com/plugins/plugins_6ae55ee6e0588191a2d0542ed0235781 | Story, storyboard, cinematography, art direction and acting |
| Nolane 3D & VFX | 0.1.0 | `plugins_6ae55ef184748191beda13ca683156ac` | https://chatgpt.com/plugins/plugins_6ae55ef184748191beda13ca683156ac | Procedural 3D, Blender, lighting, depth and compositing |
| Nolane Render & QA | 0.1.0 | `plugins_6ae55efbf7b08191af89450a747370cd` | https://chatgpt.com/plugins/plugins_6ae55efbf7b08191af89450a747370cd | GitHub Actions, pinned runtimes, FFmpeg, caption/OCR QA and delivery gates |
| Nolane Manim Explainer Studio | 0.1.0 | `plugins_6ae56882d1408191bbbb2a2d53a9ba7e` | https://chatgpt.com/plugins/plugins_6ae56882d1408191bbbb2a2d53a9ba7e | Mathematics, science and engineering animations |
| Nolane Audio & Speech Studio | 0.1.0 | `plugins_6ae5688dc41081919a3251586f71d0e2` | https://chatgpt.com/plugins/plugins_6ae5688dc41081919a3251586f71d0e2 | Voice, WhisperX/Demucs, speech alignment, sound design and mastering |
| Nolane Editorial Interchange Studio | 0.1.0 | `plugins_6ae5689896388191bae1cb45fcc257e1` | https://chatgpt.com/plugins/plugins_6ae5689896388191bae1cb45fcc257e1 | OTIO, PySceneDetect, proxies, source metadata and shot logs |
| Nolane AI Media & Capture Studio | 0.1.0 | `plugins_6ae5750828608191b46685dd61a7621c` | https://chatgpt.com/plugins/plugins_6ae5750828608191b46685dd61a7621c | AI media planning, ComfyUI graph orchestration, browser capture and provenance |

## Existing plugins retained

- Nolane Video Production Studio v0.4.0: https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd — broader 32-skill production library.
- H2 SelfImprove Studio v1.1.0: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 — native H2 renderer, rigs, packs and H2-specific production workflow.

## How routing works

Use the Command Center as the only required plugin for ordinary production. It contains its own specialist skills and works with connected GitHub tools. Separate private plugins remain optional entry points; ChatGPT does not silently activate another private plugin on the Command Center's behalf.

The router chooses a small compatible set of skills and tools for each project. It does not install or run every engine on every request. Remotion/HyperFrames/Manim are proven CPU lanes; Blender is an on-demand CPU proof; WhisperX/Demucs are manually installed without downloading model weights; Motion Canvas remains outside core until a separate compatibility proof passes.

## Workstream boundary

The parallel asset workstream owns `video-library/**`, asset source catalogues, downloaders and the asset-library workflow. The Command Center may plan and audit already-selected resources, but must not modify, ingest, reorganize or trigger the asset acquisition pipeline unless explicitly reassigned.
