import { SfxKey } from "./assets";

export interface SfxChoreographyEvent {
  primarySfx: SfxKey | null;
  layer2Sfx?: SfxKey;
  timingOffsetFrames: number;
  volumeMultiplier: number;
}

export const SFX_MATRIX: Record<string, SfxChoreographyEvent> = {
  cardEntrance: {
    primarySfx: "cleanFast",
    layer2Sfx: "pop01",
    timingOffsetFrames: -2,
    volumeMultiplier: 0.15,
  },
  dataBarGrowth: {
    primarySfx: "scratch01",
    layer2Sfx: "click01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.15,
  },
  numberTickerStep: {
    primarySfx: "click02",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.12,
  },
  cameraPunchIn: {
    primarySfx: null,
    timingOffsetFrames: 0,
    volumeMultiplier: 0.0,
  },
  thesisStatement: {
    primarySfx: "bassDrop01",
    layer2Sfx: "suckBack01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.20,
  },
  wordHighlight: {
    primarySfx: "select01",
    timingOffsetFrames: 0,
    volumeMultiplier: 0.12,
  },
  paperDocumentSlide: {
    primarySfx: "cameraClickFast",
    timingOffsetFrames: -1,
    volumeMultiplier: 0.15,
  },
  sceneTransition: {
    primarySfx: "syntheticTransition",
    timingOffsetFrames: -2,
    volumeMultiplier: 0.10,
  },
} as const;

export type SfxEventType = keyof typeof SFX_MATRIX;
