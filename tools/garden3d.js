/* 3D garden for the "حديقتي" tab (three.js, bundled by build.mjs with esbuild into www/garden3d.js).
   The page component publishes its state in window.__gdData and fires "gd-sync"; taps are sent back via window.__gdApi.water(i).
   If WebGL is not available the page keeps showing the flat 2D grid (window.__g3d stays unset). */
import * as THREE from './three.module.js';

const COLS = 4, ROWS = 4, SP = 1.0;                   // plot grid
const PET_AT = [3, 6, 10, 15, 22];                     // blooms needed per visitor (same as the 2D list)
const C = { green: '#4CAF50', lgreen: '#7ED957', dgreen: '#2E7D32', brown: '#8B5A2B', soil: '#7A4B2A', white: '#FFFFFF' };
const mats = {};
const M = (c, o) => { const k = c + (o ? JSON.stringify(o) : ''); return mats[k] || (mats[k] = new THREE.MeshLambertMaterial(Object.assign({ color: c, flatShading: true }, o || {}))); };
const GEO = { sph: new THREE.IcosahedronGeometry(1, 1), sph0: new THREE.IcosahedronGeometry(1, 0), cone: new THREE.ConeGeometry(1, 1, 7), cyl: new THREE.CylinderGeometry(1, 1, 1, 8), oct: new THREE.OctahedronGeometry(1), box: new THREE.BoxGeometry(1, 1, 1), tor: new THREE.TorusGeometry(1, 0.12, 6, 28), circ: new THREE.CircleGeometry(1, 24), ring: new THREE.RingGeometry(0.7, 1, 28) };
function add(parent, g, mat, s, p, r) { const m = new THREE.Mesh(GEO[g], mat); if (s) m.scale.set(s[0], s[1], s[2]); if (p) m.position.set(p[0], p[1], p[2]); if (r) m.rotation.set(r[0], r[1], r[2]); parent.add(m); return m; }
const rnd = (a, b) => a + Math.random() * (b - a);

/* ---------- plants ---------- */
function leaves(body, h, n, col) { for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2 + 0.6; add(body, 'sph', M(col || C.green), [0.17, 0.035, 0.07], [Math.cos(a) * 0.12, h, Math.sin(a) * 0.12], [0, -a, 0.35]); } }
function flower(o) {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  const H = o.h || 0.85; add(body, 'cyl', M(C.green), [0.035, H, 0.035], [0, H / 2, 0]); leaves(body, H * 0.35, 2); head.position.y = H;
  if (o.cup) { for (let i = 0; i < 5; i++) { const a = (i / 5) * Math.PI * 2; add(head, 'sph', M(o.petal), [0.075, 0.2, 0.09], [Math.cos(a) * 0.075, 0.13, Math.sin(a) * 0.075], [Math.sin(a) * 0.35, -a, -Math.cos(a) * 0.35]); } }
  else if (o.rose) { add(head, 'sph', M(o.petal), [0.2, 0.15, 0.2], [0, 0.04, 0]); add(head, 'sph', M(o.center), [0.13, 0.13, 0.13], [0, 0.1, 0]); for (let i = 0; i < 5; i++) { const a = (i / 5) * Math.PI * 2; add(head, 'sph', M(o.petal), [0.11, 0.1, 0.07], [Math.cos(a) * 0.15, 0.04, Math.sin(a) * 0.15], [0, -a, 0.5]); } }
  else { const n = o.n || 8, L = o.len || 0.2; add(head, 'sph', M(o.center), [o.cr || 0.13, o.cr ? o.cr * 0.5 : 0.07, o.cr || 0.13], [0, 0.03, 0]); for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2; add(head, 'sph', M(o.petal), [L, 0.035, L * 0.45], [Math.cos(a) * (L + 0.04), 0.02, Math.sin(a) * (L + 0.04)], [0, -a, 0.08]); } head.rotation.x = o.tilt || 0.25; }
  return { g, body, head };
}
function tree(o) {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  const T = o.trunk || 0.55; add(body, 'cyl', M(C.brown), [0.08, T, 0.08], [0, T / 2, 0]); head.position.y = T;
  const cs = o.canopy; [[0, 0.3, 0, 0.36], [0.2, 0.18, 0.08, 0.26], [-0.2, 0.2, -0.05, 0.27], [0.02, 0.2, -0.2, 0.25]].forEach((p, i) => add(head, 'sph', M(cs[i % cs.length]), [p[3], p[3] * 0.92, p[3]], [p[0], p[1], p[2]]));
  if (o.fruit) for (let i = 0; i < (o.fn || 6); i++) { const a = i * 2.1, r = 0.3; add(head, 'sph', M(o.fruit), [0.06, 0.06, 0.06], [Math.cos(a) * r * 0.9, 0.18 + (i % 3) * 0.1, Math.sin(a) * r * 0.9]); }
  return { g, body, head };
}
function pine() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'cyl', M(C.brown), [0.07, 0.35, 0.07], [0, 0.17, 0]); head.position.y = 0.3;
  [[0.38, 0.45, 0], [0.3, 0.4, 0.28], [0.22, 0.36, 0.52]].forEach((c, i) => add(head, 'cone', M(i % 2 ? '#2E8B57' : '#1F7A4A'), [c[0], c[1], c[0]], [0, c[2] + c[1] / 2 + 0.06, 0]));
  return { g, body, head };
}
function palm() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  for (let i = 0; i < 4; i++) add(body, 'cyl', M(i % 2 ? '#A9743E' : '#8B5A2B'), [0.07 - i * 0.008, 0.22, 0.07 - i * 0.008], [i * 0.035, 0.11 + i * 0.2, 0], [0, 0, -0.08 * i * 0.6]);
  head.position.set(0.12, 0.85, 0);
  for (let i = 0; i < 7; i++) { const a = (i / 7) * Math.PI * 2; add(head, 'cone', M(i % 2 ? C.green : C.lgreen), [0.07, 0.6, 0.02], [Math.cos(a) * 0.28, 0.0, Math.sin(a) * 0.28], [Math.sin(a) * 1.25, 0, -Math.cos(a) * 1.25]); }
  add(head, 'sph', M('#6B4423'), [0.08, 0.08, 0.08], [0.05, -0.05, 0.05]); add(head, 'sph', M('#6B4423'), [0.08, 0.08, 0.08], [-0.06, -0.06, 0]);
  return { g, body, head };
}
function cactus(o) {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'cyl', M('#3E9B4F'), [0.16, 0.6, 0.16], [0, 0.3, 0]); add(body, 'sph', M('#3E9B4F'), [0.16, 0.16, 0.16], [0, 0.6, 0]);
  add(body, 'cyl', M('#3E9B4F'), [0.07, 0.2, 0.07], [0.22, 0.34, 0], [0, 0, 0]); add(body, 'cyl', M('#3E9B4F'), [0.07, 0.14, 0.07], [0.15, 0.25, 0], [0, 0, 1.57]); add(body, 'sph', M('#3E9B4F'), [0.07, 0.07, 0.07], [0.22, 0.45, 0]);
  add(body, 'cyl', M('#3E9B4F'), [0.07, 0.16, 0.07], [-0.22, 0.28, 0]); add(body, 'cyl', M('#3E9B4F'), [0.07, 0.14, 0.07], [-0.15, 0.2, 0], [0, 0, 1.57]); add(body, 'sph', M('#3E9B4F'), [0.07, 0.07, 0.07], [-0.22, 0.38, 0]);
  head.position.y = 0.72; for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; add(head, 'sph', M(o.flower), [0.08, 0.03, 0.05], [Math.cos(a) * 0.08, 0.02, Math.sin(a) * 0.08], [0, -a, 0.3]); } add(head, 'sph', M('#FFD54F'), [0.05, 0.05, 0.05], [0, 0.04, 0]);
  return { g, body, head };
}
function carrot() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  for (let i = 0; i < 5; i++) { const a = (i / 5) * Math.PI * 2; add(body, 'cone', M(i % 2 ? C.green : C.lgreen), [0.05, 0.5, 0.03], [Math.cos(a) * 0.07, 0.27, Math.sin(a) * 0.07], [Math.sin(a) * 0.5, 0, -Math.cos(a) * 0.5]); }
  head.position.y = 0.05; add(head, 'cone', M('#FF8F1F'), [0.13, 0.42, 0.13], [0, 0.02, 0], [Math.PI, 0, 0]); add(head, 'cyl', M('#FF8F1F'), [0.13, 0.04, 0.13], [0, 0.22, 0]);
  return { g, body, head };
}
function corn() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'cyl', M(C.green), [0.05, 1.05, 0.05], [0, 0.52, 0]); for (let i = 0; i < 4; i++) { const a = i * 1.57 + 0.4; add(body, 'cone', M(i % 2 ? C.green : C.lgreen), [0.07, 0.55, 0.02], [Math.cos(a) * 0.22, 0.4 + (i % 2) * 0.2, Math.sin(a) * 0.22], [Math.sin(a) * 1.1, 0, -Math.cos(a) * 1.1]); }
  head.position.set(0.12, 0.7, 0); add(head, 'sph', M('#FFD84A'), [0.09, 0.26, 0.09], [0, 0.05, 0]); add(head, 'cone', M(C.lgreen), [0.1, 0.2, 0.1], [0, -0.1, 0], [Math.PI, 0, 0]);
  return { g, body, head };
}
function melon(o) {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  for (let i = 0; i < 4; i++) { const a = i * 1.6; add(body, 'sph', M(C.green), [0.2, 0.03, 0.12], [Math.cos(a) * 0.25, 0.07, Math.sin(a) * 0.25], [0, -a, 0]); }
  const sg = new THREE.IcosahedronGeometry(1, 2), pos = sg.attributes.position, col = []; const c1 = new THREE.Color(o.a), c2 = new THREE.Color(o.b);
  for (let i = 0; i < pos.count; i++) { const ang = Math.atan2(pos.getZ(i), pos.getX(i)); const k = Math.floor(((ang + Math.PI) / (Math.PI * 2)) * 10) % 2 ? c1 : c2; col.push(k.r, k.g, k.b); }
  sg.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); head.position.y = 0.27;
  const m = new THREE.Mesh(sg, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true })); m.scale.set(0.3, 0.26, 0.3); head.add(m);
  return { g, body, head };
}
function bush(o) {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'sph', M(C.green), [0.3, 0.2, 0.3], [0, 0.17, 0]); add(body, 'sph', M(C.lgreen), [0.2, 0.15, 0.2], [0.18, 0.15, 0.08]); add(body, 'sph', M(C.dgreen), [0.2, 0.14, 0.2], [-0.16, 0.14, -0.06]);
  head.position.y = 0.2; for (let i = 0; i < (o.n || 7); i++) { const a = i * 2.4, r = 0.2 + (i % 2) * 0.1; add(head, 'sph', M(o.fruit), [o.r || 0.07, (o.r || 0.07) * (o.tall || 1), o.r || 0.07], [Math.cos(a) * r, 0.04 + (i % 3) * 0.05, Math.sin(a) * r]); }
  return { g, body, head };
}
function grapes() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'cyl', M(C.brown), [0.03, 0.8, 0.03], [0, 0.4, 0]); add(body, 'cyl', M(C.brown), [0.03, 0.5, 0.03], [0.2, 0.75, 0], [0, 0, 1.2]); leaves(body, 0.62, 3, C.lgreen);
  head.position.set(0.1, 0.6, 0); [[0.1, 0.04], [0.08, -0.04], [0.06, -0.12], [0.03, -0.19]].forEach((r, ri) => { const n = ri === 3 ? 1 : 3 - ri % 2 + 1; for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2; add(head, 'sph', M(ri % 2 ? '#7B3FA8' : '#8E4BC2'), [0.065, 0.065, 0.065], [Math.cos(a) * r[0] * 0.7, r[1], Math.sin(a) * r[0] * 0.7]); } });
  return { g, body, head };
}
function clover() {
  const g = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); g.add(body); g.add(head);
  add(body, 'cyl', M(C.green), [0.03, 0.4, 0.03], [0, 0.2, 0]); for (let i = 0; i < 3; i++) { const a = (i / 3) * Math.PI * 2; add(body, 'sph', M(i % 2 ? '#3FB065' : '#58C97B'), [0.15, 0.03, 0.15], [Math.cos(a) * 0.15, 0.4, Math.sin(a) * 0.15]); }
  head.position.set(0.1, 0.5, 0.05); add(head, 'sph', M('#FFFFFF'), [0.07, 0.07, 0.07], [0, 0.02, 0]); for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; add(head, 'sph', M('#FFE1EF'), [0.04, 0.04, 0.04], [Math.cos(a) * 0.08, 0.0, Math.sin(a) * 0.08]); }
  return { g, body, head };
}
const BOY = [() => flower({ petal: '#FFC81F', center: '#6B3E1A', n: 14, len: 0.17, cr: 0.17, h: 0.95, tilt: 0.45 }), () => cactus({ flower: '#FF6FA5' }), () => tree({ canopy: ['#3CAF55', '#4CC465'], trunk: 0.55 }), () => tree({ canopy: ['#3CAF55', '#4CC465'], fruit: '#E53935', fn: 7 }), palm,
  () => flower({ petal: '#F44369', cup: true, h: 0.7 }), clover, pine, () => bush({ fruit: '#E8344E', n: 7, r: 0.075, tall: 1.25 }), carrot, () => melon({ a: '#2E9E4F', b: '#1B6F36' }), corn,
  () => tree({ canopy: ['#3CAF55', '#4CC465'], fruit: '#FF9800', fn: 7 }), grapes, () => tree({ canopy: ['#5BC96B', '#6FD97E'], fruit: '#FFEB3B', fn: 7 }), () => bush({ fruit: '#C2185B', n: 6, r: 0.08 })];
const GIRL = [() => tree({ canopy: ['#FFB7D5', '#FF9EC4', '#FFC9E0'], trunk: 0.5 }), () => flower({ petal: '#FF6FA5', cup: true, h: 0.7 }), () => flower({ petal: '#E0243C', center: '#B3122A', rose: true, h: 0.8 }), () => flower({ petal: '#FF4F8B', center: '#FFD54F', n: 5, len: 0.26, cr: 0.08, h: 0.85, tilt: 0.5 }),
  () => flower({ petal: '#FFFFFF', center: '#FFC107', n: 12, len: 0.16, cr: 0.12, h: 0.75 }), () => flower({ petal: '#FFC81F', center: '#6B3E1A', n: 14, len: 0.17, cr: 0.17, h: 0.95, tilt: 0.45 }), () => bush({ fruit: '#E8344E', n: 7, r: 0.075, tall: 1.25 }), () => bush({ fruit: '#C2185B', n: 6, r: 0.08 }),
  () => tree({ canopy: ['#3CAF55', '#4CC465'], fruit: '#FF9E80', fn: 7 }), grapes, () => tree({ canopy: ['#5BC96B', '#6FD97E'], fruit: '#FFEB3B', fn: 7 }), () => melon({ a: '#2E9E4F', b: '#1B6F36' }), clover, () => tree({ canopy: ['#3CAF55', '#4CC465'], fruit: '#E53935', fn: 7 }), palm, () => tree({ canopy: ['#3CAF55', '#4CC465'], trunk: 0.55 })];

/* ---------- state ---------- */
let renderer, scene, camera, island, cv, ok = false, shown = false, raf = 0, last = 0, sig = '';
let spots = [], pets = [], clouds = [], drops = [], stars = [], rings = [], can = null, sun, moon, starsPts, girlMode = null, yaw = 0, vyaw = 0, pitch = 0.98, dragging = false, idle = 0, curTab = '';
const clock = new THREE.Clock(); const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();

function glowTex() { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d'), g = x.createRadialGradient(32, 32, 0, 32, 32, 32); g.addColorStop(0, 'rgba(255,240,150,.95)'); g.addColorStop(0.4, 'rgba(255,214,90,.35)'); g.addColorStop(1, 'rgba(255,214,90,0)'); x.fillStyle = g; x.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); }

function build() {
  scene = new THREE.Scene(); camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x9bd37a, 2.1)); const dl = new THREE.DirectionalLight(0xfff6e0, 2.6); dl.position.set(4, 9, 6); scene.add(dl);
  island = new THREE.Group(); scene.add(island);
  add(island, 'cyl', M('#7ED957'), [3.15, 0.5, 3.15], [0, -0.25, 0]); add(island, 'cyl', M('#5DBB3F'), [3.19, 0.1, 3.19], [0, 0.0, 0]);
  const under = add(island, 'cone', M('#9B6A43'), [3.0, 3.8, 3.0], [0, -2.4, 0], [Math.PI, 0, 0]); under.geometry = new THREE.ConeGeometry(1, 1, 12);
  add(island, 'cone', M('#B07B4E'), [3.08, 0.9, 3.08], [0, -0.95, 0], [Math.PI, 0, 0]).geometry = new THREE.ConeGeometry(1, 1, 12);
  [[-1.2, -2.4, 0.4, 0.3], [1.1, -3.0, -0.5, 0.24], [0.3, -3.7, 0.8, 0.18]].forEach((r) => add(island, 'sph0', M('#8B5E3C'), [r[3], r[3], r[3]], [r[0], r[1], r[2]]));
  const rail = add(island, 'tor', M('#C98A4B'), [1, 1, 1], [0, 0.5, 0], [Math.PI / 2, 0, 0]); rail.geometry = new THREE.TorusGeometry(2.95, 0.05, 6, 48);
  for (let i = 0; i < 24; i++) { const a = (i / 24) * Math.PI * 2; add(island, 'cyl', M('#B87333'), [0.04, 0.46, 0.04], [Math.cos(a) * 2.95, 0.26, Math.sin(a) * 2.95]); }
  for (let i = 0; i < 46; i++) { const a = rnd(0, 6.28), r = rnd(2.55, 2.85); const x = Math.cos(a) * r, z = Math.sin(a) * r; if (i % 3 === 0) { add(island, 'cyl', M(C.green), [0.015, 0.1, 0.015], [x, 0.08, z]); add(island, 'sph', M(['#FF7EB3', '#FFD54F', '#FFFFFF', '#9C7BFF'][i % 4]), [0.05, 0.05, 0.05], [x, 0.17, z]); } else add(island, 'cone', M(i % 2 ? C.dgreen : C.lgreen), [0.04, 0.18, 0.04], [x, 0.13, z]); }
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    const i = r * COLS + c, x = (c - (COLS - 1) / 2) * SP, z = (r - (ROWS - 1) / 2) * SP + 0.1; const g = new THREE.Group(); g.position.set(x, 0.05, z); island.add(g);
    add(g, 'cyl', M('#6E4423'), [0.46, 0.1, 0.46], [0, 0.03, 0]); add(g, 'cyl', M(C.soil), [0.39, 0.14, 0.39], [0, 0.05, 0]); add(g, 'circ', new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.17, depthWrite: false }), [0.46, 0.46, 0.46], [0, 0.125, 0], [-Math.PI / 2, 0, 0]);
    const ring = add(g, 'ring', new THREE.MeshBasicMaterial({ color: 0xFFD23F, transparent: true, opacity: 0.0, depthWrite: false, side: THREE.DoubleSide }), [0.5, 0.5, 0.5], [0, 0.135, 0], [-Math.PI / 2, 0, 0]);
    const seed = new THREE.Group(); add(seed, 'sph', M('#4A2C12'), [0.12, 0.085, 0.12], [0, 0.17, 0]); add(seed, 'sph', M('#6B3F1D'), [0.06, 0.04, 0.06], [-0.03, 0.22, 0.02]); g.add(seed);
    const sprout = new THREE.Group(); add(sprout, 'cyl', M(C.green), [0.025, 0.22, 0.025], [0, 0.22, 0]); add(sprout, 'sph', M(C.lgreen), [0.13, 0.03, 0.065], [0.09, 0.34, 0], [0, 0, 0.5]); add(sprout, 'sph', M(C.lgreen), [0.13, 0.03, 0.065], [-0.09, 0.34, 0], [0, 0, -0.5]); g.add(sprout);
    const star = add(g, 'oct', new THREE.MeshBasicMaterial({ color: 0xFFD23F }), [0.09, 0.12, 0.09], [0, 1.5, 0]); star.visible = false;
    const hit = add(g, 'cyl', M('#fff'), [0.55, 1.5, 0.55], [0, 0.75, 0]); hit.visible = false; hit.userData.spot = i;
    spots.push({ i, g, seed, sprout, ring, star, hit, plant: null, kind: -1, stage: -1, cur: { body: 0, head: 0, seed: 0, sprout: 0 }, bounce: 0, x, z });
  }
  // sky things
  const gt = glowTex(); sun = new THREE.Group(); sun.position.set(-2.4, 0.9, -5.5); add(sun, 'sph', new THREE.MeshBasicMaterial({ color: 0xFFD23F }), [0.8, 0.8, 0.8]); const gs = new THREE.Sprite(new THREE.SpriteMaterial({ map: gt, blending: THREE.AdditiveBlending, depthWrite: false })); gs.scale.set(4.2, 4.2, 1); sun.add(gs); scene.add(sun);
  moon = new THREE.Group(); moon.position.set(-2.4, 0.9, -5.5); add(moon, 'sph', new THREE.MeshBasicMaterial({ color: 0xFFF3C4 }), [0.7, 0.7, 0.7]); add(moon, 'sph', new THREE.MeshBasicMaterial({ color: 0xE9DCA8 }), [0.14, 0.14, 0.05], [0.2, 0.15, 0.62]); add(moon, 'sph', new THREE.MeshBasicMaterial({ color: 0xE9DCA8 }), [0.1, 0.1, 0.05], [-0.25, -0.2, 0.62]); moon.visible = false; scene.add(moon);
  const sp = []; for (let i = 0; i < 70; i++) sp.push(rnd(-5, 5), rnd(-0.5, 2.8), rnd(-8, -5)); const sgm = new THREE.BufferGeometry(); sgm.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3)); starsPts = new THREE.Points(sgm, new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.2 })); starsPts.visible = false; scene.add(starsPts);
  for (let i = 0; i < 7; i++) { const g = new THREE.Group(), r = rnd(4.2, 7.2), a = rnd(1.15, 1.85) * Math.PI, y = i < 4 ? rnd(2.4, 4.6) : rnd(-3.4, -1.8); [[0, 0, 0, 0.55], [0.55, -0.08, 0.1, 0.42], [-0.55, -0.1, -0.05, 0.4], [0.2, 0.2, 0, 0.42]].forEach((p) => add(g, 'sph', new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true, emissive: 0xffffff, emissiveIntensity: 0.55 }), [p[3] * 1.2, p[3] * 0.8, p[3]], [p[0], p[1], p[2]])); g.userData = { r, a, a0: a, y, sp: rnd(0.12, 0.25), ph: rnd(0, 6.28) }; scene.add(g); clouds.push(g); }
  // can
  can = new THREE.Group(); add(can, 'cyl', M('#3FA9F5'), [0.2, 0.26, 0.2], [0, 0, 0]); add(can, 'cyl', M('#2B86CC'), [0.205, 0.04, 0.205], [0, 0.14, 0]); add(can, 'cyl', M('#3FA9F5'), [0.03, 0.34, 0.03], [0.3, 0.06, 0], [0, 0, -0.9]); add(can, 'cyl', M('#2B86CC'), [0.06, 0.04, 0.06], [0.45, 0.22, 0], [0, 0, -0.9]); add(can, 'tor', M('#FFFFFF'), [0.14, 0.18, 0.14], [-0.24, 0.02, 0], [0, 0, 0]); can.visible = false; can.userData = { t: -1, spot: 0 }; scene.add(can);
  for (let i = 0; i < 48; i++) { const m = add(scene, 'sph', new THREE.MeshBasicMaterial({ color: 0x4FC3F7 }), [0.045, 0.06, 0.045]); m.visible = false; m.userData = { v: new THREE.Vector3(), life: 0 }; drops.push(m); }
  for (let i = 0; i < 40; i++) { const m = add(scene, 'oct', new THREE.MeshBasicMaterial({ color: [0xFFD23F, 0xFF7EB3, 0x7BE0FF, 0xB69CFF][i % 4] }), [1, 1, 1]); m.geometry = new THREE.OctahedronGeometry(0.09); m.visible = false; m.userData = { v: new THREE.Vector3(), life: 0, sp: 0 }; stars.push(m); }
  for (let i = 0; i < 6; i++) { const m = add(scene, 'ring', new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide }), [0.2, 0.2, 0.2], null, [-Math.PI / 2, 0, 0]); m.visible = false; m.userData = { life: 0, c: 0xFFFFFF, big: 1 }; rings.push(m); }
}

function petMesh(kind) {
  const g = new THREE.Group();
  if (kind === 0) { const wm = new THREE.MeshLambertMaterial({ color: 0xFF7EB3, side: THREE.DoubleSide, flatShading: true }), w2 = new THREE.MeshLambertMaterial({ color: 0xFFC94D, side: THREE.DoubleSide, flatShading: true }); const mk = (m, s) => { const sh = new THREE.Mesh(new THREE.CircleGeometry(0.2, 8), m); sh.position.x = 0.2 * s; const pv = new THREE.Group(); pv.add(sh); return pv; }; const l = mk(wm, -1), r = mk(wm, 1); g.add(l, r); add(g, 'sph', M('#4A2C12'), [0.03, 0.03, 0.12]); g.userData = { l, r, kind }; }
  if (kind === 1) { add(g, 'sph', M('#FFD23F'), [0.1, 0.09, 0.14]); add(g, 'sph', M('#222'), [0.102, 0.09, 0.03], [0, 0, 0.02]); add(g, 'sph', M('#222'), [0.102, 0.09, 0.03], [0, 0, -0.06]); const wm = new THREE.MeshLambertMaterial({ color: 0xE9F6FF, side: THREE.DoubleSide, transparent: true, opacity: 0.8 }); const l = new THREE.Group(), r = new THREE.Group(); const a = new THREE.Mesh(new THREE.CircleGeometry(0.1, 8), wm); a.position.x = -0.1; l.add(a); const b = new THREE.Mesh(new THREE.CircleGeometry(0.1, 8), wm); b.position.x = 0.1; r.add(b); l.position.y = r.position.y = 0.09; g.add(l, r); g.userData = { l, r, kind }; }
  if (kind === 2) { add(g, 'sph', M('#5AA9F0'), [0.17, 0.15, 0.26]); add(g, 'sph', M('#5AA9F0'), [0.12, 0.12, 0.12], [0, 0.1, 0.22]); add(g, 'cone', M('#FF9F1C'), [0.04, 0.1, 0.04], [0, 0.09, 0.34], [Math.PI / 2, 0, 0]); add(g, 'cone', M('#3F8DD8'), [0.08, 0.2, 0.03], [0, 0.0, -0.3], [-Math.PI / 2, 0, 0]); const wm = M('#3F8DD8'); const l = new THREE.Group(), r = new THREE.Group(); const a = add(l, 'sph', wm, [0.3, 0.025, 0.14], [-0.3, 0, 0]); const b = add(r, 'sph', wm, [0.3, 0.025, 0.14], [0.3, 0, 0]); l.position.y = r.position.y = 0.04; g.add(l, r); g.userData = { l, r, kind }; }
  if (kind === 3) { add(g, 'sph', M('#E53935'), [0.14, 0.1, 0.17], [0, 0.07, 0]); add(g, 'sph', M('#222'), [0.07, 0.07, 0.07], [0, 0.06, 0.17]); [[0.06, 0.15, 0.03], [-0.06, 0.15, -0.05], [0.05, 0.14, -0.08], [-0.07, 0.13, 0.05]].forEach((p) => add(g, 'sph', M('#222'), [0.025, 0.02, 0.025], p)); g.userData = { kind }; }
  if (kind === 4) { add(g, 'sph', M('#FFFFFF'), [0.17, 0.15, 0.22], [0, 0.17, 0]); add(g, 'sph', M('#FFFFFF'), [0.11, 0.11, 0.11], [0, 0.3, 0.17]); add(g, 'sph', M('#FFFFFF'), [0.035, 0.14, 0.03], [0.045, 0.45, 0.16], [0.2, 0, 0.1]); add(g, 'sph', M('#FFFFFF'), [0.035, 0.14, 0.03], [-0.045, 0.45, 0.16], [0.2, 0, -0.1]); add(g, 'sph', M('#FFB3C7'), [0.02, 0.1, 0.02], [0.045, 0.45, 0.17]); add(g, 'sph', M('#FFB3C7'), [0.02, 0.1, 0.02], [-0.045, 0.45, 0.17]); add(g, 'sph', M('#FFB3C7'), [0.07, 0.07, 0.07], [0, 0.18, -0.22]); add(g, 'sph', M('#222'), [0.02, 0.02, 0.02], [0.05, 0.33, 0.26]); add(g, 'sph', M('#222'), [0.02, 0.02, 0.02], [-0.05, 0.33, 0.26]); g.userData = { kind }; }
  g.scale.setScalar(0.001); return g;
}

/* ---------- plant management ---------- */
function setPlant(s, kind, girl) {
  if (s.plant) { s.g.remove(s.plant.g); s.plant = null; }
  if (kind < 0) return; const b = (girl ? GIRL : BOY)[kind % 16](); s.plant = b; s.g.add(b.g); b.g.position.y = 0.12; b.g.scale.setScalar(1.18); s.kind = kind;
}
function tgt(stage) { return { seed: stage === 0 ? 1 : 0, sprout: stage === 1 ? 1 : 0, body: [0, 0.5, 0.75, 0.95, 1][stage] || 0, head: [0, 0, 0.28, 0.6, 1][stage] || 0 }; }
function ringBurst(x, y, z, col, big) { const r = rings.find((q) => !q.visible); if (!r) return; r.visible = true; r.position.set(x, y, z); r.userData.life = 1; r.userData.big = big || 1; r.material.color.setHex(col); }
function bloomBurst(s, cnt) { const p = new THREE.Vector3(); s.g.getWorldPosition(p); p.y += 0.7; ringBurst(p.x, p.y - 0.55, p.z, 0xFFD23F, 2.4); let n = 0; stars.forEach((m) => { if (n >= (cnt || 18) || m.visible) return; n++; m.visible = true; m.position.copy(p); m.userData.v.set(rnd(-1.4, 1.4), rnd(1.6, 3.2), rnd(-1.4, 1.4)); m.userData.life = 1.3; m.userData.sp = rnd(3, 9); }); }
function pour(s) { can.visible = true; can.userData.t = 0; can.userData.spot = s.i; can.userData.did = false; }

function sync() {
  const d = window.__gdData; if (!d || !ok) return;
  const gd = d.gd || { p: [], bl: 0 }, js = JSON.stringify([gd.p, gd.bl, d.girl, d.tab, d.view]); const wasShown = shown;
  shown = d.view === 'garden'; if (shown && !wasShown) { startLoop(); } if (!shown) stopLoop();
  if (js === sig) return; sig = js;
  const night = d.tab === 'pm'; sun.visible = !night; moon.visible = night; starsPts.visible = night; 
  hemi().color.setHex(night ? 0xB8C3FF : 0xffffff); hemi().intensity = night ? 1.5 : 2.1; dir().color.setHex(night ? 0xA9B8FF : 0xfff6e0); dir().intensity = night ? 1.6 : 2.6;
  girlMode = !!d.girl;
  spots.forEach((s) => {
    const pl = gd.p[s.i];
    if (!pl) { if (s.plant) setPlant(s, -1); s.kind = -1; s.stage = -1; return; }
    const first = s.kind !== pl.k || !s.plant || s.stage < 0; if (first) { const was = s.stage; setPlant(s, pl.k, girlMode); s.stage = -1; s.cur = { body: 0, head: 0, seed: 0, sprout: 0 }; s.bounce = was < 0 && gd._anim !== false ? 1 : 0.0; }
    if (pl.s !== s.stage) { const up = s.stage >= 0 && pl.s > s.stage; if (up) { pour(s); s.pending = pl.s; s.pendT = 0.75; } else { s.stage = pl.s; } if (!up) s.stage = pl.s; }
  });
  PET_AT.forEach((need, k) => { if ((gd.bl || 0) >= need && !pets[k]) { const m = petMesh(k); island.add(m); pets[k] = { m, t: rnd(0, 6), k }; } });
}
let _h, _d; const hemi = () => _h || (_h = scene.children.find((c) => c.isHemisphereLight)); const dir = () => _d || (_d = scene.children.find((c) => c.isDirectionalLight));

/* ---------- frame ---------- */
function frame(t) {
  raf = requestAnimationFrame(frame); const dt = Math.min(0.05, clock.getDelta()), T = clock.elapsedTime;
  // place canvas over #g3dBox
  const box = document.getElementById('g3dBox'); if (!box) { cv.style.display = 'none'; return; }
  const r = box.getBoundingClientRect(); if (r.width < 20 || r.height < 20) { cv.style.display = 'none'; return; }
  cv.style.display = 'block'; const w = Math.round(r.width), h = Math.round(r.height);
  if (cv._w !== w || cv._h !== h || cv._x !== Math.round(r.left) || cv._y !== Math.round(r.top)) { cv._w = w; cv._h = h; cv._x = Math.round(r.left); cv._y = Math.round(r.top); cv.style.left = cv._x + 'px'; cv.style.top = cv._y + 'px'; cv.style.width = w + 'px'; cv.style.height = h + 'px'; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  // camera orbit
  if (!dragging) { yaw += vyaw * dt; vyaw *= Math.pow(0.04, dt); idle += dt; if (idle > 2 && Math.abs(vyaw) < 0.05) yaw += Math.sin(T * 0.3) * 0.0016; }
  const fov = camera.fov * Math.PI / 180, need = 3.55, dist = Math.max(need / (Math.tan(fov / 2) * camera.aspect), 8.2); const cy = Math.sin(pitch) * dist, cz = Math.cos(pitch) * dist;
  camera.position.set(0, cy - 0.4, cz); camera.lookAt(0, -0.45, 0); island.rotation.y = yaw;
    // plants
  spots.forEach((s) => {
    if (s.pending != null) { s.pendT -= dt; if (s.pendT <= 0) { const was = s.stage; s.stage = s.pending; s.pending = null; s.bounce = 1; const P = new THREE.Vector3(); s.g.getWorldPosition(P); ringBurst(P.x, P.y + 0.15, P.z, 0x7BE0FF, 1.2); if (s.stage === 4 && was < 4) bloomBurst(s); } }
    const st = s.stage < 0 ? 0 : s.stage, k = tgt(s.stage < 0 ? 0 : st); const e = Math.min(1, dt * 7);
    ['seed', 'sprout', 'body', 'head'].forEach((n) => { s.cur[n] += (k[n] - s.cur[n]) * e; });
    if (s.stage < 0) { s.cur.seed = 0; }
    s.seed.visible = s.cur.seed > 0.02 && s.kind >= 0; s.seed.scale.setScalar(Math.max(0.001, s.cur.seed)); s.sprout.visible = s.cur.sprout > 0.02; s.sprout.scale.setScalar(Math.max(0.001, s.cur.sprout));
    s.bounce *= Math.pow(0.02, dt); const bn = 1 + Math.sin(T * 22) * 0.18 * s.bounce;
    if (s.plant) { const b = s.plant.body, h = s.plant.head; b.visible = s.cur.body > 0.05; h.visible = s.cur.head > 0.05; const bs = Math.max(0.001, s.cur.body); b.scale.set(bs * (s.stage < 3 ? 0.8 : 1), bs * bn, bs * (s.stage < 3 ? 0.8 : 1)); const hs = Math.max(0.001, s.cur.head) * (1 + 0.2 * s.bounce * Math.sin(T * 20)); h.scale.setScalar(hs); if (h._y === undefined) h._y = h.position.y; h.position.y = h._y * bs * bn; s.plant.g.rotation.z = Math.sin(T * 1.7 + s.i) * 0.03 * (s.stage >= 1 ? 1 : 0); s.plant.g.rotation.x = Math.cos(T * 1.3 + s.i * 1.3) * 0.02; }
    const bl = s.stage === 4; s.ring.material.opacity += ((bl ? 0.55 + Math.sin(T * 3 + s.i) * 0.2 : 0) - s.ring.material.opacity) * Math.min(1, dt * 5);
    s.star.visible = bl; if (bl) { s.star.position.y = 1.45 + Math.sin(T * 2.4 + s.i) * 0.07 + (s.plant ? (s.plant.head._y || 0.7) * 0.3 : 0); s.star.rotation.y = T * 2; }
  });
  // watering can
  if (can.visible) { const u = can.userData; u.t += dt; const s = spots[u.spot], P = new THREE.Vector3(); s.g.getWorldPosition(P); const k = Math.min(1, u.t / 0.35), out = u.t > 1.0 ? Math.min(1, (u.t - 1.0) / 0.3) : 0;
    can.position.set(P.x - 0.55, P.y + 1.45 + (1 - k) * 0.6 + out * 0.8, P.z + 0.15); can.rotation.z = -k * 0.75 + out * 0.75; can.rotation.y = 0; const sc = (1 - out) * Math.min(1, u.t * 6); can.scale.setScalar(Math.max(0.001, sc));
    if (u.t > 0.3 && u.t < 0.95) { if (Math.random() < 0.7) { const m = drops.find((q) => !q.visible); if (m) { const sp = new THREE.Vector3(0.52, 0.02, 0).applyEuler(can.rotation).add(can.position); m.visible = true; m.position.copy(sp); m.userData.v.set(0.25 + rnd(0, 0.15), -0.3, rnd(-0.05, 0.05)); m.userData.life = 1; } } }
    if (u.t > 1.35) can.visible = false; }
  drops.forEach((m) => { if (!m.visible) return; const u = m.userData; u.v.y -= 7 * dt; m.position.addScaledVector(u.v, dt); if (m.position.y < 0.16 || (u.life -= dt) < 0) { if (m.position.y < 0.5) ringBurst(m.position.x, 0.17, m.position.z, 0x7BE0FF, 0.5); m.visible = false; } });
  stars.forEach((m) => { if (!m.visible) return; const u = m.userData; u.v.y -= 3.2 * dt; m.position.addScaledVector(u.v, dt); m.rotation.x += u.sp * dt; m.rotation.y += u.sp * dt; u.life -= dt; m.scale.setScalar(Math.max(0.01, u.life / 1.3) * 1.1); if (u.life <= 0) m.visible = false; });
  rings.forEach((m) => { if (!m.visible) return; const u = m.userData; u.life -= dt * 1.6; const k = 1 - u.life; m.scale.setScalar(0.2 + k * 0.9 * u.big); m.material.opacity = Math.max(0, u.life) * 0.8; if (u.life <= 0) m.visible = false; });
  // clouds + sun
  clouds.forEach((c) => { const u = c.userData; u.a = u.a0 + Math.sin(T * u.sp * 0.5 + u.ph) * 0.28; c.position.set(Math.cos(u.a) * u.r, u.y + Math.sin(T * 0.5 + u.r) * 0.1, Math.min(-1.2, Math.sin(u.a) * u.r * 0.7 - 1.5)); });
  sun.rotation.z += dt * 0.2; if (sun.children[1]) sun.children[1].scale.setScalar(4.2 + Math.sin(T * 2) * 0.25);
  // visitors
  pets.forEach((p) => { if (!p) return; p.t += dt; if (p.jump) p.jump = Math.max(0, p.jump - dt * 1.6); const m = p.m, u = m.userData; m.scale.setScalar(Math.min(1, m.scale.x + dt * 2.5) * 1.0 || 0.001); const t = p.t;
    if (p.k === 0) { m.position.set(Math.cos(t * 0.5) * 2.4, 1.2 + Math.sin(t * 1.3) * 0.35, Math.sin(t * 0.8) * 1.9); m.rotation.y = -t * 0.5 + 1.2; u.l.rotation.y = Math.sin(t * 16) * 0.9; u.r.rotation.y = -Math.sin(t * 16) * 0.9; m.rotation.x = 0.4; }
    if (p.k === 1) { const a = t * 0.9; m.position.set(Math.cos(a) * 1.8, 1.05 + Math.sin(t * 3) * 0.12, Math.sin(a) * 1.8); m.rotation.y = -a; u.l.rotation.z = Math.sin(t * 40) * 0.6; u.r.rotation.z = -Math.sin(t * 40) * 0.6; }
    if (p.k === 2) { const a = -t * 0.45; m.position.set(Math.cos(a) * 3.1, 2.3 + Math.sin(t * 0.9) * 0.3, Math.sin(a) * 3.1); m.rotation.y = -a + Math.PI; u.l.rotation.z = Math.sin(t * 6) * 0.5; u.r.rotation.z = -Math.sin(t * 6) * 0.5; }
    if (p.k === 3) { const a = t * 0.22; m.position.set(Math.cos(a) * 2.95, 0.12, Math.sin(a) * 2.95); m.rotation.y = -a + Math.PI; }
    if (p.k === 4) { const a = t * 0.35 + 2, hop = Math.abs(Math.sin(t * 3.2)); m.position.set(Math.cos(a) * 2.7, 0.1 + hop * 0.28, Math.sin(a) * 2.7); m.rotation.y = -a + Math.PI; }
  });
  pets.forEach((p) => { if (p && p.jump) p.m.position.y += Math.sin(p.jump * Math.PI) * 0.55; });
  renderer.render(scene, camera);
}

/* ---------- input ---------- */
function pick(cx, cy) { const r = cv.getBoundingClientRect(); ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); const hits = ray.intersectObjects(spots.map((s) => s.hit), false); if (hits.length) return hits[0].object.userData.spot; return -1; }
function pickPet(cx, cy) { const r = cv.getBoundingClientRect(); ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera); const live = pets.filter(Boolean); const hits = ray.intersectObjects(live.map((p) => p.m), true); if (!hits.length) return -1; let o = hits[0].object; while (o && !live.some((p) => p.m === o)) o = o.parent; const p = live.find((q) => q.m === o); return p ? p.k : -1; }
function petTap(k) { const p = pets[k]; if (!p) return; p.jump = 1; const P = new THREE.Vector3(); p.m.getWorldPosition(P); let n = 0; stars.forEach((m) => { if (n >= 7 || m.visible) return; n++; m.visible = true; m.position.copy(P); m.userData.v.set(rnd(-0.9, 0.9), rnd(1.4, 2.4), rnd(-0.9, 0.9)); m.userData.life = 1.1; m.userData.sp = rnd(3, 9); }); }
function bind() {
  let px = 0, py = 0, sx = 0, sy = 0, t0 = 0, moved = 0, id = null;
  cv.addEventListener('pointerdown', (e) => { id = e.pointerId; try { cv.setPointerCapture(id); } catch (x) {} px = sx = e.clientX; py = sy = e.clientY; t0 = performance.now(); moved = 0; dragging = true; vyaw = 0; idle = 0; });
  cv.addEventListener('pointermove', (e) => { if (!dragging || e.pointerId !== id) return; const dx = e.clientX - px, dy = e.clientY - py; px = e.clientX; py = e.clientY; moved += Math.abs(dx) + Math.abs(dy); yaw += dx * 0.011; vyaw = dx * 0.011 / Math.max(0.016, 1 / 60) * 0.6; pitch = Math.min(1.2, Math.max(0.5, pitch + dy * 0.004)); });
  const up = (e) => { if (e.pointerId !== id) return; dragging = false; id = null; if (moved < 10 && performance.now() - t0 < 500) { const api = window.__gdApi; const pk = pickPet(e.clientX, e.clientY); if (pk >= 0) { petTap(pk); if (api && api.pet) api.pet(pk); return; } const i = pick(e.clientX, e.clientY); if (i >= 0 && spots[i].stage === 4) { spots[i].bounce = 1; bloomBurst(spots[i], 8); } if (api) api.water(i); } };
  cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', (e) => { dragging = false; id = null; });
}

function startLoop() { if (!raf && ok) { clock.getDelta(); raf = requestAnimationFrame(frame); } }
function stopLoop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } cv.style.display = 'none'; }

function init() {
  try {
    cv = document.createElement('canvas'); cv.id = 'g3d'; cv.style.cssText = 'position:fixed;left:0;top:0;width:10px;height:10px;display:none;z-index:6;touch-action:none;border-radius:22px;outline:none'; document.body.appendChild(cv);
    renderer = new THREE.WebGLRenderer({ canvas: cv, alpha: true, antialias: true, powerPreference: 'high-performance' }); renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setClearColor(0x000000, 0);
    build(); bind(); ok = true; window.__g3d = 'ok';
    cv.addEventListener('webglcontextlost', (e) => { e.preventDefault(); ok = false; window.__g3d = ''; stopLoop(); try { window.__tkMain && window.__tkMain.setState({ gdTick: Date.now() }); } catch (x) {} });
    window.addEventListener('gd-sync', sync); document.addEventListener('visibilitychange', () => { if (document.hidden) stopLoop(); else sync(); });
    sig = ''; sync(); try { window.__tkMain && window.__tkMain.setState({ gdTick: Date.now() }); } catch (x) {}
  } catch (e) { try { console.error('garden3d', e); cv && cv.remove(); } catch (x) {} window.__g3d = ''; ok = false; }
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
