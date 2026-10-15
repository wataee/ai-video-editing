import { sendCommand } from "./send_ae_command.mjs";

async function main() {
  const code = `
    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) {
      if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "Aziz - Viral Reel Master") {
        comp = item = app.project.item(i);
        break;
      }
    }
    var t = comp.layers.addText("test");
    var doc = t.property("ADBE Text Properties").property("ADBE Text Document").value;
    var res = {};
    var testFonts = ["Caveat-Bold", "Caveat-Regular", "Caveat", "SegoeScript-Bold"];
    for (var f = 0; f < testFonts.length; f++) {
      var fname = testFonts[f];
      try {
        doc.font = fname;
        t.property("ADBE Text Properties").property("ADBE Text Document").setValue(doc);
        res[fname] = "AVAILABLE";
      } catch(e) {
        res[fname] = e.toString();
      }
    }
    t.remove();
    return res;
  `;
  const res = await sendCommand("system.runJsx", { code }, code, "Test Font");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
