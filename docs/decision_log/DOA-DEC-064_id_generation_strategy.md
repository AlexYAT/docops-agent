# DocOps Agent — decision_log

## Metadata
Project: docops-agent
Doc type: decision_log
ID: DOA-DEC-064
Date: 2026-04-25
Parent: DOA-OP-038
Status: accepted

---

## Title
Use repository scan for ID generation

---

## Context

В текущем процессе ID документов задаются вручную,
что приводит к конфликтам и несоответствиям.

Необходим детерминированный способ генерации ID.

---

## Options considered

### Option 1 — Scan repository
Определять следующий ID на основе анализа существующих файлов в репозитории.

### Option 2 — Registry file
Хранить последний ID в отдельном файле.

### Option 3 — External storage
Использовать внешний источник (БД, сервис).

---

## Decision

Использовать Option 1:

генерация ID выполняется через сканирование репозитория
и определение следующего доступного значения.

---

## Why

- не требует дополнительного состояния
- соответствует create-only модели
- работает в текущем workflow (Cursor имеет доступ к файлам)
- минимальная сложность

---

## Consequences

- Cursor должен анализировать существующие ID
- ID всегда определяется автоматически
- ручное задание ID запрещено
- исключаются конфликты при правильной работе

---

## Non-goals

- не вводить registry
- не использовать внешние сервисы
- не менять существующие ID

---

## Follow-up

Следующий шаг по DOA-OP-038:

T03 — Define naming convention
