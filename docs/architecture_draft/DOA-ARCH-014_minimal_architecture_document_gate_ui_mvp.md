# architecture_draft — DOA-ARCH-014

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-014
- Status: draft
- Date: 2026-04-10
- Parent: DOA-IDEA-003

---

## Overview

**Document Gate UI MVP** — минимальный локальный интерфейс для **dogfooding** и ускорения личного ежедневного
DocOps workflow. UI не внедряет новые правила проверки и не меняет source of truth: он запускает существующий
gate, читает его JSON-отчет и показывает результат человеку.

## Architectural choice

Выбран минимально затратный вариант MVP:

- **FastAPI + Jinja2 templates**
- **local web UI**
- **server-side rendering**
- **subprocess call to `scripts/doa_document_gate.py`**

Почему этот вариант минимально затратный:

- **против desktop UI:** не требует упаковки бинарников/инсталляторов, проще запуск локально в dev-режиме;
- **против SPA/frontend-first:** не нужен отдельный frontend pipeline (bundler, state management, API contract);
- **против API-first + отдельный frontend:** меньше кода и интеграционных точек, быстрее дойти до рабочего dogfooding.

Идея: сначала получить рабочий UX-слой поверх текущего CLI gate, потом при необходимости эволюционировать.

## System position

Рекомендуемая цепочка в MVP:

**ChatGPT -> Cursor -> Files -> Gate -> UI (human view) -> Git**

Разделение ответственности:

- **Gate** остается execution/policy layer (engine adapter, severity mapping, gate_status, JSON report).
- **UI** остается visualization/trigger layer (запуск процесса, чтение результата, отображение).

UI не принимает решений вместо gate и не меняет policy.

## Components

1. **UI page**  
   Одна страница с кнопкой запуска и блоками результата.

2. **Backend route handler**  
   HTTP-обработчик принимает действие "run" и ограниченный набор параметров.

3. **Subprocess runner for gate**  
   Безопасно запускает существующий `scripts/doa_document_gate.py`.

4. **Report reader / parser**  
   Читает сгенерированный JSON report (`doa-gate-report/1`) и извлекает поля для отображения.

5. **Result renderer**  
   SSR-рендер страницы с `gate_status`, counts, findings и путем к отчету.

## Execution model

- UI вызывает существующий `doa_document_gate.py` как subprocess.
- Входные параметры ограничены (root/out/dry-run; без произвольного shell passthrough).
- Результат берется из generated JSON report.
- UI **не пересчитывает findings** и **не реализует свою policy logic**.

## Data flow

`user action -> backend route -> subprocess gate run -> JSON report -> UI render`

Дополнительно:

- stderr/stdout процесса используется только как техническая диагностика;
- итоговые данные для интерфейса берутся из JSON report как из машинного контракта.

## Routes / screens

Минимум для MVP:

- **`GET /`** — главная страница (форма + последний результат при наличии);
- **`POST /run`** — запуск gate;
- **result view** — на той же странице после redirect (`POST/Redirect/GET`) или прямой SSR-ответ.

## MVP scope

UI MVP умеет только:

- запуск gate;
- показывать `gate_status`;
- показывать `counts`;
- показывать `findings`;
- показывать путь к report;
- работать только в **dry-run** режиме.

## Constraints

- **no validator duplication**
- **no gate logic duplication**
- **no semantic edits**
- **no autofix**
- **no git operations**
- **source of truth remains repo + JSON report**

UI не должен становиться вторым engine или вторым policy-слоем.

## Risks

- **Subprocess/security boundaries:** риск небезопасной передачи параметров и запуска команд.
- **Temptation to move logic into UI:** при росте требований есть риск дублировать policy/findings parsing.
- **Overgrowth into full product UI:** MVP может разрастись в тяжелый интерфейс раньше стабилизации gate/validator.

## Open questions

- Нужен ли **HTMX** сразу, или оставить чистый SSR и добавить позже?
- На следующем этапе лучше оставить **subprocess** или перейти на импортируемый API gate?
- Должен ли `repo_root` быть фиксированным (current repo) или редактируемым в UI?

## Next steps

- **decision_log** — только если потребуется отдельная фиксация по security/process policy для UI.
- **operational_plan** — реализация UI MVP (минимальный сервер, маршруты, первый запуск, snapshot).
