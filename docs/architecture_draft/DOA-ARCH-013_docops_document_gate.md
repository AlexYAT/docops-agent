# architecture_draft — DOA-ARCH-013

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-013
- Status: draft
- Date: 2026-04-10
- Parent: DOA-IDEA-002

---

## Overview

**DocOps Document Gate** — это тонкий **оркестрационный слой** поверх существующего **link/ID validator**: он не заменяет правила проверки документов, а **вызывает** validator как **engine**, затем применяет **политику** (severity → итоговый статус), формирует **единый machine-readable отчёт** и принимает **output decision** (разрешить или заблокировать фиксацию изменений в Git). Gate соответствует **DOA-IDEA-002**: без семантических правок, с опциональными **механическими** autofix только в отдельном режиме и белым списком.

## System position

Цепочка размещения в жизненном цикле артефактов:

**ChatGPT → Cursor → Files → Gate → Git**

- **ChatGPT / Cursor** производят и редактируют markdown в рабочей копии.
- **Files** — локальное дерево репозитория (source of truth для содержимого).
- **Gate** выполняется **перед** `git commit` / `git push` (или эквивалентом), читает файлы, вызывает validator, применяет policy, пишет отчёт и выставляет решение.
- **Git** фиксирует только прошедшие gate (или фиксация осознанно обходит gate вне данной архитектуры — не рекомендуется для канона DocOps).

## Components

### 1. Input handler

- Принимает параметры запуска: корень репозитория, **scope** (например `docs/**/*.md`, `README.md`, `WORKFLOW.md`), режим (**dry-run** / **autofix**), путь вывода JSON.
- Нормализует пути, проверяет доступность корня, опционально — список изменённых файлов (для инкрементального режима в будущем; в MVP допустим полный охват).

### 2. Validator (reuse existing)

- Вызывает **`scripts/doa_link_id_validator.py`** (или его модульный API после рефакторинга) как **единственный источник находок** по ссылкам, ID, метаданным и markdown-ссылкам в согласованном scope.
- Validator возвращает структурированные **findings** (категория, режим canonical/legacy, файл, детали) и агрегаты; Gate **не дублирует** бизнес-логику проверок.

### 3. Policy engine

- Загружает **политику** (конфиг: YAML/JSON/TOML рядом с репозиторием или встроенный default).
- Сопоставляет каждой **category** + **mode** (canonical / legacy / root) уровень **severity** от validator с **порогами** gate: что считается `error`, что `warn`, что `info`.
- Вычисляет итоговый **Gate status**: **ACCEPT**, **ACCEPT_WITH_WARNINGS**, **REJECT** (см. Decision model).

### 4. Report generator

- Собирает **единый JSON-отчёт** gate: метаданные прогона, версия validator, версия policy, сырой или вложенный блок findings, сводки, итоговый статус, код выхода.
- Опционально — краткий человекочитаемый summary в stdout (не заменяет JSON как контракт для CI).

### 5. Output decision

- На основе policy выставляет **process exit code** (например 0 = ACCEPT, 1 = REJECT, 2 = ACCEPT_WITH_WARNINGS — конкретная схема фиксируется в operational/decision документе).
- В **dry-run** решение всё равно вычисляется и записывается в отчёт; отличие — отсутствие записи файлов и отсутствие autofix.

## Decision model

### Статусы

| Статус | Смысл |
|--------|--------|
| **ACCEPT** | Нет находок с severity **error** по policy; допускается отсутствие предупреждений или только `info`. |
| **ACCEPT_WITH_WARNINGS** | Нет **error**; есть хотя бы одна находка с severity **warn** (например legacy-находки, разрешённые политикой MVP). |
| **REJECT** | Есть хотя бы одна находка с severity **error** (например неразрешённый Parent в каноническом документе, дубликат ID, битая ссылка в `docs/` — по таблице policy). |

### Severity → status

- Validator (v0.1+) отдаёт для каждой находки **category** и при v0.2+ нормализованный **severity** (`error` / `warn` / `info`), либо Gate **маппит** category→severity по default policy, если severity в отчёте validator отсутствует.
- **Policy engine** агрегирует: если любой finding → `error` → **REJECT**; иначе если любой → `warn` → **ACCEPT_WITH_WARNINGS**; иначе → **ACCEPT**.
- Политика может пометить отдельные **legacy** категории как `warn`, а **canonical** нарушения контракта **DOA-DEC-031** как `error` — это основной рычаг согласования с create-only (не чинить историю, но блокировать новые канонические ошибки).

## Validator integration

### Использование текущего validator

- Gate **подпроцессом или импортом** вызывает существующий скрипт; на вход передаётся root и scope; на выходе потребляется JSON (**stdout** или временный файл).
- Gate **не** форкнет альтернативную реализацию проверок ID/Parent; расширения делаются в validator (**DOA-OP-019**), Gate поднимает версию engine в отчёте.

### Совместимость v0.1 и v0.2

- **v0.1** (`doa-validator-report/1`): findings в `canonical_violations` / `legacy_findings`; Gate применяет **встроенную default policy** для category→severity, если поля severity отсутствуют.
- **v0.2** (план **DOA-OP-019**): ожидаются нормализованные **category**, явный **severity**, возможно `policy_version` / schema `doa-validator-report/2`; Gate читает оба варианта через **адаптер версии** (определяет schema по полю отчёта validator).
- Переход **v0.1 → v0.2** не ломает Gate, если адаптер зафиксирован; в отчёте gate указываются **engine_version** и **adapter_version**.

## Data contracts

### JSON report schema (high-level)

Объект верхнего уровня **gate_report** (имя конвенции, финальное имя — в operational):

- `schema`: строка, например `doa-gate-report/1`
- `generated_at_utc`: ISO-8601
- `repo_root`: путь
- `modes`: `{ "dry_run": bool, "autofix": bool }`
- `engine`: `{ "name", "version", "report_schema" }` — отражение validator
- `policy`: `{ "id", "version" }`
- `summary`: `{ "gate_status", "counts_by_severity", "files_scanned" }`
- `findings`: массив объектов `{ "severity", "mode", "category", "file", "detail", "source": "validator" }`
- `validator_report`: опционально вложенный сырой JSON validator для отладки

### Input / output

- **Input (CLI/config):** `--root`, `--scope` (повторяемые или glob-список), `--dry-run`, `--autofix` (optional), `--policy path`, `--out report.json`, `--format json`.
- **Output:** файл JSON по контракту выше + exit code; stderr — только диагностика, не контракт.

## Modes

### dry-run

- Полный прогон validator + policy + отчёт; **нет** записи в markdown файлы; autofix **выключен**.

### (optional) autofix mode

- Включён только явным флагом; выполняются **только** операции из **белого списка** (например CRLF→LF в metadata-блоке, trim trailing spaces в строках metadata) — без изменения смысла текста, заголовков, ID, Parent.
- Любое действие вне списка → **REJECT** конфигурации или no-op с записью в отчёт.
- После autofix рекомендуется второй прогон в dry-run для подтверждения.

## Constraints

- **create-only** для смысловой истории документов: Gate не отменяет политику новых файлов вместо правок.
- **no semantic edits:** запрещены переформулировки, смена ID/Parent/Replaces по «догадке», merge конфликтующих смыслов.
- **mechanical autofix only:** только явно перечисленные безопасные трансформации, отключаемые по умолчанию.

## Risks

- Расхождение версий validator и adapter gate → ложные ACCEPT/REJECT; митигация — явные версии в отчёте и закрепление в CI.
- Слишком мягкая policy превратит Gate в шум; слишком жёсткая — остановит работу на legacy; нужна калибровка с **DOA-OP-019**.
- Autofix «ползёт» к семантике — жёсткий whitelist и отдельное **decision_log** при расширении.

## Open questions

- Инкрементальный scope только по `git diff` vs полный прогон по умолчанию.
- Единый exit code mapping для всех CI (Windows/Linux).
- Нужен ли отдельный doc_type `rules` только для policy-файла gate в репозитории.
- Встраивание в Cursor hooks vs отдельная команда `make gate`.

## Next steps

- **decision_log** (при необходимости): обязательность gate, exit codes, whitelist autofix.
- **operational_plan**: реализация CLI gate, первый прогон против **DOA-OP-019**-совместимого validator v0.2, затем **implementation_snapshot**.
- Обновление **WORKFLOW.md** или отдельный **rules** документ — только create-only новым файлом, без правки исторических документов в рамках данной идеи.
