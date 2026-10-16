import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACTIVE_STYLE } from "../config/stylePresets";

export interface SpeakerBadgeProps {
  name: string;
  role: string;
  enterFrame?: number;
  style?: React.CSSProperties;
}

export const SpeakerBadge: React.FC<SpeakerBadgeProps> = ({
  name,
  role,
  enterFrame = 15,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - enterFrame);

  const entrance = spring({
    frame: relFrame,
    fps,
    config: {
      damping: 15,
      stiffness: 110,
    },
  });

  const opacity = interpolate(relFrame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });
  const translateX = interpolate(entrance, [0, 0.85, 1], [-40, 2.5, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 14,
        backgroundColor: "rgba(10, 10, 14, 0.82)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        border: `1px solid ${ACTIVE_STYLE.colors.cardBorder}`,
        borderRadius: 100,
        padding: "10px 22px",
        boxShadow: "0 12px 30px rgba(0, 0, 0, 0.5)",
        transform: `translateX(${translateX}px)`,
        opacity,
        pointerEvents: "none",
        ...style,
      }}
    >
      <div
        style={{
          width: 10,
          height: 10,
          borderRadius: "50%",
          backgroundColor: ACTIVE_STYLE.colors.accent,
          boxShadow: `0 0 10px ${ACTIVE_STYLE.colors.accent}`,
        }}
      />
      <div>
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.headline,
            fontWeight: 800,
            fontSize: 18,
            color: ACTIVE_STYLE.colors.textPrimary,
            lineHeight: 1.2,
          }}
        >
          {name}
        </div>
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.body,
            fontWeight: 500,
            fontSize: 13,
            color: ACTIVE_STYLE.colors.textSecondary,
            lineHeight: 1.2,
          }}
        >
          {role}
        </div>
      </div>
    </div>
  );
};
