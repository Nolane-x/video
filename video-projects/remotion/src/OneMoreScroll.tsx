import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Pose = "scroll" | "slump" | "stand" | "walk" | "run" | "write" | "meet" | "hero" | "tired" | "sit" | "stretch" | "punch" | "drink" | "tie" | "listen" | "cheer";
type Setting =
  | "bedroom" | "phone" | "street" | "calendar" | "mirror" | "desk"
  | "stairs" | "cafe" | "bus" | "void" | "dawn" | "end"
  | "locker" | "classroom" | "busStop" | "bathroom" | "kitchen" | "park" | "gym" | "library";

type Shot = {
  title: string;
  subtitle: string;
  setting: Setting;
  pose: Pose;
  x0: number;
  x1: number;
  y0: number;
  y1: number;
  scale: number;
  shirt: string;
  shadow: number;
  shadowX: number;
  zoom0: number;
  zoom1: number;
  pan0: number;
  pan1: number;
  phone?: boolean;
  phoneOnDesk?: boolean;
  friend?: boolean;
  hideCharacter?: boolean;
  day?: string;
  redWords?: string[];
  dip?: boolean;
};

const FPS = 24;
const SHOT_FRAMES = 120;
const shots: Shot[] = [
  {title:"ONE MORE SCROLL",subtitle:"It starts with one small decision.",setting:"bedroom",pose:"scroll",x0:760,x1:760,y0:-60,y1:-60,scale:1.28,shirt:"#c56d9b",shadow:.48,shadowX:970,zoom0:1,zoom1:1.08,pan0:10,pan1:-8,phone:true,dip:true},
  {title:"THE NEXT THING",subtitle:"The feed always has one more thing.",setting:"phone",pose:"scroll",x0:885,x1:870,y0:0,y1:0,scale:1.12,shirt:"#c56d9b",shadow:.74,shadowX:1035,zoom0:1,zoom1:1.12,pan0:14,pan1:-8,phone:true,redWords:["ONE MORE","LATER"]},
  {title:"WALKING, BUT NOT HERE",subtitle:"Your body moves. Your attention stays behind.",setting:"street",pose:"walk",x0:235,x1:985,y0:0,y1:0,scale:1.08,shirt:"#c56d9b",shadow:.79,shadowX:965,zoom0:1,zoom1:1.055,pan0:24,pan1:-34,phone:true,redWords:["SCROLL"]},
  {title:"WAITING FOR NOTHING",subtitle:"You don't notice the world passing.",setting:"busStop",pose:"tired",x0:425,x1:420,y0:0,y1:0,scale:1.13,shirt:"#c56d9b",shadow:.68,shadowX:1000,zoom0:1,zoom1:1.09,pan0:2,pan1:-14,phone:true,day:"DAY 03"},
  {title:"EVERYONE ELSE IS THERE",subtitle:"A room full of people can still feel empty.",setting:"classroom",pose:"scroll",x0:745,x1:745,y0:0,y1:0,scale:1.03,shirt:"#c56d9b",shadow:.62,shadowX:1035,zoom0:1,zoom1:1.06,pan0:8,pan1:-5,phone:true},
  {title:"JUST FIVE MORE MINUTES",subtitle:"And then the night is gone.",setting:"bedroom",pose:"scroll",x0:810,x1:810,y0:-54,y1:-54,scale:1.32,shirt:"#c56d9b",shadow:.79,shadowX:955,zoom0:1.02,zoom1:1.14,pan0:0,pan1:-10,phone:true},
  {title:"THE DAYS DISAPPEAR",subtitle:"One day becomes a habit.",setting:"calendar",pose:"slump",x0:290,x1:275,y0:0,y1:8,scale:1.18,shirt:"#c56d9b",shadow:.69,shadowX:1000,zoom0:1,zoom1:1.13,pan0:-4,pan1:-24,day:"DAY 07",dip:true},
  {title:"THE MORNING AFTER",subtitle:"You promise it will be different tonight.",setting:"bathroom",pose:"tired",x0:450,x1:448,y0:0,y1:0,scale:1.24,shirt:"#c56d9b",shadow:.58,shadowX:900,zoom0:1,zoom1:1.09,pan0:0,pan1:-8,day:"6:12 AM"},
  {title:"THE SHADOW GROWS",subtitle:"What you feed begins to follow you.",setting:"mirror",pose:"tired",x0:420,x1:410,y0:0,y1:0,scale:1.4,shirt:"#c56d9b",shadow:.98,shadowX:850,zoom0:1,zoom1:1.14,pan0:0,pan1:-18,redWords:["TOMORROW","ONE MORE","LATER"]},
  {title:"IT KNOWS YOUR NAME",subtitle:"The voice starts sounding like your own.",setting:"mirror",pose:"slump",x0:470,x1:466,y0:0,y1:0,scale:1.56,shirt:"#c56d9b",shadow:.98,shadowX:830,zoom0:1.04,zoom1:1.18,pan0:0,pan1:-9,redWords:["NOT ENOUGH","LATER"]},
  {title:"THE LOOP",subtitle:"Scroll. Regret. Promise. Repeat.",setting:"void",pose:"slump",x0:640,x1:640,y0:0,y1:0,scale:1.36,shirt:"#c56d9b",shadow:.95,shadowX:900,zoom0:1.03,zoom1:1.16,pan0:0,pan1:-9,redWords:["ONE MORE","TOMORROW","JUST ONCE","LATER"]},
  {title:"NO BIG SPEECH",subtitle:"The change begins quietly.",setting:"phone",pose:"stand",x0:640,x1:640,y0:0,y1:0,scale:1.12,shirt:"#c56d9b",shadow:.48,shadowX:915,zoom0:1.06,zoom1:1.03,pan0:0,pan1:0,phone:true,dip:true},
  {title:"PUT IT DOWN",subtitle:"Let the silence last a second.",setting:"bedroom",pose:"stand",x0:760,x1:720,y0:-6,y1:0,scale:1.18,shirt:"#c56d9b",shadow:.37,shadowX:1000,zoom0:1.06,zoom1:1,pan0:0,pan1:4,phoneOnDesk:true,dip:true},
  {title:"START WITH ONE PAGE",subtitle:"Not a new life. One small action.",setting:"desk",pose:"write",x0:720,x1:715,y0:-8,y1:-8,scale:1.27,shirt:"#c56d9b",shadow:.34,shadowX:1000,zoom0:1,zoom1:1.08,pan0:2,pan1:-10,phoneOnDesk:true},
  {title:"ONE LINE AT A TIME",subtitle:"You don't need to feel ready.",setting:"desk",pose:"write",x0:730,x1:730,y0:-8,y1:-8,scale:1.38,shirt:"#c56d9b",shadow:.27,shadowX:1040,zoom0:1.08,zoom1:1.18,pan0:-2,pan1:-14,phoneOnDesk:true,redWords:["BEGIN"]},
  {title:"MAKE SPACE",subtitle:"Water. Air. A little movement.",setting:"kitchen",pose:"drink",x0:540,x1:555,y0:0,y1:0,scale:1.2,shirt:"#c56d9b",shadow:.23,shadowX:1000,zoom0:1,zoom1:1.06,pan0:0,pan1:-10},
  {title:"TIE YOUR SHOES",subtitle:"The first step can be very small.",setting:"bedroom",pose:"tie",x0:565,x1:570,y0:20,y1:20,scale:1.22,shirt:"#c56d9b",shadow:.2,shadowX:1000,zoom0:1.04,zoom1:1.12,pan0:0,pan1:-4,day:"DAY 01"},
  {title:"SHOW UP AGAIN",subtitle:"Progress is a direction, not a streak.",setting:"stairs",pose:"walk",x0:245,x1:855,y0:10,y1:-82,scale:1.1,shirt:"#d7a56d",shadow:.25,shadowX:1030,zoom0:1,zoom1:1.075,pan0:10,pan1:-18,day:"DAY 02"},
  {title:"MOVE THROUGH THE FEELING",subtitle:"You can be tired and still begin.",setting:"park",pose:"walk",x0:240,x1:930,y0:0,y1:-4,scale:1.12,shirt:"#d7a56d",shadow:.21,shadowX:1040,zoom0:1,zoom1:1.055,pan0:22,pan1:-26},
  {title:"MISS. RESET. TRY AGAIN.",subtitle:"Discipline is a practice, not a pose.",setting:"gym",pose:"punch",x0:610,x1:635,y0:0,y1:0,scale:1.25,shirt:"#d7a56d",shadow:.18,shadowX:1010,zoom0:1,zoom1:1.12,pan0:0,pan1:-9},
  {title:"ONE MORE REP",subtitle:"Let your actions speak first.",setting:"gym",pose:"punch",x0:565,x1:590,y0:0,y1:0,scale:1.36,shirt:"#d7a56d",shadow:.12,shadowX:1030,zoom0:1.04,zoom1:1.16,pan0:0,pan1:-12},
  {title:"LOOK UP",subtitle:"There is a world beyond the screen.",setting:"street",pose:"stand",x0:390,x1:410,y0:0,y1:0,scale:1.2,shirt:"#d7a56d",shadow:.09,shadowX:1050,zoom0:1.04,zoom1:1.1,pan0:0,pan1:-8,dip:true},
  {title:"YOU ARE NOT ALONE",subtitle:"Some things become lighter when shared.",setting:"cafe",pose:"meet",x0:440,x1:458,y0:0,y1:0,scale:1.16,shirt:"#d7a56d",shadow:.12,shadowX:1010,zoom0:1,zoom1:1.045,pan0:-3,pan1:-8,friend:true,dip:true},
  {title:"LISTEN",subtitle:"A real conversation pulls you back.",setting:"cafe",pose:"listen",x0:465,x1:465,y0:0,y1:0,scale:1.26,shirt:"#d7a56d",shadow:.08,shadowX:1040,zoom0:1.05,zoom1:1.13,pan0:0,pan1:-8,friend:true},
  {title:"BE WHERE YOUR FEET ARE",subtitle:"Notice the people around you.",setting:"bus",pose:"walk",x0:340,x1:800,y0:0,y1:0,scale:1.05,shirt:"#d7a56d",shadow:.08,shadowX:1030,zoom0:1,zoom1:1.04,pan0:16,pan1:-25,friend:true},
  {title:"PROTECT THE FIRST HOUR",subtitle:"Your attention belongs to you.",setting:"library",pose:"write",x0:730,x1:730,y0:0,y1:0,scale:1.2,shirt:"#d7a56d",shadow:.06,shadowX:1030,zoom0:1,zoom1:1.08,pan0:0,pan1:-7,day:"DAY 14"},
  {title:"THE DAYS ADD UP",subtitle:"Small choices leave a mark.",setting:"calendar",pose:"stand",x0:310,x1:310,y0:0,y1:0,scale:1.08,shirt:"#d7a56d",shadow:.05,shadowX:1030,zoom0:1,zoom1:1.06,pan0:0,pan1:-8,day:"DAY 21"},
  {title:"THE SHADOW SHRINKS",subtitle:"You don't have to obey every urge.",setting:"mirror",pose:"hero",x0:430,x1:448,y0:0,y1:0,scale:1.4,shirt:"#d7a56d",shadow:.07,shadowX:920,zoom0:1.05,zoom1:1.13,pan0:0,pan1:-8,redWords:["LATER"]},
  {title:"A LIFE OUTSIDE THE LOOP",subtitle:"The world was here the whole time.",setting:"park",pose:"meet",x0:470,x1:485,y0:0,y1:0,scale:1.13,shirt:"#d7a56d",shadow:.025,shadowX:1100,zoom0:1,zoom1:1.06,pan0:5,pan1:-12,friend:true},
  {title:"A DIFFERENT DIRECTION",subtitle:"Tomorrow begins with this moment.",setting:"dawn",pose:"walk",x0:450,x1:820,y0:0,y1:-10,scale:1.18,shirt:"#d7a56d",shadow:.018,shadowX:1100,zoom0:1,zoom1:1.055,pan0:12,pan1:-14},
  {title:"YOUR ATTENTION IS YOUR LIFE",subtitle:"Choose where it goes.",setting:"end",pose:"hero",x0:640,x1:640,y0:0,y1:0,scale:.88,shirt:"#d7a56d",shadow:0,shadowX:900,zoom0:1,zoom1:1,pan0:0,pan1:0,dip:true},
];;

const clampInterp = (v: number, input: number[], output: number[]) =>
  interpolate(v, input, output, { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const Window: React.FC<{ x: number; y: number; w?: number; h?: number; warm?: boolean }> = ({
  x, y, w = 80, h = 110, warm = false,
}) => (
  <g>
    <rect x={x - 8} y={y - 8} width={w + 16} height={h + 16} rx="2" fill="#211d29" stroke="#584455" strokeWidth="4" />
    <rect x={x} y={y} width={w} height={h} fill={warm ? "#d49a65" : "#292532"} />
    {warm && <rect x={x + 4} y={y + 4} width={w - 8} height={h - 8} fill="#f4c48d" opacity=".52" />}
    <path d={"M" + (x + w / 2) + " " + y + " V" + (y + h) + " M" + x + " " + (y + h / 2) + " H" + (x + w)} stroke="#453747" strokeWidth="5" />
    {warm && <path d={"M" + (x + 7) + " " + (y + 10) + " H" + (x + w - 7)} stroke="#ffe3b3" strokeWidth="3" opacity=".45" />}
  </g>
);

const FlowerPot: React.FC<{ x: number; y: number; scale?: number }> = ({ x, y, scale = 1 }) => (
  <g transform={"translate(" + x + " " + y + ") scale(" + scale + ")"}>
    <path d="M-31 0 H31 L23 42 H-23Z" fill="#855543" stroke="#4c3740" strokeWidth="3" />
    <ellipse cx="0" cy="0" rx="32" ry="9" fill="#495b41" />
    {Array.from({ length: 7 }, (_, i) => {
      const px = -24 + i * 8;
      const py = -12 - (i % 3) * 8;
      return <g key={i}>
        <path d={"M" + px + " 0 Q" + (px - 3) + " -14 " + (px - 1) + " " + py} stroke="#354b39" strokeWidth="3" fill="none" />
        <circle cx={px} cy={py} r={i % 2 ? 5.7 : 6.5} fill={i % 2 ? "#cb7786" : "#dd9098"} />
        <circle cx={px - 2} cy={py - 2} r="2" fill="#f6c4b3" opacity=".8" />
      </g>;
    })}
  </g>
);

const Backdrop: React.FC<{ setting: Setting; t: number; frame: number }> = ({ setting, t, frame }) => (
  <svg width="100%" height="100%" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMid slice" style={{ position: "absolute", inset: 0 }}>
    <defs>
      <linearGradient id="h2Wall" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#2c2734" /><stop offset="100%" stopColor="#473543" />
      </linearGradient>
      <linearGradient id="h2Road" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#4a3a49" /><stop offset="100%" stopColor="#201e27" />
      </linearGradient>
      <radialGradient id="h2WarmLamp">
        <stop offset="0%" stopColor="#f9d49d" stopOpacity=".65" /><stop offset="100%" stopColor="#f9d49d" stopOpacity="0" />
      </radialGradient>
      <linearGradient id="h2Dawn" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#393047" /><stop offset="55%" stopColor="#8b6474" /><stop offset="100%" stopColor="#e4b18b" />
      </linearGradient>
    </defs>

    {setting === "bedroom" && <g>
      <rect width="1280" height="720" fill="#201e29" />
      <rect x="0" y="0" width="1280" height="550" fill="url(#h2Wall)" />
      <path d="M0 555 H1280" stroke="#181720" strokeWidth="12" />
      <rect x="80" y="80" width="265" height="240" fill="#171924" stroke="#554356" strokeWidth="8" />
      <rect x="94" y="94" width="237" height="212" fill="#222b3c" />
      <circle cx="270" cy="143" r="27" fill="#ddd8c7" opacity=".88" />
      <path d="M94 274 L162 215 L210 258 L272 195 L331 254 V306 H94Z" fill="#334151" />
      <path d="M212 94 V306 M94 202 H331" stroke="#655367" strokeWidth="6" />
      <rect x="410" y="95" width="130" height="150" fill="#2b2632" stroke="#463647" strokeWidth="5" />
      <rect x="425" y="110" width="100" height="120" fill="#282633" />
      <path d="M0 355 H1280" stroke="#665268" strokeWidth="4" opacity=".4" />
      <rect x="230" y="472" width="610" height="116" rx="7" fill="#403746" stroke="#78647b" strokeWidth="5" />
      <rect x="250" y="447" width="570" height="48" rx="10" fill="#777085" />
      <rect x="260" y="458" width="172" height="46" rx="10" fill="#aaa0ae" />
      <path d="M442 493 Q615 525 822 490 V571 H442Z" fill="#655b73" />
      <path d="M442 494 Q618 528 822 493" fill="none" stroke="#a69baa" strokeWidth="3" opacity=".62" />
      <rect x="845" y="412" width="116" height="20" rx="4" fill="#554655" />
      <rect x="857" y="430" width="12" height="120" fill="#37303d" /><rect x="938" y="430" width="12" height="120" fill="#37303d" />
      <path d="M888 412 V376 Q888 361 903 361 Q918 361 918 376 V412" stroke="#554655" strokeWidth="6" fill="none" />
      <ellipse cx="904" cy="371" rx="70" ry="62" fill="url(#h2WarmLamp)" />
      <circle cx="904" cy="371" r="7" fill="#f4d4a0" />
      <rect x="0" y="590" width="1280" height="130" fill="#29232f" />
      <path d="M0 596 H1280" stroke="#6c596c" strokeWidth="3" opacity=".4" />
    </g>}

    {setting === "phone" && <g>
      <rect width="1280" height="720" fill="#17161f" />
      <ellipse cx="620" cy="360" rx="440" ry="400" fill="url(#h2WarmLamp)" opacity=".12" />
      <rect x="390" y="75" width="370" height="560" rx="48" fill="#0e0e13" stroke="#766578" strokeWidth="7" />
      <rect x="408" y="96" width="334" height="518" rx="32" fill="#28232f" />
      <rect x="520" y="107" width="118" height="18" rx="9" fill="#111117" />
      <text x="434" y="151" fontSize="18" fill="#e6d8ca" fontWeight="700">9:41</text>
      <circle cx="700" cy="146" r="7" fill="#83b8a0" />
      <path d="M431 171 H719" stroke="#554454" strokeWidth="2" />
      <g transform={"translate(0 " + (-t * 118) + ")"}>
        <rect x="430" y="191" width="290" height="124" rx="14" fill="#504252" />
        <circle cx="463" cy="223" r="13" fill="#d08b9b" />
        <rect x="487" y="213" width="136" height="8" rx="4" fill="#dfcfc2" opacity=".8" />
        <rect x="487" y="230" width="190" height="6" rx="3" fill="#9f8da3" />
        <rect x="451" y="252" width="246" height="48" rx="7" fill="#746078" />
        <rect x="430" y="329" width="290" height="132" rx="14" fill="#3f4357" />
        <circle cx="463" cy="360" r="13" fill="#d7a56d" />
        <rect x="487" y="351" width="155" height="8" rx="4" fill="#e6dbcf" opacity=".8" />
        <rect x="487" y="368" width="190" height="6" rx="3" fill="#9f9aaa" />
        <rect x="451" y="390" width="246" height="58" rx="7" fill="#6f758e" />
        <rect x="430" y="477" width="290" height="124" rx="14" fill="#5b3c50" />
        <circle cx="463" cy="506" r="13" fill="#d18a94" />
        <rect x="487" y="497" width="145" height="8" rx="4" fill="#f0dfd2" opacity=".8" />
        <rect x="487" y="514" width="180" height="6" rx="3" fill="#a98b9c" />
        <rect x="451" y="536" width="246" height="48" rx="7" fill="#855366" />
      </g>
      <g opacity={0.65 + 0.2 * Math.sin(t * 10)}>
        <circle cx="825" cy="235" r="36" fill="#c66f7d" opacity=".13" />
        <circle cx="825" cy="235" r="18" fill="#c66f7d" opacity=".2" />
        <circle cx="825" cy="235" r="6" fill="#f1c7b4" />
      </g>
      <rect x="0" y="660" width="1280" height="60" fill="#111017" />
    </g>}

    {setting === "street" && <g>
      <rect width="1280" height="720" fill="#29232f" />
      <rect x="0" y="0" width="1280" height="545" fill="url(#h2Wall)" />
      <g opacity=".72">
        <rect x="-20" y="30" width="300" height="480" fill="#282431" />
        <rect x="300" y="0" width="280" height="520" fill="#302936" />
        <rect x="922" y="0" width="380" height="520" fill="#2b2632" />
        <Window x={30} y={65} w={67} h={97} /><Window x={144} y={65} w={67} h={97} />
        <Window x={345} y={55} w={70} h={100} warm={false} /><Window x={457} y={55} w={70} h={100} warm={true} />
        <Window x={988} y={55} w={82} h={105} /><Window x={1120} y={55} w={82} h={105} />
      </g>
      <path d="M0 212 H1280" stroke="#1b1922" strokeWidth="13" /><path d="M0 221 H1280" stroke="#7c617b" strokeWidth="3" opacity=".42" />
      <Window x={64} y={268} w={138} h={173} warm={true} />
      <Window x={545} y={268} w={135} h={173} warm={true} />
      <Window x={964} y={268} w={155} h={173} warm={true} />
      <rect x="298" y="255" width="145" height="225" fill="#211e29" stroke="#4e3c4f" strokeWidth="8" />
      <rect x="321" y="280" width="99" height="196" fill="#29232e" stroke="#5d465e" strokeWidth="4" />
      <rect x="346" y="298" width="48" height="99" fill="#dc9f68" opacity=".88" /><circle cx="404" cy="414" r="5" fill="#e4bc82" />
      <path d="M273 494 H469 V511 H273Z M251 511 H491 V529 H251Z M229 529 H513 V546 H229Z" fill="#4c3f50" stroke="#241f2b" strokeWidth="4" />
      <FlowerPot x={244} y={475} scale={1.03} /><FlowerPot x={1185} y={475} scale={1.08} />
      <rect x="0" y="546" width="1280" height="174" fill="url(#h2Road)" />
      <path d="M0 550 H1280 M0 604 H1280" stroke="#6a5368" strokeWidth="3" opacity=".45" />
      <path d="M100 665 H340 M770 665 H1020" stroke="#b49a9a" strokeWidth="3" opacity=".22" />
      <path d="M850 545 V360 Q850 335 875 335 H922" stroke="#201d28" strokeWidth="10" fill="none" strokeLinecap="round" />
      <path d="M911 335 H947 L953 351 H904Z" fill="#5a465f" stroke="#af8798" strokeWidth="2" />
      <ellipse cx="928" cy="355" rx="58" ry="43" fill="url(#h2WarmLamp)" opacity=".6" />
      <circle cx="928" cy="350" r="6" fill="#f8d6a0" />
    </g>}

    {setting === "calendar" && <g>
      <rect width="1280" height="720" fill="#211e29" />
      <rect x="0" y="0" width="1280" height="720" fill="url(#h2Wall)" opacity=".72" />
      <path d="M0 572 H1280" stroke="#17161f" strokeWidth="12" />
      <rect x="590" y="88" width="470" height="430" rx="6" fill="#c4b8aa" stroke="#403340" strokeWidth="10" />
      <rect x="590" y="88" width="470" height="66" fill="#9a7a8f" />
      <text x="624" y="130" fontSize="28" letterSpacing="4" fill="#211e29" fontWeight="700">THIS MONTH</text>
      {Array.from({ length: 28 }, (_, i) => {
        const x = 620 + (i % 7) * 60;
        const y = 178 + Math.floor(i / 7) * 75;
        const passed = i < Math.min(28, Math.floor(t * 28) + 5);
        return <g key={i} opacity={0.8 + 0.2 * Math.sin((i + 1) * 2)}>
          <rect x={x} y={y} width="46" height="52" rx="3" fill={passed ? "#b97074" : "#e0d7cc"} />
          {passed && <path d={"M" + (x + 8) + " " + (y + 11) + " l28 30 M" + (x + 35) + " " + (y + 10) + " l-27 31"} stroke="#f5d6c5" strokeWidth="3" />}
        </g>;
      })}
      <circle cx="310" cy="240" r="106" fill="#24212d" stroke="#8f778e" strokeWidth="8" />
      <circle cx="310" cy="240" r="86" fill="#d3c3b1" />
      <path d="M310 240 L310 178 M310 240 L365 260" stroke="#403343" strokeWidth="9" strokeLinecap="round" />
      <circle cx="310" cy="240" r="11" fill="#403343" />
      <path d="M310 135 V151 M415 240 H399 M310 345 V329 M205 240 H221" stroke="#ad8c96" strokeWidth="5" />
      <rect x="0" y="596" width="1280" height="124" fill="#24212b" />
    </g>}

    {setting === "mirror" && <g>
      <rect width="1280" height="720" fill="#211e29" />
      <rect x="0" y="0" width="1280" height="590" fill="url(#h2Wall)" />
      <rect x="714" y="78" width="315" height="445" rx="6" fill="#111119" stroke="#a48a9b" strokeWidth="10" />
      <rect x="734" y="98" width="275" height="405" fill="#242634" stroke="#4a3a50" strokeWidth="3" />
      <path d="M744 110 L1000 490" stroke="#a3a0b6" strokeWidth="7" opacity=".13" />
      <ellipse cx="870" cy="213" rx="98" ry="104" fill="#17151f" />
      <path d="M794 315 Q746 365 765 487 H978 Q995 369 945 315Z" fill="#18151e" />
      <circle cx="865" cy="215" r="5" fill="#be5c71" opacity=".55" /><circle cx="900" cy="215" r="5" fill="#be5c71" opacity=".55" />
      <path d="M0 590 H1280" stroke="#15141b" strokeWidth="15" />
      <rect x="90" y="130" width="260" height="330" fill="#2d2834" stroke="#534154" strokeWidth="5" />
      <rect x="110" y="150" width="220" height="290" fill="#242431" />
      <path d="M128 180 H312 M128 208 H285 M128 236 H302" stroke="#4d4254" strokeWidth="3" opacity=".5" />
      <rect x="0" y="603" width="1280" height="117" fill="#25212d" />
    </g>}

    {setting === "desk" && <g>
      <rect width="1280" height="720" fill="#28232f" />
      <rect width="1280" height="560" fill="url(#h2Wall)" />
      <rect x="80" y="80" width="270" height="260" fill="#201e2a" stroke="#655169" strokeWidth="7" />
      <rect x="94" y="94" width="242" height="232" fill="#273144" />
      <circle cx="277" cy="150" r="24" fill="#d8d4c5" opacity=".8" />
      <path d="M94 285 L176 213 L237 270 L336 186 V326 H94Z" fill="#384657" />
      <path d="M214 94 V326 M94 206 H336" stroke="#5e4e64" strokeWidth="6" />
      <rect x="356" y="150" width="145" height="170" fill="#302936" stroke="#4f3d50" strokeWidth="5" />
      <path d="M0 566 H1280" stroke="#16151d" strokeWidth="14" />
      <rect x="328" y="454" width="648" height="22" rx="4" fill="#806978" stroke="#302632" strokeWidth="4" />
      <path d="M362 475 V582 M938 475 V582" stroke="#342b37" strokeWidth="18" />
      <rect x="520" y="335" width="164" height="118" rx="6" fill="#24222e" stroke="#a08b9d" strokeWidth="5" />
      <rect x="532" y="347" width="140" height="94" fill="#65717c" />
      <path d="M532 425 L563 388 L596 414 L625 377 L672 419 V441 H532Z" fill="#a4b0b7" opacity=".7" />
      <rect x="520" y="445" width="164" height="12" fill="#9b8d9f" />
      <path d="M711 446 L738 376 L750 378 L726 447" fill="#bb9b82" stroke="#4c3948" strokeWidth="2" />
      <ellipse cx="735" cy="373" rx="66" ry="51" fill="url(#h2WarmLamp)" opacity=".7" />
      <rect x="768" y="420" width="72" height="28" rx="4" fill="#a98f87" />
      <rect x="0" y="592" width="1280" height="128" fill="#25212c" />
    </g>}

    {setting === "stairs" && <g>
      <rect width="1280" height="720" fill="#27232e" />
      <rect width="1280" height="600" fill="url(#h2Wall)" />
      <path d="M0 0 L475 0 L1090 585 L0 585Z" fill="#312936" />
      <path d="M140 570 H290 V518 H425 V466 H560 V414 H695 V362 H830 V310 H965 V258 H1100 V206 H1250" fill="none" stroke="#4e4053" strokeWidth="28" strokeLinejoin="miter" />
      {Array.from({ length: 8 }, (_, i) => {
        const x = 150 + i * 135;
        const y = 570 - i * 52;
        return <g key={i}>
          <path d={"M" + x + " " + y + " H" + (x + 138) + " V" + (y + 52)} fill="none" stroke={i % 2 ? "#6b5b70" : "#594b60"} strokeWidth="5" />
          <path d={"M" + x + " " + y + " H" + (x + 138)} stroke="#a18aa2" strokeWidth="2" opacity=".45" />
        </g>;
      })}
      <path d="M125 572 L1200 135" stroke="#201d27" strokeWidth="17" />
      <path d="M125 560 L1200 123" stroke="#9d8598" strokeWidth="4" opacity=".7" />
      <rect x="0" y="600" width="1280" height="120" fill="#26212d" />
    </g>}

    {setting === "cafe" && <g>
      <rect width="1280" height="720" fill="#332934" />
      <rect width="1280" height="566" fill="#443643" />
      <rect x="70" y="70" width="260" height="210" fill="#292530" stroke="#7a6176" strokeWidth="7" />
      <rect x="85" y="85" width="230" height="180" fill="#7e5d65" />
      <path d="M85 195 H315 M200 85 V265" stroke="#473444" strokeWidth="6" />
      <rect x="370" y="74" width="540" height="180" fill="#332938" stroke="#624c65" strokeWidth="8" />
      {Array.from({ length: 5 }, (_, i) => <g key={i}>
        <rect x={390 + i * 102} y="95" width="80" height="140" fill={i % 2 ? "#765b6a" : "#685264"} />
        {Array.from({ length: 3 }, (_, j) => <rect key={j} x={399 + i * 102} y={108 + j * 38} width="62" height="5" fill="#a58a91" opacity=".45" />)}
      </g>)}
      <path d="M625 0 V90 M610 90 H640" stroke="#201b26" strokeWidth="6" />
      <path d="M576 90 Q625 52 674 90 L660 116 H590Z" fill="#d3a078" stroke="#5b4053" strokeWidth="4" />
      <ellipse cx="625" cy="140" rx="170" ry="95" fill="url(#h2WarmLamp)" />
      <rect x="0" y="570" width="1280" height="150" fill="#28232f" />
      <path d="M290 501 H999 V534 H290Z" fill="#906d74" stroke="#352937" strokeWidth="6" />
      <path d="M344 534 V630 M945 534 V630" stroke="#352937" strokeWidth="20" />
      <ellipse cx="625" cy="506" rx="330" ry="45" fill="#e5b68d" opacity=".08" />
    </g>}

    {setting === "bus" && <g>
      <rect width="1280" height="720" fill="#292431" />
      <rect width="1280" height="535" fill="url(#h2Wall)" />
      <Window x={60} y={78} w={105} h={142} warm={true} /><Window x={225} y={78} w={105} h={142} />
      <Window x={920} y={78} w={105} h={142} warm={true} /><Window x={1085} y={78} w={105} h={142} />
      <path d="M0 238 H1280" stroke="#1b1922" strokeWidth="13" />
      <rect x="96" y="300" width="192" height="237" rx="7" fill="#22202a" stroke="#79667d" strokeWidth="6" />
      <rect x="111" y="316" width="162" height="190" fill="#283345" />
      <path d="M111 316 L273 506 M273 316 L111 506" stroke="#9c829f" strokeWidth="3" opacity=".24" />
      <text x="139" y="348" fontSize="18" fill="#d9c9b8" letterSpacing="2">BUS</text>
      <rect x="72" y="525" width="242" height="16" rx="4" fill="#655568" />
      <path d="M102 541 V590 M285 541 V590" stroke="#332b37" strokeWidth="16" />
      <rect x="735" y="356" width="434" height="150" rx="20" fill="#334050" stroke="#9b829d" strokeWidth="6" />
      <rect x="755" y="377" width="80" height="73" fill="#d59d6b" opacity=".8" />
      <rect x="849" y="377" width="80" height="73" fill="#d59d6b" opacity=".8" />
      <rect x="943" y="377" width="80" height="73" fill="#d59d6b" opacity=".8" />
      <rect x="1037" y="377" width="80" height="73" fill="#d59d6b" opacity=".8" />
      <circle cx={810 + t * 15} cy="462" r="8" fill="#f0d5a4" opacity=".6" />
      <circle cx={1000 + t * 15} cy="462" r="8" fill="#f0d5a4" opacity=".6" />
      <rect x="0" y="540" width="1280" height="180" fill="url(#h2Road)" />
      <path d="M0 548 H1280 M0 618 H1280" stroke="#6e576d" strokeWidth="3" opacity=".42" />
    </g>}

    {setting === "locker" && <g>
      <rect width="1280" height="720" fill="#211e29" />
      <rect width="1280" height="555" fill="#38303c" />
      <path d="M0 135 H1280 M0 505 H1280" stroke="#211d28" strokeWidth="13" />
      <path d="M0 142 H1280 M0 512 H1280" stroke="#80667d" strokeWidth="3" opacity=".35" />
      {Array.from({length:10},(_,i)=>{
        const x=34+i*124;
        return <g key={i}>
          <rect x={x} y="165" width="108" height="326" rx="4" fill={i===3?"#5d4a60":"#4a3c4e"} stroke="#b29cb2" strokeWidth="3" />
          <rect x={x+8} y="174" width="92" height="309" fill={i===3?"#282431":"#322a38"} stroke="#28212e" strokeWidth="2" />
          <path d={"M"+(x+18)+" 198 H"+(x+88)+" M"+(x+18)+" 210 H"+(x+88)+" M"+(x+18)+" 222 H"+(x+88)} stroke="#746075" strokeWidth="3" opacity=".65" />
          {Array.from({length:6},(_,j)=><path key={j} d={"M"+(x+23+j*11)+" 445 v21"} stroke="#1d1a24" strokeWidth="3" />)}
          <circle cx={x+89} cy="334" r="4" fill="#d6b596" />
        </g>;
      })}
      <rect x="0" y="555" width="1280" height="165" fill="url(#h2Road)" />
      <path d="M0 561 H1280" stroke="#a18a9d" strokeWidth="3" opacity=".25" />
      <rect x="300" y="495" width="390" height="28" rx="4" fill="#6c5a70" stroke="#322a38" strokeWidth="4" />
      <path d="M330 523 V560 M660 523 V560" stroke="#322a38" strokeWidth="15" />
      <Window x={1050} y={42} w={95} h={112} warm={true} />
      <ellipse cx="1095" cy="205" rx="125" ry="140" fill="url(#h2WarmLamp)" opacity=".24" />
    </g>}

    {setting === "classroom" && <g>
      <rect width="1280" height="720" fill="#27232f" />
      <rect width="1280" height="530" fill="url(#h2Wall)" />
      <Window x={58} y={60} w={130} h={170} warm={true} />
      <Window x={228} y={60} w={130} h={170} warm={false} />
      <rect x="470" y="90" width="495" height="270" rx="3" fill="#1c2428" stroke="#846d82" strokeWidth="8" />
      <path d="M500 140 Q620 122 730 146 T925 135 M515 175 H890 M540 215 Q680 200 820 220" stroke="#c4c3ba" strokeWidth="3" opacity=".16" fill="none" />
      <text x="527" y="292" fontSize="31" fontWeight="700" fill="#a7b5a4" opacity=".68">PAY ATTENTION</text>
      <circle cx="1100" cy="105" r="43" fill="#d8c8b4" stroke="#554356" strokeWidth="7" />
      <path d="M1100 105 L1100 77 M1100 105 L1121 119" stroke="#3b303d" strokeWidth="5" strokeLinecap="round" />
      <path d="M0 542 H1280" stroke="#201d28" strokeWidth="12" />
      {Array.from({length:4},(_,i)=>{
        const x=80+i*300;
        return <g key={i}>
          <path d={"M"+x+" 435 h250 l-18 32 h-214Z"} fill="#786475" stroke="#312835" strokeWidth="5" />
          <path d={"M"+(x+17)+" 465 v80 M"+(x+217)+" 465 v80"} stroke="#312835" strokeWidth="15" />
          <rect x={x+82} y="401" width="92" height="30" rx="4" fill="#3e3c4c" />
          <path d={"M"+(x+89)+" 409 H"+(x+168)} stroke="#9890a2" strokeWidth="3" opacity=".5" />
        </g>;
      })}
      <rect x="0" y="570" width="1280" height="150" fill="#24212c" />
    </g>}

    {setting === "busStop" && <g>
      <rect width="1280" height="720" fill="#28232f" />
      <rect width="1280" height="545" fill="url(#h2Wall)" />
      <Window x={46} y={55} w={92} h={130} warm={true} />
      <Window x={180} y={55} w={92} h={130} warm={false} />
      <Window x={1000} y={55} w={92} h={130} warm={true} />
      <Window x={1135} y={55} w={92} h={130} warm={false} />
      <path d="M0 236 H1280" stroke="#1b1922" strokeWidth="13" />
      <rect x="260" y="233" width="610" height="18" fill="#8b7187" stroke="#2a2430" strokeWidth="5" />
      <path d="M284 245 V526 M845 245 V526" stroke="#91839a" strokeWidth="10" />
      <rect x="292" y="269" width="540" height="231" fill="#3d4857" opacity=".23" stroke="#a4a0b5" strokeWidth="4" />
      <path d="M292 270 L832 500 M832 270 L292 500" stroke="#a4a0b5" strokeWidth="3" opacity=".11" />
      <rect x="250" y="504" width="610" height="18" rx="4" fill="#6a596d" stroke="#302735" strokeWidth="4" />
      <path d="M292 522 V570 M818 522 V570" stroke="#302735" strokeWidth="16" />
      <rect x="885" y="160" width="68" height="170" rx="8" fill="#28232e" stroke="#bca5b0" strokeWidth="4" />
      <rect x="897" y="174" width="44" height="32" rx="4" fill="#d1ab81" />
      <text x="919" y="194" fontSize="10" fontWeight="800" fill="#332735" textAnchor="middle">BUS</text>
      <path d="M0 550 H1280" stroke="#5f4b60" strokeWidth="4" />
      <rect x="0" y="554" width="1280" height="166" fill="url(#h2Road)" />
      <path d="M60 650 H330 M870 650 H1140" stroke="#b7a0a1" strokeWidth="3" opacity=".23" />
      <ellipse cx={980+t*55} cy="520" rx="68" ry="14" fill="#e6b58d" opacity=".13" />
    </g>}

    {setting === "bathroom" && <g>
      <rect width="1280" height="720" fill="#25232d" />
      <rect width="1280" height="560" fill="#3b3340" />
      {Array.from({length:8},(_,i)=><path key={"v"+i} d={"M"+(i*160)+" 0 V560"} stroke="#574b5d" strokeWidth="3" opacity=".6" />)}
      {Array.from({length:5},(_,i)=><path key={"h"+i} d={"M0 "+(i*110)+" H1280"} stroke="#574b5d" strokeWidth="3" opacity=".6" />)}
      <rect x="620" y="68" width="390" height="360" rx="5" fill="#101118" stroke="#b5a1b2" strokeWidth="11" />
      <rect x="638" y="85" width="354" height="326" fill="#28303c" />
      <path d="M650 112 L960 388" stroke="#c3bdcb" strokeWidth="7" opacity=".11" />
      <rect x="240" y="420" width="810" height="58" rx="6" fill="#c4b8bb" stroke="#4f4053" strokeWidth="6" />
      <path d="M270 477 V555 M1020 477 V555" stroke="#514455" strokeWidth="22" />
      <ellipse cx="725" cy="454" rx="105" ry="16" fill="#f1ded0" opacity=".4" />
      <path d="M686 452 V436 Q730 407 773 436 V452" fill="#d6c8ca" stroke="#625368" strokeWidth="4" />
      <rect x="0" y="560" width="1280" height="160" fill="#24212c" />
      <ellipse cx="810" cy="330" rx="150" ry="174" fill="url(#h2WarmLamp)" opacity=".18" />
      <circle cx="810" cy="228" r="7" fill="#f4d6a3" />
    </g>}

    {setting === "kitchen" && <g>
      <rect width="1280" height="720" fill="#28242f" />
      <rect width="1280" height="555" fill="url(#h2Wall)" />
      <Window x={88} y={62} w={148} h={185} warm={true} />
      <rect x="340" y="80" width="210" height="190" fill="#4c3c4d" stroke="#8a7088" strokeWidth="5" />
      <rect x="355" y="95" width="180" height="160" fill="#312a39" />
      <path d="M445 95 V255" stroke="#78627a" strokeWidth="4" />
      <rect x="610" y="80" width="210" height="190" fill="#4c3c4d" stroke="#8a7088" strokeWidth="5" />
      <rect x="625" y="95" width="180" height="160" fill="#312a39" />
      <path d="M715 95 V255" stroke="#78627a" strokeWidth="4" />
      <rect x="830" y="105" width="160" height="380" rx="8" fill="#393342" stroke="#a08a9b" strokeWidth="5" />
      <path d="M845 293 H975" stroke="#78677e" strokeWidth="4" />
      <circle cx="960" cy="275" r="5" fill="#c7ad9d" /><circle cx="960" cy="320" r="5" fill="#c7ad9d" />
      <rect x="0" y="455" width="1280" height="35" fill="#796678" stroke="#352b39" strokeWidth="5" />
      <path d="M80 490 V570 M1180 490 V570" stroke="#342b38" strokeWidth="18" />
      <rect x="420" y="414" width="75" height="39" rx="5" fill="#d2c4b6" stroke="#655268" strokeWidth="3" />
      <ellipse cx="456" cy="414" rx="45" ry="14" fill="#f0c58e" opacity=".25" />
      <rect x="0" y="578" width="1280" height="142" fill="#24212c" />
    </g>}

    {setting === "park" && <g>
      <rect width="1280" height="720" fill="#302b39" />
      <rect width="1280" height="520" fill={t<.5?"#3b3240":"#51414a"} />
      <circle cx="1010" cy="190" r="88" fill="#e1b18d" opacity=".22" />
      <path d="M0 370 L150 270 L270 350 L425 245 L575 350 L760 235 L915 350 L1100 250 L1280 345 V560 H0Z" fill="#292a36" />
      <path d="M0 442 Q230 358 405 442 T815 432 T1280 433 V590 H0Z" fill="#343541" />
      {Array.from({length:6},(_,i)=>{
        const x=50+i*225;
        return <g key={i}>
          <path d={"M"+x+" 480 Q"+(x-35)+" 370 "+x+" 290 Q"+(x+45)+" 370 "+(x+26)+" 480Z"} fill="#202a29" />
          <path d={"M"+(x+7)+" 475 V515"} stroke="#584444" strokeWidth="13" />
          <circle cx={x} cy="350" r="69" fill={i%2?"#2c3831":"#27342f"} />
          <circle cx={x+28} cy="391" r="48" fill="#2a352f" />
        </g>;
      })}
      <path d="M0 520 Q280 485 520 545 T1000 522 T1280 535 V720 H0Z" fill="#413c49" />
      <path d="M0 604 Q320 552 650 612 T1280 591" stroke="#9c7a8a" strokeWidth="4" fill="none" opacity=".24" />
      <path d="M335 480 H570 V502 H335Z" fill="#7b6575" stroke="#28232f" strokeWidth="4" />
      <path d="M362 502 V558 M548 502 V558" stroke="#29232e" strokeWidth="15" />
      <ellipse cx="655" cy="572" rx="230" ry="32" fill="#edc19b" opacity=".045" />
      <rect x="0" y="650" width="1280" height="70" fill="#282431" opacity=".65" />
    </g>}

    {setting === "gym" && <g>
      <rect width="1280" height="720" fill="#22212b" />
      <rect width="1280" height="550" fill="#312c39" />
      {Array.from({length:7},(_,i)=><path key={i} d={"M"+(i*185)+" 0 V550"} stroke="#4b4051" strokeWidth="5" />)}
      <path d="M0 138 H1280 M0 285 H1280 M0 432 H1280" stroke="#55485b" strokeWidth="4" opacity=".6" />
      <rect x="885" y="65" width="20" height="150" fill="#1b1a22" />
      <rect x="815" y="198" width="160" height="14" rx="7" fill="#655369" />
      <path d="M895 211 V254" stroke="#b99eae" strokeWidth="7" />
      <path d="M860 246 Q895 232 930 246 L945 415 Q946 445 912 455 L878 455 Q844 445 845 415Z" fill="#1c1a23" stroke="#ad94a6" strokeWidth="4" />
      <path d="M851 285 H939 M848 405 H942" stroke="#514254" strokeWidth="5" />
      <rect x="0" y="550" width="1280" height="170" fill="#25222d" />
      <path d="M0 565 H1280 M0 620 H1280 M0 674 H1280" stroke="#6d5c6f" strokeWidth="3" opacity=".4" />
      <rect x="120" y="445" width="180" height="22" rx="8" fill="#9a8495" />
      <circle cx="144" cy="438" r="20" fill="#22212a" stroke="#b8a0b1" strokeWidth="4" />
      <circle cx="276" cy="438" r="20" fill="#22212a" stroke="#b8a0b1" strokeWidth="4" />
    </g>}

    {setting === "library" && <g>
      <rect width="1280" height="720" fill="#292530" />
      <rect width="1280" height="558" fill="#3b313e" />
      {Array.from({length:4},(_,i)=>{
        const x=46+i*300;
        return <g key={i}>
          <rect x={x} y="70" width="255" height="430" fill="#2a222f" stroke="#8a6f88" strokeWidth="7" />
          {Array.from({length:4},(_,r)=><g key={r}>
            <path d={"M"+(x+5)+" "+(155+r*91)+" H"+(x+250)} stroke="#ab8c9d" strokeWidth="5" />
            {Array.from({length:7},(_,k)=>{
              const w=15+(k%3)*5; const bh=43+(k%4)*8; const bx=x+12+k*32; const by=151+r*91-bh;
              return <rect key={k} x={bx} y={by} width={w} height={bh} rx="2" fill={["#644b61","#7c5669","#6b5d78","#ad896e","#465660"][((k+r)%5)]} stroke="#c3a6b4" strokeWidth="1.2" opacity=".85" />;
            })}
          </g>)}
        </g>;
      })}
      <rect x="230" y="470" width="830" height="24" rx="5" fill="#7d687a" stroke="#342b39" strokeWidth="4" />
      <path d="M260 494 V585 M1027 494 V585" stroke="#342b39" strokeWidth="18" />
      <rect x="635" y="395" width="175" height="77" rx="4" fill="#292630" stroke="#a28a9e" strokeWidth="5" />
      <rect x="649" y="408" width="147" height="51" fill="#e2ba8c" opacity=".22" />
      <ellipse cx="720" cy="390" rx="100" ry="95" fill="url(#h2WarmLamp)" opacity=".45" />
      <path d="M0 588 H1280" stroke="#655367" strokeWidth="4" />
      <rect x="0" y="600" width="1280" height="120" fill="#24212c" />
    </g>}

    {setting === "void" && <g>
      <rect width="1280" height="720" fill="#15131b" />
      <radialGradient id="voidSpot"><stop offset="0%" stopColor="#7f546f" stopOpacity=".2" /><stop offset="100%" stopColor="#15131b" stopOpacity="0" /></radialGradient>
      <rect width="1280" height="720" fill="url(#voidSpot)" />
      <path d="M0 590 H1280" stroke="#534054" strokeWidth="3" opacity=".65" />
      {Array.from({ length: 40 }, (_, i) => <circle key={i} cx={(i * 173 + 31) % 1270} cy={(i * 79 + 45) % 550} r={i % 5 === 0 ? 2 : 1} fill="#d5b5be" opacity=".2" />)}
      <ellipse cx="640" cy="575" rx="240" ry="36" fill="#a64d65" opacity=".05" />
    </g>}

    {setting === "dawn" && <g>
      <rect width="1280" height="720" fill="url(#h2Dawn)" />
      <circle cx="1000" cy="270" r="94" fill="#f0c69e" opacity=".85" />
      <circle cx="1000" cy="270" r="145" fill="#efc9a6" opacity=".12" />
      <path d="M0 430 L150 360 L275 418 L420 330 L568 417 L700 340 L835 413 L970 335 L1128 410 L1280 350 V600 H0Z" fill="#5a4b60" />
      <path d="M0 495 L205 430 L385 475 L595 405 L780 475 L1010 412 L1280 466 V610 H0Z" fill="#3e394a" />
      <path d="M0 600 L1280 545 V720 H0Z" fill="#282431" />
      <path d="M0 630 Q300 586 520 626 T1030 611 T1280 620" stroke="#9f7f85" strokeWidth="3" fill="none" opacity=".55" />
      <path d="M940 620 L1090 720 M1000 620 L1160 720" stroke="#c39a96" strokeWidth="3" opacity=".25" />
    </g>}

    {setting === "end" && <g>
      <rect width="1280" height="720" fill="#15131b" />
      <rect x="0" y="0" width="1280" height="720" fill="url(#h2Wall)" opacity=".13" />
      {Array.from({ length: 26 }, (_, i) => <circle key={i} cx={(i * 127 + 60) % 1260} cy={(i * 61 + 42) % 600} r={i % 4 === 0 ? 1.7 : 1} fill="#cfb5bd" opacity=".18" />)}
      <path d="M0 598 H1280" stroke="#766079" strokeWidth="2" opacity=".6" />
      <ellipse cx="640" cy="600" rx="85" ry="14" fill="#f0c69e" opacity=".1" />
    </g>}
  </svg>
);

const PhoneInsert: React.FC<{ t: number }> = ({ t }) => (
  <svg width="100%" height="100%" viewBox="0 0 1280 720" style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
    <g transform={"translate(" + (Math.sin(t * Math.PI * 2) * 3) + " 0)"}>
      <rect x="390" y="82" width="360" height="555" rx="48" fill="#0d0d12" stroke="#d2bda7" strokeWidth="5" />
      <rect x="405" y="98" width="330" height="522" rx="34" fill="#29242f" />
      <rect x="515" y="110" width="110" height="16" rx="8" fill="#0f1015" />
      <text x="434" y="153" fontSize="17" fontWeight="700" fill="#e7dacb">9:41</text>
      <circle cx="699" cy="145" r="6" fill="#8ac4a5" />
      <path d="M429 169 H711" stroke="#625064" strokeWidth="2" />
      <g transform={"translate(0 " + (-t * 110) + ")"}>
        <rect x="428" y="188" width="284" height="122" rx="13" fill="#504354" />
        <circle cx="461" cy="218" r="13" fill="#d18395" />
        <rect x="484" y="209" width="139" height="8" rx="4" fill="#dfd1c6" />
        <rect x="484" y="226" width="190" height="6" rx="3" fill="#a798ab" />
        <rect x="449" y="249" width="245" height="47" rx="7" fill="#7a657d" />
        <rect x="428" y="325" width="284" height="128" rx="13" fill="#3c4657" />
        <circle cx="461" cy="355" r="13" fill="#d3a16c" />
        <rect x="484" y="346" width="155" height="8" rx="4" fill="#e1d4c9" />
        <rect x="484" y="363" width="184" height="6" rx="3" fill="#9c9aae" />
        <rect x="449" y="387" width="245" height="51" rx="7" fill="#6a788d" />
        <rect x="428" y="468" width="284" height="126" rx="13" fill="#593b4c" />
        <circle cx="461" cy="498" r="13" fill="#d18395" />
        <rect x="484" y="489" width="142" height="8" rx="4" fill="#e1d4c9" />
        <rect x="484" y="506" width="186" height="6" rx="3" fill="#a798ab" />
        <rect x="449" y="530" width="245" height="51" rx="7" fill="#8a5266" />
      </g>
      <circle cx="570" cy="603" r="4" fill="#e9d7c3" />
    </g>
    <g opacity={0.35 + Math.sin(t * 10) * 0.12}>
      <circle cx="830" cy="260" r="38" fill="#c66d83" opacity=".22" />
      <circle cx="830" cy="260" r="8" fill="#f0c3b2" />
      <path d="M790 316 Q830 294 870 316" stroke="#bc7a91" strokeWidth="3" fill="none" />
    </g>
  </svg>
);

const ShadowFigure: React.FC<{ x: number; strength: number; frame: number }> = ({ x, strength, frame }) => {
  const breathe = 1 + Math.sin(frame / 22) * 0.018;
  return (
    <svg width="430" height="525" viewBox="0 0 430 525" style={{
      position: "absolute", left: x - 215, top: 28, opacity: strength,
      transform: "scale(" + (breathe * (0.38 + 0.62 * strength)) + "," + (0.52 + 0.48 * strength) + ")", transformOrigin: "50% 100%",
      filter: "blur(1.2px)", pointerEvents: "none",
    }}>
      <defs>
        <linearGradient id="shadowBody" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#211927" /><stop offset="100%" stopColor="#110f17" />
        </linearGradient>
      </defs>
      <ellipse cx="230" cy="125" rx="94" ry="104" fill="url(#shadowBody)" />
      <path d="M154 220 Q103 243 91 327 L65 493 Q222 515 364 493 L344 321 Q334 244 280 220Z" fill="#131019" />
      <path d="M178 227 Q228 251 284 225" stroke="#67485f" strokeWidth="4" opacity=".22" fill="none" />
      <path d="M191 126 Q229 104 266 126" stroke="#d86670" strokeWidth="5" opacity=".58" fill="none" strokeLinecap="round" />
      <ellipse cx="118" cy="232" rx="42" ry="54" fill="#c86a77" opacity=".05" />
    </svg>
  );
};

const Character: React.FC<{
  x: number; y: number; pose: Pose; t: number; shirt: string; scale?: number; companion?: boolean;
}> = ({ x, y, pose, t, shirt, scale = 1, companion = false }) => {
  const walking = pose === "walk" || pose === "run" || (pose === "meet" && companion);
  const phase = t * Math.PI * (pose === "run" ? 6.2 : 4.2);
  const swing = walking ? Math.sin(phase) : 0;
  const bob = walking ? -Math.abs(Math.sin(phase)) * (pose === "run" ? 9 : 5) : pose === "scroll" ? Math.sin(t * Math.PI * 2) * 1.5 : pose === "drink" ? Math.sin(t * Math.PI * 2) * 1.2 : 0;
  const lean = pose === "slump" ? 12 : pose === "scroll" ? 8 : pose === "tired" ? 6 : pose === "tie" ? 25 : pose === "punch" ? -7 : pose === "run" ? 15 : pose === "stretch" ? -4 : pose === "hero" || pose === "cheer" ? -4 : 0;
  const headTilt = pose === "scroll" ? 15 : pose === "slump" || pose === "tired" ? 20 : pose === "tie" ? 25 : pose === "drink" ? 8 : pose === "hero" || pose === "cheer" ? -5 : pose === "meet" || pose === "listen" ? -8 : 0;
  const scrollReach = clampInterp(t, [0.05, 0.42, 0.78, 1], [0, 1, 0.35, 0.15]);
  const writeReach = clampInterp(t, [0.05, 0.6, 1], [0, 1, 0.7]);
  const leftArm = pose === "scroll" ? -37 - scrollReach * 19 : pose === "write" ? -38 - writeReach * 26 : pose === "slump" || pose === "tired" ? 25 : pose === "tie" ? -56 : pose === "drink" ? -55 : pose === "punch" ? -66 : pose === "stretch" || pose === "cheer" ? -112 : pose === "hero" ? -32 : walking ? -18 + swing * (pose === "run" ? 37 : 27) : pose === "meet" && !companion ? -37 : -8;
  const rightArm = pose === "scroll" ? 34 + scrollReach * 7 : pose === "write" ? 14 : pose === "slump" || pose === "tired" ? 36 : pose === "tie" ? -24 : pose === "drink" ? -65 : pose === "punch" ? 66 : pose === "stretch" || pose === "cheer" ? 112 : pose === "hero" ? 20 : walking ? 18 - swing * (pose === "run" ? 37 : 27) : pose === "meet" && companion ? -30 : pose === "meet" || pose === "listen" ? -24 : 9;
  const leftLeg = walking ? (pose === "run" ? -30 : -22) + swing * (pose === "run" ? 40 : 31) : pose === "scroll" ? 25 : pose === "slump" ? 10 : pose === "tie" ? 38 : pose === "sit" ? 58 : pose === "punch" ? -8 : 0;
  const rightLeg = walking ? (pose === "run" ? 30 : 22) - swing * (pose === "run" ? 40 : 31) : pose === "scroll" ? 31 : pose === "slump" ? 15 : pose === "tie" ? 42 : pose === "sit" ? 62 : pose === "punch" ? 14 : 0;
  const mouth = pose === "slump" || pose === "tired" ? "M-7 -137 Q0 -143 7 -137" : pose === "hero" ? "M-8 -137 Q0 -129 8 -137" : pose === "scroll" ? "M-6 -139 Q0 -137 6 -139" : "M-7 -137 H7";
  const blink = (Math.sin(t * 13.5 + (companion ? 2 : 0)) > 0.975) ? 0.25 : 1;
  const phonePulse = 0.82 + Math.sin(t * 12) * 0.1;
  const handY = pose === "scroll" ? -62 : pose === "write" ? -49 : pose === "slump" ? -46 : -40;
  const motionSpring = spring({ frame: Math.round(t * 36), fps: 24, config: { damping: 14, stiffness: 105, mass: 0.7 } });
  return (
    <svg width={180 * scale} height={270 * scale} viewBox="-90 -210 180 270" style={{
      position: "absolute", left: x - 90 * scale,
      top: 323 + y + bob - 247 * (scale - 1),
      overflow: "visible", zIndex: companion ? 3 : 5,
    }}>
      <ellipse cx="0" cy="28" rx={walking ? 39 : 32} ry="7" fill="#17151f" opacity=".48" />
      <g transform={"rotate(" + leftLeg + " -15 -38)"}>
        <path d="M-15 -38 L-20 -4 L-35 20" fill="none" stroke="#ead7c1" strokeWidth="15" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M-15 -38 L-20 -4 L-35 20" fill="none" stroke="#24212b" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M-45 23 Q-40 16 -29 21 L-16 30 Q-13 35 -20 37 L-43 32 Q-50 29 -45 23Z" fill="#24212b" stroke="#ead7c1" strokeWidth="2.8" />
      </g>
      <g transform={"rotate(" + rightLeg + " 15 -38)"}>
        <path d="M15 -38 L22 -4 L34 20" fill="none" stroke="#ead7c1" strokeWidth="15" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M15 -38 L22 -4 L34 20" fill="none" stroke="#24212b" strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M25 23 Q32 16 42 21 L54 29 Q58 34 50 37 L27 32 Q21 29 25 23Z" fill="#24212b" stroke="#ead7c1" strokeWidth="2.8" />
      </g>
      <g transform={"rotate(" + lean + " 0 -82)"}>
        <path d="M-20 -119 Q-34 -112 -32 -82 L-28 -39 Q0 -32 28 -39 L32 -82 Q34 -112 20 -119Z" fill={shirt} stroke="#ead7c1" strokeWidth="3" strokeLinejoin="round" />
        <path d="M-13 -109 Q-19 -91 -15 -71" fill="none" stroke="#f5ccbb" strokeWidth="2.1" opacity=".45" />
        <path d="M-10 -55 H10" stroke="#8e4f62" strokeWidth="2.2" opacity=".56" />
        <path d="M-4 -104 V-82" stroke="#f0d5c1" strokeWidth="2.2" opacity=".8" />
        <circle cx="-4" cy="-78" r="2.1" fill="#f4dfca" />
      </g>
      <g transform={"rotate(" + leftArm + " -24 -105)"}>
        <path d="M-24 -105 Q-42 -88 -46 -70 L-49 -48" fill="none" stroke="#ead7c1" strokeWidth="15" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M-24 -105 Q-42 -88 -46 -70 L-49 -48" fill="none" stroke={shirt} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="-49" cy={handY} r="8" fill="#24212b" stroke="#ead7c1" strokeWidth="2.8" />
      </g>
      <g transform={"rotate(" + rightArm + " 24 -105)"}>
        <path d="M24 -105 Q42 -87 47 -68 L50 -47" fill="none" stroke="#ead7c1" strokeWidth="15" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M24 -105 Q42 -87 47 -68 L50 -47" fill="none" stroke={shirt} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="50" cy={handY} r="8" fill="#24212b" stroke="#ead7c1" strokeWidth="2.8" />
      </g>
      <g transform={"rotate(" + headTilt + " 0 -154)"}>
        <circle cx="0" cy="-154" r="37" fill="#17151e" stroke="#ead7c1" strokeWidth="3.2" />
        <ellipse cx="-12" cy="-156" rx="4.1" ry={5.2 * blink} fill="#f5eee3" />
        <ellipse cx="12" cy="-156" rx="4.1" ry={5.2 * blink} fill="#f5eee3" />
        <circle cx="-11" cy="-157" r="1.5" fill="#29242d" /><circle cx="13" cy="-157" r="1.5" fill="#29242d" />
        <path d={mouth} fill="none" stroke="#f5eee3" strokeWidth={pose === "slump" || pose === "tired" ? 2 : 2.6} strokeLinecap="round" />
        {(pose === "slump" || pose === "tired") && <path d="M-22 -176 L-9 -180 M8 -180 L22 -176" stroke="#f5eee3" strokeWidth="2.7" strokeLinecap="round" />}
        {pose === "hero" && <path d="M-18 -179 L-8 -177 M8 -177 L18 -179" stroke="#f5eee3" strokeWidth="2.5" strokeLinecap="round" />}
      </g>
      {pose === "scroll" && !companion && (
        <g transform={"translate(" + (47 + motionSpring * 2) + " " + (-64 + scrollReach * 4) + ") rotate(-12)"}>
          <rect x="-11" y="-25" width="22" height="42" rx="4" fill="#17151e" stroke="#ead7c1" strokeWidth="2.5" />
          <rect x="-7.5" y="-19" width="15" height="28" rx="2" fill="#a84f65" opacity={phonePulse} />
          <circle cx="0" cy="12" r="1.8" fill="#ead7c1" />
        </g>
      )}
      {pose === "write" && !companion && <g>
        <path d="M47 -52 L67 -39" stroke="#ead7c1" strokeWidth="4" strokeLinecap="round" />
        <path d={"M" + (66 + writeReach * 3) + " " + (39 - writeReach * 2) + " l10 7"} stroke="#d7b79b" strokeWidth="2.6" />
      </g>}
      {pose === "drink" && !companion && <g transform="translate(62 -92)">
        <path d="M-9 -14 H9 L7 10 Q0 16 -7 10Z" fill="#d6c8bb" stroke="#ead7c1" strokeWidth="2.2"/>
        <path d="M9 -10 Q20 -11 16 -1 Q14 5 8 4" fill="none" stroke="#ead7c1" strokeWidth="2.2"/>
        <path d="M-5 -9 H5" stroke="#9ab7be" strokeWidth="2" opacity=".7"/>
      </g>}
      {pose === "tie" && !companion && <g>
        <path d="M-28 17 Q0 9 28 17" fill="none" stroke="#ead7c1" strokeWidth="3"/>
        <path d="M-18 25 Q0 16 18 25" fill="none" stroke="#c56d9b" strokeWidth="3"/>
      </g>}
      {pose === "punch" && !companion && <g opacity={0.65 + Math.sin(t*18)*0.25}>
        <path d="M72 -81 l22 -8 M74 -69 l27 0 M70 -58 l21 9" stroke="#f0c58f" strokeWidth="3" strokeLinecap="round"/>
        <circle cx="73" cy="-69" r="3.5" fill="#f0c58f"/>
      </g>}
      {pose === "stretch" && !companion && <path d="M-52 -134 l-12 -15 M52 -134 l12 -15" stroke="#ead7c1" strokeWidth="2.5" opacity=".55"/>}
      {pose === "cheer" && !companion && <g>
        <path d="M-74 -108 l-12 -9 M-64 -123 l-6 -15 M74 -108 l12 -9 M64 -123 l6 -15" stroke="#f2d0a0" strokeWidth="3" strokeLinecap="round"/>
      </g>}
      {pose === "hero" && !companion && <path d="M-55 -74 l-11 -8 M-49 -86 l-4 -14 M55 -74 l11 -8 M49 -86 l4 -14" stroke="#f2d0a0" strokeWidth="3" strokeLinecap="round" opacity=".7" />}
    </svg>
  );
};

const Foreground: React.FC<{ setting: Setting; t: number; phoneOnDesk?: boolean }> = ({ setting, t, phoneOnDesk }) => (
  <svg width="100%" height="100%" viewBox="0 0 1280 720" style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 7 }}>
    {setting === "bedroom" && <>
      <path d="M255 496 Q493 525 825 493 V578 H255Z" fill="#64596f" opacity=".98" />
      <path d="M255 496 Q493 525 825 493" fill="none" stroke="#a79bb0" strokeWidth="3" opacity=".75" />
      <path d="M450 510 Q560 535 670 510" fill="none" stroke="#4e465b" strokeWidth="3" opacity=".8" />
    </>}
    {setting === "desk" && <>
      <path d="M328 454 H976 V480 H328Z" fill="#9b7a85" stroke="#352936" strokeWidth="4" />
      <path d="M360 480 V580 M940 480 V580" stroke="#362b39" strokeWidth="18" />
      <rect x="490" y="438" width="112" height="9" rx="3" fill="#e1d2c4" transform="rotate(-5 490 438)" />
      <path d="M500 434 l14 -19 l12 18" fill="none" stroke="#c9b7aa" strokeWidth="3" />
      {phoneOnDesk && <g transform={"translate(" + (t * 8) + " 0)"}>
        <rect x="798" y="417" width="28" height="49" rx="5" fill="#15141c" stroke="#dac7b4" strokeWidth="2" transform="rotate(10 812 441)" />
        <rect x="804" y="424" width="16" height="34" rx="2" fill="#473a4e" transform="rotate(10 812 441)" />
      </g>}
    </>}
    {setting === "cafe" && <>
      <path d="M280 500 Q615 470 1010 500 L980 540 H310Z" fill="#9b777c" stroke="#382b39" strokeWidth="5" />
      <path d="M350 540 V637 M934 540 V637" stroke="#342936" strokeWidth="20" />
      <ellipse cx="645" cy="501" rx="335" ry="24" fill="#e7b68e" opacity=".12" />
      <rect x="585" y="475" width="49" height="8" rx="3" fill="#d4c1ae" />
      <path d="M591 474 V456 Q610 445 628 456 V474" fill="#ded0c1" stroke="#6a5267" strokeWidth="2" />
    </>}
    {setting === "bus" && <>
      <path d="M0 602 H1280" stroke="#8d6f83" strokeWidth="3" opacity=".35" />
      <path d="M0 634 H1280" stroke="#a38a9b" strokeWidth="2" opacity=".18" />
    </>}
    {setting === "stairs" && <>
      <path d="M640 600 L1280 325" stroke="#b59ab1" strokeWidth="3" opacity=".4" />
    </>}
  </svg>
);

const DayCounter: React.FC<{ day: string }> = ({ day }) => (
  <div style={{
    position: "absolute", left: 42, top: 25, zIndex: 12,
    padding: "9px 15px", borderRadius: 11,
    border: "1.5px solid rgba(218,187,151,.82)",
    background: "rgba(26,22,32,.9)", boxShadow: "0 4px 14px rgba(0,0,0,.22)",
    color: "#e7d4be", fontSize: 13, fontWeight: 800, letterSpacing: 2,
  }}>{day}</div>
);

const RedWords: React.FC<{ words: string[]; t: number }> = ({ words, t }) => (
  <div style={{ position: "absolute", inset: 0, zIndex: 8, pointerEvents: "none" }}>
    {words.map((word, i) => {
      const x = 64 + ((i * 197 + 80) % 1100);
      const y = 150 + ((i * 83 + 38) % 330) + Math.sin(t * 5 + i) * 8;
      return <div key={word + i} style={{
        position: "absolute", left: x, top: y,
        color: "#c85c70", fontFamily: '"Comic Neue", Arial, sans-serif',
        fontWeight: 800, fontSize: i % 2 ? 21 : 27,
        opacity: Math.min(0.75, 0.2 + t * 0.8), transform: "rotate(" + ((i % 3) * 5 - 5) + "deg)",
        textShadow: "0 0 12px rgba(191,69,91,.13)",
      }}>{word}</div>;
    })}
  </div>
);

const Caption: React.FC<{ title: string; subtitle: string; t: number; isEnd: boolean }> = ({ title, subtitle, t, isEnd }) => {
  if (isEnd) return (
    <div style={{
      position: "absolute", inset: 0, zIndex: 15,
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      padding: "0 80px 40px", textAlign: "center",
    }}>
      <div style={{
        opacity: clampInterp(t, [0.08, 0.32], [0, 1]),
        transform: "translateY(" + (12 * (1 - clampInterp(t, [0.08, 0.32], [0, 1])) - 35) + "px)",
        fontSize: 42, lineHeight: 1.16, fontWeight: 800, letterSpacing: 1.2,
        color: "#f2e7da", maxWidth: 1040, textShadow: "0 5px 26px rgba(0,0,0,.5)",
      }}>{title}</div>
      <div style={{ marginTop: 22, color: "#d2a28e", fontSize: 21, letterSpacing: 2, opacity: clampInterp(t, [0.28, 0.5], [0, 1]) }}>
        {subtitle}
      </div>
      <div style={{ marginTop: 26, width: 70, height: 3, background: "#c56d9b", opacity: clampInterp(t, [0.45, 0.62], [0, 1]) }} />
    </div>
  );
  return (
    <div style={{
      position: "absolute", left: 0, right: 0, bottom: 30, zIndex: 15,
      display: "flex", justifyContent: "center", padding: "0 90px", textAlign: "center",
      opacity: clampInterp(t, [0.03, 0.17, 0.82, 0.97], [0, 1, 1, 0]),
    }}>
      <div style={{
        maxWidth: 1070, padding: "8px 16px 9px",
        background: "rgba(17,15,22,.58)",
        color: "#f3e9de", borderRadius: 4,
        borderBottom: "1px solid rgba(224,194,170,.24)",
        fontSize: 21, fontWeight: 600, letterSpacing: ".1px", lineHeight: 1.3,
        textShadow: "0 2px 6px rgba(0,0,0,.85)",
      }}>{subtitle}</div>
    </div>
  );
};


const MusicSlice: React.FC<{ file: string; from: number; duration: number; volume: number }> = ({ file, from, duration, volume }) => (
  <Sequence from={from} durationInFrames={duration}>
    <Audio
      src={staticFile("audio/" + file + ".wav")}
      volume={(f) => volume * clampInterp(f, [0, 18, Math.max(19, duration - 18), duration], [0, 1, 1, 0])}
    />
  </Sequence>
);

const SoundCue: React.FC<{ file: string; from: number; duration: number; volume: number }> = ({ file, from, duration, volume }) => (
  <Sequence from={from} durationInFrames={duration}>
    <Audio
      src={staticFile("audio/" + file + ".wav")}
      volume={(f) => volume * clampInterp(f, [0, Math.min(3, duration - 1), Math.max(4, duration - 3), duration], [0, 1, 1, 0])}
    />
  </Sequence>
);

const AudioDesign: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    {/* H2 music arc: sad -> dark -> intentional silence -> hope -> rise -> resolve. */}
    <MusicSlice file="bed_sad_Am_64bpm" from={0} duration={360} volume={0.28} />
    <MusicSlice file="bed_dark_E_drone" from={360} duration={240} volume={0.22} />
    {/* frames 600-719 are intentionally silent: the choice to put the phone down. */}
    <MusicSlice file="bed_hope_F_76bpm" from={720} duration={240} volume={0.24} />
    <MusicSlice file="bed_rise_Am_96bpm" from={960} duration={300} volume={0.25} />
    <MusicSlice file="bed_resolve_C_70bpm" from={1260} duration={180} volume={0.28} />

    {/* SFX are tied to the action beats, not sprinkled randomly. */}
    <SoundCue file="notif_msg" from={38} duration={12} volume={0.32} />
    <SoundCue file="notif_msg" from={150} duration={12} volume={0.27} />
    <SoundCue file="clock_tick" from={364} duration={96} volume={0.23} />
    <SoundCue file="tempt_whisper" from={493} duration={40} volume={0.22} />
    <SoundCue file="page_flip" from={672} duration={16} volume={0.26} />
    <SoundCue file="footsteps" from={736} duration={78} volume={0.28} />
    <SoundCue file="door_open" from={858} duration={32} volume={0.24} />
    <SoundCue file="footsteps" from={990} duration={78} volume={0.22} />
    <SoundCue file="glass_shatter" from={1144} duration={40} volume={0.3} />
    <SoundCue file="breath_in" from={1210} duration={24} volume={0.24} />
    <SoundCue file="sting_low" from={1360} duration={72} volume={0.22} />
  </AbsoluteFill>
);

export const OneMoreScroll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const shotIndex = Math.min(shots.length - 1, Math.floor(frame / SHOT_FRAMES));
  const local = frame - shotIndex * SHOT_FRAMES;
  const t = Math.max(0, Math.min(1, local / (SHOT_FRAMES - 1)));
  const shot = shots[shotIndex];
  const next = shots[shotIndex + 1];
  const eased = Easing.inOut(Easing.cubic)(t);
  const x = shot.x0 + (shot.x1 - shot.x0) * eased;
  const y = shot.y0 + (shot.y1 - shot.y0) * eased;
  const zoom = shot.zoom0 + (shot.zoom1 - shot.zoom0) * eased;
  const pan = shot.pan0 + (shot.pan1 - shot.pan0) * eased;
  const isEnd = shot.setting === "end";

  const fadeIn = clampInterp(local, [0, 14], [0, 1]);
  const fadeOut = clampInterp(local, [SHOT_FRAMES - 14, SHOT_FRAMES - 1], [1, 0]);
  const incomingDip = shotIndex === 0 || !!shot.dip;
  const outgoingDip = !!next?.dip;
  const visibility = Math.min(incomingDip ? fadeIn : 1, outgoingDip ? fadeOut : 1);

  const shadowStrength = shot.shadow * (0.9 + Math.sin(local / 18) * 0.1);
  const shadowX = shot.shadowX + Math.sin(t * Math.PI) * 16;
  const headerOpacity = clampInterp(local, [0, 16], [0, 0.85]);

  return (
    <AbsoluteFill style={{
      backgroundColor: "#17151e", color: "#f1e5d8",
      fontFamily: '"Be Vietnam Pro", "Arial", sans-serif', overflow: "hidden",
    }}>
      {/* Background and character stage move at different rates for parallax. */}
      <div style={{
        position: "absolute", inset: -16,
        transform: "translateX(" + (pan * 0.34) + "px) scale(" + (zoom * 0.99) + ")",
        transformOrigin: "50% 56%",
      }}>
        <Backdrop setting={shot.setting} t={t} frame={frame} />
      </div>
      <div style={{
        position: "absolute", inset: -18, overflow: "hidden",
        transform: "translateX(" + pan + "px) scale(" + zoom + ")",
        transformOrigin: "50% 55%",
      }}>
        {shot.shadow > 0.025 && shot.setting !== "end" && (
          <ShadowFigure x={shadowX} strength={shadowStrength} frame={frame} />
        )}
        {shot.setting === "phone" && <PhoneInsert t={t} />}
        {!shot.hideCharacter && shot.setting !== "phone" && (
          <Character x={x} y={y} pose={shot.pose} t={t} shirt={shot.shirt} scale={shot.scale} />
        )}
        {shot.friend && <Character
          x={x + (shot.setting === "cafe" ? 270 : 220)}
          y={shot.setting === "cafe" ? 0 : 0}
          pose="meet" t={Math.max(0, t - 0.12)} shirt="#6e59bd"
          scale={shot.setting === "cafe" ? 1.08 : 0.92} companion
        />}
        {shot.setting === "bus" && <>
          <Character x={180} y={0} pose="walk" t={t + 0.2} shirt="#d7a56d" scale={0.78} companion />
          <Character x={1030} y={0} pose="stand" t={t} shirt="#6c8292" scale={0.85} companion />
        </>}
        {shot.setting === "phone" && <RedWords words={shot.redWords || []} t={t} />}
        {shot.setting === "mirror" && <RedWords words={shot.redWords || []} t={t} />}
        {shot.setting === "void" && <RedWords words={shot.redWords || []} t={t} />}
        {shot.setting === "end" && <Character x={640} y={15} pose="hero" t={t} shirt={shot.shirt} scale={0.74} />}
        <Foreground setting={shot.setting} t={t} phoneOnDesk={shot.phoneOnDesk} />
      </div>

      {/* Cinematic letterbox; content stays inside a safe area. */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 12, background: "#09080d", zIndex: 20 }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 13, background: "#09080d", zIndex: 20 }} />

      {shot.day && <DayCounter day={shot.day} />}

      {!isEnd && <>
        <div style={{
          position: "absolute", top: 26, right: 42, zIndex: 12,
          color: "#c9a48d", fontSize: 10, fontWeight: 800, letterSpacing: 2.5, opacity: headerOpacity,
        }}>AN ANIMATED SHORT FILM</div>
        <div style={{
          position: "absolute", left: 0, right: 0, bottom: 0, height: 164, zIndex: 10,
          background: "linear-gradient(180deg,rgba(13,11,17,0),rgba(13,11,17,.22) 38%,rgba(13,11,17,.76))",
          pointerEvents: "none",
        }} />
      </>}

      <Caption title={shot.title} subtitle={shot.subtitle} t={t} isEnd={isEnd} />
      <AudioDesign />
      <div style={{ position: "absolute", inset: 0, backgroundColor: "#100e16", opacity: 1 - visibility, pointerEvents: "none", zIndex: 30 }} />
    </AbsoluteFill>
  );
};
