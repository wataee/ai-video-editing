import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACTIVE_STYLE } from "../config/stylePresets";
import { CAPTION_RECT, shrinkForCamera } from "../config/safeZones";

export interface CaptionWord {
  text: string;
  startFrame: number;
  endFrame: number;
}

export interface WordByWordCaptionsProps {
  words: readonly CaptionWord[];
  activeColor?: string;
  inactiveColor?: string;
  backgroundColor?: string;
  fontSize?: number;
  fontFamily?: string;
  highlightScale?: number;
  top?: number;
  cameraScale?: number;
  cameraShiftX?: number;
  style?: React.CSSProperties;
}

export const WordByWordCaptions: React.FC<WordByWordCaptionsProps> = ({
  words,
  activeColor = ACTIVE_STYLE.subtitles.activeColor,
  inactiveColor = ACTIVE_STYLE.subtitles.inactiveColor,
  backgroundColor = ACTIVE_STYLE.subtitles.bgBox,
  fontSize = ACTIVE_STYLE.subtitles.fontSize,
  fontFamily = ACTIVE_STYLE.fonts.headline,
  highlightScale = 1.08,
  top,
  cameraScale = 1,
  cameraShiftX = 0,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const band = shrinkForCamera(CAPTION_RECT, cameraScale, cameraShiftX);

  const visibleWords = words.filter((w) => {
    const isAroundCurrent = frame >= w.startFrame - 15 && frame <= w.endFrame + 15;
    return isAroundCurrent;
  });

  if (visibleWords.length === 0) {
    return null;
  }

  const displayList = visibleWords;

  return (
    <div
      style={{
        position: "absolute",
        left: band.left,
        top: top ?? band.top,
        width: band.right - band.left,
        height: band.bottom - (top ?? band.top),
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        boxSizing: "border-box",
        pointerEvents: "none",
        ...style,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "12px 16px",
          maxWidth: "100%",
          boxSizing: "border-box",
          backgroundColor,
          padding: "16px 28px",
          borderRadius: 20,
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
        }}
      >
        {displayList.map((word, index) => {
          const isActive = frame >= word.startFrame && frame <= word.endFrame;

          const relFrame = Math.max(0, frame - word.startFrame);
          const pop = spring({
            frame: relFrame,
            fps,
            config: {
              damping: 12,
              stiffness: 200,
            },
          });

          const scale = isActive
            ? interpolate(pop, [0, 1], [1, highlightScale])
            : 1.0;

          return (
            <span
              key={`${word.text}-${index}-${word.startFrame}`}
              style={{
                fontFamily,
                fontSize,
                fontWeight: 900,
                textTransform: "uppercase",
                letterSpacing: "-0.01em",
                color: isActive ? activeColor : inactiveColor,
                transform: `scale(${scale})`,
                display: "inline-block",
                transition: "none",
                textShadow: isActive
                  ? `0 0 20px ${activeColor}88, 0 4px 10px rgba(0,0,0,0.8)`
                  : "0 2px 4px rgba(0,0,0,0.6)",
              }}
            >
              {word.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};
