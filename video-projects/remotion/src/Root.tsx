import React from "react";
import {Composition} from "remotion";
import {OneMoreScroll} from "./OneMoreScroll";

export const Root: React.FC = () => (
  <Composition
    id="OneMoreScroll"
    component={OneMoreScroll}
    durationInFrames={8 * 180}
    fps={24}
    width={1280}
    height={720}
  />
);
