import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type CameraMotion = "push-in" | "push-out" | "pan-left" | "pan-right" | "static-fade";

export interface CameraRigProps {
  children?: React.ReactNode;
  motion?: CameraMotion;
  durationFrames?: number;
  intensity?: number;
  origin?: string;
  style?: React.CSSProperties;
}

export const CameraRig: React.FC<CameraRigProps> = ({
  children,
  motion = "push-in",
  durationFrames,
  intensity = 1.0,
  origin = "center center",
  style,
}) => {
  const frame = useCurrentFrame();
  const videoConfig = useVideoConfig();
  const totalFrames = durationFrames ?? videoConfig.durationInFrames;

  const progress = Math.min(1, Math.max(0, frame / Math.max(1, totalFrames)));

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;
  let opacity = 1.0;

  if (motion === "push-in") {
    const targetScale = 1.0 + 0.08 * intensity;
    scale = interpolate(progress, [0, 1], [1.0, targetScale]);
  } else if (motion === "push-out") {
    const initialScale = 1.0 + 0.08 * intensity;
    scale = interpolate(progress, [0, 1], [initialScale, 1.0]);
  } else if (motion === "pan-left") {
    scale = 1.0 + 0.04 * intensity;
    translateX = interpolate(progress, [0, 1], [0, -40 * intensity]);
  } else if (motion === "pan-right") {
    scale = 1.0 + 0.04 * intensity;
    translateX = interpolate(progress, [0, 1], [0, 40 * intensity]);
  } else if (motion === "static-fade") {
    scale = 1.0;
    opacity = interpolate(progress, [0, 0.15], [0.0, 1.0], {
      extrapolateRight: "clamp",
    });
  }

  return (
    <AbsoluteFill
      style={{
        overflow: "hidden",
        transformOrigin: origin,
        transform: `scale(${scale}) translate3d(${translateX}px, ${translateY}px, 0)`,
        opacity,
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
