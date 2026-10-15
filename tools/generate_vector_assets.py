#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_vector_assets.py — Создание профессиональных оверлеев и UI-ассетов для AI-монтажа.
Генерирует SVG сетки (стиль Iman Gadzhi), разметку безопасных зон и векторные плашки.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def generate_grid_svg():
    width, height = 1080, 1920
    cell = 70
    lines = []
    
    # Вертикальные линии
    for x in range(0, width + 1, cell):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#ffffff" stroke-width="1" stroke-opacity="0.10" />')
    
    # Горизонтальные линии
    for y in range(0, height + 1, cell):
        lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#ffffff" stroke-width="1" stroke-opacity="0.10" />')
        
    # Координатные перекрестья по центру
    crosses = []
    for x in range(cell, width, cell * 3):
        for y in range(cell, height, cell * 3):
            crosses.append(f'<path d="M {x-4} {y} L {x+4} {y} M {x} {y-4} L {x} {y+4}" stroke="#38BDF8" stroke-width="1.5" stroke-opacity="0.30" />')

    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
    <rect width="{width}" height="{height}" fill="#0B0B0B" />
    <g id="grid_lines">
        {''.join(lines)}
    </g>
    <g id="crosshairs">
        {''.join(crosses)}
    </g>
</svg>'''
    out = ROOT / "assets" / "overlays" / "grids" / "tech_grid_1080x1920.svg"
    out.write_text(content, encoding="utf-8")
    print(f"Generated: {out}")


def generate_safe_zones_svg():
    width, height = 1080, 1920
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
    <!-- Верхняя зона интерфейса (Поиск, статус-бар: 220px) -->
    <rect x="0" y="0" width="{width}" height="220" fill="#EF4444" fill-opacity="0.22" />
    <text x="540" y="120" fill="#EF4444" font-family="Arial, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">ВЕРХНЯЯ ЗОНА ИНТЕРФЕЙСА (НЕ ЗАНИМАТЬ)</text>

    <!-- Нижняя зона (Описание, звук, CTA: 380px) -->
    <rect x="0" y="{height - 380}" width="{width}" height="380" fill="#EF4444" fill-opacity="0.22" />
    <text x="540" y="{height - 180}" fill="#EF4444" font-family="Arial, sans-serif" font-size="28" font-weight="bold" text-anchor="middle">НИЖНЯЯ ЗОНА ОПИСАНИЯ И ЗВУКА (380px)</text>

    <!-- Правая зона (Лайки, комменты, репосты: 130px) -->
    <rect x="{width - 130}" y="220" width="130" height="{height - 600}" fill="#F59E0B" fill-opacity="0.25" />
    <text x="{width - 65}" y="700" fill="#F59E0B" font-family="Arial, sans-serif" font-size="20" font-weight="bold" text-anchor="middle" transform="rotate(90, {width - 65}, 700)">КНОПКИ ТИКТОК / REELS</text>

    <!-- Рекомендуемая центральная зона внимания для субтитров и спикера -->
    <rect x="130" y="920" width="{width - 260}" height="420" stroke="#10B981" stroke-width="2" stroke-dasharray="8 8" fill="none" />
    <text x="540" y="1140" fill="#10B981" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">ЗОНА СУБТИТРОВ И АКЦЕНТОВ (Y: 920..1340)</text>
</svg>'''
    out = ROOT / "assets" / "overlays" / "safe_zones" / "safe_zones_9x16.svg"
    out.write_text(content, encoding="utf-8")
    print(f"Generated: {out}")


def generate_ui_badges():
    badges_dir = ROOT / "assets" / "ui" / "badges"
    
    # 1. Badge "ФАКТ" (Gold / Tech)
    fact_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="48" viewBox="0 0 180 48" fill="none">
    <rect x="1" y="1" width="178" height="46" rx="23" fill="#141416" fill-opacity="0.9" stroke="#D4AF37" stroke-width="2" />
    <circle cx="24" cy="24" r="6" fill="#D4AF37" />
    <text x="96" y="31" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="16" font-weight="700" text-anchor="middle" letter-spacing="1">ФАКТ</text>
</svg>'''
    (badges_dir / "badge_fact.svg").write_text(fact_svg, encoding="utf-8")

    # 2. Badge "ОШИБКА" (Red / Warning)
    mistake_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="190" height="48" viewBox="0 0 190 48" fill="none">
    <rect x="1" y="1" width="188" height="46" rx="12" fill="#1F1315" fill-opacity="0.95" stroke="#EF4444" stroke-width="2" />
    <path d="M 20 18 L 28 26 M 28 18 L 20 26" stroke="#EF4444" stroke-width="2.5" stroke-linecap="round" />
    <text x="104" y="31" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="16" font-weight="700" text-anchor="middle" letter-spacing="1">ОШИБКА</text>
</svg>'''
    (badges_dir / "badge_mistake.svg").write_text(mistake_svg, encoding="utf-8")

    # 3. Badge "РЕЗУЛЬТАТ" (Emerald / Growth)
    result_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="210" height="48" viewBox="0 0 210 48" fill="none">
    <rect x="1" y="1" width="208" height="46" rx="12" fill="#0D1E17" fill-opacity="0.95" stroke="#10B981" stroke-width="2" />
    <path d="M 18 24 L 24 30 L 32 18" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
    <text x="114" y="31" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="16" font-weight="700" text-anchor="middle" letter-spacing="1">РЕЗУЛЬТАТ</text>
</svg>'''
    (badges_dir / "badge_result.svg").write_text(result_svg, encoding="utf-8")

    # 4. Verified Checkmark
    check_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
    <circle cx="18" cy="18" r="16" fill="#38BDF8" />
    <path d="M 11 18 L 16 23 L 25 14" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
</svg>'''
    (badges_dir / "verified_badge.svg").write_text(check_svg, encoding="utf-8")

    # 5. Clean minimalist Callout Arrow
    arrows_dir = ROOT / "assets" / "ui" / "arrows"
    arrow_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" fill="none">
    <path d="M 12 12 Q 32 12 44 28 T 48 50" stroke="#FFFFFF" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-dasharray="4 4" />
    <polygon points="42,46 48,56 54,46" fill="#FFFFFF" />
</svg>'''
    (arrows_dir / "callout_arrow.svg").write_text(arrow_svg, encoding="utf-8")

    print(f"Generated UI badges and arrows in: {badges_dir}")


if __name__ == "__main__":
    generate_grid_svg()
    generate_safe_zones_svg()
    generate_ui_badges()
