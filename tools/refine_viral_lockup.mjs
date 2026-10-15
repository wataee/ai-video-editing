import { sendCommand } from "./send_ae_command.mjs";

const extendscriptCode = `
var comp = null;
for (var i = 1; i <= app.project.numItems; i++) {
  var item = app.project.item(i);
  if (item instanceof CompItem && item.name === "Aziz - Viral Reel Master") {
    comp = item;
    break;
  }
}
if (!comp) return "Comp not found";

// 1. Очищаем старые текстовые и фоновые слои
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("BLOOM:") === 0 || lyr.name.indexOf("STUDIO VIGNETTE") === 0 || lyr.name.indexOf("COLOR GRADE") === 0) {
    lyr.remove();
  }
}

// 2. Создаем правильную мягкую студийную виньетку
// Центр открыт для лица и верхней части тела, затемняются только углы и дальний план
var vig = comp.layers.addSolid([0, 0, 0], "STUDIO VIGNETTE (Moody Studio)", comp.width, comp.height, 1, comp.duration);
var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
mask.maskMode = MaskMode.SUBTRACT;
var myShape = mask.property("ADBE Mask Shape").value;
// Большой овал в центре
myShape.vertices = [
  [comp.width * 0.05, comp.height * 0.04],
  [comp.width * 0.95, comp.height * 0.04],
  [comp.width * 0.95, comp.height * 0.78],
  [comp.width * 0.05, comp.height * 0.78]
];
myShape.closed = true;
mask.property("ADBE Mask Shape").setValue(myShape);
mask.property("ADBE Mask Feather").setValue([220, 260]);
vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(45);

// Ставим виньетку над видео
var topVideoIndex = 1;
for (var vi = 1; vi <= comp.numLayers; vi++) {
  if (comp.layer(vi).name.indexOf("Keep ") === 0) {
    topVideoIndex = vi;
    break;
  }
}
vig.moveBefore(comp.layer(topVideoIndex));

// 3. Создаем идеальный виральный Typography Lockup в стиле Mahabur Rahman
function createViralTitleLockup(primaryText, scriptText, inTime, outTime, posY, scriptSize, scriptOffsetX, scriptOffsetY) {
  var yPos = posY || 1380;
  var sSize = scriptSize || 96;
  var sOffX = (scriptOffsetX !== undefined) ? scriptOffsetX : 50;
  var sOffY = (scriptOffsetY !== undefined) ? scriptOffsetY : 45; // Перекрытие 30-40% снизу

  // --- СЛОЙ 0: Ambient Red Bloom (Световое пятно за текстом, как на референсе) ---
  var bloom = comp.layers.addSolid([1.0, 0.05, 0.15], "BLOOM: " + primaryText, 700, 320, 1, outTime - inTime);
  bloom.startTime = inTime;
  bloom.inPoint = inTime;
  bloom.outPoint = outTime;
  var bMask = bloom.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
  bMask.maskMode = MaskMode.ADD;
  var bShape = bMask.property("ADBE Mask Shape").value;
  bShape.vertices = [[60, 40], [640, 40], [640, 280], [60, 280]];
  bShape.closed = true;
  bMask.property("ADBE Mask Shape").setValue(bShape);
  bMask.property("ADBE Mask Feather").setValue([160, 110]);
  bloom.property("ADBE Transform Group").property("ADBE Position").setValue([comp.width / 2, yPos + 10]);
  bloom.property("ADBE Transform Group").property("ADBE Opacity").setValue(42);
  bloom.blendingMode = BlendingMode.SCREEN;

  // --- СЛОЙ 1: Неоновый красный 3D заголовок ---
  var tMain = comp.layers.addText(primaryText);
  tMain.name = "TEXT: MAIN " + primaryText;
  tMain.startTime = inTime;
  tMain.inPoint = inTime;
  tMain.outPoint = outTime;

  var pMain = tMain.property("ADBE Text Properties").property("ADBE Text Document");
  var dMain = pMain.value;
  dMain.fontSize = 124;
  dMain.font = "Montserrat-Black";
  dMain.justification = ParagraphJustification.CENTER_JUSTIFY;
  dMain.fillColor = [1.0, 0.09, 0.16]; // #FF1729
  dMain.applyStroke = true;
  dMain.strokeColor = [0.32, 0.0, 0.04];
  dMain.strokeWidth = 3.5;
  dMain.tracking = 20;
  pMain.setValue(dMain);

  var posMain = tMain.property("ADBE Transform Group").property("ADBE Position");
  posMain.setValue([comp.width / 2, yPos]);

  // Глубокая черная тень (Drop Shadow)
  try {
    var ds = tMain.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    if (ds) {
      ds.property("ADBE Drop Shadow-0002").setValue([0.0, 0.0, 0.0, 1.0]);
      ds.property("ADBE Drop Shadow-0003").setValue(95);
      ds.property("ADBE Drop Shadow-0004").setValue(135);
      ds.property("ADBE Drop Shadow-0005").setValue(16);
      ds.property("ADBE Drop Shadow-0006").setValue(32);
    }
  } catch (eDS) {}

  // Неоновое свечение (Outer Glow)
  try {
    var glow = tMain.property("ADBE Effect Parade").addProperty("ADBE Glo2");
    if (glow) {
      glow.property("ADBE Glo2-0001").setValue(38);
      glow.property("ADBE Glo2-0002").setValue(65);
      glow.property("ADBE Glo2-0003").setValue(1.8);
      glow.property("ADBE Glo2-0006").setValue(2);
      glow.property("ADBE Glo2-0007").setValue([1.0, 0.18, 0.25, 1.0]);
      glow.property("ADBE Glo2-0008").setValue([0.8, 0.0, 0.1, 1.0]);
    }
  } catch (eGL) {}

  // Пружинная кинетическая анимация
  var scMain = tMain.property("ADBE Transform Group").property("ADBE Scale");
  scMain.setValueAtTime(inTime, [72, 72, 100]);
  scMain.setValueAtTime(inTime + 0.15, [107, 107, 100]);
  scMain.setValueAtTime(inTime + 0.28, [100, 100, 100]);

  var opMain = tMain.property("ADBE Transform Group").property("ADBE Opacity");
  opMain.setValueAtTime(inTime, 0);
  opMain.setValueAtTime(inTime + 0.08, 100);
  opMain.setValueAtTime(outTime - 0.12, 100);
  opMain.setValueAtTime(outTime, 0);

  // --- СЛОЙ 2: Элегантный белый рукописный курсив ВНАХЛЕСТ ---
  if (scriptText) {
    var tScript = comp.layers.addText(scriptText);
    tScript.name = "TEXT: SCRIPT " + scriptText;
    tScript.startTime = inTime;
    tScript.inPoint = inTime;
    tScript.outPoint = outTime;

    var pScript = tScript.property("ADBE Text Properties").property("ADBE Text Document");
    var dScript = pScript.value;
    dScript.fontSize = sSize;
    dScript.font = "SegoeScript-Bold";
    dScript.justification = ParagraphJustification.CENTER_JUSTIFY;
    dScript.fillColor = [1.0, 1.0, 1.0]; // #FFFFFF
    dScript.applyStroke = true;
    dScript.strokeColor = [0.0, 0.0, 0.0];
    dScript.strokeWidth = 4.0;
    dScript.tracking = 15;
    pScript.setValue(dScript);

    // Накладываем прямо поверх нижней трети красного слова с наклоном -8 градусов
    var posScript = tScript.property("ADBE Transform Group").property("ADBE Position");
    posScript.setValue([comp.width / 2 + sOffX, yPos + sOffY]);

    var rotScript = tScript.property("ADBE Transform Group").property("ADBE Rotate Z");
    rotScript.setValue(-8);

    // Белое свечение + глубокая тень для отделения от красного слоя
    try {
      var sDS = tScript.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
      if (sDS) {
        sDS.property("ADBE Drop Shadow-0003").setValue(100);
        sDS.property("ADBE Drop Shadow-0005").setValue(12);
        sDS.property("ADBE Drop Shadow-0006").setValue(24);
      }
      var sGlow = tScript.property("ADBE Effect Parade").addProperty("ADBE Glo2");
      if (sGlow) {
        sGlow.property("ADBE Glo2-0001").setValue(55);
        sGlow.property("ADBE Glo2-0002").setValue(35);
        sGlow.property("ADBE Glo2-0003").setValue(1.1);
      }
    } catch (eSG) {}

    // Каскадный пружинный вход со сдвигом на 3 кадра
    var scScript = tScript.property("ADBE Transform Group").property("ADBE Scale");
    scScript.setValueAtTime(inTime + 0.08, [68, 68, 100]);
    scScript.setValueAtTime(inTime + 0.24, [108, 108, 100]);
    scScript.setValueAtTime(inTime + 0.36, [100, 100, 100]);

    var opScript = tScript.property("ADBE Transform Group").property("ADBE Opacity");
    opScript.setValueAtTime(inTime + 0.08, 0);
    opScript.setValueAtTime(inTime + 0.16, 100);
    opScript.setValueAtTime(outTime - 0.12, 100);
    opScript.setValueAtTime(outTime, 0);

    // Гарантируем строгий порядок слоев:
    // 1. Script (сверху)
    // 2. Main Red (посередине)
    // 3. Bloom (под текстом)
    tScript.moveBefore(tMain);
    bloom.moveAfter(tMain);
  }
}

// РАССТАНОВКА 4 СЮЖЕТНЫХ БЛОКОВ
// 1. Хук (0.0 - 3.8s): «ДИПЛОМ» + «психолога»
createViralTitleLockup("ДИПЛОМ", "психолога", 0.0, 3.8, 1380, 94, 60, 48);

// 2. Тезис (7.8 - 23.8s): «ТЕРАПИЯ» + «это контакт»
createViralTitleLockup("ТЕРАПИЯ", "это контакт", 7.8, 23.8, 1380, 84, 50, 46);

// 3. Эмоциональный кульминационный хук (23.8 - 36.8s): «С БОГОМ» + «поговорил...»
createViralTitleLockup("С БОГОМ", "поговорил...", 23.8, 36.8, 1380, 88, 55, 48);

// 4. Финал (36.8 - 45.3s): «ЧЕЛОВЕК» + «человек»
createViralTitleLockup("ЧЕЛОВЕК", "человек", 36.8, 45.3, 1380, 92, 60, 48);

return {
  ok: true,
  compName: comp.name,
  numLayers: comp.numLayers
};
`;

async function main() {
  console.log("Refining Viral Typography Lockups & Ambient Red Bloom...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Refine Pinterest Style");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
