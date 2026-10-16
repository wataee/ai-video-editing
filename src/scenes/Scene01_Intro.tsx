import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { HookHeadline, SpeakerBadge, AudioTrigger, AntiSlopOverlay, SafeZoneContainer } from "../components";
import beatSheet from "../data/beat_sheet.json";
import { BeatSheet, SceneProps } from "../types/beatSheet";

const sheet = beatSheet as unknown as BeatSheet;
const scene = sheet.scenes[0];

export const Scene01_Intro: React.FC<SceneProps> = ({ renderMode = "full" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const isAlpha = renderMode === "ui_only_alpha";

  const scale = spring({
    frame,
    fps,
    config: scene.spring_config,
  });

  const content = (
    <SafeZoneContainer showGuides={false}>
      <div
        style={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "120px 0",
          transform: `scale(${0.9 + 0.1 * scale})`,
          opacity: Math.min(1, frame / 15),
        }}
      >
        <HookHeadline
          headline={scene.title}
          accentWord={scene.accent_word}
          categoryBadge={scene.badge}
          enterFrame={0}
        />
        {scene.author_name && (
          <SpeakerBadge
            name={scene.author_name}
            role={scene.author_role || ""}
            enterFrame={10}
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
