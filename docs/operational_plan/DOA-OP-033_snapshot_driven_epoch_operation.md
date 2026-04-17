# DOA-OP-033 — Snapshot-driven epoch operation

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-033
- Status: draft
- Date: 2026-04-17
- Parent: DOA-DEC-052

---

## Summary

Операционный план для работы в режиме fixed snapshot boundary.

Цель плана:
- формализовать практическую работу от фиксированного snapshot
- ограничить активную разработку controlled zone
- зафиксировать правила создания новых эпох
- сделать snapshot-driven development стандартным режимом работы системы

---

## Goal

Перевести DocOps Agent в устойчивый режим работы, где:

- активный контур разработки = fixed snapshot + controlled документы после него
- legacy рассматривается как исторический слой
- новые изменения оформляются только как новые документы после snapshot
- переход к следующей эпохе выполняется через новый fixed snapshot

---

## Scope

Входит:
- правила операционной работы от snapshot
- правила допустимых ссылок в controlled zone
- правила фиксации новых документов после snapshot
- правила подготовки следующего snapshot
- правила использования gate_status_controlled как primary operational signal

Не входит:
- переработка legacy документов
- массовая миграция исторического слоя
- изменение уже принятых snapshot-артефактов
- сложная автоматизация epoch lifecycle

---

## Tasks

### T01 — Зафиксировать рабочую модель epoch

Done when:
- описано, что active scope = snapshot + post-snapshot controlled docs
- явно указано, что legacy не используется как источник для новых прямых решений, кроме разрешённых мостов

### T02 — Зафиксировать правила ссылочной дисциплины

Done when:
- описаны допустимые направления ссылок для controlled документов
- отдельно зафиксировано, что snapshot является boundary artifact

### T03 — Зафиксировать operational semantics gate

Done when:
- указано, что `gate_status_controlled` используется как primary operational indicator
- указано, что исторический `gate_status` сохраняется как secondary/historical indicator

### T04 — Описать правило работы над изменениями внутри эпохи

Done when:
- зафиксировано, что новые изменения оформляются только новыми документами
- зафиксировано, что accepted snapshot не редактируется

### T05 — Описать критерии создания следующего fixed snapshot

Done when:
- перечислены условия, при которых controlled zone можно фиксировать в новый snapshot
- указано, что следующий snapshot открывает новую operational epoch

### T06 — Подготовить implementation snapshot после выполнения плана

Done when:
- явно указано, что результат выполнения данного operational_plan должен быть зафиксирован отдельным implementation_snapshot

---

## Dependencies

- DOA-DEC-052
- текущий fixed snapshot boundary
- действующая controlled zone
- актуальные validator/gate semantics

---

## Risks

- смешение historical и operational semantics
- частичное возвращение legacy в активный контур
- неоднозначность правил для новых ссылок после snapshot
- premature automation до стабилизации процесса эпох

---

## Expected Result

После выполнения плана система работает в явной модели:

- snapshot = граница эпохи
- controlled zone = рабочий контур
- новые документы создаются только внутри текущей эпохи
- следующая эпоха открывается только через новый fixed snapshot

---

## Follow-up

После выполнения плана создать новый implementation_snapshot, который фиксирует:
- принятый operational workflow эпохи
- статус controlled zone
- готовность системы к следующему snapshot cycle
