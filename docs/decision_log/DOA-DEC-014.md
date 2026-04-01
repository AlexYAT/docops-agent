# Decision: DOA-DEC-014

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
MCP требует доступа через Notion Integration, а не обычный Share

---

## Context

При настройке доступа к странице пользователь использовал стандартный Share:

- email
- public link

Но MCP продолжает возвращать 404

---

## Problem

Notion API не использует обычный Share-доступ.

Требуется:

→ доступ через Integration

---

## Chosen Solution

Подключить интеграцию Notion к странице:

→ Share → Invite → выбрать Integration

---

## Rule

Для MCP:

❌ недостаточно "Anyone with link"  
✅ нужно "Integration access"