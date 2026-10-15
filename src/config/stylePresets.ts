export interface StylePreset {
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
    accentSecondary?: string;
  };
  fonts: {
    primary: string;
    secondary: string;
    accentScript?: string;
  };
  cameraDefault: "push-in" | "push-out" | "pan-left" | "pan-right" | "static-fade";
  springConfig: {
    damping: number;
    stiffness: number;
    mass: number;
  };
}

export const STYLE_PRESETS: Record<string, StylePreset> = {
  "ali-minimal-workspace": {
    id: "ali-minimal-workspace",
    name: "Ali Minimal Workspace",
    description: "Approachable intellectual productivity with clean cards and warm lighting",
    colors: {
      background: "#F9F9F8",
      card: "#FFFFFF",
      cardBorder: "rgba(0, 0, 0, 0.08)",
      textPrimary: "#18181B",
      textSecondary: "#71717A",
      accent: "#3B82F6",
      accentSecondary: "#FF6B6B",
    },
    fonts: {
      primary: "Inter, sans-serif",
      secondary: "Inter, sans-serif",
    },
    cameraDefault: "push-in",
    springConfig: {
      damping: 20,
      stiffness: 80,
      mass: 1.0,
    },
  },
  "gadzhi-noir-luxury": {
    id: "gadzhi-noir-luxury",
    name: "Gadzhi Noir Luxury",
    description: "High-status financial documentary aesthetic with obsidian tones and gold script",
    colors: {
      background: "#070709",
      card: "rgba(18, 18, 22, 0.85)",
      cardBorder: "rgba(255, 255, 255, 0.14)",
      textPrimary: "#FFFFFF",
      textSecondary: "#A1A1AA",
      accent: "#D4AF37",
      accentSecondary: "#10B981",
    },
    fonts: {
      primary: "Montserrat, sans-serif",
      secondary: "Inter, sans-serif",
      accentScript: "Caveat, cursive",
    },
    cameraDefault: "push-in",
    springConfig: {
      damping: 15,
      stiffness: 95,
      mass: 1.0,
    },
  },
  "vox-editorial-data": {
    id: "vox-editorial-data",
    name: "Vox Editorial Data",
    description: "Documentary data journalism with metric grids, high-contrast yellow accents and charts",
    colors: {
      background: "#0D0D11",
      card: "rgba(22, 22, 28, 0.9)",
      cardBorder: "rgba(255, 255, 255, 0.16)",
      textPrimary: "#FFFFFF",
      textSecondary: "#CCCCCC",
      accent: "#FFD60A",
      accentSecondary: "#FF3B30",
    },
    fonts: {
      primary: "Oswald, sans-serif",
      secondary: "Inter, sans-serif",
    },
    cameraDefault: "static-fade",
    springConfig: {
      damping: 14,
      stiffness: 110,
      mass: 0.8,
    },
  },
  "apple-liquid-glass": {
    id: "apple-liquid-glass",
    name: "Apple Liquid Glass",
    description: "Premium hardware presentation with heavy frosted glass and specular lighting",
    colors: {
      background: "radial-gradient(circle at 50% 30%, #1A1A24 0%, #070709 100%)",
      card: "rgba(255, 255, 255, 0.14)",
      cardBorder: "1px solid rgba(255, 255, 255, 0.28)",
      textPrimary: "#FFFFFF",
      textSecondary: "rgba(255, 255, 255, 0.75)",
      accent: "#0071E3",
      accentSecondary: "#2997FF",
    },
    fonts: {
      primary: "Inter, sans-serif",
      secondary: "Inter, sans-serif",
    },
    cameraDefault: "push-in",
    springConfig: {
      damping: 14,
      stiffness: 110,
      mass: 0.9,
    },
  },
  "hormozi-kinetic-punch": {
    id: "hormozi-kinetic-punch",
    name: "Hormozi Kinetic Punch",
    description: "Relentless velocity with punchy 2-word groups and bright acid highlights",
    colors: {
      background: "#000000",
      card: "#111111",
      cardBorder: "#FFFF00",
      textPrimary: "#FFFFFF",
      textSecondary: "#EEEEEE",
      accent: "#FFFF00",
      accentSecondary: "#FF5500",
    },
    fonts: {
      primary: "Montserrat, sans-serif",
      secondary: "Rubik, sans-serif",
    },
    cameraDefault: "push-in",
    springConfig: {
      damping: 10,
      stiffness: 180,
      mass: 0.6,
    },
  },
  "devin-jatho-saas": {
    id: "devin-jatho-saas",
    name: "Devin Jatho SaaS",
    description: "High-velocity SaaS motion design with frosted dark glass, isometric tilts, and tactile clicks",
    colors: {
      background: "#0B0E14",
      card: "rgba(18, 22, 31, 0.65)",
      cardBorder: "1.5px solid rgba(255, 255, 255, 0.12)",
      textPrimary: "#FFFFFF",
      textSecondary: "rgba(255, 255, 255, 0.6)",
      accent: "#6366F1",
      accentSecondary: "#10B981",
    },
    fonts: {
      primary: "Inter, sans-serif",
      secondary: "Inter, sans-serif",
    },
    cameraDefault: "push-in",
    springConfig: {
      damping: 24,
      stiffness: 280,
      mass: 0.85,
    },
  },
} as const;

export type StylePresetId = keyof typeof STYLE_PRESETS;
