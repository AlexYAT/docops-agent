# DOA-OP-035 — Snapshot validator and gate rules

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-035
- Status: draft
- Date: 2026-04-17
- Parent: DOA-ARCH-024

---

## Summary

Операционный план по внедрению правил проверки fixed snapshot артефактов
в validator и document gate.

Цель:
сделать snapshot не только описанным архитектурно, но и формально проверяемым.

---

## Goal

Определить и подготовить правила, по которым система сможет валидировать snapshot-документы и учитывать их в gate semantics.

---

## Scope

Входит:
- правила проверки metadata snapshot
- правила проверки invariants
- правила проверки linking semantics
- правила учёта snapshot в document gate

Не входит:
- полная автоматизация lifecycle
- изменение уже созданных snapshot-документов
- UI для snapshot management

---

## Tasks

### T01 — Зафиксировать validator checks для snapshot metadata

Done when:
- определены обязательные поля snapshot
- определены проверки формата ID, type, status, parent

### T02 — Зафиксировать validator checks для snapshot invariants

Done when:
- определено, что snapshot immutable
- определено, что snapshot не должен ссылаться на future artifacts
- определено, что snapshot является boundary artifact

### T03 — Зафиксировать linking rules для controlled зоны

Done when:
- описаны правила ссылок controlled → snapshot
- описаны ограничения прямых ссылок controlled → legacy

### T04 — Зафиксировать gate semantics для snapshot

Done when:
- определено, как gate учитывает snapshot
- определено, какие ошибки snapshot считаются критическими

### T05 — Подготовить decision_log по policy level

Done when:
- указано, что policy severity для snapshot должна быть зафиксирована отдельным decision_log

### T06 — Подготовить implementation snapshot после внедрения

Done when:
- указано, что после выполнения плана нужен отдельный implementation_snapshot

---

## Dependencies

- DOA-ARCH-024
- DOA-DEC-053
- DOA-OP-034
- templates/fixed_snapshot_template.md

---

## Risks

- слишком жёсткие правила на раннем этапе
- расхождение между архитектурой snapshot и validator implementation
- смешение legacy-проверок и snapshot-проверок

---

## Expected Result

Система получает формальный и проверяемый набор правил для fixed snapshot:

- validator понимает snapshot как отдельный artifact class
- gate умеет учитывать snapshot semantics
- epoch boundary становится не только концепцией, но и машинно-проверяемым правилом

---

## Follow-up

- decision_log по severity/policy
- implementation_snapshot по результату внедрения
- возможное расширение отчётов validator/gate для snapshot diagnostics
