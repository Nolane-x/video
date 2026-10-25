# ChatGPT Plugin Creator integration — H2 SelfImprove Studio

## Exact plugin created

- Name: `h2-selfimprove-studio`
- Plugin ID: `plugins_6ade1c3ca8d0819188070ae20f2792d0`
- Version created from the user-provided plugin: `1.0.2`
- Scope: private personal plugin (`USER`)
- Open/activate in ChatGPT: https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0
- Source input: `h2-selfimprove-studio.plugin` supplied in the production chat
- Creation result: Plugin Creator reported `status=created` and release ID `pluginrel_6ade1c3ecb20819199def25125d2f89a`.

## What the plugin contains

The Plugin Creator successfully ingested the supplied archive and reported these principal components:
- `skills/kich-ban-selfimprove/SKILL.md` plus story-structure and thumbnail references.
- `skills/lam-video-selfimprove/SKILL.md` plus style, audio, install and scene QA references.
- The H2 kit: `kit/engine/`, `kit/packs/dem/`, `kit/packs/doodle/`, `kit/render.mjs`, the project shot plan, audio generation/mixing tools, draft/doctor/import helpers and package manifest.
- The actual character rig, scene templates, environment/prop drawing code, procedural audio and render scripts from the supplied plugin archive.

This means the H2 kit is preserved inside the private ChatGPT plugin; it is not the same as a full upstream Remotion, Blender or Krita application checkout.

## How a future ChatGPT session should use it

1. Open the plugin link above and make sure it is available in the user's ChatGPT workspace. Its current discoverability is private to the user's account.
2. For script work, invoke the `kich-ban-selfimprove` workflow.
3. For H2 film production, invoke the `lam-video-selfimprove` workflow and read the H2 package's scene/schema/install/QA references before changing templates.
4. Also read this repository's canonical production skill at `.agents/skills/video-production-master/SKILL.md`, `docs/STATE.md`, `docs/AI_HANDOFF.md`, `docs/TOOL_INVENTORY.md`, and the current per-video manifest.
5. Select the renderer per scene. Use H2 for its native rig/scene packs; use Remotion for timeline and compositing; Blender for selected shots that benefit from depth/3D; Krita for intentional hand-authored assets; FFmpeg for mastering/validation.
6. Distinguish the H2 master from the Remotion reference render. A successful render or generated contact sheet is not a manual visual QA sign-off.

## Versioning and honest status

- Version `1.0.2` is the successfully created private plugin release.
- The canonical production playbook and QA gates are maintained in this repo and are linked above; they are not silently claimed to be embedded in version 1.0.2.
- A plugin update requires building a new ZIP/tar.gz overlay and calling Plugin Creator's guarded `update_plugin` action with the current release ID. The original plugin should be preserved, and omitted files must remain intact.
- Do not say the plugin was updated to a new version until Plugin Creator returns that updated version and release ID.
