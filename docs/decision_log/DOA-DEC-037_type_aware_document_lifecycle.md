# Decision: DOA-DEC-037

## Metadata

- Project: DocOps Agent
- Doc type: decision_log
- ID: DOA-DEC-037
- Status: accepted
- Date: 2026-04-13
- Parent: DOA-ARCH-015

---

## Title

Введение type-aware жизненного цикла документов

## Context

В системе DocOps Agent использовался неявный глобальный enum статусов документов.

Это привело к конфликту:

- статус "planned" корректен для planning-документов
- validator интерпретирует его как ошибку

Проблема возникла из-за отсутствия модели жизненного цикла, учитывающей тип документа.

## Decision

Ввести type-aware модель жизненного цикла:

- каждый doc_type имеет свой набор допустимых статусов
- глобальный enum статусов запрещён
- validator в будущем должен учитывать doc_type

## Lifecycle Model (кратко)

### Planning документы

- draft
- planned
- active
- superseded

### Implementation snapshot

- draft
- recorded
- accepted

### Decision log

- draft
- accepted
- rejected
- superseded

### Architecture документы

- draft
- accepted
- superseded

## Why

- устраняет системный конфликт validator vs документы
- делает модель статусов логичной и расширяемой
- соответствует docs-first и create-only подходу

## Trade-offs

- требуется усложнение validator (type-aware логика)
- временно возможна несогласованность системы

## Follow-ups

- обновить validator под type-aware модель
- обновить Document Gate
- определить source of truth для naming (AUD vs AUDIT)
