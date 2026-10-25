import React from "react";
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from "remotion";

type Pose = "sit" | "scroll" | "slump" | "stand" | "walk" | "write" | "meet" | "hero";
type Shot = {
  title: string;
  subtitle: string;
  setting: "bedroom" | "void" | "calendar" | "desk" | "stairs" | "hall" | "dawn";
  pose: Pose;
  x0: number;
  x1: number;
  y: number;
  shadow: number;
  phone?: boolean;
};
const SHOT_FRAMES = 180;
const shots: Shot[] = [
  {title: "ONE MORE SCROLL", subtitle: "It starts with one small decision.", setting: "bedroom", pose: "sit", x0: 650, x1: 650, y: 0, shadow: 0.72, phone: true},
  {title: "JUST ONE MINUTE", subtitle: "The next scroll never feels like the last.", setting: "void", pose: "scroll", x0: 700, x1: 710, y: 0, shadow: 0.88, phone: true},
  {title: "THE DAYS DISAPPEAR", subtitle: "Time moves, even when we do not.", setting: "calendar", pose: "slump", x0: 540, x1: 510, y: 10, shadow: 0.68},
  {title: "RESET TO ZERO", subtitle: "A reset is not a failure. It is a choice.", setting: "void", pose: "stand", x0: 610, x1: 650, y: 0, shadow: 0.48},
  {title: "START SMALL", subtitle: "Put the phone down. Begin with one page.", setting: "desk", pose: "write", x0: 510, x1: 535, y: 0, shadow: 0.34, phone: true},
  {title: "SHOW UP AGAIN", subtitle: "Progress is a direction, not a perfect streak.", setting: "stairs", pose: "walk", x0: 370, x1: 790, y: -28, shadow: 0.24},
  {title: "YOU ARE NOT ALONE", subtitle: "Some things get easier when shared.", setting: "hall", pose: "meet", x0: 500, x1: 610, y: 0, shadow: 0.13},
  {title: "YOUR ATTENTION IS YOUR LIFE", subtitle: "Choose what gets a piece of it.", setting: "dawn", pose: "hero", x0: 630, x1: 650, y: -8, shadow: 0.04}
];

const clampInterpolate = (value: number, input: number[], output: number[]) =>
  interpolate(value, input, output, {extrapolateLeft: "clamp", extrapolateRight: "clamp"});

const Character: React.FC<{x: number; y: number; pose: Pose; t: number; scale?: number; red?: boolean}> = ({
  x, y, pose, t, scale = 1, red = false
}) => {
  const walk = pose === "walk";
  const step = walk ? Math.sin(t * Math.PI * 4) : 0;
  const bob = walk ? Math.abs(Math.sin(t * Math.PI * 4)) * -5 : Math.sin(t * Math.PI * 2) * 1.5;
  const bodyTilt = pose === "slump" ? 10 : pose === "hero" ? -3 : pose === "scroll" ? 5 : 0;
  const armA = pose === "scroll" ? -46 : pose === "write" ? -62 : walk ? -20 + step * 25 : pose === "hero" ? -27 : pose === "meet" ? -32 : pose === "slump" ? 26 : -8;
  const armB = pose === "scroll" ? 35 : pose === "write" ? 12 : walk ? 28 - step * 24 : pose === "hero" ? 14 : pose === "meet" ? -42 : pose === "slump" ? 38 : 10;
  const legA = walk ? -18 + step * 32 : pose === "sit" || pose === "scroll" ? 50 : 0;
  const legB = walk ? 18 - step * 32 : pose === "sit" || pose === "scroll" ? 55 : 0;
  const ink = red ? "#b94e52" : "#e9e2d4";
  const hoodie = red ? "#762f39" : "#5b6068";
  const headY = pose === "slump" ? -117 : pose === "scroll" || pose === "write" ? -123 : -132;
  const face = red ? "#762f39" : "#25282d";
  return (
    <svg width="220" height="330" viewBox="-100 -245 200 300" style={{position: "absolute", left: x - 110, top: 240 + y + bob, overflow: "visible", transform: "scale(" + scale + ")", transformOrigin: "50% 100%"}}>
      <g opacity={red ? 0.95 : 1} transform={"rotate(" + bodyTilt + " 0 -72)"}>
        <path d="M-28 -110 Q-55 -76 -37 -36 L-28 -5 L28 -5 L38 -38 Q54 -82 27 -111 Z" fill={hoodie} stroke={ink} strokeWidth="3" strokeLinejoin="round"/>
        <path d="M-20 -102 Q0 -82 20 -102" fill="none" stroke={red ? "#9f4248" : "#737983"} strokeWidth="3"/>
        <path d="M-9 -79 L-9 -20 M9 -79 L9 -20" fill="none" stroke={red ? "#9f4248" : "#737983"} strokeWidth="2"/>
        <g transform={"rotate(" + armA + " -28 -88)"}>
          <path d="M-28 -88 Q-52 -66 -50 -38" fill="none" stroke={hoodie} strokeWidth="18" strokeLinecap="round"/>
          <path d="M-28 -88 Q-52 -66 -50 -38" fill="none" stroke={ink} strokeWidth="2" strokeLinecap="round"/>
          <circle cx="-50" cy="-36" r="7" fill={ink}/>
        </g>
        <g transform={"rotate(" + armB + " 28 -88)"}>
          <path d="M28 -88 Q51 -66 48 -42" fill="none" stroke={hoodie} strokeWidth="18" strokeLinecap="round"/>
          <path d="M28 -88 Q51 -66 48 -42" fill="none" stroke={ink} strokeWidth="2" strokeLinecap="round"/>
          <circle cx="48" cy="-40" r="7" fill={ink}/>
        </g>
        <g transform={"rotate(" + legA + " -18 -8)"}>
          <path d="M-18 -8 L-26 22 L-35 29" fill="none" stroke={hoodie} strokeWidth="16" strokeLinecap="round"/>
          <path d="M-18 -8 L-26 22 L-35 29" fill="none" stroke={ink} strokeWidth="2" strokeLinecap="round"/>
          <path d="M-43 31 Q-27 26 -18 34 L-18 40 L-45 40 Z" fill={ink}/>
        </g>
        <g transform={"rotate(" + legB + " 18 -8)"}>
          <path d="M18 -8 L26 22 L35 29" fill="none" stroke={hoodie} strokeWidth="16" strokeLinecap="round"/>
          <path d="M18 -8 L26 22 L35 29" fill="none" stroke={ink} strokeWidth="2" strokeLinecap="round"/>
          <path d="M18 34 Q28 26 43 31 L45 40 L18 40 Z" fill={ink}/>
        </g>
        <circle cx="0" cy={headY} r="38" fill={ink} stroke={red ? "#762f39" : "#e9e2d4"} strokeWidth="3"/>
        {!red && <>
          <ellipse cx="-12" cy={headY - 3} rx="3.4" ry={pose === "slump" ? 2 : 4.7} fill={face}/>
          <ellipse cx="12" cy={headY - 3} rx="3.4" ry={pose === "slump" ? 2 : 4.7} fill={face}/>
          <path d={pose === "hero" ? "M-8 -126 Q0 -120 8 -126" : pose === "slump" ? "M-7 -107 Q0 -112 7 -107" : "M-7 -112 Q0 -108 7 -112"} fill="none" stroke={face} strokeWidth="2.5" strokeLinecap="round"/>
          {pose === "slump" && <path d="M-20 -150 L-8 -153 M8 -153 L20 -150" stroke={face} strokeWidth="2.5" strokeLinecap="round"/>}
        </>}
      </g>
      {pose === "scroll" && !red && <g transform={"translate(55 -55) rotate(-7)"}>
        <rect x="-11" y="-21" width="22" height="38" rx="4" fill="#15171b" stroke="#e9e2d4" strokeWidth="2"/>
        <rect x="-7" y="-16" width="14" height="25" rx="2" fill="#a9434b"/>
        <circle cx="0" cy="13" r="1.8" fill="#e9e2d4"/>
      </g>}
    </svg>
  );
};

const Backdrop: React.FC<{setting: Shot["setting"]; t: number}> = ({setting, t}) => (
  <AbsoluteFill style={{background: setting === "dawn" ? "linear-gradient(180deg,#293642 0%,#62656a 55%,#c09a76 100%)" : "linear-gradient(180deg,#15171b 0%,#202329 65%,#111317 100%)"}}>
    <svg width="100%" height="100%" viewBox="0 0 1280 720" style={{position: "absolute"}}>
      {setting === "bedroom" && <>
        <rect x="70" y="90" width="300" height="240" rx="3" fill="#252a32" stroke="#535963" strokeWidth="5"/>
        <rect x="84" y="104" width="272" height="212" fill="#1b2634"/>
        <circle cx="287" cy="160" r="28" fill="#d9d6c7" opacity=".82"/>
        <path d="M85 270 L160 210 L210 258 L262 195 L355 275 V316 H85Z" fill="#283847"/>
        <path d="M0 565 H1280" stroke="#444850" strokeWidth="3"/>
        <rect x="470" y="485" width="365" height="90" rx="8" fill="#393e46"/>
        <rect x="460" y="470" width="385" height="24" rx="6" fill="#565c66"/>
        <rect x="470" y="505" width="355" height="53" rx="6" fill="#727783"/>
        <path d="M490 505 Q620 530 818 505" fill="none" stroke="#969ba2" strokeWidth="2"/>
        <rect x="890" y="430" width="210" height="12" rx="4" fill="#5d626a"/>
        <path d="M930 430 V385 H1040 V430" fill="#353a43" stroke="#5d626a" strokeWidth="4"/>
      </>}
      {setting === "void" && <>
        {Array.from({length: 9}, (_, i) => <circle key={i} cx={130 + i * 145} cy={130 + (i % 3) * 95} r={1.6} fill="#858a91" opacity=".35"/>)}
        <path d="M0 570 H1280" stroke="#474b53" strokeWidth="2"/>
      </>}
      {setting === "calendar" && <>
        <rect x="790" y="100" width="310" height="280" rx="5" fill="#d9d3c6"/>
        <rect x="790" y="100" width="310" height="46" fill="#a9a295"/>
        <text x="812" y="130" fill="#292b30" fontSize="19" fontWeight="700">THIS WEEK</text>
        {Array.from({length: 21}, (_, i) => <g key={i}><rect x={812 + (i % 7) * 39} y={165 + Math.floor(i / 7) * 57} width="25" height="31" rx="3" fill={i < 10 ? "#9a6665" : "#bcb6a9"}/><path d={"M" + (818+(i%7)*39) + " " + (181+Math.floor(i/7)*57) + " l5 6 l9 -12"} fill="none" stroke="#ded8cb" strokeWidth="2" opacity={i < 10 ? 1 : 0}/></g>)}
        <path d="M0 570 H1280" stroke="#474b53" strokeWidth="2"/>
      </>}
      {setting === "desk" && <>
        <rect x="120" y="450" width="500" height="18" rx="5" fill="#66615b"/>
        <rect x="145" y="468" width="16" height="125" fill="#45474b"/>
        <rect x="580" y="468" width="16" height="125" fill="#45474b"/>
        <rect x="285" y="405" width="150" height="45" rx="3" fill="#393e47" stroke="#6a7078" strokeWidth="3"/>
        <path d="M302 415 H417 V439 H302Z" fill="#171b20"/>
        <rect x="225" y="432" width="42" height="5" rx="2" fill="#c3b7a0"/>
        <path d="M0 595 H1280" stroke="#444850" strokeWidth="3"/>
      </>}
      {setting === "stairs" && <>
        {Array.from({length: 9}, (_, i) => <path key={i} d={"M" + (160+i*104) + " " + (580-i*35) + " h104 v35"} fill="none" stroke="#515761" strokeWidth="5"/>)}
        <path d="M160 580 L1100 265" stroke="#747b83" strokeWidth="3" opacity=".5"/>
        <path d="M0 620 H1280" stroke="#444850" strokeWidth="3"/>
      </>}
      {setting === "hall" && <>
        <path d="M0 80 L390 210 V560 L0 630Z" fill="#1d2026" stroke="#383c44" strokeWidth="3"/>
        <path d="M1280 80 L890 210 V560 L1280 630Z" fill="#1d2026" stroke="#383c44" strokeWidth="3"/>
        <path d="M390 210 H890 V560 H390Z" fill="#262a31"/>
        <path d="M0 630 L390 560 H890 L1280 630" fill="none" stroke="#565b64" strokeWidth="3"/>
      </>}
      {setting === "dawn" && <>
        <circle cx="1000" cy="265" r="90" fill="#d5b18b" opacity=".85"/>
        {Array.from({length: 7}, (_, i) => <path key={i} d={"M" + (i*190-20) + " 570 L" + (i*190+105) + " " + (420+(i%3)*28) + " L" + (i*190+240) + " 570 Z"} fill={["#333b45","#3d4249","#4a4d50"][i%3]}/>)}
        <path d="M0 610 H1280" stroke="#9c866f" strokeWidth="3"/>
      </>}
    </svg>
  </AbsoluteFill>
);

export const OneMoreScroll: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const idx = Math.min(shots.length - 1, Math.floor(frame / SHOT_FRAMES));
  const local = frame - idx * SHOT_FRAMES;
  const t = Math.max(0, Math.min(1, local / (SHOT_FRAMES - 1)));
  const shot = shots[idx];
  const fadeIn = clampInterpolate(local, [0, 18], [0, 1]);
  const fadeOut = clampInterpolate(local, [SHOT_FRAMES - 18, SHOT_FRAMES - 1], [1, 0]);
  const visibility = Math.min(fadeIn, fadeOut);
  const eased = Easing.inOut(Easing.cubic)(t);
  const x = shot.x0 + (shot.x1 - shot.x0) * eased;
  const walk = shot.pose === "walk";
  const phoneX = x + 58;
  const shadowPulse = shot.shadow * (0.85 + Math.sin(local / fps * 2.4) * 0.15);

  return (
    <AbsoluteFill style={{backgroundColor: "#15171b", color: "#eee7d9", fontFamily: "Arial, Helvetica, sans-serif", overflow: "hidden"}}>
      <Backdrop setting={shot.setting} t={t}/>
      <div style={{position: "absolute", left: 0, top: 0, width: "100%", height: "100%", background: "radial-gradient(ellipse at 50% 45%, transparent 15%, rgba(7,8,10,.48) 100%)"}}/>
      <div style={{position: "absolute", left: x - 110, top: 410, width: 230, height: 150, borderRadius: "50%", background: "radial-gradient(ellipse, rgba(178,54,62," + shadowPulse + ") 0%, rgba(178,54,62," + (shadowPulse * 0.28) + ") 32%, transparent 72%)", transform: "scale(" + (1 + Math.sin(local / 16) * 0.035) + ",.48)", filter: "blur(10px)"}}/>
      <Character x={x} y={shot.y} pose={shot.pose} t={t} scale={1 + Math.sin(local / 20) * 0.004}/>
      {shot.pose === "meet" && <Character x={x + 300} y={0} pose="stand" t={t} scale={0.92}/>}
      {shot.phone && shot.pose !== "scroll" && <div style={{position: "absolute", left: phoneX, top: shot.pose === "sit" ? 360 : 435, width: 16, height: 30, border: "2px solid #bcb5a7", borderRadius: 4, background: "#a9434b", boxShadow: "0 0 16px rgba(169,67,75,.3)", opacity: shot.pose === "write" ? .5 : .9}}/>}
      {shot.setting === "desk" && <div style={{position: "absolute", left: 300, top: 440, width: 122, height: 9, background: "#d7d0c2", transform: "rotate(-4deg)", opacity: .9}}/>}
      <div style={{position: "absolute", left: 0, right: 0, bottom: 0, height: 230, background: "linear-gradient(180deg,transparent,rgba(8,9,11,.78) 34%,rgba(8,9,11,.94))"}}/>
      <div style={{position: "absolute", left: 70, right: 70, bottom: 62, opacity: visibility, transform: "translateY(" + ((1 - fadeIn) * 10) + "px)"}}>
        <div style={{fontSize: 13, letterSpacing: 3, color: "#b9b2a5", marginBottom: 14, fontWeight: 700}}>H2 / SELF-IMPROVEMENT FILM　　{String(idx + 1).padStart(2, "0")} — 08</div>
        <div style={{fontSize: shot.title.length > 22 ? 34 : 43, fontWeight: 800, letterSpacing: 1.2, lineHeight: 1.08, maxWidth: 1000}}>{shot.title}</div>
        <div style={{fontSize: 22, color: "#d0c9bd", marginTop: 12, lineHeight: 1.35}}>{shot.subtitle}</div>
      </div>
      <div style={{position: "absolute", left: 0, right: 0, top: 0, height: 5, background: "#30343a"}}>
        <div style={{height: 5, width: ((idx + t) / shots.length * 100) + "%", background: "#b94e52"}}/>
      </div>
      <div style={{position: "absolute", inset: 0, backgroundColor: "#08090b", opacity: 1 - visibility, pointerEvents: "none"}}/>
    </AbsoluteFill>
  );
};
