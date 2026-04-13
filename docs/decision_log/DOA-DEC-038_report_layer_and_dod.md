# Decision: DOA-DEC-038

## Metadata

- Project: DocOps Agent
- Doc type: decision_log
- ID: DOA-DEC-038
- Status: accepted
- Date: 2026-04-13
- Parent: DOA-ARCH-016

---

## Title

Введение Report Layer и нового Definition of Done

## Context

В системе DocOps Agent отсутствовал слой представления, понятный человеку.

implementation_snapshot не решает задачу:

- дублирует данные
- устаревает
- конфликтует с create-only

## Decision

Ввести Report Layer как отдельный слой системы:

- отчет не является документом
- отчет не хранится
- отчет формируется динамически

## Definition of Done

DoD считается выполненным, если:

1. Система проходит validator / gate
2. На основе документов можно сгенерировать понятный человеку отчет

## Why

- устраняет дублирование
- сохраняет create-only
- делает систему понятной извне

## Trade-offs

- требуется реализация генерации отчета
- повышаются требования к структуре документов

## Follow-ups

- реализовать MVP генератора отчета (CLI)
- интегрировать с Document Gate
- определить формат отчета
