import React from "react";
import { Audio, Sequence, useVideoConfig } from "remotion";
import { ALL_SFX, SfxKey } from "../config/assets";

export interface SfxTriggerProps {
  sfxKey?: SfxKey;
  src?: string;
  frame?: number;
  volume?: number;
  playbackRate?: number;
  maxSeconds?: number;
}

export const SfxTrigger: React.FC<SfxTriggerProps> = ({
  sfxKey,
  src,
  frame = 0,
  volume,
  playbackRate = 1,
  maxSeconds = 8,
}) => {
  const { fps } = useVideoConfig();
  const asset = sfxKey ? ALL_SFX[sfxKey] : undefined;
  const audioSrc = src ?? asset?.file;

  if (!audioSrc) {
    return null;
  }

  const finalVolume = volume ?? asset?.defaultVolume ?? 0.3;

  return (
    <Sequence from={frame} durationInFrames={Math.ceil(maxSeconds * fps)} layout="none">
      <Audio src={audioSrc} volume={finalVolume} playbackRate={playbackRate} />
    </Sequence>
  );
};
