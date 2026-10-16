import React from "react";
import { Audio, interpolate, Sequence, staticFile } from "remotion";
import { ALL_SFX, SfxKey } from "../config/assets";

export interface SfxAudioProps {
  sfxKey?: SfxKey;
  localPath?: string;
  frame?: number;
  startFrom?: number;
  durationInFrames?: number;
  volume?: number;
  fadeInFrames?: number;
  fadeOutFrames?: number;
  playbackRate?: number;
}

const resolveLocalSfxPath = (path: string): string => {
  if (path.startsWith("http://") || path.startsWith("https://")) {
    throw new Error(`[SfxAudio Security Error] External URLs are forbidden: '${path}'. Use only local assets/sfx/.`);
  }
  const clean = path.replace(/\\/g, "/");
  if (!clean.includes("assets/sfx/")) {
    return `assets/sfx/${clean.replace(/^\/?(assets\/)?/, "")}`;
  }
  return clean;
};

export const SfxAudio: React.FC<SfxAudioProps> = ({
  sfxKey,
  localPath,
  frame = 0,
  startFrom = 0,
  durationInFrames = 60,
  volume,
  fadeInFrames = 3,
  fadeOutFrames = 5,
  playbackRate = 1.0,
}) => {
  let resolvedSrc = "";
  let baseVolume = 0.25;

  if (sfxKey && ALL_SFX[sfxKey]) {
    const asset = ALL_SFX[sfxKey];
    resolvedSrc = asset.file;
    baseVolume = volume ?? asset.defaultVolume;
  } else if (localPath) {
    const safeLocal = resolveLocalSfxPath(localPath);
    resolvedSrc = staticFile(safeLocal);
    baseVolume = volume ?? 0.25;
  } else {
    return null;
  }

  const volumeEnvelope = (f: number): number => {
    let factor = 1.0;
    if (fadeInFrames > 0 && f < fadeInFrames) {
      factor = interpolate(f, [0, fadeInFrames], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
    } else if (fadeOutFrames > 0 && f >= durationInFrames - fadeOutFrames) {
      factor = interpolate(f, [durationInFrames - fadeOutFrames, durationInFrames], [1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
    }
    return Math.max(0, Math.min(1.0, baseVolume * factor));
  };

  return (
    <Sequence from={frame} durationInFrames={durationInFrames} layout="none">
      <Audio
        src={resolvedSrc}
        startFrom={startFrom}
        volume={volumeEnvelope}
        playbackRate={playbackRate}
      />
    </Sequence>
  );
};
