import { sendCommand } from "./send_ae_command.mjs";

const code = `
var comp = app.project.activeItem;
var adj = comp.layer("COLOR GRADE (HDR to SDR)");
var fx = adj.property("ADBE Effect Parade").property(1);
var res = [];
for (var i = 1; i <= fx.numProperties; i++) {
  var p = fx.property(i);
  res.push({
    index: i,
    name: p.name,
    matchName: p.matchName,
    type: String(p.propertyValueType)
  });
}
return res;
`;

sendCommand("system.runJsx", { code }, code)
  .then(r => console.log("Exposure props:", JSON.stringify(r, null, 2)))
  .catch(console.error);
