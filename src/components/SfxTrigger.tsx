import React from "react";
import { Audio, Sequence } from "remotion";
import { ALL_SFX, SfxKey } from "../config/assets";

export interface SfxTriggerProps {
  sfxKey?: SfxKey;
  src?: string;
  frame?: number;
  volume?: number;
  playbackRate?: number;
}

export const SfxTrigger: React.FC<SfxTriggerProps> = ({
  sfxKey,
  src,
  frame = 0,
  volume,
  playbackRate = 1,
}) => {
  const asset = sfxKey ? ALL_SFX[sfxKey] : undefined;
  const audioSrc = src ?? asset?.file;

  if (!audioSrc) {
    return null;
  }

  const finalVolume = volume ?? asset?.defaultVolume ?? 0.3;

  return (
    <Sequence from={frame} durationInFrames={120} layout="none">
      <Audio src={audioSrc} volume={finalVolume} playbackRate={playbackRate} />
    </Sequence>
  );
};
