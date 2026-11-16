import fs from 'node:fs';
import path from 'node:path';
import project from '../src/shots.json' with {type: 'json'};

const root = path.resolve('.');
const imageDir = path.join(root, 'public', 'images');
const audioDir = path.join(root, 'public', 'audio');
const expected = Array.from({length: 90}, (_, i) => 'A' + String(i + 1).padStart(3, '0'));
const imageErrors = [];
for (const id of expected) {
  const file = path.join(imageDir, id + '.jpg');
  if (!fs.existsSync(file)) {
    imageErrors.push('missing ' + id + '.jpg');
    continue;
  }
  const buf = fs.readFileSync(file);
  if (buf.length < 2048 || buf[0] !== 0xff || buf[1] !== 0xd8 || buf[2] !== 0xff) {
    imageErrors.push('invalid JPEG ' + id);
  }
  // The processor writes 1920 x 1080 JPEGs. Validate SOF dimensions with a tiny marker walk.
  let width = 0, height = 0, offset = 2;
  while (offset + 9 < buf.length) {
    if (buf[offset] !== 0xff) { offset++; continue; }
    const marker = buf[offset + 1];
    const length = buf.readUInt16BE(offset + 2);
    if ([0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf].includes(marker)) {
      height = buf.readUInt16BE(offset + 5);
      width = buf.readUInt16BE(offset + 7);
      break;
    }
    if (length < 2) break;
    offset += 2 + length;
  }
  if (width !== 1920 || height !== 1080) imageErrors.push(id + ' dimensions ' + width + 'x' + height);
}
const shots = project.shots;
const timingErrors = [];
let end = 0;
for (const shot of shots) {
  if (shot.from !== end) timingErrors.push(shot.id + ' starts at ' + shot.from + ', expected ' + end);
  if (!Number.isInteger(shot.duration) || shot.duration < 1) timingErrors.push(shot.id + ' invalid duration ' + shot.duration);
  if (!expected.includes(shot.asset)) timingErrors.push(shot.id + ' unknown asset ' + shot.asset);
  if (!Array.isArray(shot.captionWords) || shot.captionWords.length === 0) timingErrors.push(shot.id + ' missing aligned caption words');
  end = shot.from + shot.duration;
}
if (end !== project.durationInFrames) timingErrors.push('timeline end ' + end + ' != ' + project.durationInFrames);
if (shots.length !== 273) timingErrors.push('expected 273 planned shot instances, got ' + shots.length);
if (project.fps !== 30 || project.width !== 1920 || project.height !== 1080) timingErrors.push('composition is not 1920x1080 30fps');

const requiredAudio = ['narration.wav', 'music-bed.wav', 'captions.srt', 'captions.vtt', 'voice-manifest.json', 'alignment-report.json'];
const missingAudio = requiredAudio.filter((name) => !fs.existsSync(path.join(audioDir, name)));
const sfx = [...new Set(shots.map((s) => s.sfx).filter(Boolean))];
for (const name of sfx) {
  if (!fs.existsSync(path.join(audioDir, 'sfx', name + '.wav'))) missingAudio.push('sfx/' + name + '.wav');
}
if (project.audio?.voiceEnabled !== true || project.audio?.musicEnabled !== true || project.audio?.sfxEnabled !== true) {
  missingAudio.push('audio toggles are not all enabled');
}
const reportPath = path.join(root, 'public', 'production-manifest.json');
if (!fs.existsSync(reportPath)) missingAudio.push('production-manifest.json');

console.log('Images:', expected.length, 'verified');
console.log('Shot instances:', shots.length);
console.log('Timeline:', project.durationInFrames, 'frames /', (project.durationInFrames / project.fps).toFixed(3), 'seconds');
console.log('SFX cues:', sfx.length);
if (imageErrors.length || timingErrors.length || missingAudio.length) {
  for (const item of imageErrors) console.error('IMAGE:', item);
  for (const item of timingErrors) console.error('TIMING:', item);
  for (const item of missingAudio) console.error('AUDIO:', item);
  process.exit(1);
}
console.log('All image, voice, caption, audio and timeline gates passed.');
