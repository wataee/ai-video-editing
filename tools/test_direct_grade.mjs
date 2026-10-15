import { sendCommand } from "./send_ae_command.mjs";

const code = `
var comp = app.project.activeItem;
for (var i = 1; i <= comp.numLayers; i++) {
  var l = comp.layer(i);
  if (l.name.indexOf("Keep ") === 0) {
    // Add Exposure directly to the video layer
    try {
      var exp = l.property("ADBE Effect Parade").addProperty("ADBE Exposure2");
      exp.property("ADBE Exposure2-0003").setValue(-2.5); // Direct exposure drop
      exp.property("ADBE Exposure2-0005").setValue(0.90);
    } catch(e) {}
  }
}
return "Applied direct exposure to all cuts";
`;

sendCommand("system.runJsx", { code }, code)
  .then(r => console.log("Result:", JSON.stringify(r, null, 2)))
  .catch(console.error);
