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

// 1. Очистка старых текстовых слоев и виньеток
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("COLOR GRADE") === 0 || lyr.name.indexOf("STUDIO VIGNETTE") === 0) {
    lyr.remove();
  }
}

// 2. Создаем эффект кинематографичной студии (Studio Vignette & Moody Lighting)
// Затемняем фон и комнату, оставляя фокус на лице спикера
var vig = comp.layers.addSolid([0, 0, 0], "STUDIO VIGNETTE", comp.width, comp.height, 1, comp.duration);
var mask = vig.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
mask.maskMode = MaskMode.SUBTRACT;
var myShape = mask.property("ADBE Mask Shape").value;
// Овальная маска в центре на лицо
myShape.vertices = [
  [comp.width * 0.15, comp.height * 0.10],
  [comp.width * 0.85, comp.height * 0.10],
  [comp.width * 0.85, comp.height * 0.65],
  [comp.width * 0.15, comp.height * 0.65]
];
myShape.closed = true;
mask.property("ADBE Mask Shape").setValue(myShape);
mask.property("ADBE Mask Feather").setValue([280, 320]); // Огромное мягкое перо
vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(65);

// 3. Коррекция тона кожи спикера (HDR Fix)
var grade = comp.layers.addSolid([1, 1, 1], "COLOR GRADE (Studio Tone)", comp.width, comp.height, 1, comp.duration);
grade.adjustmentLayer = true;
try {
  var exp = grade.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
  if (exp) {
    exp.property("ADBE Exposure2-0003").setValue(-2.4); // Убираем пересвет
    exp.property("ADBE Exposure2-0005").setValue(0.92); // Гамма
  }
  var bc = grade.property("ADBE Effect Parade").addProperty("ADBE Brightness & Contrast 2");
  if (bc) {
    bc.property("ADBE Brightness & Contrast 2-0002").setValue(18); // Плотный кино-контраст
  }
} catch (eG) {}

// 4. Функция создания фирменного заголовка в стиле Mahabur Rahman ($30,000 Business)
// Жирный 3D Неоновый Red Sans + Наложенный элегантный белый курсив с наклоном
function createViralTitleLockup(primaryText, scriptText, inTime, outTime, posY) {
  var yPos = posY || 1420;

  // --- СЛОЙ 1: Основное жирное слово (Red 3D Glow Sans) ---
  var tMain = comp.layers.addText(primaryText);
  tMain.name = "TEXT: MAIN " + primaryText;
  tMain.startTime = inTime;
  tMain.inPoint = inTime;
  tMain.outPoint = outTime;

  var pMain = tMain.property("ADBE Text Properties").property("ADBE Text Document");
  var dMain = pMain.value;
  dMain.fontSize = 115;
  dMain.font = "Montserrat-Black";
  dMain.justification = ParagraphJustification.CENTER_JUSTIFY;
  dMain.fillColor = [1.0, 0.08, 0.15]; // Яркий насыщенный неоновый красный (#FF1526)
  dMain.applyStroke = true;
  dMain.strokeColor = [0.35, 0.0, 0.05];
  dMain.strokeWidth = 3;
  dMain.tracking = 15;
  pMain.setValue(dMain);

  var posMain = tMain.property("ADBE Transform Group").property("ADBE Position");
  posMain.setValue([comp.width / 2, yPos]);

  // Эффект Drop Shadow (Глубокая тень для объема)
  try {
    var ds = tMain.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
    if (ds) {
      ds.property("ADBE Drop Shadow-0002").setValue([0.0, 0.0, 0.0, 1.0]); // Черная тень
      ds.property("ADBE Drop Shadow-0003").setValue(85); // Непрозрачность
      ds.property("ADBE Drop Shadow-0004").setValue(135); // Угол
      ds.property("ADBE Drop Shadow-0005").setValue(18); // Дистанция
      ds.property("ADBE Drop Shadow-0006").setValue(35); // Мягкость
    }
  } catch (eDS) {}

  // Эффект Неонового свечения (Red Glow)
  try {
    var glow = tMain.property("ADBE Effect Parade").addProperty("ADBE Glo2");
    if (glow) {
      glow.property("ADBE Glo2-0001").setValue(45); // Threshold
      glow.property("ADBE Glo2-0002").setValue(50); // Radius
      glow.property("ADBE Glo2-0003").setValue(1.4); // Intensity
      glow.property("ADBE Glo2-0006").setValue(2); // A&B colors
      glow.property("ADBE Glo2-0007").setValue([1.0, 0.12, 0.18, 1.0]); // Color A
      glow.property("ADBE Glo2-0008").setValue([0.7, 0.0, 0.08, 1.0]); // Color B
    }
  } catch (eGL) {}

  // Пружинная анимация входа (Pop-in spring)
  var scMain = tMain.property("ADBE Transform Group").property("ADBE Scale");
  scMain.setValueAtTime(inTime, [70, 70, 100]);
  scMain.setValueAtTime(inTime + 0.16, [106, 106, 100]);
  scMain.setValueAtTime(inTime + 0.28, [100, 100, 100]);

  var opMain = tMain.property("ADBE Transform Group").property("ADBE Opacity");
  opMain.setValueAtTime(inTime, 0);
  opMain.setValueAtTime(inTime + 0.08, 100);
  opMain.setValueAtTime(outTime - 0.12, 100);
  opMain.setValueAtTime(outTime, 0);


  // --- СЛОЙ 2: Рукописный курсив (Elegant White Script Overlay) ---
  if (scriptText) {
    var tScript = comp.layers.addText(scriptText);
    tScript.name = "TEXT: SCRIPT " + scriptText;
    tScript.startTime = inTime;
    tScript.inPoint = inTime;
    tScript.outPoint = outTime;

    var pScript = tScript.property("ADBE Text Properties").property("ADBE Text Document");
    var dScript = pScript.value;
    dScript.fontSize = 82;
    // Используем встроенный в Windows Segoe Script
    dScript.font = "SegoeScript-Bold";
    dScript.justification = ParagraphJustification.CENTER_JUSTIFY;
    dScript.fillColor = [1.0, 1.0, 1.0]; // Идеально белый
    dScript.applyStroke = true;
    dScript.strokeColor = [0.0, 0.0, 0.0];
    dScript.strokeWidth = 4;
    dScript.tracking = 25;
    pScript.setValue(dScript);

    // Смещаем вниз и поворачиваем на -7 градусов, чтобы перекрывал нижнюю часть красного слова
    var posScript = tScript.property("ADBE Transform Group").property("ADBE Position");
    posScript.setValue([comp.width / 2 + 50, yPos + 65]);

    var rotScript = tScript.property("ADBE Transform Group").property("ADBE Rotate Z");
    rotScript.setValue(-7); // Элегантный наклон

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
        sDS.property("ADBE Drop Shadow-0003").setValue(90);
        sDS.property("ADBE Drop Shadow-0005").setValue(12);
        sDS.property("ADBE Drop Shadow-0006").setValue(20);
      }
    } catch (eSG) {}

    // Появление с микро-задержкой на 0.06 сек (Organic cascade)
    var scScript = tScript.property("ADBE Transform Group").property("ADBE Scale");
    scScript.setValueAtTime(inTime + 0.06, [65, 65, 100]);
    scScript.setValueAtTime(inTime + 0.22, [108, 108, 100]);
    scScript.setValueAtTime(inTime + 0.34, [100, 100, 100]);

    var opScript = tScript.property("ADBE Transform Group").property("ADBE Opacity");
    opScript.setValueAtTime(inTime + 0.06, 0);
    opScript.setValueAtTime(inTime + 0.14, 100);
    opScript.setValueAtTime(outTime - 0.12, 100);
    opScript.setValueAtTime(outTime, 0);

    tScript.moveBefore(tMain); // Курсив сверху над красным словом
  }
}

// РАССТАНОВКА ВИРАЛЬНЫХ ТИТРОВ ПО СЦЕНАМ
// 1. Хук (0.0 - 3.8s): "ДИПЛОМ" + "психолога"
createViralTitleLockup("ДИПЛОМ", "психолога", 0.0, 3.8, 1420);

// 2. Тезис (7.8 - 23.8s): "ТЕРАПИЯ" + "это контакт"
createViralTitleLockup("ТЕРАПИЯ", "это контакт", 7.8, 23.8, 1420);

// 3. Эмоциональный пик (23.8 - 36.8s): "С БОГОМ" + "поговорил"
createViralTitleLockup("С БОГОМ", "поговорил...", 23.8, 36.8, 1420);

// 4. Финал (36.8 - 45.3s): "ЧЕЛОВЕК" + "человек"
createViralTitleLockup("ЧЕЛОВЕК", "человек", 36.8, 45.3, 1420);

return {
  ok: true,
  comp: comp.name,
  layers: comp.numLayers
};
`;

async function main() {
  console.log("Rebuilding comp in Mahabur Rahman Viral Style ($30,000 Business)...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Viral Title Lockup ($30,000 Business Style)");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
