// three3d.js — canh 3D (Three.js) cung phong cach: nguoi que den vien sang, nha cua so sang den, suong mu, mau theo mood.
// Dung trong shot: registerShot('s010', { kind: '3d', init(T, info) {...; return { stage }}, draw(s, t, info, T) {...}, overlay(g, t, info, s) {...} })
// Don vi: met. Nguoi que cao ~1.75 m, nhin ve huong +x.
import * as THREE from 'three';
import { E, mood, hex, rng, lerp, clamp, ease, UI } from './core.js';

let R = null;              // WebGLRenderer dung chung
const shadowPrepared = new WeakSet();
export function renderer(w, h) {
  if (!R) {
    const c = document.createElement('canvas');
    R = new THREE.WebGLRenderer({ canvas: c, antialias: true, preserveDrawingBuffer: true, alpha: false, powerPreference: 'high-performance' });
    R.outputColorSpace = THREE.SRGBColorSpace;
    R.toneMapping = THREE.ACESFilmicToneMapping;
    R.toneMappingExposure = 1.12;
    R.shadowMap.enabled = true;
    R.shadowMap.type = THREE.PCFSoftShadowMap;
    R.setPixelRatio(1);
  }
  if (R.domElement.width !== w || R.domElement.height !== h) R.setSize(w, h, false);
  return R;
}
const col = (c) => new THREE.Color(...hex(c).map((v) => v / 255)).convertSRGBToLinear();
const lam = (c, o = {}) => {
  const { roughness = 0.82, metalness = 0.025, emissiveIntensity = 0.055, ...extra } = o;
  return new THREE.MeshStandardMaterial({
    color: col(c), emissive: col(c).multiplyScalar(emissiveIntensity),
    roughness, metalness, flatShading: false, ...extra,
  });
};
const basic = (c, o = {}) => new THREE.MeshBasicMaterial({ color: col(c), ...o });

function gradTex(stops) {
  const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 256); stops.forEach((s, i) => gr.addColorStop(i / (stops.length - 1), s)); g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
let _glowTex = null;
function glowTex() {
  if (_glowTex) return _glowTex;
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,255,.45)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); _glowTex = new THREE.CanvasTexture(c); return _glowTex;
}

// ---------- san khau
export function stage(o = {}) {
  const M = mood(o.mood || 'dusk');
  const cinematic = !!o.cinematic;
  const scene = new THREE.Scene();
  scene.background = gradTex(M.sky);
  const fogC = col(o.fogColor || M.fog);
  scene.fog = new THREE.Fog(fogC, (o.fog || [18, 90])[0], (o.fog || [18, 90])[1]);
  const camera = new THREE.PerspectiveCamera(o.fov || 38, E.W / E.H, 0.1, 600);
  scene.add(new THREE.HemisphereLight(col(M.sky[2]), col(M.floor), o.ambient ?? (cinematic ? 0.88 : 1.6)));
  const key = new THREE.DirectionalLight(col(M.key), o.keyIntensity ?? (cinematic ? 3.25 : 2.6));
  key.position.set(...(o.keyPos || [-20, 14, -30]));
  if (cinematic) {
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    key.shadow.camera.left = -30; key.shadow.camera.right = 30;
    key.shadow.camera.top = 25; key.shadow.camera.bottom = -25;
    key.shadow.camera.near = 0.5; key.shadow.camera.far = 110;
    key.shadow.camera.updateProjectionMatrix();
    key.shadow.bias = -0.00028; key.shadow.normalBias = 0.035;
    key.shadow.radius = 4;
  }
  scene.add(key);
  const fill = new THREE.DirectionalLight(col(M.sky[1]), cinematic ? 0.52 : 0.8);
  fill.position.set(15, 10, 20); scene.add(fill);
  const rim = new THREE.DirectionalLight(col(M.rim), cinematic ? (o.rimIntensity ?? 1.45) : 0.45);
  rim.position.set(10, 8, -14); scene.add(rim);
  const bounce = new THREE.PointLight(col(M.practical), cinematic ? (o.practicalIntensity ?? 0.8) : 0.25, 26, 2);
  bounce.position.set(-1, 3.2, 2.4); scene.add(bounce);
  const st = { scene, camera, M, key, cinematic, add: (...objs) => { objs.forEach((x) => scene.add(x)); return objs[0]; } };
  if (o.sun !== false) { const sun = sprite(M.sun, o.sunSize || 26, 0.9); sun.position.set(...(o.sunPos || [-60, 8, -140])); scene.add(sun); }
  return st;
}
function prepareCinematicShadows(st) {
  if (!st?.cinematic || shadowPrepared.has(st.scene)) return;
  st.scene.traverse((obj) => {
    if (!obj.isMesh) return;
    const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
    const translucent = materials.some((m) => !m || m.transparent || (m.opacity ?? 1) < 0.88 || m.depthWrite === false);
    obj.castShadow = !translucent;
    obj.receiveShadow = !translucent;
  });
  shadowPrepared.add(st.scene);
}
export function render(st, w, h) {
  const r = renderer(w, h);
  st.camera.aspect = E.W / E.H;
  st.camera.updateProjectionMatrix();
  prepareCinematicShadows(st);
  r.render(st.scene, st.camera);
  return r.domElement;
}
export function dispose(st) { st.scene.traverse((o) => { o.geometry?.dispose?.(); if (o.material) [].concat(o.material).forEach((m) => { m.map?.dispose?.(); m.dispose?.(); }); }); }

// ---------- hinh khoi co ban
export const box = (w, h, d, c, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), o.basic ? basic(c, o.mat) : lam(c, o.mat)); m.position.set(o.x || 0, (o.y ?? h / 2), o.z || 0); return m; };
export const cyl = (rt, rb, h, c, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, o.seg || 12), lam(c, o.mat)); m.position.set(o.x || 0, (o.y ?? h / 2), o.z || 0); return m; };
export const sphere = (r, c, o = {}) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, o.seg || 16, o.seg || 12), o.basic ? basic(c) : lam(c)); m.position.set(o.x || 0, o.y || 0, o.z || 0); return m; };
export function ground(w, d, c, o = {}) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), lam(c)); m.rotation.x = -Math.PI / 2; m.position.y = o.y || 0; m.receiveShadow = true;
  if (o.lines) { const g = new THREE.Group(); g.add(m); for (let x = -w / 2; x <= w / 2; x += o.lines) { const l = box(0.08, 0.01, d, o.lineColor || '#c8b890', { y: (o.y || 0) + 0.01, x, basic: true, mat: { transparent: true, opacity: 0.35 } }); g.add(l); } return g; }
  return m;
}
// quang sang (sprite cong sang)
export function sprite(c, size, opacity = 0.8) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: col(c), transparent: true, opacity, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
  s.scale.set(size, size, 1); return s;
}
// mat phang tu phat sang (cua so, man hinh)
export function pane(w, h, c, o = {}) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), basic(c, { transparent: o.opacity !== undefined, opacity: o.opacity ?? 1 })); m.position.set(o.x || 0, o.y || 0, o.z || 0); if (o.ry) m.rotation.y = o.ry; return m; }

// toa nha co luoi cua so sang den (texture ve bang canvas)
export function building(w, h, d, o = {}) {
  const M = mood(o.mood || 'dusk'), color = o.color || M.wall, lit = o.lit || M.practical, r = rng(o.seed || 1);
  const cols = o.cols || Math.max(2, Math.round(w / 2.4)), rows = o.rows || Math.max(2, Math.round(h / 3));
  const c = document.createElement('canvas'); c.width = 256; c.height = Math.round(256 * h / w); const g = c.getContext('2d');
  g.fillStyle = color; g.fillRect(0, 0, c.width, c.height);
  const cw = c.width / cols, rh = c.height / rows;
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) { const on = r() < (o.litChance ?? 0.45); g.fillStyle = on ? lit : '#0d0a12'; g.globalAlpha = on ? 0.75 + r() * 0.25 : 0.7; g.fillRect(i * cw + cw * 0.22, j * rh + rh * 0.25, cw * 0.56, rh * 0.5); }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const side = new THREE.MeshStandardMaterial({ map: tex, emissive: col('#ffffff'), emissiveMap: tex, emissiveIntensity: 0.42, roughness: 0.9 });
  const plain = lam(color);
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), [side, side, plain, plain, side, side]);
  m.position.set(o.x || 0, h / 2, o.z || 0); if (o.ry) m.rotation.y = o.ry; return m;
}
export function lamp(o = {}) {
  const M = mood(o.mood || 'dusk'), c = o.color || M.practical, g = new THREE.Group();
  g.add(cyl(0.06, 0.08, 4.2, M.dark)); const arm = box(0.9, 0.08, 0.08, M.dark, { y: 4.15, x: 0.4 }); g.add(arm);
  const bulb = sphere(0.14, c, { x: 0.8, y: 4.05, basic: true }); g.add(bulb);
  const s = sprite(c, 3.2, 0.9); s.position.set(0.8, 4.0, 0); g.add(s);
  const pl = new THREE.PointLight(col(c), o.intensity ?? 8, 12, 1.6); pl.position.set(0.8, 3.9, 0); g.add(pl);
  const pool = new THREE.Mesh(new THREE.CircleGeometry(2.6, 32), new THREE.MeshBasicMaterial({ map: glowTex(), color: col(c), transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false }));
  pool.rotation.x = -Math.PI / 2; pool.position.set(0.8, 0.02, 0); g.add(pool);
  g.position.set(o.x || 0, 0, o.z || 0); return g;
}
export function tree(o = {}) { const M = mood(o.mood || 'dusk'), g = new THREE.Group(), s = o.s || 1; g.add(cyl(0.12 * s, 0.16 * s, 2 * s, M.dark)); [[0, 2.6, 0, 1.1], [-0.6, 2.2, 0.2, 0.8], [0.6, 2.25, -0.2, 0.85]].forEach(([x, y, z, r]) => g.add(sphere(r * s, shade3(M.dark, 0.05), { x: x * s, y: y * s, z: z * s, seg: 8 }))); g.position.set(o.x || 0, 0, o.z || 0); return g; }
const shade3 = (c, k) => { const v = hex(c).map((x) => clamp(x + k * 255, 0, 255)); return `rgb(${v.join(',')})`; };
export function car(o = {}) {
  const c = o.color || '#1a1418', g = new THREE.Group();
  g.add(box(4, 0.7, 1.8, c, { y: 0.65 })); g.add(box(2.2, 0.65, 1.6, c, { y: 1.3, x: -0.2 }));
  [[-1.3, 0.85], [1.3, 0.85], [-1.3, -0.85], [1.3, -0.85]].forEach(([x, z]) => { const w = cyl(0.35, 0.35, 0.3, '#0a080c', { y: 0.35, x, z }); w.rotation.x = Math.PI / 2; g.add(w); });
  if (o.lights !== false) { [-0.6, 0.6].forEach((z) => { const s = sprite('#ffe9b0', 1.4, 0.8); s.position.set(2.05, 0.75, z); g.add(s); const r = sprite('#ff4040', 0.8, 0.7); r.position.set(-2.05, 0.75, z); g.add(r); }); }
  g.position.set(o.x || 0, 0, o.z || 0); g.rotation.y = o.ry || 0; return g;
}
export function stars(count = 400, o = {}) {
  const r = rng(o.seed || 3), pos = []; for (let i = 0; i < count; i++) { const a = r() * Math.PI * 2, el = 0.15 + r() * 1.2, d = 300; pos.push(Math.cos(a) * Math.cos(el) * d, Math.sin(el) * d, Math.sin(a) * Math.cos(el) * d); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.4, sizeAttenuation: false, fog: false, transparent: true, opacity: 0.8 }));
}
// khan dai dam dong (instanced)
export function crowd(o = {}) {
  const { rows = 6, perRow = 40, width = 40, step = 1.2, rise = 0.8, z0 = 0, color = '#15101a', seed = 4 } = o, r = rng(seed);
  const n = rows * perRow, head = new THREE.InstancedMesh(new THREE.SphereGeometry(0.22, 8, 6), lam(color), n), body = new THREE.InstancedMesh(new THREE.BoxGeometry(0.5, 0.7, 0.35), lam(color), n);
  const m = new THREE.Matrix4(); let k = 0;
  for (let j = 0; j < rows; j++) for (let i = 0; i < perRow; i++) { const x = -width / 2 + (i + r() * 0.5) * (width / perRow), y = j * rise, z = z0 + j * step; m.makeTranslation(x, y + 1.25, z); head.setMatrixAt(k, m); m.makeTranslation(x, y + 0.75, z); body.setMatrixAt(k, m); k++; }
  const g = new THREE.Group(); g.add(head, body); return g;
}

// ---------- nguoi que 3D
const PO = {
  stand: { lA: [0.05, -0.05], rA: [-0.05, 0.05], lL: [0, 0.03], rL: [0, -0.03] },
  wave: { lA: [0.05, -0.05], rA: [2.6, 0.2], lL: [0, 0.03], rL: [0, -0.03] },
  cheer: { lA: [2.8, -0.3], rA: [2.8, 0.3], lL: [0, 0.05], rL: [0, -0.05] },
  point: { lA: [0.05, -0.05], rA: [1.5, 0.1], lL: [0, 0.03], rL: [0, -0.03] },
  reach: { lA: [0.02, -0.1], rA: [1.62, 0.2], lL: [0.02, 0.03], rL: [-0.02, -0.03] },
  pull: { lA: [1.05, -0.28], rA: [1.18, 0.28], lL: [-0.16, 0.08], rL: [0.10, -0.08] },
  carry: { lA: [1.18, -0.28], rA: [1.18, 0.28], lL: [0, 0.03], rL: [0, -0.03] },
  hug: { lA: [1.48, -0.8], rA: [1.48, 0.8], lL: [0.02, 0.04], rL: [-0.02, -0.04] },
  shield: { lA: [1.9, -0.42], rA: [1.9, 0.42], lL: [-0.48, 0.12], rL: [-0.38, -0.12] },
  crouch: { lA: [0.72, -0.32], rA: [0.72, 0.32], lL: [-0.62, 0.1], rL: [-0.55, -0.1] },
  kneel: { lA: [0.48, -0.22], rA: [0.48, 0.22], lL: [-1.1, 0.05], rL: [0.16, -0.05] },
  sit: { lA: [0.15, -0.12], rA: [0.15, 0.12], lL: [-1.08, 0.05], rL: [-1.08, -0.05] },
  bike: { lA: [1.16, -0.12], rA: [1.16, 0.12], lL: [-0.45, 0.15], rL: [0.42, -0.15] },
};
// arms/legs: [goc nang ra truoc (rad), goc dang ngang]
export function figure(outfit = {}, o = {}) {
  const M = mood(o.mood || 'dusk'), ink = UI.ink, s = (o.s || 1) * (outfit.kid ? 0.72 : 1), grp = new THREE.Group();
  const rimC = o.rim || M.rim, parts = [];
  const limb = (len, r, c) => { const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, len, 4, 8), lam(c)); m.geometry.translate(0, -len / 2, 0); return m; };
  const torsoC = outfit.top && outfit.top !== 'none' ? (outfit.top === 'labcoat' ? '#ece8e0' : outfit.color || '#d64a33') : ink;
  const hip = new THREE.Group(); hip.position.y = 0.9; grp.add(hip);
  const torso = limb(0.5, outfit.top && outfit.top !== 'none' ? 0.15 : 0.07, torsoC); torso.rotation.z = Math.PI; torso.position.y = 0.0; hip.add(torso); parts.push(torso);
  const skinC = outfit.skin || '#dfb29a';
  const skinM = lam(skinC);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 24, 18), skinM);
  head.scale.set(1.0, 1.08, 0.94); head.position.y = 0.82; hip.add(head); parts.push(head);
  // Small ears, pupils and a nose make the side-facing expression readable.
  for (const side of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.043, 10, 8), skinM);
    ear.position.set(0.005, 0.82, side * 0.19); hip.add(ear);
  }
  const eyeM = basic('#fff9ef'), pupilM = basic('#1a1d27');
  [-0.07, 0.07].forEach((z) => {
    const e = new THREE.Mesh(new THREE.SphereGeometry(0.034, 10, 8), eyeM);
    e.scale.set(0.52, 1.28, 1); e.position.set(0.176, 0.86, z); hip.add(e);
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.014, 8, 6), pupilM);
    pupil.position.set(0.199, 0.86, z); hip.add(pupil);
  });
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.027, 8, 6), skinM);
  nose.scale.set(1.3, 0.75, 0.9); nose.position.set(0.205, 0.805, 0); hip.add(nose);
  const mouth = new THREE.Mesh(new THREE.TorusGeometry(0.043, 0.009, 6, 12, Math.PI), basic('#693c3d'));
  mouth.position.set(0.187, 0.755, 0); mouth.rotation.set(0, Math.PI / 2, Math.PI); hip.add(mouth);
  if (outfit.head === 'cap' || outfit.head === 'beanie') { const hc = outfit.headColor || outfit.color; const cap = new THREE.Mesh(new THREE.SphereGeometry(0.205, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2.2), lam(hc)); cap.position.y = 0.86; hip.add(cap); if (outfit.head === 'cap') { const b = box(0.2, 0.02, 0.22, hc, { y: 0.9, x: 0.2 }); hip.add(b); } }
  const arm = (side) => {
    const sh = new THREE.Group(); sh.position.set(0, 0.55, side * 0.2);
    const sleeve = outfit.top === 'hoodie' || outfit.top === 'labcoat' || outfit.top === 'tracksuit';
    const sleeveColor = sleeve ? torsoC : ink, radius = sleeve ? 0.075 : 0.05;
    const upper = limb(0.30, radius, sleeveColor); sh.add(upper); parts.push(upper);
    // Separate elbow pivot and forearm add articulated reaching and hugging.
    const elbow = new THREE.Group(); elbow.position.y = -0.29; sh.add(elbow);
    const forearm = limb(0.30, radius * 0.92, sleeveColor); elbow.add(forearm); parts.push(forearm);
    const hand = new THREE.Mesh(new THREE.SphereGeometry(radius * 1.18, 10, 8), lam(skinC));
    hand.position.y = -0.31; elbow.add(hand); parts.push(hand);
    sh.userData.elbow = elbow; hip.add(sh); return sh;
  };
  const leg = (side) => {
    const h = new THREE.Group(); h.position.set(0, 0, side * 0.08);
    const upper = limb(0.36, 0.06, outfit.legs || ink); h.add(upper); parts.push(upper);
    const knee = new THREE.Group(); knee.position.y = -0.35; h.add(knee);
    const lower = limb(0.43, 0.057, outfit.legs || ink); knee.add(lower); parts.push(lower);
    const shoe = new THREE.Mesh(new THREE.SphereGeometry(0.082, 10, 8), lam(outfit.legs || ink));
    shoe.scale.set(1.35, 0.56, 0.85); shoe.position.set(0.025, -0.43, 0); knee.add(shoe);
    h.userData.knee = knee; hip.add(h); return h;
  };
  const L = { lA: arm(-1), rA: arm(1), lL: leg(-1), rL: leg(1) };
  // vien sang: ban sao phong to mat sau, mau rim
  const rimMat = new THREE.MeshBasicMaterial({ color: col(rimC), side: THREE.BackSide, transparent: true, opacity: o.rimOpacity ?? 0.9 });
  parts.forEach((p) => { const h = new THREE.Mesh(p.geometry, rimMat); h.scale.setScalar(1.12); p.add(h); });
  const setPose = (name, t = 0) => {
    let P = PO[name] || PO.stand;
    hip.position.y = name === 'crouch' || name === 'shield' ? 0.76
      : name === 'kneel' ? 0.70
      : name === 'sit' ? 0.66 : 0.9;
    if (name === 'walk' || name === 'run') { const k = name === 'run' ? 1 : 0.5, ph = t * Math.PI * 2 * (name === 'run' ? 1.5 : 0.9), sw = Math.sin(ph) * k; P = { lA: [-sw, -0.05], rA: [sw, 0.05], lL: [sw, 0.03], rL: [-sw, -0.03] }; hip.position.y = 0.9 + Math.abs(Math.cos(ph)) * 0.04 * k; }
    for (const k of Object.keys(L)) {
      L[k].rotation.z = P[k][0];
      L[k].rotation.x = P[k][1] + (k === 'lA' ? 0.18 : k === 'rA' ? -0.18 : 0);
    }
    const elbowBend = name === 'carry' ? { lA: -0.34, rA: 0.34 }
      : name === 'hug' ? { lA: -0.72, rA: 0.72 }
      : name === 'pull' ? { lA: -0.22, rA: 0.28 }
      : name === 'shield' ? { lA: 0.48, rA: -0.48 }
      : name === 'crouch' ? { lA: 0.2, rA: -0.2 }
      : name === 'reach' ? { lA: -0.08, rA: -0.08 }
      : name === 'bike' ? { lA: -0.14, rA: -0.14 }
      : { lA: 0, rA: 0 };
    L.lA.userData.elbow.rotation.z = elbowBend.lA;
    L.rA.userData.elbow.rotation.z = elbowBend.rA;
    const kneeBend = name === 'crouch' || name === 'shield' ? { lL: 1.08, rL: 1.08 }
      : name === 'kneel' ? { lL: 1.32, rL: 0.14 }
      : name === 'sit' ? { lL: 1.28, rL: 1.28 }
      : name === 'run' ? { lL: 0.28 + Math.max(0, Math.sin(t * Math.PI * 3)) * 0.72, rL: 0.28 + Math.max(0, Math.sin(t * Math.PI * 3 + Math.PI)) * 0.72 }
      : name === 'walk' ? { lL: 0.18 + Math.max(0, Math.sin(t * Math.PI * 1.8)) * 0.42, rL: 0.18 + Math.max(0, Math.sin(t * Math.PI * 1.8 + Math.PI)) * 0.42 }
      : { lL: 0.04, rL: 0.04 };
    L.lL.userData.knee.rotation.z = kneeBend.lL;
    L.rL.userData.knee.rotation.z = kneeBend.rL;
    if (name === 'hug') {
      hip.rotation.y = Math.sin(t * 1.7) * 0.035;
      L.lA.userData.elbow.rotation.z += Math.sin(t * 1.6) * 0.05;
      L.rA.userData.elbow.rotation.z -= Math.sin(t * 1.6) * 0.05;
    } else if (name === 'pull' || name === 'shield') {
      hip.rotation.y = Math.sin(t * 2.2) * 0.025;
    } else hip.rotation.y = 0;
  };
  setPose(o.pose || 'stand');
  grp.scale.setScalar(s); grp.position.set(o.x || 0, 0, o.z || 0); grp.rotation.y = o.ry || 0;
  grp.userData.setPose = setPose;
  // bong tiep dat
  const sh = new THREE.Mesh(new THREE.CircleGeometry(0.45, 20), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.35, depthWrite: false })); sh.rotation.x = -Math.PI / 2; sh.position.y = 0.01; grp.add(sh);
  return grp;
}


// ---------- cinematic character rig (rounded proportions, articulated clothing and expressive motion)
// Kept additive so older projects may continue using the original compact stick-figure rig.
export function figureCinematic(outfit = {}, o = {}) {
  const M = mood(o.mood || 'dusk');
  const scale = (o.s || 1) * (outfit.kid ? 0.78 : 1);
  const skinColor = outfit.skin || '#e5c5ad';
  const shirtColor = outfit.color || '#3c7186';
  const pantsColor = outfit.legs || '#202938';
  const faceInk = '#362b31';
  const grp = new THREE.Group();
  const rig = new THREE.Group();
  rig.position.y = 0.93;
  grp.add(rig);

  const solid = (color, extra = {}) => lam(color, extra);
  const capsule = (radius, length, color, segments = 12) =>
    new THREE.Mesh(new THREE.CapsuleGeometry(radius, length, 6, segments), solid(color));
  const addRoundDetail = (parent, radius, color, pos, seg = 12) => {
    const m = new THREE.Mesh(new THREE.SphereGeometry(radius, seg, Math.max(8, seg - 2)), solid(color));
    m.position.set(...pos); parent.add(m); return m;
  };

  const topType = outfit.top || 'hoodie';
  const torsoColor = topType === 'labcoat' ? '#ece8e0' : shirtColor;
  const upperBody = new THREE.Group();
  rig.add(upperBody);

  const torso = capsule(0.18, 0.55, torsoColor, 16);
  torso.position.set(0, 0.22, 0);
  upperBody.add(torso);

  const pelvis = capsule(0.135, 0.19, pantsColor, 12);
  pelvis.position.set(0, -0.18, 0);
  upperBody.add(pelvis);

  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.067, 0.078, 0.17, 14), solid(skinColor));
  neck.position.set(0, 0.66, 0); upperBody.add(neck);

  const headGroup = new THREE.Group();
  headGroup.position.set(0, 0.80, 0);
  upperBody.add(headGroup);
  const headRadius = 0.162;
  const head = new THREE.Mesh(new THREE.SphereGeometry(headRadius, 24, 18), solid(skinColor));
  head.scale.set(1.0, 1.08, 0.96); headGroup.add(head);

  for (const side of [-1, 1]) {
    const ear = addRoundDetail(headGroup, 0.035, skinColor, [0, 0, side * 0.151], 12);
    ear.scale.set(0.82, 1.08, 0.78);
  }

  const eyeWhite = basic('#fff8ec');
  const pupilMat = basic('#171c25');
  const eyeMeshes = [];
  const browMeshes = [];
  for (const side of [-1, 1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.027, 12, 10), eyeWhite);
    eye.scale.set(0.62, 1.10, 0.9);
    eye.position.set(0.139, 0.025, side * 0.052);
    headGroup.add(eye); eyeMeshes.push(eye);

    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.012, 10, 8), pupilMat);
    pupil.position.set(0.161, 0.022, side * 0.052);
    headGroup.add(pupil);

    const brow = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.012, 0.055), solid(outfit.hairColor || '#30262c'));
    brow.position.set(0.137, 0.071, side * 0.052);
    brow.rotation.x = side * -0.08;
    headGroup.add(brow); browMeshes.push(brow);
  }

  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.022, 10, 8), solid(skinColor));
  nose.scale.set(1.25, 0.8, 0.85); nose.position.set(0.164, -0.015, 0); headGroup.add(nose);
  const mouth = new THREE.Mesh(new THREE.TorusGeometry(0.031, 0.0065, 6, 14, Math.PI), basic('#70434a'));
  mouth.position.set(0.147, -0.073, 0);
  mouth.rotation.set(0, Math.PI / 2, Math.PI);
  headGroup.add(mouth);

  const hairColor = outfit.headColor || outfit.hairColor || '#30252d';
  if (outfit.head === 'cap' || outfit.head === 'beanie') {
    const cap = new THREE.Mesh(
      new THREE.SphereGeometry(headRadius * 1.055, 18, 12, 0, Math.PI * 2, 0, Math.PI / 2.12),
      solid(hairColor)
    );
    cap.position.y = 0.052; headGroup.add(cap);
    if (outfit.head === 'cap') {
      const brim = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.025, 0.18), solid(hairColor));
      brim.position.set(0.105, 0.035, 0); headGroup.add(brim);
    } else {
      const band = new THREE.Mesh(new THREE.TorusGeometry(0.151, 0.018, 8, 20), solid(outfit.color || hairColor));
      band.position.y = -0.012; headGroup.add(band);
    }
  } else {
    // Short swept hair gives uncovered characters a clear silhouette without changing their identity palette.
    const hair = new THREE.Mesh(
      new THREE.SphereGeometry(headRadius * 1.04, 18, 12, 0, Math.PI * 2, 0, Math.PI / 2.15),
      solid(hairColor)
    );
    hair.position.set(-0.006, 0.056, 0); headGroup.add(hair);
    const fringe = new THREE.Mesh(new THREE.SphereGeometry(0.064, 12, 8), solid(hairColor));
    fringe.scale.set(0.72, 0.35, 1.15);
    fringe.position.set(0.105, 0.065, 0.012); headGroup.add(fringe);
  }

  // Hoodie hood, front zipper, drawstrings and a soft pouch pocket establish a readable wardrobe.
  if (topType === 'hoodie' || topType === 'tracksuit') {
    const hood = new THREE.Mesh(new THREE.TorusGeometry(0.145, 0.035, 8, 24), solid(shirtColor));
    hood.rotation.y = Math.PI / 2; hood.position.set(-0.105, 0.48, 0); upperBody.add(hood);
    const zip = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.40, 0.012), basic('#c6d3da'));
    zip.position.set(0.174, 0.17, 0); upperBody.add(zip);
    const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.13, 0.21), solid(shirtColor));
    pocket.position.set(0.171, -0.075, 0); upperBody.add(pocket);
    for (const side of [-1, 1]) {
      const string = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 0.12, 6), basic('#e1d8cc'));
      string.position.set(0.177, 0.36, side * 0.044); upperBody.add(string);
      addRoundDetail(upperBody, 0.012, '#e1d8cc', [0.177, 0.295, side * 0.044], 8);
    }
  }

  const limbs = {};
  const arm = (side) => {
    const shoulder = new THREE.Group();
    shoulder.position.set(0, 0.51, side * 0.205);
    upperBody.add(shoulder);
    const sleeveColor = topType === 'none' ? skinColor : torsoColor;
    const radius = topType === 'none' ? 0.057 : 0.073;
    addRoundDetail(shoulder, radius * 1.16, sleeveColor, [0, -0.025, 0], 12);
    const upper = capsule(radius, 0.275, sleeveColor, 12);
    upper.position.y = -0.15; shoulder.add(upper);
    const elbow = new THREE.Group();
    elbow.position.y = -0.285; shoulder.add(elbow);
    const forearm = capsule(radius * 0.88, 0.265, sleeveColor, 12);
    forearm.position.y = -0.14; elbow.add(forearm);
    const cuff = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.88, radius * 0.88, 0.055, 12), solid(topType === 'none' ? skinColor : shirtColor));
    cuff.position.y = -0.275; elbow.add(cuff);
    const hand = addRoundDetail(elbow, 0.058, skinColor, [0.018, -0.325, 0], 12);
    const thumb = addRoundDetail(elbow, 0.026, skinColor, [0.045, -0.302, side * -0.04], 8);
    shoulder.userData.elbow = elbow;
    shoulder.userData.hand = hand;
    return shoulder;
  };
  limbs.lA = arm(-1);
  limbs.rA = arm(1);

  const leg = (side) => {
    const hip = new THREE.Group();
    hip.position.set(0, -0.055, side * 0.087);
    rig.add(hip);
    const upper = capsule(0.073, 0.335, pantsColor, 12);
    upper.position.y = -0.17; hip.add(upper);
    const knee = new THREE.Group();
    knee.position.y = -0.335; hip.add(knee);
    addRoundDetail(knee, 0.067, pantsColor, [0, -0.012, 0], 10);
    const lower = capsule(0.063, 0.375, pantsColor, 12);
    lower.position.y = -0.19; knee.add(lower);
    const ankle = new THREE.Mesh(new THREE.CylinderGeometry(0.061, 0.064, 0.07, 12), solid(pantsColor));
    ankle.position.y = -0.375; knee.add(ankle);
    const shoe = new THREE.Mesh(new THREE.SphereGeometry(0.095, 14, 10), solid(outfit.shoes || '#20242c'));
    shoe.scale.set(1.42, 0.62, 0.92);
    shoe.position.set(0.055, -0.425, 0); knee.add(shoe);
    const sole = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.025, 0.12), solid('#151a22'));
    sole.position.set(0.052, -0.473, 0); knee.add(sole);
    hip.userData.knee = knee;
    return hip;
  };
  limbs.lL = leg(-1);
  limbs.rL = leg(1);

  // Compact emissive edge highlights keep the 3D silhouette legible against night scenes.
  const rimColor = col(o.rim || M.rim);
  const rimMaterial = new THREE.MeshBasicMaterial({
    color: rimColor, side: THREE.BackSide, transparent: true, opacity: o.rimOpacity ?? 0.62,
    depthWrite: false,
  });
  [torso, pelvis, head].forEach((part) => {
    const outline = new THREE.Mesh(part.geometry, rimMaterial);
    outline.scale.setScalar(1.055); part.add(outline);
  });

  const setPose = (name, t = 0) => {
    const base = PO[name] || PO.stand;
    let pose = base;
    let phase = 0;
    if (name === 'walk' || name === 'run') {
      const speed = name === 'run' ? 1.55 : 0.92;
      const stride = name === 'run' ? 0.78 : 0.46;
      phase = t * Math.PI * 2 * speed;
      const swing = Math.sin(phase) * stride;
      pose = {
        lA: [-swing * 0.82, -0.06], rA: [swing * 0.82, 0.06],
        lL: [swing, 0.035], rL: [-swing, -0.035],
      };
    }

    Object.keys(limbs).forEach((key) => {
      limbs[key].rotation.set(0, 0, pose[key][0]);
      limbs[key].rotation.x = pose[key][1] + (key === 'lA' ? 0.16 : key === 'rA' ? -0.16 : 0);
    });

    const elbowBase = {
      carry: [-0.34, 0.34], hug: [-0.72, 0.72], pull: [-0.28, 0.32],
      shield: [0.42, -0.42], crouch: [0.18, -0.18], reach: [-0.08, -0.08],
      bike: [-0.16, -0.16], run: [-0.52, -0.52], walk: [-0.22, -0.22],
      wave: [0.0, -0.18], point: [0.0, -0.02],
    }[name] || [0, 0];
    limbs.lA.userData.elbow.rotation.z = elbowBase[0];
    limbs.rA.userData.elbow.rotation.z = elbowBase[1];

    const knee = {
      crouch: [0.98, 0.98], shield: [0.88, 0.88], kneel: [1.30, 0.12],
      sit: [1.22, 1.22], run: [0.25 + Math.max(0, Math.sin(phase + Math.PI * 0.5)) * 0.78,
        0.25 + Math.max(0, Math.sin(phase - Math.PI * 0.5)) * 0.78],
      walk: [0.10 + Math.max(0, Math.sin(phase + Math.PI * 0.5)) * 0.40,
        0.10 + Math.max(0, Math.sin(phase - Math.PI * 0.5)) * 0.40],
    }[name] || [0.025, 0.025];
    limbs.lL.userData.knee.rotation.z = knee[0];
    limbs.rL.userData.knee.rotation.z = knee[1];

    // Weight shifts and anticipation make poses read as actions rather than static icon gestures.
    const breathe = Math.sin(t * 2.15) * 0.012;
    const lean = name === 'run' ? -0.105 : name === 'walk' ? -0.045
      : name === 'bike' ? -0.15 : name === 'pull' ? -0.10
      : name === 'reach' ? -0.045 : name === 'shield' ? -0.085 : 0;
    upperBody.rotation.z = lean + breathe;
    upperBody.rotation.x = name === 'run' ? Math.sin(phase) * 0.035
      : name === 'walk' ? Math.sin(phase) * 0.018 : 0;
    upperBody.position.y = name === 'run' ? 0.035 + Math.abs(Math.cos(phase)) * 0.055
      : name === 'walk' ? 0.012 + Math.abs(Math.cos(phase)) * 0.022 : breathe * 0.45;

    headGroup.rotation.z = name === 'run' ? 0.055 : name === 'kneel' ? 0.035
      : name === 'hug' ? Math.sin(t * 1.35) * 0.025 : Math.sin(t * 1.5) * 0.012;
    headGroup.rotation.x = name === 'run' ? -0.035 : 0;
    const blink = Math.abs(Math.sin(t * 2.9 + 0.7)) > 0.989 ? 0.18 : 1;
    eyeMeshes.forEach((eye) => { eye.scale.y = 1.10 * blink; });
    browMeshes.forEach((brow, i) => {
      brow.rotation.z = name === 'sad' ? (i === 0 ? -0.18 : 0.18)
        : name === 'surprised' ? (i === 0 ? 0.12 : -0.12) : 0;
    });
    if (name === 'hug') {
      limbs.lA.userData.elbow.rotation.z += Math.sin(t * 1.6) * 0.07;
      limbs.rA.userData.elbow.rotation.z -= Math.sin(t * 1.6) * 0.07;
      upperBody.rotation.y = Math.sin(t * 1.4) * 0.035;
    } else if (name === 'pull' || name === 'shield') {
      upperBody.rotation.y = Math.sin(t * 2.2) * 0.025;
    } else {
      upperBody.rotation.y = name === 'run' ? Math.sin(phase) * 0.025 : 0;
    }
  };

  grp.scale.setScalar(scale);
  grp.position.set(o.x || 0, 0, o.z || 0);
  grp.rotation.y = o.ry || 0;
  grp.userData.setPose = setPose;
  grp.userData.modelVersion = 'cinematic-v1';

  const shadow = new THREE.Mesh(
    new THREE.CircleGeometry(0.53, 28),
    new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.28, depthWrite: false })
  );
  shadow.rotation.x = -Math.PI / 2;
  shadow.position.y = 0.012;
  shadow.scale.set(1.0, 0.54, 1);
  grp.add(shadow);

  setPose(o.pose || 'stand', 0);
  return grp;
}

// ---------- may quay
// xoay quanh diem target: goc tu `from` den `to` (rad) trong `dur` giay
export function orbit(cam, t, o = {}) {
  const { target = [0, 1, 0], radius = 8, height = 2.5, from = -0.6, to = 0.4, dur = 4, lift = 0 } = o;
  const k = ease.inOut(clamp(t / dur)), a = lerp(from, to, k);
  cam.position.set(target[0] + Math.cos(a) * radius, target[1] + height + lift * k, target[2] + Math.sin(a) * radius); cam.lookAt(...target);
}
// bay theo keyframe: [[t, {pos:[x,y,z], look:[x,y,z], fov}], ...]
export function dolly(cam, t, keys) {
  let a = keys[0], b = keys[keys.length - 1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { a = keys[i - 1]; b = keys[i]; break; }
  const k = ease.inOut(clamp((t - a[0]) / Math.max(1e-6, b[0] - a[0])));
  const L = (p, q) => p.map((v, i) => lerp(v, q[i], k));
  cam.position.set(...L(a[1].pos, b[1].pos)); cam.lookAt(...L(a[1].look, b[1].look));
  if (a[1].fov) { cam.fov = lerp(a[1].fov, b[1].fov ?? a[1].fov, k); cam.updateProjectionMatrix(); }
}
export { THREE };
