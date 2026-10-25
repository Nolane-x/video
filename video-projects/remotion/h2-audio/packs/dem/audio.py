"""H2 dem style pack: generated music and sound effects for wordless self-improvement films."""
import os, sys
import numpy as np, soundfile as sf
AUDIO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "audio")
sys.path.insert(0, AUDIO); os.chdir(AUDIO)
from synth import SR, t, norm, lp, hp, bp, reverb, save, ding, impact, whoosh, heartbeat, riser, rng
from music import render, piano, pad, sub, place, chord_freqs, pluck, kick, hat, CHORDS
CHORDS.update({"Cm":("C",[0,3,7]),"Ab":("G#",[0,4,7]),"Eb":("D#",[0,4,7]),"Bbs":("A#",[0,4,7]),"Am9":("A",[0,3,7,10,14]),"Fadd9":("F",[0,4,7,14])})
def mixp(a,b):
    n=max(len(a),len(b)); return np.pad(a,(0,n-len(a)))+np.pad(b,(0,n-len(b)))
def drone_bed(name,root_hz,d=72.0,beat_bpm=None,bells=True):
    n=int(d*SR); tt=np.arange(n)/SR; x=np.zeros(n)
    for k,a in ((1,1.0),(1.5,.35),(2,.5),(3,.18)):
        f=root_hz*k; ph=rng.uniform(0,6)
        x += a*(2*((f*(1+.002*np.sin(2*np.pi*.07*tt))*tt+ph)%1)-1)
    x=hp(lp(x,900,2),70)*(.75+.25*np.sin(2*np.pi*.05*tt))
    buf=np.stack([x,np.roll(x,900)],1)*.25
    if beat_bpm:
        hb=heartbeat(beat_bpm,int(d*beat_bpm/60)-1); L=min(len(hb),n); hb=hp(hb,45); buf[:L]+=np.stack([hb[:L],hb[:L]],1)*.35
    if bells:
        for s in np.arange(4,d-4,6.0): place(buf,ding(root_hz*8*rng.choice([1,1.2,1.5]),4.0,.3),s,.12,p=rng.uniform(-.6,.6))
    buf=reverb(buf,3.5,.4,3000)[:n]; f=int(2*SR); buf[:f]*=np.linspace(0,1,f)[:,None]; buf[-f:]*=np.linspace(1,0,f)[:,None]
    buf=norm(buf,.7); p=os.path.join(AUDIO,"music",name+".wav"); os.makedirs(os.path.dirname(p),exist_ok=True); sf.write(p,buf.astype(np.float32),SR,subtype="PCM_24"); print(p)
def sad_piano(name,prog,bpm,loops,notes_per_bar=4,oct_=4,drone=True):
    beat=60/bpm; bar=beat*4; total=len(prog)*loops*bar; buf=np.zeros((int((total+5)*SR),2))
    for i,ch in enumerate(prog*loops):
        t0=i*bar; fr=chord_freqs(ch,3); place(buf,hp(pad(fr,bar+1.5,1400),160),t0,.16)
        mel=[fr[0]*2,fr[2]*2,fr[1]*4,fr[2]*2]
        for k in range(notes_per_bar): place(buf,piano(mel[k%4]*2,3.5,.55 if k else .7),t0+k*bar/notes_per_bar,.42,p=-.25+.16*k)
        place(buf,piano(fr[0],4,.5),t0,.22)
    buf=reverb(buf,3.8,.42,4200)[:int((total+3)*SR)]
    f=int(SR); buf[:f]*=np.linspace(0,1,f)[:,None]; g=int(3*SR); buf[-g:]*=np.linspace(1,0,g)[:,None]
    buf=norm(buf,.7); p=os.path.join(AUDIO,"music",name+".wav"); os.makedirs(os.path.dirname(p),exist_ok=True); sf.write(p,buf.astype(np.float32),SR,subtype="PCM_24"); print(p)
def build_music():
    sad_piano("bed_sad_Am_64bpm",["Am","F","C","G"],64,5)
    drone_bed("bed_dark_E_drone",41.2,72,beat_bpm=62)
    render("bed_rise_Am_96bpm",["Am","F","C","G"],96,1,8,("pad","sub","arp","piano","drums"),pad_cut=1800,rev=(2.6,.32,5000))
    sad_piano("bed_resolve_C_70bpm",["C","G","Am","F"],70,4,notes_per_bar=3)
    render("bed_hope_F_76bpm",["Fadd9","C","Am9","G"],76,1,5,("pad","bell","sub"),pad_cut=2400,rev=(4.0,.45,6000))
def alarm(beeps=4,f=2900):
    one=np.sin(2*np.pi*f*t(.11))*.5; one=np.sign(one)*.3+one*.5; out=np.zeros(int(SR*(beeps*.5+.2)))
    for b in range(beeps):
        for k in range(2): s=int((b*.5+k*.15)*SR); out[s:s+len(one)]+=one
    return bp(out,800,7000)
def shatter(d=1.6):
    n=int(d*SR); tt=t(d); x=hp(rng.standard_normal(n),2500)*np.exp(-tt*5)
    for _ in range(40):
        s=int(rng.uniform(0,.9)*SR); L=int(.05*SR); x[s:s+L]+=np.sin(2*np.pi*rng.uniform(2500,7000)*t(.05))*np.exp(-t(.05)*60)[:len(x[s:s+L])]*.6
    return mixp(x,lp(impact(.6,140,50,.7,.5),900)*.6)
def rain_loop(d=8.0):
    n=int(d*SR); x=bp(rng.standard_normal(n),400,9000)*.3
    for _ in range(int(d*60)):
        s=int(rng.uniform(0,d-.05)*SR); L=int(.01*SR); x[s:s+L]+=hp(rng.standard_normal(L),3000)*rng.uniform(.1,.5)
    f=int(.3*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f); return np.stack([x,np.roll(x,3000)],1)
def notif():
    a=np.sin(2*np.pi*1320*t(.09))*np.exp(-t(.09)*30); b=np.sin(2*np.pi*1760*t(.16))*np.exp(-t(.16)*22); out=np.zeros(int(.3*SR)); out[:len(a)]+=a; s=int(.08*SR); out[s:s+len(b)]+=b; return out
def sent():
    tt=t(.25); f=600+1800*tt/.25; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*12)*.6+hp(rng.standard_normal(len(tt)),3000)*np.exp(-tt*25)*.15
def boom(): return lp(impact(3.0,70,28,1.0,.2),300)
def swell(d=2.2):
    tt=t(d); x=bp(rng.standard_normal(len(tt)),200,1800)*(tt/d)**2.5; tone=np.sin(2*np.pi*55*tt)*.5+np.sin(2*np.pi*58.3*tt)*.4; return (x+tone*(tt/d)**2)*np.minimum(1,(d-tt)/.05)
def whisper(d=1.3):
    tt=t(d); env=np.abs(np.sin(np.pi*tt/d))**1.5*(.6+.4*np.sin(2*np.pi*7*tt)); return bp(rng.standard_normal(len(tt)),1800,6500)*env*.6
def clock_tick(d=4.0):
    out=np.zeros(int(d*SR))
    for k in range(int(d)):
        s=int(k*SR); c=hp(rng.standard_normal(int(.02*SR)),2500)*np.exp(-t(.02)*300)*(1 if k%2 else .7); out[s:s+len(c)]+=c
    return out
def footsteps(n=6,gap=.48):
    out=np.zeros(int((n*gap+.3)*SR))
    for k in range(n):
        s=int(k*gap*SR); st=lp(impact(.18,160,80,.4,.4),1800)*rng.uniform(.7,1); out[s:s+len(st)]+=st[:len(out)-s]
    return out
def door():
    tt=t(1.1); f=300+200*np.sin(2*np.pi*1.3*tt); x=bp(np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*.3,400,3000)*np.exp(-tt*2); return mixp(x,lp(impact(.4,90,50,.5,.2),500)*.5)
def breath():
    tt=t(.9); return bp(rng.standard_normal(len(tt)),500,3000)*np.sin(np.pi*tt/.9)**2*.5
def sting():
    tt=t(3.0); x=sum(np.sin(2*np.pi*f*tt) for f in (55,58.27,82.4))*np.exp(-tt*.9); return mixp(lp(x,600),lp(impact(1.2,80,35,1.0,.3),400)*.6)
def page():
    tt=t(.4); return bp(rng.standard_normal(len(tt)),1500,8000)*np.exp(-((tt-.15)/.07)**2)*.6
def build_sfx():
    d="sfx"; paths=[]
    paths.append(save(f"{d}/alarm_beep",alarm(4),.7)); paths.append(save(f"{d}/alarm_long",alarm(10),.7))
    paths.append(save(f"{d}/glass_shatter",shatter(),.85,rev=(1.4,.2,7000))); paths.append(save(f"{d}/rain_loop",rain_loop(),.5))
    paths.append(save(f"{d}/notif_msg",notif(),.6)); paths.append(save(f"{d}/msg_sent",sent(),.55))
    paths.append(save(f"{d}/punch_bag",lp(impact(.45,110,55,.9,.3),1200),.9)); paths.append(save(f"{d}/boom_deep",boom(),.95,rev=(2.5,.3,1500)))
    paths.append(save(f"{d}/tempt_swell",swell(),.8,rev=(2.0,.35,3000))); paths.append(save(f"{d}/tempt_whisper",whisper(),.55,rev=(1.6,.4,6000)))
    paths.append(save(f"{d}/clock_tick",clock_tick(),.5)); paths.append(save(f"{d}/footsteps",footsteps(),.7)); paths.append(save(f"{d}/door_open",door(),.6,rev=(1.0,.2,4000)))
    paths.append(save(f"{d}/breath_in",breath(),.5)); paths.append(save(f"{d}/sting_low",sting(),.9,rev=(3.0,.35,2000))); paths.append(save(f"{d}/page_flip",page(),.5))
    return paths
if __name__ == "__main__":
    for p in build_sfx(): print(p)
    build_music()
