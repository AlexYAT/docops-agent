## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-032
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-ARCH-013

---

## Title

Policy model for DocOps Document Gate MVP

## Context

Идея **DOA-IDEA-002** и архитектура **DOA-ARCH-013** вводят **DocOps Document Gate** как слой над существующим **link/ID validator** с политикой статусов и severity. До **operational_plan** нужно зафиксировать **обязательные policy-решения** MVP, согласованные с **DOA-DEC-031** (canonical vs legacy) и текущим validator track (**DOA-OP-018**, **DOA-OP-019**, **DOA-IMP-013**). **DOA-ARCH-013** считается валидным идентификатором архитектурного артефакта в репозитории.

## Options considered

1. **Статусы только PASS/FAIL** — проще, но не отражает допустимость legacy-предупреждений при create-only.
2. **Gate как форк validator с собственными проверками** — дублирование логики и расхождение с **DOA-OP-019**.
3. **Трёхуровневая модель статусов + маппинг severity + dry-run по умолчанию + строгий autofix** — соответствует **DOA-ARCH-013** и **DOA-IDEA-002**.

## Chosen solution

Принять для **MVP Document Gate** следующую политику:

### 1. Gate status model

- **ACCEPT** — прогон разрешён; блокирующих условий нет.
- **ACCEPT_WITH_WARNINGS** — прогон разрешён с предупреждениями; блокирующих условий нет.
- **REJECT** — прогон не считается допустимым для фиксации (commit/push по согласованному workflow); есть хотя бы одно блокирующее условие по политике.

### 2. Severity mapping

Агрегация находок от **engine (validator)** после применения **policy** к severity каждой находки:

- **error** → итог **REJECT** (если присутствует хотя бы одна находка с severity **error**).
- **warn** → при отсутствии **error** итог **ACCEPT_WITH_WARNINGS** (если есть хотя бы одна **warn**).
- **info** (только) → при отсутствии **error** и **warn** итог **ACCEPT**.

Приоритет: **error** жёстче **warn**, **warn** жёстче **info**.

### 3. Default mode

- По умолчанию для внедрения и первых интеграций: **dry-run first** — полный прогон проверок и отчёт **без** записи в файлы и **без** autofix, если не указано иное явной конфигурацией/флагом.

### 4. Autofix policy

- **Семантические правки запрещены** (смысл текста, ID, Parent, Replaces, формулировки решений и т.п. gate не меняет).
- **Только механические autofix** и **только** при **явном флаге/режиме** (opt-in); перечень допустимых операций — белый список в **operational_plan** / реализации, не в данном решении.

### 5. Validator reuse

- **Gate использует существующий validator как engine** и **не дублирует** правила проверки ссылок, ID и метаданных; расширения проверок вносятся в **validator** (линия **DOA-OP-018** / **DOA-OP-019**), Gate отвечает за **policy**, **агрегацию severity**, **итоговый статус** и **формат gate-отчёта**.

## Why

- Три статуса отражают реальность репозитория с **legacy** без нарушения **create-only**.
- Детерминированный маппинг **severity → статус** устраняет споры в CI и в ручном запуске.
- **Dry-run по умолчанию** снижает риск случайных правок и упрощает первое внедрение.
- Запрет семантического autofix сохраняет доверие к документам как SoT.
- Единый **engine** исключает расхождение двух наборов правил.

## Trade-offs

- Пока validator **v0.1** не всегда отдаёт **severity**, Gate или policy должны временно **маппить category → severity** (как описано в **DOA-ARCH-013**) — дополнительная сложность до **v0.2**.
- **ACCEPT_WITH_WARNINGS** может привыкнуть к «всегда зелёно» — нужен дисциплинированный **operational_plan** и при необходимости ужесточение policy позже (новый **decision_log**, create-only).

## Follow-ups

- **operational_plan**: реализация CLI gate, путь к policy-файлу, exit codes, первый прогон.
- После **DOA-OP-019** (validator v0.2): выровнять policy с нормализованными **severity** в отчёте engine.
- При расширении whitelist механических autofix — отдельное **decision_log** (create-only).
