// sets.js — boi canh nen toi net manh: set(g, ten, o) ve nen va tra ve "moc" (vi tri giuong, ghe, cua...) de dat nhan vat.
// Ten: bedroom city street lockers classroom court cafe gym stairs hill mirror kitchen void black doorway
// o chung: t (giay), gy (mat san 0..1), dim (0..1 lam toi), seed
import { E, clamp, lerp, ease, rng, noise, alpha, shade, mix, text } from '/engine/core.js';
import { PAL, accent, obj, box, oval, ln, fillAll, vgrad, light, beam, FONT_UI, FONT_NARR } from './ink.js';

const W = () => E.W, H = () => E.H;
const X = (k) => k * E.W, Y = (k) => k * E.H;
// khung doc: dat vat theo ti le cua chieu ngang 16:9 trung tam
const VX = (k) => (E.vertical ? E.W / 2 + (k - 0.5) * E.H * 0.5625 * 1.0 : k * E.W);

function wall(g, top = '#17171c', bot = '#1d1e24') { vgrad(g, [[0, top], [1, bot]]); }
function floor(g, gy, c = PAL.floor) { g.fillStyle = c; g.fillRect(-60, gy, E.W + 120, E.H - gy + 60); ln(g, [[-60, gy], [E.W + 60, gy]], { lw: 2, la: 0.45 }); }
export function rain(g, t, o = {}) {
  const r = rng(o.seed || 7), n = o.n || 160, sp = o.speed || 1400, len = o.len || 34;
  g.save(); g.strokeStyle = alpha(o.color || '#aab4c8', o.a ?? 0.35); g.lineWidth = o.lw || 1.6;
  for (let i = 0; i < n; i++) { const x0 = r() * (E.W + 200) - 100, y0 = r() * E.H, y = (y0 + t * sp * (0.8 + r() * 0.4)) % (E.H + 60) - 30, x = x0 - (y / E.H) * 60; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 6, y + len); g.stroke(); }
  g.restore();
}
export function dust(g, t, o = {}) {
  const r = rng(o.seed || 5); g.save();
  for (let i = 0; i < (o.n || 40); i++) { const x = (r() * E.W + Math.sin(t * 0.3 + i) * 30), y = (r() * E.H - t * 12 * (0.5 + r())) % E.H; g.fillStyle = alpha(o.color || '#e8e2d0', 0.15 + r() * 0.25); g.beginPath(); g.arc(x, y < 0 ? y + E.H : y, 1 + r() * 2, 0, 7); g.fill(); }
  g.restore();
}
function moon(g, x, y, r) { light(g, x, y, r * 4, '#cfd8ff', 0.25); g.beginPath(); g.arc(x, y, r, 0, 7); g.fillStyle = PAL.moon; g.fill(); }
function skyGrad(g, x, y, w, h, kind, t = 0) {
  const S = { moon: ['#151a2c', '#202842'], night: ['#11131f', '#1c2238'], dawn: ['#3b2b4f', '#c8705a'], dusk: ['#2c2140', '#d47a5e'], day: ['#6e9cc8', '#a9cce6'], rain: ['#151821', '#232a38'], dark: ['#0f1014', '#15161b'] }[kind] || ['#151a2c', '#202842'];
  const gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, S[0]); gr.addColorStop(1, S[1]); g.fillStyle = gr; g.fillRect(x, y, w, h);
  if (kind === 'moon' || kind === 'night') moon(g, x + w * 0.62, y + h * 0.3, Math.min(w, h) * 0.09);
  if (kind === 'rain') { g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip(); g.strokeStyle = 'rgba(170,185,210,0.35)'; g.lineWidth = 1.2; const r = rng(3); for (let i = 0; i < 26; i++) { const xx = x + r() * w, yy = y + ((r() * h + t * 500) % h); g.beginPath(); g.moveTo(xx, yy); g.lineTo(xx - 3, yy + 16); g.stroke(); } g.restore(); }
  if (kind === 'day') { const r = rng(9); for (let i = 0; i < 4; i++) { g.beginPath(); g.ellipse(x + w * (0.15 + i * 0.25), y + h * (0.88 + r() * 0.05), w * 0.16, h * 0.2, 0, 0, 7); g.fillStyle = '#5c9a5a'; g.fill(); } }
}
export function windowBox(g, x, y, w, h, o = {}) {
  box(g, x - 8, y - 8, w + 16, h + 16, { fill: '#2a2c33', r: 6 });
  skyGrad(g, x, y, w, h, o.sky || 'moon', o.t);
  g.save(); g.strokeStyle = alpha(PAL.line, 0.8); g.lineWidth = 5; g.strokeRect(x, y, w, h); g.beginPath(); g.moveTo(x + w / 2, y); g.lineTo(x + w / 2, y + h); g.moveTo(x, y + h / 2); g.lineTo(x + w, y + h / 2); g.stroke(); g.restore();
}
// ---------- do vat
export function digitClock(g, x, y, s, o = {}) {
  const w = s * 1.6, h = s * 0.8, col = o.color || PAL.clock;
  box(g, x - w / 2, y - h, w, h, { fill: '#202127', r: s * 0.12 });
  const blink = o.blink ? (Math.floor((o.t || 0) * 2) % 2 === 0) : true;
  let str = String(o.time ?? '3:17'); if (!blink) str = str.replace(':', ' ');
  g.save(); g.shadowColor = col; g.shadowBlur = s * 0.25;
  text(g, str, x, y - h / 2 + s * 0.02, { size: s * 0.5, font: '"Be Vietnam Pro"', weight: 700, color: col, spacing: 2 }); g.restore();
  light(g, x, y - h / 2, s * 1.4, col, 0.12);
  if (o.ring) { const k = Math.sin((o.t || 0) * 26) > 0; if (k) for (const d of [-1, 1]) for (let i = 0; i < 2; i++) ln(g, [[x + d * (w / 2 + 10 + i * 12), y - h * 0.9 + i * 6], [x + d * (w / 2 + 22 + i * 12), y - h * 1.1 + i * 6]], { color: col, lw: 3, la: 0.9 }); }
}
export function calendar(g, x, y, w, o = {}) {
  const h = w * 1.1, col = o.headColor || '#c9463d';
  box(g, x, y, w, h, { fill: '#e9e6df', line: '#6d6f76', r: 4 });
  g.fillStyle = col; g.fillRect(x + 1, y + 1, w - 2, h * 0.2);
  text(g, o.month || 'OCT', x + w / 2, y + h * 0.105, { size: h * 0.12, font: '"Be Vietnam Pro"', weight: 700, color: '#fff' });
  const cw = (w - 12) / 7, ch = (h * 0.78 - 8) / 5, n = Math.round(o.fill ?? 0), mode = o.mode || 'x', mc = o.color || (mode === 'x' ? '#d23b33' : accent());
  for (let i = 0; i < 35; i++) {
    const cx = x + 6 + (i % 7) * cw, cy = y + h * 0.22 + 4 + Math.floor(i / 7) * ch;
    g.fillStyle = '#d6d2c9'; g.fillRect(cx + 1, cy + 1, cw - 2, ch - 2);
    if (i < n) { if (mode === 'x') { g.strokeStyle = mc; g.lineWidth = Math.max(1.5, cw * 0.12); g.beginPath(); g.moveTo(cx + 3, cy + 3); g.lineTo(cx + cw - 3, cy + ch - 3); g.moveTo(cx + cw - 3, cy + 3); g.lineTo(cx + 3, cy + ch - 3); g.stroke(); } else { g.fillStyle = mc; g.fillRect(cx + 1, cy + 1, cw - 2, ch - 2); } }
  }
}
export function deskLamp(g, x, y, s, on = true) {
  ln(g, [[x, y], [x + s * 0.25, y - s * 0.6], [x - s * 0.05, y - s * 0.95]], { lw: s * 0.05, color: '#6b6e77', la: 1 });
  obj(g, (c) => { c.moveTo(x - s * 0.05, y - s * 0.95); c.lineTo(x - s * 0.4, y - s * 0.7); c.lineTo(x - s * 0.15, y - s * 1.12); c.closePath(); }, { fill: '#5a5d66' });
  box(g, x - s * 0.2, y - s * 0.06, s * 0.4, s * 0.08, { fill: '#4a4d55', r: 3 });
  if (on) { beam(g, x - s * 0.3, y - s * 0.82, x - s * 1.2, x + s * 0.6, y + s * 0.05, PAL.lamp, 0.22); light(g, x - s * 0.3, y - s * 0.8, s * 1.6, PAL.lamp, 0.35); }
}
export function books(g, x, y, s) { const cs = ['#3f6ea8', '#c9463d', '#5f8f5a', '#e8b33c', '#7b6a8a']; for (let i = 0; i < 5; i++) box(g, x - s * 0.5 + (i % 2) * 6, y - (i + 1) * s * 0.13, s * (0.9 - i * 0.05), s * 0.12, { fill: cs[i], line: '#222', r: 2, la: 0.4 }); }
export function laptop(g, x, y, s, o = {}) {
  const c = o.color || '#9fb6ff';
  obj(g, (k) => { k.moveTo(x - s * 0.55, y - 2); k.lineTo(x + s * 0.55, y - 2); k.lineTo(x + s * 0.62, y + 4); k.lineTo(x - s * 0.62, y + 4); k.closePath(); }, { fill: '#3a3d45' });
  obj(g, (k) => { k.moveTo(x - s * 0.5, y - 4); k.lineTo(x - s * 0.42, y - s * 0.72); k.lineTo(x + s * 0.48, y - s * 0.72); k.lineTo(x + s * 0.5, y - 4); k.closePath(); }, { fill: o.on ? c : '#202127' });
  if (o.on) light(g, x, y - s * 0.4, s * 2.2, c, 0.28);
}
export function chair(g, x, gy, s, f = 1) {
  ln(g, [[x - f * s * 0.25, gy - s * 0.95], [x - f * s * 0.25, gy]], { lw: 5, color: '#5c5f68', la: 1 });
  ln(g, [[x - f * s * 0.25, gy - s * 0.5], [x + f * s * 0.25, gy - s * 0.5], [x + f * s * 0.25, gy]], { lw: 5, color: '#5c5f68', la: 1 });
  box(g, x - s * 0.3, gy - s * 0.54, s * 0.6, s * 0.07, { fill: '#3a3d45', r: 3 });
}
export function table(g, x, gy, w, h, o = {}) { box(g, x - w / 2, gy - h, w, h * 0.08, { fill: o.fill || '#3a3d45', r: 3 }); ln(g, [[x - w * 0.42, gy - h], [x - w * 0.42, gy]], { lw: 4, la: 0.7 }); ln(g, [[x + w * 0.42, gy - h], [x + w * 0.42, gy]], { lw: 4, la: 0.7 }); }
export function door(g, x, gy, w, h, o = {}) {
  box(g, x - w / 2, gy - h, w, h, { fill: o.open ? '#0d0d10' : '#2b2d34', r: 3 });
  if (o.open) { const k = o.open; g.save(); g.globalCompositeOperation = 'lighter'; g.fillStyle = alpha(o.lightColor || PAL.lamp, 0.55 * k); g.fillRect(x - w / 2 + 4, gy - h + 4, w * k - 8, h - 8); g.restore(); beam(g, x, gy - h * 0.5, x - w * 0.2, x + w * 1.6, gy + E.H * 0.2, o.lightColor || PAL.lamp, 0.18 * k); }
  else { oval(g, x + w * 0.35, gy - h * 0.48, 5, 5, { fill: '#9a9da6', line: null }); }
}
export function punchBag(g, x, y, s, o = {}) {
  const t = o.t || 0;
  let recoil = 0;
  for (const at of (o.impacts || [])) {
    const d = t - at;
    if (d >= 0 && d < 1.5) recoil += Math.sin(d * 7.5) * Math.exp(-d * 1.6) * (o.impactSwing ?? 0.22);
  }
  const sw = Math.sin(t * 5) * (o.swing ?? 0.025) + recoil;
  g.save(); g.translate(x, y); g.rotate(sw);
  ln(g, [[0, 0], [0, s * 0.2]], { lw: 3, color: '#777' });
  box(g, -s * 0.18, s * 0.2, s * 0.36, s * 0.8, { fill: o.color || '#c4302b', line: '#5e1512', r: s * 0.12, la: 1 });
  g.restore();
  light(g, x, y + s * 0.6, s * 0.7, o.color || '#c4302b', 0.12);
  const hitAt = (o.impacts || []).find(at => t >= at && t - at < 0.16);
  if (hitAt !== undefined) {
    g.save(); g.globalCompositeOperation = 'lighter'; g.strokeStyle = alpha(o.spark || '#e8c28a', 0.8); g.lineWidth = 2.2;
    const age = t - hitAt;
    for (let i = 0; i < 5; i++) {
      const a = -0.7 + i * 0.35, r = s * (0.22 + age * 0.35);
      g.beginPath(); g.moveTo(x + Math.cos(a) * r, y + s * 0.45 + Math.sin(a) * r * 0.4);
      g.lineTo(x + Math.cos(a) * (r + s * 0.07), y + s * 0.45 + Math.sin(a) * (r + s * 0.07) * 0.4); g.stroke();
    }
    g.restore();
  }
}
export function barbell(g, x, gy, s) { ln(g, [[x - s * 0.7, gy - s * 0.18], [x + s * 0.7, gy - s * 0.18]], { lw: 6, color: '#8a8d96', la: 1 }); for (const d of [-1, 1]) for (let i = 0; i < 2; i++) box(g, x + d * s * (0.5 + i * 0.09) - 9, gy - s * 0.18 - s * (0.18 - i * 0.04), 18, s * (0.36 - i * 0.08), { fill: '#202127', r: 4 }); }
export function plant(g, x, gy, s) { box(g, x - s * 0.18, gy - s * 0.3, s * 0.36, s * 0.3, { fill: '#7a5340', r: 3 }); const r = rng(4); for (let i = 0; i < 7; i++) { const a = -Math.PI / 2 + (r() - 0.5) * 1.6; obj(g, (c) => c.ellipse(x + Math.cos(a) * s * 0.3, gy - s * 0.3 + Math.sin(a) * s * 0.35, s * 0.07, s * 0.24, a + Math.PI / 2, 0, 7), { fill: '#4f7a4e', line: '#2c4a2c', la: 0.6 }); } }
export function bench(g, x, gy, w) { box(g, x - w / 2, gy - 52, w, 10, { fill: '#6b4e3a', r: 3 }); box(g, x - w / 2, gy - 82, w, 9, { fill: '#6b4e3a', r: 3 }); ln(g, [[x - w * 0.4, gy - 42], [x - w * 0.4, gy]], { lw: 4 }); ln(g, [[x + w * 0.4, gy - 42], [x + w * 0.4, gy]], { lw: 4 }); }
export function streetLamp(g, x, gy, h, on = true) { ln(g, [[x, gy], [x, gy - h], [x + h * 0.12, gy - h - 10]], { lw: 4, color: '#555861', la: 1 }); if (on) { light(g, x + h * 0.12, gy - h - 4, h * 0.35, PAL.lamp, 0.5); beam(g, x + h * 0.12, gy - h, x - h * 0.15, x + h * 0.4, gy, PAL.lamp, 0.08); } }

function skyline(g, gy, o = {}) {
  const r = rng(o.seed || 11), n = o.n || 14, col = o.color || '#1b1622', lit = o.lit ?? 0.25;
  for (let i = 0; i < n; i++) {
    const w = E.W / n * (0.8 + r() * 0.6), x = i * E.W / n - 20, h = E.H * (o.hmin ?? 0.18) + r() * E.H * (o.hvar ?? 0.28);
    obj(g, (c) => c.rect(x, gy - h, w, h + 4), { fill: col, line: o.line ?? null, la: 0.25 });
    if (lit) for (let k = 0; k < h / 34; k++) for (let j = 0; j < w / 30; j++) if (r() < lit) { g.fillStyle = alpha(PAL.lamp, 0.35 + r() * 0.4); g.fillRect(x + 10 + j * 30, gy - h + 14 + k * 34, 8, 12); }
  }
}

// ---------- boi canh
// moc tra ve: { gy, bed: {head:[x,y], sit:[x,y], lie:[x,y]}, clock:[x,y], desk:{seat:[x,y]}, door:[x,y], ... }
export function set(g, kind = 'bedroom', o = {}) {
  const t = o.t || 0, gy = Y(o.gy ?? (E.vertical ? 0.7 : 0.8)), M = { gy };
  switch (kind) {
    case 'black': fillAll(g, '#0b0b0d'); break;
    case 'void': {
      fillAll(g, '#0d0d10'); const sx = X(o.spot ?? 0.5); beam(g, sx, -20, sx - E.W * 0.16, sx + E.W * 0.16, gy + 40, '#e8e4dc', 0.13);
      g.save(); g.scale(1, 0.18); light(g, sx, gy / 0.18, E.W * 0.16, '#e8e4dc', 0.22); g.restore(); ln(g, [[-60, gy], [E.W + 60, gy]], { lw: 1.5, la: 0.18 }); dust(g, t, { n: 30 }); break; }
    case 'bedroom': {
      wall(g); floor(g, gy);
      const bx = VX(o.bedX ?? 0.27), bw = E.vertical ? E.W * 0.5 : X(o.bedW ?? 0.33), bh = E.H * 0.11;
      if (o.stage) {
        for (const q of [0.035, 0.235, 0.47, 0.765, 0.965]) ln(g, [[X(q), Y(0.10)], [X(q), gy - 28]], { color: '#56515e', lw: 2, la: 0.28 });
        ln(g, [[0, Y(0.145)], [E.W, Y(0.145)]], { color: '#514b58', lw: 3, la: 0.32 });
        ln(g, [[0, gy - 24], [E.W, gy - 24]], { color: '#59535f', lw: 4, la: 0.46 });
        for (let i = -3; i <= 3; i++) ln(g, [[E.W * 0.5 + i * E.W * 0.045, gy + 8], [E.W * 0.5 + i * E.W * 0.22, E.H + 25]], { color: '#3d3c45', lw: 2, la: 0.20 });
        box(g, bx - 42, gy - 14, bw + 165, 54, { fill: '#191922', line: '#45414e', r: 10, la: 0.72, lw: 2 });
      }
      const wx = VX(o.windowX ?? 0.5), wy = Y(0.24), ww = E.vertical ? E.W * 0.26 : X(o.windowW ?? (o.stage ? 0.16 : 0.115)), wh = Y(0.2);
      if (o.window !== false) {
        windowBox(g, wx, wy, ww, wh, { sky: o.sky || 'moon', t });
        if ((o.sky || 'moon') === 'moon' || o.sky === 'dawn') beam(g, wx + ww / 2, wy + wh, bx + bw * 0.2, bx + bw * 0.9, gy + 30, o.sky === 'dawn' ? '#ffb48a' : '#c8d4ff', 0.07);
        if (o.stage) {
          const top = wy - 13, bottom = wy + wh + 27;
          obj(g, (c) => {
            c.moveTo(wx - 15, top); c.lineTo(wx + ww * 0.20, top); c.lineTo(wx + ww * 0.17, bottom - 3);
            c.quadraticCurveTo(wx + ww * 0.08, bottom - 18, wx - 15, bottom); c.closePath();
          }, { fill: '#302737', line: '#64536a', lw: 2, la: 0.96 });
          obj(g, (c) => {
            c.moveTo(wx + ww * 0.80, top); c.lineTo(wx + ww + 15, top); c.lineTo(wx + ww + 15, bottom);
            c.quadraticCurveTo(wx + ww * 0.91, bottom - 12, wx + ww * 0.82, bottom - 3); c.closePath();
          }, { fill: '#302737', line: '#64536a', lw: 2, la: 0.96 });
          box(g, wx - 18, wy - 15, ww + 36, 7, { fill: '#62556a', line: '#85728a', r: 3, la: 0.85 });
          box(g, wx - 12, wy + wh + 8, ww + 24, 12, { fill: '#56515d', line: '#7c7583', r: 3, la: 0.88 });
          for (const q of [0.04, 0.13, 0.87, 0.96]) ln(g, [[wx + ww * q, wy + 3], [wx + ww * q, wy + wh - 2]], { color: '#8f7f91', lw: 2, la: 0.22 });
        }
      }
      if (o.calendar !== false && !E.vertical) calendar(g, X(o.calX ?? 0.79), Y(0.26), X(o.stage ? 0.065 : 0.055), o.calendar || {});
      if (o.desk !== false && !E.vertical) {
        const dx = X(o.deskX ?? 0.84), dw = X(o.deskW ?? (o.stage ? 0.22 : 0.15)), dh = E.H * (o.stage ? 0.20 : 0.17);
        table(g, dx, gy, dw, dh, { fill: o.stage ? '#403542' : '#3a3d45' });
        const chairX = dx - dw * (o.stage ? 0.32 : 0.15);
        chair(g, chairX, gy, E.H * (o.stage ? 0.14 : 0.20), -1);
        if (!o.phoneOnDesk) books(g, dx + dw * (o.stage ? 0.31 : 0.18), gy - dh, o.stage ? E.H * 0.065 : 60);
        deskLamp(g, dx - dw * 0.35, gy - dh, o.stage ? E.H * 0.085 : 90, o.lamp);
        if (o.laptop) laptop(g, dx + dw * (o.stage ? 0.02 : -0.02), gy - dh, o.stage ? E.H * 0.10 : 70, { on: o.laptop !== 'off', t, color: o.laptopColor });
        if (o.typing) {
          const kw = dw * (o.stage ? 0.30 : 0.26), kx = dx - dw * (o.stage ? 0.10 : 0.07), ky = gy - dh + 12;
          box(g, kx - kw / 2, ky - 9, kw, 18, { fill: '#20232b', line: '#7b8290', r: 4, lw: 1.2 });
          for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 11; col++) {
              const xx = kx - kw * 0.43 + col * kw * 0.078;
              const yy = ky - 6 + row * 4.6;
              box(g, xx, yy, kw * 0.054, 2.8, { fill: '#9198a5', line: null, r: 1, la: 0.86 });
            }
          }
          box(g, kx - kw * 0.19, ky + 5, kw * 0.38, 2.8, { fill: '#a6adb8', line: null, r: 1, la: 0.8 });
        }
        if (o.stage && !o.phoneOnDesk) {
          box(g, dx - dw * 0.40, gy - dh - 8, dw * 0.19, 8, { fill: '#d5d0c3', line: '#7c7780', r: 2, la: 0.82 });
          ln(g, [[dx - dw * 0.38, gy - dh - 5], [dx - dw * 0.24, gy - dh - 5]], { color: '#77727b', lw: 1.3, la: 0.7 });
        }
        let phonePos = null;
        if (o.phoneOnDesk) {
          const pCfg = typeof o.phoneOnDesk === 'object' ? o.phoneOnDesk : {};
          let px = pCfg.x !== undefined ? X(pCfg.x) : dx + dw * 0.30;
          if (pCfg.slide) {
            const slideK = ease.inOut(clamp((t - (pCfg.slide.at ?? 0.5)) / Math.max(0.1, pCfg.slide.dur ?? 0.5)));
            px += X(pCfg.slide.dx ?? 0) * slideK;
          }
          const vibrating = !!pCfg.vibrate && t >= (pCfg.vibrateAt ?? 0) && t <= (pCfg.vibrateUntil ?? 6);
          const jitter = vibrating ? Math.sin(t * 54) * 4.5 : 0;
          const py = gy - dh - 7;
          g.save(); g.translate(px + jitter, py); g.rotate(vibrating ? Math.sin(t * 54) * 0.025 : -0.035);
          box(g, -49, -30, 98, 60, { fill: '#0b0d12', line: '#7d8391', r: 9, lw: 3 });
          box(g, -41, -23, 82, 46, { fill: vibrating ? '#28334a' : '#20242d', line: '#444b5b', r: 6, lw: 1.5 });
          oval(g, -27, -10, 4, 4, { fill: '#9fb6ff', line: null });
          ln(g, [[-18, -10], [25, -10]], { color: '#c2c8d6', lw: 2, la: 0.72 });
          ln(g, [[-27, 1], [22, 1]], { color: '#8d94a4', lw: 2, la: 0.60 });
          if (vibrating) {
            ln(g, [[-58, -9], [-66, -16]], { color: '#9fb6ff', lw: 3, la: 0.8 });
            ln(g, [[58, -9], [66, -16]], { color: '#9fb6ff', lw: 3, la: 0.8 });
          }
          g.restore(); phonePos = [px, py];
        }
        M.desk = { seat: [chairX, gy], top: [dx, gy - dh], laptop: [dx + dw * (o.stage ? 0.02 : -0.02), gy - dh], phone: phonePos };
      }
      if (o.door) door(g, X(o.doorX ?? 0.95), gy, X(0.07), E.H * 0.42, { open: o.doorOpen });
      const nx = bx - E.W * (E.vertical ? 0.1 : 0.045);
      box(g, nx - 50, gy - 95, 100, 95, { fill: '#26272d', r: 6 });
      ln(g, [[nx - 40, gy - 55], [nx + 40, gy - 55]], { lw: 1.5, la: 0.5 });
      oval(g, nx, gy - 30, 4, 4, { fill: '#888', line: null });
      if (o.clock !== false) digitClock(g, nx, gy - 97, 62, { time: o.clock ?? '3:17', ring: o.ring, blink: o.blink, t });
      M.clock = [nx, gy - 130];
      ln(g, [[bx, gy], [bx, gy - E.H * 0.25]], { lw: 9, color: '#33353d', la: 1 });
      ln(g, [[bx, gy - E.H * 0.25], [bx, gy - E.H * 0.13]], { lw: 3, la: 0.5 });
      box(g, bx, gy - bh, bw, bh * 0.55, { fill: '#2c2e35', r: 4 });
      ln(g, [[bx + bw - 6, gy - bh * 0.5], [bx + bw - 6, gy]], { lw: 6, color: '#33353d', la: 1 });
      M.bed = { head: [bx + bw * 0.1, gy - bh - 22], sit: [bx + bw * 0.62, gy], lie: [bx + bw * 0.4, gy - bh], x0: bx, x1: bx + bw, top: gy - bh };
      M.pillow = () => oval(g, bx + bw * 0.1, gy - bh - 6, bw * 0.09, 16, { fill: PAL.pillow });
      M.blanket = (occupied) => obj(g, (c) => {
        c.moveTo(bx + bw * (occupied ? 0.17 : 0.24), gy - bh + 4);
        if (occupied) {
          c.quadraticCurveTo(bx + bw * 0.19, gy - bh - 34, bx + bw * 0.35, gy - bh - 28);
          c.quadraticCurveTo(bx + bw * 0.6, gy - bh - 36, bx + bw * 0.8, gy - bh - 18);
        } else c.quadraticCurveTo(bx + bw * 0.6, gy - bh - 14, bx + bw * 0.95, gy - bh - 4);
        c.lineTo(bx + bw * 0.98, gy - bh + bh * 0.5);
        c.lineTo(bx + bw * 0.16, gy - bh + bh * 0.5); c.closePath();
      }, { fill: PAL.blanket, line: '#8c95b5', la: 0.5 });
      if (!o.occupied) { M.pillow(); M.blanket(false); }
      break; }
    case 'city': {
      const tm = o.time || 'dusk', S = { dusk: ['#251c35', '#6a3f5c', '#d0745a'], night: ['#0c0f1c', '#182038', '#25304e'], dawn: ['#2a2a4a', '#8a5a78', '#f0a070'], day: ['#5c8fc4', '#8fb8de', '#cfe2f0'] }[tm] || ['#251c35', '#6a3f5c', '#d0745a'];
      vgrad(g, [[0, S[0]], [0.55, S[1]], [1, S[2]]], 0, gy);
      if (tm !== 'night') light(g, X(0.5), gy, E.W * 0.45, tm === 'day' ? '#ffffff' : '#ffb070', 0.35); else moon(g, X(0.8), Y(0.25), 22);
      skyline(g, gy, { color: tm === 'day' ? '#7d8fa6' : '#2a2033', seed: 3, hmin: 0.22, hvar: 0.3, lit: tm === 'day' ? 0 : 0.18 });
      skyline(g, gy, { color: tm === 'day' ? '#5d6e86' : '#17131d', seed: 8, n: 9, hmin: 0.1, hvar: 0.22, lit: tm === 'day' ? 0 : 0.3 });
      g.fillStyle = '#1a1a20'; g.fillRect(-60, gy, E.W + 120, E.H); ln(g, [[-60, gy], [E.W + 60, gy]], { lw: 2, la: 0.35 });
      for (let i = 0; i < 12; i++) { const x = ((i * 220 - t * (o.scroll || 0) * 60) % (E.W + 220) + E.W + 220) % (E.W + 220) - 110; g.fillStyle = 'rgba(200,200,210,0.25)'; g.fillRect(x, gy + (E.H - gy) * 0.55, 90, 5); }
      for (const k of o.lamps || [0.12, 0.88]) streetLamp(g, X(k), gy, E.H * 0.3);
      if (o.birds) { g.save(); g.strokeStyle = '#2a2030'; g.lineWidth = 2.5; for (let i = 0; i < 3; i++) { const bx = X(0.7) + i * 34 + t * 20, by = Y(0.25) + i * 10 + Math.sin(t * 3 + i) * 4; g.beginPath(); g.moveTo(bx - 8, by); g.quadraticCurveTo(bx - 3, by - 6, bx, by); g.quadraticCurveTo(bx + 3, by - 6, bx + 8, by); g.stroke(); } g.restore(); }
      break; }
    case 'street': {
      wall(g, '#15171d', '#1d212a'); skyline(g, gy - E.H * 0.05, { color: '#1b1f27', seed: 21, n: 10, hmin: 0.3, hvar: 0.25, lit: 0.12 });
      g.fillStyle = '#16181d'; g.fillRect(-60, gy, E.W + 120, E.H); ln(g, [[-60, gy], [E.W + 60, gy]], { lw: 2, la: 0.4 });
      if (o.neonDoor !== undefined && o.neonDoor !== false) { const dx = X(o.neonDoor === true ? 0.32 : o.neonDoor), dh = E.H * 0.34; box(g, dx - 60, gy - dh, 120, dh, { fill: '#0b0b0f', line: accent(), la: 0.9, lw: 3 }); g.save(); g.globalCompositeOperation = 'lighter'; const gr = g.createLinearGradient(0, gy - dh, 0, gy); gr.addColorStop(0, alpha(accent(), 0.05)); gr.addColorStop(1, alpha(accent(), 0.45)); g.fillStyle = gr; g.fillRect(dx - 56, gy - dh + 4, 112, dh - 4); g.restore(); light(g, dx, gy - dh * 0.5, dh * 0.8, accent(), 0.2); M.neon = [dx, gy]; }
      if (o.busstop !== false) { const sx = X(o.busX ?? 0.72), sw = X(0.2); box(g, sx - sw / 2, gy - E.H * 0.36, sw, 10, { fill: '#30333b' }); ln(g, [[sx - sw / 2 + 6, gy - E.H * 0.36], [sx - sw / 2 + 6, gy]], { lw: 5 }); ln(g, [[sx + sw / 2 - 6, gy - E.H * 0.36], [sx + sw / 2 - 6, gy]], { lw: 5 }); g.fillStyle = 'rgba(160,180,210,0.07)'; g.fillRect(sx - sw / 2 + 8, gy - E.H * 0.35, sw - 16, E.H * 0.3); bench(g, sx, gy, sw * 0.7); light(g, sx, gy - E.H * 0.34, sw * 0.6, '#d8e4ff', 0.25); box(g, sx + sw / 2 + 20, gy - E.H * 0.42, 34, 26, { fill: '#2f6fd0', r: 3 }); M.bus = { seat: [sx, gy], x: sx }; }
      streetLamp(g, X(o.lampX ?? 0.55), gy, E.H * 0.42);
      if (o.rain !== false) { rain(g, t, { n: 180 }); g.save(); g.globalAlpha = 0.12; g.fillStyle = '#9fb0d0'; for (let i = 0; i < 10; i++) g.fillRect(X(0.05 + i * 0.1), gy + 12 + (i % 3) * 18, 70, 3); g.restore(); }
      break; }
    case 'lockers': {
      wall(g, '#1c1d22', '#23252c'); floor(g, gy, '#1e1f24'); const n = 16, lw = E.W / n, top = gy - E.H * 0.5, cs = ['#3d5277', '#3d5277', '#6b3f3f', '#3d5277', '#3d5277', '#3d5277', '#6b3f3f'];
      for (let i = 0; i < n; i++) { const x = i * lw; box(g, x + 2, top, lw - 4, E.H * 0.5, { fill: cs[(i * 3) % cs.length], line: '#151619', la: 0.8, r: 3 }); ln(g, [[x + lw * 0.3, top + E.H * 0.12], [x + lw * 0.3, top + E.H * 0.18]], { lw: 3, la: 0.6 }); for (let k = 0; k < 3; k++) ln(g, [[x + lw * 0.55, top + 20 + k * 10], [x + lw * 0.8, top + 20 + k * 10]], { lw: 2, la: 0.3 }); }
      if (o.board !== false) { const bx = X(o.boardX ?? 0.68); box(g, bx - 110, top - E.H * 0.17, 220, 130, { fill: '#8a6a45', r: 8 }); const nc = ['#f4e48b', '#bcdaf5', '#f4e48b', '#f2f0ea']; for (let i = 0; i < 4; i++) box(g, bx - 90 + i * 46, top - E.H * 0.15 + (i % 2) * 22, 38, 42, { fill: nc[i], line: null, r: 2 }); }
      break; }
    case 'classroom': {
      wall(g, '#1e2027', '#24262e'); floor(g, gy, '#1d1e23'); windowBox(g, X(0.08), Y(0.18), X(0.16), Y(0.28), { sky: o.sky || 'day', t });
      box(g, X(0.62), Y(0.17), X(0.3), Y(0.3), { fill: '#2b3a33', line: '#8c7a68', r: 4 }); text(g, o.board || 'x + 4 = 10', X(0.77), Y(0.27), { size: 46, font: FONT_NARR, weight: 700, color: '#d8ddd5' }); text(g, 'x = ?', X(0.72), Y(0.37), { size: 46, font: FONT_NARR, weight: 700, color: '#d8ddd5' });
      oval(g, X(0.47), Y(0.18), 26, 26, { fill: '#e9e6df', line: '#555' }); ln(g, [[X(0.47), Y(0.18)], [X(0.47), Y(0.18) - 16]], { color: '#222', lw: 3, la: 1 }); ln(g, [[X(0.47), Y(0.18)], [X(0.47) + 12, Y(0.18)]], { color: '#222', lw: 3, la: 1 });
      for (const k of o.desks || [0.2, 0.45, 0.7]) table(g, X(k) + 60, gy, 150, E.H * 0.16, { fill: '#5a4a3c' });
      break; }
    case 'court': {
      vgrad(g, [[0, '#2a2038'], [1, '#7a4a5c']], 0, gy - E.H * 0.1); skyline(g, gy - E.H * 0.1, { color: '#2a2234', seed: 5, n: 12, hmin: 0.12, hvar: 0.18, lit: 0.25 });
      g.fillStyle = '#b77a45'; g.fillRect(-60, gy - E.H * 0.1, E.W + 120, E.H); ln(g, [[-60, gy + E.H * 0.06], [E.W + 60, gy + E.H * 0.06]], { lw: 3, color: '#f0d6b0', la: 0.5 });
      g.save(); g.strokeStyle = 'rgba(200,200,210,0.25)'; g.lineWidth = 1.5; const ft = gy - E.H * 0.42, fb = gy - E.H * 0.1; for (let x = -200; x < E.W + 200; x += 26) { g.beginPath(); g.moveTo(x, fb); g.lineTo(x + (fb - ft), ft); g.moveTo(x, ft); g.lineTo(x + (fb - ft), fb); g.stroke(); } g.restore(); ln(g, [[-60, gy - E.H * 0.42], [E.W + 60, gy - E.H * 0.42]], { lw: 3, la: 0.5 });
      const hx = X(o.hoopX ?? 0.84); ln(g, [[hx, gy], [hx, gy - E.H * 0.5]], { lw: 7, color: '#3d4048', la: 1 }); box(g, hx - 70, gy - E.H * 0.56, 90, 60, { fill: '#e9e6df', line: '#444', r: 2 }); oval(g, hx - 80, gy - E.H * 0.47, 26, 6, { fill: null, line: '#e2562b', lw: 4, la: 1 });
      streetLamp(g, X(0.55), gy - E.H * 0.1, E.H * 0.35); bench(g, X(o.benchX ?? 0.3), gy - E.H * 0.06, 220); M.bench = [X(o.benchX ?? 0.3), gy - E.H * 0.06];
      break; }
    case 'cafe': {
      wall(g, '#2a2019', '#33271f'); floor(g, gy, '#241b15');
      const wx = X(0.22), ww = X(0.56);
      box(g, wx, Y(0.16), ww, Y(0.42), { fill: '#141821', line: '#6b5644', r: 4 });
      g.save(); g.beginPath(); g.rect(wx, Y(0.16), ww, Y(0.42)); g.clip();
      skyline(g, Y(0.58), { color: '#1d2230', seed: 13, n: 9, hmin: 0.12, hvar: 0.2, lit: 0.35 });
      rain(g, t, { n: 70, a: 0.3 }); g.restore();
      ln(g, [[wx + ww / 2, Y(0.16)], [wx + ww / 2, Y(0.58)]], { lw: 4, color: '#6b5644', la: 1 });
      const lx = X(o.lampX ?? 0.5);
      ln(g, [[lx, -10], [lx, Y(0.2)]], { lw: 2, color: '#666' });
      obj(g, (c) => { c.moveTo(lx - 40, Y(0.26)); c.lineTo(lx + 40, Y(0.26)); c.lineTo(lx + 12, Y(0.2)); c.lineTo(lx - 12, Y(0.2)); c.closePath(); }, { fill: '#c99a3a', line: null });
      light(g, lx, Y(0.27), E.H * 0.55, PAL.lamp, 0.45);
      const tw = E.W * (o.tableW ?? 0.26), th = E.H * 0.20;
      const leftX = lx - tw * 0.68, rightX = lx + tw * 0.68;
      chair(g, leftX, gy, E.H * 0.16, -1); chair(g, rightX, gy, E.H * 0.16, 1);
      table(g, lx, gy, tw, th, { fill: '#5a3f2c' });
      for (const cupX of [lx - tw * 0.25, lx + tw * 0.25]) {
        box(g, cupX - 23, gy - th - 55, 46, 50, { fill: '#ded7c9', line: '#786a5c', r: 7, lw: 2 });
        oval(g, cupX, gy - th - 54, 19, 4, { fill: '#4d3a2b', line: '#a99579', lw: 1.5 });
        g.save(); g.strokeStyle = alpha('#ead8bd', 0.35); g.lineWidth = 2.2;
        for (let k = 0; k < 2; k++) {
          const sx = cupX - 8 + k * 15, wob = Math.sin(t * 2.5 + k) * 4;
          g.beginPath(); g.moveTo(sx, gy - th - 59); g.bezierCurveTo(sx - 10, gy - th - 75, sx + 10 + wob, gy - th - 83, sx + wob, gy - th - 94); g.stroke();
        }
        g.restore();
      }
      plant(g, X(0.9), gy, 160);
      M.table = { left: [leftX, gy], right: [rightX, gy], top: gy - th };
      break; }
    case 'gym': {
      wall(g, '#141417', '#1a1a1e'); floor(g, gy, '#111114'); for (let i = 0; i < 8; i++) ln(g, [[X(i / 7), gy], [X(i / 7) + (i - 3.5) * 40, E.H]], { lw: 1, la: 0.12 });
      beam(g, X(o.spot ?? 0.5), -20, X(o.spot ?? 0.5) - 380, X(o.spot ?? 0.5) + 380, gy + 60, '#ffe2b0', 0.1);
      if (o.bag !== false) punchBag(g, X(o.bagX ?? 0.62), Y(0.1), E.H * 0.42, { t, swing: o.swing, impacts: o.impacts, impactSwing: o.impactSwing, spark: o.spark });
      if (o.barbell) barbell(g, X(o.barbellX ?? 0.3), gy, 220);
      break; }
    case 'stairs': {
      fillAll(g, '#0f0f12'); const n = 9, sx = X(0.1), sy = gy, dx = (E.W * 0.85) / n, dy = (E.H * 0.62) / n;
      obj(g, (c) => { c.moveTo(sx, sy + 200); for (let i = 0; i < n; i++) { c.lineTo(sx + i * dx, sy - i * dy); c.lineTo(sx + (i + 1) * dx, sy - i * dy); } c.lineTo(E.W + 60, sy - n * dy); c.lineTo(E.W + 60, E.H + 60); c.lineTo(sx, E.H + 60); c.closePath(); }, { fill: '#25262c', line: PAL.line, la: 0.5 });
      if (o.top !== false) light(g, E.W * 0.98, sy - n * dy, E.H * 0.5, o.topColor || '#ffd9a0', 0.35);
      M.step = (k) => [sx + (k + 0.5) * dx, sy - k * dy]; M.steps = n;
      break; }
    case 'hill': {
      vgrad(g, [[0, '#2a1c2e'], [0.45, '#6b3446'], [0.8, '#c4604a'], [1, '#e8915a']], 0, gy); light(g, X(0.55), gy - E.H * 0.06, E.W * 0.4, '#ffb070', 0.45);
      for (const [c, a, s] of [['#4a2a3a', 0.18, 2], ['#3a2030', 0.12, 5]]) { g.fillStyle = c; g.beginPath(); g.moveTo(-60, gy); const r = rng(s); for (let i = 0; i <= 10; i++) g.lineTo(-60 + i * (E.W + 120) / 10, gy - E.H * a * (0.4 + r())); g.lineTo(E.W + 60, gy); g.closePath(); g.fill(); }
      g.fillStyle = '#c87a50'; g.fillRect(-60, gy, E.W + 120, E.H * 0.04); g.fillStyle = '#18121a'; g.beginPath(); g.moveTo(X(0.18), E.H + 20); g.quadraticCurveTo(X(0.45), gy - E.H * 0.33, X(0.72), E.H + 20); g.closePath(); g.fill();
      ln(g, [[X(0.25), E.H * 0.97], [X(0.45), gy - E.H * 0.16]], { color: '#e8915a', lw: 2, la: 0.4 });
      M.top = [X(0.45), gy - E.H * 0.165];
      break; }
    case 'mirror': {
      wall(g, '#1b1d22', '#202228'); g.save(); g.strokeStyle = 'rgba(200,205,215,0.09)'; g.lineWidth = 2; for (let x = 0; x < E.W; x += 70) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, E.H); g.stroke(); } for (let y = 0; y < E.H; y += 70) { g.beginPath(); g.moveTo(0, y); g.lineTo(E.W, y); g.stroke(); } g.restore();
      const mx = X(o.mirrorX ?? 0.55), mw = X(0.18), mh = Y(0.36); box(g, mx - mw / 2, Y(0.24), mw, mh, { fill: '#2b3038', line: PAL.line, r: 10 }); box(g, mx - mw * 0.35, Y(0.2), mw * 0.7, 10, { fill: '#e8ecf5', line: null, r: 5 }); light(g, mx, Y(0.2), mw * 0.8, '#e8ecf5', 0.35);
      box(g, mx - mw * 0.6, gy - E.H * 0.2, mw * 1.2, E.H * 0.06, { fill: '#c9ccd4', line: '#666', r: 6 });
      M.mirror = { x: mx, y: Y(0.24), w: mw, h: mh };
      break; }
    case 'kitchen': {
      wall(g, '#1c1e24', '#22242b'); floor(g, gy); windowBox(g, X(0.45), Y(0.2), X(0.12), Y(0.2), { sky: o.sky || 'moon', t });
      box(g, X(0.08), gy - E.H * 0.5, X(0.11), E.H * 0.5, { fill: '#3a3d45', r: 6 }); ln(g, [[X(0.08), gy - E.H * 0.3], [X(0.19), gy - E.H * 0.3]], { lw: 2, la: 0.5 });
      box(g, X(0.25), gy - E.H * 0.2, X(0.6), E.H * 0.2, { fill: '#2c2e35', r: 3 }); box(g, X(0.25), gy - E.H * 0.22, X(0.6), 14, { fill: '#4a4d55', r: 3 }); box(g, X(0.62), Y(0.17), X(0.22), E.H * 0.16, { fill: '#2c2e35', r: 3 });
      if (o.lamp) light(g, X(0.5), gy - E.H * 0.24, E.H * 0.4, PAL.lamp, 0.3);
      break; }
    case 'doorway': {
      wall(g, '#121216', '#18181d'); floor(g, gy); door(g, X(o.doorX ?? 0.62), gy, X(0.1), E.H * 0.45, { open: o.doorOpen ?? 1 }); M.door = [X(o.doorX ?? 0.62), gy];
      break; }
    // ---------- New cinematic environments (authored in-code; no third-party image dependency)
    case 'metro': {
      wall(g, '#121821', '#242d38');
      // Tunnel ribs converge toward a distant vanishing point.
      const vx = X(0.52), vy = Y(0.28);
      for (let i = 0; i < 8; i++) {
        const k = i / 7, x = X(-0.06 + k * 1.12), yTop = Y(0.08 + Math.abs(k - 0.5) * 0.15);
        ln(g, [[x, yTop], [vx + (x - vx) * 0.28, vy], [x, gy - E.H * 0.02]], { color: '#69717e', lw: 4, la: 0.32 });
      }
      box(g, 0, Y(0.5), E.W, Y(0.13), { fill: '#1b222c', line: '#454d5a', r: 0, la: 0.9, lw: 2 });
      for (let i = 0; i < 14; i++) {
        const x = i * E.W / 13;
        ln(g, [[x, Y(0.51)], [x, Y(0.63)]], { color: '#88919d', lw: 2, la: 0.2 });
      }
      // Platform edge and tracks add strong horizontal/perspective cues.
      floor(g, gy, '#282b32');
      ln(g, [[0, gy - 18], [E.W, gy - 18]], { color: '#e6b65e', lw: 8, la: 0.9 });
      ln(g, [[0, gy + E.H * 0.07], [vx, gy + E.H * 0.02], [E.W, gy + E.H * 0.07]], { color: '#818995', lw: 5, la: 0.55 });
      ln(g, [[0, gy + E.H * 0.13], [vx, gy + E.H * 0.03], [E.W, gy + E.H * 0.13]], { color: '#818995', lw: 4, la: 0.42 });
      for (const k of [0.12, 0.36, 0.62, 0.87]) {
        box(g, X(k) - 40, Y(0.06), 80, 16, { fill: '#e6e0d3', line: null, r: 4, la: 0.9 });
        light(g, X(k), Y(0.1), E.H * 0.22, '#d4e6ff', 0.12);
      }
      box(g, X(0.06), Y(0.17), X(0.17), Y(0.08), { fill: '#243d47', line: '#8cabb0', r: 4, lw: 2 });
      text(g, o.sign || 'PLATFORM 02', X(0.145), Y(0.222), { size: 22, font: FONT_UI, weight: 700, color: '#dce9e6' });
      M.platform = [X(0.5), gy - 10]; M.vanish = [vx, vy];
      break;
    }
    case 'rooftop': {
      const tm = o.time || 'dusk';
      const sky = tm === 'dawn' ? [[0, '#292a4a'], [0.58, '#9a647c'], [1, '#f2ad7e']] :
        tm === 'night' ? [[0, '#090f20'], [0.65, '#202b45'], [1, '#3f4050']] :
        [[0, '#171b32'], [0.55, '#5a4568'], [1, '#c77d70']];
      vgrad(g, sky, 0, gy);
      skyline(g, gy - E.H * 0.04, { color: '#252335', seed: 19, n: 15, hmin: 0.18, hvar: 0.34, lit: tm === 'night' ? 0.36 : 0.14 });
      skyline(g, gy - E.H * 0.02, { color: '#171b27', seed: 27, n: 11, hmin: 0.10, hvar: 0.2, lit: 0.22 });
      if (tm === 'night') moon(g, X(0.78), Y(0.19), E.H * 0.025);
      else light(g, X(0.7), Y(0.42), E.H * 0.34, '#ffb878', 0.23);
      floor(g, gy, '#25232e');
      // Roof tiles and leading lines guide the eye into the frame.
      for (let i = -4; i <= 4; i++) ln(g, [[E.W * 0.5 + i * 18, gy], [E.W * 0.5 + i * 140, E.H + 24]], { color: '#77707d', lw: 2, la: 0.2 });
      box(g, 0, gy - E.H * 0.16, E.W, E.H * 0.16, { fill: '#36313f', line: '#8a7281', r: 0, la: 1, lw: 3 });
      ln(g, [[0, gy - E.H * 0.16], [E.W, gy - E.H * 0.16]], { color: '#d1b0a0', lw: 4, la: 0.48 });
      // Ventilation blocks, water tank, aerial and warm maintenance lamp.
      box(g, X(0.12), gy - E.H * 0.31, X(0.16), E.H * 0.15, { fill: '#4a4652', line: '#77717c', r: 5 });
      for (let j = 0; j < 5; j++) ln(g, [[X(0.13), gy - E.H * (0.29 - j * 0.022)], [X(0.27), gy - E.H * (0.29 - j * 0.022)]], { color: '#9b929c', lw: 2, la: 0.36 });
      box(g, X(0.73), gy - E.H * 0.28, X(0.12), E.H * 0.12, { fill: '#343642', line: '#86818a', r: 10 });
      oval(g, X(0.79), gy - E.H * 0.28, X(0.06), E.H * 0.025, { fill: '#585561', line: '#96909a', lw: 2 });
      ln(g, [[X(0.86), gy - E.H * 0.28], [X(0.86), gy - E.H * 0.43], [X(0.91), gy - E.H * 0.43]], { color: '#a29ba7', lw: 3, la: 0.8 });
      light(g, X(0.31), gy - E.H * 0.27, E.H * 0.25, '#ffc878', 0.18);
      M.parapet = [X(0.5), gy - E.H * 0.16]; M.vent = [X(0.2), gy - E.H * 0.2];
      break;
    }
    case 'underpass': {
      wall(g, '#171b24', '#272d37');
      const vanX = X(o.vanishX ?? 0.52), vanY = Y(0.24);
      // Receding concrete ribs and wet floor make the depth legible.
      for (let i = 0; i < 7; i++) {
        const x = X(-0.1 + i * 0.2), top = Y(0.02 + Math.abs(i - 3) * 0.035);
        obj(g, (c) => {
          c.moveTo(x - E.W * 0.075, top); c.lineTo(x + E.W * 0.075, top);
          c.lineTo(vanX + (x + E.W * 0.075 - vanX) * 0.55, gy - 10);
          c.lineTo(vanX + (x - E.W * 0.075 - vanX) * 0.55, gy - 10); c.closePath();
        }, { fill: '#303541', line: '#737b87', lw: 3, la: 0.65, a: 0.72 });
      }
      floor(g, gy, '#1a1f28');
      for (let i = 0; i < 7; i++) {
        const x = X(i / 6);
        ln(g, [[x, gy], [vanX + (x - vanX) * 0.08, vanY]], { color: '#656d79', lw: 2, la: 0.23 });
      }
      for (const [x, c] of [[0.18, '#dbe9ff'], [0.48, '#f1d2a0'], [0.79, '#c5dcff']]) {
        box(g, X(x) - 48, Y(0.12 + Math.abs(x - 0.5) * 0.08), 96, 14, { fill: c, line: null, r: 5, la: 0.78 });
        light(g, X(x), Y(0.17), E.H * 0.31, c, 0.16);
      }
      // Puddles reflect the lamps without overwhelming the character silhouette.
      for (let i = 0; i < 5; i++) oval(g, X(0.13 + i * 0.18), gy + E.H * (0.055 + (i % 2) * 0.03), E.W * (0.032 + (i % 3) * 0.008), E.H * 0.008, { fill: '#8b9aaf', line: null, a: 0.13 });
      if (o.rain) rain(g, t, { n: 90, a: 0.16, speed: 880 });
      M.vanish = [vanX, vanY]; M.walkway = [X(0.5), gy];
      break;
    }
    case 'hospital': {
      wall(g, '#172329', '#26363c');
      const vx = X(0.5), vy = Y(0.2);
      // Long corridor with paired doors, ceiling panels and perspective floor.
      box(g, X(0.22), Y(0.1), X(0.56), Y(0.49), { fill: '#202e34', line: '#61777b', r: 0, lw: 3, la: 0.72 });
      obj(g, (c) => { c.moveTo(0, 0); c.lineTo(X(0.22), Y(0.1)); c.lineTo(X(0.22), Y(0.59)); c.lineTo(0, gy); c.closePath(); }, { fill: '#1d3036', line: '#71888b', lw: 2, la: 0.48 });
      obj(g, (c) => { c.moveTo(E.W, 0); c.lineTo(X(0.78), Y(0.1)); c.lineTo(X(0.78), Y(0.59)); c.lineTo(E.W, gy); c.closePath(); }, { fill: '#1d3036', line: '#71888b', lw: 2, la: 0.48 });
      for (const side of [0.08, 0.92]) {
        for (let i = 0; i < 3; i++) {
          const y = Y(0.17 + i * 0.13), w = E.W * (0.12 - i * 0.018);
          box(g, side < 0.5 ? X(side) : X(side) - w, y, w, E.H * (0.12 - i * 0.015), { fill: '#34454b', line: '#6c8186', r: 2, lw: 2, la: 0.8 });
          box(g, side < 0.5 ? X(side) + w * 0.7 : X(side) - w * 0.25, y + E.H * 0.055, 6, 6, { fill: '#b7a98c', line: null, r: 2 });
        }
      }
      floor(g, gy, '#28333a');
      for (let i = 0; i < 9; i++) {
        const x = X(i / 8);
        ln(g, [[vx, Y(0.55)], [x, gy + E.H * 0.2]], { color: '#6e8286', lw: 2, la: 0.24 });
      }
      for (let i = 0; i < 5; i++) box(g, X(0.32 + i * 0.09), Y(0.07), X(0.055), 18, { fill: '#d5e7df', line: null, r: 4, la: 0.85 });
      box(g, X(0.38), Y(0.25), X(0.24), Y(0.055), { fill: '#31564d', line: '#8db2a0', r: 4 });
      text(g, o.sign || 'QUIET ZONE', X(0.5), Y(0.287), { size: 22, font: FONT_UI, weight: 700, color: '#e2f0e8' });
      light(g, X(0.5), Y(0.15), E.H * 0.4, '#d7f0ec', 0.10);
      M.corridor = [vx, gy]; M.doorLeft = [X(0.16), Y(0.53)]; M.doorRight = [X(0.84), Y(0.53)];
      break;
    }
    case 'library': {
      wall(g, '#211c22', '#30252b');
      // High windows, tall shelves and a central aisle.
      windowBox(g, X(0.05), Y(0.1), X(0.17), Y(0.28), { sky: o.sky || 'dawn', t });
      for (const side of [0, 1]) {
        const sx = side === 0 ? X(0.025) : X(0.76), sw = E.W * 0.215;
        box(g, sx, Y(0.08), sw, gy - Y(0.08), { fill: '#46332d', line: '#96745c', r: 3, lw: 3, la: 0.82 });
        for (let shelf = 0; shelf < 5; shelf++) {
          const y = Y(0.16 + shelf * 0.115);
          ln(g, [[sx + 5, y], [sx + sw - 5, y]], { color: '#a28a73', lw: 5, la: 0.75 });
          for (let b = 0; b < 15; b++) {
            const x = sx + 10 + b * (sw - 22) / 15, bh = E.H * (0.045 + ((b * 7 + shelf * 3) % 5) * 0.009);
            const colors = ['#607080', '#9a6754', '#b69a65', '#526657', '#78677d', '#d0bda0'];
            box(g, x, y - bh, Math.max(5, sw / 24), bh, { fill: colors[(b + shelf * 2) % colors.length], line: '#30252a', r: 1, lw: 1, la: 0.92 });
          }
        }
      }
      // Perspective aisle floor and reading tables.
      floor(g, gy, '#1e1b20');
      for (let i = -3; i <= 3; i++) ln(g, [[X(0.5), Y(0.39)], [X(0.5) + i * E.W * 0.18, E.H + 20]], { color: '#7d6570', lw: 2, la: 0.25 });
      table(g, X(0.5), gy, X(0.38), E.H * 0.22, { fill: '#644637' });
      for (const x of [0.39, 0.61]) {
        books(g, X(x), gy - E.H * 0.22, E.H * 0.11);
        deskLamp(g, X(x), gy - E.H * 0.22, E.H * 0.08, true);
        light(g, X(x), gy - E.H * 0.22, E.H * 0.23, '#ffc77d', 0.18);
      }
      // Ladder silhouette on the right shelf.
      ln(g, [[X(0.81), Y(0.22)], [X(0.85), gy]], { color: '#bba07c', lw: 5, la: 0.7 });
      ln(g, [[X(0.87), Y(0.22)], [X(0.91), gy]], { color: '#bba07c', lw: 5, la: 0.7 });
      for (let i = 0; i < 7; i++) ln(g, [[X(0.82 + i * 0.013), Y(0.27 + i * 0.08)], [X(0.87 + i * 0.013), Y(0.27 + i * 0.08)]], { color: '#bba07c', lw: 3, la: 0.7 });
      M.table = { left: [X(0.32), gy], right: [X(0.68), gy], top: [X(0.5), gy - E.H * 0.22] };
      M.aisle = [X(0.5), gy];
      break;
    }
    case 'warehouse': {
      wall(g, '#1a1c21', '#272b31');
      const vx = X(0.52), vy = Y(0.18);
      // Roof trusses and steel columns form large industrial scale.
      for (let i = 0; i < 7; i++) {
        const x = X(i / 6);
        ln(g, [[x, 0], [vx + (x - vx) * 0.22, vy], [x, gy]], { color: '#747b82', lw: 5, la: 0.36 });
        ln(g, [[x, Y(0.08)], [vx + (x - vx) * 0.22, vy + 18], [E.W - x, Y(0.08)]], { color: '#535a63', lw: 3, la: 0.34 });
      }
      for (const x of [0.12, 0.34, 0.7, 0.89]) {
        box(g, X(x) - E.W * 0.035, Y(0.27), E.W * 0.07, gy - Y(0.27), { fill: '#353b43', line: '#69717a', r: 2, lw: 2, la: 0.92 });
      }
      // Stacked crates have different footprints/heights, rather than repeated flat cards.
      const crates = [[0.08, 0.61, 0.12, 0.16], [0.2, 0.69, 0.14, 0.11], [0.76, 0.58, 0.13, 0.19], [0.86, 0.7, 0.09, 0.09]];
      for (let i = 0; i < crates.length; i++) {
        const [x, y, w, h] = crates[i];
        box(g, X(x), Y(y), X(w), Y(h), { fill: i % 2 ? '#5a5044' : '#665744', line: '#9b8870', r: 2, lw: 2 });
        ln(g, [[X(x + 0.025), Y(y + 0.025)], [X(x + w - 0.025), Y(y + h - 0.025)]], { color: '#b7a084', lw: 3, la: 0.48 });
        ln(g, [[X(x + w - 0.025), Y(y + 0.025)], [X(x + 0.025), Y(y + h - 0.025)]], { color: '#b7a084', lw: 3, la: 0.32 });
      }
      floor(g, gy, '#202329');
      for (let i = 0; i < 5; i++) {
        const x = X(0.16 + i * 0.17);
        box(g, x - 35, Y(0.1), 70, 12, { fill: '#d3dce2', line: null, r: 5, la: 0.76 });
        light(g, x, Y(0.15), E.H * 0.28, '#e8d8ad', 0.12);
      }
      beam(g, X(0.72), Y(0.16), X(0.6), X(0.9), gy, '#ffd08b', 0.08);
      M.vanish = [vx, vy]; M.crates = [X(0.16), Y(0.68)]; M.gy = gy;
      break;
    }
    case 'laboratory': {
      wall(g, '#12212a', '#24333b');
      // Long windows suggest a working lab, not a generic sci-fi HUD.
      for (let i = 0; i < 4; i++) {
        const x = X(0.05 + i * 0.15);
        box(g, x, Y(0.12), X(0.125), Y(0.26), { fill: '#263a46', line: '#7296a0', r: 3, lw: 3, la: 0.9 });
        ln(g, [[x + X(0.0625), Y(0.12)], [x + X(0.0625), Y(0.38)]], { color: '#6d929d', lw: 2, la: 0.5 });
        light(g, x + X(0.0625), Y(0.24), E.H * 0.18, '#7bd5db', 0.1);
      }
      box(g, X(0.67), Y(0.11), X(0.27), Y(0.18), { fill: '#0e171e', line: '#52727b', r: 5, lw: 3 });
      // Oscilloscope and simple signal traces.
      ln(g, [[X(0.69), Y(0.21)], [X(0.73), Y(0.21)], [X(0.75), Y(0.15)], [X(0.79), Y(0.25)], [X(0.83), Y(0.19)], [X(0.88), Y(0.19),], [X(0.92), Y(0.23)]], { color: '#67d8cb', lw: 3, la: 0.95 });
      floor(g, gy, '#182329');
      table(g, X(0.5), gy, X(0.72), E.H * 0.24, { fill: '#38454c' });
      // Flask/vial silhouettes with colored liquid and a warm task lamp.
      for (let i = 0; i < 5; i++) {
        const x = X(0.25 + i * 0.105), h = E.H * (0.075 + (i % 3) * 0.02), y = gy - E.H * 0.24;
        box(g, x - 10, y - h, 20, h, { fill: '#17353d', line: '#82b9bd', r: 5, lw: 2, la: 0.95 });
        box(g, x - 7, y - h * 0.42, 14, h * 0.32, { fill: ['#3ca9a0', '#90bd86', '#cf9d5c', '#6484b4', '#9a7ab0'][i], line: null, r: 3, la: 0.88 });
        ln(g, [[x - 2, y - h + 7], [x - 2, y - h * 0.45]], { color: '#e1f8f2', lw: 2, la: 0.45 });
      }
      deskLamp(g, X(0.77), gy - E.H * 0.24, E.H * 0.12, true);
      light(g, X(0.77), gy - E.H * 0.24, E.H * 0.3, '#ffcf82', 0.2);
      M.table = { left: [X(0.14), gy], right: [X(0.86), gy], top: [X(0.5), gy - E.H * 0.24] };
      M.scope = [X(0.8), Y(0.2)];
      break;
    }
    case 'forest': {
      const tm = o.time || 'dusk';
      const sky = tm === 'dawn' ? [[0, '#283047'], [0.55, '#8d6572'], [1, '#e6a16d']] :
        tm === 'night' ? [[0, '#080f1a'], [0.65, '#162736'], [1, '#27353a']] :
        [[0, '#14272c'], [0.62, '#38534d'], [1, '#bd8668']];
      vgrad(g, sky, 0, gy);
      if (tm === 'night') moon(g, X(0.78), Y(0.18), E.H * 0.025);
      else light(g, X(0.68), Y(0.39), E.H * 0.38, '#e5b27b', 0.18);
      // Distant trunks, then layered foreground trees; the open center is a motivated stage.
      for (let layer = 0; layer < 3; layer++) {
        const count = 13 - layer * 2, spread = E.W / count;
        for (let i = 0; i < count; i++) {
          const x = i * spread - spread * 0.12 + ((i * 37 + layer * 19) % 17);
          const baseY = gy + layer * 10, trunkW = 8 + layer * 5, treeH = E.H * (0.28 + ((i * 5 + layer * 3) % 6) * 0.045);
          if (layer === 2 && x > E.W * 0.28 && x < E.W * 0.72) continue;
          box(g, x, baseY - treeH, trunkW, treeH, { fill: layer === 0 ? '#243b38' : layer === 1 ? '#172d2b' : '#101e20', line: '#71806d', r: 3, lw: 1.5, la: layer === 2 ? 0.45 : 0.3 });
          for (let b = 0; b < 4; b++) {
            const cy = baseY - treeH + b * treeH * 0.18;
            oval(g, x + trunkW / 2 + Math.sin(i * 4 + b) * E.W * 0.012, cy, treeH * (0.12 + layer * 0.025), treeH * 0.14, { fill: layer === 0 ? '#39564b' : layer === 1 ? '#223f3a' : '#162b2b', line: null, a: 0.68 });
          }
        }
      }
      // Mist ribbons and sparse fireflies.
      for (let i = 0; i < 4; i++) oval(g, X(0.15 + i * 0.23), Y(0.56 + i * 0.035), E.W * 0.13, E.H * 0.022, { fill: '#c6d3be', line: null, a: 0.055 });
      for (let i = 0; i < 12; i++) {
        const x = X(0.08 + ((i * 37) % 83) / 100), y = Y(0.32 + ((i * 19) % 45) / 100) + Math.sin(t * 1.7 + i) * 5;
        oval(g, x, y, 2.5, 2.5, { fill: '#f4d68a', line: null, a: 0.7 });
        light(g, x, y, 16, '#f4d68a', 0.18);
      }
      floor(g, gy, '#18231f');
      for (let i = 0; i < 24; i++) {
        const x = X(i / 23);
        ln(g, [[x, gy], [x + (i % 2 ? 26 : -18), gy - E.H * (0.03 + (i % 4) * 0.006)]], { color: '#57705a', lw: 2, la: 0.4 });
      }
      M.clearing = [X(0.5), gy]; M.gy = gy;
      break;
    }
    case 'beach': {
      const tm = o.time || 'dawn';
      const sky = tm === 'day' ? [[0, '#5f9bc1'], [0.62, '#a5d3d7'], [1, '#f2d8b1']] :
        tm === 'sunset' ? [[0, '#292a52'], [0.48, '#b35f76'], [1, '#f4a16e']] :
        [[0, '#172a45'], [0.52, '#6d718b'], [1, '#f4b48a']];
      vgrad(g, sky, 0, Y(0.64));
      const sunX = X(o.sunX ?? 0.73), sunY = Y(tm === 'day' ? 0.24 : 0.42);
      light(g, sunX, sunY, E.H * 0.3, '#ffd39a', 0.28);
      oval(g, sunX, sunY, E.H * 0.052, E.H * 0.052, { fill: '#ffe0a9', line: null, a: 0.92 });
      // Bands of water change hue and scale toward the horizon.
      vgrad(g, [[0, '#526e86'], [0.38, '#36566d'], [1, '#182f40']], Y(0.64), gy);
      for (let i = 0; i < 22; i++) {
        const y = Y(0.66 + i * 0.013);
        const x = X(((i * 29) % 91) / 100);
        ln(g, [[x, y], [Math.min(E.W, x + X(0.05 + (i % 5) * 0.018)), y + Math.sin(t * 1.6 + i) * 2]], { color: i % 4 ? '#c2ccd0' : '#f8dfb7', lw: i < 7 ? 2 : 3, la: 0.16 + (i % 4) * 0.035 });
      }
      floor(g, gy, '#342e31');
      // Broken foam edge, scattered stones and a few grasses.
      for (let i = 0; i < 14; i++) {
        const x = X(i / 13), y = gy - E.H * (0.02 + (i % 3) * 0.012);
        ln(g, [[x - 15, y], [x + 22, y + Math.sin(i * 3) * 6], [x + 58, y - 4]], { color: '#e3d5c3', lw: 3, la: 0.24 });
      }
      for (let i = 0; i < 7; i++) oval(g, X(0.07 + i * 0.14), gy + E.H * 0.03 + (i % 3) * 8, 8 + i * 1.4, 4 + i * 0.7, { fill: '#6c5b53', line: '#aa9783', lw: 1, a: 0.75 });
      for (let i = 0; i < 8; i++) {
        const x = X(0.05 + i * 0.12);
        ln(g, [[x, gy + 20], [x - 8, gy - 18 - (i % 3) * 6]], { color: '#657552', lw: 3, la: 0.72 });
      }
      M.shore = [X(0.5), gy]; M.horizon = [X(0.5), Y(0.64)];
      break;
    }
    case 'parking': {
      wall(g, '#1a1c21', '#282b30');
      const vx = X(0.5), vy = Y(0.22);
      // Concrete garage, fluorescent ceiling bars and lane markings.
      obj(g, (c) => { c.moveTo(0, 0); c.lineTo(E.W, 0); c.lineTo(X(0.78), Y(0.32)); c.lineTo(X(0.22), Y(0.32)); c.closePath(); }, { fill: '#343941', line: '#757b84', lw: 3, la: 0.6 });
      obj(g, (c) => { c.moveTo(0, gy); c.lineTo(X(0.22), Y(0.32)); c.lineTo(X(0.78), Y(0.32)); c.lineTo(E.W, gy); c.closePath(); }, { fill: '#353940', line: '#7c8189', lw: 3, la: 0.5 });
      for (let i = 0; i < 5; i++) {
        const x = X(i / 4);
        ln(g, [[x, Y(0.02)], [vx + (x - vx) * 0.28, Y(0.3)]], { color: '#8a9097', lw: 4, la: 0.25 });
        box(g, vx + (x - vx) * 0.48 - 30, Y(0.12 + Math.abs(i - 2) * 0.018), 60, 12, { fill: '#e1dfd7', line: null, r: 4, la: 0.7 });
      }
      for (const x of [0.06, 0.2, 0.8, 0.94]) {
        box(g, X(x) - E.W * 0.025, Y(0.32), E.W * 0.05, gy - Y(0.32), { fill: '#4b4f55', line: '#8b9096', r: 4, lw: 2, la: 0.9 });
        ln(g, [[X(x) - E.W * 0.025, Y(0.42)], [X(x) + E.W * 0.025, Y(0.42)]], { color: '#b3a06c', lw: 3, la: 0.7 });
      }
      floor(g, gy, '#22252a');
      for (let i = 0; i < 6; i++) {
        const x = X(0.18 + i * 0.13);
        ln(g, [[x, gy - 4], [vx + (x - vx) * 0.15, Y(0.32)]], { color: '#d3c48c', lw: 3, la: 0.4 });
      }
      // Far-car silhouettes are background dressing; keep the protagonist lane open.
      for (const [x, scale] of [[0.13, 0.62], [0.79, 0.72]]) {
        const y = gy - E.H * 0.11 * scale, w = E.W * 0.14 * scale, h = E.H * 0.07 * scale;
        box(g, X(x), y, w, h, { fill: '#313944', line: '#8a929c', r: 10, lw: 2, la: 0.9 });
        oval(g, X(x) + w * 0.2, y + h, w * 0.12, h * 0.22, { fill: '#101216', line: '#858b94', lw: 2 });
        oval(g, X(x) + w * 0.78, y + h, w * 0.12, h * 0.22, { fill: '#101216', line: '#858b94', lw: 2 });
      }
      light(g, X(0.51), Y(0.37), E.H * 0.42, '#ecd5a2', 0.08);
      M.vanish = [vx, vy]; M.lane = [X(0.5), gy];
      break;
    }
    case 'workshop': {
      wall(g, '#25211f', '#322a26');
      windowBox(g, X(0.07), Y(0.1), X(0.19), Y(0.24), { sky: o.sky || 'dawn', t });
      // Pegboard with individually silhouetted tools.
      box(g, X(0.56), Y(0.1), X(0.36), Y(0.29), { fill: '#55443a', line: '#967b65', r: 5, lw: 3 });
      for (let i = 0; i < 5; i++) {
        const x = X(0.61 + i * 0.063), y = Y(0.17 + (i % 2) * 0.1);
        ln(g, [[x, y], [x, y + E.H * 0.07], [x - 13, y + E.H * 0.09]], { color: '#c5b8a4', lw: 5, la: 0.82 });
        oval(g, x, y - 5, 7, 10, { fill: null, line: '#c5b8a4', lw: 3, la: 0.82 });
      }
      // Wall shelves, bolts, jars and a heavy timber bench.
      for (let i = 0; i < 3; i++) {
        box(g, X(0.06), Y(0.42 + i * 0.07), X(0.25), 12, { fill: '#765744', line: '#b28c6d', r: 2, lw: 2 });
        for (let j = 0; j < 5; j++) box(g, X(0.08 + j * 0.043), Y(0.38 + i * 0.07), X(0.027), Y(0.04), { fill: ['#8f8e82', '#b68b57', '#657887', '#9b735d'][j % 4], line: '#463c38', r: 3, lw: 1 });
      }
      floor(g, gy, '#211d1b');
      table(g, X(0.5), gy, X(0.72), E.H * 0.24, { fill: '#73513b' });
      box(g, X(0.32), gy - E.H * 0.255, X(0.16), E.H * 0.035, { fill: '#9c8066', line: '#4d3a2e', r: 4 });
      for (let i = 0; i < 4; i++) oval(g, X(0.65 + i * 0.025), gy - E.H * 0.255, 4, 4, { fill: '#d4bc8b', line: null, a: 0.9 });
      deskLamp(g, X(0.78), gy - E.H * 0.24, E.H * 0.12, true);
      light(g, X(0.78), gy - E.H * 0.24, E.H * 0.3, '#ffc77f', 0.23);
      M.table = { left: [X(0.14), gy], right: [X(0.86), gy], top: [X(0.5), gy - E.H * 0.24] };
      break;
    }
    case 'museum': {
      wall(g, '#242127', '#353039');
      // Quiet gallery wall, track lights, and framed works with generous negative space.
      box(g, 0, Y(0.13), E.W, Y(0.5), { fill: '#2d2931', line: '#645965', r: 0, lw: 3, la: 0.72 });
      ln(g, [[0, Y(0.13)], [E.W, Y(0.13)]], { color: '#aca0ad', lw: 5, la: 0.52 });
      for (let i = 0; i < 5; i++) {
        const x = X(0.1 + i * 0.2), y = Y(0.21 + (i % 2) * 0.03), w = X(0.12 + (i % 3) * 0.025), h = Y(0.23 + (i % 2) * 0.04);
        box(g, x, y, w, h, { fill: '#4f454e', line: '#bba889', r: 2, lw: 5, la: 0.95 });
        box(g, x + 10, y + 10, w - 20, h - 20, { fill: ['#596778', '#8c6c56', '#6e7160', '#9b826f', '#464e60'][i], line: null, r: 0, la: 0.9 });
        // Abstract shapes in the picture so each frame differs from a blank card.
        oval(g, x + w * 0.45, y + h * 0.44, w * 0.2, h * 0.19, { fill: '#d4b68a', line: null, a: 0.7 });
        ln(g, [[x + w * 0.12, y + h * 0.76], [x + w * 0.48, y + h * 0.5], [x + w * 0.88, y + h * 0.82]], { color: '#d7c7ad', lw: 4, la: 0.63 });
        ln(g, [[x + w * 0.05, Y(0.11)], [x + w * 0.5, y + 1]], { color: '#c9d8ec', lw: 3, la: 0.28 });
        light(g, x + w / 2, y, E.H * 0.2, '#ffe1ad', 0.15);
      }
      floor(g, gy, '#29252d');
      // Pedestals break the flat-wall composition and create foreground depth.
      for (const [x, w, h] of [[0.25, 0.11, 0.13], [0.63, 0.14, 0.17]]) {
        box(g, X(x), gy - E.H * h, X(w), E.H * h, { fill: '#78717b', line: '#bab0ba', r: 3, lw: 2, la: 0.88 });
        oval(g, X(x + w / 2), gy - E.H * h - 13, X(w * 0.22), E.H * 0.035, { fill: '#bda58a', line: '#d6c8b4', lw: 2 });
      }
      for (let i = 0; i < 9; i++) ln(g, [[X(i / 8), gy], [X(0.5 + (i / 8 - 0.5) * 0.18), Y(0.62)]], { color: '#827984', lw: 2, la: 0.17 });
      M.gallery = [X(0.5), gy]; M.pedestal = [X(0.68), gy - E.H * 0.16];
      break;
    }
    default: wall(g); floor(g, gy);
  }
  if (o.dim) { g.save(); g.fillStyle = `rgba(0,0,0,${o.dim})`; g.fillRect(-60, -60, E.W + 120, E.H + 120); g.restore(); }
  return M;
}
export const SETS = ['bedroom', 'city', 'street', 'lockers', 'classroom', 'court', 'cafe', 'gym', 'stairs', 'hill', 'mirror', 'kitchen', 'void', 'black', 'doorway', 'metro', 'rooftop', 'underpass', 'hospital', 'library', 'warehouse', 'laboratory', 'forest', 'beach', 'parking', 'workshop', 'museum'];
