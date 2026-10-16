import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { SafeZoneContainer } from "./SafeZoneContainer";
import { LiquidGlassCard } from "./LiquidGlassCard";
import { VoxBarChart } from "./VoxBarChart";

export interface PlanBeatProps {
  beatIndex: number;
  timeRange: [number, number];
  line: string;
  visual: "speaker" | "proof" | "typography" | "chart" | "broll" | string;
  camera: "static" | "push-in" | "push-out" | "pan-left" | "pan-right" | string;
  proofSource?: string | null;
  sfx?: string;
  why?: string;
  frameImagePath?: string;
}

export const PlanBeatStill: React.FC<PlanBeatProps> = ({
  beatIndex = 0,
  timeRange = [0, 3],
  line = "Пример реплики спикера для раскадровки",
  visual = "speaker",
  camera = "push-in",
  proofSource = null,
  sfx = "hits/sub_bass_thud",
  why = "Хук привлекает внимание спикером",
  frameImagePath,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#09090B", overflow: "hidden" }}>
      {frameImagePath ? (
        <Img
          src={frameImagePath.startsWith("http") || frameImagePath.startsWith("data:") ? frameImagePath : staticFile(frameImagePath)}
          style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: visual === "typography" ? 0.35 : 0.85,
          }}
        />
      ) : (
        <AbsoluteFill
          style={{
            background: "radial-gradient(circle at 50% 40%, #1A1A24 0%, #09090B 100%)",
          }}
        />
      )}

      <SafeZoneContainer showGuides={true}>
        <div
          style={{
            height: "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            padding: "24px 0",
            boxSizing: "border-box",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              backgroundColor: "rgba(0, 0, 0, 0.75)",
              backdropFilter: "blur(12px)",
              padding: "12px 20px",
              borderRadius: 16,
              border: "1px solid rgba(255, 255, 255, 0.15)",
              color: "#FFFFFF",
              fontFamily: "Inter, sans-serif",
            }}
          >
            <div>
              <span style={{ fontWeight: 800, color: "#FFD60A", fontSize: 24, marginRight: 12 }}>
                BEAT #{beatIndex}
              </span>
              <span style={{ fontSize: 20, color: "rgba(255, 255, 255, 0.7)" }}>
                {timeRange[0].toFixed(1)}s – {timeRange[1].toFixed(1)}s
              </span>
            </div>
            <div style={{ display: "flex", gap: 10 }}>
              <span
                style={{
                  backgroundColor: visual === "typography" ? "#FF453A" : visual === "chart" ? "#30D158" : "#0A84FF",
                  padding: "6px 14px",
                  borderRadius: 10,
                  fontSize: 16,
                  fontWeight: 700,
                  textTransform: "uppercase",
                }}
              >
                {visual}
              </span>
              <span
                style={{
                  backgroundColor: "rgba(255, 255, 255, 0.15)",
                  padding: "6px 14px",
                  borderRadius: 10,
                  fontSize: 16,
                  fontWeight: 600,
                }}
              >
                {camera}
              </span>
            </div>
          </div>

          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              margin: "30px 0",
            }}
          >
            {visual === "chart" && (
              <LiquidGlassCard
                badge="PROOF / CHART"
                title="Аналитический график"
                subtitle={proofSource ? `Источник: ${proofSource}` : "Демонстрация динамики конверсии"}
                enterFrame={0}
              >
                <VoxBarChart
                  items={[
                    { label: "До", value: 38, formattedValue: "38%" },
                    { label: "После", value: 89, formattedValue: "+89%", color: "#30D158" },
                  ]}
                  height={240}
                  startFrame={0}
                />
              </LiquidGlassCard>
            )}

            {visual === "proof" && (
              <LiquidGlassCard
                badge="VERIFIED PROOF"
                title="Доказательство тезиса"
                subtitle={proofSource ? proofSource : "Реальный скриншот метрики"}
                enterFrame={0}
              >
                <div
                  style={{
                    backgroundColor: "rgba(255, 255, 255, 0.05)",
                    border: "1px dashed rgba(255, 255, 255, 0.25)",
                    borderRadius: 14,
                    padding: "36px 20px",
                    textAlign: "center",
                    color: "rgba(255, 255, 255, 0.8)",
                    fontSize: 20,
                    fontFamily: "Inter, sans-serif",
                  }}
                >
                  {proofSource ? `[Вставка артефакта: ${proofSource}]` : "[Скриншот продукта / аналитики]"}
                </div>
              </LiquidGlassCard>
            )}

            {visual === "typography" && (
              <div
                style={{
                  backgroundColor: "rgba(10, 10, 14, 0.9)",
                  border: "2px solid #FFD60A",
                  borderRadius: 24,
                  padding: "40px 32px",
                  textAlign: "center",
                  maxWidth: "90%",
                  boxShadow: "0 20px 60px rgba(0,0,0,0.8)",
                }}
              >
                <div
                  style={{
                    fontFamily: "Montserrat, sans-serif",
                    fontWeight: 900,
                    fontSize: 52,
                    lineHeight: 1.15,
                    color: "#FFFFFF",
                    textTransform: "uppercase",
                  }}
                >
                  {line}
                </div>
              </div>
            )}

            {visual === "speaker" && (
              <div
                style={{
                  border: "2px dashed rgba(255, 255, 255, 0.2)",
                  borderRadius: 20,
                  padding: "20px 30px",
                  backgroundColor: "rgba(0, 0, 0, 0.4)",
                  color: "rgba(255, 255, 255, 0.6)",
                  fontSize: 22,
                  fontFamily: "Inter, sans-serif",
                }}
              >
                [ФОКУС НА СПИКЕРЕ — {camera.toUpperCase()}]
              </div>
            )}

            {visual === "broll" && (
              <div
                style={{
                  border: "2px dashed #0A84FF",
                  borderRadius: 20,
                  padding: "24px 36px",
                  backgroundColor: "rgba(10, 132, 255, 0.15)",
                  color: "#FFFFFF",
                  fontSize: 24,
                  fontFamily: "Inter, sans-serif",
                  textAlign: "center",
                }}
              >
                [B-ROLL МАТЕРИАЛ]
                <div style={{ fontSize: 16, marginTop: 8, color: "rgba(255,255,255,0.7)" }}>
                  {proofSource || "Кадры работы / рабочего стола"}
                </div>
              </div>
            )}
          </div>

          <div
            style={{
              backgroundColor: "rgba(0, 0, 0, 0.82)",
              backdropFilter: "blur(16px)",
              padding: "20px 24px",
              borderRadius: 20,
              border: "1px solid rgba(255, 255, 255, 0.12)",
            }}
          >
            <div
              style={{
                fontFamily: "Manrope, sans-serif",
                fontSize: 26,
                fontWeight: 700,
                color: "#FFFFFF",
                lineHeight: 1.35,
                textAlign: "center",
                marginBottom: 10,
              }}
            >
              «{line}»
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: 16,
                color: "rgba(255, 255, 255, 0.6)",
                fontFamily: "Inter, sans-serif",
                borderTop: "1px solid rgba(255, 255, 255, 0.1)",
                paddingTop: 10,
              }}
            >
              <span>SFX: <strong style={{ color: "#FFD60A" }}>{sfx}</strong></span>
              <span>Мотив: <strong>{why}</strong></span>
            </div>
          </div>
        </div>
      </SafeZoneContainer>
    </AbsoluteFill>
  );
};
