#!/usr/bin/env python3
"""Generate an original layered score at the source-measured pulse; no reference samples."""
from __future__ import annotations
import argparse,math,os,wave
from array import array
from pathlib import Path
SR=48000
DURATION=37.3
BPM=114.84375
TAU=math.tau
SCALE=[146.83,174.61,196,220,261.63,293.66,349.23,392]
CHORDS=[(73.42,87.31,110,130.81),(58.27,69.3,87.31,103.83),(65.41,82.41,98,130.81),(65.41,78,98,116.54)]
CUES=[0,2.767,5.767,6.967,8.133,10.7,20,21.367,25.967,29.833,31.1,35.3]
def clamp(x,a=0.,b=1.): return max(a,min(b,x))
def smooth(x):
 x=clamp(x); return x*x*(3-2*x)
def main():
 p=argparse.ArgumentParser(); p.add_argument("--out",default="public/audio/opendesign-motion-score.wav"); out=Path(p.parse_args().out); out.parent.mkdir(parents=True,exist_ok=True)
 total=int(DURATION*SR); beat=60/BPM; sixteenth=beat/4
 left=array("h"); right=array("h"); cues=[(int(t*SR),int(.34*SR)) for t in CUES]; ci=0; active=[]
 roots=[0,1,2,3,0,2,1,3,0,2]; phrase=[0,2,4,5,3,2,6,4,5,3,1,4,7,5,3,2]
 for i in range(total):
  t=i/SR; pos=t/beat; bi=int(pos); phase=pos-bi; bar=int(t/(beat*4)); chord=CHORDS[roots[min(9,bar//2)]]
  section=.62 if t<4.5 else 1.
  if 18.9<=t<20.9: section*=.18
  elif 20.9<=t<21.5: section*=.45
  master=min(smooth(t/.18),smooth((DURATION-t)/.8))*section*.76
  pad=0.
  for k,freq in enumerate(chord):
   amp=(.031,.024,.018,.011)[k]; detune=1+(k-1.5)*.0009
   pad+=math.sin(TAU*freq*detune*t+k*.44)*amp+math.sin(TAU*freq*2.003*t+k*.83)*amp*.15
  pad*=1+.012*math.sin(TAU*.19*t)
  st=int(t/sixteenth); age=(t/sixteenth-st)*sixteenth; note=SCALE[phrase[st%16]]
  arp=(math.sin(TAU*note*t)*.052+math.sin(TAU*note*2*t+.2)*.015)*math.exp(-age*7.8)*(1 if st%4 in (0,2,3) else .55)
  bassEnv=math.exp(-phase*4) if bi%4 in (0,2) else .35*math.exp(-phase*3.2)
  bass=(math.sin(TAU*chord[0]*.5*t)*.115+math.sin(TAU*chord[0]*t)*.025)*bassEnv
  kick=0.
  if bi%4 in (0,2) and phase<.34:
   a=phase*beat; env=math.exp(-a*28); kick=math.sin(TAU*(73-42*a)*a)*env*.23+math.sin(TAU*180*a)*math.exp(-a*90)*.045
  snare=0.
  if bi%4 in (1,3) and phase<.42:
   a=phase*beat; env=math.exp(-a*34); noise=math.sin(TAU*1931*a)*math.sin(TAU*2741*a); snare=noise*env*.082+math.sin(TAU*194*a)*env*.027
  eighth=(t/(beat/2))%1; hat=0.
  if eighth<.115:
   a=eighth*beat/2; noise=math.sin(TAU*7103*a)*math.sin(TAU*9137*a); hat=noise*math.exp(-a*(170 if bi%2 else 120))*.031
  if ci<len(cues) and i>=cues[ci][0]: active.append([cues[ci][1],0]); ci+=1
  whoosh=0.; keep=[]
  for item in active:
   length,age2=item
   if age2<length:
    q=age2/length; whoosh+=math.sin(TAU*(180+570*q)*(age2/SR))*math.sin(math.pi*q)**1.35*.045; item[1]+=1; keep.append(item)
  active=keep; mono=(pad+arp+bass+kick+snare+hat+whoosh)*master; stereo=.006*math.sin(TAU*.13*t)
  left.append(int(clamp(mono+stereo,-.93,.93)*32767)); right.append(int(clamp(mono-stereo,-.93,.93)*32767))
 inter=array("h")
 for l,r in zip(left,right): inter.append(l); inter.append(r)
 if os.sys.byteorder!="little": inter.byteswap()
 with wave.open(str(out),"wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(inter.tobytes())
 print(f"Generated original layered score: {out}; 37.3s; {BPM:.5f} BPM; 48kHz stereo")
 print("Arrangement: restrained opening / rhythmic build / 19-21s low-energy reset / end resolve")
if __name__=="__main__": main()
