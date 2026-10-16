import fs from "fs";
import path from "path";

const rootDir = process.cwd();
const planCandidates = [
  path.join(rootDir, "work", "plan", "edit_plan.json"),
  path.join(rootDir, "rules", "templates", "edit_plan.template.json"),
  path.join(rootDir, ".claude", "rulebooks", "templates", "edit_plan.template.json"),
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
  for (const p of planCandidates) {
    if (fs.existsSync(p)) {
      targetPlan = p;
      break;
    }
  }
}

if (!targetPlan || !fs.existsSync(targetPlan)) {
  console.log("ℹ️ Файл edit_plan.json не найден. Продолжение без блокировки.");
  process.exit(0);
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
