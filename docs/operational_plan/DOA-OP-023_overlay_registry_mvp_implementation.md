# operational_plan — DOA-OP-023

## Metadata

- Project: DocOps Agent
- Doc type: operational_plan
- ID: DOA-OP-023
- Status: planned
- Date: 2026-04-10
- Parent: DOA-DEC-036

---

## Goal

Operationalize overlay registry MVP для canonical remediation без правки исторических документов: ввести
прозрачный и трассируемый слой mapping/alias/override, который снижает влияние legacy/canonical blockers,
сохраняя create-only и canonical metadata как source of truth для новых документов.

## Scope

### In

- спецификация формата overlay registry;
- начальный набор overlay-правил;
- поддержка overlay в validator;
- классификация findings (`resolved_via_overlay` / `unresolved`);
- учет resolved findings на уровне gate;
- повторный прогон validator + gate и сравнение с предыдущим baseline;
- фиксация результата в implementation_snapshot.

### Out

- массовая правка исторических markdown документов;
- изменение смысла legacy документов;
- смена source of truth для новых документов (остается canonical metadata);
- UI-расширения вне необходимого отображения статусов.

## Inputs

- `DOA-OP-022` — hardening cycle;
- `DOA-DEC-036` — overlay remediation strategy;
- последние отчеты validator/gate (`reports/doa_link_id_validator_run_001.json`, `reports/doa_document_gate_run_001.json`);
- существующие `scripts/doa_link_id_validator.py` и `scripts/doa_document_gate.py`;
- текущий набор canonical blockers из аудита.

## Tasks

### T01 — Define overlay registry format

- зафиксировать минимальный формат registry: mapping, alias, override;
- определить обязательные поля для traceability (id, reason, source, date/status при необходимости);
- описать порядок применения overlay.

### T02 — Create initial overlay rules document(s)

- создать начальный overlay документ (или набор документов) с правилами для известных blockers;
- каждое правило должно быть явным и трассируемым.

### T03 — Add validator support for overlay loading

- добавить чтение overlay слоя в validator pipeline;
- порядок: сначала overlay, затем документы.

### T04 — Classify findings as resolved_via_overlay / unresolved

- в результатах validator отметить, какие проблемы закрыты overlay;
- сохранять исходный сигнал + статус разрешения, чтобы не терять прозрачность.

### T05 — Adjust gate handling for resolved findings

- обновить gate-агрегацию так, чтобы findings со статусом `resolved_via_overlay` не считались `error`;
- допустить downgrade по policy (например до `info`) без сокрытия источника.

### T06 — Rerun validator and gate

- выполнить повторный прогон после внедрения overlay поддержки;
- сохранить новые machine-readable отчеты.

### T07 — Compare against previous canonical blockers

- сравнить новый прогон с предыдущим baseline;
- отдельно оценить: что закрыто overlay, что осталось unresolved.

### T08 — Create implementation_snapshot

- оформить новый implementation_snapshot с результатами цикла и ссылками на отчеты/overlay-документы.

## Success criteria

- overlay registry формализован и прозрачен (traceable правила);
- исторические markdown документы не изменяются;
- validator и gate учитывают overlay в соответствии с `DOA-DEC-036`;
- findings разделяются на `resolved_via_overlay` и `unresolved`;
- наблюдается снижение критичных canonical blockers или их переход в контролируемую категорию;
- создан новый implementation_snapshot.

## Risks

- усложнение validator/gate из-за дополнительного слоя overlay;
- риск скрыть реальные проблемы при неправильной классификации resolved/unresolved;
- несогласованность формата overlay при быстром росте правил без строгого контракта.

## Out of scope

- ручная перепись legacy документов;
- изменение бизнес-смысла существующих документов;
- автоматический semantic autofix;
- git automation или принудительные workflow-ограничения на этом шаге.

## Next artifact

- новый `implementation_snapshot` (следующий свободный `DOA-IMP-*`) после выполнения T08.
