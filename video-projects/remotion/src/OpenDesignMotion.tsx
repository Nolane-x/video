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
      <div style={{ position: "absolute", top: 153, left: 0, right: 0, textAlign: "center", color: "rgba(35,52,58,.6)", fontSize: 14, letterSpacing: ".09em", fontWeight: 600 }}>
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

const GalleryCard = ({ index, frame }: { index: number; frame: number }) => {
  const drift = Math.sin((frame + index * 13) / 18) * 9;
  const rotation = (index % 2 ? -1 : 1) * (1.4 + Math.sin(frame / 19 + index) * 0.8);
  return (
    <div style={{
      width: 370,
      height: 206,
      borderRadius: 10,
      position: "relative",
      overflow: "hidden",
      transform: "translateY(" + drift + "px) rotate(" + rotation + "deg)",
      boxShadow: "0 24px 48px rgba(19,24,32,.20),0 2px 8px rgba(19,24,32,.12)",
      background: "#fff",
    }}>
      <GalleryPoster index={index} frame={frame} />
      <div style={{ position: "absolute", left: 14, bottom: 9, fontSize: 8, fontWeight: 900, letterSpacing: ".2em", color: "rgba(20,25,30,.58)" }}>OD / 0{index + 1}</div>
    </div>
  );
};

const GalleryWall = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = pop(f, fps, 0, 68, 18);
  const pan = e(f, 0, 90, 85, -100);
  const rotation = e(f, 0, 90, 12, -7);
  return (
    <AbsoluteFill style={{ ...full, background: "#f2f0eb" }}>
      <div style={{ position: "absolute", left: 82, top: 58, fontSize: 17, fontWeight: 900, letterSpacing: ".21em", color: "#393d40" }}>OPEN DESIGN / MOTION COLLECTION</div>
      <div style={{ position: "absolute", right: 86, top: 58, fontSize: 15, fontWeight: 800, letterSpacing: ".2em", color: "#8a8c8a" }}>SELECTED WORKS / 2026</div>
      <div style={{
        position: "absolute",
        left: 95,
        top: 130,
        width: 1730,
        display: "grid",
        gridTemplateColumns: "repeat(4, 1fr)",
        gap: 28,
        transform: "perspective(1700px) rotateY(" + rotation + "deg) rotateX(4deg) translateX(" + pan + "px) translateY(" + ((1 - p) * 150) + "px) scale(" + (0.84 + p * 0.2) + ")",
        transformOrigin: "center center",
      }}>
        {Array.from({ length: 12 }, (_, i) => <GalleryCard key={i} index={i} frame={f} />)}
      </div>
      <div style={{ position: "absolute", bottom: 58, right: 88, fontSize: 15, color: "#8a8c8a", letterSpacing: ".2em", fontWeight: 850 }}>SCROLL TO EXPLORE ↘</div>
      <Noise opacity={0.04} />
    </AbsoluteFill>
  );
};

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
const PosterSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={17}><Comic1965 /></Sequence>
    <Sequence from={17} durationInFrames={17}><DotPoster /></Sequence>
    <Sequence from={34} durationInFrames={17}><GlitchPoster /></Sequence>
    <Sequence from={51} durationInFrames={17}><WorldPoster /></Sequence>
    <Sequence from={68} durationInFrames={17}><MindPoster /></Sequence>
    <Sequence from={85} durationInFrames={17}><RingPoster /></Sequence>
    <Sequence from={102} durationInFrames={17}><MorroPoster /></Sequence>
    <Sequence from={119} durationInFrames={17}><OutPoster /></Sequence>
    <Sequence from={136} durationInFrames={17}><EasePoster /></Sequence>
    <Sequence from={153} durationInFrames={17}><NeverPoster /></Sequence>
    <Sequence from={170} durationInFrames={17}><LinearPoster /></Sequence>
    <Sequence from={187} durationInFrames={17}><ClockPoster /></Sequence>
    <Sequence from={204} durationInFrames={17}><MotionFilmsPoster /></Sequence>
    <Sequence from={221} durationInFrames={17}><TogglePoster /></Sequence>
    <Sequence from={238} durationInFrames={17}><EyePoster /></Sequence>
    <Sequence from={255} durationInFrames={8}><Comic1952 /></Sequence>
    <Sequence from={263} durationInFrames={7}><Future3D /></Sequence>
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

const ModelAgentScene = () => {
  const InlinePhrase = ({ agent }: { agent:boolean }) => {
    const prefix=agent?"Any ":"Any m";
    const centerLetter=agent?"a":"o";
    const suffix=agent?"gent.":"del.";
    return (
      <div style={{ position: "absolute", left: 0, right: 0, top: 330, display: "flex", justifyContent: "center", alignItems: "baseline", color: "#111315", fontFamily: displayFont, fontSize: 158, fontWeight: 900, letterSpacing: "-.09em", whiteSpace: "nowrap" }}>
        <span>{prefix}</span><span style={{ position:"relative", display:"inline-block" }}>{centerLetter}
          <div style={{position:"absolute",left:"49%",top:-22,transform:"translateX(-50%)",display:"flex",alignItems:"center"}}>
            {Array.from({length:5},(_,i)=><div key={i} style={{width:47,height:47,marginLeft:i?-13:0,borderRadius:"50%",border:"3px solid #fff",background:["#fff","#e8f0ff","#fff","#f6f2e9","#fff"][i],boxShadow:"0 5px 15px rgba(0,0,0,.13)",display:"grid",placeItems:"center",fontSize:21,fontWeight:950,color:["#263b75","#e66b52","#303239","#5375bf","#d39d53"][i]}}>{["✦","◈","M","∞","A"][i]}</div>)}
          </div>
        </span><span>{suffix}</span>
      </div>
    );
  };
  return (
    <AbsoluteFill style={full}>
      <Sequence from={0} durationInFrames={34}>
        <AbsoluteFill style={{background:"#9ed2e4"}}><InlinePhrase agent={false}/><div style={{position:"absolute",left:0,right:0,top:535,textAlign:"center",fontSize:18,fontWeight:850,letterSpacing:".18em",color:"#446879"}}>ONE CANVAS / ANY MODEL</div></AbsoluteFill>
      </Sequence>
      <Sequence from={34} durationInFrames={34}>
        <AbsoluteFill style={{background:"#dfa77f"}}><InlinePhrase agent={false}/><div style={{position:"absolute",left:0,right:0,top:535,textAlign:"center",fontSize:18,fontWeight:850,letterSpacing:".18em",color:"#754d37"}}>CHOOSE THE ENGINE THAT FITS</div></AbsoluteFill>
      </Sequence>
      <Sequence from={68} durationInFrames={34}>
        <AbsoluteFill style={{background:"#b7d6c7"}}><InlinePhrase agent={true}/><div style={{position:"absolute",left:0,right:0,top:535,textAlign:"center",fontSize:18,fontWeight:850,letterSpacing:".18em",color:"#456b58"}}>ANY AGENT / YOUR TOOLS</div></AbsoluteFill>
      </Sequence>
      <Sequence from={102} durationInFrames={33}>
        <AbsoluteFill style={{background:"#d1dfe0"}}>
          <div style={{position:"absolute",left:0,right:0,top:350,textAlign:"center",fontFamily:displayFont,fontSize:157,fontWeight:950,letterSpacing:"-.09em",color:"#111315"}}>Any agent.</div>
          <div style={{position:"absolute",left:0,right:0,top:535,textAlign:"center",fontSize:18,fontWeight:850,letterSpacing:".18em",color:"#647679"}}>THE MODEL IS YOURS / THE TOOLS ARE YOURS</div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
const PreviewArtwork = ({ variant, frame }: { variant: number; frame: number }) => {
  if (variant === 0) return (
    <div style={{position:"absolute",inset:0,background:"#d5c39d",overflow:"hidden"}}>
      <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#b9b29a 0%,#d8c7a2 60%,#9e8965 100%)"}}/>
      <svg viewBox="0 0 1000 650" width="100%" height="100%" style={{position:"absolute",inset:0}}>
        <path d="M0 390 Q130 325 260 370 T510 360 T760 365 T1000 340 L1000 650 L0 650Z" fill="#786b57"/>
        <path d="M0 440 Q180 345 340 432 T650 410 T1000 415 L1000 650 L0 650Z" fill="#b19a76"/>
        <path d="M0 525 Q260 460 420 515 T780 490 T1000 508 L1000 650 L0 650Z" fill="#e0cda5"/>
        {Array.from({length:26},(_,i)=><path key={i} d={"M"+(i*42-40)+" "+(160+(i*53)%360)+" q 45 -26 80 8"} stroke={i%2?"#5a5548":"#f0e4c7"} strokeWidth="5" fill="none" opacity=".35"/>)}
        <g transform={"translate(520 330) rotate("+(frame*.9)+")"}>
          <circle r="122" fill="#d2ad52" stroke="#6b5531" strokeWidth="18"/><circle r="99" fill="#e9d49b" stroke="#584d39" strokeWidth="8"/>
          <path d="M0 -70 L11 12 L0 73 L-11 12Z" fill="#272c2b"/><circle r="16" fill="#242829"/>
        </g>
      </svg>
      <div style={{position:"absolute",top:26,left:30,fontSize:16,fontWeight:950,letterSpacing:".15em",color:"#272c2d"}}>1889 / THE MECHANICAL AGE</div>
      <div style={{position:"absolute",right:35,bottom:25,width:115,height:130,borderRadius:"48% 48% 35% 35%",background:"#18202a",border:"6px solid #f3ead9",boxShadow:"0 8px 20px rgba(0,0,0,.25)"}}>
        <div style={{position:"absolute",left:22,top:34,width:17,height:17,borderRadius:"50%",background:"#fff"}}/><div style={{position:"absolute",right:22,top:34,width:17,height:17,borderRadius:"50%",background:"#fff"}}/><div style={{position:"absolute",left:39,top:78,width:35,height:7,borderRadius:8,background:"#eaa27c"}}/>
      </div>
    </div>
  );
  if (variant === 1) return (
    <div style={{position:"absolute",inset:0,background:"#b8ee48",overflow:"hidden"}}>
      <div style={{position:"absolute",inset:0,background:"linear-gradient(135deg,#c7f879,#92d630)"}}/>
      <div style={{position:"absolute",top:40,left:44,fontSize:15,fontWeight:950,letterSpacing:".2em",color:"#20301d"}}>EASING STUDY / 04</div>
      <Word size={250} color="#111914" tracking={-.14} style={{position:"absolute",left:25,top:145}}>EASE</Word>
      <div style={{position:"absolute",left:45,bottom:45,width:320,height:4,background:"#17201a"}}/>
      <div style={{position:"absolute",left:45,bottom:64,fontSize:13,fontWeight:900,letterSpacing:".18em",color:"#253922"}}>OUT / CUBIC / SPRING</div>
    </div>
  );
  if (variant === 2) return (
    <div style={{position:"absolute",inset:0,background:"radial-gradient(circle at 70% 35%,#456ee6,#132ab3 62%,#081678)"}}>
      <div style={{position:"absolute",inset:0,backgroundImage:"linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px)",backgroundSize:"35px 35px"}}/>
      <Word size={165} color="#eef3ff" tracking={-.11} style={{position:"absolute",left:30,top:125,textShadow:"3px 3px 0 #7f99f0,9px 11px 20px rgba(0,0,0,.25)"}}>FUTURE</Word>
      <Word size={90} color="#fff" tracking={-.07} style={{position:"absolute",left:42,top:300}}>IS ALREADY HERE.</Word>
      <div style={{position:"absolute",right:60,bottom:55,width:140,height:140,borderRadius:"50%",border:"8px solid #9df3ff",boxShadow:"0 0 35px #74dff6"}}/>
    </div>
  );
  if (variant === 3) return (
    <div style={{position:"absolute",inset:0,background:"#2e7ac4",color:"#fff",overflow:"hidden"}}>
      <div style={{position:"absolute",top:34,left:40,fontSize:16,fontWeight:900,letterSpacing:".16em"}}>COURSE / NEW RELEASE</div>
      <div style={{position:"absolute",left:50,bottom:55,width:310,height:300,borderRadius:"48%",background:"#f6e7c8",transform:"rotate(-8deg)"}}>
        <div style={{position:"absolute",left:74,top:37,width:160,height:225,borderRadius:"48% 48% 38% 38%",background:"#202b3b"}}/>
        <div style={{position:"absolute",left:106,top:94,width:22,height:22,borderRadius:"50%",background:"#fff"}}/><div style={{position:"absolute",left:180,top:94,width:22,height:22,borderRadius:"50%",background:"#fff"}}/><div style={{position:"absolute",left:130,top:166,width:60,height:10,borderRadius:8,background:"#e8896f"}}/>
      </div>
      <div style={{position:"absolute",right:42,top:140,width:280,height:305,background:"#fff",borderRadius:18,padding:24,boxSizing:"border-box",color:"#162333",boxShadow:"0 20px 32px rgba(0,0,0,.18)"}}>
        <div style={{fontSize:17,fontWeight:900}}>Courses</div><div style={{marginTop:25,height:125,borderRadius:12,background:"#e8eff4"}}/><div style={{marginTop:22,fontSize:29,fontWeight:950}}>Learn to create.</div>
      </div>
    </div>
  );
  if (variant === 4) return (
    <div style={{position:"absolute",inset:0,background:"#bfe2d4",overflow:"hidden",color:"#263d34"}}>
      <div style={{position:"absolute",left:45,top:35,fontSize:16,fontWeight:900,letterSpacing:".15em"}}>WEBSITES / OPEN DESIGN</div>
      <div style={{position:"absolute",left:48,right:48,top:100,bottom:55,background:"#f5efe2",borderRadius:14,padding:28,boxSizing:"border-box",boxShadow:"0 25px 40px rgba(42,73,60,.12)"}}>
        <Word size={104} color="#243c31">a little</Word><Word size={104} color="#243c31">wonder.</Word>
        <div style={{position:"absolute",right:48,top:58,width:190,height:190,borderRadius:"50%",background:"#e6bb54"}}><div style={{position:"absolute",left:80,top:28,width:30,height:130,background:"#fff4d4",transform:"rotate(22deg)"}}/><div style={{position:"absolute",left:25,top:78,width:130,height:30,background:"#f27e6e",transform:"rotate(-18deg)"}}/></div>
        <div style={{position:"absolute",left:28,bottom:20,fontSize:23,fontWeight:950,letterSpacing:".12em"}}>websites</div>
      </div>
    </div>
  );
  if (variant === 5) return (
    <div style={{position:"absolute",inset:0,background:"#f0efea",color:"#141719",overflow:"hidden"}}>
      <Word size={210} color="#141719" tracking={-.12} style={{position:"absolute",left:-20,top:20}}>MORRO</Word>
      <Word size={210} color="#f0efea" tracking={-.12} style={{position:"absolute",left:-20,top:170,WebkitTextStroke:"3px #141719"}}>MORRO</Word>
      <Word size={210} color="#141719" tracking={-.12} style={{position:"absolute",left:-20,top:320,opacity:.9}}>MORRO</Word>
    </div>
  );
  return (
    <div style={{position:"absolute",inset:0,background:"#e43c31",overflow:"hidden"}}>
      <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#fff 0 5px,transparent 5px)",backgroundSize:"26px 26px"}}/>
      <div style={{position:"absolute",left:"50%",top:"50%",width:370,height:370,marginLeft:-185,marginTop:-185,borderRadius:"50%",border:"19px solid #171719",background:"#f6d43f",display:"grid",placeItems:"center"}}>
        <div style={{width:260,height:260,borderRadius:"50%",background:"#fff",border:"8px solid #171719",display:"grid",placeItems:"center"}}><PlayGlyph size={180} color="#111315"/></div>
      </div>
    </div>
  );
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

const LaunchKitWindow = ({ frame, variant, countdown = -1 }: { frame: number; variant: number; countdown?: number }) => {
  const { fps } = useVideoConfig();
  const p = pop(frame, fps, 0, 80, 19);
  return (
    <AbsoluteFill style={{ ...full, background: "#f1eee6" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 48%,#fff 0%,#f3f0e9 65%)" }} />
      <div style={{
        position: "absolute", left: 200, right: 200, top: 92, bottom: 85,
        borderRadius: 24, background: "#fff", border: "1px solid #e7e4de",
        boxShadow: "0 38px 90px rgba(30,35,38,.16),0 4px 18px rgba(30,35,38,.06)",
        transform: "translateY(" + ((1 - p) * 100) + "px) scale(" + (.97 + .03 * p) + ")",
        overflow: "hidden",
      }}>
        <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 54, borderBottom: "1px solid #efede8", display: "flex", alignItems: "center", padding: "0 26px", justifyContent: "space-between" }}>
          <div style={{ display: "flex", gap: 7 }}>
            {["#e9a18d", "#e9d18a", "#98c6a5"].map((c, i) => <div key={i} style={{ width: 9, height: 9, borderRadius: "50%", background: c }} />)}
          </div>
          <div style={{ fontSize: 14, fontWeight: 850, color: "#7a817e", letterSpacing: ".18em" }}>LAUNCH KIT</div>
          <div style={{ fontSize: 13, fontWeight: 800, color: "#a4a7a4" }}>Preview / Export / ⋯</div>
        </div>
        <div style={{ position: "absolute", top: 54, bottom: 0, left: 0, width: 430, borderRight: "1px solid #efede8", padding: "40px 35px", boxSizing: "border-box", display: "flex", flexDirection: "column" }}>
          <div style={{ fontSize: 13, fontWeight: 900, color: "#a0a4a1", letterSpacing: ".15em" }}>PROMPT / YOUR BRIEF</div>
          <div style={{ marginTop: 23, maxWidth: 322, alignSelf: "flex-start", background: "#f3f3f0", color: "#373d3e", padding: "20px 22px", borderRadius: "4px 18px 18px 18px", fontSize: 20, lineHeight: 1.35, fontWeight: 580 }}>
            Make a 10s launch film for our app.
          </div>
          <div style={{ marginTop: 24, fontSize: 14, color: "#8f9896", fontWeight: 800 }}>MODEL</div>
          <div style={{ marginTop: 10, display: "flex", alignItems: "center", justifyContent: "space-between", background: "#fbfaf8", border: "1px solid #e5e5e0", padding: "14px 17px", borderRadius: 12 }}>
            <div style={{ fontSize: 16, fontWeight: 800, color: "#384142" }}>✦ Claude Opus 5.5</div><div style={{ fontSize: 16, color: "#9ca29f" }}>⌄</div>
          </div>
          <div style={{ marginTop: 26, fontSize: 14, color: "#8f9896", fontWeight: 800 }}>DIRECTION</div>
          <div style={{ marginTop: 10, background: "#fbfaf8", border: "1px solid #e5e5e0", padding: "19px 17px", borderRadius: 12, color: "#56605f", fontSize: 16, lineHeight: 1.42 }}>
            Make it feel like a launch. Keep the typography bold, the pace cinematic and the visuals tactile.
          </div>
          <div style={{ marginTop: "auto", border: "1px solid #e5e5e0", background: "#fff", borderRadius: 14, padding: "16px 16px 16px 19px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span style={{ fontSize: 15, color: "#a1a6a3" }}>Make it feel like a launch.</span>
            <div style={{ width: 38, height: 38, borderRadius: "50%", background: "#161b1c", display: "grid", placeItems: "center" }}><svg viewBox="0 0 30 30" width="20" height="20"><path d="M5 15H24M16 6L25 15L16 24" stroke="#fff" strokeWidth="2.4" strokeLinecap="round" fill="none" /></svg></div>
          </div>
          <div style={{ marginTop: 14, fontSize: 12, fontWeight: 800, color: "#9ca29f" }}>✦ Motion · Claude Opus 5.5 · 16:9</div>
        </div>
        <div style={{ position: "absolute", left: 430, right: 0, top: 54, bottom: 0, padding: 32, boxSizing: "border-box", background: "#faf9f6" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 22 }}>
            <div style={{ fontSize: 14, fontWeight: 900, letterSpacing: ".14em", color: "#707a77" }}>PREVIEW</div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, fontSize: 13, color: "#8d9693" }}><span>Made with</span><span style={{ background: "#fff", border: "1px solid #e7e7e2", padding: "6px 12px", borderRadius: 20, fontWeight: 850, color: "#40484a" }}>✦ {["Claude Opus 5.5", "Milo", "GPT-4.1", "Mistral Vibe"][variant % 4]}</span></div>
          </div>
          <div style={{ position: "absolute", left: 32, right: 32, top: 105, bottom: 36, background: "#fff", borderRadius: 15, border: "1px solid #e9e7e1", overflow: "hidden", boxShadow: "0 14px 32px rgba(35,41,39,.08)" }}>
            {countdown >= 0 ? <CountdownArtwork value={countdown} frame={frame} /> : <PreviewArtwork variant={variant} frame={frame} />}
          </div>
          <div style={{ position: "absolute", bottom: 15, right: 44, fontSize: 11, letterSpacing: ".12em", color: "#a3a7a4", fontWeight: 800 }}>GENERATED PREVIEW / 16:9</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const LaunchVariant = ({ variant, countdown = -1 }: { variant: number; countdown?: number }) => {
  const frame = useCurrentFrame();
  return <LaunchKitWindow frame={frame} variant={variant} countdown={countdown} />;
};

const LaunchKitSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={21}><LaunchVariant variant={0} /></Sequence>
    <Sequence from={21} durationInFrames={21}><LaunchVariant variant={1} /></Sequence>
    <Sequence from={42} durationInFrames={21}><LaunchVariant variant={2} /></Sequence>
    <Sequence from={63} durationInFrames={21}><LaunchVariant variant={3} /></Sequence>
    <Sequence from={84} durationInFrames={21}><LaunchVariant variant={4} /></Sequence>
    <Sequence from={105} durationInFrames={21}><LaunchVariant variant={5} /></Sequence>
    <Sequence from={126} durationInFrames={24}><LaunchVariant variant={6} /></Sequence>
  </AbsoluteFill>
);
const CountdownSequence = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={20}><LaunchVariant variant={0} countdown={3} /></Sequence>
    <Sequence from={20} durationInFrames={20}><LaunchVariant variant={1} countdown={2} /></Sequence>
    <Sequence from={40} durationInFrames={20}><LaunchVariant variant={2} countdown={1} /></Sequence>
  </AbsoluteFill>
);

const CubeFaceArtwork = ({ kind }: { kind: number }) => {
  if (kind === 0) return <div style={{ position: "absolute", inset: 0, background: "linear-gradient(145deg,#e9b3a4,#e56c56)" }}><div style={{ position: "absolute", inset: 28, border: "4px solid rgba(255,255,255,.82)", borderRadius: 16 }} /><div style={{ position: "absolute", left: 35, bottom: 40, fontSize: 38, color: "#fff", fontWeight: 950 }}>MOTION</div><div style={{ position: "absolute", right: 30, top: 30, width: 100, height: 100, border: "12px solid #fff", borderRadius: "50%" }} /></div>;
  if (kind === 1) return <div style={{ position: "absolute", inset: 0, background: "#1927bb" }}><div style={{ position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(0deg,transparent 0 25px,rgba(255,255,255,.12) 26px 28px)" }} /><Word size={65} color="#fff" style={{ position: "absolute", left: 26, top: 30 }}>WORLD</Word><Word size={65} color="#b7ee50" style={{ position: "absolute", left: 26, top: 95 }}>MIND</Word></div>;
  if (kind === 2) return <div style={{ position: "absolute", inset: 0, background: "#f4efdf" }}><div style={{ position: "absolute", left: "20%", top: "20%", width: "60%", height: "60%", border: "10px solid #16191b", borderRadius: "50%" }} /><div style={{ position: "absolute", left: "38%", top: "38%", width: "24%", height: "24%", background: "#e96e55", borderRadius: "50%" }} /><div style={{ position: "absolute", left: 24, bottom: 24, color: "#171b1b", fontSize: 20, fontWeight: 950 }}>THE FUTURE</div></div>;
  if (kind === 3) return <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle,#fff 0%,#f2d449 58%,#d84e3c 100%)" }}><div style={{ position: "absolute", inset: 34, border: "5px dotted #181a1d", borderRadius: "50%" }} /><div style={{ position: "absolute", inset: 70, border: "8px solid #181a1d", borderRadius: "50%" }} /><div style={{ position: "absolute", inset: 135, background: "#17191c", borderRadius: "50%" }} /></div>;
  if (kind === 4) return <div style={{ position: "absolute", inset: 0, background: "#a7ed6b" }}><Word size={67} color="#101b13" style={{ position: "absolute", left: 26, top: 30 }}>EASE</Word><div style={{ position: "absolute", left: 30, right: 30, bottom: 40, height: 6, background: "#101b13" }} /></div>;
  return <div style={{ position: "absolute", inset: 0, background: "#111416", display: "grid", placeItems: "center" }}><div style={{ width: 150, height: 150, border: "9px solid #fff", borderRadius: "50%", display: "grid", placeItems: "center" }}><PlayGlyph size={80} /></div></div>;
};

const SvgCube3D = ({ frame, size, x, y, seed=0 }: { frame:number; size:number; x:number; y:number; seed?:number }) => {
  const rx=0.62+Math.sin(frame/19+seed)*0.06;
  const ry=-0.86+frame*0.006+seed*0.18;
  const rz=0.08*Math.sin(frame/27+seed);
  const base=[
    [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
    [-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1],
  ];
  const transformed=base.map(([px,py,pz])=>{
    const y1=py*Math.cos(rx)-pz*Math.sin(rx);
    const z1=py*Math.sin(rx)+pz*Math.cos(rx);
    const x2=px*Math.cos(ry)+z1*Math.sin(ry);
    const z2=-px*Math.sin(ry)+z1*Math.cos(ry);
    const x3=x2*Math.cos(rz)-y1*Math.sin(rz);
    const y3=x2*Math.sin(rz)+y1*Math.cos(rz);
    return {x:x3,y:y3,z:z2};
  });
  const projected=transformed.map(p=>{
    const perspective=4.2/(4.2-p.z*.48);
    return {x:x+p.x*size*.5*perspective,y:y+p.y*size*.5*perspective,z:p.z};
  });
  const faces=[
    {ids:[4,5,6,7],color:"#e58d78",label:"MOTION",kind:0},
    {ids:[5,1,2,6],color:"#1c2da6",label:"WORLD",kind:1},
    {ids:[0,4,7,3],color:"#f4ead5",label:"FUTURE",kind:2},
    {ids:[0,1,5,4],color:"#e5c24a",label:"EASE",kind:3},
    {ids:[3,2,6,7],color:"#a5de75",label:"CREATE",kind:4},
    {ids:[0,1,2,3],color:"#17202b",label:"PLAY",kind:5},
  ].map(face=>{
    const pts=face.ids.map(i=>projected[i]);
    return {...face,pts,depth:pts.reduce((a,p)=>a+p.z,0)/pts.length,
      cx:pts.reduce((a,p)=>a+p.x,0)/pts.length,
      cy:pts.reduce((a,p)=>a+p.y,0)/pts.length};
  }).sort((a,b)=>a.depth-b.depth);
  const colors=["#fff","#d5eeff","#1b2531","#fff","#1e2c1e","#fff"];
  return (
    <g filter="url(#cube-shadow)">
      {faces.map((face,i)=>{
        const points=face.pts.map(p=>p.x+","+p.y).join(" ");
        const r=size*.075;
        return (
          <g key={face.kind}>
            <polygon points={points} fill={face.color} stroke="#fff" strokeWidth={Math.max(4,size*.009)} strokeLinejoin="round"/>
            <polygon points={points} fill="url(#cube-gloss)" opacity=".32"/>
            <circle cx={face.cx} cy={face.cy} r={r} fill="rgba(12,16,23,.35)" stroke="rgba(255,255,255,.86)" strokeWidth={Math.max(3,size*.007)}/>
            <path d={"M"+(face.cx-r*.34)+" "+(face.cy-r*.54)+" L"+(face.cx+r*.57)+" "+face.cy+" L"+(face.cx-r*.34)+" "+(face.cy+r*.54)+"Z"} fill={colors[face.kind]}/>
            <text x={face.cx} y={face.cy+r*1.72} textAnchor="middle" fontSize={size*.045} fontFamily="Arial,sans-serif" fontWeight="900" letterSpacing="3" fill={face.kind===2?"#253041":"#fff"}>{face.label}</text>
            <polyline points={face.pts.map(p=>p.x+","+p.y).join(" ")} fill="none" stroke="rgba(255,255,255,.22)" strokeWidth={2}/>
          </g>
        );
      })}
    </g>
  );
};

const TexturedCube = () => {
  const f=useCurrentFrame();
  return (
    <AbsoluteFill style={{...full,background:"radial-gradient(ellipse at 50% 43%,#f3f4f3 0%,#d4dadb 65%,#b6c1c4 100%)"}}>
      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
        <defs>
          <linearGradient id="cube-gloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#fff" stopOpacity=".55"/><stop offset="42%" stopColor="#fff" stopOpacity="0"/><stop offset="100%" stopColor="#06101f" stopOpacity=".2"/></linearGradient>
          <filter id="cube-shadow" x="-40%" y="-40%" width="180%" height="190%"><feGaussianBlur in="SourceAlpha" stdDeviation="24"/><feOffset dy="34"/><feComponentTransfer><feFuncA type="linear" slope=".34"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <ellipse cx="960" cy="850" rx="420" ry="80" fill="rgba(28,38,52,.15)" filter="url(#cube-shadow)"/>
        <SvgCube3D frame={f} size={610} x={960} y={510}/>
        <SvgCube3D frame={f+17} size={270} x={430} y={675} seed={1}/>
        <SvgCube3D frame={f+34} size={235} x={1500} y={350} seed={2}/>
      </svg>
      <div style={{position:"absolute",left:0,right:0,bottom:70,textAlign:"center",color:"#6c7a82",fontSize:17,fontWeight:900,letterSpacing:".21em"}}>ROTATE / REVEAL / REPEAT</div>
    </AbsoluteFill>
  );
};
const FinalLockup = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = pop(f, fps, 0, 80, 18);
  return (
    <AbsoluteFill style={{ ...full, background: "#faf9f5" }}>
      <div style={{position:"absolute",left:0,right:0,top:205,display:"flex",flexDirection:"column",alignItems:"center",transform:"translateY(" + ((1-p)*45) + "px)"}}>
        <div style={{position:"relative",width:190,height:190,borderRadius:"50%",border:"9px solid #9bcbd0",display:"grid",placeItems:"center",background:"#f8fbf8",boxShadow:"0 18px 45px rgba(64,100,107,.12)"}}>
          <div style={{position:"absolute",left:50,top:42,width:90,height:96,borderRadius:22,background:"#111719",display:"grid",placeItems:"center",boxShadow:"inset 0 2px 0 rgba(255,255,255,.24)"}}><PlayGlyph size={63} color="#fff"/></div>
          <div style={{position:"absolute",left:61,top:20,width:23,height:23,borderRadius:"50%",background:"#e7a18c",border:"4px solid #faf9f5"}}/>
          <div style={{position:"absolute",right:53,top:20,width:18,height:18,borderRadius:"50%",background:"#edc47e",border:"3px solid #faf9f5"}}/>
          <div style={{position:"absolute",left:33,top:4,width:16,height:27,borderRadius:"100% 0 100% 0",background:"#9bc9be",transform:"rotate(-30deg)"}}/>
          <div style={{position:"absolute",right:34,top:7,width:16,height:27,borderRadius:"100% 0 100% 0",background:"#e6b39f",transform:"rotate(35deg)"}}/>
        </div>
        <div style={{marginTop:24,fontFamily:displayFont,fontSize:78,fontWeight:950,color:"#14191b",letterSpacing:"-.075em"}}>OpenDesign Motion</div>
        <div style={{marginTop:16,fontSize:18,fontWeight:850,color:"#7f9495",letterSpacing:".22em"}}>MAKE EVERY FRAME MOVE</div>
        <div style={{marginTop:20,background:"#e8f3e4",color:"#496f50",borderRadius:24,padding:"8px 24px",fontSize:14,fontWeight:900,letterSpacing:".1em"}}>OPEN DESIGN / CREATIVE STUDIO</div>
      </div>
    </AbsoluteFill>
  );
};
export const OpenDesignMotion: React.FC = () => (
  <AbsoluteFill style={{ ...full, background: "#101214" }}>
    <Sequence from={0} durationInFrames={90}><OpeningScene /></Sequence>
    <Sequence from={90} durationInFrames={45}><HeroTitle /></Sequence>
    <Sequence from={135} durationInFrames={30}><BrandReveal /></Sequence>
    <Sequence from={165} durationInFrames={60}><ClaimScene /></Sequence>
    <Sequence from={225} durationInFrames={90}><GalleryWall /></Sequence>
    <Sequence from={315} durationInFrames={270}><PosterSequence /></Sequence>
    <Sequence from={585} durationInFrames={45}><NotJustOpus /></Sequence>
    <Sequence from={630} durationInFrames={135}><ModelAgentScene /></Sequence>
    <Sequence from={765} durationInFrames={150}><LaunchKitSequence /></Sequence>
    <Sequence from={915} durationInFrames={60}><CountdownSequence /></Sequence>
    <Sequence from={975} durationInFrames={84}><TexturedCube /></Sequence>
    <Sequence from={1059} durationInFrames={60}><FinalLockup /></Sequence>
    <Audio src={staticFile("audio/opendesign-motion-score.wav")} volume={0.92} />
  </AbsoluteFill>
);
