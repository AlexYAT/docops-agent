# DOA-OP-036 — Snapshot readiness checks

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-036
- Status: draft
- Date: 2026-04-17
- Parent: DOA-IMP-035

---

## Summary

Операционный план по формализации readiness checks перед созданием нового fixed snapshot.

Цель:
сделать переход к следующему snapshot не ad-hoc, а проверяемым и воспроизводимым.

---

## Goal

Определить минимальный набор проверок, который подтверждает готовность controlled зоны к фиксации в новый snapshot.

---

## Scope

Входит:
- readiness criteria для controlled зоны
- использование validator/gate отчётов
- минимальный checklist перед snapshot creation
- правила фиксации результата проверки

Не входит:
- автоматический запуск readiness checks
- изменение существующего validator/gate UI
- полная lifecycle automation

---

## Tasks

### T01 — Зафиксировать обязательные readiness criteria

Done when:
- определено, что `gate_status_controlled = ACCEPT`
- определено, что отсутствуют критические snapshot-related ошибки в controlled зоне
- определено, что отсутствуют cross-zone violations

### T02 — Зафиксировать входные артефакты проверки

Done when:
- перечислены validator report
- перечислены gate report
- перечислены ключевые документы текущей эпохи

### T03 — Зафиксировать минимальный readiness checklist

Done when:
- описан пошаговый checklist
- checklist можно выполнить вручную без неоднозначности

### T04 — Зафиксировать правила интерпретации результатов

Done when:
- описано, когда система считается ready
- описано, когда readiness check считается failed
- описано, какие findings допустимы, а какие блокируют snapshot

### T05 — Зафиксировать артефакт результата проверки

Done when:
- указано, что результат readiness check должен фиксироваться отдельным implementation_snapshot или audit_check

### T06 — Подготовить follow-up на snapshot creation run

Done when:
- указано, что после успешного readiness check выполняется отдельный шаг создания нового DOA-FSN

---

## Dependencies

- DOA-ARCH-024
- DOA-DEC-053
- DOA-DEC-054
- DOA-OP-034
- DOA-OP-035
- DOA-IMP-035

---

## Risks

- слишком мягкие readiness criteria
- слишком жёсткие readiness criteria для MVP
- смешение historical REJECT и operational ACCEPT
- пропуск snapshot-specific ошибок при ручной интерпретации

---

## Expected Result

Система получает воспроизводимый readiness protocol:

- ясно, когда controlled зона готова к snapshot
- validator/gate отчёты используются как operational evidence
- создание snapshot начинается только после формальной readiness проверки

---

## Follow-up

- audit_check или implementation_snapshot по readiness run
- создание следующего fixed snapshot
- возможное последующее ужесточение readiness criteria
