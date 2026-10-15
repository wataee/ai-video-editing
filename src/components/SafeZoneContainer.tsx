import React from "react";
import { AbsoluteFill } from "remotion";

export interface SafeZoneContainerProps {
  children?: React.ReactNode;
  showGuides?: boolean;
  style?: React.CSSProperties;
}

export const SafeZoneContainer: React.FC<SafeZoneContainerProps> = ({
  children,
  showGuides = false,
  style,
}) => {
  return (
    <AbsoluteFill
      style={{
        width: 1080,
        height: 1920,
        overflow: "hidden",
        backgroundColor: "transparent",
        pointerEvents: "none",
        ...style,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 220,
          bottom: 380,
          left: 100,
          right: 100,
          width: 880,
          height: 1320,
          boxSizing: "border-box",
          pointerEvents: "auto",
        }}
      >
        {children}
      </div>

      {showGuides && (
        <AbsoluteFill style={{ pointerEvents: "none" }}>
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              height: 220,
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderBottom: "2px dashed #FF3B30",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FFFFFF",
              fontSize: 24,
              fontFamily: "Inter, sans-serif",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
            }}
          >
            Top Exclusion Zone (220px)
          </div>

          <div
            style={{
              position: "absolute",
              bottom: 0,
              left: 0,
              right: 0,
              height: 380,
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderTop: "2px dashed #FF3B30",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#FFFFFF",
              fontSize: 24,
              fontFamily: "Inter, sans-serif",
              fontWeight: 700,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
            }}
          >
            Bottom Exclusion Zone (380px)
          </div>

          <div
            style={{
              position: "absolute",
              top: 220,
              bottom: 380,
              left: 0,
              width: 100,
              backgroundColor: "rgba(255, 200, 0, 0.15)",
              borderRight: "2px dashed #FFD60A",
            }}
          />

          <div
            style={{
              position: "absolute",
              top: 220,
              bottom: 380,
              right: 0,
              width: 100,
              backgroundColor: "rgba(255, 200, 0, 0.15)",
              borderLeft: "2px dashed #FFD60A",
            }}
          />

          <div
            style={{
              position: "absolute",
              top: 220,
              left: 100,
              width: 880,
              height: 1320,
              border: "2px solid #34C759",
              boxSizing: "border-box",
            }}
          />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
