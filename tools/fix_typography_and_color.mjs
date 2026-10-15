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

// 1. Очищаем старые текстовые слои и корректирующий слой
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("COLOR GRADE") === 0) {
    lyr.remove();
  }
}

// 2. Создаем профессиональный Color Grade (iPhone HDR -> SDR Normalization)
var adj = comp.layers.addSolid([1, 1, 1], "COLOR GRADE (HDR to SDR)", comp.width, comp.height, 1, comp.duration);
adj.adjustmentLayer = true;
try {
  var exp = adj.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
  if (exp) {
    exp.property("ADBE Exposure2-0002").setValue(-1.7); // Возвращаем текстуру и тон кожи
    exp.property("ADBE Exposure2-0004").setValue(0.90); // Гамма
  }
  var bc = adj.property("ADBE Effect Parade").addProperty("ADBE Brightness & Contrast 2");
  if (bc) {
    bc.property("ADBE Brightness & Contrast 2-0002").setValue(14); // Контраст
  }
} catch (eFx) {}

// 3. Создаем кинетическую типографику с автопереносом и безопасными зонами
function addProTitle(linesArr, inTime, outTime, accentColor) {
  var textStr = linesArr.join("\\r");
  var tl = comp.layers.addText(textStr);
  tl.name = "TEXT: " + linesArr[0];
  tl.inTime = inTime;
  tl.outTime = outTime;
  tl.startTime = inTime;
  tl.inPoint = inTime;
  tl.outPoint = outTime;

  var prop = tl.property("ADBE Text Properties").property("ADBE Text Document");
  var doc = prop.value;
  doc.fontSize = 68;
  doc.font = "Montserrat-ExtraBold";
  doc.justification = ParagraphJustification.CENTER_JUSTIFY;
  doc.fillColor = accentColor;
  doc.applyStroke = true;
  doc.strokeColor = [0.05, 0.05, 0.05];
  doc.strokeWidth = 6;
  doc.applyFill = true;
  doc.tracking = 20;
  prop.setValue(doc);

  var pos = tl.property("ADBE Transform Group").property("ADBE Position");
  pos.setValue([comp.width / 2, 460]); // Идеальная зона над головой спикера

  // Мягкая плавная анимация появления (Fade In 4 кадра)
  var op = tl.property("ADBE Transform Group").property("ADBE Opacity");
  op.setValueAtTime(inTime, 0);
  op.setValueAtTime(inTime + 0.12, 100);
  op.setValueAtTime(outTime - 0.12, 100);
  op.setValueAtTime(outTime, 0);

  return tl;
}

// Заголовок 1 (Хук)
addProTitle(["У МЕНЯ", "НОРМАЛЬНЫЙ ДИПЛОМ"], 0.0, 3.8, [0.98, 0.8, 0.08]);

// Заголовок 2 (Смена парадигмы)
addProTitle(["ТЕРАПИЯ", "≠ ДИПЛОМ"], 7.8, 23.8, [1.0, 1.0, 1.0]);

// Заголовок 3 (Кульминация)
addProTitle(["«С БОГОМ", "ПОГОВОРИЛ»"], 23.8, 36.8, [1.0, 1.0, 1.0]);

// Заголовок 4 (Финальный вывод)
addProTitle(["КОНТАКТ:", "ЧЕЛОВЕК — ЧЕЛОВЕК"], 36.8, 45.3, [0.98, 0.8, 0.08]);

return {
  ok: true,
  layers: comp.numLayers,
  compName: comp.name
};
`;

async function main() {
  console.log("Applying Typography & Color Normalization...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Typography & Color Polish");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
