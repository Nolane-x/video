import { thumb } from '/packs/squire/pack.js';

// Cannae long-form thumbnail: one trapped Roman hero, distant Carthaginian wings, one clear phrase.
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
    x: 0.76, y: 0.61, R: 0.255,
    face: 'shock', pose: 'guard', weapon: 'pilum',
    shield: { type: 'scutum', color: '#9f4037', charge: 'eagle', chargeColor: '#d7c39b' }
  },
  symbols: [
    { kind: 'arrow', x: 0.22, y: 0.52, to: [0.48, 0.52], r: 0.16, color: '#d94736' },
    { kind: 'arrow', x: 0.48, y: 0.77, to: [0.64, 0.66], r: 0.14, color: '#d94736' }
  ],
  title: ['NO', 'ESCAPE'],
  tx: 0.06, ty: 0.12, tsize: 0.16, tgap: 0.17, align: 'left',
});
