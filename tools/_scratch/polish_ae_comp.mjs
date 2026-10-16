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

// 1. Настройка масштаба и зумов (Punch-in) по нашему регламенту монтажера
for (var l = 1; l <= comp.numLayers; l++) {
  var layer = comp.layer(l);
  var tg = layer.property("ADBE Transform Group");
  if (!tg) continue;
  
  if (layer.name.indexOf("Keep 1") !== -1) {
    tg.property("ADBE Scale").setValue([106, 106, 100]);
    tg.property("ADBE Position").setValue([comp.width / 2, comp.height / 2 - 20]);
  } else if (layer.name.indexOf("Keep 2") !== -1) {
    tg.property("ADBE Scale").setValue([100, 100, 100]);
    tg.property("ADBE Position").setValue([comp.width / 2, comp.height / 2]);
  } else if (layer.name.indexOf("Keep 3") !== -1) {
    // Панч-ин на ключевом аргументе против дипломов
    tg.property("ADBE Scale").setValue([114, 114, 100]);
    tg.property("ADBE Position").setValue([comp.width / 2, comp.height / 2 - 40]);
  } else if (layer.name.indexOf("Keep 4") !== -1) {
    // Плавный отъезд на откровении
    tg.property("ADBE Scale").setValue([103, 103, 100]);
    tg.property("ADBE Position").setValue([comp.width / 2, comp.height / 2]);
  } else if (layer.name.indexOf("Keep 5") !== -1) {
    tg.property("ADBE Scale").setValue([108, 108, 100]);
    tg.property("ADBE Position").setValue([comp.width / 2, comp.height / 2 - 20]);
  }
}

// 2. Добавление Adjustment Layer для нормализации пересветов iPhone HDR
var adj = comp.layers.addSolid([1, 1, 1], "COLOR GRADE (HDR Fix)", comp.width, comp.height, 1, comp.duration);
adj.adjustmentLayer = true;
try {
  var fx = adj.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
  if (fx) {
    fx.property("ADBE Exposure2-0002").setValue(-1.1); // Снижаем экспозицию для возврата деталей лица
    fx.property("ADBE Exposure2-0004").setValue(0.92); // Гамма
  }
} catch (eExp) {}

// 3. Импорт и расстановка SFX слоев
function importAndPlaceSfx(filePath, layerName, startTime, volDb) {
  var f = new File(filePath);
  if (!f.exists) return null;
  var io = new ImportOptions(f);
  io.importAs = ImportAsType.FOOTAGE;
  var sfxItem = app.project.importFile(io);
  var sfxLayer = comp.layers.add(sfxItem);
  sfxLayer.name = layerName;
  sfxLayer.startTime = startTime;
  sfxLayer.inPoint = startTime;
  sfxLayer.outPoint = startTime + sfxItem.duration;
  try {
    var audio = sfxLayer.property("ADBE Audio Group").property("ADBE Audio Levels - 0001");
    if (audio) audio.setValue([volDb, volDb]);
  } catch (eVol) {}
  return sfxLayer;
}

var sfx1 = importAndPlaceSfx("C:/Users/timur/Videos/AI-Video-Editing/assets/sfx/hits/sub_bass_thud.wav", "SFX: Sub Bass Punch", 1.3, -3.0);
var sfx2 = importAndPlaceSfx("C:/Users/timur/Videos/AI-Video-Editing/assets/sfx/whooshes/whoosh_clean_fast.wav", "SFX: Transition Whoosh", 3.7, -6.0);
var sfx3 = importAndPlaceSfx("C:/Users/timur/Videos/AI-Video-Editing/assets/sfx/clicks/switch_01.wav", "SFX: Switch Thesis", 7.7, -4.0);
var sfx4 = importAndPlaceSfx("C:/Users/timur/Videos/AI-Video-Editing/assets/sfx/pops/glass_pop.wav", "SFX: Emotion Pop", 23.7, -5.0);
var sfx5 = importAndPlaceSfx("C:/Users/timur/Videos/AI-Video-Editing/assets/sfx/whooshes/whoosh_subtle_air.wav", "SFX: Final Whoosh", 36.7, -6.0);

// 4. Текстовые плашки заголовков (в верхней безопасной зоне)
function addHeadline(textStr, inTime, outTime, isAccent) {
  var txtLayer = comp.layers.addText(textStr);
  txtLayer.name = "TEXT: " + textStr;
  txtLayer.inPoint = inTime;
  txtLayer.outPoint = outTime;
  var txtProp = txtLayer.property("ADBE Text Properties").property("ADBE Text Document");
  var doc = txtProp.value;
  doc.fontSize = 50;
  doc.font = "Montserrat-ExtraBold";
  doc.justification = ParagraphJustification.CENTER_JUSTIFY;
  if (isAccent) {
    doc.fillColor = [0.98, 0.8, 0.08]; // Yellow Accent
  } else {
    doc.fillColor = [1.0, 1.0, 1.0]; // Crisp White
  }
  doc.applyStroke = true;
  doc.strokeColor = [0, 0, 0];
  doc.strokeWidth = 4;
  txtProp.setValue(doc);
  
  var pos = txtLayer.property("ADBE Transform Group").property("ADBE Position");
  pos.setValue([comp.width / 2, 380]);
  return txtLayer;
}

addHeadline("«У МЕНЯ НОРМАЛЬНЫЙ ДИПЛОМ»", 0.0, 3.8, true);
addHeadline("ТЕРАПИЯ ≠ ДИПЛОМ", 7.8, 23.8, false);
addHeadline("ИСТИННЫЙ КОНТАКТ: ЧЕЛОВЕК — ЧЕЛОВЕК", 36.8, 45.3, true);

return {
  status: "success",
  comp: comp.name,
  numLayers: comp.numLayers,
  duration: comp.duration
};
`;

async function main() {
  console.log("Applying Senior Editor Polish to After Effects comp...");
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Senior Editor Polish: Aziz Reel");
  console.log("Result:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
