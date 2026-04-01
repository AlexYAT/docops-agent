# Decision: DOA-DEC-015

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Для MCP Notion необходимо включить Insert/Update capabilities

---

## Context

Интеграция Notion создана (Cursor AI), но включена только:

- Read content

При попытке создать страницу возникает ошибка 404 / object_not_found

---

## Problem

Без прав:

- Insert content
- Update content

Notion API не позволяет создавать страницы

---

## Chosen Solution

Включить:

- Insert content
- Update content

в настройках integration

---

## Rule

Любая MCP интеграция должна иметь минимум:

- Read content
- Insert content
- Update content