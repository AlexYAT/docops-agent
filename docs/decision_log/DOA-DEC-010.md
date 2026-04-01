# Decision: DOA-DEC-010

## Project
DocOps Agent (DOA)

## Date
2026-03-31

## Status
accepted

---

## Title
Использовать Cursor Rules как системный слой для auto-doc

---

## Context

Для работы auto-doc generation требуется постоянный контекст:

- определение типа документа
- шаблоны
- правила MCP

Cursor поддерживает механизм Rules (.cursor/rules)

---

## Problem

Без системного prompt:

- каждый раз нужно вручную писать инструкции
- auto-doc не работает стабильно

---

## Chosen Solution

Использовать Cursor Rules как системный слой:

→ один раз задать правила  
→ использовать во всех запросах  

---

## Why

- постоянный контекст
- упрощение работы
- устойчивость системы

---

## Trade-offs

- требуется первоначальная настройка

---

## Rule

Все auto-doc инструкции должны быть заданы через Cursor Rules