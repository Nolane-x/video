#!/usr/bin/env python3
"""Generate original, redistributable procedural sound effects for the video asset library."""
from __future__ import annotations
import math
import random
import struct
import wave
from pathlib import Path

SFX_PRESETS = [
    ("ui-click-soft","click",0.18),("ui-click-sharp","click-sharp",0.12),
    ("ui-confirm","chime",0.8),("ui-error","buzz",0.45),
    ("notification-soft","chime-soft",0.9),("notification-urgent","pulse",0.7),
    ("camera-shutter","shutter",0.35),("camera-flash","impact",0.2),
    ("keyboard-typing-short","typing",1.5),("typewriter-hit","click-sharp",0.1),
    ("page-flip","paper",0.7),("paper-rustle","paper",1.4),
    ("clock-tick","tick",0.8),("alarm-clock","alarm",1.8),
    ("heartbeat-slow","heartbeat",2.8),("heartbeat-fast","heartbeat-fast",2.5),
    ("footsteps-concrete","steps",2.4),("footsteps-wood","steps-wood",2.4),
    ("footsteps-gravel","steps-gravel",2.4),("impact-soft","impact",0.45),
    ("impact-heavy","impact-heavy",0.8),("sub-hit","subhit",0.9),
    ("whoosh-short","whoosh",0.7),("whoosh-long","whoosh",1.8),
    ("transition-sweep","sweep",1.4),("transition-impact","impact-heavy",0.9),
    ("riser-tension","riser",2.4),("sting-dark","darksting",1.4),
    ("sting-hopeful","hope",1.6),("success-chime","chime",1.2),
    ("magic-sparkle","sparkle",1.5),("glass-tinkle","glass",1.1),
    ("glass-break","glassbreak",1.5),("sci-fi-beep","scifi",0.8),
    ("laser-pulse","laser",0.7),("glitch-burst","glitch",0.65),
    ("tape-stop","tapestop",0.8),("wind-ambience","wind",5.5),
    ("rain-ambience","rain",5.5),("city-ambience","city",5.5),
    ("forest-night-stylized","forest",5.5),("ocean-waves-ambience","ocean",5.5),
    ("underwater-bubbles","bubbles",4.0),("fire-crackle-stylized","fire",5.5),
    ("thunder-roll-stylized","thunder",4.5),("drone-tension","drone",5.0),
    ("drone-warm","warmdrone",5.0),("vinyl-crackle","vinyl",4.0),
    ("crowd-cheer-stylized","crowd",3.0),("bird-chirps-stylized","birds",4.0),
    ("wind-chime","chime",2.0),("soft-piano-single","piano",1.8),
    ("string-pluck","pluck",1.0),("sweep-dark","sweepdark",1.2),
    ("sweep-bright","sweepbright",1.2),("deep-boom","impact-heavy",1.0),
    ("soft-morse-beeps","morse",1.4),("metallic-clank","metal",0.55),
    ("glass-shard-fall","glassbreak",1.2),("distant-train","train",4.0),
    ("rain-on-window","rainwindow",5.5),("page-turn-fast","paper",0.4),
    ("heartbeat-impact","heartbeat",0.55),("digital-scan","scifi",0.6),
    ("wind-gust-short","wind",2.2),("wind-gust-long","wind",5.5),
    ("rain-light","rain",5.5),("rain-heavy","rainwindow",5.5),
    ("distant-thunder","thunder",4.5),("thunder-deep","thunder",5.5),
    ("forest-ambience-dawn","forest",5.5),("forest-insects-night","forest",5.5),
    ("ocean-surf-close","ocean",5.5),("ocean-surf-distant","ocean",5.5),
    ("underwater-bubbles-cluster","bubbles",4.0),("deep-ocean-drone","drone",5.0),
    ("industrial-ambience","city",5.5),("subway-rumble","train",4.0),
    ("crowd-murmur","crowd",3.0),("crowd-climax","crowd",3.0),
    ("birds-morning","birds",5.5),("bird-single-chirp","birds",1.8),
    ("old-film-static","vinyl",4.0),("vinyl-scratch","vinyl",3.0),
    ("typing-fast","typing",2.0),("typewriter-run","typing",2.2),
    ("ui-toggle","click",0.18),("ui-soft-blip","chime-soft",0.45),
    ("scanner-beep","scifi",0.8),("radar-ping","chime-soft",0.9),
    ("horror-riser","riser",3.0),("tension-drone-deep","drone",5.0),
    ("reverse-swell","sweepdark",1.5),("transition-swish-medium","whoosh",0.9),
    ("transition-swish-fast","whoosh",0.45),("impact-metallic","metal",0.65),
    ("impact-bass-slam","impact-heavy",1.0),("heartbeat-distant","heartbeat",3.2),
    ("heartbeat-panic","heartbeat-fast",2.8),("camera-shutter-burst","shutter",0.4),
    ("camera-flash-pop","impact",0.2),("page-turn-old-paper","paper",0.8),
    ("magic-chime-light","sparkle",1.5),("magic-chime-deep","darksting",1.4),
    ("hopeful-rise","hope",1.8),("piano-pulse","piano",1.8),
    ("single-note-low","darksting",1.1),("single-note-high","piano",1.1),
    ("glass-tinkling-small","glass",1.0),("metal-object-fall","metal",0.8),
    ("footsteps-hallway","steps-wood",2.8),("footsteps-running","steps",2.0),
    ("alarm-digital","alarm",1.8),("clock-ticking-fast","tick",1.2),
    ("data-glitch-sweep","glitch",0.8),("tape-warp","tapestop",1.0),
    ("laser-shot-double","laser",0.8),("submarine-sonar","scifi",1.0),
    ("wind-chimes-distant","chime",2.0),("music-intro-sting","hope",1.6),
    ("dark-reveal-sting","darksting",1.3),("soft-transition-swish","sweepbright",1.2),
    ("buzz-low","buzz",0.7),("electrical-pulse","pulse",0.8),
    ("notification-double-chime","chime",0.9)
    ("wind-through-alley","wind",5.5),
    ("forest-wind-canopy","wind",5.5),
    ("night-insects-bed","forest",5.5),
    ("rain-on-metal-roof","rainwindow",5.5),
    ("waves-on-pebbles","ocean",5.5),
    ("distant-harbor-roomtone","city",5.5),
    ("crowd-in-station","crowd",3),
    ("subway-arrival-rumble","train",4),
    ("industrial-fan-roomtone","city",5.5),
    ("campfire-close-crackle","fire",5.5),
    ("storm-rumble-low","thunder",5.5),
    ("underwater-pressure-drone","drone",5),
    ("dawn-bird-chorus","birds",5.5),
    ("vinyl-room-tone","vinyl",4),
    ("desert-wind-gust","wind",5.5),
    ("transition-airy-swell","sweepbright",1.8),
    ("transition-deep-swell","sweepdark",1.8),
    ("impact-low-cinematic","impact-heavy",1.1),
    ("impact-metal-short","metal",0.65),
    ("reveal-hopeful-sting","hope",1.8),
    ("reveal-dark-sting","darksting",1.5),
    ("reverse-cymbal-style-swell","sweep",1.6),
    ("cinematic-riser-short","riser",1.7),
    ("cinematic-riser-long","riser",3.5),
    ("transition-soft-whoosh","whoosh",0.9),
    ("transition-fast-whoosh","whoosh",0.42),
    ("title-card-chime","chime",1),
    ("logo-reveal-sparkle","sparkle",1.5),
    ("quiet-piano-resolve","piano",2.1),
    ("tension-pulse-slow","pulse",2),
    ("tension-pulse-fast","pulse",1),
    ("ui-hover-tick","click",0.16),
    ("ui-menu-open","chime-soft",0.48),
    ("ui-menu-close","tapestop",0.38),
    ("ui-navigation-confirm","chime",0.65),
    ("ui-notification-triple","chime",1),
    ("ui-warning-pulse","buzz",0.55),
    ("ui-data-arrival","scifi",0.7),
    ("ui-loading-sweep","sweepbright",1.1),
    ("ui-scan-complete","success-chime",1),
    ("digital-packet-burst","glitch",0.7),
    ("terminal-keystroke-run","typing",2.2),
    ("server-power-up","drone",2.2),
    ("scanner-calibration","scifi",0.9),
    ("radio-signal-dropout","glitch",1),
    ("camera-focus-confirm","chime-soft",0.55),
    ("camera-reel-start","train",1.3),
    ("film-projector-roomtone","vinyl",4),
    ("tape-rewind-short","tapestop",1),
    ("footsteps-marble-hall","steps-wood",2.7),
    ("footsteps-tile-corridor","steps",2.4),
    ("footsteps-wet-pavement","steps-gravel",2.4),
    ("footsteps-wood-staircase","steps-wood",2.5),
    ("footsteps-running-concrete","steps",2),
    ("paper-stack-drop","paper",0.75),
    ("pen-and-notebook-rustle","paper",1.25),
    ("page-turn-heavy-book","paper",0.8),
    ("glass-fragments-settle","glassbreak",1.5),
    ("metal-door-clang","metal",0.85),
    ("small-object-drop","impact",0.32),
    ("heavy-object-set-down","impact-heavy",0.7),
    ("clock-slow-tick","tick",1),
    ("clock-urgent-tick","tick",1.4),
    ("alarm-digital-short","alarm",1.2),
    ("heartbeat-muted","heartbeat",2.8),
    ("heartbeat-race-close","heartbeat-fast",2.5),
    ("doorway-wind-swell","wind",2.4),
    ("subtle-magic-shimmer","sparkle",1.2),
    ("morse-transmission","morse",1.8),
    ("low-voltage-buzz","buzz",0.8),
    ("electrical-switch-snap","click-sharp",0.16),
]

def synthesize(kind: str, duration: float, seed: int, sample_rate: int = 48000) -> bytes:
    rng = random.Random(seed)
    count = int(sample_rate * duration)
    samples = [0.0] * count
    low = 0.0
    deep = 0.0
    for i in range(count):
        t = i / sample_rate
        n = rng.random() * 2.0 - 1.0
        low += (n - low) * 0.035
        deep += (n - deep) * 0.004
        high = n - low
        value = 0.0

        if kind in {"click","click-sharp","shutter","typing","tick","morse","metal","train"}:
            if kind == "typing":
                interval = 0.115
                phase = t % interval
                width = 0.012
                active = phase < width
            elif kind == "tick":
                phase = t % 0.7
                width = 0.012
                active = phase < width
            elif kind == "morse":
                pattern = [0.08,0.08,0.22,0.08,0.08,0.32]
                pos = t % sum(pattern)
                active = int(pos / 0.08) % 2 == 0 and pos < 0.8
                phase = t % 0.08
                width = 0.08
            elif kind == "train":
                phase = t % 0.42
                width = 0.13
                active = phase < width
            else:
                phase = t % 0.19
                width = 0.034 if kind == "shutter" else 0.005
                active = phase < width
            if active:
                decay = 35 if kind in {"click","click-sharp","tick","morse"} else 19
                freq = 2100 if kind == "click-sharp" else 1350 if kind == "click" else 820 if kind == "metal" else 520
                value = (0.55 * n + 0.45 * math.sin(2 * math.pi * freq * t)) * math.exp(-phase * decay)
                if kind == "shutter":
                    value += high * math.exp(-phase * 28) * 0.6
                if kind == "metal":
                    value += sum(math.sin(2*math.pi*f*t)*math.exp(-phase*10)*0.18 for f in (640,910,1330))
                if kind == "train":
                    value += math.sin(2*math.pi*90*t)*math.exp(-phase*7)*0.3

        elif kind in {"chime","chime-soft","hope","sparkle","glass","piano","pluck","darksting","glassbreak"}:
            freqs = {
                "piano":[220,329.63,440], "hope":[392,493.88,587.33,783.99],
                "darksting":[73.42,110,146.83], "pluck":[196,293.66,392],
                "glass":[880,1174.66,1567.98,2093], "sparkle":[987.77,1318.51,1760,2349.32,2637],
                "glassbreak":[1240,1570,1980,2470], "chime-soft":[587.33,739.99,880],
                "chime":[523.25,659.25,783.99,1046.5]
            }.get(kind,[523.25,659.25,783.99])
            decay = 2.4 if kind == "piano" else 1.55 if kind == "darksting" else 3.0 if kind in {"glass","glassbreak"} else 2.6
            value = sum(math.sin(2*math.pi*f*t)*math.exp(-t*decay)*(0.22/(1+j*.25)) for j,f in enumerate(freqs))
            if kind in {"glassbreak"}:
                value += high * math.exp(-t*3.8) * 0.22
                if t < 0.09:
                    value += n * (1 - t/0.09) * 0.7
            if kind == "sparkle":
                value += math.sin(2*math.pi*(1400+600*math.sin(t*4))*t)*math.exp(-t*3)*0.13

        elif kind in {"impact","impact-heavy","subhit","heartbeat","heartbeat-fast","steps","steps-wood","steps-gravel","alarm","buzz","pulse","crowd","fire","thunder"}:
            if kind in {"heartbeat","heartbeat-fast"}:
                interval = 0.78 if kind == "heartbeat" else 0.42
                phase = t % interval
                env1 = math.exp(-phase*22) if phase < 0.22 else 0
                env2 = math.exp(-(phase-0.12)*25) if 0.12 <= phase < 0.34 else 0
                value = (math.sin(2*math.pi*63*t)*env1 + math.sin(2*math.pi*48*t)*env2)*0.9
            elif kind in {"steps","steps-wood","steps-gravel"}:
                phase = t % 0.55
                env = math.exp(-phase*28) if phase < 0.17 else 0
                freq = 82 if kind == "steps" else 125 if kind == "steps-wood" else 74
                texture = low*0.25 if kind == "steps-wood" else high*0.23
                value = math.sin(2*math.pi*freq*t)*env + texture*env
            elif kind == "alarm":
                value = (math.sin(2*math.pi*(850+220*math.sin(t*7))*t)*0.55+high*0.14)*(0.55+0.45*math.sin(t*9)**2)
            elif kind == "buzz":
                value = (math.sin(2*math.pi*94*t)+0.5*math.sin(2*math.pi*188*t))*0.35*(0.55+0.45*math.sin(t*44))
            elif kind == "pulse":
                env = math.exp(-t*5)
                value = (math.sin(2*math.pi*120*t)+0.5*math.sin(2*math.pi*240*t))*env
            elif kind == "crowd":
                value = (low*0.6+high*0.08)*(0.25+0.25*math.sin(t*2)+0.15*math.sin(t*3.7))
                for f in (180,245,315,410,520):
                    value += math.sin(2*math.pi*(f+8*math.sin(t*3))*t)*0.06
            elif kind == "fire":
                value = low*0.35+high*0.04
                if rng.random() < 0.00055:
                    value += rng.choice([-1,1])*rng.uniform(0.1,0.8)
            elif kind == "thunder":
                env = math.exp(-t*0.55)*(0.5+0.5*math.sin(t*1.1))
                value = (low*0.8+deep*0.9+high*0.13)*env
            else:
                env = math.exp(-t*(11 if kind == "impact" else 5))
                f0 = 98 if kind == "subhit" else 48 if kind == "impact-heavy" else 145
                freq = f0*(1-0.55*min(t/max(duration,0.001),1))
                value = math.sin(2*math.pi*freq*t)*env + high*env*(0.28 if kind=="impact-heavy" else 0.12)

        elif kind in {"whoosh","sweep","sweepdark","sweepbright","riser","tapestop","laser","scifi","glitch"}:
            u = t/max(duration,0.001)
            if kind == "riser":
                value = (math.sin(2*math.pi*(110+1000*u)*t)+high*0.45)*(u**1.8)*0.45
            elif kind == "laser":
                value = math.sin(2*math.pi*(1350-1000*u)*t)*math.exp(-t*4)+high*math.exp(-t*5)*0.32
            elif kind == "scifi":
                value = math.sin(2*math.pi*(390+170*math.sin(t*18)+100*math.sin(t*7))*t)*(0.45+0.3*math.sin(t*33)**2)
            elif kind == "glitch":
                gate = 1 if rng.random() > 0.72 else 0.05
                value = (high*0.6+math.sin(2*math.pi*(180+u*3200)*t)*0.3)*gate*(0.8-0.3*u)
            elif kind == "tapestop":
                freq = max(45,850*(1-u)**2+45)
                value = (math.sin(2*math.pi*freq*t)+high*0.25)*(1-u)**0.7
            else:
                env = math.sin(math.pi*min(1,max(0,u)))**0.8
                value = high*env*0.55+low*env*0.45
                if kind == "sweepdark":
                    value += math.sin(2*math.pi*(80+u*50)*t)*env*0.18
                if kind == "sweepbright":
                    value += math.sin(2*math.pi*(300+u*800)*t)*env*0.14

        elif kind in {"rain","wind","city","forest","ocean","bubbles","drone","warmdrone","vinyl","birds","paper","rainwindow"}:
            if kind in {"rain","rainwindow"}:
                value = high*0.25+low*0.36+(rng.uniform(-0.5,0.5) if rng.random()<0.0015 else 0)
                if kind == "rainwindow":
                    value += math.sin(2*math.pi*760*t)*0.015
            elif kind == "wind":
                value = (low*0.75+deep*0.4)*(0.45+0.55*(0.5+0.5*math.sin(t*0.45+math.sin(t*0.12))))
            elif kind == "city":
                value = low*0.45+deep*0.25+high*0.035+math.sin(2*math.pi*55*t)*0.03
            elif kind == "forest":
                value = low*0.12+high*0.025
                for base in (1.7,3.1,4.2):
                    phase = (t-base)%0.28
                    if 0 <= phase < 0.13:
                        freq = 2200+700*math.sin(phase*16)
                        value += math.sin(2*math.pi*freq*t)*math.sin(math.pi*phase/0.13)*0.08
            elif kind == "ocean":
                wave_env = 0.15+0.85*(0.5+0.5*math.sin(t*0.85+math.sin(t*0.24)))
                value = (low*0.65+high*0.05)*wave_env
            elif kind == "bubbles":
                period = 0.23+(seed%5)*0.025
                phase = t%period
                freq = 220+650*(phase/period)
                value = math.sin(2*math.pi*freq*t)*math.exp(-phase*9)*0.24+high*math.exp(-phase*11)*0.08
            elif kind == "drone":
                value = (math.sin(2*math.pi*55*t)+0.42*math.sin(2*math.pi*82.4*t)+0.2*math.sin(2*math.pi*110*t))*0.25+low*0.05
                value *= 0.7+0.3*math.sin(t*0.5)
            elif kind == "warmdrone":
                value = (math.sin(2*math.pi*130.81*t)+0.5*math.sin(2*math.pi*164.81*t)+0.3*math.sin(2*math.pi*196*t))*0.2*(0.8+0.2*math.sin(t*0.4))
            elif kind == "vinyl":
                value = high*0.08+low*0.08
                if rng.random() < 0.003:
                    value += rng.choice([-1,1])*rng.uniform(0.2,0.7)
            elif kind == "birds":
                value = high*0.025
                for base in (0.35,1.1,2.3,3.25):
                    phase = (t-base)%0.26
                    if 0 <= phase < 0.16:
                        freq = 1500+1200*math.sin(phase*9)
                        value += math.sin(2*math.pi*freq*t)*math.sin(math.pi*phase/0.16)*0.12
            elif kind == "paper":
                env = 0.3+0.7*math.sin(math.pi*(t/max(duration,0.001)))**2
                value = high*env*0.35+low*env*0.08
            else:
                value = high*0.1+low*0.1
        samples[i] = value

    peak=max(max(abs(x) for x in samples),1e-8)
    gain=0.88/peak
    packed=bytearray()
    for sample in samples:
        value=max(-32767,min(32767,int(sample*gain*32767)))
        packed.extend(struct.pack("<h",value))
    return bytes(packed)

def generate_original_audio(root: Path, index: list[dict], cc0_url: str) -> int:
    import hashlib
    target_dir=root/"originals/audio"
    target_dir.mkdir(parents=True,exist_ok=True)
    count=0
    for i,(name,kind,duration) in enumerate(SFX_PRESETS):
        payload=synthesize(kind,duration,seed=8021+i)
        path=target_dir/(name+".wav")
        with wave.open(str(path),"wb") as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(48000); wav.writeframes(payload)
        digest=hashlib.sha256(payload).hexdigest()
        index.append({"id":name,"path":path.relative_to(root).as_posix(),"type":"original-procedural-sfx",
                      "description":name.replace("-"," ").title(),"duration_seconds":duration,"sample_rate":48000,
                      "channels":1,"sample_format":"PCM_S16LE","license":"CC0-1.0","license_url":cc0_url,
                      "redistributable":True,"originally_synthesized":True,"sha256":digest,"size_bytes":path.stat().st_size})
        count+=1
    return count
