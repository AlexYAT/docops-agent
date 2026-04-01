# Decision: DOA-DEC-013

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Для работы MCP Notion требуется явный доступ к странице (Share integration)

---

## Context

При попытке создать страницу через MCP возникла ошибка:

404 object_not_found для parent_page_id

При этом:
- page_id корректный
- страница существует в Notion

---

## Problem

MCP Notion не имеет доступа к странице, если:

- страница не расшарена на интеграцию
- или открыта не тем аккаунтом

---

## Chosen Solution

Перед использованием MCP:

→ вручную дать доступ интеграции Notion к нужным страницам

---

## Why

- Notion API требует явного доступа
- иначе любые операции возвращают 404

---

## Rule

Любая страница, используемая через MCP, должна быть:

→ Share → подключена к интеграции Cursor / MCP