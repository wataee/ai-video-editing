import { sendCommand } from "./send_ae_command.mjs";

async function main() {
  const time = parseFloat(process.argv[2] || "2.0");
  const outFile = process.argv[3] || "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/ae_frame_test.png";

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
    var f = new File("${outFile}");
    if (f.exists) f.remove();
    comp.saveFrameToPng(${time}, f);
    return { exists: f.exists, path: "${outFile}", size: f.length };
  `;

  const res = await sendCommand("system.runJsx", { code }, code, "Capture Frame");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
