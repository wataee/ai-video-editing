import React from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import {
  SafeZoneContainer,
  ProofCard,
  SpeakerBadge,
  HookHeadline,
  WordByWordCaptions,
  CaptionWord,
  ProceduralNoiseOverlay,
  SfxAudio,
} from "../components";
import { ACTIVE_STYLE } from "../config/stylePresets";

export interface ReelPlanBeat {
  beat_index: number;
  time_range: [number, number];
  line: string;
  visual: string;
  camera: string;
  proof_source?: string | null;
  accent_word?: string;
  sfx?: string;
  why?: string;
  words?: Array<{
    text: string;
    start_sec: number;
    end_sec: number;
  }>;
}

export interface ReframeKeyframe {
  frame: number;
  time_sec: number;
  x_center: number;
  y_center: number;
}

export interface ReelPlanData {
  project_id: string;
  target_duration_sec: number;
  width?: number;
  height?: number;
  fps?: number;
  sdr_path?: string;
  proxy_path?: string;
  approved?: boolean;
  style_preset?: string;
  reframe?: {
    keyframes: ReframeKeyframe[];
  };
  beats: ReelPlanBeat[];
}

export interface ReelFromPlanProps {
  plan: ReelPlanData;
  videoSrc?: string;
  reframe?: {
    keyframes: ReframeKeyframe[];
  };
  [key: string]: unknown;
}

export const calculateReelMetadata: CalculateMetadataFunction<ReelFromPlanProps> = async ({
  props,
}) => {
  const fps = props?.plan?.fps ?? 30;
  const width = props?.plan?.width ?? 1080;
  const height = props?.plan?.height ?? 1920;
  const targetDuration = props?.plan?.target_duration_sec ?? 15;
  const durationInFrames = Math.max(1, Math.round(targetDuration * fps));

  return {
    fps,
    width,
    height,
    durationInFrames,
    props,
  };
};

export const ReelFromPlan: React.FC<ReelFromPlanProps> = ({
  plan,
  videoSrc,
  reframe,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const beats = plan?.beats || [];
  const currentSec = frame / fps;
  const targetDuration = plan?.target_duration_sec || 15;

  let currentBeat = beats.find(
    (b) => currentSec >= b.time_range[0] && currentSec < b.time_range[1]
  );
  if (!currentBeat && beats.length > 0) {
    currentBeat = beats[beats.length - 1];
  }

  let cameraScale = 1.0;
  if (currentBeat) {
    const beatStartFrame = Math.round(currentBeat.time_range[0] * fps);
    const beatEndFrame = Math.round(currentBeat.time_range[1] * fps);
    const rel = Math.max(0, frame - beatStartFrame);
    const animSpan = Math.min(Math.max(1, beatEndFrame - beatStartFrame), 30);
    const p = Math.min(1.0, rel / animSpan);

    if (currentBeat.camera === "push-in") {
      cameraScale = interpolate(p, [0, 1], [1.0, ACTIVE_STYLE.camera.zoomScale]);
    } else if (currentBeat.camera === "push-out") {
      cameraScale = interpolate(p, [0, 1], [ACTIVE_STYLE.camera.zoomScale, 1.0]);
    }
  }

  const driftProgress = Math.min(1.0, currentSec / Math.max(1, targetDuration));
  const microDriftScale = interpolate(driftProgress, [0, 1], [1.0, 1.03], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const finalScale = cameraScale * microDriftScale;

  const reframeData = reframe || plan?.reframe;
  let reframeX = 50;
  let reframeY = 40;
  if (reframeData && reframeData.keyframes && reframeData.keyframes.length > 0) {
    const kfs = reframeData.keyframes;
    const nextIdx = kfs.findIndex((k) => k.frame >= frame);
    if (nextIdx === -1) {
      const last = kfs[kfs.length - 1];
      reframeX = last.x_center * 100;
      reframeY = last.y_center * 100;
    } else if (nextIdx === 0) {
      reframeX = kfs[0].x_center * 100;
      reframeY = kfs[0].y_center * 100;
    } else {
      const prev = kfs[nextIdx - 1];
      const next = kfs[nextIdx];
      const span = Math.max(1, next.frame - prev.frame);
      const factor = (frame - prev.frame) / span;
      const interpX = prev.x_center + factor * (next.x_center - prev.x_center);
      const interpY = prev.y_center + factor * (next.y_center - prev.y_center);
      reframeX = interpX * 100;
      reframeY = interpY * 100;
    }
  }

  const resolvedVideo = videoSrc || plan?.sdr_path || plan?.proxy_path;
  const cleanVideoSrc = resolvedVideo
    ? resolvedVideo.startsWith("http://") ||
      resolvedVideo.startsWith("https://") ||
      resolvedVideo.startsWith("data:")
      ? resolvedVideo
      : staticFile(resolvedVideo.replace(/\\/g, "/").replace(/^\/+/, ""))
    : null;

  return (
    <AbsoluteFill style={{ backgroundColor: ACTIVE_STYLE.colors.background }}>
      <div
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          overflow: "hidden",
          transform: `scale(${finalScale})`,
          transformOrigin: `${reframeX}% ${reframeY}%`,
        }}
      >
        {cleanVideoSrc ? (
          <OffthreadVideo
            src={cleanVideoSrc}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: `${reframeX}% ${reframeY}%`,
            }}
          />
        ) : (
          <AbsoluteFill
            style={{
              backgroundColor: ACTIVE_STYLE.colors.background,
              backgroundImage:
                "radial-gradient(circle at 50% 35%, rgba(255, 214, 10, 0.08) 0%, transparent 60%)",
            }}
          />
        )}
      </div>

      <SafeZoneContainer showGuides={false}>
        {beats.map((b) => {
          const bStartFrame = Math.round(b.time_range[0] * fps);
          const bEndFrame = Math.round(b.time_range[1] * fps);
          const bDurFrames = Math.max(1, bEndFrame - bStartFrame);

          if (b.visual === "proof") {
            if (!b.proof_source || b.proof_source.trim() === "") {
              throw new Error(
                `[ReelFromPlan Error] Beat #${b.beat_index} has visual='proof', but proof_source is missing or empty.`
              );
            }
          }

          const captionWords: CaptionWord[] = (b.words || []).map((w) => ({
            text: w.text,
            startFrame: Math.round(w.start_sec * fps),
            endFrame: Math.round(w.end_sec * fps),
          }));

          return (
            <Sequence
              key={`beat-${b.beat_index}`}
              from={bStartFrame}
              durationInFrames={bDurFrames}
            >
              <div
                style={{
                  position: "relative",
                  width: "100%",
                  height: "100%",
                }}
              >
                {b.sfx && b.sfx !== "TODO" && b.sfx.trim() !== "" && (
                  <SfxAudio
                    localPath={b.sfx}
                    frame={0}
                    durationInFrames={Math.min(bDurFrames, 90)}
                    volume={0.25}
                  />
                )}

                {b.beat_index === 0 && (
                  <div
                    style={{
                      position: "absolute",
                      top: 40,
                      left: 0,
                      right: 0,
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <HookHeadline
                      headline={b.line}
                      accentWord={b.accent_word}
                      categoryBadge="ХУК"
                      enterFrame={0}
                    />
                  </div>
                )}

                {b.visual === "proof" && b.proof_source && (
                  <div
                    style={{
                      position: "absolute",
                      top: 420,
                      left: 0,
                      right: 0,
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <ProofCard
                      badge="ДОКАЗАТЕЛЬСТВО"
                      title={b.line}
                      imageSrc={b.proof_source.replace(/\\/g, "/")}
                      enterFrame={0}
                    />
                  </div>
                )}

                {captionWords.length > 0 && (
                  <WordByWordCaptions
                    words={captionWords}
                    top={ACTIVE_STYLE.subtitles.yPos}
                  />
                )}
              </div>
            </Sequence>
          );
        })}
      </SafeZoneContainer>

      <ProceduralNoiseOverlay opacity={0.04} />
    </AbsoluteFill>
  );
};
