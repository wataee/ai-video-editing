export interface StyleTokens {
  id: string;
  name: string;
  description: string;
  colors: {
    background: string;
    card: string;
    cardBorder: string;
    textPrimary: string;
    textSecondary: string;
    accent: string;
    accentSecondary: string;
    shadow: string;
  };
  fonts: {
    headline: string;
    body: string;
    accentScript: string;
  };
  subtitles: {
    wordsPerChunk: number;
    yPos: number;
    activeColor: string;
    inactiveColor: string;
    bgBox: string;
    backdropBlur: string;
    fontSize: number;
  };
  camera: {
    zoomScale: number;
    durationFrames: number;
    motion: "push-in" | "push-out" | "pan-left" | "pan-right" | "static-fade";
    easing: string;
  };
  audio: {
    sfxHitsDb: number;
    sfxTexturesDb: number;
    sfxWhooshesDb: number;
    musicDb: number;
    maxSfxPer30s: number;
  };
  safeZones: {
    top: number;
    bottom: number;
    left: number;
    right: number;
  };
}

export const STYLE_PRESETS: Record<string, StyleTokens> = {
  "editorial-authority": {
    id: "editorial-authority",
    name: "Editorial Authority",
    description: "Премиальный аналитический стиль: глубокий темный цинк, матовое стекло, Montserrat + Manrope, желтый акцент",
    colors: {
      background: "#09090B",
      card: "rgba(18, 18, 24, 0.85)",
      cardBorder: "rgba(255, 255, 255, 0.14)",
      textPrimary: "#F4F4F5",
      textSecondary: "rgba(244, 244, 245, 0.65)",
      accent: "#FFD60A",
      accentSecondary: "#30D158",
      shadow: "0 24px 60px rgba(0, 0, 0, 0.65)",
    },
    fonts: {
      headline: "Montserrat, sans-serif",
      body: "Manrope, sans-serif",
      accentScript: "Caveat, cursive",
    },
    subtitles: {
      wordsPerChunk: 3,
      yPos: 1220,
      activeColor: "#FFD60A",
      inactiveColor: "#F4F4F5",
      bgBox: "rgba(9, 9, 11, 0.85)",
      backdropBlur: "16px",
      fontSize: 34,
    },
    camera: {
      zoomScale: 1.07,
      durationFrames: 14,
      motion: "push-in",
      easing: "power2.out",
    },
    audio: {
      sfxHitsDb: -14.0,
      sfxTexturesDb: -16.0,
      sfxWhooshesDb: -20.0,
      musicDb: -24.0,
      maxSfxPer30s: 5,
    },
    safeZones: {
      top: 220,
      bottom: 380,
      left: 100,
      right: 130,
    },
  },
  "nordic-minimalist": {
    id: "nordic-minimalist",
    name: "Nordic Minimalist",
    description: "Аскетичный швейцарский минимализм: глубокий черный OLED, чистый Inter, без лишних плашек, зеленый статус",
    colors: {
      background: "#000000",
      card: "rgba(12, 12, 12, 0.95)",
      cardBorder: "rgba(255, 255, 255, 0.1)",
      textPrimary: "#FFFFFF",
      textSecondary: "rgba(255, 255, 255, 0.6)",
      accent: "#30D158",
      accentSecondary: "#0A84FF",
      shadow: "0 10px 30px rgba(0, 0, 0, 0.8)",
    },
    fonts: {
      headline: "Inter, sans-serif",
      body: "Inter, sans-serif",
      accentScript: "Caveat, cursive",
    },
    subtitles: {
      wordsPerChunk: 4,
      yPos: 1280,
      activeColor: "#FFFFFF",
      inactiveColor: "rgba(255, 255, 255, 0.5)",
      bgBox: "transparent",
      backdropBlur: "0px",
      fontSize: 32,
    },
    camera: {
      zoomScale: 1.04,
      durationFrames: 24,
      motion: "push-in",
      easing: "linear",
    },
    audio: {
      sfxHitsDb: -14.0,
      sfxTexturesDb: -18.0,
      sfxWhooshesDb: -22.0,
      musicDb: -28.0,
      maxSfxPer30s: 2,
    },
    safeZones: {
      top: 220,
      bottom: 380,
      left: 100,
      right: 130,
    },
  },
};

export const ACTIVE_STYLE: StyleTokens = STYLE_PRESETS["editorial-authority"];

export const FORBIDDEN_FONTS = ["Arial", "Roboto", "Times New Roman", "Comic Sans", "system-ui"] as const;

export const ALLOWED_LOCAL_FONTS = [
  "Montserrat",
  "Inter",
  "Unbounded",
  "Manrope",
  "Oswald",
  "Rubik",
  "Caveat",
  "Segoe Script",
] as const;

export const assertValidFont = (fontName: string): void => {
  for (const forbidden of FORBIDDEN_FONTS) {
    if (fontName.toLowerCase().includes(forbidden.toLowerCase())) {
      throw new Error(
        `[Typography Violation] Font '${fontName}' is strictly prohibited. Use only local fonts from assets/fonts/ (${ALLOWED_LOCAL_FONTS.join(", ")}).`
      );
    }
  }
};
