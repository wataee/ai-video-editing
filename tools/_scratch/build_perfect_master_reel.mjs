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

// 1. Очистка старых текстовых слоев и adjustment layers
for (var l = comp.numLayers; l >= 1; l--) {
  var lyr = comp.layer(l);
  if (lyr.name.indexOf("TEXT:") === 0 || lyr.name.indexOf("COLOR GRADE") === 0) {
    lyr.remove();
  }
}

// 2. Идеальный Color Grade (нормализация iPhone HLG HDR)
var adj = comp.layers.addSolid([1, 1, 1], "COLOR GRADE (HDR to SDR)", comp.width, comp.height, 1, comp.duration);
adj.adjustmentLayer = true;
try {
  var exp = adj.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
  if (exp) {
    exp.property("ADBE Exposure2-0003").setValue(-2.2); // Точный слайдер Exposure!
    exp.property("ADBE Exposure2-0005").setValue(0.92); // Gamma
  }
  var sat = adj.property("ADBE Effect Parade").addProperty("ADBE HUE SATURATION");
  if (sat) {
    sat.property("ADBE HUE SATURATION-0005").setValue(8);
  }
} catch (eFx) {}

// 3. Кинетические титры: 2-3 короткие строки, размер 46, безопасная зона груди (y = 1380)
function addMasterTitle(linesArr, inTime, outTime, accentYellow) {
  var textStr = linesArr.join("\\r");
  var tl = comp.layers.addText(textStr);
  tl.name = "TEXT: " + linesArr[0];
  tl.startTime = inTime;
  tl.inPoint = inTime;
  tl.outPoint = outTime;

  var prop = tl.property("ADBE Text Properties").property("ADBE Text Document");
  var doc = prop.value;
  doc.fontSize = 46;
  doc.font = "Montserrat-ExtraBold";
  doc.justification = ParagraphJustification.CENTER_JUSTIFY;
  doc.fillColor = accentYellow ? [0.98, 0.8, 0.08] : [1.0, 1.0, 1.0];
  doc.applyStroke = true;
  doc.strokeColor = [0.0, 0.0, 0.0];
  doc.strokeWidth = 6;
  doc.applyFill = true;
  doc.tracking = 15;
  prop.setValue(doc);

  var pos = tl.property("ADBE Transform Group").property("ADBE Position");
  pos.setValue([comp.width / 2, 1380]);

  // Плавная анимация появления
  var op = tl.property("ADBE Transform Group").property("ADBE Opacity");
  op.setValueAtTime(inTime, 0);
  op.setValueAtTime(inTime + 0.1, 100);
  op.setValueAtTime(outTime - 0.1, 100);
  op.setValueAtTime(outTime, 0);

  return tl;
}

addMasterTitle(["У МЕНЯ", "НОРМАЛЬНЫЙ ДИПЛОМ,", "А У ТЕБЯ — НЕТ"], 0.0, 3.8, true);
addMasterTitle(["СООБЩЕСТВО", "ПСИХОЛОГОВ"], 3.8, 7.8, false);
addMasterTitle(["ТЕРАПИЯ ПРОИСХОДИТ", "НЕ ЧЕРЕЗ ДИПЛОМ"], 7.8, 23.8, true);
addMasterTitle(["КОГДА ОЩУЩЕНИЕ,", "ЧТО С БОГОМ ПОГОВОРИЛ"], 23.8, 36.8, false);
addMasterTitle(["ИСТИННЫЙ КОНТАКТ:", "ЧЕЛОВЕК — ЧЕЛОВЕК"], 36.8, 45.3, true);

return {
  ok: true,
  comp: comp.name,
  layers: comp.numLayers,
  duration: comp.duration
};
`;

async function main() {
  console.log("Applying final Master Polish in After Effects...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Final Master Polish");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
