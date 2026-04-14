# audit_check — DOA-AUD-007

## Metadata

- Project: docops-agent
- Doc type: audit_check
- ID: DOA-AUD-007
- Status: draft
- Date: 2026-04-14
- Parent: DOA-ARCH-020

---

## Title

Архитектурная проверка инвариантов после стабилизации (Policy Contract, binding, Report Layer, DoD)

## Scope

Проверка **только текста** следующих артефактов на взаимную согласованность с заявленными инвариантами (без анализа кода validator/gate и без запуска инструментов):

- `docs/architecture_draft/DOA-ARCH-018_policy_contract_type_aware_lifecycle.md`
- `docs/architecture_draft/DOA-ARCH-019_report_layer_and_minimal_report_schema.md`
- `docs/architecture_draft/DOA-ARCH-020_policy_contract_binding_validator_gate.md`
- `docs/decision_log/DOA-DEC-039_machine_verifiable_dod_for_report_generator_mvp.md`

## Audit criteria

### Policy Contract consistency

- В `DOA-ARCH-018` зафиксирован единый Policy Contract для статусов, переходов, validator, gate и нормализации severity (`DOA-ARCH-018`, разделы «Policy contract role», «Validator contract», «Gate contract», «Severity normalization rules»).

### Validator / Gate alignment

- В `DOA-ARCH-018` и `DOA-ARCH-020` зафиксировано: validator и gate **MUST** опираться на один и тот же контракт; gate **MUST NOT** переопределять severity вне контракта; gate **MUST** использовать вывод validator как вход (`DOA-ARCH-018`; `DOA-ARCH-020`, разделы «Validator binding rules», «Gate binding rules», «Forbidden divergence scenarios»).

### Report Layer anti-SoT invariants

- В `DOA-ARCH-019` зафиксировано: отчёт — производный артефакт; **MUST NOT** быть SoT; **MUST NOT** порождать report-only факты; запрет `Parent`/`Replaces` на отчёт и запрет решений только по отчёту без ссылок на канон (`DOA-ARCH-019`, разделы «Report Layer definition», «Anti-SoT invariants», «Forbidden usages»).
- В `DOA-ARCH-018` (Scope) и `DOA-ARCH-020` (Policy Contract binding model / Traceability) отчёты **MUST NOT** быть источником норм policy — согласуется с `DOA-ARCH-019`.

### Machine-verifiable DoD completeness

- В `DOA-DEC-039` DoD MVP генератора отчёта выражен **исключительно** перечнем проверяемых условий (шесть критериев) и явным запретом субъективных обязательных критериев (`DOA-DEC-039`, разделы «Machine-verifiable DoD criteria», «Rejected criteria»).

## Findings

| Критерий | Утверждение (привязка к документу) |
|-----------|-------------------------------------|
| Policy Contract consistency | `DOA-ARCH-018` объявляет Policy Contract единственным архитектурным источником норм для перечисленных аспектов жизненного цикла и severity (раздел «Policy contract role»). |
| Validator / Gate alignment | `DOA-ARCH-020` указывает policy на `DOA-ARCH-018` и преемниках и дублирует запрет на независимую трактовку и на изменение severity gate вне контракта (разделы «Policy Contract binding model», «Gate binding rules»). Содержательно согласуется с `DOA-ARCH-018`. |
| Report Layer anti-SoT | `DOA-ARCH-019` содержит явные **MUST NOT** против SoT и против использования отчёта как нормативного источника; `DOA-ARCH-020` запрещает использовать отчёты как источник policy. Противоречий между `DOA-ARCH-019` и `DOA-ARCH-020` по данному пункту не обнаружено. |
| Machine-verifiable DoD | `DOA-DEC-039` фиксирует «if and only if» по шести механическим условиям и перечисляет отклонённые субъективные критерии; ссылочно опирается на схему отчёта `DOA-ARCH-019` (разделы «Machine-verifiable DoD criteria», п. 2–3). |
| Объём вывода | Настоящий аудит **не** устанавливает факт соответствия **реализации** validator/gate или генератора отчёта данным артефактам: это **вне** объявленного Scope. |

## Violations

Нарушений согласованности **между четырьмя перечисленными документами** не зафиксировано.

## Pass / Fail

**Pass** — для цели «согласованность архитектурной документации в Scope»: противоречий между `DOA-ARCH-018`, `DOA-ARCH-019`, `DOA-ARCH-020` и `DOA-DEC-039` по проверенным критериям нет.

**Не оценивается в рамках настоящего аудита** (не **Fail**, а **вне Scope**): соответствие исполняемых компонентов репозитория этим артефактам.

## Notes

- Статусы `draft` у проверенных `architecture_draft` и `decision_log` отражают стадию канона документа, а не результат настоящего аудита.
- Условие «раздельный запуск» validator/gate в `DOA-ARCH-020` оговорено нормативно совместимостью версий policy; это **не** ослабление единого контракта при соблюдении раздела «Policy versioning» и «Failure conditions» того же документа.

## Traceability

- `docs/architecture_draft/DOA-ARCH-018_policy_contract_type_aware_lifecycle.md`
- `docs/architecture_draft/DOA-ARCH-019_report_layer_and_minimal_report_schema.md`
- `docs/architecture_draft/DOA-ARCH-020_policy_contract_binding_validator_gate.md`
- `docs/decision_log/DOA-DEC-039_machine_verifiable_dod_for_report_generator_mvp.md`
