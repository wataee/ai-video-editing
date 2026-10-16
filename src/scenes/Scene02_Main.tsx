import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ProofCard, VoxBarChart, AudioTrigger, AntiSlopOverlay, SafeZoneContainer } from "../components";
import beatSheet from "../data/beat_sheet.json";
import { BeatSheet, SceneProps } from "../types/beatSheet";

const sheet = beatSheet as unknown as BeatSheet;
const scene = sheet.scenes[1];

export const Scene02_Main: React.FC<SceneProps> = ({ renderMode = "full" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const isAlpha = renderMode === "ui_only_alpha";

  const enterProgress = spring({
    frame,
    fps,
    config: scene.spring_config,
  });

  const chartItems = (scene.chart_data || []).map((c) => ({
    label: c.label,
    value: c.value,
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
          gap: 40,
          transform: `scale(${0.92 + 0.08 * enterProgress})`,
          opacity: Math.min(1, frame / 15),
        }}
      >
        <ProofCard
          badge={scene.badge}
          title={scene.title}
          subtitle={scene.subtitle}
          enterFrame={0}
        />
        {chartItems.length > 0 && (
          <VoxBarChart
            items={chartItems}
            accentColor={sheet.global_styles.color_primary}
            startFrame={10}
            height={320}
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
