import fs from "fs";
import path from "path";

const rootDir = process.cwd();
const planCandidates = [
  path.join(rootDir, "work", "plan", "edit_plan.json"),
];

let targetPlan = null;
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--plan" && args[i + 1]) {
    targetPlan = path.resolve(args[i + 1]);
    break;
  }
}

if (!targetPlan) {
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("-")) continue;
    const resolved = path.resolve(a);
    if (a.endsWith(".json")) {
      targetPlan = resolved;
      break;
    }
    if (fs.existsSync(resolved) && fs.statSync(resolved).isDirectory()) {
      targetPlan = resolved;
      break;
    }
  }
}

if (!targetPlan) {
  for (const p of planCandidates) {
    if (fs.existsSync(p)) {
      targetPlan = p;
      break;
    }
  }
}

if (targetPlan && fs.existsSync(targetPlan) && fs.statSync(targetPlan).isDirectory()) {
  targetPlan = path.join(targetPlan, "edit_plan.json");
}

if (!targetPlan || !fs.existsSync(targetPlan)) {
  console.error("==================================================================");
  console.error("❌ ПЛАН МОНТАЖА НЕ НАЙДЕН (APPROVAL GATE BLOCKED)");
  console.error(`Указанный или стандартный файл плана не существует: ${targetPlan || "work/plan/edit_plan.json"}`);
  console.error("Для финального рендера требуется существующий утвержденный edit_plan.json.");
  console.error("Используйте --plan <путь> для указания пути к плану монтажа.");
  console.error("==================================================================");
  process.exit(1);
}

try {
  const content = fs.readFileSync(targetPlan, "utf-8");
  const data = JSON.parse(content);
  if (data.approved !== true) {
    console.error("==================================================================");
    console.error("❌ ФИНАЛЬНЫЙ РЕНДЕР ЗАБЛОКИРОВАН (APPROVAL GATE)");
    console.error(`План монтажа: ${targetPlan}`);
    console.error('Поле "approved" имеет значение: false');
    console.error("");
    console.error("Согласно правилу .claude/rulebooks/03-beat-map-and-planning.md,");
    console.error("финальный мастер-рендер требует подтверждения человека.");
    console.error("");
    console.error("1. Проверьте beat table: python tools/beat_table.py");
    console.error("2. Проверьте контактный лист: work/plan/contact_sheet_plan.png");
    console.error('3. Для утверждения установите в edit_plan.json: "approved": true');
    console.error("4. Для чернового предпросмотра запускайте: npm run draft");
    console.error("==================================================================");
    process.exit(1);
  } else {
    console.log(`✅ План монтажа утвержден ("approved": true): ${targetPlan}`);
    process.exit(0);
  }
} catch (err) {
  console.error("Ошибка при проверке edit_plan.json:", err.message);
  process.exit(1);
}
