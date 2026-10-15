import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { AppFont, loadFont } from "./load-font";

interface WordTiming {
  text: string;
  startMs: number;
  endMs: number;
}

// Пословные метки из Whisper
const WORDS_TIMING: WordTiming[] = [
  { text: "Добро", startMs: 0, endMs: 520 },
  { text: "пожаловать", startMs: 520, endMs: 1240 },
  { text: "в", startMs: 1240, endMs: 1420 },
  { text: "рабочую", startMs: 1420, endMs: 1960 },
  { text: "станцию", startMs: 1960, endMs: 2580 },
  { text: "для", startMs: 2580, endMs: 2900 },
  { text: "монтажа", startMs: 2900, endMs: 3500 },
  { text: "видео.", startMs: 3500, endMs: 3880 },
  { text: "Современный", startMs: 4860, endMs: 5700 },
  { text: "контент", startMs: 5700, endMs: 6200 },
  { text: "требует", startMs: 6200, endMs: 6840 },
  { text: "качественного", startMs: 6840, endMs: 7760 },
  { text: "монтажа,", startMs: 7760, endMs: 8540 },
  { text: "чистого", startMs: 8800, endMs: 9340 },
  { text: "звука", startMs: 9340, endMs: 9760 },
  { text: "и", startMs: 9760, endMs: 9960 },
  { text: "точных", startMs: 9960, endMs: 10400 },
  { text: "динамических", startMs: 10400, endMs: 11200 },
  { text: "субтитров.", startMs: 11200, endMs: 12100 },
];

export const BattleTestComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  React.useEffect(() => {
    loadFont();
  }, []);

  const currentMs = (frame / fps) * 1000;

  // Определение текущей активной группы слов (синтагмы по 2-4 слова)
  const currentChunk = useMemo(() => {
    if (currentMs < 3900) {
      // Chunk 1
      return WORDS_TIMING.slice(0, 8);
    } else if (currentMs < 8700) {
      // Chunk 2
      return WORDS_TIMING.slice(8, 13);
    } else {
      // Chunk 3
      return WORDS_TIMING.slice(13, 19);
    }
  }, [currentMs]);

  // Spring анимация для Split Screen нижней карточки
  const splitEntrance = spring({
    frame: frame - 114, // стартует на 3.8s
    fps,
    config: { damping: 15, mass: 0.7, stiffness: 130 },
  });

  const cardTranslateY = interpolate(splitEntrance, [0, 1], [300, 0]);
  const cardOpacity = interpolate(splitEntrance, [0, 0.4], [0, 1], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  // Zoom в сцене 1 (0..114)
  const scene1Scale = interpolate(frame, [0, 114], [1.0, 1.05], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#09090B", fontFamily: AppFont }}>
      {/* -------------------- 1. ВИЗУАЛЬНЫЙ СЛОЙ (СЦЕНЫ) -------------------- */}

      {/* СЦЕНА 1: Fullscreen A-Roll + Slow Zoom (0.0s - 3.8s / Кадры 0 - 114) */}
      <Sequence from={0} durationInFrames={114}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("russian_ref_15s.mp4")}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${scene1Scale})`,
            }}
          />
          {/* Subtle Grid Overlay */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage: `url(${staticFile("overlays/tech_grid.svg")})`,
              backgroundSize: "cover",
              opacity: 0.12,
              pointerEvents: "none",
            }}
          />
          {/* Верхний статус-бейджик */}
          <div
            style={{
              position: "absolute",
              top: 180,
              left: "50%",
              transform: "translateX(-50%)",
              padding: "8px 18px",
              backgroundColor: "rgba(0,0,0,0.65)",
              border: "1px solid rgba(255,255,255,0.15)",
              borderRadius: 30,
              backdropFilter: "blur(12px)",
              color: "#A1A1AA",
              fontSize: 18,
              fontWeight: 800,
              letterSpacing: 2,
              textTransform: "uppercase",
            }}
          >
            ⚡ SYSTEM ONLINE // PRO
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* СЦЕНА 2: SPLIT SCREEN (Joseph Eid Viral Layout) (3.8s - 8.8s / Кадры 114 - 264) */}
      <Sequence from={114} durationInFrames={150}>
        <AbsoluteFill style={{ backgroundColor: "#09090B" }}>
          {/* Верхняя половина: Спикер крупным планом (52% высоты) */}
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: height * 0.52,
              overflow: "hidden",
            }}
          >
            <OffthreadVideo
              src={staticFile("russian_ref_15s.mp4")}
              startFrom={114}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                transform: "scale(1.15)", // Punch-in
              }}
            />
          </div>

          {/* Неоновый разделитель */}
          <div
            style={{
              position: "absolute",
              top: height * 0.52 - 1,
              left: 0,
              width: "100%",
              height: 2,
              backgroundColor: "rgba(250, 204, 21, 0.4)", // Желтый акцент
              boxShadow: "0 0 16px rgba(250, 204, 21, 0.6)",
              zIndex: 10,
            }}
          />

          {/* Нижняя половина: Карточка доказательства (Dark Glass Card) */}
          <div
            style={{
              position: "absolute",
              top: height * 0.52,
              left: 0,
              width: "100%",
              height: height * 0.48,
              display: "flex",
              justifyContent: "center",
              alignItems: "flex-start",
              padding: "40px 40px 390px 40px",
              boxSizing: "border-box",
              backgroundColor: "#0C0D0E",
            }}
          >
            <div
              style={{
                transform: `translateY(${cardTranslateY}px)`,
                opacity: cardOpacity,
                width: "100%",
                padding: "36px 32px",
                borderRadius: 24,
                backgroundColor: "rgba(24, 24, 27, 0.95)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.7)",
                display: "flex",
                flexDirection: "column",
                gap: 16,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <span
                  style={{
                    backgroundColor: "#FACC15",
                    color: "#000000",
                    fontWeight: 900,
                    fontSize: 16,
                    padding: "4px 12px",
                    borderRadius: 6,
                    letterSpacing: 1.2,
                  }}
                >
                  ПРАВИЛО №1
                </span>
                <span style={{ color: "#71717A", fontSize: 16, fontWeight: 700 }}>
                  HUMAN EDITING
                </span>
              </div>
              <div
                style={{
                  fontSize: 34,
                  fontWeight: 900,
                  color: "#FFFFFF",
                  lineHeight: 1.2,
                }}
              >
                КАЧЕСТВО &gt; НЕЙРОСЛОП
              </div>
              <div
                style={{
                  fontSize: 20,
                  color: "#A1A1AA",
                  lineHeight: 1.4,
                  display: "flex",
                  flexDirection: "column",
                  gap: 8,
                }}
              >
                <div>✓ 3-уровневый саунд-дизайн (-14 LUFS)</div>
                <div>✓ Никаких пляшущих эмодзи и зумов</div>
              </div>
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* СЦЕНА 3: Fullscreen Proof + Polish (8.8s - 13.0s / Кадры 264 - 390) */}
      <Sequence from={264} durationInFrames={126}>
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <OffthreadVideo
            src={staticFile("russian_ref_15s.mp4")}
            startFrom={264}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </AbsoluteFill>
      </Sequence>

      {/* -------------------- 2. ДИНАМИЧЕСКИЕ СУБТИТРЫ (SAFE ZONES) -------------------- */}
      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          bottom: currentMs >= 3900 && currentMs < 8700 ? 1100 : 380, // Поднимаем титры над сплит-экраном
          display: "flex",
          justifyContent: "center",
          flexWrap: "wrap",
          gap: "10px 18px",
          textAlign: "center",
          pointerEvents: "none",
          zIndex: 50,
          transition: "bottom 0.2s ease-out",
        }}
      >
        {currentChunk.map((w, idx) => {
          const isActive = currentMs >= w.startMs && currentMs <= w.endMs;
          return (
            <span
              key={idx}
              style={{
                fontSize: 60,
                fontWeight: 900,
                textTransform: "uppercase",
                color: isActive ? "#FACC15" : "#FFFFFF",
                transform: isActive ? "scale(1.08)" : "scale(1.0)",
                textShadow: isActive
                  ? "0 4px 24px rgba(250, 204, 21, 0.6), 0 2px 6px #000000"
                  : "0 3px 16px rgba(0,0,0,0.9)",
                display: "inline-block",
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>

      {/* -------------------- 3. САУНД-ДИЗАЙН (SFX LAYERS) -------------------- */}
      {/* 1. Whoosh на старте (0.0s) */}
      <Sequence from={0} durationInFrames={30}>
        <Audio src={staticFile("sfx/whoosh_clean_fast.wav")} volume={0.2} />
      </Sequence>

      {/* 2. Sub-bass панч на слове "видео" (3.5s = Кадр 105) */}
      <Sequence from={105} durationInFrames={45}>
        <Audio src={staticFile("sfx/sub_bass_thud.wav")} volume={0.35} />
      </Sequence>

      {/* 3. Whoosh на переход в Split Screen (3.8s = Кадр 114) */}
      <Sequence from={114} durationInFrames={30}>
        <Audio src={staticFile("sfx/whoosh_clean_fast.wav")} volume={0.25} />
      </Sequence>

      {/* 4. Glass Pop на слове "чистого звука" (8.8s = Кадр 264) */}
      <Sequence from={264} durationInFrames={30}>
        <Audio src={staticFile("sfx/glass_pop.wav")} volume={0.3} />
      </Sequence>

      {/* 5. Crisp Click на "динамических субтитров" (10.4s = Кадр 312) */}
      <Sequence from={312} durationInFrames={20}>
        <Audio src={staticFile("sfx/click_01.wav")} volume={0.25} />
      </Sequence>
    </AbsoluteFill>
  );
};
