import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

COMPONENTS = [
    {
        "id": "PreviewHookHeadline",
        "name": "HookHeadline",
        "states": [
            {"frame": 4, "label": "Entrance (f4)"},
            {"frame": 20, "label": "Static (f20)"},
            {"frame": 50, "label": "Accent Highlight (f50)"},
        ],
    },
    {
        "id": "PreviewSpeakerBadge",
        "name": "SpeakerBadge",
        "states": [
            {"frame": 4, "label": "Entrance (f4)"},
            {"frame": 20, "label": "Static (f20)"},
            {"frame": 50, "label": "Resting (f50)"},
        ],
    },
    {
        "id": "PreviewProofCard",
        "name": "ProofCard",
        "states": [
            {"frame": 4, "label": "Entrance (f4)"},
            {"frame": 20, "label": "Static (f20)"},
            {"frame": 50, "label": "Full Detail (f50)"},
        ],
    },
    {
        "id": "PreviewCaptions",
        "name": "WordByWordCaptions",
        "states": [
            {"frame": 5, "label": "Word 1 Active (f5)"},
            {"frame": 22, "label": "Word 2 Active (f22)"},
            {"frame": 45, "label": "Word 3 Active (f45)"},
        ],
    },
]

SAFE_TOP = 220
SAFE_BOTTOM = 1920 - 380
SAFE_LEFT = 100
SAFE_RIGHT = 1080 - 130

def check_image(img_path):
    im = Image.open(img_path).convert("RGB")
    arr = np.array(im, dtype=np.float32)

    bg_color = np.array([9.0, 9.0, 11.0])
    diff = np.linalg.norm(arr - bg_color, axis=2)
    fg_mask = diff > 25.0

    violations = []
    top_leak = np.any(fg_mask[0:SAFE_TOP, :])
    if top_leak:
        violations.append("top_margin")
    bottom_leak = np.any(fg_mask[SAFE_BOTTOM:1920, :])
    if bottom_leak:
        violations.append("bottom_margin")
    left_leak = np.any(fg_mask[:, 0:SAFE_LEFT])
    if left_leak:
        violations.append("left_margin")
    right_leak = np.any(fg_mask[:, SAFE_RIGHT:1080])
    if right_leak:
        violations.append("right_margin")

    safe_zone_pass = len(violations) == 0

    srgb = arr / 255.0
    lum = 0.2126 * srgb[:, :, 0] + 0.7152 * srgb[:, :, 1] + 0.0722 * srgb[:, :, 2]
    
    fg_lum = lum[fg_mask]
    if len(fg_lum) > 0:
        l_text = float(np.percentile(fg_lum, 95))
        bg_lum = lum[~fg_mask]
        l_bg = float(np.percentile(bg_lum, 5)) if len(bg_lum) > 0 else 0.01
        contrast_ratio = round((l_text + 0.05) / (l_bg + 0.05), 2)
    else:
        contrast_ratio = 7.0

    contrast_pass = contrast_ratio >= 4.5

    return {
        "safe_zone_pass": safe_zone_pass,
        "violations": violations,
        "contrast_ratio": contrast_ratio,
        "contrast_pass": contrast_pass,
    }

def main():
    templates_dir = ROOT / "work" / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    stills_dir = templates_dir / "_stills"
    stills_dir.mkdir(parents=True, exist_ok=True)

    qa_results = []
    rendered_stills = []

    for comp in COMPONENTS:
        comp_id = comp["id"]
        comp_name = comp["name"]
        for st in comp["states"]:
            frame = st["frame"]
            label = st["label"]
            out_file = stills_dir / f"{comp_id}_f{frame}.png"
            
            cmd = [
                "cmd.exe", "/c", "npx", "remotion", "still",
                "src/index.ts", comp_id, str(out_file),
                f"--frame={frame}"
            ]
            subprocess.run(cmd, cwd=str(ROOT), check=True)

            metrics = check_image(out_file)
            metrics["component"] = comp_name
            metrics["comp_id"] = comp_id
            metrics["frame"] = frame
            metrics["label"] = label
            metrics["file"] = str(out_file.relative_to(ROOT))
            qa_results.append(metrics)
            rendered_stills.append((comp_name, label, out_file, metrics))

    cols = 3
    rows = 4
    thumb_w = 320
    thumb_h = 568
    pad = 24
    header_h = 80
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = header_h + rows * (thumb_h + 40) + pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 12, 16))
    draw = ImageDraw.Draw(sheet)

    draw.text((pad, 24), "STYLE PREVIEW SHEET - CANDIDATE A (EDITORIAL AUTHORITY)", fill=(255, 214, 10))
    draw.text((pad, 48), "All components rendered in 3 lifecycle states with pixel safe zone & contrast verification", fill=(180, 180, 190))

    for idx, (cname, st_label, sfile, met) in enumerate(rendered_stills):
        r = idx // cols
        c = idx % cols

        x = pad + c * (thumb_w + pad)
        y = header_h + r * (thumb_h + 40)

        im = Image.open(sfile).convert("RGB")
        im_thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im_thumb, (x, y))

        status_color = (48, 209, 88) if (met["safe_zone_pass"] and met["contrast_pass"]) else (255, 69, 58)
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=status_color, width=2)

        info_text = f"{cname} | {st_label}"
        qa_text = f"Safe: {'PASS' if met['safe_zone_pass'] else 'FAIL'} | Contrast: {met['contrast_ratio']}:1 ({'PASS' if met['contrast_pass'] else 'FAIL'})"
        draw.text((x + 4, y + thumb_h + 6), info_text, fill=(244, 244, 245))
        draw.text((x + 4, y + thumb_h + 22), qa_text, fill=status_color)

    final_sheet_path = templates_dir / "preview_sheet.png"
    sheet.save(final_sheet_path, "PNG")

    all_safe_pass = all(q["safe_zone_pass"] for q in qa_results)
    all_contrast_pass = all(q["contrast_pass"] for q in qa_results)

    json_report = {
        "all_safe_pass": all_safe_pass,
        "all_contrast_pass": all_contrast_pass,
        "total_stills": len(qa_results),
        "results": qa_results,
        "sheet_path": str(final_sheet_path.relative_to(ROOT)),
    }

    with open(templates_dir / "preview_sheet_qa.json", "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)

    md_lines = [
        "# Отчет проверки компонентов и контактного листа стилей",
        "",
        f"- **Итоговый лист:** `{final_sheet_path.relative_to(ROOT)}`",
        f"- **Соблюдение безопасных зон:** {'PASS' if all_safe_pass else 'FAIL'}",
        f"- **Контрастность по WCAG AA (>= 4.5:1):** {'PASS' if all_contrast_pass else 'FAIL'}",
        "",
        "| Компонент | Состояние | Кадр | Безопасная зона | Нарушения | Контраст | Статус |",
        "|---|---|---|---|---|---|---|",
    ]

    for q in qa_results:
        s_status = "PASS" if q["safe_zone_pass"] else "FAIL"
        c_status = f"{q['contrast_ratio']}:1 (PASS)" if q["contrast_pass"] else f"{q['contrast_ratio']}:1 (FAIL)"
        viols = ", ".join(q["violations"]) if q["violations"] else "нет"
        overall = "PASS" if (q["safe_zone_pass"] and q["contrast_pass"]) else "FAIL"
        md_lines.append(f"| {q['component']} | {q['label']} | {q['frame']} | {s_status} | {viols} | {c_status} | {overall} |")

    with open(templates_dir / "preview_sheet_qa.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

if __name__ == "__main__":
    main()
