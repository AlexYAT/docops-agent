## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-011
- Status: draft
- Date: 2026-04-08
- Parent: DOA-IDEA-001

---

## Summary

Архитектурный чертёж **DocOps Agent (MVP)**: markdown-only репозиторий документов с doc_types, metadata, naming и workflow на одного пользователя; **create-only** как инвариант.

## Goal

Зафиксировать договорённости, достаточные для **ручного** ведения DocOps без автоматической оркестрации.

## Scope

- Репозиторий проекта: корень + `docs/<doc_type>/` + `templates/<doc_type>/`
- Все новые содержательные изменения — **новые файлы** (новые ID); исторические файлы не переписываются ради «чистоты»
- Внешние публикации (например Notion через MCP) не являются источником правды для Git

## Roles & Scenarios

- **Роль**: владелец документации / разработчик (один субъект на bootstrap)
- **Сценарии**: завести идею → зафиксировать архитектурный черновик → планировать (LT/MT/OP) → принять решения (DEC) → снять снапшот (IMP) → аудит (AUD)

## Document Model

- Один файл = один логический артефакт с уникальным **ID**
- Каждый файл начинается с блока **Metadata** (Project, Doc type, ID, Status, Date, Parent)
- Тип артефакта = **doc_type** и соответствующая папка в `docs/`

## Metadata Model

Обязательные поля в начале документа: **Project**, **Doc type**, **ID**, **Status**, **Date**, **Parent** (ID родителя или `null`).

## Naming Convention

`<PROJECT>-<TYPE>-<NNN>`  
Типы: `IDEA`, `ARCH`, `DEC`, `IMP`, `AUD`, `LT`, `MT`, `OP`.

## System Rules

- **create-only** для содержательной эволюции утверждённых артефактов
- **planning-first**: работа вне `operational_plan` только до первого accepted OP (см. `WORKFLOW.md`)
- **explicit decisions** в `decision_log`

## Workflow

Цепочка документов (логическая):  
`idea_to_mvp` → `architecture_draft` → … → `operational_plan` → `decision_log` / `implementation_snapshot` → `audit_check`  
(детали порядка см. `WORKFLOW.md`.)

## Constraints

- Без схемы БД для документов на уровне MVP
- Без обязательного механизма миграции legacy-файлов в «правильные» папки в одном шаге

## Definition of Done

Система пригодна для **ручного** использования: можно создать согласованный набор документов по шаблонам, выставить Parent, пройти аудит чеклистом без противоречий в ID и типах.
