# 12. Anti-Slop Code & Human Editor Quality

## 1. What is AI Slop in Video Editing?
AI Slop is the mindless, mechanical application of automation templates (bouncing emojis on every word, neon strokes, metronome zooms every 2.5s, random stock footage, sterile vector plastic look) that induces banner blindness and causes instant viewer swipe.

## 2. Anti-Slop Post-Processing & Texture
1. **Procedural Noise Overlay (Anti-Vector Grain)**:
   - Поверх всех композиций и сцен в Remotion накладывается глобальный процедурный оверлей `<ProceduralNoiseOverlay opacity={0.04} />` на базе SVG-фильтра `<feTurbulence>`.
   - Прозрачность: строго **3–5%** (режим наложения `overlay`).
   - Назначение: убрать эффект «стерильного векторного рендера» и придать кадру текстуру живой оптики и кинопленки.
2. **Camera Parallax & Micro-Drift**:
   - Никаких застывших статичных "мертвых" планов.
   - Каждая сцена получает плавный микро-дрифт камеры (`scale` от 1.0 до 1.03 за всю длительность сцены) с легким микро-параллаксом по оси X.
3. **Remotion Spring Physics (No CSS Transitions)**:
   - Категорически **запрещены** CSS-классы с анимациями (`@keyframes`) и обычные `transition: all`.
   - Всё движение рассчитывается через физику Remotion: `spring({ fps, frame, config: { damping, mass, stiffness } })` и функцию `interpolate()` с овершутом и отскоком (`bounce-back` на 2–5%).

## 3. The 8 Editorial Rules

1. **No Bouncing Emoji Karaoke**:
   - Subtitles appear in semantic clauses (2–4 words) in the lower third (`y: 1120..1380`).
   - Highlight maximum 1 word per phrase, or leave clean white text. No bouncing 3D emojis.
2. **No Metronome Zooms**:
   - Zooms occur ONLY on thesis shifts or emotional punchwords. If speech is steady and reflective, keep the shot static with micro-drift.
3. **Proof-Driven B-Roll (No Generic Stock Footage)**:
   - Only real physical artifacts: screenshots of code/docs, screen recordings, product in hand.
   - If no real artifact exists: keep the speaker on camera with a subtle crop change.
4. **Natural Breathing (No Android Voice)**:
   - Keep natural intakes of breath and 0.2–0.4s pauses after conclusions. Cut only long pauses > 0.6s and filler sounds.
5. **Calibrated SFX (No Whoosh Abuse)**:
   - Использовать звуки только из локальной папки `assets/01_SFX/` через `<Audio/>` (`<SfxAudio />`) с расчетом фреймов и затуханием.
   - Volume strictly at `−20 dB` relative to voice RMS. Zooms have NO sound. Max 6 SFX per 30 seconds.
6. **Strict Typography Hierarchy**:
   - Шрифты только локальные из `assets/02_FONTS/` (`Montserrat`, `Inter`, `Unbounded`, `Manrope`). Шрифты `Arial`, `Roboto`, `TheBoldFont` категорически запрещены.
7. **Genre-Matched Music**:
   - Background music at `−22 dB` relative to voice RMS, ducked with sidechain during speech.
8. **Closed Narrative Loops**:
   - Every premise promised in the first 3 seconds must be resolved before the video ends.
