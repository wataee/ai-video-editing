# Сборочный чертеж монтажа: Бизнес & Экспертный Минимализм (01_business_minimal)
> **Стандарт для Claude:** Используй этот сценарий сборки при работе с B2B, SaaS, инвестиционными и экспертными видео.

---

## 1. Параметры дизайн-системы (Design Tokens Lock)
- **Preset ID:** `SYS-01_BUSINESS_MINIMAL`
- **Шрифты (assets/02_FONTS/):** Заголовки: `Montserrat-Bold`, Субтитры: `Inter-Medium` (или `Manrope-SemiBold`).
- **Цветовая триада:**
  - `Background`: `#0A0B0E` (глубокий графит/черный)
  - `Surface`: `rgba(255, 255, 255, 0.08)` (матовое стекло, `backdropFilter: blur(16px)`, скругление `20px`)
  - `Accent`: `#3B82F6` (кобальт) или `#E5A93C` (янтарное золото)
- **Единая физика Remotion:**
  ```tsx
  spring({ frame, fps: 30, config: { damping: 20, stiffness: 90, mass: 0.8 } })
  ```
- **Текстура:** `<ProceduralNoiseOverlay opacity={0.03} />` (чистый кадр, едва заметное кинопленочное зерно).

---

## 2. Посекундный рецепт таймлайна (60-секундная структура)

### Beat 01: The Hook Hero [0.0s – 3.0s] (Кадры 0–90)
- **Референсы:** `talking_head_flag_halo_callout.jpg`, `talking_head_hook_attention.jpg`
- **Действие:**
  - Кроп камеры спикера `1.12x` (punch-in).
  - Заглавный вопрос или тезис (макс 3 слова) по центру экрана (`y: 960`).
  - Опционально: 3D halo-элемент или акцентная плашка за головой спикера.
- **SFX:** `assets/sfx/hits/sub_bass_thud.wav` (-16 dB).

### Beat 02: Core Narrative & Subtitles [3.0s – 18.0s] (Кадры 90–540)
- **Референсы:** `davinci_talking_head_crop_subtitles.jpg`, `business_minimal_01.jpg`
- **Действие:**
  - Плавный микро-дрифт камеры `scale: 1.0 -> 1.03`.
  - Субтитры строго в нижней трети (`safe zone y: 1240`). 2–3 слова на экран.
  - Подсветка активного слова через `Color_Accent`. Никаких прыгающих эмодзи.
- **SFX:** Только фоновый лоу-фай / эмбиент грув (-24 dB relative to voice).

### Beat 03: Visual Evidence & Data Proof [18.0s – 38.0s] (Кадры 540–1140)
- **Референсы:** `biz_saas_explainer_3d_wireframe.jpg`, `production_timeline_breakdown_card.jpg`, `ref_01_split_metric_callout.jpg`
- **Действие:**
  - На тезисе с цифрами появляется компонент `<CalloutCard />` или `<DeviceMockup />` справа или снизу от спикера.
  - Анимированный счетчик метрики (`+142% MRR`, `$48,000`).
  - Тонкая рамка `1px solid rgba(255,255,255,0.12)`.
- **SFX:** `assets/sfx/clicks/mouse_click_soft.wav` (-20 dB) на вход карточки.

### Beat 04: Pacing Acceleration & Takeaways [38.0s – 52.0s] (Кадры 1140–1560)
- **Референсы:** `business_minimal_05.jpg`, `ref_02_document_highlight_proof.jpg`
- **Действие:**
  - 3 быстрых пункта вывода (чеклист) с интервалом в 1.2–1.5 сек.
  - Jump-cut спикера на новый угол или масштаб.
- **SFX:** Легкий свип `assets/sfx/whooshes/air_whoosh_clean.wav` (-22 dB).

### Beat 05: Loop Seam & CTA [52.0s – 60.0s] (Кадры 1560–1800)
- **Референсы:** `viral_talking_head_business.jpg`
- **Действие:**
  - Финальная фраза бесшовно перетекает в первую фразу Beat 01.
  - В правом верхнем углу (Safe Zone) появляется компактный бейдж призыва к действию (Link in bio / Подпишись).
- **SFX:** Затухание музыки (fade-out 0.8s) и мгновенный рестарт.

---

## 3. Анти-Солянка: Что СТРОГО ЗАПРЕЩЕНО в этом стиле
- ❌ Никакой рваной бумаги, скотча или газетных текстур (это стиль `07_mixed_media`).
- ❌ Никаких неоновых кибер-прицелов, глитчей и зеленых матричных линий (`05_cyber_tech`).
- ❌ Никаких кричащих желто-красных комиксных эмодзи Хормози (`02_kinetic_viral`).
- ❌ Никаких антикварных вензелей и золотых рукописных шрифтов (`04_luxury_dark`).
