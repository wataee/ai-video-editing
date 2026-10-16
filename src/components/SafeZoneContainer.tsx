import React from "react";
import { AbsoluteFill } from "remotion";
import { FRAME, SAFE_RECT, shrinkForCamera } from "../config/safeZones";

export interface SafeZoneContainerProps {
  children?: React.ReactNode;
  showGuides?: boolean;
  cameraScale?: number;
  cameraShiftX?: number;
  style?: React.CSSProperties;
}

const guideLabel: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  color: "#FFFFFF",
  fontSize: 24,
  fontFamily: "Inter, sans-serif",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.08em",
};

export const SafeZoneContainer: React.FC<SafeZoneContainerProps> = ({
  children,
  showGuides = false,
  cameraScale = 1,
  cameraShiftX = 0,
  style,
}) => {
  const rect = shrinkForCamera(SAFE_RECT, cameraScale, cameraShiftX);

  return (
    <AbsoluteFill
      style={{
        width: FRAME.width,
        height: FRAME.height,
        overflow: "hidden",
        backgroundColor: "transparent",
        pointerEvents: "none",
        ...style,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: rect.left,
          top: rect.top,
          width: rect.right - rect.left,
          height: rect.bottom - rect.top,
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
              ...guideLabel,
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              height: SAFE_RECT.top,
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderBottom: "2px dashed #FF3B30",
            }}
          >
            Top Exclusion Zone ({SAFE_RECT.top}px)
          </div>
          <div
            style={{
              ...guideLabel,
              position: "absolute",
              bottom: 0,
              left: 0,
              right: 0,
              height: FRAME.height - SAFE_RECT.bottom,
              backgroundColor: "rgba(255, 0, 0, 0.2)",
              borderTop: "2px dashed #FF3B30",
            }}
          >
            Bottom Exclusion Zone ({FRAME.height - SAFE_RECT.bottom}px)
          </div>
          <div
            style={{
              position: "absolute",
              top: SAFE_RECT.top,
              bottom: FRAME.height - SAFE_RECT.bottom,
              left: 0,
              width: SAFE_RECT.left,
              backgroundColor: "rgba(255, 200, 0, 0.15)",
              borderRight: "2px dashed #FFD60A",
            }}
          />
          <div
            style={{
              position: "absolute",
              top: SAFE_RECT.top,
              bottom: FRAME.height - SAFE_RECT.bottom,
              right: 0,
              width: FRAME.width - SAFE_RECT.right,
              backgroundColor: "rgba(255, 200, 0, 0.15)",
              borderLeft: "2px dashed #FFD60A",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: SAFE_RECT.left,
              top: SAFE_RECT.top,
              width: SAFE_RECT.right - SAFE_RECT.left,
              height: SAFE_RECT.bottom - SAFE_RECT.top,
              border: "2px solid #34C759",
              boxSizing: "border-box",
            }}
          />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
