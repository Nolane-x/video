import { thumb } from '/packs/squire/pack.js';

// Cannae long-form thumbnail v2: the Roman soldier remains fully inside the frame.
thumb({
  bg: 'hills',
  time: 'sunset',
  blur: 8,
  bgOpts: { volcano: false, trees: 3, bushes: 3 },
  back: [
    { preset: 'latinOld', rows: 3, cols: 13, x0: 0.02, x1: 0.43, yFront: 0.88, yBack: 0.7, hFront: 0.18, hBack: 0.09, flip: false },
    { preset: 'latin', rows: 3, cols: 13, x0: 0.57, x1: 0.98, yFront: 0.86, yBack: 0.69, hFront: 0.17, hBack: 0.09, flip: true },
    { preset: 'hastatus', rows: 2, cols: 11, x0: 0.24, x1: 0.78, yFront: 0.96, yBack: 0.84, hFront: 0.14, hBack: 0.08 },
  ],
  hero: {
    preset: 'hastatus',
    x: 0.74, y: 0.64, R: 0.18,
    face: 'shock', pose: 'guard', weapon: 'pilum',
    shield: { type: 'scutum', color: '#9f4037', charge: 'eagle', chargeColor: '#d7c39b' }
  },
  symbols: [
    { kind: 'arrow', x: 0.40, y: 0.68, to: [0.58, 0.65], r: 0.13, color: '#d94736' }
  ],
  title: ['NO', 'ESCAPE'],
  tx: 0.055, ty: 0.13, tsize: 0.145, tgap: 0.155, align: 'left',
});
