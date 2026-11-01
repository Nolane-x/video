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
  const highlight = e(f, 17, 31);
  const title = e(f, 3, 15);
  const drift = e(f, 0, 50, 25, -20);
  return (
    <AbsoluteFill style={{ ...full, background: "#e9e5db" }}>
      <div style={{
        position: "absolute", inset: -40, opacity: .42,
        display: "grid", gridTemplateColumns: "repeat(4,1fr)", gridTemplateRows: "repeat(3,1fr)",
        gap: 17, transform: "perspective(1600px) rotateY(-7deg) translateX(" + drift + "px) scale(1.12)",
        filter: "saturate(.78)",
      }}>
        {Array.from({ length: 12 }, (_, i) => (
          <div key={i} style={{ position: "relative", minHeight: 140, overflow: "hidden", boxShadow: "0 10px 24px rgba(0,0,0,.12)" }}>
            <GalleryPoster index={i} frame={f + i * 4} />
          </div>
        ))}
      </div>
      <div style={{
        position: "absolute", left: 360, right: 360, top: 278, bottom: 260,
        background: "rgba(255,255,255,.97)", boxShadow: "0 34px 90px rgba(40,45,44,.15)",
        border: "1px solid rgba(255,255,255,.9)", borderRadius: 4,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        opacity: title, transform: "translateY(" + ((1 - title) * 38) + "px)",
      }}>
        <div style={{ display: "flex", justifyContent: "center", alignItems: "baseline", gap: 17, whiteSpace: "nowrap" }}>
          <Word size={83} weight={900}>The</Word>
          <span style={{ position: "relative", display: "inline-block" }}>
            <span style={{ position: "absolute", left: -7, right: -9, top: "56%", height: 54, background: "#b8eb50", transform: "scaleX(" + highlight + ") rotate(-1deg)", transformOrigin: "left center" }} />
            <span style={{ position: "relative" }}><Word size={90} weight={950}>open-source</Word></span>
          </span>
        </div>
        <Word size={84} weight={900}>alternative</Word>
        <div style={{ marginTop: 23, display: "flex", alignItems: "center", gap: 10, color: "#8d8b86" }}>
          <span style={{ fontSize: 27 }}>to</span>
          <RadialMark frame={f} size={32} color="#e76c55" />
          <span style={{ fontSize: 32, fontWeight: 850, color: "#202124", letterSpacing: "-.05em" }}>Claude Motion.</span>
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
 const drift=Math.sin((frame+index*13)/18)*5,rotation=(index%2?-1:1)*(1+Math.sin(frame/19+index)*.55);
 return <div style={{width:270,height:152,borderRadius:8,position:"relative",overflow:"hidden",transform:"translateY("+drift+"px) rotate("+rotation+"deg)",boxShadow:"0 16px 34px rgba(19,24,32,.18),0 2px 6px rgba(19,24,32,.1)",background:"#fff"}}><GalleryPoster index={index} frame={frame}/><div style={{position:"absolute",left:10,bottom:7,fontSize:7,fontWeight:950,letterSpacing:".2em",color:"rgba(20,25,30,.58)"}}>OD / 0{index+1}</div></div>;
}


const GalleryWall=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,72,17),pan=e(f,0,77,68,-180),rotation=e(f,0,77,8,-6);
 return <AbsoluteFill style={{...full,background:"#f1efe9"}}>
  <div style={{position:"absolute",left:76,top:46,fontSize:16,fontWeight:950,letterSpacing:".2em",color:"#363b3e"}}>OPEN DESIGN / MOTION COLLECTION</div>
  <div style={{position:"absolute",right:78,top:46,fontSize:14,fontWeight:850,letterSpacing:".18em",color:"#8a8f8e"}}>SELECTED WORKS / 2026</div>
  <div style={{position:"absolute",left:76,top:115,width:1768,display:"grid",gridTemplateColumns:"repeat(6,1fr)",gap:14,transform:"perspective(1750px) rotateY("+rotation+"deg) rotateX(3deg) translateX("+pan+"px) translateY("+((1-p)*100)+"px) scale("+(0.9+p*.13)+")",transformOrigin:"center center"}}>
   {Array.from({length:30},(_,i)=><GalleryCard key={i} index={i%12} frame={f+i*2}/>)}
  </div><div style={{position:"absolute",bottom:49,right:82,fontSize:14,color:"#8a8f8e",letterSpacing:".18em",fontWeight:900}}>SCROLL TO EXPLORE ↘</div><Noise opacity={.045}/>
 </AbsoluteFill>;
}


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
  const f = useCurrentFrame();
  const blink = f < 7 ? e(f, 0, 7, 0.15, 1) : f > 17 ? 1 - e(f, 17, 22, 0, .85) : 1;
  return (
    <AbsoluteFill style={{ ...full, background: "#080a12", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 50%,#1d2867 0%,#090c1b 60%)" }} />
      <svg viewBox="0 0 1400 650" width="1320" height="620" style={{ position: "absolute", left: "50%", top: "47%", transform: "translate(-50%,-50%)" }}>
        <defs>
          <radialGradient id="iris-gradient"><stop offset="0%" stopColor="#080a15" /><stop offset="21%" stopColor="#18276e" /><stop offset="51%" stopColor="#485ef8" /><stop offset="76%" stopColor="#202e89" /><stop offset="100%" stopColor="#080a15" /></radialGradient>
          <filter id="iris-glow"><feGaussianBlur stdDeviation="8" /></filter>
        </defs>
        <path d="M75 325 Q700 0 1325 325 Q700 650 75 325Z" fill="#151c46" stroke="#9eacff" strokeWidth="8" />
        <path d={"M90 325 Q700 " + (325 - 265 * blink) + " 1310 325 Q700 " + (325 + 265 * blink) + " 90 325Z"} fill="#f5f3ed" />
        <circle cx="700" cy="325" r="210" fill="url(#iris-gradient)" stroke="#8c9bff" strokeWidth="13" />
        {Array.from({ length: 64 }, (_, i) => <path key={i} d="M700 118 L700 250" stroke={i % 2 ? "#9cb1ff" : "#435be3"} strokeWidth={i % 4 ? 4 : 8} opacity=".78" transform={"rotate(" + (i * 5.625) + " 700 325)"} />)}
        <circle cx="700" cy="325" r="105" fill="#03050b" stroke="#7188ff" strokeWidth="8" />
        <circle cx="650" cy="265" r="34" fill="#fff" opacity=".88" filter="url(#iris-glow)" />
        <circle cx="650" cy="265" r="18" fill="#fff" />
      </svg>
      <div style={{ position: "absolute", left: 120, bottom: 75, fontSize: 32, fontWeight: 950, letterSpacing: "-.04em" }}>3.7%</div>
      <div style={{ position: "absolute", right: 125, bottom: 83, color: "#8793c9", fontSize: 16, fontWeight: 850, letterSpacing: ".18em" }}>A STUDY IN FOCUS</div>
    </AbsoluteFill>
  );
};

const Comic1952 = () => {
  const f = useCurrentFrame();
  const zig = e(f, 0, 22, -60, 0);
  return (
    <AbsoluteFill style={{ ...full, background: "#f6d948" }}>
      <div style={{ position: "absolute", inset: 80, border: "9px solid #121315", background: "#fff4db", display: "grid", gridTemplateColumns: "1fr 2.2fr 1fr", gridTemplateRows: "1fr 1fr", gap: 12, padding: 12, boxSizing: "border-box" }}>
        <div style={{ background: "#f7f2e7", border: "5px solid #131517", padding: 18 }}><Word size={33} color="#141619">ONE</Word><Word size={33} color="#141619">IDEA.</Word></div>
        <div style={{ gridRow: "span 2", position: "relative", overflow: "hidden", background: "repeating-conic-gradient(#fff 0deg 5deg,#78a3e8 5deg 10deg)" }}>
          <div style={{ position: "absolute", inset: 80, background: "#f2ce41", borderRadius: "50%", border: "8px solid #111" }} />
          <div style={{ position: "absolute", left: "20%", top: "17%", width: "60%", height: "66%", border: "14px solid #111", borderRadius: "50%", background: "#e64b37", display: "grid", placeItems: "center" }}><div style={{ width: "63%", height: "63%", borderRadius: "50%", background: "#fff", display: "grid", placeItems: "center" }}><PlayGlyph size={128} color="#101114" /></div></div>
          <svg viewBox="0 0 500 250" width="100%" height="100%" style={{ position: "absolute", left: 0, top: 0, transform: "translateX(" + zig + "px)" }}><path d="M0 0 L500 250 M0 60 L440 280" stroke="#141517" strokeWidth="13" /></svg>
          <div style={{ position: "absolute", bottom: 20, right: 18, padding: "9px 17px", background: "#f7d743", border: "5px solid #131517", fontSize: 24, fontWeight: 950, transform: "rotate(-8deg)" }}>CLICK!</div>
        </div>
        <div style={{ background: "#f7f2e7", border: "5px solid #131517", display: "grid", placeItems: "center", fontSize: 38, fontWeight: 950 }}>•••</div>
        <div style={{ background: "#f7f2e7", border: "5px solid #131517", display: "grid", placeItems: "center", fontSize: 18, fontWeight: 950 }}>SFX / 02</div>
        <div style={{ background: "#f7f2e7", border: "5px solid #131517", display: "grid", placeItems: "center", fontSize: 18, fontWeight: 950 }}>CUT / OUT</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 27, textAlign: "center", fontSize: 18, fontWeight: 950, letterSpacing: ".2em" }}>1952 / CUT-OUTS</div>
    </AbsoluteFill>
  );
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
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#e43c31", color: "#171719" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(#fff 0 6px,transparent 6px)", backgroundSize: "31px 31px", opacity: .82 }} />
      <div style={{ position: "absolute", inset: 72, background: "#ffda43", border: "10px solid #171719", borderRadius: 4, transform: "rotate(" + (Math.sin(f/8)*.8) + "deg)" }} />
      <div style={{ position: "absolute", left: "50%", top: "50%", width: 600, height: 600, marginLeft: -300, marginTop: -300, border: "26px solid #171719", borderRadius: "50%", background: "#ec4c37", display: "grid", placeItems: "center", boxShadow: "inset 0 0 0 20px #f8db44" }}>
        <div style={{ width: 365, height: 365, border: "13px solid #171719", borderRadius: "50%", background: "#fff", display: "grid", placeItems: "center" }}><PlayGlyph size={250} color="#111315" /></div>
      </div>
      <div style={{ position: "absolute", top: 58, left: 0, right: 0, textAlign: "center", background: "#fff", padding: "10px 0", fontSize: 27, fontWeight: 950, letterSpacing: ".13em" }}>1965 / INFINITY DOTS</div>
    </AbsoluteFill>
  );
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

const EasePoster = () => (
  <AbsoluteFill style={{ ...full, background: "#b9ee4c", color: "#101812" }}>
    <div style={{ position: "absolute", inset: 0, background: "linear-gradient(135deg,#c7f879,#95d832)" }} />
    <Word size={375} color="#111914" tracking={-.14} style={{ position: "absolute", left: 75, top: 330 }}>EASE<span style={{ color: "#fff" }}>.</span></Word>
    <div style={{ position: "absolute", left: 90, bottom: 86, fontSize: 19, fontWeight: 950, letterSpacing: ".2em" }}>MAKE IT FEEL RIGHT</div>
    <svg viewBox="0 0 700 300" width="620" height="265" style={{ position: "absolute", right: 70, bottom: 100 }}>
      <path d="M15 270 C105 270 120 35 680 20" stroke="#f8ffe9" strokeWidth="12" fill="none" strokeLinecap="round"/>
      <path d="M15 270 C105 270 120 35 680 20" stroke="#1d2c18" strokeWidth="3" fill="none" strokeDasharray="10 18"/>
    </svg>
  </AbsoluteFill>
);

const MotionFilmsPoster = () => {
  const f=useCurrentFrame();
  const planeX=Math.sin(f/7)*15;
  return (
    <AbsoluteFill style={{ ...full, background: "#263d8e", color: "#fff" }}>
      <div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#314f9d,#15245c)"}}/>
      <div style={{position:"absolute",left:230,top:160,width:1460,height:560,border:"12px dashed #f4f0df",borderRadius:5,transform:"rotate(-1deg)",boxShadow:"0 0 0 6px rgba(255,255,255,.08)"}}/>
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
        <path d="M330 690 Q500 600 710 680 T1100 670 T1600 655" fill="none" stroke="#fff5df" strokeWidth="8" strokeLinecap="round" opacity=".9"/>
        <path d={"M500 400 L"+(690+planeX)+" 265 L615 427 L575 387Z"} fill="#f9f7eb" stroke="#fff" strokeWidth="5"/>
        <path d="M570 385 L690 265 L655 438 L615 427Z" fill="#d4e0f1"/>
        <path d="M1050 345 Q1120 290 1200 345 Q1230 402 1170 435 Q1100 452 1050 345Z" fill="#111a31" stroke="#fff" strokeWidth="7"/>
        <circle cx="1114" cy="354" r="16" fill="#fff"/><circle cx="1176" cy="354" r="16" fill="#fff"/>
        <path d="M1110 404 Q1145 430 1180 400" fill="none" stroke="#f0a088" strokeWidth="9" strokeLinecap="round"/>
        <path d="M1260 545 Q1350 495 1420 548" fill="none" stroke="#f4f0df" strokeWidth="7" strokeDasharray="15 18"/>
      </svg>
      <div style={{position:"absolute",left:250,top:735,color:"#f9f7eb",fontSize:80,fontFamily:displayFont,fontWeight:650,letterSpacing:"-.04em"}}>motion films</div>
      <div style={{position:"absolute",right:240,top:95,fontSize:17,fontWeight:900,letterSpacing:".2em",color:"#d7e0f1"}}>SKETCH / FRAME / MOTION</div>
    </AbsoluteFill>
  );
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
 const f=useCurrentFrame(),k=e(f,0,7);
 return <AbsoluteFill style={{...full,background:"#8ec4db"}}><CloudSky frame={f+140}/><div style={{position:"absolute",left:510,top:115,width:900,height:810,borderRadius:22,background:"rgba(255,255,255,.95)",padding:58,boxSizing:"border-box",boxShadow:"0 25px 70px rgba(30,70,90,.2)"}}><div style={{display:"flex",justifyContent:"space-between",fontSize:19,fontWeight:850,color:"#77858c"}}><span>GROWTH / REPORT</span><span>DAY 104</span></div><div style={{marginTop:48,fontSize:155,fontWeight:950,fontFamily:displayFont,color:"#10171d",letterSpacing:"-.1em"}}>84K</div><div style={{fontSize:23,fontWeight:750,color:"#77818a"}}>CREATORS / REACHED</div><svg viewBox="0 0 760 320" width="100%" height="320" style={{marginTop:30}}><path d="M25 280H735M25 210H735M25 140H735M25 70H735" stroke="#e4eaeb" strokeWidth="2"/><path d="M25 275 C140 260 170 235 245 218 S380 170 450 126 S590 85 735 30L735 280H25Z" fill="#8fdcad" opacity=".35"/><path d={"M25 275 C140 260 170 235 245 218 S380 170 450 126 S590 85 "+(735*k+600*(1-k))+" "+(30+245*k+55*(1-k))} stroke="#39a77c" strokeWidth="8" fill="none" strokeLinecap="round"/></svg></div></AbsoluteFill>;
};
const KoalaPoster=()=><AbsoluteFill style={{...full,background:"linear-gradient(120deg,#2a8bd1,#144a9a)",color:"#fff"}}><div style={{position:"absolute",left:330,top:190,width:430,height:540,borderRadius:220,background:"#f5ead0",transform:"rotate(-5deg)"}}><svg viewBox="0 0 430 540" width="100%" height="100%"><ellipse cx="82" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="348" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="215" cy="255" rx="155" ry="170" fill="#9099a1"/><ellipse cx="215" cy="298" rx="120" ry="100" fill="#f2efe6"/><circle cx="160" cy="246" r="16" fill="#151a1d"/><circle cx="270" cy="246" r="16" fill="#151a1d"/><ellipse cx="215" cy="300" rx="42" ry="57" fill="#20262c"/><path d="M180 365Q215 392 250 365" stroke="#252a2c" strokeWidth="10" fill="none"/></svg></div><div style={{position:"absolute",right:270,top:195,width:450,height:650,background:"#fff",color:"#182431",borderRadius:20,padding:38,boxSizing:"border-box",boxShadow:"0 24px 55px rgba(0,0,0,.22)"}}><div style={{fontSize:21,fontWeight:950,letterSpacing:".1em"}}>COURSES / 2026</div><div style={{marginTop:34,height:250,borderRadius:14,background:"linear-gradient(135deg,#f2dfba,#e4a27b,#83b9cb)"}}/><div style={{marginTop:34,fontSize:48,fontWeight:950,lineHeight:.95}}>Learn to create.</div><div style={{marginTop:25,fontSize:18,color:"#7e8991"}}>A new way to make ideas move.</div></div></AbsoluteFill>;
const GreenTransition=()=>{const f=useCurrentFrame(),r=e(f,0,7,90,650);return <AbsoluteFill style={{...full,background:"#b7ee5b"}}><svg viewBox="0 0 1920 1080" width="100%" height="100%"><circle cx="960" cy="540" r={r} fill="none" stroke="#efffd4" strokeWidth="3"/><circle cx="960" cy="540" r={r*.7} fill="none" stroke="#efffd4" strokeWidth="2"/></svg><Word size={420} color="#142016" style={{position:"absolute",left:0,right:0,top:300,textAlign:"center"}}>OUT.</Word></AbsoluteFill>;};



const PosterSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={13}><ClockComic /></Sequence>
    <Sequence from={13} durationInFrames={13}><DotPoster /></Sequence>
    <Sequence from={26} durationInFrames={8}><LightSweep1973 /></Sequence>
    <Sequence from={34} durationInFrames={22}><MarioGamePoster /></Sequence>
    <Sequence from={56} durationInFrames={13}><WorldPoster /></Sequence>
    <Sequence from={69} durationInFrames={13}><MindPoster /></Sequence>
    <Sequence from={82} durationInFrames={30}><RingPoster /></Sequence>
    <Sequence from={112} durationInFrames={13}><PosterGrid /></Sequence>
    <Sequence from={125} durationInFrames={8}><PointCloudPoster /></Sequence>
    <Sequence from={133} durationInFrames={13}><EasePoster /></Sequence>
    <Sequence from={146} durationInFrames={7}><InPoster /></Sequence>
    <Sequence from={153} durationInFrames={7}><EasePoster /></Sequence>
    <Sequence from={160} durationInFrames={13}><OutPoster /></Sequence>
    <Sequence from={173} durationInFrames={13}><NeverPoster /></Sequence>
    <Sequence from={186} durationInFrames={13}><LinearPoster /></Sequence>
    <Sequence from={199} durationInFrames={7}><GreenTransition /></Sequence>
    <Sequence from={206} durationInFrames={13}><ClockPoster /></Sequence>
    <Sequence from={219} durationInFrames={7}><StatsPoster /></Sequence>
    <Sequence from={226} durationInFrames={7}><TogglePoster /></Sequence>
    <Sequence from={233} durationInFrames={8}><MotionFilmsPoster /></Sequence>
    <Sequence from={241} durationInFrames={15}><EyePoster /></Sequence>
    <Sequence from={256} durationInFrames={8}><KoalaPoster /></Sequence>
    <Sequence from={264} durationInFrames={8}><Comic1952 /></Sequence>
    <Sequence from={272} durationInFrames={7}><Future3D /></Sequence>
  </AbsoluteFill>
);


const NotJustOpus = () => {
  const f = useCurrentFrame();
  const p = pop(f, 30, 2, 120, 15);
  const x = e(f, 0, 28, 90, 0);
  return (
    <AbsoluteFill style={{ ...full, background: "#08090b", color: "#fff" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 390, display: "flex", alignItems: "center", justifyContent: "center", gap: 18, transform: "translateX(" + x + "px) scale(" + (0.94 + p * .06) + ")" }}>
        <Word size={91} color="#f6f6f2" tracking={-0.07}>Not just</Word>
        <div style={{ background: "#e98e78", color: "#141516", padding: "12px 26px 16px", borderRadius: 15, transform: "rotate(-1deg)", boxShadow: "0 10px 0 rgba(0,0,0,.15)" }}>
          <Word size={88} color="#141516" tracking={-0.07}>Opus 5.5.</Word>
        </div>
      </div>
      <div style={{ position: "absolute", left: 100, bottom: 80, fontSize: 16, color: "#7d8182", letterSpacing: ".18em", fontWeight: 850 }}>CHOICE / CONTROL / CREATION</div>
    </AbsoluteFill>
  );
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


const ModelAgentScene=()=>{
 const f=useCurrentFrame();
 const Phrase=({agent}:{agent:boolean})=><div style={{position:"absolute",left:0,right:0,top:330,display:"flex",justifyContent:"center",alignItems:"baseline",color:"#111315",fontFamily:displayFont,fontSize:158,fontWeight:900,letterSpacing:"-.09em",whiteSpace:"nowrap"}}><span>{agent?"Any":"Any m"}</span><span>{agent?" agent.":"odel."}</span></div>;
 const Logos=({seed=0}:{seed?:number})=><div style={{position:"absolute",left:0,right:0,top:535,display:"flex",justifyContent:"center",gap:17}}>{Array.from({length:7},(_,i)=><div key={i} style={{width:58,height:58,borderRadius:18,background:["#263b75","#e66b52","#303239","#5275bf","#d39d53","#4c8b74","#363d86"][(i+seed)%7],border:"2px solid #fff",display:"grid",placeItems:"center",fontSize:25,fontWeight:950,color:"#fff",transform:"translateY("+(Math.sin(f/7+i)*4)+"px)"}}>{["✦","◈","M","∞","A","⌘","N"][(i+seed)%7]}</div>)}</div>;
 const Sub=({children,color}:{children:string;color:string})=><div style={{position:"absolute",left:0,right:0,top:650,textAlign:"center",fontSize:18,fontWeight:850,letterSpacing:".18em",color}}>{children}</div>;
 return <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={39}><AbsoluteFill style={{background:"#9ed2e4"}}><Phrase agent={false}/><Logos seed={0}/><Sub color="#446879">ONE CANVAS / ANY MODEL</Sub></AbsoluteFill></Sequence>
  <Sequence from={39} durationInFrames={39}><AbsoluteFill style={{background:"#dfa77f"}}><Phrase agent={false}/><Logos seed={1}/><Sub color="#754d37">CHOOSE THE ENGINE THAT FITS</Sub></AbsoluteFill></Sequence>
  <Sequence from={78} durationInFrames={30}><AbsoluteFill style={{background:"#b7d6c7"}}><Phrase agent={true}/><Logos seed={2}/><Sub color="#456b58">ANY AGENT / YOUR TOOLS</Sub></AbsoluteFill></Sequence>
  <Sequence from={108} durationInFrames={30}><AbsoluteFill style={{background:"#d1dfe0"}}><Phrase agent={true}/><Logos seed={3}/><Sub color="#647679">THE MODEL IS YOURS / THE TOOLS ARE YOURS</Sub></AbsoluteFill></Sequence>
 </AbsoluteFill>;
};


const PreviewArtwork=({variant,frame}:{variant:number;frame:number})=>{
 if(variant===0)return <div style={{position:"absolute",inset:0,background:"#dfd2b3"}}><svg viewBox="0 0 1000 650" width="100%" height="100%"><path d="M0 400Q180 330 350 390T700 360T1000 382V650H0Z" fill="#a28e6d"/><path d="M0 460Q210 390 400 440T760 410T1000 430V650H0Z" fill="#d0b98c"/><g transform={"translate(500 325) rotate("+frame*.85+")"}><circle r="145" fill="#d8b65d" stroke="#6b5939" strokeWidth="22"/><circle r="112" fill="#e8d7ab" stroke="#62523d" strokeWidth="9"/><path d="M0 -75L14 22L0 83L-14 22Z" fill="#232a2b"/></g></svg><div style={{position:"absolute",left:25,top:22,fontSize:15,fontWeight:950,letterSpacing:".15em",color:"#272e33"}}>1889 / THE MECHANICAL AGE</div></div>;
 if(variant===1)return <div style={{position:"absolute",inset:0,background:"#e84736"}}><div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#fff 0 5px,transparent 5px)",backgroundSize:"25px 25px",opacity:.75}}/><div style={{position:"absolute",inset:"9% 14%",background:"#ffdb40",border:"7px solid #17191b"}}/><div style={{position:"absolute",left:"50%",top:"50%",width:360,height:360,marginLeft:-180,marginTop:-180,borderRadius:"50%",background:"#e64a37",border:"18px solid #17191b",boxShadow:"inset 0 0 0 16px #f9d64d",display:"grid",placeItems:"center"}}><div style={{width:235,height:235,borderRadius:"50%",background:"#fff8e9",border:"9px solid #17191b",display:"grid",placeItems:"center"}}><OpenDesignSymbol size={145}/></div></div><div style={{position:"absolute",top:22,left:25,fontSize:15,fontWeight:950,color:"#17191b"}}>1965 / INFINITY DOTS</div></div>;
 if(variant===2)return <div style={{position:"absolute",inset:0,background:"#172ee5"}}><div style={{position:"absolute",inset:0,backgroundImage:"linear-gradient(rgba(255,255,255,.11) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.11) 1px,transparent 1px)",backgroundSize:"34px 34px"}}/><div style={{position:"absolute",inset:0,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}><Word size={180} color="#f6f7ff" tracking={-.14} style={{textShadow:"1px 1px 0 #d9def6,4px 4px 0 #a5b2e8,8px 8px 0 #788ee0,14px 16px 0 #334fb8,25px 32px 22px rgba(0,0,0,.35)"}}>FUTURE</Word><Word size={65} color="#fff">IS ALREADY HERE</Word></div></div>;
 if(variant===3)return <div style={{position:"absolute",inset:0,background:"#95ef4a"}}><div style={{position:"absolute",left:42,top:38,fontSize:17,fontWeight:950}}>OPEN DESIGN / CREATIVE STUDIO</div><Word size={160} color="#101713" style={{position:"absolute",left:30,top:175}}>OPEN</Word><Word size={160} color="#101713" style={{position:"absolute",left:30,top:320}}>DESIGN</Word><div style={{position:"absolute",right:45,bottom:42}}><OpenDesignSymbol size={104}/></div></div>;
 if(variant===4)return <div style={{position:"absolute",inset:0,background:"#2c79c3",color:"#fff"}}><div style={{position:"absolute",left:65,top:110,width:330,height:390,borderRadius:"48% 48% 42% 42%",background:"#f7e9d0"}}><div style={{position:"absolute",top:46,left:55,width:220,height:255,borderRadius:"48%",background:"#9098a2"}}/></div><div style={{position:"absolute",right:36,top:120,width:290,height:375,background:"#fff",color:"#1b2a37",borderRadius:18,padding:25,boxSizing:"border-box"}}><b>Courses</b><div style={{marginTop:28,height:145,borderRadius:12,background:"linear-gradient(135deg,#eee0c0,#e5a47d,#83b9cb)"}}/><div style={{marginTop:24,fontSize:33,fontWeight:950}}>Learn to create.</div></div></div>;
 if(variant===5)return <div style={{position:"absolute",inset:0,background:"#f5f4ed"}}><svg viewBox="0 0 1000 650" width="100%" height="100%">{Array.from({length:13},(_,i)=><path key={i} d={"M"+(-160+i*86)+" -40 C"+(150+i*43)+" 125 "+(-40+i*93)+" 390 "+(190+i*60)+" 700"} stroke="#111315" strokeWidth="38" fill="none" strokeLinecap="round"/>)}</svg><div style={{position:"absolute",top:27,left:30,color:"#16191a",fontSize:15,fontWeight:950}}>FORM / FLOW / SYSTEM</div></div>;
 return <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#1a2c7d,#111638 60%,#060915)"}}><div style={{position:"absolute",inset:0,backgroundImage:"linear-gradient(rgba(78,143,255,.4) 2px,transparent 2px),linear-gradient(90deg,rgba(78,143,255,.4) 2px,transparent 2px)",backgroundSize:"56px 38px",transform:"perspective(460px) rotateX(58deg)",transformOrigin:"bottom"}}/><Word size={260} color="#fff" style={{position:"absolute",left:42,top:100}}>3</Word><div style={{position:"absolute",right:48,top:50,color:"#d8e9ff",fontSize:16,fontWeight:900}}>READY / MOTION</div></div>;
};


const CountdownArtwork = ({ value, frame }: { value: number; frame: number }) => {
  const p = pop(frame, 30, 0, 75, 14);
  const scale = .82 + p * .18;
  return (
    <AbsoluteFill style={{ background: "linear-gradient(115deg,#10131b 0%,#141b38 52%,#2a41c1 100%)", color: "#f4f6ff" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "radial-gradient(ellipse at 50% 50%,rgba(71,104,255,.4),transparent 50%),linear-gradient(90deg,transparent 49%,rgba(255,255,255,.08) 50%,transparent 51%)", backgroundSize: "100% 100%,50px 50px" }} />
      <div style={{ position: "absolute", top: 28, left: 40, fontSize: 16, fontWeight: 900, letterSpacing: ".18em", color: "#dce1ff" }}>OPEN DESIGN / LAUNCH COUNTDOWN</div>
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
 return <AbsoluteFill style={{...full,background:"#f3f2ee"}}><div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 52% 45%,#fff,#f2f1ec 68%)"}}/>
  <div style={{position:"absolute",left:118,right:118,top:72,bottom:72,borderRadius:22,background:"#fff",border:"1px solid #e9e8e3",boxShadow:"0 34px 90px rgba(30,35,38,.17)",transform:"translateY("+((1-p)*80)+"px) scale("+(0.98+.02*p)+")",overflow:"hidden"}}>
   <div style={{position:"absolute",top:0,left:0,right:0,height:68,borderBottom:"1px solid #efeee9",display:"flex",alignItems:"center",padding:"0 28px",gap:14}}>{["#e5e5df","#e5e5df","#e5e5df"].map((c,i)=><div key={i} style={{width:15,height:15,borderRadius:"50%",background:c}}/>)}<div style={{marginLeft:14,fontSize:20,fontWeight:850,color:"#252a2d"}}>Launch film</div></div>
   <div style={{position:"absolute",top:68,bottom:0,left:0,width:520,borderRight:"1px solid #efeee9",padding:"42px 38px",boxSizing:"border-box",background:"#fff"}}>
    <div style={{maxWidth:370,background:"#f1f1ee",color:"#2c3032",borderRadius:"22px 22px 4px 22px",padding:"22px 24px",fontSize:24,lineHeight:1.38}}>Make a 10s launch film for our app.</div>
    <div style={{position:"absolute",left:38,right:36,bottom:36,height:152,border:"1px solid #e7e7e2",borderRadius:24,background:"#fff",padding:"20px 22px",boxSizing:"border-box"}}>
     <div style={{color:"#434a4c",fontSize:20}}>Make it feel like a launch.</div>
     <div style={{position:"absolute",left:22,bottom:18,display:"flex",alignItems:"center",gap:12}}><div style={{width:28,height:28,borderRadius:9,background:"#df805b",color:"#fff",display:"grid",placeItems:"center"}}>✦</div><div style={{fontSize:18,color:"#232a2b",fontWeight:850}}>Claude Opus 5.5</div><div style={{marginLeft:9,background:"#ecf7e8",color:"#277b32",borderRadius:7,padding:"6px 12px",fontSize:15,fontWeight:900}}>▣ Motion</div></div>
     <div style={{position:"absolute",right:15,bottom:14,width:52,height:52,borderRadius:"50%",background:"#101416",display:"grid",placeItems:"center"}}><svg viewBox="0 0 30 30" width="24" height="24"><path d="M5 15H24M16 6L25 15L16 24" stroke="#a5ed65" strokeWidth="2.5" fill="none"/></svg></div>
    </div>
   </div>
   <div style={{position:"absolute",left:520,right:0,top:68,bottom:0,background:"#f8f8f6",padding:34,boxSizing:"border-box"}}><div style={{fontSize:22,color:"#777f81",fontWeight:850}}>Preview</div><div style={{position:"absolute",left:30,right:30,top:92,bottom:30,background:"#fff",borderRadius:18,border:"1px solid #e9e8e2",overflow:"hidden"}}>{countdown>=0?<CountdownArtwork value={countdown} frame={frame}/>:<PreviewArtwork variant={variant} frame={frame}/>}<div style={{position:"absolute",left:22,top:20,display:"flex",alignItems:"center",gap:11,background:"rgba(255,255,255,.96)",borderRadius:30,padding:"10px 18px",color:"#30383b",fontSize:18,fontWeight:800}}><span style={{color:"#8a94a2",fontWeight:650}}>Made with</span><span style={{width:28,height:28,borderRadius:"50%",background:"#edf0ff",color:"#5964aa",display:"grid",placeItems:"center"}}>◈</span>GPT-6-Astra</div></div></div>
  </div>
 </AbsoluteFill>;
};


const LaunchVariant = ({ variant, countdown = -1 }: { variant: number; countdown?: number }) => {
  const frame = useCurrentFrame();
  return <LaunchKitWindow frame={frame} variant={variant} countdown={countdown} />;
};


const LaunchKitSequence=()=>(
 <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={23}><LaunchVariant variant={0}/></Sequence>
  <Sequence from={23} durationInFrames={8}><LaunchVariant variant={1}/></Sequence>
  <Sequence from={31} durationInFrames={8}><LaunchVariant variant={2}/></Sequence>
  <Sequence from={39} durationInFrames={8}><LaunchVariant variant={3}/></Sequence>
  <Sequence from={47} durationInFrames={8}><LaunchVariant variant={4}/></Sequence>
  <Sequence from={55} durationInFrames={8}><LaunchVariant variant={5}/></Sequence>
  <Sequence from={63} durationInFrames={8}><LaunchVariant variant={6}/></Sequence>
  <Sequence from={71} durationInFrames={15}><LaunchVariant variant={2} countdown={3}/></Sequence>
  <Sequence from={86} durationInFrames={15}><LaunchVariant variant={2} countdown={2}/></Sequence>
  <Sequence from={101} durationInFrames={15}><LaunchVariant variant={2} countdown={1}/></Sequence>
 </AbsoluteFill>
);


const CountdownSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={20}><LaunchVariant variant={0} countdown={3} /></Sequence>
    <Sequence from={20} durationInFrames={20}><LaunchVariant variant={1} countdown={2} /></Sequence>
    <Sequence from={40} durationInFrames={20}><LaunchVariant variant={2} countdown={1} /></Sequence>
  </AbsoluteFill>
);


const CubeFace=({kind,transform,frame}:{kind:number;transform:string;frame:number})=>{
 const style:React.CSSProperties={position:"absolute",inset:0,width:"100%",height:"100%",overflow:"hidden",borderRadius:31,border:"2px solid rgba(255,255,255,.7)",boxSizing:"border-box",backfaceVisibility:"hidden",transform,boxShadow:"inset 0 0 0 2px rgba(255,255,255,.16),inset 0 -18px 32px rgba(0,0,0,.16)"};
 const badge=<div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:116,height:116,borderRadius:32,background:"#111315",border:"3px solid #fff",display:"grid",placeItems:"center",boxShadow:"0 12px 28px rgba(0,0,0,.28)"}}><OpenDesignSymbol size={96}/></div>;
 return <div style={style}>
  {kind===0?<div style={{position:"absolute",inset:0,background:"#101416",display:"grid",placeItems:"center"}}><OpenDesignSymbol size={205}/></div>:
  kind===1?<div style={{position:"absolute",inset:0,background:"linear-gradient(135deg,#142fb5,#09104f)"}}><Word size={58} color="#fff" style={{position:"absolute",left:22,top:38}}>FUTURE</Word><Word size={39} color="#b9ed4a" style={{position:"absolute",left:24,top:103}}>IS HERE</Word>{badge}</div>:
  kind===2?<div style={{position:"absolute",inset:0,background:"#f2d44f"}}><svg viewBox="0 0 360 360" width="100%" height="100%"><circle cx="180" cy="180" r="136" fill="#e8a942" stroke="#22272c" strokeWidth="14"/><circle cx="180" cy="180" r="107" fill="#f7edd1" stroke="#5a503f" strokeWidth="8"/><path d={"M180 180L"+(180+Math.cos(frame*.06)*82)+" "+(180+Math.sin(frame*.06)*82)} stroke="#1e252b" strokeWidth="14"/></svg>{badge}</div>:
  kind===3?<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#a3ec70,#68a94f)"}}><Word size={61} color="#142019" style={{position:"absolute",left:18,top:27}}>OPEN</Word><Word size={61} color="#142019" style={{position:"absolute",left:18,top:90}}>DESIGN</Word>{badge}</div>:
  kind===4?<div style={{position:"absolute",inset:0,background:"#e7a17e"}}><div style={{position:"absolute",left:37,top:28,width:178,height:250,borderRadius:"50%",background:"#f8eed9"}}/><div style={{position:"absolute",left:76,top:80,width:100,height:142,borderRadius:"48%",background:"#8e969e"}}/>{badge}</div>:
  <div style={{position:"absolute",inset:0,background:"#a9ed5d"}}><Word size={81} color="#172019" style={{position:"absolute",left:18,top:45}}>EASE</Word><div style={{position:"absolute",left:24,right:24,bottom:34,height:5,background:"#172019"}}/>{badge}</div>}
  <div style={{position:"absolute",inset:0,borderRadius:29,pointerEvents:"none",background:"linear-gradient(135deg,rgba(255,255,255,.44),transparent 32%,rgba(0,0,0,.18) 100%)"}}/>
 </div>;
};
const ProjectCube=()=>{
 const f=useCurrentFrame(),rotateY=-34-360*e(f,0,116)-e(f,116,126),rotateX=23*(1-e(f,105,126)),rotateZ=-5+Math.sin(f/18)*3;
 const scale=(.68+.32*e(f,0,18))*(1-.35*e(f,108,126)),size=360,z=size/2;
 return <AbsoluteFill style={{...full,background:"linear-gradient(145deg,#f8f7f2,#e9e9e3 58%,#d8dedf)"}}>
  <div style={{position:"absolute",left:"50%",top:"82%",width:520,height:84,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"rgba(24,30,38,.17)",filter:"blur(28px)"}}/>
  <div style={{position:"absolute",left:"50%",top:"48%",width:size,height:size,perspective:1100,transform:"translate(-50%,-50%)"}}><div style={{position:"absolute",inset:0,transformStyle:"preserve-3d",transform:"rotateX("+rotateX+"deg) rotateY("+rotateY+"deg) rotateZ("+rotateZ+"deg) scale("+scale+")",filter:"drop-shadow(0 34px 36px rgba(20,27,35,.3))"}}>
   <CubeFace kind={0} frame={f} transform={"translateZ("+z+"px)"}/><CubeFace kind={1} frame={f} transform={"rotateY(90deg) translateZ("+z+"px)"}/><CubeFace kind={2} frame={f} transform={"rotateY(-90deg) translateZ("+z+"px)"}/><CubeFace kind={3} frame={f} transform={"rotateX(90deg) translateZ("+z+"px)"}/><CubeFace kind={4} frame={f} transform={"rotateX(-90deg) translateZ("+z+"px)"}/><CubeFace kind={5} frame={f} transform={"rotateY(180deg) translateZ("+z+"px)"}/>
  </div></div>
 </AbsoluteFill>;
};
const MorroCubeIntro=()=>{const f=useCurrentFrame(),p=pop(f,30,3,90,18),scale=.45+.85*e(f,4,36);return <AbsoluteFill style={full}><MorroPoster/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) scale("+scale+")",opacity:e(f,3,13),filter:"drop-shadow(0 25px 35px rgba(0,0,0,.24))"}}><div style={{width:215,height:215,borderRadius:54,background:"#111315",display:"grid",placeItems:"center",border:"5px solid #fff"}}><OpenDesignSymbol size={180}/></div></div><div style={{position:"absolute",left:0,right:0,bottom:50,textAlign:"center",fontSize:14,fontWeight:900,letterSpacing:".2em",color:"#75777a",opacity:1-p}}>MORRO / PROJECT MARK</div></AbsoluteFill>;};
const TexturedCube=()=> <ProjectCube />;

const FinalLockup=()=>{
 const {fps}=useVideoConfig(),p=pop(useCurrentFrame(),fps,0,78,18),fade=e(useCurrentFrame(),0,10);
 return <AbsoluteFill style={{...full,background:"#faf9f5"}}><div style={{position:"absolute",left:0,right:0,top:245,display:"flex",flexDirection:"column",alignItems:"center",transform:"translateY("+((1-p)*32)+"px)",opacity:fade}}>
  <div style={{width:150,height:150,borderRadius:39,background:"#101416",display:"grid",placeItems:"center",boxShadow:"0 18px 38px rgba(25,35,40,.2)"}}><OpenDesignSymbol size={128}/></div>
  <div style={{marginTop:31,fontFamily:displayFont,fontSize:70,fontWeight:950,color:"#14191b",letterSpacing:"-.075em"}}>OpenDesign Motion</div>
  <div style={{marginTop:22,background:"#10313a",color:"#e7f3f2",borderRadius:24,padding:"9px 27px",fontSize:15,fontWeight:850}}>open-design.ai</div>
 </div></AbsoluteFill>;
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