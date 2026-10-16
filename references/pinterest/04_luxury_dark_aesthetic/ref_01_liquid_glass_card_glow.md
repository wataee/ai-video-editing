# Референс: Liquid Glass Card + Edge Light Sweep (Apple Keynote)

- **Название приёма:** Премиальная стеклянная карточка с матовым размытием и бегущим световым бликом
- **Стиль:** `04_luxury_dark_aesthetic`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=glassmorphism%20ui%20motion%20design%20apple`
- **Референс авторов:** Apple Keynote, Nothing Phone

---

## 1. Смысловой хук
- Демонстрация ключевого оффера или премиального тезиса с ощущением физической осязаемости.
- Фон глубокий черный `#07080B`, под карточкой нежное радиальное свечение фиолетового цвета.

---

## 2. Параметры анимации (Remotion)
- **Компонент:** `<LiquidGlassCard width={860} badge="EXECUTIVE" title="Система масштабирования" />`.
- **Световой блик:** `linear-gradient` под углом 45 градусов, смещение `translateX` от -100% до +200% за 40 кадров.
- **Spring:** Высокая вязкость `damping: 22, mass: 1.1, stiffness: 90`.

---

## 3. Звуковой дизайн
- В момент раскрытия карточки: глубокий кристаллический звук или `assets/sfx/pops/glass_pop.wav` (-20 dB).
- Фоновый суб-бас `assets/sfx/hits/cinematic_boom_01.wav` (-16 dB).
