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
    var res = {};
    res.hasSaveFrame = (typeof comp.saveFrameToPng === "function");
    res.hasSaveFrameToPng = (typeof comp.saveFrameToPng);
    
    // Test renderQueue save frame
    // or test File object
    var f = new File("C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/work/test_ae.png");
    try {
      comp.saveFrameToPng(2.0, f);
      res.saveFrameCall = "ok";
    } catch(e) {
      res.saveFrameError = e.toString();
    }
    return res;
  `;
  const res = await sendCommand("system.runJsx", { code }, code, "Check saveFrame");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
