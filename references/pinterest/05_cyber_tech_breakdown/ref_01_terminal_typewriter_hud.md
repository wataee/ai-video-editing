# Референс: Terminal Typewriter + Sci-Fi HUD (Fireship Tech)

- **Название приёма:** Окно терминала с бегущим кодом и футуристичными линиями сетки
- **Стиль:** `05_cyber_tech_breakdown`
- **Pinterest поиск:** `pinterest.com/search/pins/?q=cyberpunk%20hud%20ui%20motion%20graphics`
- **Референс авторов:** Fireship, PirateSoftware

---

## 1. Смысловой хук
- Быстрое разъяснение технической концепции (AI, алгоритм, скрипт).
- Текст печатается с высокой скоростью с мигающим курсором `_`.

---

## 2. Параметры анимации (Remotion)
- Подстрочный вывод кода: `code.slice(0, Math.floor(frame * 1.5))`.
- Мигающий курсор: `Math.floor(frame / 8) % 2 === 0 ? "█" : " "`.
- Цвет текста: Кибер-зеленый `#22C55E` на глубоком фоне `#0D1117`.

---

## 3. Звуковой дизайн
- Звук непрерывного стука клавиш `assets/sfx/clicks/click_01.wav` (-22 dB).
- В момент завершения выполнения: `assets/sfx/glitches/activate_energy_hit.wav` (-16 dB).
