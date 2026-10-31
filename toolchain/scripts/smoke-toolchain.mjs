import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';

const modules = [
  'remotion', 'gsap', 'motion', 'three', 'pixi.js', 'typescript',
  '@theatre/core', '@svgdotjs/svg.js', 'roughjs', 'd3',
  'postprocessing', '@resvg/resvg-js', 'sharp', 'playwright'
];
for (const name of modules) {
  await import(name);
  console.log(`module ok: ${name}`);
}
function run(command, args) {
  const result = spawnSync(command, args, { encoding: 'utf8' });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(' ')} failed: ${result.stderr || result.stdout}`);
  }
  return (result.stdout || result.stderr || '').trim();
}
const remotion = run('remotion', ['--version']);
const hyperframes = run('hyperframes', ['--version']);
const typescript = run('tsc', ['--version']);
const ffmpeg = run('ffmpeg', ['-version']).split('\n')[0];
const ffprobe = run('ffprobe', ['-version']).split('\n')[0];
const tesseract = run('tesseract', ['--list-langs']);
assert.match(tesseract, /eng/);
assert.match(tesseract, /vie/);
console.log(JSON.stringify({ remotion, hyperframes, typescript, ffmpeg, ffprobe, tesseractLanguages: tesseract }, null, 2));
