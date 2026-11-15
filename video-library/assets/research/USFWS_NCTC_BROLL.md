# USFWS/NCTC B-roll — source research and rights gate

**Status:** CANDIDATE / source-only / not imported / not counted in any asset-library build  
**Checked:** 2026-10-31  
**Owner:** video-library asset research

## Why this source is worth keeping

The U.S. Fish & Wildlife Service's National Conservation Training Center (USFWS/NCTC) maintains six B-roll collections. The material adds real nature footage not well represented by generic procedural loops: birds, wildlife, fisheries, Monarch butterflies, underwater habitats, and landscapes.

The official collection says its B-roll was created by USFWS/NCTC videographers Brett Billings, Ryan Hagerty, and Doug Canfield; it invites users to download and use the clips when creating videos and asks for USFWS credit. The category pages describe MP4 downloads through their embedded VBrick players and ask for photographer/videographer/creator credit plus USFWS credit.

This is a strong *use-in-video source*, but it is not designated CC0 and the page does not grant a blanket right to redistribute the original files as a standalone asset pack. Keep it source-only until the exact clip-level download and redistribution terms have been reviewed.

## Official collection index and category pages

- [USFWS/NCTC B-roll collection index](https://www.fws.gov/library/collections/b-roll-videos) — lists six B-roll collections.
- [American Birds](https://www.fws.gov/NCTC-american-bird-b-rolls) — perching birds, shorebirds, terns, raptors, waterfowl and bird habitats.
- [Fisheries](https://www.fws.gov/NCTC-fisheries-b-rolls) — fisheries fieldwork, fish, invasive carp, river habitats and underwater footage.
- [Monarch Butterfly](https://www.fws.gov/NCTC-monarch-butterfly-b-rolls) — milkweed, pollinators and Monarch life-cycle footage.
- [People and Places](https://www.fws.gov/NCTC-people-and-places-b-rolls) — Alaska landscapes, glaciers, wetlands, wildflowers, forests, wind power, recreation and conservation work.
- [Underwater](https://www.fws.gov/NCTC-underwater-b-rolls) — brook trout, other fish, salamanders, manatee and underwater habitats.
- Wildlife — listed as the sixth category on the official collection index; use the index link and resolve the exact item page rather than guessing a slug.

## Rights and usage evidence

The official notice on the [collection index](https://www.fws.gov/library/collections/b-roll-videos) says:
- The B-rolls were created by named USFWS/NCTC videographers.
- The Service invites people to download and use these clips when creating videos.
- USFWS credit is requested.

The official category pages additionally state:
- MP4 files can be downloaded through each embedded VBrick player.
- Credit the photographer/videographer or creator and the U.S. Fish & Wildlife Service. A sample format is `Credit: [creator], USFWS`.
- Some video productions contain music licensed to USFWS. The music license covers free distribution of the finished production in its entirety; non-private public use of productions containing that licensed music requires a separate license.

**Do not relabel this source CC0.** The page grants video-creation use and requests credit, but it does not state that the raw files may be mirrored and redistributed in a multi-source downloadable library. Until that is explicitly cleared, keep only source links and per-item notes in the catalog; do not place original clips in the public release ZIP.

## Conservative import policy if an importer is proposed

1. Resolve each embedded VBrick player to the exact official MP4 download URL. Do not invent or reconstruct a VBrick URL from a title. Record the canonical FWS item page and the exact player/download URL.
2. Keep a per-clip record: title, category, creator/photographer, source page, exact media URL, download date, byte size, SHA-256, duration, dimensions, codec, and rights/usage evidence.
3. **Audio:** do not use the supplied soundtrack as a reusable music/SFX asset. If a clip contains licensed music or the audio status is unclear, exclude it until a separate license is documented. A muted derivative may be considered only after confirming that removing the entire audio stream is supported by the clip's terms and verifying the exported file has no audio stream.
4. **People and publicity:** default to wildlife, bird, landscape, plant and underwater shots without recognizable people. Skip or separately review identifiable people, patients, children, rangers, visitors, researchers, fishermen, cultural activities, vehicle plates, and private-property details. A shot log is a discovery aid, not a model release.
5. **Marks and endorsement:** preserve requested credit, do not use agency marks as decoration, and do not imply USFWS endorsement.
6. Maintain the original source terms with the asset record. Missing creator attribution, ambiguous rights, third-party content, unresolved soundtrack rights or an unverifiable direct file means skip.
7. Keep the raw footage source-only unless a separate, explicit redistribution permission is obtained. Never count search hits or player pages as downloaded assets.

## Good first candidates for manual review

The People and Places page lists an 11:40 “Alaska Landscapes” compilation with mountains, lakes, rivers, glaciers, wetlands, flowers and aerial landscape shots. The Birds collection includes species-focused clips; the Underwater and Fisheries collections include fish and aquatic habitat footage. Prefer short, visual-only shots with no identifiable people or embedded soundtrack, then record the exact selected segment and attribution.

These are candidate topics, **not evidence that a specific file has been downloaded or approved**.

## Build handoff

- This research note intentionally does not modify `tools/**`, workflows, plugin packages or the active Build 74/75 runs.
- It does not change the asset index, source totals, release size or successful-download counts.
- A separate importer proposal should be reviewed by the asset/tooling owner before it is connected to the build matrix. Start with a small, manually reviewed sample; only then consider a bounded lane.
