import { E, registerTemplate, clamp, lerp, ease, rng, alpha, noise, glow, circle, seg, poly, linGrad } from '/engine/core.js';
import { bg, formation, drawPeople, prop, drawThing, camera, overlays, flag, castle, cloud } from '/packs/squire/pack.js';

const W=()=>E.W, H=()=>E.H;
const BLUE='#536b83', RED='#9c493c', GOLD='#d1ad68', STONE='#b9a98c', INK='#241f20';

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
    {preset:'greek',x:.48,y:.91,h:.38,face:'worried',pose:'run',walk:true,dir:-1,speed:1.1,flip:true},
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
    {preset:'knight12',x:.47,y:.85,h:.52,face:'determined',pose:'guard'},
    {preset:'greek',x:.66,y:.86,h:.43,face:'neutral',pose:'point'},
    {preset:'greek',x:.33,y:.86,h:.40,face:'neutral',pose:'guard'}
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
  drawCity(g,t,{damage:a.damage??0.08,water:true,chain:!!a.chain});
  // near foreground parapet and watch post
  g.fillStyle='#7e6d58';g.fillRect(0,850,W(),230);
  for(let x=0;x<W();x+=85){g.fillStyle='#b29e7e';g.fillRect(x,820,55,65);}
  drawPeople(g,t,{dur:6,globalT:t,start:0,args:{}},[
    {preset:'greek',x:.27,y:.87,h:.40,face:'determined',pose:'guard'},
    {preset:'greek',x:.76,y:.88,h:.43,face:'worried',pose:'guard',flip:true}
  ],.93,.4);
  if(a.chain){line(g,[[250,950],[600,895],[960,910],[1280,860],[1620,900]],'#28292a',12);for(let i=0;i<24;i++)circle(g,260+i*58,940-Math.sin(i/23*Math.PI)*55,7,'#5d5c56');}
  overlays(g,t,{...a.info,dur:6,args:a});
}
registerTemplate('city_panorama',{draw(g,lt,info){camera(g,lt,info,()=>cityPanorama(g,lt,{...info.args,info}));}});
registerTemplate('command_camp',{draw(g,lt,info){camera(g,lt,info,()=>{drawCamp(g,lt);for(let i=0;i<8;i++)flag(g,80+i*250,620,140,{color:i%2?RED:BLUE,t:lt,lw:2});dust(g,lt,1200,870,88,40);});}});
registerTemplate('city_interior',{draw(g,lt,info){camera(g,lt,info,()=>drawCityInterior(g,lt));}});
registerTemplate('wall_battery',{draw(g,lt,info){
  const a=info.args||{},fireAt=a.fireAt??.52,age=lt-fireAt,impact=fireAt+1.02;
  camera(g,lt,info,()=>{
    wallBase(g,lt,lt>impact?clamp((lt-impact)/.35):0);
    // two defensive formations in depth
    formation(g,{preset:'greek',rows:3,cols:17,x0:.56,x1:.99,yFront:.78,yBack:.61,hFront:.18,hBack:.075,face:'determined',seed:71,t:lt,flip:true});
    cannon(g,330,870,1.5,age,age>=0);
    drawPeople(g,lt,info,[
      {preset:'greek',x:.18,y:.94,h:.39,face:'determined',pose:'run',walk:true,dir:1,speed:.65},
      {preset:'greek',x:.32,y:.94,h:.36,face:'worried',pose:'guard'},
      {preset:'greek',x:.49,y:.93,h:.42,face:'worried',pose:'run',walk:true,dir:1,speed:.4}
    ],.93,.42);
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
    formation(g,{preset:'greek',rows:3,cols:13,x0:.02,x1:.42,yFront:.98,yBack:.82,hFront:.16,hBack:.08,face:'determined',march:.55,seed:21,t:lt});
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
    formation(g,{preset:'greek',presets:['greek','knight12'],rows:5,cols:18,x0:.02,x1:.77,yFront:.99,yBack:.75,hFront:.20,hBack:.07,face:'determined',march:.24,seed:45,t:lt});
    formation(g,{preset:'englishArcher',rows:3,cols:14,x0:.05,x1:.71,yFront:.78,yBack:.66,hFront:.11,hBack:.06,face:'determined',seed:48,t:lt,flip:true});
    // ladders rise in staggered beats
    for(let i=0;i<5;i++){const x=1160+i*155, rise=clamp((lt-.35-i*.18)/1.15);drawLadder(g,x,810,330*rise,lt,i);}
    // attackers climbing at different phases
    const climbers=[];
    for(let i=0;i<7;i++){const q=clamp((lt-.7-i*.16)/2.0);climbers.push({preset:'greek',x:(.62+i*.055),y:.76-q*.29,h:.23,face:'determined',pose:'run',walk:true,dir:1,speed:.5,flip:true});}
    drawPeople(g,lt,info,climbers,.93,.25);
    // defenders at the parapet and falling masonry
    formation(g,{preset:'knight12',rows:2,cols:14,x0:.58,x1:.98,yFront:.46,yBack:.41,hFront:.12,hBack:.075,face:'worried',seed:81,t:lt,flip:true});
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
    for(let i=0;i<9;i++){const x=150+i*205;circle(g,x,900+Math.sin(lt+i)*3,4,'#c8b391');}
  });
}});
