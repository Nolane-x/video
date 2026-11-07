#!/usr/bin/env python3
"""Author varied, voice-timed H2 Squire scenes for the Ain Jalut long-form film."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path

VALID_TEMPLATES={"scene","close","army","top","plan","map","board","item","split","title","black"}
MAMLUK="#41677f"
MONGOL="#a6533b"
PAPER="#d7c39b"

def load(path:Path,default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def choose_template(text:str,index:int,progress:float,usage:dict,last_at:dict,last_template:str|None)->str:
    t=text.casefold()
    def available(name,cap,gap=4):
        return usage.get(name,0)<cap and index-last_at.get(name,-999)>=gap and last_template!=name
    if index==0:
        return "scene"
    if "baghdad" in t and available("title",2,18):
        return "title"
    if any(k in t for k in ("ayn jalut","gaza","acre","damascus","aleppo","cairo","baghdad","jezreel valley")) and available("map",4,12):
        return "map"
    if any(k in t for k in ("smaller detachment","succession crisis","main army","two forces","equipment and methods","more heavily armoured")) and available("board",4,7):
        return "board"
    if any(k in t for k in ("feigned retreat","reserve","counterattack","line has opened","formation","flank","withdraw","close combat","pursue","pursuit")) and available("top",14,4):
        return "top"
    if any(k in t for k in ("remember one rule","remember the rule","the real answer","the strategic fact","the lesson","the opportunity")) and available("plan",8,5):
        return "plan"
    if any(k in t for k in ("bowstring","arrow","shield","lance","saddle","armour","armor","quiver","sword","mace","water skin")) and available("item",14,4):
        return "item"
    if any(k in t for k in ("qutuz","baybars","kitbuqa","hülegü","hulegu","mongke","möngke","you are","you tighten","you raise")) and available("close",32,3):
        return "close"
    if any(k in t for k in ("horse","mounted","cavalry","riders","horse archer","gallop")) and available("army",24,3):
        return "army"
    seq=("scene","army","close","scene","item","top","scene","split","army","close","plan","scene")
    pick=seq[index%len(seq)]
    if pick==last_template:
        pick="scene" if last_template!="scene" else "army"
    caps={"army":24,"close":32,"top":14,"plan":8,"split":8,"item":14,"map":4,"board":4,"title":2}
    if pick in caps and not available(pick,caps[pick],4):
        pick="scene"
    return pick

def cue(sfx_root:Path,*names,at:float=0.25,gain:int=-9):
    for name in names:
        if (sfx_root/f"{name}.wav").is_file():
            return [{"name":name,"at":at,"gain":gain}]
    return []

def mamluk_person(x=.5,y=.72,h=.44,face="determined",pose="guard",horse=None,weapon="spear",flip=False):
    p={"preset":"knight12","helmet":"turban","body":"mail","tunicColor":MAMLUK,
       "cape":"#34566b","legs":"mail","x":x,"y":y,"h":h,"face":face,"pose":pose,
       "weapon":weapon,"flip":flip,
       "shield":{"type":"round","color":MAMLUK,"charge":"star","chargeColor":PAPER}}
    if horse: p["horse"]=horse
    return p

def mongol_person(x=.5,y=.72,h=.42,face="determined",pose="guard",horse=None,flip=False):
    p={"preset":"englishArcher","helmet":"cap","body":"gambeson","tunicColor":MONGOL,
       "scarf":"#78412f","x":x,"y":y,"h":h,"face":face,"pose":pose,
       "weapon":"bow","shield":None,"flip":flip}
    if horse: p["horse"]=horse
    return p

def base_args(tpl:str,text:str,index:int,progress:float,sfx_root:Path):
    low=text.casefold()
    rng=random.Random(1260+index*7919)
    time="dawn" if progress<.12 else ("golden" if progress<.45 else ("day" if progress<.76 else "dusk"))
    if tpl=="map":
        args={
            "view":[28.0,24.0,47.2,40.5],
            "places":[
                {"text":"Cairo","lon":31.2357,"lat":30.0444},
                {"text":"Gaza","lon":34.4668,"lat":31.5017},
                {"text":"Acre","lon":35.0818,"lat":32.9271},
                {"text":"Damascus","lon":36.2765,"lat":33.5138},
                {"text":"Aleppo","lon":37.15,"lat":36.2},
                {"text":"Baghdad","lon":44.3661,"lat":33.3152},
                {"text":"Ayn Jalut (approx.)","lon":35.35,"lat":32.55}
            ],
            "routes":[
                {"pts":[[44.36,33.31],[40.5,34.1],[37.15,36.2],[36.27,33.51]],"at":0.3,"dur":1.2},
                {"pts":[[31.23,30.04],[32.6,30.5],[34.46,31.5],[35.35,32.55]],"at":1.0,"dur":1.4}
            ],
            "troops":[
                {"lon":36.1,"lat":33.7,"side":"red","at":0.7},
                {"lon":34.8,"lat":32.0,"side":"blue","at":1.1}
            ],
            "move":"in","moveAmt":0.022
        }
        return args,cue(sfx_root,"wind_loop","wind_loop",at=.1,gain=-12)
    if tpl=="board":
        args={
            "title":"THE WINDOW",
            "bars":[
                {"label":"HÜLEGÜ","v":1.0,"top":"MAIN FORCE EAST","at":.2},
                {"label":"KITBUQA","v":1.0,"top":"WESTERN DETACHMENT","at":.7}
            ],
            "mult":{"text":"THE BALANCE CHANGES","x":.5,"y":.35,"at":1.0},
            "labels":[{"text":"NO EXACT MUSTER SURVIVES","x":.5,"y":.18,"size":27,"at":.2,"color":"#f0dfbf"}]
        }
        return args,cue(sfx_root,"battle_roar","wind_loop",at=.15,gain=-11)
    if tpl=="top":
        battle=any(k in low for k in ("battle","line","retreat","counterattack","reserve","surrounded","pursue","formation","flank"))
        if "retreat" in low or "gave ground" in low or "withdraw" in low:
            labels=[{"text":"ONE ACCOUNT","x":.25,"y":.1,"size":32,"at":.2,"color":MONGOL},
                    {"text":"ALTERNATIVE ACCOUNTS","x":.72,"y":.1,"size":29,"at":.8,"color":MAMLUK}]
            blocks=[
                {"x":.35,"y":.48,"w":.22,"h":.27,"cols":9,"rows":8,"cell":.018,"side":"blue","path":[[0,.35,.48],[1.6,.48,.54]]},
                {"x":.69,"y":.44,"w":.17,"h":.35,"cols":7,"rows":13,"cell":.018,"side":"red","path":[[0,.69,.44],[1.8,.58,.46]]}
            ]
            arrows=[{"from":[.47,.5],"to":[.36,.5],"at":.5,"color":MAMLUK},{"from":[.64,.42],"to":[.52,.5],"at":1.15,"color":MONGOL}]
        elif "reserve" in low or "counterattack" in low or "qutuz" in low:
            labels=[{"text":"MAMLUK RESERVE","x":.5,"y":.1,"size":34,"at":.2,"color":MAMLUK},
                    {"text":"COUNTERATTACK","x":.5,"y":.88,"size":34,"at":1.2,"color":MONGOL}]
            blocks=[
                {"x":.5,"y":.69,"w":.24,"h":.19,"cols":10,"rows":6,"cell":.018,"side":"blue","path":[[0,.5,.69],[1.8,.5,.52]]},
                {"x":.5,"y":.39,"w":.35,"h":.22,"cols":13,"rows":8,"cell":.017,"side":"red"},
                {"x":.2,"y":.47,"w":.14,"h":.28,"cols":6,"rows":10,"cell":.018,"side":"red"},
                {"x":.8,"y":.47,"w":.14,"h":.28,"cols":6,"rows":10,"cell":.018,"side":"red"}
            ]
            arrows=[{"from":[.5,.78],"to":[.5,.56],"at":.55,"color":MAMLUK}]
        else:
            labels=[{"text":"MAMLUKS","x":.22,"y":.1,"size":34,"at":.25,"color":MAMLUK},
                    {"text":"MONGOLS","x":.78,"y":.1,"size":34,"at":.65,"color":MONGOL}]
            blocks=[
                {"x":.5,"y":.52,"w":.28,"h":.28,"cols":11,"rows":10,"cell":.017,"side":"blue","face":1},
                {"x":.18,"y":.46,"w":.17,"h":.26,"cols":7,"rows":10,"cell":.018,"side":"red","path":[[0,.18,.46],[1.6,.38,.5]]},
                {"x":.82,"y":.46,"w":.17,"h":.26,"cols":7,"rows":10,"cell":.018,"side":"red","path":[[0,.82,.46],[1.6,.62,.5]]}
            ]
            arrows=[{"from":[.18,.46],"to":[.38,.5],"at":.6,"color":MONGOL},{"from":[.82,.46],"to":[.62,.5],"at":1.0,"color":MONGOL}]
        args={"ground":{"color":"#c6a878","grass":True,"rocks":True},"blocks":blocks,"zones":[{"x":.5,"y":.52,"w":.6,"h":.48,"color":"#7c533b","at":.1,"dur":.7,"dashed":True}],"arrows":arrows,"labels":labels,"move":"in"}
        return args,cue(sfx_root,"battle_roar","wind_loop",at=.3,gain=-14)
    if tpl=="plan":
        args={
            "paper":"parchment",
            "zones":[
                {"x":.5,"y":.5,"w":.64,"h":.45,"color":"#9d8a66","at":.2,"dur":.6},
                {"x":.5,"y":.5,"w":.28,"h":.23,"color":"#41677f","at":.8,"dur":.7,"dashed":True}
            ],
            "blocks":[
                {"x":.23,"y":.46,"w":.14,"h":.24,"side":"red","cols":6,"rows":9,"at":.2},
                {"x":.5,"y":.46,"w":.2,"h":.16,"side":"blue","cols":9,"rows":6,"at":.5},
                {"x":.77,"y":.46,"w":.14,"h":.24,"side":"red","cols":6,"rows":9,"at":.8}
            ],
            "arrows":[
                {"from":[.23,.68],"to":[.43,.55],"at":1.0,"color":MONGOL},
                {"from":[.77,.68],"to":[.57,.55],"at":1.3,"color":MONGOL}
            ],
            "labels":[
                {"text":"TIMING","x":.5,"y":.18,"size":46,"at":.4,"color":"#2a2117"},
                {"text":"RESERVES","x":.5,"y":.8,"size":34,"at":1.1,"color":"#2a2117"}
            ]
        }
        return args,cue(sfx_root,"wind_loop","wind_loop",at=.1,gain=-12)
    if tpl=="army":
        bg="hills" if index%2 else "field"
        mounted=any(k in low for k in ("horse","cavalry","rider","mounted","gallop"))
        if mounted:
            args={
                "bg":bg,"time":time,
                "bgOpts":{"volcano":False,"trees":3,"bushes":3,"flags":[{"x":.12,"color":MAMLUK},{"x":.86,"color":MONGOL}]},
                "back":[{"preset":"englishArcher","rows":2,"cols":13,"x0":.04,"x1":.96,"yFront":.82,"yBack":.68,"hFront":.13,"hBack":.07,"flip":True}],
                "mid":[{"preset":"greek","rows":2,"cols":10,"x0":.02,"x1":.53,"yFront":.96,"yBack":.78,"hFront":.22,"hBack":.12,"march":.28,"face":"determined"},
                       {"preset":"englishArcher","rows":2,"cols":10,"x0":.48,"x1":.98,"yFront":.93,"yBack":.76,"hFront":.2,"hBack":.11,"march":.34,"flip":True,"face":"determined"}],
                "people":[
                    mamluk_person(.29,.68,.40,"determined","guard",{"color":"chestnut","gait":"gallop","travel":False},"spear"),
                    mongol_person(.73,.7,.38,"determined","guard",{"color":"bay","gait":"gallop","travel":False},True)
                ],
                "fx":[{"kind":"dust","at":.2,"x":.52,"y":.84,"s":.18}],
                "move":("left","right","in","out")[index%4]
            }
            return args,cue(sfx_root,"hooves_gallop","wind_loop",at=.2,gain=-7)
        args={
            "bg":bg,"time":time,
            "bgOpts":{"volcano":False,"trees":4,"bushes":4,"tents":2,"flags":[{"x":.12,"color":MAMLUK},{"x":.86,"color":MONGOL}]},
            "mid":[
                {"preset":"greek","presets":["greek","knight12"],"rows":3,"cols":12,"x0":.02,"x1":.49,"yFront":.97,"yBack":.7,"hFront":.25,"hBack":.09,"march":.22},
                {"preset":"englishArcher","rows":3,"cols":12,"x0":.52,"x1":.98,"yFront":.94,"yBack":.7,"hFront":.23,"hBack":.09,"march":.24,"flip":True}
            ],
            "people":[mamluk_person(.25,.72,.42,"determined","point"),mongol_person(.78,.74,.38,"determined","guard",None,True)],
            "move":("in","left","out","right")[index%4]
        }
        return args,cue(sfx_root,"battle_roar","wind_loop",at=.3,gain=-14)
    if tpl=="close":
        mongol=any(k in low for k in ("mongol","kitbuqa","hülegü","hulegu","horse archer","mongke","möngke"))
        face="worried" if any(k in low for k in ("danger","fear","arrow","falling","trap","wounded","crush","battle")) else "determined"
        main=mongol_person(.48,.52,.4,face,"guard") if mongol else mamluk_person(.48,.52,.42,face,"guard")
        main["R"]=.235
        main.pop("h",None)
        main["y"]=.52
        other=mamluk_person(.83,.7,.25,"worried","guard",None,True) if mongol else mongol_person(.83,.7,.25,"worried","guard",None,True)
        other.pop("h",None); other["R"]=.14
        args={
            **main,
            "bg":"tent" if any(k in low for k in ("camp","command","cairo","qutuz","baybars")) else ("castle" if "baghdad" in low else "hills"),
            "time":time,
            "bgOpts":{"volcano":False,"trees":2,"flags":[{"x":.14,"color":MAMLUK},{"x":.86,"color":MONGOL}],"tents":2},
            "others":[other],
            "move":("in","left","out","right")[index%4],
            "fx":[{"kind":"dust","at":.4,"x":.78,"y":.8,"s":.1}] if progress>.35 else []
        }
        if "qutuz" in low: args["signs"]=[{"text":"QUTUZ","x":.5,"y":.13,"at":.2,"size":38,"tail":"down"}]
        if "baybars" in low: args["signs"]=[{"text":"BAYBARS","x":.5,"y":.13,"at":.2,"size":38,"tail":"down"}]
        return args,cue(sfx_root,"sword_clash","battle_roar",at=.28,gain=-12)
    if tpl=="item":
        if "bow" in low or "arrow" in low or "archer" in low:
            thing="bow"
        elif "helmet" in low:
            thing="helmet"
        elif "shield" in low:
            thing="shield"
        elif "saddle" in low or "horse" in low:
            thing="horse"
        elif "spear" in low or "lance" in low:
            thing="spear"
        else:
            thing="sword"
        args={"thing":{"kind":thing,"s":.58,"anim":"grow" if index%2 else "pop"},"bg":"plain","time":time,"sway":True,
              "props":[{"kind":"arrow","x":.2,"y":.78,"s":.22,"rot":-.35}] if thing in ("bow","arrow") else []}
        return args,cue(sfx_root,"arrow_whoosh" if thing in ("bow","arrow") else "sword_clash","wind_loop",at=.25,gain=-10)
    if tpl=="split":
        args={
            "left":{"color":MAMLUK,"people":[mamluk_person(.28,.78,.62,"determined","guard")]},
            "right":{"color":MONGOL,"people":[mongol_person(.72,.78,.62,"determined","guard",None,True)]},
            "labels":[{"text":"MAMLUKS","x":.25,"y":.15,"size":58,"at":.2,"color":MAMLUK},{"text":"MONGOLS","x":.75,"y":.15,"size":58,"at":.7,"color":MONGOL}],
            "move":"in"
        }
        return args,cue(sfx_root,"wind_loop","wind_loop",at=.2,gain=-12)
    if tpl=="title":
        if "baghdad" in low:
            return {"text":"BAGHDAD\n1258","sub":"THE MONGOL ADVANCE","bg":"castle","time":"dusk","dim":.18},cue(sfx_root,"wind_loop","wind_loop",at=.1,gain=-12)
        return {"text":"AYN JALUT\n1260","sub":"THE BATTLE IN THE VALLEY","bg":"hills","time":"dawn","dim":.15},cue(sfx_root,"wind_loop","wind_loop",at=.1,gain=-12)
    if tpl=="black":
        return {},[]
    # Scene is the lived, narrative default. Choose a purposeful environment.
    if "baghdad" in low or "caliph" in low or "library" in low:
        bg="castle"; tod="dusk"
        people=[{"preset":"senator","x":.33,"y":.76,"h":.4,"face":"worried","pose":"guard"},
                {"preset":"peasant","x":.72,"y":.78,"h":.35,"face":"worried","pose":"guard","flip":True}]
        back=[{"preset":"englishArcher","rows":2,"cols":12,"x0":.04,"x1":.96,"yFront":.8,"yBack":.66,"hFront":.12,"hBack":.06,"flip":True}]
        props=[{"kind":"scroll","x":.16,"y":.86,"s":.17},{"kind":"torch","x":.88,"y":.76,"s":.2}]
        fx=[{"kind":"smoke","at":.5,"x":.75,"y":.4,"s":.18}]
    elif "cairo" in low or "camp" in low or "supply" in low or "march" in low or "water" in low:
        bg="tent"; tod="golden"
        people=[mamluk_person(.34,.76,.43,"determined","point"),
                mamluk_person(.74,.78,.34,"neutral","guard",None,True)]
        back=[{"preset":"greek","rows":2,"cols":10,"x0":.04,"x1":.96,"yFront":.82,"yBack":.69,"hFront":.13,"hBack":.07}]
        props=[{"kind":"scroll","x":.82,"y":.85,"s":.16},{"kind":"barrel","x":.16,"y":.87,"s":.14}]
        fx=[]
    elif "battle" in low or "arrow" in low or "line" in low or "dust" in low:
        bg="hills"; tod="day"
        people=[mamluk_person(.27,.7,.46,"worried","guard",{"color":"chestnut","gait":"gallop","travel":False},"spear"),
                mongol_person(.75,.72,.4,"determined","guard",{"color":"bay","gait":"gallop","travel":False},True)]
        back=[{"preset":"englishArcher","rows":3,"cols":16,"x0":.02,"x1":.98,"yFront":.82,"yBack":.62,"hFront":.15,"hBack":.07,"flip":True}]
        props=[]
        fx=[{"kind":"dust","at":.2,"x":.5,"y":.83,"s":.2}]
    elif "death" in low or "assassinated" in low or "aftermath" in low:
        bg="field"; tod="dusk"
        people=[mamluk_person(.38,.82,.46,"worried","guard"),
                {"preset":"greek","x":.76,"y":.85,"h":.32,"face":"worried","pose":"guard","flip":True}]
        back=[]
        props=[{"kind":"shield","type":"round","x":.2,"y":.87,"s":.18,"rot":-.4},{"kind":"standard","x":.86,"y":.82,"s":.23}]
        fx=[{"kind":"smoke","at":.2,"x":.72,"y":.44,"s":.18}]
    else:
        bg="field" if progress<.7 else "hills"; tod=time
        people=[mamluk_person(.33,.74,.43,"determined","guard"),
                mongol_person(.73,.75,.36,"determined","guard",None,True)]
        back=[{"preset":"greek","rows":2,"cols":10,"x0":.02,"x1":.47,"yFront":.84,"yBack":.68,"hFront":.14,"hBack":.07},
              {"preset":"englishArcher","rows":2,"cols":10,"x0":.53,"x1":.98,"yFront":.84,"yBack":.68,"hFront":.14,"hBack":.07,"flip":True}]
        props=[]
        fx=[{"kind":"dust","at":.35,"x":.5,"y":.82,"s":.12}]
    args={"bg":bg,"time":tod,"bgOpts":{"volcano":False,"trees":3,"bushes":3,"flags":[{"x":.12,"color":MAMLUK},{"x":.88,"color":MONGOL}],"tents":2 if bg=="tent" else 0},
          "people":people,"back":back,"props":props,"fx":fx,"move":("in","left","out","right")[index%4],"moveAmt":.025}
    return args,cue(sfx_root,"hooves_gallop" if "horse" in low or "cavalry" in low else "battle_roar","wind_loop",at=.25,gain=-13)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True)
    args=ap.parse_args()
    project=Path(args.project).resolve()
    path=project/"story"/"shots.json"
    story=load(path,{})
    shots=story.get("shots") or []
    if len(shots)<80:
        raise ValueError(f"Long-form voice timeline produced only {len(shots)} shots ({len(shots)} expected minimum 80)")
    duration=float(story.get("duration") or shots[-1]["end"])
    if duration<=600:
        raise ValueError(f"Voice timeline must exceed ten minutes; got {duration:.1f}s")
    sfx_root=project.parents[1]/"audio"/"sfx"
    usage={}; last_at={}; last=None
    for i,shot in enumerate(shots):
        text=str(shot.get("line") or "")
        start,end=float(shot["start"]),float(shot["end"])
        if end<=start:
            raise ValueError(f"Invalid shot duration: {shot.get('id')}")
        progress=((start+end)/2)/duration
        tpl=choose_template(text,i,progress,usage,last_at,last)
        visual,cues=base_args(tpl,text,i,progress,sfx_root)
        usage[tpl]=usage.get(tpl,0)+1; last_at[tpl]=i; last=tpl
        shot["tpl"]=tpl
        shot["args"]=visual
        shot["sfx"]=cues
        shot["in"]={"type":"fade" if i==0 else "cut"}
        if ("kitbuqa is killed" in text.casefold() or "you began this story" in text.casefold()):
            shot["notes"]="DROP"
        else:
            shot["notes"]="Historical reconstruction; Mamluk and Mongol costume palettes are illustrative, not authenticated uniform claims."
    templates={s["tpl"] for s in shots}
    if len(templates)<8:
        raise ValueError(f"Only {len(templates)} visual templates were authored: {sorted(templates)}")
    story["title"]="The Day the Mongols Were Stopped at Ain Jalut"
    story["genre"]="historical-military-animation"
    story["engine"]="H2 Squire 2D/vector"
    story["historical_caution"]="Medieval sources differ on the feigned-retreat narrative; exact force strengths and tactical movement are not treated as certain."
    story["shots"]=shots
    story["music"]=[
        {"start":0,"end":round(duration*.15,3),"bed":"ancient","gainDb":-2},
        {"start":round(duration*.15,3),"end":round(duration*.32,3),"bed":"medieval","gainDb":-2},
        {"start":round(duration*.32,3),"end":round(duration*.48,3),"bed":"suspense","gainDb":-2},
        {"start":round(duration*.48,3),"end":round(duration*.78,3),"bed":"war","gainDb":-1},
        {"start":round(duration*.78,3),"end":round(duration*.91,3),"bed":"somber","gainDb":-2},
        {"start":round(duration*.91,3),"end":round(duration,3),"bed":"mystery","gainDb":-2}
    ]
    path.write_text(json.dumps(story,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    cfg_path=project/"config.json"
    cfg=load(cfg_path,{})
    cfg.update({
        "title":"The Day the Mongols Were Stopped at Ain Jalut",
        "aspect":"16:9","resolution":"1080p","fps":24,"style":"flat",
        "captions":False,"bars":"none","pack":"squire","lang":"en",
        "music":{"enabled":True,"gainDb":-14},
        "sfx":{"enabled":True,"gainDb":-7},"loudness":-14,"duration":round(duration,3)
    })
    cfg_path.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    counts={k:sum(1 for s in shots if s["tpl"]==k) for k in sorted(templates)}
    print(f"AIN JALUT SHOTS: {len(shots)} | {len(templates)} templates | {duration:.1f}s | {counts}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
