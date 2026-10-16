import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACTIVE_STYLE } from "../config/stylePresets";

export interface HookHeadlineProps {
  headline: string;
  accentWord?: string;
  categoryBadge?: string;
  enterFrame?: number;
  style?: React.CSSProperties;
}

export const HookHeadline: React.FC<HookHeadlineProps> = ({
  headline,
  accentWord,
  categoryBadge = "РАЗБОР ОШИБКИ",
  enterFrame = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - enterFrame);

  const entrance = spring({
    frame: relFrame,
    fps,
    config: {
      damping: 13,
      stiffness: 140,
    },
  });

  const opacity = interpolate(relFrame, [0, 8], [0, 1], {
    extrapolateRight: "clamp",
  });
  const scale = interpolate(entrance, [0, 0.85, 1], [0.92, 1.035, 1.0], {
    extrapolateRight: "clamp",
  });

  const words = headline.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        textAlign: "center",
        maxWidth: 900,
        padding: "0 20px",
        transform: `scale(${scale})`,
        opacity,
        pointerEvents: "none",
        ...style,
      }}
    >
      {categoryBadge && (
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.body,
            fontWeight: 800,
            fontSize: 15,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: ACTIVE_STYLE.colors.accent,
            backgroundColor: "rgba(255, 214, 10, 0.14)",
            border: `1px solid rgba(255, 214, 10, 0.35)`,
            borderRadius: 100,
            padding: "8px 20px",
            marginBottom: 20,
            boxShadow: "0 4px 16px rgba(0, 0, 0, 0.4)",
          }}
        >
          {categoryBadge}
        </div>
      )}

      <h1
        style={{
          fontFamily: ACTIVE_STYLE.fonts.headline,
          fontWeight: 900,
          fontSize: 60,
          lineHeight: 1.15,
          color: ACTIVE_STYLE.colors.textPrimary,
          textTransform: "uppercase",
          letterSpacing: "-0.02em",
          margin: 0,
          textShadow: "0 10px 40px rgba(0, 0, 0, 0.8)",
        }}
      >
        {words.map((w, i) => {
          const isAccent = accentWord && w.toLowerCase().includes(accentWord.toLowerCase());
          return (
            <span
              key={`${w}-${i}`}
              style={{
                color: isAccent ? ACTIVE_STYLE.colors.accent : ACTIVE_STYLE.colors.textPrimary,
                marginRight: 14,
                display: "inline-block",
              }}
            >
              {w}
            </span>
          );
        })}
      </h1>
    </div>
  );
};
