import React from "react";
import { Composition, AbsoluteFill } from "remotion";
import {
  SafeZoneContainer,
  CameraRig,
  LiquidGlassCard,
  VoxBarChart,
  NumberTicker,
  WordByWordCaptions,
  SfxTrigger,
} from "./components";

const MainComposition: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#09090B" }}>
      <SfxTrigger sfxKey="bassDrop01" frame={0} />
      <SfxTrigger sfxKey="cleanFast" frame={15} />

      <CameraRig motion="push-in" intensity={1.0}>
        <SafeZoneContainer showGuides={false}>
          <div
            style={{
              height: "100%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "20px 0",
            }}
          >
            <div style={{ textAlign: "center", marginTop: 40 }}>
              <NumberTicker
                from={0}
                to={4820000}
                prefix="$"
                fontSize={84}
                color="#FFD60A"
              />
              <div
                style={{
                  fontSize: 26,
                  fontFamily: "Inter, sans-serif",
                  fontWeight: 600,
                  color: "rgba(255, 255, 255, 0.7)",
                  marginTop: 8,
                }}
              >
                CAPITAL ALLOCATED IN Q3
              </div>
            </div>

            <LiquidGlassCard
              badge="VERIFIED METRIC"
              title="Growth Velocity"
              subtitle="Quarterly transaction volume across 12 markets."
              enterFrame={10}
            >
              <VoxBarChart
                items={[
                  { label: "Q1", value: 34, formattedValue: "+34%" },
                  { label: "Q2", value: 62, formattedValue: "+62%" },
                  { label: "Q3", value: 94, formattedValue: "+94%", color: "#FF3B30" },
                ]}
                height={260}
                startFrame={25}
              />
            </LiquidGlassCard>

            <WordByWordCaptions
              words={[
                { text: "LOOK", startFrame: 0, endFrame: 15 },
                { text: "AT", startFrame: 16, endFrame: 25 },
                { text: "THESE", startFrame: 26, endFrame: 40 },
                { text: "NUMBERS", startFrame: 41, endFrame: 70 },
                { text: "RIGHT", startFrame: 71, endFrame: 90 },
                { text: "NOW", startFrame: 91, endFrame: 120 },
              ]}
              activeColor="#FF3B30"
            />
          </div>
        </SafeZoneContainer>
      </CameraRig>
    </AbsoluteFill>
  );
};

const GreenScreenComposition: React.FC<{ chromaMode?: boolean }> = ({
  chromaMode = true,
}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: chromaMode ? "#00FF00" : "transparent",
      }}
    >
      <SafeZoneContainer>
        <div
          style={{
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <LiquidGlassCard
            badge="OVERLAY"
            title="Liquid Glass Modal"
            subtitle="Extracted alpha layer for NLE composite."
            chromaMode={chromaMode}
            enterFrame={5}
          />
        </div>
      </SafeZoneContainer>
    </AbsoluteFill>
  );
};

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="Main"
        component={MainComposition}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="GreenScreenOverlay"
        component={GreenScreenComposition}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          chromaMode: true,
        }}
      />
    </>
  );
};
