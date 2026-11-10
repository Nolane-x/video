import React from "react";
import {Composition} from "remotion";
import storyPlan from "../public/story/shots.json";
import {OneMoreScroll} from "./OneMoreScroll";
import {OpenDesignMotion} from "./OpenDesignMotion";

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
      id="OpenDesignMotion"
      component={OpenDesignMotion}
      durationInFrames={1119}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
