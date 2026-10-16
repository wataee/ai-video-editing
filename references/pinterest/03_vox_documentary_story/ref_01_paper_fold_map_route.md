# Референс: Paper Fold & 3D Map Route (Vox Borders)

- **Название приёма:** Анимированная 3D-карта на текстуре мятой бумаги с траекторией маршрута
- **Стиль:** `03_vox_documentary_story`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=vox%20map%20motion%20graphics%20johnny%20harris`
- **Референс авторов:** Johnny Harris, Vox Earworm

---

## 1. Смысловой хук
- Визуализация географии или масштаба событий через изометрическую карту.
- Камера движется вдоль пунктирной линии, оставляя за собой подсвеченный след.

---

## 2. Параметры анимации (Remotion)
- Фоновый оверлей: `<ProceduralNoiseOverlay />` (SVG filter feTurbulence).
- Линия маршрута: SVG path с `strokeDashoffset: interpolate(frame, [0, 60], [pathLength, 0])`.
- Угол наклона: `perspective(800px) rotateX(25deg)`.

---

## 3. Звуковой дизайн
- Начало движения: шелест раскрывающейся бумаги.
- Движение маркера: мягкое скольжение `assets/sfx/whooshes/whoosh_subtle_air.wav` (-22 dB).
