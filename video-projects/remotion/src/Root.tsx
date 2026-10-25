import React from "react";
import {Composition} from "remotion";
import storyPlan from "../public/story/shots.json";
import {OneMoreScroll} from "./OneMoreScroll";

export const Root: React.FC = () => (
  <Composition
    id="OneMoreScroll"
    component={OneMoreScroll}
    durationInFrames={storyPlan.duration * storyPlan.fps}
    fps={storyPlan.fps}
    width={1280}
    height={720}
  />
);
