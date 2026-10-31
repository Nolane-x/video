# Specialist plugin registry

Use the route matching the task. Each plugin is private and separately activated; do not claim that this command-center plugin silently invokes another plugin. Open/activate the specialist when needed. The matching repository Agent Skill is the fallback.

| Work type | Specialist plugin | Plugin ID |
|---|---|---|
| Motion choreography, Remotion, HyperFrames, optional Motion Canvas, GSAP, browser 2D/3D | [Nolane Motion Lab](https://chatgpt.com/plugins/plugins_6ae55edab2a881919d80ab5cc7a54dfe) | \`plugins_6ae55edab2a881919d80ab5cc7a54dfe\` |
| Story, storyboard, cinematography, art direction, acting | [Nolane Story Studio](https://chatgpt.com/plugins/plugins_6ae55ee6e0588191a2d0542ed0235781) | \`plugins_6ae55ee6e0588191a2d0542ed0235781\` |
| Blender, Three.js, procedural 3D, VFX and compositing | [Nolane 3D & VFX](https://chatgpt.com/plugins/plugins_6ae55ef184748191beda13ca683156ac) | \`plugins_6ae55ef184748191beda13ca683156ac\` |
| GitHub Actions, installs, captions/OCR, render QA and release | [Nolane Render & QA](https://chatgpt.com/plugins/plugins_6ae55efbf7b08191af89450a747370cd) | \`plugins_6ae55efbf7b08191af89450a747370cd\` |

Existing independent plugins (not modified):
- [Nolane Video Production Studio v0.4.0](https://chatgpt.com/plugins/plugins_6ae4bb1670748191989e6c0058d1b5bd) — broad 32-skill production library.
- [H2 SelfImprove Studio v1.1.0](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) — native H2 engine/plugin.

## Engine routing
- React/frame timeline and captions → Remotion.
- HTML/GSAP deterministic scenes → HyperFrames.
- Vector explainers → Remotion/GSAP by default; Motion Canvas only with a separately validated optional runtime.
- Kinetic typography → GSAP + Motion.
- Browser 3D → Three.js; 2D particles/filters → PixiJS.
- Real geometry/physical lighting/rigging → optional Blender 5.2.3 CPU proof.
- Output mastering/QA → FFmpeg/ffprobe, Playwright and Tesseract.
- Prefer the smallest lane that meets the shot. Do not install GPU models or giant native stacks for CPU-first jobs.
