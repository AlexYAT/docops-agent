# idea_to_mvp — DOA-IDEA-003

## Metadata

- Project: DOA
- Doc type: idea_to_mvp
- ID: DOA-IDEA-003
- Status: draft
- Date: 2026-04-10
- Parent: DOA-IMP-015

---

## Summary

**Minimal UI for DocOps Document Gate** — тонкий клиентский слой поверх уже реализованного **`scripts/doa_document_gate.py`**: запуск gate из интерфейса, отображение **`gate_status`**, **counts**, списка **findings** и пути к сгенерированному **JSON**; первая версия UI работает только в режиме **dry-run** и **не** дублирует логику validator/gate.

## Problem

- CLI и сырые JSON-отчёты достаточны для автоматизации, но **медленнее** для человека при быстром цикле «прогон → просмотр результата».
- Риск соблазна встроить проверки в UI — **дублирование** engine и расхождение с **DOA-DEC-031** / **DOA-DEC-032**.
- Нужен **минимальный** визуальный слой без новых источников правды и без операций, которые меняют смысл документов или историю Git.

## Proposed solution

Ввести **минимальный UI** (например локальное веб-приложение или десктоп-оболочка — выбор в **architecture_draft**), который:

1. Вызывает **существующий** gate так же, как CLI (подпроцесс или согласованный API-вызов **без копирования** правил проверки).
2. Читает результат из **сгенерированного JSON** (`doa-gate-report/1`) или из stdout/stderr, не пересчитывая findings самостоятельно.
3. Показывает **gate_status**, **counts**, таблицу/список **findings**, **путь к отчёту** на диске.
4. В **MVP UI** запуск только с **dry-run** (как дефолт gate); **autofix**, **git** и семантические действия **отсутствуют**.

## MVP scope

### In

- **Run gate from UI** — одна явная команда «прогнать» с параметрами root/out по умолчанию или из простого поля ввода.
- **Show gate_status** — **ACCEPT** / **ACCEPT_WITH_WARNINGS** / **REJECT**.
- **Show counts** — **total**, **error**, **warn**, **info** из отчёта.
- **Show findings list** — из JSON (type, severity, file, details; опционально engine_mode).
- **Show path to generated JSON report** — абсолютный или относительный путь к файлу, записанному gate.
- **Dry-run only** в первой версии UI (не предлагать и не включать autofix).

### Out

- Дублирование **validator** или **policy** в UI.
- **Semantic edits** документов из UI.
- **Autofix** в UI MVP.
- **Git operations** (commit, push, stage) из UI MVP.

## Constraints

- **No validator duplication** — все проверки остаются в **`doa_link_id_validator.py`**; агрегация статуса — в **`doa_document_gate.py`**.
- **No semantic edits** — UI не является редактором смысла markdown.
- **No autofix in UI MVP** — только отображение и запуск в dry-run-потоке.
- **No git operations in UI MVP** — без кнопок commit/push; пользователь управляет Git вне UI.

## Success criteria

- Один прогон из UI даёт **тот же** JSON на диске, что и эквивалентная команда CLI (при тех же аргументах).
- Пользователь видит **gate_status**, **counts** и **findings** без ручного открытия JSON.
- Путь к отчёту **явно** показан в UI (копирование в буфер — опционально в следующих итерациях).

## Risks

- Зоопарк платформ (Electron vs браузер vs Tauri) — откладывается в архитектуру; риск переусложнить MVP.
- Небезопасный запуск произвольных команд, если UI не ограничит аргументы — нужны guardrails в **architecture_draft** / **operational_plan**.

## Relation to current gate track

- **UI is a thin shell over existing `doa_document_gate.py`** — не заменяет и не форкает логику T01–T04.
- **Source of truth** остаётся **репозиторий** и **JSON-отчёты** на диске; UI только отображает и инициирует прогон.
- **UI does not replace CLI** — автоматизация, CI и скрипты продолжают использовать CLI; UI — опциональное удобство для человека.
- Связь с цепочкой: **DOA-IDEA-002** / **DOA-ARCH-013** / **DOA-DEC-032** / **DOA-OP-020** / **DOA-IMP-015** — UI следующий шаг поверх зафиксированного MVP Gate.

## Next documents

- **architecture_draft** — выбор стека (локальный web, Tauri, и т.д.), модель процесса, границы безопасности вызова subprocess.
- **decision_log** (при необходимости) — если появятся обязательные пути установки или политика распространения UI.
- **operational_plan** — реализация MVP UI, тестовый прогон, **implementation_snapshot**.
