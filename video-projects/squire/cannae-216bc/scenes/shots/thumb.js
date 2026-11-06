import { thumb } from '/packs/squire/pack.js';

// Cannae long-form thumbnail: show the enclosure immediately; one-word title.
thumb({
  split: { left: '#9f4037', right: '#3e5e82', slant: -0.05 },
  heroes: [
    {
      preset: 'hastatus',
      x: 0.28, y: 0.58, R: 0.245,
      face: 'shock', pose: 'guard', weapon: 'pilum',
      shield: { type: 'scutum', color: '#9f4037', charge: 'eagle', chargeColor: '#d7c39b' }
    },
    {
      preset: 'latin',
      x: 0.73, y: 0.58, R: 0.245,
      face: 'determined', pose: 'point', weapon: 'spear', flip: true,
      shield: { type: 'round', color: '#3e5e82', charge: 'sun', chargeColor: '#e6d2a8' }
    }
  ],
  symbols: [
    { kind: 'arrow', x: 0.48, y: 0.38, to: [0.56, 0.52], r: 0.16, color: '#f0d7a3' },
    { kind: 'arrow', x: 0.52, y: 0.68, to: [0.58, 0.55], r: 0.16, color: '#f0d7a3' }
  ],
  title: ['SURROUNDED'],
  tx: 0.5, ty: 0.12, tsize: 0.19,
});
