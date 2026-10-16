# 08. Typography Scale & Pairing Matrix (9:16)

## 1. Hard Rule: Local Fonts Only (No Arial / Roboto)
- **Local Source**: Все шрифты обязаны загружаться исключительно локально из `assets/fonts/` через нативные правила `@font-face` в `src/styles/fonts.css` или `@remotion/google-fonts`.
- **Approved Font Stack**:
  - **Headlines / Key Hook**: `Montserrat` (ExtraBold/Black) или `Unbounded` (Black).
  - **Body / Subtitles / Captions**: `Manrope` (SemiBold/Bold) или `Inter` (SemiBold/Bold).
  - **Numeric Badges & Secondary**: `Oswald` (Bold) или `Rubik` (Bold).
  - **Signature Accent (2nd Layer Only)**: `Caveat` (Bold, наклон -8°..-10°).
- **STRICT PROHIBITION**:
  - Любые системные дефолтные шрифты (`Arial`, `Roboto`, `Times New Roman`, `Comic Sans`, дефолтный `system-ui`) **категорически запрещены**.
  - Шрифт `TheBoldFont` **запрещен** (отсутствие качественной кириллицы и шаблонный вид).
  - Нарушение шрифтовой дисциплины приводит к ошибке сборки через валидатор `assertValidFont()`.

## 2. 1080x1920 Type Scale
Vertical video demands large, instantly legible type. Never set body text under 32px.

| Role | Font Size | Line Height | Tracking | Approved Font |
|---|---|---|---|---|
| **Mega Hook** | `96px - 120px` | `1.05` | `-0.03em` | Montserrat Black / Unbounded Black |
| **Headline / Stat** | `72px - 88px` | `1.15` | `-0.02em` | Montserrat ExtraBold |
| **Section Header** | `48px - 60px` | `1.20` | `-0.01em` | Montserrat Bold / Inter Bold |
| **Captions (Karaoke)** | `44px - 56px` | `1.25` | `0` | Manrope SemiBold / Inter Bold |
| **Subtext / Detail** | `32px - 38px` | `1.35` | `+0.01em` | Manrope Regular / Inter Medium |

## 3. Pairing Rules
1. **Rule of Two**: Maximum 2 fonts in a single scene (e.g. Montserrat headline + Manrope subtitles).
2. **Caveat Accent Layer**: Caveat may ONLY be used as an overlapping second layer for 1–2 emphasis words (tilt -8° to -10°), never for entire sentences or captions.
3. **Legibility First**: Maximum 3 to 5 words per line on mobile vertical screens.
