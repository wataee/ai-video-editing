# 07. Creator Style Presets & Archetypes

## 1. The 5 Production Archetypes

### Archetype 1: `ali-minimal-workspace` (Ali Abdaal Aesthetic)
- **Concept**: Clean, approachable, intellectual, modern study/workspace productivity.
- **Palette**:
  - Background: Off-white / Warm paper `#F9F9F8` or Soft Charcoal `#1A1A1E`.
  - Primary Accent: Soft Coral `#FF6B6B` or Slate Blue `#3B82F6`.
  - Card Fill: White `#FFFFFF` with ultra-fine border `rgba(0,0,0,0.06)`.
- **Typography**: Inter (Body), SF Pro / Helvetica (Headers). Minimalist casing.
- **Motion**: Gentle subtle eases (`damping: 20, stiffness: 80`), soft floating cards, paper rustles.
- **SFX**: Subtle acoustic clicks, pencil on paper, soft switch pops.

### Archetype 2: `gadzhi-noir-luxury` (Iman Gadzhi Aesthetic)
- **Concept**: High-status, mysterious, cinematic financial documentary.
- **Palette**:
  - Background: Deep Obsidian `#070709`.
  - Accents: Desaturated Platinum `#E2E8F0`, Antique Gold `#C5A880`, Emerald Accent `#10B981`.
  - Cards: High-gloss black with subtle specular edge highlight (`1px solid rgba(255,255,255,0.12)`).
- **Typography**: Montserrat Black (All-caps punches) + Caveat / Segoe Script (golden/white signature callouts).
- **Motion**: Cinematic slow zoom (`push-in` 1.0 -> 1.05), vignette pulsing, film grain texture.
- **SFX**: Deep sub-bass rumbles, low cinematic impacts, dark whooshes.

### Archetype 3: `vox-editorial-data` (Vox / Johnny Harris Aesthetic)
- **Concept**: Data journalism, investigative cartography, documentary explainers.
- **Palette**:
  - Background: Charcoal `#111116` with isometric or Cartesian grid lines.
  - Accents: Canary Yellow `#FFDE59`, Highlighter Neon `#FF3B30`, Cyan `#00F0FF`.
- **Typography**: Space Mono / Roboto Mono (metrics) + Oswald / Montserrat (headlines).
- **Motion**: Dynamic spring-driven bar charts, highlighted callout circles, ruler measurements.
- **SFX**: Fast digital clicks, camera shutter, paper slide, marker squeak.

### Archetype 4: `apple-liquid-glass` (Cupertino Keynote Aesthetic)
- **Concept**: State-of-the-art UI hardware presentation, precision engineering.
- **Palette**:
  - Surface: `backdropFilter: 'blur(24px) saturate(180%)'`, `background: 'rgba(255,255,255,0.14)'`.
  - Border: `1px solid rgba(255,255,255,0.28)`, `borderRadius: 28px`.
  - Shadow: Multi-layered soft ambient occlusion `0 20px 40px rgba(0,0,0,0.35)`.
- **Typography**: SF Pro Display / Inter Semi-bold.
- **Motion**: Clean spring curves, liquid expansion, device tilts.
- **SFX**: Air swooshes, clean glass tinks, soft tap clicks.

### Archetype 5: `hormozi-kinetic-punch` (Alex Hormozi Aesthetic)
- **Concept**: Relentless energy, bold sales psychology, high-velocity retention.
- **Palette**:
  - Background: Pitch Black `#000000` or High-contrast Green `#00FF66`.
  - Accents: Acid Yellow `#FFFF00`, Fire Orange `#FF6600`.
- **Typography**: Giant Montserrat Black or Rubik ExtraBold, word-by-word bold highlighting, 2-word groups.
- **Motion**: Instantaneous snaps (damping: 10, stiffness: 200), explosive scale-ups, screen shake.
- **SFX**: Heavy whip whooshes, boxing punches, cash register dings, comic pops.

---

## 2. Creative Reference Mapping (Pinterest Library)

При формировании `beat_sheet.json` и `edit_plan.json` агент обязан брать конкретные приемы, параметры spring и хуки из папки `references/pinterest/`:

| Архетип | Папка референсов | Манифест стиля | Сборочный чертеж |
|---|---|---|---|
| `ali-minimal-workspace` | `references/pinterest/01_business_minimal/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/01_business_minimal/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/01_business_minimal/assembly_blueprint.md) |
| `hormozi-kinetic-punch` | `references/pinterest/02_kinetic_viral_retention/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/02_kinetic_viral_retention/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/02_kinetic_viral_retention/assembly_blueprint.md) |
| `vox-editorial-data` | `references/pinterest/03_vox_documentary_story/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/03_vox_documentary_story/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/03_vox_documentary_story/assembly_blueprint.md) |
| `apple-liquid-glass` | `references/pinterest/04_luxury_dark_aesthetic/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/04_luxury_dark_aesthetic/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/04_luxury_dark_aesthetic/assembly_blueprint.md) |
| `cyber-tech-breakdown` | `references/pinterest/05_cyber_tech_breakdown/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/05_cyber_tech_breakdown/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/05_cyber_tech_breakdown/assembly_blueprint.md) |
| `podcast-splitscreen` | `references/pinterest/06_podcast_splitscreen_subtitles/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/06_podcast_splitscreen_subtitles/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/06_podcast_splitscreen_subtitles/assembly_blueprint.md) |
| `mixed-media-collage` | `references/pinterest/07_mixed_media_paper_collage/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/07_mixed_media_paper_collage/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/07_mixed_media_paper_collage/assembly_blueprint.md) |
| `product-3d-showcase` | `references/pinterest/08_product_3d_mockup_showcase/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/08_product_3d_mockup_showcase/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/08_product_3d_mockup_showcase/assembly_blueprint.md) |
| `cinematic-travel` | `references/pinterest/09_cinematic_travel_story/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/09_cinematic_travel_story/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/09_cinematic_travel_story/assembly_blueprint.md) |
| `fitness-motivation-grit` | `references/pinterest/10_fitness_motivation_grit/` | [style_manifest.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/10_fitness_motivation_grit/style_manifest.md) | [assembly_blueprint.md](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/10_fitness_motivation_grit/assembly_blueprint.md) |

Полный каталог референсов доступен в [`references/pinterest/CATALOG.md`](file:///c:/Users/timur/Videos/AI-Video-Editing/references/pinterest/CATALOG.md).
Правила связности стилей и защита от солянки: [`.claude/rulebooks/16-anti-mishmash-cohesion.md`](file:///c:/Users/timur/Videos/AI-Video-Editing/.claude/rulebooks/16-anti-mishmash-cohesion.md).
Обновление каталога после ручной чистки файлов: `python tools/sync_pinterest_references.py`.

