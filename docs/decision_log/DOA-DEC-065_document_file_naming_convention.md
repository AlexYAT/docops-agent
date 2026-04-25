# DocOps Agent — decision_log

## Metadata
Project: docops-agent
Doc type: decision_log
ID: DOA-DEC-065
Date: 2026-04-25
Parent: DOA-OP-038
Status: accepted

---

## Title
Use ID-first lowercase slug file naming

---

## Context

После фиксации правил doc_type → folder и генерации ID необходимо
зафиксировать единый формат имени файла.

Без единого naming convention документы могут иметь корректный ID,
но оставаться непредсказуемыми для навигации и поиска.

---

## Options considered

### Option 1 — ID-first lowercase slug
Формат:

DOA-TYPE-NNN_short_lowercase_slug.md

### Option 2 — Title-first naming
Формат:

short_lowercase_slug_DOA-TYPE-NNN.md

### Option 3 — ID-only naming
Формат:

DOA-TYPE-NNN.md

---

## Decision

Использовать Option 1:

DOA-TYPE-NNN_short_lowercase_slug.md

---

## Why

- ID остаётся главным ключом документа
- файлы удобно сортируются
- slug помогает понять содержание без открытия файла
- формат совместим с текущей практикой репозитория

---

## Rule

Имя файла должно строиться так:

<ID>_<short_lowercase_slug>.md

Пример:

DOA-DEC-064_id_generation_strategy.md

---

## Consequences

- ID всегда стоит первым
- slug пишется в lowercase
- слова slug разделяются underscore
- имя файла не должно задаваться вручную без проверки ID
- Cursor должен формировать имя после определения ID

---

## Non-goals

- не переименовывать существующие документы
- не вводить aliases
- не использовать title-first формат
- не использовать ID-only формат

---

## Follow-up

Следующий шаг по DOA-OP-038:

T04 — Define creation workflow
