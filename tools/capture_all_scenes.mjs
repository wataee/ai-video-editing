import { sendCommand } from "./send_ae_command.mjs";

async function main() {
  const code = `
    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) {
      var item = app.project.item(i);
      if (item instanceof CompItem && item.name === "Aziz - Viral Reel Master") {
        comp = item;
        break;
      }
    }
    if (!comp) return "Comp not found";

    var captures = [
      { time: 2.0, path: "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/proof/scene1_hook.png" },
      { time: 10.5, path: "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/proof/scene2_thesis.png" },
      { time: 26.5, path: "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/proof/scene3_climax.png" },
      { time: 39.5, path: "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/proof/scene4_conclusion.png" }
    ];

    var out = [];
    for (var c = 0; c < captures.length; c++) {
      var cap = captures[c];
      var f = new File(cap.path);
      if (f.exists) f.remove();
      comp.saveFrameToPng(cap.time, f);
      out.push(cap.path);
    }
    return out;
  `;

  const res = await sendCommand("system.runJsx", { code }, code, "Capture All Scenes");
  console.log("Captured:", JSON.stringify(res, null, 2));
}

main().catch(console.error);
