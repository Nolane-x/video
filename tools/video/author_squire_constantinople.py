#!/usr/bin/env python3
"""Author a dense, event-specific H2 Squire film about the 1453 siege."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path

STANDARD={"scene","close","army","top","map","plan","board","item","split","title","black"}
CUSTOM={"city_panorama","command_camp","city_interior","wall_battery","relief_galleys","ship_portage","last_assault","aftermath_city"}
BLUE="#536b83"; RED="#9c493c"; GOLD="#d1ad68"

def load(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default

def cue(root, names, at=.25, gain=-9):
    for name in names:
        if (root/f"{name}.wav").is_file():
            return [{"name":name,"at":at,"gain":gain}]
    return []

def progress_phase(p, text):
    t=text.casefold()
    if p < .075 or any(k in t for k in ("final assault","last assault","janissar","ladder","before dawn","twenty-ninth of may")):
        return "final"
    if any(k in t for k in ("golden horn","chain","four christian ships","four ships","relief ships","convoy","harbour","harbor")):
        return "sea"
    if any(k in t for k in ("hauled overland","overland","rollers","ships are appearing inside","ships inside")):
        return "portage"
    if any(k in t for k in ("bombard","cannon","gun crew","stone shot","artillery","powder","wall is hit","impact")):
        return "guns"
    if any(k in t for k in ("giustiniani","constantine","emperor","defenders","repair crews","tunnel","countermin","wounded","food is rationed","churches")):
        return "inside"
    if any(k in t for k in ("mehmed","rumeli","bosporus","bosphorus","orban","sultan")):
        return "camp"
    if any(k in t for k in ("city","walls","constantinople","theodosian","capital","harbours","harbors")):
        return "city"
    if p > .88:
        return "aftermath"
    return ("city","camp","guns","sea","portage","inside","final")[int(p*1000)%7]

def choose_template(p, text, i, usage, last):
    phase=progress_phase(p,text)
    priority={
        "final":"last_assault","sea":"relief_galleys","portage":"ship_portage",
        "guns":"wall_battery","inside":"city_interior","camp":"command_camp",
        "city":"city_panorama","aftermath":"aftermath_city"
    }
    custom=priority[phase]
    # Keep a custom sequence dominant but vary scale and detail shots between hero actions.
    if i % 7 in (2,5) and phase in ("guns","final","inside"):
        return "close" if i%7==2 else "item"
    if i % 9 == 4 and phase in ("city","camp","sea","portage"):
        return "map" if phase in ("city","camp","portage") else "top"
    if i % 11 == 8 and phase in ("guns","final"):
        return "top"
    if i % 13 == 6 and phase in ("city","camp","inside"):
        return "split" if phase=="camp" else "plan"
    if last==custom and i%3==0:
        return "scene"
    return custom

def scene_args(phase,i,p,text):
    t=text.casefold()
    motion=("in","left","right","out","up","down")[i%6]
    cam={"move":motion,"moveAmt":.035 if i%3 else .055,"shake":.25 if phase in ("guns","final") and i%4==0 else 0}
    if phase=="city":
        return {**cam,"bg":"castle","time":"dawn" if p<.2 else "day","bgOpts":{"window":False,"torch":False,"trees":3,"bushes":3,"banner":{"color":BLUE}},"back":[{"preset":"byzantineGuard","rows":4,"cols":18,"x0":.02,"x1":.98,"yFront":.78,"yBack":.65,"hFront":.12,"hBack":.06,"seed":i+5}],"people":[{"preset":"byzantineGuard","x":.31,"y":.91,"h":.45,"face":"determined","pose":"guard"},{"preset":"peasant","x":.71,"y":.92,"h":.36,"face":"worried","pose":"walk","walk":True,"dir":-1}],"props":[{"kind":"shield","type":"round","x":.16,"y":.9,"s":.18},{"kind":"flag","x":.84,"y":.74,"s":.22,"color":BLUE}],"fx":[{"kind":"dust","at":.2,"x":.55,"y":.8,"s":.09}]}
    if phase=="camp":
        return {**cam,"bg":"tent","time":"golden","bgOpts":{"tents":5,"flags":[{"x":.14,"color":RED},{"x":.84,"color":RED}]},"people":[{"preset":"ottomanCommander","x":.47,"y":.76,"h":.52,"face":"determined","pose":"point"},{"preset":"ottomanElite","x":.72,"y":.81,"h":.37,"face":"neutral","pose":"guard"},{"preset":"ottomanElite","x":.2,"y":.82,"h":.36,"face":"neutral","pose":"guard","flip":True}],"props":[{"kind":"scroll","x":.8,"y":.9,"s":.17},{"kind":"barrel","x":.15,"y":.9,"s":.18}],"fx":[{"kind":"smoke","at":.1,"x":.65,"y":.38,"s":.1}]}
    if phase=="guns":
        return {**cam,"bg":"hills","time":"day","bgOpts":{"volcano":False,"trees":2,"bushes":2},"mid":[{"preset":"byzantineGuard","rows":3,"cols":13,"x0":.56,"x1":.98,"yFront":.8,"yBack":.65,"hFront":.15,"hBack":.07,"seed":i}],"people":[{"preset":"byzantineGuard","x":.19,"y":.91,"h":.43,"face":"determined","pose":"run","walk":True,"dir":1,"speed":.7},{"preset":"byzantineGuard","x":.34,"y":.92,"h":.38,"face":"worried","pose":"guard"}],"props":[{"kind":"cart","x":.33,"y":.88,"s":.32},{"kind":"barrel","x":.46,"y":.9,"s":.17}],"fx":[{"kind":"smoke","at":.4,"x":.42,"y":.6,"s":.15},{"kind":"dust","at":.5,"x":.71,"y":.82,"s":.16}]}
    if phase=="sea":
        return {**cam,"bg":"field","time":"dawn","bgOpts":{"trees":0,"bushes":0,"clouds":3},"people":[{"preset":"byzantineGuard","x":.26,"y":.85,"h":.37,"face":"worried","pose":"point"},{"preset":"byzantineGuard","x":.76,"y":.87,"h":.36,"face":"determined","pose":"guard"}],"props":[{"kind":"flag","x":.2,"y":.55,"s":.26,"color":BLUE},{"kind":"flag","x":.82,"y":.54,"s":.26,"color":RED}],"fx":[{"kind":"rain","at":.1,"len":.06,"n":42}]}
    if phase=="inside":
        return {**cam,"bg":"castle","time":"night" if i%2 else "dusk","bgOpts":{"window":True,"torch":True,"floorY":.78},"people":[{"preset":"byzantineGuard","x":.32,"y":.88,"h":.49,"face":"worried","pose":"guard"},{"preset":"peasant","x":.69,"y":.9,"h":.34,"face":"worried","pose":"run","walk":True,"dir":1},{"preset":"byzantineGuard","x":.84,"y":.9,"h":.37,"face":"neutral","pose":"guard"}],"props":[{"kind":"torch","x":.1,"y":.7,"s":.27},{"kind":"shield","type":"round","x":.86,"y":.82,"s":.2}],"fx":[{"kind":"smoke","at":.2,"x":.62,"y":.39,"s":.12}]}
    return {**cam,"bg":"hills","time":"dusk","bgOpts":{"trees":2,"flags":[{"x":.15,"color":BLUE},{"x":.85,"color":RED}]},"people":[{"preset":"byzantineGuard","x":.26,"y":.83,"h":.46,"face":"worried","pose":"guard"},{"preset":"knight12","x":.74,"y":.82,"h":.44,"face":"determined","pose":"guard","flip":True}],"mid":[{"preset":"byzantineGuard","rows":3,"cols":16,"x0":.02,"x1":.98,"yFront":.78,"yBack":.62,"hFront":.14,"hBack":.06,"seed":i+44}],"fx":[{"kind":"dust","at":.2,"x":.5,"y":.83,"s":.12}]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",required=True)
    args=ap.parse_args()
    project=Path(args.project).resolve()
    path=project/"story"/"shots.json"
    story=load(path,{})
    shots=story.get("shots") or []
    if len(shots)<350:
        raise ValueError(f"Expected at least 350 voice-timed shots, received {len(shots)}. Tighten shot drafting; do not pad with duplicate frames.")
    duration=float(story.get("duration") or shots[-1]["end"])
    if duration<650:
        raise ValueError(f"Long-form narration must exceed 10:50; got {duration:.1f}s.")
    if len(shots)>1100:
        raise ValueError(f"Shot count {len(shots)} is too high; protect readability and action comprehension.")
    sfx_root=project.parents[1]/"audio"/"sfx"
    usage={}; last=None
    transitions=("cut","cut","cut","whip","cut","flash","cut","zoom","cut","dip")
    for i,shot in enumerate(shots):
        start,end=float(shot["start"]),float(shot["end"])
        if end<=start: raise ValueError(f"Bad timing in {shot.get('id')}")
        p=((start+end)/2)/duration
        text=str(shot.get("line") or "")
        phase=progress_phase(p,text)
        tpl=choose_template(p,text,i,usage,last)
        if tpl in STANDARD:
            if tpl=="close":
                main={"preset":"byzantineGuard" if phase=="inside" else "knight12","x":.48,"y":.5,"R":.24,"face":"worried" if phase in ("final","inside","guns") else "determined","bg":"castle" if phase=="inside" else "hills","time":"dusk" if phase=="final" else "day","others":[{"preset":"byzantineGuard","x":.82,"y":.69,"R":.12,"face":"worried"}],"move":"in","moveAmt":.045}
                visual=main
            elif tpl=="item":
                thing="bow" if "arrow" in text.casefold() else ("helmet" if "helmet" in text.casefold() else ("shield" if "shield" in text.casefold() else ("sword" if "sword" in text.casefold() else "spear")))
                visual={"thing":{"kind":thing,"s":.62,"anim":"spin" if i%2 else "grow"},"bg":"plain","time":"golden","move":"in","moveAmt":.07,"props":[{"kind":"scroll","x":.18,"y":.8,"s":.18}]}
            elif tpl=="top":
                visual={"ground":{"color":"#b99f75","grass":True,"rocks":True},"blocks":[{"x":.48,"y":.57,"w":.26,"h":.28,"cols":11,"rows":10,"side":"blue","path":[[0,.48,.57],[1.1,.52,.54]]},{"x":.18,"y":.45,"w":.16,"h":.3,"cols":7,"rows":12,"side":"red","path":[[0,.18,.45],[1.4,.38,.5]]},{"x":.82,"y":.45,"w":.16,"h":.3,"cols":7,"rows":12,"side":"red","path":[[0,.82,.45],[1.4,.62,.5]]}],"arrows":[{"from":[.18,.45],"to":[.38,.5],"at":.35,"color":RED},{"from":[.82,.45],"to":[.62,.5],"at":.8,"color":RED}],"labels":[{"text":"DEFENCE UNDER PRESSURE","x":.5,"y":.12,"size":31,"at":.25,"color":"#f5e5c6"}],"move":"in"}
            elif tpl=="map":
                visual={"view":[25,37,35,45],"places":[{"text":"CONSTANTINOPLE","lon":28.9784,"lat":41.0082},{"text":"BOSPHORUS","lon":29.06,"lat":41.16},{"text":"GOLDEN HORN","lon":28.96,"lat":41.03},{"text":"RUMELI HISARI","lon":29.05,"lat":41.08}],"routes":[{"pts":[[29.05,41.08],[29.0,41.05],[28.98,41.02]],"at":.4,"dur":1.2}],"move":"in","moveAmt":.03}
            elif tpl=="plan":
                visual={"paper":"parchment","zones":[{"x":.5,"y":.5,"w":.72,"h":.45,"color":"#9b876b","at":.2,"dur":.7},{"x":.5,"y":.5,"w":.3,"h":.25,"color":BLUE,"at":.85,"dur":.55,"dashed":True}],"blocks":[{"x":.5,"y":.55,"w":.2,"h":.18,"side":"blue","cols":9,"rows":7,"at":.25},{"x":.2,"y":.47,"w":.14,"h":.24,"side":"red","cols":6,"rows":10,"at":.6},{"x":.8,"y":.47,"w":.14,"h":.24,"side":"red","cols":6,"rows":10,"at":.9}],"arrows":[{"from":[.2,.65],"to":[.42,.55],"at":.85,"color":RED}],"labels":[{"text":"THE DEFENCE","x":.5,"y":.18,"size":36,"at":.25,"color":"#2a2117"}]}
            elif tpl=="split":
                visual={"left":{"color":BLUE,"people":[{"preset":"byzantineGuard","x":.26,"y":.78,"h":.55,"face":"determined"}]},"right":{"color":RED,"people":[{"preset":"knight12","x":.74,"y":.78,"h":.55,"face":"determined"}]},"labels":[{"text":"DEFENDERS","x":.25,"y":.14,"size":43,"at":.2,"color":BLUE},{"text":"SIEGE ARMY","x":.75,"y":.14,"size":43,"at":.8,"color":RED}],"move":"in"}
            elif tpl=="army":
                visual={"bg":"hills","time":"day","rows":5,"cols":18,"preset":"byzantineGuard","enemy":"ottomanElite","march":.28,"flags":[{"x":.2,"color":BLUE},{"x":.8,"color":RED}],"move":"right","moveAmt":.055,"fx":[{"kind":"dust","at":.2,"x":.5,"y":.85,"s":.13}]}
            else:
                visual=scene_args(phase,i,p,text)
        else:
            visual={"move":("in","left","right","out","up","down")[i%6],"moveAmt":.035+(i%3)*.012}
            if tpl=="wall_battery":
                visual.update({"fireAt":.35+(i%4)*.1,"seed":i})
            elif tpl=="last_assault":
                visual.update({"moment":"breach" if i%3==0 else "climb","seed":i})
            elif tpl=="relief_galleys":
                visual.update({"label":"THE RELIEF CONVOY" if i%4==0 else ""})
            elif tpl=="ship_portage":
                visual.update({"seed":i})
            elif tpl=="city_panorama":
                visual.update({"chain":phase=="sea","damage":.12 if p>.25 else 0})
        shot["tpl"]=tpl
        shot["args"]=visual
        shot["in"]={"type":"fade","dur":.18} if i==0 else ({"type":transitions[i%len(transitions)],"dur":.13,"dir":1 if i%2 else -1} if transitions[i%len(transitions)]!="cut" else {"type":"cut"})
        shot["sfx"]=cue(sfx_root,["siege_impact","battle_roar","arrow_whoosh"] if tpl in {"last_assault","wall_battery"} else (["sword_clash","battle_roar"] if tpl in {"city_interior","command_camp"} else ["wind_loop"]),at=.18,gain=-12 if tpl not in {"last_assault","wall_battery"} else -8)
        shot["notes"]="Composite visual reconstruction; no invented eyewitness quotation or exact unverified tactical count."
        usage[tpl]=usage.get(tpl,0)+1; last=tpl
    custom_count=sum(usage.get(x,0) for x in CUSTOM)
    templates=sorted(usage)
    if custom_count<220: raise ValueError(f"Insufficient bespoke siege shots: {custom_count}")
    story["title"]="53 Days to the End of an Empire"
    story["genre"]="historical-military-animation"
    story["engine"]="H2 Squire 2D/vector — bespoke 1453 siege scenes"
    story["fps"]=240
    story["historical_caution"]="Composite narrator; disputed ship-portage details, final-assault sequence and Constantine XI death circumstances are stated cautiously."
    story["shot_counts"]=usage
    story["shots"]=shots
    story["music"]=[
      {"start":0,"end":round(duration*.08,3),"bed":"mystery","gainDb":-3},
      {"start":round(duration*.08,3),"end":round(duration*.28,3),"bed":"wonder","gainDb":-2},
      {"start":round(duration*.28,3),"end":round(duration*.48,3),"bed":"curious","gainDb":-2},
      {"start":round(duration*.48,3),"end":round(duration*.72,3),"bed":"tension","gainDb":-1},
      {"start":round(duration*.72,3),"end":round(duration*.91,3),"bed":"war","gainDb":-1},
      {"start":round(duration*.91,3),"end":round(duration,3),"bed":"emotional","gainDb":-3}
    ]
    path.write_text(json.dumps(story,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    cfg_path=project/"config.json"; cfg=load(cfg_path,{})
    cfg.update({"title":"53 Days to the End of an Empire","aspect":"16:9","resolution":"1080p","fps":240,"style":"flat","captions":True,"captionStyle":"squire","bars":"none","pack":"squire","lang":"en","music":{"enabled":True,"gainDb":-14},"sfx":{"enabled":True,"gainDb":-6},"loudness":-14,"maxrate":"48M","bufsize":"96M","crf":18,"renderPreset":"slow","duration":round(duration,3)})
    cfg_path.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"CONSTANTINOPLE HFR SHOTS: {len(shots)} | {duration:.1f}s | {custom_count} bespoke custom shots | {len(templates)} templates | 240fps native")
    print("SHOT COUNTS:",json.dumps(usage,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
