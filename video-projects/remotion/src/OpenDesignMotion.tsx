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

const W = 1920;
const H = 1080;
const TOTAL = 1119;
const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

const ease = (f: number, from: number, to: number, start = 0, end = 1) =>
  interpolate(f, [from, to], [start, end], { ...clamp, easing: Easing.outCubic });

const fadeIn = (f: number, frames = 18) => ease(f, 0, frames);
const fadeOut = (f: number, length: number, frames = 14) =>
  1 - ease(f, length - frames, length);

const full: React.CSSProperties = {
  width: "100%",
  height: "100%",
  overflow: "hidden",
  position: "relative",
  fontFamily: "Arial, Helvetica, sans-serif",
};

const shadowText = "0 3px 0 rgba(20,35,70,.16), 0 12px 35px rgba(30,50,80,.12)";

const Cloud = ({
  left,
  top,
  width,
  scale = 1,
  speed = 1,
  opacity = 0.8,
  frame,
}: {
  left: number;
  top: number;
  width: number;
  scale?: number;
  speed?: number;
  opacity?: number;
  frame: number;
}) => {
  const drift = interpolate(frame, [0, TOTAL], [0, 110 * speed], clamp);
  return (
    <div
      style={{
        position: "absolute",
        left,
        top,
        width,
        height: width * 0.4,
        opacity,
        transform: `translate3d(${drift}px,0,0) scale(${scale})`,
        filter: "blur(2px)",
      }}
    >
      <div style={{ position: "absolute", left: 0, top: width * 0.17, width: width * 0.62, height: width * 0.23, borderRadius: 999, background: "rgba(255,255,255,.86)" }} />
      <div style={{ position: "absolute", left: width * 0.18, top: 0, width: width * 0.36, height: width * 0.35, borderRadius: "50%", background: "rgba(255,255,255,.92)" }} />
      <div style={{ position: "absolute", left: width * 0.40, top: width * 0.09, width: width * 0.34, height: width * 0.29, borderRadius: "50%", background: "rgba(255,255,255,.9)" }} />
      <div style={{ position: "absolute", left: width * 0.57, top: width * 0.19, width: width * 0.35, height: width * 0.19, borderRadius: 999, background: "rgba(255,255,255,.86)" }} />
    </div>
  );
};

const Cloudscape = ({ frame, warm = false }: { frame: number; warm?: boolean }) => (
  <AbsoluteFill
    style={{
      background: warm
        ? "linear-gradient(180deg,#94b2cf 0%,#c7d6dc 36%,#f5e5d8 72%,#e5d6d1 100%)"
        : "linear-gradient(180deg,#8fb0d5 0%,#bfd0df 42%,#f4e0d4 78%,#e7d1cd 100%)",
    }}
  >
    <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 38%,rgba(255,255,255,.5),transparent 56%)" }} />
    <Cloud frame={frame} left={-120} top={190} width={540} speed={0.7} opacity={0.7} />
    <Cloud frame={frame} left={940} top={130} width={650} speed={-0.45} scale={1.16} opacity={0.66} />
    <Cloud frame={frame} left={1330} top={460} width={520} speed={0.36} scale={1.4} opacity={0.44} />
    <Cloud frame={frame} left={210} top={620} width={690} speed={-0.26} scale={1.35} opacity={0.34} />
    <Cloud frame={frame} left={-180} top={870} width={780} speed={0.22} scale={1.5} opacity={0.34} />
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 170, background: "linear-gradient(180deg,rgba(220,214,213,0),rgba(199,193,199,.45))", filter: "blur(18px)" }} />
  </AbsoluteFill>
);

const Cursor = ({ x, y, scale = 1 }: { x: number; y: number; scale?: number }) => (
  <svg
    viewBox="0 0 34 44"
    width={34 * scale}
    height={44 * scale}
    style={{
      position: "absolute",
      left: x,
      top: y,
      filter: "drop-shadow(0 3px 3px rgba(0,0,0,.25))",
      pointerEvents: "none",
    }}
  >
    <path d="M3 2 L3 35 L12 27 L19 41 L25 38 L18 24 L31 23 Z" fill="#fff" stroke="#20232b" strokeWidth="2.3" strokeLinejoin="round" />
  </svg>
);

const Word = ({
  children,
  size,
  color = "#171a20",
  weight = 900,
  italic = false,
  tracking = -0.06,
  style = {},
}: {
  children: React.ReactNode;
  size: number;
  color?: string;
  weight?: number;
  italic?: boolean;
  tracking?: number;
  style?: React.CSSProperties;
}) => (
  <div
    style={{
      fontSize: size,
      lineHeight: 0.88,
      fontWeight: weight,
      color,
      fontStyle: italic ? "italic" : "normal",
      letterSpacing: `${tracking}em`,
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </div>
);

const SkyIntro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const typeProgress = Math.floor(ease(frame, 54, 126, 0, 27));
  const phrase = "Introducing OpenDesign Motion";
  const cursorX = interpolate(frame, [0, 74, 142, 186], [820, 1160, 1360, 1510], clamp);
  const press = frame > 157 ? ease(frame, 157, 165) : 0;
  const cardY = interpolate(spring({ frame, fps, config: { damping: 21, stiffness: 80 } }), [0, 1], [64, 0]);
  const topFade = fadeIn(frame, 18);
  return (
    <AbsoluteFill style={{ ...full }}>
      <Cloudscape frame={frame} />
      <AbsoluteFill style={{ padding: "74px 120px", opacity: topFade }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontSize: 22, fontWeight: 800, letterSpacing: ".08em", color: "#334353" }}>OPENDESIGN <span style={{ opacity: .6, fontWeight: 500 }}> / MOTION LAB</span></div>
          <div style={{ display: "flex", gap: 24, alignItems: "center", color: "#4b5a6d", fontSize: 18, letterSpacing: ".08em" }}>
            <span>STUDIO</span><span>WORKFLOW</span><span>01 / 09</span>
          </div>
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 240, textAlign: "center" }}>
          <div style={{ fontFamily: "Georgia, 'Times New Roman', serif", fontSize: 88, letterSpacing: "-.045em", color: "#fff", textShadow: "0 3px 24px rgba(55,76,102,.24)", opacity: ease(frame, 4, 30) }}>
            Let’s create Motion design
          </div>
          <div style={{ marginTop: 24, color: "#f7fbff", fontSize: 22, letterSpacing: ".19em", fontWeight: 600, opacity: ease(frame, 22, 42) }}>
            A NEW WAY TO MAKE IDEAS MOVE
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            left: 270,
            right: 270,
            bottom: 170,
            height: 190,
            borderRadius: 34,
            background: "rgba(255,255,255,.82)",
            border: "1px solid rgba(255,255,255,.95)",
            boxShadow: "0 28px 90px rgba(53,75,101,.2), inset 0 1px 0 rgba(255,255,255,.95)",
            backdropFilter: "blur(18px)",
            transform: `translateY(${cardY}px) scale(${1 - press * .025})`,
            padding: "34px 42px",
            boxSizing: "border-box",
          }}
        >
          <div style={{ color: "#6c7b8e", fontSize: 17, fontWeight: 700, letterSpacing: ".14em", marginBottom: 20 }}>DESCRIBE THE MOTION YOU WANT</div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div style={{ fontSize: 37, color: "#293747", fontWeight: 500, letterSpacing: "-.03em" }}>
              {phrase.slice(0, typeProgress)}
              <span style={{ display: "inline-block", width: 3, height: 38, verticalAlign: "middle", background: frame < 126 ? "#6a87ad" : "transparent", marginLeft: 3 }} />
            </div>
            <div style={{ width: 66, height: 66, borderRadius: 22, background: "#293e5e", display: "grid", placeItems: "center", transform: `scale(${1 - press * .12})`, boxShadow: "0 8px 22px rgba(27,53,88,.22)" }}>
              <svg width="30" height="30" viewBox="0 0 30 30"><path d="M4 15 H25 M16 5 L26 15 L16 25" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </div>
          </div>
          <div style={{ position: "absolute", bottom: 18, right: 42, color: "#94a1b0", fontSize: 14, letterSpacing: ".08em" }}>SHIFT + ENTER TO ADD A LINE</div>
        </div>
        <div style={{ position: "absolute", left: 440, bottom: 95, fontSize: 16, color: "#edf4fb", letterSpacing: ".15em", opacity: ease(frame, 110, 140) }}>GENERATING YOUR FIRST SCENE <span style={{ display: "inline-block", width: 9, height: 9, borderRadius: 99, background: "#fff", marginLeft: 10, boxShadow: "0 0 16px #fff" }} /></div>
        <Cursor x={cursorX} y={frame > 158 ? 846 : 780} scale={1.06} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const TitleScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 18, stiffness: 72, mass: 0.8 } });
  const y = interpolate(p, [0, 1], [260, 0]);
  const scale = interpolate(p, [0, 1], [0.86, 1]);
  const exit = ease(frame, 75, 90);
  const titleStyle: React.CSSProperties = {
    fontSize: 188,
    lineHeight: 0.88,
    letterSpacing: "-.075em",
    fontWeight: 900,
    fontStyle: "italic",
    color: "#fff",
    textShadow: "5px 8px 0 rgba(53,75,111,.14), 0 18px 48px rgba(50,67,91,.2)",
    whiteSpace: "nowrap",
  };
  return (
    <AbsoluteFill style={full}>
      <Cloudscape frame={frame + 205} warm />
      <div style={{ position: "absolute", left: 0, right: 0, top: 112, textAlign: "center", color: "#fff", opacity: fadeIn(frame, 10) }}>
        <div style={{ fontSize: 22, letterSpacing: ".28em", fontWeight: 800 }}>OPENDESIGN PRESENTS</div>
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 5,
          transform: `translate3d(${interpolate(frame, [0, 90], [0, -520], clamp)}px,${y + exit * -260}px,0) scale(${scale})`,
          opacity: 1 - exit,
        }}
      >
        <div style={titleStyle}>Introducing</div>
        <div style={{ ...titleStyle, fontSize: 206, transform: "translateX(-8px)" }}>OpenDesign</div>
        <div style={{ ...titleStyle, fontSize: 226, letterSpacing: "-.09em" }}>MOTION.</div>
      </div>
      <div style={{ position: "absolute", bottom: 90, left: 0, right: 0, textAlign: "center", color: "#fff", fontWeight: 700, letterSpacing: ".22em", fontSize: 17, opacity: fadeOut(frame, 90, 14) }}>
        DESIGN IS NOT STATIC
      </div>
    </AbsoluteFill>
  );
};

const starPoints = (points: number, outer: number, inner: number) =>
  Array.from({ length: points * 2 }, (_, i) => {
    const angle = -Math.PI / 2 + (i * Math.PI) / points;
    const radius = i % 2 === 0 ? outer : inner;
    return `${100 + Math.cos(angle) * radius},${100 + Math.sin(angle) * radius}`;
  }).join(" ");

const RadialMark = ({ frame, size = 168 }: { frame: number; size?: number }) => (
  <svg width={size} height={size} viewBox="0 0 200 200" style={{ transform: `rotate(${frame * 1.8}deg)`, filter: "drop-shadow(0 14px 18px rgba(176,54,35,.16))" }}>
    <polygon points={starPoints(16, 92, 58)} fill="#f05a38" />
    <circle cx="100" cy="100" r="13" fill="#fff1d8" />
  </svg>
);

const ClaimScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const mark = spring({ frame, fps, config: { damping: 15, stiffness: 100 } });
  const scale = interpolate(mark, [0, 1], [0.2, 1]);
  const reveal = ease(frame, 26, 50);
  const wipe = ease(frame, 54, 75);
  return (
    <AbsoluteFill style={{ ...full, background: "#f4efe3" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 50% 42%,#fff9ec 0%,#f4efe3 66%)" }} />
      <div style={{ position: "absolute", top: 125, left: 170, color: "#a2a09a", fontSize: 18, letterSpacing: ".2em", fontWeight: 800 }}>A NEW CREATIVE RUNTIME</div>
      <div style={{ position: "absolute", top: 335, left: 0, right: 0, display: "flex", justifyContent: "center", alignItems: "center", gap: 26, transform: `scale(${scale})`, opacity: fadeIn(frame, 16) }}>
        <RadialMark frame={frame} size={156} />
        <Word size={118} color="#222326" tracking={-0.055} weight={800}>Claude Motion.</Word>
      </div>
      <div style={{ position: "absolute", top: 590, left: 180, right: 180, textAlign: "center", opacity: reveal }}>
        <Word size={78} weight={850} tracking={-0.06}>The open-source alternative</Word>
        <div style={{ display: "inline-block", position: "relative", marginTop: 22 }}>
          <div style={{ position: "absolute", left: -14, right: -14, top: 13, height: 78, background: "#b9e64e", transform: `scaleX(${wipe}) rotate(-1deg)`, transformOrigin: "left center" }} />
          <Word size={82} weight={900} color="#242a23" style={{ position: "relative" }}>to Claude Motion.</Word>
        </div>
      </div>
      <div style={{ position: "absolute", bottom: 85, left: 0, right: 0, textAlign: "center", fontSize: 17, color: "#aaa49a", letterSpacing: ".19em", opacity: fadeIn(frame, 45) }}>OPEN SOURCE · FRAME BY FRAME · YOUR WORKFLOW</div>
    </AbsoluteFill>
  );
};

const miniPosters = [
  { title: "FUTURE\nIS NOW", bg: "#202e9a", fg: "#fff", accent: "#8af85f", size: 37 },
  { title: "MIND", bg: "#f1b8a7", fg: "#202124", accent: "#ec5a42", size: 58 },
  { title: "EASE", bg: "#b9ee4c", fg: "#152219", accent: "#152219", size: 66 },
  { title: "NEVER\nLINEAR", bg: "#151515", fg: "#fff", accent: "#b9ee4c", size: 46 },
  { title: "MOVE\nWITH\nINTENT", bg: "#ff6c4d", fg: "#191919", accent: "#ffe2aa", size: 35 },
  { title: "3.7%", bg: "#e0e8e5", fg: "#172c30", accent: "#ff654a", size: 58 },
  { title: "TYPE\nIS\nMOTION", bg: "#e5b6e9", fg: "#25212e", accent: "#4b45c6", size: 35 },
  { title: "SHIFT", bg: "#f0e9d6", fg: "#df5138", accent: "#222", size: 60 },
  { title: "FORM\nFOLLOWS\nFEELING", bg: "#19212d", fg: "#e3e8fa", accent: "#7c9af8", size: 31 },
  { title: "STAY\nCURIOUS", bg: "#d6d8ff", fg: "#28215e", accent: "#ee6f47", size: 40 },
  { title: "CREATE", bg: "#f7d44d", fg: "#181818", accent: "#fff", size: 50 },
  { title: "MORE\nTHAN\nSTATIC", bg: "#e6f2f3", fg: "#273e46", accent: "#ef684b", size: 34 },
];

const MiniPoster = ({ index, frame }: { index: number; frame: number }) => {
  const p = miniPosters[index];
  const drift = Math.sin((frame + index * 9) / 19) * 8;
  const rotate = (index % 2 ? -1 : 1) * (2 + Math.sin(frame / 22 + index) * 1.8);
  return (
    <div
      style={{
        height: 270,
        borderRadius: 14,
        overflow: "hidden",
        background: p.bg,
        color: p.fg,
        position: "relative",
        boxShadow: "0 24px 48px rgba(17,22,35,.2)",
        transform: `translateY(${drift}px) rotate(${rotate}deg)`,
        padding: 22,
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <div style={{ fontSize: 11, letterSpacing: ".18em", fontWeight: 800, opacity: .75 }}>OD / 0{index + 1}</div>
      <div style={{ fontSize: p.size, fontWeight: 950, lineHeight: .83, letterSpacing: "-.075em", whiteSpace: "pre-line" }}>{p.title}</div>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 10, fontWeight: 700, letterSpacing: ".12em" }}>
        <span>MOTION STUDY</span><span style={{ color: p.accent }}>2026</span>
      </div>
      {index === 5 && <div style={{ position: "absolute", width: 110, height: 110, border: `8px solid ${p.accent}`, borderRadius: "50%", right: 20, top: 55, opacity: .8 }} />}
    </div>
  );
};

const GalleryScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 20, stiffness: 62 } });
  const angle = interpolate(frame, [0, 81], [16, -12], clamp);
  const zoom = interpolate(enter, [0, 1], [0.8, 1.04]);
  return (
    <AbsoluteFill style={{ ...full, background: "#e9e6df" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 42%,#fff 0%,#e9e6df 65%)" }} />
      <div style={{ position: "absolute", top: 52, left: 80, fontSize: 18, fontWeight: 800, color: "#343842", letterSpacing: ".18em" }}>MOTION DESIGN / SELECTED WORKS</div>
      <div
        style={{
          position: "absolute",
          left: -90,
          top: 110,
          width: 2100,
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 24,
          transform: `perspective(1500px) rotateY(${angle}deg) rotateX(5deg) scale(${zoom}) translate3d(${interpolate(frame, [0, 81], [130, -90], clamp)}px,${interpolate(frame, [0, 81], [80, -45], clamp)}px,0)`,
          transformOrigin: "center center",
        }}
      >
        {miniPosters.map((_, i) => <MiniPoster key={i} index={i} frame={frame} />)}
      </div>
      <div style={{ position: "absolute", bottom: 52, right: 88, color: "#777b80", fontSize: 16, letterSpacing: ".2em", fontWeight: 800 }}>SCROLL TO EXPLORE ↘</div>
    </AbsoluteFill>
  );
};

const PosterFuture = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 55], [170, -15], clamp);
  const y = interpolate(spring({ frame: f, fps: 30, config: { damping: 18, stiffness: 80 } }), [0, 1], [140, 0]);
  return (
    <AbsoluteFill style={{ ...full, background: "#2534b8", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 75% 35%,rgba(104,135,255,.7),transparent 42%)" }} />
      <div style={{ position: "absolute", left: 95, top: 80, fontSize: 18, letterSpacing: ".18em", fontWeight: 800 }}>FUTURE SYSTEMS / 001</div>
      <div style={{ position: "absolute", left: 85, top: 230, transform: `translateX(${x}px) translateY(${y}px)` }}>
        <Word size={184} color="#fff" tracking={-0.075}>THE FUTURE</Word>
        <Word size={184} color="#fff" tracking={-0.075}>IS ALREADY</Word>
        <Word size={206} color="#a8fa5a" tracking={-0.08}>HERE<span style={{ color: "#fff" }}>.</span></Word>
      </div>
      <div style={{ position: "absolute", right: 120, bottom: 95, width: 260, height: 260, border: "2px solid rgba(255,255,255,.5)", borderRadius: "50%", transform: `rotate(${f * 1.5}deg)` }}>
        <div style={{ position: "absolute", inset: 30, border: "1px solid rgba(255,255,255,.5)", borderRadius: "50%" }} />
        <div style={{ position: "absolute", width: 22, height: 22, borderRadius: "50%", background: "#a8fa5a", left: 112, top: -10, boxShadow: "0 0 35px #a8fa5a" }} />
      </div>
    </AbsoluteFill>
  );
};

const CirclePoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#f0b7a9", color: "#252126" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(120deg,#f1c3b5,#e4a9ac)" }} />
      <div style={{ position: "absolute", top: 70, left: 90, fontSize: 18, letterSpacing: ".2em", fontWeight: 800 }}>MOTION / STUDY 02</div>
      <div style={{ position: "absolute", left: "50%", top: "50%", width: 820, height: 820, transform: `translate(-50%,-50%) rotate(${f * 1.9}deg)` }}>
        {[0, 1, 2, 3].map((i) => (
          <div key={i} style={{ position: "absolute", left: i * 66, top: i * 66, right: i * 66, bottom: i * 66, border: `${i === 0 ? 18 : 5}px solid rgba(32,28,35,${0.85 - i * 0.15})`, borderRadius: "50%", display: "grid", placeItems: "center" }}>
            <div style={{ position: "absolute", fontWeight: 950, fontSize: 42 - i * 4, letterSpacing: ".24em", transform: `rotate(${i % 2 ? -20 : 20}deg)` }}>THE FUTURE · THE FUTURE</div>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", right: 100, bottom: 95, fontSize: 18, letterSpacing: ".18em", fontWeight: 800 }}>ORBITAL TYPE / 02</div>
    </AbsoluteFill>
  );
};

const EasePoster = () => {
  const f = useCurrentFrame();
  const p = spring({ frame: f, fps: 30, config: { damping: 14, stiffness: 85 } });
  const scale = interpolate(p, [0, 1], [0.72, 1]);
  return (
    <AbsoluteFill style={{ ...full, background: "#b9ed47", color: "#16211a" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(140deg,#ccf36b,#9fda37)" }} />
      <div style={{ position: "absolute", top: 75, left: 85, fontSize: 18, fontWeight: 800, letterSpacing: ".2em" }}>EASING IS FEELING / 03</div>
      <div style={{ position: "absolute", left: 60, right: 60, top: 275, transform: `scale(${scale}) rotate(-3deg)`, transformOrigin: "left center" }}>
        <Word size={390} color="#142019" tracking={-0.12}>EASE</Word>
      </div>
      <svg viewBox="0 0 900 230" style={{ position: "absolute", right: 85, bottom: 90, width: 760, height: 195 }}>
        <path d="M20 190 C150 190 155 20 870 20" fill="none" stroke="#f4f0df" strokeWidth="9" strokeLinecap="round" />
        <path d="M20 190 C150 190 155 20 870 20" fill="none" stroke="#17241b" strokeWidth="2" strokeDasharray="10 15" />
      </svg>
      <div style={{ position: "absolute", left: 95, bottom: 95, fontSize: 19, fontWeight: 800, letterSpacing: ".17em" }}>OUT-CUBIC / SPRING / MOMENTUM</div>
    </AbsoluteFill>
  );
};

const LinearPoster = () => {
  const f = useCurrentFrame();
  const offset = interpolate(f, [0, 55], [260, -50], clamp);
  return (
    <AbsoluteFill style={{ ...full, background: "#16171a", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 80% 20%,rgba(120,130,140,.22),transparent 48%)" }} />
      <div style={{ position: "absolute", top: 70, left: 90, fontSize: 18, fontWeight: 800, letterSpacing: ".2em", color: "#a5a6a8" }}>ANTI-GRAVITY / 04</div>
      <div style={{ position: "absolute", left: 80, top: 220, transform: `translateX(${offset}px)` }}>
        <Word size={250} color="#fff" tracking={-0.11}>NEVER</Word>
        <Word size={280} color="#b7ed4b" tracking={-0.12}>LINEAR.</Word>
      </div>
      <div style={{ position: "absolute", right: 105, top: 260, width: 360, height: 360, border: "20px solid #fff", borderRadius: "50%", transform: `rotate(${f * 2.4}deg)` }}>
        <div style={{ position: "absolute", inset: 45, border: "4px solid #b7ed4b", borderRadius: "50%" }} />
        <div style={{ position: "absolute", width: 25, height: 25, background: "#b7ed4b", borderRadius: "50%", left: 146, top: -12 }} />
      </div>
      <div style={{ position: "absolute", bottom: 94, left: 90, fontSize: 19, letterSpacing: ".18em", fontWeight: 800 }}>CURVE / REACT / RELEASE</div>
    </AbsoluteFill>
  );
};


const MindPoster = () => {
  const f = useCurrentFrame();
  const orb = interpolate(f, [0, 42], [0.72, 1.04], clamp);
  return (
    <AbsoluteFill style={{ ...full, background: "#070a18", color: "#fff" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 65% 46%,#2536af 0%,#10142f 44%,#05060c 78%)" }} />
      <div style={{ position: "absolute", left: 82, top: 64, fontSize: 18, letterSpacing: ".2em", fontWeight: 800, color: "#b9c7ff" }}>MIND / MOTION STUDY</div>
      <div style={{ position: "absolute", left: 75, top: 210, transform: \`translateX(\${interpolate(f, [0, 40], [180, -15], clamp)}px)\` }}>
        <Word size={310} color="#3457ed" tracking={-0.1}>MIND</Word>
        <Word size={310} color="#3457ed" tracking={-0.1} style={{ opacity: .42 }}>MIND</Word>
        <Word size={310} color="#3457ed" tracking={-0.1}>MIND</Word>
      </div>
      <div style={{ position: "absolute", width: 430, height: 430, borderRadius: "50%", left: 1080, top: 265, transform: \`scale(\${orb})\`, background: "radial-gradient(circle at 34% 28%,rgba(255,255,255,.95),rgba(104,155,255,.4) 18%,rgba(25,44,148,.1) 48%,transparent 68%)", border: "3px solid rgba(150,190,255,.6)", boxShadow: "0 0 100px rgba(50,90,255,.5)" }}>
        <div style={{ position: "absolute", inset: 42, border: "2px solid rgba(150,240,110,.75)", borderRadius: "50%", transform: \`rotate(\${f * 2}deg)\` }} />
        <div style={{ position: "absolute", inset: 95, border: "2px solid rgba(150,240,110,.55)", borderRadius: "50%" }} />
      </div>
      <div style={{ position: "absolute", right: 90, bottom: 78, fontSize: 17, fontWeight: 800, letterSpacing: ".18em", color: "#a8b5f4" }}>THINK BEYOND THE FRAME</div>
    </AbsoluteFill>
  );
};

const ClockPoster = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ ...full, background: "#101d53", color: "#fff1b0" }}>
      <div style={{ position: "absolute", inset: 0, background: "repeating-radial-gradient(circle at 50% 50%,rgba(94,144,241,.24) 0 3px,transparent 4px 18px),radial-gradient(circle at 50% 50%,#253d9a,#08112f 70%)" }} />
      <div style={{ position: "absolute", top: 67, left: 90, color: "#ffdd75", fontSize: 22, fontWeight: 900, letterSpacing: ".16em" }}>1889</div>
      <div style={{ position: "absolute", width: 540, height: 540, left: 690, top: 220, borderRadius: "50%", border: "26px solid #e5b94f", boxShadow: "0 0 0 11px rgba(255,224,126,.25),0 0 70px rgba(247,192,65,.46)", background: "radial-gradient(circle,#f7d86e 0%,#b98729 58%,#4a3a2a 100%)", transform: \`rotate(\${f * 1.4}deg)\` }}>
        <div style={{ position: "absolute", inset: 24, border: "7px solid #f8e69d", borderRadius: "50%" }} />
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
          <div style={{ position: "absolute", width: 12, height: 195, background: "#27356c", borderRadius: 20, top: 86, transform: \`rotate(\${f * 5 + 20}deg)\`, transformOrigin: "50% 84%" }} />
          <div style={{ position: "absolute", width: 185, height: 12, background: "#27356c", borderRadius: 20, transform: \`rotate(\${f * 1.8 + 45}deg)\` }} />
          <div style={{ width: 34, height: 34, borderRadius: "50%", background: "#f8e69d", zIndex: 2 }} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 90, bottom: 85, fontSize: 19, fontWeight: 800, letterSpacing: ".15em" }}>TIME IS A MATERIAL</div>
    </AbsoluteFill>
  );
};

const EyePoster = () => {
  const f = useCurrentFrame();
  const blink = frameBlink(f);
  const pupilX = Math.sin(f / 9) * 16;
  return (
    <AbsoluteFill style={{ ...full, background: "#e8e9e2", color: "#1d2b31" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(135deg,#f4f2e8,#dce5df)" }} />
      <div style={{ position: "absolute", top: 65, left: 90, fontSize: 18, fontWeight: 800, letterSpacing: ".2em" }}>ATTENTION / 05</div>
      <svg viewBox="0 0 920 500" style={{ position: "absolute", width: 930, height: 505, left: 440, top: 230 }}>
        <path d={`M40 250 Q460 ${250 - 180 * blink} 880 250 Q460 ${250 + 180 * blink} 40 250Z`} fill="#fffaf0" stroke="#1d2b31" strokeWidth="12" />
        <circle cx={460 + pupilX} cy="250" r="135" fill="#e55c47" />
        <circle cx={460 + pupilX} cy="250" r="83" fill="#16242a" />
        <circle cx={430 + pupilX} cy="213" r="29" fill="#fff" />
      </svg>
      <div style={{ position: "absolute", left: 110, bottom: 90 }}>
        <Word size={190} color="#1d2b31" tracking={-0.1}>3.7%</Word>
        <div style={{ fontSize: 22, fontWeight: 800, letterSpacing: ".18em", marginTop: 22 }}>MAKE EVERY FRAME COUNT</div>
      </div>
      <div style={{ position: "absolute", right: 95, bottom: 110, fontSize: 16, fontWeight: 800, letterSpacing: ".16em", color: "#78868a" }}>A STUDY IN FOCUS</div>
    </AbsoluteFill>
  );
};

const frameBlink = (frame: number) => {
  const pulse = Math.sin(frame / 23);
  return Math.max(0.18, Math.min(1, 0.86 + pulse * 0.14));
};

const PosterReel = () => (
  <AbsoluteFill style={full}>
    <Sequence from={0} durationInFrames={42}><PosterFuture /></Sequence>
    <Sequence from={38} durationInFrames={40}><MindPoster /></Sequence>
    <Sequence from={74} durationInFrames={40}><CirclePoster /></Sequence>
    <Sequence from={110} durationInFrames={40}><EasePoster /></Sequence>
    <Sequence from={146} durationInFrames={35}><LinearPoster /></Sequence>
    <Sequence from={177} durationInFrames={25}><ClockPoster /></Sequence>
    <Sequence from={198} durationInFrames={21}><EyePoster /></Sequence>
  </AbsoluteFill>
);

const Chip = ({ label, color, index, frame }: { label: string; color: string; index: number; frame: number }) => {
  const { fps } = useVideoConfig();
  const p = spring({ frame: Math.max(0, frame - index * 3), fps, config: { damping: 13, stiffness: 115 } });
  const y = interpolate(p, [0, 1], [130, 0]);
  return (
    <div style={{ width: 94, height: 94, borderRadius: 30, background: color, display: "grid", placeItems: "center", color: "#fff", fontWeight: 900, fontSize: 31, boxShadow: "0 12px 24px rgba(25,30,45,.13)", transform: `translateY(${y}px) rotate(${(index % 2 ? -1 : 1) * (1 - p) * 24}deg)` }}>
      {label}
    </div>
  );
};

const ModelAgentScene = () => {
  const frame = useCurrentFrame();
  const second = frame > 65;
  const colors = ["#f3c7ad", "#c7d7f4", "#d4e7b0", "#d9c7e8", "#ecd6a1"];
  return (
    <AbsoluteFill style={{ ...full, background: "#f5f3ed" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5,1fr)", height: "100%", position: "absolute", inset: 0 }}>
        {colors.map((c, i) => <div key={i} style={{ background: c, opacity: 0.8, transform: `translateY(${Math.sin(frame / 23 + i) * 10}px)` }} />)}
      </div>
      <div style={{ position: "absolute", left: 95, top: 120, color: "#20242a", opacity: second ? 0 : 1, transform: `translateX(${interpolate(frame, [48, 68], [0, -180], clamp)}px)` }}>
        <Word size={185} color="#20242a">Any model.</Word>
        <div style={{ fontSize: 20, fontWeight: 800, letterSpacing: ".2em", marginTop: 30 }}>ONE CREATIVE CANVAS / MANY MODELS</div>
      </div>
      <div style={{ position: "absolute", left: 95, top: 120, color: "#20242a", opacity: second ? 1 : 0, transform: `translateX(${interpolate(frame, [62, 83], [170, 0], clamp)}px)` }}>
        <Word size={185} color="#20242a">Any agent.</Word>
        <div style={{ fontSize: 20, fontWeight: 800, letterSpacing: ".2em", marginTop: 30 }}>THE TOOLS YOU ALREADY TRUST</div>
      </div>
      <div style={{ position: "absolute", left: 112, right: 112, bottom: 190, display: "flex", gap: 26, justifyContent: "space-between", alignItems: "center" }}>
        {["A", "✳", "M", "✦", "◉", "G", "∞", "⌘", "✣", "N"].map((label, i) =>
          <Chip key={i} label={label} color={["#293d62", "#e95b43", "#34313b", "#6683b7", "#d88e64", "#485b48", "#5551a0", "#3e4247", "#e3a94d", "#4b7994"][i]} index={i} frame={frame} />
        )}
      </div>
      <div style={{ position: "absolute", left: 112, bottom: 93, right: 112, height: 4, background: "rgba(32,36,42,.16)" }}>
        <div style={{ height: 4, width: `${interpolate(frame, [0, 129], [0, 100], clamp)}%`, background: "#252a2f" }} />
      </div>
    </AbsoluteFill>
  );
};

const Toggle = ({ label, value }: { label: string; value: boolean }) => (
  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "18px 22px", borderRadius: 14, background: "#f6f7f6", marginBottom: 12 }}>
    <span style={{ fontSize: 20, color: "#4b5359", fontWeight: 600 }}>{label}</span>
    <div style={{ width: 52, height: 30, borderRadius: 30, padding: 3, boxSizing: "border-box", background: value ? "#6e9c72" : "#bfc6c7", display: "flex", justifyContent: value ? "flex-end" : "flex-start" }}>
      <div style={{ width: 24, height: 24, borderRadius: 30, background: "#fff" }} />
    </div>
  </div>
);

const WorkspaceScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 19, stiffness: 70 } });
  const leftX = interpolate(p, [0, 1], [-180, 0]);
  const rightY = interpolate(p, [0, 1], [160, 0]);
  const previews = [
    ["POSTER 01", "#293cb6", "THE FUTURE"],
    ["TYPE STUDY", "#b8ed4a", "EASE"],
    ["COLOR FIELD", "#e9b6ac", "MOTION"],
    ["3D OBJECT", "#d5dded", "FORM"],
  ];
  return (
    <AbsoluteFill style={{ ...full, background: "#edece6" }}>
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(circle at 65% 40%,#fff 0%,#edece6 67%)" }} />
      <div style={{ position: "absolute", top: 54, left: 80, right: 80, display: "flex", justifyContent: "space-between", alignItems: "center", color: "#22272d", fontSize: 17, fontWeight: 850, letterSpacing: ".16em" }}>
        <span>OPENDESIGN / CREATIVE WORKSPACE</span><span>PROJECT 014 · MOTION KIT</span>
      </div>
      <div style={{ position: "absolute", left: 88, top: 158, width: 660, height: 790, background: "#fff", borderRadius: 28, padding: 34, boxSizing: "border-box", boxShadow: "0 32px 80px rgba(26,35,46,.15)", transform: `translateX(${leftX}px) rotate(-1deg)` }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 34 }}>
          <div style={{ fontSize: 25, fontWeight: 900, color: "#20242a" }}>Motion workspace</div>
          <div style={{ borderRadius: 99, padding: "9px 18px", background: "#e8f6e4", color: "#4b7953", fontWeight: 800, fontSize: 14 }}>ALL SYSTEMS READY</div>
        </div>
        <div style={{ fontSize: 17, fontWeight: 800, color: "#9ba1a4", letterSpacing: ".13em", marginBottom: 14 }}>YOUR GENERATION</div>
        <div style={{ fontSize: 31, color: "#20242a", fontWeight: 800, lineHeight: 1.15, marginBottom: 28 }}>Product launch<br/> motion sequence</div>
        <Toggle label="Kinetic typography" value />
        <Toggle label="Depth & perspective" value />
        <Toggle label="Auto transitions" value />
        <Toggle label="Sound design" value />
        <div style={{ marginTop: 26, padding: 22, borderRadius: 18, background: "#f4f5f2" }}>
          <div style={{ display: "flex", justifyContent: "space-between", color: "#858d90", fontSize: 15, fontWeight: 800, marginBottom: 17 }}><span>RENDER PROGRESS</span><span>84%</span></div>
          <div style={{ height: 9, borderRadius: 20, background: "#dde2df", overflow: "hidden" }}><div style={{ width: "84%", height: "100%", background: "#8bbd5b", borderRadius: 20 }} /></div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 810, top: 175, right: 84, bottom: 110, display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 22, transform: `translateY(${rightY}px) scale(${interpolate(p, [0, 1], [.88, 1])})` }}>
        {previews.map(([tag, color, title], i) => (
          <div key={tag} style={{ borderRadius: 24, background: color, overflow: "hidden", position: "relative", boxShadow: "0 24px 55px rgba(35,43,52,.16)", padding: 25, boxSizing: "border-box", color: i === 1 ? "#182019" : i === 2 ? "#292026" : "#fff" }}>
            <div style={{ fontSize: 13, fontWeight: 900, letterSpacing: ".18em", opacity: .72 }}>{tag}</div>
            <div style={{ position: "absolute", left: 28, bottom: 45, fontSize: i === 0 ? 62 : 56, fontWeight: 950, letterSpacing: "-.08em", lineHeight: .85 }}>{title}</div>
            <div style={{ position: "absolute", right: 26, top: 40, width: 82, height: 82, border: "7px solid currentColor", borderRadius: "50%", opacity: .62, transform: `rotate(${frame * (i + 1) * 0.3}deg)` }} />
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", bottom: 53, left: 90, fontSize: 17, color: "#818887", fontWeight: 800, letterSpacing: ".18em" }}>ONE BRIEF. MANY MOTION SYSTEMS.</div>
    </AbsoluteFill>
  );
};

const CountdownNumber = ({ value, index }: { value: number; index: number }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame, fps, config: { damping: 12, stiffness: 85, mass: 0.9 } });
  const scale = interpolate(p, [0, 1], [2.2, 1]);
  const rotate = interpolate(p, [0, 1], [28, 0]);
  return (
    <AbsoluteFill style={{ ...full, background: "radial-gradient(circle at 50% 44%,#586fe1 0%,#252f95 57%,#111b53 100%)" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: "linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px)", backgroundSize: "80px 80px", opacity: .35, transform: `perspective(700px) rotateX(58deg) translateY(300px)` }} />
      <div style={{ position: "absolute", top: 78, left: 90, fontSize: 18, fontWeight: 800, letterSpacing: ".2em", color: "rgba(255,255,255,.68)" }}>MOTION / COUNTDOWN 0{index + 1}</div>
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", perspective: 900 }}>
        <div style={{ fontSize: 640, lineHeight: .8, fontWeight: 950, letterSpacing: "-.12em", color: "#e8ecff", transform: `rotateX(${rotate}deg) rotateY(${-rotate * .6}deg) scale(${scale})`, textShadow: "1px 1px 0 #aeb9ed, 3px 3px 0 #7f8ddd, 6px 6px 0 #5264c2, 10px 10px 0 #263a91, 22px 25px 55px rgba(0,0,0,.38)" }}>{value}</div>
      </div>
      <div style={{ position: "absolute", bottom: 86, left: 90, fontSize: 17, color: "#dce2ff", fontWeight: 800, letterSpacing: ".18em" }}>MAKE THE MOMENT MOVE</div>
    </AbsoluteFill>
  );
};

const Cube = ({
  size,
  x,
  y,
  delay,
  frame,
  colour,
  symbol,
}: {
  size: number;
  x: number;
  y: number;
  delay: number;
  frame: number;
  colour: string;
  symbol: "play" | "window" | "spark";
}) => {
  const local = Math.max(0, frame - delay);
  const rotY = local * 1.1 + delay * 0.8;
  const rotX = local * 0.65 + delay * 0.35;
  const faceStyle: React.CSSProperties = {
    position: "absolute",
    inset: 0,
    borderRadius: size * 0.15,
    border: "1px solid rgba(255,255,255,.26)",
    display: "grid",
    placeItems: "center",
    backfaceVisibility: "hidden",
    background: `linear-gradient(145deg,${colour},#243b91)`,
    boxShadow: "inset 0 1px 0 rgba(255,255,255,.38)",
  };
  const glyph = (which: string) => which === "play"
    ? <svg viewBox="0 0 100 100" width="48%" height="48%"><path d="M31 18 Q25 15 25 26 V74 Q25 85 36 79 L80 54 Q91 48 80 42Z" fill="#fff" /></svg>
    : which === "window"
      ? <svg viewBox="0 0 100 100" width="52%" height="52%"><rect x="18" y="18" width="64" height="64" rx="11" fill="none" stroke="#fff" strokeWidth="8"/><path d="M18 42 H82 M42 18 V82" stroke="#fff" strokeWidth="7"/></svg>
      : <svg viewBox="0 0 100 100" width="50%" height="50%"><path d="M50 4 L61 38 L96 50 L61 62 L50 96 L39 62 L4 50 L39 38Z" fill="#fff"/></svg>;
  const half = size / 2;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: size, height: size, perspective: 1200, transform: `translateY(${Math.sin((frame + delay) / 20) * 22}px)` }}>
      <div style={{ position: "absolute", inset: 0, transformStyle: "preserve-3d", transform: `translateZ(-${half}px) rotateX(${rotX}deg) rotateY(${rotY}deg)`, filter: "drop-shadow(0 35px 24px rgba(14,22,54,.28))" }}>
        <div style={{ ...faceStyle, transform: `translateZ(${half}px)` }}>{glyph(symbol)}</div>
        <div style={{ ...faceStyle, transform: `rotateY(180deg) translateZ(${half}px)`, filter: "brightness(.68)" }}>{glyph("spark")}</div>
        <div style={{ ...faceStyle, transform: `rotateY(90deg) translateZ(${half}px)`, filter: "brightness(.86)" }}>{glyph("window")}</div>
        <div style={{ ...faceStyle, transform: `rotateY(-90deg) translateZ(${half}px)`, filter: "brightness(.76)" }}>{glyph("play")}</div>
        <div style={{ ...faceStyle, transform: `rotateX(90deg) translateZ(${half}px)`, filter: "brightness(.62)" }}>{glyph("spark")}</div>
        <div style={{ ...faceStyle, transform: `rotateX(-90deg) translateZ(${half}px)`, filter: "brightness(.9)" }}>{glyph("window")}</div>
      </div>
    </div>
  );
};

const CubeEnding = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logo = spring({ frame: Math.max(0, frame - 8), fps, config: { damping: 18, stiffness: 78 } });
  const y = interpolate(logo, [0, 1], [140, 0]);
  const alpha = ease(frame, 12, 24);
  return (
    <AbsoluteFill style={{ ...full, background: "radial-gradient(ellipse at 50% 42%,#e7ecff 0%,#b8c7ec 42%,#7c91ca 100%)" }}>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(130deg,rgba(255,255,255,.38),transparent 44%,rgba(34,53,120,.2))" }} />
      <Cube size={248} x={320} y={220} delay={0} frame={frame} colour="#5a79d7" symbol="play" />
      <Cube size={300} x={810} y={135} delay={7} frame={frame} colour="#4560c2" symbol="window" />
      <Cube size={220} x={1330} y={265} delay={13} frame={frame} colour="#7b8de1" symbol="spark" />
      <Cube size={180} x={570} y={650} delay={18} frame={frame} colour="#344ea7" symbol="window" />
      <Cube size={260} x={1120} y={650} delay={22} frame={frame} colour="#6883dd" symbol="play" />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 90, display: "flex", alignItems: "center", justifyContent: "center", gap: 28, opacity: alpha, transform: `translateY(${y}px)` }}>
        <div style={{ width: 108, height: 108, borderRadius: 32, background: "linear-gradient(145deg,#2446b9,#5878e8)", display: "grid", placeItems: "center", boxShadow: "0 20px 40px rgba(28,43,112,.25)", transform: `scale(${logo})` }}>
          <svg viewBox="0 0 100 100" width="62" height="62"><path d="M32 17 Q24 13 24 28 V72 Q24 86 37 78 L81 54 Q92 48 81 42Z" fill="#fff"/></svg>
        </div>
        <div>
          <div style={{ fontSize: 76, fontWeight: 950, color: "#1c2f68", letterSpacing: "-.07em", lineHeight: .9 }}>OpenDesign <span style={{ color: "#fff" }}>Motion</span></div>
          <div style={{ fontSize: 18, marginTop: 18, color: "#3d5285", fontWeight: 800, letterSpacing: ".22em" }}>MAKE EVERY FRAME MOVE</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const OpenDesignMotion: React.FC = () => (
  <AbsoluteFill style={{ ...full, backgroundColor: "#101319" }}>
    <Sequence from={0} durationInFrames={204}><SkyIntro /></Sequence>
    <Sequence from={204} durationInFrames={90}><TitleScene /></Sequence>
    <Sequence from={294} durationInFrames={81}><ClaimScene /></Sequence>
    <Sequence from={375} durationInFrames={81}><GalleryScene /></Sequence>
    <Sequence from={456} durationInFrames={219}><PosterReel /></Sequence>
    <Sequence from={675} durationInFrames={129}><ModelAgentScene /></Sequence>
    <Sequence from={804} durationInFrames={105}><WorkspaceScene /></Sequence>
    <Sequence from={909} durationInFrames={111}>
      <AbsoluteFill style={full}>
        <Sequence from={0} durationInFrames={37}><CountdownNumber value={3} index={0} /></Sequence>
        <Sequence from={37} durationInFrames={37}><CountdownNumber value={2} index={1} /></Sequence>
        <Sequence from={74} durationInFrames={37}><CountdownNumber value={1} index={2} /></Sequence>
      </AbsoluteFill>
    </Sequence>
    <Sequence from={1020} durationInFrames={99}><CubeEnding /></Sequence>
    <Audio src={staticFile("audio/opendesign-motion-score.wav")} volume={0.82} />
  </AbsoluteFill>
);
