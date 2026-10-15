import { continueRender, delayRender, staticFile } from "remotion";

export const AppFont = "Montserrat";
export const TheBoldFont = AppFont;

let loaded = false;

export const loadFont = async (): Promise<void> => {
  if (loaded) {
    return Promise.resolve();
  }

  const waitForFont = delayRender();
  loaded = true;

  const font = new FontFace(
    AppFont,
    `url('${staticFile("montserrat.ttf")}') format('truetype')`,
    { weight: "800", style: "normal" },
  );

  await font.load();
  document.fonts.add(font);

  continueRender(waitForFont);
};
