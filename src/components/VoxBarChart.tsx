import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface VoxBarItem {
  label: string;
  value: number;
  formattedValue?: string;
  color?: string;
}

export interface VoxBarChartProps {
  items: readonly VoxBarItem[];
  maxValue?: number;
  accentColor?: string;
  startFrame?: number;
  staggerFrames?: number;
  height?: number;
  showGrid?: boolean;
  style?: React.CSSProperties;
}

export const VoxBarChart: React.FC<VoxBarChartProps> = ({
  items,
  maxValue,
  accentColor = "#FFD60A",
  startFrame = 0,
  staggerFrames = 4,
  height = 360,
  showGrid = true,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const innerHeight = Math.max(0, height - 64);
  const barAreaHeight = Math.max(0, innerHeight - 74);
  const computedMax = maxValue ?? Math.max(...items.map((item) => item.value), 1);

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height,
        backgroundColor: "rgba(13, 13, 17, 0.85)",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        borderRadius: 20,
        padding: "32px 28px",
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        overflow: "hidden",
        ...style,
      }}
    >
      {showGrid && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px)",
            backgroundSize: "28px 28px",
            pointerEvents: "none",
          }}
        />
      )}

      <div
        style={{
          position: "relative",
          zIndex: 1,
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-around",
          gap: 20,
          minHeight: 0,
        }}
      >
        {items.map((item, index) => {
          const itemStart = startFrame + index * staggerFrames;
          const springProgress = spring({
            frame: Math.max(0, frame - itemStart),
            fps,
            config: {
              damping: 14,
              stiffness: 90,
              mass: 0.8,
            },
          });

          const normalizedHeight = Math.min(1, Math.max(0, item.value / computedMax));
          const currentBarHeight = normalizedHeight * springProgress * barAreaHeight;
          const barColor = item.color ?? accentColor;

          return (
            <div
              key={item.label}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "flex-end",
                height: "100%",
                gap: 12,
              }}
            >
              <div
                style={{
                  fontSize: 22,
                  fontFamily: "Inter, sans-serif",
                  fontVariantNumeric: "tabular-nums",
                  fontWeight: 700,
                  color: barColor,
                  opacity: springProgress > 0.1 ? 1 : 0,
                }}
              >
                {item.formattedValue ?? `${Math.round(item.value * springProgress)}`}
              </div>

              <div
                style={{
                  width: "100%",
                  height: currentBarHeight,
                  backgroundColor: barColor,
                  borderRadius: "8px 8px 4px 4px",
                  boxShadow: `0 0 20px ${barColor}44`,
                  transition: "none",
                }}
              />

              <div
                style={{
                  fontSize: 18,
                  fontFamily: "Inter, sans-serif",
                  fontWeight: 600,
                  color: "#CCCCCC",
                  textAlign: "center",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  width: "100%",
                }}
              >
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
