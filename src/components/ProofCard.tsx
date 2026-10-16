import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ACTIVE_STYLE } from "../config/stylePresets";

export interface ProofCardProps {
  badge?: string;
  title: string;
  subtitle?: string;
  imageSrc?: string;
  enterFrame?: number;
  width?: number;
  tiltAngle?: number;
  style?: React.CSSProperties;
}

export const ProofCard: React.FC<ProofCardProps> = ({
  badge = "ДОКАЗАТЕЛЬСТВО / ПРУФ",
  title,
  subtitle,
  imageSrc,
  enterFrame = 0,
  width = 860,
  tiltAngle = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const relFrame = Math.max(0, frame - enterFrame);

  const entrance = spring({
    frame: relFrame,
    fps,
    config: {
      damping: 14,
      stiffness: 120,
      mass: 0.8,
    },
  });

  const opacity = interpolate(relFrame, [0, 8], [0, 1], {
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(entrance, [0, 1], [40, 0]);
  const scale = interpolate(entrance, [0, 0.85, 1], [0.94, 1.03, 1.0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width,
        maxWidth: "92%",
        backgroundColor: ACTIVE_STYLE.colors.card,
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        border: `1.5px solid ${ACTIVE_STYLE.colors.cardBorder}`,
        borderRadius: 24,
        padding: "28px 32px",
        boxShadow: ACTIVE_STYLE.colors.shadow,
        boxSizing: "border-box",
        transform: `translateY(${translateY}px) scale(${scale}) rotate(${tiltAngle}deg)`,
        opacity,
        display: "flex",
        flexDirection: "column",
        gap: 16,
        pointerEvents: "none",
        ...style,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.body,
            fontSize: 14,
            fontWeight: 800,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: ACTIVE_STYLE.colors.accent,
            backgroundColor: "rgba(255, 214, 10, 0.12)",
            padding: "6px 14px",
            borderRadius: 8,
            border: "1px solid rgba(255, 214, 10, 0.3)",
          }}
        >
          {badge}
        </div>
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.body,
            fontSize: 13,
            color: ACTIVE_STYLE.colors.textSecondary,
          }}
        >
          ВЕРИФИЦИРОВАНО
        </div>
      </div>

      <div>
        <div
          style={{
            fontFamily: ACTIVE_STYLE.fonts.headline,
            fontWeight: 900,
            fontSize: 28,
            lineHeight: 1.25,
            color: ACTIVE_STYLE.colors.textPrimary,
          }}
        >
          {title}
        </div>
        {subtitle && (
          <div
            style={{
              fontFamily: ACTIVE_STYLE.fonts.body,
              fontSize: 18,
              fontWeight: 500,
              lineHeight: 1.4,
              color: ACTIVE_STYLE.colors.textSecondary,
              marginTop: 6,
            }}
          >
            {subtitle}
          </div>
        )}
      </div>

      {imageSrc && (
        <div
          style={{
            borderRadius: 14,
            overflow: "hidden",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            maxHeight: 460,
            backgroundColor: "#000000",
          }}
        >
          <Img
            src={imageSrc.startsWith("data:") || imageSrc.startsWith("http") ? imageSrc : staticFile(imageSrc)}
            style={{
              width: "100%",
              height: "auto",
              objectFit: "contain",
              display: "block",
            }}
          />
        </div>
      )}
    </div>
  );
};
