import { thumb } from '/packs/squire/pack.js';
thumb({
  bg:'hills',time:'dusk',blur:5,wash:.02,
  bgOpts:{castle:true,castleX:.74,trees:2,tents:8,flags:[{x:.12,color:'#9c493c'},{x:.86,color:'#536b83'}]},
  back:[
    {preset:'greek',rows:5,cols:20,x0:.05,x1:.96,yFront:.8,yBack:.6,hFront:.14,hBack:.065,seed:1453},
    {preset:'englishArcher',rows:3,cols:18,x0:.04,x1:.96,yFront:.65,yBack:.54,hFront:.08,hBack:.04,seed:53}
  ],
  mid:[
    {preset:'greek',rows:2,cols:16,x0:.56,x1:.96,yFront:.84,yBack:.74,hFront:.18,hBack:.09,seed:29,flip:true}
  ],
  heroes:[
    {preset:'knight12',full:true,x:.79,y:.95,h:.82,body:'mail',helmet:'bascinet',beard:'short',tunicColor:'#536b83',tabard:true,tabardColor:'#536b83',face:'determined',weapon:'spear',flip:true},
    {preset:'englishArcher',full:true,x:.17,y:.94,h:.72,body:'gambeson',helmet:'cap',tunicColor:'#9c493c',face:'angry',weapon:'sword'}
  ],
  symbols:[
    {kind:'!',x:.51,y:.68,r:.25,color:'#e24c3c'},
    {kind:'arrow',x:.50,y:.28,to:[.75,.38],color:'#e3c28b',r:.17}
  ],
  title:[
    {text:'53 DAYS',x:.5,y:.15,size:.205,color:'#fff8e9'},
    {text:'TO THE END',x:.5,y:.34,size:.11,color:'#f0d19b'}
  ],
  tx:.5,ty:.15,tsize:.2,tcolor:'#fff8e9',align:'center'
});
