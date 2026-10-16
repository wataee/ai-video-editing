import { sendCommand } from "./send_ae_command.mjs";

async function main() {
  const code = `
    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) {
      if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "Aziz - Viral Reel Master") {
        comp = app.project.item(i);
        break;
      }
    }
    var l = comp.layer("TEXT: SCRIPT психолога");
    if (l) {
      var prop = l.property("ADBE Text Properties").property("ADBE Text Document");
      var d = prop.value;
      d.font = "Caveat-Regular";
      prop.setValue(d);
      var verify = prop.value.font;
      return { setFont: "Caveat-Regular", actualFont: verify };
    }
    return "layer not found";
  `;
  const res = await sendCommand("system.runJsx", { code }, code, "Test Caveat-Regular");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
