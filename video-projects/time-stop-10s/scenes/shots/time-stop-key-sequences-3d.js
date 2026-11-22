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
const addPerson = (color, mood, scale = 1, head = 'none') => T3.figureCinematic({
  top: 'hoodie', color, legs: '#18212d', skin: '#171722', head,
  headColor: color, faceStyle: 'mascot',
}, { mood, s: scale, rim: '#b9dfff', rimOpacity: 0.72 });
function stage(mood, options = {}) {
  const st = T3.stage({ mood, cinematic: true, fog: options.fog || [30, 105], fov: options.fov || 34,
    ambient: options.ambient ?? 0.92, keyIntensity: options.keyIntensity ?? 3.15,
    rimIntensity: options.rimIntensity ?? 1.5, keyPos: options.keyPos || [-8, 12, 9], sun: false });
  st.scene.add(st.camera);
  return st;
}
function setCamera(s, pos, look, fov, t) {
  const p = smooth(t / 4.5);
  // Stronger motivated dolly, lateral parallax and a tiny crane move make the frame breathe.
  const push = 0.78 * p;
  const arc = Math.sin(p * Math.PI) * 0.30;
  s.camera.position.set(pos[0] + arc + Math.sin(t * 0.34) * 0.012,
    pos[1] + 0.13 * p + Math.sin(t * 0.48) * 0.009, pos[2] - push);
  s.camera.lookAt(look[0] + Math.sin(p * Math.PI) * 0.16, look[1] + Math.sin(p * Math.PI) * 0.035, look[2]);
  s.camera.fov = fov; s.camera.updateProjectionMatrix();
}
function overlay(g, t, info, frozen = false) {
  if (frozen) {
    const id = String(info?.shot?.id || 's000');
    const seed = Number(id.slice(1)) || 0;
    const x = E.W * (0.40 + (seed % 5) * 0.035);
    const y = E.H * (0.34 + (seed % 4) * 0.028);
    const pulse = 0.5 + 0.5 * Math.sin(t * 2.1);
    g.save(); g.globalCompositeOperation = 'screen';
    const glow = g.createRadialGradient(x, y, 12, x, y, 470 + pulse * 80);
    glow.addColorStop(0, 'rgba(116,205,255,0.13)');
    glow.addColorStop(0.48, 'rgba(74,155,231,0.055)');
    glow.addColorStop(1, 'rgba(40,95,170,0)');
    g.fillStyle = glow; g.fillRect(0, 0, E.W, E.H);
    // Fine suspended streaks imply air frozen in motion; no repetitive target reticle.
    for (let i = 0; i < 34; i++) {
      const phase = (i * 0.61803398875 + t * (0.025 + (i % 4) * 0.006)) % 1;
      const px = (i * 137.5 + phase * 190) % E.W;
      const py = (i * 83.7 + (i % 7) * 21 + phase * 24) % E.H;
      const len = 12 + (i % 5) * 8;
      g.beginPath(); g.moveTo(px, py); g.lineTo(px + len, py - len * 0.17);
      g.strokeStyle = 'rgba(170,224,255,' + (0.10 + (i % 4) * 0.025) + ')';
      g.lineWidth = i % 5 === 0 ? 2.2 : 1.1; g.stroke();
    }
    for (let i = 0; i < 5; i++) {
      const k = (t * 0.08 + i * 0.19) % 1;
      g.beginPath();
      g.ellipse(x + Math.sin(i * 1.7) * 70, y + Math.cos(i * 1.3) * 42,
        190 + i * 92 + k * 36, 42 + i * 19, -0.22, -0.45 + k * 0.5, 1.55 + k * 0.45);
      g.strokeStyle = 'rgba(154,218,255,' + (0.085 - i * 0.009) + ')';
      g.lineWidth = 1.4; g.stroke();
    }
    g.restore();
  }
  const timer = info?.shot?.args?.hud?.rows?.[0]?.n;
  if (timer !== undefined) {
    g.save(); g.font = '700 24px ' + FONTS.mono; g.textAlign = 'left'; g.textBaseline = 'middle';
    g.fillStyle = 'rgba(5,12,22,0.78)'; g.beginPath(); g.roundRect(72, 166, 238, 52, 12); g.fill();
    g.strokeStyle = 'rgba(135,210,255,0.72)'; g.lineWidth = 1.5; g.stroke();
    g.fillStyle = '#b8e9ff'; g.fillText('GIÂY CÒN  ' + String(timer).padStart(2, '0'), 91, 192);
    g.fillStyle = 'rgba(118,205,255,0.16)'; g.fillRect(91, 207, 198, 2);
    g.fillStyle = '#8bd7ff'; g.fillRect(91, 207, 198 * clamp(Number(timer) / 10), 2);
    g.restore();
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
    const ratio = E.cfg.bars === 'scope' ? 2.39
      : E.cfg.bars === 'wide' ? 2.0
      : typeof E.cfg.bars === 'number' ? E.cfg.bars : 0;
    const bar = !E.vertical && ratio ? Math.max(0, (E.H - E.W / ratio) / 2) : 0;
    const safeBottom = E.H - bar;
    const top = safeBottom - 28 - h;
    g.fillStyle = 'rgba(5,10,18,0.78)'; g.beginPath(); g.roundRect(150, top, E.W - 300, h, 15); g.fill();
    g.fillStyle = 'rgba(120,205,246,0.78)'; g.fillRect(150, top + 9, 3, h - 18);
    g.strokeStyle = 'rgba(150,205,240,0.38)'; g.lineWidth = 1.3; g.stroke();
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
  const pendant = new THREE.Group();
  pendant.add(new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.72, 10), std('#47343a')));
  const shade = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.36, 0.26, 24, 1, true), std('#d5a36f', { metalness: 0.2, roughness: 0.48, side: THREE.DoubleSide }));
  shade.position.y = -0.42; pendant.add(shade);
  const bulb = new THREE.PointLight('#ffc27b', 5.2, 10, 2); bulb.position.y = -0.53; pendant.add(bulb);
  pendant.position.set(0.2, 5.05, 0.7); scene.add(pendant);
  for (let i = 0; i < 4; i++) {
    const jar = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.095, 0.34, 16), std(i % 2 ? '#a7b5a4' : '#c58e72', { roughness: 0.38 }));
    jar.position.set(-7.6 + i * 0.48, 1.98, -5.15); scene.add(jar);
  }
  const hero = addPerson('#3c7186', 'interiorWarm', 1.12);
  const mom = T3.figureCinematic({ top: 'hoodie', color: '#a75b73', legs: '#292331',
    skin: '#171722', faceStyle: 'mascot' },
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
    s.hero.userData.setPose('reach', t); setCamera(s, [1.15, 2.35, 5.55], [0.28, 1.28, 0.70], 28, t);
  } else if (id === 's014') {
    s.cup.position.x = lerp(0.28, 0.72, p); s.cup.rotation.z = -0.48 * p;
    s.hero.userData.setPose('reach', t); s.hero.rotation.z = -0.07 * p;
    setCamera(s, [0.48, 2.25, 5.0], [0.48, 1.38, 0.70], 27, t);
  } else if (id === 's015') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.userData.setPose('point', t); setCamera(s, [-0.35, 3.25, 8.1], [0.48, 1.72, 0.72], 30, t);
  } else if (id === 's016') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.userData.setPose('stand', t); s.mom.userData.setPose('stand', t);
    setCamera(s, [0.1, 3.1, 9.8], [0.2, 1.55, 0.7], 34, t);
  } else if (id === 's017') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    s.hero.position.x = lerp(-3.1, -0.6, p); s.hero.userData.setPose('walk', t * 0.85);
    setCamera(s, [-0.8, 2.55, 7.6], [-0.45, 1.32, 0.7], 31, t);
  } else if (id === 's018') {
    s.cup.position.set(0.65, 1.9, 0.72); s.cup.rotation.z = -0.42;
    // Keep the protagonist and suspended cup inside frame while the countdown HUD remains readable.
    s.hero.position.x = -1.7; s.hero.userData.setPose('point', t);
    setCamera(s, [-0.55, 2.45, 6.5], [-0.1, 1.42, 0.72], 30, t);
  } else if (id === 's019') {
    s.cup.position.set(0.28, 1.56, 0.72); s.cup.rotation.z = 0;
    s.hero.position.x = -0.5; s.hero.userData.setPose('reach', t);
    setCamera(s, [0.15, 2.05, 5.2], [0.05, 1.40, 0.72], 27, t);
  } else if (id === 's020') {
    s.cup.position.set(0.28, 1.56, 0.72);
    s.mom.userData.setPose('stand', t); s.hero.visible = true;
    setCamera(s, [3.85, 2.35, 5.4], [2.65, 1.34, 1.0], 27, t);
  } else if (id === 's021') {
    s.cup.position.set(0.28, 1.56, 0.72);
    s.hero.userData.setPose('point', t); setCamera(s, [-2.35, 2.2, 5.3], [-2.45, 1.42, 1.1], 27, t);
  } else if (id === 's022') {
    s.cup.position.set(0.28, 1.04, 0.72); s.cup.rotation.z = -0.05 * (1 - p);
    s.water.visible = false; s.mom.userData.setPose('point', t);
    s.hero.position.x = -2.8; s.hero.userData.setPose('stand', t);
    setCamera(s, [0.2, 3.35, 10.2], [0.3, 1.5, 0.6], 34, t);
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
  const scoreboard = new THREE.Group();
  scoreboard.add(T3.box(3.2, 1.55, 0.16, '#192538', { y: 4.25, z: -7.0 }));
  scoreboard.add(T3.pane(2.92, 1.28, '#183a50', { y: 4.25, z: -6.89 }));
  const scoreCanvas = document.createElement('canvas'); scoreCanvas.width = 512; scoreCanvas.height = 220;
  const sg = scoreCanvas.getContext('2d');
  sg.fillStyle = '#10283a'; sg.fillRect(0, 0, 512, 220);
  sg.fillStyle = '#9de3ff'; sg.font = '800 44px Arial'; sg.textAlign = 'center'; sg.fillText('HOME  08  :  07  AWAY', 256, 86);
  sg.fillStyle = '#ffd58d'; sg.font = '700 25px Arial'; sg.fillText('00:10  •  COURT CLOCK', 256, 151);
  const scoreTex = new THREE.CanvasTexture(scoreCanvas); scoreTex.colorSpace = THREE.SRGBColorSpace;
  const scoreFace = new THREE.Mesh(new THREE.PlaneGeometry(2.9, 1.24), new THREE.MeshBasicMaterial({ map: scoreTex }));
  scoreFace.position.set(0, 4.25, -6.78); scoreboard.add(scoreFace); scene.add(scoreboard);
  const spectators = T3.crowd({ rows: 2, perRow: 18, width: 17, step: 0.82, rise: 0.66, z0: -10.4, color: '#18202e', seed: 21 });
  spectators.position.y = 0.15; scene.add(spectators);
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
    const travel = smooth(p);
    const drop = smooth(clamp(p / 0.42));
    // Release, gravity arc, first bounce and rolling friction are staged as one continuous trajectory.
    s.friend.position.z = 0.9;
    const x = lerp(2.6, 7.45, travel);
    const bouncePhase = clamp((p - 0.42) / 0.34);
    const bounce = p > 0.42 ? 0.13 * Math.sin(Math.PI * bouncePhase) : 0;
    s.ball.position.set(x, 0.30 + 1.17 * (1 - drop) + bounce, 1.1);
    s.ball.rotation.z = -(x - 2.6) / 0.25;
    s.friend.userData.setPose('reach', t); s.hero.userData.setPose('point', t);
    setCamera(s, [0.9, 3.05, 10.3], [2.0, 1.15, 0.5], 32, t);
  } else if (id === 's027') {
    s.hero.position.x = -0.25; s.hero.userData.setPose('point', t);
    s.ball.position.set(7.45, 0.3, 1.1);
    setCamera(s, [7.45, 2.1, 5.8], [7.45, 0.38, 1.1], 26, t);
  } else if (id === 's028') {
    s.ball.position.set(7.45, 1.0, 1.1); s.hero.userData.setPose('point', t);
    setCamera(s, [2.8, 3.25, 10.2], [3.0, 1.35, 0.7], 33, t);
  } else if (id === 's029') {
    const cx = lerp(-0.8, 4.4, p);
    s.hero.position.x = lerp(-3.8, 6.1, p); s.hero.userData.setPose('run', t * 1.1);
    s.ball.position.set(7.45, 1.0, 1.1);
    setCamera(s, [cx, 2.7, 8.5], [cx + 0.5, 1.15, 0.9], 32, t);
  } else if (id === 's030') {
    s.hero.position.x = 6.15; s.hero.userData.setPose('crouch', t); s.hero.rotation.z = -0.045 * smooth(p);
    s.ball.position.set(6.45 - 0.10 * p, 1.18 - 0.12 * p, 1.15); setCamera(s, [5.95, 2.25, 5.5], [6.1, 1.0, 1.0], 28, t);
  } else if (id === 's031') {
    s.hero.position.x = 5.85; s.hero.userData.setPose('carry', t);
    s.ball.position.set(6.0, 1.12, 1.15); setCamera(s, [5.05, 2.25, 5.2], [5.8, 1.3, 1.0], 27, t);
  } else if (id === 's032') {
    s.hero.position.x = 2.9; s.hero.userData.setPose('reach', t);
    s.friend.position.x = 5.0; s.friend.rotation.y = Math.PI; s.friend.userData.setPose('carry', t);
    s.ball.position.set(3.9, 1.45, 0.95); setCamera(s, [3.25, 2.65, 8.3], [4.0, 1.35, 0.8], 31, t);
  } else if (id === 's033') {
    s.hero.position.x = -1.4; s.friend.position.x = 2.4; s.friend.rotation.y = Math.PI;
    s.friend.userData.setPose('carry', t); s.ball.position.set(2.05, 1.45, 0.95);
    setCamera(s, [0.35, 3.1, 10.5], [0.4, 1.3, 0.5], 34, t);
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
    const glow = T3.sprite('#d6e9ff', 3.3, 0.22); glow.position.set(0, 4.55, z); scene.add(glow);
    const pool = new THREE.PointLight('#b9d7ff', 1.65, 7.5, 2);
    pool.position.set(0, 4.0, z); scene.add(pool);
  }
  for (let i = 0; i < 4; i++) {
    const poster = T3.box(1.05, 1.45, 0.05, i % 2 ? '#7c5960' : '#3f667e',
      { x: i % 2 ? -5.70 : 5.70, y: 3.45, z: 8.4 - i * 3.8 });
    scene.add(poster);
    const pin = T3.sphere(0.055, '#e3ba76', { x: i % 2 ? -5.64 : 5.64, y: 4.08, z: 8.43 - i * 3.8, seg: 10 });
    scene.add(pin);
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
    const baseY = 1.35 + Math.floor(i / 3) * 0.24;
    const fall = id === 's037' ? Math.min(baseY - 0.16, p * p * (1.55 + i * 0.035)) : 0;
    book.position.set(1.9 + (i % 3) * 0.14, baseY - fall, -0.7 + (i % 2) * 0.25);
    book.rotation.z = (i % 2 ? 1 : -1) * (0.08 + (id === 's037' ? Math.sin(p * Math.PI * 1.25 + i * 0.3) * 0.16 : 0));
    book.rotation.x = id === 's037' ? Math.sin(p * Math.PI + i * 0.4) * 0.12 : 0;
  });
  if (id === 's037') {
    s.child.userData.setPose('kneel', t); s.hero.userData.setPose('reach', t);
    setCamera(s, [1.3, 2.35, 7.0], [0.9, 1.25, -0.1], 29, t);
  } else if (id === 's038') {
    s.hero.userData.setPose('stand', t); s.child.userData.setPose('kneel', t);
    s.books.children.forEach((book, i) => { book.position.y = 1.9 + Math.floor(i / 3) * 0.28; });
    setCamera(s, [0.2, 2.85, 10.7], [0.15, 1.4, -0.3], 33, t);
  } else if (id === 's039') {
    s.hero.position.z = lerp(4.5, -0.15, p); s.hero.position.x = lerp(-2.8, 0.9, p);
    s.hero.userData.setPose('run', t * 1.15);
    s.books.children.forEach((book, i) => { book.position.y = 1.9 + Math.floor(i / 3) * 0.28; });
    setCamera(s, [0.25, 2.45, 8.0], [0.65, 1.3, -0.5], 31, t);
  } else if (id === 's040') {
    s.hero.position.set(0.75, 0, -0.1); s.hero.userData.setPose('kneel', t);
    s.child.userData.setPose('reach', t);
    s.books.children.forEach((book, i) => {
      const targetX = 1.92 + (i % 2) * 0.38;
      const targetY = 0.90 + Math.floor(i / 2) * 0.145;
      const targetZ = -0.42 + (i % 3) * 0.035;
      const startX = 0.85 + (i % 2) * 0.12, startY = 0.45 + Math.floor(i / 2) * 0.16;
      const startZ = -0.3 + (i % 3) * 0.12;
      const arc = Math.sin(Math.PI * p) * (0.22 + (i % 3) * 0.045);
      book.position.set(lerp(startX, targetX, p), lerp(startY, targetY, p) + arc, lerp(startZ, targetZ, p));
      book.rotation.z = lerp(-0.16 + (i % 2) * 0.08, 0.015, smooth(p)) + Math.sin(Math.PI * p) * 0.055;
      book.rotation.x = Math.sin(Math.PI * p + i * 0.5) * 0.10 * (1 - p);
    });
    setCamera(s, [1.45, 2.05, 5.4], [1.35, 1.2, -0.35], 27, t);
  } else if (id === 's041') {
    s.hero.position.set(-0.2, 0, 0.2); s.hero.userData.setPose('stand', t);
    s.child.position.set(1.7, 0, -0.6); s.child.userData.setPose('carry', t);
    s.books.children.forEach((book, i) => {
      book.position.set(1.92 + (i % 2) * 0.38, 0.90 + Math.floor(i / 2) * 0.145, -0.42 + (i % 3) * 0.035);
    });
    setCamera(s, [0.35, 2.5, 8.5], [0.9, 1.35, -0.4], 31, t);
  } else if (id === 's042') {
    s.hero.position.set(-2.4, 0, 2.3); s.child.position.set(1.7, 0, -0.6);
    s.child.userData.setPose('carry', t); s.hero.userData.setPose('stand', t);
    s.books.children.forEach((book, i) => {
      book.position.set(1.92 + (i % 2) * 0.38, 0.90 + Math.floor(i / 2) * 0.145, -0.42 + (i % 3) * 0.035);
    });
    setCamera(s, [0.2, 3.0, 10.5], [0.5, 1.3, 0], 34, t);
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
