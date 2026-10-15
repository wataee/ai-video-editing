import { broker } from "./after-effects-mcp/dist/index.js";

async function main() {
  console.log("Checking instances...");
  const instances = broker.listInstances();
  console.log("Live instances:", instances);
  if (instances.length === 0) {
    console.error("No live instances found!");
    process.exit(1);
  }

  console.log("Invoking edit.fromCuts in After Effects...");
  const result = await broker.invoke({
    method: "edit.fromCuts",
    args: {
      path: "C:/Users/timur/Videos/AI-Video-Editing/clients/aziz/raw/a_roll/IMG_2137.MOV",
      comp_name: "Aziz - Viral Reel (1080x1920)",
      segments: [
        { start: 0.0, end: 3.8 },   // Сцена 1: Хук
        { start: 12.0, end: 16.0 }, // Сцена 2: Контекст сообщества
        { start: 16.0, end: 32.0 }, // Сцена 3: Истинная терапия
        { start: 32.0, end: 45.0 }, // Сцена 4: Эмоциональный пик
        { start: 51.0, end: 59.5 }  // Сцена 5: Финальный панчлайн
      ]
    },
    undoName: "AI Assembly: Aziz Reel"
  });

  console.log("Result:", JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
