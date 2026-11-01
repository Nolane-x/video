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
 const common:React.CSSProperties={position:"absolute",inset:0,overflow:"hidden"};
 const Char=({x=0,y=0,scale=1}:{x?:number;y?:number;scale?:number})=><svg viewBox="0 0 160 170" width="130" height="138" style={{position:"absolute",right:x,bottom:y,transform:"scale("+scale+")",transformOrigin:"bottom right"}}>
  <ellipse cx="81" cy="160" rx="49" ry="7" fill="rgba(0,0,0,.12)"/>
  <path d="M40 158Q34 119 53 96Q80 77 109 98Q128 124 121 158Z" fill="#e8e8e3" stroke="#202326" strokeWidth="2"/>
  <path d="M54 43Q53 10 80 9Q108 7 114 40L125 66Q139 57 146 75Q151 94 126 101L116 124H47L34 99Q13 102 13 80Q13 62 34 66Z" fill="#d6d7d5" stroke="#25282a" strokeWidth="2"/>
  <path d="M42 47Q46 13 82 16Q111 19 118 50L102 38L80 40L60 34Z" fill="#22272a"/>
  <circle cx="62" cy="77" r="5" fill="#17191b"/><circle cx="100" cy="77" r="5" fill="#17191b"/>
  <ellipse cx="81" cy="93" rx="9" ry="11" fill="#45494a"/>
  <path d="M69 108Q81 117 94 108" stroke="#44484a" strokeWidth="3" fill="none" strokeLinecap="round"/>
  <path d="M58 139L48 157M104 139L115 157" stroke="#777e80" strokeWidth="7" strokeLinecap="round"/>
 </svg>;
 if(index===0)return <div style={{...common,background:"radial-gradient(ellipse at 50% 38%,#5338a6,#20124c 65%,#090b1c)",color:"#fff"}}>
  <div style={{position:"absolute",inset:"60% -20% -25%",background:"repeating-linear-gradient(0deg,rgba(127,90,249,.45) 0 1px,transparent 1px 17px),repeating-linear-gradient(90deg,rgba(127,90,249,.4) 0 1px,transparent 1px 24px)",transform:"perspective(180px) rotateX(58deg)"}}/>
  <div style={{position:"absolute",inset:"0 0 0",background:"radial-gradient(ellipse at 50% 85%,transparent 0 30%,rgba(13,8,43,.3) 70%)"}}/>
  <div style={{position:"absolute",left:14,top:28,fontSize:11,fontWeight:900,letterSpacing:".2em"}}>MOTION STUDY / 02</div>
  <Word size={52} color="#fff" style={{position:"absolute",left:18,bottom:20,textShadow:"0 3px 12px #000"}}>20</Word>
  <Word size={52} color="#fff" style={{position:"absolute",right:18,bottom:20,textShadow:"0 3px 12px #000"}}>10</Word>
  <div style={{position:"absolute",left:"50%",top:"46%",width:64,height:64,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"#f3e6ff",border:"3px solid rgba(255,255,255,.8)",display:"grid",placeItems:"center",boxShadow:"0 0 20px #d2a5ff"}}><PlayGlyph size={38} color="#5532ab"/></div>
  <div style={{position:"absolute",left:30,top:75,width:2,height:45,background:"#b9a4fb"}}/><div style={{position:"absolute",right:30,top:75,width:2,height:45,background:"#b9a4fb"}}/>
 </div>;
 if(index===1)return <div style={{...common,background:"#030508",color:"#fff"}}>
  <div style={{position:"absolute",left:0,right:0,top:0,bottom:0,background:"radial-gradient(ellipse at 50% 45%,rgba(40,76,255,.22),transparent 68%)"}}/>
  <svg viewBox="0 0 320 180" width="100%" height="100%"><g transform={"translate(165 86) rotateY("+Math.sin(frame/9)*9+"deg)"}><path d="M-62 -45L54 -54L54 55L-62 46Z" fill="#1738c8" stroke="#496bff" strokeWidth="3"/><path d="M-62 -45L-26 -70L87 -70L54 -54Z" fill="#3157ff"/><path d="M54 -54L87 -70L87 39L54 55Z" fill="#10207c"/><path d="M-62 -45L-26 -70L-26 37L-62 46Z" fill="#07114b" stroke="#3d63fa" strokeWidth="2"/></g><path d="M165 20V150M55 86H267" stroke="#2244be" strokeWidth="1" opacity=".3"/></svg>
  <div style={{position:"absolute",left:10,top:7,fontSize:9,color:"#aab9ff",letterSpacing:".18em"}}>VOLUMETRIC / CUBE</div>
 </div>;
 if(index===2)return <div style={{...common,background:"linear-gradient(135deg,#d3f3e8,#f2f9ed 55%,#8fcfc2)"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,transparent 0 60%,rgba(84,182,166,.2) 100%)"}}/>
  <div style={{position:"absolute",right:12,top:12,width:118,height:113,background:"#fff",borderRadius:5,boxShadow:"0 5px 15px rgba(0,0,0,.1)",padding:"9px",boxSizing:"border-box"}}>
   <div style={{fontSize:8,color:"#4b5b5a",fontWeight:800}}>Growth / Report</div>
   <svg viewBox="0 0 120 82" width="100%" height="78"><path d="M3 73H116M3 52H116M3 31H116M3 10H116" stroke="#e6eeeb" strokeWidth="1"/><path d="M4 68C20 63 30 58 42 50S70 39 79 23S99 16 114 5" stroke="#4fa98d" strokeWidth="3" fill="none"/><path d="M4 68C20 63 30 58 42 50S70 39 79 23S99 16 114 5V80H4Z" fill="#93dfc0" opacity=".26"/></svg>
  </div>
  <div style={{position:"absolute",left:-20,bottom:-12,width:160,height:50,background:"#75cbbb",borderRadius:"50%"}}/><div style={{position:"absolute",left:25,bottom:24,width:130,height:24,background:"#cae6d7",filter:"blur(9px)"}}/>
 </div>;
 if(index===3)return <div style={{...common,background:"#f4f3f0",display:"grid",placeItems:"center"}}>
  <div style={{width:136,height:48,borderRadius:9,background:"#11161a",display:"flex",alignItems:"center",padding:"0 10px",gap:9,boxShadow:"0 4px 10px rgba(0,0,0,.17)"}}>
   <div style={{width:22,height:22,borderRadius:5,background:"linear-gradient(135deg,#f4c64a,#e76e61,#a37ae8)"}}/>
   <div style={{fontSize:9,color:"#fff",fontWeight:750,flex:1}}>motion study 02</div>
   <div style={{display:"flex",gap:3,alignItems:"center"}}><span style={{fontSize:9,color:"#fff"}}>◀</span><span style={{fontSize:10,color:"#fff"}}>Ⅱ</span><span style={{fontSize:9,color:"#fff"}}>▶</span></div>
  </div>
 </div>;
 if(index===4)return <div style={{...common,background:"#fff",color:"#17191c"}}>
  <div style={{position:"absolute",left:16,top:25,fontSize:26,fontWeight:600,letterSpacing:"-.04em"}}>Got something</div>
  <Char x={4} y={-3} scale={.86}/>
 </div>;
 if(index===5)return <div style={{...common,background:"linear-gradient(130deg,#d8f4e7,#bce6d8 60%,#8bc9ba)"}}>
  <Word size={64} color="#121817" style={{position:"absolute",left:10,top:24}}>100K</Word>
  <div style={{position:"absolute",right:9,top:25,width:111,height:78,background:"#fff",borderRadius:4,boxShadow:"0 4px 12px rgba(0,0,0,.1)",padding:7,boxSizing:"border-box"}}>
   <div style={{fontSize:8,fontWeight:800,color:"#252b2c"}}>nexu-io / open-design</div><div style={{fontSize:7,color:"#75807f",marginTop:4}}>✦ stars / 100K</div><div style={{height:4,background:"#e9efec",marginTop:8}}/><div style={{height:4,width:"70%",background:"#7dcda7",marginTop:5}}/>
  </div>
 </div>;
 if(index===6)return <div style={{...common,background:"#dfd2ad"}}>
  <div style={{position:"absolute",inset:0,background:"repeating-linear-gradient(90deg,rgba(108,75,37,.08) 0 1px,transparent 2px 12px)"}}/>
  <div style={{position:"absolute",left:12,top:9,right:12,bottom:9,background:"#f2e4c2",border:"2px solid #29241d",padding:9,boxSizing:"border-box",boxShadow:"inset 0 0 0 2px #b5945b"}}>
   <div style={{display:"flex",justifyContent:"space-between",fontSize:7,fontFamily:"Georgia,serif",color:"#2d2a25"}}><span>1,350 BC</span><span>ANCIENT TIME</span></div>
   <div style={{position:"absolute",left:"50%",top:"55%",width:70,height:70,transform:"translate(-50%,-50%)",borderRadius:"50%",border:"7px solid #be9b4d",background:"#dfc784",boxShadow:"inset 0 0 0 4px #f1e0a8"}}>
    <div style={{position:"absolute",left:"50%",top:"50%",width:5,height:28,background:"#171817",transform:"translate(-50%,-100%) rotate(18deg)",transformOrigin:"bottom"}}/><div style={{position:"absolute",left:"50%",top:"50%",width:25,height:4,background:"#171817",transform:"translateY(-50%) rotate(-10deg)"}}/>
   </div>
   <div style={{position:"absolute",left:8,right:8,bottom:6,fontSize:7,textAlign:"center",color:"#65502b"}}>SOLAR OBSERVATION / ASTRONOMY</div>
  </div>
 </div>;
 if(index===7)return <div style={{...common,background:"#050710"}}>
  <svg viewBox="0 0 260 148" width="100%" height="100%"><defs><radialGradient id="galeye"><stop offset="0" stopColor="#f7f5ff"/><stop offset=".25" stopColor="#8d86ff"/><stop offset=".6" stopColor="#2535aa"/><stop offset="1" stopColor="#070b24"/></radialGradient></defs><path d="M12 74Q130 -30 248 74Q130 178 12 74Z" fill="#171956" stroke="#8a8eff" strokeWidth="3"/><ellipse cx="130" cy="74" rx="91" ry="48" fill="#312bd5"/><ellipse cx="130" cy="74" rx="42" ry="42" fill="url(#galeye)" stroke="#aaaaff" strokeWidth="3"/><circle cx="130" cy="74" r="18" fill="#070910"/><circle cx="119" cy="62" r="7" fill="#fff"/><path d="M130 28V13M130 135V120" stroke="#fff" strokeWidth="2"/></svg>
  <div style={{position:"absolute",right:10,bottom:8,fontSize:10,color:"#fff"}}>5.7%</div>
 </div>;
 if(index===8)return <div style={{...common,background:"#82ef45",color:"#101710"}}>
  <div style={{position:"absolute",left:12,top:10,fontSize:7,color:"#24441b",letterSpacing:".2em"}}>OPEN DESIGN / MOTION DESIGN</div>
  <Word size={56} color="#101710" style={{position:"absolute",left:12,top:43,lineHeight:.86}}>OPEN<br/>DESIGN</Word>
  <div style={{position:"absolute",left:12,bottom:9,fontFamily:"Georgia,serif",fontSize:12,fontStyle:"italic",color:"#255421"}}>motion design</div>
 </div>;
 if(index===9)return <div style={{...common,background:"#fff",display:"grid",placeItems:"center"}}>
  <div style={{width:110,height:44,borderRadius:30,background:"#eeefee",boxShadow:"inset 0 2px 5px rgba(0,0,0,.12)",padding:4,boxSizing:"border-box"}}><div style={{width:36,height:36,borderRadius:"50%",background:"#fff",boxShadow:"0 2px 6px rgba(0,0,0,.12)",transform:"translateX("+(frame%24>12?64:0)+"px)"}}/></div>
 </div>;
 if(index===10)return <div style={{...common,background:"#2876db"}}>
  <Char x={88} y={-8} scale={.78}/>
  <div style={{position:"absolute",right:12,top:19,width:55,height:83,background:"#edf1fc",transform:"rotate(8deg)",boxShadow:"0 3px 7px rgba(0,0,0,.15)",display:"grid",placeItems:"center"}}>
   <svg viewBox="0 0 80 80" width="43" height="43"><path d="M40 6L73 26L40 47L7 26Z" fill="#111827"/><path d="M7 26L40 47V75L7 55Z" fill="#526da8"/><path d="M73 26L40 47V75L73 55Z" fill="#273d71"/></svg>
   <div style={{fontSize:7,color:"#333"}}>Courses</div>
  </div>
 </div>;
 if(index===11)return <div style={{...common,background:"#d8b98d"}}>
  <div style={{position:"absolute",inset:0,background:"repeating-linear-gradient(90deg,rgba(102,70,34,.08) 0 2px,transparent 2px 11px),repeating-linear-gradient(0deg,rgba(102,70,34,.04) 0 2px,transparent 3px 14px)"}}/>
  <div style={{position:"absolute",left:52,top:27,width:152,height:91,background:"#fffdf4",border:"1px solid #e0d8c5",boxShadow:"0 3px 8px rgba(73,48,20,.16)",transform:"rotate(-1deg)",display:"grid",placeItems:"center"}}>
   <div style={{fontFamily:"Georgia,serif",fontSize:16,color:"#405c7d",borderBottom:"1px solid #bfc7cf",padding:6}}>OpenDesign</div>
  </div>
  <div style={{position:"absolute",right:28,top:35,width:10,height:118,background:"#54aa82",borderRadius:5,transform:"rotate(18deg)",transformOrigin:"top",boxShadow:"3px 2px 0 #d8dfc8"}}/>
  <div style={{position:"absolute",right:17,bottom:12,width:25,height:25,background:"#e0b14a",borderRadius:"50%"}}/>
 </div>;
 if(index===12)return <div style={{...common,background:"#172d7d"}}>
  <svg viewBox="0 0 263 148" width="100%" height="100%"><defs><pattern id="stars1889" width="32" height="27" patternUnits="userSpaceOnUse"><circle cx="5" cy="8" r="1.5" fill="#b4bce9"/><circle cx="23" cy="20" r="1" fill="#d9dced"/></pattern></defs><rect width="263" height="148" fill="url(#stars1889)"/><circle cx="133" cy="73" r="51" fill="#d9b95a" stroke="#f4dd87" strokeWidth="7"/><circle cx="133" cy="73" r="41" fill="#16286e" stroke="#9e7b36" strokeWidth="5"/><path d="M135 51L165 75L135 83Z" fill="#f6d365"/><path d="M38 130L56 83L72 130M194 134L211 89L227 134" stroke="#1a623b" strokeWidth="12" fill="#174b31"/><text x="132" y="17" fill="#e8d38a" fontSize="10" textAnchor="middle">1889</text></svg>
 </div>;
 if(index===13)return <div style={{...common,background:"#1438d5",color:"#fff"}}>
  <div style={{position:"absolute",left:12,top:9,fontSize:8,letterSpacing:".15em"}}>01 / THE NEW ERA</div>
  <Word size={56} color="#fff" style={{position:"absolute",left:10,top:36,lineHeight:.86}}>THE<br/>FUTURE</Word>
  <div style={{position:"absolute",right:10,bottom:10,fontSize:9,fontWeight:900}}>MOTION / 2026</div>
  <div style={{position:"absolute",right:20,top:10,width:40,height:40,border:"2px solid #fff"}}/>
 </div>;
 if(index===14)return <div style={{...common,background:"#fff",color:"#111315",display:"grid",placeItems:"center"}}>
  <div style={{textAlign:"center",fontSize:20,fontWeight:700,lineHeight:1.04}}>The <span style={{background:"#9ff05b"}}>open-source</span><br/>alternative<br/><small style={{fontSize:9,color:"#777"}}>to ✳ Claude Motion.</small></div>
 </div>;
 if(index===15)return <div style={{...common,background:"#fff",display:"grid",placeItems:"center"}}>
  <div style={{width:150,height:22,borderRadius:20,background:"#fff",border:"1px solid #e9e9e9",boxShadow:"0 3px 8px rgba(0,0,0,.09)"}}/>
 </div>;
 if(index===16)return <div style={{...common,background:"#2876db"}}>
  <Char x={78} y={-8} scale={.78}/>
  <div style={{position:"absolute",right:14,top:30,width:72,height:78,background:"#fff",borderRadius:2,display:"grid",placeItems:"center",boxShadow:"0 4px 8px rgba(0,0,0,.15)"}}>
   <svg viewBox="0 0 80 75" width="56" height="52"><path d="M40 6L73 26L40 47L7 26Z" fill="#111827"/><path d="M7 26L40 47V70L7 52Z" fill="#526da8"/><path d="M73 26L40 47V70L73 52Z" fill="#273d71"/></svg>
   <div style={{fontSize:7,color:"#333"}}>Courses</div>
  </div>
 </div>;
 if(index===17)return <div style={{...common,background:"linear-gradient(140deg,#151d50,#09112c)",color:"#fff"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(circle at 22% 20%,#6c74c9 0 1px,transparent 2px),radial-gradient(circle at 70% 70%,#8a9aff 0 1px,transparent 2px)",backgroundSize:"30px 27px"}}/>
  <div style={{position:"absolute",right:38,top:31,width:64,height:70,borderRadius:"50% 50% 42% 42%",border:"4px solid #e9ecfa",background:"#121b47",display:"grid",placeItems:"center",fontSize:31}}>◉</div>
  <div style={{position:"absolute",left:13,top:31,fontSize:13,fontWeight:700}}>What if you could<br/>design?</div>
  <div style={{position:"absolute",left:15,bottom:13,fontSize:7,color:"#aab2e6"}}>A little wonder, out there.</div>
 </div>;
 if(index===18)return <div style={{...common,background:"#efe6d2",color:"#17191b"}}>
  <div style={{position:"absolute",inset:0,background:"repeating-linear-gradient(0deg,rgba(110,81,45,.05) 0 1px,transparent 1px 9px)"}}/>
  <div style={{position:"absolute",left:16,top:22,fontFamily:"Georgia,serif",fontSize:11}}>1923 / THE FUTURE</div>
  <div style={{position:"absolute",left:17,top:51,fontFamily:displayFont,fontSize:33,fontWeight:950,lineHeight:.88}}>open<br/>design</div>
  <div style={{position:"absolute",left:80,top:30,width:66,height:66,borderRadius:"50%",border:"7px solid #e64b45",display:"grid",placeItems:"center",color:"#111",fontSize:34}}>➤</div>
  <div style={{position:"absolute",left:0,right:0,bottom:22,height:7,background:"#111"}}/><div style={{position:"absolute",left:0,bottom:16,width:163,height:3,background:"#111",transform:"rotate(-9deg)"}}/>
  <div style={{position:"absolute",right:13,bottom:9,width:34,height:20,background:"#3658aa"}}/>
 </div>;
 if(index===19)return <div style={{...common,background:"#050609",color:"#fff"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(100deg,#fff 0 50%,#101216 50% 100%)",opacity:.96}}/>
  <div style={{position:"absolute",left:12,top:10,fontSize:8,color:"#111"}}>1923</div>
  <Word size={48} color="#111" style={{position:"absolute",left:9,top:31}}>NOW</Word>
  <Word size={37} color="#fff" style={{position:"absolute",right:5,top:50}}>FUTURE</Word>
  <div style={{position:"absolute",left:10,bottom:9,fontSize:8,color:"#111"}}>49%</div>
  <div style={{position:"absolute",right:10,bottom:9,fontSize:8,color:"#fff"}}>2026</div>
 </div>;
 if(index===20||index===21||index===27)return <div style={{...common,background:"#fff",color:"#373d40"}}>
  <div style={{position:"absolute",left:14,top:12,fontSize:8,fontWeight:850}}>The ways we grow from A to B.</div>
  {Array.from({length:index===20?5:4},(_,i)=><div key={i} style={{position:"absolute",left:15,right:15,top:39+i*20,height:1,background:"#e7e9e7"}}/>)}
  {Array.from({length:index===20?5:4},(_,i)=><div key={i} style={{position:"absolute",right:20,top:34+i*20,width:9,height:9,borderRadius:"50%",background:"#77c78e",boxShadow:"0 0 0 2px #e6f7e9"}}/>)}
  <div style={{position:"absolute",left:15,bottom:9,fontSize:7,color:"#858b8b"}}>Ideas / systems / delivery</div>
 </div>;
 if(index===22||index===28)return <div style={{...common,background:"#07090e",color:"#fff"}}>
  <div style={{position:"absolute",left:15,top:48,fontFamily:"Georgia,serif",fontSize:18}}>You create.</div>
  <div style={{position:"absolute",left:15,top:77,fontFamily:"Georgia,serif",fontSize:16,color:"#ccd0d3"}}>We handle the rest.</div>
  <Char x={3} y={-5} scale={.75}/>
 </div>;
 if(index===23)return <div style={{...common,background:"#e0f3e7",color:"#293a35"}}>
  <div style={{position:"absolute",left:13,top:9,fontSize:8,letterSpacing:".1em"}}>WEB / PORTFOLIO</div>
  <div style={{position:"absolute",left:44,top:29,width:144,height:85,background:"#fff4e0",boxShadow:"0 3px 8px rgba(0,0,0,.09)",padding:8,boxSizing:"border-box",transform:"rotate(-2deg)"}}>
   <div style={{fontFamily:"Georgia,serif",fontSize:14}}>a little<br/>wonder.</div><div style={{position:"absolute",right:13,top:25,width:22,height:33,background:"#e9886a"}}/>
  </div>
  <div style={{position:"absolute",left:0,right:0,bottom:9,textAlign:"center",fontSize:11,fontWeight:900}}>websites</div>
  <div style={{position:"absolute",right:13,bottom:25,width:31,height:24,borderRadius:7,background:"#101316",color:"#fff",display:"grid",placeItems:"center",fontSize:9}}>◉</div>
 </div>;
 if(index===24)return <div style={{...common,background:"#03050a",color:"#fff"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(circle at 55% 52%,#161a25,transparent 65%)"}}/>
  <Word size={52} color="#161b27" style={{position:"absolute",left:5,bottom:-3}}>1973</Word>
  <div style={{position:"absolute",left:29,top:"48%",height:3,width:210,background:"linear-gradient(90deg,#fff,transparent)"}}/>
  <div style={{position:"absolute",left:"50%",top:"50%",width:53,height:53,borderRadius:12,background:"#0b0d12",border:"2px solid #e4e6f2",transform:"translate(-50%,-50%)",boxShadow:"0 0 0 5px rgba(255,255,255,.12)"}}>
   <div style={{position:"absolute",left:52,top:12,width:130,height:4,background:"linear-gradient(90deg,#f5f8ff,#efb2f5,#ff8b6d,#57d9f5)",transform:"rotate(-12deg)",transformOrigin:"left"}}/>
   <div style={{position:"absolute",left:11,top:12,width:27,height:27,borderRadius:6,border:"2px solid #fff"}}/>
  </div>
 </div>;
 if(index===25)return <div style={{...common,background:"#fff"}}>
  <svg viewBox="0 0 263 148" width="100%" height="100%">{[63,52,41,30,19,9].map((r,i)=><circle key={r} cx="131" cy="74" r={r} fill="none" stroke="#08090b" strokeWidth={i===0?6:3}/>)}<text x="131" y="14" fontSize="13" fontWeight="900" textAnchor="middle" fill="#111">THE FUTURE IS HERE</text><text x="131" y="137" fontSize="12" fontWeight="900" textAnchor="middle" fill="#111">IS ALREADY HERE</text></svg>
 </div>;
 if(index===26)return <div style={{...common,background:"#080a0c"}}/>;
 if(index===29)return <div style={{...common,background:"#efa9c2",color:"#17191b"}}>
  <div style={{position:"absolute",left:54,top:20,width:138,height:106,background:"#fff2d7",boxShadow:"0 4px 10px rgba(0,0,0,.14)",transform:"rotate(3deg)",padding:8,boxSizing:"border-box"}}>
   <div style={{fontSize:11,fontWeight:950}}>MAKE</div><div style={{fontFamily:"Georgia,serif",fontSize:12}}>something</div>
   <div style={{position:"absolute",left:35,top:43,fontSize:42,color:"#df8b5e"}}>✿</div>
   <div style={{position:"absolute",bottom:8,right:9,fontSize:9}}>wonderful.</div>
  </div>
  <div style={{position:"absolute",left:0,right:0,bottom:7,textAlign:"center",fontSize:12,fontWeight:900}}>posters</div>
  <div style={{position:"absolute",right:24,bottom:25,width:34,height:25,borderRadius:7,background:"#111",color:"#fff",display:"grid",placeItems:"center",fontSize:9}}>◉</div>
 </div>;
 return <div style={{...common,background:"#090b10",color:"#fff"}}><Word size={44} color="#fff" style={{position:"absolute",left:12,top:45}}>MOTION</Word></div>;
};

const GalleryCard=({index,frame}:{index:number;frame:number})=>{
 const drift=Math.sin((frame+index*11)/19)*2.8;
 const rotation=(index%2?-1:1)*.18;
 return <div style={{width:263,height:148,borderRadius:5,position:"relative",overflow:"hidden",transform:"translateY("+drift+"px) rotate("+rotation+"deg)",boxShadow:"0 6px 18px rgba(19,24,32,.12)",background:"#fff"}}>
  <GalleryPoster index={index%23} frame={frame+index*2}/>
 </div>;
};

const GalleryWall=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,72,16);
 const pan=e(f,0,77,5,-34),ry=e(f,0,77,-1.5,-7),rz=e(f,0,77,.15,-.45);
 const order=Array.from({length:30},(_,i)=>i);
 return <AbsoluteFill style={{...full,background:"#f3f1e9",overflow:"hidden"}}>
  <div style={{position:"absolute",left:78,right:78,top:76,bottom:58,display:"grid",gridTemplateColumns:"repeat(6,263px)",gridTemplateRows:"repeat(5,148px)",gap:13,justifyContent:"center",alignContent:"center",transform:"perspective(1750px) rotateY("+ry+"deg) rotateX(1.5deg) rotateZ("+rz+"deg) translateX("+pan+"px) translateY("+((1-p)*40)+"px) scale("+(0.965+.035*p)+")",transformOrigin:"center center"}}>
   {order.map((id,i)=><GalleryCard key={i} index={id} frame={f+i*2}/>)}
  </div>
  <div style={{position:"absolute",inset:0,pointerEvents:"none",background:"linear-gradient(180deg,rgba(255,255,255,.18),transparent 14%,transparent 85%,rgba(210,205,193,.12))"}}/>
  <Noise opacity={.025}/>
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
 const f=useCurrentFrame(),rot=10+f*.9;
 return <AbsoluteFill style={{...full,background:"#1b2be7",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 52% 48%,#3654ff,#1928d7 72%)"}}/>
  <div style={{position:"absolute",inset:-50,display:"flex",flexDirection:"column",justifyContent:"space-around",transform:"translateX("+Math.sin(f/6)*16+"px)"}}>
   {Array.from({length:5},(_,i)=><div key={i} style={{whiteSpace:"nowrap",fontFamily:displayFont,fontSize:230,fontWeight:950,letterSpacing:"-.11em",color:i%2===0?"#070a29":"transparent",WebkitTextStroke:i%2===0?"0":"2px rgba(6,10,36,.8)"}}>MIND / MIND / MIND</div>)}
  </div>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><linearGradient id="opd-mind-glass" x1="0" x2="1" y1="0" y2="1"><stop offset="0%" stopColor="#fff" stopOpacity=".85"/><stop offset="42%" stopColor="#b1d7ff" stopOpacity=".42"/><stop offset="100%" stopColor="#f5aaff" stopOpacity=".36"/></linearGradient></defs>
   <g transform={"translate(960 545) rotate("+rot+")"}>
    <path d="M0 -330L275 -120L210 235L-90 315L-300 60Z" fill="url(#opd-mind-glass)" stroke="#dceaff" strokeWidth="5"/>
    <path d="M0 -330L-90 315L-300 60Z" fill="#c4e8ff" opacity=".3"/><path d="M0 -330L275 -120L210 235Z" fill="#fff" opacity=".24"/>
    <path d="M-300 60L275 -120M-90 315L275 -120" stroke="#fff" strokeWidth="4" opacity=".72"/>
    <path d="M-90 315L210 235L0 -330" fill="none" stroke="#eef7ff" strokeWidth="2" opacity=".65"/>
   </g>
   {Array.from({length:14},(_,i)=>{const a=i*Math.PI*2/14;const x=960+Math.cos(a)*390,y=545+Math.sin(a)*290;return <g key={i}><circle cx={x} cy={y} r={i%3===0?13:8} fill="#fff" opacity=".94"/><circle cx={x} cy={y} r="24" fill="none" stroke="#e5eeff" strokeOpacity=".25" strokeWidth="2"/></g>;})}
  </svg>
  <div style={{position:"absolute",left:42,bottom:36,color:"#fff",fontSize:20,fontWeight:950,letterSpacing:".13em"}}>MIND / MATERIAL / MOTION</div>
  <div style={{position:"absolute",right:48,top:34,color:"#fff",fontSize:15,fontWeight:850,letterSpacing:".15em"}}>FTH/2B26 — THE FUTURE IS ALREADY HERE</div>
  <div style={{position:"absolute",right:64,top:140,width:310,height:108,border:"1px solid rgba(255,255,255,.7)",background:"rgba(6,10,32,.72)",color:"#eef4ff",padding:14,boxSizing:"border-box",fontSize:13,fontFamily:"monospace",lineHeight:1.65}}>SPEC / 4K28<br/>MATERIAL / GLASS<br/>IOR / 1.48</div>
 </AbsoluteFill>;
};

const RingPoster = () => {
 const f=useCurrentFrame();
 return <AbsoluteFill style={{...full,background:"#030304",color:"#fff"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0,transform:"rotate("+(f*.15)+"deg)"}}>
   <defs>
    <path id="od-ring-a" d="M960 540m-640 0a640 640 0 1 1 1280 0a640 640 0 1 1 -1280 0"/>
    <path id="od-ring-b" d="M960 540m-520 0a520 520 0 1 1 1040 0a1040 1040 0 1 1 -1040 0"/>
    <path id="od-ring-c" d="M960 540m-405 0a405 405 0 1 1 810 0a810 810 0 1 1 -810 0"/>
    <path id="od-ring-d" d="M960 540m-293 0a293 293 0 1 1 586 0a586 586 0 1 1 -586 0"/>
    <path id="od-ring-e" d="M960 540m-183 0a183 183 0 1 1 366 0a366 366 0 1 1 -366 0"/>
   </defs>
   {[640,520,405,293,183].map((r,i)=><circle key={r} cx="960" cy="540" r={r} fill="none" stroke="#f4f4f2" strokeWidth={i===0?8:4}/>)}
   <text fill="#fff" fontSize="81" fontWeight="950" letterSpacing="6"><textPath href="#od-ring-a">THE FUTURE IS ALREADY HERE · THE FUTURE IS ALREADY HERE ·</textPath></text>
   <text fill="#fff" fontSize="68" fontWeight="950" letterSpacing="5"><textPath href="#od-ring-b">THE FUTURE IS HERE · THE FUTURE IS HERE ·</textPath></text>
   <text fill="#fff" fontSize="56" fontWeight="950" letterSpacing="4"><textPath href="#od-ring-c">THE FUTURE · THE FUTURE · THE FUTURE · THE FUTURE ·</textPath></text>
   <text fill="#fff" fontSize="43" fontWeight="900" letterSpacing="3"><textPath href="#od-ring-d">IS ALREADY HERE · IS ALREADY HERE · IS ALREADY HERE ·</textPath></text>
   <text fill="#fff" fontSize="31" fontWeight="900" letterSpacing="2"><textPath href="#od-ring-e">THE FUTURE IS NOW · THE FUTURE IS NOW · THE FUTURE IS NOW ·</textPath></text>
   <circle cx="960" cy="540" r="116" fill="#fff"/><circle cx="960" cy="540" r="98" fill="#030304"/>
  </svg>
 </AbsoluteFill>;
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

const GreenGhostTransition=()=>{
 const f=useCurrentFrame(),x=e(f,0,7,-180,80);
 return <AbsoluteFill style={{...full,background:"#d8f6ad",overflow:"hidden"}}>
  <div style={{position:"absolute",left:90,bottom:-90,fontFamily:displayFont,fontSize:680,fontWeight:950,lineHeight:.8,color:"#158324",transform:"translateX("+x+"px)",letterSpacing:"-.15em",textShadow:"12px 0 0 rgba(36,155,53,.35),24px 0 0 rgba(36,155,53,.25),36px 0 0 rgba(36,155,53,.15)"}}>N</div>
  <div style={{position:"absolute",left:25,top:28,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#304a24"}}>OPEN DESIGN / MOTION REEL — 2026</div>
  <div style={{position:"absolute",right:25,top:28,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#304a24"}}>06 — KINETIC TYPE</div>
  <div style={{position:"absolute",left:26,right:26,bottom:24,height:2,background:"#274b26",opacity:.45}}/>
 </AbsoluteFill>;
};

const NeverPoster = () => (
 <AbsoluteFill style={{...full,background:"#d7f7ae",color:"#101713",overflow:"hidden"}}>
  <Word size={340} color="#111713" tracking={-.13} style={{position:"absolute",left:"-2%",right:"-2%",top:340,textAlign:"center"}}>NEVER</Word>
  <div style={{position:"absolute",left:25,top:28,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#304a24"}}>OPEN DESIGN / MOTION REEL — 2026</div>
  <div style={{position:"absolute",right:25,top:28,fontSize:15,fontWeight:900,letterSpacing:".18em",color:"#304a24"}}>06 — KINETIC TYPE</div>
  <div style={{position:"absolute",left:26,right:26,bottom:24,height:2,background:"#274b26",opacity:.45}}/>
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
 const f=useCurrentFrame(),rotate=f*1.1;
 return <AbsoluteFill style={{...full,background:"#152e86",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(140deg,#2542a3,#111b5d)"}}/>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   {Array.from({length:80},(_,i)=><path key={i} d={"M"+((i*113)%1920)+" "+((i*97)%1080)+"q 80 -45 160 "+((i%5)*19-38)} stroke={i%3?"#5068bd":"#e1c46c"} strokeWidth={i%4?6:11} fill="none" opacity=".25"/>)}
   <circle cx="960" cy="540" r="338" fill="#d9b34c" stroke="#f3d783" strokeWidth="27"/>
   <circle cx="960" cy="540" r="294" fill="#1b368f" stroke="#ad8135" strokeWidth="16"/>
   <circle cx="960" cy="540" r="244" fill="none" stroke="#f5d478" strokeWidth="7" strokeDasharray="4 16"/>
   <circle cx="960" cy="540" r="195" fill="#192b71" stroke="#e9c65c" strokeWidth="11"/>
   <g transform={"translate(960 540) rotate("+rotate+")"}><path d="M-90 -190L22 10L-40 30L-62 165Z" fill="#f8d975" stroke="#8d6e33" strokeWidth="7"/></g>
   <circle cx="960" cy="540" r="31" fill="#eac75c" stroke="#fff0a0" strokeWidth="8"/>
  </svg>
  <div style={{position:"absolute",left:0,right:0,top:45,textAlign:"center",fontSize:39,fontWeight:950,color:"#f3d47c",letterSpacing:".16em"}}>1889</div>
 </AbsoluteFill>;
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
 const f=useCurrentFrame(),light=e(f,0,12);
 return <AbsoluteFill style={{...full,background:"#fff9ef",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,display:"grid",gridTemplateColumns:"20% 60% 20%",gridTemplateRows:"1fr 1fr",padding:30,gap:12,boxSizing:"border-box"}}>
   <div style={{gridColumn:"1",gridRow:"1",background:"#ffd839",border:"9px solid #151719",backgroundImage:"radial-gradient(#e6ad17 2px,transparent 2.5px)",backgroundSize:"17px 17px"}}/>
   <div style={{gridColumn:"1",gridRow:"2",background:"#f5c9d8",border:"9px solid #151719",backgroundImage:"radial-gradient(#e8a6bd 2px,transparent 2.5px)",backgroundSize:"17px 17px"}}/>
   <div style={{gridColumn:"3",gridRow:"1",background:"#f6cbd9",border:"9px solid #151719",backgroundImage:"radial-gradient(#e6a9c0 2px,transparent 2.5px)",backgroundSize:"16px 16px"}}/>
   <div style={{gridColumn:"3",gridRow:"2",background:"#ffda39",border:"9px solid #151719",backgroundImage:"radial-gradient(#e8ad1b 2px,transparent 2.5px)",backgroundSize:"17px 17px"}}/>
   <div style={{gridColumn:"2",gridRow:"1 / span 2",position:"relative",background:"#6f9ddb",border:"9px solid #151719",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:-30,background:"repeating-conic-gradient(from "+(f*1.2)+"deg at 50% 50%,rgba(255,255,255,.98) 0deg 3deg,rgba(64,111,187,.16) 3deg 8deg)"}}/>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#4d85cc 0 4px,transparent 4.5px)",backgroundSize:"22px 22px",mixBlendMode:"multiply",opacity:.65}}/>
    <div style={{position:"absolute",left:"17%",top:"13%",width:"66%",height:"74%",borderRadius:"50%",background:"#ffe55a",border:"7px solid #151719",boxShadow:"0 0 0 12px rgba(255,255,255,.58)"}}/>
    <div style={{position:"absolute",left:"24%",top:"23%",width:"53%",height:"56%",borderRadius:"48% 48% 45% 45%",background:"#e93730",border:"9px solid #151719",boxShadow:"inset 0 0 0 7px rgba(255,255,255,.7)"}}/>
    <div style={{position:"absolute",left:"37%",top:"35%",width:"29%",height:"31%",borderRadius:"50%",background:"#fff",border:"7px solid #151719",display:"grid",placeItems:"center"}}>
     <svg viewBox="0 0 100 120" width="100%" height="100%"><path d="M8 4L94 61L52 68L38 116Z" fill="#101214"/></svg>
    </div>
    <svg viewBox="0 0 1200 1000" width="100%" height="100%" style={{position:"absolute",inset:0}}>
     <path d="M-60 70L70 70L340 280L255 350L550 530L468 604L770 770L690 842L1040 1035L1125 1010" stroke="#151719" strokeWidth="34" fill="none" strokeLinejoin="miter"/>
     <path d="M-60 70L70 70L340 280L255 350L550 530L468 604L770 770L690 842L1040 1035L1125 1010" stroke="#ffd739" strokeWidth="23" fill="none" strokeLinejoin="miter"/>
    </svg>
    <div style={{position:"absolute",top:18,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontStyle:"italic",fontSize:34,fontWeight:900,color:"#1a3872",textShadow:"0 1px #fff"}}>1952 · CUT-OUTS</div>
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
 const f=useCurrentFrame(),pulse=1+Math.sin(f/3)*.012;
 return <AbsoluteFill style={{...full,background:"#e83f31",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#fff8ec 0 10px,transparent 10.7px)",backgroundSize:"40px 40px",backgroundPosition:"0 0"}}/>
  <div style={{position:"absolute",left:"50%",top:"55%",width:540,height:540,marginLeft:-270,marginTop:-270,transform:"scale("+pulse+")",borderRadius:45,background:"#f6cc35",boxShadow:"0 0 0 10px #e83f31,0 0 0 16px rgba(20,20,20,.95)"}}>
   <div style={{position:"absolute",inset:24,borderRadius:35,border:"8px solid #18191a",background:"#e83f31",backgroundImage:"radial-gradient(#fff8ec 0 7px,transparent 7.5px)",backgroundSize:"28px 28px",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:36,borderRadius:"50%",border:"9px solid #17191b",background:"rgba(233,61,48,.28)"}}/>
    {Array.from({length:30},(_,i)=>{const a=i*Math.PI*2/30;return <circle key={i} cx={270+Math.cos(a)*220} cy={220+Math.sin(a)*220} r={i%3===0?7:5} fill="#17191b" opacity=".9"/>;})}
    <svg viewBox="0 0 100 120" width="170" height="205" style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)"}}><path d="M8 5L94 60L52 67L38 115Z" fill="#101214"/></svg>
   </div>
  </div>
  <div style={{position:"absolute",left:"50%",top:28,transform:"translateX(-50%)",padding:"12px 58px 16px",background:"#fff8ec",border:"6px solid #fff8ec",clipPath:"polygon(0 0,100% 0,96% 100%,4% 100%)",textAlign:"center",color:"#111315",fontFamily:displayFont,fontSize:29,fontWeight:950,whiteSpace:"nowrap",boxShadow:"0 8px 0 rgba(0,0,0,.1)"}}>1965 <span style={{fontSize:24}}>Infinity dots</span></div>
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
 const f=useCurrentFrame(),ray=e(f,0,8,-80,1250);
 return <AbsoluteFill style={{...full,background:"#030509",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 51% 51%,#182436,#030509 65%)"}}/>
  <div style={{position:"absolute",left:55,bottom:24,fontFamily:displayFont,fontSize:265,fontWeight:950,color:"#161e2b",letterSpacing:"-.1em"}}>1973</div>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <radialGradient id="opd1973lens"><stop offset="0%" stopColor="#172236"/><stop offset="36%" stopColor="#53627b"/><stop offset="63%" stopColor="#142132"/><stop offset="100%" stopColor="#03070d"/></radialGradient>
    <linearGradient id="opd1973spectrum" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stopColor="#fff"/><stop offset="14%" stopColor="#ffe77c"/><stop offset="27%" stopColor="#ff793e"/><stop offset="40%" stopColor="#f14dbd"/><stop offset="54%" stopColor="#856aff"/><stop offset="69%" stopColor="#43aaff"/><stop offset="84%" stopColor="#35eadc"/><stop offset="100%" stopColor="#fff"/></linearGradient>
   </defs>
   <path d="M0 540H670" stroke="#fff" strokeWidth="10" opacity=".96"/>
   <path d="M0 520H670" stroke="#d3efff" strokeWidth="3" opacity=".8"/>
   <circle cx="960" cy="540" r="260" fill="url(#opd1973lens)" stroke="#d7e6f6" strokeWidth="11"/>
   <circle cx="960" cy="540" r="220" fill="none" stroke="#8caac4" strokeWidth="4" opacity=".58"/>
   <circle cx="960" cy="540" r="185" fill="none" stroke="#fff" strokeWidth="3" opacity=".32"/>
   <path d="M760 420Q960 250 1160 420" fill="none" stroke="#f4f6ff" strokeWidth="11" opacity=".36"/>
   <path d="M840 430L1045 535L910 560L880 680Z" fill="#eff5ff" opacity=".95"/>
   <circle cx="960" cy="540" r="27" fill="#0b111e" stroke="#fff" strokeWidth="4"/>
   <path d={"M1210 440L"+(1920+ray)+" 230L"+(1920+ray)+" 850L1210 640Z"} fill="url(#opd1973spectrum)" opacity=".96"/>
  </svg>
  <div style={{position:"absolute",left:64,top:44,color:"#aab6c8",fontSize:15,fontWeight:900,letterSpacing:".2em"}}>OPTICAL MEDIA / LIGHT REFRACTION</div>
 </AbsoluteFill>;
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
 const f=useCurrentFrame(),progress=e(f,0,15),count=Math.round(80+16*progress),day=Math.round(88+50*progress);
 const y=470-330*progress;
 return <AbsoluteFill style={{...full,background:"linear-gradient(180deg,#c5e6e1 0%,#c9ebe0 42%,#f0cbb8 65%,#71c8c5 100%)",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <path d="M0 650Q170 592 340 664T690 660T1050 676T1410 640T1740 674T1920 650V1080H0Z" fill="#6cc9bd" opacity=".76"/>
   <path d="M0 820Q195 750 390 830T800 812T1220 845T1600 808T1920 842V1080H0Z" fill="#f2cdb2" opacity=".68"/>
   <path d="M0 935Q230 875 430 934T840 923T1280 947T1700 914T1920 937V1080H0Z" fill="#4db9bb" opacity=".55"/>
   {Array.from({length:26},(_,i)=><path key={i} d={"M"+(i*77)+" "+(704+(i%5)*22)+"q 55 -25 105 4"} stroke="#fff5e8" strokeWidth="7" fill="none" opacity=".44"/>)}
  </svg>
  <div style={{position:"absolute",left:78,top:245,fontFamily:displayFont,fontSize:254,fontWeight:950,color:"#111315",letterSpacing:"-.12em",textShadow:"0 6px 10px rgba(0,0,0,.16)"}}>{count}K</div>
  <div style={{position:"absolute",left:263,top:500,fontSize:54,fontWeight:850,color:"#343b38"}}>Day {day}</div>
  <div style={{position:"absolute",left:665,top:80,width:1180,height:900,borderRadius:28,background:"#fff",padding:"70px 70px 54px",boxSizing:"border-box",boxShadow:"0 18px 55px rgba(37,85,92,.13)"}}>
   <div style={{textAlign:"center",fontSize:36,fontWeight:900,color:"#202326",marginBottom:48}}>◉ Star History</div>
   <div style={{position:"absolute",left:110,top:175,fontSize:20,fontWeight:800,color:"#45494b"}}>nexu-io/open-design</div>
   <svg viewBox="0 0 1040 560" width="100%" height="560">
    {[0,1,2,3,4].map(v=><g key={v}><line x1="82" x2="1010" y1={80+v*105} y2={80+v*105} stroke="#e6e6e3" strokeWidth="2"/><text x="12" y={87+v*105} fontSize="22" fill="#4a4e50">{100-v*20}K</text></g>)}
    <path d={"M82 500C120 465 135 330 210 280S315 225 375 203S530 150 610 125S760 95 855 "+y+"L930 "+(y-25)} stroke="#c94d3e" strokeWidth="7" fill="none" strokeLinecap="round"/>
    <circle cx="930" cy={y-25} r="12" fill="#b9f05b" stroke="#141719" strokeWidth="4"/>
    <text x="82" y="535" fontSize="20" fill="#303638">May</text><text x="270" y="535" fontSize="20" fill="#303638">June</text><text x="455" y="535" fontSize="20" fill="#303638">July</text><text x="645" y="535" fontSize="20" fill="#303638">August</text><text x="835" y="535" fontSize="20" fill="#303638">September</text><text x="960" y="535" fontSize="20" fill="#303638">October</text>
   </svg>
   <div style={{position:"absolute",left:78,bottom:23,fontSize:18,color:"#737a79"}}>GitHub stars</div>
  </div>
 </AbsoluteFill>;
};

const KoalaPoster=()=><AbsoluteFill style={{...full,background:"linear-gradient(120deg,#2a8bd1,#144a9a)",color:"#fff"}}><div style={{position:"absolute",left:330,top:190,width:430,height:540,borderRadius:220,background:"#f5ead0",transform:"rotate(-5deg)"}}><svg viewBox="0 0 430 540" width="100%" height="100%"><ellipse cx="82" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="348" cy="165" rx="70" ry="90" fill="#818b94"/><ellipse cx="215" cy="255" rx="155" ry="170" fill="#9099a1"/><ellipse cx="215" cy="298" rx="120" ry="100" fill="#f2efe6"/><circle cx="160" cy="246" r="16" fill="#151a1d"/><circle cx="270" cy="246" r="16" fill="#151a1d"/><ellipse cx="215" cy="300" rx="42" ry="57" fill="#20262c"/><path d="M180 365Q215 392 250 365" stroke="#252a2c" strokeWidth="10" fill="none"/></svg></div><div style={{position:"absolute",right:270,top:195,width:450,height:650,background:"#fff",color:"#182431",borderRadius:20,padding:38,boxSizing:"border-box",boxShadow:"0 24px 55px rgba(0,0,0,.22)"}}><div style={{fontSize:21,fontWeight:950,letterSpacing:".1em"}}>COURSES / 2026</div><div style={{marginTop:34,height:250,borderRadius:14,background:"linear-gradient(135deg,#f2dfba,#e4a27b,#83b9cb)"}}/><div style={{marginTop:34,fontSize:48,fontWeight:950,lineHeight:.95}}>Learn to create.</div><div style={{marginTop:25,fontSize:18,color:"#7e8991"}}>A new way to make ideas move.</div></div></AbsoluteFill>;
const GreenTransition=()=>{const f=useCurrentFrame(),r=e(f,0,7,90,650);return <AbsoluteFill style={{...full,background:"#b7ee5b"}}><svg viewBox="0 0 1920 1080" width="100%" height="100%"><circle cx="960" cy="540" r={r} fill="none" stroke="#efffd4" strokeWidth="3"/><circle cx="960" cy="540" r={r*.7} fill="none" stroke="#efffd4" strokeWidth="2"/></svg><Word size={420} color="#142016" style={{position:"absolute",left:0,right:0,top:300,textAlign:"center"}}>OUT.</Word></AbsoluteFill>;};



const Comic1962=()=>{
 const f=useCurrentFrame(),scale=1+e(f,0,16)*.012;
 return <AbsoluteFill style={{...full,background:"#fbf5e9",transform:"scale("+scale+")",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:26,display:"grid",gridTemplateColumns:"20% 60% 20%",gridTemplateRows:"1fr 1fr",gap:10}}>
   <div style={{background:"#ffdd3d",border:"8px solid #17191b",display:"grid",placeItems:"center",fontFamily:displayFont,fontSize:34,fontWeight:950,color:"#17191b",fontStyle:"italic"}}>ONE IDEA…</div>
   <div style={{gridColumn:"2",gridRow:"1 / span 2",position:"relative",overflow:"hidden",border:"9px solid #17191b",background:"#76a5e4"}}>
    <div style={{position:"absolute",inset:-40,background:"repeating-conic-gradient(from -6deg at 50% 48%,#fff 0deg 2.5deg,#6c9cdd 2.5deg 9deg)"}}/>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#3977c4 0 4px,transparent 4.4px)",backgroundSize:"24px 24px",opacity:.65}}/>
    <div style={{position:"absolute",left:"14%",top:"13%",width:"72%",height:"74%",borderRadius:"50%",background:"#ffe25b",boxShadow:"0 0 0 8px rgba(255,255,255,.65)"}}/>
    <div style={{position:"absolute",left:"23%",top:"25%",width:"55%",height:"55%",borderRadius:"34% 43% 36% 38%",background:"#ed3c2d",border:"9px solid #151719",boxShadow:"inset 0 0 0 8px rgba(20,20,20,.22)",display:"grid",placeItems:"center"}}>
     <div style={{width:"72%",height:"72%",borderRadius:"50%",background:"#fff",border:"7px solid #151719",backgroundImage:"radial-gradient(#71a0dc 0 3px,transparent 3.5px)",backgroundSize:"20px 20px",display:"grid",placeItems:"center"}}>
      <svg viewBox="0 0 100 120" width="100%" height="100%"><path d="M8 5L92 59L53 69L38 115Z" fill="#090b0d"/></svg>
     </div>
    </div>
    <div style={{position:"absolute",left:25,top:24,padding:"8px 18px",background:"#ffdf36",border:"5px solid #17191b",fontSize:25,fontWeight:950,fontStyle:"italic",color:"#17191b"}}>MEANWHILE, IN 1962…</div>
    <div style={{position:"absolute",right:30,top:22,textAlign:"right",fontFamily:displayFont,fontSize:54,fontWeight:950,color:"#101214",lineHeight:.85}}>1962<div style={{fontSize:20,fontStyle:"italic"}}>POP ART</div></div>
    <div style={{position:"absolute",right:16,bottom:28,padding:"10px 24px",background:"#ffdf37",border:"6px solid #17191b",clipPath:"polygon(50% 0,60% 18%,80% 5%,82% 30%,100% 36%,84% 54%,98% 75%,70% 73%,60% 100%,45% 81%,22% 96%,22% 70%,0 60%,19% 42%,8% 20%,36% 24%)",fontSize:37,fontWeight:950,fontStyle:"italic",color:"#ed392d",textShadow:"2px 2px #111"}}>CLICK!</div>
   </div>
   <div style={{background:"#fae7eb",border:"8px solid #17191b",backgroundImage:"radial-gradient(#dca9b6 2px,transparent 2.5px)",backgroundSize:"16px 16px",display:"grid",placeItems:"center",fontSize:42,fontWeight:950}}>•••</div>
   <div style={{background:"#fae7eb",border:"8px solid #17191b",backgroundImage:"radial-gradient(#dca9b6 2px,transparent 2.5px)",backgroundSize:"16px 16px",display:"grid",placeItems:"center",fontSize:26,fontWeight:950}}>SFX</div>
   <div style={{background:"#ffdd3d",border:"8px solid #17191b",display:"grid",placeItems:"center",fontSize:26,fontWeight:950}}>CUT / OUT</div>
  </div>
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
  <Sequence from={0} durationInFrames={13}><Comic1952 /></Sequence>
  <Sequence from={13} durationInFrames={16}><Comic1962 /></Sequence>
  <Sequence from={29} durationInFrames={8}><DotPoster /></Sequence>
  <Sequence from={37} durationInFrames={15}><LightSweep1973 /></Sequence>
  <Sequence from={52} durationInFrames={13}><PixelGamePoster /></Sequence>
  <Sequence from={65} durationInFrames={9}><PortfolioFlash /></Sequence>
  <Sequence from={74} durationInFrames={10}><MindPoster /></Sequence>
  <Sequence from={84} durationInFrames={30}><RingPoster /></Sequence>
  <Sequence from={114} durationInFrames={24}><EditorialPosterGrid /></Sequence>
  <Sequence from={138} durationInFrames={22}><EaseGreen /></Sequence>
  <Sequence from={160} durationInFrames={7}><OutPoster /></Sequence>
  <Sequence from={167} durationInFrames={7}><GreenGhostTransition /></Sequence>
  <Sequence from={174} durationInFrames={5}><NeverPoster /></Sequence>
  <Sequence from={179} durationInFrames={15}><LinearPoster /></Sequence>
  <Sequence from={194} durationInFrames={13}><GreenCircleTransition /></Sequence>
  <Sequence from={207} durationInFrames={16}><StatsPoster /></Sequence>
  <Sequence from={223} durationInFrames={11}><MotionFilmsPoster /></Sequence>
  <Sequence from={234} durationInFrames={5}><EyePoster /></Sequence>
  <Sequence from={239} durationInFrames={15}><CoursesPoster /></Sequence>
  <Sequence from={254} durationInFrames={15}><Future3D /></Sequence>
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
 if(variant===3)return <div style={{position:"absolute",inset:0,background:"#090a0c",overflow:"hidden"}}><svg viewBox="0 0 1000 650" width="100%" height="100%">{Array.from({length:20},(_,i)=><path key={i} d={"M"+(-120+i*68)+" -20 C"+(60+i*34)+" 130 "+(-40+i*50)+" 370 "+(180+i*39)+" 670"} stroke="#fff" strokeWidth="31" fill="none" strokeLinecap="round"/>)}</svg></div>;
 if(variant===4)return <div style={{position:"absolute",inset:0,background:"#83ed43",overflow:"hidden"}}><div style={{position:"absolute",left:"-6%",right:"-8%",top:"31%",textAlign:"center",fontFamily:displayFont,fontWeight:950,fontSize:210,letterSpacing:"-.12em",color:"#12170e",textShadow:"10px 11px 0 rgba(36,58,18,.26)"}}>EASE</div><div style={{position:"absolute",left:22,right:22,bottom:28,height:2,background:"#1b3314",opacity:.55}}/><div style={{position:"absolute",left:22,bottom:37,fontSize:12,color:"#1b3314"}}>66 FPS</div><div style={{position:"absolute",right:22,bottom:37,fontSize:12,color:"#1b3314"}}>128 BPM</div></div>;
 if(variant===5)return <div style={{position:"absolute",inset:0,background:"linear-gradient(90deg,#f2f1ea 0 52%,#1746d6 52% 100%)",overflow:"hidden"}}><div style={{position:"absolute",left:38,top:50,fontSize:19,fontWeight:950,color:"#111315",letterSpacing:".16em"}}>CREATIVE / 03</div><div style={{position:"absolute",left:"12%",top:"22%",fontSize:390,fontWeight:950,fontFamily:displayFont,color:"#151719",letterSpacing:"-.12em",textShadow:"9px 11px 0 rgba(0,0,0,.16)"}}>3</div><div style={{position:"absolute",right:44,bottom:42,color:"#fff",fontSize:18,fontWeight:900,letterSpacing:".2em"}}>READY / MOTION</div></div>;
 return <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#f2f0e8,#fff)",overflow:"hidden"}}><div style={{position:"absolute",inset:0,display:"grid",placeItems:"center",fontSize:430,fontWeight:950,color:"#111315",fontFamily:displayFont,textShadow:"12px 14px 0 rgba(0,0,0,.15)"}}>3</div></div>;
};

const CountdownArtwork = ({ value, frame }: { value: number; frame: number }) => {
 const p=pop(frame,30,0,75,14),scale=.88+.12*p;
 const isThree=value===3,isTwo=value===2;
 const background=isThree?"#ecebe6":isTwo?"#1730ee":"#050609";
 const numeralColor=isThree?"#050609":isTwo?"#f0f0ee":"#2637ef";
 const shadows=isThree
  ?"2px 2px 0 #b5b5b1,5px 5px 0 #858784,10px 11px 0 #656866,18px 22px 0 #3c3e42,30px 42px 36px rgba(0,0,0,.28)"
  :isTwo
  ?"2px 2px 0 #bfc2ca,5px 5px 0 #9297a3,10px 11px 0 #707583,18px 22px 0 #454b5a,28px 38px 36px rgba(0,0,0,.45)"
  :"2px 2px 0 #6f7dff,6px 7px 0 #4858eb,12px 14px 0 #2837be,21px 25px 0 #161d71,34px 44px 40px rgba(0,0,0,.7)";
 return <AbsoluteFill style={{background,color:"#fff",overflow:"hidden"}}>
  {isThree?<div style={{position:"absolute",right:0,top:0,bottom:0,width:"31%",background:"#2438ed"}}/>:null}
  {isTwo?<div style={{position:"absolute",right:0,top:0,bottom:0,width:"29%",background:"#05060b"}}/>:null}
  {!isThree&&!isTwo?<div style={{position:"absolute",right:0,bottom:0,width:"31%",height:"38%",background:"#1533ef",clipPath:"polygon(100% 0,100% 100%,0 100%)"}}/>:null}
  <svg viewBox="0 0 1000 650" width="100%" height="100%" style={{position:"absolute",inset:0,opacity:isThree?.52:.72}}>
   <ellipse cx="500" cy="325" rx="365" ry="255" fill="none" stroke={isThree?"#a4a6a5":isTwo?"#d9d9ff":"#797bff"} strokeWidth="2"/>
   <ellipse cx="500" cy="325" rx="340" ry="225" fill="none" stroke={isThree?"#fff":isTwo?"#aab6ff":"#cbccff"} strokeWidth="1.3" transform={"rotate("+(frame*1.2)+" 500 325)"}/>
   {isThree?<path d="M0 325H1000" stroke="#a0a0a0" strokeWidth="1" opacity=".22"/>:null}
  </svg>
  <div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) perspective(1200px) rotateX(8deg) rotateY(-9deg) scale("+scale+")",fontFamily:displayFont,fontSize:isThree?470:500,lineHeight:.78,fontWeight:1000,letterSpacing:"-.12em",color:numeralColor,textShadow:shadows}}>{value}</div>
  <div style={{position:"absolute",left:34,top:"47%",fontFamily:"monospace",fontSize:14,fontWeight:900,letterSpacing:".12em",color:isThree?"#101214":isTwo?"#eff0ff":"#f3f3ff"}}>{isThree?"IGNITION SEQUENCE / 01":"IGNITION SEQUENCE / "+(isTwo?"02":"03")}</div>
  <div style={{position:"absolute",right:35,top:"48%",fontFamily:"monospace",fontSize:13,fontWeight:850,letterSpacing:".16em",color:isThree?"#222":isTwo?"#eee":"#fff",textAlign:"right"}}>SNARE ROLL / {isThree?"1":isTwo?"2":"3"}</div>
  <div style={{position:"absolute",right:35,bottom:35,display:"flex",gap:8}}>{[0,1,2].map(v=><div key={v} style={{width:24,height:6,background:v<=(isThree?0:isTwo?1:2)?"#fff":"rgba(255,255,255,.22)"}}/>)}</div>
  {!isThree&&!isTwo?<div style={{position:"absolute",left:45,top:32,fontSize:17,fontWeight:900,letterSpacing:".2em",color:"#fff"}}>GO</div>:null}
 </AbsoluteFill>;
};

const LaunchKitWindow=({frame,variant,countdown=-1}:{frame:number;variant:number;countdown?:number})=>{
 const {fps}=useVideoConfig(),p=pop(frame,fps,0,84,19);
 const names=["Claude Opus 5.5","Claude Opus 5.5","Gemini","GLM","MiMo","DeepSeek V4.1","OpenDesign"];
 const name=names[variant%names.length];
 const symbols=["✣","✣","▶","Z","MiMo","🐳","◈"];
 const colors=["#df805b","#df805b","#151c30","#191919","#1d2328","#4879df","#293a92"];
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
 const variant=frame<15?0:frame<30?1:frame<45?2:frame<60?3:frame<75?4:frame<76?5:frame<91?5:frame<106?5:6;
 const countdown=frame<76?-1:frame<91?3:frame<106?2:1;
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
 const f=useCurrentFrame();
 const typeOut=1-e(f,12,25),shape=e(f,14,34);
 return <AbsoluteFill style={{...full,background:"#f2f1e9",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,opacity:typeOut,display:"flex",flexDirection:"column",justifyContent:"space-between",transform:"translateX("+(e(f,0,20,-18,8))+"px)"}}>
   <Word size={330} color="#08090b" tracking={-.12}>MORRO</Word>
   <Word size={330} color="#f2f1e9" tracking={-.12} style={{WebkitTextStroke:"3px #08090b"}}>MORRO</Word>
   <Word size={330} color="#08090b" tracking={-.12}>MORRO</Word>
  </div>
  <div style={{position:"absolute",left:"50%",top:"50%",width:640,height:640,transform:"translate(-50%,-50%) scale("+(0.68+.28*shape)+")",opacity:shape}}>
   <div style={{position:"absolute",inset:70,borderRadius:100,background:"#2035ed",boxShadow:"0 20px 0 #7a54bc,0 32px 0 #b58ae1",transform:"rotate(0deg)"}}/>
   <div style={{position:"absolute",left:"36%",top:-10,width:180,height:670,background:"linear-gradient(90deg,#b38ddf,#f0c9ff 45%,#8e6bc8)",transform:"rotate(13deg) skewY(-8deg)",boxShadow:"16px 0 0 rgba(98,58,161,.35),-12px 0 0 rgba(255,255,255,.6)"}}/>
   <div style={{position:"absolute",left:"52%",top:"30%",width:190,height:410,background:"linear-gradient(90deg,#ac7bd5,#e7b8f4,#7d5bb8)",transform:"rotate(13deg) skewY(-8deg)",boxShadow:"12px 0 0 rgba(98,58,161,.4)"}}/>
  </div>
  <div style={{position:"absolute",left:"50%",top:"50%",width:610,height:610,transform:"translate(-50%,-50%) scale("+(0.84+.16*e(f,25,36))+")",opacity:e(f,24,35),borderRadius:105,background:"linear-gradient(135deg,#1925ab,#070b2f 58%,#09114a)",boxShadow:"0 23px 50px rgba(0,0,0,.2)",overflow:"hidden"}}>
   <div style={{position:"absolute",inset:0,background:"linear-gradient(125deg,rgba(255,255,255,.32),transparent 35%,rgba(0,0,0,.28))"}}/>
   <svg viewBox="0 0 610 610" width="100%" height="100%"><path d="M140 70H458Q535 70 535 148V454Q535 535 455 535H160Q70 535 70 445V165Q70 70 140 70Z" fill="none" stroke="#fff" strokeWidth="12"/><circle cx="305" cy="303" r="151" fill="none" stroke="#fff" strokeWidth="14"/><circle cx="305" cy="303" r="119" fill="none" stroke="#a7c5ff" strokeWidth="7"/><path d="M251 180L400 290L322 301L287 416Z" fill="#fff"/></svg>
  </div>
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
    <Sequence from={83} durationInFrames={57}><HeroTitle /></Sequence>
    <Sequence from={140} durationInFrames={30}><BrandReveal /></Sequence>
    <Sequence from={170} durationInFrames={70}><ClaimScene /></Sequence>
    <Sequence from={240} durationInFrames={76}><GalleryWall /></Sequence>
    <Sequence from={316} durationInFrames={269}><PosterSequence /></Sequence>
    <Sequence from={585} durationInFrames={56}><NotJustOpus /></Sequence>
    <Sequence from={641} durationInFrames={138}><ModelAgentScene /></Sequence>
    <Sequence from={779} durationInFrames={118}><LaunchKitSequence /></Sequence>
    <Sequence from={897} durationInFrames={36}><MorroCubeIntro /></Sequence>
    <Sequence from={933} durationInFrames={117}><TexturedCube /></Sequence>
    <Sequence from={1050} durationInFrames={69}><FinalLockup /></Sequence>
    <Audio src={staticFile("audio/opendesign-motion-score.wav")} volume={0.92} />
  </AbsoluteFill>
);