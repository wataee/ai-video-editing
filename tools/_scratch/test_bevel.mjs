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

// Регулируем виньетку
var vig = comp.layer("STUDIO VIGNETTE (Moody Studio)");
if (vig) {
  vig.property("ADBE Transform Group").property("ADBE Opacity").setValue(24);
}

// Тестируем заголовок 1
var tMain = comp.layer("TEXT: MAIN ДИПЛОМ");
if (tMain) {
  var pMain = tMain.property("ADBE Text Properties").property("ADBE Text Document");
  var dMain = pMain.value;
  dMain.fontSize = 136;
  dMain.tracking = 15;
  pMain.setValue(dMain);

  // Добавляем Bevel Edges для 3D фаски как на референсе
  try {
    var bev = tMain.property("ADBE Effect Parade").addProperty("ADBE Bevel Edges");
    if (bev) {
      bev.property("ADBE Bevel Edges-0001").setValue(1.5); // Thickness
      bev.property("ADBE Bevel Edges-0002").setValue(45);  // Light Angle
      bev.property("ADBE Bevel Edges-0003").setValue(0.5); // Light Intensity
    }
  } catch(eB) {}
}

var tScript = comp.layer("TEXT: SCRIPT психолога");
if (tScript) {
  var pScript = tScript.property("ADBE Text Properties").property("ADBE Text Document");
  var dScript = pScript.value;
  dScript.font = "Caveat-Regular";
  dScript.fontSize = 148; // Крупный, выразительный рукописный шрифт
  dScript.strokeWidth = 4.5;
  dScript.tracking = 5;
  pScript.setValue(dScript);

  // Позиционируем прямо внахлест на правый нижний край слова ДИПЛОМ
  var pos = tScript.property("ADBE Transform Group").property("ADBE Position");
  pos.setValue([comp.width / 2 + 75, 1425]);
  tScript.property("ADBE Transform Group").property("ADBE Rotate Z").setValue(-9);
}

return "OK";
`;

async function main() {
  const res = await sendCommand("system.runJsx", { code: extendscriptCode }, extendscriptCode, "Test Bevel & Big Caveat");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
