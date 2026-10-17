# ⚠️ [АРХИВ / DEPRECATED] Интеграция After Effects MCP (HeroicSwan)

> **СТАТУС: АРХИВ / ЗАПРЕЩЕНО К ИСПОЛЬЗОВАНИЮ В ПРОДАКШЕНЕ.**  
> Согласно Правилу #1 проекта (CLAUDE.md и rulebook 13), взаимодействие с After Effects происходит ИСКЛЮЧИТЕЛЬНО путем генерации монолитного ExtendScript (`scripts/build_ae_project.jsx`) с ручным запуском пользователем. Использование любых MCP-серверов AE запрещено.  
> Данный документ сохранен исключительно как архив локальных исследований.


## 🛡️ Внесённые патчи безопасности и производительности

### 1. Полная изоляция файлового обмена (IPC)
* **Было:** Сервер создавал папки и файлы обмена в корневом каталоге пользователя `C:\Users\timur\.ae-mcp\`.
* **Стало:** Все очереди команд, результаты, логи и временные превью-рендеры перенаправлены строго внутрь проекта:
  `C:\Users\timur\Videos\AI-Video-Editing\work\.ae-mcp\`
* **Файлы:**
  * `tools\after-effects-mcp\src\util\paths.ts` — значение по умолчанию для `getDataRoot()` переопределено на `work\.ae-mcp`.
  * `tools\after-effects-mcp\host-scripts\ae-mcp-engine.jsx` — функция `getDataDir()` читает `AE_MCP_DATA_DIR` с жестким фоллбэком на `C:/Users/timur/Videos/AI-Video-Editing/work/.ae-mcp`.
  * `tools\after-effects-mcp\host-scripts\ae-mcp-methods.jsx` — директория рендера превью `previews/` перенаправлена в `work\.ae-mcp\previews`.
  * `tools\after-effects-mcp\host-scripts\ae-mcp-status.jsx` — статусная панель отслеживает файлы в `work\.ae-mcp`.

### 2. Умный барьер безопасности (Security Guard) для `ae_run_jsx`
* **Было:** Инструмент `ae_run_jsx` принимал произвольный код без проверки, позволяя вызывать системные команды Windows через `system.callSystem(...)` и удалять файлы через `.remove()`.
* **Стало:** В `tools\after-effects-mcp\src\mcp\tools\index.ts` перед выполнением JSX добавлен строгий guard-фильтр:
  * **Блокировка опасных вызовов:** немедленный отказ при наличии `callSystem`, `system.`, `.remove`, `.execute`, `Folder.startup`, `File.encode`.
  * **Блокировка путей вне проекта:** проверка всех путей файловой системы по регулярному выражению — запрещены любые пути за пределами `C:/Users/timur/Videos/AI-Video-Editing`.

### 3. Увеличение скорости отклика (Polling)
* **Было:** Интервал проверки очереди в After Effects составлял 1500 мс (1.5 с).
* **Стало:** В `host-scripts\ae-mcp-engine.jsx` константа `POLL_MS` уменьшена до **400 мс**. Задержка между действиями агента сокращена почти в 4 раза.

### 4. Поддержка After Effects 2026
* **Было:** Скрипты начальной загрузки проверяли только версии до `25.5` (AE 2025).
* **Стало:** В `ae-mcp-bootstrap.jsx` и `ae-mcp-engine.jsx` добавлен список версий `["26.3", "26.0", ...]`.

---

## 📂 Расположение файлов в системе

### 1. Директории скриптов After Effects:
* `%APPDATA%\Adobe\After Effects\26.0\Scripts\Startup\ae-mcp-bootstrap.jsx` — инертный стартер AE.
* `%APPDATA%\Adobe\After Effects\26.0\Scripts\ae-mcp\ae-mcp-engine.jsx` — движок поллинга (400 мс).
* `%APPDATA%\Adobe\After Effects\26.0\Scripts\ae-mcp\ae-mcp-methods.jsx` — библиотека из 27 методов.
* `%APPDATA%\Adobe\After Effects\26.0\Scripts\ScriptUI Panels\ae-mcp-status.jsx` — панель статуса в интерфейсе AE.
*(Продублировано в `26.3` для совместимости со всеми патчами версии 2026).*

### 2. Локальный конфиг MCP:
В корне проекта создан файл [`.mcp.json`](file:///C:/Users/timur/Videos/AI-Video-Editing/.mcp.json):
```json
{
  "mcpServers": {
    "after-effects": {
      "command": "C:/Program Files/nodejs/node.exe",
      "args": [
        "C:/Users/timur/Videos/AI-Video-Editing/tools/after-effects-mcp/dist/index.js",
        "serve"
      ],
      "env": {
        "AE_MCP_DATA_DIR": "C:/Users/timur/Videos/AI-Video-Editing/work/.ae-mcp"
      }
    }
  }
}
```

### 3. Быстрая диагностика:
Создан батник [`tools\after-effects-mcp.bat`](file:///C:/Users/timur/Videos/AI-Video-Editing/tools/after-effects-mcp.bat):
* `tools\after-effects-mcp.bat health` — статус подключения и процесса AE.
* `tools\after-effects-mcp.bat ensure` — ручной перезапуск моста в запущенном AE.

---

## 🧪 Инструкция: Как протестировать связку при открытом After Effects 2026

1. **Разрешите скриптам доступ к сети и файлам (один раз в AE):**
   * В After Effects откройте: `Правка (Edit)` $\to$ `Настройки (Preferences)` $\to$ `Сценарии и выражения (Scripting & Expressions)`.
   * Убедитесь, что установлена галочка: **«Разрешить сценариям выполнять запись файлов и осуществлять доступ к сети»** (*Allow Scripts to Write Files and Access Network*).
   * Нажмите **ОК**.

2. **Запустите After Effects 2026:**
   * Откройте After Effects и создайте новый проект или откройте любой существующий.

3. **Включите мост в интерфейсе AE:**
   * В верхнем меню After Effects выберите: `Окно (Window)` $\to$ `ae-mcp-status.jsx`.
   * В открывшейся небольшой панели нажмите кнопку **Connect bridge** (или **Start poller**).
   * Статус изменится на **ONLINE (Listening)**.

4. **Проверьте подключение из терминала:**
   * В терминале проекта выполните:
     ```cmd
     tools\after-effects-mcp.bat health
     ```
   * Вы увидите:
     ```text
     AE running: true
     Ensure: { "ok": true, ... }
     Live instances: 1
     ```

5. **Тест от AI-ассистента:**
   * Теперь в диалоге с Claude Code / Cursor / Codex можно давать прямые команды:
     * *«Создай композицию 1080x1920 30fps на 10 секунд с именем Test_Shorts»*
     * *«Добавь текстовый слой с надписью 'AI Video Editing' и сделай анимацию масштаба»*
