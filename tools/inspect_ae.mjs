import { sendCommand } from "./send_ae_command.mjs";

async function main() {
  const code = `
    var result = { items: [], comps: [] };
    for (var i = 1; i <= app.project.numItems; i++) {
      var item = app.project.item(i);
      result.items.push({ id: item.id, name: item.name, type: item.typeName });
      if (item instanceof CompItem) {
        var compInfo = { name: item.name, layers: [] };
        for (var l = 1; l <= item.numLayers; l++) {
          compInfo.layers.push({
            index: l,
            name: item.layer(l).name,
            inPoint: item.layer(l).inPoint,
            outPoint: item.layer(l).outPoint
          });
        }
        result.comps.push(compInfo);
      }
    }
    return result;
  `;
  const res = await sendCommand("system.runJsx", { code }, code, "Inspect Project");
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
