# operational_plan — DOA-OP-021

## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-021
- Status: draft
- Date: 2026-04-10
- Parent: DOA-ARCH-014

---

## Goal

Реализовать минимальный локальный UI над существующим Document Gate для dogfooding и ускорения ежедневного
DocOps workflow пользователя: быстрый запуск gate и удобный просмотр результата без ручного разбора JSON.

## Scope

### In

- FastAPI app;
- Jinja2 templates;
- одна главная страница;
- запуск gate через subprocess;
- чтение JSON report;
- отображение `gate_status` / `counts` / `findings` / `report path`;
- только dry-run.

### Out

- validator changes;
- gate logic changes;
- autofix;
- git operations;
- semantic edits;
- SPA / frontend-heavy stack.

## Inputs

- `DOA-IDEA-003`
- `DOA-ARCH-014`
- `DOA-OP-020`
- `DOA-IMP-015`
- `scripts/doa_document_gate.py`

## Tasks

### T01 — FastAPI app skeleton

Создать минимальную структуру UI-приложения: `app`, шаблоны, конфиг путей, entrypoint запуска.

**Done when:** сервер стартует локально, рендерит базовый шаблон без интеграции gate.

---

### T02 — Main page route

Реализовать `GET /` с формой запуска и областью для результата/ошибок.

**Done when:** страница открывается в браузере и содержит контролы запуска dry-run.

---

### T03 — Gate subprocess integration

Реализовать `POST /run`, который вызывает существующий `scripts/doa_document_gate.py` как subprocess.

**Done when:** маршрут вызывает existing gate и не внедряет собственные проверки validator/policy.

---

### T04 — Report loading/parsing

После прогона читать сгенерированный JSON report и готовить данные для шаблона.

**Done when:** данные извлекаются из report по ключам (`gate_status`, `counts`, `findings`, путь).

---

### T05 — Result rendering

Отобразить в UI: `gate_status`, `counts`, список `findings`, путь к report.

**Done when:** пользователь видит те же значения, что записаны в JSON report, без дополнительной логики
пересчета на стороне UI.

---

### T06 — Dry-run only guardrail

Жестко зафиксировать режим UI только dry-run; autofix и любые git-действия в интерфейсе отсутствуют.

**Done when:** UI не предоставляет параметров/кнопок для autofix и git operations.

---

### T07 — First UI run

Выполнить первый локальный end-to-end прогон: открыть UI, запустить gate, проверить корректный рендер результата.

**Done when:** подтверждена рабочая цепочка `UI -> subprocess gate -> JSON report -> UI`.

---

### T08 — Implementation snapshot

Создать новый `implementation_snapshot` с фиксацией первого UI-прогона.

**Done when:** новый `DOA-IMP-*` документ создан и ссылается на результаты T07.

## Success criteria

- UI не дублирует validator/gate logic.
- UI запускает существующий gate.
- UI показывает те же результаты, что и JSON report.
- UI работает только в dry-run.
- После первого запуска создается implementation_snapshot.

## Risks

- subprocess/security boundaries (передача аргументов, контроль путей, обработка ошибок запуска);
- temptation to move logic into UI (риск постепенного дублирования policy/findings logic);
- overengineering of UI (выход за рамки минимального dogfooding-инструмента).

## Out of scope

- autofix;
- git operations;
- editing documents;
- changing validator/gate contracts;
- multi-user/server deployment.

## Next artifact

После T08 — новый `implementation_snapshot` (следующий свободный `DOA-IMP-*`) с результатами первого UI-run.
