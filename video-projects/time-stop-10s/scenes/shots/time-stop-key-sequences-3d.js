import { registerShot, E, FONTS } from '/engine/core.js';
import * as T3 from '/engine/three3d.js';

const THREE = T3.THREE;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const smooth = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const std = (color, extra = {}) => new THREE.MeshStandardMaterial({
  color, roughness: 0.78, metalness: 0.05, ...extra,
});
const addRod = (group, a, b, radius, material) => {
  const av = new THREE.Vector3(...a), bv = new THREE.Vector3(...b);
  const delta = bv.clone().sub(av), length = delta.length();
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, length, 10), material);
  mesh.position.copy(av.add(bv).multiplyScalar(0.5));
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), delta.normalize());
  group.add(mesh); return mesh;
};
const addPerson = (color, mood, scale = 1, head = 'none') => T3.figure({
  top: 'hoodie', color, legs: '#18212d', skin: '#efd8c2', head,
  headColor: color,
}, { mood, s: scale, rim: '#b9dfff', rimOpacity: 0.62 });
function stage(mood, options = {}) {
  const st = T3.stage({ mood, fog: options.fog || [34, 110], fov: options.fov || 36,
    ambient: options.ambient ?? 1.55, keyIntensity: options.keyIntensity ?? 1.9,
    keyPos: options.keyPos || [-8, 12, 9], sun: false });
  st.scene.add(st.camera);
  return st;
}
function setCamera(s, pos, look, fov, t) {
  const p = clamp(t / 4.5);
  s.camera.position.set(pos[0] + Math.sin(t * 0.34) * 0.045,
    pos[1] + Math.sin(t * 0.46) * 0.025, pos[2]);
  s.camera.lookAt(look[0] + Math.sin(p * Math.PI) * 0.08, look[1], look[2]);
  s.camera.fov = fov; s.camera.updateProjectionMatrix();
}
function overlay(g, t, info, frozen = false) {
  if (frozen) {
    g.save(); g.globalCompositeOperation = 'screen';
    const x = E.W * 0.5, y = E.H * 0.43, pulse = 0.5 + 0.5 * Math.sin(t * 3.1);
    const radius = 150 + pulse * 42;
    const glow = g.createRadialGradient(x, y, 8, x, y, radius * 2.3);
    glow.addColorStop(0, 'rgba(104,205,255,0.15)');
    glow.addColorStop(0.55, 'rgba(72,158,255,0.055)');
    glow.addColorStop(1, 'rgba(40,110,230,0)');
    g.fillStyle = glow; g.fillRect(0, 0, E.W, E.H);
    for (let i = 0; i < 3; i++) {
      g.beginPath(); g.arc(x, y, radius * (0.55 + i * 0.44), 0, Math.PI * 2);
      g.strokeStyle = 'rgba(149,221,255,' + (0.32 - i * 0.075) + ')';
      g.lineWidth = 2.5 - i * 0.35; g.stroke();
    }
    g.restore();
  }
  const timer = info?.shot?.args?.hud?.rows?.[0]?.n;
  if (timer !== undefined) {
    g.save(); g.font = '700 25px ' + FONTS.mono; g.textAlign = 'left'; g.textBaseline = 'middle';
    g.fillStyle = 'rgba(5,12,22,0.78)'; g.beginPath(); g.roundRect(72, 166, 260, 56, 13); g.fill();
    g.strokeStyle = 'rgba(135,210,255,0.75)'; g.lineWidth = 2; g.stroke();
    g.fillStyle = '#b8e9ff'; g.fillText('GIÂY CÒN  ' + String(timer).padStart(2, '0'), 94, 194); g.restore();
  }
  const line = String(info?.line || '').trim();
  if (line) {
    g.save();
    const fontSize = 37, maxWidth = E.W - 360, rows = [];
    g.font = '600 ' + fontSize + 'px ' + FONTS.body;
    let row = '';
    for (const word of line.split(/\s+/)) {
      const next = row ? row + ' ' + word : word;
      if (g.measureText(next).width > maxWidth && row) { rows.push(row); row = word; }
      else row = next;
    }
    if (row) rows.push(row);
    const visible = rows.slice(0, 2), lineHeight = 46;
    const h = Math.max(66, visible.length * lineHeight + 24);
    // Keep the subtitle plate above the active image's lower letterbox bar.
    const ratio = E.cfg.bars === 'scope' ? 2.39
      : E.cfg.bars === 'wide' ? 2.0
      : typeof E.cfg.bars === 'number' ? E.cfg.bars : 0;
    const bar = !E.vertical && ratio ? Math.max(0, (E.H - E.W / ratio) / 2) : 0;
    const safeBottom = E.H - bar;
    const top = safeBottom - 28 - h;
    g.fillStyle = 'rgba(5,10,18,0.86)'; g.beginPath(); g.roundRect(150, top, E.W - 300, h, 17); g.fill();
    g.strokeStyle = 'rgba(150,205,240,0.48)'; g.lineWidth = 1.5; g.stroke();
    g.font = '600 ' + fontSize + 'px ' + FONTS.body; g.textAlign = 'center';
    g.textBaseline = 'middle'; g.fillStyle = '#f7f8fa';
    visible.forEach((txt, i) => g.fillText(txt, E.W / 2,
      top + h / 2 + (i - (visible.length - 1) / 2) * lineHeight));
    g.restore();
  }
}
function install(id, build, draw, frozen) {
  registerShot(id, {
    kind: '3d',
    init: (_T, info) => build(info),
    draw: (s, t, info) => draw(s, t, info, id),
    overlay: (g, t, info) => overlay(g, t, info, frozen),
  });
  const shot = E.shots.find((x) => x.id === id);
  if (!shot) throw new Error('Missing story shot ' + id + ' for key-sequence 3D scene');
  shot.captions = false;
}

// -----------------------------------------------------------------------------
// SEQUENCE A — warm kitchen, a falling cup, suspended water and a ten-second rule
function makeCup() {
  const root = new THREE.Group(), ceramic = std('#e8e1d7', { roughness: 0.3 });
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.145, 0.42, 28), ceramic);
  body.position.y = 0.22; root.add(body);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(0.178, 0.018, 8, 28), std('#faf5e9', { roughness: 0.24 }));
  rim.position.y = 0.43; root.add(rim);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(0.135, 0.027, 8, 20), ceramic);
  handle.rotation.y = Math.PI / 2; handle.position.set(0.17, 0.24, 0); root.add(handle);
  const liquid = new THREE.Mesh(new THREE.CylinderGeometry(0.145, 0.145, 0.014, 24), std('#8b5b3d'));
  liquid.position.y = 0.34; root.add(liquid);
  return root;
}
function makeKitchen(info) {
  const st = stage('interiorWarm', { fog: [30, 90], fov: 37, ambient: 1.65 });
  const { scene, camera } = st;
  scene.add(T3.ground(22, 18, '#57443f'));
  scene.add(T3.box(22, 5.8, 0.35, '#49363b', { y: 2.9, z: -6.6 }));
  scene.add(T3.box(0.35, 5.8, 13, '#352932', { x: -10.8, y: 2.9, z: 0 }));
  scene.add(T3.box(22, 0.18, 0.45, '#211c24', { y: 0.12, z: -6.34 }));
  // Warm window with a deep frame and cool dawn outside.
  scene.add(T3.box(3.3, 2.25, 0.18, '#241f2c', { x: -4.7, y: 3.12, z: -6.34 }));
  scene.add(T3.pane(3.0, 1.95, '#59768b', { x: -4.7, y: 3.12, z: -6.22 }));
  scene.add(T3.box(0.08, 2.0, 0.08, '#c18b68', { x: -4.7, y: 3.12, z: -6.12 }));
  scene.add(T3.box(3.0, 0.08, 0.08, '#c18b68', { x: -4.7, y: 3.12, z: -6.12 }));
  // Cabinets, tiled backsplash, sink and stove build actual room depth.
  for (let i = 0; i < 5; i++) {
    scene.add(T3.box(1.75, 1.05, 0.62, i % 2 ? '#60464a' : '#695052',
      { x: -7.2 + i * 3.05, y: 3.92, z: -5.95 }));
    scene.add(T3.box(1.75, 0.07, 0.66, '#b98c6c', { x: -7.2 + i * 3.05, y: 3.35, z: -5.95 }));
  }
  for (let i = 0; i < 11; i++) for (let j = 0; j < 2; j++) {
    scene.add(T3.box(0.72, 0.48, 0.04, (i + j) % 2 ? '#6c5553' : '#735d59',
      { x: -7.2 + i * 1.45, y: 2.45 + j * 0.53, z: -6.28 }));
  }
  scene.add(T3.box(2.6, 1.55, 0.72, '#292833', { x: 6.6, y: 1.15, z: -5.7 }));
  scene.add(T3.box(2.8, 0.12, 0.85, '#aaa19a', { x: 6.6, y: 1.95, z: -5.65 }));
  scene.add(T3.box(1.15, 1.05, 0.72, '#35333b', { x: -8.5, y: 0.82, z: -5.5 }));
  // Table and visible wooden edge.
  scene.add(T3.box(5.25, 0.16, 1.72, '#a77b58', { x: 0.1, y: 0.96, z: 0.85 }));
  scene.add(T3.box(5.1, 0.05, 1.62, '#d2aa7e', { x: 0.1, y: 1.055, z: 0.85 }));
  for (const x of [-2.25, 2.45]) for (const z of [0.22, 1.48])
    scene.add(T3.box(0.13, 0.93, 0.13, '#654a3b', { x, y: 0.46, z }));
  scene.add(T3.lamp({ x: 2.2, z: -0.9, mood: 'interiorWarm', color: '#ffc985', intensity: 7 }));
  const hero = addPerson('#3c7186', 'interiorWarm', 1.05);
  const mom = T3.figure({ top: 'hoodie', color: '#a75b73', legs: '#292331',
    skin: '#e8cbb8' },
    { mood: 'interiorWarm', s: 1.04, rim: '#ffd7b0', rimOpacity: 0.72 });
  // The shared figure rig has no built-in "bun" head token, so author the hairstyle as real geometry.
  const momHair = std('#35232a', { roughness: 0.96 });
  const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.212, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2.05), momHair);
  hairCap.position.set(0, 1.78, 0); mom.add(hairCap);
  const hairBun = new THREE.Mesh(new THREE.SphereGeometry(0.12, 14, 10), momHair);
  hairBun.position.set(-0.13, 1.82, 0); mom.add(hairBun);
  hero.position.set(-3.1, 0, 1.65); mom.position.set(3.35, 0, 1.6);
  scene.add(hero, mom);
  const cup = makeCup(); cup.position.set(0.28, 1.04, 0.72); scene.add(cup);
  const water = new THREE.Group(); const waterMat = std('#b5e6ff', { transparent: true, opacity: 0.72, roughness: 0.1 });
  for (let i = 0; i < 16; i++) {
    const a = i * 2.399, r = 0.18 + (i % 4) * 0.10;
    const drop = new THREE.Mesh(new THREE.SphereGeometry(0.035 + (i % 3) * 0.012, 10, 8), waterMat);
    drop.position.set(0.28 + Math.cos(a) * r, 1.55 + (i % 5) * 0.13, 0.72 + Math.sin(a) * r);
    water.add(drop);
  }
  scene.add(water); water.visible = false;
  camera.position.set(0.2, 4.3, 13.6); camera.lookAt(0, 1.55, 0.1);
  return { stage: st, scene, camera, hero, mom, cup, water };
}
function drawKitchen(s, t, info, id) {
  const p = smooth(t / 4.5), frozen = id >= 's015' && id <= 's021';
  s.hero.position.set(-3.1, 0, 1.65); s.mom.position.set(3.35, 0, 1.6);
  s.hero.rotation.set(0, 0, 0); s.mom.rotation.set(0, 0, 0);
  s.cup.position.set(0.28, 1.04, 0.72); s.cup.rotation.set(0, 0, 0);
  s.water.visible = frozen;
  s.hero.userData.setPose('stand', t); s.mom.userData.setPose('stand', t);
  if (id === 's013') {
    s.hero.userData.setPose('reach', t); setCamera(s, [1.4, 2.65, 7.3], [0.2, 1.3, 0.65], 31, t);
  } else if (id === 's014') {
    s.cup.position.x = lerp(0.28, 0.72, p); s.cup.rotation.z = -0.48 * p;
    s.hero.userData.setPose('reach', t); s.hero.rotation.z = -0.07 * p;
    setCamera(s, [0.55, 2.6, 7.1], [0.25, 1.25, 0.65], 32, t);
  } else if (id === 's015') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.userData.setPose('point', t); setCamera(s, [0.2, 4.1, 13.4], [0, 1.55, 0.6], 37, t);
  } else if (id === 's016') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.userData.setPose('stand', t); s.mom.userData.setPose('stand', t);
    setCamera(s, [0.1, 3.8, 12.9], [0.2, 1.55, 0.7], 38, t);
  } else if (id === 's017') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.position.x = lerp(-3.1, -0.6, p); s.hero.userData.setPose('walk', t * 0.85);
    setCamera(s, [-0.5, 2.9, 9.5], [-0.5, 1.3, 0.7], 35, t);
  } else if (id === 's018') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    // Keep the protagonist and suspended cup inside frame while the countdown HUD remains readable.
    s.hero.position.x = -1.7; s.hero.userData.setPose('point', t);
    setCamera(s, [-0.6, 2.95, 8.0], [-0.1, 1.42, 0.72], 34, t);
  } else if (id === 's019') {
    s.cup.position.set(0.28, 1.56, 0.72); s.cup.rotation.z = 0;
    s.hero.position.x = -0.5; s.hero.userData.setPose('reach', t);
    setCamera(s, [0.25, 2.35, 6.4], [0.05, 1.42, 0.72], 30, t);
  } else if (id === 's020') {
    s.cup.position.set(0.28, 1.56, 0.72);
    s.mom.userData.setPose('stand', t); s.hero.visible = true;
    setCamera(s, [4.1, 2.75, 6.8], [2.35, 1.35, 1.0], 30, t);
  } else if (id === 's021') {
    s.cup.position.set(0.28, 1.56, 0.72);
    s.hero.userData.setPose('point', t); setCamera(s, [-2.45, 2.5, 6.4], [-2.55, 1.4, 1.1], 31, t);
  } else if (id === 's022') {
    s.cup.position.set(0.28, 1.04, 0.72); s.cup.rotation.z = -0.05 * (1 - p);
    s.water.visible = false; s.mom.userData.setPose('point', t);
    s.hero.position.x = -2.8; s.hero.userData.setPose('stand', t);
    setCamera(s, [0.2, 3.8, 13.2], [0, 1.5, 0.6], 38, t);
  }
}

// -----------------------------------------------------------------------------
// SEQUENCE B — outdoor school court, a ball runs towards the road
function makeBasketball() {
  const st = stage('dusk', { fog: [38, 130], fov: 36, ambient: 1.5 });
  const scene = st.scene, camera = st.camera;
  scene.add(T3.ground(42, 32, '#263342'));
  scene.add(T3.ground(14, 15, '#79513e', { y: 0.035 }));
  // A compact court has a clearly readable end line; the asphalt access road sits immediately beyond it.
  const road = T3.ground(7, 15, '#171c25', { y: 0.025 });
  road.position.set(10.05, 0.025, 0); scene.add(road);
  scene.add(T3.box(0.08, 0.025, 15, '#e7d8ad', { x: 6.95, y: 0.075 }));
  for (let z = -6; z <= 6; z += 3) scene.add(T3.box(0.12, 0.025, 0.8, '#d7caa4', { x: 10.05, y: 0.075, z }));
  // Painted court markings and the centre circle.
  const line = std('#e8c99b', { roughness: 0.6 });
  for (const z of [-5.6, 5.6]) scene.add(T3.box(14, 0.025, 0.055, '#e8c99b', { y: 0.065, z }));
  for (const x of [-6.8, 6.8]) scene.add(T3.box(0.055, 0.025, 11.2, '#e8c99b', { x, y: 0.065 }));
  const circle = new THREE.Mesh(new THREE.TorusGeometry(1.45, 0.035, 8, 48), line);
  circle.rotation.x = -Math.PI / 2; circle.position.y = 0.07; scene.add(circle);
  // Chain-link fence, posts, and a real hoop silhouette.
  for (let x = -10; x <= 10; x += 2.5) {
    scene.add(T3.cyl(0.055, 0.055, 4.1, '#303a48', { x, y: 2.05, z: -7.2 }));
  }
  scene.add(T3.box(22, 0.075, 0.09, '#3b4655', { y: 3.6, z: -7.2 }));
  scene.add(T3.box(22, 0.055, 0.06, '#3b4655', { y: 1.3, z: -7.2 }));
  const hoop = new THREE.Group();
  hoop.add(T3.cyl(0.09, 0.12, 4.2, '#303947', { x: -5.7, y: 2.1, z: -5.8 }));
  hoop.add(T3.box(1.7, 1.12, 0.14, '#d9dce1', { x: -6.35, y: 3.75, z: -5.8 }));
  hoop.add(T3.pane(1.36, 0.82, '#8fa8b7', { x: -6.35, y: 3.75, z: -5.69 }));
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.045, 8, 32), std('#e56f48', { metalness: 0.35 }));
  ring.rotation.x = Math.PI / 2; ring.position.set(-6.35, 3.1, -5.2); hoop.add(ring); scene.add(hoop);
  scene.add(T3.lamp({ x: -7.5, z: 0, mood: 'dusk', color: '#ffc77a', intensity: 6 }));
  scene.add(T3.building(6, 8, 4, { x: -14, z: -12, mood: 'dusk', seed: 31, litChance: 0.5 }));
  scene.add(T3.building(8, 10, 4, { x: 14, z: -13, mood: 'dusk', seed: 19, litChance: 0.55 }));
  const bench = T3.box(3.0, 0.18, 0.55, '#76513c', { x: -4.4, y: 0.72, z: 4.4 }); scene.add(bench);
  const hero = addPerson('#3c7186', 'dusk', 1.05);
  const friend = addPerson('#bd9861', 'dusk', 1.02, 'cap');
  hero.position.set(-3.3, 0, 1.0); friend.position.set(2.0, 0, 0.5);
  scene.add(hero, friend);
  const ball = new THREE.Group(), orange = std('#e17a32', { roughness: 0.64 });
  ball.add(new THREE.Mesh(new THREE.SphereGeometry(0.25, 24, 18), orange));
  for (let i = 0; i < 3; i++) {
    const seam = new THREE.Mesh(new THREE.TorusGeometry(0.252, 0.009, 6, 32), std('#30252a'));
    seam.rotation.set(i * 0.8, i * 0.9, i * 0.5); ball.add(seam);
  }
  ball.position.set(2.8, 0.3, 1.1); scene.add(ball);
  const dust = new THREE.Group();
  for (let i = 0; i < 18; i++) {
    const bit = new THREE.Mesh(new THREE.SphereGeometry(0.025 + (i % 3) * 0.012, 8, 6),
      std('#b8d9ef', { transparent: true, opacity: 0.7 }));
    bit.position.set(3.8 + Math.sin(i * 2.4) * 0.45, 0.45 + (i % 5) * 0.18, 1.1 + Math.cos(i * 1.7) * 0.55);
    dust.add(bit);
  }
  scene.add(dust); dust.visible = false;
  camera.position.set(0, 4.3, 15); camera.lookAt(0, 1.3, 0);
  return { stage: st, scene, camera, hero, friend, ball, dust };
}
function drawBasketball(s, t, info, id) {
  const p = smooth(t / 4.5), frozen = id >= 's028' && id <= 's032';
  s.hero.visible = true; s.friend.visible = true; s.ball.visible = true;
  s.hero.position.set(-3.3, 0, 1.0); s.friend.position.set(2.0, 0, 0.5);
  s.hero.rotation.set(0, 0, 0); s.friend.rotation.set(0, 0, 0);
  s.ball.position.set(2.8, 0.3, 1.1); s.ball.rotation.set(0, 0, 0); s.dust.visible = frozen;
  s.hero.userData.setPose('stand', t); s.friend.userData.setPose('stand', t);
  if (id === 's026') {
    const drop = smooth(clamp(p * 1.25));
    // Align the ball's first frame with the friend's outstretched right hand before it drops and rolls to the road.
    s.friend.position.z = 0.9;
    s.ball.position.set(lerp(2.6, 7.45, p), lerp(1.47, 0.3, drop) + (p > 0.18 ? Math.abs(Math.sin((p - 0.18) * Math.PI * 2.5)) * 0.16 : 0), 1.1);
    s.ball.rotation.z = -p * 8;
    s.friend.userData.setPose('reach', t); s.hero.userData.setPose('point', t);
    setCamera(s, [0.7, 4.0, 13.4], [1.8, 1.2, 0.5], 37, t);
  } else if (id === 's027') {
    s.hero.position.x = -0.25; s.hero.userData.setPose('point', t);
    s.ball.position.set(7.45, 0.3, 1.1);
    setCamera(s, [7.45, 2.1, 5.8], [7.45, 0.38, 1.1], 26, t);
  } else if (id === 's028') {
    s.ball.position.set(7.45, 1.0, 1.1); s.hero.userData.setPose('point', t);
    setCamera(s, [2.2, 4.2, 13.8], [2.7, 1.4, 0.2], 37, t);
  } else if (id === 's029') {
    const cx = lerp(-0.8, 4.4, p);
    s.hero.position.x = lerp(-3.8, 6.1, p); s.hero.userData.setPose('run', t * 1.1);
    s.ball.position.set(7.45, 1.0, 1.1);
    setCamera(s, [cx, 3.1, 10.8], [cx + 0.5, 1.15, 0.9], 35, t);
  } else if (id === 's030') {
    s.hero.position.x = 6.15; s.hero.userData.setPose('crouch', t);
    s.ball.position.set(6.45, 1.18, 1.15); setCamera(s, [5.95, 2.6, 7.0], [6.1, 1.0, 1.0], 31, t);
  } else if (id === 's031') {
    s.hero.position.x = 5.85; s.hero.userData.setPose('point', t);
    s.ball.position.set(6.1, 1.25, 1.15); setCamera(s, [5.35, 2.65, 6.3], [5.8, 1.35, 1.0], 30, t);
  } else if (id === 's032') {
    s.hero.position.x = 2.9; s.hero.userData.setPose('reach', t);
    s.friend.position.x = 5.0; s.friend.rotation.y = Math.PI; s.friend.userData.setPose('carry', t);
    s.ball.position.set(3.9, 1.45, 0.95); setCamera(s, [3.2, 3.2, 10.2], [4.0, 1.35, 0.8], 34, t);
  } else if (id === 's033') {
    s.hero.position.x = -1.4; s.friend.position.x = 2.4; s.friend.rotation.y = Math.PI;
    s.friend.userData.setPose('carry', t); s.ball.position.set(2.05, 1.45, 0.95);
    setCamera(s, [0.25, 3.9, 13.2], [0.4, 1.3, 0.5], 37, t);
  }
}

// -----------------------------------------------------------------------------
// SEQUENCE C — deep school corridor; falling books and a fast rescue
function makeHallway() {
  const st = stage('interiorCool', { fog: [24, 100], fov: 35, ambient: 1.7, keyIntensity: 1.55 });
  const scene = st.scene, camera = st.camera;
  scene.add(T3.ground(12, 32, '#303342'));
  scene.add(T3.box(0.26, 5.2, 31, '#343746', { x: -5.9, y: 2.6 }));
  scene.add(T3.box(0.26, 5.2, 31, '#343746', { x: 5.9, y: 2.6 }));
  scene.add(T3.box(12, 0.22, 0.28, '#212634', { y: 0.1, z: -15.3 }));
  // A long vanishing-point corridor with repeating lockers, vents and ceiling panels.
  for (let side of [-1, 1]) {
    for (let i = 0; i < 7; i++) {
      const z = 11 - i * 3.8, x = side * 5.55;
      scene.add(T3.box(0.22, 2.65, 3.25, '#536071', { x, y: 1.38, z }));
      for (let k = 0; k < 3; k++) {
        scene.add(T3.box(0.06, 0.72, 0.045, '#8393a4', { x: side * 5.40, y: 0.65 + k * 0.83, z: z - 0.7 }));
      }
      scene.add(T3.box(0.045, 0.12, 0.045, '#d0b88f', { x: side * 5.38, y: 1.35, z: z + 0.95 }));
    }
  }
  for (let z = 10; z >= -12; z -= 5.5) {
    scene.add(T3.box(1.1, 0.10, 0.55, '#d3dce4', { y: 4.9, z }));
    const glow = T3.sprite('#d6e9ff', 3.3, 0.18); glow.position.set(0, 4.55, z); scene.add(glow);
  }
  scene.add(T3.box(2.4, 3.0, 0.18, '#182434', { x: 0, y: 1.5, z: -15.0 }));
  scene.add(T3.pane(2.0, 2.65, '#536b81', { x: 0, y: 1.55, z: -14.88 }));
  const hero = addPerson('#3c7186', 'interiorCool', 1.03);
  const child = addPerson('#d2d9dc', 'interiorCool', 0.82, 'cap');
  hero.position.set(-2.6, 0, 3.1); child.position.set(2.0, 0, -0.8);
  scene.add(hero, child);
  const books = new THREE.Group(), bookMats = ['#a65e62', '#c99b55', '#527995', '#d7d1c5', '#7b638e'];
  for (let i = 0; i < 6; i++) {
    const root = new THREE.Group();
    root.add(T3.box(0.52, 0.13, 0.72, bookMats[i % bookMats.length], { y: 0.065 }));
    root.add(T3.box(0.46, 0.035, 0.66, '#e8e4d8', { y: 0.147 }));
    root.rotation.z = (i % 2 ? 1 : -1) * 0.08; root.position.set(1.9 + (i % 3) * 0.14, 1.35 + Math.floor(i / 3) * 0.24, -0.7 + (i % 2) * 0.25);
    books.add(root);
  }
  scene.add(books);
  camera.position.set(0.2, 3.2, 13.8); camera.lookAt(0, 1.35, -0.4);
  return { stage: st, scene, camera, hero, child, books };
}
function drawHallway(s, t, info, id) {
  const p = smooth(t / 4.5), frozen = id >= 's038' && id <= 's041';
  s.hero.visible = true; s.child.visible = true; s.books.visible = true;
  s.hero.position.set(-2.6, 0, 3.1); s.child.position.set(2.0, 0, -0.8);
  s.hero.userData.setPose('stand', t); s.child.userData.setPose('kneel', t);
  s.books.children.forEach((book, i) => {
    book.position.set(1.9 + (i % 3) * 0.14, 1.35 + Math.floor(i / 3) * 0.24 - (id === 's037' ? p * (1.0 + i * 0.04) : 0),
      -0.7 + (i % 2) * 0.25);
  });
  if (id === 's037') {
    s.child.userData.setPose('kneel', t); s.hero.userData.setPose('reach', t);
    setCamera(s, [1.4, 2.7, 8.8], [0.8, 1.3, -0.1], 32, t);
  } else if (id === 's038') {
    s.hero.userData.setPose('stand', t); s.child.userData.setPose('kneel', t);
    s.books.children.forEach((book, i) => { book.position.y = 1.9 + Math.floor(i / 3) * 0.28; });
    setCamera(s, [0.1, 3.3, 13.6], [0, 1.35, -0.3], 36, t);
  } else if (id === 's039') {
    s.hero.position.z = lerp(4.5, -0.15, p); s.hero.position.x = lerp(-2.8, 0.9, p);
    s.hero.userData.setPose('run', t * 1.15);
    s.books.children.forEach((book, i) => { book.position.y = 1.9 + Math.floor(i / 3) * 0.28; });
    setCamera(s, [0.2, 2.8, 10.0], [0.5, 1.3, -0.5], 34, t);
  } else if (id === 's040') {
    s.hero.position.set(0.75, 0, -0.1); s.hero.userData.setPose('kneel', t);
    s.child.userData.setPose('reach', t);
    s.books.children.forEach((book, i) => {
      const targetX = 1.92 + (i % 2) * 0.38;
      const targetY = 0.90 + Math.floor(i / 2) * 0.145;
      const targetZ = -0.42 + (i % 3) * 0.035;
      const startX = 0.85 + (i % 2) * 0.12, startY = 0.45 + Math.floor(i / 2) * 0.16;
      const startZ = -0.3 + (i % 3) * 0.12;
      book.position.set(lerp(startX, targetX, p), lerp(startY, targetY, p), lerp(startZ, targetZ, p));
      book.rotation.z = lerp(-0.04, 0.015, p);
    });
    setCamera(s, [1.7, 2.35, 6.8], [1.35, 1.2, -0.35], 30, t);
  } else if (id === 's041') {
    s.hero.position.set(-0.2, 0, 0.2); s.hero.userData.setPose('stand', t);
    s.child.position.set(1.7, 0, -0.6); s.child.userData.setPose('carry', t);
    s.books.children.forEach((book, i) => {
      book.position.set(1.92 + (i % 2) * 0.38, 0.90 + Math.floor(i / 2) * 0.145, -0.42 + (i % 3) * 0.035);
    });
    setCamera(s, [0.2, 2.9, 10.5], [0.9, 1.35, -0.4], 34, t);
  } else if (id === 's042') {
    s.hero.position.set(-2.4, 0, 2.3); s.child.position.set(1.7, 0, -0.6);
    s.child.userData.setPose('carry', t); s.hero.userData.setPose('stand', t);
    s.books.children.forEach((book, i) => {
      book.position.set(1.92 + (i % 2) * 0.38, 0.90 + Math.floor(i / 2) * 0.145, -0.42 + (i % 3) * 0.035);
    });
    setCamera(s, [0.1, 3.4, 12.8], [0.5, 1.3, 0], 37, t);
  }
}

const kitchenIds = ['s013','s014','s015','s016','s017','s018','s019','s020','s021','s022'];
const kitchenFreeze = new Set(['s015','s016','s017','s018','s019','s020','s021']);
kitchenIds.forEach((id) => install(id, makeKitchen, drawKitchen, kitchenFreeze.has(id)));
const courtIds = ['s026','s027','s028','s029','s030','s031','s032','s033'];
const courtFreeze = new Set(['s028','s029','s030','s031','s032']);
courtIds.forEach((id) => install(id, makeBasketball, drawBasketball, courtFreeze.has(id)));
const hallwayIds = ['s037','s038','s039','s040','s041','s042'];
const hallwayFreeze = new Set(['s038','s039','s040','s041']);
hallwayIds.forEach((id) => install(id, makeHallway, drawHallway, hallwayFreeze.has(id)));
