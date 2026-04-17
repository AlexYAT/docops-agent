# DOA-OP-037 — Snapshot creation execution

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-037
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-057

---

## Title

Execution plan для создания fixed snapshot (boundary epoch)

---

## Objective

Создать fixed snapshot как boundary, изолирующий legacy слой и запускающий новую controlled эпоху.

---

## Scope

Snapshot должен:

- зафиксировать текущее состояние системы “как есть”
- не исправлять legacy ошибки
- определить boundary между legacy и controlled
- стать единственной точкой входа в новую эпоху

---

## Tasks

### OP-037-T01 — Snapshot scope definition

Определить список документов, входящих в snapshot:

Done when:
- сформирован полный список DOA-* документов
- scope зафиксирован

---

### OP-037-T02 — Snapshot artifact creation

Создать fixed snapshot документ:

Done when:
- создан DOA-FSN-XXX
- заполнены:
  - System State
  - Scope
  - Gate Status
  - Validator Status
  - Epoch Definition

---

### OP-037-T03 — Boundary activation

Зафиксировать snapshot как boundary:

Done when:
- snapshot используется как root reference
- новая controlled зона считается начатой

---

### OP-037-T04 — Controlled mode enforcement

Зафиксировать правила работы после snapshot:

Done when:
- новые документы создаются только post-snapshot
- ссылки на legacy идут только через snapshot

---

## Execution Order

1. T01
2. T02
3. T03
4. T04

---

## Success Criteria

- snapshot создан
- snapshot принят как boundary
- controlled epoch активирована
- новые документы работают только через snapshot

---

## Notes

Snapshot не требует устранения legacy ошибок.
