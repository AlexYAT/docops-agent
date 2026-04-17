# DOA-DEC-054 — Snapshot policy severity

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-054
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-OP-035

---

## Title

Определить severity policy для snapshot-related findings

---

## Context

Система DocOps ввела fixed snapshot как отдельный artifact class.

Для дальнейшей интеграции snapshot в validator и document gate необходимо определить policy severity для типовых нарушений, связанных со snapshot:

- metadata violations
- invariant violations
- linking violations
- lifecycle-related violations

Без явного policy severity невозможно консистентно определить:

- что блокирует gate
- что считается warning
- что является informational finding

---

## Options considered

1. Не фиксировать severity явно и определять case-by-case
2. Зафиксировать минимальную severity policy для snapshot findings
3. Сразу ввести жёсткую и полную policy matrix

---

## Chosen solution

Зафиксировать минимальную severity policy для snapshot findings на MVP-этапе

---

## Policy

### Error

К error относятся нарушения, которые ломают snapshot как boundary artifact:

- неверный `Doc type` у snapshot
- неверный ID format (`DOA-FSN-XXX`)
- `Status` не равен `accepted`
- отсутствует обязательное поле metadata
- snapshot ссылается на future artifact
- snapshot нарушает boundary semantics
- controlled документ ссылается напрямую на legacy, минуя snapshot, в случаях где это запрещено policy

### Warning

К warning относятся нарушения, которые не ломают snapshot полностью, но ухудшают качество и предсказуемость:

- неполный scope
- недостаточно ясное описание epoch
- неполный validator status
- неполный gate status
- неуточнённый parent в допустимых пограничных случаях

### Info

К info относятся наблюдения, не влияющие на gate decision напрямую:

- дополнительные notes
- расширенные пояснения по состоянию системы
- диагностические annotations

---

## Why

- позволяет сделать snapshot machine-checkable
- делает gate semantics предсказуемыми
- отделяет критические нарушения от качественных замечаний
- поддерживает постепенное ужесточение policy

---

## Trade-offs

- часть спорных случаев останется на уровне интерпретации
- policy MVP может потребовать уточнения позже
- на раннем этапе возможны conservative classifications

---

## Consequences

- validator/gate implementation получает базовую policy опору
- snapshot findings можно классифицировать единообразно
- snapshot становится полноценной частью control layer

---

## Follow-ups

- implementation operational tasks по validator/gate
- implementation_snapshot после внедрения правил
- возможное расширение severity matrix в следующих эпохах
