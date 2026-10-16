import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface NumberTickerProps {
  from?: number;
  to: number;
  startFrame?: number;
  durationFrames?: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  useLocale?: boolean;
  locale?: string;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
  style?: React.CSSProperties;
}

export const NumberTicker: React.FC<NumberTickerProps> = ({
  from = 0,
  to,
  startFrame = 0,
  durationFrames,
  prefix = "",
  suffix = "",
  decimals = 0,
  useLocale = true,
  locale = "en-US",
  fontSize = 96,
  color = "#FFFFFF",
  fontFamily = "Montserrat, sans-serif",
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = durationFrames
    ? interpolate(frame - startFrame, [0, durationFrames], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : spring({
        frame: Math.max(0, frame - startFrame),
        fps,
        config: {
          damping: 18,
          stiffness: 80,
          mass: 1.0,
        },
      });

  const clampedProgress = Math.min(1, Math.max(0, progress));
  const currentValue = from + (to - from) * clampedProgress;

  const formattedNumber = useLocale
    ? currentValue.toLocaleString(locale, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      })
    : currentValue.toFixed(decimals);

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "baseline",
        fontSize,
        fontFamily,
        fontWeight: 900,
        color,
        letterSpacing: "-0.03em",
        lineHeight: 1,
        fontVariantNumeric: "tabular-nums",
        textShadow: "0 4px 20px rgba(0, 0, 0, 0.4)",
        ...style,
      }}
    >
      {prefix && <span style={{ marginRight: "0.1em" }}>{prefix}</span>}
      <span>{formattedNumber}</span>
      {suffix && <span style={{ marginLeft: "0.1em" }}>{suffix}</span>}
    </div>
  );
};
