import React from "react";
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from "remotion";

type Pose = "scroll" | "slump" | "stand" | "walk" | "write" | "meet" | "hero";
type Setting = "bedroom" | "street" | "calendar" | "void" | "desk" | "stairs" | "hall" | "dawn";
type Shot = {
  title: string;
  subtitle: string;
  setting: Setting;
  pose: Pose;
  x0: number;
  x1: number;
  y: number;
  shadow: number;
  attention: number;
  shirt: string;
  phone?: boolean;
  friend?: boolean;
};

const SHOT_FRAMES = 180;
const shots: Shot[] = [
  {title: "ONE MORE SCROLL", subtitle: "It starts with one more scroll.", setting: "bedroom", pose: "scroll", x0: 690, x1: 690, y: 0, shadow: 0.92, attention: 100, shirt: "#c56d9b", phone: true},
  {title: "JUST ONE MINUTE", subtitle: "The next scroll never feels like the last.", setting: "street", pose: "scroll", x0: 700, x1: 775, y: 0, shadow: 0.85, attention: 79, shirt: "#c8745d", phone: true},
  {title: "THE DAYS DISAPPEAR", subtitle: "Time keeps moving while you stay still.", setting: "calendar", pose: "slump", x0: 555, x1: 520, y: 0, shadow: 0.69, attention: 55, shirt: "#c8745d"},
  {title: "RESET TO ZERO", subtitle: "A reset can be the first honest decision.", setting: "void", pose: "stand", x0: 610, x1: 660, y: 0, shadow: 0.51, attention: 24, shirt: "#c8745d"},
  {title: "START SMALL", subtitle: "Put the phone down. Open one page.", setting: "desk", pose: "write", x0: 500, x1: 535, y: 0, shadow: 0.39, attention: 32, shirt: "#c8745d", phone: true},
  {title: "SHOW UP AGAIN", subtitle: "Progress is a direction, not a perfect streak.", setting: "stairs", pose: "walk", x0: 340, x1: 815, y: -18, shadow: 0.25, attention: 55, shirt: "#c8745d"},
  {title: "YOU ARE NOT ALONE", subtitle: "Some things become lighter when shared.", setting: "hall", pose: "meet", x0: 495, x1: 575, y: 0, shadow: 0.14, attention: 77, shirt: "#c8745d", friend: true},
  {title: "YOUR ATTENTION IS YOUR LIFE", subtitle: "Choose what gets a piece of it.", setting: "dawn", pose: "hero", x0: 650, x1: 680, y: -8, shadow: 0.05, attention: 92, shirt: "#c8745d"}
];

const clampInterpolate = (value: number, input: number[], output: number[]) =>
  interpolate(value, input, output, {extrapolateLeft: "clamp", extrapolateRight: "clamp"});

const Window: React.FC<{x: number; y: number; warm?: boolean; w?: number; h?: number}> = ({x, y, warm = false, w = 76, h = 94}) => (
  <g>
    <rect x={x - 7} y={y - 7} width={w + 14} height={h + 14} rx="2" fill="#181820" stroke="#403844" strokeWidth="4"/>
    <rect x={x} y={y} width={w} height={h} fill={warm ? "#d99d68" : "#292630"}/>
    {warm && <rect x={x + 4} y={y + 4} width={w - 8} height={h - 8} fill="#f1c28b" opacity=".48"/>}
    <path d={`M${x + w / 2} ${y} V${y + h} M${x} ${y + h / 2} H${x + w}`} stroke="#443744" strokeWidth="5"/>
    {warm && <rect x={x + 6} y={y + 6} width={w - 12} height="8" fill="#ffe0a7" opacity=".3"/>}
  </g>
);

const FlowerPot: React.FC<{x: number; y: number; scale?: number}> = ({x, y, scale = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${scale})`}>
    <path d="M-34 0 L34 0 L25 45 L-25 45Z" fill="#8d5947" stroke="#574047" strokeWidth="3"/>
    <ellipse cx="0" cy="0" rx="35" ry="9" fill="#4c5b40"/>
    {Array.from({length: 7}, (_, i) => {
      const px = -25 + i * 8;
      const py = -11 - (i % 3) * 8;
      return <g key={i}>
        <path d={`M${px} 0 Q${px - 4} -18 ${px - 1} ${py}`} stroke="#385340" strokeWidth="3" fill="none"/>
        <circle cx={px} cy={py} r={5 + (i % 2)} fill={i % 2 ? "#cb7180" : "#d98791"}/>
        <circle cx={px - 2} cy={py - 2} r="1.8" fill="#f4c0ae" opacity=".75"/>
      </g>;
    })}
  </g>
);

const StreetLamp: React.FC<{x: number; y: number}> = ({x, y}) => (
  <g>
    <path d={`M${x} ${y} V${y - 160} Q${x} ${y - 185} ${x + 25} ${y - 185} H${x + 52}`} stroke="#211d27" strokeWidth="11" fill="none" strokeLinecap="round"/>
    <path d={`M${x + 18} ${y - 184} H${x + 63} L${x + 72} ${y - 170} H${x + 15}Z`} fill="#3b3340" stroke="#796174" strokeWidth="2"/>
    <ellipse cx={x + 43} cy={y - 169} rx="34" ry="23" fill="#f5c684" opacity=".08"/>
    <ellipse cx={x + 43} cy={y - 169} rx="18" ry="12" fill="#f6d9a4" opacity=".19"/>
    <circle cx={x + 43} cy={y - 169} r="5" fill="#ffe4ae"/>
    <path d={`M${x - 13} ${y} H${x + 13}`} stroke="#211d27" strokeWidth="8" strokeLinecap="round"/>
  </g>
);

const Backdrop: React.FC<{setting: Setting; t: number; frame: number}> = ({setting, t, frame}) => {
  const shift = Math.sin(frame / 180 * Math.PI) * 9;
  const dawn = setting === "dawn";
  const interior = setting === "bedroom" || setting === "desk" || setting === "calendar";
  return (
    <AbsoluteFill style={{overflow: "hidden", background: dawn ? "linear-gradient(180deg,#34313e 0%,#655365 49%,#c69c83 100%)" : "linear-gradient(180deg,#24212c 0%,#3a303c 57%,#29252f 100%)"}}>
      <svg width="100%" height="100%" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMid slice" style={{position:"absolute"}}>
        <defs>
          <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#38303c"/>
            <stop offset="70%" stopColor="#4b3a49"/>
            <stop offset="100%" stopColor="#342b38"/>
          </linearGradient>
          <linearGradient id="streetFloor" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#51404d"/>
            <stop offset="100%" stopColor="#29252e"/>
          </linearGradient>
          <radialGradient id="warmWindow">
            <stop offset="0%" stopColor="#f5d2a0" stopOpacity=".8"/>
            <stop offset="100%" stopColor="#f5b874" stopOpacity="0"/>
          </radialGradient>
          <filter id="softBackdrop"><feGaussianBlur stdDeviation="1.35"/></filter>
          <filter id="lampGlow"><feGaussianBlur stdDeviation="10"/></filter>
          <linearGradient id="dawnLight" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#f3c39d" stopOpacity=".38"/>
            <stop offset="100%" stopColor="#f3c39d" stopOpacity="0"/>
          </linearGradient>
        </defs>
        <g transform={`translate(${shift} 0)`}>
          {/* Distant apartment blocks give the frame a real location and scale. */}
          <g opacity=".74" filter="url(#softBackdrop)">
            <path d="M-50 32 H320 V500 H-50Z" fill="#282531"/>
            <path d="M330 0 H535 V520 H330Z" fill="#312936"/>
            <path d="M920 18 H1325 V512 H920Z" fill="#292531"/>
            <Window x={35} y={56} warm={false} w={70} h={108}/>
            <Window x={152} y={56} warm={false} w={70} h={108}/>
            <Window x={362} y={45} warm={false} w={62} h={96}/>
            <Window x={970} y={52} warm={false} w={84} h={105}/>
            <Window x={1112} y={52} warm={false} w={84} h={105}/>
            <Window x={1230} y={52} warm={false} w={72} h={105}/>
          </g>
          {/* Main facade: layered windows, mullions, balcony, doors and masonry. */}
          <rect x="-10" y="0" width="1300" height="526" fill="url(#wall)"/>
          <path d="M0 215 H1280 M0 465 H1280" stroke="#211e28" strokeWidth="15" opacity=".8"/>
          <path d="M0 222 H1280 M0 472 H1280" stroke="#796275" strokeWidth="3" opacity=".43"/>
          <rect x="0" y="0" width="18" height="526" fill="#6b5067" opacity=".45"/>
          <rect x="515" y="0" width="8" height="526" fill="#d8a6c1" opacity=".85"/>
          <rect x="930" y="0" width="7" height="526" fill="#a9769b" opacity=".42"/>
          <Window x={46} y={267} warm={!dawn} w={138} h={174}/>
          <Window x={555} y={267} warm={!dawn} w={136} h={174}/>
          <Window x={960} y={267} warm={!dawn} w={164} h={174}/>
          <Window x={1164} y={267} warm={dawn} w={126} h={174}/>
          <Window x={350} y={56} warm={false} w={74} h={110}/>
          <Window x={590} y={38} warm={!dawn} w={78} h={124}/>
          <Window x={716} y={38} warm={!dawn} w={78} h={124}/>
          <Window x={842} y={38} warm={false} w={78} h={124}/>
          <Window x={1046} y={38} warm={false} w={72} h={124}/>
          {/* Balcony and railing: tiny human details make the background believable. */}
          <rect x="542" y="164" width="175" height="7" fill="#211e28"/>
          <rect x="548" y="164" width="5" height="30" fill="#211e28"/>
          {Array.from({length:8},(_,i)=><rect key={i} x={564+i*19} y="169" width="3.5" height="29" fill="#211e28"/>)}
          <rect x="536" y="195" width="186" height="6" fill="#211e28"/>
          {/* Door and short steps. */}
          <rect x="300" y="253" width="142" height="220" fill="#2a2530" stroke="#27212d" strokeWidth="9"/>
          <rect x="324" y="276" width="94" height="186" fill="#211e29" stroke="#493949" strokeWidth="4"/>
          <rect x="345" y="297" width="54" height="96" fill="#d79d69" opacity=".91"/>
          <rect x="351" y="303" width="42" height="84" fill="#f3c38c" opacity=".44"/>
          <circle cx="404" cy="412" r="5" fill="#e3b77c"/>
          <path d="M275 490 H467 V508 H275Z M254 508 H487 V526 H254Z M232 526 H510 V544 H232Z" fill="#4b4050" stroke="#2a2530" strokeWidth="4"/>
          <path d="M270 491 H466 M250 509 H485 M230 527 H508" stroke="#877187" strokeWidth="2" opacity=".55"/>
          {/* Street floor and warm reflections. */}
          <rect x="-20" y="544" width="1320" height="190" fill="url(#streetFloor)"/>
          <path d="M0 550 H1280" stroke="#5c4858" strokeWidth="4"/>
          <path d="M0 592 H1280" stroke="#776175" strokeWidth="2" opacity=".35"/>
          <path d="M500 549 L560 549 L640 720 L590 720Z" fill="url(#dawnLight)" opacity={dawn ? .6 : .15}/>
          <path d="M40 630 Q190 608 300 638 M850 637 Q1000 606 1190 634" fill="none" stroke="#b68d91" strokeWidth="3" opacity=".16"/>
          {/* Plants by the entrance, with visible leaves and flowers. */}
          <FlowerPot x={257} y={475} scale={1.05}/>
          <FlowerPot x={1198} y={475} scale={1.1}/>
          <StreetLamp x={890} y={544}/>
          {/* Background mood light is localized, never a full-frame neon glow. */}
          <ellipse cx={650} cy={305} rx={118} ry={166} fill="url(#warmWindow)" opacity={dawn ? .28 : .2} filter="url(#lampGlow)"/>
          {dawn && <circle cx="1020" cy="236" r="76" fill="#f0c49f" opacity=".7"/>}
          {/* Story-specific props. */}
          {setting === "bedroom" && <>
            <rect x="74" y="378" width="365" height="112" rx="9" fill="#403744" stroke="#776478" strokeWidth="4"/>
            <rect x="87" y="391" width="128" height="54" rx="9" fill="#8d7c93" opacity=".85"/>
            <path d="M220 390 Q306 421 425 393 L425 478 H220Z" fill="#6b6178"/>
            <rect x="445" y="420" width="18" height="123" fill="#322b39"/>
            <rect x="420" y="416" width="76" height="10" rx="4" fill="#645568"/>
            <circle cx="458" cy="405" r="7" fill="#f2d4a3"/>
          </>}
          {setting === "calendar" && <>
            <rect x="814" y="90" width="286" height="275" rx="3" fill="#c9bcae" stroke="#473746" strokeWidth="8"/>
            <rect x="814" y="90" width="286" height="45" fill="#9e7b8d"/>
            <text x="835" y="120" fontSize="19" fontWeight="700" fill="#2b2530" letterSpacing="2">THIS MONTH</text>
            {Array.from({length:28},(_,i)=><g key={i}>
              <rect x={832+(i%7)*37} y={151+Math.floor(i/7)*49} width="26" height="32" rx="2" fill={i<14?"#bb7a79":"#a89a9b"}/>
              {i<14&&<path d={`M${837+(i%7)*37} ${165+Math.floor(i/7)*49} l5 5 l8 -11`} stroke="#f0d5c0" strokeWidth="2" fill="none"/>}
            </g>)}
          </>}
          {setting === "desk" && <>
            <path d="M90 436 H625 V458 H90Z" fill="#705b65" stroke="#302934" strokeWidth="4"/>
            <path d="M122 458 V545 M592 458 V545" stroke="#302934" strokeWidth="16"/>
            <rect x="292" y="362" width="154" height="91" rx="5" fill="#22232d" stroke="#8a7688" strokeWidth="5"/>
            <rect x="302" y="372" width="134" height="70" fill="#6b7b88"/>
            <path d="M302 428 L337 397 L365 417 L394 387 L436 424 V442 H302Z" fill="#a4b5bd" opacity=".65"/>
            <path d="M270 454 H466 L452 465 H284Z" fill="#a9999d"/>
            <rect x="495" y="429" width="68" height="10" rx="3" fill="#c4b7a6" transform="rotate(-4 495 429)"/>
            <path d="M508 427 l10 -18 l12 18" fill="none" stroke="#cab9a9" strokeWidth="3"/>
          </>}
          {setting === "stairs" && <>
            {Array.from({length:7},(_,i)=><path key={i} d={`M${730+i*62} ${540-i*42} h70 v42 h-70Z`} fill={i%2?"#57495a":"#4b4052"} stroke="#302936" strokeWidth="3"/>)}
            <path d="M718 540 L1138 294" stroke="#ae92a5" strokeWidth="5" opacity=".55"/>
            <path d="M731 525 L1148 281" stroke="#2d2532" strokeWidth="8"/>
          </>}
          {setting === "hall" && <>
            <path d="M0 62 L230 180 V544 H0Z" fill="#292530" opacity=".85"/>
            <path d="M1280 40 L1045 180 V544 H1280Z" fill="#28242e" opacity=".8"/>
            <path d="M230 180 H1045" stroke="#5f4d62" strokeWidth="7"/>
            <rect x="740" y="229" width="18" height="192" fill="#211e27"/>
            <rect x="740" y="222" width="128" height="12" fill="#211e27"/>
            <Window x={778} y={270} warm={true} w={74} h={145}/>
          </>}
          {setting === "void" && <>
            <rect x="0" y="0" width="1280" height="545" fill="#201e29" opacity=".55"/>
            {Array.from({length:26},(_,i)=><circle key={i} cx={(i*173+37)%1280} cy={(i*67+41)%500} r={i%4===0?2:1} fill="#c1aebc" opacity=".22"/>)}
          </>}
        </g>
      </svg>
    </AbsoluteFill>
  );
};

const ShadowFigure: React.FC<{x: number; strength: number; frame: number}> = ({x, strength, frame}) => {
  const breathe = 1 + Math.sin(frame / 22) * 0.014;
  return (
    <svg width="460" height="520" viewBox="0 0 460 520" style={{position:"absolute",left:x-230,top:22,opacity:strength,transform:`scale(${breathe},1)`,transformOrigin:"50% 100%",filter:"blur(1.1px)",pointerEvents:"none"}}>
      <defs><linearGradient id="shadowEdge" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#201a28"/><stop offset="100%" stopColor="#17151f"/></linearGradient><radialGradient id="streetLight"><stop offset="0%" stopColor="#f6d8a6" stopOpacity=".9"/><stop offset="100%" stopColor="#f6d8a6" stopOpacity="0"/></radialGradient></defs>
      <ellipse cx="246" cy="132" rx="97" ry="105" fill="url(#shadowEdge)"/>
      <path d="M167 228 Q107 254 101 334 L75 494 Q223 518 365 494 L345 324 Q337 245 286 224Z" fill="#17151f"/>
      <path d="M180 231 Q222 253 284 228" fill="none" stroke="#5c465e" strokeWidth="4" opacity=".25"/>
      <ellipse cx="117" cy="236" rx="54" ry="48" fill="url(#streetLight)" opacity=".72"/>
      <ellipse cx="117" cy="236" rx="8" ry="5" fill="#ffe3b0" opacity=".75"/>
    </svg>
  );
};

const Character: React.FC<{x: number; y: number; pose: Pose; t: number; shirt: string; scale?: number; companion?: boolean}> = ({
  x, y, pose, t, shirt, scale = 1, companion = false
}) => {
  const walking = pose === "walk" || (pose === "meet" && companion);
  const phase = t * Math.PI * 4.4;
  const swing = walking ? Math.sin(phase) : 0;
  const bob = walking ? -Math.abs(Math.sin(phase)) * 4.5 : pose === "scroll" ? Math.sin(t * Math.PI * 2) * 1.7 : 0;
  const lean = pose === "slump" ? 11 : pose === "scroll" ? 7 : pose === "hero" ? -4 : 0;
  const headTilt = pose === "scroll" ? 14 : pose === "slump" ? 22 : pose === "hero" ? -5 : pose === "meet" && !companion ? -8 : 0;
  const leftArm = pose === "scroll" ? -50 : pose === "write" ? -65 : pose === "slump" ? 25 : pose === "hero" ? -32 : walking ? -18 + swing * 27 : pose === "meet" && !companion ? -35 : -8;
  const rightArm = pose === "scroll" ? 39 : pose === "write" ? 14 : pose === "slump" ? 36 : pose === "hero" ? 20 : walking ? 18 - swing * 27 : pose === "meet" && companion ? -30 : 9;
  const leftLeg = walking ? -22 + swing * 31 : pose === "scroll" || pose === "slump" ? 9 : pose === "write" ? 3 : 0;
  const rightLeg = walking ? 22 - swing * 31 : pose === "scroll" || pose === "slump" ? 15 : pose === "write" ? -4 : 0;
  const mouth = pose === "slump" ? "M-7 -137 Q0 -142 7 -137" : pose === "hero" ? "M-8 -137 Q0 -129 8 -137" : pose === "scroll" ? "M-6 -139 Q0 -137 6 -139" : "M-7 -137 H7";
  const handY = pose === "scroll" ? -70 : pose === "write" ? -50 : pose === "slump" ? -46 : -40;
  return (
    <svg width="180" height="270" viewBox="-90 -210 180 270" style={{position:"absolute",left:x-90*scale,top:323+y+bob-247*(scale-1),width:180*scale,height:270*scale,overflow:"visible",transformOrigin:"50% 100%",zIndex:4}}>
      {/* Ground contact shadow keeps feet anchored to the environment. */}
      <ellipse cx="0" cy="28" rx={walking?39:32} ry="7" fill="#17151f" opacity=".45"/>
      {/* Legs use a warm outline and a dark inner stroke, matching the reference style. */}
      <g transform={`rotate(${leftLeg} -15 -38)`}>
        <path d="M-15 -38 L-20 -4 L-35 20" fill="none" stroke="#e7d4bd" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M-15 -38 L-20 -4 L-35 20" fill="none" stroke="#24212b" strokeWidth="11" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M-45 23 Q-40 16 -29 21 L-16 30 Q-13 35 -20 37 L-43 32 Q-50 29 -45 23Z" fill="#24212b" stroke="#e7d4bd" strokeWidth="3"/>
      </g>
      <g transform={`rotate(${rightLeg} 15 -38)`}>
        <path d="M15 -38 L22 -4 L34 20" fill="none" stroke="#e7d4bd" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M15 -38 L22 -4 L34 20" fill="none" stroke="#24212b" strokeWidth="11" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M25 23 Q32 16 42 21 L54 29 Q58 34 50 37 L27 32 Q21 29 25 23Z" fill="#24212b" stroke="#e7d4bd" strokeWidth="3"/>
      </g>
      {/* Torso is a clean, colored silhouette rather than a realistic human body. */}
      <g transform={`rotate(${lean} 0 -82)`}>
        <path d="M-20 -119 Q-34 -112 -32 -82 L-28 -39 Q0 -32 28 -39 L32 -82 Q34 -112 20 -119Z" fill={shirt} stroke="#e6d2bd" strokeWidth="3.2" strokeLinejoin="round"/>
        <path d="M-13 -109 Q-19 -91 -15 -71" fill="none" stroke="#f2c9bd" strokeWidth="2.2" opacity=".42"/>
        <path d="M-10 -55 H10" stroke="#8a4b5f" strokeWidth="2.2" opacity=".55"/>
        <path d="M-4 -104 V-82" stroke="#f0d5c1" strokeWidth="2.2" opacity=".8"/>
        <circle cx="-4" cy="-78" r="2.3" fill="#f4dfca"/>
      </g>
      {/* Shoulder-to-hand joint action: anticipation, action and recovery come from pose-specific angles. */}
      <g transform={`rotate(${leftArm} -24 -105)`}>
        <path d="M-24 -105 Q-42 -88 -46 -70 L-49 -48" fill="none" stroke="#e7d4bd" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M-24 -105 Q-42 -88 -46 -70 L-49 -48" fill="none" stroke={shirt} strokeWidth="11" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx="-49" cy={handY} r="8.5" fill="#24212b" stroke="#e7d4bd" strokeWidth="3"/>
      </g>
      <g transform={`rotate(${rightArm} 24 -105)`}>
        <path d="M24 -105 Q42 -87 47 -68 L50 -47" fill="none" stroke="#e7d4bd" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M24 -105 Q42 -87 47 -68 L50 -47" fill="none" stroke={shirt} strokeWidth="11" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx="50" cy={handY} r="8.5" fill="#24212b" stroke="#e7d4bd" strokeWidth="3"/>
      </g>
      {/* Near-black face with a thin light rim; expression stays readable at YouTube scale. */}
      <g transform={`rotate(${headTilt} 0 -154)`}>
        <circle cx="0" cy="-154" r="37" fill="#17151e" stroke="#ead6bf" strokeWidth="3.2"/>
        <ellipse cx="-12" cy="-156" rx="4.1" ry={pose === "slump" ? 2.8 : 5.2} fill="#f5eee3"/>
        <ellipse cx="12" cy="-156" rx="4.1" ry={pose === "slump" ? 2.8 : 5.2} fill="#f5eee3"/>
        <circle cx="-11" cy="-157" r="1.5" fill="#29242d"/>
        <circle cx="13" cy="-157" r="1.5" fill="#29242d"/>
        <path d={mouth} fill="none" stroke="#f5eee3" strokeWidth={pose === "slump" ? 2 : 2.7} strokeLinecap="round"/>
        {pose === "slump" && <path d="M-22 -176 L-9 -180 M8 -180 L22 -176" stroke="#f5eee3" strokeWidth="3" strokeLinecap="round"/>}
        {(pose === "meet" && !companion) && <path d="M-19 -178 L-8 -181 M8 -181 L19 -178" stroke="#f5eee3" strokeWidth="2.5" strokeLinecap="round"/>}
        {pose === "hero" && <path d="M-18 -179 L-8 -177 M8 -177 L18 -179" stroke="#f5eee3" strokeWidth="2.5" strokeLinecap="round"/>}
      </g>
      {pose === "scroll" && !companion && <>
        <g transform="translate(47 -59) rotate(-12)">
          <rect x="-11" y="-25" width="22" height="42" rx="4" fill="#17151e" stroke="#e7d4bd" strokeWidth="2.5"/>
          <rect x="-7.5" y="-19" width="15" height="28" rx="2" fill="#a84f65"/>
          <circle cx="0" cy="12" r="1.8" fill="#e7d4bd"/>
        </g>
        <path d="M55 -90 Q68 -80 65 -67" stroke="#f3d8a4" strokeWidth="2" fill="none" opacity={.35 + Math.sin(t*14)*.12}/>
      </>}
      {pose === "write" && !companion && <path d="M48 -52 L62 -37" stroke="#ead6bf" strokeWidth="4" strokeLinecap="round"/>}
      {pose === "hero" && !companion && <path d="M-55 -74 l-11 -8 M-49 -86 l-4 -14 M55 -74 l11 -8 M49 -86 l4 -14" stroke="#f2d0a0" strokeWidth="3" strokeLinecap="round" opacity=".7"/>}
    </svg>
  );
};

const AttentionMeter: React.FC<{value: number}> = ({value}) => {
  const needle = -125 + value * 2.5;
  return (
    <div style={{position:"absolute",left:50,top:22,width:238,height:76,background:"rgba(27,23,34,.88)",border:"2px solid #9c8063",borderRadius:19,boxShadow:"0 5px 18px rgba(0,0,0,.24)",display:"flex",alignItems:"center",zIndex:10,color:"#e9d7c0"}}>
      <svg width="82" height="65" viewBox="0 0 82 65" style={{marginLeft:4}}>
        <path d="M15 49 A28 28 0 0 1 68 49" stroke="#4a414f" strokeWidth="8" fill="none" strokeLinecap="round"/>
        <path d="M15 49 A28 28 0 0 1 68 49" stroke="#c2a172" strokeWidth="2" fill="none" opacity=".8"/>
        {Array.from({length:7},(_,i)=><path key={i} d="M0 -3 V3" transform={`translate(${18+i*7.6} ${48-Math.sin((i/6)*Math.PI)*24}) rotate(${-45+i*15} ${18+i*7.6} ${48-Math.sin((i/6)*Math.PI)*24})`} stroke="#d9b883" strokeWidth="2" opacity=".8"/>)}
        <path d="M41 47 L61 36" stroke="#e7d6bf" strokeWidth="3.5" strokeLinecap="round" transform={`rotate(${needle} 41 47)`}/>
        <circle cx="41" cy="47" r="4.5" fill="#e7d6bf"/>
      </svg>
      <div style={{paddingLeft:11,lineHeight:1}}>
        <div style={{fontSize:12,fontWeight:800,letterSpacing:2,color:"#bea57f",marginBottom:8}}>ATTENTION</div>
        <div style={{fontSize:29,fontWeight:800,letterSpacing:1,color:"#f0e4d5"}}>{Math.round(value).toString().padStart(2,"0")}</div>
      </div>
    </div>
  );
};

export const OneMoreScroll: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const idx = Math.min(shots.length - 1, Math.floor(frame / SHOT_FRAMES));
  const local = frame - idx * SHOT_FRAMES;
  const t = Math.max(0, Math.min(1, local / (SHOT_FRAMES - 1)));
  const shot = shots[idx];
  const fadeIn = clampInterpolate(local, [0, 12], [0, 1]);
  const fadeOut = clampInterpolate(local, [SHOT_FRAMES - 12, SHOT_FRAMES - 1], [1, 0]);
  const visibility = Math.min(fadeIn, fadeOut);
  const eased = Easing.inOut(Easing.cubic)(t);
  const x = shot.x0 + (shot.x1 - shot.x0) * eased;
  const cameraZoom = 1.015 + Math.sin(t * Math.PI) * (idx === 2 || idx === 7 ? 0.035 : 0.015);
  const cameraShift = (t - .5) * (idx === 5 ? -26 : idx === 6 ? 14 : 6);
  const attention = clampInterpolate(frame, [idx * SHOT_FRAMES, (idx + 1) * SHOT_FRAMES - 1], [shot.attention, shots[Math.min(idx + 1, shots.length - 1)].attention]);
  const ghostX = idx === 0 ? 890 : idx < 3 ? 930 : idx < 5 ? 865 : idx < 7 ? 1015 : 1080;

  return (
    <AbsoluteFill style={{backgroundColor:"#211f29",color:"#f0e5d7",fontFamily:"Arial, Helvetica, sans-serif",overflow:"hidden"}}>
      <div style={{position:"absolute",inset:-20,transform:`translateX(${cameraShift}px) scale(${cameraZoom})`,transformOrigin:"50% 55%"}}>
        <Backdrop setting={shot.setting} t={t} frame={frame}/>
        <ShadowFigure x={ghostX} strength={shot.shadow} frame={frame}/>
        <div style={{position:"absolute",left:0,right:0,bottom:126,height:110,background:"linear-gradient(180deg,transparent,rgba(17,15,22,.16))",pointerEvents:"none"}}/>
        {/* Companion stays behind the protagonist and shares the same ground plane. */}
        {shot.friend && <Character x={x+236} y={0} pose="meet" t={t} shirt="#6e59bd" scale={1.22} companion/>}
        <Character x={x} y={shot.y} pose={shot.pose} t={t} shirt={shot.shirt} scale={1.45}/>
        {/* A restrained pool of warm light anchors the characters to the street. */}
        <div style={{position:"absolute",left:x-105,top:572,width:210,height:22,borderRadius:"50%",background:"rgba(234,190,145,.08)",filter:"blur(8px)"}}/>
      </div>
      <AttentionMeter value={attention}/>
      <div style={{position:"absolute",left:0,right:0,top:0,height:4,background:"rgba(20,18,26,.42)",zIndex:8}}>
        <div style={{height:4,width:`${((idx+t)/shots.length)*100}%`,background:"#c48b79",opacity:.88}}/>
      </div>
      {/* Small cinematic subtitle, not a giant headline covering the action. */}
      <div style={{position:"absolute",left:100,right:100,bottom:31,display:"flex",justifyContent:"center",opacity:visibility,zIndex:12}}>
        <div style={{maxWidth:1080,padding:"12px 24px",borderRadius:8,background:"rgba(20,18,25,.72)",border:"1px solid rgba(229,204,181,.18)",boxShadow:"0 7px 22px rgba(0,0,0,.15)",textAlign:"center"}}>
          <div style={{fontSize:12,fontWeight:700,letterSpacing:3,color:"#c9a98d",marginBottom:5}}>{shot.title}</div>
          <div style={{fontSize:20,fontWeight:500,color:"#f0e7dc",letterSpacing:.15}}>{shot.subtitle}</div>
        </div>
      </div>
      <div style={{position:"absolute",inset:0,backgroundColor:"#14121a",opacity:1-visibility,pointerEvents:"none",zIndex:20}}/>
    </AbsoluteFill>
  );
};
