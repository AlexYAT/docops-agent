# DOA-IDEA-007 — Enforcement of Document Creation Invariants

## Metadata

Project: docops-agent  
Doc type: idea_to_mvp  
ID: DOA-IDEA-007  
Status: draft  
Date: 2026-04-25  
Parent: DOA-IMP-037  

---

## Summary

В системе DocOps Agent правила создания документов определены и стабилизированы,
но отсутствует механизм их принудительной проверки (enforcement).

Это приводит к зависимости от дисциплины пользователя и риску нарушения инвариантов.

Данная IDEA инициирует внедрение минимального enforcement-слоя
для проверки корректности создания документов.

---

## Problem

Текущее состояние системы:

- правила существуют:
  - doc_type → folder
  - ID generation
  - naming convention
  - creation workflow

- но:

❗ отсутствует enforcement

Следствия:

- правила могут нарушаться
- ошибки не детектируются автоматически
- система не является self-validating

---

## Goal

Создать минимальный enforcement-слой,
который позволяет:

- автоматически проверять соблюдение инвариантов создания документов
- детектировать нарушения
- повысить надежность системы

---

## Scope

### In scope

- проверка соответствия doc_type и папки
- проверка формата ID
- проверка naming convention
- проверка базового creation workflow

- detection-only (без изменения документов)

---

### Out of scope

- автоматическое исправление документов
- изменение существующих документов
- интеграция с внешними системами
- полный enforcement всей системы DocOps
- усложнение архитектуры

---

## Constraints

- MVP simplicity
- create-only must be preserved
- no breaking changes
- минимальная сложность реализации

---

## Expected Outcome

- система становится self-validating
- нарушения обнаруживаются автоматически
- снижается человеческий фактор
- повышается надежность DocOps системы

---

## Notes

- enforcement должен быть инкрементальным
- validator является потенциальной точкой входа
- возможное расширение через Document Gate на следующих этапах
