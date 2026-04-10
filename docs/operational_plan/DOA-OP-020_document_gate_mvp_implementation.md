# operational_plan — DOA-OP-020

## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-020
- Status: draft
- Date: 2026-04-10
- Parent: DOA-DEC-032

---

## Goal

Реализовать **MVP DocOps Document Gate** по **DOA-ARCH-013** и принятой политике **DOA-DEC-032**: тонкий оркестратор поверх **`scripts/doa_link_id_validator.py`**, который **не дублирует** логику проверок validator, применяет **severity → gate status**, по умолчанию работает в **dry-run**, опционально допускает **только механические** autofix под guardrails, выдаёт **machine-readable JSON** с **`gate_status`**, **`engine_version`**, **`policy_version`** и **counts**. **Семантический autofix запрещён** (см. **DOA-DEC-032**).

## Scope

### Includes

- интерфейс CLI (или эквивалент) для gate;
- адаптер к отчёту validator **v0.1** и задел под **v0.2**;
- policy mapping и генерация gate JSON;
- первый полный прогон по репозиторию и **implementation_snapshot** по результатам.

### Excludes

- дублирование правил link/ID/metadata вне validator (**gate must not duplicate validator logic**);
- семантические автоправки содержимого документов (**semantic autofix forbidden**);
- обязательная интеграция в конкретный CI-провайдер (может быть follow-up);
- изменение существующих markdown в `docs/` для «зелёного» прогона (create-only дисциплина сохраняется).

## Inputs

- **DOA-IDEA-002** — цель и границы Gate MVP.
- **DOA-ARCH-013** — компоненты, контракты, режимы.
- **DOA-DEC-032** — статусы, маппинг severity, dry-run по умолчанию, autofix policy, reuse validator.
- **scripts/doa_link_id_validator.py** — engine (текущая линия **DOA-OP-018** / **DOA-OP-019**).
- **DOA-DEC-031** — canonical vs legacy для интерпретации находок.

## Tasks

### T01 — Define gate CLI interface

**Описание:** Зафиксировать контракт запуска: флаги `--root`, `--out`, `--policy`, `--dry-run` (default on), `--autofix` (opt-in), опционально `--engine-args`; коды выхода, согласованные с **DOA-DEC-032** (детализация в реализации).

**Done when:** Интерфейс описан в README рядом с кодом gate или в docstring entrypoint; пример команды воспроизводим.

---

### T02 — Implement validator adapter (v0.1 / v0.2 compatibility)

**Описание:** Вызов validator как **единственного** источника находок; разбор JSON (`doa-validator-report/1` и задел под `/2`); нормализация списка findings для policy-слоя. **Gate не реализует повторно** проверки Parent/ID/ссылок.

**Done when:** Адаптер возвращает унифицированную структуру findings + `engine_version` / schema из отчёта validator.

---

### T03 — Implement policy mapping severity → gate status

**Описание:** Загрузка default policy (category/mode → severity при отсутствии severity в engine); агрегация: **error → REJECT**, **warn → ACCEPT_WITH_WARNINGS** (если нет error), **info only → ACCEPT** (**DOA-DEC-032**).

**Done when:** Для тестового набора находок итоговый `gate_status` детерминирован и покрыт минимальными unit/ручными проверками.

---

### T04 — Implement gate JSON report

**Описание:** Сформировать отчёт по контуру **DOA-ARCH-013**; **обязательные поля верхнего уровня:** **`gate_status`**, **`engine_version`**, **`policy_version`**, **`counts`** (как минимум агрегаты по severity и/или по canonical vs legacy — уточнить в схеме `doa-gate-report/1`).

**Done when:** Один прогон пишет валидируемый JSON файл; перечисленные ключи присутствуют.

---

### T05 — Implement dry-run default flow

**Описание:** По умолчанию: полный прогон engine + policy + отчёт **без** записи в markdown и **без** autofix (**DOA-DEC-032**).

**Done when:** Запуск без `--autofix` не модифицирует `docs/` и корневые md; поведение задокументировано.

---

### T06 — Implement optional mechanical autofix guardrails

**Описание:** Режим только при явном флаге; **whitelist** механических операций (например нормализация перевода строк в блоке metadata); отказ при любой попытке семантического изменения. **Semantic autofix forbidden.**

**Done when:** Без флага autofix не выполняется; с флагом разрешены только операции из whitelist; любое расширение списка — только через новый **decision_log** (create-only).

---

### T07 — First gate run on repository

**Описание:** Прогон на том же охвате, что и validator по умолчанию (`docs/**/*.md`, `README.md`, `WORKFLOW.md` или эквивалент, согласованный с engine); сохранить gate JSON (например `reports/doa_document_gate_run_001.json`).

**Done when:** Артефакт отчёта существует, `gate_status` и обязательные поля заполнены.

---

### T08 — Implementation snapshot after first run

**Описание:** Создать новый **implementation_snapshot** с уникальным ID, **Parent:** **DOA-OP-020**, со ссылкой на отчёт T07, версии engine/policy и кратким резюме.

**Done when:** Файл в `docs/implementation_snapshot/` создан; цикл MVP gate зафиксирован для следующего этапа (CI / v0.2 alignment).

## Success criteria

- Gate вызывает **только** validator для проверок; **дублирования логики validator в gate нет**.
- **Семантический autofix** отсутствует; **механический** — только opt-in и whitelist (**T06**).
- JSON-отчёт содержит **`gate_status`**, **`engine_version`**, **`policy_version`**, **`counts`**.
- Поток по умолчанию — **dry-run** (**T05**).
- Выполнены **T07** и **T08**.

## Risks

- Несовпадение версий engine и адаптера → неверный `gate_status`; митигация — явные версии в отчёте и тест на sample JSON.
- Расширение whitelist autofix может размыть границу с семантикой — жёсткий контроль через **decision_log**.

## Out of scope

- Правка legacy-документов под нулевые предупреждения.
- Замена **DOA-OP-019**; gate потребляет результаты engine по мере готовности **v0.2**.

## Next artifact

После **T08** — новый **`implementation_snapshot`** (следующий свободный **DOA-IMP-***) с приложенным путём к **`reports/doa_document_gate_run_001.json`** (или фактическое имя отчёта первого прогона).
