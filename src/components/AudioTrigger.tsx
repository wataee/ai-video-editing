import React from "react";
import { Audio, interpolate, Sequence, staticFile } from "remotion";

export interface AudioTriggerProps {
  sample: string;
  frame?: number;
  startFrom?: number;
  durationInFrames?: number;
  volume?: number;
  fadeInFrames?: number;
  fadeOutFrames?: number;
  playbackRate?: number;
}

const resolveSfxPath = (samplePath: string): string => {
  if (samplePath.startsWith("http://") || samplePath.startsWith("https://")) {
    throw new Error(`[AudioTrigger Error] External sound URLs are forbidden: '${samplePath}'. Use local assets/sfx/.`);
  }
  const normalized = samplePath.replace(/\\/g, "/").replace(/^\/+/, "");
  if (normalized.startsWith("assets/sfx/")) {
    return normalized.replace("assets/sfx/", "sfx/");
  }
  if (normalized.startsWith("assets/sfx/")) {
    return normalized.replace("assets/sfx/", "sfx/");
  }
  if (normalized.startsWith("assets/")) {
    return normalized.replace("assets/", "");
  }
  if (normalized.startsWith("01_SFX/")) {
    return normalized.replace("01_SFX/", "sfx/");
  }
  if (normalized.startsWith("sfx/")) {
    return normalized;
  }
  return `sfx/${normalized}`;
};

export const AudioTrigger: React.FC<AudioTriggerProps> = ({
  sample,
  frame = 0,
  startFrom = 0,
  durationInFrames = 60,
  volume = 0.3,
  fadeInFrames = 2,
  fadeOutFrames = 8,
  playbackRate = 1.0,
}) => {
  const localRelative = resolveSfxPath(sample);
  const src = staticFile(localRelative);

  const calculateVolume = (currentRelFrame: number): number => {
    let scale = 1.0;
    if (fadeInFrames > 0 && currentRelFrame < fadeInFrames) {
      scale = interpolate(currentRelFrame, [0, fadeInFrames], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
    } else if (fadeOutFrames > 0 && currentRelFrame >= durationInFrames - fadeOutFrames) {
      scale = interpolate(
        currentRelFrame,
        [durationInFrames - fadeOutFrames, durationInFrames],
        [1, 0],
        {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }
      );
    }
    return Math.max(0, Math.min(1.0, volume * scale));
  };

  return (
    <Sequence from={frame} durationInFrames={durationInFrames} layout="none">
      <Audio
        src={src}
        startFrom={startFrom}
        volume={calculateVolume}
        playbackRate={playbackRate}
      />
    </Sequence>
  );
};
