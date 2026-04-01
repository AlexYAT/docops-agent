# Decision: DOA-DEC-006

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Полный reset Notion workspace перед запуском DOA

---

## Context

Текущее пространство Notion содержит:

- стандартные шаблоны (Home, Work, To Do List)
- обучающие страницы
- структуры, не связанные с DOA

Данные не представляют ценности.

---

## Problem

- шум в структуре
- мешает построению минимальной системы
- усложняет навигацию

---

## Chosen Solution

Полностью очистить Notion workspace и создать новую структуру:

- Inbox
- Decisions
- Snapshots
- Plans

---

## Why

- чистая точка старта
- упрощение структуры
- соответствие Notion v1 architecture

---

## Trade-offs

- потеря стандартных шаблонов Notion (не критично)

---

## Constraints

- не создавать сложные базы данных
- не использовать встроенные шаблоны

---

## Notes

Workspace рассматривается как пустой storage под DOA.