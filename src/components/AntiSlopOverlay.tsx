import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export interface AntiSlopOverlayProps {
  children?: React.ReactNode;
  durationInFrames?: number;
  grainOpacity?: number;
  driftScale?: number;
  vignetteOpacity?: number;
  showVignette?: boolean;
  style?: React.CSSProperties;
}

export const AntiSlopOverlay: React.FC<AntiSlopOverlayProps> = ({
  children,
  durationInFrames,
  grainOpacity = 0.04,
  driftScale = 1.03,
  vignetteOpacity = 0.35,
  showVignette = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames: configDuration } = useVideoConfig();
  const total = Math.max(1, durationInFrames ?? configDuration);

  const progress = Math.min(1.0, Math.max(0, frame / total));
  const scale = interpolate(progress, [0, 1], [1.0, driftScale], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const clampedGrain = Math.max(0.02, Math.min(0.06, grainOpacity));

  return (
    <AbsoluteFill style={{ overflow: "hidden", ...style }}>
      <div
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          transform: `scale(${scale})`,
          transformOrigin: "center center",
          willChange: "transform",
        }}
      >
        {children}
      </div>

      {showVignette && (
        <AbsoluteFill
          style={{
            pointerEvents: "none",
            zIndex: 9998,
            background:
              "radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.85) 100%)",
            opacity: vignetteOpacity,
            mixBlendMode: "multiply",
          }}
        />
      )}

      <AbsoluteFill
        style={{
          pointerEvents: "none",
          zIndex: 9999,
          mixBlendMode: "overlay",
          opacity: clampedGrain,
        }}
      >
        <svg
          width="100%"
          height="100%"
          xmlns="http://www.w3.org/2000/svg"
          style={{ width: "100%", height: "100%" }}
        >
          <filter id="anti-slop-turbulence">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.82"
              numOctaves="3"
              stitchTiles="stitch"
            />
            <feColorMatrix type="saturate" values="0" />
          </filter>
          <rect width="100%" height="100%" filter="url(#anti-slop-turbulence)" />
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
