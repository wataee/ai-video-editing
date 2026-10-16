import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINTEREST_DIR = ROOT / "references" / "pinterest"
CATALOG_PATH = PINTEREST_DIR / "CATALOG.md"
JSON_CATALOG_PATH = PINTEREST_DIR / "catalog.json"

CATEGORY_NAMES = {
    "01_business_minimal": "Бизнес & Экспертный минимализм (Clean Talking Head)",
    "02_kinetic_viral_retention": "Кинетическая типографика & Retention (Hormozi / Viral)",
    "03_vox_documentary_story": "Vox-документалистика & Сторителлинг (Paper, Charts, Parallax)",
    "04_luxury_dark_aesthetic": "Luxury Dark & Glassmorphism (Apple-Style, Liquid Glass)",
    "05_cyber_tech_breakdown": "Cyber & Tech Breakdown (Fireship, Code, HUD, UI Overlays)",
    "06_podcast_splitscreen_subtitles": "Подкасты & Сплит-Скрин Интервью (Podcast & Multi-Speaker)",
    "07_mixed_media_paper_collage": "Mixed Media & Рваный Коллаж (Paper Tear & Grunge)",
    "08_product_3d_mockup_showcase": "Продуктовый Моушн & E-Commerce 3D (Product Showcase)",
    "09_cinematic_travel_story": "Кинематографичный Тревел & Лайфстайл (Cinematic Travel)",
    "10_fitness_motivation_grit": "Фитнес & Жесткая Мотивация (Fitness & Grit)"
}

def detect_role(filename: str) -> str:
    fn = filename.lower()
    if any(k in fn for k in ["hook", "attention", "hero", "title_card", "statue_cutout", "moody_stencil", "billion_dollar", "sports_motion", "agency_motion"]):
        return "ROLE_HOOK_HERO (Захват внимания, 0-3s)"
    elif any(k in fn for k in ["caption", "subtitle", "punch", "davinci_talking_head", "director", "wisdom"]):
        return "ROLE_SUBTITLE_ENGINE (Титры и подача спикера)"
    elif any(k in fn for k in ["mockup", "phone", "drink", "cup", "product", "folder", "ketone", "starbucks", "powerbank"]):
        return "ROLE_DEVICE_MOCKUP (3D/2D презентация интерфейса и продукта)"
    elif any(k in fn for k in ["proof", "document", "highlighter", "newspaper", "venezuela"]):
        return "ROLE_DOCUMENT_PROOF (Пруф-материалы, статьи, хайлайтер)"
    elif any(k in fn for k in ["splitscreen", "multicam", "before", "breakdown_target"]):
        return "ROLE_SPLIT_SCREEN (Сравнения до/после, 2 спикера)"
    elif any(k in fn for k in ["callout", "metric", "timeline", "dashboard", "fui", "brain", "explainer", "halo"]):
        return "ROLE_CALLOUT_UI (Плашки с метриками, графики, данные)"
    elif any(k in fn for k in ["whip", "transition", "seam"]):
        return "ROLE_TRANSITION_SEAM (Бесшовные склейки)"
    elif any(k in fn for k in ["paper", "collage", "crumpled", "street_flow"]):
        return "ROLE_TEXTURE_TACTILE (Тактильная фактура и нарезка)"
    return "ROLE_SUPPORTING_ASSET (Фоновый ассет / B-Roll)"

def scan_references():
    if not PINTEREST_DIR.exists():
        print(f"Directory {PINTEREST_DIR} not found.")
        sys.exit(1)
        
    categories = {}
    total_media = 0
    
    for sub in sorted(PINTEREST_DIR.iterdir()):
        if not sub.is_dir():
            continue
        folder_name = sub.name
        cat_title = CATEGORY_NAMES.get(folder_name, folder_name)
        
        media_files = []
        md_cards = []
        blueprint_exists = (sub / "assembly_blueprint.md").exists()
        manifest_exists = (sub / "style_manifest.md").exists()
        
        for item in sorted(sub.iterdir()):
            if item.is_file():
                suffix = item.suffix.lower()
                if suffix in [".mp4", ".mov", ".gif", ".webp", ".png", ".jpg", ".jpeg"]:
                    role = detect_role(item.name)
                    media_files.append({
                        "name": item.name,
                        "path": str(item.relative_to(ROOT)).replace("\\", "/"),
                        "size_kb": round(item.stat().st_size / 1024, 1),
                        "role": role
                    })
                elif suffix == ".md" and item.name not in ["README.md", "style_manifest.md", "assembly_blueprint.md"]:
                    md_cards.append({
                        "name": item.name,
                        "path": str(item.relative_to(ROOT)).replace("\\", "/")
                    })
                    
        total_media += len(media_files)
        categories[folder_name] = {
            "title": cat_title,
            "path": str(sub.relative_to(ROOT)).replace("\\", "/"),
            "blueprint": f"{sub.relative_to(ROOT).as_posix()}/assembly_blueprint.md" if blueprint_exists else None,
            "manifest": f"{sub.relative_to(ROOT).as_posix()}/style_manifest.md" if manifest_exists else None,
            "media_files": media_files,
            "cards": md_cards
        }
        
    catalog_md = []
    catalog_md.append("# Каталог креативных референсов Pinterest & Motion Design\n")
    catalog_md.append("> **WORKSTATION INDEX & ANTI-MISHMASH PROTOCOL**\n")
    catalog_md.append("> Этот каталог генерируется автоматически через `python tools/sync_pinterest_references.py`.\n")
    catalog_md.append("> **Правило для Claude:** Строго изолируй выбранный стиль видео. Используй `assembly_blueprint.md` каждой категории и бери референсы строго по их ролям (`ROLE_HOOK_HERO`, `ROLE_CALLOUT_UI`, `ROLE_SUBTITLE_ENGINE`), чтобы не создавать визуальную «солянку».\n\n")
    catalog_md.append(f"**Всего категорий:** {len(categories)} | **Всего проверенных медиа-референсов:** {total_media}\n")
    catalog_md.append("---\n\n")
    
    for folder, data in categories.items():
        catalog_md.append(f"## {data['title']}\n")
        catalog_md.append(f"- **Папка:** `{data['path']}/`\n")
        if data['blueprint']:
            catalog_md.append(f"- 📐 **Сборочный чертеж монтажа:** [`assembly_blueprint.md`]({data['blueprint']})\n")
        if data['manifest']:
            catalog_md.append(f"- 🎨 **Манифест стиля:** [`style_manifest.md`]({data['manifest']})\n")
        
        catalog_md.append(f"- **Медиа-референсов:** {len(data['media_files'])} | **Карточек разбора:** {len(data['cards'])}\n\n")
        
        if data['media_files']:
            catalog_md.append("### Структурированные референсы по ролям в таймлайне:\n")
            roles_grouped = {}
            for m in data['media_files']:
                r = m['role']
                roles_grouped.setdefault(r, []).append(m)
                
            for role_name, files in sorted(roles_grouped.items()):
                catalog_md.append(f"#### {role_name}:\n")
                for f in files:
                    catalog_md.append(f"- `{f['name']}` ({f['size_kb']} KB) -> [`{f['name']}`]({f['path']})\n")
                catalog_md.append("\n")
                
        if data['cards']:
            catalog_md.append("### Дополнительные карточки приёмов и хуков:\n")
            for c in data['cards']:
                catalog_md.append(f"- [{c['name']}]({c['path']})\n")
            catalog_md.append("\n")
            
        catalog_md.append("---\n\n")
        
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        f.write("".join(catalog_md))
        
    with open(JSON_CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
        
    print(f"Catalog synced successfully: {CATALOG_PATH}")
    print(f"Total categories: {len(categories)}, Total verified media references: {total_media}")

if __name__ == "__main__":
    scan_references()
