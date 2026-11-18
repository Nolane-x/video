// three3d.js — canh 3D (Three.js) cung phong cach: nguoi que den vien sang, nha cua so sang den, suong mu, mau theo mood.
// Dung trong shot: registerShot('s010', { kind: '3d', init(T, info) {...; return { stage }}, draw(s, t, info, T) {...}, overlay(g, t, info, s) {...} })
// Don vi: met. Nguoi que cao ~1.75 m, nhin ve huong +x.
import * as THREE from 'three';
import { E, mood, hex, rng, lerp, clamp, ease, UI } from './core.js';

let R = null;              // WebGLRenderer dung chung
export function renderer(w, h) {
  if (!R) {
    const c = document.createElement('canvas');
    R = new THREE.WebGLRenderer({ canvas: c, antialias: true, preserveDrawingBuffer: true, alpha: false });
    R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.NoToneMapping;
  }
  if (R.domElement.width !== w || R.domElement.height !== h) R.setSize(w, h, false);
  return R;
}
const col = (c) => new THREE.Color(...hex(c).map((v) => v / 255)).convertSRGBToLinear();
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: col(c), emissive: col(c).multiplyScalar(0.22), flatShading: true, ...o });
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
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128); _glo
…[1 chars truncated — re-run with head/grep/tail for full output]…
+ lift * k, target[2] + Math.sin(a) * radius); cam.lookAt(...target);
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
