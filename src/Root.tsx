import React from "react";
import { Composition, AbsoluteFill, Sequence } from "remotion";
import {
  SafeZoneContainer,
  LiquidGlassCard,
  ProofCard,
  SpeakerBadge,
  HookHeadline,
} from "./components";
import { Scene01_Intro, Scene02_Main, Scene03_Outro } from "./scenes";
import beatSheet from "./data/beat_sheet.json";
import { BeatSheet } from "./types/beatSheet";
import { loadProjectFonts } from "./config";

loadProjectFonts();

const sheet = beatSheet as unknown as BeatSheet;

const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: sheet.global_styles.color_background }}>
      <Sequence from={0} durationInFrames={180}>
        <Scene01_Intro renderMode="full" />
      </Sequence>
      <Sequence from={180} durationInFrames={240}>
        <Scene02_Main renderMode="full" />
      </Sequence>
      <Sequence from={420} durationInFrames={180}>
        <Scene03_Outro renderMode="full" />
      </Sequence>
    </AbsoluteFill>
  );
};

const Scene01StemsComp: React.FC = () => <Scene01_Intro renderMode="ui_only_alpha" />;
const Scene02StemsComp: React.FC = () => <Scene02_Main renderMode="ui_only_alpha" />;
const Scene03StemsComp: React.FC = () => <Scene03_Outro renderMode="ui_only_alpha" />;

const GreenScreenComposition: React.FC<{ chromaMode?: boolean }> = ({ chromaMode = true }) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: chromaMode ? "#00FF00" : "transparent",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <SafeZoneContainer showGuides={false}>
        <LiquidGlassCard
          badge="ГИБРИДНЫЙ ЭКСПОРТ"
          title="Стемы в ProRes 4444"
          subtitle="Чистый прозрачный UI без потерь качества"
          width={860}
        />
      </SafeZoneContainer>
    </AbsoluteFill>
  );
};

const PreviewProofCardComp: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#08090C", display: "flex", alignItems: "center", justifyContent: "center" }}>
    <SafeZoneContainer showGuides={true}>
      <ProofCard
        badge="ДОКАЗАТЕЛЬСТВО"
        title="Метрики проверены"
        subtitle="Аудит показал рост удержания на 42%"
      />
    </SafeZoneContainer>
  </AbsoluteFill>
);

const PreviewSpeakerBadgeComp: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#08090C", display: "flex", alignItems: "center", justifyContent: "center" }}>
    <SafeZoneContainer showGuides={true}>
      <SpeakerBadge name="ТИМУР ВАТАЕВ" role="MOTION DIRECTOR" />
    </SafeZoneContainer>
  </AbsoluteFill>
);

const PreviewHookHeadlineComp: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#08090C", display: "flex", alignItems: "center", justifyContent: "center" }}>
    <SafeZoneContainer showGuides={true}>
      <HookHeadline headline="ГЛАВНЫЙ СЕКРЕТ МОНТАЖА В 2026 ГОДУ" accentWord="СЕКРЕТ" categoryBadge="РАЗБОР" />
    </SafeZoneContainer>
  </AbsoluteFill>
);

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="Main"
        component={MainVideo}
        durationInFrames={600}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="Scene01-Intro"
        component={Scene01_Intro}
        durationInFrames={180}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{ renderMode: "full" as const }}
      />
      <Composition
        id="Scene02-Main"
        component={Scene02_Main}
        durationInFrames={240}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{ renderMode: "full" as const }}
      />
      <Composition
        id="Scene03-Outro"
        component={Scene03_Outro}
        durationInFrames={180}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{ renderMode: "full" as const }}
      />
      <Composition
        id="Scene01-Stems"
        component={Scene01StemsComp}
        durationInFrames={180}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="Scene02-Stems"
        component={Scene02StemsComp}
        durationInFrames={240}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="Scene03-Stems"
        component={Scene03StemsComp}
        durationInFrames={180}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="GreenScreenOverlay"
        component={GreenScreenComposition}
        durationInFrames={180}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{ chromaMode: true }}
      />
      <Composition
        id="PreviewProofCard"
        component={PreviewProofCardComp}
        durationInFrames={60}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="PreviewSpeakerBadge"
        component={PreviewSpeakerBadgeComp}
        durationInFrames={60}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="PreviewHookHeadline"
        component={PreviewHookHeadlineComp}
        durationInFrames={60}
        fps={60}
        width={1080}
        height={1920}
      />
    </>
  );
};
