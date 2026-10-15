import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface LiquidGlassCardProps {
  title?: string;
  subtitle?: string;
  badge?: string;
  children?: React.ReactNode;
  chromaMode?: boolean;
  enterFrame?: number;
  width?: number | string;
  padding?: number | string;
  style?: React.CSSProperties;
}

export const LiquidGlassCard: React.FC<LiquidGlassCardProps> = ({
  title,
  subtitle,
  badge,
  children,
  chromaMode = false,
  enterFrame = 0,
  width = "100%",
  padding = 40,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: Math.max(0, frame - enterFrame),
    fps,
    config: {
      damping: 14,
      stiffness: 110,
      mass: 0.9,
    },
  });

  const scale = entrance;
  const opacity = Math.min(1, Math.max(0, entrance));

  return (
    <div
      style={{
        position: "relative",
        width,
        boxSizing: "border-box",
        padding,
        borderRadius: 28,
        backgroundColor: chromaMode ? "#00FF00" : "rgba(255, 255, 255, 0.14)",
        backdropFilter: chromaMode ? undefined : "blur(24px) saturate(180%)",
        WebkitBackdropFilter: chromaMode ? undefined : "blur(24px) saturate(180%)",
        border: chromaMode ? undefined : "1px solid rgba(255, 255, 255, 0.28)",
        boxShadow: chromaMode ? undefined : "0 20px 40px rgba(0, 0, 0, 0.35)",
        transform: `scale(${scale})`,
        opacity,
        display: "flex",
        flexDirection: "column",
        gap: 20,
        ...style,
      }}
    >
      {(badge || title) && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 16,
          }}
        >
          {badge && (
            <span
              style={{
                alignSelf: "flex-start",
                padding: "6px 16px",
                borderRadius: 999,
                backgroundColor: chromaMode ? "#000000" : "rgba(255, 255, 255, 0.2)",
                color: chromaMode ? "#FFFFFF" : "#FFFFFF",
                fontSize: 20,
                fontFamily: "Inter, sans-serif",
                fontWeight: 700,
                letterSpacing: "0.05em",
                textTransform: "uppercase",
              }}
            >
              {badge}
            </span>
          )}

          {title && (
            <h3
              style={{
                margin: 0,
                color: chromaMode ? "#000000" : "#FFFFFF",
                fontSize: 36,
                fontFamily: "Inter, sans-serif",
                fontWeight: 800,
                letterSpacing: "-0.02em",
                textShadow: chromaMode ? undefined : "0 2px 10px rgba(0,0,0,0.5)",
              }}
            >
              {title}
            </h3>
          )}
        </div>
      )}

      {subtitle && (
        <p
          style={{
            margin: 0,
            color: chromaMode ? "#222222" : "rgba(255, 255, 255, 0.8)",
            fontSize: 24,
            fontFamily: "Inter, sans-serif",
            fontWeight: 500,
            lineHeight: 1.4,
          }}
        >
          {subtitle}
        </p>
      )}

      {children && (
        <div
          style={{
            width: "100%",
            color: chromaMode ? "#000000" : "#FFFFFF",
          }}
        >
          {children}
        </div>
      )}
    </div>
  );
};
