import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ProofCard, WordByWordCaptions, AudioTrigger, AntiSlopOverlay, SafeZoneContainer } from "../components";
import beatSheet from "../data/beat_sheet.json";
import { BeatSheet, SceneProps } from "../types/beatSheet";

const sheet = beatSheet as unknown as BeatSheet;
const scene = sheet.scenes[2];

export const Scene03_Outro: React.FC<SceneProps> = ({ renderMode = "full" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const isAlpha = renderMode === "ui_only_alpha";

  const scale = spring({
    frame,
    fps,
    config: scene.spring_config,
  });

  const captions = (scene.captions || []).map((c) => ({
    text: c.text,
    startFrame: c.start_frame,
    endFrame: c.end_frame,
  }));

  const content = (
    <SafeZoneContainer showGuides={false}>
      <div
        style={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 60,
          transform: `scale(${0.9 + 0.1 * scale})`,
          opacity: Math.min(1, frame / 15),
        }}
      >
        <ProofCard
          badge={scene.badge}
          title={scene.title}
          subtitle={scene.subtitle}
          enterFrame={0}
        />
        {captions.length > 0 && (
          <WordByWordCaptions
            words={captions}
            top={1380}
            style={{ width: "100%" }}
          />
        )}
      </div>
    </SafeZoneContainer>
  );

  if (isAlpha) {
    return <AbsoluteFill style={{ backgroundColor: "transparent" }}>{content}</AbsoluteFill>;
  }

  return (
    <AntiSlopOverlay grainOpacity={0.04} driftScale={1.03}>
      {scene.sfx && <AudioTrigger sample={scene.sfx.sample} frame={scene.sfx.frame_offset} />}
      <AbsoluteFill style={{ backgroundColor: sheet.global_styles.color_background }}>
        {content}
      </AbsoluteFill>
    </AntiSlopOverlay>
  );
};
