# Decision: DOA-DEC-004

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted (temporary)

---

## Title
Временный упрощённый workflow разработки (Cursor → MCP → Notion)

---

## Context

Текущая структура документации (planning + templates + связи) сложна для удержания в голове
на этапе MVP.

Практическая работа ведётся быстрее через:

обсуждение → prompt → Cursor → результат

Дополнительно используется:

- MCP (как execution layer)
- Notion (как внешний storage/навигация)

Mindmap помогает, но не решает полностью проблему когнитивной нагрузки.

---

## Problem

Docs-first подход требует:
- создания документов до действий
- строгого следования planning layer

На практике:
- это замедляет работу на раннем этапе
- вызывает перегрузку структуры

---

## Chosen Solution

Ввести временный упрощённый workflow:

обсуждение → prompt → Cursor → MCP → Notion

с последующей фиксацией в документации (snapshot / decision / plan)

---

## Why

- снижает когнитивную нагрузку
- ускоряет MVP-итерации
- соответствует реальному процессу работы (Cursor-first)
- позволяет не блокироваться на структуре

---

## Trade-offs

- нарушение strict docs-first
- возможна потеря traceability
- риск расхождения между фактической работой и документацией

---

## Constraints

- обязательно фиксировать результат через:
  - implementation_snapshot
  - decision_log

- запрещено полностью игнорировать planning layer

---

## Follow-ups

- разработать lightweight workflow (v2)
- интегрировать mindmap в систему
- упростить metadata/navigation
- рассмотреть semi-auto doc generation

---

## Notes

Это временное решение на этапе MVP.

Цель — не заменить docs-first, а снизить порог входа.