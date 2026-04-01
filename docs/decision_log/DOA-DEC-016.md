# Decision: DOA-DEC-016

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Notion MCP требует явного доступа integration к странице (Share → Invite)

---

## Context

Интеграция настроена и имеет права:

- Read
- Insert
- Update

Но MCP возвращает 404 object_not_found

---

## Problem

Notion API НЕ имеет доступа к страницам по умолчанию.

Даже при наличии прав integration не "видит" страницы без явного подключения.

---

## Chosen solution

Каждую родительскую страницу нужно вручную:

Share → Invite → выбрать integration

---

## Rule

Integration в Notion:

НЕ имеет доступа ко всему workspace  
ТОЛЬКО к тем страницам, куда её пригласили