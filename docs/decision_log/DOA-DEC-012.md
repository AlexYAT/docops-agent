# Decision: DOA-DEC-012

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
При недоступности Notion MCP сохранять документ локально как временный fallback

---

## Context

При тесте auto-doc generation Cursor корректно определил тип документа и создал implementation_snapshot локально, но инструменты Notion MCP в текущей сессии были недоступны.

---

## Problem

End-to-end pipeline Cursor → MCP → Notion не всегда доступен в конкретной сессии.

---

## Chosen Solution

Если MCP недоступен, документ создаётся локально в проекте как временный fallback-артефакт.

---

## Why

- не теряется результат работы
- сохраняется create-only подход
- можно позже перенести документ в Notion

---

## Trade-offs

- временно нарушается единый storage
- история распределяется между локальными файлами и Notion

---

## Rules

Если MCP недоступен:
1. создать документ локально
2. не редактировать вручную после создания
3. позже отправить тот же документ в Notion отдельным шагом