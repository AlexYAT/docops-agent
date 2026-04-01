# Decision: DOA-DEC-008

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Зафиксировать Cursor → MCP → Notion как основной workflow MVP

---

## Context

После тестирования pipeline:

ChatGPT → Cursor → MCP → Notion

документы успешно создаются и сохраняются.

---

## Chosen solution

Использовать данный pipeline как основной способ работы
с документацией на этапе MVP.

---

## Why

- работает стабильно
- соответствует реальному процессу разработки
- снижает ручной ввод
- легко масштабируется

---

## Trade-offs

- зависимость от MCP
- необходимость контроля структуры

---

## Rule

Все документы создаются через:

→ Cursor → MCP → Notion