import argparse
import json
import os
import sys
from pathlib import Path


def generate_beat_table(plan_data: dict, output_path: str = None) -> tuple[str, list[str]]:
    beats = plan_data.get("beats", [])
    warnings = []

    consecutive_typo = 0
    typo_streaks = []
    current_streak = []

    for b in beats:
        idx = b.get("beat_index", 0)
        v = b.get("visual", "")
        if v == "typography":
            consecutive_typo += 1
            current_streak.append(idx)
            if consecutive_typo > 2:
                typo_streaks.append(list(current_streak))
        else:
            consecutive_typo = 0
            current_streak = []

    if typo_streaks:
        flat_indices = sorted(list({i for streak in typo_streaks for i in streak}))
        warnings.append(
            f"ПРЕДУПРЕЖДЕНИЕ: ролик превращается в слайды! Режим 'visual: typography' "
            f"используется подряд более 2 раз на битах: {flat_indices}. "
            f"Добавьте реальные доказательства (скриншот, график, продукт) или кадры спикера."
        )

    for b in beats:
        idx = b.get("beat_index", 0)
        v = b.get("visual", "")
        proof = b.get("proof_source")
        if v in ["proof", "chart", "broll"]:
            if not proof:
                warnings.append(f"Бит {idx}: visual='{v}', но proof_source не указан!")
            elif not os.path.exists(proof):
                warnings.append(f"Бит {idx}: proof_source файл не найден на диске: '{proof}'")

    md_lines = []
    project_id = plan_data.get("project_id", "clip")
    approved = plan_data.get("approved", False)

    md_lines.append(f"# Битовая карта монтажа (Beat Table): {project_id}")
    md_lines.append(f"- **Статус утверждения:** {'✅ УТВЕРЖДЕНО' if approved else '❌ НЕ УТВЕРЖДЕНО (финальный рендер заблокирован)'}")
    md_lines.append(f"- **Всего битов:** {len(beats)}")
    md_lines.append(f"- **Движок:** {plan_data.get('engine', 'remotion')}")
    md_lines.append("")

    if warnings:
        md_lines.append("## ⚠️ Предупреждения")
        for w in warnings:
            md_lines.append(f"- > **{w}**")
        md_lines.append("")

    md_lines.append("## Таблица битов")
    md_lines.append("| Бит | Время | Фраза | Визуал | Пруф / Материал | Камера | SFX | Мотивация склейки | Почему (Why) | Утверждено |")
    md_lines.append("|:---:|:---:|---|:---:|---|:---:|:---:|---|---|:---:|")

    for b in beats:
        idx = b.get("beat_index", 0)
        tr = b.get("time_range", [0, 0])
        tr_str = f"{tr[0]:.1f}–{tr[1]:.1f}s" if isinstance(tr, list) and len(tr) == 2 else str(tr)
        line = b.get("line", "").replace("|", "/")
        vis = b.get("visual", "")
        proof = b.get("proof_source")
        proof_str = proof if proof else "—"
        if proof and not os.path.exists(proof):
            proof_str = f"⚠️ `{proof}` (отсутствует)"
        cam = b.get("camera", "static")
        sfx = b.get("sfx", "none")
        mot = b.get("cut_motivation", "")
        why = b.get("why", "").replace("|", "/")
        appr = "✅" if b.get("approved", False) else "⏳"

        vis_badge = vis
        if vis == "typography":
            vis_badge = f"**{vis}**"

        md_lines.append(f"| {idx} | {tr_str} | {line} | {vis_badge} | {proof_str} | {cam} | `{sfx}` | {mot} | {why} | {appr} |")

    md_content = "\n".join(md_lines) + "\n"

    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(md_content, encoding="utf-8")

    return md_content, warnings


def main():
    parser = argparse.ArgumentParser(description="Генерация Beat Table из edit_plan.json")
    parser.add_argument("plan_path", help="Путь к edit_plan.json")
    parser.add_argument("--transcript", "-t", default=None, help="Опциональный путь к транскрипту")
    parser.add_argument("--output", "-o", default=None, help="Путь к выходному .md файлу")
    args = parser.parse_args()

    plan_file = Path(args.plan_path).resolve()
    if not plan_file.exists():
        print(f"Ошибка: файл плана не найден: {plan_file}", file=sys.stderr)
        sys.exit(1)

    with open(plan_file, "r", encoding="utf-8") as f:
        plan_data = json.load(f)

    out_file = args.output
    if not out_file:
        out_file = "work/plan/beat_table.md"

    md_content, warnings = generate_beat_table(plan_data, out_file)
    print(f"Beat Table сгенерирована: {out_file}")
    if warnings:
        print("\nОБНАРУЖЕНЫ ПРЕДУПРЕЖДЕНИЯ:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("Проверка структуры битов пройдена без замечаний.")


if __name__ == "__main__":
    main()
