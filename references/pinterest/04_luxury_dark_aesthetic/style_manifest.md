# Стиль: Luxury Dark & Glassmorphism (Apple Keynote, Liquid Glass)

> **Ключевые авторы:** Apple Keynote presentations, Dieter Rams minimalist aesthetics, luxury brand teasers.  
> **Целевая аудитория:** Премиум брендинг, fintech, luxury real estate, AI-стартапы, дизайн-студии.

---

## 1. Визуальный ДНК
- **Стекло (Glassmorphism):** Полупрозрачные матовые плашки `backdrop-filter: blur(24px)`, тонкая граница 1px `rgba(255, 255, 255, 0.12)`.
- **Свечение:** Мягкий рассеянный градиент на фоне (радиальное свечение индиго/фиолетового `#6366F1` или изумрудного).
- **Цветовая палитра:**
  - Базовый: Глубочайший черный `#050508` с темным виньетированием
  - Текст: Молочно-белый `#F8FAFC`, серебристый градиент `#94A3B8` -> `#FFFFFF`
  - Акценты: Перламутровый cyan `#38BDF8`, неоновый фиолетовый `#A855F7`

---

## 2. Анимация и физика (Remotion Spring)
- **Камера:** Невесомое парение, ультра-гладкий ease:
  ```tsx
  spring({ frame, fps: 30, config: { damping: 24, mass: 1.2, stiffness: 80 } })
  ```
- **Свет:** Бегущий блик по кромке стеклянной карточки (linear gradient mask сдвиг).
- **Склейки (ASL):** 2.5 – 4.0 секунды. Ощущение премиальности и контроля.

---

## 3. Типографика и Титры
- **Шрифты:** `Unbounded-Light` / `Unbounded-Regular` (заголовки) + `Inter-Light` (подзаголовки).
- **Кернинг:** Широкий трекинг (`letterSpacing: '0.05em'`), утонченные линии.

---

## 4. Звуковой дизайн (assets/01_SFX)
- **Удар хука:** Кинематографический саб-бум `assets/sfx/hits/cinematic_boom_01.wav` (-14 dB).
- **Фокус/Клик:** `assets/sfx/clicks/mechanical_button.wav` (-22 dB).
- **Эмбиент:** Низкий высокотехнологичный гул `assets/sfx/ambience/tech_drone_subtle.wav` (-26 dB).

---

## 5. Доказательства (Proof Assets)
- Карточки Remotion: `<LiquidGlassCard />` со сложными градиентами, 3D мокапы iPhone/MacBook, плавающие виджеты.
