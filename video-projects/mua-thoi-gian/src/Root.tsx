import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import project from './shots.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MainVideo"
    component={Video}
    durationInFrames={project.durationInFrames}
    fps={project.fps}
    width={project.width}
    height={project.height}
    defaultProps={{}}
  />
);