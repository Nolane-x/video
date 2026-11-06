import React from "react";
import {Composition} from "remotion";
import storyPlan from "../public/story/shots.json";
import {OneMoreScroll} from "./OneMoreScroll";
import {IllustratedHistoryCannae45s} from "./IllustratedHistoryCannae45s";

export const Root: React.FC = () => (
  <>
    <Composition
      id="OneMoreScroll"
      component={OneMoreScroll}
      durationInFrames={storyPlan.duration * storyPlan.fps}
      fps={storyPlan.fps}
      width={1280}
      height={720}
    />
    <Composition
      id="CannaeIllustrated45s"
      component={IllustratedHistoryCannae45s}
      durationInFrames={45 * 24}
      fps={24}
      width={1920}
      height={1080}
    />
  </>
);
