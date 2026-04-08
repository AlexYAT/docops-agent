# DOA-DEC-027 — TZ import conflict resolution

## Metadata

- Project: DOA
- Type: decision_log
- ID: DOA-DEC-027
- Status: approved
- Date: 2026-04-08

---

## Context

В рамках DOA-OP-003 выполнен анализ staging-каталога TZ (23 файла).

Выявлены проблемные случаи:

- конфликт ID с уже существующими документами в Project/docs
- нарушение naming convention
- неоднозначность канонической версии

Следующие файлы требуют решения:

1. DOA-DEC-004_TZ_structure_fixed.md
2. DOA-IMP-008_project_snapshot_2026-04-08.md
3. DOA-OP-TZ-001_full_TZ_plan.md

---

## Decision

### 1. DEC-004 (ID collision)

**Файл:**  
DOA-DEC-004_TZ_structure_fixed.md

**Проблема:**

- В Project уже существует DOA-DEC-004.md
- Дублирование ID недопустимо

**Решение:**

- Не импортировать файл как DEC-004
- Считать TZ-версию legacy-артефактом
- НЕ выполнять автоматическую перенумерацию

**Причина:**

- Decision_log должен быть стабильным и неизменяемым
- Перенумерация может нарушить ссылки и историю

---

### 2. IMP-008 (snapshot conflict + naming mismatch)

**Файл:**  
DOA-IMP-008_project_snapshot_2026-04-08.md

**Проблема:**

- В Project уже есть DOA-IMP-008.md
- Имя файла содержит дату → нарушение naming convention

**Решение:**

- Не импортировать как canonical snapshot
- Считать TZ-версию временным staging snapshot
- НЕ переносить в docs/implementation_snapshot/

**Причина:**

- Snapshot должен иметь строгий ID без даты
- В проекте уже есть canonical версия

---

### 3. OP-TZ-001 (invalid ID)

**Файл:**  
DOA-OP-TZ-001_full_TZ_plan.md

**Проблема:**

- Нарушение naming convention (ожидается DOA-OP-<NNN>)
- Нестандартный формат ID

**Решение:**

- Не импортировать в docs/operational_plan/
- Считать invalid артефактом
- Допускается ручная переработка в будущем (с новым ID)

**Причина:**

- Нарушение naming ломает систему навигации
- Автоматическое исправление недопустимо

---

## Consequences

- Импорт выполняется только для canonical файлов без конфликтов
- Conflict/invalid файлы остаются в TZ
- Система сохраняет консистентность ID и структуры

---

## Next steps

- Выполнить DOA-OP-003-T03:
  → перемещение только canonical файлов
  → без conflict/invalid
