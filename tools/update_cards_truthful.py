import glob
import re
import os

cards = sorted(glob.glob('references/library/cards/*.md'))

for card_path in cards:
    with open(card_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update status line
    content = re.sub(
        r'- \*\*Статус проверки:\*\*.*',
        '- **Статус проверки:** ссылка подтверждена (oEmbed), монтаж не просматривался',
        content
    )

    # 2. Update timing of hook if present
    content = re.sub(
        r'- \*\*Тайминг хука:\*\*.*',
        '- **Тайминг хука:** НЕ ИЗМЕРЕНО',
        content
    )

    # 3. Update ASL
    content = re.sub(
        r'- \*\*Средняя длина плана \(ASL\):\*\*.*',
        '- **Средняя длина плана (ASL):** НЕ ИЗМЕРЕНО',
        content
    )

    # 4. Update cuts per 30s
    content = re.sub(
        r'- \*\*Число смен кадра за 30 секунд:\*\*.*',
        '- **Число смен кадра за 30 секунд:** НЕ ИЗМЕРЕНО',
        content
    )

    # 5. Update air/pause
    content = re.sub(
        r'- \*\*Где оставлен «воздух»:\*\*.*',
        '- **Где оставлен «воздух»:** НЕ ИЗМЕРЕНО',
        content
    )

    # 6. Update text motion & camera
    content = re.sub(
        r'- \*\*Движение текста:\*\*.*',
        '- **Движение текста:** НЕ ИЗМЕРЕНО',
        content
    )
    content = re.sub(
        r'- \*\*Камера:\*\*.*',
        '- **Камера:** НЕ ИЗМЕРЕНО',
        content
    )

    # 7. Update subtitles position, font, display logic
    content = re.sub(
        r'- \*\*Положение в кадре:\*\*.*',
        '- **Положение в кадре:** НЕ ИЗМЕРЕНО',
        content
    )
    content = re.sub(
        r'- \*\*Шрифт и стиль:\*\*.*',
        '- **Шрифт и стиль:** НЕ ИЗМЕРЕНО (шрифт визуально не идентифицировался)',
        content
    )
    content = re.sub(
        r'- \*\*Логика показа:\*\*.*',
        '- **Логика показа:** НЕ ИЗМЕРЕНО',
        content
    )

    # 8. Update sound design (music & SFX)
    content = re.sub(
        r'- \*\*Фоновая музыка:\*\*.*',
        '- **Фоновая музыка:** НЕ ИЗМЕРЕНО (уровень в dB не измерялся)',
        content
    )
    content = re.sub(
        r'- \*\*SFX в миксе:\*\*.*',
        '- **SFX в миксе:** НЕ ИЗМЕРЕНО (число и уровни SFX не измерялись)',
        content
    )

    with open(card_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(cards)} cards successfully.")
