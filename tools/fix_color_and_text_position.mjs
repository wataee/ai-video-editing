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

// 2. Настраиваем Color Grade (нормализация HDR экспозиции)
var adj = comp.layers.addSolid([1, 1, 1], "COLOR GRADE (HDR to SDR)", comp.width, comp.height, 1, comp.duration);
adj.adjustmentLayer = true;
try {
  var exp = adj.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
  if (exp) {
    // Снижаем экспозицию на 2.3 стопа для возврата ярких деталей кожи
    exp.property("ADBE Exposure2-0002").setValue(-2.4);
    exp.property("ADBE Exposure2-0004").setValue(0.95);
  }
  var sat = adj.property("ADBE Effect Parade").addProperty("ADBE HUE SATURATION");
  if (sat) {
    sat.property("ADBE HUE SATURATION-0005").setValue(10); // +10% сочности
  }
} catch (eFx) {}

// 3. Создаем кинетические титры на черной футболке (y = 1320 px)
function addSub(textArr, inTime, outTime, isAccent) {
  var textStr = textArr.join("\\r");
  var tl = comp.layers.addText(textStr);
  tl.name = "TEXT: " + textArr[0];
  tl.startTime = inTime;
  tl.inPoint = inTime;
  tl.outPoint = outTime;

  var prop = tl.property("ADBE Text Properties").property("ADBE Text Document");
  var doc = prop.value;
  doc.fontSize = 54;
  doc.font = "Montserrat-ExtraBold";
  doc.justification = ParagraphJustification.CENTER_JUSTIFY;
  doc.fillColor = isAccent ? [0.98, 0.8, 0.08] : [1.0, 1.0, 1.0];
  doc.applyStroke = true;
  doc.strokeColor = [0.0, 0.0, 0.0];
  doc.strokeWidth = 5;
  doc.applyFill = true;
  doc.tracking = 10;
  prop.setValue(doc);

  var pos = tl.property("ADBE Transform Group").property("ADBE Position");
  // Позиционируем на груди спикера (темная зона, отличный контраст)
  pos.setValue([comp.width / 2, 1320]);

  // Плавный Fade In/Out
  var op = tl.property("ADBE Transform Group").property("ADBE Opacity");
  op.setValueAtTime(inTime, 0);
  op.setValueAtTime(inTime + 0.1, 100);
  op.setValueAtTime(outTime - 0.1, 100);
  op.setValueAtTime(outTime, 0);

  return tl;
}

addSub(["У МЕНЯ НОРМАЛЬНЫЙ ДИПЛОМ,", "А У ТЕБЯ — НЕТ"], 0.0, 3.8, true);
addSub(["СООБЩЕСТВО ПСИХОЛОГОВ"], 3.8, 7.8, false);
addSub(["ТЕРАПИЯ ПРОИСХОДИТ", "НЕ ЧЕРЕЗ ДИПЛОМ"], 7.8, 23.8, true);
addSub(["КОГДА ОЩУЩЕНИЕ,", "ЧТО С БОГОМ ПОГОВОРИЛ"], 23.8, 36.8, false);
addSub(["ИСТИННЫЙ КОНТАКТ:", "ЧЕЛОВЕК — ЧЕЛОВЕК"], 36.8, 45.3, true);

return {
  ok: true,
  comp: comp.name,
  layers: comp.numLayers
};
`;

async function main() {
  console.log("Updating titles on chest position & tuning HDR exposure...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Chest Titles & HDR Normalization");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
