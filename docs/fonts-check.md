# Проверка шрифтов и покрытия кириллицы (Cyrillic Coverage Audit)
**Дата аудита:** 2026-10-15  
**Обязательный диапазон:** U+0410–U+044F (А–Я, а–я, 64 символа) + U+0401 (Ё) + U+0451 (ё) = 66 символов.  

## Сводная таблица шрифтов

| Семейство | Файл шрифта | Символов в шрифте | Кириллица (из 66) | Статус кириллицы | Лицензия |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `Inter` | `Inter-Italic[opsz,wght].ttf` | 2813 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Inter` | `Inter[opsz,wght].ttf` | 2849 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Manrope` | `Manrope[wght].ttf` | 678 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Montserrat` | `Montserrat-Italic[wght].ttf` | 1312 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Montserrat` | `Montserrat[wght].ttf` | 1312 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Onest` | `Onest[wght].ttf` | 780 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Oswald` | `Oswald[wght].ttf` | 850 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Rubik` | `Rubik-Italic[wght].ttf` | 885 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Rubik` | `Rubik[wght].ttf` | 885 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `Unbounded` | `Unbounded[wght].ttf` | 1138 | 66/66 | **ПОЛНОСТЬЮ** | OFL 1.1 (OFL.txt) |
| `TheBoldFont (TikTok Starter)` | `theboldfont.ttf` | 109 | 0/66 | **НЕТ (0/66)** | theboldfont-license.rtf (Free for personal use only?) |

## Ограничения и замечания по шрифтам

1. **The Bold Font (из шаблона remotion-tiktok-starter):**
   - **Кириллица:** Полностью отсутствует (0 из 66 базовых букв кириллицы).
   - **Лицензия:** В комплекте идет `theboldfont-license.rtf` (автор: Thibault Labrecque). Лицензия не является стандартной открытой OFL/Apache и имеет коммерческие ограничения. Помечена в реестре как: **лицензия не подтверждена для коммерческого видеомонтажа**.
   - **Рекомендация:** Для роликов на русском языке использовать семейство **Montserrat** или **Rubik** из `assets/fonts`.

2. **Шрифты из Google Fonts (assets/fonts):**
   - Все 7 семейств (Montserrat, Manrope, Onest, Rubik, Oswald, Inter, Unbounded) имеют 100% покрытие кириллицы.
   - Каждое семейство сопровождается юридическим файлом `OFL.txt` (SIL Open Font License 1.1), разрешающим бесплатное коммерческое использование в любых видеороликах.