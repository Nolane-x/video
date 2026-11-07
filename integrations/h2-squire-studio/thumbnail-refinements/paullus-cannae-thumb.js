import { thumb } from '/packs/squire/pack.js';

thumb({
  bg: 'plain',
  time: 'golden',
  bgOpts: { trees: 4, bushes: 4, flags: true, clouds: 2 },
  blur: 11,
  back: [
    { preset: 'latin', rows: 3, cols: 18, x0: 0.02, x1: 0.98, yFront: 0.80, yBack: 0.65, hFront: 0.12, hBack: 0.07, flip: true },
    { preset: 'hastatus', rows: 2, cols: 10, x0: 0.06, x1: 0.94, yFront: 0.67, yBack: 0.56, hFront: 0.10, hBack: 0.06 }
  ],
  mid: [
    { preset: 'hastatus', rows: 2, cols: 8, x0: 0.02, x1: 0.36, yFront: 0.79, yBack: 0.69, hFront: 0.14, hBack: 0.08, flip: true },
    { preset: 'latin', rows: 2, cols: 8, x0: 0.63, x1: 0.98, yFront: 0.79, yBack: 0.69, hFront: 0.14, hBack: 0.08 }
  ],
  hero: { preset: 'consul', x: 0.68, y: 0.69, R: 0.16, face: 'scared', pose: 'guard', shield: null },
  symbols: [
    { kind: 'arrow', x: 0.21, y: 0.58, to: [0.49, 0.58], color: '#3e64a3', r: 0.12 },
    { kind: 'q', x: 0.13, y: 0.43, r: 0.085, glow: true }
  ],
  title: [
    { text: "HANNIBAL'S", x: 0.39, y: 0.11, size: 0.055, color: '#fff4df' },
    { text: 'TRAP', x: 0.39, y: 0.225, size: 0.115, color: '#fff4df' }
  ],
  tx: 0.39,
  ty: 0.14,
  tsize: 0.09,
  align: 'center'
});
