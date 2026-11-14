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
function drawCamp(g,t,beat='tents'){
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
  if(beat==='engineers'){
    // Measuring rope and survey rods make the engineering preparation a distinct beat.
    line(g,[[290,810],[1610,745]],'#d2bd90',5,.85);
    for(let i=0;i<9;i++){const x=380+i*145;line(g,[[x,788-i*4],[x,710-i*4]],'#c0a276',6,.8);}
    line(g,[[560,735],[1360,735]],'#e0c99c',3,.75);
    for(let i=0;i<5;i++)circle(g,610+i*165,735,8,'#b98d5a');
  }
  if(beat==='supply'){
    for(let i=0;i<5;i++){
      const x=140+i*360,y=930-(i%2)*18;
      circle(g,x,y,38,'#4a3426');circle(g,x,y-4,29,'#876341');
      line(g,[[x-28,y-28],[x+28,y-28]],'#c1a171',5,.8);
      path(g,[[x-78,y+55],[x+78,y+55],[x+63,y+86],[x-64,y+86]],'#76563a','#302218',4);
    }
  }
  if(beat==='march'){
    drawPeople(g,t,{dur:6,globalT:t,start:0,args:{}},[
      {preset:'ottomanInfantry',x:.16,y:.97,h:.34,face:'determined',pose:'walk',walk:true,dir:1,speed:.22},
      {preset:'ottomanInfantry',x:.83,y:.96,h:.33,face:'neutral',pose:'carry',walk:true,dir:-1,speed:.16}
    ],.94,.34);
    dust(g,t,980,875,83,32,'#bda37f');
  }
  if(beat==='tents'){
    for(let i=0;i<6;i++)smoke(g,t+i*.14,240+i*270,505-(i%2)*32,31+i);
    for(let i=0;i<7;i++)glow(g,140+i*270,620,86,'#e7a45f',.12);
  }
}
function drawArtilleryHaul(g,t,info,a){
  const beat=a.beat||"departure";
  gradient(g,0,H(),[[0,"#78818a"],[.38,"#c4b094"],[1,"#60503d"]]);
  // Distant siege camp and broken earth establish the approach road.
  path(g,[[0,520],[180,450],[390,500],[650,420],[870,485],[1110,410],[1390,480],[1630,420],[1920,460],[1920,1080],[0,1080]],"#766b5b",null,0);
  for(let i=0;i<11;i++){
    const x=45+i*184,y=565+(i%3)*30;
    path(g,[[x-45,y],[x,y-74-(i%3)*9],[x+48,y]],i%2?"#806447":"#6b543e","#33281f",3);
    if(i%2===0)glow(g,x,y-5,48,"#d99450",.12);
  }
  // Rutted muddy road creates a strong foreground vanishing line.
  path(g,[[0,860],[370,790],[760,830],[1140,735],[1530,780],[1920,700],[1920,1080],[0,1080]],"#544638",null,0);
  for(let i=0;i<20;i++){
    const x=i*104-20,y=915+(i%4)*24;
    line(g,[[x,y],[x+125,y-28-(i%3)*7]],"#b39a78",5,.35);
  }
  // Heavy timber carriage and cannon are illustrative, not an authenticated Orban design.
  cannon(g,1335,865,1.72,t,false);
  function ox(x,y,scale,phase){
    const step=Math.sin(t*4.6+phase)*12;
    const bob=Math.sin(t*2.3+phase)*3;
    g.save();g.translate(x,y);g.scale(scale,scale);
    path(g,[[-112,-52+bob],[-86,-104+bob],[-16,-120+bob],[66,-102+bob],[111,-54+bob],[91,-4],[24,18],[-81,7]],"#4f3a2b","#211a14",7);
    path(g,[[63,-96+bob],[106,-128+bob],[142,-116+bob],[128,-72+bob],[87,-58+bob]],"#604733","#211a14",6);
    circle(g,133,-103+bob,5,"#181615");
    path(g,[[104,-128+bob],[92,-163+bob],[74,-174+bob],[83,-145+bob]],"#433125","#201913",5);
    path(g,[[121,-127+bob],[145,-154+bob],[161,-159+bob],[143,-130+bob]],"#433125","#201913",5);
    path(g,[[-85,-100+bob],[-108,-134+bob],[-83,-124+bob]],"#493528",null,0);
    for(let i=0;i<4;i++){
      const lx=-68+i*42;
      const stride=(i%2?step:-step)*.38;
      line(g,[[lx,-5+bob],[lx+stride,50]],"#2b211a",15);
      line(g,[[lx+stride,50],[lx+stride+4,90+Math.max(0,step*.2)]],"#211a15",11);
      circle(g,lx+stride+4,92+Math.max(0,step*.2),7,"#241b15");
    }
    // Shoulder yoke and harness straps.
    line(g,[[88,-84+bob],[160,-70+bob]],"#98744a",9);
    line(g,[[100,-63+bob],[108,6]],"#aa8a5a",6);
    line(g,[[72,-66+bob],[-48,-32+bob]],"#ae8a5b",5,.85);
    g.restore();
  }
  ox(400,830,.94,0);
  ox(690,844,.86,1.4);
  // Yoke, traces and hauling ropes connect the team to the gun carriage.
  line(g,[[750,760],[890,760]],"#916d43",17);
  line(g,[[750,748],[890,748]],"#c5a06b",5,.9);
  line(g,[[862,753],[1070,805]],"#b28a56",10,.85);
  line(g,[[862,776],[1070,835]],"#8d6b43",6,.9);
  for(let i=0;i<7;i++)circle(g,770+i*19,760,5,"#4b3c2c");
  drawPeople(g,t,info,[
    {preset:'ottomanInfantry',x:.49,y:.98,h:.43,face:'determined',pose:'push',walk:true,dir:1,speed:beat==='incline'?.38:.22},
    {preset:'ottomanInfantry',x:.70,y:.98,h:.40,face:'focused',pose:'carry',walk:true,dir:1,speed:.15},
    {preset:'ottomanElite',x:.88,y:.97,h:.42,face:'neutral',pose:'point',flip:true}
  ],.94,.43);
  if(beat==='incline'||beat==='departure'){
    dust(g,t,760,900,91,44,'#c4a783');
    dust(g,t,1050,860,92,32,'#b89c76');
  }
  if(beat==='emplacement'){
    path(g,[[1200,900],[1262,900],[1245,932],[1210,932]],"#86633d","#332315",4);
    path(g,[[1450,900],[1512,900],[1495,932],[1460,932]],"#86633d","#332315",4);
    glow(g,1390,760,112,"#dca465",.13);
  }
  if(beat==='guides'){
    for(let i=0;i<8;i++)dust(g,t,940+i*35,850-(i%3)*22,99+i,17,'#c5a881');
  }
}

function wallBase(g,t,breach=0){
  gradient(g,0,H(),[[0,'#56697a'],[.45,'#c7b08a'],[1,'#69533d']]);
  path(g,[[0,650],[0,500],[220,445],[430,490],[670,420],[900,460],[1160,400],[1390,470],[1640,425],[1920,460],[1920,800],[0,800]],'#777b6b',null,0);
  // broad curtain wall
  g.fillStyle='#a99a82';g.fillRect(1080,470,840,350);
  g.strokeStyle='#453d37';g.lineWidth=9;g.strokeRect(1080,470,840,350);
  const stonePalette=['#b2a38a','#a7977f','#9c8b73','#bcae96','#8f816d'];
  for(let row=0,y=490;y<810;y+=35,row++){
    for(let col=0,x=1080;x<1920;x+=42,col++){
      const xx=x+(row%2)*14,tone=(row*13+col*7)%stonePalette.length;
      g.fillStyle=alpha(stonePalette[tone],.24);g.fillRect(xx+1,y+1,36,28);
      g.strokeStyle=alpha('#51473c',.62);g.lineWidth=2;g.strokeRect(xx,y,38,30);
      if((row*19+col*11)%17===0)line(g,[[xx+8,y+6],[xx+17,y+15],[xx+13,y+23]],alpha('#4a3f34',.5),2,.7);
      if((row*7+col*5)%23===0)circle(g,xx+28,y+8,3,alpha('#d8c9af',.6));
    }
  }
  for(let i=0;i<55;i++){const x=1090+(i*149)%810,y=500+(i*61)%300;line(g,[[x,y],[x+4+(i%5)*3,y+4+(i%3)*5]],alpha('#40382f',.32),2,.55);}
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

function drawActorCloseup(g,t,info,a){
  const preset=a.actorPreset || (a.hero ? 'byzantineYou' : 'byzantineGuard');
  gradient(g,0,H(),[[0,'#18212d'],[.42,'#39414b'],[1,'#15191e']]);
  path(g,[[0,0],[W()*.31,0],[W()*.38,H()],[0,H()]],'#64584b','#292724',7);
  path(g,[[W()*.72,0],[W(),0],[W(),H()],[W()*.65,H()]],'#51483f','#292724',7);
  for(let i=0;i<7;i++){
    const y=130+i*132;
    line(g,[[W()*.06,y],[W()*.27,y-12]],'#b29b79',7,.36);
    line(g,[[W()*.76,y-12],[W()*.95,y]],'#b29b79',7,.3);
  }
  glow(g,W()*.73,H()*.47,230,'#e0a15c',.22);
  circle(g,W()*.73,H()*.47,11,'#f0b66e');
  drawCinematicActor(g,t,info,{
    preset, x:.55, y:1.23, h:1.08, face:a.expression||'worried',
    pose:a.pose||'guard', weapon:a.weapon===undefined?'spear':a.weapon,
    shield:a.hero===false?false:undefined, seed:a.seed||21
  },.93,.6,false);
  const vg=g.createRadialGradient(W()*.55,H()*.5,H()*.12,W()*.55,H()*.5,H()*.8);
  vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,'rgba(5,8,12,.62)');
  g.fillStyle=vg; g.fillRect(0,0,W(),H());
}
registerTemplate('actor_closeup',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawActorCloseup(g,lt,info,a));}});

function drawCityDetail(g,t,info,a){
  const variant=Math.abs(Number(a.variant)||0)%5;
  gradient(g,0,H(),[[0,'#6a7880'],[.38,'#c3aa8c'],[1,'#55473d']]);
  path(g,[[0,520],[0,390],[180,350],[330,410],[510,320],[680,390],[870,305],[1050,380],[1270,315],[1450,390],[1670,330],[1920,380],[1920,650],[0,650]],'#657168',null,0);
  g.fillStyle='#ae9c82';g.fillRect(670,405,580,210);
  g.beginPath();g.ellipse(960,405,205,110,0,Math.PI,Math.PI*2);g.fill();
  g.strokeStyle='#433b34';g.lineWidth=7;g.stroke();
  for(let i=0;i<5;i++){const x=700+i*116;g.fillStyle='#9b8871';g.fillRect(x,340,27,160);g.beginPath();g.arc(x+13,340,13,Math.PI,0);g.fill();}
  const wallY=690+(variant%2)*20;
  path(g,[[0,wallY+70],[0,wallY-90],[260,wallY-130],[540,wallY-70],[850,wallY-150],[1160,wallY-85],[1470,wallY-140],[1920,wallY-55],[1920,H()],[0,H()]],'#968873','#35302c',9);
  for(let row=0;row<7;row++)for(let col=0;col<24;col++){
    const x=col*88+(row%2)*42, y=wallY-78+row*58;
    g.strokeStyle=alpha('#4a4037',.48);g.lineWidth=2;g.strokeRect(x,y,82,52);
    if((row*17+col*7+variant)%11===0) line(g,[[x+14,y+8],[x+28,y+24],[x+20,y+45]],'#3e3630',3,.64);
  }
  if(variant===0){smoke(g,t,1480,405,120);flag(g,1590,660,130,{color:BLUE,t,lw:2});}
  if(variant===1){drawSea(g,t,wallY+80);for(let i=0;i<2;i++)ship(g,280+i*640+t*24,wallY+15,.38,t,{banner:i?BLUE:RED});}
  if(variant===2){smoke(g,t,880,470,122);dust(g,t,960,700,123,35,'#d2b58c');}
  if(variant===3){for(let i=0;i<9;i++){const x=130+i*215;glow(g,x,wallY-120,100,'#e8a85e',.12);}}
  if(variant===4){for(let i=0;i<8;i++){const x=90+i*260;path(g,[[x,wallY+40],[x+45,wallY-15],[x+90,wallY+40]],'#7c5e4c',null,0);}}
  if(a.hero===false){
    if(a.actorPreset && a.actorPreset!=='byzantineYou') drawPeople(g,t,info,[{preset:a.actorPreset,x:.80,y:.99,h:.48,face:'determined',pose:'guard',flip:true}],.94,.48);
  } else drawHero(g,t,info,{x:.24,y:.99,h:.58,face:'determined',pose:'guard'});
}
registerTemplate('city_detail',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawCityDetail(g,lt,info,a));}});
registerTemplate('command_camp',{draw(g,lt,info){const a=info.args||{},beat=a.beat||"tents";camera(g,lt,info,()=>{drawCamp(g,lt,beat);const count=beat==="standards"?11:8;for(let i=0;i<count;i++)flag(g,50+i*(1820/(count-1)),620,beat==="standards"?172:140,{color:i%2?RED:BLUE,t:lt,lw:2});dust(g,lt,1200,870,88,40);});}});
registerTemplate('artillery_haul',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawArtilleryHaul(g,lt,info,a));}});
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
function drawNightCamp(g,t,info,a){
  const beat=a.beat||"horizon";
  gradient(g,0,H(),[[0,"#101a2a"],[.42,"#26313b"],[1,"#3a3029"]]);
  circle(g,1570,150,74,"#cfc6ad");
  path(g,[[0,570],[180,520],[360,555],[560,465],[780,530],[1010,450],[1240,520],[1490,450],[1710,520],[1920,460],[1920,1080],[0,1080]],"#1b2630",null,0);
  // Three layers of A-frame tents give the camp a readable horizon rather than one flat line.
  for(let row=0;row<3;row++){
    for(let i=0;i<13;i++){
      const x=i*164-55+(row%2)*58, base=590+row*70+(i%4)*8, scale=0.56+row*.18;
      const w=54*scale,h=62*scale;
      path(g,[[x-w,base],[x,base-h],[x+w,base]],(i+row)%2?"#604a39":"#75553e","#302923",3);
      line(g,[[x,base-h],[x,base]],"#a0845d",2,.55);
    }
  }
  // Small moving fires and smoke sell distance and wind.
  for(let i=0;i<15;i++){
    const x=50+i*132, y=585+(i%3)*56;
    glow(g,x,y,55+(i%3)*12,"#e29a4d",.24);
    circle(g,x,y,5+(i%2)*2,"#f0b56a");
    if(i%3===0) smoke(g,t+i*.13,x,y-12,70+i);
  }
  // Supply carts sit in the middle ground; their wheels rotate independently.
  for(let i=0;i<3;i++){
    const x=360+i*590+Math.sin(t*.45+i)*14, y=868+i%2*12;
    line(g,[[x-55,y-22],[x+55,y-22]],"#886b48",12);
    for(const wx of [x-40,x+40]){
      circle(g,wx,y,25,"#302922");circle(g,wx,y,15,"#b18a59");
      line(g,[[wx,y-16],[wx,y+16]],"#d0b382",3,.6);
    }
  }
  // The wall-side defender watches the camp from a dark parapet in the foreground.
  path(g,[[0,925],[0,870],[220,830],[470,870],[720,815],[960,860],[1180,815],[1450,860],[1680,815],[1920,850],[1920,1080],[0,1080]],"#51483d","#211f1d",7);
  for(let x=0;x<1920;x+=58) path(g,[[x,865],[x+32,856],[x+32,890],[x,900]],"#81705b","#302a25",3);
  if(a.hero!==false){
    drawHero(g,t,info,{x:.24,y:.99,h:.57,face:"worried",pose:"point",
      poseAt:[[0,"point"],[.65,"guard"],[1.3,"point"]],
      faceAt:[[0,"worried"],[1.1,"tired"]]});
  }
  drawPeople(g,t,info,[
    {preset:"ottomanInfantry",x:.68,y:.92,h:.31,face:"determined",pose:"walk",walk:true,dir:1,speed:.22},
    {preset:"ottomanInfantry",x:.81,y:.92,h:.28,face:"neutral",pose:"carry",walk:true,dir:1,speed:.17}
  ],.94,.31);
  if(beat==="movement") for(let i=0;i<4;i++) dust(g,t,1040+i*70,850,80+i,14,"#baa080");
}
function drawNightGuns(g,t,info,a){
  const beat=a.beat||"distant_flash";
  gradient(g,0,H(),[[0,"#0d1522"],[.48,"#202c38"],[1,"#332a24"]]);
  circle(g,1560,138,62,"#cbc2a9");
  path(g,[[0,620],[170,540],[380,600],[610,500],[840,575],[1080,480],[1300,560],[1540,470],[1770,550],[1920,500],[1920,1080],[0,1080]],"#18222c",null,0);
  if(beat==="silhouette"){
    const x=1030,y=830;
    line(g,[[x-250,y],[x+250,y]],"#4e3929",24);
    line(g,[[x-110,y-62],[x+260,y-218]],"#171715",48);
    line(g,[[x-102,y-78],[x+254,y-229]],"#6f5740",7);
    for(const wx of [x-160,x+145]){
      circle(g,wx,y+4,92,"#1a1918");circle(g,wx,y+4,62,"#7c6247");
      for(let k=0;k<10;k++){const an=k*Math.PI/5;line(g,[[wx,y+4],[wx+73*Math.cos(an),y+4+73*Math.sin(an)]],"#c09b6b",6);}
    }
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.28,y:.98,h:.48,face:"focused",pose:"brace"},
      {preset:"ottomanInfantry",x:.72,y:.98,h:.42,face:"determined",pose:"carry",flip:true}],.94,.47);
  } else {
    for(let i=0;i<5;i++){
      const x=150+i*390,y=690+(i%2)*42,scale=.55+(i%3)*.12;
      line(g,[[x-78*scale,y],[x+72*scale,y]],"#594331",13*scale);
      line(g,[[x-20*scale,y-8*scale],[x+66*scale,y-50*scale]],"#282724",17*scale);
      circle(g,x-45*scale,y+3,26*scale,"#242321");circle(g,x+44*scale,y+3,26*scale,"#242321");
      const pulse=(Math.sin(t*3.2+i*1.7)+1)*.5;
      if(beat==="distant_flash"&&i%2===0)glow(g,x+88*scale,y-72*scale,66+40*pulse,"#ef9b4d",.24+.2*pulse);
      if(beat==="smoke"||beat==="thunder"||i%2===0)smoke(g,t+i*.21,x+90*scale,y-80*scale,100+i);
    }
    if(beat==="distant_flash"||beat==="thunder"){
      const pulse=Math.max(0,Math.sin(t*3.8));glow(g,1230,640,170+90*pulse,"#f0a65d",.22+.26*pulse);
    }
    if(beat==="smoke"){
      glow(g,1150,580,150,"#d9a36c",.12);
      for(let i=0;i<9;i++)smoke(g,t+i*.24,970+i*48,430-i*10,170+i);
    }
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.43,y:.96,h:.30,face:"focused",pose:"brace"},
      {preset:"ottomanInfantry",x:.53,y:.96,h:.29,face:"determined",pose:"carry"}],.94,.30);
  }
}

function drawNightGunCrew(g,t,info,a){
  const beat=a.beat||"load";
  gradient(g,0,H(),[[0,"#101722"],[.42,"#252d34"],[1,"#32271f"]]);
  path(g,[[0,810],[300,765],[600,790],[900,745],[1220,780],[1540,740],[1920,780],[1920,1080],[0,1080]],"#282a29",null,0);
  for(let i=0;i<7;i++){
    const x=80+i*280,y=665+(i%2)*26;
    path(g,[[x-72,y],[x,y-112],[x+72,y]],"#5c4633","#261f19",4);
    glow(g,x,y-6,40,"#d98e49",.18);
  }
  cannon(g,940,930,1.86,t,false);
  line(g,[[700,835],[1250,735]],"#765b3e",20);line(g,[[700,835],[1250,735]],"#b9986d",4,.65);
  drawPeople(g,t,info,[
    {preset:"ottomanInfantry",x:.17,y:.98,h:.40,face:"determined",pose:"carry",walk:true,dir:1,speed:.22},
    {preset:"ottomanInfantry",x:.36,y:.98,h:.43,face:"focused",pose:"push",walk:true,dir:1,speed:.18},
    {preset:"ottomanInfantry",x:.67,y:.98,h:.41,face:"determined",pose:beat==="brace"?"brace":"carry",flip:true},
    {preset:"ottomanElite",x:.86,y:.97,h:.39,face:"neutral",pose:"guard",flip:true}
  ],.94,.42);
  if(beat==="match"||beat==="fire"){
    const pulse=Math.max(0,Math.sin(t*4));glow(g,1250,690,105+65*pulse,"#ffb45c",.44);
    if(beat==="fire")smoke(g,t,1280,660,140);
  } else glow(g,500,700,150,"#e59a4f",.18);
}

function drawNightWallWatch(g,t,info,a){
  const beat=a.beat||"watch";
  gradient(g,0,H(),[[0,"#101725"],[.42,"#263441"],[1,"#4a3c2d"]]);
  // The camera is now on the actual land wall: crenellations, tower shadow and the sleeping city.
  path(g,[[0,520],[190,470],[380,495],[590,420],[790,480],[1010,410],[1240,475],[1460,400],[1680,460],[1920,405],[1920,1080],[0,1080]],"#182630",null,0);
  for(let i=0;i<12;i++){
    const x=i*168-45,y=550+(i%3)*24;
    path(g,[[x,y],[x+16,y-88],[x+58,y-105],[x+102,y-78],[x+120,y]],"#645847","#292823",4);
    path(g,[[x+12,y-79],[x+108,y-79],[x+108,y-58],[x+12,y-58]],"#938068",null,0);
    for(let w=0;w<3;w++)line(g,[[x+22+w*29,y-66],[x+22+w*29,y-40]],"#302b26",5,.8);
  }
  // Near parapet and a narrow stair opening create a stronger foreground silhouette.
  path(g,[[0,825],[0,760],[280,730],[530,770],[770,715],[1040,755],[1300,710],[1580,748],[1920,695],[1920,1080],[0,1080]],"#51483d","#211f1c",8);
  for(let x=0;x<1920;x+=64)path(g,[[x,758],[x+38,751],[x+38,796],[x,804]],"#87745d","#302923",3);
  for(let i=0;i<10;i++){
    const x=95+i*190,y=685+(i%3)*22;
    glow(g,x,y,72,"#f0a451",.14);circle(g,x,y,5,"#f5bb69");
  }
  if(beat==="torch"){
    glow(g,1540,560,260,"#e9a05b",.32);
    path(g,[[1510,820],[1530,690],[1550,820]],"#372920",null,0);
    path(g,[[1530,700],[1515,650],[1545,665]],"#f4b05b",null,0);
  }
  if(beat==="dread"){
    for(let i=0;i<4;i++)smoke(g,t+i*.3,1120+i*170,470,180+i);
    glow(g,1440,620,180,"#e28a4a",.16);
  }
  drawHero(g,t,info,{x:beat==="torch"?.58:.32,y:.99,h:beat==="torch"?.82:.64,
    face:beat==="dread"?"worried":"tired",pose:beat==="patrol"?"walk":"guard",
    walk:beat==="patrol",speed:.19,dir:1,weapon:"spear",
    poseAt:[[0,"guard"],[.85,"point"],[1.7,"guard"]],
    faceAt:[[0,"tired"],[.85,"worried"],[1.7,"determined"]]});
  drawPeople(g,t,info,[{preset:"byzantineGuard",x:.79,y:.96,h:.39,face:"worried",pose:"look",flip:true}],.94,.41);
}
function drawNightCampDetail(g,t,info,a){
  const beat=a.beat||"horses";
  gradient(g,0,H(),[[0,"#0f1723"],[.42,"#242d33"],[1,"#463528"]]);
  path(g,[[0,610],[180,540],[400,590],[620,500],[850,570],[1100,485],[1340,560],[1570,475],[1780,535],[1920,480],[1920,1080],[0,1080]],"#18222b",null,0);
  const scale=beat==="horses"?.72:beat==="carts"?.58:.64;
  for(let i=0;i<6;i++){
    const x=80+i*335,y=642+(i%2)*38,w=(135+(i%3)*18)*scale;
    path(g,[[x-w,y],[x,y-150*scale],[x+w,y]],i%2?"#6e5038":"#8a6846","#30251e",5);
    line(g,[[x,y-145*scale],[x,y]],"#b09064",3,.6);
  }
  if(beat==="horses"){
    for(let i=0;i<2;i++){
      const x=610+i*690+Math.sin(t*1.35+i)*13,y=840,sc=1.42;
      g.save();g.translate(x,y);g.scale(sc,sc);
      path(g,[[-95,-48],[-60,-95],[14,-88],[80,-48],[66,5],[-65,5]],"#1d1b19","#080a0c",6);
      circle(g,84,-82,28,"#211f1c");
      path(g,[[90,-103],[119,-140],[133,-120],[103,-74]],"#211f1c",null,0);
      line(g,[[-54,0],[-67,83+Math.sin(t*3+i)*7]],"#171614",15);
      line(g,[[22,0],[35,83+Math.sin(t*3.2+i)*7]],"#171614",15);
      line(g,[[59,-32],[90,-7]],"#9a7550",6);
      line(g,[[83,-78],[119,-69]],"#9a7550",5);
      circle(g,117,-142,4,"#d8c7a4");g.restore();
    }
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.24,y:.98,h:.39,face:"tired",pose:"hold"},
      {preset:"ottomanInfantry",x:.80,y:.98,h:.37,face:"neutral",pose:"carry"}],.94,.4);
    for(let i=0;i<4;i++)dust(g,t,480+i*280,930,200+i,16,"#b99a72");
  } else if(beat==="carts"){
    const x=990+Math.sin(t*.48)*22,y=850;
    path(g,[[x-280,y-125],[x+275,y-125],[x+235,y-22],[x-245,y-22]],"#65482f","#201a15",8);
    for(let i=0;i<5;i++)path(g,[[x-215+i*102,y-126],[x-192+i*102,y-220],[x-150+i*102,y-126]],"#96734c",null,0);
    for(const wx of [x-190,x+190]){
      circle(g,wx,y+30,78,"#1d1a17");circle(g,wx,y+30,55,"#9a744d");
      for(let spoke=0;spoke<12;spoke++){
        const an=spoke*Math.PI/6+Math.sin(t*1.8)*.1;
        line(g,[[wx,y+30],[wx+62*Math.cos(an),y+30+62*Math.sin(an)]],"#d2ae78",7);
      }
      circle(g,wx,y+30,12,"#d0b58a");
    }
    line(g,[[x-340,y-105],[x-225,y-105]],"#6d4c2d",14);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.20,y:.98,h:.38,face:"strained",pose:"push",walk:true,dir:1,speed:.16},
      {preset:"ottomanInfantry",x:.78,y:.98,h:.35,face:"focused",pose:"carry",walk:true,dir:-1,speed:.12}],.94,.4);
    dust(g,t,x-330,930,218,32,"#c2a17b");
  } else if(beat==="signal"){
    for(let i=0;i<4;i++)smoke(g,t+i*.2,230+i*480,440,270+i);
    glow(g,1230,530,240,"#f0a35b",.24);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.36,y:.98,h:.50,face:"urgent",pose:"run",walk:true,dir:1,speed:.46},
      {preset:"ottomanElite",x:.72,y:.98,h:.45,face:"focused",pose:"point",flip:true}],.94,.48);
    line(g,[[1330,640],[1410,610],[1485,590]],"#8b6a48",9);glow(g,1485,590,72,"#f2b56c",.36);
  } else {
    for(let i=0;i<13;i++){
      const x=70+i*148,y=840+(i%3)*10;
      glow(g,x,y,76,"#d98c42",.28);circle(g,x,y-6,10,"#f3b15e");
      for(let j=0;j<3;j++)smoke(g,t+j*.3,x+(j-1)*11,y-30,310+j);
    }
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.29,y:.98,h:.34,face:"tired",pose:"guard"},
      {preset:"ottomanInfantry",x:.77,y:.98,h:.34,face:"neutral",pose:"guard"}],.94,.36);
  }
}

function drawNightGunCrewDetail(g,t,info,a){
  const beat=a.beat||"rammer";
  gradient(g,0,H(),[[0,"#0d1520"],[.43,"#22292f"],[1,"#30241d"]]);
  path(g,[[0,920],[280,860],[560,890],[850,820],[1200,870],[1510,815],[1920,860],[1920,1080],[0,1080]],"#252625",null,0);
  glow(g,480,690,250,"#e5a15b",.24);
  if(beat==="stone"){
    cannon(g,1110,940,1.72,t,false);
    circle(g,590,805,125,"#242522");circle(g,557,772,34,"#64655f");
    path(g,[[360,930],[405,735],[575,735],[620,930]],"#735437","#2c2118",12);
    for(let i=0;i<7;i++)line(g,[[415+i*24,755],[450+i*22,855]],"#b09064",5,.75);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.26,y:.99,h:.44,face:"focused",pose:"carry"},
      {preset:"ottomanInfantry",x:.72,y:.98,h:.43,face:"determined",pose:"push",flip:true}],.94,.43);
  } else if(beat==="powder"){
    cannon(g,1080,950,1.92,t,false);
    path(g,[[1350,830],[1390,740],[1570,740],[1610,830],[1590,965],[1370,965]],"#64482e","#211b15",10);
    path(g,[[1370,770],[1590,770],[1575,820],[1385,820]],"#30231a",null,0);
    for(let i=0;i<13;i++)circle(g,1420+(i%4)*34,789+Math.floor(i/4)*18,4,"#c7a378");
    line(g,[[1310,710],[1450,755]],"#a27b4d",9);glow(g,1320,704,75,"#e99b50",.22);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.28,y:.99,h:.44,face:"focused",pose:"carry"},
      {preset:"ottomanInfantry",x:.66,y:.98,h:.43,face:"determined",pose:"kneel",flip:true}],.94,.43);
  } else if(beat==="match"){
    cannon(g,880,960,1.7,t,false);
    for(let i=0;i<14;i++){const x=1210+i*24,y=600+Math.sin(t*3+i)*12;circle(g,x,y,3+(i%3),"#ef9e55");}
    glow(g,1450,590,170,"#ffb45b",.62);circle(g,1450,590,11,"#ffe7ae");
    line(g,[[1410,610],[1300,694],[1180,725]],"#8c6b47",10);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.54,y:.99,h:.48,face:"focused",pose:"point"},
      {preset:"ottomanElite",x:.79,y:.98,h:.45,face:"determined",pose:"guard",flip:true}],.94,.48);
  } else {
    cannon(g,1020,950,2.2,t,false);
    const rx=Math.sin(t*1.8)*48;
    line(g,[[390+rx,745],[1225+rx,570]],"#785a38",25);line(g,[[390+rx,745],[1225+rx,570]],"#d2b184",5,.75);
    for(let i=0;i<8;i++)line(g,[[550+i*75,810],[580+i*75,760]],"#b09064",4,.7);
    drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.25,y:.99,h:.46,face:"determined",pose:"push",walk:true,dir:1,speed:.22},
      {preset:"ottomanInfantry",x:.67,y:.98,h:.43,face:"focused",pose:"push",flip:true}],.94,.43);
  }
}

function drawAssaultWaves(g,t,info,a){
  const beat=a.beat||"approach";
  gradient(g,0,H(),[[0,"#a5a09a"],[.38,"#cfb58e"],[1,"#47372b"]]);
  path(g,[[0,485],[220,420],[470,455],[700,370],[950,430],[1200,365],[1460,430],[1680,370],[1920,410],[1920,1080],[0,1080]],"#756e62",null,0);
  // Three depth planes visually separate the expendable first ranks from the reserve.
  formation(g,{preset:"ottomanInfantry",rows:4,cols:18,x0:.02,x1:.82,yFront:.99,yBack:.79,hFront:.20,hBack:.075,face:"determined",march:.36,seed:31,t});
  formation(g,{preset:"ottomanArcher",rows:2,cols:13,x0:.08,x1:.76,yFront:.73,yBack:.63,hFront:.10,hBack:.06,face:"determined",seed:34,t});
  formation(g,{preset:"ottomanElite",rows:2,cols:12,x0:.24,x1:.82,yFront:.58,yBack:.51,hFront:.13,hBack:.065,face:"determined",seed:38,t});
  for(let i=0;i<6;i++){
    const x=980+i*154+(beat==="push"?Math.sin(t*2+i)*8:0);
    drawLadder(g,x,820,220+Math.sin(t*1.2+i)*16,t,i);
  }
  for(let i=0;i<14;i++)dust(g,t,160+i*120,840,50+i,22,"#c3a47f");
  for(let i=0;i<8;i++)smoke(g,t+i*.16,1180+i*88,465,20+i);
  flag(g,440,610,120,{color:RED,t,lw:2});flag(g,1600,610,120,{color:RED,t,lw:2});
}
function drawAssaultFirstWave(g,t,info,a){
  const beat=a.beat||"first_rush";
  gradient(g,0,H(),[[0,"#b1aaa0"],[.35,"#d3b58b"],[1,"#4b382b"]]);
  wallBase(g,t,.12);
  formation(g,{preset:"ottomanInfantry",rows:5,cols:16,x0:.02,x1:.71,yFront:.99,yBack:.70,hFront:.20,hBack:.075,face:"determined",march:.52,seed:43,t});
  for(let i=0;i<6;i++){const x=930+i*150;drawLadder(g,x,860,290+Math.sin(t*2+i)*18,t,i);}
  formation(g,{preset:"byzantineGuard",rows:2,cols:13,x0:.58,x1:.99,yFront:.47,yBack:.40,hFront:.12,hBack:.06,face:"worried",seed:46,t,flip:true});
  drawPeople(g,t,info,[{preset:"ottomanInfantry",x:.72,y:.82,h:.27,face:"determined",pose:"run",walk:true,speed:.5,flip:true},
    {preset:"byzantineGuard",x:.87,y:.51,h:.28,face:"worried",pose:"brace",flip:true}],.94,.3);
  arrowStorm(g,t,19);
  if(beat==="arrows")for(let i=0;i<22;i++)line(g,[[120+i*80,400+(i%4)*28],[160+i*80,375+(i%4)*27]],"#3d3025",3,.75);
}
function drawAssaultSecondWave(g,t,info,a){
  const beat=a.beat||"climb";
  gradient(g,0,H(),[[0,"#9b9287"],[.36,"#c2a47d"],[1,"#3c3028"]]);
  wallBase(g,t,.82);
  path(g,[[1080,505],[1200,530],[1300,495],[1380,565],[1480,500],[1580,555],[1700,495],[1810,540],[1920,500]],"#4b4037","#2c2621",12);
  for(let i=0;i<34;i++){
    const x=1180+(i*67)%570,y=540+(i*43)%205;
    path(g,[[x,y],[x+20,y-15],[x+35,y+7],[x+8,y+22]],i%2?"#b9a48d":"#706251",null,0);
  }
  formation(g,{preset:"ottomanElite",rows:3,cols:15,x0:.08,x1:.76,yFront:.99,yBack:.69,hFront:.21,hBack:.08,face:"determined",march:.5,seed:54,t});
  formation(g,{preset:"byzantineGuard",rows:2,cols:12,x0:.67,x1:.99,yFront:.60,yBack:.49,hFront:.13,hBack:.07,face:"worried",seed:57,t,flip:true});
  for(let i=0;i<4;i++)drawLadder(g,1190+i*168,835,390+Math.sin(t*1.8+i)*22,t,i);
  for(let i=0;i<12;i++){dust(g,t,1160+i*72,870,90+i,32,"#d3b48e");smoke(g,t+i*.22,1280+i*58,470,220+i);}
  drawPeople(g,t,info,[
    {preset:"ottomanElite",x:.22,y:.92,h:.48,face:"determined",pose:"run",walk:true,speed:.36},
    {preset:"ottomanElite",x:.48,y:.91,h:.51,face:"focused",pose:beat==="breach"?"push":"climb",walk:true,speed:.26},
    {preset:"byzantineGuard",x:.83,y:.60,h:.36,face:"worried",pose:"brace",flip:true}
  ],.94,.49);
}

function drawEliteReserve(g,t,info,a){
  const beat=a.beat||"reserve";
  gradient(g,0,H(),[[0,"#9e9184"],[.38,"#c9b18b"],[1,"#433329"]]);
  path(g,[[0,520],[230,465],[480,505],[720,435],[950,480],[1190,430],[1450,485],[1700,430],[1920,470],[1920,1080],[0,1080]],"#655b50",null,0);
  // Reserve troops held behind the first two waves; distinct formation from massed infantry.
  formation(g,{preset:"ottomanElite",rows:4,cols:18,x0:.08,x1:.92,yFront:.95,yBack:.68,hFront:.18,hBack:.075,face:"determined",march:beat==="advance"?.22:0,seed:66,t});
  for(let i=0;i<6;i++){
    const x=220+i*292;
    flag(g,x,520,170,{color:RED,t,lw:3});
    line(g,[[x,520],[x,430]],"#3d2b20",5);
  }
  drawPeople(g,t,info,[{preset:"ottomanCommander",x:.52,y:.79,h:.53,face:"determined",pose:"point"},
    {preset:"ottomanElite",x:.18,y:.94,h:.39,face:"neutral",pose:"guard",flip:true},
    {preset:"ottomanElite",x:.82,y:.94,h:.39,face:"neutral",pose:"guard"}],.94,.45);
  if(beat==="command"){glow(g,980,570,120,"#f2c37b",.22);}
}
function drawDefenderIdentity(g,t,info,a){
  const beat=a.beat||"among_thousands";
  gradient(g,0,H(),[[0,"#29333b"],[.36,"#8c816d"],[1,"#3c3027"]]);
  wallBase(g,t,.18);
  formation(g,{preset:"byzantineGuard",rows:5,cols:19,x0:.02,x1:.98,yFront:.84,yBack:.58,hFront:.12,hBack:.045,face:"tired",seed:88,t});
  for(let i=0;i<14;i++){const x=50+i*140,y=430+(i%4)*38;glow(g,x,y,50,"#d8a36a",.12);}
  drawHero(g,t,info,{x:beat==="alone"?.50:.32,y:1.02,h:beat==="alone"?.93:.78,
    face:beat==="alone"?"tired":"determined",pose:beat==="resolve"?"point":"guard",
    weapon:"spear",shield:{type:"round",color:"#536b83",charge:"cross",chargeColor:"#d1ad68"},
    poseAt:[[0,"guard"],[.9,"look"],[1.8,"point"]],faceAt:[[0,"tired"],[.9,"worried"],[1.8,"determined"]]});
  if(beat==="alone"){
    const vg=g.createRadialGradient(960,660,80,960,660,790);
    vg.addColorStop(0,"rgba(255,219,167,.14)");vg.addColorStop(1,"rgba(4,8,14,.64)");
    g.fillStyle=vg;g.fillRect(0,0,W(),H());
  }
}
function drawDefenderSupply(g,t,info,a){
  const beat=a.beat||"water";
  gradient(g,0,H(),[[0,"#343b43"],[.42,"#77776f"],[1,"#4c4133"]]);
  wallBase(g,t,.34);
  if(beat==="water"){
    path(g,[[250,920],[280,770],[415,770],[445,920]],"#61472f","#251e18",9);
    path(g,[[282,798],[412,798],[398,842],[296,842]],"#273a41",null,0);
    for(let i=0;i<7;i++)line(g,[[288+i*17,842],[295+i*17,875+Math.sin(t*3+i)*6]],"#83a6aa",4,.6);
    for(let i=0;i<3;i++){const x=1050+i*250,y=855;path(g,[[x-30,y],[x-22,y-83],[x+22,y-83],[x+30,y]],"#82613f","#302318",6);line(g,[[x-26,y-62],[x+26,y-62]],"#bd9b6b",5);}
    drawPeople(g,t,info,[{preset:"byzantineGuard",x:.18,y:.99,h:.49,face:"tired",pose:"carry",walk:true,dir:1,speed:.18},
      {preset:"byzantineYou",x:.52,y:.99,h:.61,face:"determined",pose:"carry",walk:true,dir:1,speed:.2},
      {preset:"byzantineGuard",x:.82,y:.98,h:.43,face:"worried",pose:"carry",walk:true,dir:-1,speed:.16}],.94,.5);
  } else if(beat==="stones"){
    for(let i=0;i<30;i++){
      const x=1040+(i*41)%360,y=880-Math.floor(i/8)*36+(i%3)*7;
      path(g,[[x-18,y],[x-9,y-18],[x+11,y-22],[x+23,y-4],[x+14,y+7],[x-13,y+8]],i%2?"#6d675e":"#b1a18a","#3a342e",2);
    }
    drawPeople(g,t,info,[{preset:"byzantineGuard",x:.22,y:.98,h:.45,face:"strained",pose:"carry",walk:true,dir:1,speed:.16},
      {preset:"byzantineYou",x:.52,y:.99,h:.61,face:"determined",pose:"push",walk:true,dir:1,speed:.18},
      {preset:"byzantineGuard",x:.80,y:.98,h:.43,face:"focused",pose:"brace"}],.94,.5);
  } else if(beat==="arrows"){
    for(let i=0;i<5;i++){const x=1190+i*80;line(g,[[x,865],[x+120,785]],"#735232",8);for(let j=0;j<5;j++)line(g,[[x+j*8,870],[x+44+j*8,840]],"#bd9d70",3,.7);}
    drawPeople(g,t,info,[{preset:"byzantineArcher",x:.23,y:.97,h:.48,face:"focused",pose:"aim"},
      {preset:"byzantineYou",x:.54,y:.99,h:.60,face:"determined",pose:"carry",walk:true,dir:1,speed:.21},
      {preset:"byzantineGuard",x:.84,y:.97,h:.44,face:"worried",pose:"guard"}],.94,.5);
  } else {
    glow(g,1520,610,180,"#e5a15b",.18);
    drawPeople(g,t,info,[{preset:"byzantineGuard",x:.22,y:.98,h:.42,face:"worried",pose:"point"},
      {preset:"byzantineYou",x:.52,y:.99,h:.63,face:"urgent",pose:"run",walk:true,dir:1,speed:.52},
      {preset:"byzantineGuard",x:.83,y:.97,h:.44,face:"focused",pose:"guard",flip:true}],.94,.5);
    path(g,[[1020,730],[1110,690],[1180,710],[1240,645]],"#9b784d","#33261a",5);line(g,[[1180,710],[1240,645]],"#d2b78d",4);
    for(let i=0;i<7;i++)dust(g,t,1040+i*78,940,120+i,18,"#bda37f");
  }
}
function drawRewindMap(g,t,info,a){
  const beat=a.beat||"route";
  g.fillStyle="#c9b48d";g.fillRect(0,0,W(),H());
  for(let i=0;i<42;i++){const x=(i*173)%W(),y=(i*251)%H();circle(g,x,y,12+(i%4)*8,"rgba(92,67,43,.035)");}
  path(g,[[0,0],[W(),0],[W(),170],[1570,205],[1390,180],[1210,212],[980,185],[740,225],[500,190],[250,220],[0,185]],"#ae9872",null,0);
  // Schematic Bosphorus / Golden Horn coastlines; not a measured nautical chart.
  path(g,[[1080,120],[1040,300],[1110,465],[1040,650],[1110,835],[1040,1080]],"#52798a",null,0);
  path(g,[[1070,500],[850,460],[690,500],[510,470],[320,520],[130,480]],"#52798a",null,0);
  path(g,[[620,420],[760,360],[900,385],[1000,465],[970,610],[850,700],[670,680],[550,575],[565,470]],"#a18b69","#4b3b2b",9);
  for(let i=0;i<14;i++){const x=590+i*27,y=430+(i%4)*70;path(g,[[x,y],[x+18,y-10],[x+27,y+8],[x+4,y+18]],"#665342",null,0);}
  for(let i=0;i<8;i++){const x=210+i*96,y=300+(i%3)*55;path(g,[[x,y],[x+28,y-12],[x+40,y+13],[x+8,y+23]],"#9a493a","#493021",3);}
  line(g,[[250,380],[460,420],[590,500]],"#9c493c",12,.8);
  for(let i=0;i<8;i++)circle(g,260+i*43,383+i*13,8,"#9c493c");
  g.save();g.textAlign="center";g.fillStyle="#403020";g.font="bold 56px Georgia,serif";
  g.fillText(beat==="date"?"6 APRIL 1453":"THE SIEGE OF CONSTANTINOPLE",960,140);
  g.font="bold 28px Georgia,serif";g.fillStyle="#57452f";
  g.fillText("BOSPHORUS",1275,375);g.fillText("GOLDEN HORN",430,580);g.fillText("CONSTANTINOPLE",770,780);g.restore();
  if(beat==="route"){const q=(t*.32)%1,x=250+q*365,y=380+q*120;glow(g,x,y,70,"#d3a35e",.32);circle(g,x,y,13,"#9c493c");line(g,[[250,380],[x,y]],"#9c493c",7,.9);}
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
registerTemplate('night_wall_watch',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightWallWatch(g,lt,info,a));}});
registerTemplate('night_camp',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightCamp(g,lt,info,a));}});
registerTemplate('night_camp_detail',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightCampDetail(g,lt,info,a));}});
registerTemplate('night_guns',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightGuns(g,lt,info,a));}});
registerTemplate('night_gun_crew',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightGunCrew(g,lt,info,a));}});
registerTemplate('night_gun_crew_detail',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawNightGunCrewDetail(g,lt,info,a));}});
registerTemplate('assault_waves',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawAssaultWaves(g,lt,info,a));}});
registerTemplate('assault_first_wave',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawAssaultFirstWave(g,lt,info,a));}});
registerTemplate('assault_second_wave',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawAssaultSecondWave(g,lt,info,a));}});
registerTemplate('elite_reserve',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawEliteReserve(g,lt,info,a));}});
registerTemplate('defender_identity',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawDefenderIdentity(g,lt,info,a));}});
registerTemplate('defender_supply',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawDefenderSupply(g,lt,info,a));}});
registerTemplate('rewind_map',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>drawRewindMap(g,lt,info,a));}});
registerTemplate('final_night',{draw(g,lt,info){const a=info.args||{};camera(g,lt,info,()=>{drawNightWatch(g,lt,info);if(a.beat==='dawn')gradient(g,0,H(),[[0,'rgba(189,126,83,0)'],[.45,'rgba(209,151,101,.22)'],[1,'rgba(24,27,34,0)']]);});}});
registerTemplate('gun_crew',{draw(g,lt,info){camera(g,lt,info,()=>drawGunCrew(g,lt,info,info.args||{}));}});
registerTemplate('repair_wall',{draw(g,lt,info){camera(g,lt,info,()=>drawRepairWall(g,lt,info,info.args||{}));}});
registerTemplate('golden_horn',{draw(g,lt,info){camera(g,lt,info,()=>drawGoldenHorn(g,lt,info,info.args||{}));}});
registerTemplate('tunnel_cutaway',{draw(g,lt,info){camera(g,lt,info,()=>drawTunnelCutaway(g,lt,info,info.args||{}));}});
registerTemplate('church_refuge',{draw(g,lt,info){camera(g,lt,info,()=>drawChurchRefuge(g,lt,info,info.args||{}));}});
