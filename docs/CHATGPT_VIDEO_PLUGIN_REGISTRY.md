# ChatGPT video plugin registry

Private specialist plugins created for Nolane Video. The command center is the single entry point for routing among the specialists.

| Specialist | Version | Plugin ID | Release ID | Link | Route |
|---|---:|---|---|---|---|
| Nolane Motion Lab | 0.1.0 | plugins_6ae55edab2a881919d80ab5cc7a54dfe | pluginrel_6ae55edc4cbc8191b810b9ce6a9f0c9d | https://chatgpt.com/plugins/plugins_6ae55edab2a881919d80ab5cc7a54dfe | Motion choreography, Remotion, HyperFrames, Motion Canvas, GSAP, Motion, Three.js and PixiJS |
| Nolane Story Studio | 0.1.0 | plugins_6ae55ee6e0588191a2d0542ed0235781 | pluginrel_6ae55ee88eec8191914b01705c28bbd1 | https://chatgpt.com/plugins/plugins_6ae55ee6e0588191a2d0542ed0235781 | Story, storyboard, cinematography, visual direction and character performance |
| Nolane 3D & VFX | 0.1.0 | plugins_6ae55ef184748191beda13ca683156ac | pluginrel_6ae55ef345cc819187c400bc7a5d77a7 | https://chatgpt.com/plugins/plugins_6ae55ef184748191beda13ca683156ac | Procedural 3D, optional Blender, browser VFX, lighting and compositing |
| Nolane Render & QA | 0.1.0 | plugins_6ae55efbf7b08191af89450a747370cd | pluginrel_6ae55efd96b48191ae006e08e3a3816d | https://chatgpt.com/plugins/plugins_6ae55efbf7b08191af89450a747370cd | Actions, runtime installation, technical QA, captions/OCR, release evidence and reproducibility |
| Nolane Video Command Center | 0.1.0 | plugins_6ae55f28fb148191b2eb6333f7620cbc | pluginrel_6ae55f2ad5888191937780153b70c65a | https://chatgpt.com/plugins/plugins_6ae55f28fb148191b2eb6333f7620cbc | Main entry point; selects route and tells ChatGPT which specialist to activate |

## Existing plugins (not modified)

- Nolane Video Production Studio v0.4.0: https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd
- H2 SelfImprove Studio v1.1.0: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0

## Capability boundary

The command center can choose a specialist, open its private plugin link and apply the corresponding repo Agent Skill. ChatGPT plugins are separately activated; do not claim that a router plugin can invisibly invoke another plugin. The repo Agent Skill remains the fallback so work continues when a specialist is not activated.
