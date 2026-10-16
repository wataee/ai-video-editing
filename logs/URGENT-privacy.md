# 🚨 СРОЧНО: Аудит приватности, персональных данных и авторских прав

> **Дата составления:** 16 октября 2026 г.  
> **Статус:** ТРЕБУЕТ ДЕЙСТВИЙ ЧЕЛОВЕКА  
> **Репозиторий:** `github.com/wataee/ai-video-editing` (публичный)

---

## 1. Персональные данные клиента в истории Git

### Что произошло
В публичном репозитории отслеживались файлы клиента:
- Превью кадров с лицом спикера из After Effects:
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093518995.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093606033.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093707553.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093769044.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093891193.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792093912127.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792094331994.png`
  - `work/.ae-mcp/previews/Aziz_-_Viral_Reel_Master_1792094387467.png`
- Метаданные и брифы клиента:
  - `clients/aziz/brief.json`
  - `clients/aziz/credits.md` (указан аккаунт `@its_aziz146`)
  - `clients/aziz/glossary.txt`
  - `clients/aziz/project_state.md` (детали монтажа и исходников)
  - `clients/aziz/revisions.md`
- Служебные логи After Effects:
  - `work/.ae-mcp/last-kick.json`

### Что уже сделано агентом
1. Создан полный бэкап кодовой базы: `_archive\2026-10-16\backup.zip`.
2. Файлы исключены из текущего индекса Git (`git rm --cached -r`).
3. В `.gitignore` добавлены правила игнорирования `work/`, `_archive/`, `_sandbox/`, `references/library/_private/`, `clients/*/` (кроме `clients/_template/`), `*.psd`, `*.aep`, `*.prproj`, `.mcp.json`.
4. Сделан локальный коммит `chore: stop tracking client data` (без push в origin).

### ⚠️ ВАЖНО: Удаление из индекса НЕ очищает историю Git!
Поскольку репозиторий публичный, любой пользователь интернета может открыть предыдущие коммиты на GitHub и скачать PNG с лицом человека и его личные данные.

### Пошаговые действия для владельца репозитория:
1. **Сделать репозиторий приватным прямо сейчас:**
   - Откройте `https://github.com/wataee/ai-video-editing/settings`.
   - Внизу страницы в разделе **Danger Zone** нажмите **Change repository visibility** → **Make private**.
2. **Проверить юридическое согласие спикера:**
   - Убедитесь, что клиент (`@its_aziz146`) дал письменное согласие на публикацию исходных материалов, превью и сценариев в открытом доступе.
3. **Очистить историю Git от конфиденциальных файлов:**
   - Вариант А (рекомендуемый): использовать утилиту `git-filter-repo`:
     ```bash
     pip install git-filter-repo
     git filter-repo --path work/.ae-mcp/previews --invert-paths
     git filter-repo --path clients/aziz --invert-paths
     git push origin --force --all
     ```
   - Вариант Б: пересоздать репозиторий без истории коммитов (fresh repo), если старая история не критична.

---

## 2. Материалы из сторонних/закрытых источников (ТРЕБУЕТ РЕШЕНИЯ ЧЕЛОВЕКА)

В ходе проверки обнаружены скрипты парсинга Google Drive (`tools/parse_drive.py`, `tools/parse_drive_ids.py`) и файлы в папке `references/`:
1. `references/joseph_drive/UE-Sound-Design-Claude-Training-COMPLETE.md`
2. `references/joseph_drive/Prompts_List.docx`
3. `references/joseph_drive/Prompts_List.txt`
4. `references/UE-Sound-Design-Claude-Training-COMPLETE.md`

### Анализ содержимого
- Скрипты `parse_drive*.py` искали файлы на диске Google Drive по ключевым словам ("Joseph", "Sound", "Prompt", "3 things from beginner to pro.mp4", "3 things - Edit v1 + SFX.mp4").
- Файл `UE-Sound-Design-Claude-Training-COMPLETE.md` содержит обучающие материалы по саунд-дизайну и промпты.
- Эти материалы могут являться частью платного обучающего курса или закрытой папки эксперта (Joseph).

### Что требуется от человека:
1. Проверить происхождение папки `references/joseph_drive/` и файла `references/UE-Sound-Design-Claude-Training-COMPLETE.md`.
2. Если материалы защищены авторским правом автора курса/автора папки:
   - Перенести их в `references/library/_private/` (которая уже добавлена в `.gitignore`) либо удалить из репозитория.
   - Очистить историю git через `git-filter-repo --path references/joseph_drive --invert-paths`.
