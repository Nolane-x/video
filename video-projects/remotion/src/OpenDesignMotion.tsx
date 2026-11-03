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
 const drift=frame*.019;
 const brush=Array.from({length:92},(_,i)=>{
  const x=(i*211)%2260-160,y=40+(i*149)%760,w=75+(i*83)%360,h=2+(i*13)%15;
  const colors=["#fffdf2","#eaf5f0","#b9d8e9","#fff1e2","#f4c7b6","#d8e9e8","#add4e6"];
  return {x,y,w,h,angle:-39+(i%19)*4.1,color:colors[i%colors.length],opacity:.035+(i%6)*.011};
 });
 const pigment=Array.from({length:244},(_,i)=>({
  x:(i*127)%2050-60,y:640+(i*181)%405,r:.7+(i%5)*.7,
  color:["#fff9ef","#f1c2ad","#8ec4dc","#dcebe6","#e9a39a"][i%5],
  opacity:.025+(i%7)*.013
 }));
 const flecks=Array.from({length:56},(_,i)=>({
  x:(i*89)%1060-20,y:716+(i*97)%196,
  w:8+(i*13)%52,h:2+(i*7)%12,
  angle:-55+(i%11)*10,
  color:["#fffaf0","#f4cbb5","#d6e9e9","#f1a99d"][i%4],
  opacity:.12+(i%4)*.055
 }));
 const lowerPaint=Array.from({length:132},(_,i)=>({
  x:(i*173)%2100-90,y:722+(i*139)%275,
  w:26+(i*89)%188,h:4+(i*31)%25,
  angle:-38+(i%17)*5,
  color:["#fff8e7","#f7e0cb","#f1b9a8","#e8a59b","#c5dfe2","#a9d4df","#f6c98f"][i%7],
  opacity:.055+(i%6)*.027
 }));
 return <AbsoluteFill style={{background:"#75bfe5",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" preserveAspectRatio="none" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <linearGradient id="wc-sky-v40" x1="0" y1="0" x2=".12" y2="1">
     <stop stopColor="#58b2df"/>
     <stop offset=".34" stopColor="#86c5e4"/>
     <stop offset=".66" stopColor="#bddde6"/>
     <stop offset=".87" stopColor="#ead4c7"/>
     <stop offset="1" stopColor="#efc2ac"/>
    </linearGradient>
    <linearGradient id="wc-wash-white-v40" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#fffdf4" stopOpacity=".06"/>
     <stop offset=".3" stopColor="#f9fff3" stopOpacity=".73"/>
     <stop offset=".64" stopColor="#e4f1ee" stopOpacity=".42"/>
     <stop offset="1" stopColor="#deeceb" stopOpacity=".02"/>
    </linearGradient>
    <linearGradient id="wc-wash-blue-v40" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#8bc8e5" stopOpacity=".02"/>
     <stop offset=".4" stopColor="#c7e4ec" stopOpacity=".52"/>
     <stop offset=".78" stopColor="#eaf4ef" stopOpacity=".25"/>
     <stop offset="1" stopColor="#fff3e6" stopOpacity=".02"/>
    </linearGradient>
    <linearGradient id="wc-wash-peach-v40" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#fff4e5" stopOpacity=".02"/>
     <stop offset=".4" stopColor="#f7d5c3" stopOpacity=".58"/>
     <stop offset=".74" stopColor="#ecadae" stopOpacity=".41"/>
     <stop offset="1" stopColor="#f6e1d2" stopOpacity=".02"/>
    </linearGradient>
    <linearGradient id="wc-cloud-light-v40" x1="0" y1="0" x2=".35" y2="1">
     <stop stopColor="#fffef5" stopOpacity=".96"/>
     <stop offset=".43" stopColor="#fff2df" stopOpacity=".79"/>
     <stop offset="1" stopColor="#edc0a9" stopOpacity=".04"/>
    </linearGradient>
    <linearGradient id="wc-cloud-coral-v40" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#fff1df" stopOpacity=".09"/>
     <stop offset=".38" stopColor="#f2b99e" stopOpacity=".78"/>
     <stop offset=".78" stopColor="#e79aa0" stopOpacity=".45"/>
     <stop offset="1" stopColor="#e9c7b8" stopOpacity=".03"/>
    </linearGradient>
    <linearGradient id="wc-paint-glaze-v41" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#fff7e7" stopOpacity=".88"/>
     <stop offset=".35" stopColor="#f5d6c5" stopOpacity=".7"/>
     <stop offset=".72" stopColor="#e6b5af" stopOpacity=".42"/>
     <stop offset="1" stopColor="#d7e8e4" stopOpacity=".04"/>
    </linearGradient>
    <linearGradient id="wc-ridge-far-v40" x1="0" y1="0" x2="0" y2="1">
     <stop stopColor="#347f9f"/>
     <stop offset=".62" stopColor="#1a6891"/>
     <stop offset="1" stopColor="#145783"/>
    </linearGradient>
    <linearGradient id="wc-ridge-near-v40" x1="0" y1="0" x2="0" y2="1">
     <stop stopColor="#13577f"/>
     <stop offset=".58" stopColor="#0c4772"/>
     <stop offset="1" stopColor="#083b66"/>
    </linearGradient>
    <radialGradient id="wc-dawn-v40" cx="73%" cy="77%" r="57%">
     <stop stopColor="#ffe8d4" stopOpacity=".42"/>
     <stop offset=".54" stopColor="#f7d9ca" stopOpacity=".14"/>
     <stop offset="1" stopColor="#f7d9ca" stopOpacity="0"/>
    </radialGradient>
    <filter id="wc-wash-soft-v40"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="wc-wash-texture-v40">
     <feTurbulence type="fractalNoise" baseFrequency=".008 .023" numOctaves="3" seed="151" result="broadNoise"/>
     <feDisplacementMap in="SourceGraphic" in2="broadNoise" scale="48" xChannelSelector="R" yChannelSelector="G"/>
     <feGaussianBlur stdDeviation="2.4"/>
    </filter>
    <filter id="wc-cloud-edge-v40">
     <feTurbulence type="fractalNoise" baseFrequency=".021 .047" numOctaves="2" seed="163" result="cloudNoise"/>
     <feDisplacementMap in="SourceGraphic" in2="cloudNoise" scale="20" xChannelSelector="R" yChannelSelector="G"/>
     <feGaussianBlur stdDeviation="1.5"/>
    </filter>
    <filter id="wc-pigment-v40">
     <feTurbulence type="fractalNoise" baseFrequency=".072 .12" numOctaves="2" seed="73" result="pigmentNoise"/>
     <feDisplacementMap in="SourceGraphic" in2="pigmentNoise" scale="5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="wc-paper-v40">
     <feTurbulence type="fractalNoise" baseFrequency=".72" numOctaves="2" seed="53"/>
     <feColorMatrix type="saturate" values="0"/>
    </filter>
   </defs>
   <rect width="1920" height="1080" fill="url(#wc-sky-v40)"/>
   <rect width="1920" height="1080" fill="url(#wc-dawn-v40)"/>

   <g transform={"translate("+(-drift*.55)+",0)"} filter="url(#wc-wash-texture-v40)">
    <path d="M-190 374C-104 326 14 281 153 238C270 202 352 193 478 144C589 102 718 72 842 28C774 103 673 157 562 202C448 248 322 275 202 331C72 390 -56 434 -190 505Z" fill="url(#wc-wash-white-v40)" opacity=".62"/>
    <path d="M270 495C395 421 514 365 633 320C755 272 868 239 1002 194C925 270 838 305 760 346C650 405 535 438 428 493C372 520 314 539 270 550Z" fill="url(#wc-wash-blue-v40)" opacity=".35"/>
    <path d="M900 275C1035 210 1165 168 1309 127C1450 82 1619 25 1814 -35C1693 56 1585 112 1460 162C1336 214 1209 248 1092 299C1015 331 955 343 900 355Z" fill="url(#wc-wash-peach-v40)" opacity=".72"/>
   </g>
   <g transform={"translate("+(drift*.18)+",0)"} opacity=".42" filter="url(#wc-wash-soft-v40)">
    <path d="M-100 445C110 354 238 325 391 272C520 226 655 207 794 163" fill="none" stroke="#fffef3" strokeWidth="25" strokeLinecap="round"/>
    <path d="M620 380C762 315 897 282 1024 243" fill="none" stroke="#d9eef0" strokeWidth="29" strokeLinecap="round"/>
    <path d="M1310 241C1453 192 1600 142 1736 91" fill="none" stroke="#fff0e3" strokeWidth="22" strokeLinecap="round"/>
   </g>
   <g transform={"translate("+(drift*.12)+",0)"} opacity=".34">
    {brush.map((p,i)=><path key={i} d={"M"+p.x+" "+p.y+"q "+(p.w*.27)+" "+(-p.h*1.3)+" "+(p.w*.7)+" "+(-p.h*.18)} fill="none" stroke={p.color} strokeWidth={p.h} strokeLinecap="round" opacity={p.opacity} transform={"rotate("+p.angle+" "+p.x+" "+p.y+")"}/>)}
   </g>

   <g transform={"translate("+(-drift*.17)+",0)"} filter="url(#wc-cloud-edge-v40)">
    <path d="M-100 858C-64 818 -12 811 35 818C58 780 101 760 141 779C182 739 224 765 241 796C287 772 328 795 337 825C384 816 429 839 443 867C398 884 355 879 314 868C269 902 208 890 166 873C105 905 10 888 -100 858Z" fill="url(#wc-cloud-light-v40)" opacity=".74"/>
    <path d="M-40 818C35 784 96 786 157 813C206 833 246 830 295 816" fill="none" stroke="#fffdf2" strokeWidth="43" strokeLinecap="round" opacity=".34" filter="url(#wc-wash-soft-v40)"/>
    <path d="M-14 869C70 842 118 850 183 870C238 888 288 877 352 852" fill="none" stroke="#d4e8e3" strokeWidth="19" strokeLinecap="round" opacity=".46" filter="url(#wc-wash-texture-v40)"/>
    <path d="M82 790C130 772 175 778 215 801" fill="none" stroke="#fff9e7" strokeWidth="22" strokeLinecap="round" opacity=".5" filter="url(#wc-wash-soft-v40)"/>
    <path d="M260 900C331 871 385 877 451 895" fill="none" stroke="#f0c3aa" strokeWidth="31" strokeLinecap="round" opacity=".58" filter="url(#wc-wash-soft-v40)"/>
   </g>

   <g transform={"translate("+(drift*.14)+",0)"} filter="url(#wc-cloud-edge-v40)">
    <path d="M420 895C479 854 526 837 581 856C633 815 686 824 718 850C768 822 812 842 827 873C870 860 912 878 932 907C875 919 828 911 784 895C737 926 677 916 630 897C564 926 482 920 420 895Z" fill="url(#wc-cloud-coral-v40)" opacity=".66"/>
    <path d="M450 868C519 840 575 846 627 873C675 895 725 888 773 861" fill="none" stroke="#fff4e7" strokeWidth="32" strokeLinecap="round" opacity=".42" filter="url(#wc-wash-soft-v40)"/>
    <path d="M546 924C618 893 687 899 742 920C797 939 859 924 919 898" fill="none" stroke="#e89e91" strokeWidth="21" strokeLinecap="round" opacity=".55" filter="url(#wc-wash-soft-v40)"/>
    <path d="M753 852C814 820 870 834 911 860C953 829 1009 847 1037 874C1083 865 1125 884 1142 908C1089 920 1039 912 1003 894C951 920 884 907 844 886Z" fill="url(#wc-cloud-light-v40)" opacity=".44"/>
   </g>

   <g transform={"translate("+(drift*.1)+",0)"} opacity=".54" filter="url(#wc-wash-soft-v40)">
    <path d="M-95 760C50 731 178 765 307 783C429 800 526 793 634 816" fill="none" stroke="#f6e8d7" strokeWidth="52" strokeLinecap="round"/>
    <path d="M285 816C414 778 537 794 657 824C742 846 816 843 900 816" fill="none" stroke="#f2c4b1" strokeWidth="38" strokeLinecap="round"/>
    <path d="M788 855C929 817 1058 829 1173 857C1284 884 1394 866 1511 827" fill="none" stroke="#fff0df" strokeWidth="33" strokeLinecap="round"/>
    <path d="M1315 831C1450 789 1579 802 1705 835C1788 855 1870 840 1988 792" fill="none" stroke="#f5d2c1" strokeWidth="31" strokeLinecap="round"/>
   </g>
   <g filter="url(#wc-pigment-v40)" opacity=".72">
    {flecks.map((p,i)=><path key={i} d={"M"+p.x+" "+p.y+"q "+(p.w*.28)+" "+(-p.h*1.5)+" "+p.w+" 0"} fill="none" stroke={p.color} strokeWidth={p.h} strokeLinecap="round" opacity={p.opacity} transform={"rotate("+p.angle+" "+p.x+" "+p.y+")"}/>)}
    {lowerPaint.map((p,i)=><path key={"lower-"+i} d={"M"+p.x+" "+p.y+"q "+(p.w*.32)+" "+(-p.h*1.4)+" "+p.w+" "+(p.h*.14)} fill="none" stroke={p.color} strokeWidth={p.h} strokeLinecap="round" opacity={p.opacity} transform={"rotate("+p.angle+" "+p.x+" "+p.y+")"}/>)}
    {pigment.map((p,i)=><circle key={i} cx={p.x} cy={p.y} r={p.r} fill={p.color} opacity={p.opacity}/>)}
   </g>

   <g transform={"translate("+(drift*.05)+",0)"}>
    <path d="M-120 1018C-8 1003 90 990 194 993C305 997 387 1015 493 1018C602 1020 694 1005 804 1001C913 997 1024 1009 1136 1017C1248 1025 1363 1004 1473 996C1601 986 1727 1000 1820 1009C1904 1017 1971 1012 2030 1005V1080H-120Z" fill="url(#wc-ridge-far-v40)" opacity=".86"/>
    <path d="M-120 1042C0 1025 113 1015 234 1019C345 1022 450 1040 559 1044C672 1048 785 1027 898 1025C1015 1023 1123 1035 1240 1041C1360 1047 1474 1027 1590 1022C1720 1018 1852 1032 2030 1025V1080H-120Z" fill="url(#wc-ridge-near-v40)"/>
    <path d="M-90 1007C42 988 159 983 267 997C366 1009 433 1027 522 1031" fill="none" stroke="#75bed0" strokeWidth="11" opacity=".32" filter="url(#wc-wash-soft-v40)"/>
    <path d="M735 1014C839 997 942 1002 1040 1018C1147 1035 1248 1034 1344 1017" fill="none" stroke="#3d8da5" strokeWidth="7" opacity=".28" filter="url(#wc-wash-soft-v40)"/>
   </g>
   <rect width="1920" height="1080" filter="url(#wc-paper-v40)" opacity=".12" style={{mixBlendMode:"soft-light"}}/>
  </svg>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 47%,transparent 49%,rgba(247,230,216,.07) 100%)"}}/>
  <Noise opacity={.013}/>
 </AbsoluteFill>;
};

const OpeningScene = () => {
 const f=useCurrentFrame();
 const text="Introducing OpenDesign Motion";
 const introLength="Introducing".length;
 const firstPhaseCount=Math.round(Math.max(0,Math.min(1,(f-14)/16))*introLength);
 const finalPhaseCount=introLength+Math.round(Math.max(0,Math.min(1,(f-30)/30))*(text.length-introLength));
 const count=f<30?firstPhaseCount:finalPhaseCount;
 const pressed=e(f,76,82);
 const cursor=e(f,48,76,0,1);
 const typing=f>=15;
 return <AbsoluteFill style={full}>
  <CloudSky frame={f}/>
  <div style={{position:"absolute",top:225,left:0,right:0,display:"flex",justifyContent:"center",alignItems:"center",color:"#19272c"}}>
   <div style={{fontFamily:"Georgia,serif",fontSize:100,fontWeight:700,letterSpacing:"-.055em",position:"relative",whiteSpace:"nowrap"}}>
    Let’s create <span style={{position:"relative",display:"inline-block"}}><span style={{position:"absolute",left:-5,right:-8,top:"55%",height:31,background:"#b6e65e",transform:"rotate(-1deg)"}}/><span style={{position:"relative"}}>Motion design</span><span style={{position:"absolute",right:-8,top:"-2%",height:"95%",width:5,background:"#5cda4c"}}/></span>
   </div>
  </div>
  <div style={{position:"absolute",top:350,left:0,right:0,textAlign:"center",color:"rgba(35,52,58,.68)",fontSize:18,letterSpacing:".06em",fontWeight:550}}>Good work starts here</div>
  <div style={{position:"absolute",left:290,right:290,top:390,height:345,background:"rgba(255,255,255,.48)",border:"1px solid rgba(255,255,255,.82)",borderRadius:24,boxShadow:"0 27px 75px rgba(49,82,91,.2),0 4px 16px rgba(40,72,82,.09)",backdropFilter:"blur(20px)",transform:"translateY("+(55-3*e(f,0,30))+"px) scale("+(0.99-0.05*e(f,0,30)-pressed*.008)+")",padding:"36px 38px",boxSizing:"border-box"}}>
  <div style={{position:"absolute",left:0,right:0,top:0,height:278,background:"rgba(255,255,255,.97)",borderRadius:24,boxShadow:"0 12px 30px rgba(49,82,91,.06)"}}/>
   <div style={{position:"relative",color:typing?"#263033":"#a2a9a8",fontSize:38,fontWeight:480,letterSpacing:"-.035em",minHeight:52,whiteSpace:"nowrap"}}>
    {typing?text.slice(0,count):"Create a Motion design: Motion graphics, art and product"}
    {typing?<span style={{display:"inline-block",width:2,height:34,background:count<introLength?"#313a3d":"#5cda4c",verticalAlign:"middle",marginLeft:4}}/>:null}
   </div>
   <div style={{position:"absolute",bottom:87,left:-12,display:"flex",alignItems:"center",gap:12}}>
    <div style={{width:48,height:48,border:"2px solid #e9e9e6",borderRadius:"50%",display:"grid",placeItems:"center",boxSizing:"border-box",fontSize:24,color:"#9ca5a4"}}>＋</div><div style={{width:48,height:48,border:"2px solid #e9e9e6",borderRadius:"50%",display:"grid",placeItems:"center",boxSizing:"border-box",fontSize:22,color:"#9ca5a4"}}>◐</div>
    <div style={{background:"#d9f5d9",color:"#26763d",padding:"8px 22px",borderRadius:26,fontSize:22,fontWeight:850}}>▣ Motion design⌄</div>
    
   </div>
   <div style={{position:"absolute",left:38,bottom:10,fontSize:18,color:"#899493"}}>▱ Working directory⌄</div>
   <div style={{position:"absolute",right:40,bottom:87,display:"flex",gap:10,alignItems:"center"}}>
    <span style={{width:13,height:13,borderRadius:"50%",background:"#67d46c"}}/><span style={{width:13,height:13,borderRadius:"50%",background:"#5b72dc"}}/>
    <div style={{width:68,height:68,borderRadius:"50%",background:"#12191b",display:"grid",placeItems:"center",transform:"scale("+(1-pressed*.09)+")",boxShadow:"0 4px 14px rgba(20,30,31,.22)"}}>
     <svg viewBox="0 0 30 30" width="31" height="31"><path d="M5 15H24M16 6L25 15L16 24" fill="none" stroke="#75e44c" strokeWidth="2.7" strokeLinecap="round" strokeLinejoin="round"/></svg>
    </div>
   </div>
  </div>
  <div style={{position:"absolute",top:955-315*e(f,42,60),left:1875-337*e(f,42,60),width:29,height:38,filter:"drop-shadow(0 3px 3px rgba(0,0,0,.3))"}}>
   <svg viewBox="0 0 30 40" width="29" height="38"><path d="M2 2L2 33L10 25L17 38L23 35L16 22L28 22Z" fill="#fff" stroke="#262b2d" strokeWidth="2" strokeLinejoin="round"/></svg>
  </div>
 </AbsoluteFill>;
};

const HeroTitle = () => {
 const f=useCurrentFrame(),p=pop(f,30,0,44,12),opacity=fadeOut(f,48,9);
 const letters=["M","O","T","I","O","N"];
 return <AbsoluteFill style={full}>
  <CloudSky frame={f+100}/>
  <div style={{position:"absolute",top:190,left:0,right:0,textAlign:"center",fontFamily:"Georgia,serif",fontStyle:"italic",fontSize:40,fontWeight:650,color:"#fff",opacity:e(f,0,6),textShadow:"0 2px 12px rgba(0,0,0,.12)"}}>Introducing</div>
  <div style={{position:"absolute",top:300,left:0,right:0,textAlign:"center",fontFamily:displayFont,fontSize:132,fontWeight:850,letterSpacing:"-.07em",color:"#fff",opacity,transform:"translateY("+((1-p)*45)+"px)",textShadow:"0 2px 0 #d7e5e5,0 4px 0 #b7d0d5,0 7px 0 #8fb4c2,0 11px 0 #6695aa,0 16px 23px rgba(22,69,91,.26)"}}>OpenDesign</div>
  <div style={{position:"absolute",left:0,right:0,top:440,height:300,display:"flex",justifyContent:"center",alignItems:"center",gap:0,opacity,transform:"translateY("+((1-p)*60)+"px) scale("+(0.9+.1*p)+")",perspective:1200}}>
   {letters.map((ch,i)=>{
    const lag=i*2.1,enter=e(f,lag,lag+14),swing=Math.sin((f-lag)*.18)*5;
    const colors=["#fff","#fff","#fff","#f8f1e8","#fff","#fff"];
    return <div key={i} style={{fontFamily:displayFont,fontSize:370,fontWeight:1000,letterSpacing:"-.02em",lineHeight:.85,color:colors[i],transform:"translateY("+(1-enter)*(-180+swing*7)+"px) translateX("+(i===3?0:0)+"px) rotateY("+(i===3?-18:0)+"deg) rotateX("+(i===3?8:0)+"deg)",textShadow:"1px 1px 0 #e0e7e8,3px 4px 0 #b6cbd2,6px 7px 0 #8eafbb,10px 12px 0 #5e8ba0,16px 20px 0 #345d75,24px 31px 33px rgba(25,62,83,.3)",marginLeft:i===0?0:-6}}>{ch}</div>;
   })}
  </div>
  
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

const GalleryWall=({showClaim=true}:{showClaim?:boolean})=>{
 const f=useCurrentFrame(),p=pop(f,30,0,72,16);
 const pan=e(f,0,77,8,-92),ry=e(f,0,77,-2,-18.5),rz=e(f,0,77,.25,-1.05);
 const zoom=1.0+.28*e(f,36,77),order=Array.from({length:30},(_,i)=>i),claimOpacity=showClaim?1-e(f,0,15):0;
 return <AbsoluteFill style={{...full,background:"#f3f1e9",overflow:"hidden"}}>
  <div style={{position:"absolute",left:78,right:78,top:76,bottom:58,display:"grid",gridTemplateColumns:"repeat(6,263px)",gridTemplateRows:"repeat(5,148px)",gap:13,justifyContent:"center",alignContent:"center",transform:"perspective(1080px) rotateY("+ry+"deg) rotateX(3.4deg) rotateZ("+rz+"deg) translateX("+pan+"px) translateY("+((1-p)*40)+"px) scale("+(0.965+.035*p)*zoom+")",transformOrigin:"center center"}}>
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
};

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
 const f=useCurrentFrame(),pulse=1+Math.sin(f/4)*.003;
 return <AbsoluteFill style={{...full,background:"#f4efe2",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:18,border:"8px solid #111315",display:"grid",gridTemplateColumns:"20% 1fr 20%",gridTemplateRows:"1fr 1fr",gap:9,background:"#111315",padding:0,boxSizing:"border-box"}}>
   <div style={{position:"relative",gridColumn:1,gridRow:1,background:"#f5d33f",overflow:"hidden",border:"5px solid #111315"}}>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#d9b832 0 3px,transparent 3.6px)",backgroundSize:"20px 20px",opacity:.58}}/>
    <div style={{position:"absolute",left:"13%",top:"46%",fontFamily:"Arial Black,Arial,sans-serif",fontSize:40,fontStyle:"italic",fontWeight:1000,color:"#151719",transform:"rotate(-3deg)",whiteSpace:"nowrap"}}>ONE IDEA...</div>
   </div>
   <div style={{position:"relative",gridColumn:1,gridRow:2,background:"#f7f0e8",overflow:"hidden",border:"5px solid #111315"}}>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#dc9ca8 0 3px,transparent 3.6px)",backgroundSize:"21px 21px",opacity:.62}}/>
   </div>
   <div style={{position:"relative",gridColumn:3,gridRow:1,background:"#f7f0e8",overflow:"hidden",border:"5px solid #111315"}}>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#dc9ca8 0 3px,transparent 3.6px)",backgroundSize:"21px 21px",opacity:.62}}/>
    <div style={{position:"absolute",left:"28%",top:"43%",display:"flex",gap:30}}>{[0,1,2].map(i=><div key={i} style={{width:26,height:26,borderRadius:"50%",background:i===2?"#d8d6ce":"#151719"}}/>)}</div>
   </div>
   <div style={{position:"relative",gridColumn:3,gridRow:2,background:"#f5d33f",overflow:"hidden",border:"5px solid #111315"}}>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#d9b832 0 3px,transparent 3.6px)",backgroundSize:"20px 20px",opacity:.52}}/>
   </div>
   <div style={{position:"relative",gridColumn:2,gridRow:"1 / span 2",overflow:"hidden",border:"6px solid #111315",background:"#75a7e8",transform:"scale("+pulse+")"}}>
    <div style={{position:"absolute",inset:0,background:"repeating-conic-gradient(from -10deg at 50% 53%,#fff8eb 0deg 3deg,#76a8e8 3deg 8.4deg)"}}/>
    <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(#3476c0 0 4.5px,transparent 5.3px)",backgroundSize:"25px 25px",opacity:.75}}/>
    <svg viewBox="0 0 1000 1000" width="100%" height="100%" style={{position:"absolute",inset:0}}>
     <defs>
      <pattern id="comic-yellow-dots-v29" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="4" fill="#fff4a7" opacity=".86"/></pattern>
      <filter id="comic-shade-v29"><feGaussianBlur stdDeviation="8"/></filter>
     </defs>
     <circle cx="500" cy="520" r="380" fill="#f6d447" stroke="#111315" strokeWidth="8"/>
     <circle cx="500" cy="520" r="365" fill="url(#comic-yellow-dots-v29)"/>
     <circle cx="500" cy="520" r="270" fill="#e84131" stroke="#111315" strokeWidth="15"/>
     <circle cx="500" cy="520" r="208" fill="#f7f1dc" stroke="#111315" strokeWidth="13"/>
     <circle cx="500" cy="520" r="187" fill="none" stroke="#f5cf3b" strokeWidth="13"/>
     <circle cx="500" cy="501" r="202" fill="#fff8e8" stroke="#111315" strokeWidth="13"/>
     <circle cx="500" cy="501" r="186" fill="url(#comic-yellow-dots-v29)" opacity=".76"/>
     <path d="M386 371L666 507L512 538L478 700Z" fill="#111315"/>
     <path d="M393 382L642 505L508 524" fill="none" stroke="#d5dbe0" strokeWidth="5" opacity=".7"/>
     {Array.from({length:46},(_,i)=>{const a=i*2.399963,r=282+(i%5)*15;return <circle key={i} cx={500+Math.cos(a)*r} cy={520+Math.sin(a)*r} r={3.5+(i%4)*1.4} fill="#111315" opacity=".32"/>;})}
     <path d="M0 0H0" stroke="#111315"/>
    </svg>
    <div style={{position:"absolute",left:18,top:18,padding:"13px 24px",background:"#f7d747",border:"5px solid #111315",fontFamily:"Arial Black,Arial,sans-serif",fontSize:35,fontWeight:1000,fontStyle:"italic",color:"#111315",transform:"rotate(-1.5deg)",whiteSpace:"nowrap",boxShadow:"4px 5px 0 rgba(0,0,0,.18)"}}>MEANWHILE, IN 1962...</div>
    <div style={{position:"absolute",right:24,top:15,textAlign:"right",fontFamily:"Arial Black,Arial,sans-serif",fontSize:57,lineHeight:.82,fontWeight:1000,color:"#111315",fontStyle:"italic",textShadow:"2px 2px 0 #f5d344"}}>1962<br/><span style={{fontSize:29}}>POP ART</span></div>
    <div style={{position:"absolute",right:12,bottom:35,width:240,height:160,clipPath:"polygon(50% 0,60% 17%,80% 4%,78% 27%,100% 38%,83% 54%,96% 78%,71% 74%,60% 100%,43% 82%,18% 98%,22% 71%,0 62%,18% 43%,6% 18%,37% 24%)",background:"#f5d33f",border:"6px solid #111315",display:"grid",placeItems:"center",filter:"drop-shadow(4px 5px 0 rgba(0,0,0,.2))"}}>
     <div style={{fontFamily:"Arial Black,Arial,sans-serif",fontSize:46,fontWeight:1000,fontStyle:"italic",color:"#e83f31",textShadow:"3px 3px 0 #111315, -1px -1px 0 #111315",transform:"rotate(-7deg)"}}>CLICK!</div>
    </div>
   </div>
  </div>
 </AbsoluteFill>;
};

const Future3D = () => {
 const f=useCurrentFrame(),p=e(f,0,15);
 const title={position:"absolute" as const,left:-40,right:-40,top:245,textAlign:"center" as const,fontFamily:displayFont,fontSize:380,fontWeight:1000,letterSpacing:"-.105em",lineHeight:.9,whiteSpace:"nowrap" as const};
 return <AbsoluteFill style={{...full,background:"radial-gradient(ellipse at 50% 48%,#3755f0,#142aa6 72%,#07176c)",color:"#fff",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><pattern id="future-dots-v19" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="3" fill="#a9bdff" opacity=".6"/></pattern></defs>
   <rect x="0" y="560" width="1920" height="520" fill="url(#future-dots-v19)" opacity=".25"/>
   {Array.from({length:35},(_,i)=><path key={i} d={"M"+(i*58)+" 0L"+(i*58+430)+" 1080"} stroke="#b4c4ff" strokeWidth="1" opacity=".13"/>)}
   <path d="M0 845Q400 770 800 850T1600 830T1920 845" stroke="#9db4ff" strokeWidth="2" fill="none" opacity=".3"/>
  </svg>
  <div style={{...title,transform:"translateY("+((1-p)*50+54)+"px)",color:"#0b1c70",textShadow:"0 7px 0 #0c1b69,0 17px 0 #0b1855,0 28px 0 #0a1547,0 40px 25px rgba(0,0,0,.4)"}}>FUTURE</div>
  <div style={{...title,transform:"translateY("+((1-p)*50+29)+"px)",color:"#3456d6",textShadow:"0 4px 0 #1a339e,0 10px 0 #142b87,0 18px 0 #112477"}}>FUTURE</div>
  <div style={{...title,transform:"translateY("+(1-p)*50+"px)",background:"linear-gradient(180deg,#fff 0%,#ced7df 23%,#f8f8f5 42%,#899bb5 63%,#f6f6f1 76%,#9eacc0 100%)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent",filter:"drop-shadow(0 3px 0 #8194b0) drop-shadow(0 11px 0 #334c9e) drop-shadow(0 24px 25px rgba(0,0,0,.35)"}}>FUTURE</div>
  <div style={{position:"absolute",left:0,right:0,top:655,fontSize:62,fontWeight:950,letterSpacing:".04em",textAlign:"center",color:"#fff",textShadow:"0 4px 20px rgba(0,0,0,.28)"}}>IS ALREADY</div>
  <div style={{position:"absolute",left:0,right:0,top:740,fontSize:31,fontWeight:850,letterSpacing:".38em",textAlign:"center",color:"#c4d1ff"}}>HERE.</div>
 </AbsoluteFill>;
};

const DotPoster = () => {
 const f=useCurrentFrame(),pulse=1+Math.sin(f/3)*.008;
 const dots=Array.from({length:18*36},(_,i)=>{
  const row=Math.floor(i/36),col=i%36,seed=(i*37+13)%53;
  return {x:col*54+((row%2)*17)+((seed%9)-4)*4.2,y:row*60+((seed%11)-5)*3.5,rx:16+(seed%6)*1.2,ry:14+((seed*3)%7)*1.15,angle:((seed%13)-6)*3,op:.9+(seed%4)*.025};
 });
 const specks=Array.from({length:126},(_,i)=>{const a=i*2.399963+(i%7)*.11,r=210+((i*17)%50);return {x:Math.cos(a)*r,y:Math.sin(a)*r,r:5+(i%6)*1.35};});
 return <AbsoluteFill style={{...full,background:"#e84434",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <rect width="1920" height="1080" fill="#e84434"/>
   <g fill="#fff8ed">{dots.map((d,i)=><ellipse key={i} cx={d.x} cy={d.y} rx={d.rx} ry={d.ry} transform={"rotate("+d.angle+" "+d.x+" "+d.y+")"} opacity={d.op}/>)}</g>
   <g transform={"translate(960 540) scale("+pulse+")"}>
    <path d="M-252 252V-22C-252 -165 -143 -270 0 -270C143 -270 252 -165 252 -22C252 123 145 238 0 252Z
             M-185 -22C-185 -124 -104 -194 0 -194C104 -194 185 -124 185 -22C185 79 107 163 0 163C-107 163 -185 79 -185 -22Z"
          fill="#f4ca31" fillRule="evenodd" stroke="#111315" strokeWidth="8" strokeLinejoin="round"/>
    <path d="M-248 190L-248 250L-10 250L-10 214" fill="none" stroke="#f4ca31" strokeWidth="15" strokeLinecap="square"/>
    <g fill="#111315">{specks.map((s,i)=><circle key={i} cx={s.x} cy={s.y} r={s.r}/>)}</g>
    <path d="M-88 -96L128 -6L-18 19L-51 128Z" fill="#111315"/>
   </g>
   <path d="M690 23L1220 23L1227 53L1208 77L1225 110L1195 132L1210 170L1175 183L777 183L755 163L711 164L726 130L691 108L710 78L684 56Z" fill="#fff8ed"/>
   <path d="M690 23L1220 23L1227 53L1208 77L1225 110L1195 132L1210 170L1175 183L777 183L755 163L711 164L726 130L691 108L710 78L684 56Z" fill="none" stroke="#f9f3e4" strokeWidth="7"/>
   <text x="960" y="96" textAnchor="middle" fill="#111315" fontFamily="Arial Black,Arial,sans-serif" fontSize="74" fontWeight="1000">1965</text>
   <text x="960" y="143" textAnchor="middle" fill="#111315" fontFamily="Arial, sans-serif" fontSize="34" fontWeight="900">Infinity dots</text>
  </svg>
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
 const panels=[
  ["#101820","MOTION","MOTION / 01"],["#efe6d4","OPEN","OPEN STUDIO"],["#1844bf","WORLD","GLOBAL / 24"],["#ed573f","PLAY","FORM STUDY"],
  ["#151719","◉","OPTICAL"],["#88ed4d","EASE","NATURAL MOTION"],["#16368e","FUTURE","IS ALREADY"],["#f0d15a","1952","CUT-OUTS"],
  ["#f5f2e9","TYPE","EDITORIAL"],["#183d38","FILMS","LAUNCH"],["#e5a5bc","POSTER","GRAPHIC"],["#090b11","3D","OBJECT"]
 ];
 return <AbsoluteFill style={{...full,background:"#101319",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 48% 45%,#35405a,#0b0e14 72%)"}}/>
  <div style={{position:"absolute",left:150,right:150,top:94,bottom:104,display:"grid",gridTemplateColumns:"repeat(4,1fr)",gridTemplateRows:"repeat(3,1fr)",gap:20,transform:"perspective(1500px) rotateY(-7deg) rotateX(2deg) rotateZ(-1deg)",filter:"drop-shadow(0 32px 35px rgba(0,0,0,.42))"}}>
   {panels.map((p,i)=><div key={i} style={{position:"relative",background:p[0],border:"3px solid rgba(255,255,255,.72)",overflow:"hidden",boxShadow:"0 8px 18px rgba(0,0,0,.28)"}}>
    <div style={{position:"absolute",inset:0,opacity:.22,backgroundImage:"repeating-linear-gradient(135deg,transparent 0 14px,rgba(255,255,255,.28) 15px 17px)"}}/>
    {i%4===0?<div style={{position:"absolute",inset:"18%",border:"9px solid rgba(255,255,255,.8)",borderRadius:"50%",boxShadow:"0 0 0 12px rgba(255,255,255,.12)"}}/>:null}
    {i%4===1?<div style={{position:"absolute",left:"15%",right:"15%",top:"18%",height:"64%",background:"repeating-radial-gradient(circle at 50% 50%,rgba(255,255,255,.95) 0 4px,transparent 5px 13px)"}}/>:null}
    {i%4===2?<div style={{position:"absolute",right:"9%",top:"8%",width:"36%",height:"75%",border:"7px solid rgba(255,255,255,.65)",borderRadius:"50%"}}/>:null}
    {i%4===3?<div style={{position:"absolute",left:"12%",top:"17%",width:"75%",height:"63%",border:"5px solid rgba(20,20,20,.28)",transform:"rotate(-7deg)"}}/>:null}
    <div style={{position:"absolute",left:16,top:13,fontFamily:displayFont,fontSize:Math.min(62,p[1].length>7?34:58),fontWeight:1000,color:"#fff",letterSpacing:"-.06em",textShadow:"0 3px 9px rgba(0,0,0,.35)"}}>{p[1]}</div>
    <div style={{position:"absolute",left:17,right:17,bottom:13,fontSize:12,fontWeight:850,letterSpacing:".16em",color:"rgba(255,255,255,.82)"}}>{p[2]}</div>
   </div>)}
  </div>
  <div style={{position:"absolute",left:154,top:44,fontSize:16,fontWeight:900,letterSpacing:".2em",color:"#c8cfdb"}}>SELECTED WORK / OPEN DESIGN</div>
 </AbsoluteFill>;
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

const OutPoster = () => {
 const f=useCurrentFrame(),dx=e(f,0,9,28,0);
 return <AbsoluteFill style={{ ...full, background: "#08731f", color: "#f9fff4",overflow:"hidden" }}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 45%,#168d30,#006719 74%,#004b15)"}}/>
  <div style={{position:"absolute",left:"-4%",right:"-4%",top:220,textAlign:"center",transform:"translateX("+(dx-35)+"px)",opacity:.38,filter:"blur(10px)"}}><Word size={820} color="#fff" tracking={-.16}>OUT</Word></div>
  <div style={{position:"absolute",left:"-4%",right:"-4%",top:220,textAlign:"center",transform:"translateX("+dx+"px)"}}><Word size={620} color="#fff" tracking={-.16} style={{textShadow:"0 0 22px rgba(255,255,255,.15)"}}>OUT</Word></div>
  <div style={{position:"absolute",left:"-2%",right:"-2%",top:222,textAlign:"center",transform:"translateX("+(dx+24)+"px)",opacity:.18,filter:"blur(5px)"}}><Word size={820} color="#fff" tracking={-.16}>OUT</Word></div>
 <KineticHud color="#f2f2ed"/>
 </AbsoluteFill>;
};

const EasePoster = () => {
 const f=useCurrentFrame(),shift=e(f,0,10,48,0);
 return <AbsoluteFill style={{...full,background:"#f5f5ef",color:"#111813",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#fff 0%,#f4f6ee 100%)"}}/>
  <div style={{position:"absolute",left:"-6%",right:"-6%",top:238,transform:"translateX("+shift+"px)",textAlign:"center",fontFamily:displayFont,fontSize:760,fontWeight:1000,letterSpacing:"-.15em",color:"#07832b",textShadow:"3px 2px 0 #0b6f2a,7px 6px 0 #075c24,13px 13px 24px rgba(0,60,15,.22)"}}>EASE</div>
 <KineticHud/>
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
 const f=useCurrentFrame(),beam=e(f,0,14,-260,260);
 return <AbsoluteFill style={{...full,background:"#030508",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 43% 48%,#18212a 0%,#080c12 42%,#020305 78%)"}}/>
  <div style={{position:"absolute",left:"-2%",bottom:30,fontFamily:"Georgia,serif",fontSize:190,fontWeight:500,color:"#89929a",opacity:.19,letterSpacing:"-.08em"}}>1973</div>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <radialGradient id="source1973-orb-v30" cx="35%" cy="24%" r="80%"><stop stopColor="#f2fff0"/><stop offset=".25" stopColor="#a2d3c9"/><stop offset=".54" stopColor="#245e65"/><stop offset="1" stopColor="#06121a"/></radialGradient>
    <linearGradient id="source1973-white-v30" x1="0" x2="1"><stop stopColor="#fff" stopOpacity="0"/><stop offset=".34" stopColor="#fff" stopOpacity=".98"/><stop offset=".51" stopColor="#f8ffff" stopOpacity=".97"/><stop offset="1" stopColor="#fff" stopOpacity="0"/></linearGradient>
    <linearGradient id="source1973-spectrum-v30" x1="0" x2="1"><stop stopColor="#ed3bcb"/><stop offset=".16" stopColor="#574bfa"/><stop offset=".33" stopColor="#22b8ff"/><stop offset=".5" stopColor="#4de28e"/><stop offset=".67" stopColor="#f2e74c"/><stop offset=".83" stopColor="#ff9a33"/><stop offset="1" stopColor="#ee3a48"/></linearGradient>
    <pattern id="source1973-dots-v30" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="5.3" fill="#f05c44"/></pattern>
    <filter id="source1973-glow-v30"><feGaussianBlur stdDeviation="24"/></filter>
    <filter id="source1973-grain-v30"><feTurbulence type="fractalNoise" baseFrequency=".08" numOctaves="2" seed="19"/><feColorMatrix type="saturate" values="0"/></filter>
   </defs>
   <path d="M1040 -90L1510 1170" stroke="#fff" strokeWidth="190" opacity=".24" filter="url(#source1973-glow-v30)"/>
   <path d="M1080 -70L1495 1180" stroke="url(#source1973-white-v30)" strokeWidth="98" opacity=".98"/>
   <path d="M1010 -60L1425 1180" stroke="#f8ffff" strokeWidth="8" opacity=".96"/>
   <path d="M1102 -70L1517 1180" stroke="#88cfff" strokeWidth="3" opacity=".7"/>
   <path d="M1030 505L1920 345L1920 730L1080 575Z" fill="url(#source1973-spectrum-v30)" opacity=".88"/>
   <path d="M1100 525L1920 458" stroke="#fff" strokeWidth="18" opacity=".65" filter="url(#source1973-glow-v30)"/>
   <path d="M1095 535L1920 490" stroke="#fff" strokeWidth="3" opacity=".88"/>
   <path d="M1110 555L1920 590" stroke="#fff7d5" strokeWidth="2" opacity=".6"/>
   <circle cx="925" cy="545" r="202" fill="#071018" stroke="#e9fff0" strokeWidth="8"/>
   <circle cx="925" cy="545" r="179" fill="url(#source1973-orb-v30)" stroke="#c5e9df" strokeWidth="7"/>
   <circle cx="925" cy="545" r="151" fill="none" stroke="#dffdf4" strokeWidth="4" opacity=".82"/>
   <circle cx="925" cy="545" r="123" fill="none" stroke="#89d5cf" strokeWidth="3" opacity=".7"/>
   <path d="M870 425L1065 548L896 574L865 690Z" fill="#f5f3d9" stroke="#f9ffff" strokeWidth="8" opacity=".98"/>
   <path d="M884 444L1030 545L898 560Z" fill="#17312c"/>
   <path d="M0 820L550 650L785 740" stroke="#9fa9ad" strokeWidth="2" opacity=".24" fill="none"/>
   <rect x="1570" y="0" width="350" height="1080" fill="url(#source1973-dots-v30)" opacity=".95"/>
   <path d="M1540 0H1572V1080H1540Z" fill="#fff" opacity=".82"/>
   {Array.from({length:21},(_,i)=><path key={i} d={"M"+(1595+i*17)+" 0L"+(1595+i*17)+" 1080"} stroke="#ffb08e" strokeWidth="1" opacity=".18"/>)}
   <rect width="1920" height="1080" filter="url(#source1973-grain-v30)" opacity=".06"/>
  </svg>
  <div style={{position:"absolute",left:56,top:42,fontSize:18,color:"#9eabb5",fontWeight:850,letterSpacing:".2em"}}>OPTICAL STUDY / 1973</div>
  <div style={{position:"absolute",right:56,bottom:42,fontSize:15,color:"#f2b09c",fontWeight:850,letterSpacing:".19em"}}>LIGHT / COLOUR / MOTION</div>
 </AbsoluteFill>;
};

const PixelGamePoster=()=>{
 const f=useCurrentFrame(),jump=Math.sin(f/3)*7,glow=.5+.5*Math.sin(f/5);
 return <AbsoluteFill style={{...full,background:"#2eaef0",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0,shapeRendering:"crispEdges"}}>
   <rect width="1920" height="1080" fill="#36b8f5"/>
   <path d="M0 585L160 565L260 520L355 574L520 450L690 584L840 490L990 585L1150 440L1330 575L1490 485L1650 582L1800 500L1920 555V850H0Z" fill="#829be9" stroke="#5f7dd8" strokeWidth="9"/>
   <path d="M0 685L130 620L300 700L440 575L615 695L770 595L940 700L1100 578L1270 700L1430 605L1630 690L1800 590L1920 660V890H0Z" fill="#6a8ae4"/>
   <path d="M0 815L120 725L320 800L490 710L690 810L900 718L1090 810L1290 720L1510 815L1740 730L1920 805V1080H0Z" fill="#43b4e9"/>
   <g fill="#fff6da"><path d="M55 245h70v16H55zM75 230h40v15H75zM1280 185h85v16h-85zM1305 169h48v16h-48zM470 410h50v12h-50z"/></g>
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
   <g transform={"translate(960 "+(512+jump)+")"}>
    <path d="M-132 178V-72C-132 -205 132 -205 132 -72V178" fill="none" stroke="#111315" strokeWidth="46" strokeLinejoin="round"/>
    <path d="M-132 178V-72C-132 -205 132 -205 132 -72V178" fill="none" stroke="#f2bf31" strokeWidth="27" strokeLinejoin="round"/>
    <path d="M-112 165V-68C-112 -178 112 -178 112 -68V165" fill="none" stroke="#ffe57c" strokeWidth="7" opacity=".8"/>
    <path d="M-130 180H-35M35 180H130" stroke="#111315" strokeWidth="42"/>
    <path d="M-114 166H-44M44 166H114" stroke="#dfa72c" strokeWidth="20"/>
    <path d="M-12 -185L-12 -254L-3 -254L-3 -282L15 -282L15 -259L45 -259L45 -240L72 -240L72 -221L94 -221L94 -197L64 -197L64 -181L39 -181L39 -164L18 -164L18 -130L-4 -130L-4 -170L-12 -170Z" fill="#111315"/>
    <path d="M-2 -246V-274H17V-250H47V-231H77V-209H48V-192H21V-161H4V-189L-2 -189Z" fill="#fff"/>
    <path d="M-2 -246V-274H17V-250H47V-231H77V-209H48V-192H21V-161H4V-189L-2 -189Z" fill="none" stroke="#111315" strokeWidth="9"/>
    <path d="M-116 -75L-116 -164M116 -75L116 -164" stroke="#fff0ad" strokeWidth="6" opacity={glow}/>
   </g>
   <g fill="#f7c73a" stroke="#a56c16" strokeWidth="5">
    {Array.from({length:9},(_,i)=><g key={i} transform={"translate("+(1210+i*58)+" "+(390+Math.sin(i*.9)*45)+")"}><path d="M0 -17V17M-17 0H17" strokeWidth="11"/></g>)}
   </g>
   <path d="M0 910H1920V1080H0Z" fill="#e2b65f"/><path d="M0 910H1920" stroke="#ffe08b" strokeWidth="12"/>
   {Array.from({length:90},(_,i)=><rect key={i} x={(i*97)%1920} y={945+(i%4)*30} width="13" height="11" fill="#a6772d" opacity=".75"/>)}
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
 const f=useCurrentFrame(),rot=f*1.8;
 return <AbsoluteFill style={{...full,background:"#e9e8e2",overflow:"hidden"}}>
  <div style={{position:"absolute",left:0,top:0,bottom:0,width:54,background:"#c7c8c4",borderRight:"1px solid #aeb2b0"}}/>
  <div style={{position:"absolute",left:54,right:58,top:52,bottom:55,borderRadius:24,background:"#f8f8f4",border:"1px solid #bfc3c0",boxShadow:"0 24px 60px rgba(17,23,26,.16)",overflow:"hidden"}}>
   <div style={{position:"absolute",left:0,right:0,top:0,height:52,background:"#eceeea",borderBottom:"1px solid #cdd0cc",display:"flex",alignItems:"center",paddingLeft:26,gap:11}}>
    {["#d7aaa4","#d9c17e","#a9c8a9"].map((c,i)=><div key={i} style={{width:12,height:12,borderRadius:"50%",background:c}}/>)}<div style={{marginLeft:16,fontSize:15,fontWeight:800,color:"#6b7373",letterSpacing:".08em"}}>FIELD / PARTICLE MOTION</div>
   </div>
   <div style={{position:"absolute",left:30,right:30,top:80,bottom:28,borderRadius:15,background:"#07090d",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 51%,#1a1f25,#080a0e 56%,#030407)"}}/>
    <svg viewBox="0 0 1680 820" width="100%" height="100%" style={{position:"absolute",inset:0}}>
     <defs><radialGradient id="particle-core-v18"><stop stopColor="#e8f5ec" stopOpacity=".9"/><stop offset=".18" stopColor="#8daea0" stopOpacity=".38"/><stop offset="1" stopColor="#030508" stopOpacity="0"/></radialGradient><filter id="particle-blur-v18"><feGaussianBlur stdDeviation="6"/></filter></defs>
     <g transform={"translate(840 410) rotate("+rot+")"}>
      {Array.from({length:520},(_,i)=>{
       const a=i*2.399963,rad=32+Math.sqrt(i)*14+(i%9)*3;
       const x=Math.cos(a)*rad*1.2,y=Math.sin(a)*rad*.74;
       const size=1.4+(i%7)*.42,opacity=.18+(i%8)*.075;
       return <circle key={i} cx={x} cy={y} r={size} fill={i%11===0?"#d7eee1":"#bac5c2"} opacity={opacity}/>;
      })}
      <ellipse cx="0" cy="0" rx="360" ry="185" fill="none" stroke="#a7b9b3" strokeWidth="2" opacity=".14"/>
      <ellipse cx="0" cy="0" rx="295" ry="150" fill="none" stroke="#d9eee2" strokeWidth="1.5" opacity=".2" transform="rotate(-28)"/>
     </g>
     <ellipse cx="840" cy="410" rx="270" ry="220" fill="url(#particle-core-v18)" filter="url(#particle-blur-v18)" opacity=".5"/>
     <path d="M215 410H1465M840 105V715" stroke="#dce7e0" strokeWidth="1" opacity=".1"/>
    </svg>
    <div style={{position:"absolute",left:28,top:24,color:"#d0d7d5",fontSize:13,fontWeight:800,letterSpacing:".2em"}}>VORTEX / 001</div>
    <div style={{position:"absolute",right:28,bottom:24,color:"#a3b1ad",fontSize:12,fontWeight:800,letterSpacing:".17em"}}>PARTICLE FIELD — LIVE</div>
   </div>
  </div>
  <div style={{position:"absolute",right:14,top:90,bottom:90,width:26,background:"#c7c9c5",borderRadius:14,boxShadow:"inset 0 1px 4px rgba(0,0,0,.18)"}}/>
 </AbsoluteFill>;
};

const KineticHud=({color="#131a14"}:{color?:string})=>{
 const f=useCurrentFrame(),ticks=679+f*2,seconds=Math.floor(ticks/60),frames=ticks%60;
 const time="00:00:"+String(seconds).padStart(2,"0")+":"+String(frames).padStart(2,"0");
 return <AbsoluteFill style={{...full,pointerEvents:"none",color,fontFamily:"monospace",fontSize:15,fontWeight:850,letterSpacing:".14em"}}>
  <div style={{position:"absolute",left:70,top:32}}>OPEN DESIGN <span style={{opacity:.55}}>MOTION REEL — 2026</span></div>
  <div style={{position:"absolute",right:70,top:32}}>06 — KINETIC TYPE</div>
  <div style={{position:"absolute",left:35,top:35,width:22,height:22,borderLeft:"2px solid currentColor",borderTop:"2px solid currentColor"}}/>
  <div style={{position:"absolute",right:35,top:35,width:22,height:22,borderRight:"2px solid currentColor",borderTop:"2px solid currentColor"}}/>
  <div style={{position:"absolute",left:35,bottom:36,width:22,height:22,borderLeft:"2px solid currentColor",borderBottom:"2px solid currentColor"}}/>
  <div style={{position:"absolute",right:35,bottom:36,width:22,height:22,borderRight:"2px solid currentColor",borderBottom:"2px solid currentColor"}}/>
  <div style={{position:"absolute",left:70,bottom:53}}>{time}　60 FPS</div>
  <div style={{position:"absolute",right:70,bottom:53}}>128 BPM　■ □ □ □　BAR 7/8</div>
  <div style={{position:"absolute",left:40,right:40,bottom:25,height:2,background:"currentColor",opacity:.46}}>
   <div style={{width:(Math.min(1,f/72)*100)+"%",height:"100%",background:"currentColor"}}/>
  </div>
 </AbsoluteFill>;
};
const EaseGreen=()=>{
 const f=useCurrentFrame(),shift=e(f,0,7,95,0),ghost=1-e(f,1,8);
 return <AbsoluteFill style={{...full,background:"#8ff04e",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(115deg,#9af55f,#82e846 60%,#a7f77b)"}}/>
  <div style={{position:"absolute",left:"-8%",right:"-8%",top:282,textAlign:"center",transform:"translateX("+(shift-34)+"px) scaleX(1.9) scaleY(.6)",opacity:.24*ghost,filter:"blur(8px)"}}><Word size={880} color="#101512" tracking={-.15}>EASE</Word></div>
  <div style={{position:"absolute",left:"-8%",right:"-8%",top:282,textAlign:"center",transform:"translateX("+shift+"px) scaleX(1.9) scaleY(.6)",filter:"blur(.25px)"}}><Word size={600} color="#101512" tracking={-.15} style={{textShadow:"0 4px 0 rgba(20,52,21,.25)"}}>EASE</Word></div>
 <KineticHud/>
 </AbsoluteFill>;
};

const GreenCircleTransition=()=>{
 const f=useCurrentFrame(),r=860-100*e(f,0,1),fade=1-e(f,5,6),bloom=930*e(f,0,1);
 return <AbsoluteFill style={{...full,background:"#8df04e",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%">
   <circle cx="960" cy="540" r={bloom} fill="#f8faf5"/>
   <circle cx="960" cy="540" r="930" fill="none" stroke="#eaffdf" strokeWidth="8" opacity=".78"/>
   <circle cx="960" cy="540" r={r} fill="none" stroke="#f5ffed" strokeWidth="9" opacity={fade}/>
   <circle cx="960" cy="540" r={r*.78} fill="none" stroke="#e7ffda" strokeWidth="2" opacity={fade*.78}/>
   <g transform={"translate(960 540) rotate(-12)"}><rect x="-24" y="-24" width="48" height="48" rx="9" fill="#111713"/><path d="M-8 -15L15 0L-8 15Z" fill="#eef7e9"/></g>
   <circle cx="1120" cy="752" r="5" fill="#111713"/>
  </svg>
 </AbsoluteFill>;
};
const NotText=({fullText=false}:{fullText?:boolean})=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{...full,background:"#090a0b",color:"#333537"}}>
  <div style={{position:"absolute",left:0,right:0,top:424,textAlign:"center",transform:"scale("+(0.97+e(f,0,9)*.03)+")",opacity:.76}}><Word size={fullText?130:132} color="#343638" tracking={-.07}>{fullText?"Not just":"Not"}</Word></div>
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
 const f=useCurrentFrame(),rise=e(f,0,5,45,0),trail=1-e(f,0,8);
 const glyphs=(front:boolean)=>(
  <div style={{position:"absolute",left:"50%",top:"31%",width:680,height:520,transform:"translate(-50%,-50%) translateY("+rise+"px) scale(1.02,1.08)",fontFamily:displayFont,fontWeight:1000,whiteSpace:"nowrap",lineHeight:.78}}>
   <span style={{position:"absolute",left:20,top:155,fontSize:500,letterSpacing:"-.08em"}}>I</span>
   <span style={{position:"absolute",left:160,top:0,fontSize:650,letterSpacing:"-.1em"}}>N</span>
  </div>
 );
 return <AbsoluteFill style={{...full,background:"#08090b",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 48% 52%,#22282e,#08090b 70%)"}}/>
  {Array.from({length:10},(_,i)=><div key={i} style={{position:"absolute",left:"50%",top:"31%",width:680,height:520,transform:"translate(-50%,-50%) translate("+(i*1.5-18)+"px,"+(i*18+3)+"px) scale(1.02,1.08)",fontFamily:displayFont,fontWeight:1000,whiteSpace:"nowrap",lineHeight:.78,color:["#aeb4b9","#959da3","#7e878e","#68727a","#535e67","#414b54","#333d46","#252e37","#1a222a","#11181f"][i]}}>
    <span style={{position:"absolute",left:20,top:155,fontSize:500,letterSpacing:"-.08em"}}>I</span>
    <span style={{position:"absolute",left:160,top:0,fontSize:650,letterSpacing:"-.1em"}}>N</span>
   </div>)}
  <div style={{position:"absolute",left:"50%",top:"31%",width:680,height:520,transform:"translate(-50%,-50%) translateY("+rise+"px) scale(1.02,1.08)",fontFamily:displayFont,fontWeight:1000,whiteSpace:"nowrap",lineHeight:.78,color:"#f7f7f3",filter:"drop-shadow(0 3px 1px rgba(0,0,0,.25))"}}>
   <span style={{position:"absolute",left:20,top:155,fontSize:500,letterSpacing:"-.08em"}}>I</span>
   <span style={{position:"absolute",left:160,top:0,fontSize:650,letterSpacing:"-.1em"}}>N</span>
  </div>
  <KineticHud color="#f2f2ed"/>
 </AbsoluteFill>;
};
const InPoster=()=>{
 const f=useCurrentFrame(),dot=.9+.1*Math.sin(f/2);
 return <AbsoluteFill style={{...full,background:"#07080b",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"-3%",right:"-3%",top:245,textAlign:"center",fontFamily:displayFont,fontSize:650,fontWeight:1000,letterSpacing:"-.14em",lineHeight:.9,color:"#f6f6f1",textShadow:"0 4px 0 rgba(255,255,255,.12)"}}>IN.</div>
  <div style={{position:"absolute",left:"58.1%",top:535,width:47,height:47,borderRadius:"50%",background:"#9ceb51",boxShadow:"0 0 34px rgba(156,235,81,.5)",transform:"scale("+dot+")"}}/>
 <KineticHud color="#f2f2ed"/>
 </AbsoluteFill>;
};

const MindPoster = () => {
 const f=useCurrentFrame(),shift=Math.sin(f/5)*12;
 return <AbsoluteFill style={{...full,background:"#192be4",color:"#060816",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(125deg,#263cf2,#1723cb 60%,#101b9a)"}}/>
  <div style={{position:"absolute",inset:0,backgroundImage:"radial-gradient(rgba(255,255,255,.17) 1.5px,transparent 2px)",backgroundSize:"22px 22px",opacity:.35}}/>
  <div style={{position:"absolute",left:-110,right:-22,top:35,transform:"translateX("+shift+"px)"}}>
   <Word size={286} color="#080b18" tracking={-.13}>MIND MIND</Word>
   <Word size={286} color="#111a6a" tracking={-.13} style={{WebkitTextStroke:"2px rgba(240,242,255,.72)"}}>MIND MIND</Word>
   <Word size={286} color="#090d20" tracking={-.13}>MIND MIND</Word>
   <Word size={286} color="#0e174f" tracking={-.13} style={{WebkitTextStroke:"2px rgba(240,242,255,.42)"}}>MIND MIND</Word>
  </div>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><linearGradient id="mind-prism-v30" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#f7f9ff" stopOpacity=".8"/><stop offset=".42" stopColor="#8fa8ff" stopOpacity=".5"/><stop offset="1" stopColor="#bfe9ff" stopOpacity=".13"/></linearGradient><filter id="mind-glass-v30"><feGaussianBlur stdDeviation="3"/></filter></defs>
   <g transform={"translate(960 540) rotate("+(-8+Math.sin(f/13)*3)+")"} opacity=".72">
    <path d="M0 -205L182 -75L145 160L-70 208L-205 35L-140 -160Z" fill="url(#mind-prism-v30)" stroke="#d9e7ff" strokeWidth="7"/>
    <path d="M0 -205L-70 208L-205 35Z" fill="#e7f5ff" fillOpacity=".19"/>
    <path d="M0 -205L182 -75L-70 208Z" fill="#a8c4ff" fillOpacity=".24"/>
    <path d="M182 -75L145 160L-70 208Z" fill="#f3dcff" fillOpacity=".23"/>
    <path d="M-140 -160L0 -205L-205 35" fill="none" stroke="#fff" strokeWidth="5" opacity=".72" filter="url(#mind-glass-v30)"/>
   </g>
  </svg>
  <div style={{position:"absolute",left:76,top:35,fontSize:15,fontWeight:900,letterSpacing:".19em",color:"#d8dcff"}}>MIND / TYPOGRAPHIC SYSTEM</div>
  <div style={{position:"absolute",right:80,bottom:48,fontSize:15,fontWeight:900,letterSpacing:".17em",color:"#d8dcff"}}>IDEAS IN MOTION / 04</div>
 </AbsoluteFill>;
};

const RingPoster = () => {
 const f=useCurrentFrame(),zoom=1.92+0.04*Math.sin(f/7);
 const rings=[540,475,410,345,280,215,150,85,28];
 const slogans=[
  "THE FUTURE IS ALREADY HERE · THE FUTURE IS ALREADY HERE ·",
  "THE FUTURE · MOTION DESIGN · OPEN DESIGN · THE FUTURE ·",
  "THE FUTURE IS ALREADY HERE · THE FUTURE IS ALREADY HERE ·",
  "OPEN DESIGN / MOTION / THE FUTURE IS HERE /",
  "THE FUTURE IS ALREADY HERE · OPEN DESIGN ·",
  "MOTION / THE FUTURE / OPEN DESIGN /",
  "THE FUTURE · MOTION · THE FUTURE ·",
  "OPEN DESIGN / MOTION / THE FUTURE /",
  "THE FUTURE / MOTION /"
 ];
 const sizes=[76,64,54,46,38,31,25,19,14];
 return <AbsoluteFill style={{...full,background:"#030405",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0,transform:"rotate("+f*.12+"deg) scale("+zoom+")"}}>
   <defs>
    {rings.map((r,i)=>{const next=rings[i+1]??Math.max(10,r-28),pathR=(r+next)/2;return <path key={r} id={"ring-v53-"+i} d={"M960 540m-"+pathR+" 0a"+pathR+" "+pathR+" 0 1 1 "+(pathR*2)+" 0a"+pathR+" "+pathR+" 0 1 1 -"+(pathR*2)+" 0"}/>;})}
    <filter id="ring-paper-v53"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="1.8"/></filter>
   </defs>
   {rings.map((r,i)=><circle key={r} cx="960" cy="540" r={r} fill={i%2===0?"#f7f6f1":"#050609"}/>)}
   <g fontFamily="Arial Black,Arial,sans-serif" fontWeight="1000" filter="url(#ring-paper-v53)">
    {rings.map((r,i)=><text key={"text-"+i} fill={i%2===0?"#111315":"#f7f6f1"} fontSize={sizes[i]} letterSpacing={i<3?4:2}>
      <textPath href={"#ring-v53-"+i}>{slogans[i]}</textPath>
     </text>)}
   </g>
   <circle cx="960" cy="540" r="16" fill="#f7f6f1"/>
  </svg>
  <Noise opacity={.065}/>
 </AbsoluteFill>;
};
const NeverPoster = () => {
 const f=useCurrentFrame(),shift=e(f,0,9,26,0);
 return <AbsoluteFill style={{...full,background:"#c8f7a6",color:"#101713",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"linear-gradient(110deg,#d5f9b9,#c3f59b 62%,#ddfbc5)"}}/>
  <div style={{position:"absolute",left:"-2%",right:"-2%",top:305,textAlign:"center",display:"flex",justifyContent:"center",alignItems:"baseline",gap:2,transform:"translateX("+shift+"px)"}}>
   {"NEVER".split("").map((ch,i)=><span key={i} style={{fontFamily:displayFont,fontSize:640-(i===2?35:0),fontWeight:1000,letterSpacing:"-.13em",color:"#111713",transform:"translateY("+(i===0?26:i===1?0:i===2?-80:i===3?-104:-20)+"px) skewX("+(i===2?-9:0)+"deg)",textShadow:"0 5px 0 rgba(15,35,16,.2)"}}>{ch}</span>)}
  </div>
 <KineticHud/>
 </AbsoluteFill>;
};

const LinearPoster = () => {
 const f=useCurrentFrame(),resolve=e(f,0,2),dot=e(f,2,4),ghost=1-e(f,0,5);
 const common={position:"absolute" as const,left:"-4%",right:"-4%",top:305,textAlign:"center" as const,fontFamily:displayFont,fontWeight:1000,letterSpacing:"-.12em",lineHeight:.9};
 return <AbsoluteFill style={{...full,background:"#0b0d10",color:"#f5f6f3",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 48%,#171b20,#080a0c 70%)"}}/>
  <div style={{...common,fontSize:600,transform:"translateX(-65px)",opacity:(1-resolve)*.45*ghost,filter:"blur(10px)"}}><Word size={660} color="#fff" tracking={-.12}>IN</Word></div>
  <div style={{...common,fontSize:600,transform:"translateX(-28px)",opacity:1-resolve,filter:"blur(1.5px)"}}><Word size={600} color="#f4f5f4" tracking={-.12}>IN</Word></div>
  <div style={{...common,fontSize:560,opacity:resolve,transform:"translateX("+(10*(1-resolve))+"px)"}}><Word size={660} color="#f4f5f2" tracking={-.12}>LINEAR.</Word></div>
  <div style={{position:"absolute",left:"72.3%",top:525,width:30,height:30,borderRadius:"50%",background:"#a3ef4d",opacity:dot,boxShadow:"0 0 20px rgba(163,239,77,.25)"}}/>
  <div style={{position:"absolute",left:48,right:48,bottom:31,height:2,background:"#5d6569",opacity:.28}}/>
 <KineticHud color="#f2f2ed"/>
 </AbsoluteFill>;
};

const ClockPoster = () => {
 const f=useCurrentFrame(),rot=f*1.1;
 const sky=Array.from({length:1350},(_,i)=>{
  const x=(i*197)%1920,y=(i*113)%1080,cx=960+(i%5-2)*140,cy=440+(i%7-3)*80;
  const angle=Math.atan2(y-cy,x-cx)+Math.PI/2+Math.sin(i*1.73)*.35;
  const len=28+(i*29)%104,dx=Math.cos(angle)*len,dy=Math.sin(angle)*len*.62;
  return {x1:x-dx*.5,y1:y-dy*.5,x2:x+dx*.5,y2:y+dy*.5,qx:x+Math.sin(angle)*len*.24,qy:y-Math.cos(angle)*len*.18,w:4+(i*7)%12,c:["#102d82","#19409b","#2b56b5","#4773cc","#6f94db","#8ba9e7","#bfd1eb"][i%7],o:.24+(i%6)*.075};
 });
 const halo=Array.from({length:410},(_,i)=>{
  const a=i*2.399963,r=320+(i%13)*9,x=960+Math.cos(a)*r,y=520+Math.sin(a)*r*.9;
  const len=22+(i*19)%70,dx=-Math.sin(a)*len,dy=Math.cos(a)*len*.9;
  return {x1:x-dx*.5,y1:y-dy*.5,x2:x+dx*.5,y2:y+dy*.5,qx:x+Math.cos(a)*12,qy:y+Math.sin(a)*10,w:5+(i%8)*3,c:["#b87524","#d79735","#f4c75a","#ffe18c","#eab64c"][i%5],o:.38+(i%5)*.09};
 });
 const treeMarks=Array.from({length:390},(_,i)=>{
  const y=35+(i*27)%1030,half=18+Math.sin(y/82)*63+(i%7)*4,x=135+Math.sin(i*2.1)*half,side=i%2?1:-1;
  return {x,y,w:5+(i%8)*3,dx:side*(20+(i%6)*10),c:["#052f27","#0a4334","#14543d","#1c6548"][i%4]};
 });
 const townStrokes=Array.from({length:220},(_,i)=>{
  const x=1260+(i*37)%610,y=730+(i*23)%260;
  return {x,y,w:10+(i%8)*5,dx:8+(i%5)*8,c:i%3===0?"#293b79":"#101c54"};
 });
 const faceMarks=Array.from({length:240},(_,i)=>{
  const a=i*2.399963+(i%9)*.08,r=26+((i*31)%166),x=960+Math.cos(a)*r,y=520+Math.sin(a)*r*.92;
  const len=9+(i*17)%32,dx=-Math.sin(a)*len,dy=Math.cos(a)*len*.7;
  return {x1:x-dx*.5,y1:y-dy*.5,x2:x+dx*.5,y2:y+dy*.5,qx:x+Math.cos(a)*5,qy:y+Math.sin(a)*5,w:2+(i%5)*1.5,c:["#16377e","#2852a0","#4670bf","#7293d0","#d5b45f"][i%5],o:.16+(i%5)*.055};
 });
 const stars=[{x:485,y:150,r:15},{x:1310,y:72,r:18},{x:1568,y:585,r:12},{x:340,y:590,r:10},{x:1130,y:220,r:8}];
 return <AbsoluteFill style={{...full,background:"#163d9f",overflow:"hidden",color:"#f3d47c"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <radialGradient id="clock-sky-v53" cx="51%" cy="44%" r="72%"><stop stopColor="#3765c0"/><stop offset=".45" stopColor="#1d46a7"/><stop offset="1" stopColor="#071b59"/></radialGradient>
    <radialGradient id="clock-face-v53"><stop stopColor="#224aab"/><stop offset="1" stopColor="#0d2a77"/></radialGradient>
    <linearGradient id="clock-gold-v53" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#fff1a2"/><stop offset=".26" stopColor="#f2c44e"/><stop offset=".62" stopColor="#c8862e"/><stop offset="1" stopColor="#fce18b"/></linearGradient>
    <filter id="clock-paint-v53"><feTurbulence type="fractalNoise" baseFrequency=".026 .034" numOctaves="3" seed="18" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation=".5"/></filter>
    <filter id="clock-glow-v53"><feGaussianBlur stdDeviation="26"/></filter>
    <clipPath id="clock-face-clip-v67"><circle cx="960" cy="520" r="238"/></clipPath>
   </defs>
   <rect width="1920" height="1080" fill="url(#clock-sky-v53)"/>
   <g fill="none" strokeLinecap="round" filter="url(#clock-paint-v53)">
    {sky.map((p,i)=><path key={i} d={"M"+p.x1+" "+p.y1+"Q"+p.qx+" "+p.qy+" "+p.x2+" "+p.y2} stroke={p.c} strokeWidth={p.w} opacity={p.o}/>)}
   </g>
   <g fill="none" strokeLinecap="round" filter="url(#clock-paint-v53)">
    {halo.map((p,i)=><path key={"halo-"+i} d={"M"+p.x1+" "+p.y1+"Q"+p.qx+" "+p.qy+" "+p.x2+" "+p.y2} stroke={p.c} strokeWidth={p.w} opacity={p.o}/>)}
   </g>
   {stars.map((s,i)=><g key={"star-"+i}>
     <circle cx={s.x} cy={s.y} r={s.r*2.9} fill="#ffd958" opacity=".32" filter="url(#clock-glow-v53)"/>
     <circle cx={s.x} cy={s.y} r={s.r} fill="#ffdf5e"/>
     <path d={"M"+(s.x-s.r*2.8)+" "+s.y+"Q"+s.x+" "+(s.y-s.r*.8)+" "+(s.x+s.r*2.8)+" "+s.y} stroke="#fff0a2" strokeWidth="5" opacity=".75"/>
    </g>)}
   <g filter="url(#clock-paint-v53)">
    <path d="M0 894C195 858 315 890 453 917C597 946 712 1004 845 1000C1020 995 1174 934 1304 943C1528 959 1663 1024 1920 982V1080H0Z" fill="#112b78"/>
    <path d="M0 1008C186 957 361 970 512 1011C674 1054 824 1041 986 1014C1148 987 1296 975 1451 1002C1630 1033 1797 1041 1920 1019V1080H0Z" fill="#071d59"/>
   </g>
   <g filter="url(#clock-paint-v53)">
    <path d="M62 1080C18 974 84 887 46 800C82 719 40 639 71 562C34 474 85 386 73 311C92 222 112 124 160 24C211 110 195 205 229 293C201 387 239 467 204 555C241 644 200 731 233 815C267 912 218 1007 258 1080Z" fill="#07392c" stroke="#0a563b" strokeWidth="12"/>
    <path d="M58 887C22 804 44 723 88 651C139 727 138 815 185 938Z" fill="#0c563c"/>
    <path d="M78 669C11 609 21 521 72 425C147 486 148 584 78 669Z" fill="#0c4b36"/>
    <path d="M105 492C174 422 182 334 139 256C78 327 72 415 105 492Z" fill="#105b3e"/>
    <path d="M130 311C71 267 62 187 129 106C183 187 180 263 130 311Z" fill="#0b5137"/>
    {treeMarks.map((p,i)=><path key={"tree-mark-"+i} d={"M"+p.x+" "+p.y+"q "+p.dx+" -"+p.w+" "+(p.dx*1.2)+" "+(p.w*.4)} stroke={p.c} strokeWidth={p.w} strokeLinecap="round" opacity=".78" fill="none"/>)}
   </g>
   <g filter="url(#clock-paint-v53)">
    <path d="M1228 1006L1228 890L1274 890L1274 835L1317 835L1317 874L1364 874L1364 928L1407 928L1407 1006Z" fill="#17235f"/>
    <path d="M1378 1006L1378 840L1413 840L1413 785L1447 785L1447 840L1481 840L1481 1006Z" fill="#0d1b56"/>
    <path d="M1450 1006L1450 888L1497 888L1497 831L1540 831L1540 879L1585 879L1585 1006Z" fill="#19255e"/>
    <path d="M1548 1006L1548 910L1592 910L1592 851L1632 851L1632 910L1681 910L1681 1006Z" fill="#101a50"/>
    <path d="M1419 790L1432 565L1445 790Z" fill="#0b1747"/>
    {townStrokes.map((p,i)=><path key={"town-"+i} d={"M"+p.x+" "+p.y+"l"+p.dx+" -"+(p.w*.35)} stroke={p.c} strokeWidth={p.w} strokeLinecap="round" opacity=".35"/>)}
    {Array.from({length:46},(_,i)=>{
      const x=1260+(i*57)%450,y=884+(i*33)%100;
      return <rect key={"window-"+i} x={x} y={y} width={6+(i%3)*3} height={11+(i%4)*2} fill="#ffdb62" opacity={.55+(i%4)*.1}/>;
    })}
   </g>
   <g filter="url(#clock-glow-v53)" opacity=".35"><circle cx="960" cy="520" r="320" fill="#f8cb5c"/></g>
   <g transform={"translate(960 520) rotate("+rot+")"} filter="url(#clock-paint-v53)">
    <circle r="282" fill="url(#clock-gold-v53)" stroke="#ffeaa1" strokeWidth="12"/>
    <circle r="246" fill="url(#clock-face-v53)" stroke="#e3ac42" strokeWidth="14"/>
    <circle r="226" fill="none" stroke="#ffdc74" strokeWidth="5"/>
    <circle r="212" fill="none" stroke="#08245f" strokeWidth="5"/>
    <g clipPath="url(#clock-face-clip-v67)" fill="none" strokeLinecap="round" opacity=".75">{faceMarks.map((m,i)=><path key={"face-brush-"+i} d={"M"+m.x1+" "+m.y1+"Q"+m.qx+" "+m.qy+" "+m.x2+" "+m.y2} stroke={m.c} strokeWidth={m.w} opacity={m.o}/>)}</g>
    <path d="M-12 -18L22 -11L147 60L80 69L-3 7Z" fill="#ffd64e" stroke="#d18b2b" strokeWidth="5"/>
    <path d="M-4 -6L125 59" stroke="#fff0a1" strokeWidth="4" opacity=".7"/>
    <circle r="17" fill="#ffe082" stroke="#c18429" strokeWidth="6"/>
   </g>
   <g fill="none" strokeLinecap="round" opacity=".6">
    {Array.from({length:150},(_,i)=>{
      const a=i*2.399963,r=255+(i%8)*12,x=960+Math.cos(a)*r,y=520+Math.sin(a)*r;
      return <path key={"clock-glaze-"+i} d={"M"+x+" "+y+"q "+(Math.cos(a+1.2)*16)+" "+(Math.sin(a+1.2)*12)+" "+(Math.cos(a+1.5)*32)+" "+(Math.sin(a+1.5)*16)} stroke={i%2===0?"#ffe38c":"#9b5c28"} strokeWidth={3+(i%5)*2} opacity={.25+(i%4)*.12}/>;
    })}
   </g>
  </svg>
  <div style={{position:"absolute",left:0,right:0,top:24,textAlign:"center",fontFamily:"Georgia,serif",fontSize:84,fontWeight:900,letterSpacing:".03em",color:"#ffca35",textShadow:"0 4px 0 #9a6023,0 7px 12px rgba(0,0,0,.28)"}}>1889</div>
  <div style={{position:"absolute",left:0,right:0,top:104,textAlign:"center",fontFamily:"Georgia,serif",fontSize:38,fontWeight:850,letterSpacing:".025em",color:"#f4c348",textShadow:"0 3px 0 #935b29,0 5px 10px rgba(0,0,0,.25)"}}>Post-Impressionism</div>
 </AbsoluteFill>;
};
const StatsPoster = () => {
 const f=useCurrentFrame();
 const counts=[80,82,84,87,91,93,94,96],days=[88,96,104,111,119,126,132,138];
 const index=Math.max(0,Math.min(7,Math.round(f))),count=counts[index],day=days[index],y=590-5.25*count;
 return <AbsoluteFill style={{...full,background:"linear-gradient(180deg,#bfe9e5 0%,#b9e8de 45%,#e9d5bd 70%,#70c6bd 100%)",overflow:"hidden"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <path d="M0 675Q170 610 360 678T720 680T1100 675T1510 680T1920 670V1080H0Z" fill="#69c4bd" opacity=".72"/>
   <path d="M0 810Q190 750 375 817T760 817T1150 810T1510 825T1920 800V1080H0Z" fill="#f0cfb3" opacity=".67"/>
   <path d="M0 935Q205 870 430 934T870 938T1300 925T1700 944T1920 925V1080H0Z" fill="#49b5b2" opacity=".45"/>
   {Array.from({length:22},(_,i)=><path key={i} d={"M"+(i*105-80)+" 700q 55 -25 105 0t 105 0"} fill="none" stroke="#f1f4e4" strokeWidth="5" opacity=".2"/>)}
  </svg>
  <div style={{position:"absolute",left:47,top:255,fontFamily:displayFont,fontSize:275,fontWeight:1000,color:"#111315",letterSpacing:"-.13em",lineHeight:.86,textShadow:"0 4px 0 rgba(0,0,0,.06)"}}>{count}K</div>
  <div style={{position:"absolute",left:65,top:535,fontSize:51,fontWeight:850,color:"#303a39"}}>Day {day}</div>
  <div style={{position:"absolute",left:650,top:94,width:1200,height:850,borderRadius:16,background:"#fff",padding:"38px 43px 26px",boxSizing:"border-box",boxShadow:"0 15px 45px rgba(37,85,92,.16)"}}>
   <div style={{textAlign:"center",fontSize:27,fontWeight:900,color:"#202326",marginBottom:17}}>◉ Star History</div>
   <div style={{position:"absolute",left:48,top:87,fontSize:18,fontWeight:750,color:"#45494b"}}>nexu-io / open-design</div>
   <svg viewBox="0 0 1040 590" width="100%" height="590">
    {[0,1,2,3,4].map(v=><g key={v}><line x1="70" x2="985" y1={65+v*105} y2={65+v*105} stroke="#e6e6e3" strokeWidth="2"/><text x="8" y={72+v*105} fontSize="21" fill="#4a4e50">{100-v*20}K</text></g>)}
    <path d={"M70 575C98 490 132 350 210 300S360 225 455 205S660 175 900 "+y} stroke="#cb4b3e" strokeWidth="7" fill="none" strokeLinecap="round"/>
    <circle cx="900" cy={y} r="13" fill="#b9f05b" stroke="#141719" strokeWidth="4"/>
    <text x="70" y="560" fontSize="19" fill="#303638">May</text><text x="245" y="560" fontSize="19" fill="#303638">June</text><text x="415" y="560" fontSize="19" fill="#303638">July</text><text x="585" y="560" fontSize="19" fill="#303638">August</text><text x="750" y="560" fontSize="19" fill="#303638">September</text><text x="900" y="560" fontSize="19" fill="#303638">October</text>
    <text x="5" y="35" fontSize="16" fill="#535a5b">GitHub Stars</text>
    <text x="520" y="585" textAnchor="middle" fontSize="16" fill="#535a5b">Date</text>
   </svg>
   <div style={{position:"absolute",right:25,bottom:12,fontSize:15,color:"#737a79"}}>★ star-history.com</div>
  </div>
 </AbsoluteFill>;
};

const TogglePoster = () => {
 const f=useCurrentFrame(),on=e(f,0,4);
 return <AbsoluteFill style={{...full,background:"#f1f0eb",color:"#151719",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"50%",top:"50%",width:190,height:98,transform:"translate(-50%,-50%)",borderRadius:52,background:"#deded9",boxShadow:"inset 0 3px 9px rgba(0,0,0,.13),0 3px 9px rgba(0,0,0,.08)",padding:8,boxSizing:"border-box"}}>
   <div style={{position:"absolute",left:8,top:8,width:82,height:82,borderRadius:"50%",background:"#fff",transform:"translateX("+(82*on)+"px)",boxShadow:"0 3px 9px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.8)"}}/>
   <div style={{position:"absolute",right:31,top:42,width:7,height:7,borderRadius:"50%",background:"#969995",opacity:.45}}/>
  </div>
 </AbsoluteFill>;
};

const EyePoster = () => {
 const f=useCurrentFrame(),blink=1-.05*Math.max(0,Math.sin(f/5));
 return <AbsoluteFill style={{...full,background:"#03040a",overflow:"hidden",color:"#edf3ff"}}>
  <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs>
    <linearGradient id="eye-field-v30" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#111d78"/><stop offset=".36" stopColor="#2847ef"/><stop offset=".66" stopColor="#172cba"/><stop offset="1" stopColor="#070d46"/></linearGradient>
    <radialGradient id="eye-iris-v30"><stop stopColor="#050817"/><stop offset=".14" stopColor="#1c36bd"/><stop offset=".42" stopColor="#3174ff"/><stop offset=".72" stopColor="#8cb6ff"/><stop offset="1" stopColor="#162667"/></radialGradient>
    <pattern id="eye-grid-v30" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#8eb6ff" strokeWidth="1" opacity=".42"/><circle cx="11" cy="11" r="1.5" fill="#e0ecff" opacity=".65"/></pattern>
    <clipPath id="eye-clip-v30"><path d="M0 540L220 387L605 270L960 242L1315 270L1700 387L1920 540L1700 693L1315 810L960 838L605 810L220 693Z"/></clipPath>
   </defs>
   <path d="M0 540L220 387L605 270L960 242L1315 270L1700 387L1920 540L1700 693L1315 810L960 838L605 810L220 693Z" fill="url(#eye-field-v30)" stroke="#5478ef" strokeWidth="8"/>
   <g clipPath="url(#eye-clip-v30)">
    <rect width="1920" height="1080" fill="url(#eye-grid-v30)" opacity=".68"/>
    <path d="M40 540H1880M960 250V830" stroke="#b4d0ff" strokeWidth="2" opacity=".2"/>
    <circle cx="960" cy="540" r={294*blink} fill="url(#eye-iris-v30)" stroke="#0a164d" strokeWidth="16"/>
    <circle cx="960" cy="540" r="265" fill="none" stroke="#a2c2ff" strokeWidth="5" opacity=".82"/>
    {Array.from({length:180},(_,i)=>{const a=i*Math.PI*2/180,inner=102+(i%7)*5,outer=276-(i%5)*7;return <path key={i} d={"M"+(960+Math.cos(a)*inner)+" "+(540+Math.sin(a)*inner)+"L"+(960+Math.cos(a)*outer)+" "+(540+Math.sin(a)*outer)} stroke={i%3===0?"#d5e7ff":"#6295ff"} strokeWidth={i%5===0?5:2} opacity={.42+(i%4)*.1}/>;})}
    <circle cx="960" cy="540" r="111" fill="#02050d" stroke="#0b1554" strokeWidth="14"/>
    <circle cx="921" cy="488" r="31" fill="#f3f7ff" opacity=".95"/><circle cx="1001" cy="600" r="10" fill="#c8ddff" opacity=".8"/>
    <path d="M0 540L220 387L605 270L960 242L1315 270L1700 387" fill="none" stroke="#b9d4ff" strokeWidth="6" opacity=".6"/>
    <path d="M0 540L220 693L605 810L960 838L1315 810L1700 693" fill="none" stroke="#081a62" strokeWidth="8" opacity=".8"/>
   </g>
   <path d="M0 540L220 387L605 270L960 242L1315 270L1700 387L1920 540L1700 693L1315 810L960 838L605 810L220 693Z" fill="none" stroke="#89acff" strokeWidth="5"/>
  </svg>
  <div style={{position:"absolute",left:88,top:74,fontFamily:"monospace",fontSize:16,fontWeight:900,letterSpacing:".2em",color:"#8baaff"}}>OPTIC / IRIS ANALYSIS</div>
  <div style={{position:"absolute",right:85,bottom:75,textAlign:"right",fontFamily:displayFont,fontSize:48,fontWeight:950,color:"#f2f5ff",letterSpacing:"-.04em"}}>3.7%</div>
 </AbsoluteFill>;
};

const PosterSequence = () => (
 <AbsoluteFill style={full}>
  <Sequence from={0} durationInFrames={2}><GalleryWall showClaim={false}/></Sequence>
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
  <Sequence from={180} durationInFrames={14}><LinearPoster /></Sequence>
  <Sequence from={194} durationInFrames={6}><GreenCircleTransition /></Sequence>
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
 const orbitProgress=e(f,109,119);
 const Phrase=({phase}:{phase:number})=>{
  if(phase===0)return <div style={{position:"absolute",left:0,right:0,top:360,height:320,display:"flex",alignItems:"center",justifyContent:"center",opacity:.38+.62*e(f,0,5)}}>
   <Word size={186} color="#101113" weight={900} tracking={-.09}>Any</Word>
  </div>;
  if(phase===1){
   const reveal=e(f,4,9);
   return <div style={{position:"absolute",left:0,right:0,top:355,height:330,display:"flex",alignItems:"center",justifyContent:"center"}}>
    <Word size={230} color="#101113" weight={900} tracking={-.09}>Any m</Word>
    <div style={{width:136,height:136,display:"grid",placeItems:"center",marginLeft:-5,marginRight:-5,transform:"translateY("+Math.sin(f/8)*3+"px)"}}>
     <div style={{transform:"scale(1.22)"}}><ProviderBadge index={f<29?1:f<39?4:f<49?5:f<59?3:6} frame={f}/></div>
    </div>
    <Word size={230} color="#101113" weight={900} tracking={-.09} style={{opacity:.14+.86*reveal,transform:"translateY("+((1-reveal)*14)+"px)"}}>del.</Word>
   </div>;
  }
  const count=phase===2?4:7;
  const textSize=phase===2?210+30*(1-e(f,69,79)):210;
  const rowTop=phase===2?358+12*e(f,69,79):370;
  const rowOpacity=phase===3?1-orbitProgress:1;
  const rowLift=phase===3?-12*orbitProgress:0;
  const badges=Array.from({length:count},(_,i)=>phase===3
   ? <div key={i} style={{width:92,height:92,marginLeft:i===0?0:-4,display:"grid",placeItems:"center",flex:"none"}}><div style={{transform:"scale(.88)"}}><ProviderBadge index={i} frame={f+i}/></div></div>
   : <ProviderBadge key={i} index={i} frame={f+i}/>);
  return <div style={{position:"absolute",left:"10%",right:"10%",top:rowTop,height:340,display:"flex",alignItems:"center",justifyContent:"space-between",gap:12,opacity:rowOpacity,transform:"translateY("+rowLift+"px)"}}>
   <Word size={textSize} color="#101113" weight={900} tracking={-.09}>Any</Word>
   <div style={{display:"flex",gap:phase===2?8:0,alignItems:"center",flex:"none"}}>{badges}</div>
   <Word size={textSize} color="#101113" weight={900} tracking={-.09}>agent.</Word>
  </div>;
 };
 const BadgeOrbit=()=>(
  <div style={{position:"absolute",inset:0,opacity:orbitProgress,pointerEvents:"none"}}>
   <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
    <ellipse cx="1195" cy="585" rx="238" ry="158" fill="none" stroke="rgba(255,255,255,.66)" strokeWidth="6" strokeDasharray="24 18" transform={"rotate(-14 1195 585)"}/>
    <ellipse cx="1195" cy="585" rx="204" ry="132" fill="none" stroke="rgba(255,255,255,.30)" strokeWidth="3" transform={"rotate(18 1195 585)"}/>
   </svg>
   {Array.from({length:11},(_,i)=>{
    const angle=(i/11)*Math.PI*2+(f-109)*.075;
    const x=1195+Math.cos(angle)*230;
    const y=585+Math.sin(angle)*153;
    const depth=.72+.34*((Math.sin(angle)+1)/2);
    const rotation=Math.sin(angle)*11;
    return <div key={i} style={{position:"absolute",left:x,top:y,width:104,height:104,marginLeft:-52,marginTop:-52,transform:"scale("+depth+") rotate("+rotation+"deg)",zIndex:Math.round(depth*100),filter:"drop-shadow(0 18px 22px rgba(28,44,43,.16))"}}>
     <ProviderBadge index={i} frame={f+i*2}/>
    </div>;
   })}
  </div>
 );
 const fade=1-e(f,125,129);
 return <AbsoluteFill style={{...full,background:"#f1ece5"}}>
  <div style={{position:"absolute",inset:0,opacity:fade}}>
   <Sequence from={0} durationInFrames={19}><AbsoluteFill style={{...full,background:"#87bfdc"}}/></Sequence>
   <Sequence from={19} durationInFrames={20}><AbsoluteFill style={{...full,background:"#e3a97e"}}/></Sequence>
   <Sequence from={39} durationInFrames={10}><AbsoluteFill style={{...full,background:"#8eb897"}}/></Sequence>
   <Sequence from={49} durationInFrames={15}><AbsoluteFill style={{...full,background:"#b5d0d3"}}/></Sequence>
   <Sequence from={64} durationInFrames={15}><AbsoluteFill style={{...full,background:"#87bfdc"}}/></Sequence>
   <Sequence from={79} durationInFrames={20}><AbsoluteFill style={{...full,background:"#e3a97e"}}/></Sequence>
   <Sequence from={99} durationInFrames={10}><AbsoluteFill style={{...full,background:"#8eb897"}}/></Sequence>
   <Sequence from={109} durationInFrames={20}><AbsoluteFill style={{...full,background:"#bad2d4"}}/></Sequence>
   <Sequence from={0} durationInFrames={4}><Phrase phase={0}/></Sequence>
   <Sequence from={4} durationInFrames={65}><Phrase phase={1}/></Sequence>
   <Sequence from={69} durationInFrames={30}><Phrase phase={2}/></Sequence>
   <Sequence from={99} durationInFrames={30}>
    <Phrase phase={3}/>
    <BadgeOrbit/>
   </Sequence>
  </div>
 </AbsoluteFill>;
};
const PreviewArtwork=({variant,frame}:{variant:number;frame:number})=>{
 if(variant===0)return <div style={{position:"absolute",inset:0,background:"#e8e1d2",overflow:"hidden"}}>
  <svg viewBox="0 0 1000 650" width="100%" height="100%">
   <defs>
    <linearGradient id="ink-mtn-sky-v30" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#eee8d9"/><stop offset=".6" stopColor="#e3dfd1"/><stop offset="1" stopColor="#c8c9c0"/></linearGradient>
    <filter id="ink-mtn-texture-v30"><feTurbulence type="fractalNoise" baseFrequency=".052" numOctaves="3" seed="4"/><feDisplacementMap in="SourceGraphic" scale="15"/></filter>
    <filter id="ink-mtn-soft-v30"><feGaussianBlur stdDeviation="12"/></filter>
   </defs>
   <rect width="1000" height="650" fill="url(#ink-mtn-sky-v30)"/>
   <g opacity=".7" filter="url(#ink-mtn-soft-v30)">
    <path d="M-80 390L110 236L210 318L342 142L455 310L590 178L710 317L850 145L1010 304V650H-80Z" fill="#9c9d96"/>
    <path d="M-50 470L130 332L260 418L384 264L520 425L650 292L802 438L925 310L1040 408V650H-50Z" fill="#777f7b" opacity=".75"/>
   </g>
   <g filter="url(#ink-mtn-texture-v30)" opacity=".74">
    <path d="M-50 390L105 244L210 318L338 151L454 312L583 190L709 322L853 155L1020 308V650H-50Z" fill="#b0afa5"/>
    <path d="M-50 471L125 336L260 420L384 270L520 430L650 299L803 442L925 318L1040 420V650H-50Z" fill="#828985"/>
    <path d="M-60 536L145 435L280 490L420 394L565 510L710 404L850 505L1005 430V650H-60Z" fill="#6e7b7b" opacity=".8"/>
   </g>
   <g transform={"translate(515 333) rotate("+(Math.sin(frame/22)*1.1)+")"}>
    <path d="M-185 -20A188 188 0 1 1 -165 100" fill="none" stroke="#161a1a" strokeWidth="48" strokeLinecap="round"/>
    <path d="M-148 -142A164 164 0 1 1 -126 93" fill="none" stroke="#f3ecdc" strokeWidth="10" strokeLinecap="round" opacity=".9"/>
    <path d="M-47 -123L135 2L-13 35L-41 147Z" fill="#121616"/>
   </g>
   <path d="M25 192q32 -31 66 -7q24 -19 45 3M110 223q24 -18 45 0M820 155q25 -24 52 1M864 190q22 -18 43 0" stroke="#313735" strokeWidth="7" fill="none" opacity=".7"/>
   <path d="M806 125q42 18 68 0l22 39q-42 38 -79 4Z" fill="#d6d0c0" opacity=".55"/>
   <rect x="804" y="472" width="78" height="94" fill="#b93d34"/><text x="843" y="535" textAnchor="middle" fontFamily="serif" fontSize="42" fill="#f9ead0">設</text>
   <g fill="none" stroke="#f9f5eb" strokeWidth="12" opacity=".22"><path d="M0 585q185 -28 360 10t350 -5t330 0"/><path d="M0 617q185 -26 360 8t350 -5t330 0"/></g>
  </svg>
 </div>;
 if(variant===1)return <div style={{position:"absolute",inset:0,background:"#e6d6ae",overflow:"hidden",color:"#151719"}}>
  <div style={{position:"absolute",inset:14,border:"7px solid #273e72",background:"#f6e9c9",boxShadow:"inset 0 0 0 5px #fff7e9"}}>
   <div style={{position:"absolute",left:24,top:20,fontFamily:"Georgia,serif",fontSize:22,fontWeight:800}}>THE MOTION CHRONICLE</div>
   <div style={{position:"absolute",right:25,top:18,fontSize:15,fontWeight:900,letterSpacing:".15em"}}>ISSUE 1962</div>
   <div style={{position:"absolute",left:28,top:83,width:220,bottom:35,fontFamily:"Georgia,serif",fontSize:17,lineHeight:1.3,color:"#353a39",overflow:"hidden"}}>The moving image becomes a new language. Forms collide, colour breaks open, and a simple symbol begins to travel through time.</div>
   <div style={{position:"absolute",right:28,top:75,width:690,height:500,border:"8px solid #243d7d",background:"#f6d04b",overflow:"hidden",boxShadow:"0 7px 0 #b18a43"}}>
    <div style={{position:"absolute",inset:-60,background:"repeating-conic-gradient(from 4deg at 50% 50%,#f9ebc8 0deg 2deg,#76a9d8 2deg 8deg)"}}/>
    <div style={{position:"absolute",left:"16%",top:"10%",width:"68%",height:"80%",borderRadius:"50%",background:"#f4d34b",border:"14px solid #151719",boxShadow:"0 0 0 10px #f8e9c4"}}>
     <div style={{position:"absolute",inset:"14%",borderRadius:"50%",background:"#da4137",border:"12px solid #111820",display:"grid",placeItems:"center"}}>
      <div style={{width:"78%",height:"78%",borderRadius:"50%",background:"#f7e8c4",border:"12px solid #3159a4",display:"grid",placeItems:"center"}}>
       <svg viewBox="0 0 100 120" width="100%" height="100%"><path d="M7 5L94 61L48 68L36 116Z" fill="#101214"/></svg>
      </div>
     </div>
    </div>
    <div style={{position:"absolute",left:24,top:17,background:"#f5d247",border:"4px solid #151719",padding:"8px 13px",fontSize:19,fontWeight:1000,transform:"rotate(-3deg)"}}>CLICK!</div>
   </div>
  </div>
 </div>;
 if(variant===2)return <div style={{position:"absolute",inset:0,background:"#82ee44",overflow:"hidden",color:"#090d08"}}>
  <div style={{position:"absolute",left:0,top:0,fontSize:18,fontWeight:900,letterSpacing:".18em",padding:"24px 28px"}}>OPEN DESIGN / MOTION</div>
  <div style={{position:"absolute",left:"-3%",right:"-3%",top:"27%",textAlign:"center",fontFamily:displayFont,fontSize:205,fontWeight:1000,letterSpacing:"-.105em",lineHeight:.9,color:"#050806"}}>OPEN<br/>DESIGN</div>
  <div style={{position:"absolute",left:30,bottom:25,fontSize:17,fontWeight:900,letterSpacing:".16em"}}>A NEW WAY TO CREATE</div>
  <div style={{position:"absolute",right:36,bottom:28,width:84,height:84,borderRadius:"50%",border:"7px solid #101914"}}/>
 </div>;
 if(variant===3)return <div style={{position:"absolute",inset:0,background:"#050607",overflow:"hidden"}}>
  <svg viewBox="0 0 1000 650" width="100%" height="100%">
   <defs><pattern id="squiggle-preview-v18" width="120" height="84" patternUnits="userSpaceOnUse"><path d="M-20 42C0 2 40 2 60 42S120 82 140 42" fill="none" stroke="#f3f3ed" strokeWidth="16" strokeLinecap="round"/></pattern></defs>
   <rect width="1000" height="650" fill="#050607"/><rect width="1000" height="650" fill="url(#squiggle-preview-v18)"/>
   <path d="M0 0H1000V650H0Z" fill="none" stroke="#fff" strokeWidth="8" opacity=".45"/>
  </svg>
 </div>;
 return <div style={{position:"absolute",inset:0,background:"#88f047",overflow:"hidden",color:"#090d08"}}>
  <div style={{position:"absolute",left:"-9%",right:"-9%",top:"24%",textAlign:"center",fontFamily:displayFont,fontSize:280,fontWeight:1000,letterSpacing:"-.15em",color:"#080d08",transform:"translateX("+(Math.sin(frame/4)*13)+"px)",textShadow:"0 5px 0 rgba(16,49,15,.2)"}}>EASE</div>
  <div style={{position:"absolute",left:26,top:20,fontSize:15,fontWeight:900,letterSpacing:".18em"}}>NATURAL MOTION / 05</div>
 </div>;
};

const CountdownPrism=({width="45%",height="76%",scale=1}:{width?:string;height?:string;scale?:number})=>(
 <svg viewBox="0 0 600 760" width={width} height={height} style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) scale("+scale+")",overflow:"visible"}}>
  <defs>
   <linearGradient id="countdown-prism-front-v29" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#263cf5"/><stop offset=".56" stopColor="#1626d5"/><stop offset="1" stopColor="#111fb5"/></linearGradient>
   <linearGradient id="countdown-prism-top-v29" x1="0" x2="1"><stop stopColor="#f0eaff"/><stop offset=".58" stopColor="#c1a8ff"/><stop offset="1" stopColor="#8c7df1"/></linearGradient>
   <linearGradient id="countdown-prism-side-v29" x1="0" x2="1"><stop stopColor="#6874d9"/><stop offset=".34" stopColor="#2533a8"/><stop offset="1" stopColor="#111958"/></linearGradient>
   <linearGradient id="countdown-prism-left-v29" x1="0" x2="1"><stop stopColor="#3549db"/><stop offset="1" stopColor="#101c7e"/></linearGradient>
  </defs>
  <path d="M80 185L330 105L510 105L510 690L285 690L285 315L80 370Z" transform="translate(26 -5)" fill="#080f6a" opacity=".84"/>
  <path d="M510 105L536 101L536 683L510 690Z" fill="url(#countdown-prism-side-v29)" stroke="#8d91f3" strokeWidth="4"/>
  <path d="M285 315L311 307L311 690L285 690Z" fill="url(#countdown-prism-left-v29)" opacity=".85"/>
  <path d="M80 185L330 105L510 105L536 101L353 138L95 220Z" fill="url(#countdown-prism-top-v29)" stroke="#9fa2ff" strokeWidth="3"/>
  <path d="M80 185L330 105L510 105L510 690L285 690L285 315L80 370Z" fill="url(#countdown-prism-front-v29)" stroke="#5367ec" strokeWidth="5"/>
  <path d="M80 185L330 105L330 135L95 220Z" fill="#f7f4ff"/>
  <path d="M330 105L510 105L510 138L330 138Z" fill="#987cf1"/>
  <path d="M506 112L506 682" stroke="#e5e6ff" strokeWidth="5" opacity=".75"/>
  <path d="M291 322L291 681" stroke="#6375ff" strokeWidth="3" opacity=".52"/>
  <path d="M84 189L84 367" stroke="#6377f5" strokeWidth="4" opacity=".8"/>
 </svg>
);

const CountdownArtwork = ({ value, frame }: { value: number; frame: number }) => {
 const p=pop(frame,30,0,75,14),scale=.88+.12*p;
 const isThree=value===3,isTwo=value===2,isOne=value===1;
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
  {isOne?<div style={{position:"absolute",right:0,bottom:0,width:"31%",height:"38%",background:"#1533ef",clipPath:"polygon(100% 0,100% 100%,0 100%)"}}/>:null}
  <svg viewBox="0 0 1000 650" width="100%" height="100%" style={{position:"absolute",inset:0,opacity:isThree?.52:.72}}>
   <ellipse cx="500" cy="325" rx="365" ry="255" fill="none" stroke={isThree?"#a4a6a5":isTwo?"#d9d9ff":"#dd874d"} strokeWidth="2"/>
   <ellipse cx="500" cy="325" rx="340" ry="225" fill="none" stroke={isThree?"#fff":isTwo?"#aab6ff":"#6678ff"} strokeWidth="1.7"/>
   {isThree?<path d="M0 325H1000" stroke="#a0a0a0" strokeWidth="1" opacity=".22"/>:null}
   {isOne?<path d="M150 290L830 470" stroke="#b9c5ff" strokeWidth="1" opacity=".48"/>:null}
  </svg>
  {isOne?<CountdownPrism width="42%" height="74%" scale={.98+.04*p}/>:<div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) perspective(1200px) scale("+scale+")",fontFamily:displayFont,fontSize:isThree?470:500,lineHeight:.78,fontWeight:1000,letterSpacing:"-.12em",color:numeralColor,textShadow:shadows}}>{value}</div>}
  <div style={{position:"absolute",left:34,top:"47%",fontFamily:"monospace",fontSize:14,fontWeight:900,letterSpacing:".12em",color:isThree?"#101214":isTwo?"#eff0ff":"#f3f3ff"}}>{isThree?"IGNITION SEQUENCE / 01":"IGNITION SEQUENCE / "+(isTwo?"02":"03")}</div>
  <div style={{position:"absolute",right:35,top:"48%",fontFamily:"monospace",fontSize:13,fontWeight:850,letterSpacing:".16em",color:isThree?"#222":isTwo?"#eee":"#fff",textAlign:"right"}}>SNARE ROLL / {isThree?"1":isTwo?"2":"3"}</div>
  <div style={{position:"absolute",right:35,bottom:35,display:"flex",gap:8}}>{[0,1,2].map(v=><div key={v} style={{width:24,height:6,background:v<=(isThree?0:isTwo?1:2)?"#fff":"rgba(255,255,255,.22)"}}/>)}</div>
  {!isThree&&!isTwo?<div style={{position:"absolute",left:45,top:32,fontSize:17,fontWeight:900,letterSpacing:".2em",color:"#fff"}}>GO</div>:null}
 </AbsoluteFill>;
};

const LaunchKitWindow=({frame,variant,countdown=-1}:{frame:number;variant:number;countdown?:number})=>{
 const handoff=e(frame,100,111),zoomExit=e(frame,100,106);
 const names=["Claude Opus 5.5","Claude Opus 5.5","Gemini","GLM","MiMo","DeepSeek V4.1","OpenDesign"];
 const name=names[variant%names.length];
 const symbols=["✣","✣","▶","Z","MiMo","🐳","◈"];
 const colors=["#df805b","#df805b","#151c30","#191919","#1d2328","#4879df","#293a92"];
 const shellLeft=118*(1-zoomExit);
 const shellRight=frame<106?118+265*zoomExit:0;
 const shellTop=72*(1-zoomExit),shellBottom=80*(1-zoomExit),headerHeight=54*(1-zoomExit),shellRadius=24*(1-zoomExit);
 const sidebarWidth=frame<106?586-86*zoomExit:frame<110?500-220*e(frame,106,110):280-84*e(frame,110,111);
 const paneRight=frame<106?285*(1-zoomExit):frame<110?109*e(frame,106,110):109+16*e(frame,110,111);
 const cardInset=frame<110?27:27*(1-e(frame,110,111));
 const cardTop=frame<106?89+39*zoomExit:frame<110?128-116*e(frame,106,110):12-12*e(frame,110,111);
 const cardBottom=frame<106?197:frame<110?197-197*e(frame,106,110):0;
 const bubbleLeft=frame<106?242-182*zoomExit:60;
 const bubbleTop=frame<106?45+27*zoomExit:72;
 const composerHeight=164+47*zoomExit,composerBottom=36+134*zoomExit;
 const previewLabelTop=44+36*zoomExit;
 return <AbsoluteFill style={{...full,background:"#f3f1ed"}}>
  <div style={{position:"absolute",left:shellLeft,right:shellRight,top:shellTop,bottom:shellBottom,borderRadius:shellRadius,background:"#fff",border:"1px solid #e9e8e3",boxShadow:"0 28px 78px rgba(30,35,38,.15)",overflow:"hidden"}}>
   <div style={{position:"absolute",top:0,left:0,right:0,height:headerHeight,borderBottom:"1px solid #efeee9",display:"flex",alignItems:"center",padding:"0 28px",gap:14,background:"#fff",opacity:1-zoomExit}}>{["#e5e5df","#e5e5df","#e5e5df"].map((c,i)=><div key={i} style={{width:15,height:15,borderRadius:"50%",background:c}}/>)}<div style={{marginLeft:14,fontSize:21,fontWeight:850,color:"#252a2d"}}>Launch film</div></div>
   <div style={{position:"absolute",top:headerHeight,bottom:0,left:0,width:sidebarWidth,background:"#fff",opacity:1-e(frame,106,111),overflow:"hidden"}}>
    <div style={{position:"absolute",left:bubbleLeft,top:bubbleTop,width:340+25*zoomExit,minHeight:96+16*zoomExit,background:"#f0efec",color:"#222629",borderRadius:"25px 25px 5px 25px",padding:"19px 24px",fontSize:25,lineHeight:1.42,boxSizing:"border-box"}}>Make a 10s launch film<br/>for our app.</div>
    <div style={{position:"absolute",left:18,right:18,bottom:composerBottom,height:composerHeight,border:"1px solid #e7e7e2",borderRadius:25,background:"#fff",padding:"19px 22px",boxSizing:"border-box",boxShadow:"0 3px 12px rgba(20,25,28,.04)"}}>
     <div style={{color:"#434a4c",fontSize:21}}>Make it feel like a launch.</div>
     <div style={{position:"absolute",left:18,bottom:18,display:"flex",alignItems:"center",gap:12}}>
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
   <div style={{position:"absolute",left:sidebarWidth,right:paneRight,top:headerHeight,bottom:0,background:"#f6f5f1",padding:0,boxSizing:"border-box",zIndex:4,overflow:"hidden"}}>
    <div style={{position:"absolute",left:27,top:previewLabelTop,fontSize:22,color:"#777f81",fontWeight:850,opacity:1-zoomExit}}>Preview</div>
    <div style={{position:"absolute",left:cardInset,right:cardInset,top:cardTop,bottom:cardBottom,background:"#050609",borderRadius:20+22*handoff,border:"1px solid #e9e8e2",overflow:"hidden",boxShadow:handoff?"0 0 0 rgba(0,0,0,0)":"0 1px 3px rgba(0,0,0,.04)"}}>
     {countdown>=0?<CountdownArtwork value={countdown} frame={frame}/>:<PreviewArtwork variant={variant} frame={frame}/>}
     {countdown<0?<div style={{position:"absolute",left:22,top:18,display:"flex",alignItems:"center",gap:10,background:"rgba(255,255,255,.96)",borderRadius:30,padding:"10px 17px",color:"#30383b",fontSize:20,fontWeight:800,boxShadow:"0 5px 16px rgba(0,0,0,.1)",opacity:1-zoomExit}}>
      <span style={{color:"#8a8f91",fontWeight:600}}>Made with</span><span style={{width:34,height:34,borderRadius:8,background:colors[variant%7],color:"#fff",display:"grid",placeItems:"center",fontSize:21}}>{symbols[variant%7]}</span>{name}
     </div>:null}
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
 const p=e(frame,0,8),rotate=e(frame,0,12,0,2);
 return <AbsoluteFill style={{...full,background:"#f2f0e9",color:"#f8f8f4",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"6.1%",right:"6.25%",top:0,bottom:0,borderRadius:42,background:"#050609",overflow:"hidden",boxShadow:"0 10px 45px rgba(0,0,0,.14)"}}>
   <div style={{position:"absolute",right:0,bottom:0,width:"28%",height:"38%",background:"#2238ee",clipPath:"polygon(100% 0,100% 100%,0 100%)"}}/>
   <svg viewBox="0 0 1668 1080" width="100%" height="100%" style={{position:"absolute",inset:0}}>
    <ellipse cx="834" cy="550" rx="530" ry="165" fill="none" stroke="#df884c" strokeWidth="3" opacity=".94" transform={"rotate("+rotate+" 834 550)"}/>
    <ellipse cx="834" cy="550" rx="478" ry="133" fill="none" stroke="#5a6dff" strokeWidth="3" opacity=".88" transform={"rotate("+(-rotate*.6)+" 834 550)"}/>
    <path d="M360 410L1420 710" stroke="#b9c5ff" strokeWidth="2" opacity=".42"/>
   </svg>
   <CountdownPrism width="34.5%" height="76%" scale={1.02+.025*p}/>
   <div style={{position:"absolute",left:-14,top:"39%",fontFamily:"monospace",fontSize:16,fontWeight:900,letterSpacing:".18em",color:"#aeb9ff"}}>IGNITION SEQUENCE / 01</div>
   <div style={{position:"absolute",left:-12,top:"45%",fontFamily:displayFont,fontSize:76,fontWeight:1000,letterSpacing:"-.08em",color:"#fff"}}>GO</div>
   <div style={{position:"absolute",left:-12,top:"55%",fontFamily:"monospace",fontSize:14,fontWeight:850,letterSpacing:".16em",color:"#b7c2ff"}}>03 · 3/3<br/>0.500</div>
   <div style={{position:"absolute",right:10,top:"39%",textAlign:"right",fontFamily:"monospace",fontSize:14,fontWeight:850,letterSpacing:".15em",color:"#c6cdff"}}>IGNITION SEQUENCE<br/>SNARE ROLL 3</div>
   <div style={{position:"absolute",right:10,top:"46%",display:"flex",gap:7}}>{[0,1,2].map(i=><div key={i} style={{width:37,height:7,background:"#f4f5ff"}}/>)}</div>
  </div>
 </AbsoluteFill>;
};

const LaunchKitSequence=()=>{
 // The Launch Film page starts at source frame 770; preserve the original
 // local countdown/keyframe map by subtracting the nine-frame pre-roll.
 const frame=useCurrentFrame()-10;
 if(frame>=112)return <CountdownOne frame={frame-112}/>;
 const variant=frame<15?0:frame<30?1:frame<45?2:frame<60?3:4;
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
 const style:React.CSSProperties={position:"absolute",inset:0,width:"100%",height:"100%",overflow:"hidden",borderRadius:48,border:"3px solid rgba(255,255,255,.82)",boxSizing:"border-box",backfaceVisibility:"hidden",transform,boxShadow:"inset 0 0 0 2px rgba(255,255,255,.2),inset 0 -26px 42px rgba(0,0,0,.18)"};
 const blackMark=<div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 28% 15%,#20242b,#050609 66%,#020304)",display:"grid",placeItems:"center"}}>
  <div style={{position:"absolute",inset:22,border:"3px solid rgba(255,255,255,.25)",borderRadius:34}}/>
  <svg id="cameraMark-v68" viewBox="0 0 360 360" width="100%" height="100%">
   <path d="M111 48C80 48 56 71 56 105V253C56 286 80 310 114 310H184C269 310 310 260 310 180C310 98 266 48 184 48Z" fill="#f7f7f2"/>
   <path d="M137 91C116 91 101 107 101 129V231C101 253 117 269 140 269H180C236 269 270 232 270 180C270 127 237 91 180 91Z" fill="#07090d"/>
   <path d="M147 119L239 176L163 197L146 250Z" fill="#f7f7f2" stroke="#d8e1e4" strokeWidth="3" strokeLinejoin="round"/>
   <path d="M147 119L180 165L163 197Z" fill="#b8c6cc"/>
  </svg>
 </div>;
 const portrait=<div style={{position:"absolute",inset:0,background:"linear-gradient(135deg,#e88d9e 0%,#f2c94f 22%,#f6d66c 72%,#d87f90 100%)"}}>
  <div style={{position:"absolute",inset:18,border:"8px solid #fff3df",borderRadius:34,boxShadow:"inset 0 0 0 3px rgba(86,53,31,.27)"}}/>
  <div style={{position:"absolute",left:22,top:19,fontFamily:displayFont,fontSize:20,fontWeight:950,color:"#352b2a",letterSpacing:".12em"}}>MORRO / 01</div>
  <div style={{position:"absolute",left:52,right:52,top:72,bottom:61,borderRadius:"45% 45% 35% 35%",background:"#fff2dc",border:"9px solid #fff",boxShadow:"0 9px 0 rgba(80,49,33,.18),inset 0 0 0 5px #d9b58b",display:"grid",placeItems:"center"}}>
   <svg viewBox="0 0 260 300" width="100%" height="100%">
    <defs><linearGradient id="camPortrait-v24" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#f0c49b"/><stop offset="1" stopColor="#c77f63"/></linearGradient></defs>
    <rect width="260" height="300" fill="#f6e8ce"/>
    <path d="M25 300Q30 213 86 188L175 187Q232 220 240 300Z" fill="#298b7b"/>
    <ellipse cx="132" cy="146" rx="83" ry="104" fill="url(#camPortrait-v24)"/>
    <path d="M48 133Q38 39 132 31Q228 37 218 134L184 94L144 81L93 100L63 153Z" fill="#40332f"/>
    <path d="M57 119Q78 68 125 77Q172 69 209 116L197 63Q158 10 105 26Q43 41 57 119Z" fill="#292726"/>
    <ellipse cx="102" cy="147" rx="8" ry="11" fill="#1b1c1d"/><ellipse cx="163" cy="147" rx="8" ry="11" fill="#1b1c1d"/>
    <ellipse cx="88" cy="183" rx="17" ry="10" fill="#e88b91" opacity=".7"/><ellipse cx="179" cy="183" rx="17" ry="10" fill="#e88b91" opacity=".7"/>
    <path d="M112 205Q135 221 157 203" stroke="#5c3932" strokeWidth="6" fill="none" strokeLinecap="round"/>
    <path d="M14 297Q16 262 52 240L86 228L112 300M246 297Q241 252 209 236L176 226L155 300" fill="#e4b98e" opacity=".9"/>
   </svg>
  </div>
  <div style={{position:"absolute",right:35,top:35,width:48,height:50,borderRadius:9,background:"#fff8e8",border:"5px solid #94734f",display:"grid",placeItems:"center"}}><div style={{width:25,height:25,borderRadius:6,background:"#15191a",display:"grid",placeItems:"center",color:"#fff",fontSize:17}}>◉</div></div>
  <div style={{position:"absolute",right:40,bottom:35,width:27,height:42,background:"#f6efe0",borderRadius:4}}><div style={{width:13,height:13,margin:"-7px auto",borderRadius:"50%",background:"#dd5d52"}}/></div>
  <div style={{position:"absolute",left:0,right:0,bottom:0,height:38,background:"#44327c"}}/>
 </div>;
 const clockBrushMarks=Array.from({length:260},(_,i)=>{
  const x=(i*137+19)%360,y=(i*83+41)%360,a=(i*47%360)*Math.PI/180,len=5+(i*11)%24;
  const palette=["#15377e","#2654a7","#527bc5","#8ca9dc","#0c286c","#d6a94e","#f2d27a"];
  return {x,y,x2:x+Math.cos(a)*len,y2:y+Math.sin(a)*len*.68,w:2+(i*7)%6,c:palette[i%palette.length],o:.2+(i%6)*.09};
 });
 const clockRingMarks=Array.from({length:144},(_,i)=>{
  const a=i*Math.PI*2/144,r=129+(i%5)*1.8,da=.025+(i%4)*.008;
  return {x1:180+Math.cos(a)*r,y1:172+Math.sin(a)*r,x2:180+Math.cos(a+da)*(r+2),y2:172+Math.sin(a+da)*(r+2),w:2+(i%5)*1.1,c:i%3===0?"#fff0a6":i%3===1?"#ad762f":"#e5c46d",o:.45+(i%4)*.1};
 });
 const clock=<div style={{position:"absolute",inset:0,overflow:"hidden",background:"#183a91"}}>
  <svg viewBox="0 0 360 360" width="100%" height="100%">
   <defs>
    <radialGradient id="cubeClock-v68" cx=".42" cy=".35"><stop stopColor="#315cb3"/><stop offset=".55" stopColor="#173985"/><stop offset="1" stopColor="#0b1d57"/></radialGradient>
    <radialGradient id="cubeClockGold-v68"><stop stopColor="#f8df91"/><stop offset=".72" stopColor="#d7ae54"/><stop offset="1" stopColor="#8c5b27"/></radialGradient>
    <filter id="cubeClockPaper-v68"><feTurbulence type="fractalNoise" baseFrequency=".075" numOctaves="3" seed="19"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .23"/></feComponentTransfer></filter>
   </defs>
   <rect width="360" height="360" fill="url(#cubeClock-v68)"/>
   <g opacity=".85">{clockBrushMarks.map((m,i)=><path key={"clock-brush-v68-"+i} d={"M"+m.x+" "+m.y+"L"+m.x2+" "+m.y2} stroke={m.c} strokeWidth={m.w} opacity={m.o} strokeLinecap="round"/>)}</g>
   <circle cx="180" cy="172" r="137" fill="url(#cubeClockGold-v68)" stroke="#f7df9b" strokeWidth="8"/>
   <circle cx="180" cy="172" r="119" fill="none" stroke="#9a682d" strokeWidth="13"/>
   <g>{clockRingMarks.map((m,i)=><path key={"clock-ring-v68-"+i} d={"M"+m.x1+" "+m.y1+"L"+m.x2+" "+m.y2} stroke={m.c} strokeWidth={m.w} opacity={m.o} strokeLinecap="round"/>)}</g>
   <circle cx="180" cy="172" r="105" fill="#080b16" stroke="#f0cd76" strokeWidth="14"/>
   <circle cx="180" cy="172" r="83" fill="#173879" stroke="#d9b15d" strokeWidth="7"/>
   <path d="M137 91L253 165L165 192L132 256Z" fill="#05070e"/>
   <path d="M137 91L183 159L165 192Z" fill="#f5d985"/>
   <path d="M144 107Q169 125 179 159M166 194L151 240" stroke="#ffe9a8" strokeWidth="4" fill="none" opacity=".8"/>
   <g fill="#ffe08b" opacity=".8">{[0,1,2,3,4,5,6,7].map(i=><circle key={i} cx={180+Math.cos(i*Math.PI/4)*151} cy={172+Math.sin(i*Math.PI/4)*151} r={i%2?3:5}/>)}</g>
   <text x="180" y="39" textAnchor="middle" fill="#ffdb72" fontSize="25" fontWeight="950" letterSpacing="4" stroke="#815323" strokeWidth="1.3" paintOrder="stroke">1889</text>
   <text x="180" y="60" textAnchor="middle" fill="#e8c76f" fontSize="8" fontWeight="900" letterSpacing="2">PAINTED TIME / MOTION</text>
   <rect width="360" height="360" filter="url(#cubeClockPaper-v68)" opacity=".34"/>
  </svg>
 </div>;
 const yellow=<div style={{position:"absolute",inset:0,background:"linear-gradient(180deg,#f7f8ed 0%,#e6f3e9 62%,#c8e7df 100%)",color:"#121916",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:14,border:"7px solid #e4bb54",borderRadius:20}}/>
  <div style={{position:"absolute",left:25,right:25,top:20,height:31,display:"flex",alignItems:"center",justifyContent:"space-between",fontFamily:"monospace",fontSize:14,fontWeight:950,letterSpacing:".12em",color:"#30291b"}}><span>100K</span><span>OPEN DESIGN</span></div>
  <svg viewBox="0 0 360 360" width="100%" height="100%" style={{position:"absolute",inset:0}}>
   <defs><pattern id="stars-grid-v57" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" stroke="#28734e" strokeWidth="1.2" opacity=".56"/><circle cx="8" cy="8" r="1.8" fill="#28734e" opacity=".55"/></pattern><linearGradient id="stars-wash-v68" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#a9e0d3" stopOpacity="0"/><stop offset=".55" stopColor="#9bd5ce" stopOpacity=".3"/><stop offset="1" stopColor="#7dc6bd" stopOpacity=".66"/></linearGradient></defs>
   <rect x="22" y="64" width="316" height="250" fill="url(#stars-grid-v57)" opacity=".78"/>
   <path d="M42 92H318V274H42Z" fill="none" stroke="#1d7147" strokeWidth="8" strokeDasharray="18 4"/>
   <path d="M0 260Q57 237 110 261T218 258T360 246V360H0Z" fill="url(#stars-wash-v68)"/>
   <path d="M-10 290Q62 268 122 289T250 285T380 278" fill="none" stroke="#f7fff0" strokeWidth="12" opacity=".66"/>
   <path d="M-10 314Q72 296 147 315T280 307T380 300" fill="none" stroke="#67b9ad" strokeWidth="9" opacity=".36"/>
  </svg>
  <div style={{position:"absolute",left:0,right:0,top:"29%",textAlign:"center",fontFamily:displayFont,fontSize:218,fontWeight:1000,letterSpacing:"-.12em",color:"#101713",textShadow:"3px 4px 0 #a7d6b9",transform:"scaleX(1.06)"}}>100K</div>
  <div style={{position:"absolute",left:0,right:0,top:"69%",textAlign:"center",fontSize:19,fontWeight:950,letterSpacing:".16em",color:"#194c35"}}>GitHub stars</div>
  <div style={{position:"absolute",left:0,right:0,bottom:18,textAlign:"center",fontFamily:"monospace",fontSize:12,fontWeight:950,letterSpacing:".2em",color:"#4b7963"}}>OPEN DESIGN / 100K</div>
 </div>;
 const blackSide=<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#07090d,#15171a 60%,#030405)",display:"grid",placeItems:"center"}}>
  <div style={{position:"absolute",inset:22,border:"3px solid rgba(255,255,255,.28)",borderRadius:36}}/>
  <svg viewBox="0 0 360 360" width="100%" height="100%"><path d="M180 48Q300 48 312 162Q322 274 208 308Q85 338 50 216Q16 93 131 54Z" fill="#fff"/><path d="M127 90L280 179L165 198L134 280Z" fill="#080a0d"/><path d="M127 90L180 164L165 198Z" fill="#d8dce0"/></svg>
 </div>;
 const nightCity=<div style={{position:"absolute",inset:0,overflow:"hidden",background:"linear-gradient(145deg,#173b91 0%,#244bb5 50%,#081d5b 100%)"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 42% 37%,rgba(111,158,235,.7),transparent 53%),repeating-linear-gradient(172deg,rgba(255,255,255,.13) 0 2px,transparent 2px 13px)"}}/>
  <svg viewBox="0 0 360 360" width="100%" height="100%">
   <g opacity=".45" fill="none" stroke="#8db6ef" strokeWidth="3">{Array.from({length:25},(_,i)=><path key={i} d={"M"+(i*19-35)+" "+(20+i%5*17)+"l"+(15+i%4*9)+" "+(i%2?17:-13)}/>)}</g>
   <circle cx="182" cy="154" r="108" fill="#102b75" stroke="#f4e8c9" strokeWidth="18"/>
   <circle cx="182" cy="154" r="91" fill="none" stroke="#d6c7a0" strokeWidth="5"/>
   <path d="M151 82L254 154L168 177L145 239Z" fill="#fff8e8"/><path d="M151 82L192 147L168 177Z" fill="#91b9ec"/>
   <g fill="#0b1e52"><path d="M0 286L0 226L32 226L32 244L63 244L63 207L91 207L91 286Z"/><path d="M263 286L263 224L290 224L290 195L319 195L319 237L360 237L360 286Z"/></g>
   <g fill="#ffdf77">{Array.from({length:25},(_,i)=><rect key={i} x={8+(i*29)%340} y={294+(i*17)%43} width="6" height="11" opacity={.65+(i%3)*.12}/>)}</g>
   <path d="M0 333Q66 312 124 333T242 332T360 327V360H0Z" fill="#0a194b"/>
  </svg>
  <div style={{position:"absolute",left:15,right:15,top:14,display:"flex",justifyContent:"space-between",fontFamily:"monospace",fontSize:12,fontWeight:950,letterSpacing:".13em",color:"#fff1c8"}}><span>BLUE HOUR</span><span>OPEN / 01</span></div>
 </div>;
 const glossyLogo=<div style={{position:"absolute",inset:0,overflow:"hidden",background:"radial-gradient(ellipse at 28% 16%,#2d3945,#06090d 62%,#020305)"}}>
  <div style={{position:"absolute",inset:20,border:"3px solid rgba(255,255,255,.18)",borderRadius:39}}/>
  <svg viewBox="0 0 360 360" width="100%" height="100%">
   <defs><linearGradient id="glossy-d-v57" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#ffdf55"/><stop offset=".3" stopColor="#9cf05d"/><stop offset=".62" stopColor="#65e7d1"/><stop offset="1" stopColor="#6aa7ff"/></linearGradient><filter id="glossy-glow-v57"><feGaussianBlur stdDeviation="10"/></filter></defs>
   <path d="M91 55Q55 55 55 97V266Q55 305 96 305H180Q307 305 307 180Q307 55 180 55Z" fill="none" stroke="#9cf05d" strokeWidth="30" opacity=".55" filter="url(#glossy-glow-v57)"/>
   <path d="M91 55Q55 55 55 97V266Q55 305 96 305H180Q307 305 307 180Q307 55 180 55Z" fill="none" stroke="url(#glossy-d-v57)" strokeWidth="24" strokeLinejoin="round"/>
   <path d="M124 101Q100 101 100 128V234Q100 256 128 256H178Q258 256 258 180Q258 101 178 101Z" fill="#070b11" stroke="rgba(255,255,255,.7)" strokeWidth="4"/>
   <path d="M151 130L226 180L151 230Z" fill="#f6f7f4"/><path d="M151 130L182 177L151 230Z" fill="#a4ed76"/>
  </svg>
  <div style={{position:"absolute",left:0,right:0,bottom:17,textAlign:"center",fontFamily:"monospace",fontSize:12,fontWeight:950,letterSpacing:".2em",color:"#cbd9d6"}}>OPEN DESIGN / PLAY</div>
 </div>;
 const topCream=<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#fffdf3,#d8e3ed 68%,#b9c7da)",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:18,border:"5px solid rgba(19,28,46,.7)",borderRadius:28}}/>
  <svg viewBox="0 0 360 360" width="100%" height="100%"><ellipse cx="180" cy="174" rx="105" ry="76" fill="#101720"/><ellipse cx="180" cy="174" rx="83" ry="58" fill="#f8f6ea" stroke="#c5d2df" strokeWidth="8"/><path d="M153 126L225 174L153 222Z" fill="#111924"/><path d="M153 126L181 169L153 222Z" fill="#7da3df"/><text x="180" y="298" fontSize="15" textAnchor="middle" fontWeight="900" letterSpacing="5" fill="#263449">MORRO / FORM</text></svg>
 </div>;
 const topBlue=<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#2c53ec,#132ba4 65%,#07153d)",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:15,border:"6px solid #f7f4e9",borderRadius:30}}/><svg viewBox="0 0 360 360" width="100%" height="100%"><circle cx="180" cy="173" r="105" fill="#f4f2e8" stroke="#9fb1f0" strokeWidth="8"/><circle cx="180" cy="173" r="80" fill="#101720"/><path d="M151 119L224 173L151 228Z" fill="#fff"/><path d="M151 119L181 166L151 228Z" fill="#7898eb"/></svg>
 </div>;
 const archiveFace=<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#f1cf73,#b57a2e 65%,#75451d)",overflow:"hidden",color:"#20160e"}}>
  <div style={{position:"absolute",inset:13,border:"5px solid #f7e5a4",borderRadius:22}}/>
  <div style={{position:"absolute",left:0,right:0,top:17,textAlign:"center",fontFamily:"Georgia,serif",fontSize:24,fontWeight:900,letterSpacing:".12em",textShadow:"0 1px 0 #ffe59a"}}>1889</div>
  <div style={{position:"absolute",left:"50%",top:"49%",width:236,height:236,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"radial-gradient(circle,#17130f 0 34%,#dcb35d 35% 40%,#17130f 41% 55%,#f5da8c 56% 64%,#9a6829 65% 72%,#f1d27a 73% 100%)",boxShadow:"0 0 0 9px rgba(255,239,187,.48),0 14px 24px rgba(56,30,10,.35),inset 0 0 20px rgba(42,21,7,.55)"}}>
   <svg id="archive-engrave-v68" viewBox="0 0 240 240" width="100%" height="100%">
    <g fill="none" stroke="#f1d48a" strokeWidth="3" opacity=".84"><circle cx="120" cy="120" r="105"/><circle cx="120" cy="120" r="88" strokeDasharray="4 7"/><circle cx="120" cy="120" r="72"/><path d="M120 14Q151 47 120 72Q89 47 120 14ZM226 120Q193 151 168 120Q193 89 226 120ZM120 226Q89 193 120 168Q151 193 120 226ZM14 120Q47 89 72 120Q47 151 14 120Z"/></g>
    <g fill="none" stroke="#bd8e42" strokeWidth="5" strokeLinecap="round"><path d="M48 76Q82 28 120 56T192 76M48 164Q82 212 120 184T192 164"/></g>
    <path d="M78 48L169 117L97 137L72 199Z" fill="#f1d78c" stroke="#2b1e10" strokeWidth="8" strokeLinejoin="round"/>
    <path d="M78 48L119 108L97 137Z" fill="#20160e"/>
   </svg>
  </div>
  <svg viewBox="0 0 360 360" width="100%" height="100%" style={{position:"absolute",inset:0,pointerEvents:"none",opacity:.18}}><defs><filter id="archive-paper-v68"><feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="3" seed="29"/><feColorMatrix type="saturate" values="0"/></filter></defs><rect width="360" height="360" filter="url(#archive-paper-v68)"/></svg>
  <div style={{position:"absolute",left:0,right:0,bottom:19,textAlign:"center",fontFamily:"monospace",fontSize:13,fontWeight:950,letterSpacing:".2em"}}>TIME / CULTURE / MOTION</div>
 </div>;
 const archive1923=<div style={{position:"absolute",inset:0,background:"linear-gradient(145deg,#fff8e8,#e8ddc3)",overflow:"hidden",color:"#1b1715"}}>
  <div style={{position:"absolute",inset:13,border:"5px solid #171717",borderRadius:20}}/>
  <div style={{position:"absolute",left:0,right:0,top:13,textAlign:"center",fontFamily:"Georgia,serif",fontSize:26,fontWeight:900,letterSpacing:".08em"}}>1923</div>
  <div style={{position:"absolute",left:"50%",top:"52%",width:225,height:225,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"radial-gradient(circle,#191817 0 42%,#d4493d 43% 57%,#f5ead6 58% 67%,#191817 68% 100%)",boxShadow:"0 5px 18px rgba(0,0,0,.28)"}}><div style={{position:"absolute",left:"50%",top:"50%",width:0,height:0,transform:"translate(-50%,-50%)",borderTop:"61px solid transparent",borderBottom:"61px solid transparent",borderLeft:"91px solid #f6ecdb"}}/></div>
  <div style={{position:"absolute",left:0,right:0,bottom:17,textAlign:"center",fontFamily:"monospace",fontSize:14,fontWeight:950,letterSpacing:".22em"}}>OPEN / DESIGN</div>
 </div>;
  const dynamicFront=frame<27?portrait:frame<55?nightCity:frame<72?archiveFace:archive1923;
 const dynamicSide=frame<27?blackSide:frame<42?glossyLogo:frame<55?clock:frame<72?yellow:archive1923;
 const topArtwork=frame<42?topCream:frame<55?blackSide:frame<72?blackSide:topBlue;
 return <div style={style}>
  {kind===0?dynamicFront:
   kind===1?(frame<42?glossyLogo:frame<55?clock:frame<72?archiveFace:archive1923):
   kind===2?dynamicSide:
   kind===3?topArtwork:
   kind===4?ease:
   (frame<55?nightCity:frame<72?archiveFace:blackMark)}
  <div style={{position:"absolute",inset:0,borderRadius:44,pointerEvents:"none",background:"linear-gradient(135deg,rgba(255,255,255,.28),transparent 28%,rgba(0,0,0,.18) 100%)"}}/>
 </div>;
};

const ProjectCube=({startAt=0}:{startAt?:number})=>{
 const f=Math.max(0,useCurrentFrame()-startAt);
 const rotateY=f<15?-90+128*e(f,0,15):f<30?38-83*e(f,15,30):f<45?-45-25*e(f,30,45):f<60?-70+230*e(f,45,60):160+50*e(f,60,75);
 const rotateX=f<15?18-14*e(f,0,15):f<30?4-26*e(f,15,30):f<45?-22+47*e(f,30,45):f<60?25-43*e(f,45,60):-18+10*e(f,60,75);
 const rotateZ=-4+2*Math.sin(f/18),scale=(.78+.22*e(f,0,18))*(1-.16*e(f,108,126)),size=560,z=size/2;
 return <AbsoluteFill style={{...full,background:"#f2f0e9",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 50% 82%,rgba(25,27,31,.17),transparent 43%)"}}/>
  <div style={{position:"absolute",left:"50%",top:"47%",width:size,height:size,perspective:1500,transform:"translate(-50%,-50%)"}}>
   <div style={{position:"absolute",inset:0,transformStyle:"preserve-3d",transform:"rotateX("+rotateX+"deg) rotateY("+rotateY+"deg) rotateZ("+rotateZ+"deg) scale("+scale+")"}}>
    <CubeFace kind={0} frame={f} transform={"translateZ("+z+"px)"}/>
    <CubeFace kind={1} frame={f} transform={"rotateY(90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={2} frame={f} transform={"rotateY(-90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={3} frame={f} transform={"rotateX(90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={4} frame={f} transform={"rotateX(-90deg) translateZ("+z+"px)"}/>
    <CubeFace kind={5} frame={f} transform={"rotateY(180deg) translateZ("+z+"px)"}/>
   </div>
  </div>
  <div style={{position:"absolute",left:"50%",top:"81%",width:690,height:105,transform:"translate(-50%,-50%)",borderRadius:"50%",background:"rgba(18,22,29,.17)",filter:"blur(42px)"}}/>
 </AbsoluteFill>;
};

const MorroCubeIntro=()=>{
 const f=useCurrentFrame();
 const typeOpacity=1-e(f,4,9),tile=e(f,3,8),blueTile=e(f,8,16),ribbon=e(f,10,17),tileFade=1-e(f,34,36);
 const size=1120-400*e(f,8,18);
 const rows=[-112,178,468,758];
 return <AbsoluteFill style={{...full,background:"#f2f0e8",overflow:"hidden"}}>
  <div style={{position:"absolute",inset:0,opacity:typeOpacity,overflow:"hidden"}}>
   {rows.map((y,i)=><div key={i} style={{position:"absolute",left:-110,right:-110,top:y,height:290,display:"flex",alignItems:"center",width:"max-content",transform:"translateX("+(-f*7+(i%2?80:-20))+"px)",gap:14}}>
    {Array.from({length:5},(_,k)=><Word key={k} size={i%2===0?286:276} color={i%2===0?"#090a0c":"#f2f0e8"} weight={1000} tracking={-.13} style={i%2===0?{}:{WebkitTextStroke:"3px #151719",color:"transparent"}}>MORRO</Word>)}
   </div>)}
   <div style={{position:"absolute",right:90,top:118,width:290,borderTop:"1px solid #a9a8a0",borderBottom:"1px solid #a9a8a0",padding:"12px 0",fontFamily:"monospace",fontSize:15,fontWeight:900,letterSpacing:".14em",color:"#313438",lineHeight:1.8}}>SPEC / PRISM<br/>MATERIAL<br/>IOR<br/>ROUGH<br/>ROT/S</div>
  </div>
  <div style={{position:"absolute",left:"50%",top:"49%",width:520,height:410,transform:"translate(-50%,-50%) perspective(1000px) rotateY(-15deg) rotateX(9deg) scale("+(0.72+.28*e(f,0,8))+")",opacity:e(f,0,1)*(1-e(f,7,10)),transformStyle:"preserve-3d",pointerEvents:"none"}}>
   <div style={{position:"absolute",left:95,top:8,width:300,height:190,clipPath:"polygon(18% 0,100% 0,84% 100%,0 100%)",background:"linear-gradient(135deg,#f4f3eb,#bfc8c7 55%,#8b9998)",border:"4px solid rgba(58,72,71,.45)",transform:"translateZ(30px)",boxShadow:"18px 10px 0 rgba(40,50,52,.13)"}}/>
   <div style={{position:"absolute",left:60,top:160,width:360,height:190,clipPath:"polygon(0 0,100% 0,78% 100%,17% 100%)",background:"linear-gradient(145deg,#eceee8,#bac4c1 50%,#6d7c7a)",border:"4px solid rgba(58,72,71,.4)",transform:"translateZ(80px)",boxShadow:"12px 16px 0 rgba(40,50,52,.17)"}}/>
   <div style={{position:"absolute",left:177,top:78,width:145,height:260,clipPath:"polygon(50% 0,100% 18%,84% 100%,16% 100%,0 18%)",background:"linear-gradient(90deg,#c3ccca,#f4f2e9 45%,#798987)",transform:"translateZ(120px) rotate(7deg)",border:"4px solid rgba(54,66,65,.3)"}}/>
  </div>
  <div style={{position:"absolute",left:"50%",top:"50%",width:size,height:size,transform:"translate(-50%,-50%) scale("+(0.98+.02*tile)+")",opacity:tile*tileFade,borderRadius:58,overflow:"hidden",background:"#f4f1e9",boxShadow:"0 30px 80px rgba(30,26,48,.15)"}}>
   <div style={{position:"absolute",inset:0,opacity:1-blueTile,background:"#f5f2e9",overflow:"hidden"}}>
    <div style={{position:"absolute",left:-90,top:-30,fontFamily:displayFont,fontSize:310,fontWeight:1000,letterSpacing:"-.14em",color:"#111315",whiteSpace:"nowrap"}}>MORRO</div>
    <div style={{position:"absolute",left:-160,top:205,fontFamily:displayFont,fontSize:306,fontWeight:1000,letterSpacing:"-.14em",color:"transparent",WebkitTextStroke:"5px #22262a",whiteSpace:"nowrap"}}>MORRO</div>
    <div style={{position:"absolute",left:-15,top:465,fontFamily:displayFont,fontSize:310,fontWeight:1000,letterSpacing:"-.14em",color:"#171a1e",whiteSpace:"nowrap"}}>MORRO</div>
    <div style={{position:"absolute",left:"43%",top:0,bottom:0,width:"57%",background:"rgba(235,231,221,.72)"}}/>
   </div>
   <div style={{position:"absolute",inset:0,opacity:blueTile,background:"#f3f1e8",overflow:"hidden"}}>
    <div style={{position:"absolute",inset:0,background:"#f3f1e8"}}/>
    <div style={{position:"absolute",left:-140,top:-115,fontFamily:displayFont,fontSize:420,fontWeight:1000,letterSpacing:"-.16em",color:"#2439e9",whiteSpace:"nowrap"}}>MORRO</div>
    <div style={{position:"absolute",left:-100,top:250,fontFamily:displayFont,fontSize:400,fontWeight:1000,letterSpacing:"-.16em",color:"#2439e9",whiteSpace:"nowrap"}}>MORRO</div>
    <div style={{position:"absolute",left:30,bottom:-150,fontFamily:displayFont,fontSize:390,fontWeight:1000,letterSpacing:"-.16em",color:"#2439e9",whiteSpace:"nowrap"}}>MORRO</div>
   </div>
   <svg viewBox="0 0 1120 1120" width="100%" height="100%" style={{position:"absolute",inset:0,opacity:ribbon}}>
    <defs>
     <linearGradient id="morro-ribbon-a-v31" x1="0" x2="1" y1="0" y2="0"><stop stopColor="#9668bc"/><stop offset=".24" stopColor="#d8b4eb"/><stop offset=".53" stopColor="#f3d7ff"/><stop offset=".78" stopColor="#c38cda"/><stop offset="1" stopColor="#7950a7"/></linearGradient>
     <linearGradient id="morro-ribbon-b-v31" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#efcffa"/><stop offset=".45" stopColor="#c995e3"/><stop offset=".8" stopColor="#9966c4"/><stop offset="1" stopColor="#71469e"/></linearGradient>
    </defs>
    <path d="M390 -55L635 -55L380 1175L124 1175Z" fill="#61438f" opacity=".35" transform="translate(24 16)"/>
    <path d="M390 -55L635 -55L380 1175L124 1175Z" fill="url(#morro-ribbon-a-v31)" stroke="#e4c7f3" strokeWidth="7"/>
    <path d="M635 -55L671 -55L416 1175L380 1175Z" fill="#744d9d" opacity=".74"/>
    <path d="M765 205L1015 105L735 1095L480 1095Z" fill="url(#morro-ribbon-b-v31)" stroke="#f0d6fa" strokeWidth="7"/>
    <path d="M765 205L1015 105L1015 165L793 255Z" fill="#f5ddff"/>
    <path d="M480 1095L735 1095L678 1175L416 1175Z" fill="#8053ac"/>
    <path d="M585 450L736 390L654 720L502 780Z" fill="#b17bd1" stroke="#e5c5f4" strokeWidth="6"/>
    <path d="M600 470L725 418" stroke="#fff1ff" strokeWidth="11" opacity=".7"/>
   </svg>
  </div>
  <div style={{position:"absolute",left:0,right:0,bottom:0,textAlign:"center",fontFamily:displayFont,fontSize:15,fontWeight:900,letterSpacing:".22em",color:"#d9d4f5",opacity:.45*(1-tileFade)}}>MORRO / FORM STUDY</div>
 </AbsoluteFill>;
};

const TexturedCube=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,12,4);
 if(f<12)return <AbsoluteFill style={{...full,background:"#f2f0e9",overflow:"hidden"}}>
  <div style={{position:"absolute",left:"50%",top:"49%",width:520,height:520,transform:"translate(-50%,-50%) scale("+(0.92+.08*p)+")",borderRadius:76,overflow:"hidden",background:"linear-gradient(145deg,#284fee 0%,#1936bf 35%,#07131e 67%,#03070d 100%)",boxShadow:"0 18px 0 #5d45ae,0 29px 0 #a68bd8,0 44px 42px rgba(24,20,82,.22)"}}>
   <div style={{position:"absolute",inset:0,background:"radial-gradient(ellipse at 22% 9%,rgba(255,255,255,.82),transparent 31%),linear-gradient(120deg,rgba(75,141,255,.5),transparent 34%,rgba(3,8,13,.74) 70%,rgba(255,255,255,.2) 100%)"}}/>
   <div style={{position:"absolute",left:"-8%",right:"-12%",top:"-10%",height:"48%",background:"linear-gradient(135deg,rgba(255,255,255,.36),rgba(73,126,255,.12) 46%,transparent 70%)",transform:"skewY(-12deg)",filter:"blur(12px)"}}/>
   <svg viewBox="0 0 520 520" width="100%" height="100%" style={{position:"absolute",inset:0}}>
    <defs><linearGradient id="glossy-play-ring-v29" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#fff"/><stop offset=".5" stopColor="#dce3ef"/><stop offset="1" stopColor="#8b9dbb"/></linearGradient><filter id="glossy-soft-v29"><feGaussianBlur stdDeviation="8"/></filter></defs>
    <path d="M85 82Q54 112 54 161V343Q54 418 129 418H324Q433 418 433 309V213Q433 90 309 82Z" fill="rgba(238,246,255,.17)" stroke="#f4f7ff" strokeWidth="15"/>
    <circle cx="264" cy="250" r="112" fill="rgba(4,10,20,.46)" stroke="url(#glossy-play-ring-v29)" strokeWidth="17"/>
    <circle cx="264" cy="250" r="91" fill="none" stroke="rgba(255,255,255,.56)" strokeWidth="3"/>
    <path d="M227 171L352 248L231 332Z" fill="#08121d" stroke="#f5f7ff" strokeWidth="10" strokeLinejoin="round"/>
    <path d="M102 108Q180 70 255 103" fill="none" stroke="#fff" strokeWidth="13" opacity=".68" strokeLinecap="round" filter="url(#glossy-soft-v29)"/>
    <path d="M77 357Q190 405 353 375" fill="none" stroke="#68b8ff" strokeWidth="7" opacity=".45"/>
   </svg>
   <div style={{position:"absolute",inset:0,background:"linear-gradient(140deg,transparent 20%,rgba(255,255,255,.12) 46%,transparent 68%)"}}/>
  </div>
 </AbsoluteFill>;
 return <ProjectCube startAt={12}/>;
};

const FinalLockup=()=>{
 const f=useCurrentFrame(),p=pop(f,30,0,78,18),fade=e(f,0,12),urlFade=e(f,58,66);
 return <AbsoluteFill style={{...full,background:"#f5f4ed"}}>
  <div style={{position:"absolute",left:0,right:0,top:164,display:"flex",flexDirection:"column",alignItems:"center",transform:"translateY("+((1-p)*18)+"px) scale("+(0.96+.04*p)+")",opacity:fade}}>
   <div style={{width:270,height:270,display:"grid",placeItems:"center"}}>
    <svg viewBox="0 0 240 240" width="270" height="270">
     <circle cx="120" cy="120" r="91" fill="none" stroke="#8bcfe2" strokeWidth="8"/>
     <path d="M91 25Q112 0 130 25M145 27L161 10M157 43L180 30" fill="none" stroke="#e8a38e" strokeWidth="9" strokeLinecap="round"/>
     <rect x="67" y="61" width="105" height="111" rx="22" fill="#111315"/>
     <circle cx="119" cy="115" r="34" fill="none" stroke="#f5f5ef" strokeWidth="8"/>
     <circle cx="119" cy="115" r="21" fill="#f5f5ef"/>
     <circle cx="150" cy="79" r="7" fill="#e8a38e"/>
    </svg>
   </div>
   <div style={{marginTop:36,fontFamily:displayFont,fontSize:116,fontWeight:950,color:"#14191b",letterSpacing:"-.075em"}}>OpenDesign Motion</div>
   <div style={{marginTop:42,background:"#10313a",color:"#e7f3f2",borderRadius:26,padding:"13px 39px",fontSize:32,fontWeight:850,letterSpacing:".005em",opacity:urlFade}}><span style={{color:"#a0dcaa"}}>●</span> open-design.ai</div>
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
    <Sequence from={641} durationInFrames={128}><ModelAgentScene /></Sequence>
    <Sequence from={769} durationInFrames={128}><LaunchKitSequence /></Sequence>
    <Sequence from={897} durationInFrames={36}><MorroCubeIntro /></Sequence>
    <Sequence from={933} durationInFrames={117}><TexturedCube /></Sequence>
    <Sequence from={1050} durationInFrames={69}><FinalLockup /></Sequence>
    <Audio src={staticFile("audio/opendesign-motion-score.wav")} volume={0.92} />
  </AbsoluteFill>
);