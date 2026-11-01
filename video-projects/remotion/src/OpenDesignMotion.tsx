import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import "@fontsource-variable/inter";
import "@fontsource-variable/space-grotesk";

const W = 1920;
const H = 1080;
const TOTAL = 1119;
const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const full: React.CSSProperties = { width: "100%", height: "100%", overflow: "hidden", position: "relative", fontFamily: "Inter Variable, Inter, sans-serif" };
const displayFont = "Space Grotesk Variable, Inter Variable, sans-serif";
const ink = "#111315";
const green = "#b9ed4a";

const e = (f: number, a: number, b: number, x0 = 0, x1 = 1) =>
  interpolate(f, [a, b], [x0, x1], { ...clamp, easing: Easing.out(Easing.cubic) });
const fadeOut = (f: number, end: number, span = 10) => 1 - e(f, end - span, end);
const pop = (f: number, fps = 30, delay = 0, stiffness = 130, damping = 16) =>
  spring({ frame: Math.max(0, f - delay), fps, config: { stiffness, damping, mass: 0.8 } });

const Word = ({
  children,
  size,
  color = ink,
  weight = 850,
  tracking = -0.065,
  line = 0.88,
  italic = false,
  style = {},
}: {
  children: React.ReactNode;
  size: number;
  color?: string;
  weight?: number;
  tracking?: number;
  line?: number;
  italic?: boolean;
  style?: React.CSSProperties;
}) => (
  <div style={{
    fontFamily: displayFont,
    fontSize: size,
    fontWeight: weight,
    color,
    letterSpacing: tracking + "em",
    lineHeight: line,
    fontStyle: italic ? "italic" : "normal",
    whiteSpace: "nowrap",
    ...style,
  }}>{children}</div>
);

const Noise = ({ opacity = 0.09 }: { opacity?: number }) => (
  <svg viewBox="0 0 1920 1080" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity, pointerEvents: "none" }}>
    <filter id="grain-filter">
      <feTurbulence type="fractalNoise" baseFrequency="0.82" numOctaves="3" seed="13" />
      <feColorMatrix type="saturate" values="0" />
    </filter>
    <rect width="1920" height="1080" filter="url(#grain-filter)" opacity="0.55" />
  </svg>
);

const RadialMark = ({ frame = 0, size = 112, color = "#f06a51" }: { frame?: number; size?: number; color?: string }) => (
  <svg width={size} height={size} viewBox="0 0 200 200" style={{ display: "block", flex: "none", transform: "rotate(" + (frame * 0.7) + "deg)" }}>
    <defs>
      <radialGradient id="mark-grad" cx="34%" cy="24%" r="80%">
        <stop offset="0%" stopColor="#ffb19e" />
        <stop offset="100%" stopColor={color} />
      </radialGradient>
    </defs>
    <polygon points="100,5 113,70 150,18 130,82 190,55 144,101 199,115 137,125 175,184 118,145 100,199 82,145 25,184 63,125 1,115 56,101 10,55 70,82 50,18 87,70" fill="url(#mark-grad)" />
    <circle cx="100" cy="101" r="13" fill="#fff6ed" />
  </svg>
);

const PlayGlyph = ({ size = 54, color = "#fff" }: { size?: number; color?: string }) => (
  <svg viewBox="0 0 100 100" width={size} height={size} style={{ display: "block" }}>
    <path d="M33 18 Q24 13 24 29 V71 Q24 87 38 78 L81 55 Q94 48 81 41Z" fill={color} />
  </svg>
);

const CloudSky = ({ frame }: { frame: number }) => {
  const drift = frame * 0.28;
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg,#68afe1 0%,#98cce5 35%,#d6e6e4 61%,#edcbbd 100%)" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 51% 37%,rgba(255,255,255,.58),transparent 52%),linear-gradient(115deg,rgba(255,245,223,.16),transparent 45%,rgba(255,255,255,.22))" }} />
      <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
        <defs>
          <linearGradient id="sky-cloud" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#fff" stopOpacity=".86" />
            <stop offset="100%" stopColor="#fff" stopOpacity=".12" />
          </linearGradient>
          <filter id="sky-soft-cloud"><feGaussianBlur stdDeviation="18" /></filter>
          <filter id="sky-haze"><feGaussianBlur stdDeviation="44" /></filter>
        </defs>
        <g opacity=".52" filter="url(#sky-haze)" transform={"translate(" + (drift * -0.55) + ",0)"}>
          <path d="M-100 260 C80 125 245 135 360 245 C505 110 675 150 765 265 C905 140 1100 165 1190 282 C1340 165 1480 175 1600 270 C1740 150 1900 160 2020 290 L2020 490 L-100 490Z" fill="#fff" />
          <path d="M-180 610 C20 485 205 512 330 620 C485 485 630 495 790 640 C940 490 1115 515 1235 625 C1370 525 1550 520 1680 640 C1800 545 1940 560 2060 650 L2060 820 L-180 820Z" fill="#fff1e5" />
        </g>
        <g opacity=".66" filter="url(#sky-soft-cloud)" transform={"translate(" + drift + ",0)"}>
          <path d="M-80 310 C60 205 180 200 310 295 C430 160 595 160 710 290 C850 188 1000 212 1105 310 C1270 196 1445 204 1545 322 C1705 205 1860 245 2000 350 L2000 435 L-80 435Z" fill="url(#sky-cloud)" />
          <path d="M-120 740 C20 640 175 632 305 720 C430 605 590 610 710 738 C860 620 1040 635 1150 745 C1315 638 1460 640 1590 754 C1740 654 1900 672 2030 780 L2030 875 L-120 875Z" fill="#fff7ef" opacity=".7" />
        </g>
        <path d="M0 810 C230 792 350 812 515 806 C740 800 840 825 1030 812 C1270 792 1385 808 1560 798 C1710 790 1810 808 1920 795 L1920 910 L0 910Z" fill="#7eb5bf" opacity=".25" />
        <path d="M0 845 C260 812 395 858 590 832 C810 804 965 850 1160 827 C1365 802 1555 840 1730 822 C1810 814 1870 820 1920 816 L1920 1080 L0 1080Z" fill="url(#sky-cloud)" opacity=".52" />
        <path d="M0 1005 C180 968 325 1003 495 982 C690 960 810 1004 995 981 C1190 954 1320 990 1510 971 C1700 952 1805 984 1920 961 L1920 1080 L0 1080Z" fill="#e8bfb2" opacity=".38" />
      </svg>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg,transparent 65%,rgba(244,220,207,.46))" }} />
      <Noise opacity={0.055} />
    </AbsoluteFill>
  );
};

const OpeningScene = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const card = pop(f, fps, 4, 80, 22);
  const text = "Introducing OpenDesign Motion";
  const count = Math.floor(e(f, 17, 64, 0, text.length));
  const pressed = e(f, 76, 82);
  const cursor = e(f, 48, 76, 0, 1);
  return (
    <AbsoluteFill style={full}>
      <CloudSky frame={f} />
      <div style={{ position: "absolute", top: 82, left: 0, right: 0, display: "flex", justifyContent: "center", alignItems: "center", color: "#1e292c" }}>
        <div style={{ fontFamily: "Georgia,serif", fontSize: 76, fontWeight: 700, letterSpacing: "-.05em", position: "relative", zIndex: 2 }}>
          Let’s create <span style={{ position: "relative", display: "inline-block" }}>
            <span style={{ position: "absolute", left: -5, right: -8, top: "55%", height: 30, background: "#b7e95a", transform: "rotate(-1.2deg)" }} />
            <span style={{ position: "relative" }}>Motion design</span>
          </span>
        </div>
      </div>
      <div style={{ position: "absolute", top: 184, left: 0, right: 0, textAlign: "center", color: "rgba(35,52,58,.68)", fontSize: 14, letterSpacing: ".09em", fontWeight: 600 }}>
        Good work starts here
      </div>
      <div style={{
        position: "absolute",
        left: 325,
        right: 325,
        top: 565,
        height: 210,
        background: "rgba(255,255,255,.91)",
        border: "1px solid rgba(255,255,255,.98)",
        borderRadius: 23,
        boxShadow: "0 27px 75px rgba(49,82,91,.18),0 4px 16px rgba(40,72,82,.09)",
        backdropFilter: "blur(22px)",
        transform: "translateY(" + ((1 - card) * 95) + "px) scale(" + (0.96 + 0.04 * card - pressed * 0.012) + ")",
        opacity: e(f, 4, 15),
        padding: "31px 38px",
        boxSizing: "border-box",
      }}>
        <div style={{ color: "#8c9798", fontSize: 14, fontWeight: 850, letterSpacing: ".17em", marginBottom: 23 }}>CREATE A MOTION DESIGN</div>
        <div style={{ color: "#252c30", fontSize: 36, fontWeight: 550, letterSpacing: "-.035em", minHeight: 40 }}>
          {text.slice(0, count)}
          <span style={{ display: "inline-block", width: 2, height: 29, background: count < text.length ? "#313a3d" : "transparent", verticalAlign: "middle", marginLeft: 3 }} />
        </div>
        <div style={{ position: "absolute", bottom: 20, left: 38, display: "flex", alignItems: "center", gap: 18 }}>
          <div style={{ fontSize: 13, color: "#9ca5a4" }}>◉</div>
          <div style={{ fontSize: 13, color: "#9ca5a4" }}>⌁</div>
          <div style={{ background: "#d9f5d9", color: "#26763d", padding: "7px 15px", borderRadius: 7, fontSize: 14, fontWeight: 850 }}>✦ Motion design</div>
          <div style={{ fontSize: 13, color: "#8e9998" }}>Working directory</div>
        </div>
        <div style={{ position: "absolute", right: 32, bottom: 24, width: 48, height: 48, borderRadius: "50%", background: "#12191b", display: "grid", placeItems: "center", transform: "scale(" + (1 - pressed * .09) + ")", boxShadow: "0 4px 14px rgba(20,30,31,.22)" }}>
          <svg viewBox="0 0 30 30" width="23" height="23"><path d="M5 15H24M16 6L25 15L16 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" /></svg>
        </div>
      </div>
      <div style={{ position: "absolute", top: 785, left: 620 + cursor * 640, width: 29, height: 38, filter: "drop-shadow(0 3px 3px rgba(0,0,0,.3))" }}>
        <svg viewBox="0 0 30 40" width="29" height="38"><path d="M2 2L2 33L10 25L17 38L23 35L16 22L28 22Z" fill="#fff" stroke="#262b2d" strokeWidth="2" strokeLinejoin="round" /></svg>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 74, textAlign: "center", color: "#edf4f4", fontSize: 16, fontWeight: 750, letterSpacing: ".22em", textShadow: "0 2px 12px rgba(20,55,72,.32)" }}>
        IDEAS IN MOTION / 01
      </div>
    </AbsoluteFill>
  );
};

const HeroTitle = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = pop(f, fps, 0, 74, 17);
  const opacity = fadeOut(f, 45, 9);
  return (
    <AbsoluteFill style={full}>
      <CloudSky frame={f + 110} />
      <div style={{ position: "absolute", top: 116, left: 0, right: 0, textAlign: "center", opacity: e(f, 0, 12), color: "#fff", fontSize: 18, fontWeight: 800, letterSpacing: ".28em", textShadow: "0 2px 10px rgba(0,0,0,.12)" }}>INTRODUCING</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 306, display: "flex", flexDirection: "column", alignItems: "center", gap: 3, transform: "translateY(" + ((1 - p) * 160) + "px) scale(" + (0.88 + p * 0.12) + ")", opacity }}>
        <Word size={106} color="#fff" tracking={-0.075} weight={900} style={{ textShadow: "0 3px 0 rgba(67,94,109,.18),0 14px 30px rgba(40,68,78,.12)" }}>OpenDesign</Word>
        <Word size={222} color="#fff" tracking={-0.095} weight={950} style={{ textShadow: "0 4px 0 rgba(67,94,109,.2),0 17px 28px rgba(40,68,78,.12)" }}>MOTION</Word>
      </div>
      <div style={{ position: "absolute", bottom: 94, left: 0, right: 0, textAlign: "center", color: "#fff", fontSize: 18, fontWeight: 800, letterSpacing: ".25em", opacity: fadeOut(f, 45, 8), textShadow: "0 2px 12px rgba(0,0,0,.14)" }}>A NEW CREATIVE WORKFLOW</div>
    </AbsoluteFill>
  );
};

const BrandReveal = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = pop(f, fps, 0, 100, 15);
  const word = e(f, 7, 26);
  const wordText = "Claude Motion.";
  const chars = Math.floor(e(f, 14, 28, 0, wordText.length));
  return (
    <AbsoluteFill style={{ ...full, background: "#fbfaf7" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 350, display: "flex", justifyContent: "center", alignItems: "center", gap: 18 }}>
        <div style={{ transform: "scale(" + (0.3 + p * 0.7) + ") rotate(" + (f * 0.9) + "deg)" }}>
          <RadialMark frame={f} size={88} color="#e76c55" />
        </div>
        <Word size={92} color="#141618" tracking={-0.07} weight={850} style={{ opacity: word, transform: "translateX(" + ((1 - word) * 46) + "px)" }}>
          {wordText.slice(0, chars)}
        </Word>
      </div>
      <div style={{ position: "absolute", bottom: 76, left: 0, right: 0, textAlign: "center", color: "#b8b6b0", fontSize: 16, fontWeight: 800, letterSpacing: ".22em", opacity: e(f, 12, 27) }}>MOTION DESIGN / CREATIVE TOOLS</div>
    </AbsoluteFill>
  );
};

const ClaimScene = () => {
  const f = useCurrentFrame();
  const title = e(f, 0, 12);
  const marker = e(f, 6, 21);
  return (
    <AbsoluteFill style={{ ...full, background: "#faf9f5", color: "#111315" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 315, display: "flex", flexDirection: "column", alignItems: "center", opacity: title, transform: "translateY(" + ((1-title)*28) + "px)" }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "center", whiteSpace: "nowrap", gap: 18 }}>
          <Word size={104} color="#111315" tracking={-.065}>The</Word>
          <span style={{ position: "relative", display: "inline-block" }}>
            <span style={{ position: "absolute", left: -10, right: -12, top: "52%", height: 58, background: "#a8f05c", transform: "scaleX(" + marker + ") rotate(-.6deg)", transformOrigin: "left center" }} />
            <span style={{ position: "relative" }}><Word size={104} color="#111315" tracking={-.065}>open-source</Word></span>
          </span>
        </div>
        <Word size={104} color="#111315" tracking={-.065}>alternative</Word>
        <div style={{ marginTop: 24, display: "flex", alignItems: "center", gap: 13, color: "#898985" }}>
          <span style={{ fontSize: 26, fontWeight: 550 }}>to</span>
          <RadialMark frame={f} size={31} color="#e97962" />
          <span style={{ fontSize: 32, fontWeight: 850, color: "#1b1c1e", letterSpacing: "-.055em" }}>Claude Motion.</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const GalleryPoster = ({ index, frame }: { index: number; frame: number }) => {
  const common: React.CSSProperties = { position: "absolute", inset: 0, overflow: "hidden" };
  if (index === 0) return (
    <div style={{ ...common, background: "linear-gradient(130deg,#4024a5,#090b2e)", color: "#fff" }}>
      <div style={{ position: "absolute", left: 18, top: 16, fontSize: 11, letterSpacing: ".2em", fontWeight: 850 }}>MOTION FILM / 01</div>
      <div style={{ position: "absolute", right: 22, top: 32, width: 125, height: 125, border: "3px solid #a18bff", borderRadius: "50%", boxShadow: "0 0 45px #6044f5" }} />
      <Word size={62} color="#fff" style={{ position: "absolute", left: 25, bottom: 30 }}>WORLD</Word>
      <Word size={62} color="#a5ff64" style={{ position: "absolute", left: 25, bottom: -18 }}>WORLD</Word>
      <div style={{ position: "absolute", right: 38, bottom: 38, width: 80, height: 80, border: "10px solid #8c77ed", borderRadius: "50%" }} />
    </div>
  );
  if (index === 1) return (
    <div style={{ ...common, background: "#b8ed4b", color: "#121713" }}>
      <div style={{ position: "absolute", inset: 15, border: "2px solid rgba(20,28,22,.28)" }} />
      <div style={{ position: "absolute", right: 20, top: 20, width: 95, height: 95, borderRadius: "50%", background: "#ed603f" }} />
      <Word size={67} color="#171e16" style={{ position: "absolute", left: 25, bottom: 18 }}>EASE</Word>
      <div style={{ position: "absolute", bottom: 15, right: 24, fontSize: 10, letterSpacing: ".2em", fontWeight: 900 }}>OUT / CUBIC</div>
    </div>
  );
  if (index === 2) return (
    <div style={{ ...common, background: "#f0c9bc", color: "#242226" }}>
      <svg viewBox="0 0 400 240" width="100%" height="100%">
        <circle cx="200" cy="120" r="93" fill="none" stroke="#242226" strokeWidth="6" />
        <circle cx="200" cy="120" r="58" fill="none" stroke="#e45e49" strokeWidth="16" />
        <circle cx="200" cy="120" r="22" fill="#242226" />
        <path d="M200 36V6 M200 234v-30 M110 120H70 M330 120h-40" stroke="#242226" strokeWidth="5" />
        <path d="M200 120 L245 78 L214 144Z" fill="#242226" />
      </svg>
      <div style={{ position: "absolute", left: 18, top: 14, fontWeight: 900, fontSize: 11, letterSpacing: ".18em" }}>1965 / INFINITY DOTS</div>
    </div>
  );
  if (index === 3) return (
    <div style={{ ...common, background: "#181b23", color: "#f9f7eb" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(rgba(255,255,255,.22) 1.5px,transparent 1.5px)", backgroundSize: "12px 12px" }} />
      <Word size={72} color="#f4f0e6" style={{ position: "absolute", left: 18, top: 32 }}>THE</Word>
      <Word size={58} color="#8f9fdf" style={{ position: "absolute", right: 18, top: 90 }}>FUTURE</Word>
      <div style={{ position: "absolute", left: 16, bottom: 24, width: 170, height: 4, background: "#b9ed4a" }} />
      <div style={{ position: "absolute", right: 28, bottom: 12, width: 70, height: 70, border: "2px solid #f9f7eb", borderRadius: "50%" }} />
    </div>
  );
  if (index === 4) return (
    <div style={{ ...common, background: "#f5e9d4", color: "#1c2422" }}>
      <div style={{ position: "absolute", top: 18, left: 19, fontSize: 11, fontWeight: 900, letterSpacing: ".16em" }}>ONE IDEA / MANY FORMS</div>
      <div style={{ position: "absolute", left: 22, top: 51, width: 116, height: 135, background: "#eec83b" }} />
      <div style={{ position: "absolute", left: 158, top: 48, right: 20, bottom: 24, background: "#fff", border: "2px solid #202326" }} />
      <Word size={52} color="#202326" style={{ position: "absolute", left: 28, top: 75 }}>01</Word>
      <div style={{ position: "absolute", right: 35, top: 73, width: 120, height: 90, borderRadius: "50%", background: "repeating-radial-gradient(circle,#e75b48 0 5px,#fff 5px 12px)" }} />
      <div style={{ position: "absolute", left: 20, bottom: 19, fontSize: 12, fontWeight: 900 }}>THINK / MAKE / MOVE</div>
    </div>
  );
  if (index === 5) return (
    <div style={{ ...common, background: "#2439be", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "repeating-radial-gradient(circle at 50% 50%,transparent 0 18px,rgba(255,255,255,.12) 19px 21px)" }} />
      <Word size={59} color="#fff" style={{ position: "absolute", left: 20, top: 44 }}>THE FUTURE</Word>
      <Word size={59} color="#baf052" style={{ position: "absolute", left: 20, top: 104 }}>IS HERE.</Word>
      <div style={{ position: "absolute", right: 21, bottom: 20, width: 80, height: 80, border: "8px solid #fff", borderRadius: "50%" }} />
    </div>
  );
  if (index === 6) return (
    <div style={{ ...common, background: "#e8e9ed", color: "#151820" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "linear-gradient(90deg,transparent 49%,rgba(0,0,0,.1) 50%,transparent 51%),linear-gradient(transparent 49%,rgba(0,0,0,.1) 50%,transparent 51%)", backgroundSize: "42px 42px" }} />
      <Word size={63} color="#151820" style={{ position: "absolute", left: 20, top: 28 }}>MIND</Word>
      <Word size={63} color="#4968ec" style={{ position: "absolute", left: 20, top: 88 }}>MIND</Word>
      <div style={{ position: "absolute", right: 25, bottom: 25, width: 65, height: 65, borderRadius: "50%", background: "radial-gradient(circle at 32% 28%,#fff,#8ca4ff 30%,#1b2f9b 70%)", boxShadow: "0 0 25px #4e69e7" }} />
    </div>
  );
  if (index === 7) return (
    <div style={{ ...common, background: "#0c0d0f", color: "#fff" }}>
      <Word size={72} color="#fff" style={{ position: "absolute", left: 19, top: 25 }}>NEVER</Word>
      <Word size={64} color="#b9ed4a" style={{ position: "absolute", left: 19, top: 92 }}>LINEAR.</Word>
      <div style={{ position: "absolute", right: 22, bottom: 22, width: 83, height: 83, border: "6px solid #fff", borderRadius: "50%" }} />
      <div style={{ position: "absolute", right: 56, bottom: 56, width: 14, height: 14, borderRadius: "50%", background: green }} />
    </div>
  );
  if (index === 8) return (
    <div style={{ ...common, background: "#a5d8bd", color: "#19332a" }}>
      <Word size={58} color="#19332a" style={{ position: "absolute", left: 18, top: 35 }}>CREATE</Word>
      <div style={{ position: "absolute", right: 25, bottom: 25, width: 125, height: 90, border: "3px solid #19332a", borderRadius: 15, transform: "rotate(-8deg)" }} />
      <div style={{ position: "absolute", right: 66, bottom: 59, width: 48, height: 48, borderRadius: "50%", background: "#ee7052" }} />
    </div>
  );
  if (index === 9) return (
    <div style={{ ...common, background: "#11141d", color: "#fff" }}>
      <div style={{ position: "absolute", left: 14, top: 13, fontSize: 11, letterSpacing: ".18em", fontWeight: 900 }}>VISUAL SYSTEM / 09</div>
      <svg viewBox="0 0 400 240" width="100%" height="100%">
        <path d="M20 120 Q200 -10 380 120 Q200 250 20 120Z" fill="#354dcb" stroke="#f6f6f6" strokeWidth="4" />
        <circle cx="200" cy="120" r="70" fill="#11141d" stroke="#a6b8ff" strokeWidth="8" />
        <circle cx="200" cy="120" r="49" fill="#687eff" />
        <circle cx="200" cy="120" r="27" fill="#0b0e1a" />
        <circle cx="182" cy="100" r="10" fill="#fff" />
      </svg>
    </div>
  );
  if (index === 10) return (
    <div style={{ ...common, background: "#f5d33b", color: "#16181a" }}>
      <div style={{ position: "absolute", inset: 12, border: "3px solid #181a1d" }} />
      <div style={{ position: "absolute", left: 18, top: 15, fontSize: 11, fontWeight: 900 }}>1952 / CUT-OUTS</div>
      <Word size={64} color="#16181a" style={{ position: "absolute", left: 25, top: 61 }}>IN.</Word>
      <svg viewBox="0 0 400 200" width="100%" height="100%" style={{ position: "absolute", bottom: 0 }}>
        <path d="M0 95 L100 25 L160 80 L225 10 L300 90 L400 20" stroke="#e04435" strokeWidth="18" fill="none" />
        <path d="M0 120 L100 50 L160 105 L225 35 L300 115 L400 45" stroke="#141414" strokeWidth="4" fill="none" />
      </svg>
    </div>
  );
  return (
    <div style={{ ...common, background: "#171c28", color: "#fff" }}>
      <Word size={69} color="#fff" style={{ position: "absolute", left: 22, top: 20 }}>FUTURE</Word>
      <div style={{ position: "absolute", left: 25, top: 92, width: 170, height: 8, background: "#b9ed4a" }} />
      <Word size={24} color="#fff" tracking={0.04} style={{ position: "absolute", left: 25, bottom: 28 }}>IS ALREADY HERE</Word>
      <div style={{ position: "absolute", right: 20, top: 28, width: 90, height: 90, border: "6px solid #5472e4", transform: "rotate(26deg)" }} />
    </div>
  );
};


const GalleryCard=({index,frame}:{index:number;frame:number})=>{
 const drift=Math.sin((frame+index*11)/19)*3.2;
 const rotation=(index%2?-1:1)*.22;
 return <div style={{width:310,height:164,borderRadius:3,position:"relative",overflow:"hidden",transform:"translateY("+drift+"px) rotate("+rotation+"deg)",boxShadow:"0 8px 22px rgba(19,24,32,.13)",background:"#fff"}}>
   <GalleryPoster index={index%12} frame={frame+index*3}/>
   <div style={{position:"absolute",left:9,bottom:6,fontSize:7,fontWeight:900,letterSpacing:".16em",color:"rgba(20,25,30,.5)"}}>OD / {String(index+1).padStart(2,"0")}</div>
 </div>;
};

const GalleryWall=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,72,16);
 const x=e(f,0,77,30,-110), ry=e(f,0,77,-8,-15), rz=e(f,0,77,.6,-1.1);
 return <AbsoluteFill style={{...full,background:"#f4f1e9"}}>
   <div style={{position:"absolute",left:80,right:80,top:74,bottom:64,display:"grid",gridTemplateColumns:"repeat(5,310px)",gridTemplateRows:"repeat(5,164px)",gap:13,justifyContent:"center",alignContent:"center",transform:"perspective(1800px) rotateX(5deg) rotateY("+ry+"deg) rotateZ("+rz+"deg) translateX("+x+"px) translateY("+((1-p)*90)+"px) scale("+(0.92+.08*p)+")",transformOrigin:"center center"}}>
    {Array.from({length:25},(_,i)=><GalleryCard key={i} index={[4,9,0,6,11,2,5,10,3,8,7,1,4,9,2,6,11,5,0,10,3,8,1,7,4][i]} frame={f+i*2}/>)}
   </div>
   <div style={{position:"absolute",inset:0,pointerEvents:"none",background:"linear-gradient(180deg,rgba(255,255,255,.16),transparent 18%,transparent 84%,rgba(210,205,193,.12))"}}/>
   <Noise opacity={.035}/>
 </AbsoluteFill>;
}

const Comic1965

const Comic1965 = () => {
  const f = useCurrentFrame();
  const zoom = e(f, 0, 22, 0.9, 1.05);
  return (
    <AbsoluteFill style={{ ...full, background: "#e74b36" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(#fff 0 5px,transparent 5px)", backgroundSize: "34px 34px", opacity: .75 }} />
      <div style={{ position: "absolute", left: 140, right: 140, top: 100, bottom: 100, display: "grid", gridTemplateColumns: "250px 1fr 250px", gap: 20, border: "12px solid #171719", background: "#fff" }}>
        <div style={{ background: "#f7d43b", border: "7px solid #18191c", margin: 0, display: "grid", placeItems: "center", textAlign: "center", padding: 18, boxSizing: "border-box" }}>
          <Word size={52} color="#15171a" line={0.9}>ONE IDEA.</Word>
          <div style={{ fontSize: 16, fontWeight: 900, letterSpacing: ".15em" }}>ONLY ONE</div>
        </div>
        <div style={{ position: "relative", overflow: "hidden", background: "repeating-conic-gradient(#fff 0deg 6deg,#4a88d6 6deg 12deg)" }}>
          <div style={{ position: "absolute", inset: "13% 17%", borderRadius: "50%", background: "#ffde43", border: "10px solid #18191c", transform: "scale(" + zoom + ")" }} />
          <div style={{ position: "absolute", left: "22%", top: "17%", width: "56%", height: "66%", borderRadius: "50%", background: "#e44435", border: "12px solid #18191c", display: "grid", placeItems: "center", boxShadow: "inset 0 0 0 12px #f7d43b" }}>
            <div style={{ width: "63%", height: "63%", borderRadius: "50%", background: "#fff", border: "7px solid #15171a", display: "grid", placeItems: "center" }}><PlayGlyph size={120} color="#121315" /></div>
          </div>
          <div style={{ position: "absolute", left: 20, top: 20, background: "#f7d43b", color: "#15171a", padding: "11px 19px", border: "5px solid #15171a", fontSize: 23, fontWeight: 950, letterSpacing: ".12em" }}>MEANWHILE, IN 1965...</div>
          <div style={{ position: "absolute", right: 28, bottom: 30, background: "#f4dc37", color: "#171719", padding: "12px 22px", border: "5px solid #171719", transform: "rotate(-7deg)", fontSize: 26, fontWeight: 950 }}>CLICK!</div>
        </div>
        <div style={{ background: "#fff7e6", border: "7px solid #18191c", display: "grid", placeItems: "center", fontSize: 42, fontWeight: 950 }}>•••</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 55, textAlign: "center", color: "#fff", fontSize: 18, fontWeight: 900, letterSpacing: ".2em" }}>1965 / INFINITY DOTS</div>
      <Noise opacity={0.05} />
    </AbsoluteFill>
  );
};

const MindPoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#2026ce", color: "#050b44" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(130deg,#2026ce 0%,#2528bb 44%,#151c70 100%)" }} />
      <div style={{ position: "absolute", inset: 0, opacity: .26, backgroundImage: "linear-gradient(rgba(255,255,255,.36) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.36) 1px,transparent 1px)", backgroundSize: "60px 60px" }} />
      <div style={{ position: "absolute", left: -25, top: 80, opacity: .9, transform: "translateX(" + e(f, 0, 22, 70, -50) + "px)" }}>
        <Word size={220} color="#0a124e">MIND MIND</Word>
        <Word size={220} color="#0a124e">MIND MIND</Word>
        <Word size={220} color="#0a124e">MIND MIND</Word>
      </div>
      <svg viewBox="0 0 820 820" width="780" height="780" style={{ position: "absolute", right: 180, top: 145, filter: "drop-shadow(0 30px 50px rgba(0,0,0,.24))", transform: "rotate(" + (f * 1.4) + "deg)" }}>
        <defs>
          <radialGradient id="mind-glass"><stop offset="0%" stopColor="#fff" /><stop offset="18%" stopColor="#bfd0ff" /><stop offset="45%" stopColor="#435bde" /><stop offset="70%" stopColor="#111b72" /><stop offset="100%" stopColor="#060b39" /></radialGradient>
        </defs>
        <circle cx="410" cy="410" r="330" fill="none" stroke="#8ba6ff" strokeOpacity=".35" strokeWidth="2" />
        <circle cx="410" cy="410" r="255" fill="none" stroke="#a2b4ff" strokeOpacity=".55" strokeWidth="3" />
        <circle cx="410" cy="410" r="172" fill="url(#mind-glass)" stroke="#e5ebff" strokeWidth="8" />
        <circle cx="410" cy="410" r="118" fill="none" stroke="#c5d2ff" strokeOpacity=".7" strokeWidth="4" />
        <circle cx="410" cy="410" r="66" fill="#0d174e" />
        <circle cx="370" cy="355" r="33" fill="#fff" opacity=".8" />
        {Array.from({ length: 32 }, (_, i) => <line key={i} x1="410" y1="220" x2="410" y2="160" stroke="#b8c9ff" strokeWidth="3" transform={"rotate(" + (i * 11.25) + " 410 410)"} />)}
      </svg>
      <div style={{ position: "absolute", left: 95, bottom: 76, color: "#e9edff", fontSize: 17, fontWeight: 900, letterSpacing: ".18em" }}>MIND / MATTER / MOTION</div>
      <Noise opacity={0.055} />
    </AbsoluteFill>
  );
};

const RingPoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#f7f6f0", color: "#101214" }}>
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{ position: "absolute", inset: 0, transform: "rotate(" + (f * .18) + "deg)" }}>
        <defs>
          <path id="ringA" d="M960 540 m-635 0 a635 635 0 1 1 1270 0 a635 635 0 1 1 -1270 0" />
          <path id="ringB" d="M960 540 m-520 0 a520 520 0 1 1 1040 0 a520 520 0 1 1 -1040 0" />
          <path id="ringC" d="M960 540 m-405 0 a405 405 0 1 1 810 0 a405 405 0 1 1 -810 0" />
          <path id="ringD" d="M960 540 m-293 0 a293 293 0 1 1 586 0 a293 293 0 1 1 -586 0" />
          <path id="ringE" d="M960 540 m-183 0 a183 183 0 1 1 366 0 a183 183 0 1 1 -366 0" />
        </defs>
        {[635,520,405,293,183].map((r,i) => <circle key={r} cx="960" cy="540" r={r} fill="none" stroke="#111315" strokeWidth={i===0?5:3} />)}
        <text fill="#111315" fontSize="83" fontWeight="950" letterSpacing="7"><textPath href="#ringA">THE FUTURE IS ALREADY HERE · THE FUTURE IS ALREADY HERE ·</textPath></text>
        <text fill="#111315" fontSize="72" fontWeight="950" letterSpacing="6"><textPath href="#ringB">FUTURE IS ALREADY HERE · FUTURE IS ALREADY HERE ·</textPath></text>
        <text fill="#111315" fontSize="59" fontWeight="950" letterSpacing="5"><textPath href="#ringC">THE FUTURE · THE FUTURE · THE FUTURE · THE FUTURE ·</textPath></text>
        <text fill="#111315" fontSize="45" fontWeight="900" letterSpacing="4"><textPath href="#ringD">IS ALREADY HERE · IS ALREADY HERE · IS ALREADY HERE ·</textPath></text>
        <text fill="#111315" fontSize="31" fontWeight="900" letterSpacing="3"><textPath href="#ringE">THE FUTURE IS NOW · THE FUTURE IS NOW · THE FUTURE IS NOW ·</textPath></text>
        <circle cx="960" cy="540" r="126" fill="#111315" />
        <text x="960" y="526" fill="#f7f6f0" textAnchor="middle" fontSize="39" fontWeight="950">FUTURE</text>
        <text x="960" y="574" fill="#f7f6f0" textAnchor="middle" fontSize="31" fontWeight="850">IS NOW</text>
      </svg>
    </AbsoluteFill>
  );
};
const FutureCollage = () => (
  <AbsoluteFill style={{ ...full, background: "#111315", color: "#f6f5ef" }}>
    <div style={{ position: "absolute", inset: 35, display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 14 }}>
      <div style={{ gridColumn: "span 2", background: "#f5f4ec", color: "#161819", padding: 30, boxSizing: "border-box", position: "relative" }}>
        <Word size={96} color="#161819" style={{ position: "absolute", left: 35, top: 32 }}>THE</Word>
        <Word size={75} color="#161819" style={{ position: "absolute", left: 35, top: 122 }}>FUTURE</Word>
        <div style={{ position: "absolute", right: 30, bottom: 25, width: 140, height: 140, border: "3px solid #161819", borderRadius: "50%" }} />
      </div>
      <div style={{ background: "#f2d73e", color: "#141516", padding: 24, position: "relative" }}>
        <Word size={56} color="#141516">ONE</Word><Word size={56} color="#141516">IDEA.</Word>
        <div style={{ position: "absolute", bottom: 25, right: 25, width: 70, height: 70, borderRadius: "50%", background: "#e14939" }} />
      </div>
      <div style={{ background: "#fff", color: "#151719", padding: 18 }}>
        <div style={{ height: 2, background: "#151719", marginBottom: 15 }} />
        <div style={{ fontSize: 22, fontWeight: 900 }}>— — —</div>
        <div style={{ height: 65, marginTop: 18, backgroundImage: "repeating-linear-gradient(135deg,#151719 0 5px,transparent 5px 14px)" }} />
      </div>
      <div style={{ background: "#191b1e", color: "#f6f5ef", padding: 25, border: "1px solid #eee" }}>
        <Word size={65} color="#f6f5ef">IS</Word><Word size={65} color="#b9ed4a">NOW.</Word>
      </div>
      <div style={{ background: "#111315", color: "#f6f5ef", padding: 25, border: "1px solid #eee" }}><div style={{ width: 115, height: 115, border: "3px solid #f6f5ef", borderRadius: "50%", margin: "auto" }} /></div>
      <div style={{ gridColumn: "span 2", background: "#f2d73e", color: "#141516", padding: 28 }}>
        <Word size={86} color="#141516">FUTURE</Word>
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 13, fontSize: 18, letterSpacing: ".18em", fontWeight: 900 }}><span>IS ALREADY HERE</span><span>04 / 06</span></div>
      </div>
      <div style={{ background: "#e9e9e4", color: "#111315", padding: 23 }}>
        <Word size={58} color="#111315">FORM</Word>
        <div style={{ height: 70, border: "2px solid #111315", transform: "skew(-16deg)", marginTop: 10 }} />
      </div>
    </div>
    <div style={{ position: "absolute", left: 75, top: 49, fontSize: 17, fontWeight: 900, letterSpacing: ".2em" }}>EDITORIAL SYSTEM / 04</div>
  </AbsoluteFill>
);

const InPoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#080a0c", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 45%,#22272a 0%,#080a0c 60%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 270, textAlign: "center", transform: "translateY(" + e(f, 0, 14, 100, 0) + "px)" }}>
        <Word size={310} color="#f9f9f4" tracking={-0.105}>IN<span style={{ color: green }}>.</span></Word>
      </div>
      <div style={{ position: "absolute", left: 105, bottom: 82, color: "#878d8e", fontSize: 16, fontWeight: 900, letterSpacing: ".2em" }}>THE MOMENT / 05</div>
    </AbsoluteFill>
  );
};

const NeverPoster = () => (
  <AbsoluteFill style={{ ...full, background: "#b9f17a", color: "#101713" }}>
    <div style={{ position: "absolute", inset: 0, opacity: .35, backgroundImage: "repeating-linear-gradient(0deg,transparent 0 48px,rgba(17,26,18,.13) 49px 51px)" }} />
    <div style={{ position: "absolute", top: -20, left: -20, opacity: .13 }}>
      <Word size={140} color="#16231b">NEVER NEVER</Word>
      <Word size={140} color="#16231b">NEVER NEVER</Word>
      <Word size={140} color="#16231b">NEVER NEVER</Word>
      <Word size={140} color="#16231b">NEVER NEVER</Word>
    </div>
    <div style={{ position: "absolute", left: 85, right: 85, top: 360, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
      <Word size={205} color="#121713">NEVER</Word>
      <div style={{ width: 3, height: 210, background: "#121713", opacity: .35 }} />
      <Word size={195} color="#121713">NEVER</Word>
    </div>
    <div style={{ position: "absolute", left: 92, bottom: 84, fontSize: 18, fontWeight: 900, letterSpacing: ".2em" }}>NOT LINEAR / NOT STATIC</div>
  </AbsoluteFill>
);

const LinearPoster = () => {
  const f = useCurrentFrame();
  const slide = e(f, 0, 20, 110, -40);
  return (
    <AbsoluteFill style={{ ...full, background: "#0b0d10", color: "#f6f5ef" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 210, transform: "translateX(" + slide + "px)" }}>
        <Word size={280} color="#f5f4ee" tracking={-0.115}>LINEAR<span style={{ color: green }}>.</span></Word>
      </div>
      <div style={{ position: "absolute", left: 90, top: 78, fontSize: 18, fontWeight: 900, letterSpacing: ".2em", color: "#858d90" }}>MOTION / 06</div>
      <div style={{ position: "absolute", right: 100, bottom: 88, fontSize: 18, color: "#8f969a", fontWeight: 850, letterSpacing: ".16em" }}>IN / OUT / AGAIN</div>
    </AbsoluteFill>
  );
};

const ClockPoster = () => {
  const f = useCurrentFrame();
  const rot = 22 + f * 1.5;
  return (
    <AbsoluteFill style={{ ...full, background: "#162d82", color: "#f3ce67" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(135deg,#1c3b9a,#111d5e)" }} />
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        {Array.from({ length: 46 }, (_, i) => <path key={i} d={"M" + (i * 49 - 180) + " " + (170 + ((i * 67) % 730)) + " q 95 -34 180 " + ((i % 4) * 15 - 20)} fill="none" stroke={i % 2 ? "#5266bc" : "#2445a3"} strokeWidth={i % 3 ? 8 : 14} opacity=".42" />)}
        <g transform={"translate(960 540) rotate(" + (f * 0.3) + ")"}>
          <circle r="320" fill="#e2b84c" stroke="#f2d67b" strokeWidth="26" />
          <circle r="280" fill="#1b348a" stroke="#c18a30" strokeWidth="18" />
          <circle r="236" fill="none" stroke="#f8da7a" strokeWidth="8" strokeDasharray="3 15" />
          <circle r="205" fill="#172764" stroke="#e9bf4b" strokeWidth="11" />
          <path d="M-120 -210 Q0 -250 130 -200 M-190 135 Q0 240 180 130" fill="none" stroke="#f8d56c" strokeWidth="9" opacity=".6" />
          <g transform={"rotate(" + rot + ")"}>
            <path d="M0 -158 L22 24 L0 160 L-22 24Z" fill="#f7d45a" stroke="#8e6c2e" strokeWidth="10" />
          </g>
          <circle r="31" fill="#e9c34c" stroke="#fff0a0" strokeWidth="9" />
        </g>
      </svg>
      <div style={{ position: "absolute", top: 60, left: 0, right: 0, textAlign: "center", fontSize: 24, fontWeight: 950, color: "#f3d47c", letterSpacing: ".16em" }}>1889</div>
      <div style={{ position: "absolute", bottom: 70, left: 0, right: 0, textAlign: "center", fontSize: 18, fontWeight: 850, color: "#e6d7a4", letterSpacing: ".18em" }}>TIME IS A MATERIAL</div>
    </AbsoluteFill>
  );
};

const TogglePoster = () => {
  const f = useCurrentFrame();
  const x = e(f, 5, 16, 0, 1);
  return (
    <AbsoluteFill style={{ ...full, background: "#f7f7f5", color: "#2a2c2c" }}>
      <div style={{ position: "absolute", left: "50%", top: "50%", width: 250, height: 120, transform: "translate(-50%,-50%)", borderRadius: 100, background: "#e5e6e4", boxShadow: "inset 0 8px 22px rgba(0,0,0,.09),0 14px 35px rgba(0,0,0,.12)", padding: 10, boxSizing: "border-box" }}>
        <div style={{ position: "absolute", left: 10 + x * 120, top: 10, width: 100, height: 100, borderRadius: "50%", background: "#fff", boxShadow: "0 4px 16px rgba(0,0,0,.13)", border: "1px solid #d7d9d6" }} />
      </div>
      <div style={{ position: "absolute", bottom: 95, left: 0, right: 0, textAlign: "center", fontSize: 16, fontWeight: 850, color: "#969d9d", letterSpacing: ".2em" }}>TINY ACTION / BIG IMPACT</div>
    </AbsoluteFill>
  );
};

const EyePoster = () => {
 const f=useCurrentFrame();
 const blink=f<7?e(f,0,7,.15,1):f>17?1-e(f,17,22,0,.85):1;
 return <AbsoluteFill style={{...full,background:"#080a12",color:"#fff"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 50%,#1d2867 0%,#090c1b 60%)"}}/>
  <svg viewBox="0 0 1400 650" width="1320" height="620" style={{position:"absolute",left:"50%",top:"47%",transform:"translate(-50%,-50%)"}}>
   <defs><radialGradient id="iris-gradient-v10"><stop offset="0%" stopColor="#080a15"/><stop offset="21%" stopColor="#18276e"/><stop offset="51%" stopColor="#485ef8"/><stop offset="76%" stopColor="#202e89"/><stop offset="100%" stopColor="#080a15"/></radialGradient><filter id="iris-glow-v10"><feGaussianBlur stdDeviation="8"/></filter></defs>
   <path d="M75 325Q700 0 1325 325Q700 650 75 325Z" fill="#151c46" stroke="#9eacff" strokeWidth="8"/>
   <path d={"M90 325Q700 "+(325-265*blink)+" 1310 325Q700 "+(325+265*blink)+" 90 325Z"} fill="#f5f3ed"/>
   <circle cx="700" cy="325" r="210" fill="url(#iris-gradient-v10)" stroke="#8c9bff" strokeWidth="13"/>
   {Array.from({length:64},(_,i)=><path key={i} d="M700 118L700 250" stroke={i%2?"#9cb1ff":"#435be3"} strokeWidth={i%4?4:8} opacity=".78" transform={"rotate("+(i*5.625)+" 700 325)"}/>)}
   <circle cx="700" cy="325" r="105" fill="#03050b" stroke="#7188ff" strokeWidth="8"/>
   <circle cx="650" cy="265" r="34" fill="#fff" opacity=".88" filter="url(#iris-glow-v10)"/><circle cx="650" cy="265" r="18" fill="#fff"/>
  </svg>
  <div style={{position:"absolute",left:120,bottom:75,fontSize:32,fontWeight:950,letterSpacing:"-.04em"}}>4.7%</div>
  <div style={{position:"absolute",right:125,bottom:83,color:"#8793c9",fontSize:16,fontWeight:850,letterSpacing:".18em"}}>A STUDY IN FOCUS</div>
 </AbsoluteFill>;
};

const Comic1952 = () => {
 const f=useCurrentFrame(),n=e(f,0,2);
 return <AbsoluteFill style={{...full,background:"#f1e7d2",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,display:"grid",gridTemplateColumns:"1fr 1.12fr 1fr"}}>
   <div style={{position:"relative",background:"#d64c8f",borderRight:"9px solid #17191b"}}>
    <div style={{position:"absolute",left:46,top:65,fontFamily:"Georgia,serif",fontSize:35,fontWeight:900,color:"#ffe7d1"}}>1952</div>
    <svg viewBox="0 0 570 1080" width="100%" height="100%"><path d="M50 760L400 215L530 315L180 865Z" fill="#f4d74a" stroke="#151719" strokeWidth="18"/><path d="M5 500L310 120L415 200L115 580Z" fill="#f8e7c9" stroke="#151719" strokeWidth="14"/><path d="M135 905L470 430" stroke="#17191b" strokeWidth="28"/><circle cx="170" cy="340" r="82" fill="#fff1dc" stroke="#141719" strokeWidth="13"/><path d="M160 262L245 365L150 415Z" fill="#283e97"/></svg>
   </div>
   <div style={{position:"relative",background:"#f8f1df",display:"grid",placeItems:"center",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:45,border:"8px solid #151719",background:"repeating-linear-gradient(135deg,#f5e7cf 0 22px,#9fb8e4 22px 25px)"}}/>
    <div style={{position:"absolute",width:520,height:520,borderRadius:"50%",background:"#f5d447",border:"15px solid #161719",boxShadow:"inset 0 0 0 14px #fff5dc"}}/>
    <div style={{position:"absolute",width:350,height:350,borderRadius:"50%",background:"#e44e39",border:"15px solid #161719",display:"grid",placeItems:"center"}}><div style={{width:200,height:200,borderRadius:"50%",background:"#fff",border:"12px solid #141719",display:"grid",placeItems:"center"}}><svg viewBox="0 0 100 120" width="180" height="210"><path d="M8 5L91 64L48 70L35 115Z" fill="#111315"/></svg></div></div>
    <div style={{position:"absolute",top:25,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontSize:32,fontWeight:900,color:"#23346d"}}>Cut-outs / 1952</div>
   </div>
   <div style={{position:"relative",background:"#168c86",borderLeft:"9px solid #17191b"}}>
    <div style={{position:"absolute",right:35,top:60,fontFamily:"Georgia,serif",fontSize:30,fontWeight:900,color:"#f7ecd6"}}>FORM</div>
    <svg viewBox="0 0 570 1080" width="100%" height="100%"><path d="M-30 360L360 810L515 670L120 225Z" fill="#f2c83d" stroke="#141719" strokeWidth="18"/><path d="M40 800L430 270" stroke="#f4ecda" strokeWidth="31"/><path d="M150 875L530 350" stroke="#111315" strokeWidth="18"/><circle cx="380" cy="220" r="100" fill="#f2d84e" stroke="#17191b" strokeWidth="14"/><circle cx="380" cy="220" r="48" fill="#df4a89"/></svg>
   </div>
  </div>
 </AbsoluteFill>;
};

const Future3D = () => {
  const f = useCurrentFrame();
  const scale = e(f, 0, 18, .88, 1.02);
  return (
    <AbsoluteFill style={{ ...full, background: "radial-gradient(ellipse at 50% 48%,#344de5,#192a9e 67%,#111b66 100%)", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, opacity: .28, backgroundImage: "linear-gradient(rgba(255,255,255,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.22) 1px,transparent 1px)", backgroundSize: "78px 78px", transform: "perspective(600px) rotateX(61deg) translateY(350px)" }} />
      <div style={{ position: "absolute", top: 250, left: 0, right: 0, textAlign: "center", transform: "scale(" + scale + ")" }}>
        <div style={{ fontSize: 260, lineHeight: .84, fontWeight: 950, letterSpacing: "-.1em", color: "#e8ecff", textShadow: "1px 1px 0 #a5b2ec,3px 3px 0 #7b8edf,7px 7px 0 #5264bd,12px 12px 0 #283e98,22px 28px 35px rgba(0,0,0,.35)" }}>FUTURE</div>
        <div style={{ marginTop: 30, fontSize: 50, fontWeight: 850, letterSpacing: ".04em", color: "#fff", textShadow: "0 4px 20px rgba(0,0,0,.25)" }}>IS ALREADY HERE.</div>
      </div>
    </AbsoluteFill>
  );
};


const DotPoster = () => {
 const f=useCurrentFrame(),r=314+Math.sin(f/4)*2;
 return <AbsoluteFill style={{...full,background:"#e63d32",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#fff 0 7px,transparent 7px)",backgroundSize:"31px 31px"}}/>
  <div style={{position:"absolute",left:"50%",top:"52%",width:r*2,height:r*2,marginLeft:-r,marginTop:-r,borderRadius:"50%",background:"#f7d343",border:"10px solid #17191a"}}>
   <div style={{position:"absolute",inset:52,borderRadius:"50%",background:"#df4434",border:"17px solid #17191a",boxShadow:"inset 0 0 0 18px #f5d446"}}>
    <div style={{position:"absolute",inset:43,borderRadius:"50%",background:"#fff",border:"8px solid #17191a",display:"grid",placeItems:"center"}}>
     <svg viewBox="0 0 100 120" width="155" height="180"><path d="M12 7L91 63L50 68L37 115Z" fill="#111315"/></svg>
    </div>
   </div>
  </div>
  <div style={{position:"absolute",top:25,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontSize:35,fontWeight:900,color:"#111315"}}>1965 / INFINITY DOTS</div>
 </AbsoluteFill>;
};

const GlitchPoster = () => {
  const f = useCurrentFrame();
  const shift = Math.sin(f*1.9)*13;
  return (
    <AbsoluteFill style={{ ...full, background: "#07090d" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 48% 48%,#131b28 0%,#030407 72%)" }} />
      <svg viewBox="0 0 1920 1080" width="100%" height="100%">
        <defs>
          <radialGradient id="glitch-eye"><stop offset="0%" stopColor="#fff" /><stop offset="18%" stopColor="#a8e9f7" /><stop offset="39%" stopColor="#286eea" /><stop offset="65%" stopColor="#101a34" /><stop offset="100%" stopColor="#05070c" /></radialGradient>
          <filter id="glitch-blur"><feGaussianBlur stdDeviation="11" /></filter>
        </defs>
        <path d="M220 540 Q960 140 1700 540 Q960 940 220 540Z" fill="#121826" stroke="#f5f4eb" strokeWidth="8" />
        <ellipse cx={960+shift} cy="540" rx="410" ry="285" fill="url(#glitch-eye)" stroke="#8de9ff" strokeWidth="8" />
        <circle cx={960+shift} cy="540" r="178" fill="#060a12" stroke="#daeaff" strokeWidth="10" />
        <circle cx={960+shift} cy="540" r="110" fill="#f7f8f4" filter="url(#glitch-blur)" />
        <circle cx={960+shift} cy="540" r="57" fill="#05070a" />
        <circle cx={920+shift} cy="495" r="29" fill="#fff" />
        {Array.from({length:18},(_,i)=><rect key={i} x={i*120-20} y={180+(i%5)*145} width={70+(i%3)*65} height={10+(i%4)*9} fill={i%2?"#27f2df":"#f332e8"} opacity=".7" />)}
      </svg>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(0deg,transparent 0 7px,rgba(255,255,255,.035) 8px 9px)" }} />
      <div style={{ position: "absolute", bottom: 73, left: 95, color: "#aab1bd", fontSize: 18, fontWeight: 900, letterSpacing: ".2em" }}>SIGNAL / NOISE / VISION</div>
    </AbsoluteFill>
  );
};

const WorldPoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#1227bb", color: "#f7f7f0" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 70% 42%,rgba(119,157,255,.45),transparent 42%),linear-gradient(130deg,#182bcb,#07106a)" }} />
      <div style={{ position: "absolute", inset: 0, opacity: .28, backgroundImage: "repeating-linear-gradient(0deg,transparent 0 44px,rgba(255,255,255,.18) 45px 47px)" }} />
      <div style={{ position: "absolute", left: 80, top: 140, transform: "translateX("+(Math.sin(f/6)*9)+"px)" }}>
        <Word size={235} color="#fff" tracking={-.1}>WORLD</Word>
        <Word size={235} color="#f8f6e8" tracking={-.1}>WIDE.</Word>
      </div>
      <div style={{ position: "absolute", right: 200, top: 210, width: 420, height: 420, border: "13px solid #9bffff", borderRadius: "50%", boxShadow: "0 0 65px rgba(91,255,255,.55)" }}>
        <div style={{ position: "absolute", inset: 54, border: "5px solid rgba(255,255,255,.85)", borderRadius: "50%" }} />
        <div style={{ position: "absolute", inset: 130, background: "#13cbd1", borderRadius: "50%" }} />
      </div>
      <div style={{ position: "absolute", left: 88, bottom: 80, color: "#9befff", fontSize: 18, fontWeight: 900, letterSpacing: ".2em" }}>ONE WORLD / MANY IDEAS</div>
    </AbsoluteFill>
  );
};

const MorroPoster = () => (
  <AbsoluteFill style={{ ...full, background: "#efeee8", color: "#181a1d" }}>
    <div style={{ position: "absolute", inset: 0, background: "repeating-linear-gradient(90deg,transparent 0 90px,rgba(0,0,0,.035) 91px 93px)" }} />
    <div style={{ position: "absolute", left: -80, top: 72, transform: "rotate(-8deg)" }}>
      <Word size={370} color="#111315" tracking={-.13}>MORRO</Word>
      <Word size={370} color="#efeee8" tracking={-.13} style={{ WebkitTextStroke: "4px #111315", marginTop: -45 }}>MORRO</Word>
      <Word size={370} color="#111315" tracking={-.13} style={{ opacity: .88, marginTop: -45 }}>MORRO</Word>
    </div>
    <div style={{ position: "absolute", right: 90, bottom: 75, fontSize: 20, fontWeight: 900, letterSpacing: ".2em" }}>TYPE AS IMAGE / 03</div>
  </AbsoluteFill>
);

const OutPoster = () => (
  <AbsoluteFill style={{ ...full, background: "#00851e", color: "#f9fff4" }}>
    <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 50% 44%,rgba(255,255,255,.1),transparent 48%)" }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: 235, textAlign: "center" }}>
      <Word size={420} color="#fff" tracking={-.14}>OUT<span style={{ color: "#b9ed4a" }}>.</span></Word>
    </div>
    <div style={{ position: "absolute", left: 95, bottom: 80, fontSize: 18, fontWeight: 900, letterSpacing: ".2em", color: "#c5f1c1" }}>EASING / DIRECTION / FEEL</div>
  </AbsoluteFill>
);

const EasePoster = () => {
 const f=useCurrentFrame(),shift=e(f,0,13,30,0);
 return <AbsoluteFill style={{...full,background:"#f6f5ef",color:"#111813",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"-4%",right:"-4%",top:270,transform:"translateX("+shift+"px)",textAlign:"center",fontFamily:displayFont,fontSize:330,fontWeight:950,letterSpacing:"-.14em",color:"#9beb48",textShadow:"2px 2px 0 #77bf36,5px 5px 0 #5c9b2f,9px 9px 0 #3f712a,15px 18px 22px rgba(35,65,23,.25)"}}>EASE</div>
  <div style={{position:"absolute",left:80,bottom:75,fontSize:17,fontWeight:900,letterSpacing:".18em",color:"#777e75"}}>MAKE IT FEEL RIGHT</div>
  <svg viewBox="0 0 700 300" width="620" height="265" style={{position:"absolute",right:70,bottom:100}}><path d="M15 270C105 270 120 35 680 20" stroke="#9beb48" strokeWidth="13" fill="none" strokeLinecap="round"/><path d="M15 270C105 270 120 35 680 20" stroke="#1d2c18" strokeWidth="3" fill="none" strokeDasharray="10 18"/></svg>
 </AbsoluteFill>;
};

const MotionFilmsPoster = () => {
 const f=useCurrentFrame(),planeX=Math.sin(f/7)*18;
 return <AbsoluteFill style={{...full,background:"#182765",color:"#fff",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"repeating-linear-gradient(162deg,rgba(255,255,255,.055) 0 4px,transparent 5px 34px),linear-gradient(145deg,#263c87,#101d53)"}}/>
  <div style={{position:"absolute",left:470,top:105,width:960,height:520,border:"10px solid #f7f1e0",boxSizing:"border-box",boxShadow:"0 0 0 2px rgba(255,255,255,.25)"}}>
   <div style={{position:"absolute",left:-6,right:-6,top:-27,height:23,background:"repeating-linear-gradient(90deg,#f7f1e0 0 40px,transparent 40px 56px)"}}/>
   <div style={{position:"absolute",left:-6,right:-6,bottom:-27,height:23,background:"repeating-linear-gradient(90deg,#f7f1e0 0 40px,transparent 40px 56px)"}}/>
   {[0,1,2].map(i=><div key={i} style={{position:"absolute",left:60+i*285,top:360,width:210,height:3,background:"#f7f1e0",opacity:.75}}/>)}
   <svg viewBox="0 0 960 520" width="100%" height="100%">
    <path d={"M55 305L"+(240+planeX)+" 160L175 330L142 286Z"} fill="#f8f4e8" stroke="#fff" strokeWidth="5"/><path d="M142 286L240 160L210 340L175 330Z" fill="#d9ddea"/>
    <path d="M625 320Q705 245 800 320Q820 390 735 425Q650 438 625 320Z" fill="#10192e" stroke="#f8f4e8" strokeWidth="7"/>
    <circle cx="700" cy="329" r="12" fill="#fff"/><circle cx="765" cy="329" r="12" fill="#fff"/><path d="M695 370Q730 397 775 370" stroke="#e7a38f" strokeWidth="8" fill="none" strokeLinecap="round"/>
    <path d="M80 425Q210 370 330 420" stroke="#f5efdf" strokeWidth="5" fill="none"/>
   </svg>
   <div style={{position:"absolute",left:15,top:15,fontSize:15,color:"#f4eaca",fontWeight:900,letterSpacing:".18em"}}>MOTION FILMS / 02</div>
  </div>
  <div style={{position:"absolute",left:370,bottom:190,width:260,height:230,borderRadius:"24% 30% 20% 20%",background:"#101113",border:"5px solid #f7f1e0",transform:"rotate(-4deg)",display:"grid",placeItems:"center",boxShadow:"0 8px 0 rgba(0,0,0,.15)"}}>
   <div style={{width:142,height:142,borderRadius:"50%",background:"#090a0c",border:"12px solid #f7f1e0",display:"grid",placeItems:"center",color:"#fff",fontSize:56}}>•ᴗ•</div>
   <div style={{position:"absolute",right:-44,bottom:24,width:70,height:35,borderRadius:30,background:"#101113",border:"3px solid #f7f1e0"}}/>
  </div>
  <div style={{position:"absolute",left:0,right:0,bottom:66,textAlign:"center",fontFamily:"Georgia,serif",fontSize:88,color:"#fff",letterSpacing:".03em"}}>motion films</div>
 </AbsoluteFill>;
};

const OpenDesignSymbol=({size=100}:{size?:number})=><svg viewBox="0 0 100 100" width={size} height={size}><rect x="3" y="3" width="94" height="94" rx="25" fill="#111315"/><circle cx="50" cy="50" r="28" fill="none" stroke="#fff" strokeWidth="5.5"/><path d="M42 30L42 70L72 50Z" fill="#fff"/></svg>;
const ClockComic=()=>{
 const f=useCurrentFrame(),a=32+f*5;
 return <AbsoluteFill style={{...full,background:"#77a9dc"}}>
  <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#fff 0 5px,transparent 5px)",backgroundSize:"27px 27px",opacity:.6}}/>
  <div style={{position:"absolute",inset:"80px 125px",display:"grid",gridTemplateColumns:"220px 1fr 210px",gap:14,padding:14,background:"#fff7e7",border:"12px solid #17191b"}}>
   <div style={{background:"#ffda42",border:"6px solid #17191b",padding:20,display:"flex",flexDirection:"column",justifyContent:"space-between"}}><Word size={38} color="#17191b">A NEW</Word><Word size={65} color="#17191b">AGE</Word><b>OF MOTION</b></div>
   <div style={{position:"relative",background:"repeating-conic-gradient(#fff 0deg 7deg,#78a6dc 7deg 14deg)",border:"7px solid #17191b",display:"grid",placeItems:"center"}}>
    <div style={{width:490,height:490,borderRadius:"50%",background:"#e64b39",border:"18px solid #17191b",boxShadow:"inset 0 0 0 18px #f6d84b",display:"grid",placeItems:"center"}}><svg viewBox="0 0 320 320" width="100%" height="100%"><circle cx="160" cy="160" r="132" fill="#fbf4e4" stroke="#17191b" strokeWidth="8"/><circle cx="160" cy="160" r="105" fill="none" stroke="#333" strokeWidth="4" strokeDasharray="4 10"/><path d={"M160 160 L"+(160+Math.cos(a*Math.PI/180)*92)+" "+(160+Math.sin(a*Math.PI/180)*92)} stroke="#17191b" strokeWidth="13" strokeLinecap="round"/><circle cx="160" cy="160" r="13" fill="#17191b"/></svg></div>
    <div style={{position:"absolute",top:14,right:16,background:"#fff2d9",border:"4px solid #17191b",padding:"5px 12px",fontSize:24,fontWeight:950}}>1962</div>
   </div>
   <div style={{background:"#fff0df",border:"6px solid #17191b",display:"grid",placeItems:"center",fontSize:48}}>•••</div>
  </div><div style={{position:"absolute",top:28,left:0,right:0,textAlign:"center",color:"#fff",fontSize:18,fontWeight:950,letterSpacing:".2em"}}>1962 / MECHANICAL TIME</div>
 </AbsoluteFill>;
};
const LightSweep1973=()=>{
 const f=useCurrentFrame(),x=e(f,0,8,-700,1500);
 return <AbsoluteFill style={{...full,background:"#05070b"}}><div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 50%,#252936,#050608 65%)"}}/><Word size={300} color="#151a22" style={{position:"absolute",left:0,right:0,top:220,textAlign:"center"}}>1973</Word><div style={{position:"absolute",inset:0,transform:"translateX("+x+"px)",background:"linear-gradient(112deg,transparent 0 42%,rgba(255,255,255,.9) 49%,rgba(77,218,255,.8) 51%,rgba(255,87,191,.5) 54%,transparent 62%)",mixBlendMode:"screen"}}/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:225,height:225,borderRadius:60,background:"linear-gradient(145deg,#2d343d,#050607)",border:"4px solid #d6f4ff",display:"grid",placeItems:"center",boxShadow:"0 0 42px rgba(73,209,255,.4)"}}><OpenDesignSymbol size={188}/></div></AbsoluteFill>;
};
const MarioGamePoster=()=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{...full,background:"#28a8e7"}}><svg viewBox="0 0 1920 1080" width="100%" height="100%"><path d="M0 690L300 430L560 700L830 395L1120 700L1460 425L1740 700L1920 600V1080H0Z" fill="#718fd0"/><path d="M0 795L320 620L590 790L880 620L1190 805L1500 620L1920 790V1080H0Z" fill="#369a82"/><path d="M0 875H1920V1080H0Z" fill="#d19a42"/><path d="M0 950H1920" stroke="#fff0b9" strokeWidth="12" strokeDasharray="30 24"/>{Array.from({length:16},(_,i)=><g key={i} transform={"translate("+(i*120-40)+" "+(300+i%3*44)+")"}><rect width="80" height="26" rx="4" fill="#fff"/><rect x="12" y="8" width="56" height="10" fill="#d6ebf6"/></g>)}<g transform={"translate("+(850+Math.sin(f/7)*24)+" 545)"}><circle r="155" fill="#f7f0d4" stroke="#17202a" strokeWidth="16"/><circle r="120" fill="#2f8dda"/><path d="M-42 -60V60L70 0Z" fill="#fff"/></g></svg><div style={{position:"absolute",left:65,top:55,color:"#fff",fontSize:18,fontWeight:950,letterSpacing:".18em"}}>PIXEL WORLD / 1985</div></AbsoluteFill>;
};
const PosterGrid=()=><AbsoluteFill style={{...full,background:"#f2f1ec"}}><div style={{position:"absolute",inset:16,display:"grid",gridTemplateColumns:"1.1fr 1.1fr 1fr 1.6fr",gridTemplateRows:"1fr 1fr 1fr",gap:10}}><div style={{background:"#17191e",display:"grid",placeItems:"center"}}><Word size={90} color="#fff">THE</Word></div><div style={{background:"#fff",display:"grid",placeItems:"center"}}><Word size={92}>FUTURE</Word></div><div style={{background:"#17191e",display:"grid",placeItems:"center"}}><Word size={110} color="#fff">IS</Word></div><div style={{gridRow:"span 2",background:"repeating-radial-gradient(circle,#16191c 0 5px,#efeee9 6px 18px)",display:"grid",placeItems:"center"}}><OpenDesignSymbol size={220}/></div><div style={{background:"#f5d64a",display:"grid",placeItems:"center"}}><Word size={120}>NOW</Word></div><div style={{background:"#20232a",display:"grid",placeItems:"center"}}><Word size={95} color="#fff">HERE.</Word></div><div style={{background:"#1e39d4",display:"grid",placeItems:"center"}}><Word size={85} color="#fff">MAKE</Word></div><div style={{background:"#a5ed62",display:"grid",placeItems:"center"}}><Word size={78}>MOVE</Word></div><div style={{background:"#e6e4dc",display:"grid",placeItems:"center"}}><Word size={65}>MOTION</Word></div></div></AbsoluteFill>;
const PointCloudPoster=()=>{
 const f=useCurrentFrame(),points=Array.from({length:300},(_,i)=>{const z=1-2*(i+.5)/300,a=i*2.399963+f*.018,r=Math.sqrt(1-z*z),x=r*Math.cos(a),d=r*Math.sin(a),p=4.8/(5.2-d*.45);return{x:960+x*380*p,y:520+z*250*p,r:1.6+(d+1)*2,a:.25+(d+1)*.32}});
 return <AbsoluteFill style={{...full,background:"radial-gradient(ellipse at 50% 50%,#252b32,#050608 66%)"}}><svg viewBox="0 0 1920 1080" width="100%" height="100%"><ellipse cx="960" cy="520" rx="390" ry="272" fill="none" stroke="#a3b1b0" strokeOpacity=".22" strokeWidth="2"/>{points.map((p,i)=><circle key={i} cx={p.x} cy={p.y} r={p.r} fill={i%7===0?"#b9ed4a":"#e8efed"} opacity={p.a}/>)}</svg><div style={{position:"absolute",top:50,left:88,color:"#8d9998",fontSize:16,fontWeight:900,letterSpacing:".2em"}}>DEPTH / POINTS / MOTION</div></AbsoluteFill>;
};
const StatsPoster=()=>{
 const f=useCurrentFrame(),k=e(f,0,8);
 return <AbsoluteFill style={{...full,background:"linear-gradient(180deg,#c6e7e5 0%,#b7e5d6 43%,#edcab9 64%,#7fc8c5 100%)",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(ellipse at 18% 78%,rgba(254,242,210,.65),transparent 34%),linear-gradient(160deg,transparent 42%,rgba(39,183,185,.35) 43%,transparent 56%)"}}/>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <path d="M0 720Q180 660 330 720T650 715T980 740T1300 700T1620 730T1920 690V1080H0Z" fill="#65c5bb" opacity=".65"/>
   <path d="M0 825Q190 780 390 835T800 820T1160 850T1570 815T1920 835V1080H0Z" fill="#f0c6a9" opacity=".54"/>
   <path d="M0 920Q230 865 430 920T840 915T1280 940T1700 900T1920 920V1080H0Z" fill="#4db9bb" opacity=".55"/>
  </svg>
  <div style={{position:"absolute",left:78,top:250,fontFamily:displayFont,fontSize:235,fontWeight:950,color:"#111315",letterSpacing:"-.11em",textShadow:"0 6px 10px rgba(0,0,0,.16)"}}>84K</div>
  <div style={{position:"absolute",left:260,top:500,fontSize:50,fontWeight:800,color:"#343b38"}}>Day 104</div>
  <div style={{position:"absolute",left:665,top:80,width:1180,height:900,borderRadius:28,background:"#fff",padding:"70px 70px 54px",boxSizing:"border-box",boxShadow:"0 18px 55px rgba(37,85,92,.13)"}}>
   <div style={{textAlign:"center",fontSize:36,fontWeight:900,color:"#202326",marginBottom:48}}>◉ Star History</div>
   <div style={{position:"absolute",left:110,top:175,fontSize:20,fontWeight:800,color:"#45494b"}}>nexu-io/open-design</div>
   <svg viewBox="0 0 1040 560" width="100%" height="560">
    {[0,1,2,3,4].map((v)=><g key={v}><line x1="82" x2="1010" y1={80+v*105} y2={80+v*105} stroke="#e6e6e3" strokeWidth="2"/><text x="12" y={87+v*105} fontSize="22" fill="#4a4e50">{100-v*20}K</text></g>)}
    <path d="M82 500C120 465 135 330 210 280S315 225 375 203S530 150 610 125S760 95 855 70" stroke="#c94d3e" strokeWidth="7" fill="none" strokeLinecap="round"/>
    <path d="M855 70L875 66" stroke="#c94d3e" strokeWidth="7" fill="none"/>
    <circle cx="875" cy="66" r="11" fill="#b9f05b" stroke="#141719" strokeWidth="4"/>
    <text x="82" y="535" fontSize="20" fill="#303638">May</text><text x="270" y="535" fontSize="20" fill="#303638">June</text><text x="455" y="535" fontSize="20" fill="#303638">July</text><text x="645" y="535" fontSize="20" fill="#303638">August</text><text x="835" y="535" fontSize="20" fill="#303638">September</text><text x="960" y="535" fontSize="20" fill="#303638">October</text>
   </svg>
   <div style={{position:"absolute",left:78,bottom:23,fontSize:18,color:"#737a79"}}>GitHub stars</div>
  </div>
 </AbsoluteFill>;
};

const KoalaPoster=()=><AbsoluteFill style={{...full,background:"linear-gradient(120deg,#2a8bd1,#144a9a)",color:"#fff"}}><div style={{position:"absolute",left:330,top:190,width:430,height:540,borderRadius:220,background:"#f5ead0",transform:"rotate(-5deg)"}}><svg viewBox="0 0 430 540" width="100%" height="100%"><ellipse cx="82" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="348" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="215" cy="255" rx="155" ry="170" fill="#9099a1"/><ellipse cx="215" cy="298" rx="120" ry="100" fill="#f2efe6"/><circle cx="160" cy="246" r="16" fill="#151a1d"/><circle cx="270" cy="246" r="16" fill="#151a1d"/><ellipse cx="215" cy="300" rx="42" ry="57" fill="#20262c"/><path d="M180 365Q215 392 250 365" stroke="#252a2c" strokeWidth="10" fill="none"/></svg></div><div style={{position:"absolute",right:270,top:195,width:450,height:650,background:"#fff",color:"#182431",borderRadius:20,padding:38,boxSizing:"border-box",boxShadow:"0 24px 55px rgba(0,0,0,.22)"}}><div style={{fontSize:21,fontWeight:950,letterSpacing:".1em"}}>COURSES / 2026</div><div style={{marginTop:34,height:250,borderRadius:14,background:"linear-gradient(135deg,#f2dfba,#e4a27b,#83b9cb)"}}/><div style={{marginTop:34,fontSize:48,fontWeight:950,lineHeight:.95}}>Learn to create.</div><div style={{marginTop:25,fontSize:18,color:"#7e8991"}}>A new way to make ideas move.</div></div></AbsoluteFill>;
const GreenTransition=()=>{const f=useCurrentFrame(),r=e(f,0,7,90,650);return <AbsoluteFill style={{...full,background:"#b7ee5b"}}><svg viewBox="0 0 1920 1080" width="100%" height="100%"><circle cx="960" cy="540" r={r} fill="none" stroke="#efffd4" strokeWidth="3"/><circle cx="960" cy="540" r={r*.7} fill="none" stroke="#efffd4" strokeWidth="2"/></svg><Word size={420} color="#142016" style={{position:"absolute",left:0,right:0,top:300,textAlign:"center"}}>OUT.</Word></AbsoluteFill>;};



const Comic1962=()=>{
 const f=useCurrentFrame(),z=e(f,0,10,.98,1.02);
 return <AbsoluteFill style={{...full,background:"#f7f0df",transform:"scale("+z+")"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(circle at 50% 45%,#fff8e9,#e9dfc8)"}}/>
  <div style={{position:"absolute",left:0,top:0,width:360,bottom:0,background:"#f5ce3d",borderRight:"9px solid #151515"}}/>
  <div style={{position:"absolute",right:0,top:0,width:280,bottom:0,background:"#fbf7eb",borderLeft:"9px solid #151515",backgroundImage:"radial-gradient(#151515 1.5px,transparent 1.5px)",backgroundSize:"14px 14px"}}/>
  <div style={{position:"absolute",left:390,right:300,top:0,bottom:0,background:"repeating-conic-gradient(from 0deg at 50% 50%,#f9eac9 0deg 5deg,#8eb8ed 5deg 10deg)",borderLeft:"9px solid #151515",borderRight:"9px solid #151515"}}/>
  <div style={{position:"absolute",left:455,right:365,top:175,bottom:155,background:"#fff4d6",border:"12px solid #171719",clipPath:"polygon(0 0,100% 0,100% 100%,0 100%)"}}/>
  <div style={{position:"absolute",left:"50%",top:"51%",width:520,height:520,marginLeft:-260,marginTop:-260,borderRadius:"50%",background:"#efcf42",border:"16px solid #171719",boxShadow:"inset 0 0 0 15px #fbf6e8",display:"grid",placeItems:"center"}}>
    <div style={{width:360,height:360,borderRadius:"50%",background:"#e64a37",border:"13px solid #171719",display:"grid",placeItems:"center",boxShadow:"inset 0 0 0 12px #f3d442"}}>
      <PlayGlyph size={230} color="#111315"/>
    </div>
  </div>
  <div style={{position:"absolute",left:0,right:0,top:54,textAlign:"center",fontSize:36,fontWeight:950,color:"#151515",letterSpacing:".05em"}}>MEANWHILE, IN 1962…</div>
  <div style={{position:"absolute",right:310,bottom:104,padding:"10px 22px",background:"#f6d647",border:"7px solid #151515",fontSize:32,fontWeight:950,transform:"rotate(-8deg)"}}>CLICK!</div>
  <div style={{position:"absolute",left:45,bottom:52,fontSize:23,fontWeight:950,letterSpacing:".13em"}}>ONE IDEA.</div>
 </AbsoluteFill>;
};

const PixelGamePoster=()=>{
 const f=useCurrentFrame(),jump=Math.sin(f/2.8)*10;
 return <AbsoluteFill style={{...full,background:"#38b9f2",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(#38b9f2 0 62%,#80d85a 62% 100%)"}}/>
  <div style={{position:"absolute",left:0,right:0,top:110,height:630,backgroundImage:"radial-gradient(#fff 0 3px,transparent 3px)",backgroundSize:"90px 90px",opacity:.35}}/>
  <div style={{position:"absolute",left:90,top:100,fontSize:20,fontWeight:950,color:"#fff",letterSpacing:".18em"}}>SCORE 000100</div>
  <div style={{position:"absolute",right:120,top:100,fontSize:20,fontWeight:950,color:"#fff",letterSpacing:".18em"}}>LEVEL 1965</div>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <path d="M0 800 Q260 690 490 810 T920 800 T1370 790 T1920 810V1080H0Z" fill="#54bd4b"/>
   <path d="M0 900 Q300 810 580 890 T1110 900 T1600 875 T1920 920V1080H0Z" fill="#1c8c55"/>
   {Array.from({length:8},(_,i)=><g key={i} transform={"translate("+(i*270-80)+" 0)"}><rect x="0" y="735" width="100" height="85" fill="#39a34b"/><rect x="25" y="685" width="50" height="50" fill="#48c85b"/><rect x="15" y="670" width="18" height="18" fill="#fff"/></g>)}
   <g transform={"translate(960 "+(420+jump)+")"}><path d="M-85 10L0 -165L85 10L40 125H-40Z" fill="#f3d74a" stroke="#151515" strokeWidth="12"/><circle cx="0" cy="-20" r="46" fill="#fff" stroke="#151515" strokeWidth="10"/><path d="M-9 -53L28 -5L-9 25Z" fill="#151515"/></g>
   <path d="M0 980H1920" stroke="#fff" strokeWidth="8" opacity=".7"/>
  </svg>
  <div style={{position:"absolute",left:120,bottom:70,fontSize:24,fontWeight:950,color:"#fff",letterSpacing:".15em"}}>PIXEL PLAY / 01</div>
 </AbsoluteFill>;
};

const PortfolioFlash=()=>{
 const f=useCurrentFrame();
 const cards=[["#101217","#f4f2e8"],["#f5f0df","#17191c"],["#1d37bd","#fff"],["#111315","#fff"],["#d8edc7","#14221a"],["#252525","#f9f7ed"]];
 return <AbsoluteFill style={{...full,background:"#f3f1e9"}}>
  <div style={{position:"absolute",inset:0,display:"grid",gridTemplateColumns:"repeat(4,1fr)",gridTemplateRows:"repeat(3,1fr)",gap:10,padding:26,transform:"scale("+(1+e(f,0,9)*.04)+") rotate(-.4deg)"}}>
   {Array.from({length:12},(_,i)=><div key={i} style={{position:"relative",overflow:"hidden",background:cards[i%6][0],color:cards[i%6][1],display:"grid",placeItems:"center"}}>
    {i%4===0?<Word size={92} color={cards[i%6][1]}>THE</Word>:i%4===1?<div style={{width:160,height:160,borderRadius:"50%",border:"16px solid "+cards[i%6][1],display:"grid",placeItems:"center"}}><OpenDesignSymbol size={108}/></div>:i%4===2?<Word size={74} color={cards[i%6][1]}>FUTURE</Word>:<svg viewBox="0 0 300 170" width="100%" height="100%"><path d="M10 85Q150 -20 290 85Q150 190 10 85Z" fill="none" stroke={cards[i%6][1]} strokeWidth="9"/><circle cx="150" cy="85" r="35" fill={cards[i%6][1]}/></svg>}
    <div style={{position:"absolute",left:14,bottom:8,fontSize:10,fontWeight:900,letterSpacing:".2em"}}>MOTION / {String(i+1).padStart(2,"0")}</div>
   </div>)}
  </div>
 </AbsoluteFill>;
};

const EditorialPosterGrid=()=>{
 const cells=[["#fff","#111315","THE"],["#111315","#fff","FUTURE"],["#f8f6ef","#111315","IS"],["#f7f4e9","#111315","ALREADY"],["#f7f4e9","#111315","NOW"],["#17191c","#fff","HERE"]];
 return <AbsoluteFill style={{...full,background:"#090a0c",padding:55,boxSizing:"border-box"}}>
  <div style={{position:"absolute",inset:60,display:"grid",gridTemplateColumns:"1fr 1.1fr 1fr 1.1fr",gridTemplateRows:"1fr 1fr",gap:12}}>
   <div style={{background:"#f5f3ed",display:"grid",placeItems:"center"}}><div style={{width:"100%",height:"100%",background:"repeating-linear-gradient(135deg,#111 0 10px,#f5f3ed 10px 22px)"}}/></div>
   <div style={{background:"#f4f2e9",display:"grid",placeItems:"center"}}><Word size={95} color="#111315">THE</Word></div>
   <div style={{background:"#16181c",display:"grid",placeItems:"center"}}><Word size={85} color="#fff">FUTURE</Word></div>
   <div style={{background:"#f5f3ed",display:"grid",placeItems:"center"}}><svg viewBox="0 0 400 220" width="100%" height="100%"><circle cx="200" cy="110" r="83" stroke="#111" strokeWidth="8" fill="none"/>{Array.from({length:18},(_,i)=><line key={i} x1="200" y1="15" x2="200" y2="205" stroke="#111" strokeWidth="2" transform={"rotate("+(i*10)+" 200 110)"}/>)}</svg></div>
   <div style={{background:"#f3f1e9",display:"grid",placeItems:"center"}}><Word size={120} color="#111315">IS</Word></div>
   <div style={{background:"#17191d",display:"grid",placeItems:"center"}}><Word size={73} color="#fff">ALREADY</Word></div>
   <div style={{background:"#f4f2e9",display:"grid",placeItems:"center"}}><Word size={72} color="#111315">NOW</Word></div>
   <div style={{background:"#f7f5ef",display:"grid",placeItems:"center"}}><Word size={88} color="#111315">HERE</Word></div>
  </div>
  <div style={{position:"absolute",left:80,top:27,color:"#f5f3ed",fontSize:14,fontWeight:850,letterSpacing:".2em"}}>OPEN DESIGN / EDITORIAL WALL</div>
 </AbsoluteFill>;
};

const DepthField=()=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{...full,background:"#0a0b0d",color:"#fff"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%">
   <defs><filter id="depth-blur"><feGaussianBlur stdDeviation="1.4"/></filter></defs>
   {Array.from({length:520},(_,i)=>{
    const a=i*2.399963, ring=180+(i%19)*10, wobble=Math.sin(f*.08+i*.23)*16;
    const x=960+Math.cos(a)*(ring+wobble), y=540+Math.sin(a)*(ring*.62+wobble), z=Math.sin(a*2+f*.04);
    const len=13+(i%7)*2;
    return <line key={i} x1={x} y1={y} x2={x+Math.cos(a+z)*len} y2={y+Math.sin(a+z)*len} stroke={i%9===0?"#9cf15c":"#e8ebe8"} strokeWidth={i%5===0?3:2} opacity={.42+(i%6)*.08}/>;
   })}
   <ellipse cx="960" cy="540" rx="190" ry="125" fill="none" stroke="#8d9b96" strokeOpacity=".15" strokeWidth="1"/>
  </svg>
  <div style={{position:"absolute",left:70,top:56,fontSize:15,fontWeight:900,letterSpacing:".2em",color:"#d9ddda"}}>OPEN DESIGN MOTION REEL — 2026</div>
  <div style={{position:"absolute",right:70,top:56,fontSize:15,fontWeight:900,letterSpacing:".2em",color:"#d9ddda"}}>05 — DEPTH</div>
  <div style={{position:"absolute",left:70,bottom:64,fontSize:15,fontWeight:800,letterSpacing:".18em",color:"#8f9694"}}>128 BPM / BAR 7 OF 8</div>
 </AbsoluteFill>;
};

const EaseGreen=()=>{
 const f=useCurrentFrame(),x=e(f,0,9,65,0);
 return <AbsoluteFill style={{...full,background:"#77ee43",color:"#101710"}}>
  <div style={{position:"absolute",left:0,right:0,top:330,textAlign:"center",transform:"translateX("+x+"px)"}}><Word size={310} color="#101710" tracking={-.12}>EASE</Word></div>
  <div style={{position:"absolute",left:27,top:31,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#16331c"}}>OPEN DESIGN MOTION REEL — 2026</div>
  <div style={{position:"absolute",right:34,top:31,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#16331c"}}>06 — KINETIC TYPE</div>
  <div style={{position:"absolute",left:28,right:28,bottom:26,height:2,background:"#173719",opacity:.6}}/>
 </AbsoluteFill>;
};

const GreenCircleTransition=()=>{
 const f=useCurrentFrame(),r=e(f,0,10,0,610),fade=1-e(f,8,10);
 return <AbsoluteFill style={{...full,background:"#78eb48"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%"><circle cx="960" cy="540" r={r} fill="none" stroke="#b6ff93" strokeWidth="4" opacity={fade}/><circle cx="960" cy="540" r={r*.76} fill="none" stroke="#b6ff93" strokeWidth="2" opacity={fade}/><circle cx={1050+f*8} cy="740" r="7" fill="#121812"/></svg>
  <div style={{position:"absolute",left:26,top:26,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#17371a"}}>07 — END</div>
 </AbsoluteFill>;
};

const NotText=({fullText=false}:{fullText?:boolean})=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{...full,background:"#090a0b",color:"#f5f5f0"}}>
  <div style={{position:"absolute",left:0,right:0,top:430,textAlign:"center",transform:"scale("+(0.96+e(f,0,9)*.04)+")"}}><Word size={fullText?130:126} color="#f4f4f0" tracking={-.065}>{fullText?"Not just":"Not"}</Word></div>
 </AbsoluteFill>;
};

const CoursesPoster=()=>{
 const f=useCurrentFrame(),bob=Math.sin(f/6)*6;
 return <AbsoluteFill style={{...full,background:"#1769e8",overflow:"hidden"}}>
  <div style={{position:"absolute",left:0,top:0,fontSize:18,fontWeight:900,letterSpacing:".13em",color:"#b6d8ff"}}>02 — anything</div>
  <div style={{position:"absolute",right:40,top:0,fontSize:18,fontWeight:900,letterSpacing:".12em",color:"#b6d8ff"}}>PENNYFLOW 00:00:03:00</div>
  <svg viewBox="0 0 660 850" width="660" height="850" style={{position:"absolute",left:0,bottom:-95,transform:"translateY("+bob+"px)"}}>
   <defs><pattern id="course-dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="2.1" fill="#101114"/></pattern></defs>
   <path d="M75 305C10 270 18 150 103 90C160 30 245 38 300 68C382 23 485 86 500 174C585 215 584 345 530 394L515 480L70 480Z" fill="#111315"/>
   <path d="M75 305C10 270 18 150 103 90C160 30 245 38 300 68C382 23 485 86 500 174C585 215 584 345 530 394L515 480L70 480Z" fill="url(#course-dots)"/>
   <path d="M85 230C105 115 420 105 500 230C532 332 474 483 310 535C155 515 65 400 85 230Z" fill="#fff"/>
   <path d="M85 230C105 115 420 105 500 230C532 332 474 483 310 535C155 515 65 400 85 230Z" fill="url(#course-dots)"/>
   <path d="M55 480Q300 420 550 510L665 850H-45Z" fill="#fff"/>
   <path d="M55 480Q300 420 550 510L665 850H-45Z" fill="url(#course-dots)"/>
   <circle cx="210" cy="310" r="34" fill="#111315"/><circle cx="385" cy="310" r="34" fill="#111315"/>
   <circle cx="220" cy="300" r="9" fill="#fff"/><circle cx="395" cy="300" r="9" fill="#fff"/>
   <circle cx="220" cy="365" r="10" fill="#111315"/><circle cx="385" cy="365" r="10" fill="#111315"/>
   <path d="M260 405Q300 437 345 405" stroke="#111315" strokeWidth="10" fill="none" strokeLinecap="round"/>
   <path d="M145 540L135 650M415 545L430 670" stroke="#111315" strokeWidth="12" fill="none"/>
  </svg>
  <div style={{position:"absolute",left:675,top:170,width:410,height:680,borderRadius:28,background:"#fff",boxShadow:"0 12px 34px rgba(0,0,0,.18)",padding:"38px 35px",boxSizing:"border-box"}}>
   <div style={{fontFamily:"monospace",fontSize:24,color:"#777"}}>// course <span style={{float:"right"}}>01</span></div>
   <div style={{height:350,display:"grid",placeItems:"center"}}>
    <svg viewBox="0 0 260 260" width="240" height="240"><path d="M130 12L235 82L130 143L25 82Z" fill="#111315"/><path d="M25 82L130 143V244L25 180Z" fill="#25282b"/><path d="M235 82L130 143V244L235 180Z" fill="#08090a"/><path d="M130 12V143" stroke="#fff" strokeWidth="3" opacity=".75"/></svg>
   </div>
   <div style={{fontSize:52,fontWeight:900,color:"#151719"}}>Courses</div><div style={{fontSize:32,color:"#929292",marginTop:10}}>$149</div>
  </div>
 </AbsoluteFill>;
};

const PosterSequence = () => (
 <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={2}><Comic1952 /></Sequence>
  <Sequence from={2} durationInFrames={17}><Comic1962 /></Sequence>
  <Sequence from={19} durationInFrames={20}><DotPoster /></Sequence>
  <Sequence from={39} durationInFrames={10}><LightSweep1973 /></Sequence>
  <Sequence from={49} durationInFrames={10}><PixelGamePoster /></Sequence>
  <Sequence from={59} durationInFrames={10}><PortfolioFlash /></Sequence>
  <Sequence from={69} durationInFrames={10}><MindPoster /></Sequence>
  <Sequence from={79} durationInFrames={30}><RingPoster /></Sequence>
  <Sequence from={109} durationInFrames={20}><EditorialPosterGrid /></Sequence>
  <Sequence from={129} durationInFrames={10}><DepthField /></Sequence>
  <Sequence from={139} durationInFrames={10}><EaseGreen /></Sequence>
  <Sequence from={149} durationInFrames={10}><EasePoster /></Sequence>
  <Sequence from={159} durationInFrames={10}><OutPoster /></Sequence>
  <Sequence from={169} durationInFrames={10}><NeverPoster /></Sequence>
  <Sequence from={179} durationInFrames={10}><LinearPoster /></Sequence>
  <Sequence from={189} durationInFrames={10}><GreenCircleTransition /></Sequence>
  <Sequence from={199} durationInFrames={5}><ClockPoster /></Sequence>
  <Sequence from={204} durationInFrames={12}><StatsPoster /></Sequence>
  <Sequence from={216} durationInFrames={10}><MotionFilmsPoster /></Sequence>
  <Sequence from={226} durationInFrames={10}><EyePoster /></Sequence>
  <Sequence from={236} durationInFrames={10}><CoursesPoster /></Sequence>
  <Sequence from={246} durationInFrames={10}><Future3D /></Sequence>
  <Sequence from={256} durationInFrames={10}><NotText fullText={false}/></Sequence>
  <Sequence from={266} durationInFrames={13}><NotText fullText={true}/></Sequence>
 </AbsoluteFill>
);
const NotJustOpus = () => {
 const f=useCurrentFrame(),p=pop(f,30,1,110,16),shift=e(f,0,24,70,0);
 return <AbsoluteFill style={{...full,background:"#08090b",color:"#fff"}}>
  <div style={{position:"absolute",left:0,right:0,top:355,display:"flex",justifyContent:"center",alignItems:"center",gap:20,transform:"translateX("+shift+"px) scale("+(0.94+.06*p)+")"}}>
   <Word size={133} color="#f5f4f0" tracking={-.075}>Not just</Word>
   <div style={{background:"#e98e78",color:"#111315",padding:"12px 32px 22px",borderRadius:24,transform:"rotate(-1deg)",boxShadow:"0 13px 0 rgba(0,0,0,.2)"}}><Word size={129} color="#111315" tracking={-.075}>Opus 5.5.</Word></div>
  </div>
 </AbsoluteFill>;
};

const LogoChip = ({ index, frame }: { index: number; frame: number }) => {
  const { fps } = useVideoConfig();
  const p = pop(frame, fps, index * 2, 125, 16);
  const symbols = ["A", "✳", "M", "◈", "✦", "∞", "G", "⌘", "◉", "N"];
  const colors = ["#263b75", "#e66b52", "#303239", "#5275bf", "#d39d53", "#4c8b74", "#363d86", "#21252c", "#b7a2cf", "#547c91"];
  return (
    <div style={{
      width: 76,
      height: 76,
      borderRadius: 23,
      background: colors[index],
      color: "#fff",
      display: "grid",
      placeItems: "center",
      fontSize: 30,
      fontWeight: 950,
      boxShadow: "0 12px 28px rgba(23,37,45,.18)",
      border: "2px solid rgba(255,255,255,.7)",
      transform: "translateY(" + ((1 - p) * 100) + "px) rotate(" + ((1 - p) * (index % 2 ? -19 : 19)) + "deg)",
    }}>{symbols[index]}</div>
  );
};


const ProviderBadge=({index,frame=0}:{index:number;frame?:number})=>{
 const palettes=["#f2a64c","#e9f0ff","#15191e","#8d7be8","#e7ebf1","#f4a28a","#cce3d5","#111315"];
 const symbol=["✣","◉","⬟",">","◆","✦","●","◈"][index%8];
 return <div style={{width:104,height:104,borderRadius:"50%",background:"#fff",display:"grid",placeItems:"center",boxShadow:"0 10px 24px rgba(0,0,0,.12)",border:"3px solid rgba(255,255,255,.8)",transform:"translateY("+Math.sin(frame/8+index)*3+"px)"}}>
  <div style={{width:64,height:64,borderRadius:index%3===0?14:"50%",background:palettes[index%8],display:"grid",placeItems:"center",color:index%8===1?"#5368be":"#fff",fontSize:40,fontWeight:950,boxShadow:"inset 0 0 0 3px rgba(0,0,0,.08)"}}>{symbol}</div>
 </div>;
};
const ModelAgentScene=()=>{
 const f=useCurrentFrame();
 const Phrase=({phase}:{phase:number})=><div style={{position:"absolute",left:0,right:0,top:360,height:310,display:"flex",alignItems:"center",justifyContent:"center"}}>
  {phase<2?<div style={{position:"relative",width:1180,height:260}}>
   <div style={{position:"absolute",left:0,top:22,fontFamily:displayFont,fontSize:176,fontWeight:950,color:"#08090b",letterSpacing:"-.095em"}}>Any m</div>
   <div style={{position:"absolute",left:646,top:23,fontFamily:displayFont,fontSize:176,fontWeight:950,color:"#08090b",letterSpacing:"-.095em",opacity:1-e(f,33,53)}}>odel.</div>
   <div style={{position:"absolute",left:650+e(f,33,53)*58,top:33,width:118,height:118,borderRadius:"50%",background:"#fff",border:"9px solid rgba(15,20,25,.8)",display:"grid",placeItems:"center",boxShadow:"0 8px 20px rgba(0,0,0,.1)"}}><ProviderBadge index={phase===0?3:1} frame={f}/></div>
   {phase===1?<div style={{position:"absolute",left:745,top:145,fontSize:145,fontWeight:950,color:"rgba(0,0,0,.12)",letterSpacing:"-.08em"}}>del.</div>:null}
  </div>:<div style={{display:"flex",alignItems:"center",width:1600,justifyContent:"space-between"}}>
   <Word size={170} color="#101113" tracking={-.09}>Any</Word>
   <div style={{display:"flex",gap:phase===2?12:9,alignItems:"center",marginLeft:5,marginRight:8}}>
    {(phase===2?[0,1,2,3]:[0,1,2,3,4,5,6]).map(v=><ProviderBadge key={v} index={v} frame={f}/>)}
   </div>
   <Word size={170} color="#101113" tracking={-.09}>agent.</Word>
  </div>}
 </div>;
 return <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={39}><AbsoluteFill style={{background:"#8fc5dd"}}><Phrase phase={0}/></AbsoluteFill></Sequence>
  <Sequence from={39} durationInFrames={39}><AbsoluteFill style={{background:"#acd7e5"}}><Phrase phase={1}/></AbsoluteFill></Sequence>
  <Sequence from={78} durationInFrames={30}><AbsoluteFill style={{background:"#dfa77f"}}><Phrase phase={2}/></AbsoluteFill></Sequence>
  <Sequence from={108} durationInFrames={30}><AbsoluteFill style={{background:"#bfdccf"}}><Phrase phase={3}/></AbsoluteFill></Sequence>
 </AbsoluteFill>;
};


const PreviewArtwork=({variant,frame}:{variant:number;frame:number})=>{
 if(variant===0)return <div style={{position:"absolute",inset:0,background:"#eee5cf",overflow:"hidden"}}>
  <svg viewBox="0 0 1000 650" width="100%" height="100%">
   <defs><filter id="paper-grain"><feTurbulence type="fractalNoise" baseFrequency=".65" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter><filter id="mountain-soft"><feGaussianBlur stdDeviation="2.5"/></filter></defs>
   <rect width="1000" height="650" fill="#eee5cf"/><rect width="1000" height="650" filter="url(#paper-grain)" opacity=".12"/>
   <text x="500" y="88" fontFamily="Georgia" fontSize="74" textAnchor="middle" fill="#1c1a15">100</text><text x="500" y="126" fontFamily="serif" fontSize="25" textAnchor="middle" fill="#28231c">宋 · 水墨</text>
   <path d="M0 390L100 315 155 344 225 245 290 350 375 270 445 340 510 235 595 330 690 255 765 350 835 267 900 335 1000 285V650H0Z" fill="#c5c0b3" opacity=".8" filter="url(#mountain-soft)"/>
   <path d="M0 450L95 400 155 424 250 344 330 420 415 360 500 430 580 355 675 430 770 365 855 433 930 374 1000 420V650H0Z" fill="#a9a69e" opacity=".65"/>
   <path d="M0 510L115 465 190 493 290 430 375 480 480 430 560 485 670 425 755 485 850 440 945 490 1000 470V650H0Z" fill="#8d908c" opacity=".52"/>
   <g transform={"translate(500 350) rotate("+(Math.sin(frame/30)*1.5)+")"} fill="none" stroke="#181815" strokeWidth="12" strokeLinecap="round">
    <path d="M-205 110C-240 -40 -150 -160 8 -160C170 -160 240 -33 198 95" strokeWidth="22" opacity=".95"/><path d="M-192 120C-225 -27 -136 -140 6 -144C145 -145 219 -26 185 89" strokeWidth="5" opacity=".85"/><path d="M-176 110C-205 -14 -125 -122 7 -125C130 -126 195 -15 171 77" strokeWidth="5" opacity=".75"/>
    <path d="M-5 -65L78 6L-5 78Z" fill="#161715" stroke="none" transform="rotate(-22)"/>
   </g>
   <path d="M820 140Q880 190 940 145" stroke="#23221c" strokeWidth="8" fill="none"/><path d="M60 235q22 -22 45 0M125 245q18 -18 36 0" stroke="#24211b" fill="none" strokeWidth="4"/>
   <rect x="780" y="445" width="78" height="94" fill="#c53d32"/><text x="819" y="502" textAnchor="middle" fontFamily="serif" fontSize="43" fill="#f7e8d4">設</text>
  </svg>
 </div>;
 if(variant===1)return <div style={{position:"absolute",inset:0,background:"#f1e5c8",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:"7% 5%",borderTop:"8px solid #c99a36",borderBottom:"8px solid #c99a36",background:"repeating-linear-gradient(0deg,rgba(135,102,50,.04) 0 2px,transparent 2px 9px)"}}/>
  <div style={{position:"absolute",left:"2%",top:"24%",width:"24%",height:"56%",fontFamily:"Georgia,serif",fontWeight:700,fontSize:22,lineHeight:1.5,color:"#28221a",overflow:"hidden"}}>et lux in tenebris signum apertum ab initio erat idea et forma et forma et lux in tenebris</div>
  <div style={{position:"absolute",right:"2%",top:"24%",width:"23%",height:"56%",fontFamily:"Georgia,serif",fontWeight:700,fontSize:22,lineHeight:1.5,color:"#28221a",overflow:"hidden"}}>idea et idea erat forma forma facta est lux in lucet designum omnibus ab initio erat forma</div>
  <div style={{position:"absolute",left:"27%",right:"26%",top:"25%",bottom:"17%",background:"#1549a0",border:"8px solid #c79935",boxShadow:"inset 0 0 0 7px #142f6d"}}>
   <div style={{position:"absolute",inset:18,backgroundImage:"radial-gradient(#d9edff 1.6px,transparent 1.6px)",backgroundSize:"29px 29px"}}/>
   <div style={{position:"absolute",left:"50%",top:"50%",width:300,height:300,marginLeft:-150,marginTop:-150,borderRadius:"50%",border:"30px solid #dba83d",background:"#2355ab",boxShadow:"inset 0 0 0 13px #f2cf71",display:"grid",placeItems:"center"}}><svg viewBox="0 0 100 100" width="190" height="190"><path d="M22 8L87 55L48 58L41 96Z" fill="#b83224" stroke="#f6d58b" strokeWidth="4"/></svg></div>
  </div>
  <div style={{position:"absolute",left:0,right:0,top:"10%",textAlign:"center",color:"#a64035",fontFamily:"Georgia,serif"}}><div style={{fontSize:40,fontWeight:900}}>1290</div><div style={{fontSize:24}}>Gothic illumination</div></div>
 </div>;
 if(variant===2)return <div style={{position:"absolute",inset:0,background:"#83ec45",overflow:"hidden"}}><div style={{position:"absolute",inset:0,backgroundImage:"linear-gradient(rgba(0,0,0,.08) 1px,transparent 1px)",backgroundSize:"100% 12px"}}/><div style={{position:"absolute",top:"27%",left:"-7%",width:"114%",textAlign:"center",fontFamily:displayFont,fontSize:118,fontWeight:950,letterSpacing:"-.09em",lineHeight:1.15,color:"#11160e",textShadow:"7px 7px 0 rgba(25,40,15,.28)"}}>OPEN<br/>DESIGN</div><div style={{position:"absolute",right:24,top:16,fontSize:12,color:"#284b20",fontWeight:900}}>SHOWREEL / OPEN</div><div style={{position:"absolute",left:0,right:0,top:"49%",height:2,background:"#11190d",opacity:.5}}/></div>;
 if(variant===3)return <div style={{position:"absolute",inset:0,background:"#f5f4ef",overflow:"hidden"}}><svg viewBox="0 0 1000 650" width="100%" height="100%">{Array.from({length:18},(_,i)=><path key={i} d={"M"+(-130+i*72)+" -30 C"+(90+i*30)+" 120 "+(-70+i*62)+" 390 "+(150+i*55)+" 700"} stroke="#111315" strokeWidth="34" fill="none" strokeLinecap="round"/>)}</svg></div>;
 if(variant===4)return <div style={{position:"absolute",inset:0,background:"#83ed43",overflow:"hidden"}}><div style={{position:"absolute",left:"-6%",right:"-8%",top:"31%",textAlign:"center",fontFamily:displayFont,fontWeight:950,fontSize:210,letterSpacing:"-.12em",color:"#12170e",textShadow:"10px 11px 0 rgba(36,58,18,.26)"}}>EASE</div><div style={{position:"absolute",left:22,right:22,bottom:28,height:2,background:"#1b3314",opacity:.55}}/><div style={{position:"absolute",left:22,bottom:37,fontSize:12,color:"#1b3314"}}>66 FPS</div><div style={{position:"absolute",right:22,bottom:37,fontSize:12,color:"#1b3314"}}>128 BPM</div></div>;
 if(variant===5)return <div style={{position:"absolute",inset:0,background:"linear-gradient(90deg,#f2f1ea 0 52%,#1746d6 52% 100%)",overflow:"hidden"}}><div style={{position:"absolute",left:38,top:50,fontSize:19,fontWeight:950,color:"#111315",letterSpacing:".16em"}}>CREATIVE / 03</div><div style={{position:"absolute",left:"12%",top:"22%",fontSize:390,fontWeight:950,fontFamily:displayFont,color:"#151719",letterSpacing:"-.12em",textShadow:"9px 11px 0 rgba(0,0,0,.16)"}}>3</div><div style={{position:"absolute",right:44,bottom:42,color:"#fff",fontSize:18,fontWeight:900,letterSpacing:".2em"}}>READY / MOTION</div></div>;
 return <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#f2f0e8,#fff)",overflow:"hidden"}}><div style={{position:"absolute",inset:0,display:"grid",placeItems:"center",fontSize:430,fontWeight:950,color:"#111315",fontFamily:displayFont,textShadow:"12px 14px 0 rgba(0,0,0,.15)"}}>3</div></div>;
};

const CountdownArtwork = ({ value, frame }: { value: number; frame: number }) => {
  const p = pop(frame, 30, 0, 75, 14);
  const scale = .82 + p * .18;
  return (
    <AbsoluteFill style={{ background: "linear-gradient(115deg,#10131b 0%,#141b38 52%,#2a41c1 100%)", color: "#f4f6ff" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(ellipse at 50% 50%,rgba(71,104,255,.4),transparent 50%),linear-gradient(90deg,transparent 49%,rgba(255,255,255,.08) 50%,transparent 51%)", backgroundSize: "100% 100%,50px 50px" }} />
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", perspective: 1200 }}>
        <div style={{
          fontSize: 490,
          lineHeight: .8,
          fontFamily: displayFont,
          fontWeight: 950,
          letterSpacing: "-.12em",
          color: "#eef0fa",
          transform: "rotateX(" + (12 + Math.sin(frame / 7) * 3) + "deg) rotateY(-11deg) scale(" + scale + ")",
          textShadow: "1px 1px 0 #c4cce9,3px 3px 0 #9ba9df,6px 6px 0 #7185d5,10px 10px 0 #4b63b5,15px 18px 0 #253c89,28px 36px 35px rgba(0,0,0,.55)",
        }}>{value}</div>
      </div>
      <div style={{ position: "absolute", left: 40, bottom: 25, fontSize: 15, fontWeight: 850, color: "#aebcf8", letterSpacing: ".18em" }}>3 / 2 / 1 — THE MOMENT MOVES</div>
    </AbsoluteFill>
  );
};


const LaunchKitWindow=({frame,variant,countdown=-1}:{frame:number;variant:number;countdown?:number})=>{
 const {fps}=useVideoConfig(),p=pop(frame,fps,0,84,19);
 const names=["Claude Opus 5.5","GPT-6-Astra","Gemini","MiMo","Cursor","Antigravity","Kilo Code"];
 const name=names[variant%names.length];
 const symbols=["✣","◉","➤","M","◆","▲","K"];
 const colors=["#df805b","#8c9bff","#222a39","#4b93a4","#111315","#6a54d5","#373c40"];
 return <AbsoluteFill style={{...full,background:"#f3f1ed"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 48% 40%,#fff,#f1f0eb 72%)"}}/>
  <div style={{position:"absolute",left:118,right:118,top:72,bottom:72,borderRadius:24,background:"#fff",border:"1px solid #e9e8e3",boxShadow:"0 28px 78px rgba(30,35,38,.15)",transform:"translateY("+((1-p)*44)+"px) scale("+(0.985+.015*p)+")",overflow:"hidden"}}>
   <div style={{position:"absolute",top:0,left:0,right:0,height:64,borderBottom:"1px solid #efeee9",display:"flex",alignItems:"center",padding:"0 28px",gap:14,background:"#fff"}}>{["#e5e5df","#e5e5df","#e5e5df"].map((c,i)=><div key={i} style={{width:15,height:15,borderRadius:"50%",background:c}}/>)}<div style={{marginLeft:14,fontSize:21,fontWeight:850,color:"#252a2d"}}>Launch film</div></div>
   <div style={{position:"absolute",top:64,bottom:0,left:0,width:700,borderRight:"1px solid #efeee9",background:"#fff"}}>
    <div style={{position:"absolute",left:260,top:52,width:340,minHeight:106,background:"#f0efec",color:"#222629",borderRadius:"25px 25px 5px 25px",padding:"19px 24px",fontSize:25,lineHeight:1.42,boxSizing:"border-box"}}>Make a 10s launch film<br/>for our app.</div>
    <div style={{position:"absolute",left:38,right:36,bottom:36,height:164,border:"1px solid #e7e7e2",borderRadius:25,background:"#fff",padding:"19px 22px",boxSizing:"border-box",boxShadow:"0 3px 12px rgba(20,25,28,.04)"}}>
     <div style={{color:"#434a4c",fontSize:21}}>Make it feel like a launch.</div>
     <div style={{position:"absolute",left:22,bottom:18,display:"flex",alignItems:"center",gap:12}}>
      <div style={{width:48,height:48,borderRadius:"50%",border:"2px solid #e9e9e6",display:"grid",placeItems:"center",color:"#8c9290",fontSize:24}}>＋</div>
      <div style={{width:48,height:48,borderRadius:"50%",border:"2px solid #e9e9e6",display:"grid",placeItems:"center",color:"#8c9290",fontSize:23}}>◎</div>
      <div style={{background:"#e8f7e6",color:"#217c38",borderRadius:8,padding:"11px 18px",fontSize:20,fontWeight:900,whiteSpace:"nowrap"}}>▣ Motion</div>
      <div style={{display:"flex",alignItems:"center",gap:10,background:"#f5f4f1",padding:"7px 10px",borderRadius:26,whiteSpace:"nowrap"}}>
       <div style={{width:34,height:34,borderRadius:9,background:colors[variant%7],display:"grid",placeItems:"center",color:"#fff",fontSize:20,fontWeight:950}}>{symbols[variant%7]}</div>
       <div style={{fontSize:20,color:"#252a2d",fontWeight:850}}>{name}</div>
      </div>
     </div>
     <div style={{position:"absolute",right:12,bottom:15,width:60,height:60,borderRadius:"50%",background:"#101416",display:"grid",placeItems:"center"}}><svg viewBox="0 0 30 30" width="25" height="25"><path d="M5 15H24M16 6L25 15L16 24" stroke="#71e34b" strokeWidth="2.8" fill="none"/></svg></div>
    </div>
    {variant!==0?<div style={{position:"absolute",left:350,top:520,fontSize:24,fontWeight:850,color:"#4b4f50",fontStyle:"italic"}}>{name}</div>:null}
   </div>
   <div style={{position:"absolute",left:700,right:0,top:64,bottom:0,background:"#f6f5f1",padding:"24px 27px 27px",boxSizing:"border-box"}}>
    <div style={{fontSize:22,color:"#777f81",fontWeight:850,marginBottom:18}}>Preview</div>
    <div style={{position:"absolute",left:27,right:27,top:108,bottom:27,background:"#fff",borderRadius:20,border:"1px solid #e9e8e2",overflow:"hidden",boxShadow:"0 1px 3px rgba(0,0,0,.04)"}}>
     {countdown>=0?<CountdownArtwork value={countdown} frame={frame}/>:<PreviewArtwork variant={variant} frame={frame}/>}
     <div style={{position:"absolute",left:22,top:18,display:"flex",alignItems:"center",gap:10,background:"rgba(255,255,255,.96)",borderRadius:30,padding:"10px 17px",color:"#30383b",fontSize:20,fontWeight:800,boxShadow:"0 5px 16px rgba(0,0,0,.1)"}}>
      <span style={{color:"#8a8f91",fontWeight:600}}>Made with</span><span style={{width:34,height:34,borderRadius:8,background:colors[variant%7],color:"#fff",display:"grid",placeItems:"center",fontSize:21}}>{symbols[variant%7]}</span>{name}
     </div>
    </div>
   </div>
  </div>
 </AbsoluteFill>;
};

const LaunchVariant = ({ variant, countdown = -1 }: { variant: number; countdown?: number }) => {
  const frame = useCurrentFrame();
  return <LaunchKitWindow frame={frame} variant={variant} countdown={countdown} />;
};


const LaunchKitSequence=()=>{
 const frame=useCurrentFrame();
 const variant=frame<23?0:frame<31?1:frame<39?2:frame<47?3:frame<55?4:frame<63?5:6;
 const countdown=frame<90?-1:frame<99?3:frame<108?2:1;
 return <LaunchKitWindow frame={frame} variant={variant} countdown={countdown}/>;
};

const CountdownSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={20}><LaunchVariant variant={0} countdown={3} /></Sequence>
    <Sequence from={20} durationInFrames={20}><LaunchVariant variant={1} countdown={2} /></Sequence>
    <Sequence from={40} durationInFrames={20}><LaunchVariant variant={2} countdown={1} /></Sequence>
  </AbsoluteFill>
);


const CubeFace=({kind,transform,frame}:{kind:number;transform:string;frame:number})=>{
 const style:React.CSSProperties={position:"absolute",inset:0,width:"100%",height:"100%",overflow:"hidden",borderRadius:44,border:"2px solid rgba(255,255,255,.74)",boxSizing:"border-box",backfaceVisibility:"hidden",transform,boxShadow:"inset 0 0 0 2px rgba(255,255,255,.17),inset 0 -18px 32px rgba(0,0,0,.13)"};
 return <div style={style}>
  {kind===0?<div style={{position:"absolute",inset:0,background:"linear-gradient(90deg,#e77d8d 0 14%,#e9bb47 14% 86%,#df7b8b 86% 100%)"}}>
   <div style={{position:"absolute",left:0,right:0,top:0,height:"18%",background:"#e8be47"}}/>
   <div style={{position:"absolute",left:35,right:35,top:35,bottom:52,borderRadius:"50%",background:"#efe6cb",border:"14px solid #fff6e6",boxShadow:"0 9px 0 rgba(80,52,22,.18),inset 0 0 0 8px #c7a06a",display:"grid",placeItems:"center"}}>
    <div style={{position:"relative",width:205,height:220,borderRadius:"48% 48% 43% 43%",background:"#dba27d",overflow:"hidden",boxShadow:"inset 0 -12px 18px rgba(83,43,28,.15)"}}>
     <div style={{position:"absolute",left:0,top:0,width:205,height:75,background:"#392d27",borderRadius:"50% 50% 25% 25%"}}/>
     <div style={{position:"absolute",left:16,top:48,width:48,height:145,background:"#44332d",borderRadius:"30px 25px 18px 22px"}}/><div style={{position:"absolute",right:16,top:48,width:48,height:145,background:"#44332d",borderRadius:"25px 30px 22px 18px"}}/>
     <div style={{position:"absolute",left:60,top:105,width:16,height:20,borderRadius:"50%",background:"#181715",boxShadow:"70px 0 0 #181715"}}/>
     <div style={{position:"absolute",left:48,top:143,width:28,height:18,borderRadius:"50%",background:"#ed9994",opacity:.78,boxShadow:"82px 0 0 #ed9994"}}/>
     <div style={{position:"absolute",left:88,top:148,width:30,height:18,borderBottom:"5px solid #4d2822",borderRadius:"50%"}}/>
     <div style={{position:"absolute",left:55,right:55,bottom:0,height:54,background:"#178778",clipPath:"polygon(0 0,100% 0,100% 100%,0 100%)"}}/>
    </div>
   </div>
   <div style={{position:"absolute",right:25,top:22,width:52,height:62,background:"#fff",display:"grid",placeItems:"center",boxShadow:"0 3px 7px rgba(0,0,0,.12)"}}><div style={{width:33,height:33,borderRadius:8,background:"#111",display:"grid",placeItems:"center",color:"#fff",fontSize:22}}>◉</div></div>
   <div style={{position:"absolute",right:20,bottom:42,width:26,height:37,background:"#f3f0db",borderRadius:4}}><div style={{position:"absolute",left:8,top:-18,width:12,height:20,borderRadius:"50%",background:"#da4a54"}}/></div>
   <div style={{position:"absolute",left:0,right:0,bottom:0,height:48,background:"#342a78"}}/>
  </div>:
  kind===1?<div style={{position:"absolute",inset:0,background:"#111315",display:"grid",placeItems:"center"}}><svg viewBox="0 0 360 360" width="100%" height="100%"><path d="M120 30Q42 30 42 110V250Q42 322 118 322H242Q318 322 318 242V117Q318 42 242 42Z" fill="#fff"/><circle cx="180" cy="180" r="104" fill="#111315" stroke="#fff" strokeWidth="14"/><path d="M137 87L246 177L162 190L151 272Z" fill="#fff"/></svg></div>:
  kind===2?<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#ee8fa3,#eac54c 48%,#4b3c9a)"}}><Word size={70} color="#151719" style={{position:"absolute",left:24,top:34}}>MORRO</Word><div style={{position:"absolute",inset:70,border:"10px solid rgba(255,255,255,.8)",borderRadius:34}}/><div style={{position:"absolute",right:30,bottom:25,width:78,height:78,borderRadius:"50%",background:"#f7eed7"}}/></div>:
  kind===3?<div style={{position:"absolute",inset:0,background:"#1748c7"}}><svg viewBox="0 0 360 360" width="100%" height="100%">{Array.from({length:10},(_,i)=><path key={i} d={"M"+(i*42-60)+" 0L"+(i*35+90)+" 360"} stroke="#d9e6ff" strokeWidth="6" opacity=".55"/>)}<circle cx="180" cy="180" r="105" fill="#e8edff" opacity=".9"/><path d="M120 160L180 115L235 184L180 248Z" fill="#292e4b"/></svg></div>:
  kind===4?<div style={{position:"absolute",inset:0,background:"#f3e7cd"}}><div style={{position:"absolute",inset:25,border:"8px solid #151718"}}/><Word size={68} color="#121719" style={{position:"absolute",left:22,top:55}}>EASE</Word><div style={{position:"absolute",right:30,bottom:30,width:100,height:100,borderRadius:"50%",background:"#e44f43"}}/></div>:
  <div style={{position:"absolute",inset:0,background:"#d34e3b"}}><Word size={72} color="#fff1db" style={{position:"absolute",left:22,top:36}}>OPEN</Word><Word size={62} color="#fff1db" style={{position:"absolute",left:22,top:112}}>DESIGN</Word><div style={{position:"absolute",right:28,bottom:26,width:92,height:92,border:"11px solid #fff",borderRadius:"50%"}}/></div>}
  <div style={{position:"absolute",inset:0,borderRadius:42,pointerEvents:"none",background:"linear-gradient(135deg,rgba(255,255,255,.34),transparent 31%,rgba(0,0,0,.12) 100%)"}}/>
 </div>;
};
const ProjectCube=()=>{
 const f=useCurrentFrame();
 const rotateY=-28-300*e(f,0,126),rotateX=18+5*Math.sin(f/17),rotateZ=-3+Math.sin(f/18)*2;
 const scale=(.72+.28*e(f,0,18))*(1-.2*e(f,108,126)),size=470,z=size/2;
 return <AbsoluteFill style={{...full,background:"#f3f0e9"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 80%,rgba(25,27,31,.12),transparent 42%)"}}/>
  <div style={{position:"absolute",left:"50%",top:"47%",width:size,height:size,perspective:1450,transform:"translate(-50%,-50%)"}}>
   <div style={{position:"absolute",inset:0,transformStyle:"preserve-3d",transform:"rotateX("+rotateX+"deg) rotateY("+rotateY+"deg) rotateZ("+rotateZ+"deg) scale("+scale+")"}}>
    <CubeFace kind={0} frame={f} transform={"translateZ("+z+"px)"}/>
    <CubeFace kind={1} frame={f} transform={"rotateY(90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={2} frame={f} transform={"rotateY(-90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={3} frame={f} transform={"rotateX(90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={4} frame={f} transform={"rotateX(-90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={5} frame={f} transform={"rotateY(180deg) translateZ("+z+"px)"}/>
   </div>
  </div>
  <div style={{position:"absolute",left:"50%",top:"80%",width:600,height:95,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"rgba(18,22,29,.13)",filter:"blur(36px)"}}/>
 </AbsoluteFill>;
};

const MorroCubeIntro=()=>{
 const f=useCurrentFrame(),p=e(f,0,35);
 return <AbsoluteFill style={{...full,background:"#f5f4ed",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,display:"flex",flexDirection:"column",justifyContent:"space-between",padding:"-90px 0",transform:"translateX("+(-30*p)+"px)"}}>
   <Word size={290} color="#101113" tracking={-.12}>MORRO</Word>
   <Word size={290} color="#f5f4ed" tracking={-.12} style={{WebkitTextStroke:"4px #101113"}}>MORRO</Word>
   <Word size={290} color="#101113" tracking={-.12}>MORRO</Word>
  </div>
  <div style={{position:"absolute",left:690,top:110,width:620,height:790,transform:"translateY("+(-18*p)+"px) rotate(-2deg)",background:"rgba(255,255,255,.2)",clipPath:"polygon(48% 0,100% 19%,96% 73%,51% 100%,0 77%,5% 20%)",border:"1px solid rgba(0,0,0,.24)",boxShadow:"0 24px 35px rgba(0,0,0,.12)"}}>
   <svg viewBox="0 0 620 790" width="100%" height="100%"><path d="M310 0L600 150L590 570L310 790L24 605L30 145Z" fill="rgba(255,255,255,.32)" stroke="#999" strokeWidth="4"/><path d="M310 0L310 790M30 145L590 570M600 150L24 605" stroke="#9c9c9c" strokeWidth="3" fill="none"/><path d="M180 430L300 340L435 445L310 535Z" fill="#79837f" opacity=".52"/></svg>
  </div>
  <div style={{position:"absolute",right:80,top:70,width:210,height:200,border:"2px solid #191a1b",background:"#f5f4ed",padding:16,boxSizing:"border-box",fontSize:16,fontWeight:900,letterSpacing:".12em",lineHeight:1.8}}>SPEC / PRISM<br/>MATERIAL<br/>IOR<br/>ROUGH<br/>ROT/S</div>
 </AbsoluteFill>;
};

const TexturedCube=()=> <ProjectCube />;

const FinalLockup=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,78,18),fade=e(f,0,12);
 return <AbsoluteFill style={{...full,background:"#f5f4ed"}}>
  <div style={{position:"absolute",left:0,right:0,top:250,display:"flex",flexDirection:"column",alignItems:"center",transform:"translateY("+((1-p)*24)+"px)",opacity:fade}}>
   <div style={{width:230,height:230,borderRadius:48,background:"#101113",display:"grid",placeItems:"center"}}>
    <svg viewBox="0 0 100 100" width="206" height="206"><path d="M26 10H72C86 10 92 17 92 31V70C92 85 83 92 68 92H28C14 92 8 84 8 70V30C8 17 14 10 26 10Z" fill="#fff"/><circle cx="52" cy="49" r="31" fill="#111315"/><path d="M38 25L70 49L47 52L42 74Z" fill="#fff"/></svg>
   </div>
   <div style={{marginTop:64,fontFamily:displayFont,fontSize:84,fontWeight:950,color:"#14191b",letterSpacing:"-.075em"}}>OpenDesign Motion</div>
   <div style={{marginTop:74,background:"#10313a",color:"#e7f3f2",borderRadius:26,padding:"12px 42px",fontSize:31,fontWeight:850,letterSpacing:".005em"}}><span style={{color:"#a0dcaa"}}>•</span> open-design.ai</div>
  </div>
 </AbsoluteFill>;
};

export const OpenDesignMotion: React.FC = () => (
  <AbsoluteFill style={{ ...full, background: "#101214" }}>
    <Sequence from={0} durationInFrames={83}><OpeningScene /></Sequence>
    <Sequence from={83} durationInFrames={90}><HeroTitle /></Sequence>
    <Sequence from={173} durationInFrames={36}><BrandReveal /></Sequence>
    <Sequence from={209} durationInFrames={35}><ClaimScene /></Sequence>
    <Sequence from={244} durationInFrames={77}><GalleryWall /></Sequence>
    <Sequence from={321} durationInFrames={279}><PosterSequence /></Sequence>
    <Sequence from={600} durationInFrames={41}><NotJustOpus /></Sequence>
    <Sequence from={641} durationInFrames={138}><ModelAgentScene /></Sequence>
    <Sequence from={779} durationInFrames={116}><LaunchKitSequence /></Sequence>
    <Sequence from={895} durationInFrames={38}><MorroCubeIntro /></Sequence>
    <Sequence from={933} durationInFrames={126}><TexturedCube /></Sequence>
    <Sequence from={1059} durationInFrames={60}><FinalLockup /></Sequence>
    <Audio src={staticFile("audio/opendesign-motion-score.wav")} volume={0.92} />
  </AbsoluteFill>
);