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
 const drift=frame*.22;
 return <AbsoluteFill style={{background:"linear-gradient(180deg,#82bce4 0%,#b9d6e2 37%,#e8d9d4 69%,#e8bda9 100%)",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <linearGradient id="oil-cloud-light" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#fff" stopOpacity=".93"/><stop offset="1" stopColor="#f6ede3" stopOpacity=".05"/></linearGradient>
    <linearGradient id="oil-cloud-warm" x1="0" x2="1"><stop stopColor="#f4c6a5" stopOpacity=".05"/><stop offset=".5" stopColor="#fff3df" stopOpacity=".75"/><stop offset="1" stopColor="#f6bba5" stopOpacity=".08"/></linearGradient>
    <filter id="oil-soft-22"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="oil-soft-8"><feGaussianBlur stdDeviation="8"/></filter>
   </defs>
   <g transform={"translate("+(-drift)+",0)"} opacity=".7" filter="url(#oil-soft-22)">
    <path d="M-80 220C90 80 280 115 405 220C535 92 715 100 825 229C940 105 1110 125 1218 240C1390 105 1568 140 1680 244C1810 150 1970 165 2060 275L2060 415L-80 430Z" fill="url(#oil-cloud-light)"/>
    <path d="M-90 500C60 410 200 425 330 520C470 390 615 390 750 535C880 407 1050 415 1180 520C1320 405 1480 420 1605 545C1750 435 1900 465 2050 560L2050 705L-90 720Z" fill="#f9e9d9" opacity=".76"/>
    <path d="M-60 690C100 580 250 600 380 700C505 600 685 605 810 725C965 595 1120 610 1250 710C1400 600 1585 620 1705 725C1835 640 1965 650 2045 755L2045 850L-60 860Z" fill="url(#oil-cloud-warm)"/>
   </g>
   <g transform={"translate("+(drift*.55)+",0)"} filter="url(#oil-soft-8)" fill="none" strokeLinecap="round">
    <path d="M-80 310C180 180 375 200 565 286S900 355 1110 260S1520 205 1745 293S1950 300 2070 265" stroke="#fff" strokeWidth="22" opacity=".55"/>
    <path d="M-55 365C170 270 350 282 525 352S835 400 1040 324S1430 270 1630 345S1900 352 2050 320" stroke="#a6cde2" strokeWidth="17" opacity=".36"/>
    <path d="M-80 580C150 490 320 500 515 578S900 620 1100 525S1490 490 1690 568S1940 570 2080 540" stroke="#fff4e4" strokeWidth="30" opacity=".62"/>
    <path d="M-70 720C190 620 420 640 625 710S1010 770 1210 680S1570 650 1760 715S1970 710 2070 685" stroke="#f0d1c8" strokeWidth="26" opacity=".5"/>
   </g>
   <path d="M0 867C170 838 280 860 430 852C580 844 700 874 850 859C1030 840 1160 871 1345 846C1535 822 1690 860 1810 835L1920 842L1920 1080H0Z" fill="#5e9eb8" opacity=".24"/>
   <path d="M0 943C180 915 310 952 470 932C630 912 755 951 910 929C1080 903 1235 945 1390 916C1580 884 1760 930 1920 898L1920 1080H0Z" fill="#2f79a3" opacity=".55"/>
   <path d="M0 1018C165 986 320 1017 505 1002C690 988 820 1022 1000 1002C1170 983 1320 1014 1510 989C1705 965 1815 1008 1920 982L1920 1080H0Z" fill="#1e6f96" opacity=".52"/>
  </svg>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,rgba(255,255,255,.06),transparent 63%,rgba(248,204,185,.25))"}}/>
  <Noise opacity={.028}/>
 </AbsoluteFill>;
};

const OpeningScene = () => {
 const f=useCurrentFrame();
 const text="Introducing OpenDesign Motion";
 const count=Math.floor(e(f,15,64,0,text.length));
 const pressed=e(f,76,82);
 const cursor=e(f,48,76,0,1);
 const typing=f>=15;
 return <AbsoluteFill style={full}>
  <CloudSky frame={f}/>
  <div style={{position:"absolute",top:225,left:0,right:0,display:"flex",justifyContent:"center",alignItems:"center",color:"#19272c"}}>
   <div style={{fontFamily:"Georgia,serif",fontSize:82,fontWeight:700,letterSpacing:"-.055em",position:"relative",whiteSpace:"nowrap"}}>
    Let’s create <span style={{position:"relative",display:"inline-block"}}><span style={{position:"absolute",left:-5,right:-8,top:"55%",height:31,background:"#b6e65e",transform:"rotate(-1deg)"}}/><span style={{position:"relative"}}>Motion design</span></span>
   </div>
  </div>
  <div style={{position:"absolute",top:345,left:0,right:0,textAlign:"center",color:"rgba(35,52,58,.68)",fontSize:18,letterSpacing:".06em",fontWeight:550}}>Good work starts here</div>
  <div style={{position:"absolute",left:330,right:330,top:438,height:286,background:"rgba(255,255,255,.94)",border:"1px solid rgba(255,255,255,.99)",borderRadius:24,boxShadow:"0 27px 75px rgba(49,82,91,.2),0 4px 16px rgba(40,72,82,.09)",backdropFilter:"blur(20px)",transform:"translateY("+((1-pop(f,30,0,80,18))*55)+"px) scale("+(0.99+.01*pop(f,30,0,80,18)-pressed*.008)+")",padding:"36px 38px",boxSizing:"border-box"}}>
   <div style={{position:"relative",color:typing?"#263033":"#a2a9a8",fontSize:35,fontWeight:480,letterSpacing:"-.035em",minHeight:52,whiteSpace:"nowrap"}}>
    {typing?text.slice(0,count):"Create a Motion design: Motion graphics, art and product"}
    {typing?<span style={{display:"inline-block",width:2,height:34,background:count<text.length?"#313a3d":"transparent",verticalAlign:"middle",marginLeft:4}}/>:null}
   </div>
   <div style={{position:"absolute",bottom:23,left:38,display:"flex",alignItems:"center",gap:18}}>
    <div style={{fontSize:22,color:"#9ca5a4"}}>＋</div><div style={{fontSize:22,color:"#9ca5a4"}}>◉</div>
    <div style={{background:"#d9f5d9",color:"#26763d",padding:"8px 17px",borderRadius:7,fontSize:17,fontWeight:850}}>✦ Motion design</div>
    <div style={{fontSize:15,color:"#899493"}}>Working directory⌄</div>
   </div>
   <div style={{position:"absolute",right:31,bottom:22,display:"flex",gap:9,alignItems:"center"}}>
    <span style={{width:10,height:10,borderRadius:"50%",background:"#67d46c"}}/><span style={{width:10,height:10,borderRadius:"50%",background:"#5b72dc"}}/>
    <div style={{width:58,height:58,borderRadius:"50%",background:"#12191b",display:"grid",placeItems:"center",transform:"scale("+(1-pressed*.09)+")",boxShadow:"0 4px 14px rgba(20,30,31,.22)"}}>
     <svg viewBox="0 0 30 30" width="27" height="27"><path d="M5 15H24M16 6L25 15L16 24" fill="none" stroke="#75e44c" strokeWidth="2.7" strokeLinecap="round" strokeLinejoin="round"/></svg>
    </div>
   </div>
  </div>
  <div style={{position:"absolute",top:760,left:730+cursor*520,width:29,height:38,filter:"drop-shadow(0 3px 3px rgba(0,0,0,.3))"}}>
   <svg viewBox="0 0 30 40" width="29" height="38"><path d="M2 2L2 33L10 25L17 38L23 35L16 22L28 22Z" fill="#fff" stroke="#262b2d" strokeWidth="2" strokeLinejoin="round"/></svg>
  </div>
 </AbsoluteFill>;
};

const HeroTitle = () => {
 const f=useCurrentFrame(),p=pop(f,30,0,44,12),opacity=fadeOut(f,48,9);
 const letters=["M","O","T","I","O","N"];
 return <AbsoluteFill style={full}>
  <CloudSky frame={f+100}/>
  <div style={{position:"absolute",top:190,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontStyle:"italic",fontSize:30,fontWeight:650,color:"#fff",opacity:e(f,0,6),textShadow:"0 2px 12px rgba(0,0,0,.12)"}}>Introducing</div>
  <div style={{position:"absolute",top:300,left:0,right:0,textAlign:"center",fontFamily:displayFont,fontSize:119,fontWeight:850,letterSpacing:"-.07em",color:"#fff",opacity,transform:"translateY("+((1-p)*45)+"px)",textShadow:"0 2px 0 #d7e5e5,0 4px 0 #b7d0d5,0 7px 0 #8fb4c2,0 11px 0 #6695aa,0 16px 23px rgba(22,69,91,.26)"}}>OpenDesign</div>
  <div style={{position:"absolute",left:0,right:0,top:440,height:300,display:"flex",justifyContent:"center",alignItems:"center",gap:0,opacity,transform:"translateY("+((1-p)*60)+"px) scale("+(0.9+.1*p)+")",perspective:1200}}>
   {letters.map((ch,i)=>{
    const lag=i*2.1,enter=e(f,lag,lag+14),swing=Math.sin((f-lag)*.18)*5;
    const colors=["#fff","#fff","#fff","#f8f1e8","#fff","#fff"];
    return <div key={i} style={{fontFamily:displayFont,fontSize:320,fontWeight:1000,letterSpacing:"-.11em",lineHeight:.85,color:colors[i],transform:"translateY("+(1-enter)*(-180+swing*7)+"px) translateX("+(i===3?0:0)+"px) rotateY("+(i===3?-18:0)+"deg) rotateX("+(i===3?8:0)+"deg)",textShadow:"1px 1px 0 #e0e7e8,3px 4px 0 #b6cbd2,6px 7px 0 #8eafbb,10px 12px 0 #5e8ba0,16px 20px 0 #345d75,24px 31px 33px rgba(25,62,83,.3)",marginLeft:i===0?0:-12}}>{ch}</div>;
   })}
  </div>
  <div style={{position:"absolute",left:0,right:0,bottom:89,textAlign:"center",color:"#fff",fontSize:18,fontWeight:800,letterSpacing:".24em",opacity:fadeOut(f,47,7),textShadow:"0 2px 12px rgba(0,0,0,.16)"}}>A NEW CREATIVE WORKFLOW</div>
 </AbsoluteFill>;
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
 const f=useCurrentFrame();
 const title=e(f,0,8),alt=e(f,13,22),marker=e(f,3,13);
 return <AbsoluteFill style={{...full,background:"#faf9f5",color:"#111315"}}>
  <div style={{position:"absolute",left:0,right:0,top:292,display:"flex",flexDirection:"column",alignItems:"center",transform:"translateY("+((1-title)*23)+"px)"}}>
   <div style={{display:"flex",alignItems:"baseline",justifyContent:"center",whiteSpace:"nowrap",gap:22,opacity:title}}>
    <Word size={168} color="#111315" tracking={-.085}>The</Word>
    <span style={{position:"relative",display:"inline-block"}}>
     <span style={{position:"absolute",left:-13,right:-18,top:"53%",height:80,background:"#a1ef4d",transform:"scaleX("+marker+") rotate(-.7deg)",transformOrigin:"left center"}}/>
     <span style={{position:"relative"}}><Word size={168} color="#111315" tracking={-.085}>open-source</Word></span>
    </span>
   </div>
   <div style={{marginTop:-4,opacity:alt,transform:"translateY("+((1-alt)*25)+"px)"}}><Word size={164} color="#111315" tracking={-.085}>alternative</Word></div>
   <div style={{marginTop:48,display:"flex",alignItems:"center",gap:16,color:"#898985",opacity:e(f,3,13)}}>
    <span style={{fontSize:39,fontWeight:550}}>to</span><RadialMark frame={f} size={47} color="#e97962"/>
    <span style={{fontSize:54,fontWeight:850,color:"#1b1c1e",letterSpacing:"-.06em"}}>Claude Motion.</span>
   </div>
  </div>
 </AbsoluteFill>;
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
  <GalleryPoster index={index%30} frame={frame+index*2}/>
 </div>;
};

const GalleryWall=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,72,16);
 const pan=e(f,0,77,5,-34),ry=e(f,0,77,-1.5,-7),rz=e(f,0,77,.15,-.45);
 const order=Array.from({length:30},(_,i)=>i),claimOpacity=1-e(f,0,15);
 return <AbsoluteFill style={{...full,background:"#f3f1e9",overflow:"hidden"}}>
  <div style={{position:"absolute",left:78,right:78,top:76,bottom:58,display:"grid",gridTemplateColumns:"repeat(6,263px)",gridTemplateRows:"repeat(5,148px)",gap:13,justifyContent:"center",alignContent:"center",transform:"perspective(1750px) rotateY("+ry+"deg) rotateX(1.5deg) rotateZ("+rz+"deg) translateX("+pan+"px) translateY("+((1-p)*40)+"px) scale("+(0.965+.035*p)+")",transformOrigin:"center center"}}>
   {order.map((id,i)=><GalleryCard key={i} index={id} frame={f+i*2}/>)}
  </div>
  <div style={{position:"absolute",inset:0,pointerEvents:"none",background:"linear-gradient(180deg,rgba(255,255,255,.18),transparent 14%,transparent 85%,rgba(210,205,193,.12))"}}/>
  <div style={{position:"absolute",inset:0,background:"rgba(24,27,29,.22)",opacity:claimOpacity,pointerEvents:"none"}}/>
  <div style={{position:"absolute",left:"15%",right:"15%",top:"18%",height:"61%",background:"#fff",borderRadius:24,boxShadow:"0 22px 65px rgba(30,34,34,.17)",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",opacity:claimOpacity,transform:"translateY("+(claimOpacity*5)+"px) scale("+(0.985+.015*claimOpacity)+")",pointerEvents:"none"}}>
   <div style={{fontFamily:displayFont,fontSize:86,fontWeight:950,color:"#111315",letterSpacing:"-.075em",lineHeight:1.06,textAlign:"center"}}>The <span style={{background:"#8ded4e",padding:"0 11px",borderRadius:5}}>open-source</span><br/>alternative</div>
   <div style={{marginTop:28,fontSize:34,color:"#8a8d8d",fontWeight:600}}>to <span style={{color:"#e08068",fontSize:36}}>✳</span> <span style={{color:"#17191b",fontWeight:900}}>Claude Motion.</span></div>
  </div>
  <Noise opacity={.025}/>
 </AbsoluteFill>;
}


const Comic1952 = () => {
 const f=useCurrentFrame(),sweep=e(f,0,4,-30,0);
 return <AbsoluteFill style={{...full,background:"#f7f1e5",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:38,display:"grid",gridTemplateColumns:"24% 52% 24%",gap:13}}>
   <div style={{position:"relative",background:"#e64f91",overflow:"hidden"}}>
    <svg viewBox="0 0 430 1000" width="100%" height="100%"><rect width="430" height="1000" fill="#e64f91"/><path d="M210 930L210 175M210 430L65 295M210 575L362 415M210 690L70 590M210 295L343 165" stroke="#176d4f" strokeWidth="32" fill="none"/>{Array.from({length:20},(_,i)=><path key={i} d={"M"+(210+(i%2?1:-1)*(35+(i%4)*19))+" "+(245+i*32)+"l"+(i%2?31:-31)+" -"+(28+(i%3)*12)} stroke="#f4d54d" strokeWidth="15" fill="none"/>)}</svg>
   </div>
   <div style={{position:"relative",background:"#faf5e8",overflow:"hidden"}}>
    <div style={{position:"absolute",top:20,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontSize:38,fontWeight:900,color:"#1f3e79"}}>1952</div>
    <div style={{position:"absolute",left:"50%",top:"51%",width:500,height:500,transform:"translate(-50%,-50%)",borderRadius:"50%",border:"24px solid #315fbb",background:"#fff8e7",display:"grid",placeItems:"center",boxShadow:"0 0 0 9px #eee5d2"}}>
     <div style={{width:275,height:275,borderRadius:"50%",border:"15px solid #f0d34b",background:"#f7f2e7",display:"grid",placeItems:"center"}}><svg viewBox="0 0 100 120" width="100%" height="100%"><path d="M8 4L93 61L52 68L38 116Z" fill="#101214"/></svg></div>
    </div>
    <svg viewBox="0 0 1000 1000" width="100%" height="100%" style={{position:"absolute",inset:0}}>
     <path d={"M-30 "+(190+sweep)+"L120 "+(190+sweep)+"L240 "+(280+sweep)+"L350 "+(250+sweep)+"L460 "+(375+sweep)+"L590 "+(345+sweep)+"L715 "+(495+sweep)+"L1030 "+(490+sweep)} stroke="#121516" strokeWidth="52" fill="none" strokeLinejoin="miter"/>
     <path d={"M-30 "+(190+sweep)+"L120 "+(190+sweep)+"L240 "+(280+sweep)+"L350 "+(250+sweep)+"L460 "+(375+sweep)+"L590 "+(345+sweep)+"L715 "+(495+sweep)+"L1030 "+(490+sweep)} stroke="#f4d044" strokeWidth="34" fill="none" strokeLinejoin="miter"/>
    </svg>
    <div style={{position:"absolute",left:0,right:0,bottom:34,textAlign:"center",fontSize:17,fontWeight:900,letterSpacing:".24em",color:"#253d70"}}>CUT-OUTS / THE IDEA</div>
   </div>
   <div style={{position:"relative",background:"#168c86",overflow:"hidden"}}>
    <svg viewBox="0 0 430 1000" width="100%" height="100%"><rect width="430" height="1000" fill="#168c86"/><path d="M215 940L215 120M215 335L60 225M215 505L366 347M215 675L73 560M215 250L350 135" stroke="#f0a04c" strokeWidth="31" fill="none"/>{Array.from({length:20},(_,i)=><path key={i} d={"M"+(215+(i%2?1:-1)*(38+(i%4)*16))+" "+(180+i*34)+"l"+(i%2?30:-30)+" -"+(23+(i%3)*12)} stroke="#f3d247" strokeWidth="15" fill="none"/>)}</svg>
   </div>
  </div>
 </AbsoluteFill>;
};


const Comic1962=()=>{
 const f=useCurrentFrame(),scale=.985+.015*e(f,0,15);
 return <AbsoluteFill style={{...full,background:"#f7efdb",overflow:"hidden",transform:"scale("+scale+")"}}>
  <div style={{position:"absolute",inset:25,display:"grid",gridTemplateColumns:"18% 64% 18%",gridTemplateRows:"1fr 1fr",gap:10}}>
   <div style={{background:"#f1cb42",border:"8px solid #17191b",display:"grid",placeItems:"center",fontFamily:displayFont,fontSize:30,fontWeight:1000,color:"#151719",writingMode:"vertical-rl",letterSpacing:".12em"}}>1962 · POP</div>
   <div style={{gridColumn:"2",gridRow:"1 / span 2",position:"relative",background:"#77a8e7",border:"9px solid #17191b",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:-45,background:"repeating-conic-gradient(from -8deg at 50% 48%,#fff9e7 0deg 2.7deg,#73a5e4 2.7deg 9deg)"}}/>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#2b66b6 0 4px,transparent 4.6px)",backgroundSize:"23px 23px",opacity:.55}}/>
    <div style={{position:"absolute",left:"16%",top:"15%",width:"68%",height:"70%",borderRadius:"50%",background:"#f7d747",border:"10px solid #151719",boxShadow:"0 0 0 10px #fff7de"}}/>
    <div style={{position:"absolute",left:"23%",top:"25%",width:"55%",height:"52%",borderRadius:"50%",background:"#e64335",border:"10px solid #151719",display:"grid",placeItems:"center",boxShadow:"inset 0 0 0 9px #f4d449"}}>
     <div style={{width:"66%",height:"66%",borderRadius:"50%",background:"#fffdf0",border:"9px solid #151719",display:"grid",placeItems:"center"}}>
      <svg viewBox="0 0 100 120" width="100%" height="100%"><path d="M8 4L94 62L49 67L37 116Z" fill="#101214"/></svg>
     </div>
    </div>
    <div style={{position:"absolute",left:27,top:24,padding:"8px 18px",background:"#f7db47",border:"5px solid #151719",fontSize:23,fontWeight:1000,fontStyle:"italic",color:"#17191b",transform:"rotate(-2deg)"}}>MEANWHILE…</div>
    <div style={{position:"absolute",right:25,top:22,textAlign:"right",fontFamily:displayFont,fontSize:54,fontWeight:1000,color:"#151719",lineHeight:.83}}>IN<br/>1962</div>
    <div style={{position:"absolute",right:18,bottom:24,padding:"8px 26px",background:"#f7d747",border:"6px solid #151719",fontFamily:displayFont,fontSize:34,fontWeight:1000,color:"#e64335",clipPath:"polygon(50% 0,61% 18%,82% 4%,81% 29%,100% 39%,84% 56%,97% 78%,71% 74%,60% 100%,44% 82%,20% 98%,23% 70%,0 61%,18% 43%,7% 18%,37% 24%)"}}>CLICK!</div>
    <div style={{position:"absolute",left:25,right:25,bottom:19,height:5,background:"#151719",opacity:.75}}/>
   </div>
   <div style={{background:"#f5d6df",border:"8px solid #17191b",backgroundImage:"radial-gradient(#dca4b6 2.3px,transparent 2.8px)",backgroundSize:"16px 16px",display:"grid",placeItems:"center",fontSize:37,fontWeight:1000,color:"#17191b"}}>•••</div>
   <div style={{background:"#f5d6df",border:"8px solid #17191b",backgroundImage:"radial-gradient(#dca4b6 2.3px,transparent 2.8px)",backgroundSize:"16px 16px",display:"grid",placeItems:"center",fontSize:29,fontWeight:1000,color:"#17191b"}}>SFX!</div>
  </div>
 </AbsoluteFill>;
};

const Future3D = () => {
 const f=useCurrentFrame(),p=e(f,0,15);
 return <AbsoluteFill style={{...full,background:"radial-gradient(ellipse at 50% 48%,#314de8,#10249b 72%,#07176c)",color:"#fff",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><linearGradient id="future-metal-v13" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#fff"/><stop offset=".28" stopColor="#c9d1d7"/><stop offset=".52" stopColor="#f8f8f5"/><stop offset=".78" stopColor="#99a6ba"/><stop offset="1" stopColor="#f4f4ed"/></linearGradient></defs>
   {Array.from({length:28},(_,i)=><path key={i} d={"M"+(i*78)+" 0L"+(i*78+450)+" 1080"} stroke="#9eb4ff" strokeWidth="1" opacity=".12"/>)}
   <path d="M0 845Q400 770 800 850T1600 830T1920 845" stroke="#9db4ff" strokeWidth="2" fill="none" opacity=".3"/>
  </svg>
  <div style={{position:"absolute",left:-20,right:-20,top:265,transform:"translateY("+(1-p)*50+"px)",textAlign:"center",fontFamily:displayFont,fontSize:320,fontWeight:1000,letterSpacing:"-.11em",color:"url(#future-metal-v13)",background:"linear-gradient(180deg,#fff,#c7d0d7 40%,#fff 55%,#8d9caf 83%,#f9f8f2)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent",filter:"drop-shadow(0 3px 0 #8b9caa) drop-shadow(0 8px 0 #4a5c9a) drop-shadow(0 17px 0 #1d337c) drop-shadow(0 29px 26px rgba(0,0,0,.3)"}}>FUTURE</div>
  <div style={{position:"absolute",left:0,right:0,top:658,fontSize:57,fontWeight:900,letterSpacing:".025em",textAlign:"center",color:"#fff",textShadow:"0 4px 20px rgba(0,0,0,.28)"}}>IS ALREADY HERE.</div>
 </AbsoluteFill>;
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
 const f=useCurrentFrame(),drift=Math.sin(f/5)*13;
 return <AbsoluteFill style={{...full,background:"#17255d",color:"#fff",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><linearGradient id="motion-sky-v15" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#233b89"/><stop offset=".5" stopColor="#101e4f"/><stop offset="1" stopColor="#304d8c"/></linearGradient></defs>
   <rect width="1920" height="1080" fill="url(#motion-sky-v15)"/>
   {Array.from({length:95},(_,i)=>{
    const x=(i*137)%1920,y=(i*293)%1080,w=45+(i%5)*34;
    return <path key={i} d={"M"+x+" "+y+"q "+w+" -18 "+(w*1.6)+" "+(i%2?24:-32)} fill="none" stroke={i%3===0?"#9caed4":"#5169a4"} strokeWidth={i%4===0?20:11} strokeLinecap="round" opacity=".28"/>;
   })}
   <path d="M370 180Q930 115 1530 182L1490 720Q945 765 385 700Z" fill="#111827" stroke="#f6f0da" strokeWidth="22"/>
   <path d="M395 198Q920 145 1505 202L1465 696Q945 735 415 680Z" fill="#1a315d" stroke="#8d9fc5" strokeWidth="4"/>
   {Array.from({length:16},(_,i)=><g key={i} fill="#f5eddb"><rect x={390+i*73} y="150" width="46" height="35" rx="5"/><rect x={390+i*73} y="714" width="46" height="35" rx="5"/></g>)}
   <path d={"M520 560L"+(830+drift)+" 285L705 585L660 500Z"} fill="#fff9e8" stroke="#d4d8df" strokeWidth="7"/>
   <path d="M705 585L830 285L765 610" fill="#cbd4e4" opacity=".65"/>
   <path d="M505 480Q650 425 780 465" stroke="#f6e9c8" strokeWidth="5" fill="none" opacity=".65"/>
   <g transform="translate(350 715) rotate(-8)">
    <rect x="0" y="30" width="315" height="235" rx="73" fill="#080b14" stroke="#f6f0df" strokeWidth="13"/>
    <circle cx="153" cy="126" r="86" fill="#121827" stroke="#f7f0e0" strokeWidth="15"/>
    <circle cx="153" cy="126" r="63" fill="#090d17" stroke="#b1bdd2" strokeWidth="5"/>
    <circle cx="111" cy="93" r="18" fill="#fff"/><circle cx="196" cy="93" r="18" fill="#fff"/>
    <path d="M110 151Q153 190 202 151" stroke="#f6eee0" strokeWidth="11" fill="none" strokeLinecap="round"/>
    <rect x="265" y="170" width="90" height="43" rx="21" fill="#0b0e18" stroke="#eee7d5" strokeWidth="5"/>
    <path d="M62 29L98 -14L210 -14L250 29" fill="#0d1220" stroke="#eee7d5" strokeWidth="9"/>
   </g>
   <path d="M0 930Q260 825 510 925T1040 910T1530 930T1920 900V1080H0Z" fill="#0b1436" opacity=".68"/>
  </svg>
  <div style={{position:"absolute",left:0,right:0,bottom:50,textAlign:"center",fontFamily:"Georgia,serif",fontSize:91,fontStyle:"italic",fontWeight:600,color:"#fff4e1",textShadow:"0 4px 12px rgba(0,0,0,.25)"}}>motion films</div>
  <div style={{position:"absolute",left:55,top:42,fontSize:14,fontWeight:850,letterSpacing:".18em",color:"#c2cce0"}}>02 / OPEN DESIGN FILMS</div>
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
 const f=useCurrentFrame();
 const palette=["#f9e6c8","#e9d55b","#e84e36","#4299ab","#3277ad","#e3b03c","#242a32","#a0cdd2"];
 return <AbsoluteFill style={{...full,background:"#030407",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 30% 52%,#151b21,#020305 62%)"}}/>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" shapeRendering="crispEdges" style={{position:"absolute",inset:0}}>
   {Array.from({length:45*25},(_,i)=>{
    const x=i%45,y=Math.floor(i/45),px=x*42,py=y*43;
    const cx=15,cy=12.5,dist=Math.hypot(x-cx,y-cy);
    let color=null,op=.95;
    if(dist<5.2&&dist>4.1)color="#d2a93c";
    else if(dist<4.1&&dist>3.3)color="#151b21";
    else if(dist<3.3&&dist>2.2)color="#3e705b";
    else if(dist<2.2&&dist>1.2)color="#e0dfc9";
    else if(dist<=1.2)color="#0b1319";
    if(x>20&&y>=11&&y<=14){
     const bands=["#f1d13d","#ee573c","#db3389","#8944cb","#3b75e9","#34c6c4"];
     color=bands[Math.min(5,Math.floor((y-11)*1.5))];op=.92;
    }
    if(x>20&&y===10&&x%4===0)color="#fff";
    if(!color)return null;
    return <rect key={i} x={px} y={py} width="42" height="43" fill={color} opacity={op}/>;
   })}
   <path d="M0 540H790" stroke="#fff" strokeWidth="3" opacity=".15"/>
   <path d="M790 470L820 485L820 595L790 610Z" fill="#f1d13d"/>
  </svg>
  <div style={{position:"absolute",left:55,top:38,fontSize:15,fontWeight:900,letterSpacing:".16em",color:"#6b7883"}}>PIXEL LIGHT / 08-BIT COLOUR</div>
  <div style={{position:"absolute",right:60,bottom:45,fontSize:13,fontWeight:850,letterSpacing:".18em",color:"#67737a"}}>SIGNAL → SPECTRUM</div>
 </AbsoluteFill>;
};

const PixelGamePoster=()=>{
 const f=useCurrentFrame(),jump=Math.sin(f/3)*7;
 return <AbsoluteFill style={{...full,background:"#2eaef0",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0,shapeRendering:"crispEdges"}}>
   <rect width="1920" height="1080" fill="#36b8f5"/>
   <path d="M0 585L160 565L260 520L355 574L520 450L690 584L840 490L990 585L1150 440L1330 575L1490 485L1650 582L1800 500L1920 555V850H0Z" fill="#829be9" stroke="#5f7dd8" strokeWidth="9"/>
   <path d="M0 685L130 620L300 700L440 575L615 695L770 595L940 700L1100 578L1270 700L1430 605L1630 690L1800 590L1920 660V890H0Z" fill="#6a8ae4"/>
   <path d="M0 815L120 725L320 800L490 710L690 810L900 718L1090 810L1290 720L1510 815L1740 730L1920 805V1080H0Z" fill="#43b4e9"/>
   <g fill="#fff6da">
    <path d="M55 245h70v16H55zM75 230h40v15H75zM1280 185h85v16h-85zM1305 169h48v16h-48zM470 410h50v12h-50z"/>
   </g>
   <g transform="translate(90 690)">
    <rect x="0" y="80" width="320" height="90" fill="#b78b2d" stroke="#64451a" strokeWidth="10"/>
    <rect x="0" y="68" width="320" height="30" fill="#50c13c"/><rect x="0" y="68" width="320" height="13" fill="#90ed3b"/>
    <rect x="30" y="109" width="20" height="20" fill="#573d1e"/><rect x="115" y="139" width="20" height="17" fill="#573d1e"/><rect x="240" y="114" width="18" height="19" fill="#573d1e"/>
    <path d="M123 63L145 10L168 63Z" fill="#e94e35"/><rect x="136" y="-5" width="24" height="26" fill="#e94e35"/>
   </g>
   <g transform={"translate(1535 "+(620+jump)+")"}>
    <ellipse cx="0" cy="140" rx="145" ry="70" fill="#1b9c37"/><rect x="-23" y="100" width="46" height="245" fill="#8b5428"/>
    <circle cx="-65" cy="20" r="85" fill="#3cba3e"/><circle cx="30" cy="-10" r="91" fill="#57cf39"/><circle cx="112" cy="44" r="71" fill="#209b36"/>
    <path d="M-110 -60L-80 -135L-40 -75L-5 -147L30 -65L80 -118L111 -46" fill="#76df42"/>
   </g>
   <path d="M0 910H1920V1080H0Z" fill="#e2b65f"/><path d="M0 910H1920" stroke="#ffe08b" strokeWidth="12"/>
   {Array.from({length:90},(_,i)=><rect key={i} x={(i*97)%1920} y={945+(i%4)*30} width="13" height="11" fill="#a6772d" opacity=".75"/>)}
   <g transform={"translate(960 "+(515+jump)+")"}>
    <path d="M-194 -126L-156 -194L-40 -224L94 -205L181 -128L215 -6L182 142L106 211L-114 214L-194 137L-220 16Z" fill="#d9a631" stroke="#111315" strokeWidth="17"/>
    <path d="M-164 -119L-130 -160L-36 -190L91 -174L153 -115L181 -4L151 121L88 174L-102 176L-157 118L-183 11Z" fill="#35aef0" stroke="#111315" strokeWidth="12"/>
    <path d="M-73 -92L98 -3L-53 111Z" fill="#fff" stroke="#111315" strokeWidth="8"/>
    <path d="M-220 20L-188 -10M190 -16L216 20" stroke="#f5d45b" strokeWidth="16"/>
   </g>
  </svg>
  <div style={{position:"absolute",left:100,top:68,fontFamily:"monospace",fontSize:38,fontWeight:950,color:"#fff",lineHeight:1.03,textShadow:"2px 2px #3374b2"}}>SCORE<br/>000250</div>
  <div style={{position:"absolute",left:"50%",top:72,transform:"translateX(-50%)",fontFamily:"monospace",fontSize:39,fontWeight:950,color:"#fff",textAlign:"center",lineHeight:1.03,textShadow:"2px 2px #3374b2"}}>YEAR<br/>1985</div>
  <div style={{position:"absolute",right:115,top:70,fontFamily:"monospace",fontSize:37,fontWeight:950,color:"#fff",textAlign:"right",lineHeight:1.03,textShadow:"2px 2px #3374b2"}}>LIVES<br/>❤️ ❤️ ❤️</div>
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
 return <AbsoluteFill style={{...full,background:"#090a0c",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><radialGradient id="particle-vortex-core"><stop offset="0" stopColor="#050607"/><stop offset=".54" stopColor="#050607"/><stop offset="1" stopColor="#192021" stopOpacity="0"/></radialGradient><filter id="particle-glow-v13"><feGaussianBlur stdDeviation="2.1"/></filter></defs>
   {Array.from({length:1150},(_,i)=>{
    const u=i/1150,a=i*2.39996323+f*.008,phi=Math.acos(1-2*u),radius=175+58*Math.sin(phi*3.4)+14*Math.sin(i*.37+f*.045);
    const x=960+Math.cos(a)*radius*Math.sin(phi)*1.18;
    const y=540+Math.sin(a)*radius*Math.sin(phi)*.9;
    const z=Math.cos(phi),len=4+(i%5)*2.8;
    const dx=Math.cos(a+phi*.4)*len,dy=Math.sin(a+phi*.4)*len;
    const bright=i%11===0||i%17===0;
    return <line key={i} x1={x} y1={y} x2={x+dx} y2={y+dy} stroke={bright?"#a2e86b":"#e2e7e3"} strokeWidth={bright?3.2:1.8} opacity={.24+(1-u)*.5} />;
   })}
   {Array.from({length:120},(_,i)=>{
    const a=i*2.39996+f*.012,r=120+(i%13)*7;
    return <circle key={"p"+i} cx={960+Math.cos(a)*r*1.4} cy={540+Math.sin(a)*r*.85} r={i%9===0?3.5:1.9} fill={i%7===0?"#9bed5d":"#fff"} opacity=".55"/>;
   })}
   <ellipse cx="960" cy="540" rx="305" ry="225" fill="none" stroke="#a8b7b0" strokeOpacity=".12" strokeWidth="2" strokeDasharray="2 12"/>
   <ellipse cx="960" cy="540" rx="185" ry="135" fill="url(#particle-vortex-core)"/>
  </svg>
  <div style={{position:"absolute",inset:0,border:"1px solid rgba(235,240,238,.45)",margin:25}}/>
  <div style={{position:"absolute",left:60,top:45,fontSize:16,fontWeight:900,letterSpacing:".18em",color:"#d7dedc"}}>OPEN DESIGN / MOTION REEL</div>
  <div style={{position:"absolute",right:60,top:45,fontSize:16,fontWeight:900,letterSpacing:".18em",color:"#d7dedc"}}>05 — DEPTH</div>
  <div style={{position:"absolute",left:60,bottom:45,fontSize:13,fontWeight:850,letterSpacing:".17em",color:"#89928f"}}>128 BPM / BAR 7 OF 8</div>
 </AbsoluteFill>;
};

const EaseGreen=()=>{
 const f=useCurrentFrame(),shift=e(f,0,7,70,0);
 return <AbsoluteFill style={{...full,background:"#a6f75c",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"-4%",right:"-4%",top:278,textAlign:"center",transform:"translateX("+shift+"px)"}}>
   <Word size={430} color="#111713" tracking={-.14} style={{textShadow:"0 5px 0 rgba(26,61,27,.25)"}}>EASE</Word>
  </div>
  <div style={{position:"absolute",left:30,top:28,fontSize:14,fontWeight:900,letterSpacing:".19em",color:"#273e20"}}>OPEN DESIGN / MOTION REEL — 2026</div>
  <div style={{position:"absolute",right:30,top:28,fontSize:14,fontWeight:900,letterSpacing:".19em",color:"#273e20"}}>06 — EASE / 128 BPM</div>
  <div style={{position:"absolute",left:28,right:28,bottom:28,height:2,background:"#1d371c",opacity:.6}}/>
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

const InMetallic=()=>{
 const f=useCurrentFrame(),rise=e(f,0,5,28,0);
 return <AbsoluteFill style={{...full,background:"#08090b",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 55%,#26292d,#08090b 67%)"}}/>
  <div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) translateY("+rise+"px) perspective(1100px) rotateX(5deg)",fontFamily:displayFont,fontSize:390,fontWeight:1000,letterSpacing:"-.13em",lineHeight:.8,background:"linear-gradient(180deg,#fff 0%,#cfd3d6 22%,#686f76 46%,#f7f8f8 55%,#858b90 78%,#fff 100%)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent",filter:"drop-shadow(0 3px 0 #999fa3) drop-shadow(0 9px 0 #555c62) drop-shadow(0 18px 24px rgba(0,0,0,.7)"}}>IN</div>
 </AbsoluteFill>;
};
const InPoster=()=>{
 const f=useCurrentFrame(),dot=.92+.08*Math.sin(f/2);
 return <AbsoluteFill style={{...full,background:"#07080b",overflow:"hidden"}}>
  <div style={{position:"absolute",left:0,right:0,top:360,textAlign:"center",fontFamily:displayFont,fontSize:315,fontWeight:1000,letterSpacing:"-.11em",color:"#f5f5f1"}}>IN.</div>
  <div style={{position:"absolute",left:"58%",top:560,width:27,height:27,borderRadius:"50%",background:"#9ceb51",boxShadow:"0 0 22px rgba(156,235,81,.38)",transform:"scale("+dot+")"}}/>
 </AbsoluteFill>;
};

const PosterSequence = () => (
 <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={2}><GalleryWall /></Sequence>
  <Sequence from={2} durationInFrames={4}><Comic1952 /></Sequence>
  <Sequence from={6} durationInFrames={16}><Comic1962 /></Sequence>
  <Sequence from={22} durationInFrames={15}><DotPoster /></Sequence>
  <Sequence from={37} durationInFrames={15}><LightSweep1973 /></Sequence>
  <Sequence from={52} durationInFrames={13}><PixelGamePoster /></Sequence>
  <Sequence from={65} durationInFrames={5}><WorldPoster /></Sequence>
  <Sequence from={70} durationInFrames={14}><MindPoster /></Sequence>
  <Sequence from={84} durationInFrames={30}><RingPoster /></Sequence>
  <Sequence from={114} durationInFrames={16}><EditorialPosterGrid /></Sequence>
  <Sequence from={130} durationInFrames={10}><DepthField /></Sequence>
  <Sequence from={140} durationInFrames={5}><EaseGreen /></Sequence>
  <Sequence from={145} durationInFrames={5}><InMetallic /></Sequence>
  <Sequence from={150} durationInFrames={5}><InPoster /></Sequence>
  <Sequence from={155} durationInFrames={5}><EasePoster /></Sequence>
  <Sequence from={160} durationInFrames={10}><OutPoster /></Sequence>
  <Sequence from={170} durationInFrames={10}><NeverPoster /></Sequence>
  <Sequence from={180} durationInFrames={15}><LinearPoster /></Sequence>
  <Sequence from={195} durationInFrames={5}><GreenCircleTransition /></Sequence>
  <Sequence from={200} durationInFrames={7}><ClockPoster /></Sequence>
  <Sequence from={207} durationInFrames={8}><StatsPoster /></Sequence>
  <Sequence from={215} durationInFrames={8}><TogglePoster /></Sequence>
  <Sequence from={223} durationInFrames={8}><MotionFilmsPoster /></Sequence>
  <Sequence from={231} durationInFrames={8}><EyePoster /></Sequence>
  <Sequence from={239} durationInFrames={8}><CoursesPoster /></Sequence>
  <Sequence from={247} durationInFrames={7}><Comic1962 /></Sequence>
  <Sequence from={254} durationInFrames={8}><Future3D /></Sequence>
  <Sequence from={262} durationInFrames={7}><NotText fullText={false}/></Sequence>
 </AbsoluteFill>
);



const NotJustOpus = () => {
 const f=useCurrentFrame(),p=pop(f,30,1,50,12),show=e(f,14,21),shift=e(f,0,18,28,0);
 return <AbsoluteFill style={{...full,background:"#08090b",color:"#fff"}}>
  <div style={{position:"absolute",left:0,right:0,top:365,display:"flex",justifyContent:"center",alignItems:"center",gap:22,transform:"translateX("+shift+"px) scale("+(0.92+.08*p)+")"}}>
   <Word size={150} color="#f5f4f0" tracking={-.08}>Not just</Word>
   <div style={{background:"#e98e78",color:"#111315",padding:"12px 34px 19px",borderRadius:22,transform:"rotate(-1deg) scale("+(0.85+.15*show)+")",opacity:show,boxShadow:"0 12px 0 rgba(0,0,0,.2)"}}>
    <Word size={142} color="#111315" tracking={-.08}>Opus 5.5.</Word>
   </div>
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
 if(variant===1)return <div style={{position:"absolute",inset:0,background:"#1232df",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 45%,#455cf7,#1029c8 68%,#0b1d84)"}}/>
  <svg viewBox="0 0 1000 650" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <path d="M0 520Q200 480 400 520T800 500T1000 520V650H0Z" fill="#2038b9"/>
   <path d="M0 580Q250 535 500 588T1000 570V650H0Z" fill="#101e88"/>
   <path d="M95 180L905 115L905 260L95 325Z" fill="#ffffff" opacity=".12"/>
   <path d="M110 448L885 387" stroke="#8aa4ff" strokeWidth="3" opacity=".5"/>
  </svg>
  <div style={{position:"absolute",left:"-6%",right:"-6%",top:"23%",textAlign:"center",fontFamily:displayFont,fontSize:225,fontWeight:1000,letterSpacing:"-.115em",lineHeight:.95,color:"#edf1ff",textShadow:"1px 1px 0 #bec9ee,4px 5px 0 #899de0,8px 10px 0 #5b74cd,14px 17px 0 #334db1,23px 28px 0 #20378b,33px 45px 32px rgba(0,0,0,.34)"}}>FUTURE</div>
  <div style={{position:"absolute",left:0,right:0,top:"65%",fontSize:39,fontWeight:900,textAlign:"center",letterSpacing:".06em",color:"#fff",textShadow:"0 4px 18px rgba(0,0,0,.28)"}}>IS ALREADY HERE.</div>
  <div style={{position:"absolute",left:20,top:15,fontSize:14,color:"#dce5ff",fontWeight:900,letterSpacing:".16em"}}>FUTURE / 03</div>
 </div>;

if(variant===2)return <div style={{position:"absolute",inset:0,background:"#1468e7",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(150deg,#2d80f7,#1456c9)"}}/>
  <div style={{position:"absolute",left:40,bottom:-25,width:420,height:590}}>
   <svg viewBox="0 0 420 590" width="100%" height="100%">
    <path d="M40 570Q0 440 60 340Q10 180 95 105Q180 15 300 95Q405 168 365 310Q415 425 380 570Z" fill="#f0f0e8" stroke="#15191c" strokeWidth="10"/>
    <path d="M53 175Q25 56 145 39Q250 0 351 100L380 205Q320 122 260 142Q155 170 53 175Z" fill="#15181a"/>
    <path d="M75 290Q40 240 67 180Q115 125 162 185Q195 240 165 315Q127 355 75 290Z" fill="#171a1d"/>
    <path d="M260 293Q238 215 273 174Q330 123 366 188Q394 255 348 312Q299 351 260 293Z" fill="#171a1d"/>
    <circle cx="117" cy="235" r="10" fill="#fff"/><circle cx="315" cy="235" r="10" fill="#fff"/>
    <ellipse cx="215" cy="320" rx="34" ry="40" fill="#6d7276"/>
    <path d="M180 394Q215 425 249 394" stroke="#25292c" strokeWidth="9" fill="none" strokeLinecap="round"/>
    <path d="M130 470Q213 405 300 470L350 590H75Z" fill="#15191d"/>
   </svg>
  </div>
  <div style={{position:"absolute",right:35,top:120,width:420,height:450,borderRadius:20,background:"#fff",boxShadow:"0 14px 36px rgba(0,0,0,.2)",padding:28,boxSizing:"border-box"}}>
   <div style={{display:"flex",justifyContent:"space-between",fontSize:18,fontFamily:"monospace",color:"#777"}}><span>// course</span><span>01</span></div>
   <svg viewBox="0 0 300 220" width="100%" height="220" style={{marginTop:20}}>
    <path d="M28 168L150 43L272 168Z" fill="#e7ecf0" stroke="#141719" strokeWidth="8"/><path d="M28 168L150 112L272 168" stroke="#141719" strokeWidth="7" fill="none"/><circle cx="150" cy="107" r="28" fill="#ebad47"/>
   </svg>
   <div style={{fontSize:46,fontWeight:950,color:"#17191c"}}>Courses</div><div style={{fontSize:26,color:"#92989a",marginTop:5}}>$149</div>
  </div>
  <div style={{position:"absolute",left:25,top:25,color:"#d8e9ff",fontSize:15,fontWeight:900,letterSpacing:".16em"}}>02 — ANYTHING</div>
 </div>;

if(variant===3)return <div style={{position:"absolute",inset:0,background:"#d7f0df",overflow:"hidden",color:"#172d24"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(135deg,#e9f6e8,#f7f0dc 55%,#abdcca)"}}/>
  <div style={{position:"absolute",left:55,right:55,top:38,bottom:35,background:"#fff9ed",boxShadow:"0 16px 40px rgba(27,72,55,.15)",borderRadius:4,padding:42,boxSizing:"border-box"}}>
   <div style={{display:"flex",justifyContent:"space-between",fontSize:17,letterSpacing:".12em",fontWeight:850,color:"#71867b"}}><span>OPEN STUDIO</span><span>ABOUT · WORK · CONTACT</span></div>
   <div style={{position:"absolute",left:42,top:155,fontFamily:"Georgia,serif",fontSize:84,fontWeight:500,lineHeight:.98,letterSpacing:"-.06em"}}>a little<br/>wonder.</div>
   <div style={{position:"absolute",left:45,top:365,width:275,height:56,background:"#89cda7",display:"grid",placeItems:"center",fontSize:20,fontWeight:850,color:"#153a2a"}}>Explore the studio →</div>
   <div style={{position:"absolute",right:65,top:125,width:310,height:310,display:"grid",placeItems:"center"}}>
    <div style={{width:190,height:190,borderRadius:"50%",background:"#f0b66d",boxShadow:"0 0 0 24px #b7dec6,0 0 0 48px #f1d5ad",display:"grid",placeItems:"center"}}>
     <svg viewBox="0 0 100 100" width="170" height="170">{Array.from({length:8},(_,i)=><ellipse key={i} cx="50" cy="22" rx="12" ry="25" fill="#e77765" transform={"rotate("+(i*45)+" 50 50)"}/>)}<circle cx="50" cy="50" r="12" fill="#f6e4a2"/></svg>
    </div>
   </div>
   <div style={{position:"absolute",left:43,bottom:28,fontSize:15,color:"#87948b",fontWeight:700}}>DESIGN THAT FEELS LIKE YOU.</div>
  </div>
 </div>;

if(variant===4)return <div style={{position:"absolute",inset:0,background:"#eee6d3",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"repeating-linear-gradient(0deg,rgba(122,100,64,.035) 0 2px,transparent 2px 7px)"}}/>
  <div style={{position:"absolute",left:"20%",top:"9%",width:"60%",height:"82%",background:"#fff8e9",boxShadow:"0 12px 30px rgba(75,55,36,.18)",border:"5px solid #c8b891"}}>
   <div style={{position:"absolute",left:20,top:18,fontFamily:"Georgia,serif",fontSize:23,color:"#7b6a4f"}}>OPEN DESIGN</div>
   <div style={{position:"absolute",left:0,right:0,top:74,textAlign:"center",fontFamily:"Georgia,serif",fontSize:42,fontWeight:700,color:"#1a3127"}}>a book of<br/>possibilities</div>
   <div style={{position:"absolute",left:"50%",top:"51%",width:220,height:220,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"#df9a79",border:"9px solid #fff",boxShadow:"0 0 0 5px #274d78"}}>
    <div style={{position:"absolute",left:54,top:71,width:25,height:28,borderRadius:"50%",background:"#1b2225",boxShadow:"82px 0 0 #1b2225"}}/>
    <div style={{position:"absolute",left:80,top:118,width:45,height:25,borderBottom:"7px solid #1c2526",borderRadius:"50%"}}/>
    <div style={{position:"absolute",left:23,top:0,width:174,height:54,background:"#3a2927",borderRadius:"50% 50% 10% 10%"}}/>
   </div>
   <div style={{position:"absolute",left:35,right:35,bottom:25,height:8,background:"#d0b990"}}/>
  </div>
 </div>;


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


const CountdownOne=({frame}:{frame:number})=>{
 const p=e(frame,0,8),rotate=e(frame,0,12,-12,0);
 return <AbsoluteFill style={{...full,background:"#050609",color:"#f8f8f4",overflow:"hidden"}}>
  <div style={{position:"absolute",right:0,top:0,bottom:0,width:"32%",background:"#2238ee",clipPath:"polygon(100% 0,100% 100%,0 100%)"}}/>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <ellipse cx="960" cy="585" rx="610" ry="215" fill="none" stroke="#4a5ce3" strokeWidth="3" opacity=".65" transform={"rotate("+rotate+" 960 585)"}/>
   <ellipse cx="960" cy="585" rx="520" ry="175" fill="none" stroke="#a9b5ff" strokeWidth="1.5" opacity=".3" transform={"rotate("+(-rotate*1.4)+" 960 585)"}/>
  </svg>
  <div style={{position:"absolute",left:"50%",top:"47%",transform:"translate(-50%,-50%) perspective(1200px) scale("+(1.06+.05*p)+") rotateY(-9deg)",fontFamily:displayFont,fontSize:580,fontWeight:1000,lineHeight:.75,letterSpacing:"-.14em",color:"#eceff1",textShadow:"2px 2px 0 #b8c4d8,6px 6px 0 #8f9fba,12px 13px 0 #5d6f9d,22px 23px 0 #334b86,36px 39px 0 #182c62,55px 65px 42px rgba(0,0,0,.7)"}}>1</div>
  <div style={{position:"absolute",left:42,top:40,fontFamily:"monospace",fontSize:16,fontWeight:900,letterSpacing:".18em",color:"#aeb9ff"}}>GO</div>
  <div style={{position:"absolute",right:45,top:"47%",textAlign:"right",fontFamily:"monospace",fontSize:14,fontWeight:850,letterSpacing:".15em",color:"#c6cdff"}}>READY / MAKE<br/>THE MOMENT MOVE</div>
 </AbsoluteFill>;
};
const LaunchKitSequence=()=>{
 const frame=useCurrentFrame();
 if(frame>=106)return <CountdownOne frame={frame-106}/>;
 const variant=frame<15?0:frame<30?1:frame<45?2:frame<60?3:4;
 const countdown=frame<76?-1:frame<91?3:2;
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