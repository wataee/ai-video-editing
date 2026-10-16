import { interpolate, spring } from "remotion";

export interface SpringPhysicsOptions {
  frame: number;
  fps: number;
  damping?: number;
  stiffness?: number;
  mass?: number;
  overshootPercent?: number;
}

export const springPhysics = ({
  frame,
  fps,
  damping = 12,
  stiffness = 130,
  mass = 0.8,
  overshootPercent = 3.5,
}: SpringPhysicsOptions): number => {
  const spr = spring({
    frame,
    fps,
    config: {
      damping,
      stiffness,
      mass,
    },
  });

  const peak = 1.0 + Math.max(0.01, Math.min(0.08, overshootPercent / 100));

  return interpolate(spr, [0, 0.85, 1], [0, peak, 1.0], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });
};

export const interpolateScaleOvershoot = (
  progress: number,
  initialScale = 0.92,
  targetScale = 1.0,
  overshootPercent = 3.0
): number => {
  const peakScale = targetScale * (1.0 + overshootPercent / 100);
  return interpolate(progress, [0, 0.85, 1], [initialScale, peakScale, targetScale], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });
};
