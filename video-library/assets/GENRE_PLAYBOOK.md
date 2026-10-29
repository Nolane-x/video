# Genre-to-asset playbook

The resource library is a toolbox, not a fixed art style. The story's intended genre decides the visual language; only then should shots choose assets.

| Genre / use case | Starting resources | Visual grammar to prefer |
|---|---|---|
| Cinematic narrative / self-improvement | Rooftop, city-rain, bedroom/studio, forest-mist, night overlays, warm practical lights, props | Character acting, meaningful foreground/background, motivated camera, deliberate negative space |
| Documentary / biography | Museum, newsroom, paper/map textures, photo/film overlays, timeline cards, archival source links | Evidence-led chronology, chapter cards, maps, period-specific imagery only after fact-checking |
| Science / education | Laboratory, blueprint grid, atom/DNA/microscope icons, equation card, diagrams and chart grids | Clear concept progression, labeled diagrams, visual metaphors that do not misstate science |
| AI / technology | Server room, cyber-security/network background, chip/robot/server/cloud icons, data nodes, terminal overlays | Real system diagrams, code/data inserts, layered depth; avoid generic glowing HUD on every shot |
| News / current affairs | Newsroom, map callouts, ticker/lower-thirds, source cards, chart/quote templates | Date-stamped facts, visible source citations, restrained graphics, no fabricated maps or data |
| History / archaeology | Museum, worn-paper texture, map routes, ruins / columns, timeline and comparison templates | Clearly mark reconstructions; do not pass invented illustrations off as documentary evidence |
| Travel / places | Mountain dawn, beach sunset, underpass/city, compass/globe/plane icons, route template | Establishing shots and transitions between distinct locations; prefer genuine licensed footage for factual places |
| Nature / wildlife | Forest-mist, mountain, beach, underwater, leaf/tree/sun/water icons, fog/rain/snow overlays | Natural color/light and scale; use source footage or verified photography for species facts |
| Business / finance | Finance dashboard, newsroom, office, charts, money/wallet/graph icons, statistic templates | Accurate scales and units, visible data sources, minimal decoration |
| Product / marketing | Product stage, studio backgrounds, UI pack, typography frames, light masks | Product truth first; clean product lighting, legible proof points and non-deceptive claims |
| Food / cooking | Food studio, kitchen, ingredients/icons, timer/recipe cards | Ingredient/step close-ups and pacing matched to actions; never invent health claims |
| Gaming / fantasy / sci-fi | Gaming arena, space, modular space, castle/food/nature kits, particles, audio packs | Distinct worlds/palettes by location, practical compositing and sound motifs |
| Health / medicine | Medical corridor, lab and microscope/flask icons, simple anatomy/science diagrams | Use authoritative medical sources; label illustrative diagrams and avoid misleading patient imagery |
| Sports / fitness | Arena/gym staging, line/charts/timer/trophy icons, speed/impact overlays | Real action beats and readable motion; prefer actual permitted footage when events are factual |
| Infographics / explainers | Icon SVGs, charts, process, flow, funnel, timeline, quote, map and comparison templates | One idea per visual, consistent scales, accessible contrast and read time |


| Experimental / abstract | Original overlays, procedural grids, topographic lines, starfield, waveform, node network | Give each motion a reason; establish one clear focal point and build/resolve the image over time |
| Horror / mystery / suspense | Horror-manor palette, rain/fog/vignette, archival objects, sparse light and long shadows | Preserve darkness detail; limit glitch to motivated beats; let negative space and sound create tension |
| Human stories / relationships | City-day/night, interiors, archival photography, faces/hands/letters, calendar and message inserts | Prioritize body language and specific objects over generic motivational text |
| Kids / family learning | Bright city/nature palettes, clear icons, animals, large labels, simple step cards | Use simple silhouettes and calm motion; keep captions readable and facts age-appropriate |
| Historical reconstruction / archaeology | Public-domain maps and illustrations, museum images, paper textures, date cards, reconstructed 3D environments | Label reconstructions and approximate dates; do not present an illustrative model as a real photograph |
| Vertical social / teaser | 9:16 safe-area overlay, giant title card, waveform, high-contrast image crop, concise stat/quote cards | Compose for phone-size readability, keep vital text clear of platform UI, and make the first 1–2 seconds distinctive |
| Music / performance visuals | Waveform overlay, spectrum-style line art, bokeh, film grain, stage palettes and light sweeps | Let rhythm inform timing; use only music/SFX with clear usage rights |
| Tutorial / software walkthrough | Accurate UI captures, step numbers, source cards, diagram/process templates, restrained cursor highlights | Show real product state; don't fabricate interface screenshots or claim a feature exists based on a decorative mockup |
| Real-estate / architecture | Architecture and city images, floor-plan/blueprint overlays, model renders, daylight/night palettes | Keep spatial scale and property details accurate; label conceptual images and illustrative renders |
| Sports highlight / training | Motion speed lines, impact overlays, timer/trophy/charts, arena environment and real permitted footage | Prioritize actual motion/action; overlays must not obscure the key action or fake score/time data |

## Practical selection rules

- Do not reuse the same establishing background two shots in a row unless the location intentionally persists.
- Try to use at least four distinct shot families in a one-minute segment: environment wide, action/prop insert, face/reaction, diagram/data insert, or real licensed footage.
- Choose an asset because it explains the current beat, not because it looks impressive.
- When using third-party factual media, store the exact source page, creator, license, relevant download date and file checksum. Keep the attribution text adjacent to the asset.
- "Free to use" does **not** always mean "free to redistribute as a raw file." Only the dedicated release builder's CC0-allowed lane is auto-bundled.
- If an external asset's license changes, that is not retroactively a reason to strip its provenance. Pin the exact download metadata with the delivered version.


## Expanded source routing and media discipline

- **Space / astronomy / planetary science:** use screened NASA imagery/video for factual establishing shots; pair it with original observatory, orbital-lab and deep-space vectors, and Poly Haven 3D lighting/props where an explanatory reconstruction helps. NASA media is not CC0; retain required attribution and review its official media-use guidance.
- **Earth science / climate / weather / ocean:** prioritize item-grounded NASA Earth-observation imagery for factual claims; use the ocean-depths, monsoon-city, tundra-aurora and underwater-reef original environments only as clearly illustrative shots. Never portray a stylized background as actual satellite evidence.
- **History / archival culture / industrial evolution:** discover Library of Congress material only when its exact item rights statement is positive; combine with The Met Open Access and verified Wikimedia CC0/Public Domain assets. Add visible dates and an “illustration/reconstruction” label when needed.
- **Science / medicine / engineering:** use clinical-lab, orbital-lab and observatory environments as visual supports, not source evidence. The anatomy-label, experiment-card, fact-check, blueprint-dimensions and source-ledger layouts should surface units, sample sizes, references and uncertainty where relevant.
- **Business / product / software:** use financial-night, product-showcase-ivory, data-visualization and cyber-operations styles; supplement with laptop, code, terminal, scales and package icons. Do not fabricate real product interfaces, market data, performance or customers.
- **Documentary / investigation / news:** archive timecode, CCTV framing, paper tears, source ledger, fact-check cards and news ticker are distinct graphic families. Do not use these overlays to make unverified media look like authentic evidence.
- **Fantasy / gaming / music / sport:** start with castle-ruins, neon-alley, concert-hall, sports-court and particle/spectrum overlays; build a separate palette and audio motif for each environment rather than applying the same look to every topic.

### Source mix before a shot is approved

1. Mark every shot as **factual source media**, **original illustration**, **3D reconstruction**, or **graphic explanation** in the shot notes.
2. For factual source media, use a provenance-backed item and preserve creator, rights, source URL, date/period and checksum where present.
3. For reconstructions, tell the viewer when that distinction materially affects interpretation; never pass a stylized 3D render off as archival footage.
4. Use at least four meaningful shot families per minute, and vary shot scale, movement, subject and composition—not merely color.
5. The catalog’s “source/license” links are an audit trail, not a blanket permission slip. When uncertain, keep the file out of the release bundle and link to the official source instead.


## Surface-texture palette

The library now includes a tileable vector texture family. Use these as controlled overlays, matte/shader inputs or backgrounds at low contrast; they are generic original illustrations, not scans of real materials.

- **Engineering / software / AI:** blueprint-grid, crosshair-grid, circuit-board, neon-circuit, hex-mesh and isometric-grid.
- **Documentary / history / archives:** archival-paper, paper-fibers, newspaper-halftone, film-scratches and diagonal-hatch.
- **Architecture / product / industrial:** concrete-speckle, marble-veins, brushed-metal, carbon-fiber, wood-grain, ceramic-tile, terrazzo-speckle, rubber-diamond and perforated-metal.
- **Nature / earth science / water:** topographic-contours, bathymetry-contours, geology-strata, ocean-waves, soft-clouds and rain-droplets.
- **Gaming / pop-art / retro:** comic-dots, pixel-grid, dither-noise, geometric-triangles and star-map.

A texture should support the material/story, not become a noisy overlay on every shot. Test at output resolution, keep key text zones clear, and avoid using a decorative texture where an actual source image is needed as evidence.
