# DOA-OP-034 — Snapshot creation protocol

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-034
- Status: draft
- Date: 2026-04-17
- Parent: DOA-DEC-053

---

## Summary

Операционный план, описывающий процедуру создания нового fixed snapshot.

Цель:
перевести lifecycle snapshot в исполняемую процедуру.

---

## Goal

Определить пошаговый процесс:

- проверки readiness системы
- фиксации snapshot
- перехода к новой эпохе

---

## Scope

Входит:
- критерии запуска snapshot
- последовательность действий
- фиксация snapshot-документа
- активация новой эпохи

Не входит:
- изменение validator/gate логики
- автоматизация процесса

---

## Tasks

### T01 — Проверка readiness

Done when:
- проверен gate_status_controlled
- отсутствуют критические validator ошибки
- система стабильна

---

### T02 — Подготовка snapshot

Done when:
- определён scope controlled зоны
- зафиксированы ключевые документы эпохи

---

### T03 — Создание snapshot-документа

Done when:
- создан новый DOA-FSN-XXX
- snapshot фиксирует состояние системы

---

### T04 — Валидация snapshot

Done when:
- snapshot проходит validator
- snapshot корректно ссылается на controlled документы

---

### T05 — Активация новой эпохи

Done when:
- snapshot становится новой boundary
- начинается новая controlled зона

---

### T06 — Создание implementation_snapshot

Done when:
- зафиксирован переход в новую эпоху

---

## Dependencies

- DOA-DEC-053
- текущий snapshot
- controlled зона

---

## Risks

- создание snapshot при нестабильной системе
- неправильное определение scope
- нарушение ссылочной дисциплины

---

## Expected Result

Система получает:

- воспроизводимый процесс создания snapshot
- управляемый переход между эпохами
- снижение хаоса изменений

---

## Follow-up

- автоматизация snapshot процесса (в будущем)
- интеграция с validator/gate
