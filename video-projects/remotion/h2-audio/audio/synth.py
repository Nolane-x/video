"""Procedural SFX + music kit for the What-If channel. 100% generated -> no copyright.
Output: 48 kHz stereo 24-bit WAV."""
import numpy as np, soundfile as sf, os
from scipy import signal

SR = 48000
rng = np.random.default_rng(7)
OUT = os.path.dirname(os.path.abspath(__file__))

def t(d): return np.arange(int(SR * d)) / SR
def norm(x, peak=0.89):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak
def env_adsr(n, a, d, s, r, sus=0.6):
    a, d, r = int(a*SR), int(d*SR), int(r*SR); s_ = max(n - a - d - r, 0)
    e = np.concatenate([np.linspace(0, 1, a, False), np.linspace(1, sus, d, False), np.full(s_, sus), np.linspace(sus, 0, r)])
    return np.pad(e, (0, max(0, n - len(e))))[:n]
def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def lp(x, f, order=2):
    sos = signal.butter(order, f, 'lowpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def hp(x, f, order=2):
    sos = signal.butter(order, f, 'highpass', fs=SR, output='sos'); return signal.sosfilt(sos, x)
def sweep_filter(x, f0, f1, q=2.0, curve='exp'):
    """time-varying bandpass via block processing"""
    n = len(x); out = np.zeros(n); blk = 256
    zi = None
    for i in range(0, n, blk):
        p = i / n
        f = f0 * (f1 / f0) ** p if curve == 'exp' else f0 + (f1 - f0) * p
        f = np.clip(f, 30, SR/2 - 2000)
        b, a = signal.iirpeak(f, q, fs=SR)
        if zi is None: zi = signal.lfilter_zi(b, a) * 0
        out[i:i+blk], zi = signal.lfilter(b, a, x[i:i+blk], zi=zi)
    return out
_ir_cache = {}
def reverb(x, size=1.8, wet=0.3, damp=4000):
    key = (size, damp)
    if key not in _ir_cache:
        n = int(size * SR); tt = np.arange(n) / SR
        irL = rng.standard_normal(n) * np.exp(-tt * 6.9 / size); irR = rng.standard_normal(n) * np.exp(-tt * 6.9 / size)
        irL, irR = lp(irL, damp), lp(irR, damp)
        _ir_cache[key] = (irL / np.sqrt((irL**2).sum()), irR / np.sqrt((irR**2).sum()))
    irL, irR = _ir_cache[key]
    if x.ndim == 1: x = np.stack([x, x], 1)
    pad = len(irL)
    xp = np.pad(x, ((0, pad), (0, 0)))
    wL = signal.fftconvolve(xp[:, 0], irL)[:len(xp)]; wR = signal.fftconvolve(xp[:, 1], irR)[:len(xp)]
    return xp * (1 - wet) + np.stack([wL, wR], 1) * wet
def pan(x, p):
    l = np.sqrt((1 - p) / 2); r = np.sqrt((1 + p) / 2)
    return np.stack([x * l, x * r], 1)
def stereo(x): return np.stack([x, x], 1) if x.ndim == 1 else x
def trim(x, thr=1e-4):
    a = np.max(np.abs(stereo(x)), 1); idx = np.where(a > thr)[0]
    return x[:idx[-1] + int(0.02*SR)] if len(idx) else x
def save(name, x, peak=0.89, rev=None, fade=0.01):
    x = stereo(x)
    if rev: x = reverb(x, *rev)
    x = trim(x)
    f = int(fade * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    x = norm(x, peak)
    path = os.path.join(OUT, name + '.wav'); os.makedirs(os.path.dirname(path), exist_ok=True)
    sf.write(path, x.astype(np.float32), SR, subtype='PCM_24'); return path

def whoosh(d=0.6, f0=300, f1=3500, q=1.2, pan_move=True, bright=1.0):
    n = int(d*SR); x = rng.standard_normal(n)
    x = sweep_filter(x, f0, f1, q) * 0.7 + sweep_filter(rng.standard_normal(n), f0*1.5, f1*1.5, q*1.5) * 0.3 * bright
    peak = 0.62; e = np.where(np.arange(n) < peak*n, (np.arange(n)/(peak*n))**2.5, np.exp(-(np.arange(n)-peak*n)/(0.12*n)))
    x *= e
    p = np.linspace(-0.7, 0.7, n) if pan_move else np.zeros(n)
    return pan(x, p)
def impact(d=1.6, f_hi=110, f_lo=38, sub=1.0, crack=0.6):
    tt = t(d); n = len(tt)
    f = f_lo + (f_hi - f_lo) * np.exp(-tt * 18)
    body = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tt * 3.2) * sub
    nz = rng.standard_normal(n); click = hp(nz, 2000) * np.exp(-tt * 90) * crack
    thump = lp(nz, 300) * np.exp(-tt * 25) * 0.8
    return np.tanh((body + click + thump) * 1.8)
def ding(f=1318.5, d=2.5, bright=1.0):
    tt = t(d)
    ratios = [(1, 1, 1.4), (2.0, 0.35, 2.0), (2.76, 0.5, 2.6), (4.07, 0.3 * bright, 3.5), (5.4, 0.25 * bright, 4.5), (8.93, 0.12 * bright, 7)]
    x = sum(a * np.sin(2*np.pi*f*r*tt) * np.exp(-tt * dec) for r, a, dec in ratios)
    return x * np.minimum(1, tt / 0.002)
def heartbeat(bpm=70, beats=4):
    one = lp(impact(0.35, 70, 40, 1, 0), 400)
    gap = int(60 / bpm * SR); out = np.zeros(gap * beats + len(one))
    for b in range(beats):
        s = b * gap; out[s:s+len(one)] += one; s2 = s + int(0.18*SR); out[s2:s2+len(one)] += one * 0.6
    return out
def riser(d=4.0, f0=120, f1=1400):
    tt = t(d); n = len(tt); p = tt / d
    f = f0 * (f1/f0) ** (p**1.6)
    tone = sum(np.sin(2*np.pi*np.cumsum(f*k)/SR + k) / k for k in (1, 1.005, 2.01, 3))
    nz = sweep_filter(rng.standard_normal(n), 300, 9000, 1.2)
    e = p ** 2.2
    x = (lp(tone, 4000) * 0.5 + nz * 0.8) * e
    return np.stack([x, np.roll(x, 400)], 1)
def shatter(d=1.6):
    n = int(d * SR); tt = t(d); x = hp(rng.standard_normal(n), 2500) * np.exp(-tt * 5)
    for _ in range(40):
        s = int(rng.uniform(0, 0.9) * SR); L = int(0.05 * SR)
        x[s:s + L] += np.sin(2 * np.pi * rng.uniform(2500, 7000) * t(0.05)) * np.exp(-t(0.05) * 60)[:len(x[s:s + L])] * 0.6
    return x + lp(impact(0.6, 140, 50, 0.7, 0.5), 900) * 0.6
def notif():
    a = np.sin(2 * np.pi * 1320 * t(0.09)) * np.exp(-t(0.09) * 30); b = np.sin(2 * np.pi * 1760 * t(0.16)) * np.exp(-t(0.16) * 22)
    out = np.zeros(int(0.3 * SR)); out[:len(a)] += a; s = int(0.08 * SR); out[s:s + len(b)] += b; return out
def page():
    tt = t(0.4); return bp(rng.standard_normal(len(tt)), 1500, 8000) * np.exp(-((tt - 0.15) / 0.07) ** 2) * 0.6
def footsteps(n=6, gap=0.48):
    out = np.zeros(int((n * gap + 0.3) * SR))
    for k in range(n):
        s = int(k * gap * SR); st = lp(impact(0.18, 160, 80, 0.4, 0.4), 1800) * rng.uniform(0.7, 1)
        out[s:s + len(st)] += st[:len(out) - s]
    return out
def door():
    tt = t(1.1); f = 300 + 200 * np.sin(2 * np.pi * 1.3 * tt)
    x = bp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3, 400, 3000) * np.exp(-tt * 2)
    return x + lp(impact(0.4, 90, 50, 0.5, 0.2), 500) * 0.5
def breath():
    tt = t(0.9); return bp(rng.standard_normal(len(tt)), 500, 3000) * np.sin(np.pi * tt / 0.9) ** 2 * 0.5
def sting():
    tt = t(3.0); x = sum(np.sin(2 * np.pi * f * tt) for f in (55, 58.27, 82.4)) * np.exp(-tt * 0.9)
    return lp(x, 600) + lp(impact(1.2, 80, 35, 1.0, 0.3), 400) * 0.6
def build_sfx():
    d = "sfx"; paths = []
    paths.append(save(f"{d}/glass_shatter", shatter(), 0.85, rev=(1.4, 0.2, 7000)))
    paths.append(save(f"{d}/notif_msg", notif(), 0.6))
    paths.append(save(f"{d}/tempt_swell", riser(2.2), 0.8, rev=(2.0, 0.35, 3000)))
    paths.append(save(f"{d}/tempt_whisper", lp(rng.standard_normal(int(1.3*SR)), 6500), 0.35, rev=(1.6, 0.4, 6000)))
    paths.append(save(f"{d}/clock_tick", np.tile(np.concatenate([np.zeros(int(.1*SR)), ding(3200,.05,.2)]), 20), 0.5))
    paths.append(save(f"{d}/footsteps", footsteps(), 0.7))
    paths.append(save(f"{d}/door_open", door(), 0.6, rev=(1.0, 0.2, 4000)))
    paths.append(save(f"{d}/breath_in", breath(), 0.5))
    paths.append(save(f"{d}/sting_low", sting(), 0.9, rev=(3.0, 0.35, 2000)))
    paths.append(save(f"{d}/page_flip", page(), 0.5))
    return paths
if __name__ == "__main__":
    for p in build_sfx(): print(p)
