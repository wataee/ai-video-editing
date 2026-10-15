import { SfxKey } from "./assets";

export interface SfxChoreographyEvent {
  primarySfx: SfxKey;
  layer2Sfx?: SfxKey;
  timingOffsetFrames: number;
  volumeMultiplier: number;
}

export const SFX_MATRIX: Record<string, SfxChoreographyEvent> = {
  cardEntrance: {
    primarySfx: "cleanFast",
    layer2Sfx: "pop01",
    timingOffsetFrames: -2,
    volumeMultiplier: 0.35,
  },
  dataBarGrowth: {
    primarySfx: "scratch01",
    layer2Sfx: "click01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.25,
  },
  numberTickerStep: {
    primarySfx: "click02",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.18,
  },
  cameraPunchIn: {
    primarySfx: "subBassThud",
    layer2Sfx: "deepVoice01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.4,
  },
  thesisStatement: {
    primarySfx: "bassDrop01",
    layer2Sfx: "suckBack01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.45,
  },
  wordHighlight: {
    primarySfx: "select01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.15,
  },
  paperDocumentSlide: {
    primarySfx: "cameraClickFast",
    timingOffsetFrames: -1,
    volumeMultiplier: 0.3,
  },
  sceneTransition: {
    primarySfx: "syntheticTransition",
    timingOffsetFrames: -2,
    volumeMultiplier: 0.32,
  },
} as const;

export type SfxEventType = keyof typeof SFX_MATRIX;
