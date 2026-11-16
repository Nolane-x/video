import React from 'react';
import {
  AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import project from './shots.json';

type CaptionWord = { text: string; start: number; end: number; alignment?: string };
type Shot = {
  id: string; asset: string; voiceId: string; beat: string; from: number; duration: number;
  framing?: string; motion?: string; scaleFrom: number; scaleTo: number;
  xFrom: number; xTo: number; yFrom: number; yTo: number; subtitle: string;
  overlay?: string; overlayType?: string; sfx?: string; captionWords?: CaptionWord[];
};
type Project = typeof project & {
  durationSeconds?: number;
  audio?: {
    voiceEnabled?: boolean; musicEnabled?: boolean; sfxEnabled?: boolean;
    voiceAsset?: string; musicAsset?: string;
    voiceVolume?: number; musicVolume?: number; sfxVolume?: number;
  };
};
const data = project as Project;
const BEAT_LABELS: Record<string, string> = {
  '01_HOOK': 'MỘT GIAO DỊCH KHÔNG TƯỞNG',
  '02_LIFE_BEFORE': 'TRƯỚC KHI THỜI GIAN ĐÓNG BĂNG',
  '03_POWER': 'MỘT GIỜ RIÊNG TƯ',
  '04_RULES': 'NĂM QUY TẮC',
  '05_BENEFIT': 'KHI THỜI GIAN THUỘC VỀ BẠN',
  '06_DRIFT': 'CÁI GIÁ CỦA SỰ TIỆN LỢI',
  '07_LOW': 'KHÔNG CÒN THỜI GIAN',
  '08_REVEAL': 'SỰ THẬT SAU GIAO DỊCH',
  '09_RESOLVE': 'KHÔNG GÌ MUA LẠI ĐƯỢC',
};
const clamp = (v: number, min: number, max: number) => Math.min(max, Math.max(min, v));

const FilmTexture: React.FC<{freeze: boolean}> = ({freeze}) => (
  <AbsoluteFill style={{pointerEvents: 'none'}}>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,8,14,.16) 0%, transparent 27%, transparent 58%, rgba(4,5,9,.55) 100%)'}} />
    <AbsoluteFill style={{
      boxShadow: 'inset 0 0 150px rgba(0,0,0,.38)',
      backgroundImage: 'repeating-linear-gradient(0deg, rgba(255,255,255,.013) 0px, rgba(255,255,255,.013) 1px, transparent 1px, transparent 3px)',
      mixBlendMode: 'soft-light',
    }} />
    {freeze ? <AbsoluteFill style={{
      background: 'radial-gradient(ellipse at 52% 48%, rgba(91,170,255,.07), rgba(10,25,48,.22) 72%, rgba(4,8,17,.42))',
      mixBlendMode: 'screen',
    }} /> : null}
  </AbsoluteFill>
);

const FreezeParticles: React.FC<{frame: number; shotId: string}> = ({frame, shotId}) => {
  const seed = [...shotId].reduce((sum, char) => sum + char.charCodeAt(0), 0);
  return (
    <AbsoluteFill style={{pointerEvents: 'none', overflow: 'hidden'}}>
      {Array.from({length: 24}, (_, index) => {
        const x = ((seed * (index + 3) * 17) % 997) / 997 * 100;
        const y = ((seed * (index + 11) * 29) % 991) / 991 * 100;
        const phase = ((seed + index * 23) % 97) / 97;
        const drift = ((frame * (0.08 + (index % 5) * 0.025) + phase * 120) % 140) - 20;
        const opacity = 0.18 + 0.42 * (0.5 + 0.5 * Math.sin(frame * 0.045 + index));
        const size = 2 + (index % 4);
        return <div key={index} style={{
          position: 'absolute', left: x + '%', top: (((y + drift * 0.18) % 108) + '%'),
          width: size, height: size, borderRadius: 99,
          background: index % 4 === 0 ? '#FFC36C' : '#B8D9FF', opacity,
          filter: 'blur(.3px)', boxShadow: '0 0 11px rgba(170,210,255,.65)',
        }} />;
      })}
    </AbsoluteFill>
  );
};

const TimerGraphic: React.FC<{frame: number; duration: number}> = ({frame, duration}) => {
  const progress = clamp(frame / Math.max(1, duration), 0, 1);
  const circumference = 2 * Math.PI * 48;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
      <svg width="112" height="112" viewBox="0 0 112 112">
        <circle cx="56" cy="56" r="48" stroke="rgba(255,255,255,.18)" strokeWidth="7" fill="none" />
        <circle cx="56" cy="56" r="48" stroke="#F08A1E" strokeWidth="7" fill="none"
          strokeLinecap="round" strokeDasharray={String(circumference)}
          strokeDashoffset={String(circumference * progress)} transform="rotate(-90 56 56)" />
        <circle cx="56" cy="56" r="38" fill="rgba(8,12,21,.72)" />
        <text x="56" y="62" textAnchor="middle" fill="#FFF3E0" fontSize="21" fontWeight="900">60:00</text>
      </svg>
      <div style={{display: 'flex', flexDirection: 'column', gap: 5}}>
        <div style={{fontSize: 17, color: '#F5B65C', letterSpacing: 3, fontWeight: 900}}>THỜI GIAN RIÊNG</div>
        <div style={{fontSize: 31, color: '#FFF7EA', fontWeight: 900, lineHeight: 1}}>MỘT GIỜ</div>
        <div style={{fontSize: 17, color: 'rgba(255,245,228,.75)'}}>Không thể hoàn lại</div>
      </div>
    </div>
  );
};

const OverlayCard: React.FC<{shot: Shot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({frame, fps, config: {damping: 18, stiffness: 110, mass: 0.8}});
  const opacity = interpolate(frame, [0, 6, 13], [0, 0.94, 1], {extrapolateRight: 'clamp'});
  const lift = interpolate(progress, [0, 1], [28, 0]);
  const type = shot.overlayType || 'data';
  if (!shot.overlay) return null;

  if (type === 'timer') {
    return <div style={{
      position: 'absolute', right: '6.5%', top: '8%', padding: '17px 23px',
      borderRadius: 18, background: 'linear-gradient(135deg, rgba(7,12,22,.88), rgba(14,25,40,.76))',
      border: '1px solid rgba(255,174,74,.36)', boxShadow: '0 18px 55px rgba(0,0,0,.34)',
      opacity, transform: 'translateY(' + lift + 'px)',
    }}><TimerGraphic frame={frame} duration={shot.duration} /></div>;
  }

  if (type === 'ledger') {
    return <div style={{
      position: 'absolute', left: '6.5%', top: '8%', width: '43%', padding: '22px 26px',
      borderRadius: 15, color: '#FFF5E8',
      background: 'linear-gradient(145deg, rgba(8,13,23,.93), rgba(24,26,34,.84))',
      border: '1px solid rgba(255,176,84,.4)', boxShadow: '0 22px 70px rgba(0,0,0,.42)',
      opacity, transform: 'translateY(' + lift + 'px)',
    }}>
      <div style={{fontSize: 15, letterSpacing: 3, color: '#FFB45B', fontWeight: 900, marginBottom: 10}}>TÀI KHOẢN NGƯỜI BÁN</div>
      <div style={{fontSize: 24, fontWeight: 900, marginBottom: 18}}>{shot.overlay}</div>
      <div style={{height: 1, background: 'rgba(255,255,255,.17)', marginBottom: 15}} />
      {['Học phí và khoản học tập', 'Máy tính và đồ dùng', 'Chi phí đầu năm'].map((label, index) => (
        <div key={label} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10, padding: '7px 0', fontSize: 17}}>
          <span style={{color: 'rgba(255,245,232,.82)'}}>{label}</span>
          <span style={{color: index === 0 ? '#FFBD72' : '#E6D8C4', fontWeight: 800}}>•••</span>
        </div>
      ))}
      <div style={{marginTop: 13, paddingTop: 13, borderTop: '1px solid rgba(255,255,255,.14)', color: '#FFBA64', fontSize: 15, letterSpacing: 1.2}}>1.440 GIỜ  ·  60 NGÀY</div>
    </div>;
  }

  const isTitle = type === 'title';
  const isRule = type === 'rule';
  const isPrice = type === 'price';
  return <div style={{
    position: 'absolute', left: '6.5%', top: isTitle ? '12%' : '8%',
    maxWidth: isTitle ? '61%' : '56%',
    padding: isTitle ? '21px 27px 23px' : '16px 21px 18px',
    borderLeft: (isTitle ? 8 : 5) + 'px solid #F08A1E',
    borderRadius: 9, background: 'linear-gradient(110deg, rgba(7,11,19,.88), rgba(7,11,19,.58))',
    color: '#FFF5E7', fontFamily: 'Noto Sans, Arial, sans-serif', fontWeight: 900,
    fontSize: isTitle ? 54 : (isPrice ? 43 : (isRule ? 35 : 42)),
    lineHeight: 1.12, letterSpacing: isTitle ? 1.6 : 0.3,
    textShadow: '0 4px 20px rgba(0,0,0,.68)', opacity,
    transform: 'translateY(' + lift + 'px)', boxShadow: '0 16px 44px rgba(0,0,0,.27)',
  }}>
    {isTitle ? <div style={{fontSize: 14, letterSpacing: 4, color: '#F5AD53', marginBottom: 12}}>CHUYỆN GIẢ TƯỞNG · WHAT IF</div> : null}
    {shot.overlay}
    {isPrice ? <div style={{fontSize: 17, marginTop: 9, color: 'rgba(255,242,221,.74)', letterSpacing: 2}}>MỘT GIỜ RIÊNG TƯ</div> : null}
    {isRule ? <div style={{fontSize: 15, marginTop: 9, color: 'rgba(255,242,221,.68)', letterSpacing: 2}}>QUY TẮC CỦA ỨNG DỤNG</div> : null}
  </div>;
};

const Captions: React.FC<{shot: Shot; absoluteTime: number}> = ({shot, absoluteTime}) => {
  const words = shot.captionWords || [];
  const activeIndex = words.findIndex((word) => absoluteTime >= word.start && absoluteTime < word.end);
  const size = shot.subtitle.length > 84 ? 26 : (shot.subtitle.length > 58 ? 30 : 34);
  const tokens = words.length ? words : shot.subtitle.split(/\s+/).map((text) => ({text, start: -1, end: -1}));
  return <div style={{
    position: 'absolute', left: '6.5%', right: '6.5%', bottom: '6.2%',
    display: 'flex', justifyContent: 'center', pointerEvents: 'none',
  }}>
    <div style={{
      maxWidth: '92%', display: 'flex', flexWrap: 'wrap', alignItems: 'center',
      justifyContent: 'center', columnGap: 10, rowGap: 3, padding: '11px 22px 13px',
      borderRadius: 12,
      background: 'linear-gradient(90deg, rgba(5,8,14,.0), rgba(5,8,14,.77) 10%, rgba(5,8,14,.77) 90%, rgba(5,8,14,.0))',
      textAlign: 'center', fontFamily: 'Noto Sans, Arial, sans-serif',
      fontSize: size, lineHeight: 1.35, fontWeight: 800, letterSpacing: 0.05,
      textShadow: '0 3px 12px rgba(0,0,0,.96)',
    }}>
      {tokens.map((word, index) => {
        const active = index === activeIndex;
        const alreadySpoken = activeIndex >= 0 && index < activeIndex;
        return <span key={shot.id + '-' + index} style={{
          color: active ? '#FFB34E' : (alreadySpoken ? '#FFF0D9' : 'rgba(255,250,241,.94)'),
          textShadow: active ? '0 0 16px rgba(255,153,44,.45), 0 3px 12px rgba(0,0,0,.96)' : '0 3px 12px rgba(0,0,0,.96)',
          transform: active ? 'translateY(-1px)' : 'none', display: 'inline-block',
        }}>{word.text}</span>;
      })}
    </div>
  </div>;
};

const ShotView: React.FC<{shot: Shot; shotIndex: number}> = ({shot, shotIndex}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const localProgress = clamp(frame / Math.max(1, shot.duration - 1), 0, 1);
  const eased = localProgress * localProgress * (3 - 2 * localProgress);
  const scale = interpolate(eased, [0, 1], [shot.scaleFrom, shot.scaleTo]);
  const x = interpolate(eased, [0, 1], [shot.xFrom, shot.xTo]) * 100;
  const y = interpolate(eased, [0, 1], [shot.yFrom, shot.yTo]) * 100;
  const micro = Math.sin((frame + shotIndex * 17) / fps * 0.42) * 0.003;
  const settle = interpolate(frame, [0, 7], [1.012, 1], {extrapolateRight: 'clamp'});
  const absoluteTime = (shot.from + frame) / fps;
  const image = staticFile('images/' + shot.asset + '.jpg');
  const freeze = shot.beat === '03_POWER' || shot.beat === '07_LOW' || shot.beat === '08_REVEAL';
  const reveal = shot.beat === '08_REVEAL';
  const lightFlash = shot.beat === '03_POWER' && ['A016', 'A017', 'A025'].includes(shot.asset);
  const rotate = Math.sin((frame / Math.max(1, shot.duration)) * Math.PI) * (shot.motion === 'handheld_micro' ? 0.12 : 0.025);

  return <AbsoluteFill style={{backgroundColor: '#080B12', overflow: 'hidden'}}>
    <Img src={image} style={{
      width: '100%', height: '100%', objectFit: 'cover',
      transform: 'scale(' + (1.16 + micro) + ')',
      filter: 'blur(22px) brightness(.34) saturate(.8)', opacity: 0.46,
    }} />
    <Img src={image} style={{
      position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover',
      transform: 'translate(' + (x + micro * 100) + '%, ' + y + '%) scale(' + (scale * settle) + ') rotate(' + rotate + 'deg)',
      transformOrigin: '50% 50%',
      filter: reveal ? 'saturate(.9) contrast(1.04)' : 'saturate(.96) contrast(1.04)',
    }} />
    <FilmTexture freeze={freeze} />
    {freeze ? <FreezeParticles frame={frame} shotId={shot.id} /> : null}
    {lightFlash ? <AbsoluteFill style={{
      background: 'radial-gradient(circle at 50% 50%, rgba(210,232,255,' + (0.08 * (1 - localProgress)) + ') 0%, transparent 62%)',
      mixBlendMode: 'screen', pointerEvents: 'none',
    }} /> : null}
    <div style={{position: 'absolute', left: '6.5%', top: '5.3%', display: 'flex', alignItems: 'center', gap: 12, opacity: 0.86}}>
      <div style={{width: 5, height: 27, borderRadius: 8, background: '#F08A1E'}} />
      <div style={{fontFamily: 'Noto Sans, Arial, sans-serif', fontSize: 14, fontWeight: 900, letterSpacing: 2.3, color: '#FFF2DC'}}>
        {BEAT_LABELS[shot.beat] || 'MỘT CÂU CHUYỆN WHAT IF'}
      </div>
    </div>
    <div style={{
      position: 'absolute', right: '6.5%', top: '5.4%', color: 'rgba(255,242,220,.58)',
      fontFamily: 'Noto Sans, Arial, sans-serif', fontSize: 14, fontWeight: 700, letterSpacing: 2,
    }}>{String(shotIndex + 1).padStart(3, '0')} / 273</div>
    <OverlayCard shot={shot} />
    <Captions shot={shot} absoluteTime={absoluteTime} />
    <div style={{position: 'absolute', left: '6.5%', right: '6.5%', bottom: '3.4%', height: 2, background: 'rgba(255,255,255,.19)', overflow: 'hidden'}}>
      <div style={{
        width: (clamp((shot.from + frame) / data.durationInFrames, 0, 1) * 100) + '%',
        height: '100%', background: 'linear-gradient(90deg,#F08A1E,#FFC16B)',
      }} />
    </div>
    {shot.sfx && data.audio?.sfxEnabled ? <Audio src={staticFile('audio/sfx/' + shot.sfx + '.wav')} volume={data.audio?.sfxVolume ?? 0.22} /> : null}
  </AbsoluteFill>;
};

export const Video: React.FC = () => {
  const audio = data.audio || {};
  const shots = data.shots as unknown as Shot[];
  return <AbsoluteFill style={{backgroundColor: '#080B12'}}>
    {shots.map((shot, index) => (
      <Sequence key={shot.id} from={shot.from} durationInFrames={shot.duration}>
        <ShotView shot={shot} shotIndex={index} />
      </Sequence>
    ))}
    {audio.voiceEnabled ? <Audio src={staticFile(audio.voiceAsset || 'audio/narration.wav')} volume={audio.voiceVolume ?? 1} /> : null}
    {audio.musicEnabled ? <Audio src={staticFile(audio.musicAsset || 'audio/music-bed.wav')} volume={audio.musicVolume ?? 0.36} /> : null}
  </AbsoluteFill>;
};
