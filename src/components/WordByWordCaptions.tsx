import React from "react";
import { useCurrentFrame } from "remotion";

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
  style?: React.CSSProperties;
}

export const WordByWordCaptions: React.FC<WordByWordCaptionsProps> = ({
  words,
  activeColor = "#FFD60A",
  inactiveColor = "#FFFFFF",
  backgroundColor = "rgba(0, 0, 0, 0.45)",
  fontSize = 52,
  fontFamily = "Montserrat, sans-serif",
  highlightScale = 1.08,
  style,
}) => {
  const frame = useCurrentFrame();

  const visibleWords = words.filter((w) => {
    const isAroundCurrent = frame >= w.startFrame - 15 && frame <= w.endFrame + 15;
    return isAroundCurrent;
  });

  const displayList = visibleWords.length > 0 ? visibleWords : words.slice(0, 4);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 400,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 40px",
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
          maxWidth: 860,
          backgroundColor,
          padding: "16px 28px",
          borderRadius: 20,
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
        }}
      >
        {displayList.map((word, index) => {
          const isActive = frame >= word.startFrame && frame <= word.endFrame;
          const isPast = frame > word.endFrame;

          return (
            <span
              key={`${word.text}-${index}-${word.startFrame}`}
              style={{
                fontSize,
                fontFamily,
                fontWeight: 900,
                textTransform: "uppercase",
                letterSpacing: "-0.01em",
                color: isActive ? activeColor : inactiveColor,
                opacity: isActive ? 1.0 : isPast ? 0.75 : 0.5,
                transform: isActive ? `scale(${highlightScale})` : "scale(1.0)",
                transformOrigin: "center bottom",
                display: "inline-block",
                transition: "none",
                textShadow: isActive
                  ? `0 0 20px ${activeColor}88, 0 4px 12px rgba(0,0,0,0.8)`
                  : "0 4px 12px rgba(0,0,0,0.8)",
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
