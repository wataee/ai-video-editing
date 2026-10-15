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

// 1. Очистка старых текстовых слоев, подложек и виньеток
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("BLOOM:") === 0 || lyr.name.indexOf("STUDIO VIGNETTE") === 0 || lyr.name.indexOf("COLOR GRADE") === 0) {
    lyr.remove();
  }
}

// 2. Проверяем замену футажа на чистый кинематографичный SDR
var footageItem = null;
for (var f = 1; f <= app.project.numItems; f++) {
  var it = app.project.item(f);
  if (it instanceof FootageItem && (it.name.indexOf("IMG_2137") === 0 || it.name.indexOf("test_rec709") === 0)) {
    footageItem = it;
    break;
  }
}
if (footageItem) {
  var sdrFile = new File("C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/IMG_2137_cinematic.mp4");
  if (sdrFile.exists && footageItem.file.name !== "IMG_2137_cinematic.mp4") {
    footageItem.replace(sdrFile);
  }
}

// 3. Создаем мягкую студийную виньетку (Moody Studio Atmosphere, 24% opacity)
var vig = comp.layers.addSolid([0, 0, 0], "STUDIO VIGNETTE (Moody Studio)", comp.width, comp.height, 1, comp.duration);
var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
mask.maskMode = MaskMode.SUBTRACT;
var myShape = mask.property("ADBE Mask Shape").value;
myShape.vertices = [
  [comp.width * 0.08, comp.height * 0.05],
  [comp.width * 0.92, comp.height * 0.05],
  [comp.width * 0.92, comp.height * 0.78],
  [comp.width * 0.08, comp.height * 0.78]
];
myShape.closed = true;
mask.property("ADBE Mask Shape").setValue(myShape);
mask.property("ADBE Mask Feather").setValue([240, 280]);
vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(24);

// Помещаем виньетку прямо над слоями видео
var topVideoIndex = 1;
for (var vi = 1; vi <= comp.numLayers; vi++) {
  if (comp.layer(vi).name.indexOf("Keep ") === 0) {
    topVideoIndex = vi;
    break;
  }
}
vig.moveBefore(comp.layer(topVideoIndex));

// 4. Генератор титров Pinterest / Mahabur Rahman Formula ($30,000 Business)
function createViralTitleLockup(primaryText, scriptText, inTime, outTime, posY, scriptSize, scriptOffsetX, scriptOffsetY) {
  var yPos = posY || 1380;
  var sSize = scriptSize || 138;
  var sOffX = (scriptOffsetX !== undefined) ? scriptOffsetX : 75;
  var sOffY = (scriptOffsetY !== undefined) ? scriptOffsetY : 45;

  // --- СЛОЙ 0: Ambient Red Bloom (Световое пятно за текстом, режим Screen) ---
  var bloom = comp.layers.addSolid([1.0, 0.06, 0.16], "BLOOM: " + primaryText, comp.width, comp.height, 1, outTime - inTime);
  bloom.startTime = inTime;
  bloom.inPoint = inTime;
  bloom.outPoint = outTime;
  var bMask = bloom.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
  bMask.maskMode = MaskMode.ADD;
  var bShape = bMask.property("ADBE Mask Shape").value;
  var bLeft = comp.width * 0.12;
  var bRight = comp.width * 0.88;
  var bTop = yPos - 130;
  var bBottom = yPos + 170;
  bShape.vertices = [[bLeft, bTop], [bRight, bTop], [bRight, bBottom], [bLeft, bBottom]];
  bShape.closed = true;
  bMask.property("ADBE Mask Shape").setValue(bShape);
  bMask.property("ADBE Mask Feather").setValue([220, 160]);
  bloom.property("ADBE Transform Group").property("ADBE Opacity").setValue(36);
  bloom.blendingMode = BlendingMode.SCREEN;

  // --- СЛОЙ 1: Неоновый красный 3D заголовок ---
  var tMain = comp.layers.addText(primaryText);
  tMain.name = "TEXT: MAIN " + primaryText;
  tMain.startTime = inTime;
  tMain.inPoint = inTime;
  tMain.outPoint = outTime;

  var pMain = tMain.property("ADBE Text Properties").property("ADBE Text Document");
  var dMain = pMain.value;
  dMain.fontSize = 136;
  dMain.font = "Montserrat-Black";
  dMain.justification = ParagraphJustification.CENTER_JUSTIFY;
  dMain.fillColor = [1.0, 0.08, 0.16]; // Насыщенный неоновый алый (#FF1429)
  dMain.applyStroke = true;
  dMain.strokeColor = [0.28, 0.0, 0.04];
  dMain.strokeWidth = 3.5;
  dMain.tracking = 16;
  pMain.setValue(dMain);

  var posMain = tMain.property("ADBE Transform Group").property("ADBE Position");
  posMain.setValue([comp.width / 2, yPos]);

  // Эффект Bevel Edges (3D фаска по краям букв)
  try {
    var bev = tMain.property("ADBE Effect Parade").addProperty("ADBE Bevel Edges");
    if (bev) {
      bev.property("ADBE Bevel Edges-0001").setValue(1.5); // Thickness
      bev.property("ADBE Bevel Edges-0002").setValue(45);  // Light Angle
      bev.property("ADBE Bevel Edges-0003").setValue(0.5); // Light Intensity
    }
  } catch (eB) {}

  // Глубокая черная тень для объема
  try {
    var ds = tMain.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    if (ds) {
      ds.property("ADBE Drop Shadow-0002").setValue([0.0, 0.0, 0.0, 1.0]);
      ds.property("ADBE Drop Shadow-0003").setValue(95);
      ds.property("ADBE Drop Shadow-0004").setValue(135);
      ds.property("ADBE Drop Shadow-0005").setValue(18);
      ds.property("ADBE Drop Shadow-0006").setValue(36);
    }
  } catch (eDS) {}

  // Неоновое свечение (Red Neon Glow)
  try {
    var glow = tMain.property("ADBE Effect Parade").addProperty("ADBE Glo2");
    if (glow) {
      glow.property("ADBE Glo2-0001").setValue(38);
      glow.property("ADBE Glo2-0002").setValue(60);
      glow.property("ADBE Glo2-0003").setValue(1.6);
      glow.property("ADBE Glo2-0006").setValue(2);
      glow.property("ADBE Glo2-0007").setValue([1.0, 0.18, 0.24, 1.0]);
      glow.property("ADBE Glo2-0008").setValue([0.8, 0.0, 0.1, 1.0]);
    }
  } catch (eGL) {}

  // Пружинная анимация входа (Pop-in spring overshoot)
  var scMain = tMain.property("ADBE Transform Group").property("ADBE Scale");
  scMain.setValueAtTime(inTime, [70, 70, 100]);
  scMain.setValueAtTime(inTime + 0.14, [108, 108, 100]);
  scMain.setValueAtTime(inTime + 0.26, [100, 100, 100]);

  var opMain = tMain.property("ADBE Transform Group").property("ADBE Opacity");
  opMain.setValueAtTime(inTime, 0);
  opMain.setValueAtTime(inTime + 0.08, 100);
  opMain.setValueAtTime(outTime - 0.12, 100);
  opMain.setValueAtTime(outTime, 0);

  // --- СЛОЙ 2: Элегантный белый рукописный курсив Caveat-Regular ВНАХЛЕСТ ---
  if (scriptText) {
    var tScript = comp.layers.addText(scriptText);
    tScript.name = "TEXT: SCRIPT " + scriptText;
    tScript.startTime = inTime;
    tScript.inPoint = inTime;
    tScript.outPoint = outTime;

    var pScript = tScript.property("ADBE Text Properties").property("ADBE Text Document");
    var dScript = pScript.value;
    dScript.fontSize = sSize;
    dScript.font = "Caveat-Regular";
    dScript.justification = ParagraphJustification.CENTER_JUSTIFY;
    dScript.fillColor = [1.0, 1.0, 1.0]; // Идеально белый #FFFFFF
    dScript.applyStroke = true;
    dScript.strokeColor = [0.0, 0.0, 0.0];
    dScript.strokeWidth = 4.5;
    dScript.tracking = 5;
    pScript.setValue(dScript);

    // Смещаем на правый нижний угол с наклоном -9 градусов (перекрытие 30-40%)
    var posScript = tScript.property("ADBE Transform Group").property("ADBE Position");
    posScript.setValue([comp.width / 2 + sOffX, yPos + sOffY]);

    var rotScript = tScript.property("ADBE Transform Group").property("ADBE Rotate Z");
    rotScript.setValue(-9);

    // Черная тень + белое свечение
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

    // Каскадное пружинное появление с микро-задержкой на 0.06s
    var scScript = tScript.property("ADBE Transform Group").property("ADBE Scale");
    scScript.setValueAtTime(inTime + 0.06, [65, 65, 100]);
    scScript.setValueAtTime(inTime + 0.22, [109, 109, 100]);
    scScript.setValueAtTime(inTime + 0.34, [100, 100, 100]);

    var opScript = tScript.property("ADBE Transform Group").property("ADBE Opacity");
    opScript.setValueAtTime(inTime + 0.06, 0);
    opScript.setValueAtTime(inTime + 0.14, 100);
    opScript.setValueAtTime(outTime - 0.12, 100);
    opScript.setValueAtTime(outTime, 0);

    // Иерархия:
    // 1. Script (верх)
    // 2. Main Red (середина)
    // 3. Bloom (подложка под текстом)
    tScript.moveBefore(tMain);
    bloom.moveAfter(tMain);
  }
}

// 5. РАССТАНОВКА 4 СЮЖЕТНЫХ КЛЮЧЕВЫХ ТИТРОВ
// 1. Хук (0.0 - 3.8s): «ДИПЛОМ» + «психолога»
createViralTitleLockup("ДИПЛОМ", "психолога", 0.0, 3.8, 1380, 148, 75, 45);

// 2. Тезис (7.8 - 23.8s): «ТЕРАПИЯ» + «это контакт»
createViralTitleLockup("ТЕРАПИЯ", "это контакт", 7.8, 23.8, 1380, 132, 65, 42);

// 3. Кульминация (23.8 - 36.8s): «С БОГОМ» + «поговорил...»
createViralTitleLockup("С БОГОМ", "поговорил...", 23.8, 36.8, 1380, 138, 70, 45);

// 4. Финальный вывод (36.8 - 45.3s): «ЧЕЛОВЕК» + «нужен человек»
createViralTitleLockup("ЧЕЛОВЕК", "нужен человек", 36.8, 45.3, 1380, 136, 70, 45);

return {
  ok: true,
  compName: comp.name,
  numLayers: comp.numLayers
};
`;

async function main() {
  console.log("Applying Broadcast Perfect Pinterest Master in After Effects...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Broadcast Pinterest Master");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
