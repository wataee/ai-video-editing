import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export type CameraMotion = "push-in" | "push-out" | "pan-left" | "pan-right" | "static-fade";

export const getCameraMaxScale = (motion: CameraMotion, intensity = 1.0): number => {
  if (motion === "push-in" || motion === "push-out") return 1.0 + 0.08 * intensity;
  if (motion === "pan-left" || motion === "pan-right") return 1.0 + 0.04 * intensity;
  return 1.0;
};

export const getCameraMaxShiftX = (motion: CameraMotion, intensity = 1.0): number =>
  motion === "pan-left" || motion === "pan-right" ? 40 * intensity : 0;

export interface CameraRigProps {
  children?: React.ReactNode;
  motion?: CameraMotion;
  durationFrames?: number;
  intensity?: number;
  origin?: string;
  microDrift?: boolean;
  style?: React.CSSProperties;
}

export const CameraRig: React.FC<CameraRigProps> = ({
  children,
  motion = "push-in",
  durationFrames,
  intensity = 1.0,
  origin = "center center",
  microDrift = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const videoConfig = useVideoConfig();
  const totalFrames = durationFrames ?? videoConfig.durationInFrames;

  const progress = Math.min(1, Math.max(0, frame / Math.max(1, totalFrames)));

  const driftScale = microDrift
    ? interpolate(progress, [0, 1], [1.0, 1.03], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 1.0;

  const driftTranslateX = microDrift
    ? interpolate(progress, [0, 0.5, 1], [0, 4, -3], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : 0;

  let motionScale = 1.0;
  let translateX = 0;
  let translateY = 0;
  let opacity = 1.0;

  if (motion === "push-in") {
    const targetScale = 1.0 + 0.08 * intensity;
    motionScale = interpolate(progress, [0, 1], [1.0, targetScale]);
  } else if (motion === "push-out") {
    const initialScale = 1.0 + 0.08 * intensity;
    motionScale = interpolate(progress, [0, 1], [initialScale, 1.0]);
  } else if (motion === "pan-left") {
    motionScale = 1.0 + 0.04 * intensity;
    translateX = interpolate(progress, [0, 1], [0, -40 * intensity]);
  } else if (motion === "pan-right") {
    motionScale = 1.0 + 0.04 * intensity;
    translateX = interpolate(progress, [0, 1], [0, 40 * intensity]);
  } else if (motion === "static-fade") {
    motionScale = 1.0;
    opacity = interpolate(progress, [0, 0.15], [0.0, 1.0], {
      extrapolateRight: "clamp",
    });
  }

  const finalScale = motionScale * driftScale;
  const finalTranslateX = translateX + driftTranslateX;

  return (
    <AbsoluteFill
      style={{
        overflow: "hidden",
        transformOrigin: origin,
        transform: `scale(${finalScale}) translate3d(${finalTranslateX}px, ${translateY}px, 0)`,
        opacity,
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
