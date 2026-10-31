# ChatGPT video plugin registry

Private specialist plugins created for Nolane Video. The **Nolane Video Command Center v0.3.0** is the main entry point and bundles all production skills. Specialists are optional focused entry points.

| Plugin | Version | ID | Private ChatGPT link | Responsibility |
|---|---:|---|---|---|
| Nolane Video Command Center | 0.3.0 | `plugins_6ae55f28fb148191b2eb6333f7620cbc` | https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc | Main router; bundles 12 production skills and repository workflow |
| Nolane Motion Lab | 0.1.0 | `plugins_6ae55edab2a881919d80ab5cc7a54dfe` | https://chatgpt.com/plugins/plugins_6ae55edab2a881919d80ab5cc7a54dfe | Remotion, HyperFrames, GSAP, Motion, Three.js and PixiJS |
| Nolane Story Studio | 0.1.0 | `plugins_6ae55ee6e0588191a2d0542ed0235781` | https://chatgpt.com/plugins/plugins_6ae55ee6e0588191a2d0542ed0235781 | Story, storyboard, cinematography and art direction |
| Nolane 3D & VFX | 0.1.0 | `plugins_6ae55ef184748191beda13ca683156ac` | https://chatgpt.com/plugins/plugins_6ae55ef184748191beda13ca683156ac | Procedural 3D, Blender, lighting and compositing |
| Nolane Render & QA | 0.1.0 | `plugins_6ae55efbf7b08191af89450a747370cd` | https://chatgpt.com/plugins/plugins_6ae55efbf7b08191af89450a747370cd | GitHub Actions, install, render QA, captions/OCR and releases |
| Nolane Manim Explainer Studio | 0.1.0 | `plugins_6ae56882d1408191bbbb2a2d53a9ba7e` | https://chatgpt.com/plugins/plugins_6ae56882d1408191bbbb2a2d53a9ba7e | Mathematics/science/engineering animations |
| Nolane Audio & Speech Studio | 0.1.0 | `plugins_6ae5688dc41081919a3251586f71d0e2` | https://chatgpt.com/plugins/plugins_6ae5688dc41081919a3251586f71d0e2 | Voice, WhisperX/Demucs, caption alignment and mastering |
| Nolane Editorial Interchange Studio | 0.1.0 | `plugins_6ae5689896388191bae1cb45fcc257e1` | https://chatgpt.com/plugins/plugins_6ae5689896388191bae1cb45fcc257e1 | OTIO, PySceneDetect, source metadata and shot logs |

## Existing plugins (unchanged)

- Nolane Video Production Studio v0.4.0: https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd — broad 32-skill library.
- H2 SelfImprove Studio v1.1.0: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0 — native H2 workflow.

## How routing works

Use the command center as the only required ChatGPT plugin for ordinary production. It contains all specialist skills. Separate specialist plugins are optional entry points; the command center does not claim invisible plugin-to-plugin invocation. Repository operations use connected GitHub tools and the bundled skills.
