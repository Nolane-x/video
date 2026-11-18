import { registerShot, E, FONTS } from '/engine/core.js';
import * as T3 from '/engine/three3d.js';

const THREE = T3.THREE;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const smooth = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const mat = (color, emissive = '#000000', intensity = 0, extra = {}) =>
  new THREE.MeshStandardMaterial({ color, emissive, emissiveIntensity: intensity, roughness: 0.78, metalness: 0.08, ...extra });

function rod(a, b, radius, material) {
  const av = V(...a), bv = V(...b), delta = bv.clone().sub(av), length = delta.length();
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, length, 10), material);
  mesh.position.copy(av.add(bv).multiplyScalar(0.5));
  mesh.quaternion.setFromUnitVectors(V(0, 1, 0), delta.normalize());
  return mesh;
}

function makeBike() {
  const root = new THREE.Group();
  const tire = mat('#101722'), rim = mat('#aebdcb', '#52718a', 0.12, { metalness: 0.72, roughness: 0.3 });
  const frame = mat('#d95a63', '#711e37', 0.2, { metalness: 0.32, roughness: 0.38 });
  const metal = mat('#a9b8c6', '#59718b', 0.1, { metalness: 0.75, roughness: 0.28 });
  const wheels = [];
  for (const x of [-0.82, 0.82]) {
    const wheel = new THREE.Group();
    wheel.add(new THREE.Mesh(new THREE.TorusGeometry(0.51, 0.043, 10, 36), tire));
    wheel.add(new THREE.Mesh(new THREE.TorusGeometry(0.455, 0.018, 8, 36), rim));
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 0.12, 12), metal); hub.rotation.x = Math.PI / 2; wheel.add(hub);
    for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; wheel.add(rod([0, 0, 0], [Math.cos(a) * 0.45, Math.sin(a) * 0.45, 0], 0.009, metal)); }
    wheel.position.set(x, 0.56, 0); root.add(wheel); wheels.push(wheel);
  }
  const rear = [-0.82, 0.56, 0], front = [0.82, 0.56, 0], crank = [-0.12, 0.55, 0], seat = [-0.36, 1.03, 0], handle = [0.55, 1.1, 0];
  [[rear, crank], [crank, front], [rear, seat], [seat, crank], [seat, handle], [handle, front]].forEach(([a, b]) => root.add(rod(a, b, 0.045, frame)));
  root.add(rod([-0.48, 1.1, 0], [-0.22, 1.1, 0], 0.05, mat('#171d28')));
  root.add(rod([0.47, 1.1, 0], [0.58, 1.32, 0], 0.04, metal));
  root.add(rod([0.38, 1.32, -0.26], [0.68, 1.32, 0.26], 0.035, metal));
  const saddle = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.08, 0.18), mat('#202a38')); saddle.position.set(-0.38, 1.08, 0); root.add(saddle);
  const crankArm = new THREE.Group(); crankArm.position.set(-0.12, 0.55, 0); root.add(crankArm); crankArm.add(rod([-0.34, 0, 0], [0.34, 0, 0], 0.025, metal));
  const light = new THREE.Mesh(new THREE.SphereGeometry(0.075, 12, 8), mat('#ffe3a1', '#ffb957', 1.6)); light.position.set(0.82, 0.82, 0.05); root.add(light);
  return { root, wheels, crankArm };
}

function makeBillboard() {
  const root = new THREE.Group(), metal = mat('#4d5968', '#1a2b3b', 0.18, { metalness: 0.66, roughness: 0.34 });
  root.add(T3.box(5.9, 0.18, 0.22, '#526174', { y: -1.65, z: 0, mat: metal }));
  root.add(T3.box(5.9, 0.18, 0.22, '#526174', { y: 1.65, z: 0, mat: metal }));
  for (const x of [-2.78, 2.78]) { root.add(T3.cyl(0.085, 0.11, 3.55, '#536174', { x, y: -0.1, z: -0.12, mat: metal })); root.add(T3.box(0.32, 0.34, 0.38, '#6a7889', { x, y: -1.78, z: -0.08, mat: metal })); }
  root.add(T3.box(5.65, 3.05, 0.16, '#19263a', { y: 0, z: 0, mat: mat('#19263a') }));
  const canvas = document.createElement('canvas'); canvas.width = 1200; canvas.height = 620;
  const g = canvas.getContext('2d'), grad = g.createLinearGradient(0, 0, 1200, 620);
  grad.addColorStop(0, '#172c4b'); grad.addColorStop(1, '#542a45'); g.fillStyle = grad; g.fillRect(0, 0, 1200, 620);
  g.strokeStyle = '#f5c17d'; g.lineWidth = 18; g.strokeRect(24, 24, 1152, 572);
  g.fillStyle = '#ffe5b6'; g.font = '800 88px Arial'; g.textAlign = 'center'; g.fillText('ĐÊM PHỐ', 600, 225);
  g.fillStyle = '#ffffff'; g.font = '700 62px Arial'; g.fillText('CỬA HÀNG 24H', 600, 335);
  g.fillStyle = '#ffd18a'; g.font = '800 132px Arial'; g.fillText('MỞ CỬA', 600, 505);
  const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace;
  const plane = new THREE.Mesh(new THREE.PlaneGeometry(5.38, 2.78), new THREE.MeshBasicMaterial({ map: tex })); plane.position.set(0, 0, 0.105); root.add(plane);
  for (const x of [-2.58, 2.58]) for (const y of [-1.27, 1.27]) { const bolt = new THREE.Mesh(new THREE.SphereGeometry(0.055, 10, 8), mat('#d8dee5', '#6f91ad', 0.2, { metalness: 0.8 })); bolt.position.set(x, y, 0.15); root.add(bolt); }
  const glow = T3.sprite('#ffbf7c', 6.5, 0.22); glow.position.set(0, 0, -0.3); root.add(glow);
  root.position.set(3.6, 3.55, -3.7); return root;
}

function makeRain(scene) {
  const count = 420, base = [], arr = new Float32Array(count * 6);
  for (let i = 0; i < count; i++) base.push({ x: (i * 71 % 190) / 10 - 9.5, y: (i * 113 % 175) / 10 + 1.5, z: (i * 47 % 180) / 10 - 9 });
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  const rain = new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: '#9fc8ed', transparent: true, opacity: 0.34, depthWrite: false })); scene.add(rain);
  const update = (t, frozen = false) => { const p = geo.attributes.position.array; for (let i = 0; i < count; i++) { const b = base[i], fall = frozen ? 0 : (t * 13.5 + i * 0.23) % 16, y = Math.max(0.15, b.y - fall), k = i * 6; p[k] = b.x; p[k + 1] = y; p[k + 2] = b.z; p[k + 3] = b.x - 0.09; p[k + 4] = y - 0.36; p[k + 5] = b.z; } geo.attributes.position.needsUpdate = true; };
  update(0, false); return { update, rain };
}

function makeStreet(info) {
  const stage = T3.stage({ mood: 'storm', fog: [22, 72], fov: 37, ambient: 1.45, keyIntensity: 1.85, keyPos: [-9, 12, 10], sun: false });
  const { scene, camera } = stage;
  scene.add(camera);
  // A dedicated camera-space subtitle plate remains inside the active picture area,
  // clear of H2's cinematic letterbox bars.
  const caption = String(info?.line || '').trim();
  if (caption) {
    const cv = document.createElement('canvas'); cv.width = 1400; cv.height = 190;
    const cg = cv.getContext('2d');
    cg.fillStyle = 'rgba(5, 12, 22, 0.82)'; cg.beginPath(); cg.roundRect(12, 12, 1376, 166, 24); cg.fill();
    cg.strokeStyle = 'rgba(146, 210, 250, 0.72)'; cg.lineWidth = 3; cg.stroke();
    const words = caption.split(/\s+/); const rows = []; let row = '';
    cg.font = '700 44px Arial';
    for (const word of words) { const test = row ? row + ' ' + word : word; if (cg.measureText(test).width > 1120 && row) { rows.push(row); row = word; } else row = test; }
    if (row) rows.push(row); cg.fillStyle = '#fff8ed'; cg.textAlign = 'center'; cg.textBaseline = 'middle';
    const textRows = rows.slice(0, 2); textRows.forEach((line, i) => cg.fillText(line, 700, textRows.length === 1 ? 96 : 65 + i * 58));
    const texture = new THREE.CanvasTexture(cv); texture.colorSpace = THREE.SRGBColorSpace;
    const plate = new THREE.Mesh(new THREE.PlaneGeometry(5.0, 0.76), new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthTest: false, depthWrite: false, side: THREE.DoubleSide, fog: false }));
    plate.position.set(0, -0.3, -5.8); camera.add(plate);
  }
  scene.add(T3.ground(48, 30, '#202733'));
  const road = new THREE.Mesh(new THREE.PlaneGeometry(48, 9.5), mat('#111923', '#101a28', 0.08)); road.rotation.x = -Math.PI / 2; road.position.set(0, 0.02, 0.1); scene.add(road);
  scene.add(T3.box(48, 0.24, 3.2, '#333e4d', { y: 0.12, z: 6.3 })); scene.add(T3.box(48, 0.24, 3.2, '#333e4d', { y: 0.12, z: -6.3 }));
  const lane = mat('#dbb66d', '#7f6137', 0.12); for (let x = -21; x <= 21; x += 4.4) { const dash = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.025, 0.11), lane); dash.position.set(x, 0.045, -0.2); scene.add(dash); }
  for (const [x, z, h, w] of [[-12, -11, 10, 5], [-6.5, -13, 8, 4], [10.5, -12, 11, 5], [15, -10, 8, 4], [-17, -8, 7, 4]]) scene.add(T3.building(w, h, 3.1, { x, z, mood: 'storm', seed: Math.abs(x * 13), litChance: 0.52 }));
  scene.add(T3.lamp({ x: -5.8, z: 3.1, mood: 'storm', color: '#ffd39b', intensity: 10 })); scene.add(T3.lamp({ x: 7.8, z: -5.2, mood: 'storm', color: '#f3c58f', intensity: 7 }));
  const bike = makeBike(); bike.root.position.set(-1.4, 0, 1.4); scene.add(bike.root);
  const mom = T3.figure({ top: 'hoodie', color: '#a94f68', legs: '#242b3b', head: 'beanie', headColor: '#642d43' }, { mood: 'storm', s: 1.0, rim: '#ffd1d9', rimOpacity: 0.85 }); mom.position.set(-1.4, 0.02, 1.4); scene.add(mom);
  const kid = T3.figure({ top: 'hoodie', color: '#3858a5', legs: '#192337', head: 'beanie', headColor: '#16223d' }, { mood: 'storm', s: 0.92, rim: '#9dd9ff', rimOpacity: 0.95 }); kid.position.set(-4.8, 0, 0.1); scene.add(kid);
  const sign = makeBillboard(); scene.add(sign); const rain = makeRain(scene);
  for (let i = 0; i < 8; i++) { const m = new THREE.Mesh(new THREE.CircleGeometry(0.45 + (i % 3) * 0.22, 24), new THREE.MeshBasicMaterial({ color: '#7799b9', transparent: true, opacity: 0.11, depthWrite: false })); m.rotation.x = -Math.PI / 2; m.position.set(-8 + i * 2.6, 0.047, i % 2 ? 1.7 : -1.8); scene.add(m); }
  const debris = new THREE.Group(); for (let i = 0; i < 9; i++) { const bit = T3.box(0.14 + (i % 3) * 0.12, 0.08, 0.1, '#69798b', { y: 0, mat: mat('#69798b', '#24364a', 0.12, { metalness: 0.6 }) }); bit.position.set(3.0 + i * 0.28, 0.2 + (i % 3) * 0.27, -2 + (i % 2) * 0.35); debris.add(bit); } scene.add(debris); debris.visible = false;
  camera.position.set(8.4, 5.2, 19.5); camera.lookAt(0.2, 2.15, -0.8);
  return { stage, scene, camera, bike, mom, kid, sign, rain, debris };
}

function cameraAt(s, t, mode = 'wide') {
  const c = s.camera; let pos, look, fov;
  if (mode === 'closeMom') { pos = [4.8, 3.1, 8.0]; look = [-1.2, 1.65, 1.2]; fov = 26; }
  else if (mode === 'feet') { pos = [1.4, 1.65, 8.6]; look = [-2.6, 0.45, 1.2]; fov = 28; }
  else if (mode === 'tracking') { pos = [5.0, 3.5, 12.0]; look = [-0.6, 1.55, 0.4]; fov = 30; }
  else if (mode === 'hug') { pos = [0.4, 2.7, 7.3]; look = [-1.35, 1.2, 1.2]; fov = 25; }
  else if (mode === 'impact') { pos = [6.2, 4.6, 14.0]; look = [1.2, 2.0, -1.5]; fov = 30; }
  else { pos = [6.0, 4.3, 13.5]; look = [0.2, 1.75, -0.8]; fov = 30; }
  const k = smooth(t / 4.5); c.position.set(pos[0] + Math.sin(t * 0.55) * 0.10, pos[1] + Math.sin(t * 0.7) * 0.045, pos[2]); c.lookAt(look[0] + (mode === 'tracking' ? lerp(-1.4, 0.9, k) : 0), look[1], look[2]); c.fov = fov; c.updateProjectionMatrix();
}

function animateCommon(s, t, frozen = false) {
  s.rain.update(t, frozen); s.bike.wheels.forEach((w, i) => { if (!frozen) w.rotation.z = -t * (1.8 + i * 0.04); });
  s.mom.userData.setPose('bike', t); s.kid.userData.setPose('stand', t); s.sign.rotation.z = 0.045 * Math.sin(t * 2.8); cameraAt(s, t, 'wide');
}

function overlay(g, t, info, freeze = false, title = '') {
  if (freeze) { g.save(); g.globalCompositeOperation = 'screen'; const x = E.W * 0.53, y = E.H * 0.48, pulse = 0.5 + 0.5 * Math.sin(t * 3.4), rad = 150 + pulse * 58; const gr = g.createRadialGradient(x, y, 10, x, y, rad * 2.2); gr.addColorStop(0, 'rgba(108,208,255,0.12)'); gr.addColorStop(0.5, 'rgba(72,165,255,0.06)'); gr.addColorStop(1, 'rgba(40,110,230,0)'); g.fillStyle = gr; g.fillRect(0, 0, E.W, E.H); for (let i = 0; i < 3; i++) { g.beginPath(); g.arc(x, y, rad * (0.55 + i * 0.45), 0, Math.PI * 2); g.strokeStyle = `rgba(149,221,255,${0.34 - i * 0.08})`; g.lineWidth = 2.5 - i * 0.35; g.stroke(); } g.restore(); }
  const line = String(info.line || '').trim();
  if (line) { g.save(); g.font = `600 37px ${FONTS.body}`; const max = E.W - 260, rows = []; let row = ''; for (const word of line.split(/\s+/)) { const test = row ? `${row} ${word}` : word; if (g.measureText(test).width > max && row) { rows.push(row); row = word; } else row = test; } if (row) rows.push(row); const lines = rows.slice(0, 2), h = lines.length * 49 + 34, y = E.H - 80 - h / 2; g.fillStyle = 'rgba(6,12,22,0.72)'; g.beginPath(); g.roundRect(95, y - h / 2, E.W - 190, h, 18); g.fill(); g.strokeStyle = 'rgba(154,208,245,0.28)'; g.lineWidth = 1.5; g.stroke(); g.fillStyle = '#f6f8fb'; g.textAlign = 'center'; g.textBaseline = 'middle'; lines.forEach((txt, i) => g.fillText(txt, E.W / 2, y - (lines.length - 1) * 24.5 + i * 49)); g.restore(); }
  if (title) { g.save(); g.font = '700 24px Arial'; g.textAlign = 'left'; g.textBaseline = 'top'; g.fillStyle = 'rgba(164,220,255,0.75)'; g.fillText(title, 70, 56); g.restore(); }
}

function reg(id, behavior, cameraMode = 'wide', frozen = false) {
  registerShot(id, { kind: '3d', init: (T, info) => makeStreet(info), draw: (s, t) => {
    const p = clamp(t / 4.5); animateCommon(s, t, frozen); s.mom.position.set(-1.4, 0.02, 1.4); s.kid.position.set(-4.8, 0, 0.1); s.bike.root.position.set(-1.4, 0, 1.4); s.debris.visible = false;
    if (behavior) behavior(s, t, p); cameraAt(s, t, cameraMode); if (frozen) { s.rain.update(t, true); s.sign.rotation.z = lerp(0.18, 0.3, smooth(p)); }
  }, overlay: (g, t, info) => overlay(g, t, info, frozen, frozen ? 'TIME STOP  /  00:10' : '') });
}

reg('s053', (s, t, p) => { s.bike.root.position.x = lerp(-2.2, -1.2, smooth(p)); s.mom.position.x = s.bike.root.position.x; s.sign.rotation.z = 0.015 * Math.sin(t * 2.6); s.kid.visible = false; }, 'wide', false);
reg('s054', (s, t) => { s.bike.root.position.x = -1.2; s.mom.position.x = -1.2; s.kid.visible = false; s.sign.rotation.z = 0.035 * Math.sin(t * 9) + 0.04 * clamp(t / 4.5); }, 'impact', false);
reg('s056', (s, t, p) => { s.bike.root.position.x = -0.9; s.mom.position.x = -0.9; s.kid.visible = false; s.sign.rotation.z = lerp(0.06, 0.32, smooth(p)); }, 'wide', false);
reg('s058', (s, t) => { s.bike.root.visible = false; s.kid.visible = false; s.mom.position.set(-1.4, 0.05, 1.3); s.mom.scale.setScalar(1.32); s.mom.userData.setPose('bike', t); }, 'closeMom', false);
reg('s059', (s, t, p) => { s.bike.root.position.x = -0.7; s.mom.position.x = -0.7; s.kid.visible = true; s.kid.position.x = lerp(-5.1, -4.2, smooth(p)); s.kid.userData.setPose('stand', t); s.sign.rotation.z = 0.29 + 0.025 * Math.sin(t * 7); }, 'wide', false);
reg('s061', (s, t, p) => { s.bike.root.position.x = -0.4; s.mom.position.x = -0.4; s.kid.position.x = -4.0; s.kid.userData.setPose('reach', t); s.sign.rotation.z = 0.33; }, 'wide', true);
reg('s062', (s, t) => { s.bike.root.visible = false; s.mom.visible = false; s.kid.position.set(-2.9, 0, 1.3); s.kid.userData.setPose('run', t * 1.4); }, 'feet', true);
reg('s063', (s, t, p) => { s.kid.position.x = lerp(-4.6, -0.5, smooth(p)); s.kid.position.z = 1.2; s.kid.userData.setPose('run', t * 1.8); s.bike.root.position.x = -0.35; s.mom.position.x = -0.35; s.sign.rotation.z = 0.33; }, 'tracking', true);
reg('s064', (s, t) => { s.kid.position.set(0.0, 0, 1.45); s.kid.userData.setPose('reach', t); s.bike.root.position.x = -0.05; s.mom.position.x = -0.05; s.mom.userData.setPose('bike', t); }, 'closeMom', true);
reg('s065', (s, t, p) => { s.kid.position.x = lerp(0.0, -1.7, smooth(p)); s.kid.userData.setPose('pull', t); s.bike.root.position.x = lerp(-0.05, -1.8, smooth(p)); s.mom.position.x = s.bike.root.position.x; s.mom.userData.setPose('bike', t); s.sign.rotation.z = 0.34; }, 'tracking', true);
reg('s066', (s, t, p) => { s.bike.root.position.x = lerp(-1.8, -2.5, smooth(p)); s.mom.position.x = s.bike.root.position.x; s.kid.position.x = lerp(-1.7, -2.9, smooth(p)); s.kid.userData.setPose('pull', t); }, 'feet', true);
reg('s067', (s, t, p) => { s.bike.root.position.x = -3.3; s.mom.position.set(-2.4, 0, 1.5); s.mom.userData.setPose('kneel', t); s.kid.position.set(-1.55, 0, 1.3); s.kid.userData.setPose('crouch', t); s.bike.root.rotation.z = -0.08 * smooth(p); }, 'tracking', true);
reg('s068', (s, t, p) => { s.bike.root.position.x = lerp(-3.3, -4.0, smooth(p)); s.mom.position.set(-2.5, 0, 1.5); s.mom.userData.setPose('stand', t); s.kid.position.x = lerp(-1.55, -2.45, smooth(p)); s.kid.userData.setPose('pull', t); }, 'wide', true);
reg('s069', (s, t, p) => { s.bike.root.position.x = -4.0; s.mom.position.set(-2.9, 0, 1.7); s.mom.userData.setPose('crouch', t); s.kid.position.set(-1.9, 0, 1.25); s.kid.userData.setPose('shield', t); s.sign.rotation.z = lerp(0.36, 0.48, smooth(p)); }, 'impact', true);
reg('s070', (s, t) => { s.bike.root.position.x = -4.0; s.mom.position.set(-2.9, 0, 1.7); s.kid.position.set(-1.9, 0, 1.25); s.mom.userData.setPose('crouch', t); s.kid.userData.setPose('shield', t); const fall = smooth(clamp((t - 0.32) / 3.6)); s.sign.rotation.z = lerp(0.48, 1.12, fall); s.debris.visible = t > 0.9; s.debris.position.y = -(Math.max(0, t - 1.1) ** 2) * 0.9; }, 'impact', false);
reg('s071', (s, t) => { s.bike.root.position.set(-4.0, 0, 1.8); s.bike.root.rotation.z = -0.8; s.mom.position.set(-2.4, 0, 1.55); s.mom.userData.setPose('sit', t); s.kid.position.set(-1.0, 0, 1.45); s.kid.userData.setPose('sit', t); s.sign.rotation.z = 1.12; }, 'hug', false);
reg('s072', (s, t) => { s.bike.root.position.set(-4.0, 0, 1.8); s.bike.root.rotation.z = -0.8; s.mom.position.set(-1.55, 0, 1.45); s.kid.position.set(-0.82, 0, 1.45); s.mom.userData.setPose('hug', t); s.kid.userData.setPose('hug', t); s.mom.rotation.y = 0; s.kid.rotation.y = Math.PI; s.sign.rotation.z = 1.12; }, 'hug', false);
