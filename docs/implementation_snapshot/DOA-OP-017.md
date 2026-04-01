# operational_plan — DOA-OP-017

## Project
DocOps Agent (DOA)

## Parent
DOA-OP-002

---

## Stage
DocOps v2 — Stabilization & Automation

---

## Status
planned

---

## Goals

Перевести систему из MVP в стабильный инструмент.

---

## Tasks

### OP-01 — Strict auto-doc
Done when:
- каждый документ создаётся сразу в Notion
- нет “локально без MCP”

---

### OP-02 — Template Pack v1
Done when:
- все doc_types имеют шаблоны
- Cursor генерирует без отклонений

---

### OP-03 — Auto ID generation
Done when:
- DOA-DEC / DOA-IMP / DOA-OP генерируются автоматически

---

### OP-04 — Prompt standardization
Done when:
- достаточно 1 строки для создания документа

---

### OP-05 — Error handling MCP
Done when:
- 404 / доступ / workspace ошибки обрабатываются явно

---

## Exit Criteria

Система считается стабильной, если:

- pipeline работает без ручных правок
- документы создаются предсказуемо
- структура не ломается при росте количества документов