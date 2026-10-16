import React from "react";
import { AbsoluteFill } from "remotion";

export interface ProceduralNoiseOverlayProps {
  opacity?: number;
  baseFrequency?: number;
  numOctaves?: number;
}

export const ProceduralNoiseOverlay: React.FC<ProceduralNoiseOverlayProps> = ({
  opacity = 0.04,
  baseFrequency = 0.85,
  numOctaves = 3,
}) => {
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        zIndex: 9999,
        mixBlendMode: "overlay",
        opacity,
      }}
    >
      <svg
        width="100%"
        height="100%"
        xmlns="http://www.w3.org/2000/svg"
        style={{ width: "100%", height: "100%" }}
      >
        <filter id="anti-slop-grain">
          <feTurbulence
            type="fractalNoise"
            baseFrequency={baseFrequency}
            numOctaves={numOctaves}
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#anti-slop-grain)" />
      </svg>
    </AbsoluteFill>
  );
};
