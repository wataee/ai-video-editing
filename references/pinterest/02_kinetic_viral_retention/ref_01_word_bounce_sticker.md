# Референс: Word Bounce + 3D Sticker Pop (Hormozi Kinetic)

- **Название приёма:** Выпрыгивающее слово с 3D-эмодзи и звуковым хлопком
- **Стиль:** `02_kinetic_viral_retention`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=hormozi%20caption%20animation%20reels`
- **Референс авторов:** Alex Hormozi, Ryan Pineda

---

## 1. Механика удержания внимания
- Каждое ударное слово увеличивается на 20% с отскоком (overshoot).
- Одновременно над словом вылетает 3D стикер (мешок денег, ракета, огонь).
- Длительность показа слова: строго 0.25 – 0.4 секунды.

---

## 2. Параметры анимации (Remotion)
- **Spring-физика отскока:**
  ```tsx
  const scale = spring({ frame: wordFrame, fps: 30, config: { damping: 9, mass: 0.5, stiffness: 240 } });
  ```
- **Текст:** `Montserrat-Black`, цвет `#FFE600`, обводка 4px `#000000`.

---

## 3. Звуковой дизайн
- В момент вылета: `assets/sfx/pops/pop_bubble_high.wav` (-16 dB).
- Без задержек, синхронизация с первым звуком гласной буквы.
