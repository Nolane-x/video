import { E, registerTemplate, clamp, lerp, ease, rng, alpha, noise, glow, circle, seg, poly, linGrad } from '/engine/core.js';
import { bg, prop, drawThing, camera, overlays, flag, castle, cloud, CAST } from '/packs/squire/pack.js';

const W=()=>E.W, H=()=>E.H;
const BLUE='#536b83', RED='#9c493c', GOLD='#d1ad68', STONE='#b9a98c', INK='#241f20';

// Period-specific visual presets for this film; Squire's stock Greek/Roman and Norman kits
// are not used as stand-ins for 15th-century Byzantine or Ottoman soldiers.
Object.assign(CAST, {
  // A recurring fictional defender: one silhouette, costume and shield across the film.
  byzantineYou: {
    ...CAST.knight15, helmet:'bascinet', visor:'up', body:'mail', arms:'mail', legs:'mail',
    tunicColor:'#536b83', tabard:false, tabardColor:'#536b83', cape:'#30455a',
    weapon:'spear', shield:{type:'round',color:'#536b83',charge:'eagle',chargeColor:'#d1ad68'}
  },
  byzantineGuard: {
    ...CAST.knight14, helmet:'bascinet', visor:'up', body:'mail', arms:'mail', legs:'mail',
    tunicColor:'#536b83', tabard:false, tabardColor:'#425a73', cape:'#30455a',
    shield:{type:'round',color:'#536b83',charge:'eagle',chargeColor:'#d1ad68'}, weapon:'spear'
  },
  byzantineArcher: {
    ...CAST.crossbowman, helmet:'coif', body:'gambeson', tunicColor:'#536b83',
    tabard:false, legs:'cloth', legColor:'#495466', weapon:'crossbow', shield:null, scarf:'#8495a2'
  },
  ottomanInfantry: {
    ...CAST.peasant, helmet:'turban', body:'mail', tunicColor:'#8e4739',
    skirt:.55, legs:'mail', weapon:'spear', shield:{type:'round',color:'#725743'},
    scarf:'#c5a36f', beard:'stubble'
  },
  ottomanArcher: {
    ...CAST.englishArcher, helmet:'turban', body:'gambeson', tunicColor:'#8e4739',
    tabard:false, legs:'cloth', legColor:'#49342f', weapon:'bow', shield:null, scarf:'#c5a36f'
  },
  ottomanElite: {
    ...CAST.knight13, helmet:'turban', body:'mail', tunicColor:'#873e33',
    tabard:true, tabardColor:'#c4a36c', legs:'mail', weapon:'sword',
    shield:{type:'round',color:'#765744',charge:'circle',chargeColor:'#d1ad68'}
  },
  ottomanCommander: {
    ...CAST.king, helmet:'turban', hair:'short', hairColor:'#302522', beard:'full',
    body:'robe', tunicColor:'#873e33', cape:'#512b27', legs:'cloth',
    legColor:'#382d2b', shield:null, weapon:'sword', crownOn:false, charge:null
  }
});

function path(g,pts,fill,stroke=INK,lw=5){
  g.beginPath(); g.moveTo(pts[0][0],pts[0][1]); for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);
  g.closePath(); if(fill){g.fillStyle=fill;g.fill();} if(stroke){g.lineWidth=lw;g.strokeStyle=stroke;g.stroke();}
}
function line(g,pts,color=INK,lw=4,alphaV=1){
  g.save();g.globalAlpha*=alphaV;g.beginPath();g.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++)g.lineTo(pts[i][0],pts[i][1]);g.strokeStyle=color;g.lineWidth=lw;g.lineCap='round';g.lineJoin='round';g.stroke();g.restore();
}
function gradient(g,y0,y1,stops){
  const gr=g.createLinearGradient(0,y0,0,y1);stops.forEach(([p,c])=>gr.addColorStop(p,c));g.fillStyle=gr;g.fillRect(0,0,W(),H());
}

function stateAt(info, lt, list, fallback) {
  let value = fallback;
  for (const pair of list || []) if (lt >= Number(pair[0])) value = pair[1];
  return value;
}
function drawCinematicActor(g, lt, info, p, gy=.93, dh=.5, distant=false) {
  const x = p.x === undefined ? .5*W() : (p.x <= 1.5 ? p.x*W() : p.x);
  const y = p.y === undefined ? gy*H() : (p.y <= 1.5 ? p.y*H() : p.y);
  const h = p.h === undefined ? dh*H() : (p.h <= 1.5 ? p.h*H() : p.h);
  if (h < 9 || h > H()*1.2) return;
  const preset = String(p.preset || "byzantineGuard").toLowerCase();
  const ottoman = preset.includes("ottoman");
  const civilian = ["peasant","monk","lady"].some(k => preset.includes(k));
  const monk = preset.includes("monk");
  const woman = preset.includes("lady");
  const blue = "#40566c", blueLight = "#7e929e", red = "#87463c";
  const tunic = ottoman ? (preset.includes("elite") ? "#744037" : "#8b5141")
               : civilian ? (monk ? "#574a3c" : woman ? "#887260" : "#65704d") : blue;
  const cloth = ottoman ? "#c2a77d" : civilian ? "#b69a78" : "#303f52";
  const steel = "#8c9695", steelLight = "#c0c3b7", leather = "#44352c";
  const scale = h/680, detail = !distant && h > 130;
  const pose = stateAt(info, lt, p.poseAt, p.pose || "guard");
  const seed = Number(p.seed || 0) + (Number(p.x)||0)*13;
  const flip = p.flip ? -1 : 1;
  const gait = p.walk ? Math.sin(lt*6.4*(p.speed||1)+seed) : Math.sin(lt*2.0+seed)*.06;
  const bob = p.walk ? Math.abs(Math.sin(lt*6.4*(p.speed||1)+seed))*h*.006 : Math.sin(lt*2+seed)*h*.002;
  let shX=-.16, shY=-.48, rhX=.18, rhY=-.47;
  if (pose==="point" || pose==="pointUp") { rhX=.36; rhY=pose==="pointUp"?-.78:-.59; }
  if (pose==="thrust") { rhX=.40; rhY=-.62; shX=-.22; }
  if (pose==="brace") { rhX=.26; rhY=-.44; shX=-.25; shY=-.43; }
  if (pose==="push") { rhX=.34; rhY=-.48; shX=-.28; shY=-.48; }
  if (pose==="carry") { rhX=.24; rhY=-.25; shX=-.24; shY=-.3; }
  if (pose==="kneel") { shY=-.34; rhY=-.35; }
  if (pose==="run") { rhX=.25+gait*.16; rhY=-.56; shX=-.22-gait*.12; shY=-.4; }
  const stride=p.walk?gait*h*.038:0;
  const hipY=pose==="kneel"?-h*.31:-h*.36;
  g.save();
  g.translate(x,y+bob); g.scale(flip,1);
  g.fillStyle="rgba(18,20,22,.26)";
  g.beginPath(); g.ellipse(0,-h*.012,h*.17,h*.022,0,0,Math.PI*2); g.fill();
  // Cloak: a separate silhouette with less visual weight than the torso.
  if(!civilian) path(g,[[-h*.085,-h*.72],[-h*.22,-h*.55],[-h*.17,-h*.26],[-h*.03,-h*.34],[h*.07,-h*.30],[h*.19,-h*.61],[h*.12,-h*.74]],cloth,INK,Math.max(1,h*.006));
  else path(g,[[-h*.10,-h*.70],[-h*.18,-h*.50],[-h*.22,-h*.04],[h*.22,-h*.04],[h*.18,-h*.50],[h*.10,-h*.70]],tunic,INK,Math.max(1,h*.006));
  // Adult leg-to-body ratio and grounded boots.
  const legCol=civilian?tunic:(ottoman?"#51463c":steel);
  line(g,[[-h*.065,hipY],[-h*.105-stride,-h*.025]],legCol,Math.max(2,h*.066));
  line(g,[[h*.065,hipY],[h*.105+stride,-h*.025]],legCol,Math.max(2,h*.066));
  line(g,[[-h*.105-stride,-h*.025],[-h*.16-stride,-h*.018]],leather,Math.max(2,h*.075));
  line(g,[[h*.105+stride,-h*.025],[h*.16+stride,-h*.018]],leather,Math.max(2,h*.075));
  // Body is roughly 3.5 heads tall, not the giant-head Squire silhouette.
  path(g,[[-h*.12,-h*.69],[h*.12,-h*.69],[h*.145,-h*.49],[h*.09,-h*.34],[-h*.09,-h*.34],[-h*.145,-h*.49]],tunic,INK,Math.max(2,h*.009));
  if(!civilian) {
    path(g,[[-h*.105,-h*.66],[h*.105,-h*.66],[h*.085,-h*.43],[-h*.085,-h*.43]],steel,INK,Math.max(1,h*.005));
    if(detail) {
      for(let r=0;r<4;r++) line(g,[[-h*.075,-h*(.63-r*.047)],[h*.075,-h*(.63-r*.047)]],"#515b5d",Math.max(1,h*.003),.8);
      line(g,[[-h*.10,-h*.5],[h*.10,-h*.5]],steelLight,Math.max(1,h*.004),.65);
      line(g,[[-h*.08,-h*.64],[h*.07,-h*.45]],"#d0c8b2",Math.max(1,h*.003),.48);
    }
    g.fillStyle="#aa8a54"; g.fillRect(-h*.095,-h*.375,h*.19,h*.026);
    g.fillStyle=leather; g.fillRect(-h*.018,-h*.40,h*.036,h*.055);
    g.fillStyle=steelLight; g.strokeStyle=INK; g.lineWidth=Math.max(1,h*.006);
    g.beginPath();g.ellipse(-h*.135,-h*.65,h*.075,h*.065,-.2,0,Math.PI*2);g.fill();g.stroke();
    g.beginPath();g.ellipse(h*.135,-h*.65,h*.075,h*.065,.2,0,Math.PI*2);g.fill();g.stroke();
  } else {
    line(g,[[-h*.09,-h*.58],[h*.09,-h*.58]],"#cfb995",Math.max(1,h*.006));
    if(monk){g.fillStyle="#3d332b";g.fillRect(-h*.13,-h*.72,h*.26,h*.05);}
  }
  // Arms respond to authored action beats.
  const leftElbow=[shX*h,-h*.53], leftHand=[shX*h*1.25,shY*h];
  const rightElbow=[h*.22,-h*.54], rightHand=[rhX*h,rhY*h];
  line(g,[[-h*.13,-h*.64],leftElbow],civilian?tunic:steel,Math.max(3,h*.075));
  line(g,[leftElbow,leftHand],civilian?tunic:steelLight,Math.max(3,h*.063));
  line(g,[[h*.13,-h*.64],rightElbow],civilian?tunic:steel,Math.max(3,h*.075));
  line(g,[rightElbow,rightHand],civilian?tunic:steelLight,Math.max(3,h*.063));
  circle(g,leftHand[0],leftHand[1],Math.max(3,h*.035),civilian?"#b98f70":"#9b9c91");
  circle(g,rightHand[0],rightHand[1],Math.max(3,h*.035),civilian?"#b98f70":"#9b9c91");
  // Small head: helmet, Ottoman wrapped turban or civilian hood.
  const headY=-h*.79, hr=h*.078;
  g.fillStyle=ottoman?"#9b755f":"#b88d70";g.strokeStyle=INK;g.lineWidth=Math.max(1,h*.006);
  g.beginPath();g.ellipse(0,headY,hr*.77,hr,0,0,Math.PI*2);g.fill();g.stroke();
  if(!civilian && !ottoman) {
    g.fillStyle=steel;g.beginPath();g.moveTo(-hr*.92,headY-hr*.1);g.quadraticCurveTo(-hr*.9,headY-hr*1.35,0,headY-hr*1.48);g.quadraticCurveTo(hr*.95,headY-hr*1.25,hr*.9,headY-hr*.08);g.lineTo(hr*.4,headY-hr*.02);g.lineTo(-hr*.55,headY-hr*.02);g.closePath();g.fill();g.stroke();
    g.strokeStyle=steelLight;g.lineWidth=Math.max(1,h*.004);g.beginPath();g.moveTo(-hr*.78,headY-hr*.45);g.lineTo(hr*.72,headY-hr*.45);g.stroke();
    g.fillStyle="#252b30";g.fillRect(-hr*.45,headY-hr*.08,hr*.9,hr*.09);
  } else if(ottoman) {
    g.fillStyle="#ddc79e";g.beginPath();g.ellipse(0,headY-hr*.52,hr*1.05,hr*.64,0,Math.PI,Math.PI*2);g.fill();g.stroke();
    line(g,[[-hr*.8,headY-hr*.42],[hr*.8,headY-hr*.42]],"#8a6852",Math.max(1,h*.004));
  } else {
    g.fillStyle=monk?"#41382e":(woman?"#9a866f":"#806d56");g.beginPath();g.arc(0,headY,hr*1.1,Math.PI,Math.PI*2);g.lineTo(hr*1.1,headY+hr*.55);g.lineTo(-hr*1.1,headY+hr*.55);g.closePath();g.fill();g.stroke();
  }
  if(detail) {
    line(g,[[-hr*.28,headY+hr*.08],[-hr*.08,headY+hr*.08]],"#2b2825",Math.max(1,h*.005));
    line(g,[[hr*.08,headY+hr*.08],[hr*.28,headY+hr*.08]],"#2b2825",Math.max(1,h*.005));
    if(ottoman) line(g,[[0,headY+hr*.25],[0,headY+hr*.48]],"#52392f",Math.max(1,h*.009));
  }
  const shieldCfg=p.shield===undefined?!civilian:!!p.shield;
  if(shieldCfg && !civilian && !distant) {
    const sx=-h*.205, sy=-h*.47, sr=h*.14, sc=p.shield?.color||(ottoman?"#725744":blue);
    g.fillStyle=sc;g.strokeStyle="#292b2c";g.lineWidth=Math.max(2,h*.012);
    g.beginPath();g.ellipse(sx,sy,sr*.78,sr,0,0,Math.PI*2);g.fill();g.stroke();
    g.strokeStyle="#c7a96a";g.lineWidth=Math.max(1,h*.007);g.beginPath();g.ellipse(sx,sy,sr*.68,sr*.88,0,0,Math.PI*2);g.stroke();
    if(detail && !ottoman) {
      line(g,[[sx-sr*.42,sy],[sx-sr*.05,sy-sr*.22],[sx,sy-sr*.05],[sx+sr*.42,sy-sr*.24]],"#d3b66f",Math.max(1,h*.008));
      line(g,[[sx-sr*.05,sy-sr*.22],[sx-sr*.26,sy+sr*.25],[sx,sy+sr*.2],[sx+sr*.28,sy+sr*.28]],"#d3b66f",Math.max(1,h*.008));
    }
  }
  const weapon=p.weapon===undefined?(preset.includes("archer")?"bow":civilian?null:"spear"):p.weapon;
  const wx=rightHand[0],wy=rightHand[1];
  if(weapon==="spear"||weapon==="lance") {
    line(g,[[wx,wy+h*.02],[wx+h*.035,wy-h*.56]],"#654a32",Math.max(2,h*.012));
    path(g,[[wx+h*.035,wy-h*.56],[wx-h*.005,wy-h*.63],[wx+h*.075,wy-h*.58]],steelLight,INK,Math.max(1,h*.004));
  } else if(weapon==="sword"||weapon==="pollaxe") {
    line(g,[[wx,wy],[wx+h*.06,wy-h*.29]],steelLight,Math.max(2,h*.015));
    line(g,[[wx-h*.055,wy-h*.045],[wx+h*.08,wy-h*.07]],"#9e8257",Math.max(2,h*.012));
    line(g,[[wx+h*.06,wy-h*.29],[wx+h*.08,wy-h*.36]],"#f0dfad",Math.max(1,h*.008));
  } else if(weapon==="bow") {
    g.beginPath();g.moveTo(wx,wy-h*.22);g.quadraticCurveTo(wx+h*.15,wy-h*.07,wx,wy+h*.02);g.strokeStyle="#59422d";g.lineWidth=Math.max(2,h*.014);g.stroke();
    line(g,[[wx,wy-h*.22],[wx,wy+h*.02]],"#d7c4a0",Math.max(1,h*.004));
  } else if(weapon==="torch") {
    line(g,[[wx,wy],[wx,wy-h*.27]],"#65472d",Math.max(2,h*.018));glow(g,wx,wy-h*.31,h*.13,"#ef9c46",.5);
  } else if(weapon==="pickaxe"||weapon==="shovel") {
    line(g,[[wx-h*.04,wy+h*.03],[wx+h*.08,wy-h*.2]],"#61452f",Math.max(2,h*.018));
    line(g,[[wx-h*.01,wy-h*.18],[wx+h*.14,wy-h*.21]],steelLight,Math.max(2,h*.015));
  }
  if(!distant) line(g,[[-h*.10,-h*.65],[-h*.07,-h*.44]],blueLight,Math.max(1,h*.004),.55);
  g.restore();
}
function drawPeople(g, lt, info, actors, gy=.93, dh=.5) {
  for (let i=0;i<(actors||[]).length;i++) {
    const actor={...actors[i],seed:actors[i].seed ?? i*17};
    drawCinematicActor(g,lt,info,actor,gy,dh,false);
  }
}
function formation(g, o={}) {
  const rows=Math.max(1,o.rows||1), cols=Math.max(1,o.cols||1);
  const x0=o.x0??0, x1=o.x1??1, yf=o.yFront??.88, yb=o.yBack??.65;
  const hf=o.hFront??.14, hb=o.hBack??.07, seed=Number(o.seed||0);
  for(let r=0;r<rows;r++) {
    const q=rows===1?.5:r/(rows-1), yy=lerp(yf,yb,q), hh=lerp(hf,hb,q);
    for(let c=0;c<cols;c++) {
      const u=cols===1?.5:c/(cols-1);
      const jitter=Math.sin(seed+r*23+c*11)*.004;
      const preset=o.presets ? o.presets[(r*cols+c)%o.presets.length] : o.preset;
      drawCinematicActor(g,o.t||0,{dur:6,start:0,args:{}},{
        preset, x:clamp(x0+(x1-x0)*u+jitter,0,1), y:yy+Math.sin(c*1.7+r)*.002,
        h:hh, face:o.face, pose:"guard", flip:!!o.flip,
        weapon:preset&&String(preset).toLowerCase().includes("archer")?"bow":"spear",
        walk:(o.march||0)>.05, speed:.45+(c%4)*.08, seed:seed+r*cols+c
      },.94,.4,true);
    }
  }
}

function drawSea(g,t,y=760){
  gradient(g,y,H(),[[0,'#476a79'],[.45,'#254958'],[1,'#142d3a']]);
  for(let j=0;j<28;j++){
    const yy=y+((j*29)%300), speed=.45+(j%5)*.19;
    const x=((t*120*speed+j*173)%(W()+320))-160;
    const len=35+(j%7)*27;
    line(g,[[x,yy],[x+len*.35,yy-2*Math.sin(t*2+j)],[x+len,yy+Math.sin(t*1.6+j)*2]],j%4?'#8ba8a8':'#c0c4ad',1.5+(j%3)*.5,.18+(j%4)*.04);
  }
}
function tower(g,x,base,s=1,damage=0){
  g.save();g.translate(x,base);g.scale(s,s);
  path(g,[[-60,0],[-60,-250],[-46,-277],[46,-277],[60,-250],[60,0]],'#9a8c79','#403b38',7);
  g.fillStyle='#796c60';g.fillRect(-61,-250,122,24);
  for(let k=-2;k<=2;k++)g.fillRect(k*22-7,-282,14,36);
  for(let y=-210;y<-20;y+=30) for(let k=-1;k<=1;k++){g.fillStyle='#322f31';g.fillRect(k*35-5,y,10,22);}
  if(damage>0){
    path(g,[[-60,-140],[-32,-154],[-8,-142],[14,-170],[34,-158],[60,-178],[60,-90],[25,-96],[0,-74],[-25,-96],[-60,-80]],null,'#302b2a',7);
  }
  g.restore();
}
function drawCity(g,t,{damage=0,water=true,chain=false}={}){
  gradient(g,0,H(),[[0,'#8ba0ad'],[.35,'#d8c3a3'],[.67,'#9b896e'],[1,'#51483e']]);
  // distant hills and city haze
  path(g,[[0,560],[0,420],[170,360],[310,410],[470,335],[620,390],[780,340],[950,385],[1150,330],[1340,392],[1510,345],[1720,390],[1920,330],[1920,700],[0,700]],'#69786d',null,0);
  // Byzantine roofs and houses
  for(let i=0;i<28;i++){
    const x=i*72-25, y=500+(i%4)*13, s=.6+(i%5)*.12;
    g.save();g.translate(x,y);g.scale(s,s);
    g.fillStyle=['#aa9276','#897966','#bd9c78','#766c60'][i%4];g.fillRect(-28,-115,56,115);
    path(g,[[-35,-112],[0,-158],[35,-112]],['#8e6254','#74645a','#a26e5e'][i%3],null,0);
    for(let k=-1;k<=1;k++)g.fillRect(k*15-4,-80+(i%3)*5,8,17);
    g.restore();
  }
  // Hagia Sophia-inspired great dome, without claiming exact architectural reconstruction
  g.fillStyle='#b7a78f';g.fillRect(690,445,470,160);
  g.beginPath();g.ellipse(920,442,190,96,0,Math.PI,Math.PI*2);g.fill();g.strokeStyle='#49423a';g.lineWidth=6;g.stroke();
  for(let k=0;k<4;k++){const x=750+k*120;g.fillStyle='#8e7c69';g.fillRect(x,395,24,95);g.beginPath();g.arc(x+12,395,12,Math.PI,0);g.fill();}
  // outer walls, towers, battlements
  const wallY=700;
  g.fillStyle='#9d8e7a';g.fillRect(0,wallY-115,W(),140);g.strokeStyle='#403a35';g.lineWidth=7;g.strokeRect(0,wallY-115,W(),140);
  for(let x=0;x<W();x+=42){g.fillStyle='#b8a88e';g.fillRect(x,wallY-144,27,29);g.fillStyle='#645a4f';g.fillRect(x+5,wallY-136,7,16);}
  for(let x=55;x<W();x+=185)tower(g,x,wallY,1.02,damage>0&&x>900&&x<1300?damage:0);
  // distant banners
  for(let i=0;i<9;i++)flag(g,80+i*220,wallY-165,100,{color:i%2?BLUE:'#9d433c',t,style:'plain',lw:2});
  if(water){drawSea(g,t,wallY+30);if(chain){
    g.save();g.strokeStyle='#292c2b';g.lineWidth=18;g.beginPath();g.moveTo(90,840);
    for(let i=1;i<=36;i++){const x=90+i*49,y=840-130*Math.sin(Math.PI*i/36);g.lineTo(x,y);}g.stroke();
    g.strokeStyle='#b0a28b';g.lineWidth=5;g.stroke();g.restore();
  }}
}
function ship(g,x,y,s,t,{sail='#e4d4b7',banner=RED,heading=1,fire=false}={}){
  g.save();g.translate(x,y);g.scale(s*heading,s);
  path(g,[[-185,-12],[-155,28],[105,35],[176,2],[128,45],[-120,52],[-185,-12]],'#493b35','#211f20',7);
  g.fillStyle='#96724f';g.fillRect(-105,-34,210,25);
  // deck rails and oar ports
  for(let i=-5;i<=5;i++){line(g,[[i*26,-32],[i*26,-1]],'#d5c0a1',3);}
  for(let i=0;i<13;i++){
    const ox=-154+i*25, ang=Math.sin(t*5+i*.7)*.25;
    line(g,[[ox,-8],[ox+Math.cos(ang)*65,-90+Math.sin(ang)*22]],'#4a3329',5);
  }
  line(g,[[0,-28],[0,-330]],'#413329',10);
  path(g,[[-2,-315],[3,-66],[120,-70],[78,-240],[6,-315]],sail,'#53483e',4);
  path(g,[[-5,-292],[-90,-90],[-8,-70]],'#d7c9ac','#53483e',4);
  // crew silhouettes
  for(let i=0;i<9;i++){const xx=-95+i*23;circle(g,xx,-42+Math.sin(t*4+i)*2,8,'#262625');line(g,[[xx,-34],[xx,-4]],'#282526',5);}
  line(g,[[0,-330],[0,-388]],'#3e332b',5);path(g,[[-2,-385],[34,-370],[-2,-352]],banner,null,0);
  if(fire){glow(g,65,-38,105,'#f29b45',.48);for(let i=0;i<9;i++){const u=(t*1.8+i*.13)%1;circle(g,25+Math.sin(i*2)*35,-45-u*145,5+u*9,alpha(i%2?'#e8bd6e':'#d95a36',1-u));}}
  g.restore();
}
function dust(g,t,x,y,seed=4,count=36,color='#d5b58d'){
  const r=rng(seed);
  for(let i=0;i<count;i++){const a=r()*Math.PI*2,sp=18+r()*130,life=(t*.45+r())%1,xx=x+Math.cos(a)*sp*life,yy=y+Math.sin(a)*sp*life-30*life;
    circle(g,xx,yy,2+r()*9,alpha(color,(1-life)*.38));}
}
function smoke(g,t,x,y,seed=9){
  const r=rng(seed);
  for(let i=0;i<24;i++){const p=(t*.22+i/24)%1,xx=x+Math.sin(t*.7+i*1.9)*48*p+(r()-.5)*12,yy=y-p*310;
    circle(g,xx,yy,12+p*53,alpha('#5a5350',(1-p)*.24));}
}
function cannon(g,x,y,s,t,fired){
  g.save();g.translate(x,y);g.scale(s,s);
  // heavy timber carriage
  path(g,[[-110,30],[-95,-40],[78,-48],[127,29],[75,50],[-78,48]],'#6e4931','#2b2420',8);
  for(const xx of [-65,78]){circle(g,xx,35,34,'#42332a');circle(g,xx,35,19,'#b18a59');circle(g,xx,35,6,'#302a27');}
  // barrel and trunnions
  g.save();g.translate(-4,-75-(fired&&t>.55&&t<.78?12*Math.sin((t-.55)*Math.PI/0.23):0));g.rotate(-.11);
  path(g,[[-30,-4],[-20,-86],[26,-86],[38,-4]],'#41413d','#221f1e',8);
  g.fillStyle='#8c8a7d';g.fillRect(-25,-90,58,15);g.fillStyle='#191b1b';g.beginPath();g.ellipse(4,-89,22,6,0,0,Math.PI*2);g.fill();
  g.restore();
  line(g,[[-15,-113],[-15,-94]],'#b99a6a',8);
  if(fired&&t>.55&&t<1.18){const q=(t-.55)/.63;glow(g,15,-150,90+q*90,'#ffb44c',.55*(1-q));path(g,[[8,-130],[-18,-200],[25,-183],[60,-220],[50,-148]],alpha('#fff0c2',1-q),null,0);}
  g.restore();
}
function drawLadder(g,x,y,h,t,phase=0){
  const sway=Math.sin(t*2+phase)*8;
  line(g,[[x-25+sway,y],[x-4+sway,y-h]],'#563d2a',12);
  line(g,[[x+25+sway,y],[x+4+sway,y-h]],'#563d2a',12);
  for(let k=0;k<9;k++){const yy=y-h+k*h/9;line(g,[[x-18+sway*(1-k/9),yy],[x+18+sway*(1-k/9),yy]],'#94724f',6);}
}
function drawCityInterior(g,t){
  gradient(g,0,H(),[[0,'#263344'],[.5,'#81756b'],[1,'#3e302a']]);
  // narrow street perspective
  path(g,[[0,440],[540,400],[780,1080],[0,1080]],'#67594b',null,0);
  path(g,[[1920,370],[1340,390],[1120,1080],[1920,1080]],'#51473f',null,0);
  for(let i=0;i<11;i++){
    const x=i*185-30, ht=200+(i%4)*70;
    g.fillStyle=['#a78d72','#716a60','#897865'][i%3];g.fillRect(x,410-ht*.4,170,ht);
    path(g,[[x-10,410-ht*.4],[x+85,360-ht*.4],[x+180,410-ht*.4]],'#705349',null,0);
    for(let k=0;k<3;k++){g.fillStyle='#302c2c';g.fillRect(x+22+k*45,445-ht*.4,18,36);}
  }
  // people crossing through the street
  drawPeople(g,t,{dur:6,globalT:t,start:0,args:{}},[
    {preset:'peasant',x:.20,y:.92,h:.32,face:'worried',pose:'run',walk:true,dir:1,speed:1.4},
    {preset:'byzantineGuard',x:.48,y:.91,h:.38,face:'worried',pose:'run',walk:true,dir:-1,speed:1.1,flip:true},
    {preset:'peasant',x:.74,y:.93,h:.31,face:'worried',pose:'walk',walk:true,dir:1,speed:.8}
  ],.93,.3);
  // smoke and warm windows
  for(let i=0;i<5;i++){const x=180+i*380,y=385-(i%2)*100;glow(g,x,y,115,'#f49b48',.16);g.fillStyle='#e0ae63';g.fillRect(x-12,y-20,24,40);}
  smoke(g,t,1460,430,30);smoke(g,t,520,420,21);
}
function drawCamp(g,t){
  gradient(g,0,H(),[[0,'#161d2a'],[.48,'#39414a'],[1,'#524539']]);
  for(let i=0;i<12;i++){const x=i*170-40;path(g,[[x,620],[x+42,510-(i%3)*22],[x+190,620]],i%2?'#7d6550':'#8e7559','#302922',4);line(g,[[x+115,620],[x+115,525]],'#3c3026',5);}
  for(let i=0;i<7;i++){glow(g,120+i*270,600,110,'#e59a4b',.21);}
  // map table and commander entourage
  g.fillStyle='#493a2f';g.fillRect(600,680,730,30);g.fillRect(670,710,28,210);g.fillRect(1235,710,28,210);
  g.fillStyle='#c4ad83';g.fillRect(635,625,660,55);line(g,[[660,654],[1270,654]],'#6d593e',3);
  for(let i=0;i<6;i++)circle(g,690+i*108,650,6,'#8b543f');
  drawPeople(g,t,{dur:6,globalT:t,start:0,args:{}},[
    {preset:'ottomanCommander',x:.47,y:.85,h:.52,face:'determined',pose:'guard'},
    {preset:'ottomanElite',x:.66,y:.86,h:.43,face:'neutral',pose:'point'},
    {preset:'ottomanElite',x:.33,y:.86,h:.40,face:'neutral',pose:'guard'}
  ],.93,.5);
}
function wallBase(g,t,breach=0){
  gradient(g,0,H(),[[0,'#56697a'],[.45,'#c7b08a'],[1,'#69533d']]);
  path(g,[[0,650],[0,500],[220,445],[430,490],[670,420],[900,460],[1160,400],[1390,470],[1640,425],[1920,460],[1920,800],[0,800]],'#777b6b',null,0);
  // broad curtain wall
  g.fillStyle='#a99a82';g.fillRect(1080,470,840,350);
  g.strokeStyle='#453d37';g.lineWidth=9;g.strokeRect(1080,470,840,350);
  for(let x=1080;x<1920;x+=42)for(let y=490;y<810;y+=35){g.strokeStyle=alpha('#51473c',.6);g.lineWidth=2;g.strokeRect(x+((y/35)%2)*14,y,38,30);}
  for(let x=1120;x<1920;x+=200)tower(g,x,470,1.0,breach);
  for(let x=1090;x<1920;x+=50){g.fillStyle='#bcae95';g.fillRect(x,430,30,40);}
  // damaged parapet / breach
  if(breach>0){
    g.save();g.globalAlpha=clamp(breach);path(g,[[1410,470],[1430,515],[1470,500],[1505,550],[1540,500],[1590,525],[1620,470]],'#493f36',null,0);
    for(let i=0;i<25;i++){const x=1450+(i*47)%210,y=530+(i*31)%230;path(g,[[x,y],[x+18,y-12],[x+27,y+3],[x+9,y+15]],i%2?'#b7a28a':'#786957',null,0);}
    g.restore();
  }
  // firing position and rough ground
  for(let i=0;i<45;i++){const x=(i*173)%W(),y=820+(i*29)%200;circle(g,x,y,3+(i%4),alpha('#473e32',.35));}
}
function arrowStorm(g,t,seed=7){
  const r=rng(seed);
  for(let i=0;i<70;i++){
    const phase=(t*1.3+i*.071)%1;
    if(phase<.12)continue;
    const x=1900-phase*2100+(r()-.5)*90, y=240+((i*83)%490)-phase*95;
    line(g,[[x,y],[x-30,y+8]],'#211e1b',2.5,.82);
  }
}
function cityPanorama(g,t,a){
  const variant=Math.abs(Number(a.variant)||0)%4;
  drawCity(g,t,{damage:a.damage??(variant===2?0.28:0.08),water:true,chain:!!a.chain||variant===3});
  if(variant===1){for(let i=0;i<3;i++){const x=((t*75+i*650+220)%(W()+500))-180;ship(g,x,785+i*46,.48+i*.05,t,{sail:'#d8ccb1',banner:i%2?RED:BLUE});}}
  if(variant===2){smoke(g,t,1290,420,71);smoke(g,t,1610,440,72);arrowStorm(g,t,73);}
  if(variant===3){glow(g,930,600,250,'#d6a76a',.18);dust(g,t,1100,710,93,28,'#d4bc95');}
  // near foreground parapet and watch post
  g.fillStyle='#7e6d58';g.fillRect(0,850,W(),230);
  for(let x=0;x<W();x+=85){g.fillStyle='#b29e7e';g.fillRect(x,820,55,65);}
  const ri=a.info||{dur:6,globalT:t,start:0,args:{}};
  if(a.fall){
    drawHero(g,t,ri,{x:.27,y:.97,h:.56,face:'tired',pose:'walk',walk:true,speed:.2,
      weapon:null,shield:null,poseAt:[[0,'walk'],[1.25,'carry'],[2.8,'walk']]});
    drawPeople(g,t,ri,[
      {preset:'ottomanElite',x:.78,y:.92,h:.45,face:'determined',pose:'guard',flip:true},
      {preset:'peasant',x:.61,y:.96,h:.38,face:'worried',pose:'run',walk:true,dir:1,speed:.42}
    ],.93,.4);
  } else {
    drawHero(g,t,ri,{x:.27,y:.87,h:.56,face:'determined',pose:'guard',
      poseAt:[[0,'guard'],[1.35,'point'],[2.9,'guard']]});
    drawPeople(g,t,ri,[{preset:'byzantineGuard',x:.76,y:.88,h:.43,face:'worried',pose:'guard',flip:true}],.93,.4);
  }
  if(a.chain){line(g,[[250,950],[600,895],[960,910],[1280,860],[1620,900]],'#28292a',12);for(let i=0;i<24;i++)circle(g,260+i*58,940-Math.sin(i/23*Math.PI)*55,7,'#5d5c56');}
  overlays(g,t,{...a.info,dur:6,args:a});
}
registerTemplate('city_panorama',{draw(g,lt,info){camera(g,lt,info,()=>cityPanorama(g,lt,{...info.args,info}));}});
registerTemplate('command_camp',{draw(g,lt,info){camera(g,lt,info,()=>{drawCamp(g,lt);for(let i=0;i<8;i++)flag(g,80+i*250,620,140,{color:i%2?RED:BLUE,t:lt,lw:2});dust(g,lt,1200,870,88,40);});}});
registerTemplate('city_interior',{draw(g,lt,info){camera(g,lt,info,()=>{drawCityInterior(g,lt);drawHero(g,lt,info,{x:.3,y:.98,h:.6,face:'tired',pose:'walk',walk:true,speed:.22,weapon:null,shield:null,poseAt:[[0,'walk'],[1.0,'carry'],[1.8,'walk']]});});}});
registerTemplate('wall_battery',{draw(g,lt,info){
  const a=info.args||{},fireAt=a.fireAt??.52,age=lt-fireAt,impact=fireAt+1.02;
  camera(g,lt,info,()=>{
    wallBase(g,lt,lt>impact?clamp((lt-impact)/.35):0);
    // two defensive formations in depth
    formation(g,{preset:'byzantineGuard',rows:3,cols:17,x0:.56,x1:.99,yFront:.78,yBack:.61,hFront:.18,hBack:.075,face:'determined',seed:71,t:lt,flip:true});
    cannon(g,330,870,1.5,age+.55,age>=0);
    const batteryActors=[
      {preset:'byzantineYou',x:.18,y:.96,h:.57,face:'determined',pose:'run',walk:true,dir:1,speed:.65,
        poseAt:[[0,'run'],[.72,'brace'],[1.45,'guard']],faceAt:[[0,'determined'],[.78,'worried'],[1.45,'determined']]},
      {preset:'byzantineGuard',x:.32,y:.94,h:.36,face:'worried',pose:'guard'},
      {preset:'byzantineGuard',x:.49,y:.93,h:.42,face:'worried',pose:'run',walk:true,dir:1,speed:.4}
    ];
    if(a.hero===false) batteryActors.shift();
    drawPeople(g,lt,info,batteryActors,.93,.42);
    if(age>0&&age<1.05){const q=clamp(age/1.05),bx=470+q*910,by=705-210*Math.sin(q*Math.PI);
      circle(g,bx,by,16+q*2,'#1b1a19');if(age>.72)glow(g,1430,580,210,'#e7b56d',.35);}
    if(age>=1.02){dust(g,lt-impact,1500,550,102,75,'#d6c1a0');smoke(g,lt-impact,1490,540,11);}
    if(age>.02&&age<.42){glow(g,470,645,170,'#ffb34d',.75);path(g,[[425,675],[385,520],[485,570],[530,450],[525,660]],'#fff0bc',null,0);}
    arrowStorm(g,lt,51);
    if(age>1.02)line(g,[[1440,560],[1488,604],[1533,574],[1570,628]],'#2b2623',10);
  });
}});
registerTemplate('relief_galleys',{draw(g,lt,info){
  const a=info.args||{};
  camera(g,lt,info,()=>{
    gradient(g,0,H(),[[0,'#8c9a9d'],[.45,'#496d80'],[1,'#183b50']]);
    // distant city coastline
    path(g,[[0,460],[230,420],[420,445],[610,385],[820,440],[1070,390],[1270,435],[1490,390],[1720,440],[1920,400],[1920,620],[0,620]],'#6d746b',null,0);
    for(let i=0;i<7;i++){const x=i*300+50;g.fillStyle='#8c8271';g.fillRect(x,420,90,105);path(g,[[x-10,422],[x+45,360],[x+100,422]],'#756052',null,0);}
    drawSea(g,lt,520);
    // four relief ships; each has its own drift and roll
    for(let i=0;i<4;i++){
      const x=((lt*(98+i*7)+i*510-350)%(W()+650))-180;
      g.save();g.translate(0,Math.sin(lt*1.6+i)*9);ship(g,x,790+i%2*70,.7+(i%3)*.08,lt,{sail:i===3?'#e8e0c9':'#d3c6a8',banner:i%2?BLUE:'#a3463d',heading:1});g.restore();
    }
    // interceptor on far right, closing fast
    const ix=1650-lt*105;ship(g,ix,700,.72,lt,{sail:'#ad9276',banner:RED,heading:-1});
    for(let i=0;i<24;i++){const x=1000+i*39,y=500+Math.sin(lt*4+i)*80;line(g,[[x,y],[x-40,y+13]],'#282524',3,.65);}
    if(lt>1.1){for(let i=0;i<7;i++)dust(g,lt-1.1,1260+i*35,720,20+i,12,'#b8d4d4');}
    drawHero(g,lt,info,{x:.18,y:.98,h:.57,face:'worried',pose:'point',poseAt:[[0,'point'],[.7,'guard'],[1.45,'pointUp']],faceAt:[[0,'worried'],[1.2,'determined']]});
    if(a.label){g.fillStyle='rgba(15,29,38,.65)';g.fillRect(65,65,620,92);g.fillStyle='#fff4de';g.font='800 44px sans-serif';g.fillText(a.label,100,126);}
  });
}});
registerTemplate('ship_portage',{draw(g,lt,info){
  camera(g,lt,info,()=>{
    gradient(g,0,H(),[[0,'#93a4a4'],[.42,'#b8af91'],[1,'#66563f']]);
    // sloping land between two bodies of water
    drawSea(g,lt,840);
    path(g,[[0,870],[0,700],[260,600],[530,560],[760,490],[1010,540],[1290,620],[1580,680],[1920,700],[1920,1080],[0,1080]],'#8b795b',null,0);
    path(g,[[0,910],[0,850],[300,760],[580,725],[920,670],[1300,740],[1650,790],[1920,810],[1920,1080],[0,1080]],'#a38b66',null,0);
    // log rollers
    for(let i=0;i<27;i++){const x=250+i*56,y=838-Math.sin(i/27*Math.PI)*178;line(g,[[x-26,y+12],[x+24,y-8]],'#503c2c',12);line(g,[[x-25,y+8],[x+23,y-12]],'#b88f5d',3);}
    // large galley moving over the hill on rollers
    const x=320+lt*72, y=630-Math.sin(clamp(lt/4)*Math.PI)*108;
    ship(g,x,y,1.08,lt,{sail:'#d8ccb1',banner:RED,heading:1});
    // ropes under load and hauling crews
    for(let i=0;i<6;i++){const hx=90+i*110,hy=830+(i%2)*36;line(g,[[hx,hy],[x-105, y-20+i*8]],'#44372b',4);circle(g,hx,hy,5,'#302923');}
    formation(g,{preset:'ottomanInfantry',rows:3,cols:13,x0:.02,x1:.42,yFront:.98,yBack:.82,hFront:.16,hBack:.08,face:'determined',march:.55,seed:21,t:lt});
    drawPeople(g,lt,info,[{preset:'ottomanInfantry',x:.14,y:.97,h:.38,pose:'push',walk:true,dir:1,face:'determined'},{preset:'ottomanInfantry',x:.35,y:.97,h:.4,pose:'carry',walk:true,dir:1,face:'tired'}],.94,.4);
    drawHero(g,lt,info,{x:.82,y:.98,h:.56,face:'worried',pose:'point',flip:true,poseAt:[[0,'point'],[.65,'brace'],[1.3,'push']],faceAt:[[0,'worried'],[1.0,'determined']]});
    // far shoreline and harbour city
    path(g,[[0,390],[400,420],[780,390],[1180,430],[1500,390],[1920,420],[1920,530],[0,530]],'#66776b',null,0);
    for(let i=0;i<14;i++){const xx=i*145;g.fillStyle='#a68e72';g.fillRect(xx,400,75,95);path(g,[[xx-6,400],[xx+37,355],[xx+81,400]],'#715c4e',null,0);}
    dust(g,lt,780,850,8,42,'#d5bc8e');
  });
}});
registerTemplate('last_assault',{draw(g,lt,info){
  const a=info.args||{};
  camera(g,lt,info,()=>{
    wallBase(g,lt,1);
    // smoke behind the wall and a wall of approaching infantry
    smoke(g,lt,1220,430,4);smoke(g,lt,1580,470,17);
    formation(g,{preset:'ottomanInfantry',presets:['ottomanInfantry','ottomanElite'],rows:5,cols:18,x0:.02,x1:.77,yFront:.99,yBack:.75,hFront:.20,hBack:.07,face:'determined',march:.24,seed:45,t:lt});
    formation(g,{preset:'ottomanArcher',rows:3,cols:14,x0:.05,x1:.71,yFront:.78,yBack:.66,hFront:.11,hBack:.06,face:'determined',seed:48,t:lt,flip:true});
    // ladders rise in staggered beats
    for(let i=0;i<5;i++){const x=1160+i*155, rise=clamp((lt-.35-i*.18)/1.15);drawLadder(g,x,810,330*rise,lt,i);}
    // attackers climbing at different phases
    const climbers=[];
    for(let i=0;i<7;i++){const q=clamp((lt-.7-i*.16)/2.0);climbers.push({preset:'ottomanInfantry',x:(.62+i*.055),y:.76-q*.29,h:.23,face:'determined',pose:'run',walk:true,dir:1,speed:.5,flip:true});}
    drawPeople(g,lt,info,climbers,.93,.25);
    drawHero(g,lt,info,{x:.25,y:.99,h:.61,face:'determined',pose:'guard',
      poseAt:[[0,'guard'],[.65,'brace'],[1.25,'thrust'],[1.9,'brace']],faceAt:[[0,'determined'],[1.25,'angry']]});
    // defenders at the parapet and falling masonry
    formation(g,{preset:'byzantineGuard',rows:2,cols:14,x0:.58,x1:.98,yFront:.46,yBack:.41,hFront:.12,hBack:.075,face:'worried',seed:81,t:lt,flip:true});
    arrowStorm(g,lt,23);
    for(let i=0;i<5;i++){const p=(lt*.8+i*.21)%1,x=1300+i*110+Math.sin(lt*3+i)*18,y=420+p*340;circle(g,x,y,4+p*7,alpha('#d0b99a',1-p));}
    if(lt>1.3){glow(g,1450,680,160,'#e68d4f',.23);dust(g,lt-1.3,1510,710,5,65);}
    if(a.moment==='breach'){g.save();g.strokeStyle='#f4d39b';g.lineWidth=9;g.beginPath();g.arc(1500,540,80+lt*12,0,Math.PI*2);g.stroke();g.restore();}
  });
}});
registerTemplate('aftermath_city',{draw(g,lt,info){
  camera(g,lt,info,()=>{
    drawCityInterior(g,lt);
    // transition from panic into a changed city: dust and slow movement
    gradient(g,0,H(),[[0,'rgba(20,24,33,.0)'],[1,'rgba(20,20,23,.28)']]);
    smoke(g,lt,350,385,31);smoke(g,lt,1510,420,32);
    drawHero(g,lt,info,{x:.32,y:.98,h:.62,face:'tired',pose:'walk',walk:true,speed:.18,flip:false,weapon:null,shield:null,
      poseAt:[[0,'walk'],[.9,'carry'],[1.8,'walk']],faceAt:[[0,'tired'],[1.0,'worried']]});
    drawPeople(g,lt,info,[{preset:'peasant',x:.72,y:.96,h:.38,face:'sad',pose:'walk',walk:true,dir:1}],.94,.4);
    for(let i=0;i<9;i++){const x=150+i*205;circle(g,x,900+Math.sin(lt+i)*3,4,'#c8b391');}
  });
}});


// Character-led set pieces added after first proof review. The defender is a recurring
// scale/continuity anchor; each template stages a different physical action and setting.
function drawHero(g,t,info,{x=.3,y=.97,h=.62,face='determined',pose='guard',flip=false,weapon='spear',
  walk=false,speed=1,dir=1,poseAt,faceAt,lookAt,to,from,moveAt,dur,enter,exit,fall,lean,
  shield={type:'round',color:BLUE,charge:'eagle',chargeColor:GOLD}}={}){
  if(info?.args?.hero===false) return;
  const actor={preset:'byzantineYou',x,y,h,face,pose,flip,weapon,walk,speed,dir,poseAt,faceAt,lookAt,to,from,moveAt,dur,enter,exit,fall,lean,shield};
  drawPeople(g,t,info,[actor],.94,.66);
}
function drawNightWatch(g,t,info){
  gradient(g,0,H(),[[0,'#111a2a'],[.48,'#293443'],[1,'#514237']]);
  g.save();g.globalAlpha=.5;
  for(let i=0;i<110;i++){const x=(i*197)%W(),y=(i*83)%470;circle(g,x,y,1.4+(i%3), '#e8d8ad');}
  g.restore();
  circle(g,1580,170,92,'#d5c9a8');
  path(g,[[0,650],[210,570],[390,615],[610,520],[850,600],[1100,520],[1360,595],[1620,520],[1920,590],[1920,1080],[0,1080]],'#202b35',null,0);
  g.fillStyle='#685c4e';g.fillRect(0,700,W(),175);
  for(let x=60;x<W();x+=205)tower(g,x,720,.82,0);
  for(let i=0;i<13;i++){const x=90+i*145;glow(g,x,650+Math.sin(t*2+i)*5,65,'#f3a34a',.18);circle(g,x,650+Math.sin(t*2+i)*5,6,'#f5b65e');}
  // Far Ottoman camp is a horizon of fires and silhouettes, not a flat empty field.
  for(let i=0;i<30;i++){const x=25+i*67,y=620+(i%4)*13;path(g,[[x,y],[x+20,y-45-(i%3)*12],[x+43,y]],i%2?'#6e4736':'#59473c',null,0);}
  drawHero(g,t,info,{x:.35,y:.97,h:.68,face:'tired',pose:'guard',poseAt:[[0,'guard'],[1.05,'point'],[2.15,'brace']],faceAt:[[0,'tired'],[1.05,'worried'],[2.15,'determined']],lookAt:[[0,.1],[.95,.6],[1.9,-.3]]});
  drawPeople(g,t,info,[{preset:'byzantineGuard',x:.78,y:.96,h:.47,face:'worried',pose:'look',flip:true}],.94,.5);
  smoke(g,t,1180,500,51);smoke(g,t,1580,520,52);
}
function drawGunCrew(g,t,info,a){
  wallBase(g,t,0);
  // Gun is staged at foreground scale; the crew loads, braces, fires, and reacts.
  const fireAt=a.fireAt??.65,age=t-fireAt;
  cannon(g,475,895,2.0,age+.55,age>=0);
  drawPeople(g,t,info,[
    {preset:'ottomanInfantry',x:.13,y:.96,h:.45,face:'determined',pose:'carry',walk:true,dir:1,speed:.45},
    {preset:'ottomanInfantry',x:.66,y:.96,h:.43,face:'determined',pose:'push',walk:true,dir:-1,speed:.32},
    {preset:'ottomanElite',x:.83,y:.95,h:.45,face:'focused',pose:'guard',flip:true}
  ],.94,.48);
  // Powder smoke, recoil and projectile arc have separate timing.
  if(age>-.42&&age<0){glow(g,460,700,90,'#d88c4d',.15);for(let i=0;i<8;i++)circle(g,430+i*10,700+Math.sin(t*12+i)*8,5,'#a59b8b');}
  if(age>=0&&age<.42){glow(g,465,695,260,'#ffbd66',.75);path(g,[[420,730],[385,540],[485,585],[550,455],[530,735]],'#fff2cf',null,0);}
  if(age>=.1&&age<1.6){const q=clamp((age-.1)/1.5),x=630+q*880,y=640-230*Math.sin(q*Math.PI);circle(g,x,y,18,'#211f1d');}
  if(age>=1.02){dust(g,t-1.02,1510,560,91,88,'#d5c1a5');smoke(g,t-1.02,1500,545,92);glow(g,1500,570,195,'#e0b16c',.28);}
  // Enemy gun crew is kept on the Ottoman side; no Byzantine protagonist is placed beside the siege cannon.
}
function drawRepairWall(g,t,info,a){
  const beat=a.beat||'rebuild';
  wallBase(g,t,beat==='rebuild'?.35:.78);
  // Timber scaffold and pulley visibly move materials into the damaged section.
  for(let x=1280;x<1740;x+=125){
    line(g,[[x,820],[x,395]],'#4b392c',15);
    line(g,[[x-42,820],[x+42,820]],'#76533a',10);
    line(g,[[x,430],[x+118,430]],'#76533a',11);
    line(g,[[x,520],[x+118,520]],'#76533a',9);
    line(g,[[x+12,435],[x+112,520]],'#4b392c',6);
  }
  const lift=(t*95)%245, blockY=745-lift;
  g.save();g.translate(1510,blockY);g.rotate(Math.sin(t*2)*.06);
  path(g,[[-42,-25],[35,-25],[48,15],[-28,24]],'#b4a48b','#4a4035',6);g.restore();
  line(g,[[1510,400],[1510,blockY-22]],'#4c3e33',4);
  drawPeople(g,t,info,[
    {preset:'byzantineGuard',x:.67,y:.94,h:.47,face:'determined',pose:'carry',walk:true,dir:-1,speed:.34},
    {preset:'byzantineGuard',x:.84,y:.94,h:.43,face:'worried',pose:'brace'},
    {preset:'peasant',x:.52,y:.95,h:.38,face:'worried',pose:'carry',walk:true,dir:1,speed:.25}
  ],.94,.48);
  for(let i=0;i<20;i++){const q=(t*.7+i*.13)%1,x=1460+Math.sin(i*4)*95+q*36,y=560+q*250;circle(g,x,y,3+q*5,alpha('#c6ae8e',1-q));}
  drawHero(g,t,info,{x:.24,y:.98,h:.57,face:'strained',pose:'carry',walk:true,speed:.24,dir:1,
    poseAt:[[0,'carry'],[.78,'brace'],[1.55,'push']],faceAt:[[0,'strained'],[1.25,'determined']]});
}
function drawGoldenHorn(g,t,info,a){
  gradient(g,0,H(),[[0,'#8299a2'],[.3,'#c5c1ac'],[.56,'#446b7a'],[1,'#102c3d']]);
  path(g,[[0,420],[210,380],[420,425],[650,360],[890,410],[1120,350],[1360,400],[1590,350],[1920,390],[1920,590],[0,590]],'#70776e',null,0);
  for(let i=0;i<18;i++){const x=i*114;g.fillStyle=i%2?'#917b66':'#a48d73';g.fillRect(x,350-(i%4)*18,70,175);path(g,[[x-8,352-(i%4)*18],[x+35,306-(i%4)*18],[x+78,352-(i%4)*18]],'#73574a',null,0);}
  drawSea(g,t,560);
  // The chain is a physical barrier, suspended from the harbour walls.
  g.save();g.strokeStyle='#2d2b2a';g.lineWidth=18;g.beginPath();g.moveTo(60,785);
  for(let i=1;i<=45;i++){const x=60+i*40,y=785-165*Math.sin(Math.PI*i/45)+Math.sin(t*2+i*.3)*3;g.lineTo(x,y);}
  g.stroke();g.strokeStyle='#b8a98e';g.lineWidth=4;g.stroke();g.restore();
  for(let i=0;i<3;i++){const x=((t*(75+i*13)+i*680-260)%(W()+700))-200;ship(g,x,740+i*58,.66+i*.07,t,{banner:i%2?BLUE:RED,heading:1,sail:'#d7c9b0'});}
  // A harbour watchman reacts as the chain is threatened.
  drawHero(g,t,info,{x:.22,y:.98,h:.61,pose:'point',face:'worried',poseAt:[[0,'point'],[.8,'guard'],[1.55,'pointUp']],faceAt:[[0,'worried'],[1.4,'determined']],lookAt:[[0,.5],[.8,-.2],[1.4,.6]]});
  drawPeople(g,t,info,[{preset:'byzantineArcher',x:.75,y:.96,h:.43,pose:'aim',face:'determined',flip:true}],.94,.45);
  if(a.beat==='chain'){glow(g,960,730,130,'#d8bf8d',.22);}
}
function drawTunnelCutaway(g,t,info,a){
  gradient(g,0,H(),[[0,'#7e9090'],[.38,'#b09b79'],[.39,'#312a27'],[1,'#151719']]);
  path(g,[[0,465],[250,410],[500,445],[740,390],[970,435],[1210,390],[1480,445],[1690,400],[1920,445],[1920,520],[0,520]],'#786e5b',null,0);
  // Surface wall and siege camp read clearly above the underground cut.
  wallBase(g,t,.22);
  g.fillStyle='#2b2927';g.fillRect(0,650,W(),430);
  path(g,[[0,795],[310,730],[550,760],[820,700],[1110,755],[1370,705],[1640,760],[1920,710],[1920,875],[0,875]],'#6c5140','#241f1c',8);
  for(let i=0;i<10;i++){const x=260+i*170,y=780+Math.sin(i*.6)*28;line(g,[[x-38,y-35],[x+38,y+35]],'#9a7b55',12);line(g,[[x-38,y+35],[x+38,y-35]],'#513c2b',8);}
  const hit=(t*1.5)%1;
  drawPeople(g,t,info,[
    {preset:'ottomanInfantry',x:.63,y:.82,h:.32,face:'determined',pose:'kneel',weapon:'pickaxe'},
    {preset:'ottomanInfantry',x:.78,y:.84,h:.29,face:'determined',pose:'thrust',weapon:'shovel'},
    {preset:'byzantineGuard',x:.46,y:.84,h:.31,face:'worried',pose:'push',weapon:'spear'}
  ],.94,.34);
  for(let i=0;i<22;i++){const q=(t*.6+i*.12)%1;circle(g,610+Math.sin(i*2)*155+q*80,740+q*135,3+q*5,alpha('#c7a57b',1-q));}
  glow(g,1200,800,100,'#e38f45',.15+.1*Math.sin(t*6));
  drawHero(g,t,info,{x:.25,y:.96,h:.54,pose:'kneel',face:'worried',poseAt:[[0,'kneel'],[1.1,'brace'],[1.85,'guard']],faceAt:[[0,'worried'],[1.5,'determined']]});
  if(hit<.08)for(let i=0;i<5;i++)circle(g,1080+i*20,760,6,'#b9a17a');
}
function drawChurchRefuge(g,t,info,a){
  gradient(g,0,H(),[[0,'#232d3b'],[.46,'#6f655c'],[1,'#312b29']]);
  // Three-dimensional nave perspective: aisle, pillars, high arches, altar and candles.
  path(g,[[0,340],[460,265],[700,680],[0,1080]],'#75695d','#302a28',8);
  path(g,[[1920,340],[1460,265],[1220,680],[1920,1080]],'#5c5148','#302a28',8);
  for(let i=0;i<7;i++){
    const x=140+i*275,top=120+(i%2)*30;
    g.fillStyle=i%2?'#99856f':'#817360';g.fillRect(x,top,62,620);
    g.fillStyle='#b49c7a';g.fillRect(x-15,top-14,92,24);
    g.beginPath();g.ellipse(x+31,top+5,105,85,0,Math.PI,Math.PI*2);g.fill();
    glow(g,x+31,top+280,145,'#eab56a',.09);
  }
  path(g,[[640,750],[1280,750],[1670,1080],[250,1080]],'#514237',null,0);
  for(let i=0;i<9;i++){const x=500+i*118;glow(g,x,740,70,'#f0a24c',.24);circle(g,x,730,8,'#ffc96f');}
  drawPeople(g,t,info,[
    {preset:'monk',x:.72,y:.94,h:.46,face:'sad',pose:'beg'},
    {preset:'peasant',x:.52,y:.96,h:.39,face:'worried',pose:'carry',walk:true,dir:-1,speed:.3},
    {preset:'lady',x:.84,y:.94,h:.38,face:'sad',pose:'hold'}
  ],.94,.45);
  drawHero(g,t,info,{x:.27,y:.98,h:.61,face:'tired',pose:'kneel',
    poseAt:[[0,'kneel'],[.75,'beg'],[1.45,'kneel']],faceAt:[[0,'tired'],[.75,'sad'],[1.45,'worried']]});
  if(a.beat==='candle'){for(let i=0;i<4;i++)glow(g,500+i*290,700,120,'#ffc66b',.18);}
}
registerTemplate('final_night',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>{drawNightWatch(g,lt,info);if(a.beat==='dawn')gradient(g,0,H(),[[0,'rgba(189,126,83,0)'],[.45,'rgba(209,151,101,.22)'],[1,'rgba(24,27,34,0)']]);});}});
registerTemplate('gun_crew',{draw(g,lt,info){camera(g,lt,info,()=>drawGunCrew(g,lt,info,info.args||{}));}});
registerTemplate('repair_wall',{draw(g,lt,info){camera(g,lt,info,()=>drawRepairWall(g,lt,info,info.args||{}));}});
registerTemplate('golden_horn',{draw(g,lt,info){camera(g,lt,info,()=>drawGoldenHorn(g,lt,info,info.args||{}));}});
registerTemplate('tunnel_cutaway',{draw(g,lt,info){camera(g,lt,info,()=>drawTunnelCutaway(g,lt,info,info.args||{}));}});
registerTemplate('church_refuge',{draw(g,lt,info){camera(g,lt,info,()=>drawChurchRefuge(g,lt,info,info.args||{}));}});
