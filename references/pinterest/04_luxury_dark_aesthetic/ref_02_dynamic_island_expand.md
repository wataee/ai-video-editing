# Референс: Dynamic Island Capsule Morph (iOS Micro-Interaction)

- **Название приёма:** Черная плавающая капсула, плавно трансформирующаяся в статусную карточку
- **Стиль:** `04_luxury_dark_aesthetic`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=dynamic%20island%20ui%20animation%20motion`
- **Референс авторов:** iOS Dynamic Island, Modern Fintech Apps

---

## 1. Смысловой хук
- В верхней трети экрана висит компактная черная капсула (статус, таймер или логотип).
- В момент ключевого слова капсула пружинисто расширяется в полноценную информационную панель.

---

## 2. Параметры анимации (Remotion)
- Размеры: `width: interpolate(progress, [0, 1], [180, 840])`, `height: interpolate(progress, [0, 1], [50, 140])`.
- Скругление углов: `borderRadius: 40px`.
- Физика: `spring({ damping: 16, stiffness: 180 })`.

---

## 3. Звуковой дизайн
- Щелчок тактильного переключателя `assets/sfx/clicks/switch_01.wav` (-22 dB).
