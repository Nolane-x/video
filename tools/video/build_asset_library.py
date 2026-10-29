#!/usr/bin/env python3
"""Create the cross-genre resource library, preserve provenance, and gate redistribution by license."""
from __future__ import annotations
import hashlib, html, json, mimetypes, re, shutil, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("dist/video-assets").resolve()
STAGE = OUT / "video-asset-library"
SOURCES_PATH = REPO / "video-library/assets/sources.json"
CC0 = "CC0-1.0"
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
UA = "NolaneVideoAssetLibrary/1.0 (+https://github.com/Nolane-x/video)"
MAX_KENNEY_ZIP = 110 * 1024 * 1024
MAX_MEDIA_FILE = 3 * 1024 * 1024
MAX_POLY_FILE = 35 * 1024 * 1024
ALLOWED = {".png",".jpg",".jpeg",".webp",".svg",".tif",".tiff",".exr",".hdr",".obj",".mtl",".glb",".gltf",".fbx",".blend",".wav",".ogg",".mp3",".flac",".ttf",".otf",".woff",".woff2",".mp4",".mov",".m4v",".webm",".ogv",".oga",".json",".txt",".md",".pdf",".csv",".xml",".mtlx",".usdz",".abc",".dae",".stl"}
DENIED = {".exe",".dll",".so",".dylib",".bat",".cmd",".ps1",".msi",".apk",".app",".dmg",".jar",".com"}

KENNEY = [
("nature-kit","Nature Kit","trees, foliage, nature props"),("space-kit","Space Kit","space vehicles and props"),
("modular-space-kit","Modular Space Kit","modular sci-fi environments"),("furniture-kit","Furniture Kit","interior props"),
("food-kit","Food Kit","food and kitchen props"),("building-kit","Building Kit","architecture"),("racing-kit","Racing Kit","cars and tracks"),
("castle-kit","Castle Kit","medieval / fantasy"),("ui-pack","UI Pack","general interface"),("pixel-ui-pack","Pixel UI Pack","pixel interface"),
("particle-pack","Particle Pack","VFX particles"),("light-masks","Light Masks","light and shadow masks"),
("smoke-particles","Smoke Particles","smoke effects"),("foliage-sprites","Foliage Sprites","2D nature"),
("impact-sounds","Impact Sounds","foley / impact SFX"),("interface-sounds","Interface Sounds","UI SFX"),
("digital-audio","Digital Audio","digital / sci-fi SFX"),("ui-audio","UI Audio","button / switch SFX"),
("road-textures","Road Textures","road textures"),("ui-pack-adventure","UI Pack Adventure","adventure interface"),
("ui-pack-sci-fi","UI Pack Sci-Fi","sci-fi interface"),("ui-pack-pixel-adventure","UI Pack Pixel Adventure","pixel adventure UI"),
("ui-pack-rpg-expansion","UI Pack RPG Expansion","RPG interface"),("casino-audio","Casino Audio","game SFX")
]

KENNEY_GITHUB_REPOS = [
    {"slug":"Starter-Kit-Racing","title":"Starter Kit Racing","category":"vehicles, racing, 3D props","evidence":"README: package assets (2D sprites, 3D models and sound effects) are CC0 licensed."},
    {"slug":"Starter-Kit-3D-Platformer","title":"Starter Kit 3D Platformer","category":"3D props, platforms, VFX, audio","evidence":"README: sprites, 3D models and sound effects are CC0 licensed."},
    {"slug":"Starter-Kit-City-Builder","title":"Starter Kit City Builder","category":"architecture, city props, structures","evidence":"README: sprites and 3D models are CC0 licensed."},
    {"slug":"Starter-Kit-Basic-Scene","title":"Starter Kit Basic Scene","category":"3D environment, scene props","evidence":"README: bundled assets are CC0 licensed; the Mini Arena pack is CC0."},
    {"slug":"Starter-Kit-Match-3","title":"Starter Kit Match-3","category":"2D sprites, UI, particles","evidence":"README labels the included 2D sprites CC0 licensed; only media files are extracted."},
    {"slug":"Starter-Kit-FPS","title":"Starter Kit FPS","category":"weapons, props, 3D models","evidence":"README labels included sprites and 3D models CC0 licensed; only media files are extracted."}
]

PALETTES = [
("studio-warm",("#171923","#312b39","#ffc77f"),"studio"),("newsroom",("#0d1724","#19354a","#f4ad69"),"news"),
("science-laboratory",("#10222c","#203c4a","#5ce1cc"),"lab"),("server-room",("#081723","#123346","#65d8f1"),"server"),
("city-night",("#101522","#352942","#ffb574"),"city"),("city-day",("#759db8","#bfd8df","#f4d4a0"),"city"),
("rooftop-dawn",("#25233d","#855f7b","#f8b17e"),"rooftop"),("metro-station",("#131a25","#2a3947","#d8e8ed"),"metro"),
("underpass-rain",("#121a23","#263a49","#8ed5e1"),"underpass"),("hospital-corridor",("#13282c","#29434a","#c4e9dc"),"hospital"),
("library-aisle",("#251e25","#43303a","#f0bd78"),"library"),("museum-gallery",("#25232b","#403a45","#dec7a2"),"museum"),
("factory-floor",("#1e2228","#394049","#f4bd72"),"factory"),("finance-desk",("#101c24","#22323a","#7be0c3"),"finance"),
("product-stage",("#11131e","#2b3045","#f6d3a0"),"product"),("food-studio",("#38261f","#5c4131","#ffd18a"),"food"),
("classroom-board",("#1c2630","#35414c","#ead6a5"),"classroom"),("castle-hall",("#201b2a","#46374b","#f3c58d"),"castle"),
("mountain-dawn",("#1a2940","#a56e83","#ffd39a"),"mountain"),("forest-mist",("#10272a","#2e5148","#e6c58c"),"forest"),
("beach-sunset",("#27274a","#b36c7b","#ffc58e"),"beach"),("underwater-blue",("#052b45","#117b91","#9cecf0"),"underwater"),
("space-observatory",("#060b20","#252b60","#9e8bfa"),"space"),("cyber-security",("#08141c","#123642","#41e8d4"),"cyber"),
("ancient-map",("#3b2b22","#806348","#ebc88e"),"map"),("sports-arena",("#172034","#33415f","#f6c36f"),"sports"),
("gaming-arcade",("#191326","#34234a","#ff65b8"),"gaming"),("desert-dusk",("#2c1b2b","#a25753","#ffd08e"),"desert"),
("snow-mountain",("#162538","#7c9faf","#e3f4f2"),"snow"),("horror-manor",("#0e1019","#252331","#c77865"),"horror"),
("greenhouse",("#102820","#2a5945","#edcc8c"),"greenhouse"),("abstract-data",("#081323","#183254","#66c3ff"),"network"),
("city-rooftop-bluehour",("#101a2b","#354b6b","#ffb984"),"city"),
("monsoon-city",("#111d2b","#344957","#8bd2dd"),"city"),
("neon-alley",("#171025","#3b1c46","#ff62b8"),"city"),
("coastal-cliffs",("#203b54","#7b9eae","#ffd29c"),"mountain"),
("ocean-depths",("#031f3a","#075c79","#66d7db"),"underwater"),
("volcanic-caldera",("#211522","#6a3438","#ff8f52"),"desert"),
("tundra-aurora",("#10243b","#34536b","#9cf4e8"),"snow"),
("botanical-conservatory",("#102c24","#2b694f","#e3d99a"),"greenhouse"),
("orbital-lab",("#071a2a","#1b354c","#59e5d4"),"lab"),
("science-observatory",("#070c25","#202b65","#b6a4ff"),"space"),
("antique-library",("#2a2026","#51403d","#e5bd82"),"museum"),
("silk-road-map",("#332719","#76583d","#f4d09a"),"map"),
("rainforest-canopy",("#092c27","#1b5b48","#a6d89d"),"forest"),
("modern-gallery",("#1c2028","#343c49","#d3dff2"),"museum"),
("factory-at-dusk",("#1b2229","#3b464c","#ffb56e"),"factory"),
("sports-court",("#101b32","#2f456b","#f7d47e"),"sports"),
("concert-hall",("#171525","#342747","#e2a0ff"),"studio"),
("subway-platform",("#141d29","#2e4352","#93dce4"),"metro"),
("clinical-lab",("#102529","#294d50","#a4f5dc"),"lab"),
("financial-night",("#0b1722","#203846","#6de0bd"),"finance"),
("product-showcase-ivory",("#28292d","#4b4c50","#f6e9ce"),"product"),
("culinary-night-market",("#2a1b1a","#684039","#ffbf6d"),"food"),
("deep-space-nebula",("#07091d","#29265b","#ed8cff"),"space"),
("frozen-lake",("#10253b","#557f98","#d7f9fb"),"snow"),
("castle-ruins",("#201a28","#443746","#ddbc8b"),"castle"),
("cyber-operations",("#071b24","#12404b","#54f0d9"),"cyber"),
("airport-at-dawn",("#19283d","#5c7089","#ffca9b"),"metro"),
("data-visualization",("#08172a","#193c5a","#73d8ff"),"network"),
("village-evening",("#1d2831","#4e5660","#ffc589"),"city"),
("mountain-storm",("#131e34","#465a72","#bfd5e4"),"mountain"),
("underwater-reef",("#06334c","#087f8d","#a9fff0"),"underwater")
]
 
TEXTURES = [
 ("blueprint-grid","Blueprint engineering grid"),("crosshair-grid","Measurement crosshair grid"),
 ("topographic-contours","Topographic contour map"),("bathymetry-contours","Ocean bathymetry lines"),
 ("archival-paper","Archival paper grain"),("newspaper-halftone","Printed newspaper halftone"),
 ("concrete-speckle","Concrete and stone fleck"),("marble-veins","Marble vein pattern"),
 ("brushed-metal","Brushed metal grain"),("carbon-fiber","Carbon-fiber weave"),
 ("wood-grain","Wood grain"),("textile-weave","Textile weave"),
 ("terrazzo-speckle","Terrazzo stone chips"),("ceramic-tile","Ceramic tile grid"),
 ("hex-mesh","Hexagonal technical mesh"),("circuit-board","Circuit-board tracks"),
 ("pixel-grid","Pixel-art grid"),("comic-dots","Comic halftone dots"),
 ("star-map","Star chart dots"),("ocean-waves","Ocean wave lines"),
 ("geometric-triangles","Geometric triangle mosaic"),("diagonal-hatch","Diagonal hatch"),
 ("rain-droplets","Rain droplets"),("film-scratches","Film scratches"),
 ("paper-fibers","Paper fiber lines"),("woven-basket","Basket weave"),
 ("rubber-diamond","Rubber diamond plate"),("perforated-metal","Perforated metal"),
 ("blueprint-dimensions","Blueprint dimension grid"),("isometric-grid","Isometric construction grid"),
 ("neon-circuit","Neon circuit traces"),("soft-clouds","Cloud contour texture"),
 ("dither-noise","Retro dither pattern"),("geology-strata","Geology strata bands")
]
ILLUSTRATIONS = [
 ("satellite-hero","Satellite / orbital hardware","space","satellite"),("telescope-hero","Space telescope","space","telescope"),
 ("rocket-hero","Launch vehicle","space","rocket"),("planet-hero","Ringed planet","space","moon-stars"),
 ("rover-hero","Planetary rover","space","car"),("earth-globe-hero","Earth globe","earth science","globe"),
 ("microscope-hero","Laboratory microscope","science","microscope"),("chemistry-flask-hero","Chemistry flask","science","flask"),
 ("dna-hero","DNA helix","science","dna"),("atom-hero","Atomic model","science","atom"),
 ("brain-hero","Brain model","medicine","brain"),("heart-hero","Heart / pulse","medicine","heart"),
 ("medical-pulse-hero","Clinical pulse monitor","medicine","pulse"),("medical-virus-hero","Virus diagram","medicine","virus"),
 ("tree-hero","Forest tree","nature","tree"),("leaf-hero","Leaf / botany","nature","leaf"),
 ("mountain-hero","Mountain range","nature","mountain"),("volcano-hero","Volcano / geology","nature","volcano"),
 ("ocean-wave-hero","Ocean swell","nature","wave"),("rain-cloud-hero","Rain cloud","weather","cloud"),
 ("storm-lightning-hero","Lightning storm","weather","lightning"),("sunflower-hero","Sun / solar energy","nature","sun"),
 ("research-aircraft-hero","Research aircraft","transport","plane"),("train-engine-hero","Railway train","transport","train"),
 ("cargo-ship-hero","Cargo ship","transport","ship"),("bicycle-hero","Bicycle","transport","bicycle"),
 ("bridge-hero","Bridge engineering","architecture","map-route"),("house-hero","House / architecture","architecture","house"),
 ("city-factory-hero","Industrial city","architecture","factory"),("industrial-plant-hero","Factory machinery","industry","factory"),
 ("storefront-hero","Retail storefront","business","shopping-bag"),("robot-hero","Robotics","technology","robot"),
 ("chip-hero","Computer chip","technology","chip"),("server-rack-hero","Server rack","technology","server"),
 ("laptop-hero","Laptop computer","technology","laptop"),("smartphone-hero","Smartphone","technology","phone"),
 ("cyber-shield-hero","Cybersecurity shield","technology","shield-lock"),("open-book-hero","Open book","education","book-open"),
 ("archival-news-hero","Archive / newspaper","history","newspaper"),("museum-building-hero","Museum / heritage building","history","house"),
 ("museum-artifact-hero","Museum artefact","history","eye"),("film-camera-hero","Film camera","film","camera-film"),
 ("clapperboard-hero","Clapperboard","film","clapperboard"),("microphone-hero","Studio microphone","music","microphone"),
 ("music-note-hero","Music / audio","music","music"),("food-bowl-hero","Food / cooking","food","food"),
 ("recipe-timer-hero","Cooking timer","food","clock"),("coin-stack-hero","Finance / money","business","dollar"),
 ("wallet-hero","Budget / wallet","business","wallet"),("trophy-hero","Sports trophy","sport","trophy"),
 ("fitness-hero","Fitness / training","sport","lightning"),("compass-hero","Travel compass","travel","compass"),
 ("suitcase-hero","Travel luggage","travel","backpack"),("delivery-parcel-hero","Delivery / logistics","business","package"),
 ("map-route-hero","Map / itinerary","travel","map-route"),("solar-installation-hero","Solar / clean energy","energy","presentation"),
 ("wind-energy-hero","Wind / power","energy","lightning"),("globe-network-hero","Global network","technology","network"),
 ("calendar-planner-hero","Calendar / planning","education","calendar"),("clock-time-hero","Time / deadline","education","clock"),
 ("film-strip-hero","Film / cinema","film","film-strip"),("speech-bubble-hero","Conversation / interview","people","speech-bubble"),
 ("paw-nature-hero","Wildlife / animal","nature","paw"),("recycle-hero","Circular economy / recycling","environment","recycle"),
 ("shopping-cart-hero","Commerce / shopping","business","shopping-bag"),("security-lock-hero","Privacy / security","technology","lock"),
 ("data-chart-hero","Data / statistics","business","chart"),("sound-wave-hero","Sound wave / waveform","music","audio-wave")
]

MOTION_LOOPS = [
    ("orbital-grid-loop","Orbital Grid Loop","space","0x071521","orbital"),
    ("data-signal-loop","Data Signal Loop","technology","0x08172a","data"),
    ("neon-circuit-loop","Neon Circuit Loop","technology","0x101026","circuit"),
    ("ocean-ripple-loop","Ocean Ripple Loop","nature","0x052b42","water"),
    ("aurora-flow-loop","Aurora Flow Loop","nature","0x10223a","aurora"),
    ("retro-scanline-loop","Retro Scanline Loop","gaming","0x171323","retro"),
    ("film-grain-loop","Archival Film Grain Loop","documentary","0x191817","film"),
    ("hazard-light-loop","Industrial Hazard Loop","industry","0x211f19","hazard"),
    ("audio-spectrum-loop","Audio Spectrum Loop","music","0x101a2a","spectrum"),
    ("particle-field-loop","Particle Field Loop","abstract","0x081420","particles"),
    ("route-tracer-loop","Route Tracer Loop","travel","0x102229","route"),
    ("soft-bokeh-loop","Soft Bokeh Loop","cinematic","0x181a2a","bokeh"),
]

FONT_FAMILIES = [
    ("bevietnampro","Be Vietnam Pro",["BeVietnamPro-Regular.ttf","BeVietnamPro-Bold.ttf","BeVietnamPro-Italic.ttf"],"Vietnamese-first captions, body copy and subtitles",True),
    ("inter","Inter",["Inter[opsz,wght].ttf","Inter-Italic[opsz,wght].ttf"],"Modern titles, body copy and UI",True),
    ("notosans","Noto Sans",["NotoSans[wdth,wght].ttf"],"Broad-script fallback and body copy",True),
    ("notoserif","Noto Serif",["NotoSerif[wdth,wght].ttf"],"Editorial, education and long-form titles",True),
    ("ibmplexsans","IBM Plex Sans",["IBMPlexSans[wdth,wght].ttf","IBMPlexSans-Italic[wdth,wght].ttf"],"Technical explainers, labels and charts",True),
    ("ibmplexmono","IBM Plex Mono",["IBMPlexMono-Regular.ttf","IBMPlexMono-Bold.ttf"],"Code, terminal, measurement and data labels",True),
    ("spacegrotesk","Space Grotesk",["SpaceGrotesk[wght].ttf"],"Technology, modern editorial and product",True),
    ("playfairdisplay","Playfair Display",["PlayfairDisplay[wght].ttf","PlayfairDisplay-Italic[wght].ttf"],"Editorial, history and cultural storytelling",True),
    ("barlow","Barlow",["Barlow-Regular.ttf","Barlow-Bold.ttf"],"Broadcast titles, sports and condensed layouts",True),
    ("oswald","Oswald",["Oswald[wght].ttf"],"Tall headline treatments and vertical video",True),
    ("manrope","Manrope",["Manrope[wght].ttf"],"Clean product, business and explanatory video",True),
    ("merriweather","Merriweather",["Merriweather[opsz,wdth,wght].ttf"],"Reading-heavy education and documentary titles",True)
]

OVERLAYS = [
("film-grain","Fine film grain"),("scanlines","CRT scanlines"),("halftone","Halftone dots"),("light-leak","Warm/cool light leak"),
("vignette","Cinematic vignette"),("letterbox","Cinematic letterbox"),("film-gate","Film gate frame"),("dust","Floating dust motes"),
("bokeh","Bokeh rings"),("rain","Rain streaks"),("snow","Snow flecks"),("speed-lines","Motion speed lines"),
("sparkles","Highlight sparkles"),("topographic","Topographic contours"),("blueprint","Technical blueprint grid"),
("chart-grid","Data chart grid"),("starfield","Space starfield"),("data-network","Network links"),("glitch","Digital glitch bands"),
("subtitle-safe","Subtitle safe-area guide"),("corner-hud","Corner framing brackets"),("waveform","Audio waveform"),
("paper-texture","Archival paper texture"),("vhs","Analog scan texture"),("embers","Floating embers"),
("map-graticule","Map graticule"),("confetti","Confetti"),("radar","Radar sweep"),("focus-frame","Camera focus frame"),
("flash-frame","Flash frame"),("film-burn","Film-burn wash"),("soft-fog","Atmospheric fog"),("rainbow-prism","Prism light"),
("screen-reflection","Screen reflection bands"),("corner-vignette","Corner vignette"),("measurement-rulers","Measurement rulers"),
("cctv-timestamp","Documentary timestamp and camera ID"),("news-ticker","Broadcast ticker frame"),
("comic-panels","Comic / storyboard panel grid"),("torn-paper","Ripped archival paper edge"),
("lens-flare","Optical lens flare"),("blueprint-dimensions","Engineering dimension arrows"),
("tracking-markers","Motion-tracking marker set"),("dust-scratches","Archival dust and scratch pass"),
("glow-bloom","Soft highlight bloom"),("thermal-map","Thermal / false-color wash"),
("tape-label","Archival tape label"),("split-screen-divider","Split-screen comparison divider"),
("map-route","Route line and location markers"),("spectrum-bars","Audio spectrum bars"),
("rain-on-glass","Rain-on-glass droplets"),("underwater-caustics","Underwater caustic light"),
("film-frame-counter","Film frame counter"),("focus-pull","Focus-distance marks"),
("caution-stripes","Caution / industrial stripe edge"),("vertical-safe-area","Vertical 9:16 safe-area guide")
]
INFO = [
("title-card","Title / chapter card"),("lower-third","Lower third"),("stat-number","Big statistic"),("timeline","Horizontal timeline"),
("vertical-timeline","Vertical timeline"),("process-steps","Four-step process"),("comparison","Side-by-side comparison"),
("pros-cons","Pros and cons"),("bar-chart","Bar chart placeholder"),("line-chart","Line chart placeholder"),
("quote-card","Quote / key evidence"),("definition-card","Definition card"),("equation-card","Equation board"),
("map-callout","Map callout frame"),("funnel","Funnel stages"),("pyramid","Layered pyramid"),("decision-tree","Decision tree"),
("ranked-list","Ranked list"),("recipe-steps","Recipe / procedure"),("chapter-divider","Chapter divider"),("source-card","Source / evidence card"),
("scatter-plot","Scatter plot / relationship"),("stacked-bar","Stacked bar / proportion"),
("venn-diagram","Set overlap / Venn diagram"),("cycle-diagram","Circular cycle / feedback loop"),
("gantt-chart","Schedule / Gantt timeline"),("roadmap","Product / project roadmap"),
("budget-breakdown","Budget allocation"),("experiment-card","Experiment design and result"),
("anatomy-label","Labeled anatomy / structure illustration"),("fact-check","Claim / evidence / verdict card"),
("map-legend","Map legend and symbols"),("before-after","Before / after comparison"),
("scorecard","KPI / evaluation scorecard"),("milestone-grid","Milestone grid"),
("funnel-conversion","Conversion funnel"),("story-beat-board","Story beat board"),
("shot-list","Shot list / coverage checklist"),("accessibility-checklist","Accessibility review"),
("source-ledger","Source and citation ledger")
]
# Original, standalone vector icons. The visual style is intentionally neutral and adaptable.
ICONS = {
"brain":'<path d="M32 11C24 2 12 9 15 19C5 22 8 36 16 38C9 49 21 58 29 51L32 48L35 51C44 58 55 49 48 38C57 36 59 22 49 19C52 9 40 2 32 11Z"/><path d="M32 12V49M17 23Q27 21 26 30M47 23Q37 21 38 30M17 40Q26 36 27 44M47 40Q38 36 37 44"/>',
"book":'<path d="M8 13Q21 8 32 17Q43 8 56 13V52Q42 46 32 55Q22 46 8 52Z"/><path d="M32 17V55M14 20Q22 18 27 22M14 29Q22 27 27 31M37 22Q44 18 50 20M37 31Q44 27 50 29"/>',
"atom":'<ellipse cx="32" cy="32" rx="26" ry="10"/><ellipse cx="32" cy="32" rx="26" ry="10" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="26" ry="10" transform="rotate(120 32 32)"/><circle cx="32" cy="32" r="4" fill="currentColor" stroke="none"/>',
"dna":'<path d="M18 7C51 20 13 44 46 57M46 7C13 20 51 44 18 57"/><path d="M23 13H41M19 24H45M19 39H45M23 50H41"/>',
"chip":'<rect x="16" y="16" width="32" height="32" rx="5"/><rect x="23" y="23" width="18" height="18" rx="2"/><path d="M24 5V16M40 5V16M24 48V59M40 48V59M5 24H16M5 40H16M48 24H59M48 40H59"/>',
"robot":'<rect x="13" y="20" width="38" height="32" rx="8"/><path d="M32 8V20M25 8H39M8 31H13M51 31H56M21 52V58M43 52V58"/><circle cx="24" cy="34" r="3" fill="currentColor" stroke="none"/><circle cx="40" cy="34" r="3" fill="currentColor" stroke="none"/><path d="M23 43H41"/>',
"server":'<rect x="11" y="8" width="42" height="16" rx="3"/><rect x="11" y="27" width="42" height="16" rx="3"/><rect x="11" y="46" width="42" height="10" rx="3"/><circle cx="19" cy="16" r="2" fill="currentColor"/><circle cx="19" cy="35" r="2" fill="currentColor"/><path d="M27 16H46M27 35H46M27 51H46"/>',
"cloud":'<path d="M18 49H48A11 11 0 0 0 48 27A16 16 0 0 0 18 25A12 12 0 0 0 18 49Z"/>',
"network":'<circle cx="32" cy="11" r="6"/><circle cx="12" cy="47" r="6"/><circle cx="52" cy="47" r="6"/><circle cx="32" cy="34" r="6"/><path d="M29 17L15 41M35 17L49 41M18 47H46M32 17V28"/>',
"globe":'<circle cx="32" cy="32" r="25"/><ellipse cx="32" cy="32" rx="11" ry="25"/><path d="M8 32H56M14 19H50M14 45H50"/>',
"plane":'<path d="M5 34L27 28L28 8Q32 3 36 8L38 27L57 19L60 24L40 39L41 53L35 57L30 43L17 50L14 46L24 35L5 38Z"/>',
"mountain":'<path d="M5 53L24 18L35 36L43 25L60 53Z"/><path d="M19 27L24 18L30 29M39 31L43 25L49 35"/>',
"leaf":'<path d="M56 8C29 8 9 19 10 42C11 59 34 60 44 45C53 33 55 20 56 8Z"/><path d="M14 53Q29 33 51 14M28 39L27 24M36 31L49 31"/>',
"tree":'<path d="M32 57V34"/><path d="M13 37Q2 22 20 19Q20 3 32 10Q46 1 47 18Q62 20 51 37Z"/><path d="M24 57H40"/>',
"water":'<path d="M32 6C25 20 14 30 14 41A18 18 0 0 0 50 41C50 30 39 20 32 6Z"/><path d="M23 42Q25 49 32 49"/>',
"sun":'<circle cx="32" cy="32" r="12"/><path d="M32 4V13M32 51V60M4 32H13M51 32H60M12 12L19 19M45 45L52 52M12 52L19 45M45 19L52 12"/>',
"moon":'<path d="M48 42A22 22 0 0 1 22 14A24 24 0 1 0 48 42Z"/>',
"hospital":'<path d="M10 57V13H54V57Z"/><path d="M26 13V5H38V13M32 23V45M21 34H43"/>',
"flask":'<path d="M23 7H41M27 7V27L13 49Q10 57 19 57H45Q54 57 51 49L37 27V7"/><path d="M19 45H45M24 38H40"/>',
"microscope":'<path d="M24 8L42 26L35 33L17 15Z"/><path d="M35 30L44 39M23 37Q13 44 22 51H49M28 51V57M16 57H54M42 15L49 8M39 18L45 24"/>',
"newspaper":'<rect x="9" y="9" width="46" height="46" rx="3"/><path d="M16 18H48M16 25H48M16 33H29M16 40H29M16 47H29M34 33H48V48H34Z"/>',
"microphone":'<rect x="24" y="7" width="16" height="31" rx="8"/><path d="M15 30A17 17 0 0 0 49 30M32 47V58M22 58H42"/>',
"headphones":'<path d="M9 34V29A23 23 0 0 1 55 29V34"/><rect x="8" y="31" width="12" height="20" rx="5"/><rect x="44" y="31" width="12" height="20" rx="5"/>',
"gamepad":'<path d="M20 20H44Q52 20 55 30L59 44Q61 54 51 54L40 43H24L13 54Q3 54 5 44L9 30Q12 20 20 20Z"/><path d="M19 29V41M13 35H25"/><circle cx="44" cy="31" r="3"/><circle cx="50" cy="38" r="3"/>',
"shield":'<path d="M32 6L53 14V31Q51 47 32 58Q13 47 11 31V14Z"/><path d="M21 32L28 39L44 22"/>',
"lock":'<rect x="12" y="27" width="40" height="30" rx="5"/><path d="M20 27V19A12 12 0 0 1 44 19V27"/><circle cx="32" cy="41" r="3"/><path d="M32 44V49"/>',
"key":'<circle cx="20" cy="25" r="12"/><path d="M30 33L54 57M43 45L49 39M49 51L55 45"/>',
"idea":'<path d="M20 29A12 12 0 1 1 44 29Q44 38 38 42V49H26V42Q20 37 20 29Z"/><path d="M26 54H38M28 59H36M32 4V9M7 18L13 21M51 21L57 18M9 43L15 41M49 41L55 43"/>',
"target":'<circle cx="32" cy="32" r="25"/><circle cx="32" cy="32" r="15"/><circle cx="32" cy="32" r="5"/><path d="M35 29L58 6M47 6H58V17"/>',
"trophy":'<path d="M19 7H45V23A13 13 0 0 1 19 23Z"/><path d="M19 13H9V21Q9 33 24 32M45 13H55V21Q55 33 40 32M32 36V50M22 56H42M25 50H39"/>',
"heart":'<path d="M32 54L9 32Q1 17 15 10Q25 5 32 18Q39 5 49 10Q63 17 55 32Z"/>',
"people":'<circle cx="24" cy="20" r="9"/><circle cx="45" cy="23" r="7"/><path d="M7 54V47A17 17 0 0 1 41 47V54ZM39 39A13 13 0 0 1 57 51V54H45"/>',
"backpack":'<rect x="15" y="19" width="34" height="39" rx="8"/><path d="M23 19V13A9 9 0 0 1 41 13V19M15 31H49M23 39H41V50H23Z"/>',
"play":'<circle cx="32" cy="32" r="26"/><path d="M26 19L45 32L26 45Z" fill="currentColor" stroke="none"/>',
"camera":'<path d="M8 20H20L25 13H39L44 20H56V54H8Z"/><circle cx="32" cy="36" r="11"/><circle cx="49" cy="27" r="2"/>',
"clock":'<circle cx="32" cy="32" r="26"/><path d="M32 15V33L45 40"/>',
"calendar":'<rect x="8" y="13" width="48" height="43" rx="4"/><path d="M8 25H56M20 6V18M44 6V18M19 34H25M31 34H37M43 34H49M19 44H25M31 44H37"/>',
"bell":'<path d="M14 44H50L45 37V25A13 13 0 0 0 19 25V37Z"/><path d="M26 51Q32 60 38 51"/>',
"phone":'<rect x="17" y="5" width="30" height="54" rx="5"/><path d="M26 12H38M28 51H36"/>',
"dollar":'<path d="M44 16Q39 8 29 10Q15 12 18 24Q20 32 34 34Q49 36 46 47Q43 58 28 55Q19 53 16 47"/><path d="M32 4V60"/>',
"wallet":'<rect x="7" y="15" width="50" height="39" rx="6"/><path d="M7 23H48Q57 23 57 32V42H43A6 6 0 0 1 43 30H57"/>',
"chart":'<path d="M9 55V9M9 55H59"/><rect x="16" y="35" width="8" height="20" rx="2"/><rect x="30" y="24" width="8" height="31" rx="2"/><rect x="44" y="12" width="8" height="43" rx="2"/>',
"linechart":'<path d="M8 55V9M8 55H59M13 45L25 32L34 39L48 18L58 25"/>',
"car":'<path d="M9 42L14 27Q16 22 22 22H42Q48 22 50 28L55 42V52H9Z"/><path d="M16 29H48M9 42H55"/><circle cx="19" cy="49" r="5"/><circle cx="45" cy="49" r="5"/>',
"house":'<path d="M5 30L32 7L59 30M12 27V57H52V27M26 57V39H39V57"/>',
"factory":'<path d="M7 57V30L22 38V28L37 36V16H50V57Z"/><path d="M42 16V7H51V16M15 46H21M27 46H33M40 46H46"/>',
"rocket":'<path d="M32 5Q48 15 45 39L32 52L19 39Q16 15 32 5Z"/><circle cx="32" cy="27" r="6"/><path d="M19 34L8 48L21 45M45 34L56 48L43 45M27 51L32 60L37 51"/>',
"warning":'<path d="M32 6L59 55H5Z"/><path d="M32 22V38M32 46V48"/>',
"search":'<circle cx="27" cy="27" r="17"/><path d="M40 40L57 57"/>',
"compass":'<circle cx="32" cy="32" r="26"/><path d="M41 21L35 36L20 43L27 28Z"/>',
"lightning":'<path d="M36 4L13 35H29L25 60L51 25H35Z"/>',
"check":'<path d="M10 34L25 49L55 14"/>',
"close":'<path d="M14 14L50 50M50 14L14 50"/>',
"arrow":'<path d="M7 32H55M38 14L56 32L38 50"/>',
"location-pin":'<path d="M32 59S11 36 11 25A21 21 0 1 1 53 25Q53 36 32 59Z"/><circle cx="32" cy="25" r="7"/>',
"food":'<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="14"/><path d="M8 7V24M4 7V17M12 7V17M55 7V59M51 7V17"/>',
"eye":'<path d="M5 32Q32 3 59 32Q32 61 5 32Z"/><circle cx="32" cy="32" r="9"/>',
"presentation":'<rect x="8" y="8" width="48" height="34" rx="2"/><path d="M32 42V57M18 57H46M15 33L25 25L32 30L45 17"/>',
"music":'<path d="M26 48V14L55 7V41"/><ellipse cx="18" cy="49" rx="8" ry="6"/><ellipse cx="47" cy="42" rx="8" ry="6"/>',
"book-open":'<path d="M7 14Q21 9 32 18Q43 9 57 14V52Q42 46 32 55Q22 46 7 52Z"/><path d="M32 18V55"/>',
"map":'<path d="M7 13L23 6L41 13L57 6V50L41 57L23 50L7 57Z"/><path d="M23 6V50M41 13V57M33 18C33 18 23 30 23 36A10 10 0 0 0 43 36C43 30 33 18 33 18Z"/>',
"audio-wave":'<path d="M6 34H12L18 19L25 49L32 10L39 52L46 20L52 35H58"/>',
"database":'<ellipse cx="32" cy="13" rx="23" ry="7"/><path d="M9 13V49C9 59 55 59 55 49V13M9 31C9 40 55 40 55 31"/>',
"shield-lock":'<path d="M32 6L53 14V31Q51 47 32 58Q13 47 11 31V14Z"/><rect x="23" y="28" width="18" height="15" rx="3"/><path d="M27 28V23A5 5 0 0 1 37 23V28"/>',
"paw":'<ellipse cx="32" cy="42" rx="15" ry="11"/><circle cx="15" cy="24" r="6"/><circle cx="28" cy="17" r="6"/><circle cx="42" cy="18" r="6"/><circle cx="53" cy="27" r="6"/>',
"camera-film":'<rect x="8" y="10" width="48" height="44" rx="4"/><path d="M17 10V18M29 10V18M41 10V18M53 10V18M17 46V54M29 46V54M41 46V54M53 46V54"/><path d="M25 23L42 32L25 41Z"/>'
}


# Additional purpose-built pictograms broaden the visual vocabulary without importing icon packs.
ICONS.update({
"satellite":'<rect x="24" y="24" width="16" height="16" rx="3"/><path d="M23 23L12 12M41 41L52 52M7 7L20 20M44 44L57 57M9 27L27 9M37 55L55 37"/>',
"telescope":'<path d="M12 12L39 5L45 22L18 29Z"/><path d="M18 29L28 42M39 24L50 48M29 42L19 59M49 48L56 59M10 59H60"/>',
"volcano":'<path d="M5 56L20 27L29 40L36 20L59 56Z"/><path d="M26 25Q20 17 27 8M36 18Q43 11 39 5M31 25L34 31M20 32L24 36"/>',
"wave":'<path d="M4 25Q13 10 22 25T40 25T58 25M4 40Q13 25 22 40T40 40T58 40M4 54Q13 39 22 54T40 54T58 54"/>',
"ship":'<path d="M7 38H57L48 53H17Z"/><path d="M16 38V20H31V38M34 38V11H45V38M8 58Q18 53 28 58T48 58T60 58"/>',
"train":'<rect x="10" y="6" width="44" height="43" rx="8"/><path d="M18 16H46V30H18ZM20 49L13 58M44 49L51 58M15 38H49"/><circle cx="21" cy="39" r="2"/><circle cx="43" cy="39" r="2"/>',
"bicycle":'<circle cx="15" cy="45" r="11"/><circle cx="49" cy="45" r="11"/><path d="M15 45L27 25L39 45H15L33 31H44M24 21H32M38 25H46"/>',
"helmet":'<path d="M7 43A25 25 0 0 1 57 43H7Z"/><path d="M17 43V29M30 43V19M43 43V29M7 43H60"/>',
"medal":'<circle cx="32" cy="37" r="17"/><path d="M21 6H43L40 22L32 29L24 22Z"/><path d="M32 28L36 35L44 36L38 42L39 50L32 46L25 50L26 42L20 36L28 35Z"/>',
"flag":'<path d="M12 59V5M14 9H52L43 22L52 35H14"/>',
"megaphone":'<path d="M8 26H22L51 12V50L22 36H8Z"/><path d="M20 36L26 54H37L31 41M55 24L61 21M55 38L61 41"/>',
"package":'<path d="M7 20L32 7L57 20V47L32 60L7 47Z"/><path d="M7 20L32 34L57 20M32 34V60M20 13L45 27"/>',
"shopping-bag":'<path d="M9 22H55L51 58H13Z"/><path d="M21 24V17A11 11 0 0 1 43 17V24"/>',
"laptop":'<rect x="12" y="8" width="40" height="34" rx="3"/><path d="M5 49H59L53 57H11Z"/>',
"code":'<path d="M23 18L9 32L23 46M41 18L55 32L41 46M36 12L28 52"/>',
"terminal":'<rect x="6" y="9" width="52" height="46" rx="5"/><path d="M15 22L23 29L15 36M29 38H45M7 17H57"/>',
"wrench":'<path d="M39 8A16 16 0 0 0 22 29L7 44A7 7 0 0 0 17 54L32 39A16 16 0 0 0 53 19L42 30L32 20Z"/>',
"scales":'<path d="M32 8V55M18 55H46M13 19H51M32 13L13 19M32 13L51 19M13 19L5 36H21ZM51 19L43 36H59Z"/>',
"gavel":'<path d="M16 11L29 24M23 5L35 17L25 27L13 15ZM33 28L47 42M40 22L52 34L42 44L30 32ZM7 56H47M23 46L31 54"/>',
"recycle":'<path d="M26 9L35 9L42 21M42 21L33 21M42 21L47 13M48 31L54 40L48 49H36M36 49L41 42M36 49L44 55M24 49H13L7 39L13 29M13 29L22 29M13 29L13 38M17 21L23 11H34M34 11L30 18M34 11L38 18"/>',
"thermometer":'<path d="M26 37V14A7 7 0 0 1 40 14V37A13 13 0 1 1 26 37Z"/><path d="M33 22V44"/>',
"pulse":'<path d="M4 34H17L24 17L35 49L43 27L48 34H60"/>',
"virus":'<circle cx="32" cy="32" r="15"/><path d="M32 6V17M32 47V58M6 32H17M47 32H58M14 14L22 22M42 42L50 50M14 50L22 42M42 22L50 14"/><circle cx="27" cy="28" r="2"/><circle cx="38" cy="36" r="2"/>',
"map-route":'<path d="M7 13L23 7L41 14L57 8V51L41 57L23 50L7 57Z"/><path d="M23 7V50M41 14V57M14 39Q28 12 37 31T50 24"/><circle cx="14" cy="39" r="3"/><circle cx="50" cy="24" r="3"/>',
"moon-stars":'<path d="M43 42A22 22 0 0 1 21 13A24 24 0 1 0 43 42Z"/><path d="M46 8L49 15L56 18L49 21L46 28L43 21L36 18L43 15ZM16 27L18 31L22 33L18 35L16 39L14 35L10 33L14 31Z"/>',
"film-strip":'<rect x="6" y="7" width="52" height="50" rx="3"/><path d="M17 7V57M47 7V57M17 18H47M17 46H47"/>',
"clapperboard":'<path d="M7 24H57V57H7Z"/><path d="M7 24L11 7H57L53 24Z"/><path d="M14 7L23 24M31 7L40 24M48 7L55 20"/>',
"star":'<path d="M32 5L40 23L60 25L45 39L49 59L32 49L15 59L19 39L4 25L24 23Z"/>',
"flame":'<path d="M33 5Q40 20 30 26Q35 13 21 12Q24 29 13 37Q5 48 17 56Q31 63 44 54Q58 43 47 29Q44 21 33 5Z"/><path d="M31 38Q38 45 31 53Q22 51 25 44Z"/>',
"droplet":'<path d="M32 5C25 20 12 34 12 44A20 20 0 0 0 52 44C52 34 39 20 32 5Z"/><path d="M23 45Q25 52 32 52"/>',
"puzzle":'<path d="M8 8H25A7 7 0 1 1 39 8H56V25A7 7 0 1 0 56 39V56H39A7 7 0 1 1 25 56H8V39A7 7 0 1 0 8 25Z"/>',
"speech-bubble":'<path d="M7 11H57V43H33L19 56V43H7Z"/><path d="M16 22H48M16 31H40"/>'
})

def make_illustration_svg(asset_id,title,category,icon_id,index):
    """Create a self-contained editorial illustration from an original vector pictogram."""
    drawing=ICONS.get(icon_id)
    if not drawing:
        raise RuntimeError(f"missing illustration icon: {icon_id}")
    palettes=[
        ("#102438","#60ddcc","#d9fff8"),("#232338","#f5bd7a","#fff0d4"),
        ("#142c23","#a3d995","#e9f2d2"),("#252330","#eaa3bd","#ffe9f0"),
        ("#252a32","#a7caff","#eef5ff"),("#2a2522","#e9cf9b","#fff5d8"),
        ("#171d30","#b6a3ff","#eee9ff"),("#1b2d39","#f2a36f","#fff0dc")
    ]
    bg,accent,light=palettes[index%len(palettes)]
    dots=[]
    for j in range(19):
        x=(j*137+31+index*23)%640; y=(j*91+57+index*17)%640
        radius=2+(j%4)
        dots.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{light}" fill-opacity="{.08+(j%4)*.025:.3f}"/>')
    css=f'<style>.line{{stroke:{light};stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;fill:none}}</style>'
    defs=f'''<radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".28"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="pedestal" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{accent}" stop-opacity=".25"/><stop offset="1" stop-color="{bg}" stop-opacity=".08"/></linearGradient>
<pattern id="microgrid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{light}" stroke-opacity=".045" stroke-width="1"/></pattern>{css}'''
    base=(f'<rect width="640" height="640" fill="url(#microgrid)"/>'
          f'<ellipse cx="320" cy="282" rx="238" ry="238" fill="url(#halo)"/>'
          f'<circle cx="320" cy="282" r="205" fill="none" stroke="{accent}" stroke-opacity=".14" stroke-width="2" stroke-dasharray="5 13"/>'
          f'<path d="M86 518Q320 466 554 518L526 568Q320 534 114 568Z" fill="url(#pedestal)" stroke="{accent}" stroke-opacity=".24" stroke-width="2"/>'
          + "".join(dots))
    icon=f'<g transform="translate(108 70) scale(6.62)" class="line" style="color:{accent}">{drawing}</g>'
    title_text=html.escape(title.upper())
    label=(f'<rect x="110" y="584" width="420" height="34" rx="17" fill="{bg}" fill-opacity=".82" stroke="{accent}" stroke-opacity=".26"/>'
           f'<text x="320" y="607" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="1.2" fill="{light}">{title_text[:46]}</text>')
    return svg_doc(base+icon+label,defs,width=640,height=640)


def generate_original_illustrations(root,index):
    target_dir=root/"originals/illustrations"
    target_dir.mkdir(parents=True,exist_ok=True)
    for i,(asset_id,title,category,icon_id) in enumerate(ILLUSTRATIONS):
        path=target_dir/(asset_id+".svg")
        write_text(path,make_illustration_svg(asset_id,title,category,icon_id,i))
        index.append({"id":asset_id,"path":path.relative_to(root).as_posix(),
                      "type":"original-svg-editorial-illustration","title":title,
                      "category":category,"icon_source_id":icon_id,"license":CC0,"license_url":CC0_URL,
                      "redistributable":True,
                      "note":"Original repository-generated vector illustration; may be scaled for a shot. The included title strip is part of the artwork."})
    return len(ILLUSTRATIONS)


def motion_loop_filters(style):
    """Return an original, periodic vector-like filter chain for a six-second 24 fps loop."""
    orbital = "drawgrid=width=72:height=72:thickness=1:color=0x3ed9c7@0.18,drawbox=x='550+240*sin(2*PI*t/6)':y='260+110*cos(2*PI*t/6)':w=180:h=180:color=0x3ed9c7@0.12:t=fill,drawbox=x='550+240*sin(2*PI*t/6)':y='260+110*cos(2*PI*t/6)':w=180:h=180:color=0x3ed9c7@0.75:t=3"
    data = "drawgrid=width=48:height=48:thickness=1:color=0x55baff@0.12,drawbox=x='100+420*(1+sin(2*PI*t/6))/2':y=0:w=5:h=720:color=0x55baff@0.6:t=fill,drawbox=x='500+420*(1+sin(2*PI*t/6+2.1))/2':y=0:w=3:h=720:color=0x66e2c5@0.55:t=fill,drawbox=x=0:y='170+90*sin(2*PI*t/6)':w=1280:h=2:color=0x55baff@0.45:t=fill"
    circuit = "drawgrid=width=64:height=64:thickness=1:color=0xff58c9@0.13,drawbox=x='160+420*(1+sin(2*PI*t/6))/2':y=180:w=240:h=5:color=0xff58c9@0.72:t=fill,drawbox=x='760+210*(1+sin(2*PI*t/6+1.4))/2':y=420:w=190:h=4:color=0x58e8ff@0.72:t=fill,drawbox=x=300:y=180:w=4:h=260:color=0xff58c9@0.42:t=fill,drawbox=x=850:y=420:w=4:h=160:color=0x58e8ff@0.42:t=fill"
    water = "drawgrid=width=128:height=64:thickness=1:color=0x5ad4e8@0.10,drawbox=x=0:y='170+45*sin(2*PI*t/6)':w=1280:h=3:color=0x5ad4e8@0.35:t=fill,drawbox=x=0:y='260+38*sin(2*PI*t/6+1.2)':w=1280:h=2:color=0x5ad4e8@0.27:t=fill,drawbox=x=0:y='360+30*sin(2*PI*t/6+2.0)':w=1280:h=3:color=0x83e8dc@0.30:t=fill,drawbox=x=0:y='490+34*sin(2*PI*t/6+3.1)':w=1280:h=2:color=0x5ad4e8@0.22:t=fill"
    aurora = "drawbox=x='-80+110*sin(2*PI*t/6)':y='80+30*cos(2*PI*t/6)':w=1440:h=80:color=0x40e0c0@0.12:t=fill,drawbox=x='-80+120*sin(2*PI*t/6+1.2)':y='180+28*cos(2*PI*t/6+1.2)':w=1440:h=50:color=0x5c8dff@0.10:t=fill,drawbox=x='-80+130*sin(2*PI*t/6+2.4)':y='270+25*cos(2*PI*t/6+2.4)':w=1440:h=36:color=0xbf68ff@0.10:t=fill,drawgrid=width=160:height=120:thickness=1:color=0xc7e8ff@0.07"
    retro = "drawgrid=width=64:height=24:thickness=1:color=0xb28cff@0.18,drawbox=x=0:y='120+12*sin(2*PI*t/6)':w=1280:h=3:color=0xff70c9@0.55:t=fill,drawbox=x='420+160*sin(2*PI*t/6)':y=250:w=440:h=220:color=0xff70c9@0.05:t=fill,drawbox=x='420+160*sin(2*PI*t/6)':y=250:w=440:h=220:color=0xff70c9@0.55:t=3"
    film = "noise=alls=5:allf=t,drawbox=x=0:y='140+6*sin(2*PI*t/6)':w=1280:h=2:color=0xf0e6d2@0.18:t=fill,drawbox=x=0:y=718:w=1280:h=2:color=0xf0e6d2@0.25:t=fill,drawgrid=width=160:height=120:thickness=1:color=0xe5d7bd@0.04"
    hazard = "drawgrid=width=84:height=84:thickness=1:color=0xffc84a@0.10,drawbox=x='100+380*(1+sin(2*PI*t/6))/2':y=0:w=30:h=720:color=0xffc84a@0.2:t=fill,drawbox=x='100+380*(1+sin(2*PI*t/6))/2':y=160:w=420:h=6:color=0xffc84a@0.65:t=fill,drawbox=x='100+380*(1+sin(2*PI*t/6))/2':y=550:w=420:h=4:color=0xffc84a@0.45:t=fill"
    spectrum_parts = ["drawgrid=width=128:height=120:thickness=1:color=0x7eaaff@0.08"]
    for i in range(28):
        x=72+i*42
        phase=i*0.37
        height_expr=f"30+200*(1+sin(2*PI*t/1.5+{phase:.3f}))/2"
        spectrum_parts.append(f"drawbox=x={x}:y='360-({height_expr})/2':w=18:h='({height_expr})':color=0x76e0d2@{0.25+(i%5)*0.1:.2f}:t=fill")
    spectrum=",".join(spectrum_parts)
    particle_parts = ["drawgrid=width=160:height=120:thickness=1:color=0xa5d5ff@0.07"]
    for i in range(18):
        base_x=40+(i*173)%1160
        base_y=35+(i*101)%650
        phase=i*0.53
        size=2+(i%4)*2
        particle_parts.append(
            f"drawbox=x='{base_x}+70*sin(2*PI*t/6+{phase:.3f})':"
            f"y='{base_y}+42*cos(2*PI*t/6+{phase:.3f})':"
            f"w={size}:h={size}:color=0x90ddff@{0.35+(i%4)*0.1:.2f}:t=fill"
        )
    particles=",".join(particle_parts)
    route = "drawgrid=width=96:height=96:thickness=1:color=0x81d7c6@0.12,drawbox=x=150:y=530:w=980:h=3:color=0x81d7c6@0.34:t=fill,drawbox=x='160+900*(1+sin(2*PI*t/6))/2':y=520:w=24:h=24:color=0x81d7c6@0.85:t=fill,drawbox=x='160+900*(1+sin(2*PI*t/6))/2':y=530:w=24:h=3:color=0xeafff8@0.95:t=fill"
    bokeh_parts = []
    for i in range(18):
        x=(i*191+47)%1180
        y=(i*113+37)%650
        radius=20+(i%5)*14
        phase=i*0.42
        color=["0x65cfff","0x86e6c9","0xc99cff","0xffc59c"][i%4]
        bokeh_parts.append(
            f"drawbox=x='{x}+55*sin(2*PI*t/6+{phase:.3f})':"
            f"y='{y}+35*cos(2*PI*t/6+{phase:.3f})':"
            f"w={radius}:h={radius}:color={color}@0.10:t=fill"
        )
    bokeh=",".join(bokeh_parts)
    choices={"orbital":orbital,"data":data,"circuit":circuit,"water":water,
             "aurora":aurora,"retro":retro,"film":film,"hazard":hazard,
             "spectrum":spectrum,"particles":particles,"route":route,"bokeh":bokeh}
    if style not in choices:
        raise ValueError(f"Unknown motion-loop style: {style}")
    return choices[style]


def generate_original_motion_loops(root,index):
    """Render original six-second motion loops and verify each file with ffprobe."""
    ffmpeg=shutil.which("ffmpeg")
    ffprobe=shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required to create/verify original motion loops")
    target_dir=root/"originals/video-loops"
    target_dir.mkdir(parents=True,exist_ok=True)
    for loop_id,title,category,base_color,style in MOTION_LOOPS:
        path=target_dir/(loop_id+".mp4")
        filter_chain=motion_loop_filters(style)
        command=[
            ffmpeg,"-hide_banner","-loglevel","error","-y",
            "-f","lavfi","-i",f"color=c={base_color}:s=1280x720:r=24:d=6",
            "-vf",filter_chain,"-an","-t","6","-r","24",
            "-c:v","libx264","-preset","veryfast","-crf","25",
            "-pix_fmt","yuv420p","-movflags","+faststart",str(path)
        ]
        result=subprocess.run(command,capture_output=True,text=True,timeout=240,check=False)
        if result.returncode!=0:
            raise RuntimeError(f"ffmpeg failed to render {loop_id}: {(result.stderr or result.stdout)[-1400:]}")
        probe=subprocess.run([
            ffprobe,"-v","error","-show_entries","format=duration:stream=codec_name,width,height,avg_frame_rate",
            "-of","json",str(path)
        ],capture_output=True,text=True,timeout=30,check=False)
        if probe.returncode!=0:
            raise RuntimeError(f"ffprobe could not inspect {loop_id}: {(probe.stderr or probe.stdout)[-800:]}")
        metadata=json.loads(probe.stdout or "{}")
        streams=metadata.get("streams") or []
        video=next((s for s in streams if s.get("codec_name")),None)
        duration=float((metadata.get("format") or {}).get("duration") or 0)
        if not video or video.get("codec_name")!="h264" or video.get("width")!=1280 or video.get("height")!=720:
            raise RuntimeError(f"Generated loop failed video-stream verification: {loop_id} ({metadata})")
        if not 5.8<=duration<=6.2:
            raise RuntimeError(f"Generated loop duration is not approximately 6 seconds: {loop_id}={duration}")
        digest=sha256_path(path)
        index.append({"id":loop_id,"path":path.relative_to(root).as_posix(),
                      "type":"original-procedural-video-loop","title":title,"category":category,
                      "duration_seconds":round(duration,3),"width":1280,"height":720,"fps":"24/1",
                      "codec":"h264","license":CC0,"license_url":CC0_URL,"redistributable":True,
                      "size_bytes":path.stat().st_size,"sha256":digest,
                      "note":"Original six-second procedural motion loop generated in-repository from FFmpeg filters; no external footage, audio or image assets are embedded."})
        print("[Motion loop] verified:",loop_id,path.stat().st_size,"bytes")
    return len(MOTION_LOOPS)


def make_texture_svg(texture_id,title,index):
    """Create tileable, original, vector texture plates with no external dependencies."""
    palettes=[
        ("#0c1d2b","#64dcca"),("#17202c","#c6d2dc"),("#d9c7a2","#7a6850"),
        ("#222832","#8fa9b8"),("#173a4a","#7be3d6"),("#e8e2d6","#4f5d69"),
        ("#2c2025","#dcad87"),("#101b29","#84c7ff")
    ]
    bg,accent=palettes[index%len(palettes)]
    pattern=""
    if texture_id in {"blueprint-grid","crosshair-grid","blueprint-dimensions","isometric-grid"}:
        step=64 if texture_id!="isometric-grid" else 96
        lines=[f'<path d="M0 {step//2}H1024M{step//2} 0V1024" stroke="{accent}" stroke-opacity=".19" stroke-width="1"/>']
        for x in range(0,1025,step):
            lines.append(f'<path d="M{x} 0V1024" stroke="{accent}" stroke-opacity="{.25 if x% (step*4)==0 else .1}" stroke-width="1"/>')
        for y in range(0,1025,step):
            lines.append(f'<path d="M0 {y}H1024" stroke="{accent}" stroke-opacity="{.25 if y%(step*4)==0 else .1}" stroke-width="1"/>')
        if texture_id=="crosshair-grid":
            for x in range(32,1024,128):
                for y in range(32,1024,128):
                    lines.append(f'<path d="M{x-8} {y}H{x+8}M{x} {y-8}V{y+8}" stroke="{accent}" stroke-opacity=".45"/>')
        if texture_id=="isometric-grid":
            for n in range(-1024,2048,96):
                lines.append(f'<path d="M{n} 0L{n+1024} 1024M{n} 1024L{n+1024} 0" stroke="{accent}" stroke-opacity=".13"/>')
        pattern="".join(lines)
    elif texture_id in {"topographic-contours","bathymetry-contours","soft-clouds","geology-strata"}:
        for i in range(24):
            x=(i*97+31)%1024; y=(i*67+20)%1024
            rx=90+(i%7)*26; ry=55+(i%5)*21
            pattern+=f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({(i*19)%70-35} {x} {y})" fill="none" stroke="{accent}" stroke-opacity="{.08+(i%5)*.035:.3f}" stroke-width="{1+i%3}"/>'
        if texture_id=="geology-strata":
            for i in range(10):
                y=i*110+40
                pattern+=f'<path d="M0 {y}Q250 {y-40} 470 {y+12}T1024 {y}" fill="none" stroke="{accent}" stroke-opacity=".22" stroke-width="{3+i%3}"/>'
    elif texture_id in {"archival-paper","paper-fibers","wood-grain","brushed-metal","film-scratches","diagonal-hatch"}:
        for i in range(110):
            x=(i*173+13)%1024; y=(i*97+7)%1024
            if texture_id=="wood-grain":
                pattern+=f'<path d="M0 {y}Q250 {y-20+(i%7)*6} 520 {y+8}T1024 {y}" fill="none" stroke="{accent}" stroke-opacity=".13" stroke-width="{1+i%4}"/>'
            elif texture_id=="diagonal-hatch":
                pattern+=f'<path d="M{x} {y}l90 -90" stroke="{accent}" stroke-opacity=".16" stroke-width="{1+i%3}"/>'
            else:
                x2=min(1024,x+(10+(i%55) if texture_id!="film-scratches" else 1+(i%3)))
                y2=min(1024,y+(2+(i%5) if texture_id=="film-scratches" else 1))
                pattern+=f'<path d="M{x} {y}L{x2} {y2}" stroke="{accent}" stroke-opacity="{.06+(i%6)*.025:.3f}" stroke-width="{1+i%3}"/>'
    elif texture_id in {"newspaper-halftone","comic-dots","pixel-grid","dither-noise","star-map","rain-droplets"}:
        step=12 if texture_id in {"newspaper-halftone","comic-dots","dither-noise"} else 32
        for y in range(step//2,1024,step):
            for x in range(step//2,1024,step):
                n=(x*31+y*17+index*7)%11
                if texture_id=="rain-droplets":
                    pattern+=f'<ellipse cx="{x}" cy="{y}" rx="{2+n%5}" ry="{4+n%8}" fill="{accent}" fill-opacity=".18"/>'
                elif texture_id=="star-map":
                    pattern+=f'<circle cx="{x}" cy="{y}" r="{.8+n%3}" fill="{accent}" fill-opacity="{.2+(n%6)*.1:.2f}"/>'
                elif texture_id=="pixel-grid":
                    pattern+=f'<rect x="{x-step/2}" y="{y-step/2}" width="{step-2}" height="{step-2}" fill="{accent}" fill-opacity="{.04+(n%6)*.045:.3f}"/>'
                else:
                    pattern+=f'<circle cx="{x}" cy="{y}" r="{.5+n%6}" fill="{accent}" fill-opacity="{.05+(n%7)*.04:.3f}"/>'
    elif texture_id in {"carbon-fiber","textile-weave","woven-basket","rubber-diamond","perforated-metal","ceramic-tile","terrazzo-speckle","concrete-speckle","marble-veins","hex-mesh","circuit-board","neon-circuit","geometric-triangles"}:
        if texture_id in {"carbon-fiber","textile-weave","woven-basket"}:
            step=16 if texture_id!="carbon-fiber" else 24
            for y in range(0,1024,step):
                for x in range(0,1024,step):
                    alt=(x//step+y//step)%2
                    fill=accent if alt else "#ffffff"
                    pattern+=f'<rect x="{x}" y="{y}" width="{step}" height="{step}" fill="{fill}" fill-opacity="{.08 if alt else .025}"/><path d="M{x} {y+step//2}H{x+step}M{x+step//2} {y}V{y+step}" stroke="{accent}" stroke-opacity=".13"/>'
        elif texture_id=="ceramic-tile":
            step=128
            for y in range(0,1024,step):
                for x in range(0,1024,step):
                    pattern+=f'<rect x="{x+4}" y="{y+4}" width="{step-8}" height="{step-8}" rx="4" fill="{accent}" fill-opacity=".04" stroke="{accent}" stroke-opacity=".23" stroke-width="3"/>'
        elif texture_id=="rubber-diamond":
            for x in range(-1024,2048,64):
                pattern+=f'<path d="M{x} 0L{x+1024} 1024M{x} 1024L{x+1024} 0" stroke="{accent}" stroke-opacity=".18" stroke-width="12"/>'
        elif texture_id=="perforated-metal":
            for y in range(16,1024,32):
                for x in range(16,1024,32):
                    pattern+=f'<circle cx="{x}" cy="{y}" r="5" fill="{accent}" fill-opacity=".18"/>'
        elif texture_id=="terrazzo-speckle":
            for i in range(260):
                x=(i*151+17)%1024; y=(i*89+27)%1024; r=2+(i%9)
                pattern+=f'<path d="M{x} {y}l{r*2} {r}l{-r} {r*2}l{-r*2} {-r}Z" fill="{accent}" fill-opacity=".16"/>'
        elif texture_id=="concrete-speckle":
            for i in range(400):
                x=(i*137+21)%1024; y=(i*83+19)%1024; r=1+(i%4)
                pattern+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent}" fill-opacity=".1"/>'
        elif texture_id=="marble-veins":
            for i in range(14):
                y=i*83+25
                pattern+=f'<path d="M0 {y}Q220 {y-35} 420 {y+8}T820 {y-12}T1024 {y+15}" fill="none" stroke="{accent}" stroke-opacity=".24" stroke-width="{1+i%4}"/>'
        elif texture_id=="hex-mesh":
            for y in range(-32,1056,56):
                for x in range(-32,1056,64):
                    xx=x+(32 if (y//56)%2 else 0)
                    pattern+=f'<path d="M{xx} {y-18}l16 -9l16 9v18l-16 9l-16 -9Z" fill="none" stroke="{accent}" stroke-opacity=".22" stroke-width="2"/>'
        elif texture_id in {"circuit-board","neon-circuit"}:
            for i in range(60):
                x=(i*139+17)%1024; y=(i*83+29)%1024
                pattern+=f'<path d="M{x} {y}h{32+(i%5)*18}v{16+(i%4)*19}h{28+(i%3)*17}" fill="none" stroke="{accent}" stroke-opacity="{.15 if texture_id=="circuit-board" else .4}" stroke-width="{1+i%3}"/><circle cx="{x}" cy="{y}" r="4" fill="{accent}" fill-opacity=".6"/>'
        else:
            for i in range(26):
                x=(i*173+23)%1024; y=(i*97+31)%1024; pts=[(x,y),(x+45+(i%5)*7,y+18),(x+8,y+70+(i%4)*9)]
                pattern+=f'<polygon points="{" ".join(f"{px},{py}" for px,py in pts)}" fill="{accent}" fill-opacity="{.045+(i%5)*.025:.3f}"/>'
    return svg_doc(f'<rect width="1024" height="1024" fill="{bg}"/><g>{pattern}</g>',width=1024,height=1024)


def generate_original_textures(root,index):
    out=root/"originals/textures"
    out.mkdir(parents=True,exist_ok=True)
    for i,(texture_id,title) in enumerate(TEXTURES):
        path=out/(texture_id+".svg")
        write_text(path,make_texture_svg(texture_id,title,i))
        index.append({"id":texture_id,"path":path.relative_to(root).as_posix(),"type":"original-svg-texture",
                      "title":title,"category":"texture / surface","license":CC0,"license_url":CC0_URL,
                      "redistributable":True,"tileable":True,
                      "note":"Original vector-generated texture. Preview at reduced opacity or use as a surface shader input."})
    return len(TEXTURES)


def request_bytes(url, timeout=45, limit=None):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=timeout) as resp:
        data=resp.read(limit+1 if limit else -1)
        if limit and len(data)>limit: raise RuntimeError(f"file larger than allowed limit: {url}")
        return data, resp.headers.get("Content-Type","application/octet-stream")

def request_json(url, timeout=45):
    raw,_=request_bytes(url,timeout,25*1024*1024)
    return json.loads(raw.decode("utf-8"))

def write_text(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding="utf-8")

def sha256_path(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def slugify(text):
    return re.sub(r"-+","-",re.sub(r"[^a-zA-Z0-9._-]+","-",str(text).lower())).strip("-")[:72] or "asset"

def svg_doc(body, defs="", width=1920, height=1080, bg=None):
    bgsvg=f'<rect width="{width}" height="{height}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs>{defs}</defs>{bgsvg}{body}</svg>'

def make_background(asset_id,palette,kind):
    top,bottom,accent=palette
    defs=f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>
<radialGradient id="glow"><stop stop-color="{accent}" stop-opacity=".72"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="{accent}" stroke-opacity=".13" stroke-width="2"/></pattern>'''
    p=[f'<rect width="1920" height="1080" fill="url(#sky)"/>','<ellipse cx="1460" cy="250" rx="420" ry="340" fill="url(#glow)"/>','<rect width="1920" height="1080" fill="url(#grid)" opacity=".28"/>']
    if kind in {"city","news","metro","underpass","rooftop","hospital"}:
        if kind=="rooftop":
            p.append(f'<circle cx="1450" cy="315" r="118" fill="{accent}" opacity=".85"/><path d="M0 610L190 510L330 575L480 430L640 560L830 470L1020 590L1190 455L1390 560L1590 440L1920 585V850H0Z" fill="{top}" opacity=".45"/>')
        else:
            n=17
            for layer,(base,color,op) in enumerate([(610,top,.55),(770,bottom,.92)]):
                width=1920/n
                for i in range(n):
                    x=i*width-layer*38; h=130+((i*71+layer*47+len(asset_id)*19)%350); y=base-h; w=width*(.74+(i%3)*.05)
                    p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="5" fill="{color}" opacity="{op}"/>')
                    for row in range(max(1,int(h/55))):
                        for col in range(2+(i%2)):
                            wx=x+18+col*(w-36)/(2+(i%2)); wy=y+28+row*48
                            p.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="12" height="22" rx="2" fill="{accent}" opacity="{.14+((i+row+col)%4)*.12:.2f}"/>')
        if kind in {"metro","underpass","hospital"}:
            for i in range(8):
                x=i*275-50
                p.append(f'<path d="M{x} 100Q960 20 {1920-x} 100M{x} 100V800M{1920-x} 100V800" fill="none" stroke="{accent}" stroke-opacity=".28" stroke-width="9"/>')
        if kind=="news":
            for i in range(5):
                x=140+i*340
                p.append(f'<rect x="{x}" y="140" width="290" height="235" rx="16" fill="#08101a" stroke="{accent}" stroke-width="4" stroke-opacity=".7"/><path d="M{x+30} 325L{x+90} 265L{x+150} 295L{x+220} 200" fill="none" stroke="{accent}" stroke-width="7"/>')
            p.append(f'<rect y="910" width="1920" height="110" fill="{top}" stroke="{accent}" stroke-opacity=".65" stroke-width="3"/>')
        if kind=="hospital":
            p.append(f'<path d="M930 260H990V330H1060V390H990V460H930V390H860V330H930Z" fill="{accent}" opacity=".82"/>')
    elif kind in {"forest","greenhouse"}:
        for layer in range(3):
            count=17-layer*4; span=1920/count
            for i in range(count):
                x=i*span-span*.3; h=230+((i*43+layer*59)%420); w=18+layer*11; col=top if layer%2==0 else bottom
                p.append(f'<path d="M{x} 930L{x+w} 930L{x+w/2} {930-h}Z" fill="{col}" opacity="{.42+layer*.18:.2f}"/>')
                p.append(f'<rect x="{x+w*.35}" y="{930-h*.48}" width="{w*.3}" height="{h*.48}" fill="{col}"/>')
                if layer<2:
                    for branch in range(4):
                        cy=930-h+40+branch*45
                        p.append(f'<ellipse cx="{x+w/2}" cy="{cy}" rx="{w*2.7}" ry="{w*1.65}" fill="{bottom}" opacity=".52"/>')
        for i in range(6): p.append(f'<ellipse cx="{150+i*330}" cy="{775+(i%2)*45}" rx="270" ry="46" fill="#e3f0d8" opacity=".055"/>')
        if kind=="greenhouse":
            p.append(f'<path d="M80 900V190H1840V900M80 190L960 70L1840 190M330 190V900M640 150V900M960 110V900M1280 150V900M1590 190V900" fill="none" stroke="{accent}" stroke-width="8" stroke-opacity=".48"/>')
    elif kind in {"mountain","beach","snow","desert"}:
        p.append(f'<circle cx="1440" cy="370" r="120" fill="{accent}" opacity=".85"/>')
        if kind=="beach":
            p.append(f'<path d="M0 590Q360 550 690 600T1350 590T1920 620V1080H0Z" fill="#477d91" opacity=".7"/>')
            for i in range(13):
                y=640+i*30; p.append(f'<path d="M0 {y}Q460 {y-25} 900 {y+8}T1920 {y}" fill="none" stroke="#d8ebe9" stroke-width="{2+i%3}" stroke-opacity=".28"/>')
            p.append(f'<path d="M0 850Q480 750 920 900T1920 830V1080H0Z" fill="{bottom}"/>')
        else:
            for layer in range(4):
                pts=[]
                for i in range(13): pts.append(f'{i*160},{440+layer*110+((i*83+layer*37+len(asset_id)*23)%180)}')
                p.append(f'<polygon points="0,1080 {" ".join(pts)} 1920,1080" fill="{bottom if layer%2 else top}" opacity="{.32+layer*.17:.2f}"/>')
            if kind=="desert":
                for i in range(5): p.append(f'<path d="M0 {700+i*75}Q460 {590+i*75} 900 {710+i*75}T1920 {680+i*75}" fill="none" stroke="{accent}" stroke-opacity=".23" stroke-width="4"/>')
            if kind=="snow":
                for i in range(140): p.append(f'<circle cx="{(i*137+19)%1920}" cy="{(i*83+11)%900}" r="{1+i%4}" fill="#f2fbff" opacity=".65"/>')
    elif kind=="space":
        for i in range(260): p.append(f'<circle cx="{(i*157+37)%1920}" cy="{(i*97+13)%940}" r="{.8+(i%5)*.65}" fill="#f2f4ff" opacity="{.25+(i%6)*.1:.2f}"/>')
        p.append(f'<circle cx="1330" cy="430" r="165" fill="{accent}" opacity=".88"/><ellipse cx="1330" cy="430" rx="260" ry="62" fill="none" stroke="{bottom}" stroke-width="33" transform="rotate(-18 1330 430)"/><ellipse cx="1330" cy="430" rx="260" ry="62" fill="none" stroke="#e4dafe" stroke-opacity=".58" stroke-width="5" transform="rotate(-18 1330 430)"/>')
    elif kind in {"lab","finance","server","classroom","museum","factory","product","food","castle","gaming","cyber","map","sports","horror","network","studio"}:
        p.append(f'<path d="M0 110H1920M0 675H1920M320 110V675M640 110V675M960 110V675M1280 110V675M1600 110V675" fill="none" stroke="{accent}" stroke-opacity=".12" stroke-width="4"/>')
        if kind=="lab":
            for i in range(7):
                x=145+i*235
                p.append(f'<rect x="{x}" y="490" width="155" height="260" rx="8" fill="{bottom}" stroke="{accent}" stroke-opacity=".55" stroke-width="4"/><path d="M{x+40} 550H{x+115}L{x+102} 690Q{x+78} 726 {x+53} 690Z" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-width="3"/><path d="M{x+53} 652H{x+103}" stroke="{accent}" stroke-width="10" stroke-opacity=".7"/>')
            p.append(f'<rect x="1200" y="150" width="520" height="260" rx="10" fill="#071319" stroke="{accent}" stroke-width="5"/><path d="M1235 320L1300 260L1360 300L1430 220L1500 272L1570 205L1670 290" fill="none" stroke="{accent}" stroke-width="7"/>')
        elif kind=="finance":
            p.append(f'<rect x="110" y="150" width="790" height="310" rx="16" fill="#06131b" stroke="{accent}" stroke-opacity=".55" stroke-width="4"/>')
            for i in range(12):
                x=160+i*58; h=55+(i*47)%180
                p.append(f'<rect x="{x}" y="{430-h}" width="31" height="{h}" rx="5" fill="{accent}" opacity="{.25+(i%4)*.14:.2f}"/>')
            p.append(f'<path d="M1100 455L1180 405L1260 430L1340 310L1420 345L1500 250L1580 295L1700 180" fill="none" stroke="{accent}" stroke-width="8"/><path d="M1100 455H1730M1100 180V455" fill="none" stroke="{accent}" stroke-opacity=".4" stroke-width="3"/>')
        elif kind=="server":
            for row in range(4):
                for col in range(7):
                    x=100+col*245; y=150+row*175
                    p.append(f'<rect x="{x}" y="{y}" width="205" height="140" rx="8" fill="#08151e" stroke="{accent}" stroke-opacity=".5" stroke-width="4"/>')
                    for j in range(5): p.append(f'<rect x="{x+22+j*31}" y="{y+35}" width="16" height="8" rx="3" fill="{accent}" opacity="{.35+(j%3)*.2:.2f}"/>')
                    p.append(f'<path d="M{x+22} {y+72}H{x+180}M{x+22} {y+101}H{x+146}" stroke="{bottom}" stroke-width="7"/>')
        elif kind=="classroom":
            p.append(f'<rect x="740" y="170" width="960" height="365" rx="8" fill="#193b35" stroke="{accent}" stroke-opacity=".45" stroke-width="7"/><path d="M830 265H1260M830 335H1110M1285 265H1590M1285 335H1480" stroke="#d9eee0" stroke-width="9" stroke-opacity=".68"/>')
            for x in [180,430,680,930,1180,1430,1680]: p.append(f'<path d="M{x} 805V945H{x+180}V805" fill="{bottom}" stroke="{accent}" stroke-opacity=".3" stroke-width="4"/>')
        elif kind=="museum":
            for i in range(5):
                x=100+i*365; y=190+(i%2)*32
                p.append(f'<rect x="{x}" y="{y}" width="260" height="340" fill="#171821" stroke="{accent}" stroke-width="15" stroke-opacity=".65"/><rect x="{x+24}" y="{y+24}" width="212" height="292" fill="{bottom}"/><circle cx="{x+130}" cy="{y+126}" r="58" fill="{accent}" fill-opacity=".5"/><path d="M{x+45} {y+260}L{x+130} {y+180}L{x+216} {y+270}" fill="none" stroke="#e5d2b1" stroke-width="7"/>')
        elif kind=="factory":
            for i in range(7):
                x=i*300
                p.append(f'<path d="M{x} 150L{x+150} 80L{x+300} 150V680H{x}Z" fill="{bottom}" fill-opacity=".3" stroke="{accent}" stroke-opacity=".28" stroke-width="5"/>')
            for i in range(4):
                x=130+i*430; y=680-i%2*40
                p.append(f'<rect x="{x}" y="{y}" width="230" height="180" fill="{bottom}" stroke="{accent}" stroke-width="4" stroke-opacity=".45"/><path d="M{x+15} {y+20}L{x+215} {y+160}M{x+215} {y+20}L{x+15} {y+160}" stroke="{accent}" stroke-opacity=".2" stroke-width="4"/>')
        elif kind=="product":
            p.append(f'<path d="M960 130L460 790H1460Z" fill="url(#glow)" opacity=".35"/><ellipse cx="960" cy="845" rx="360" ry="76" fill="{bottom}" stroke="{accent}" stroke-width="6" stroke-opacity=".65"/><path d="M740 840V670Q740 620 800 620H1120Q1180 620 1180 670V840Z" fill="{top}" stroke="{accent}" stroke-width="5" stroke-opacity=".8"/>')
        elif kind=="food":
            p.append(f'<rect y="730" width="1920" height="350" fill="{bottom}" stroke="{accent}" stroke-opacity=".25" stroke-width="4"/>')
            for i,(x,y,r,col) in enumerate([(350,660,92,"#d95f45"),(670,630,68,"#e8b64b"),(1020,670,102,"#5c9a61"),(1380,640,80,"#d88a4b"),(1610,700,54,"#c95850")]):
                p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity=".8" stroke="#f8dfac" stroke-width="5"/><circle cx="{x}" cy="{y}" r="{r*.58}" fill="#f9d7a0" fill-opacity=".42"/>')
        elif kind=="castle":
            for x,w,h in [(120,240,470),(420,290,600),(820,270,690),(1240,280,560),(1580,210,430)]:
                p.append(f'<rect x="{x}" y="{900-h}" width="{w}" height="{h}" fill="{bottom}" stroke="{accent}" stroke-opacity=".38" stroke-width="5"/><path d="M{x-20} {900-h}L{x+w/2} {820-h}L{x+w+20} {900-h}Z" fill="{top}"/>')
        elif kind=="gaming":
            for i in range(5):
                x=170+i*345; y=285+(i%2)*45
                p.append(f'<rect x="{x}" y="{y}" width="220" height="510" rx="24" fill="#0b0b18" stroke="{accent}" stroke-width="7"/><rect x="{x+20}" y="{y+35}" width="180" height="220" rx="12" fill="{bottom}" stroke="{accent}" stroke-opacity=".55" stroke-width="4"/><path d="M{x+45} {y+150}L{x+85} {y+100}L{x+120} {y+175}L{x+172} {y+90}" fill="none" stroke="{accent}" stroke-width="8"/>')
        elif kind in {"cyber","network"}:
            nodes=[]
            for i in range(30):
                x=(i*163+79)%1850+35; y=(i*137+53)%1010+35; nodes.append((x,y))
            for i,(x,y) in enumerate(nodes):
                for x2,y2 in nodes[i+1:i+4]: p.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{accent}" stroke-opacity=".12" stroke-width="3"/>')
                p.append(f'<circle cx="{x}" cy="{y}" r="{5+i%4*2}" fill="{accent}" opacity=".52"/>')
        elif kind=="map":
            for i in range(18):
                x=80+i*91; y=430+(i%5)*47
                p.append(f'<path d="M{x-260} {y}C{x-160} {y-230} {x+90} {y-240} {x+200} {y-35}S{x+320} {y+220} {x+150} {y+300}S{x-170} {y+250} {x-260} {y}" fill="none" stroke="{accent}" stroke-opacity=".2" stroke-width="4"/>')
            p.append('<path d="M220 840C430 730 500 630 720 660S1100 440 1330 480S1600 240 1710 250" fill="none" stroke="#fa8f64" stroke-width="10" stroke-dasharray="22 18"/>')
        elif kind=="sports":
            p.append(f'<path d="M0 260Q960 100 1920 260V600Q960 440 0 600Z" fill="{bottom}" opacity=".72"/>')
            for i in range(8): p.append(f'<path d="M0 {310+i*38}Q960 {160+i*38} 1920 {310+i*38}" fill="none" stroke="{accent}" stroke-opacity=".22" stroke-width="8"/>')
            p.append(f'<path d="M140 1070V820Q140 690 280 690H1640Q1780 690 1780 820V1070M960 690V1080M420 690V900H1500V690" fill="none" stroke="{accent}" stroke-opacity=".58" stroke-width="6"/>')
        elif kind=="horror":
            for i in range(7):
                x=100+i*285; h=200+(i*89)%310
                p.append(f'<path d="M{x} 790V{790-h}L{x+90} {730-h}L{x+180} {790-h}V790Z" fill="#11131b" stroke="{accent}" stroke-opacity=".18" stroke-width="4"/>')
                p.append(f'<rect x="{x+60}" y="{820-h}" width="25" height="70" fill="{accent}" opacity=".25"/><rect x="{x+110}" y="{820-h}" width="25" height="70" fill="{accent}" opacity=".18"/>')
        else:
            p.append(f'<rect x="130" y="160" width="1660" height="625" rx="24" fill="{bottom}" fill-opacity=".3" stroke="{accent}" stroke-opacity=".3" stroke-width="5"/><path d="M130 785H1790" stroke="{accent}" stroke-opacity=".4" stroke-width="6"/>')
    elif kind=="underwater":
        p.append(f'<path d="M0 0H1920V700Q960 810 0 700Z" fill="{top}" opacity=".28"/>')
        for i in range(24):
            x=(i*131+25)%1920; y=(i*113+65)%890; r=4+(i%7)*4
            p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#b6f6f4" stroke-opacity=".25" stroke-width="3"/>')
        for i in range(9):
            x=i*240; p.append(f'<path d="M{x} 1080Q{x-30} 850 {x+35} 740Q{x+90} 920 {x+120} 1080" fill="none" stroke="#56cbb8" stroke-opacity=".45" stroke-width="10"/>')
        for i in range(8):
            x=i*245+80; y=350+(i%3)*80
            p.append(f'<path d="M{x-55} {y}Q{x} {y-42} {x+55} {y}Q{x} {y+42} {x-55} {y}Z" fill="{accent}" opacity=".35"/><circle cx="{x+27}" cy="{y-4}" r="4" fill="#ecffff"/>')
    # Subtle original particles add texture without replacing detailed scene art with a flat gradient.
    for i in range(100):
        x=(i*167+29)%1920; y=(i*113+17)%1080
        p.append(f'<circle cx="{x}" cy="{y}" r="{1+i%3}" fill="#fff" opacity="{.025+(i%5)*.009:.3f}"/>')
    p.append(f'<rect x="18" y="18" width="1884" height="1044" fill="none" stroke="{accent}" stroke-opacity=".12" stroke-width="2"/>')
    return svg_doc("".join(p),defs)

def overlay_svg(name):
    defs='<linearGradient id="leak" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ff5b56" stop-opacity=".28"/><stop offset=".32" stop-color="#ffbd66" stop-opacity=".13"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient><radialGradient id="vign"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient><pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.5" fill="#fff" fill-opacity=".22"/></pattern><pattern id="lines" width="1" height="7" patternUnits="userSpaceOnUse"><rect width="1" height="2" fill="#fff" fill-opacity=".14"/></pattern><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="13"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .15"/></feComponentTransfer></filter>'
    p=[]
    if name=="film-grain": p.append('<rect width="1920" height="1080" filter="url(#noise)" opacity=".2"/>')
    elif name=="scanlines": p.append('<rect width="1920" height="1080" fill="url(#lines)" opacity=".62"/>')
    elif name=="halftone": p.append('<rect width="1920" height="1080" fill="url(#dots)" opacity=".65"/>')
    elif name in {"light-leak","film-burn","rainbow-prism"}:
        p.append('<rect width="1920" height="1080" fill="url(#leak)"/>')
        if name=="film-burn": p.append('<ellipse cx="130" cy="530" rx="620" ry="760" fill="#ff784c" opacity=".21"/><ellipse cx="1810" cy="540" rx="330" ry="720" fill="#ffcf7a" opacity=".15"/>')
        if name=="rainbow-prism": p.append('<path d="M-100 0L400 0L1300 1080H820Z" fill="#71b8ff" opacity=".055"/><path d="M250 0H570L1510 1080H1220Z" fill="#fd8eda" opacity=".06"/><path d="M1000 0H1250L1920 600V800Z" fill="#83f1ce" opacity=".07"/>')
    elif name in {"vignette","corner-vignette"}: p.append('<rect width="1920" height="1080" fill="url(#vign)"/>')
    elif name=="letterbox": p.append('<rect width="1920" height="110" fill="#000"/><rect y="970" width="1920" height="110" fill="#000"/>')
    elif name=="film-gate":
        p.append('<rect x="30" y="30" width="1860" height="1020" fill="none" stroke="#f5f0e4" stroke-opacity=".42" stroke-width="4"/>')
        for x in range(65,1880,95): p.append(f'<rect x="{x}" y="48" width="16" height="32" rx="4" fill="#f5f0e4" opacity=".65"/><rect x="{x}" y="1000" width="16" height="32" rx="4" fill="#f5f0e4" opacity=".65"/>')
    elif name in {"dust","embers","bokeh","sparkles","snow","confetti"}:
        count=210 if name in {"dust","bokeh"} else 160
        for i in range(count):
            x=(i*137+53)%1920; y=(i*191+31)%1080
            if name=="bokeh":
                r=13+(i%7)*8; p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#f6dcb0" stroke-opacity=".12" stroke-width="4"/>')
            elif name=="sparkles":
                r=5+(i%5)*2; p.append(f'<path d="M{x} {y-r*2}V{y+r*2}M{x-r*2} {y}H{x+r*2}" stroke="#ffe9b7" stroke-opacity=".35" stroke-width="2"/>')
            elif name=="snow":
                p.append(f'<circle cx="{x}" cy="{y}" r="{1+i%5}" fill="#edf8ff" opacity=".62"/>')
            elif name=="confetti":
                rot=(i*19)%360; col=["#ffcc70","#70e7d3","#ff7f98","#b4a1ff"][i%4]
                p.append(f'<rect x="{x}" y="{y}" width="{5+i%8}" height="{12+i%15}" rx="2" fill="{col}" opacity=".25" transform="rotate({rot} {x} {y})"/>')
            else:
                col="#ffb86c" if name=="embers" else "#f8e9c8"; r=1+(i%5)*.65
                p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="{.1+(i%7)*.035:.2f}"/>')
    elif name=="rain":
        for i in range(250):
            x=(i*97+31)%1920; y=(i*83+17)%1080; length=22+(i%5)*10
            p.append(f'<path d="M{x} {y}l-9 {length}" stroke="#bfe3f4" stroke-opacity="{.11+(i%4)*.04:.2f}" stroke-width="{1+i%2}"/>')
    elif name=="speed-lines":
        for i in range(46):
            y=(i*37+13)%1080; x=(i*139)%1150
            p.append(f'<path d="M{x} {y}L{x+350+(i%5)*105} {y-25+(i%4)*18}" stroke="#fff" stroke-opacity="{.035+(i%4)*.025:.2f}" stroke-width="{2+i%3}"/>')
    elif name=="topographic":
        for i in range(20):
            x=80+i*91; y=430+(i%5)*47
            p.append(f'<path d="M{x-260} {y}C{x-160} {y-230} {x+90} {y-240} {x+200} {y-35}S{x+320} {y+220} {x+150} {y+300}S{x-170} {y+250} {x-260} {y}" fill="none" stroke="#d2e5c4" stroke-opacity=".14" stroke-width="3"/>')
    elif name in {"blueprint","chart-grid","map-graticule"}:
        step=80 if name=="blueprint" else 120 if name=="chart-grid" else 160
        color="#89dff3" if name!="map-graticule" else "#e8dcc1"
        for x in range(0,1921,step): p.append(f'<path d="M{x} 0V1080" stroke="{color}" stroke-opacity=".12" stroke-width="2"/>')
        for y in range(0,1081,step): p.append(f'<path d="M0 {y}H1920" stroke="{color}" stroke-opacity=".12" stroke-width="2"/>')
    elif name=="starfield":
        for i in range(320): p.append(f'<circle cx="{(i*157+17)%1920}" cy="{(i*89+41)%1080}" r="{.8+(i%4)*.65}" fill="#eaf0ff" opacity="{.18+(i%5)*.12:.2f}"/>')
    elif name in {"data-network","radar"}:
        if name=="radar":
            p.append('<circle cx="960" cy="540" r="130" fill="none" stroke="#79f0d1" stroke-opacity=".24" stroke-width="3"/><circle cx="960" cy="540" r="260" fill="none" stroke="#79f0d1" stroke-opacity=".22" stroke-width="3"/><circle cx="960" cy="540" r="390" fill="none" stroke="#79f0d1" stroke-opacity=".18" stroke-width="3"/><path d="M570 540H1350M960 150V930M685 265L1235 815M685 815L1235 265" stroke="#79f0d1" stroke-opacity=".14" stroke-width="3"/><path d="M960 540L1215 280A365 365 0 0 1 1320 560Z" fill="#79f0d1" fill-opacity=".09"/>')
        else:
            nodes=[((i*163+79)%1850+35,(i*137+53)%1010+35) for i in range(40)]
            for i,(x,y) in enumerate(nodes):
                for x2,y2 in nodes[i+1:i+4]: p.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#70e6db" stroke-opacity=".14" stroke-width="2"/>')
                p.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#70e6db" opacity=".7"/>')
    elif name in {"glitch","vhs","screen-reflection-bands"}:
        for i in range(45):
            y=(i*73+13)%1080; x=(i*131)%1500; w=80+(i%6)*73
            col="#ff4fb5" if i%2 else "#5de9ff"
            p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{2+i%8}" fill="{col}" opacity=".14"/>')
        if name=="vhs": p.append('<path d="M0 180H1920M0 526H1920M0 802H1920" stroke="#8fd8ff" stroke-opacity=".15" stroke-width="5"/>')
        if name=="screen-reflection-bands": p.append('<path d="M0 100L1920 350M0 260L1920 510M0 420L1920 670" stroke="#fff" stroke-opacity=".065" stroke-width="90"/>')
    elif name in {"subtitle-safe","focus-frame","corner-hud","measurement-rulers"}:
        if name=="subtitle-safe": p.append('<rect x="100" y="80" width="1720" height="920" fill="none" stroke="#75ff9b" stroke-opacity=".38" stroke-width="4" stroke-dasharray="18 14"/><rect x="180" y="780" width="1560" height="210" fill="#000" fill-opacity=".035" stroke="#75ff9b" stroke-opacity=".35" stroke-width="3" stroke-dasharray="12 10"/>')
        elif name=="focus-frame": p.append('<rect x="110" y="90" width="1700" height="900" fill="none" stroke="#f5f1e9" stroke-opacity=".72" stroke-width="4"/><path d="M110 210V90H230M1690 90H1810V210M110 870V990H230M1690 990H1810V870" stroke="#f5f1e9" stroke-width="12" fill="none"/>')
        elif name=="corner-hud": p.append('<path d="M160 50H50V160M1760 50H1870V160M50 920V1030H160M1760 1030H1870V920" fill="none" stroke="#b6d6ff" stroke-opacity=".55" stroke-width="4"/>')
        else:
            for x in range(0,1920,100): p.append(f'<path d="M{x} 15V45M{x} 1035V1065" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>')
            for y in range(0,1080,100): p.append(f'<path d="M15 {y}H45M1875 {y}H1905" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>')
    elif name=="waveform":
        coords=[f'{i*19.2:.1f},{540+(((i*71)%131)-65)*(.6+(i%7)*.08):.1f}' for i in range(101)]
        p.append(f'<polyline points="{" ".join(coords)}" fill="none" stroke="#83f0df" stroke-opacity=".6" stroke-width="5"/>')
    elif name=="paper-texture":
        p.append('<rect width="1920" height="1080" fill="#e6d6b7" fill-opacity=".09"/>')
        for i in range(150): p.append(f'<path d="M{(i*173+23)%1920} {(i*97+19)%1080}h{18+(i%21)*5}" stroke="#f7e8cd" stroke-opacity=".1" stroke-width="2"/>')
    elif name=="soft-fog":
        for i in range(12):
            y=280+i*68
            p.append(f'<ellipse cx="{180+(i*223)%1560}" cy="{y}" rx="{400+(i%4)*130}" ry="{45+(i%3)*20}" fill="#d8e5e0" opacity=".028"/>')
    elif name=="audio-waveform":
        p.append('<path d="M0 540H120L160 500L200 580L245 430L300 650L360 455L420 600L480 540H620L670 485L710 565L770 410L825 675L890 470L940 540H1100L1150 495L1200 590L1260 440L1320 640L1380 510L1430 540H1920" fill="none" stroke="#83f0df" stroke-opacity=".5" stroke-width="6"/>')
    elif name in {"cctv-timestamp","news-ticker","comic-panels","torn-paper","lens-flare","blueprint-dimensions","tracking-markers","dust-scratches","glow-bloom","thermal-map","tape-label","split-screen-divider","map-route","spectrum-bars","rain-on-glass","underwater-caustics","film-frame-counter","focus-pull","caution-stripes","vertical-safe-area"}:
        if name=="cctv-timestamp":
            p.append('<rect x="54" y="48" width="470" height="74" rx="5" fill="#000" fill-opacity=".38"/><text x="78" y="94" font-size="31" font-family="monospace" fill="#e9f3e9">CAM 03 · REC 00:14:28</text><circle cx="483" cy="82" r="9" fill="#ff594f"/><path d="M55 145H145V172M55 145V235M1865 145H1775V172M1865 145V235" fill="none" stroke="#c9e1d5" stroke-opacity=".55" stroke-width="4"/>')
        elif name=="news-ticker":
            p.append('<rect y="900" width="1920" height="180" fill="#07121d" fill-opacity=".82"/><rect y="900" width="220" height="52" fill="#e84e54"/><text x="38" y="936" font-family="Arial,sans-serif" font-size="26" font-weight="700" fill="#fff">UPDATE</text><path d="M0 900H1920M0 1075H1920" stroke="#f5f5f5" stroke-opacity=".25" stroke-width="3"/>')
        elif name=="comic-panels":
            p.append('<rect x="55" y="55" width="570" height="450" fill="none" stroke="#fff" stroke-width="12"/><rect x="650" y="55" width="1215" height="450" fill="none" stroke="#fff" stroke-width="12"/><rect x="55" y="530" width="880" height="490" fill="none" stroke="#fff" stroke-width="12"/><rect x="960" y="530" width="905" height="490" fill="none" stroke="#fff" stroke-width="12"/>')
        elif name=="torn-paper":
            p.append('<path d="M0 72L88 52L164 78L260 55L375 82L498 48L620 71L760 50L875 79L1000 51L1125 81L1260 52L1380 78L1510 48L1630 76L1750 52L1920 70V180L1810 195L1690 173L1570 198L1440 175L1300 196L1160 170L1020 198L880 175L740 196L600 171L470 197L330 174L190 200L60 176L0 190Z" fill="#eee1c8" fill-opacity=".18"/>')
        elif name=="lens-flare":
            p.append('<path d="M0 390L1920 690" stroke="#ffe7b0" stroke-opacity=".16" stroke-width="130"/><circle cx="1340" cy="600" r="74" fill="#fff2c1" fill-opacity=".035"/><circle cx="580" cy="480" r="38" fill="#87e7ff" fill-opacity=".06"/>')
        elif name=="blueprint-dimensions":
            p.append('<path d="M210 230H1640M210 210V250M1640 210V250M210 230L235 220M210 230L235 240M1640 230L1615 220M1640 230L1615 240M360 330V820M340 330H380M340 820H380" fill="none" stroke="#9deaff" stroke-width="3" stroke-opacity=".65"/><text x="925" y="210" fill="#9deaff" font-family="monospace" font-size="28" text-anchor="middle">DIMENSION / SCALE</text>')
        elif name=="tracking-markers":
            for x,y in [(160,160),(960,160),(1760,160),(160,920),(960,920),(1760,920)]:
                p.append(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="#65f5cb" stroke-opacity=".75" stroke-width="3"/><path d="M{x-40} {y}H{x+40}M{x} {y-40}V{y+40}" stroke="#65f5cb" stroke-opacity=".6" stroke-width="3"/>')
        elif name=="dust-scratches":
            for i in range(240):
                x=(i*127+19)%1920; y=(i*83+47)%1080; h=6+(i%49)*2
                p.append(f'<path d="M{x} {y}l{(i%3)-1} {h}" stroke="#e4dbc8" stroke-opacity="{.04+(i%5)*.018:.3f}" stroke-width="{1+i%2}"/>')
        elif name=="glow-bloom":
            p.append('<ellipse cx="960" cy="400" rx="700" ry="430" fill="#fff6cc" fill-opacity=".055"/>')
        elif name=="thermal-map":
            p.append('<rect width="1920" height="1080" fill="#e3435f" fill-opacity=".035"/><path d="M0 220Q450 50 800 300T1500 220T1920 330V850Q1330 750 900 900T0 810Z" fill="#ffc35a" fill-opacity=".07"/><ellipse cx="1180" cy="520" rx="360" ry="230" fill="#4ce2cd" fill-opacity=".06"/>')
        elif name=="tape-label":
            p.append('<path d="M170 120H850L890 175L850 230H170L130 175Z" fill="#e8d4a9" fill-opacity=".72" stroke="#9e865d" stroke-opacity=".4" stroke-width="3"/><text x="510" y="190" fill="#302b23" font-family="monospace" text-anchor="middle" font-size="36">ARCHIVE / DATE / REEL</text>')
        elif name=="split-screen-divider":
            p.append('<rect x="952" y="0" width="16" height="1080" fill="#fff" fill-opacity=".72"/><circle cx="960" cy="540" r="46" fill="#111" fill-opacity=".55" stroke="#fff" stroke-opacity=".8" stroke-width="3"/><path d="M950 522L970 540L950 558" fill="none" stroke="#fff" stroke-width="5"/>')
        elif name=="map-route":
            p.append('<path d="M220 850C460 700 430 450 730 500S1060 710 1260 430S1510 260 1710 180" fill="none" stroke="#ffb467" stroke-width="10" stroke-dasharray="18 18" stroke-linecap="round"/><circle cx="220" cy="850" r="24" fill="#70e5cf"/><circle cx="1710" cy="180" r="24" fill="#ffb467"/>')
        elif name=="spectrum-bars":
            for i in range(86):
                x=i*22+14; h=35+((i*47+13)%230)
                p.append(f'<rect x="{x}" y="{540-h/2}" width="10" height="{h}" rx="5" fill="#8be7dc" fill-opacity="{.18+(i%5)*.1:.2f}"/>')
        elif name=="rain-on-glass":
            for i in range(90):
                x=(i*173+33)%1920; y=(i*97+21)%1080; r=5+(i%9)*2
                p.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*1.8}" fill="#a8e7ff" fill-opacity=".06" stroke="#d7f5ff" stroke-opacity=".19" stroke-width="2"/>')
        elif name=="underwater-caustics":
            for i in range(22):
                x=(i*139+10)%1920; y=(i*71+20)%1080
                p.append(f'<path d="M{x-150} {y}Q{x-75} {y-80} {x} {y}T{x+150} {y}" fill="none" stroke="#b9fff3" stroke-opacity=".13" stroke-width="18"/>')
        elif name=="film-frame-counter":
            p.append('<rect x="70" y="45" width="260" height="78" fill="#000" fill-opacity=".55" stroke="#f5eee0" stroke-opacity=".5" stroke-width="2"/><text x="200" y="98" text-anchor="middle" font-family="monospace" font-size="35" fill="#fff">FRAME 0042</text>')
        elif name=="focus-pull":
            p.append('<path d="M120 960A900 900 0 0 1 1800 960" fill="none" stroke="#e4eef3" stroke-opacity=".35" stroke-width="4"/><path d="M250 900V930M390 875V905M530 850V880M670 832V862M810 822V852M950 820V850M1090 822V852M1230 832V862M1370 850V880M1510 875V905M1650 900V930" stroke="#e4eef3" stroke-opacity=".35" stroke-width="4"/><text x="960" y="1000" fill="#e4eef3" fill-opacity=".6" font-size="24" text-anchor="middle">FOCUS DISTANCE / MARKS</text>')
        elif name=="caution-stripes":
            for i in range(-1200,2400,120):
                p.append(f'<path d="M{i} 1080L{i+500} 0H{i+560}L{i+60} 1080Z" fill="#f4c84a" fill-opacity=".065"/>')
            p.append('<path d="M0 0H1920V30H0ZM0 1050H1920V1080H0Z" fill="#f4c84a" fill-opacity=".45"/>')
        else:
            p.append('<rect x="540" y="40" width="840" height="1000" fill="none" stroke="#76f1cf" stroke-opacity=".42" stroke-width="4" stroke-dasharray="18 14"/><rect x="615" y="120" width="690" height="840" fill="none" stroke="#76f1cf" stroke-opacity=".2" stroke-width="2" stroke-dasharray="8 12"/><text x="960" y="1020" text-anchor="middle" font-size="22" fill="#76f1cf">9:16 SAFE AREA</text>')
    else: p.append('<rect width="1920" height="1080" fill="url(#vign)"/>')
    return svg_doc("".join(p),defs)

def icon_svg(drawing):
    css='<style>.line{stroke:currentColor;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;fill:none}</style>'
    return svg_doc(f'<g class="line">{drawing}</g>',css,width=64,height=64)

def infographic_svg(asset_id,title,index):
    accent=["#e6ad6c","#5dd7ca","#9faeff","#e985a2"][index%4]
    bg=["#1a1b25","#10232b","#292035","#20292a"][index%4]
    defs='<style>text{font-family:Arial,sans-serif;fill:#f4f0e6}.muted{fill:#b8c0cb}.line{stroke:#cbd1db;stroke-opacity:.35;stroke-width:4;fill:none}</style>'
    p=[f'<rect x="56" y="56" width="1808" height="968" rx="28" fill="{bg}" stroke="{accent}" stroke-opacity=".5" stroke-width="4"/><rect x="105" y="110" width="14" height="120" rx="7" fill="{accent}"/>',
       f'<text x="155" y="178" font-size="44" font-weight="700">{html.escape(title.upper())}</text>',
       '<text x="155" y="220" class="muted" font-size="22">EDIT PLACEHOLDERS · INCLUDE SOURCES WHEN NEEDED</text>']
    if asset_id in {"bar-chart","line-chart","stat-number"}:
        for y in [350,480,610,740]: p.append(f'<path d="M180 {y}H1740" class="line" stroke-dasharray="6 16"/>')
        if asset_id=="line-chart":
            p.append(f'<path d="M220 740L460 670L700 710L940 510L1180 555L1420 375L1680 410" fill="none" stroke="{accent}" stroke-width="12"/>')
        elif asset_id=="stat-number": p.append(f'<text x="960" y="590" text-anchor="middle" font-size="225" font-weight="700" fill="{accent}">00.0%</text><text x="960" y="680" text-anchor="middle" font-size="38">SOURCE / PERIOD / UNITS</text>')
        else:
            for i in range(7):
                h=120+((i*73+index*29)%360); x=260+i*215
                p.append(f'<rect x="{x}" y="{800-h}" width="115" height="{h}" rx="10" fill="{accent}" opacity="{.35+(i%4)*.15:.2f}"/><text x="{x+57}" y="850" font-size="21" text-anchor="middle">ITEM {i+1}</text>')
    elif asset_id in {"timeline","vertical-timeline","process-steps","recipe-steps","chapter-divider"}:
        if asset_id=="vertical-timeline":
            p.append(f'<path d="M410 330V850" stroke="{accent}" stroke-width="9"/>')
            for i in range(5):
                y=350+i*120
                p.append(f'<circle cx="410" cy="{y}" r="20" fill="{accent}"/><rect x="470" y="{y-30}" width="880" height="62" rx="12" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-opacity=".35" stroke-width="2"/><text x="510" y="{y+10}" font-size="25">DATE / MILESTONE {i+1}</text>')
        else:
            count=4 if asset_id in {"process-steps","recipe-steps"} else 5; span=1500/(count-1)
            p.append(f'<path d="M250 570H1670" stroke="{accent}" stroke-width="8"/>')
            for i in range(count):
                x=250+i*span
                p.append(f'<circle cx="{x}" cy="570" r="38" fill="{bg}" stroke="{accent}" stroke-width="8"/><text x="{x}" y="585" text-anchor="middle" font-size="34" font-weight="700">{i+1}</text><text x="{x}" y="660" text-anchor="middle" font-size="24">STEP / DATE</text><rect x="{x-115}" y="715" width="230" height="78" rx="12" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".35" stroke-width="2"/>')
    elif asset_id in {"comparison","pros-cons"}:
        for i in range(2):
            x=145+i*830; col="#68d9bc" if i==0 else "#ed9e88"
            p.append(f'<rect x="{x}" y="310" width="735" height="540" rx="18" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".55" stroke-width="3"/><text x="{x+42}" y="375" font-size="34" fill="{col}">{"OPTION A" if i==0 else "OPTION B"}</text>')
            for j in range(5):
                y=440+j*74; p.append(f'<circle cx="{x+58}" cy="{y}" r="10" fill="{col}"/><path d="M{x+90} {y}H{x+620-j*18}" stroke="#e8e6df" stroke-opacity=".4" stroke-width="8" stroke-linecap="round"/>')
    elif asset_id in {"funnel","pyramid"}:
        for i in range(4):
            y=330+i*135; w=1420-i*250; x=(1920-w)/2
            if asset_id=="pyramid": p.append(f'<path d="M{960-w/2} {y+108}L960 {y-30}L{960+w/2} {y+108}Z" fill="{accent}" fill-opacity="{.12+i*.09:.2f}" stroke="{accent}" stroke-opacity=".65" stroke-width="4"/>')
            else: p.append(f'<path d="M{x} {y}H{x+w}L{x+w-85} {y+105}H{x+85}Z" fill="{accent}" fill-opacity="{.14+i*.1:.2f}" stroke="{accent}" stroke-opacity=".65" stroke-width="4"/>')
            p.append(f'<text x="960" y="{y+64}" text-anchor="middle" font-size="27">LEVEL {i+1} / LABEL</text>')
    elif asset_id=="decision-tree":
        p.append(f'<rect x="760" y="310" width="400" height="95" rx="16" fill="{accent}" fill-opacity=".18" stroke="{accent}" stroke-width="4"/><text x="960" y="368" text-anchor="middle" font-size="27">QUESTION</text><path d="M960 405V495H480V555M960 495H1440V555" class="line"/>')
        for x,label in [(480,"YES / PATH A"),(1440,"NO / PATH B")]:
            p.append(f'<rect x="{x-180}" y="555" width="360" height="100" rx="14" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-width="3"/><text x="{x}" y="615" text-anchor="middle" font-size="24">{label}</text><path d="M{x} 655V715" class="line"/><rect x="{x-220}" y="715" width="440" height="100" rx="14" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".2" stroke-width="3"/><text x="{x}" y="775" text-anchor="middle" font-size="24">OUTCOME</text>')
    elif asset_id=="map-callout":
        p.append('<path d="M160 370Q330 220 520 380T890 380T1230 340T1700 400M100 610Q320 470 550 620T1000 610T1600 670" fill="none" stroke="#7ca78a" stroke-opacity=".45" stroke-width="12"/>')
        for x,y,label in [(300,350,"A"),(800,390,"B"),(1300,350,"C")]: p.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{accent}"/><rect x="{x-88}" y="{y-100}" width="176" height="56" rx="10" fill="{bg}" stroke="{accent}" stroke-width="3"/><text x="{x}" y="{y-63}" text-anchor="middle" font-size="24">{label} · PLACE</text>')
        p.append('<path d="M300 350Q500 550 800 390T1300 350" fill="none" stroke="#ed9874" stroke-width="6" stroke-dasharray="14 15"/>')
    elif asset_id in {"quote-card","source-card"}:
        p.append(f'<text x="210" y="410" font-size="110" fill="{accent}">“</text><text x="290" y="495" font-size="38">REPLACE WITH SHORT VERIFIED { "QUOTE" if asset_id=="quote-card" else "SOURCE / EVIDENCE" }</text><path d="M300 575H1580" stroke="{accent}" stroke-opacity=".65" stroke-width="4"/><text x="310" y="650" class="muted" font-size="28">AUTHOR / PUBLISHER</text><text x="310" y="700" class="muted" font-size="25">DATE · LINK · CONTEXT</text>')
    elif asset_id in {"definition-card","equation-card"}:
        p.append(f'<rect x="165" y="315" width="1590" height="435" rx="24" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".38" stroke-width="3"/><text x="235" y="420" font-size="48" font-weight="700">{"TERM / CONCEPT" if asset_id=="definition-card" else "FORMULA / EQUATION"}</text><path d="M235 465H1660" stroke="{accent}" stroke-opacity=".35" stroke-width="3"/><text x="235" y="545" font-size="30" class="muted">PLAIN-LANGUAGE EXPLANATION / VARIABLE KEY</text><text x="235" y="620" font-size="24" class="muted">SOURCE / ASSUMPTIONS / UNITS</text>')
    elif asset_id in {"venn-diagram","cycle-diagram","scatter-plot","budget-breakdown","gantt-chart","before-after","scorecard","source-ledger","fact-check","roadmap"}:
        if asset_id=="venn-diagram":
            p.append(f'<circle cx="760" cy="555" r="235" fill="{accent}" fill-opacity=".18" stroke="{accent}" stroke-width="5"/><circle cx="1000" cy="555" r="235" fill="#80d7c8" fill-opacity=".18" stroke="#80d7c8" stroke-width="5"/><circle cx="880" cy="700" r="235" fill="#d99ab6" fill-opacity=".14" stroke="#d99ab6" stroke-width="5"/><text x="640" y="510" font-size="30">SET A</text><text x="1080" y="510" font-size="30">SET B</text><text x="855" y="850" font-size="30">SET C</text>')
        elif asset_id=="cycle-diagram":
            coords=[(960,350),(1330,555),(960,770),(590,555)]
            for i,(x,y) in enumerate(coords):
                nx,ny=coords[(i+1)%4]
                p.append(f'<path d="M{x} {y}Q{(x+nx)/2+35} {(y+ny)/2-35} {nx} {ny}" fill="none" stroke="{accent}" stroke-width="7" stroke-dasharray="12 10"/>')
                p.append(f'<circle cx="{x}" cy="{y}" r="92" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-width="4"/><text x="{x}" y="{y+10}" text-anchor="middle" font-size="25">STEP {i+1}</text>')
        elif asset_id=="scatter-plot":
            p.append(f'<path d="M260 310V840H1650M260 580H1650M260 420H1650" fill="none" stroke="#d6deea" stroke-opacity=".3" stroke-width="4"/>')
            for i in range(70):
                x=310+(i*173)%1280; y=760-((i*83+int((i*31)%9)*49)%410)
                p.append(f'<circle cx="{x}" cy="{y}" r="{5+i%5}" fill="{accent}" fill-opacity="{.4+(i%5)*.1:.2f}"/>')
        elif asset_id=="budget-breakdown":
            p.append(f'<circle cx="620" cy="580" r="230" fill="none" stroke="#fff" stroke-opacity=".1" stroke-width="72"/><circle cx="620" cy="580" r="230" fill="none" stroke="{accent}" stroke-width="72" stroke-dasharray="420 1025" transform="rotate(-90 620 580)"/><circle cx="620" cy="580" r="230" fill="none" stroke="#5dd7ca" stroke-width="72" stroke-dasharray="310 1135" stroke-dashoffset="-420" transform="rotate(-90 620 580)"/>')
            for i in range(4):
                y=395+i*115
                p.append(f'<rect x="1020" y="{y}" width="{480-i*55}" height="42" rx="10" fill="{accent}" fill-opacity="{.28+i*.14:.2f}"/><text x="1020" y="{y-14}" font-size="24">CATEGORY {i+1} · %</text>')
        elif asset_id=="gantt-chart":
            for i in range(6):
                y=340+i*85
                p.append(f'<text x="200" y="{y+32}" font-size="23">TASK {i+1}</text><path d="M470 {y+20}H1690" stroke="#fff" stroke-opacity=".13" stroke-width="2"/>')
                x=500+((i*173)%580); w=280+((i*97)%440)
                p.append(f'<rect x="{x}" y="{y}" width="{w}" height="42" rx="8" fill="{accent}" fill-opacity="{.35+(i%4)*.14:.2f}"/>')
        elif asset_id=="before-after":
            for i in range(2):
                x=150+i*830; col=accent if i==0 else "#5dd7ca"
                p.append(f'<rect x="{x}" y="330" width="730" height="430" rx="20" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="3"/><text x="{x+365}" y="395" text-anchor="middle" font-size="35">{"BEFORE" if i==0 else "AFTER"}</text><path d="M{x+55} 455H{x+675}M{x+55} 535H{x+595}M{x+55} 615H{x+630}" stroke="{col}" stroke-opacity=".55" stroke-width="10" stroke-linecap="round"/>')
        elif asset_id=="scorecard":
            for i,(label,value) in enumerate([("ACCURACY","00.0%"),("GROWTH","+00%"),("QUALITY","0.0 / 10")]):
                x=180+i*550
                p.append(f'<rect x="{x}" y="360" width="470" height="340" rx="24" fill="{accent}" fill-opacity=".1" stroke="{accent}" stroke-opacity=".5" stroke-width="3"/><text x="{x+235}" y="440" font-size="28" text-anchor="middle">{label}</text><text x="{x+235}" y="570" font-size="68" font-weight="700" text-anchor="middle" fill="{accent}">{value}</text><path d="M{x+55} 625H{x+415}" stroke="#fff" stroke-opacity=".18" stroke-width="4"/>')
        elif asset_id=="source-ledger":
            for i,label in enumerate(["CLAIM / STATEMENT","AUTHOR / ORGANIZATION","DATE / VERSION","SOURCE URL","LICENSE / ACCESS DATE"]):
                y=340+i*96
                p.append(f'<rect x="190" y="{y-38}" width="1540" height="72" rx="9" fill="{accent}" fill-opacity="{.12 if i%2==0 else .05}"/><text x="230" y="{y+7}" font-size="25">{label}</text><path d="M700 {y}H1670" stroke="#fff" stroke-opacity=".18" stroke-width="3"/>')
        elif asset_id=="fact-check":
            for i,(label,col) in enumerate([("CLAIM",accent),("EVIDENCE","#5dd7ca"),("VERDICT","#e985a2")]):
                x=170+i*560
                p.append(f'<rect x="{x}" y="400" width="460" height="330" rx="20" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="3"/><text x="{x+230}" y="465" text-anchor="middle" font-size="30">{label}</text><path d="M{x+50} 530H{x+410}M{x+50} 590H{x+375}M{x+50} 650H{x+330}" stroke="{col}" stroke-opacity=".45" stroke-width="8" stroke-linecap="round"/>')
        else:
            for i in range(5):
                x=260+i*330; y=500+(i%2)*120
                p.append(f'<circle cx="{x}" cy="{y}" r="32" fill="{accent}" fill-opacity=".22" stroke="{accent}" stroke-width="4"/><path d="M{x+35} {y}H{x+155}" stroke="{accent}" stroke-width="5"/><text x="{x}" y="{y+85}" text-anchor="middle" font-size="23">PHASE {i+1}</text>')
    else:
        for i in range(5):
            y=330+i*112
            p.append(f'<circle cx="230" cy="{y}" r="28" fill="{accent}" fill-opacity=".22" stroke="{accent}" stroke-width="3"/><text x="230" y="{y+10}" text-anchor="middle" font-size="28">{i+1}</text><text x="300" y="{y+10}" font-size="28">ITEM / SHORT EXPLANATION</text><path d="M300 {y+35}H1640" stroke="#e8e6df" stroke-opacity=".2" stroke-width="3"/>')
    p.append('<text x="960" y="970" text-anchor="middle" font-size="20" fill="#aeb8c6">TEMPLATE ONLY · REPLACE PLACEHOLDERS AND VERIFY SOURCES</text>')
    return svg_doc("".join(p),defs)

def generate_originals(root,index):
    for folder in ["backgrounds","overlays","icons","infographics"]: (root/"originals"/folder).mkdir(parents=True,exist_ok=True)
    for asset_id,palette,kind in PALETTES:
        path=root/"originals/backgrounds"/(asset_id+".svg")
        write_text(path,make_background(asset_id,palette,kind))
        index.append({"id":asset_id,"path":path.relative_to(root).as_posix(),"type":"original-svg-background","category":kind,"license":CC0,"license_url":CC0_URL,"redistributable":True})
    for asset_id,title in OVERLAYS:
        path=root/"originals/overlays"/(asset_id+".svg")
        write_text(path,overlay_svg(asset_id))
        index.append({"id":asset_id,"path":path.relative_to(root).as_posix(),"type":"original-svg-overlay","description":title,"license":CC0,"license_url":CC0_URL,"transparent":True,"redistributable":True})
    for name,drawing in ICONS.items():
        path=root/"originals/icons"/(name+".svg")
        write_text(path,icon_svg(drawing))
        index.append({"id":name,"path":path.relative_to(root).as_posix(),"type":"original-svg-icon","license":CC0,"license_url":CC0_URL,"redistributable":True})
    for i,(asset_id,title) in enumerate(INFO):
        path=root/"originals/infographics"/(asset_id+".svg")
        write_text(path,infographic_svg(asset_id,title,i))
        index.append({"id":asset_id,"path":path.relative_to(root).as_posix(),"type":"original-svg-infographic-template","title":title,"license":CC0,"license_url":CC0_URL,"redistributable":True,"warning":"Replace placeholders and verify all data and sources before publishing."})
    from generate_sfx_library import generate_original_audio
    audio_count=generate_original_audio(root,index,CC0_URL)
    print("[Original SFX] generated",audio_count,"WAV files")

def safe_extract(blob,target,max_bytes=350*1024*1024):
    import io
    total=0; count=0; target=target.resolve()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        bad=z.testzip()
        if bad: raise RuntimeError("corrupt ZIP member: "+bad)
        for info in z.infolist():
            name=info.filename.replace("\\\\","/")
            pp=PurePosixPath(name); ext=Path(name).suffix.lower()
            if pp.is_absolute() or ".." in pp.parts: raise RuntimeError("unsafe ZIP path: "+name)
            if info.is_dir() or ext in DENIED or ext not in ALLOWED: continue
            total+=info.file_size
            if total>max_bytes: raise RuntimeError("pack extraction size limit exceeded")
            out=(target/Path(*pp.parts)).resolve()
            if target not in out.parents: raise RuntimeError("unsafe extraction destination")
            out.parent.mkdir(parents=True,exist_ok=True)
            with z.open(info) as src,out.open("wb") as dst: shutil.copyfileobj(src,dst)
            count+=1
    return count,total

def verify_kenney_license(page):
    try:
        data,_=request_bytes(page,timeout=35,limit=4*1024*1024)
        text=data.decode("utf-8","ignore")
        return "Creative Commons CC0" in text or "CC0 1.0 Universal" in text or "CC0-1.0" in text
    except Exception as e:
        print("[Kenney] page verification error:",page,str(e))
        return False

def download_kenney(root,index):
    import io
    report=[]
    max_archive=MAX_KENNEY_ZIP
    for source in KENNEY_GITHUB_REPOS:
        slug=source["slug"]
        page=f"https://github.com/KenneyNL/{slug}"
        archive_url=f"https://api.github.com/repos/KenneyNL/{slug}/zipball/main"
        row={"id":"kenney-github-"+slugify(slug),"title":source["title"],"provider":"Kenney / GitHub",
             "category":source["category"],"source_page":page,"archive_url":archive_url,
             "license":"CC0-1.0","license_url":CC0_URL,"license_evidence":source["evidence"]}
        try:
            blob,_=request_bytes(archive_url,timeout=70,limit=max_archive)
            if not blob.startswith(b"PK"):
                raise RuntimeError("GitHub did not return a ZIP archive")
            # Inspect official repository documentation before extracting any file.
            with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                corrupt=zf.testzip()
                if corrupt: raise RuntimeError("corrupt source ZIP member: "+corrupt)
                readmes=[]
                for info in zf.infolist():
                    basename=PurePosixPath(info.filename).name.lower()
                    if basename in {"readme.md","readme.txt","license.md","license.txt"} and not info.is_dir():
                        if info.file_size<=2*1024*1024:
                            try: readmes.append(zf.read(info).decode("utf-8","ignore").lower())
                            except Exception: pass
                documentation="\n".join(readmes)
                if "cc0" not in documentation or "licensed" not in documentation or "asset" not in documentation:
                    raise RuntimeError("repository README/license did not confirm CC0 for assets")
            dest=root/"third-party/kenney"/slugify(slug)
            extracted,unpacked=safe_extract(blob,dest,max_bytes=450*1024*1024)
            media_files=[p for p in dest.rglob("*") if p.is_file() and p.name!="SOURCE_AND_LICENSE.md"]
            if not media_files: raise RuntimeError("no allowed asset media files after safe extraction")
            write_text(dest/"SOURCE_AND_LICENSE.md",
                       f"# {source['title']} — Kenney\n\nOfficial repository: {page}\nArchive SHA-256: {hashlib.sha256(blob).hexdigest()}\nVerified documentation evidence: {source['evidence']}\nLicense: CC0 1.0 Universal — {CC0_URL}\nOnly approved media/document file types were extracted; executable and game logic files are intentionally omitted.\n")
            for path in sorted(p for p in dest.rglob("*") if p.is_file()):
                index.append({"id":f"kenney-{slugify(slug)}-{slugify(path.relative_to(dest).as_posix())}",
                              "path":path.relative_to(root).as_posix(),"type":"kenney-cc0-asset-file",
                              "provider":"Kenney / GitHub","parent_asset_id":"kenney-github-"+slugify(slug),
                              "category":source["category"],"source_page":page,"license":"CC0-1.0",
                              "license_url":CC0_URL,"license_evidence":source["evidence"],
                              "size_bytes":path.stat().st_size,"sha256":sha256_path(path),"redistributable":True})
            row.update(status="downloaded",file_count=len(media_files),unpacked_bytes=unpacked,
                       archive_sha256=hashlib.sha256(blob).hexdigest())
            print("[Kenney GitHub] OK:",slug,len(media_files),"files",unpacked,"bytes")
        except Exception as exc:
            row.update(status="failed",reason=str(exc))
            print("[Kenney GitHub] failed:",slug,str(exc))
        report.append(row); time.sleep(.3)
    # The separate official asset browser remains a useful discovery index. Do not guess
    # its current dynamic download endpoint for packs that are not present in GitHub.
    report.append({"id":"kenney-official-catalog","provider":"Kenney","status":"source_only",
                   "reason":"The main asset catalog uses a browser-driven download step. Additional packs are listed for future manual acquisition; no guessed direct download URL is used.",
                   "source_page":"https://kenney.nl/assets",
                   "packs_not_yet_mirrored":[x[0] for x in KENNEY]})
    return report


def choose_poly_file(tree,kind):
    if not isinstance(tree,dict): return None
    if kind=="hdris":
        block=tree.get("hdri",{})
        for res in ("1k","2k","4k","8k","16k","32k"):
            fmts=block.get(res,{}) if isinstance(block,dict) else {}
            for fmt in ("hdr","exr","jpg"):
                f=fmts.get(fmt) if isinstance(fmts,dict) else None
                if isinstance(f,dict) and f.get("url"): return f
        return None
    if kind=="models":
        # Prefer a Blender scene package and download its listed dependencies too.
        for fmt in ("blend","gltf","fbx","usd"):
            block=tree.get(fmt,{})
            if not isinstance(block,dict): continue
            for res in ("1k","2k","4k","8k","16k","32k"):
                fmts=block.get(res,{})
                f=fmts.get(fmt) if isinstance(fmts,dict) else None
                if isinstance(f,dict) and f.get("url"): return f
        return None
    return None

def choose_poly_texture_selection(tree):
    selected=[]
    for channel in ("Diffuse","nor_gl","nor_dx","rough","ao","disp","bump","metal"):
        block=tree.get(channel) if isinstance(tree,dict) else None
        if not isinstance(block,dict): continue
        item=None
        for res in ("1k","2k","4k","8k"):
            fmts=block.get(res,{})
            if not isinstance(fmts,dict): continue
            for fmt in ("jpg","png","exr"):
                candidate=fmts.get(fmt)
                if isinstance(candidate,dict) and candidate.get("url"):
                    item=candidate
                    break
            if item: break
        if item and item.get("url") not in {x.get("url") for x in selected}:
            selected.append(item)
    return selected[:6]

def download_polyhaven(root,index):
    report=[]
    counts={"hdris":16,"models":22,"textures":36}
    dependency_cap=8*1024*1024
    for kind,limit in counts.items():
        try:
            data=request_json(f"https://api.polyhaven.com/assets?type={kind}",timeout=35)
            entries=[(k,v) for k,v in data.items() if isinstance(v,dict)]
            entries.sort(key=lambda kv:int(kv[1].get("download_count",0) or 0),reverse=True)
            chosen=[]; seen=set()
            for asset_id,meta in entries:
                categories=meta.get("categories") if kind=="textures" else [meta.get("category","")]
                if isinstance(categories,str): categories=[categories]
                cat=str((categories or [meta.get("category","")])[0]).split("/")[0] or "other"
                if cat in seen and len(chosen)<limit-2: continue
                chosen.append((asset_id,meta)); seen.add(cat)
                if len(chosen)>=limit: break
            for asset_id,meta in chosen:
                row={"id":"polyhaven-"+asset_id,"title":meta.get("name",asset_id),"provider":"Poly Haven",
                     "source_page":f"https://polyhaven.com/a/{asset_id}","license":CC0,
                     "license_url":"https://polyhaven.com/license","category":meta.get("category",kind)}
                try:
                    tree=request_json(f"https://api.polyhaven.com/files/{urllib.parse.quote(asset_id)}",timeout=35)
                    downloaded=[]
                    if kind=="textures":
                        file_objects=choose_poly_texture_selection(tree)
                        if not file_objects: raise RuntimeError("no supported PBR maps returned by official API")
                        pack_dir=root/"third-party/polyhaven"/"textures"/slugify(asset_id)
                        for fo in file_objects:
                            url=fo["url"]
                            try:
                                blob,ctype=request_bytes(url,timeout=35,limit=dependency_cap)
                                name=Path(urllib.parse.urlparse(url).path).name
                                if Path(name).suffix.lower() not in ALLOWED: continue
                                target=pack_dir/name
                                target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                                digest=sha256_path(target)
                                entry={"id":f"polyhaven-{asset_id}-{slugify(name)}","path":target.relative_to(root).as_posix(),
                                       "type":"polyhaven-pbr-map","title":name,"parent_asset_id":"polyhaven-"+asset_id,
                                       "category":row["category"],"source_page":row["source_page"],"license":CC0,
                                       "license_url":"https://polyhaven.com/license","size_bytes":len(blob),
                                       "sha256":digest,"redistributable":True}
                                index.append(entry); downloaded.append(entry)
                            except Exception as dep_exc:
                                row.setdefault("dependency_failures",[]).append({"url":url,"reason":str(dep_exc)})
                        if not downloaded: raise RuntimeError("no PBR map could be downloaded")
                    else:
                        fileobj=choose_poly_file(tree,kind)
                        if not fileobj: raise RuntimeError("no suitable direct file in API response")
                        url=fileobj["url"]; blob,ctype=request_bytes(url,timeout=70,limit=MAX_POLY_FILE)
                        name=Path(urllib.parse.urlparse(url).path).name or (asset_id+(".hdr" if kind=="hdris" else ".blend"))
                        if Path(name).suffix.lower() not in ALLOWED: name += ".bin"
                        pack_dir=root/"third-party/polyhaven"/kind/slugify(asset_id)
                        pack_dir.mkdir(parents=True,exist_ok=True)
                        target=pack_dir/name; target.write_bytes(blob); digest=sha256_path(target)
                        entry={"id":"polyhaven-"+asset_id,"path":target.relative_to(root).as_posix(),
                               "type":"polyhaven-"+kind,"title":row["title"],"category":row["category"],
                               "source_page":row["source_page"],"license":CC0,"license_url":"https://polyhaven.com/license",
                               "size_bytes":len(blob),"sha256":digest,"redistributable":True,"file_url":url}
                        index.append(entry); downloaded.append(entry)
                        for relpath,dep in (fileobj.get("include") or {}).items():
                            try:
                                rel=PurePosixPath(str(relpath).replace("\\\\","/"))
                                ext=Path(rel.name).suffix.lower()
                                if rel.is_absolute() or ".." in rel.parts or ext not in ALLOWED or ext in DENIED: continue
                                dep_url=dep.get("url") if isinstance(dep,dict) else None
                                if not dep_url: continue
                                if int(dep.get("size",0) or 0)>dependency_cap: continue
                                dep_blob,dep_ctype=request_bytes(dep_url,timeout=35,limit=dependency_cap)
                                dep_path=(pack_dir/Path(*rel.parts)).resolve()
                                if pack_dir.resolve() not in dep_path.parents: raise RuntimeError("unsafe dependency path")
                                dep_path.parent.mkdir(parents=True,exist_ok=True); dep_path.write_bytes(dep_blob)
                                dep_sha=sha256_path(dep_path)
                                index.append({"id":"polyhaven-"+asset_id+"-dependency-"+slugify(rel.as_posix()),
                                              "path":dep_path.relative_to(root).as_posix(),"type":"polyhaven-model-dependency",
                                              "parent_asset_id":"polyhaven-"+asset_id,"source_page":row["source_page"],
                                              "license":CC0,"license_url":"https://polyhaven.com/license",
                                              "size_bytes":len(dep_blob),"sha256":dep_sha,"redistributable":True})
                                row["dependencies_downloaded"]=row.get("dependencies_downloaded",0)+1
                            except Exception as dep_exc:
                                row.setdefault("dependency_failures",[]).append({"path":str(relpath),"reason":str(dep_exc)})
                    row.update(status="downloaded",path=downloaded[0]["path"],downloaded_files=len(downloaded),
                               size_bytes=sum(x.get("size_bytes",0) for x in downloaded))
                    print("[Poly Haven] OK:",asset_id,kind,len(downloaded),"file(s)")
                except Exception as exc:
                    row.update(status="failed",reason=str(exc)); print("[Poly Haven] failed:",asset_id,str(exc))
                report.append(row); time.sleep(.35)
        except Exception as exc:
            report.append({"id":"polyhaven-"+kind,"provider":"Poly Haven","status":"failed","reason":str(exc),"source_page":"https://polyhaven.com/license"})
            print("[Poly Haven] API unavailable:",kind,str(exc))
    write_text(root/"third-party/polyhaven/POWERED-BY-POLY-HAVEN.md",
        "# Poly Haven credit\n\nAssets in this folder are CC0. When this library uses the live public API, its tools should make clear the assets came from Poly Haven. Sources: https://polyhaven.com/license and https://github.com/Poly-Haven/Public-API/blob/master/ToS.md\n")
    return report

def download_met_open_access(root,index):
    report=[]; total=0; cap=90
    queries=[
        ("landscape","landscape painting"),("botanical","botanical illustration"),("astronomy","astronomy celestial chart"),
        ("maps","antique map"),("architecture","architectural drawing"),("animals","animal painting"),
        ("food","still life fruit"),("textiles","textile pattern"),("instruments","musical instrument"),
        ("mythology","mythological painting"),("fashion","historical costume"),("science","scientific instrument"),
        ("archaeology","archaeology artifact"),("sculpture","sculpture statue"),("printmaking","etching engraving print"),
        ("marine","marine life painting"),("geology","minerals geology illustration"),("navigation","nautical instrument"),
        ("manuscripts","illuminated manuscript"),("coins","historic coin medal"),("ceramics","historic pottery vessel"),
        ("photography","historic photograph city"),("astronomy-instruments","astrolabe celestial globe"),("textile-heritage","historic textile embroidery"),
        ("architecture-plans","architectural plan drawing"),("birds","bird natural history painting"),("botanical-prints","botanical plate flowers")
    ]
    seen=set()
    for category,q in queries:
        if total>=cap: break
        search_url="https://collectionapi.metmuseum.org/public/collection/v1.1/search?"+urllib.parse.urlencode({
            "isPublicDomain":"true","hasImages":"true","q":q,"limit":14,"offset":0})
        try:
            response=request_json(search_url,timeout=20)
            for object_id in response.get("objectIDs") or []:
                if total>=cap or sum(1 for r in report if r.get("category")==category and r.get("status")=="downloaded")>=7: break
                if object_id in seen: continue
                seen.add(object_id)
                try:
                    obj=request_json(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{int(object_id)}",timeout=18)
                    if obj.get("isPublicDomain") is not True: continue
                    image_url=obj.get("primaryImageSmall") or obj.get("primaryImage")
                    if not isinstance(image_url,str) or not image_url.startswith("https://images.metmuseum.org/"): continue
                    blob,ctype=request_bytes(image_url,timeout=22,limit=MAX_MEDIA_FILE)
                    if not ctype.lower().startswith("image/") or len(blob)<2048:
                        raise RuntimeError("URL did not return a usable image")
                    ext=Path(urllib.parse.urlparse(image_url).path).suffix.lower()
                    if ext not in {".jpg",".jpeg",".png",".webp"}:
                        ext={ "image/jpeg":".jpg","image/png":".png","image/webp":".webp"}.get(ctype.split(";")[0].lower(),".jpg")
                    title=str(obj.get("title") or f"Met object {object_id}")
                    filename=f"{category}-{slugify(title)[:44]}-{int(object_id)}{ext}"
                    target=root/"third-party/met-open-access"/filename
                    target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                    digest=sha256_path(target)
                    object_page=obj.get("objectURL") or f"https://www.metmuseum.org/art/collection/search/{int(object_id)}"
                    entry={"id":f"met-oa-{int(object_id)}","path":target.relative_to(root).as_posix(),"type":"met-open-access-image",
                           "category":category,"title":title,"artist":obj.get("artistDisplayName"),"date":obj.get("objectDate"),
                           "department":obj.get("department"),"medium":obj.get("medium"),"credit_line":obj.get("creditLine"),
                           "source_page":object_page,"image_url":image_url,"license":CC0,
                           "license_url":"https://www.metmuseum.org/about-the-met/policies-and-documents/open-access",
                           "license_code_url":CC0_URL,"size_bytes":len(blob),"sha256":digest,"redistributable":True}
                    index.append(entry); total+=1
                    report.append({"id":entry["id"],"status":"downloaded","category":category,"path":entry["path"],
                                   "title":title,"source_page":object_page,"size_bytes":len(blob),"sha256":digest,"license":CC0})
                    print("[The Met Open Access] OK:",category,title[:52],len(blob))
                except Exception as item_exc:
                    report.append({"id":"met-"+str(object_id),"status":"failed","category":category,"reason":str(item_exc)})
                    print("[The Met Open Access] item failed:",object_id,str(item_exc))
                time.sleep(.15)
        except Exception as exc:
            report.append({"id":"met-"+category,"status":"failed","category":category,"reason":str(exc),
                           "source_page":"https://www.metmuseum.org/hubs/open-access"})
            print("[The Met Open Access] query failed:",q,str(exc))
        time.sleep(.2)
    return report


def nasa_item_is_eligible(data):
    """Screen NASA-center attribution and explicit rights/person markers without rejecting center codes."""
    center=str(data.get("center") or "").strip().upper()
    known_centers={"NASA","JPL","JSC","KSC","GSFC","HQ","MSFC","LRC","ARC","AFRC","SSC","GRC",
                   "LARC","DFRC","NSSC","NESC","GISS","Ames Research Center".upper(),
                   "GODDARD SPACE FLIGHT CENTER","JOHNSON SPACE CENTER","KENNEDY SPACE CENTER",
                   "MARSHALL SPACE FLIGHT CENTER","AMES RESEARCH CENTER","GLENN RESEARCH CENTER",
                   "LANGLEY RESEARCH CENTER","STENNIS SPACE CENTER"}
    if not (center in known_centers or "NASA" in center):
        return False, "record has no recognized NASA-center attribution"
    title=str(data.get("title") or "")
    description=str(data.get("description") or "")
    secondary=str(data.get("secondary_creator") or "")
    combined=" ".join([title,description,secondary,center]).lower()
    blocked=("all rights reserved","copyrighted","copyright holder","copyright restrictions","©",
             "nasa logo","nasa insignia","nasa seal","third-party copyright","permission required")
    if any(marker in combined for marker in blocked):
        return False, "explicit copyright/rights or protected NASA identifier marker found"
    keywords=data.get("keywords") or []
    if isinstance(keywords,str): keywords=[keywords]
    people_terms={"astronaut","astronauts","portrait","portraits","crew portrait","crew portraits",
                  "people","person","personnel","human subject","human subjects","self portrait"}
    normalized={str(word).strip().lower() for word in keywords}
    if any(word in people_terms for word in normalized):
        return False, "identifiable-person category excluded from the general stock pool"
    if any("third-party copyright" in str(word).lower() or "copyrighted" in str(word).lower() for word in keywords):
        return False, "item keywords include an explicit third-party rights marker"
    return True, "recognized NASA center, no explicit third-party copyright marker, NASA media guidance retained"


def download_nasa_media(root,index):
    """Bundle small NASA-origin media when the item passes the conservative policy filters."""
    report=[]; seen=set()
    searches=[
        ("space","nebula galaxy stars"),("planet","Mars surface rover"),
        ("earth","Earth from space clouds"),("solar","solar flare sun"),
        ("ocean","Earth ocean satellite"),("atmosphere","aurora atmosphere"),
        ("launch","rocket launch pad"),("aviation","NASA research aircraft"),
        ("telescope","James Webb space telescope"),("moon","Moon lunar surface"),
        ("climate","hurricane satellite view"),("observatory","deep space galaxy"),
        ("planetary","Saturn rings spacecraft"),("earth-science","Earth observation"),
        ("asteroid","asteroid Bennu surface"),("space-station","International Space Station exterior"),
        ("mars-audio","Mars rover microphone audio sound recording"),
        ("jupiter-audio","Jupiter radio emissions audio NASA"),
        ("solar-audio","solar activity sonification audio NASA"),
        ("rocket-audio","rocket engine test sound recording NASA"),
        ("spacecraft-audio","spacecraft radio signal audio recording NASA"),
        ("earth-audio","Earth ocean sound NASA audio")
    ]
    media_types=("image","video","audio")
    for category,q in searches:
        for media_type in media_types:
            if category.endswith("-audio") and media_type!="audio":
                continue
            if not category.endswith("-audio") and media_type=="audio" and category not in {"space","earth","launch","atmosphere"}:
                continue
            params={"q":q,"media_type":media_type,"page_size":25}
            search_url="https://images-api.nasa.gov/search?"+urllib.parse.urlencode(params)
            try:
                response=request_json(search_url,timeout=18)
                items=((response.get("collection") or {}).get("items") or [])
                chosen=None; chosen_data=None; chosen_id=None
                for item in items:
                    data=(item.get("data") or [{}])[0]
                    nasa_id=str(data.get("nasa_id") or "")
                    if not nasa_id or nasa_id in seen or data.get("media_type")!=media_type:
                        continue
                    eligible,reason=nasa_item_is_eligible(data)
                    if not eligible:
                        continue
                    chosen=item; chosen_data=data; chosen_id=nasa_id
                    break
                if not chosen:
                    report.append({"id":f"nasa-{category}-{media_type}","provider":"NASA Image and Video Library",
                                   "category":category,"status":"no_eligible_item","query":q,
                                   "source_page":"https://images.nasa.gov/","reason":"No distinct record passed the NASA-center and rights/person filters."})
                    continue
                seen.add(chosen_id)
                try:
                    manifest=request_json("https://images-api.nasa.gov/asset/"+urllib.parse.quote(chosen_id,safe=""),timeout=18)
                    urls=[str(x.get("href") or "") for x in ((manifest.get("collection") or {}).get("items") or [])]
                    if media_type=="image":
                        allowed_ext={".jpg",".jpeg",".png",".webp"}; cap=MAX_MEDIA_FILE
                    elif media_type=="video":
                        allowed_ext={".mp4",".mov",".m4v"}; cap=18*1024*1024
                    else:
                        allowed_ext={".mp3",".wav",".m4a",".ogg"}; cap=15*1024*1024
                    candidates=[]
                    for media_url in urls:
                        media_url=media_url.replace("http://","https://",1)
                        raw_parsed=urllib.parse.urlsplit(media_url)
                        # NASA manifest filenames often contain literal spaces and curly apostrophes.
                        # Quote only the URL path, preserving safe delimiters and any query string.
                        safe_path=urllib.parse.quote(raw_parsed.path,safe="/%:@-._~!$&'()*+,;=")
                        media_url=urllib.parse.urlunsplit((raw_parsed.scheme,raw_parsed.netloc,safe_path,raw_parsed.query,raw_parsed.fragment))
                        parsed=urllib.parse.urlparse(media_url)
                        if parsed.hostname!="images-assets.nasa.gov":
                            continue
                        ext=Path(parsed.path).suffix.lower()
                        path_lower=parsed.path.lower()
                        # NASA manifest rendition URLs may omit the extension entirely (e.g. ~smal).
                        if ext not in allowed_ext:
                            if media_type=="image" and "/image/" in path_lower and ext=="":
                                ext=".unknown"
                            elif media_type=="video" and "/video/" in path_lower and ext=="":
                                ext=".unknown"
                            elif media_type=="audio" and "/audio/" in path_lower and ext=="":
                                ext=".unknown"
                            else:
                                continue
                        name=Path(parsed.path).name.lower()
                        preference=0 if "~smal" in name or "~small" in name else 1 if "~medi" in name or "~medium" in name else 2 if "~larg" in name or "~large" in name else 3 if "~orig" in name else 4
                        candidates.append((preference,len(media_url),media_url,ext))
                    candidates.sort()
                    downloaded=None; failures=[]
                    for _,__,media_url,ext in candidates:
                        try:
                            blob,ctype=request_bytes(media_url,timeout=35,limit=cap)
                            if len(blob)<2048:
                                raise RuntimeError("media file too small / not a usable asset")
                            if media_type=="image" and not ctype.lower().startswith("image/"):
                                raise RuntimeError("URL did not return image MIME type")
                            if media_type=="video" and (len(blob)<20000 or b"ftyp" not in blob[:64]):
                                raise RuntimeError("URL did not return a usable MP4/MOV container")
                            if media_type=="audio" and not (ctype.lower().startswith("audio/") or blob.startswith(b"RIFF") or blob.startswith(b"ID3")):
                                raise RuntimeError("URL did not return a recognizable audio file")
                            if ext==".unknown":
                                mime=ctype.split(";")[0].lower()
                                inferred={"image/jpeg":".jpg","image/png":".png","image/webp":".webp","image/tiff":".tif",
                                          "video/mp4":".mp4","video/quicktime":".mov","audio/mpeg":".mp3",
                                          "audio/mp4":".m4a","audio/wav":".wav","audio/x-wav":".wav","audio/ogg":".ogg"}.get(mime)
                                if inferred is None:
                                    if blob.startswith(b"RIFF") and media_type=="audio": inferred=".wav"
                                    elif blob.startswith(b"ID3") and media_type=="audio": inferred=".mp3"
                                    elif len(blob)>12 and blob[4:8]==b"ftyp" and media_type=="video": inferred=".mp4"
                                if inferred is None:
                                    raise RuntimeError("extensionless NASA media has unrecognized MIME/container: "+ctype)
                                ext=inferred
                            downloaded=(media_url,ext,blob,ctype); break
                        except Exception as file_exc:
                            failures.append(str(file_exc))
                    if not downloaded:
                        raise RuntimeError("no suitable small media file could be retrieved: "+"; ".join(failures[-3:]))
                    media_url,ext,blob,ctype=downloaded
                    title=str(chosen_data.get("title") or chosen_id)
                    filename=f"{category}-{slugify(title)[:48]}-{slugify(chosen_id)}{ext}"
                    folder={"image":"images","video":"video","audio":"audio"}[media_type]
                    target=root/"third-party/nasa"/folder/filename
                    target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                    digest=sha256_path(target)
                    page_url="https://images.nasa.gov/details/"+urllib.parse.quote(chosen_id,safe="")
                    license_name="NASA Media Usage Guidelines — generally not copyrighted; not CC0"
                    entry={"id":"nasa-"+media_type+"-"+slugify(chosen_id),"path":target.relative_to(root).as_posix(),
                           "type":"nasa-government-"+media_type,"title":title,"category":category,
                           "description":str(chosen_data.get("description") or "")[:2500],
                           "center":chosen_data.get("center"),"date_created":chosen_data.get("date_created"),
                           "keywords":chosen_data.get("keywords") or [],"source_page":page_url,"source_file_url":media_url,
                           "license":license_name,"license_url":"https://www.nasa.gov/nasa-brand-center/images-and-media/",
                           "rights_basis":"Official NASA-center item passed a conservative copyright-marker filter; NASA guidance says NASA content is generally not copyrighted in the United States, while third-party marked material must be excluded.",
                           "usage_notes":"Credit NASA; do not imply NASA endorsement. Avoid NASA insignia/logos and assess privacy/publicity rights before commercial use. This is not a CC0 license.",
                           "license_filter_passed":True,"size_bytes":len(blob),"sha256":digest,"redistributable":True}
                    index.append(entry)
                    report.append({"id":entry["id"],"status":"downloaded","category":category,"media_type":media_type,
                                   "path":entry["path"],"title":title,"source_page":page_url,"source_file_url":media_url,
                                   "license":license_name,"size_bytes":len(blob),"sha256":digest,"rights_filter":"passed"})
                    print("[NASA media] OK:",media_type,category,title[:48],len(blob))
                except Exception as item_exc:
                    report.append({"id":"nasa-"+media_type+"-"+slugify(chosen_id),"status":"failed",
                                   "category":category,"media_type":media_type,"source_page":"https://images.nasa.gov/details/"+chosen_id,
                                   "reason":str(item_exc)})
                    print("[NASA media] item failed:",chosen_id,str(item_exc))
                time.sleep(.12)
            except Exception as exc:
                report.append({"id":f"nasa-{category}-{media_type}","provider":"NASA Image and Video Library",
                               "category":category,"status":"failed","query":q,"reason":str(exc),
                               "source_page":"https://images.nasa.gov/"})
                print("[NASA media] search failed:",q,media_type,str(exc))
    return report


def loc_rights_are_eligible(rights):
    if isinstance(rights,list): text_value=" ".join(str(x) for x in rights)
    elif isinstance(rights,dict): text_value=" ".join(str(v) for v in rights.values())
    else: text_value=str(rights or "")
    low=text_value.lower().replace("&nbsp;"," ")
    positive=("no known restrictions on publication","public domain","no known copyright restrictions")
    negative=("copyrighted","permission required","possible restrictions","restricted material","all rights reserved")
    return any(p in low for p in positive) and not any(n in low for n in negative),text_value


def loc_rights_from_item(detail):
    """Prefer the Library's item-level rights_information / rights_advisory fields."""
    item_record=detail.get("item") if isinstance(detail,dict) else {}
    if not isinstance(item_record,dict): item_record={}
    candidates=[
        item_record.get("rights_information"),
        item_record.get("rights_advisory"),
        item_record.get("rights_status"),
        item_record.get("rights"),
        detail.get("rights_information") if isinstance(detail,dict) else None,
        detail.get("rights_advisory") if isinstance(detail,dict) else None,
    ]
    for candidate in candidates:
        eligible,text_value=loc_rights_are_eligible(candidate)
        if eligible:
            return True,text_value,item_record
    # Return the first non-empty statement for a useful skipped-item report.
    for candidate in candidates:
        if candidate:
            _,text_value=loc_rights_are_eligible(candidate)
            return False,text_value,item_record
    return False,"No explicit positive item-level rights statement present",item_record


def download_loc_public_domain(root,index):
    """Only bundle LOC photos after verifying a positive rights statement on the exact item record."""
    report=[]; total=0; cap=48
    queries=[
        ("aviation","aircraft aviation"),("maps","historical map"),("industry","industrial machinery"),
        ("agriculture","farm harvest"),("city","historic city street"),("nature","national park landscape"),
        ("science","scientific instrument laboratory"),("astronomy","astronomy observatory"),
        ("architecture","historic architecture building"),("transport","railroad locomotive"),
        ("ocean","ship harbor ocean"),("history","historic poster"),("botanical","botanical illustration"),
        ("engineering","bridge engineering"),("weather","storm weather"),("culture","textile pattern pottery")
    ]
    seen=set()
    for category,q in queries:
        if total>=cap: break
        url="https://www.loc.gov/photos/?"+urllib.parse.urlencode({"fo":"json","c":30,"q":q})
        successes=0; checked=0; rejections=[]
        try:
            response=request_json(url,timeout=12)
            for item in response.get("results") or []:
                if total>=cap or successes>=3 or checked>=6: break
                item_url=str(item.get("url") or item.get("id") or "")
                if not item_url: continue
                identity=item_url.rstrip("/").split("/")[-1]
                if not identity or identity in seen: continue
                seen.add(identity); checked+=1
                detail_url=item_url.replace("http://","https://")
                detail_url += ("&" if "?" in detail_url else "?")+"fo=json"
                try:
                    detail=request_json(detail_url,timeout=14)
                except Exception as detail_exc:
                    reason=str(detail_exc)
                    rejections.append("item metadata timeout/error: "+reason)
                    # The LOC endpoint rate-limits bursty consumers; back off on 429s instead of hammering it.
                    time.sleep(2.0 if "429" in reason else 0.6)
                    continue
                time.sleep(1.15)
                eligible,rights_text,item_record=loc_rights_from_item(detail)
                if not eligible:
                    rejections.append("rights not positively stated: "+rights_text[:120])
                    continue
                if item_record.get("access_restricted") is True:
                    rejections.append("item-level access_restricted=true")
                    continue
                source_summary=item_record if item_record else item
                image_urls=source_summary.get("image_url") or item.get("image_url") or []
                if isinstance(image_urls,str): image_urls=[image_urls]
                if isinstance(image_urls,dict): image_urls=list(image_urls.values())
                candidates=[str(x) for x in image_urls if isinstance(x,str) and urllib.parse.urlparse(x).hostname in {"loc.gov","www.loc.gov","tile.loc.gov"}]
                if not candidates:
                    resources=detail.get("resources") or []
                    for resource in resources:
                        for file_group in (resource.get("files") or []):
                            group_items=file_group if isinstance(file_group,list) else [file_group]
                            for fileobj in group_items:
                                if not isinstance(fileobj,dict): continue
                                candidate=str(fileobj.get("url") or fileobj.get("filename") or fileobj.get("download") or "")
                                if candidate and urllib.parse.urlparse(candidate).hostname in {"loc.gov","www.loc.gov","tile.loc.gov"}:
                                    candidates.append(candidate)
                if not candidates:
                    rejections.append("rights passed but no direct image URL found")
                    continue
                downloaded=None
                for image_url in list(dict.fromkeys(reversed(candidates))):
                    try:
                        blob,ctype=request_bytes(image_url,timeout=12,limit=MAX_MEDIA_FILE)
                        if not ctype.lower().startswith("image/") or len(blob)<2048:
                            continue
                        ext=Path(urllib.parse.urlparse(image_url).path).suffix.lower()
                        if ext not in {".jpg",".jpeg",".png",".webp"}:
                            ext={"image/jpeg":".jpg","image/png":".png","image/webp":".webp"}.get(ctype.split(";")[0].lower(),".jpg")
                        downloaded=(image_url,ext,blob); break
                    except Exception as image_exc:
                        rejections.append("image fetch failed: "+str(image_exc))
                if not downloaded: continue
                image_url,ext,blob=downloaded
                title=str(source_summary.get("title") or item.get("title") or identity)
                target=root/"third-party/library-of-congress"/(f"{category}-{slugify(title)[:46]}-{slugify(identity)}{ext}")
                target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                digest=sha256_path(target)
                source_page=source_summary.get("id") or item_url
                source_page=str(source_page).replace("http://","https://")
                entry={"id":"loc-"+slugify(identity),"path":target.relative_to(root).as_posix(),"type":"loc-rights-verified-image",
                       "title":title,"category":category,"date":source_summary.get("date") or item.get("date"),
                       "description":str(source_summary.get("description") or item.get("description") or "")[:1500],
                       "rights_statement":rights_text,"source_page":source_page,"source_file_url":image_url,
                       "license":"Public Domain / No Known Restrictions on Publication (record-level rights statement)",
                       "license_url":"https://www.loc.gov/rr/print/195_copr.html","rights_verified_from_item_metadata":True,
                       "usage_notes":"LOC states users are responsible for evaluating rights and other restrictions; preserve this item's exact rights statement and assess context before publication.",
                       "size_bytes":len(blob),"sha256":digest,"redistributable":True}
                index.append(entry); total+=1; successes+=1
                report.append({"id":entry["id"],"status":"downloaded","category":category,"path":entry["path"],
                               "title":title,"source_page":source_page,"rights_statement":rights_text,
                               "size_bytes":len(blob),"sha256":digest})
                print("[Library of Congress] OK:",category,title[:48],len(blob))
                time.sleep(.12)
            if not successes:
                report.append({"id":"loc-"+category,"status":"no_eligible_item","category":category,"query":q,
                               "source_page":"https://www.loc.gov/apis/json-and-yaml/","items_checked":checked,
                               "reason":"No downloadable image passed exact-item rights verification. "+ " | ".join(rejections[:3])})
        except Exception as exc:
            report.append({"id":"loc-"+category,"status":"failed","category":category,"query":q,
                           "source_page":"https://www.loc.gov/apis/json-and-yaml/","reason":str(exc)})
            print("[Library of Congress] query failed:",q,str(exc))
    return report


def openverse_extension(url,ctype,kind,item):
    ext=Path(urllib.parse.urlparse(url).path).suffix.lower()
    allowed={".jpg",".jpeg",".png",".webp"} if kind=="image" else {".mp3",".wav",".ogg",".flac",".m4a"}
    if ext in allowed: return ext
    mime=ctype.split(";")[0].lower()
    m={"image/jpeg":".jpg","image/png":".png","image/webp":".webp","audio/mpeg":".mp3","audio/mp3":".mp3","audio/wav":".wav","audio/x-wav":".wav","audio/ogg":".ogg","audio/flac":".flac","audio/mp4":".m4a"}
    if m.get(mime) in allowed: return m[mime]
    ft=str(item.get("filetype") or "").lower()
    return "."+ft if "."+ft in allowed else ""


def wikimedia_license_is_eligible(short_name):
    """Only accept file-level CC0 or Public Domain labels from the Commons metadata record."""
    normalized=re.sub(r"[\s\-®()]+","",str(short_name or "").lower())
    return normalized in {
        "cc0","cc01.0","creativecommonszero",
        "publicdomain","publicdomainmark","publicdomainus","publicdomainunitedstates"
    }


def download_wikimedia_public_domain(root,index):
    report=[]; total=0; cap=160; seen=set()
    queries=[
        ("maps","historical map filetype:bitmap"),("space","space nebula public domain filetype:bitmap"),
        ("museum","museum artifact CC0 filetype:bitmap"),("architecture","architecture public domain filetype:bitmap"),
        ("ocean","ocean public domain filetype:bitmap"),("plants","plants botanical public domain filetype:bitmap"),
        ("anatomy","human anatomy public domain illustration filetype:bitmap"),("science","physics diagram public domain filetype:bitmap"),
        ("newspapers","historical newspaper public domain filetype:bitmap"),("food","fruit still life public domain filetype:bitmap"),
        ("wildlife","wildlife public domain photo filetype:bitmap"),("satellite","satellite image public domain filetype:bitmap"),
        ("landscape","landscape public domain photo filetype:bitmap"),("industry","industrial machinery public domain filetype:bitmap"),
        ("urban","historic city street public domain filetype:bitmap"),("bridges","bridge public domain photo filetype:bitmap"),
        ("spaceflight","lunar surface public domain filetype:bitmap"),("geology","geology rock formation public domain filetype:bitmap"),
        ("insects","insect scientific illustration public domain filetype:bitmap"),("portraits-archive","historic building public domain photo filetype:bitmap"),
        ("astronomy-archive","star chart astronomy public domain filetype:bitmap"),("engineering-plans","engineering drawing bridge public domain filetype:bitmap"),
        ("historic-transport","steam locomotive public domain filetype:bitmap"),("airships","airship aviation public domain filetype:bitmap"),
        ("scientific-instruments","scientific equipment public domain filetype:bitmap"),("volcanoes","volcanic eruption public domain filetype:bitmap"),
        ("coral","coral reef marine biology public domain filetype:bitmap"),("mammals","mammal natural history public domain filetype:bitmap"),
        ("botanical-prints","botanical plate flower public domain filetype:bitmap"),("world-maps","world map antique public domain filetype:bitmap"),
        ("railway","historic railroad station public domain filetype:bitmap"),("bridges-archive","historic bridge construction public domain filetype:bitmap"),
        ("craft","ceramics textile craft public domain filetype:bitmap"),("early-computing","early computer machinery public domain filetype:bitmap"),
        ("weather-maps","weather map storm public domain filetype:bitmap"),("lunar","Apollo Moon surface public domain filetype:bitmap"),
        ("historic-labs","laboratory scientific equipment public domain filetype:bitmap"),("urban-archive","historic city architecture public domain filetype:bitmap")
    ]
    for category,q in queries:
        if total>=cap: break
        params={"action":"query","format":"json","generator":"search","gsrsearch":q,"gsrnamespace":6,"gsrlimit":30,
                "prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":1600}
        url="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
        successes=0
        try:
            response=request_json(url,timeout=16)
            pages=(response.get("query") or {}).get("pages") or {}
            for page in pages.values():
                if total>=cap or successes>=8: break
                imageinfo=(page.get("imageinfo") or [{}])[0]
                meta=imageinfo.get("extmetadata") or {}
                short=str((meta.get("LicenseShortName") or {}).get("value") or "").strip()
                license_url=str((meta.get("LicenseUrl") or {}).get("value") or imageinfo.get("descriptionurl") or "")
                if not wikimedia_license_is_eligible(short):
                    continue
                asset_url=imageinfo.get("thumburl") or imageinfo.get("url")
                page_url=imageinfo.get("descriptionurl") or "https://commons.wikimedia.org/wiki/"+urllib.parse.quote(page.get("title","").replace(" ","_"))
                if not asset_url or not asset_url.startswith("https://"): continue
                identity=str(page.get("pageid") or page.get("title"))
                if identity in seen: continue
                seen.add(identity)
                try:
                    blob,ctype=request_bytes(asset_url,timeout=22,limit=MAX_MEDIA_FILE)
                    if not ctype.lower().startswith("image/") or len(blob)<2048:
                        raise RuntimeError("thumbnail endpoint did not return a usable image")
                    name=Path(urllib.parse.urlparse(asset_url).path).name
                    ext=Path(name).suffix.lower()
                    if ext not in {".jpg",".jpeg",".png",".webp"}:
                        ext={ "image/jpeg":".jpg","image/png":".png","image/webp":".webp"}.get(ctype.split(";")[0].lower(),".jpg")
                    title=str((meta.get("ObjectName") or {}).get("value") or page.get("title") or identity)
                    filename=f"{category}-{slugify(title)[:48]}-{slugify(identity)}{ext}"
                    target=root/"third-party/wikimedia"/"images"/filename
                    target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                    digest=sha256_path(target)
                    artist=str((meta.get("Artist") or {}).get("value") or (meta.get("Credit") or {}).get("value") or "")
                    description=str((meta.get("ImageDescription") or {}).get("value") or "")
                    entry={"id":"wikimedia-"+slugify(identity),"path":target.relative_to(root).as_posix(),"type":"wikimedia-public-domain-image",
                           "category":category,"title":title,"creator":artist,"description":description,
                           "source_page":page_url,"source_file_url":imageinfo.get("url"),"license":short,
                           "license_url":license_url or "https://commons.wikimedia.org/wiki/Commons:Licensing",
                           "license_verified_from_item_metadata":True,"size_bytes":len(blob),"sha256":digest,"redistributable":True,
                           "note":"Only exact CC0/Public Domain metadata is auto-bundled; other licenses are skipped."}
                    index.append(entry); total+=1; successes+=1
                    report.append({"id":entry["id"],"status":"downloaded","category":category,"path":entry["path"],
                                   "title":title,"source_page":page_url,"license":short,"size_bytes":len(blob),"sha256":digest})
                    print("[Wikimedia Commons] OK:",category,short,title[:48],len(blob))
                except Exception as item_exc:
                    report.append({"id":"wikimedia-"+slugify(identity),"status":"failed","category":category,"reason":str(item_exc),"source_page":page_url})
            time.sleep(.25)
        except Exception as exc:
            report.append({"id":"wikimedia-"+category,"status":"failed","category":category,"reason":str(exc),"source_page":"https://commons.wikimedia.org/wiki/Commons:Licensing"})
            print("[Wikimedia Commons] search failed:",q,str(exc))
    return report

def smithsonian_rights_are_cc0(record_access,media_access):
    """Require both record and exact-media rights fields to explicitly say CC0."""
    return str(record_access or "").strip().upper()=="CC0" and str(media_access or "").strip().upper()=="CC0"


def rijksmuseum_license_from_rights(rights_text):
    """Return the narrow rights class explicitly represented in a Rijksmuseum EDM rights field."""
    rights_norm=str(rights_text or "").lower()
    cc0=("creativecommons.org/publicdomain/zero/1.0" in rights_norm or
         "creativecommons.org/publicdomain/zero/" in rights_norm or
         rights_norm.strip() in {"cc0","cc0-1.0","creative commons zero"})
    pdm=("creativecommons.org/publicdomain/mark/1.0" in rights_norm or
         "creativecommons.org/publicdomain/mark/" in rights_norm or
         "public domain mark" in rights_norm)
    if cc0: return "CC0-1.0"
    if pdm: return "Public Domain Mark 1.0"
    return None


def download_smithsonian_open_access(root,index):
    """Download Smithsonian media only when both record-level and media-level rights are explicitly CC0."""
    import os
    report=[]; total=0; cap=60; seen=set()
    api_key=(os.environ.get("SMITHSONIAN_API_KEY") or "").strip() or "DEMO_KEY"
    topics=[
        ("natural-history","NMNH"),("botany","NMNHBOTANY"),("birds","NMNHBIRDS"),
        ("paleontology","NMNHPALEO"),("minerals","NMNHMINSCI"),("air-and-space","NASM"),
        ("american-history","NMAH"),("asian-art","FSG"),("design-and-craft","CHNDM"),
        ("american-art","SAAM"),("portraits","NPG"),("african-american-history","NMAAHC"),
        ("native-american-culture","NMAI"),("zoo-wildlife","NZP"),("archives","SIA")
    ]
    def field_title(content):
        value=((content.get("descriptiveNonRepeating") or {}).get("title") or {})
        return str(value.get("content") or value.get("label") or "").strip()
    def field_creator(content):
        names=((content.get("indexedStructured") or {}).get("name") or [])
        if isinstance(names,str): names=[names]
        for name in names:
            if isinstance(name,str) and name.strip(): return name.strip()
            if isinstance(name,dict):
                candidate=str(name.get("name") or name.get("content") or "").strip()
                if candidate: return candidate
        free_names=((content.get("freetext") or {}).get("name") or [])
        if isinstance(free_names,dict): free_names=[free_names]
        for name in free_names:
            if isinstance(name,dict):
                candidate=str(name.get("content") or "").strip()
                if candidate: return candidate
        return ""
    def bounded_media_url(raw_url,limit_px):
        parsed=urllib.parse.urlsplit(str(raw_url or ""))
        host=(parsed.hostname or "").lower()
        if host not in {"ids.si.edu","collections.nmnh.si.edu"}:
            return ""
        query=urllib.parse.parse_qsl(parsed.query,keep_blank_values=True)
        if host=="ids.si.edu":
            # The official IDS delivery service accepts a bounded max parameter.
            query=[(k,v) for k,v in query if k.lower() not in {"max","thumb"}]
            query.append(("max",str(limit_px)))
        elif not any(k.lower()=="thumb" for k,v in query):
            query.append(("thumb","yes"))
        return urllib.parse.urlunsplit((parsed.scheme or "https",parsed.netloc,parsed.path,urllib.parse.urlencode(query),parsed.fragment))
    for category,unit_code in topics:
        if total>=cap: break
        params={"api_key":api_key,"q":f"unit_code:{unit_code}","rows":30}
        url="https://api.si.edu/openaccess/api/v1.0/search?"+urllib.parse.urlencode(params)
        try:
            data=request_json(url,timeout=22)
            rows=((data.get("response") or {}).get("rows") or [])
            successes=0; candidates_checked=0
            for row in rows:
                if total>=cap or successes>=5 or candidates_checked>=18: break
                content=row.get("content") if isinstance(row,dict) else None
                if not isinstance(content,dict): continue
                meta_access=str(((content.get("metadata_usage") or {}).get("access") or "")).strip()
                if meta_access.upper()!="CC0":
                    continue
                desc=content.get("descriptiveNonRepeating") or {}
                record_id=str(desc.get("record_ID") or row.get("id") or "")
                if not record_id or record_id in seen: continue
                media=desc.get("online_media") or {}
                media_items=media.get("media") or []
                if isinstance(media_items,dict): media_items=[media_items]
                eligible=[]
                for media_item in media_items:
                    if not isinstance(media_item,dict): continue
                    if str(media_item.get("type") or "").strip().lower() not in {"images","image"}:
                        continue
                    media_rights=str(((media_item.get("usage") or {}).get("access") or "")).strip()
                    if not smithsonian_rights_are_cc0(meta_access,media_rights):
                        continue
                    original=str(media_item.get("content") or "")
                    thumbnail=str(media_item.get("thumbnail") or "")
                    for candidate in (bounded_media_url(original,1400),bounded_media_url(thumbnail,900)):
                        if candidate and candidate not in eligible:
                            eligible.append(candidate)
                if not eligible: continue
                title=field_title(content) or record_id
                creator=field_creator(content)
                record_url=str(desc.get("record_link") or row.get("url") or "")
                if record_url.startswith("http://"):
                    record_url="https://"+record_url[len("http://"):]
                if not record_url.startswith("https://"):
                    guid=str(desc.get("guid") or "")
                    record_url=guid if guid.startswith("https://") else "https://www.si.edu/openaccess"
                used=None; failure_reasons=[]
                candidates_checked+=1
                for media_url in eligible:
                    try:
                        blob,ctype=request_bytes(media_url,timeout=22,limit=MAX_MEDIA_FILE)
                        mime=ctype.split(";")[0].strip().lower()
                        if not mime.startswith("image/") or len(blob)<2048:
                            raise RuntimeError("media endpoint did not return a usable image")
                        ext=Path(urllib.parse.urlparse(media_url).path).suffix.lower()
                        if ext not in {".jpg",".jpeg",".png",".webp"}:
                            ext={"image/jpeg":".jpg","image/jpg":".jpg","image/png":".png","image/webp":".webp","image/tiff":".tif"}.get(mime,"")
                        if not ext:
                            raise RuntimeError("unrecognized image MIME type: "+mime)
                        used=(media_url,ext,blob); break
                    except Exception as media_exc:
                        failure_reasons.append(str(media_exc))
                if not used:
                    report.append({"id":"smithsonian-"+slugify(record_id),"status":"failed","category":category,
                                   "title":title,"source_page":record_url,
                                   "reason":"No candidate image could be retrieved: "+" | ".join(failure_reasons[-2:])})
                    continue
                media_url,ext,blob=used
                target=root/"third-party/smithsonian"/category/(f"{slugify(title)[:48]}-{slugify(record_id)}{ext}")
                target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                digest=sha256_path(target); seen.add(record_id)
                notes=(content.get("freetext") or {}).get("notes") or []
                if isinstance(notes,dict): notes=[notes]
                if not isinstance(notes,list): notes=[]
                note=next((str(n.get("content") or "") for n in notes if isinstance(n,dict) and n.get("content")), "")
                entry={"id":"smithsonian-"+slugify(record_id),"path":target.relative_to(root).as_posix(),
                       "type":"smithsonian-open-access-image","title":title,"creator":creator,"category":category,
                       "unit_code":unit_code,"description":note[:1800],"record_id":record_id,"source_page":record_url,
                       "source_file_url":media_url,"license":"CC0-1.0",
                       "license_url":"https://www.si.edu/openaccess/faq",
                       "rights_verified_from_item_metadata":True,"record_access":"CC0","media_access":"CC0",
                       "size_bytes":len(blob),"sha256":digest,"redistributable":True,
                       "usage_notes":"Both the record-level metadata_usage.access and this exact media file's usage.access were CC0. CC0 handles copyright only; review privacy, publicity, trademark, cultural-property and other non-copyright rights where relevant."}
                index.append(entry); total+=1; successes+=1
                report.append({"id":entry["id"],"status":"downloaded","title":title,"category":category,
                               "path":entry["path"],"source_page":record_url,"license":"CC0-1.0",
                               "size_bytes":len(blob),"sha256":digest})
                print("[Smithsonian Open Access] OK:",category,title[:48],len(blob))
            if not successes:
                report.append({"id":"smithsonian-"+category,"status":"no_eligible_item","category":category,
                               "provider":"Smithsonian Institution","source_page":"https://www.si.edu/openaccess",
                               "reason":"No distinct image passed both record-level and media-level CC0 filters in the current page."})
        except Exception as exc:
            report.append({"id":"smithsonian-"+category,"status":"failed","category":category,
                           "provider":"Smithsonian Institution","source_page":"https://www.si.edu/openaccess",
                           "reason":str(exc)[:400]})
            print("[Smithsonian Open Access] query failed:",category,str(exc))
        time.sleep(.35)
    return report


def resolve_rijksmuseum_iiif(record_identifier):
    """Resolve a Rijksmuseum Linked Art record to its official bounded IIIF image URL."""
    uri=str(record_identifier or "").strip()
    parsed=urllib.parse.urlparse(uri)
    if parsed.hostname!="id.rijksmuseum.nl":
        return ""
    record_uri=urllib.parse.urlunsplit(("https","data.rijksmuseum.nl",parsed.path,"_profile=la-framed",""))
    record=request_json(record_uri,timeout=8)
    shows=record.get("shows") or []
    if isinstance(shows,dict): shows=[shows]
    visual_uri=next((str(x.get("id") or "") for x in shows if isinstance(x,dict) and x.get("id")), "")
    if urllib.parse.urlparse(visual_uri).hostname!="id.rijksmuseum.nl":
        return ""
    visual_parsed=urllib.parse.urlparse(visual_uri)
    visual_uri=urllib.parse.urlunsplit(("https","data.rijksmuseum.nl",visual_parsed.path,"_profile=la-framed",""))
    visual=request_json(visual_uri,timeout=8)
    digitals=visual.get("digitally_shown_by") or []
    if isinstance(digitals,dict): digitals=[digitals]
    digital_uri=next((str(x.get("id") or "") for x in digitals if isinstance(x,dict) and x.get("id")), "")
    if urllib.parse.urlparse(digital_uri).hostname!="id.rijksmuseum.nl":
        return ""
    digital_parsed=urllib.parse.urlparse(digital_uri)
    digital_uri=urllib.parse.urlunsplit(("https","data.rijksmuseum.nl",digital_parsed.path,"_profile=la-framed",""))
    digital=request_json(digital_uri,timeout=8)
    access_points=digital.get("access_point") or []
    if isinstance(access_points,dict): access_points=[access_points]
    for point in access_points:
        raw=str(point.get("id") or "") if isinstance(point,dict) else ""
        media=urllib.parse.urlparse(raw)
        if media.hostname=="iiif.micr.io":
            parts=[p for p in media.path.split("/") if p]
            if parts:
                ident=urllib.parse.quote(parts[0],safe="-._~")
                return f"https://iiif.micr.io/{ident}/full/1200,/0/default.jpg"
    return ""


def download_rijksmuseum_open_access(root,index):
    """Harvest a capped sample of Rijksmuseum records, but only image media with explicit CC0/PDM rights."""
    import xml.etree.ElementTree as ET
    from urllib.parse import urlencode
    report=[]; total=0; cap=60; seen=set()
    oai_ns="http://www.openarchives.org/OAI/2.0/"
    edm_ns="http://www.europeana.eu/schemas/edm/"
    dc_ns="http://purl.org/dc/elements/1.1/"
    dcterms_ns="http://purl.org/dc/terms/"
    rdf_resource="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"
    token=None; page_num=0; iiif_resolutions=0; iiif_resolution_limit=18
    while total<cap and page_num<16:
        page_num+=1
        if token:
            params={"verb":"ListRecords","resumptionToken":token}
        else:
            params={"verb":"ListRecords","metadataPrefix":"edm"}
        url="https://data.rijksmuseum.nl/oai?"+urlencode(params)
        try:
            xml_bytes,_=request_bytes(url,timeout=25,limit=18*1024*1024)
            doc=ET.fromstring(xml_bytes)
            error=doc.find(f"{{{oai_ns}}}error")
            if error is not None:
                report.append({"id":f"rijksmuseum-page-{page_num}","status":"failed",
                               "reason":(error.text or error.attrib.get("code") or "OAI-PMH error")[:300],
                               "source_page":"https://data.rijksmuseum.nl/docs/oai-pmh"})
                break
            records=doc.findall(f".//{{{oai_ns}}}record")
            page_downloads=0
            for record in records:
                if total>=cap or page_downloads>=6:
                    break
                header=record.find(f"{{{oai_ns}}}header")
                identifier=(header.findtext(f"{{{oai_ns}}}identifier") if header is not None else "") or ""
                if not identifier or identifier in seen:
                    continue
                seen.add(identifier)
                metadata=record.find(f"{{{oai_ns}}}metadata")
                if metadata is None:
                    continue
                rights=[]
                image_refs=[]
                page_refs=[]
                for el in metadata.iter():
                    local=el.tag.rsplit("}",1)[-1].lower()
                    value=(el.attrib.get(rdf_resource) or (el.text or "")).strip()
                    if not value:
                        continue
                    if local in {"rights","rightsstatement","rights_statement"}:
                        rights.append(value)
                    elif local=="isshownby":
                        if value: image_refs.append(value)
                        # EDM represents media URIs on nested edm:WebResource rdf:about attributes.
                        for child in el.iter():
                            child_uri=(child.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about") or "").strip()
                            if child_uri: image_refs.append(child_uri)
                    elif local in {"isshownat","shownat"}:
                        if value: page_refs.append(value)
                        for child in el.iter():
                            child_uri=(child.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about") or "").strip()
                            if child_uri: page_refs.append(child_uri)
                rights_text=" | ".join(dict.fromkeys(rights))
                license_name=rijksmuseum_license_from_rights(rights_text)
                if not license_name:
                    continue
                cc0=license_name=="CC0-1.0"
                def read_values(local_name):
                    result=[]
                    for el in metadata.iter():
                        if el.tag.rsplit("}",1)[-1].lower()==local_name.lower() and (el.text or "").strip():
                            result.append((el.text or "").strip())
                    return result
                media_url=""
                for ref_url in image_refs:
                    parsed=urllib.parse.urlparse(ref_url)
                    host=(parsed.hostname or "").lower()
                    if host=="iiif.micr.io":
                        parts=[p for p in parsed.path.split("/") if p]
                        if parts:
                            iiif_id=urllib.parse.quote(parts[0],safe="-._~")
                            media_url=f"https://iiif.micr.io/{iiif_id}/full/1200,/0/default.jpg"
                            break
                    elif host in {"images.micr.io","www.rijksmuseum.nl","rijksmuseum.nl"} and Path(parsed.path).suffix.lower() in {".jpg",".jpeg",".png",".webp"}:
                        media_url=ref_url; break
                if not media_url and iiif_resolutions<iiif_resolution_limit:
                    iiif_resolutions+=1
                    try:
                        media_url=resolve_rijksmuseum_iiif(identifier)
                    except Exception as resolve_exc:
                        report.append({"id":"rijksmuseum-resolve-"+slugify(identifier),"status":"resolution_failed",
                                       "reason":str(resolve_exc)[:300],
                                       "source_page":"https://data.rijksmuseum.nl/docs/iiif/"})
                if not media_url:
                    continue
                try:
                    blob,ctype=request_bytes(media_url,timeout=22,limit=MAX_MEDIA_FILE)
                    if not ctype.lower().startswith("image/") or len(blob)<2048:
                        raise RuntimeError("Rijksmuseum image URL did not return a usable image")
                    ext=Path(urllib.parse.urlparse(media_url).path).suffix.lower()
                    if ext not in {".jpg",".jpeg",".png",".webp"}:
                        ext={"image/jpeg":".jpg","image/png":".png","image/webp":".webp"}.get(ctype.split(";")[0].lower(),".jpg")
                    title=(read_values("title") or [identifier])[:1][0]
                    creator=(read_values("creator") or [""])[:1][0]
                    date=(read_values("date") or read_values("created") or [""])[:1][0]
                    object_page=(page_refs or [""])[0]
                    if not object_page.startswith("https://"):
                        object_page="https://data.rijksmuseum.nl/oai?"+urlencode({"verb":"GetRecord","metadataPrefix":"edm","identifier":identifier})
                    asset_id="rijksmuseum-"+slugify(identifier)
                    target=root/"third-party/rijksmuseum"/(f"{slugify(title)[:52]}-{slugify(identifier)[:48]}{ext}")
                    target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(blob)
                    digest=sha256_path(target)
                    entry={"id":asset_id,"path":target.relative_to(root).as_posix(),"type":"rijksmuseum-open-access-image",
                           "title":title,"creator":creator,"date":date,"rights_statement":rights_text,
                           "source_page":object_page,"source_file_url":media_url,"license":license_name,
                           "license_url":"https://data.rijksmuseum.nl/policy/","rights_verified_from_item_metadata":True,
                           "size_bytes":len(blob),"sha256":digest,"redistributable":True,
                           "usage_notes":"Rijksmuseum requests credit where possible. Public Domain Mark/CC0 addresses copyright status; consider privacy, trademark, cultural heritage and other rights where relevant."}
                    index.append(entry); total+=1; page_downloads+=1
                    report.append({"id":asset_id,"status":"downloaded","title":title,"creator":creator,
                                   "path":entry["path"],"source_page":object_page,"license":license_name,
                                   "rights_statement":rights_text,"size_bytes":len(blob),"sha256":digest})
                    print("[Rijksmuseum Open Access] OK:",title[:48],license_name,len(blob))
                except Exception as item_exc:
                    report.append({"id":"rijksmuseum-"+slugify(identifier),"status":"failed",
                                   "title":(read_values("title") or [identifier])[:1][0],
                                   "reason":str(item_exc)[:300],"source_page":"https://data.rijksmuseum.nl/docs/oai-pmh"})
                time.sleep(.12)
            token_el=doc.find(f".//{{{oai_ns}}}resumptionToken")
            token=(token_el.text or "").strip() if token_el is not None else ""
            if not token or not records:
                break
            time.sleep(.25)
        except Exception as exc:
            report.append({"id":f"rijksmuseum-page-{page_num}","status":"failed","reason":str(exc)[:300],
                           "source_page":"https://data.rijksmuseum.nl/docs/oai-pmh"})
            print("[Rijksmuseum Open Access] page failed:",page_num,str(exc))
            break
    return report


def download_google_fonts(root,index):
    """Bundle selected Google Fonts only after verifying the family's official OFL and metadata listing."""
    report=[]; total_bytes=0; max_total=42*1024*1024; max_font=9*1024*1024
    allowed_signatures={b"\x00\x01\x00\x00",b"OTTO",b"ttcf"}
    for slug,family,filenames,role,vietnamese_priority in FONT_FAMILIES:
        base=f"https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/"
        family_report={"id":"google-font-"+slug,"family":family,"source_page":"https://fonts.google.com/specimen/"+urllib.parse.quote(family.replace(" ","+"),safe="+"),
                       "status":"started","fonts":[]}
        try:
            license_blob,license_mime=request_bytes(base+"OFL.txt",timeout=20,limit=300000)
            license_text=license_blob.decode("utf-8","replace")
            if "SIL OPEN FONT LICENSE" not in license_text.upper() or "VERSION 1.1" not in license_text.upper():
                raise RuntimeError("Family license file does not explicitly confirm SIL Open Font License 1.1")
            metadata_blob,metadata_mime=request_bytes(base+"METADATA.pb",timeout=20,limit=1_500_000)
            metadata_text=metadata_blob.decode("utf-8","replace")
            listed=set(re.findall(r'filename:\s*"([^"]+\.ttf)"',metadata_text))
            if not listed:
                raise RuntimeError("Official METADATA.pb lists no TTF font files")
            source_name_match=re.search(r'name:\s*"([^"]+)"',metadata_text)
            official_name=source_name_match.group(1) if source_name_match else family
            languages=[x for x in re.findall(r'languages:\s*"([^"]+)"',metadata_text) if x]
            supports_vietnamese=any(x.lower().startswith("vi_") or x.lower()=="vi" for x in languages) or vietnamese_priority
            family_dir=root/"third-party/google-fonts"/slug
            family_dir.mkdir(parents=True,exist_ok=True)
            (family_dir/"OFL.txt").write_bytes(license_blob)
            (family_dir/"METADATA.pb").write_bytes(metadata_blob)
            family_report.update({"status":"metadata_verified","license":"SIL Open Font License 1.1",
                                  "license_url":base+"OFL.txt","metadata_url":base+"METADATA.pb",
                                  "font_files_requested":filenames})
            for filename in filenames:
                if total_bytes>=max_total:
                    family_report["font_budget_exhausted"]=True
                    break
                if filename not in listed:
                    family_report["fonts"].append({"file":filename,"status":"not_in_official_metadata"})
                    continue
                encoded=urllib.parse.quote(filename,safe="-_.")
                source_url=base+encoded
                try:
                    blob,ctype=request_bytes(source_url,timeout=28,limit=max_font)
                    if len(blob)<2048:
                        raise RuntimeError("font file is too small to be valid")
                    if blob[:4] not in allowed_signatures:
                        raise RuntimeError("downloaded file does not have a recognized TTF/OTF sfnt signature")
                    if total_bytes+len(blob)>max_total:
                        family_report["fonts"].append({"file":filename,"status":"skipped_total_font_budget"})
                        continue
                    target=family_dir/filename
                    target.write_bytes(blob)
                    digest=sha256_path(target)
                    italic=("italic" in filename.lower())
                    variable=("[" in filename and "]" in filename)
                    weight= "100 900" if variable else (
                        100 if "thin" in filename.lower() else
                        200 if "extralight" in filename.lower() else
                        300 if "light" in filename.lower() else
                        500 if "medium" in filename.lower() else
                        600 if "semibold" in filename.lower() else
                        700 if "bold" in filename.lower() else
                        800 if "extrabold" in filename.lower() else
                        900 if "black" in filename.lower() else 400
                    )
                    item_id="google-font-"+slug+"-"+slugify(filename)
                    item={"id":item_id,"path":target.relative_to(root).as_posix(),"type":"open-font-license-font",
                          "title":family+" — "+filename,"font_family":official_name,"font_family_id":slug,
                          "font_filename":filename,"font_weight":weight,"font_style":"italic" if italic else "normal",
                          "font_format":"truetype","font_role":role,"supports_vietnamese":bool(supports_vietnamese),
                          "category":"typography","creator":"Google Fonts upstream family contributors",
                          "source_page":"https://fonts.google.com/specimen/"+urllib.parse.quote(family.replace(" ","+"),safe="+"),
                          "source_file_url":source_url,"source_license_file":(family_dir/"OFL.txt").relative_to(root).as_posix(),
                          "license":"SIL Open Font License 1.1","license_url":base+"OFL.txt",
                          "rights_verified_from_item_metadata":True,"redistributable":True,"size_bytes":len(blob),"sha256":digest,
                          "note":"Font file was listed in the official Google Fonts METADATA.pb, and the family's OFL.txt explicitly identifies SIL Open Font License 1.1. Keep the license when redistributing the font file and observe any Reserved Font Name terms."}
                    index.append(item); total_bytes+=len(blob)
                    family_report["fonts"].append({"file":filename,"status":"downloaded","path":item["path"],
                                                   "size_bytes":len(blob),"sha256":digest,"weight":weight,"style":item["font_style"]})
                    print("[Google Fonts] OK:",family,filename,len(blob))
                except Exception as font_exc:
                    family_report["fonts"].append({"file":filename,"status":"failed","reason":str(font_exc)[:240]})
            family_report["downloaded_count"]=sum(x.get("status")=="downloaded" for x in family_report["fonts"])
            family_report["status"]="downloaded" if family_report["downloaded_count"] else "no_valid_font_downloaded"
        except Exception as family_exc:
            family_report["status"]="failed"
            family_report["reason"]=str(family_exc)[:300]
            print("[Google Fonts] family failed:",slug,str(family_exc))
        report.append(family_report)
        time.sleep(.18)
    return report


def sanitize_cc0_svg(data):
    """Strip active SVG elements, event handlers and external resources."""
    import xml.etree.ElementTree as ET
    if not data or len(data)>2*1024*1024:
        raise RuntimeError("SVG is empty or exceeds the 2 MiB safety limit")
    text=data.decode("utf-8","replace")
    if "<!doctype" in text.lower() or "<!entity" in text.lower():
        raise RuntimeError("SVG with a DOCTYPE/entity declaration is not accepted")
    try:
        root=ET.fromstring(text)
    except ET.ParseError as exc:
        raise RuntimeError("SVG XML is invalid") from exc
    if root.tag.rsplit("}",1)[-1].lower()!="svg":
        raise RuntimeError("Downloaded XML root is not an SVG element")
    dangerous={"script","foreignobject","iframe","object","embed","audio","video","applet"}
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag.rsplit("}",1)[-1].lower() in dangerous:
                parent.remove(child)
    for elem in root.iter():
        for attr in list(elem.attrib):
            local=attr.rsplit("}",1)[-1].lower()
            value=str(elem.attrib.get(attr) or "").strip()
            if local.startswith("on"):
                del elem.attrib[attr]
            elif local in {"href","src"} and value and not value.startswith("#"):
                del elem.attrib[attr]
            elif "url(" in value.lower():
                urls=re.findall(r"url\(\s*['\"]?([^)'\" ]+)",value,flags=re.IGNORECASE)
                if any(not target.startswith("#") for target in urls):
                    del elem.attrib[attr]
        if elem.tag.rsplit("}",1)[-1].lower()=="style" and elem.text:
            if "@import" in elem.text.lower() or re.search(r"url\(\s*['\"]?(?!#)",elem.text,flags=re.IGNORECASE):
                elem.text=""
    cleaned=ET.tostring(root,encoding="utf-8",xml_declaration=True)
    low=cleaned.lower()
    if b"<script" in low or b"javascript:" in low:
        raise RuntimeError("Active content remained after SVG sanitization")
    return cleaned


def download_wikimedia_vector_svg(root,index):
    """Bundle small Commons vectors only when exact file metadata says CC0 or Public Domain."""
    report=[]; total=0; cap=45; seen=set()
    queries=[
        ("world-maps","world map countries svg filetype:svg"),
        ("historical-maps","historical map outline svg filetype:svg"),
        ("science-diagrams","physics scientific diagram svg filetype:svg"),
        ("chemistry","chemical structure molecule diagram svg filetype:svg"),
        ("biology","botanical biology anatomy illustration svg filetype:svg"),
        ("astronomy","astronomy star chart planet diagram svg filetype:svg"),
        ("architecture","architecture section plan elevation svg filetype:svg"),
        ("engineering","engineering schematic circuit diagram svg filetype:svg"),
        ("transit","transit network railway route map svg filetype:svg"),
        ("music","music notation instrument diagram svg filetype:svg"),
        ("geography","topographic contour geographic map svg filetype:svg"),
        ("infographic","flowchart cycle infographic diagram svg filetype:svg"),
        ("geometric","geometric pattern ornament svg filetype:svg"),
        ("education","educational diagram school science svg filetype:svg"),
        ("environment","renewable energy ecology diagram svg filetype:svg")
    ]
    for category,q in queries:
        if total>=cap: break
        url="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({
            "action":"query","format":"json","generator":"search","gsrsearch":q,"gsrnamespace":6,"gsrlimit":25,
            "prop":"imageinfo","iiprop":"url|extmetadata|size|mime"
        })
        success=0; checked=0
        try:
            response=request_json(url,timeout=16)
            pages=(response.get("query") or {}).get("pages") or {}
            for page in pages.values():
                if total>=cap or success>=3 or checked>=16: break
                info=(page.get("imageinfo") or [{}])[0]
                if not isinstance(info,dict): continue
                meta=info.get("extmetadata") or {}
                short=str((meta.get("LicenseShortName") or {}).get("value") or "").strip()
                if not wikimedia_license_is_eligible(short): continue
                file_url=str(info.get("url") or "")
                parsed=urllib.parse.urlparse(file_url)
                ext=Path(parsed.path).suffix.lower()
                mime=str(info.get("mime") or "").lower()
                byte_size=int(info.get("size") or 0)
                allowed_mimes={"image/svg+xml","application/svg+xml","text/xml","application/xml","application/octet-stream"}
                if parsed.scheme!="https" or parsed.hostname!="upload.wikimedia.org" or ext!=".svg": continue
                if mime not in allowed_mimes or byte_size<100 or byte_size>2*1024*1024: continue
                identity=str(page.get("pageid") or page.get("title") or "")
                if not identity or identity in seen: continue
                seen.add(identity); checked+=1
                try:
                    blob,ctype=request_bytes(file_url,timeout=18,limit=2*1024*1024)
                    mime2=ctype.split(";")[0].strip().lower()
                    if mime2 not in allowed_mimes:
                        raise RuntimeError("media endpoint returned a non-SVG MIME type")
                    cleaned=sanitize_cc0_svg(blob)
                    title=str((meta.get("ObjectName") or {}).get("value") or page.get("title") or identity)
                    target_dir=root/"third-party/wikimedia"/"svg"
                    target_dir.mkdir(parents=True,exist_ok=True)
                    target=target_dir/(f"{category}-{slugify(title)[:48]}-{slugify(identity)}.svg")
                    target.write_bytes(cleaned)
                    digest=sha256_path(target)
                    creator=str((meta.get("Artist") or {}).get("value") or (meta.get("Credit") or {}).get("value") or "")
                    page_url=str(info.get("descriptionurl") or ("https://commons.wikimedia.org/wiki/"+urllib.parse.quote(str(page.get("title") or "").replace(" ","_"))))
                    license_url=str((meta.get("LicenseUrl") or {}).get("value") or info.get("descriptionurl") or "https://commons.wikimedia.org/wiki/Commons:Licensing")
                    entry={"id":"wikimedia-svg-"+slugify(identity),"path":target.relative_to(root).as_posix(),
                           "type":"wikimedia-cc0-svg","category":category,"title":title,"creator":creator,
                           "source_page":page_url,"source_file_url":file_url,"license":short,"license_url":license_url,
                           "license_verified_from_item_metadata":True,"redistributable":True,"sanitized_svg":True,
                           "size_bytes":len(cleaned),"sha256":digest,
                           "note":"Exact Commons metadata marked CC0/Public Domain; active elements and external references are removed."}
                    index.append(entry); total+=1; success+=1
                    report.append({"id":entry["id"],"status":"downloaded","category":category,"title":title,
                                   "path":entry["path"],"source_page":page_url,"license":short,
                                   "size_bytes":len(cleaned),"sha256":digest})
                    print("[Wikimedia SVG] OK:",category,title[:42],short,len(cleaned))
                except Exception as item_exc:
                    report.append({"id":"wikimedia-svg-"+slugify(identity),"status":"failed","category":category,
                                   "title":str(page.get("title") or identity),"reason":str(item_exc)[:300],
                                   "source_page":info.get("descriptionurl")})
            time.sleep(.35)
            if not success:
                report.append({"id":"wikimedia-svg-"+category,"status":"no_eligible_svg","category":category,
                               "query":q,"source_page":"https://commons.wikimedia.org/wiki/Commons:Licensing",
                               "reason":"No small, correctly licensed and sanitizable SVG passed item-level checks."})
        except Exception as exc:
            report.append({"id":"wikimedia-svg-"+category,"status":"failed","category":category,
                           "query":q,"reason":str(exc)[:300],"source_page":"https://commons.wikimedia.org/wiki/Commons:Licensing"})
    return report


def download_wikimedia_video_audio(root,index):
    """Bundle a small set of video/audio files only when the Commons file page explicitly marks CC0 or Public Domain."""
    report=[]; total=0; total_videos=0; total_audio=0; cap=20; seen=set()
    queries=[
        ("spaceflight","video spaceflight rocket launch filetype:video"),
        ("earth-observation","video satellite Earth clouds filetype:video"),
        ("nature","wildlife nature landscape filetype:video"),
        ("ocean","ocean underwater marine filetype:video"),
        ("weather","storm lightning aurora filetype:video"),
        ("architecture","historic architecture city filetype:video"),
        ("astronomy","star trails night sky time lapse filetype:video"),
        ("science","microscopy laboratory scientific demonstration filetype:video"),
        ("birds","bird song nature field recording filetype:audio"),
        ("ocean-audio","ocean waves rain wind ambience filetype:audio"),
        ("industrial-audio","machine workshop field recording filetype:audio"),
        ("ambience-audio","forest city ambience field recording filetype:audio")
    ]
    for category,q in queries:
        if total>=cap: break
        is_audio=category.endswith("-audio") or category=="birds"
        kind="audio" if is_audio else "video"
        extensions={".mp3",".wav",".ogg",".flac",".m4a",".oga"} if is_audio else {".mp4",".m4v",".mov",".webm",".ogv"}
        cap_size=8*1024*1024 if is_audio else 18*1024*1024
        params={"action":"query","format":"json","generator":"search","gsrsearch":q,"gsrnamespace":6,"gsrlimit":25,
                "prop":"imageinfo","iiprop":"url|extmetadata|size|mime"}
        url="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(params)
        successes=0; checked=0
        try:
            response=request_json(url,timeout=18)
            pages=(response.get("query") or {}).get("pages") or {}
            for page in pages.values():
                if total>=cap or successes>=3 or checked>=18: break
                imageinfo=(page.get("imageinfo") or [{}])[0]
                if not isinstance(imageinfo,dict): continue
                meta=imageinfo.get("extmetadata") or {}
                short=str((meta.get("LicenseShortName") or {}).get("value") or "").strip()
                if not wikimedia_license_is_eligible(short):
                    continue
                file_url=str(imageinfo.get("url") or "")
                parsed=urllib.parse.urlparse(file_url)
                ext=Path(parsed.path).suffix.lower()
                mime=str(imageinfo.get("mime") or "").lower()
                byte_size=int(imageinfo.get("size") or 0)
                if parsed.scheme!="https" or parsed.hostname!="upload.wikimedia.org":
                    continue
                if ext not in extensions or byte_size<2048 or byte_size>cap_size:
                    continue
                if mime and mime!="application/octet-stream" and not mime.startswith("audio/" if is_audio else "video/"):
                    continue
                identity=str(page.get("pageid") or page.get("title") or "")
                if not identity or identity in seen: continue
                seen.add(identity); checked+=1
                try:
                    blob,ctype=request_bytes(file_url,timeout=25,limit=cap_size)
                    if len(blob)<2048: raise RuntimeError("file too small to be a useful media source")
                    mime2=ctype.split(";")[0].strip().lower()
                    if is_audio:
                        if not (mime2.startswith("audio/") or blob.startswith(b"RIFF") or blob.startswith(b"OggS") or blob.startswith(b"ID3")):
                            raise RuntimeError("download did not return recognizable audio data")
                        if ext==".mp3" and not (blob.startswith(b"ID3") or (len(blob)>2 and blob[0]==0xff and blob[1]&0xe0==0xe0)):
                            raise RuntimeError("MP3 signature is missing")
                        if ext in {".ogg",".oga"} and not blob.startswith(b"OggS"):
                            raise RuntimeError("Ogg signature is missing")
                        if ext==".wav" and not blob.startswith(b"RIFF"):
                            raise RuntimeError("WAV RIFF signature is missing")
                    else:
                        if not (mime2.startswith("video/") or (len(blob)>12 and blob[4:8]==b"ftyp") or blob.startswith(b"\x1a\x45\xdf\xa3") or blob.startswith(b"OggS")):
                            raise RuntimeError("download did not return recognizable video data")
                        if ext==".webm" and not blob.startswith(b"\x1a\x45\xdf\xa3"):
                            raise RuntimeError("WebM EBML signature is missing")
                        if ext in {".mp4",".m4v",".mov"} and not (len(blob)>12 and blob[4:8]==b"ftyp"):
                            raise RuntimeError("ISO BMFF video signature is missing")
                    target_dir=root/"third-party/wikimedia"/("audio" if is_audio else "video")
                    target_dir.mkdir(parents=True,exist_ok=True)
                    title=str((meta.get("ObjectName") or {}).get("value") or page.get("title") or identity)
                    filename=f"{category}-{slugify(title)[:48]}-{slugify(identity)}{ext}"
                    target=target_dir/filename
                    target.write_bytes(blob)
                    digest=sha256_path(target)
                    license_url=str((meta.get("LicenseUrl") or {}).get("value") or imageinfo.get("descriptionurl") or "https://commons.wikimedia.org/wiki/Commons:Licensing")
                    creator=str((meta.get("Artist") or {}).get("value") or (meta.get("Credit") or {}).get("value") or "")
                    description=str((meta.get("ImageDescription") or {}).get("value") or "")
                    page_url=str(imageinfo.get("descriptionurl") or ("https://commons.wikimedia.org/wiki/"+urllib.parse.quote(str(page.get("title") or "").replace(" ","_"))))
                    asset_id="wikimedia-"+kind+"-"+slugify(identity)
                    entry={"id":asset_id,"path":target.relative_to(root).as_posix(),
                           "type":"wikimedia-cc0-"+kind,"category":category,"title":title,
                           "creator":creator,"description":description[:1600],"source_page":page_url,
                           "source_file_url":file_url,"license":short,"license_url":license_url,
                           "license_verified_from_item_metadata":True,"size_bytes":len(blob),"sha256":digest,
                           "redistributable":True,
                           "note":"Bundled only because exact Commons file metadata explicitly labelled this item CC0 or Public Domain. Review contextual rights and intended use."}
                    index.append(entry); total+=1; successes+=1
                    if is_audio: total_audio+=1
                    else: total_videos+=1
                    report.append({"id":asset_id,"status":"downloaded","media_type":kind,"category":category,
                                   "path":entry["path"],"title":title,"source_page":page_url,
                                   "license":short,"size_bytes":len(blob),"sha256":digest})
                    print("[Wikimedia Commons AV] OK:",kind,category,title[:45],len(blob))
                except Exception as item_exc:
                    report.append({"id":"wikimedia-"+kind+"-"+slugify(identity),"status":"failed","media_type":kind,
                                   "category":category,"title":str(page.get("title") or identity),
                                   "reason":str(item_exc)[:300],"source_page":imageinfo.get("descriptionurl")})
            time.sleep(.45)
            if not successes:
                report.append({"id":"wikimedia-"+category,"status":"no_eligible_media","media_type":kind,
                               "category":category,"query":q,"source_page":"https://commons.wikimedia.org/wiki/Commons:Licensing",
                               "reason":"No distinct small media file passed exact license, size, host and container filters."})
        except Exception as exc:
            report.append({"id":"wikimedia-"+category,"status":"failed","media_type":kind,"category":category,
                           "query":q,"source_page":"https://commons.wikimedia.org/wiki/Commons:Licensing",
                           "reason":str(exc)[:300]})
            print("[Wikimedia Commons AV] search failed:",category,str(exc))
    return report

def download_openverse(root,index):
    # A small CC0-only fallback. The upstream host has intermittent tunnel timeouts in CI,
    # so requests are intentionally short and failures are recorded rather than retried for minutes.
    report=[]; total=0
    queries=[("image","nature","forest landscape",2),("image","science","science laboratory",2),("audio","rain","rain ambience",2)]
    for kind,category,q,limit in queries:
        endpoint=f"https://api.openverse.org/v1/{'images' if kind=='image' else 'audio'}/"
        url=endpoint+"?"+urllib.parse.urlencode({"q":q,"license":"cc0","page_size":limit,"page":1})
        try:
            data=request_json(url,timeout=10)
            for item in data.get("results",[]):
                if str(item.get("license","")).lower()!="cc0": continue
                media_url=str(item.get("url") or "")
                if not media_url.startswith("https://"): continue
                try:
                    blob,ctype=request_bytes(media_url,timeout=15,limit=MAX_MEDIA_FILE)
                    ext=openverse_extension(media_url,ctype,kind,item)
                    if not ext: raise RuntimeError("unsupported file type: "+ctype)
                    title=str(item.get("title") or item.get("id") or category)
                    ident=slugify(str(item.get("id") or hashlib.sha256(media_url.encode()).hexdigest()[:12]))
                    path=root/"third-party/openverse"/("images" if kind=="image" else "audio")/f"{category}-{slugify(title)[:36]}-{ident}{ext}"
                    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(blob)
                    digest=sha256_path(path)
                    entry={"id":"openverse-"+kind+"-"+ident,"path":path.relative_to(root).as_posix(),"type":"openverse-"+kind,
                           "title":title,"creator":item.get("creator"),"provider":item.get("provider"),"source":item.get("source"),
                           "source_url":media_url,"source_landing_url":item.get("foreign_landing_url") or item.get("detail_url") or media_url,
                           "license":"CC0","license_version":item.get("license_version"),"license_url":item.get("license_url") or CC0_URL,
                           "attribution_text":item.get("attribution"),"query":q,"size_bytes":len(blob),"sha256":digest,"redistributable":True}
                    index.append(entry); total+=1
                    report.append({"id":entry["id"],"status":"downloaded","path":entry["path"],"license":"CC0","size_bytes":len(blob)})
                    print("[Openverse] OK:",kind,category,title[:48],len(blob))
                except Exception as item_exc:
                    report.append({"id":item.get("id"),"status":"failed","reason":str(item_exc),"source_url":media_url})
            time.sleep(.2)
        except Exception as exc:
            report.append({"id":"openverse-"+category,"status":"failed","reason":str(exc),"query":q})
            print("[Openverse] quick attempt failed:",q,str(exc))
    return report



def make_asset_catalog(root,index,summary):
    cards=[]
    for item in index:
        rel=item.get("path")
        if not isinstance(rel,str) or not (root/rel).is_file(): continue
        path=Path(rel); ext=path.suffix.lower()
        title=str(item.get("title") or item.get("description") or item.get("id") or path.name)
        category=str(item.get("category") or item.get("type") or "asset")
        asset_type=str(item.get("type") or "asset")
        license_name=str(item.get("license") or "check source record")
        source=item.get("source_page") or item.get("source_landing_url") or ""
        license_url=item.get("license_url") or ""
        if ext in {".svg",".png",".jpg",".jpeg",".webp"}:
            preview=f'<img loading="lazy" alt="{html.escape(title,quote=True)}" src="{html.escape(rel,quote=True)}">'
        elif ext in {".mp4",".mov",".m4v",".webm",".ogv"}:
            preview=f'<video controls preload="metadata" playsinline src="{html.escape(rel,quote=True)}" style="width:100%;height:100%;object-fit:contain"></video>'
        elif ext in {".wav",".mp3",".ogg",".oga",".flac",".m4a"}:
            preview=f'<audio controls preload="none" src="{html.escape(rel,quote=True)}"></audio>'
        else:
            preview=f'<div class="file-preview"><span>{html.escape(ext.upper().lstrip(".") or "FILE")}</span><small>{html.escape(asset_type)}</small></div>'
        size=(root/rel).stat().st_size
        size_text=f"{size/1024:.0f} KB" if size<1024*1024 else f"{size/(1024*1024):.1f} MB"
        links=[f'<a class="file-link" href="{html.escape(rel,quote=True)}" download>Open / download</a>']
        if source: links.append(f'<a href="{html.escape(str(source),quote=True)}" target="_blank" rel="noreferrer">Source</a>')
        if license_url: links.append(f'<a href="{html.escape(str(license_url),quote=True)}" target="_blank" rel="noreferrer">License</a>')
        search=' '.join(str(item.get(k,"")) for k in ("id","title","description","category","type","creator","artist","date","department"))
        cards.append(
            f'<article class="card" data-category="{html.escape(category,quote=True)}" data-search="{html.escape(search.lower(),quote=True)}">'
            f'<div class="preview">{preview}</div><div class="body"><div class="kicker">{html.escape(category)} · {html.escape(asset_type)}</div>'
            f'<h3>{html.escape(title)}</h3><p class="meta">{html.escape(license_name)} · {size_text}</p>'
            f'<div class="links">{" ".join(links)}</div></div></article>'
        )
    counts = " · ".join(f"{html.escape(str(k))}: {html.escape(str(v))}" for k,v in summary.items() if isinstance(v,(str,int,float)))
    document="""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nolane Video Asset Library</title>
<style>
:root{{--bg:#10141b;--panel:#1a212b;--line:#354151;--text:#f2f4f8;--muted:#aab5c2;--accent:#79d5c8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}}
header{{padding:32px clamp(20px,5vw,70px);border-bottom:1px solid var(--line);background:linear-gradient(130deg,#192431,#121821 65%)}}
h1{{margin:0;font-size:clamp(28px,4vw,46px);letter-spacing:-.04em}}header p{{max-width:900px;color:var(--muted)}}.summary{{font-size:12px;color:var(--muted)}}
.controls{{position:sticky;top:0;z-index:2;display:flex;gap:12px;padding:15px clamp(16px,4vw,60px);background:#10141bf2;border-bottom:1px solid var(--line)}}
input,select{{min-width:0;background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:12px;font:inherit}}input{{flex:1}}
main{{padding:24px clamp(16px,4vw,60px) 65px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.card{{min-width:0;overflow:hidden;border:1px solid var(--line);border-radius:15px;background:var(--panel);display:flex;flex-direction:column}}
.preview{{height:190px;background:#111923;display:flex;align-items:center;justify-content:center;overflow:hidden;border-bottom:1px solid var(--line)}}
.preview img{{width:100%;height:100%;object-fit:contain;background:#111923}}.preview audio{{width:90%}}.file-preview{{width:100%;height:100%;display:flex;flex-direction:column;gap:8px;align-items:center;justify-content:center;color:var(--accent);background:radial-gradient(circle at 50% 40%,#283748,#111923)}}.file-preview span{{font-size:28px;font-weight:750;letter-spacing:.07em}}.file-preview small{{color:var(--muted)}}
.body{{padding:15px;display:flex;flex-direction:column;flex:1}}.kicker{{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);overflow-wrap:anywhere}}h3{{font-size:16px;line-height:1.3;margin:8px 0 6px;overflow-wrap:anywhere}}.meta{{font-size:12px;color:var(--muted);margin:0 0 15px}}.links{{display:flex;gap:12px;flex-wrap:wrap;margin-top:auto}}a{{color:var(--accent);font-size:12px;text-decoration:none}}a:hover{{text-decoration:underline}}.file-link{{font-weight:700}}#count{{color:var(--muted);font-size:13px;margin:0 0 12px}}footer{{padding:24px clamp(16px,4vw,60px);border-top:1px solid var(--line);color:var(--muted);font-size:12px}}
@media(max-width:600px){{.controls{{flex-direction:column}}.preview{{height:160px}}}}
</style></head><body>
<header><h1>Nolane · Video Asset Library</h1>
<p>Offline catalog of original vector environments, transparent motion overlays, reusable infographic frames, synthesized sound effects, and third-party media whose item-level license was verified for redistribution. Pick resources by the visual need of the shot, not by genre alone.</p>
<p class="summary">__CATALOG_COUNTS__</p></header>
<div class="controls"><input id="search" type="search" placeholder="Search assets, topics, creators, types…"><select id="category"><option value="">All categories</option></select></div>
<main><p id="count"></p><div class="grid" id="grid">__CATALOG_CARDS__</div></main>
<footer>License and provenance data lives in ASSET_INDEX.json and SOURCES_AND_LICENSES.md. A source link does not itself grant raw-file redistribution rights. Verify the asset is suitable for the actual video and honor any rights or context limitations.</footer>
<script>
const cards=[...document.querySelectorAll('.card')], search=document.querySelector('#search'), select=document.querySelector('#category'), count=document.querySelector('#count');
const categories=[...new Set(cards.map(c=>c.dataset.category).filter(Boolean))].sort();
for(const c of categories){const o=document.createElement('option');o.value=c;o.textContent=c;select.append(o)}
function filter(){const q=search.value.trim().toLowerCase(),cat=select.value;let n=0;for(const c of cards){const ok=(!q||c.dataset.search.includes(q))&&(!cat||c.dataset.category===cat);c.hidden=!ok;if(ok)n++}count.textContent=n+' assets shown';}
search.addEventListener('input',filter);select.addEventListener('change',filter);filter();
</script></body></html>"""
    document=document.replace("__CATALOG_COUNTS__",counts).replace("__CATALOG_CARDS__","".join(cards))
    write_text(root/"ASSET_CATALOG.html",document)

def main():
    if STAGE.exists(): shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    index=[]
    generate_originals(STAGE,index)
    texture_count=generate_original_textures(STAGE,index)
    illustration_count=generate_original_illustrations(STAGE,index)
    motion_loop_count=generate_original_motion_loops(STAGE,index)
    print("[Originals] generated",len(index),"original vector/audio assets plus",texture_count,"tileable textures,",illustration_count,"editorial illustrations and",motion_loop_count,"verified motion loops")
    kenney_report=download_kenney(STAGE,index)
    polyhaven_report=download_polyhaven(STAGE,index)
    met_report=download_met_open_access(STAGE,index)
    smithsonian_report=download_smithsonian_open_access(STAGE,index)
    rijksmuseum_report=download_rijksmuseum_open_access(STAGE,index)
    nasa_report=download_nasa_media(STAGE,index)
    loc_report=download_loc_public_domain(STAGE,index)
    wikimedia_report=download_wikimedia_public_domain(STAGE,index)
    wikimedia_svg_report=download_wikimedia_vector_svg(STAGE,index)
    wikimedia_av_report=download_wikimedia_video_audio(STAGE,index)
    openverse_report=download_openverse(STAGE,index)
    write_text(STAGE/"SOURCES_AND_LICENSES.md",
      "# Sources and licenses\n\n"
      "## Original vector and sound assets\nAll SVG backgrounds, overlays, icons, large-format editorial illustrations, infographic templates, tileable vector textures and procedural WAV sound effects in originals/ were generated by this repository and are dedicated to CC0 1.0: "+CC0_URL+"\n\n"
      "## Kenney CC0 pack source links\nThe official pages mark these packs CC0, but the current website uses a browser-driven download step. This automated build does not guess direct ZIP URLs; the source links remain in video-library/assets/sources.json. Status:\n\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('source_page','')} — {r.get('reason','')}" for r in kenney_report)+"\n\n"
      "## Poly Haven CC0 assets\nThe build downloads compact HDRIs, Blender models plus listed dependencies, and PBR texture maps from the official API. The API has separate terms asking tools that use the live API to make clear the assets' source. See https://polyhaven.com/license and https://github.com/Poly-Haven/Public-API/blob/master/ToS.md.\n\n"+
      "\n".join(f"- {r.get('title',r.get('id'))}: {r.get('status')} — {r.get('source_page','')}" + (f" — {r.get('reason')}" if r.get('reason') else "") for r in polyhaven_report)+
      "\n\n## The Met Open Access images\nThe build uses the current paginated v1.1 search API, then independently checks isPublicDomain on every object detail before fetching the actual image from an official Met image host. The Met's Open Access artworks are CC0; object page, title, artist and date are preserved per image. Source: https://www.metmuseum.org/hubs/open-access.\n\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('source_page',r.get('reason',''))}" for r in met_report)+
      "\n\n## Smithsonian Open Access CC0 media\nThe builder queries Smithsonian Open Access and only considers records whose top-level metadata_usage.access is exactly CC0. It then checks each candidate media object's usage.access independently and downloads only media explicitly marked CC0. The official IDS image delivery service is requested at a bounded size; source record, unit, title, creator, media URL, exact rights values and SHA-256 are kept. A caller may configure the optional GitHub Actions secret SMITHSONIAN_API_KEY; if absent, the builder makes a low-volume attempt with DEMO_KEY and records any rate-limit/authentication failure rather than claiming success. CC0 does not grant trademark, privacy, publicity or other non-copyright rights. Sources: https://www.si.edu/openaccess/faq and https://www.si.edu/openaccess/devtools.\n\n"+      "\n\n## Rijksmuseum Open Access collection\nThe builder harvests the official Rijksmuseum OAI-PMH EDM feed without an API key, but downloads only images whose own record exposes an explicit Creative Commons CC0 or Public Domain Mark rights URL. Image requests use the Rijksmuseum's official IIIF endpoint at a bounded size; record identifiers, title, creator, exact rights statement, source URL and SHA-256 are retained. CC BY and ambiguous/missing rights are not bundled by this lane. The museum requests source credit where possible. Sources: https://data.rijksmuseum.nl/docs/oai-pmh, https://data.rijksmuseum.nl/docs/iiif and https://data.rijksmuseum.nl/policy/.\n\n"+      "\n\n## NASA Image and Video Library media\nThe builder searches the official NASA Image and Video Library API for small images, video clips, and audio files. It only accepts records attributed to a NASA center, rejects copyright/third-party-rights markers and NASA insignia/logo assets, skips obvious identifiable-person keyword categories, checks the official NASA media manifest and media container, and preserves the item page, media URL, source credit, rights basis and SHA-256. NASA media is not labelled CC0: NASA says its media is generally not copyrighted in the United States, but third-party marked content, endorsement, logo and privacy/publicity constraints still apply. Review each selection before a commercial or promotional use. Source: https://www.nasa.gov/nasa-brand-center/images-and-media/.\n\n"+
      "\n\n## Library of Congress photographs\nThe builder downloads only image records with an explicit item-level rights statement containing ‘No known restrictions on publication’, ‘Public Domain’, or ‘No known copyright restrictions’, and rejects explicit conflicting limitations. Records without a rights statement are skipped. Each selected file records the exact statement, item URL, direct image URL, and SHA-256. LOC notes users remain responsible for evaluating copyright and other rights, so inspect the item/context before publication. Sources: https://www.loc.gov/apis/json-and-yaml/ and https://ask.loc.gov/faq/305466.\n\n"+
      "\n\n## Wikimedia Commons images, video and audio\nOnly file-level metadata explicitly labelled CC0 or Public Domain is auto-bundled. CC BY, CC BY-SA, NC, missing, or ambiguous licenses are skipped. Images, small video clips and audio files are bundled only when exact file-level metadata explicitly labels them CC0 or Public Domain. Video/audio downloads are limited by byte size, official upload.wikimedia.org host, filename extension, MIME type and recognizable container signature; records retain creator, source page, license URL and SHA-256. Source: https://commons.wikimedia.org/wiki/Commons:Licensing.\n\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('source_page',r.get('reason',''))}" for r in wikimedia_report)+
      "\n\n## Wikimedia Commons vector SVG download results\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('source_page',r.get('reason',''))}" for r in wikimedia_svg_report)+
      "\n\n## Wikimedia Commons video/audio download results\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('source_page',r.get('reason',''))}" for r in wikimedia_av_report)+
      "\n\n## Openverse CC0 fallback\nThe builder makes only short requests to Openverse and bundles exact-CC0 results only. Any timeout or unsupported file is explicitly recorded. It does not relabel CC-BY, NC, or unknown-license material as CC0.\n\n"+
      "\n".join(f"- {r.get('id')}: {r.get('status')} — {r.get('reason','')}" for r in openverse_report if r.get("status")!="downloaded")+
      "\n\n## Source-only libraries\n- [Pexels License](https://www.pexels.com/license/) — use suitable footage in composed videos under its terms; do not bundle raw content as a standalone stock collection.\n- [Mixkit licenses](https://mixkit.co/license/) — check each item type and item-specific license; restricted stock items must not be treated as freely redistributable.\n- [ambientCG](https://ambientcg.com/) — its materials are published as CC0; the full site is not mirrored by this build.\n- [Kenney](https://kenney.nl/assets) — official CC0 pack catalog; source links remain available even though the current download interaction is not automated.\n- [Google Fonts](https://fonts.google.com/) — inspect the selected family's exact license and preserve its license file if redistributing font binaries.\n\n## Review gate\nThe asset bundle is a source pool, not an automatically approved finished video. Review visual suitability, audio levels, model dependencies, content, metadata and exact license provenance before publication."
    )
    summary={"original_backgrounds":len(PALETTES),"original_overlays":len(OVERLAYS),"original_icons":len(ICONS),
              "original_textures":len(TEXTURES),
              "original_illustrations":len(ILLUSTRATIONS),
              "original_motion_loops":len(MOTION_LOOPS),
              "original_infographics":len(INFO),"original_sfx":len([x for x in index if x.get("type")=="original-procedural-sfx"]),
              "kenney_packs_attempted":len(kenney_report),"kenney_packs_downloaded":sum(r.get("status")=="downloaded" for r in kenney_report),
              "polyhaven_packages_downloaded":sum(r.get("status")=="downloaded" for r in polyhaven_report),
              "polyhaven_files_downloaded":sum(1 for x in index if str(x.get("type","")).startswith("polyhaven-")),
              "met_images_downloaded":sum(r.get("status")=="downloaded" for r in met_report),
              "smithsonian_images_downloaded":sum(r.get("status")=="downloaded" for r in smithsonian_report),
              "rijksmuseum_images_downloaded":sum(r.get("status")=="downloaded" for r in rijksmuseum_report),
              "nasa_images_downloaded":sum(x.get("status")=="downloaded" and x.get("media_type")=="image" for x in nasa_report),
              "nasa_videos_downloaded":sum(x.get("status")=="downloaded" and x.get("media_type")=="video" for x in nasa_report),
              "nasa_audio_downloaded":sum(x.get("status")=="downloaded" and x.get("media_type")=="audio" for x in nasa_report),
              "loc_images_downloaded":sum(r.get("status")=="downloaded" for r in loc_report),
              "wikimedia_images_downloaded":sum(r.get("status")=="downloaded" for r in wikimedia_report),
              "wikimedia_svgs_downloaded":sum(r.get("status")=="downloaded" for r in wikimedia_svg_report),
              "wikimedia_videos_downloaded":sum(r.get("status")=="downloaded" and r.get("media_type")=="video" for r in wikimedia_av_report),
              "wikimedia_audio_downloaded":sum(r.get("status")=="downloaded" and r.get("media_type")=="audio" for r in wikimedia_av_report),
              "openverse_items_downloaded":sum(r.get("status")=="downloaded" for r in openverse_report)}
    index_doc={"schema_version":"1.0.0","built_at":datetime.now(timezone.utc).isoformat(),
               "repository":"https://github.com/Nolane-x/video",
               "policy":"Original assets are CC0; third-party bundles require explicit item-level CC0/Public Domain rights statements. NASA-origin media is separately filtered against official NASA Media Usage Guidelines and explicit copyright markers; its policy is not CC0. Source-only libraries are not raw-bundled.",
               "summary":summary,"original_assets_license":{"license":CC0,"license_url":CC0_URL},
               "kenney_downloads":kenney_report,"polyhaven_downloads":polyhaven_report,
               "met_open_access_downloads":met_report,"smithsonian_open_access_downloads":smithsonian_report,
               "rijksmuseum_open_access_downloads":rijksmuseum_report,
               "nasa_media_downloads":nasa_report,
               "loc_public_domain_downloads":loc_report,"wikimedia_public_domain_downloads":wikimedia_report,
               "wikimedia_vector_svg_downloads":wikimedia_svg_report,
               "wikimedia_video_audio_downloads":wikimedia_av_report,
               "openverse_downloads":openverse_report,"assets":index}
    write_text(STAGE/"ASSET_INDEX.json",json.dumps(index_doc,ensure_ascii=False,indent=2)+"\n")
    make_asset_catalog(STAGE,index,summary)

    # Index and checksum ledger intentionally do not hash themselves; all actual resources,
    # source/license notes, and the offline catalog are included in the ledger.
    digest_lines=[]
    for path in sorted(STAGE.rglob("*")):
        if path.is_file() and path.name not in {"ASSET_INDEX.json","SHA256SUMS.txt"}:
            digest_lines.append(f"{sha256_path(path)}  {path.relative_to(STAGE).as_posix()}")
    summary["checksummed_files"]=len(digest_lines)
    index_doc["summary"]=summary
    write_text(STAGE/"ASSET_INDEX.json",json.dumps(index_doc,ensure_ascii=False,indent=2)+"\n")
    write_text(STAGE/"SHA256SUMS.txt","\n".join(digest_lines)+"\n")
    assert len(PALETTES)>=60 and len(OVERLAYS)>=50 and len(ICONS)>=90 and len(INFO)>=35 and len(TEXTURES)>=30 and len(ILLUSTRATIONS)>=50 and len(MOTION_LOOPS)>=10
    expected=len(PALETTES)+len(OVERLAYS)+len(ICONS)+len(INFO)+len(TEXTURES)+len(ILLUSTRATIONS)
    assert len(list((STAGE/"originals").rglob("*.svg")))==expected
    indexed={line.split("  ",1)[1] for line in digest_lines}
    for path in STAGE.rglob("*"):
        if path.is_file() and path.name not in {"SHA256SUMS.txt"}:
            if path.relative_to(STAGE).as_posix() not in indexed and path.name!="ASSET_INDEX.json":
                raise RuntimeError("checksum missing for "+str(path))
    OUT.mkdir(parents=True,exist_ok=True)
    archive=OUT/"video-asset-library.zip"
    if archive.exists(): archive.unlink()
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file(): z.write(path,Path("video-asset-library")/path.relative_to(STAGE))
    archive_sha=sha256_path(archive)
    write_text(OUT/"VIDEO_ASSET_LIBRARY_BUILD.txt",f"built_at={index_doc['built_at']}\nzip={archive.name}\nzip_sha256={archive_sha}\nzip_size_bytes={archive.stat().st_size}\nsummary={json.dumps(summary)}\n")
    print(json.dumps(summary,indent=2))
    print(f"[Package] {archive} size={archive.stat().st_size} SHA256={archive_sha}")
if __name__=="__main__":
    main()
