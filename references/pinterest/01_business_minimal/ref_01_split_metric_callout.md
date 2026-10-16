# Референс: Split Screen + Metric Callout (Бизнес-минимализм)

- **Название приёма:** Разделенный экран: спикер сверху / всплывающая метрика снизу
- **Стиль:** `01_business_minimal`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=clean%20minimalist%20infographics%20reels`
- **Референс авторов:** Ali Abdaal, Garry Tan, Colin & Samir

---

## 1. Структура хука (0-3s)
- **Кадр 0-1с:** Спикер смотрит в камеру, произносит парадоксальный тезис («90% людей теряют эти деньги»).
- **Кадр 1.5с:** Экран делится по горизонтали или снизу выезжает матовая графитовая карточка с цифрой `-42%`.
- **SFX:** Глухой саб-бас `assets/sfx/hits/sub_bass_thud.wav` (-14 dB).

---

## 2. Параметры анимации (Remotion)
- **Физика выезда карточки:**
  ```tsx
  spring({ frame: frame - 45, fps: 30, config: { damping: 18, mass: 0.9, stiffness: 140 } })
  ```
- **Счетчик цифр:** Инкремент от 0 до -42 за 24 кадра через `interpolate(frame, [45, 69], [0, -42], { extrapolateRight: "clamp" })`.
- **Безопасная зона:** Карточка строго в `x: 100..950`, `y: 950..1350`.

---

## 3. Звуковая партитура
- Кадр 45 (1.5с): `assets/sfx/clicks/mechanical_button.wav` (-20 dB).
- Фон: Минималистичный бас-дрон `assets/sfx/ambience/tech_drone_subtle.wav` (-26 dB).
