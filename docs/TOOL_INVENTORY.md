# Tool and asset inventory — verified scope

This document prevents future AI sessions from confusing **a production project that uses a tool** with the complete upstream application/source tree.

## ChatGPT plugin

The private [h2-selfimprove-studio plugin](https://chatgpt.com/plugins/plugins_6ade1c3ca8d0819188070ae20f2792d0) was created by Plugin Creator from the user's supplied `.plugin` archive. Its contained H2 rig/packs are distinct from the checked-in Remotion project. Exact current release and activation notes: `docs/CHATGPT_PLUGIN.md`.

## In this GitHub repository

| Component | What is actually present | What is not implied |
|---|---|---|
| Remotion | Reproducible project at `video-projects/remotion/`, storyboard, React composition, procedural music/SFX source, render/QA workflows, and a persisted 155-second reference render | This is not the full upstream Remotion monorepo |
| Blender | `tools/blender/render_h2_stage.py`, documentation and CI proof workflow | Not the Blender application or complete Blender source tree |
| Krita | `tools/krita/README.md` and asset-authoring guidance | Not the Krita application or complete Krita source tree |
| H2 SelfImprove Studio | Manifests and import/verification workflows; the original H2 master can be imported with `tools/video/archive_h2_master.py` | The complete H2 studio source/rig is not automatically present just because its prior source ZIP was attached |
| Video production skill | `.agents/skills/video-production-master/`, Claude Code adapter, root AI instructions, QA templates, audio rules, story validator, state/handoff and archive workflows | This workflow still requires the correct renderer/runtime and actual assets to exist |
| Video library | `video-library/`, versioned Remotion sample, artifact manifests/contact sheets, and a catalog of prior work | Only files with a repository path are durable in GitHub |

## Tool/source archives present in the production workspace snapshot

The following binary attachments existed in the 2026-10-25 ChatGPT production workspace. The `/mnt/data` paths are ephemeral and **are not paths on the user's Windows PC**. A later AI session should search current conversation/Library attachments first; if the binaries are absent, ask for or download the matching files rather than assuming they persist.

| Filename | Bytes | SHA-256 | Repository status |
|---|---:|---|---|
| `remotion-main.zip.001` | 104,857,600 | `4617a6c4d0b570fa5ef74f201ea99a1c5183d460dde477a4010a0a6d92b83220` | Split upstream source archive; not committed |
| `remotion-main.zip.002` | 104,857,600 | `30705af430ad8c34c8f6f6800f9128ffc7de96f824657ccff5a9148dfbd089ec` | Split upstream source archive; not committed |
| `remotion-main.zip.003` | 104,857,600 | `a4bc4c47a41957a8f2cf34f7d0303184325061c194a2533f6765cbadbc943a54` | Split upstream source archive; not committed |
| `remotion-main.zip.004` | 104,857,600 | `5863268d3c5d0eb833711c83e0c1fc1b784ac951956ac35eac7ac5c4896cc7cb` | Split upstream source archive; not committed |
| `remotion-main.zip.005` | 104,857,600 | `92e34b67329fdddd01333007ea0a6e125cf49b4de6011244fbe6fc9097915937` | Split upstream source archive; not committed |
| `remotion-main.zip.006` | 87,175,231 | `e4e71461785b34944eb6f5d2c7a465cae1cce60bb107e278370791ab1e5e57b1` | Split upstream source archive; not committed |
| `blender-main.zip` | 91,621,465 | `e6e1a89d5e17c919b6954cf017b50bd3b02d9349192b4d6ef5c64b1585a4cef7` | Upstream/application source archive; not committed |
| `krita-master.zip` | 306,708,648 | `cc79f291d119435769e5a3da09f64ca26a7db0adc1cf33f8696114d7eca912c6` | Upstream/application source archive; not committed |
| `h2-selfimprove-studio.plugin` | 188,342 | `339b410a0535cd51525df9679e774e72515b483733e70c08be4f379a25b41bf3` | Plugin attachment; not committed |
| `one-more-scroll-h2-source.zip` | 115,875,783 | `f6f8bed7179c166800b9ba2c79dbd53e12e24050645cee83b44d3ce27c11c42b` | H2 source package; not committed |
| `one-more-scroll-h2-source-v2-scene-fixes.zip` | 115,856,962 | `b8db965db214bf0e37b307d3fe1aa663c55f29ee753fd9103a5972b5fe633014` | H2 source package with later unverified fixes; not committed |

Do not blindly commit the complete upstream Remotion/Blender/Krita source ZIPs into this repo. Their size, licensing, update policy and Git history impact are different from the user's own production assets. Use official install mechanisms for the applications; retain this inventory so the files are discoverable when supplied.

## Prior rendered video assets

See [previous-works-catalog.json](../video-library/previous-works-catalog.json). Each entry distinguishes ChatGPT/session storage from files actually committed in `video-library/previous-works/`. The historical iterations are comparison material, not all approved as final quality. Review their video/contact sheets before reusing them.

To import a downloaded set of previous MP4s, run `tools/video/archive_previous_works.py --source-dir <folder>`; it checks every hash before staging. Commit/push the result and let the “Verify previous AI video assets” workflow finish before calling those files archived.

To preserve the H2 engine/source ZIPs without putting 115 MB files into Git history, run `tools/video/publish_h2_source_release.ps1 -AssetsDir <folder>` from a clone of this repo after downloading the exact files from ChatGPT attachments. It verifies each SHA-256 and uploads them as GitHub Release assets. The script writes a release manifest that must then be committed/pushed. Do not re-upload the full upstream Remotion, Blender or Krita app source archives as part of the H2 release.
