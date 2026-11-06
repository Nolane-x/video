import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const FPS = 24;
const SHOT_FRAMES = 9 * FPS;
const DURATION = 45 * FPS;
const PAPER = "#ead9b7";
const INK = "#352d2a";
const RED = "#9b493c";
const ROMAN = "#5c6570";
const CARTHAGE = "#a35b3e";
const OLIVE = "#747c50";

const clamp = (value: number, from: number, to: number) =>
  Math.max(from, Math.min(to, value));
const progress = (frame: number, from = 0, to = SHOT_FRAMES) =>
  interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
const fade = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

const Label: React.FC<{
  x: number; y: number; children: React.ReactNode;
  size?: number; color?: string; anchor?: "start" | "middle" | "end";
  opacity?: number; letterSpacing?: number;
}> = ({x, y, children, size = 28, color = INK, anchor = "start", opacity = 1, letterSpacing = 2}) => (
  <text
    x={x} y={y} textAnchor={anchor} fill={color} opacity={opacity}
    fontFamily="Arial, Helvetica, sans-serif" fontSize={size}
    fontWeight="700" letterSpacing={letterSpacing}
  >
    {children}
  </text>
);

const OliveTree: React.FC<{x:number;y:number;s?:number;phase?:number}> = ({x,y,s=1,phase=0}) => (
  <g transform={\`translate(\${x} \${y}) scale(\${s})\`}>
    <path d="M0 0 Q-10 -72 3 -126" stroke="#554333" strokeWidth="17" fill="none" strokeLinecap="round"/>
    <path d="M0 -58 Q-45 -102 -67 -128 M0 -76 Q50 -105 68 -131 M2 -96 Q-15 -141 -18 -164" stroke="#554333" strokeWidth="9" fill="none" strokeLinecap="round"/>
    {[-1,0,1,2,3].map((n) => (
      <ellipse
        key={n} cx={n*30-25} cy={-125-Math.abs(n-1)*11+Math.sin(phase+n)*3}
        rx={49} ry={23} transform={\`rotate(\${n*13-12} \${n*30-25} \${-125-Math.abs(n-1)*11})\`}
        fill={n%2 ? "#858357" : OLIVE} opacity=".88"
      />
    ))}
  </g>
);

const Soldier: React.FC<{
  x:number;y:number;s?:number;phase?:number;side?:"roman"|"carthage";shield?:boolean;
}> = ({x,y,s=1,phase=0,side="roman",shield=true}) => {
  const swing=Math.sin(phase*Math.PI*2)*13;
  const cloth=side==="roman" ? "#8e5142" : "#a18a55";
  const helmet=side==="roman" ? "#71777a" : "#8e7956";
  return (
    <g transform={\`translate(\${x} \${y}) scale(\${s})\`}>
      <ellipse cx="0" cy="5" rx="32" ry="9" fill="#493e34" opacity=".2"/>
      <path d={\`M-11 -61 L-22 -8 L-12 -4 L-1 -43 L13 -5 L24 -8 L12 -63Z\`} fill="#463d36"/>
      <path d={\`M-7 -5 L-15 31 L-30 48 L-23 54 L-2 39 L6 2 M8 -4 L15 29 L29 42 L22 50 L4 39Z\`} fill="#3c3731" stroke="#3c3731" strokeWidth="7" strokeLinecap="round"/>
      <path d="M-14 -89 Q-26 -68 -20 -36 L20 -36 Q26 -68 14 -89Z" fill={cloth} stroke="#493b33" strokeWidth="4"/>
      <path d="M-12 -76 L-29 -56 L-20 -47 L-4 -65 M12 -76 L30 -55 L22 -46 L5 -65" fill="none" stroke="#493b33" strokeWidth="9" strokeLinecap="round"/>
      <path d={\`M-21 -54 L-\${39+swing} -23 M19 -54 L\${34-swing} -28\`} stroke="#3e3932" strokeWidth="10" strokeLinecap="round"/>
      <circle cx="0" cy="-105" r="22" fill="#b58e6b" stroke="#4b3a32" strokeWidth="4"/>
      <path d="M-23 -110 Q-18 -139 8 -134 Q26 -129 24 -109 L18 -102 Q0 -115 -19 -101Z" fill={helmet} stroke="#4d453c" strokeWidth="4"/>
      <path d="M-5 -127 Q2 -145 11 -138" fill="none" stroke="#bca778" strokeWidth="5"/>
      {shield && (
        <g transform={\`translate(34 -49) rotate(\${-8+swing*.24})\`}>
          <path d="M0 -35 Q31 -42 39 -19 L35 29 Q17 49 0 32 Q-18 48 -35 27 L-38 -19 Q-28 -42 0 -35Z" fill={side==="roman" ? "#69727a" : "#98784e"} stroke="#403b34" strokeWidth="6"/>
          <path d="M0 -31 L0 34 M-26 -8 H26" stroke="#c6b98f" strokeWidth="4" opacity=".8"/>
          <circle cx="0" cy="0" r="7" fill="#d4c8a4"/>
        </g>
      )}
    </g>
  );
};

const Cavalry: React.FC<{x:number;y:number;s?:number;phase:number;direction?:1|-1}> = ({x,y,s=1,phase,direction=1}) => {
  const gait=Math.sin(phase*Math.PI*2);
  return (
    <g transform={\`translate(\${x} \${y}) scale(\${s*direction} \${s})\`}>
      <ellipse cx="0" cy="0" rx="72" ry="17" fill="#564536" opacity=".16"/>
      <path d="M-58 -22 Q-42 -57 -3 -50 L34 -39 Q58 -44 70 -20 L54 4 L28 1 L17 39 L7 40 L3 0 L-23 0 L-38 37 L-50 39 L-43 -5Z" fill="#5a4938" stroke="#40372f" strokeWidth="5"/>
      <path d="M55 -31 Q76 -61 81 -52 L70 -28" fill="#5a4938" stroke="#40372f" strokeWidth="5"/>
      <path d={\`M-39 3 L-\${49+gait*12} 43 M-15 -1 L-\${6-gait*10} 40 M27 -6 L\${37+gait*11} 38 M42 -8 L\${57-gait*9} 31\`} fill="none" stroke="#40372f" strokeWidth="8" strokeLinecap="round"/>
      <path d="M-61 -24 Q-82 -37 -83 -17" fill="none" stroke="#40372f" strokeWidth="7"/>
      <circle cx="4" cy="-78" r="16" fill="#b58d69" stroke="#453b34" strokeWidth="4"/>
      <path d="M-11 -81 Q-9 -101 10 -99 L19 -82Z" fill="#77796f" stroke="#403b34" strokeWidth="4"/>
      <path d="M-1 -61 L-17 -25 M-5 -55 L22 -32" stroke="#473a32" strokeWidth="10" strokeLinecap="round"/>
      <path d="M13 -27 L62 -68" stroke="#73513a" strokeWidth="8" strokeLinecap="round"/>
      <path d="M-10 -60 L-31 -12" stroke="#a35b3e" strokeWidth="8" strokeLinecap="round"/>
    </g>
  );
};

const PaperFrame: React.FC<{title?:string;subtitle?:string;light?:boolean}> = ({title,subtitle,light=false}) => (
  <g>
    <path d="M65 65 H1855 V1015 H65Z" fill="none" stroke={light?"#e8d6b7":"#61513f"} strokeWidth="3" opacity=".6"/>
    {title && <Label x={105} y={125} size={26} color={light?"#f0e4cb":INK}>{title}</Label>}
    {subtitle && <Label x={105} y={970} size={24} color={light?"#f0e4cb":INK}>{subtitle}</Label>}
  </g>
);

const ShotOne: React.FC<{f:number}> = ({f}) => {
  const p=progress(f,10,190);
  const river=progress(f,12,125);
  return (
    <g transform={\`translate(\${-40*p} \${-12*p}) scale(\${1+0.1*p})\`}>
      <rect width="1920" height="1080" fill="#e5d2ad"/>
      <path d="M0 0 H1920 V1080 H0Z" fill="url(#paper)"/>
      <path d="M80 170 Q320 70 590 160 T1120 160 Q1430 90 1840 240 L1800 900 Q1430 1000 1110 910 T520 950 Q260 900 90 790Z" fill="#b5a77d" opacity=".42"/>
      {[0,1,2,3,4,5,6].map((i)=>(
        <path key={i} d={\`M\${90+i*20} \${290+i*64} Q430 \${90+i*75} 800 \${260+i*55} T1800 \${220+i*90}\`} fill="none" stroke="#968762" strokeWidth="4" opacity=".34"/>
      ))}
      <path d="M120 500 Q380 405 630 465 T1040 470 Q1390 400 1800 520" fill="none" stroke="#577e80" strokeWidth="48" opacity=".28"/>
      <path d="M120 500 Q380 405 630 465 T1040 470 Q1390 400 1800 520" fill="none" stroke="#4d8286" strokeWidth="15" strokeLinecap="round" strokeDasharray="2200" strokeDashoffset={2200*(1-river)}/>
      <path d="M210 250 Q440 190 640 280 M1130 760 Q1400 650 1660 780" stroke="#8b7b55" strokeWidth="5" fill="none" opacity=".5"/>
      <g opacity={fade(f,45,80)}>
        <circle cx="1045" cy="469" r="30" fill="#9c493b"/>
        <circle cx="1045" cy="469" r="12" fill="#f4e6ca"/>
      </g>
      <g opacity={fade(f,65,110)}>
        <rect x="550" y="620" width="145" height="48" rx="22" fill="#65717a" stroke="#383c3e" strokeWidth="4"/>
        <rect x="1250" y="330" width="165" height="48" rx="22" fill="#a35b3e" stroke="#543d30" strokeWidth="4"/>
      </g>
      <Label x={110} y={190} size={33}>APULIA</Label>
      <Label x={1190} y={445} size={25} color="#315b62">AUFIDUS</Label>
      <Label x={1090} y={540} size={24} color="#8e4539">CANNAE</Label>
      <g opacity={fade(f,90,130)}>
        <path d="M1060 430 L1048 385" stroke="#9c493b" strokeWidth="4"/>
        <Label x={1070} y={370} size={22} color="#8e4539">BATTLEFIELD</Label>
      </g>
      <PaperFrame title="AUGUST 216 BCE" subtitle="A plain beside the River Aufidus"/>
    </g>
  );
};

const ShotTwo: React.FC<{f:number}> = ({f}) => {
  const p=progress(f,0,215);
  const drift=interpolate(f,[0,215],[0,-80]);
  return (
    <g>
      <rect width="1920" height="1080" fill="#d9c39a"/>
      <path d="M0 0 H1920 V600 Q1550 660 1260 602 T640 620 T0 570Z" fill="#d7bd91"/>
      <path d="M0 492 Q210 360 470 470 T900 440 T1430 460 T1920 410 V760 H0Z" fill="#a4a078"/>
      <path d="M0 640 Q350 570 700 650 T1330 610 T1920 660 V1080 H0Z" fill="#927b59"/>
      {[0,1,2,3,4,5].map(i=><OliveTree key={i} x={90+i*340} y={625+(i%2)*24} s={0.6+(i%3)*.15} phase={f/80+i}/>)}
      <path d="M0 795 Q320 750 620 790 T1210 760 T1920 805 V1080 H0Z" fill="#77684c"/>
      <g transform={\`translate(\${drift} 0)\`}>
        {Array.from({length:7},(_,row)=>Array.from({length:15},(_,col)=>{
          const x=280+col*90+(row%2)*34;
          const y=760+row*37;
          const s=.38+(row%3)*.035;
          return <Soldier key={\`\${row}-\${col}\`} x={x} y={y} s={s} phase={f/40+row*.21+col*.13} side="roman" shield={col%3!==0}/>;
        }))}
        {Array.from({length:12},(_,i)=>(
          <g key={i} transform={\`translate(\${155+i*142} \${680+(i%3)*20})\`}>
            <path d="M0 0 V-115" stroke="#51443a" strokeWidth="9"/>
            <path d="M0 -116 Q38 -137 75 -114 L67 -54 Q25 -75 0 -58Z" fill={i%2?"#a24d3c":"#8f6043"} stroke="#4b3d33" strokeWidth="5"/>
          </g>
        ))}
      </g>
      <g opacity={.28+.1*Math.sin(f/17)}>
        <ellipse cx={520+220*p} cy="870" rx="360" ry="54" fill="#f1ddba"/>
        <ellipse cx={1290-110*p} cy="825" rx="270" ry="38" fill="#f1ddba"/>
      </g>
      <PaperFrame title="THE ROMAN MASS" subtitle="Pressure builds in the centre"/>
    </g>
  );
};

const ShotThree: React.FC<{f:number}> = ({f}) => {
  const wind=progress(f,5,55);
  const contact=fade(f,92,110)*(1-fade(f,128,170));
  const recoil=progress(f,110,175);
  const bladeX=interpolate(f,[0,65,104,128,215],[660,1010,1195,1110,970],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const dust=interpolate(f,[105,138,215],[0,1,0.3],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  return (
    <g>
      <rect width="1920" height="1080" fill="#766752"/>
      <path d="M0 0 H1920 V1080 H0Z" fill="url(#battleShade)"/>
      <path d="M0 780 Q340 620 710 740 T1330 710 T1920 740 V1080 H0Z" fill="#8f7a58"/>
      <path d="M0 945 Q450 855 920 930 T1920 900" fill="none" stroke="#c2a87c" strokeWidth="9" opacity=".32"/>
      <g transform={\`translate(500 790) translate(0 \${-12*recoil})\`}>
        <Soldier x={0} y={0} s={2.45} phase={f/80} side="roman" shield={false}/>
        <path d="M86 -150 Q165 -210 250 -166" stroke="#b8a574" strokeWidth="26" fill="none"/>
        <path d="M70 -126 Q160 -162 260 -115" stroke="#4c4640" strokeWidth="12" fill="none"/>
        <path d="M55 -174 Q115 -195 170 -168" stroke="#d1bd8a" strokeWidth="9" fill="none"/>
      </g>
      <g transform={\`translate(1430 795) translate(0 \${12*recoil})\`}>
        <Soldier x={0} y={0} s={2.3} phase={f/65+0.4} side="carthage" shield={false}/>
        <path d="M-45 -150 Q-105 -193 -190 -170" stroke="#514136" strokeWidth="28" fill="none"/>
        <path d="M-45 -150 Q-105 -193 -190 -170" stroke="#bc9d67" strokeWidth="10" fill="none"/>
        <path d="M-120 -190 L-155 -185 L-198 -159" stroke="#514136" strokeWidth="10" fill="none"/>
      </g>
      <path d={\`M\${bladeX} 430 L\${bladeX+260} 620\`} stroke="#d9d5c7" strokeWidth="19" strokeLinecap="round"/>
      <path d={\`M\${bladeX-25} 418 L\${bladeX+10} 451\`} stroke="#6e4c38" strokeWidth="23" strokeLinecap="round"/>
      <path d="M1000 610 L1200 688" stroke="#42382f" strokeWidth="36" strokeLinecap="round"/>
      <g opacity={contact}>
        <circle cx="1215" cy="625" r="90" fill="none" stroke="#e2ca8d" strokeWidth="13"/>
        <path d="M1145 570 L1285 682 M1285 568 L1145 680" stroke="#f3dfb6" strokeWidth="9"/>
      </g>
      <g opacity={dust}>
        {Array.from({length:18},(_,i)=><circle key={i} cx={1060+Math.sin(i*7)*260} cy={560+Math.cos(i*4)*180} r={10+(i%4)*9} fill="#e8d2a6" opacity={.25+(i%3)*.15}/>)}
      </g>
      <PaperFrame title="THE CENTRE GIVES GROUND" subtitle="The line bends under pressure — it does not simply vanish"/>
    </g>
  );
};

const ShotFour: React.FC<{f:number}> = ({f}) => {
  const p=progress(f,10,205);
  const arc=progress(f,42,194);
  return (
    <g>
      <rect width="1920" height="1080" fill="#cbb88f"/>
      <path d="M0 0 H1920 V1080 H0Z" fill="url(#paper)"/>
      <path d="M150 170 Q500 100 860 185 T1730 210" fill="none" stroke="#928363" strokeWidth="5" opacity=".35"/>
      <path d="M160 860 Q500 720 790 860 T1740 850" fill="none" stroke="#928363" strokeWidth="5" opacity=".35"/>
      <g opacity=".8">
        {Array.from({length:9},(_,row)=>Array.from({length:15},(_,col)=>(
          <g key={\`\${row}-\${col}\`}>
            <rect x={720+col*32} y={380+row*34} width="23" height="27" rx="9" fill={ROMAN} stroke="#3f4448" strokeWidth="2"/>
          </g>
        )))}
      </g>
      <path d={\`M220 270 Q480 70 \${650+180*p} 365\`} fill="none" stroke={CARTHAGE} strokeWidth="22" strokeLinecap="round" strokeDasharray="940" strokeDashoffset={940*(1-arc)}/>
      <path d={\`M1700 280 Q1450 70 \${1290-180*p} 370\`} fill="none" stroke={CARTHAGE} strokeWidth="22" strokeLinecap="round" strokeDasharray="940" strokeDashoffset={940*(1-arc)}/>
      <path d={\`M250 300 Q490 165 \${690+150*p} 425\`} fill="none" stroke="#6e513b" strokeWidth="7" strokeDasharray="19 16" opacity=".9"/>
      <path d={\`M1670 300 Q1440 160 \${1230-150*p} 425\`} fill="none" stroke="#6e513b" strokeWidth="7" strokeDasharray="19 16" opacity=".9"/>
      <g transform={\`translate(\${300+620*arc} \${330+200*arc})\`}>
        <Cavalry x={0} y={0} s={.9} phase={f/60} direction={1}/>
      </g>
      <g transform={\`translate(\${1600-620*arc} \${330+200*arc})\`}>
        <Cavalry x={0} y={0} s={.9} phase={f/53} direction={-1}/>
      </g>
      <Label x={960} y={245} size={32} anchor="middle" color="#4c514f" opacity={fade(f,25,65)}>THE TWO WINGS TURN INWARD</Label>
      <Label x={960} y={890} size={26} anchor="middle" color="#7d4938">SCHEMATIC TACTICAL VIEW</Label>
      <PaperFrame title="THE WINGS TURN" subtitle="Cavalry movement threatens the exposed rear"/>
    </g>
  );
};

const ShotFive: React.FC<{f:number}> = ({f}) => {
  const close=progress(f,20,190);
  const camera=interpolate(f,[0,215],[1,1.12]);
  return (
    <g transform={\`translate(\${-110*(camera-1)} \${-35*(camera-1)}) scale(\${camera})\`}>
      <rect width="1920" height="1080" fill="#9c8c70"/>
      <path d="M0 0 H1920 V1080 H0Z" fill="url(#battleShade)"/>
      <path d="M0 620 Q300 510 690 620 T1310 615 T1920 590 V1080 H0Z" fill="#a28c67"/>
      <path d="M80 750 Q400 430 780 390 Q960 365 1130 390 Q1510 420 1830 750" fill="none" stroke={CARTHAGE} strokeWidth="64" strokeLinecap="round" opacity=".9"/>
      <path d={\`M80 750 Q400 430 780 390 Q960 365 1130 390 Q1510 420 1830 750\`} fill="none" stroke="#e3c79a" strokeWidth="8" strokeDasharray="24 22" strokeDashoffset={-close*360}/>
      {Array.from({length:9},(_,row)=>Array.from({length:16},(_,col)=>(
        <g key={\`\${row}-\${col}\`}>
          <rect x={600+col*38} y={520+row*36} width="27" height="30" rx="8" fill={ROMAN} stroke="#383d40" strokeWidth="3"/>
          <path d={\`M\${613+col*38} \${523+row*36} v24\`} stroke="#d4c39d" strokeWidth="3"/>
        </g>
      )))}
      <g opacity={close}>
        <path d="M600 860 Q940 1030 1320 860" fill="none" stroke="#8a4438" strokeWidth="28" strokeDasharray="20 22"/>
        <path d="M520 760 Q960 990 1400 760" fill="none" stroke="#e1c39b" strokeWidth="8" strokeDasharray="12 19"/>
      </g>
      <rect x="0" y="0" width="1920" height="1080" fill="#241f20" opacity={fade(f,165,205)*.5}/>
      <g opacity={fade(f,165,200)}>
        <Label x={960} y={430} anchor="middle" size={62} color="#f0dfbd">THE WINGS CLOSE</Label>
        <Label x={960} y={510} anchor="middle" size={30} color="#f0dfbd" letterSpacing={5}>CANNAE · 2 AUGUST 216 BCE</Label>
        <Label x={960} y={600} anchor="middle" size={24} color="#d6c39e" letterSpacing={2}>THE CENTRE BENDS. THE FLANKS CLOSE.</Label>
      </g>
    </g>
  );
};

export const IllustratedHistoryCannae45s: React.FC = () => {
  const frame=useCurrentFrame();
  const {width,height}=useVideoConfig();
  const scene=clamp(Math.floor(frame/SHOT_FRAMES),0,4);
  const local=frame-scene*SHOT_FRAMES;
  return (
    <AbsoluteFill style={{backgroundColor:PAPER,overflow:"hidden"}}>
      <svg width={width} height={height} viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
        <defs>
          <linearGradient id="paper" x1="0" y1="0" x2="0.8" y2="1">
            <stop offset="0%" stopColor="#f0e2c4"/>
            <stop offset="55%" stopColor="#e6d3ad"/>
            <stop offset="100%" stopColor="#cdbb94"/>
          </linearGradient>
          <linearGradient id="battleShade" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#b6a17d"/>
            <stop offset="56%" stopColor="#8b795e"/>
            <stop offset="100%" stopColor="#534a3f"/>
          </linearGradient>
          <pattern id="paperFibres" width="58" height="58" patternUnits="userSpaceOnUse">
            <path d="M0 13 L17 11 M30 40 L51 38 M8 55 L19 54" stroke="#745f44" strokeWidth="1.5" opacity=".09"/>
            <circle cx="42" cy="17" r="1.2" fill="#6b573e" opacity=".12"/>
            <circle cx="14" cy="31" r=".9" fill="#6b573e" opacity=".1"/>
          </pattern>
          <filter id="softDust">
            <feGaussianBlur stdDeviation="12"/>
          </filter>
        </defs>
        <rect width="1920" height="1080" fill="url(#paperFibres)" opacity=".75"/>
        {scene===0 && <ShotOne f={local}/>}
        {scene===1 && <ShotTwo f={local}/>}
        {scene===2 && <ShotThree f={local}/>}
        {scene===3 && <ShotFour f={local}/>}
        {scene===4 && <ShotFive f={local}/>}
        <rect width="1920" height="1080" fill="url(#paperFibres)" opacity=".42" pointerEvents="none"/>
        <rect x="24" y="24" width="1872" height="1032" fill="none" stroke="#5c4b39" strokeWidth="3" opacity=".32"/>
      </svg>
    </AbsoluteFill>
  );
};
