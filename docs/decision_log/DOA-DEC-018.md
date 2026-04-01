# Decision: DOA-DEC-018

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Cursor MCP подключён к другому состоянию/контексту Notion workspace

---

## Context

Обнаружено:

- страницы, созданные через MCP, отличаются от текущей структуры Notion
- при открытии ссылок видно старые страницы (до очистки)
- текущий UI Notion показывает другую структуру

---

## Problem

Cursor MCP работает не с текущим состоянием workspace, а с:

- другим workspace
или
- старым контекстом данных

---

## Chosen solution

Проверить и синхронизировать:

- workspace Notion
- MCP авторизацию
- источник данных (OAuth / integration)

---

## Rule

Если страницы из MCP ≠ страницы в UI:

→ это всегда проблема контекста (workspace / auth), а не page_id