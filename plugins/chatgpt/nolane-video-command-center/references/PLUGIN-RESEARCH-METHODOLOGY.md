# Specialist source and verification policy v0.7.8

The registry contains **37 separate specialist plugins** with recorded source or official documentation foundations. Source categories and runtime licenses are not interchangeable:
- **First-party or project-maintained skill packs** should be aligned to the exact release/commit recorded in that plugin.
- **Community skill packs** can use MIT, CC0, CC BY or other terms. Preserve author, source commit, selected files, exact license and attribution/change notice. Do not call CC BY skill text MIT because source code in the same repo has MIT license.
- **Official technical documentation** is not itself an agent skill. When a plugin relies on docs rather than a community SKILL.md, label it documentation-derived.
- **Runtime/package licenses differ from upstream engines and bundled content.** Examples include D3 ISC, PMNDRS postprocessing Zlib, Tesseract Apache-2.0 versus traineddata, Sharp Apache-2.0 versus libvips/native codecs, resvg-js MPL-2.0 versus Rust resvg Apache-2.0, and Theatre Core Apache-2.0 versus Studio AGPL-3.0.
- **Animation and media assets have independent rights.** MIT dotLottie Web does not license the `.lottie` artwork, fonts, audio, embedded images, brands or generated media.
- **Prerelease packages are not production defaults.** The currently inspected resvg-js 2.7.0-alpha.2 profile stays opt-in until a clean-runner native/WASM proof and API review are complete.
- **Plugin-authored adaptations** are not presented as upstream verbatim skills. Record what was adapted, what was paraphrased and what was excluded.

A green plugin update means the host accepted a structurally valid package. It does not prove that the upstream CLI/tool is installed, that all upstream tests were run, that a native dependency is compatible, or that a generated video is artistically approved. Each specialist must verify the exact project's version/capabilities and run a task-relevant smoke test.

Every source-backed update should keep: source repository URL, immutable commit SHA, version or source release, license and notice file, selected files, adaptation boundary, test/eval evidence (upstream vs locally run), and known limitations. Re-audit on upstream release changes before using an API or command that may have moved.
