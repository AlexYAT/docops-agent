# architecture_draft — DOA-ARCH-008

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-008
- Status: draft
- Date: 2026-04-08
- Parent: DOA-ARCH-003

---

## 7. Naming Convention

## 7.0 Summary
Раздел фиксирует единый стандарт формирования ID документов.
Naming обеспечивает уникальность, читаемость и связность системы DocOps Agent.

---

## 7.1 Цель naming
Naming должен:
- обеспечивать уникальные ID
- однозначно отражать тип документа
- быть читаемым человеком
- быть пригодным для автоматизации
- поддерживать create-only

---

## 7.2 Canonical формат ID

```
<PROJECT>-<TYPE>-<NNN>
```

### Где:
- `<PROJECT>` — код проекта (например: DOA)
- `<TYPE>` — префикс типа документа
- `<NNN>` — порядковый номер (3 цифры, с ведущими нулями)

---

## 7.3 Mapping doc_type → TYPE

| doc_type                 | TYPE |
|--------------------------|------|
| idea_to_mvp              | IDEA |
| architecture_draft       | ARCH |
| decision_log             | DEC  |
| implementation_snapshot  | IMP  |
| audit_check              | AUD  |
| longterm_plan            | LT   |
| midterm_plan             | MT   |
| operational_plan         | OP   |

---

## 7.4 Примеры

- DOA-IDEA-001
- DOA-ARCH-003
- DOA-DEC-010
- DOA-OP-017
- DOA-IMP-005

---

## 7.5 Правила нумерации

- нумерация ведётся отдельно для каждого TYPE
- используется сквозная последовательность: 001 → 002 → 003
- пропуски нежелательны, но допустимы
- повторное использование номеров запрещено
- в MVP нумерация ведётся вручную пользователем

---

## 7.6 Правила валидации naming

### Validation 1 — Format check
ID соответствует формату:
```
<PROJECT>-<TYPE>-<NNN>
```

### Validation 2 — TYPE consistency
TYPE соответствует doc_type документа.

Пример:
- `DOA-DEC-003` → doc_type = decision_log
- `DOA-OP-017` → doc_type = operational_plan

### Validation 3 — ID uniqueness
ID уникален в рамках проекта.

### Validation 4 — Numeric format
- `<NNN>` состоит ровно из 3 цифр
- используется формат с ведущими нулями

---

## 7.7 Связь с metadata

Поле `id` в metadata:
- полностью соответствует naming convention
- является primary key документа
- используется во всех ссылках (`parent`, `replaces`)

---

## 7.8 Связь с create-only

Naming поддерживает create-only:

- каждый новый документ получает новый уникальный ID
- существующие ID не изменяются
- замена документа осуществляется через новый ID + `replaces`

Пример:
- старый: DOA-OP-017
- новый: DOA-OP-018 (replaces = DOA-OP-017)

---

## 7.9 Запрещённые практики

Запрещено:
- использовать произвольный формат ID
- изменять ID существующего документа
- использовать один ID для нескольких документов
- нарушать соответствие TYPE ↔ doc_type
- использовать нечисловые значения в `<NNN>`

---

## 7.10 Definition of Done for naming

Раздел считается завершённым, если:
- определён единый формат ID
- определён mapping TYPE ↔ doc_type
- зафиксированы правила нумерации
- зафиксированы правила валидации
- naming согласован с metadata и create-only

---

## 7.11 Итог

Naming convention задаёт единый стандарт идентификации документов.
Он является основой для:
- metadata
- traceability
- валидации
- связей между документами

Без него система DocOps Agent не может быть консистентной.
