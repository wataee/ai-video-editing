import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const DATA_DIR = "C:/Users/timur/Videos/AI-Video-Editing/work/.ae-mcp/instances/default";

export async function sendCommand(method, args = {}, code = undefined, undoName = "AI Video Editing") {
  const requestId = crypto.randomUUID();
  const command = {
    protocolVersion: 1,
    requestId,
    op: "invoke",
    method,
    args,
    code,
    meta: {
      undoName,
      timeoutMs: 30000
    },
    createdAt: new Date().toISOString()
  };

  const commandPath = path.join(DATA_DIR, "command.json");
  const resultPath = path.join(DATA_DIR, "result.json");

  // Remove existing result
  if (fs.existsSync(resultPath)) {
    try { fs.unlinkSync(resultPath); } catch (e) {}
  }

  // Write command atomically
  const tmpPath = `${commandPath}.tmp`;
  fs.writeFileSync(tmpPath, JSON.stringify(command, null, 2), "utf8");
  fs.renameSync(tmpPath, commandPath);

  console.log(`[IPC] Sent command "${method}" (ID: ${requestId.slice(0, 8)})...`);

  // Wait for result.json
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    if (fs.existsSync(resultPath)) {
      try {
        const raw = fs.readFileSync(resultPath, "utf8");
        const res = JSON.parse(raw);
        if (res.requestId === requestId) {
          return res;
        }
      } catch (e) {
        // Wait for file write to complete
      }
    }
    await new Promise(r => setTimeout(r, 80));
  }
  throw new Error("Timeout waiting for After Effects response (30s)");
}

// If run directly from CLI
if (process.argv[1]?.endsWith("send_ae_command.mjs")) {
  const method = process.argv[2] || "edit.fromCuts";
  const rawPath = "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/raw/a_roll/IMG_2137.MOV";

  sendCommand(method, {
    path: rawPath,
    comp_name: "Aziz - Viral Reel Master",
    segments: [
      { start: 0.0, end: 3.8 },   // Сцена 1: Хук ("У меня нормальный диплом...")
      { start: 12.0, end: 16.0 }, // Сцена 2: Контекст в сообществе психологов
      { start: 16.0, end: 32.0 }, // Сцена 3: Истинная терапия (не через потрясывание дипломом)
      { start: 32.0, end: 45.0 }, // Сцена 4: Эмоциональный пик (с Богом поговорил)
      { start: 51.0, end: 59.5 }  // Сцена 5: Финальный вывод (контакт человек-человек)
    ]
  }, undefined, "AI Assembly: Aziz Reel")
    .then(res => {
      console.log("Success! After Effects Response:", JSON.stringify(res, null, 2));
      process.exit(0);
    })
    .catch(err => {
      console.error("Failed:", err.message);
      process.exit(1);
    });
}
