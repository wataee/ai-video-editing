import { cancelRender, continueRender, delayRender } from "remotion";
import { FONTS } from "./assets";

interface FontItem {
  family: string;
  weights: readonly string[];
  regular: string;
  italic?: string;
  bold?: string;
}

interface FaceSpec {
  family: string;
  src: string;
  descriptors: FontFaceDescriptors;
}

const weightRange = (weights: readonly string[]): string => {
  const numeric = weights.map(Number).filter((w) => Number.isFinite(w));
  return `${Math.min(...numeric)} ${Math.max(...numeric)}`;
};

const buildFaces = (font: FontItem): FaceSpec[] => {
  const faces: FaceSpec[] = [];
  if (font.bold) {
    faces.push({ family: font.family, src: font.regular, descriptors: { weight: "400", style: "normal" } });
    faces.push({ family: font.family, src: font.bold, descriptors: { weight: "700", style: "normal" } });
    return faces;
  }
  const weight = weightRange(font.weights);
  faces.push({ family: font.family, src: font.regular, descriptors: { weight, style: "normal" } });
  if (font.italic) {
    faces.push({ family: font.family, src: font.italic, descriptors: { weight, style: "italic" } });
  }
  return faces;
};

let started = false;

export const loadProjectFonts = (): void => {
  if (started || typeof document === "undefined") return;
  started = true;
  const handle = delayRender("Loading project fonts");
  const fonts = Object.values(FONTS) as unknown as FontItem[];
  const jobs = fonts
    .flatMap(buildFaces)
    .map(({ family, src, descriptors }) =>
      new FontFace(family, `url(${src})`, descriptors).load().then((face) => {
        document.fonts.add(face);
      }),
    );
  Promise.all(jobs)
    .then(() => continueRender(handle))
    .catch((error) => cancelRender(error));
};
