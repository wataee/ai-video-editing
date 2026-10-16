import { staticFile } from "remotion";

export const FONT_MONTSERRAT = "Montserrat, sans-serif";
export const FONT_INTER = "Inter, sans-serif";
export const FONT_UNBOUNDED = "Unbounded, sans-serif";
export const FONT_OSWALD = "Oswald, sans-serif";
export const FONT_RUBIK = "Rubik, sans-serif";
export const FONT_MANROPE = "Manrope, sans-serif";

export const LOCAL_FONT_FILES = {
  montserrat: staticFile("fonts/Montserrat/Montserrat[wght].ttf"),
  inter: staticFile("fonts/Inter/Inter[opsz,wght].ttf"),
  unbounded: staticFile("fonts/Unbounded/Unbounded[wght].ttf"),
  oswald: staticFile("fonts/Oswald/Oswald[wght].ttf"),
  rubik: staticFile("fonts/Rubik/Rubik[wght].ttf"),
  manrope: staticFile("fonts/Manrope/Manrope[wght].ttf"),
} as const;

export const FORBIDDEN_FALLBACK_FONTS = ["Arial", "Roboto", "Times New Roman", "Comic Sans"] as const;

export const ensureLocalFonts = async (): Promise<void> => {
  if (typeof document === "undefined" || !("fonts" in document)) {
    return;
  }
  const fontDeclarations = [
    { family: "Montserrat", url: LOCAL_FONT_FILES.montserrat },
    { family: "Inter", url: LOCAL_FONT_FILES.inter },
    { family: "Unbounded", url: LOCAL_FONT_FILES.unbounded },
    { family: "Oswald", url: LOCAL_FONT_FILES.oswald },
    { family: "Rubik", url: LOCAL_FONT_FILES.rubik },
    { family: "Manrope", url: LOCAL_FONT_FILES.manrope },
  ];

  for (const f of fontDeclarations) {
    try {
      const face = new FontFace(f.family, `url(${f.url})`, { style: "normal", weight: "100 900" });
      const loaded = await face.load();
      document.fonts.add(loaded);
    } catch {
      continue;
    }
  }
};

export const sanitizeFontFamily = (requested: string): string => {
  for (const forbidden of FORBIDDEN_FALLBACK_FONTS) {
    if (requested.toLowerCase().includes(forbidden.toLowerCase())) {
      throw new Error(`[Font Error] Forbidden font '${requested}' detected. Use local fonts from assets/fonts/.`);
    }
  }
  return requested;
};
