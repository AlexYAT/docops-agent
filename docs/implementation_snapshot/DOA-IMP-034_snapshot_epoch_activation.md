# DOA-IMP-034 — Snapshot epoch activation

## Metadata

- Project: docops-agent
- Doc type: implementation_snapshot
- ID: DOA-IMP-034
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-OP-033

---

## Summary

Зафиксировано состояние системы после перехода к snapshot-driven development.

Данный snapshot отражает первую operational epoch,
в которой controlled zone становится основным рабочим контуром.

---

## System State

Система находится в состоянии:

- fixed snapshot boundary активен
- введено разделение:
  - legacy zone
  - controlled zone
- controlled zone используется как primary operational truth

---

## Gate Status

- historical gate_status: REJECT
- operational gate_status_controlled: ACCEPT

Вывод:

👉 система операционно пригодна к работе внутри controlled зоны

---

## Operational Model

Активная модель работы:

- работа ведётся только от snapshot
- новые документы создаются после snapshot
- legacy не участвует напрямую в разработке
- snapshot выступает как boundary artifact

---

## Epoch Definition

Текущая эпоха определяется как:

- snapshot: DOA-FSN-001
- scope: все документы после snapshot
- режим: controlled-only development

---

## Key Properties

- create-only сохраняется
- traceability сохраняется
- gate semantics разделены:
  - historical
  - operational

---

## Risks

- возможное смешение legacy и controlled ссылок
- неправильное использование snapshot как обычного документа
- отсутствие дисциплины epoch boundaries

---

## Outcome

Система перешла от:

👉 document-driven

к:

👉 snapshot-driven epoch system

---

## Follow-up

Следующий шаг:

- подготовка критериев следующего snapshot
- накопление изменений внутри controlled зоны
- запуск следующего snapshot цикла
