# Nolane Video Command Center — specialist registry v0.3.0

The command center includes the relevant skills internally, so the user can invoke only this plugin for normal video work. Specialist plugins are separate private entry points and optional.

| Specialist plugin | Plugin ID | Link | Main capabilities |
|---|---|---|---|
| Nolane Motion Lab | `plugins_6ae55edab2a881919d80ab5cc7a54dfe` | https://chatgpt.com/plugins/plugins_6ae55edab2a881919d80ab5cc7a54dfe | Remotion, HyperFrames, GSAP, Motion, Three/Pixi |
| Nolane Story Studio | `plugins_6ae55ee6e0588191a2d0542ed0235781` | https://chatgpt.com/plugins/plugins_6ae55ee6e0588191a2d0542ed0235781 | Story, storyboard, cinematography, art direction and acting |
| Nolane 3D & VFX | `plugins_6ae55ef184748191beda13ca683156ac` | https://chatgpt.com/plugins/plugins_6ae55ef184748191beda13ca683156ac | Blender, Three.js, camera, lights, materials and VFX |
| Nolane Render & QA | `plugins_6ae55efbf7b08191af89450a747370cd` | https://chatgpt.com/plugins/plugins_6ae55efbf7b08191af89450a747370cd | Actions, FFmpeg, captions/OCR and release QA |
| Nolane Manim Explainer Studio | `plugins_6ae56882d1408191bbbb2a2d53a9ba7e` | https://chatgpt.com/plugins/plugins_6ae56882d1408191bbbb2a2d53a9ba7e | Math, science and engineering animation |
| Nolane Audio & Speech Studio | `plugins_6ae5688dc41081919a3251586f71d0e2` | https://chatgpt.com/plugins/plugins_6ae5688dc41081919a3251586f71d0e2 | Voice, speech recognition/alignment, stems and mastering |
| Nolane Editorial Interchange Studio | `plugins_6ae5689896388191bae1cb45fcc257e1` | https://chatgpt.com/plugins/plugins_6ae5689896388191bae1cb45fcc257e1 | OTIO, PySceneDetect, proxies and timeline exchange |

## Existing plugins kept unchanged
- Nolane Video Production Studio v0.4.0: https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd
- H2 SelfImprove Studio v1.1.0: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0

## Activation boundary
The master command center uses its own bundled skill set. It does not claim to invisibly activate other private plugins. The extra specialist links are optional. Normal routing, instructions and skill execution are available from this plugin's bundled skills plus the connected GitHub tools.
