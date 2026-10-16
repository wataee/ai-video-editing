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

// 1. Заменяем исходный HLG MOV на чистый SDR кинематографичный MP4
var footageItem = null;
for (var f = 1; f <= app.project.numItems; f++) {
  var it = app.project.item(f);
  if (it instanceof FootageItem && (it.name.indexOf("IMG_2137") === 0 || it.name.indexOf("test_rec709") === 0)) {
    footageItem = it;
    break;
  }
}

var replacedOk = false;
if (footageItem) {
  var sdrFile = new File("C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/IMG_2137_cinematic.mp4");
  if (sdrFile.exists) {
    footageItem.replace(sdrFile);
    replacedOk = true;
  }
}

// 2. Очищаем старые тестовые слои (тексты, виньетки, цветокоррекции)
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("COLOR GRADE") === 0 || lyr.name.indexOf("STUDIO VIGNETTE") === 0) {
    lyr.remove();
  }
}

// 3. Создаем мягкую кинематографичную виньетку (Moody Studio Falloff)
// 38% прозрачность, ультра-мягкое перо 360/420px, фокус на лице спикера
var vig = comp.layers.addSolid([0, 0, 0], "STUDIO VIGNETTE (Moody Atmosphere)", comp.width, comp.height, 1, comp.duration);
var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
mask.maskMode = MaskMode.SUBTRACT;
var myShape = mask.property("ADBE Mask Shape").value;
myShape.vertices = [
  [comp.width * 0.12, comp.height * 0.08],
  [comp.width * 0.88, comp.height * 0.08],
  [comp.width * 0.88, comp.height * 0.68],
  [comp.width * 0.12, comp.height * 0.68]
];
myShape.closed = true;
mask.property("ADBE Mask Shape").setValue(myShape);
mask.property("ADBE Mask Feather").setValue([350, 420]); // Огромное органичное перо
vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(38);

// Помещаем виньетку прямо над слоями видео, под SFX и текстами
// Найдем верхний видео слой
var topVideoIndex = 1;
for (var vi = 1; vi <= comp.numLayers; vi++) {
  if (comp.layer(vi).name.indexOf("Keep ") === 0) {
    topVideoIndex = vi;
    break;
  }
}
vig.moveBefore(comp.layer(topVideoIndex));

// 4. Генератор титров в формуле Mahabur Rahman ($30,000 Business)
function createViralTitleLockup(primaryText, scriptText, inTime, outTime, posY, scriptSize, scriptOffsetX) {
  var yPos = posY || 1400;
  var sSize = scriptSize || 84;
  var sOffX = scriptOffsetX || 60;

  // --- СЛОЙ 1: Неоновый красный 3D заголовок ---
  var tMain = comp.layers.addText(primaryText);
  tMain.name = "TEXT: MAIN " + primaryText;
  tMain.startTime = inTime;
  tMain.inPoint = inTime;
  tMain.outPoint = outTime;

  var pMain = tMain.property("ADBE Text Properties").property("ADBE Text Document");
  var dMain = pMain.value;
  dMain.fontSize = 120;
  dMain.font = "Montserrat-Black";
  dMain.justification = ParagraphJustification.CENTER_JUSTIFY;
  dMain.fillColor = [1.0, 0.08, 0.16]; // Неоновый алый (#FF1529)
  dMain.applyStroke = true;
  dMain.strokeColor = [0.3, 0.0, 0.04];
  dMain.strokeWidth = 3;
  dMain.tracking = 20;
  pMain.setValue(dMain);

  var posMain = tMain.property("ADBE Transform Group").property("ADBE Position");
  posMain.setValue([comp.width / 2, yPos]);

  // Глубокая черная тень
  try {
    var ds = tMain.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    if (ds) {
      ds.property("ADBE Drop Shadow-0002").setValue([0.0, 0.0, 0.0, 1.0]);
      ds.property("ADBE Drop Shadow-0003").setValue(90);
      ds.property("ADBE Drop Shadow-0004").setValue(135);
      ds.property("ADBE Drop Shadow-0005").setValue(18);
      ds.property("ADBE Drop Shadow-0006").setValue(36);
    }
  } catch (eDS) {}

  // Неоновое свечение (Red Neon Bloom)
  try {
    var glow = tMain.property("ADBE Effect Parade").addProperty("ADBE Glo2");
    if (glow) {
      glow.property("ADBE Glo2-0001").setValue(40);
      glow.property("ADBE Glo2-0002").setValue(55);
      glow.property("ADBE Glo2-0003").setValue(1.5);
      glow.property("ADBE Glo2-0006").setValue(2);
      glow.property("ADBE Glo2-0007").setValue([1.0, 0.15, 0.22, 1.0]);
      glow.property("ADBE Glo2-0008").setValue([0.75, 0.0, 0.08, 1.0]);
    }
  } catch (eGL) {}

  // Пружинная анимация входа (Pop-in spring overshoot)
  var scMain = tMain.property("ADBE Transform Group").property("ADBE Scale");
  scMain.setValueAtTime(inTime, [70, 70, 100]);
  scMain.setValueAtTime(inTime + 0.14, [107, 107, 100]);
  scMain.setValueAtTime(inTime + 0.26, [100, 100, 100]);

  var opMain = tMain.property("ADBE Transform Group").property("ADBE Opacity");
  opMain.setValueAtTime(inTime, 0);
  opMain.setValueAtTime(inTime + 0.08, 100);
  opMain.setValueAtTime(outTime - 0.12, 100);
  opMain.setValueAtTime(outTime, 0);

  // --- СЛОЙ 2: Элегантный белый рукописный курсив внахлест ---
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
    dScript.fillColor = [1.0, 1.0, 1.0]; // Чистый белый
    dScript.applyStroke = true;
    dScript.strokeColor = [0.0, 0.0, 0.0];
    dScript.strokeWidth = 3.5;
    dScript.tracking = 25;
    pScript.setValue(dScript);

    // Смещаем на правый нижний угол красного слова с наклоном -8 градусов
    var posScript = tScript.property("ADBE Transform Group").property("ADBE Position");
    posScript.setValue([comp.width / 2 + sOffX, yPos + 68]);

    var rotScript = tScript.property("ADBE Transform Group").property("ADBE Rotate Z");
    rotScript.setValue(-8);

    // Мягкое белое свечение
    try {
      var sGlow = tScript.property("ADBE Effect Parade").addProperty("ADBE Glo2");
      if (sGlow) {
        sGlow.property("ADBE Glo2-0001").setValue(60);
        sGlow.property("ADBE Glo2-0002").setValue(30);
        sGlow.property("ADBE Glo2-0003").setValue(0.9);
      }
      var sDS = tScript.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
      if (sDS) {
        sDS.property("ADBE Drop Shadow-0003").setValue(95);
        sDS.property("ADBE Drop Shadow-0005").setValue(14);
        sDS.property("ADBE Drop Shadow-0006").setValue(22);
      }
    } catch (eSG) {}

    // Каскадное появление с микро-задержкой на 0.06s
    var scScript = tScript.property("ADBE Transform Group").property("ADBE Scale");
    scScript.setValueAtTime(inTime + 0.06, [65, 65, 100]);
    scScript.setValueAtTime(inTime + 0.22, [108, 108, 100]);
    scScript.setValueAtTime(inTime + 0.34, [100, 100, 100]);

    var opScript = tScript.property("ADBE Transform Group").property("ADBE Opacity");
    opScript.setValueAtTime(inTime + 0.06, 0);
    opScript.setValueAtTime(inTime + 0.14, 100);
    opScript.setValueAtTime(outTime - 0.12, 100);
    opScript.setValueAtTime(outTime, 0);

    tScript.moveBefore(tMain); // Курсив всегда строго поверх красного слова
  }
}

// РАССТАНОВКА 4 СЮЖЕТНЫХ ТИТРОВ
// 1. Хук (0.0 - 3.8s): «ДИПЛОМ» + «психолога»
createViralTitleLockup("ДИПЛОМ", "психолога", 0.0, 3.8, 1400, 86, 65);

// 2. Тезис (7.8 - 23.8s): «ТЕРАПИЯ» + «это контакт»
createViralTitleLockup("ТЕРАПИЯ", "это контакт", 7.8, 23.8, 1400, 78, 55);

// 3. Эмоциональный кульминационный хук (23.8 - 36.8s): «С БОГОМ» + «поговорил...»
createViralTitleLockup("С БОГОМ", "поговорил...", 23.8, 36.8, 1400, 82, 60);

// 4. Финал (36.8 - 45.3s): «ЧЕЛОВЕК» + «человек»
createViralTitleLockup("ЧЕЛОВЕК", "человек", 36.8, 45.3, 1400, 86, 65);

return {
  ok: true,
  replacedFootage: replacedOk,
  compName: comp.name,
  numLayers: comp.numLayers
};
`;

async function main() {
  console.log("Applying Pinterest Master Viral Aesthetic...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Pinterest Master Aesthetic");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
