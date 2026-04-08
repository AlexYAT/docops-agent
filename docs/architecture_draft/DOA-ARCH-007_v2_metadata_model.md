# architecture_draft — DOA-ARCH-007

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-007
- Status: draft
- Date: 2026-04-08
- Parent: DOA-ARCH-003

---

## 6. Metadata model

## 6.0 Summary
Metadata model задаёт единый формат описания документов в DocOps Agent.
Она нужна для идентификации, валидации, traceability и безопасного create-only процесса.

---

## 6.1 Цель metadata model
Metadata model должна:
- однозначно идентифицировать документ
- определять его тип и статус
- связывать документ с проектом
- поддерживать parent/child связи
- быть пригодной для ручной работы и будущей автоматизации

---

## 6.2 Принципы metadata
- metadata обязательна для всех документов
- используется единый минимальный набор полей
- формат должен быть читаем человеком
- формат должен быть пригоден для автоматизации
- metadata должна поддерживать create-only

---

## 6.3 Обязательные поля metadata

### project
**Тип:** string  
**Пример:** `DOA`

### doc_type
**Тип:** enum/string  
**Допустимые значения:**  
`idea_to_mvp`, `architecture_draft`, `decision_log`, `implementation_snapshot`, `audit_check`, `longterm_plan`, `midterm_plan`, `operational_plan`

### id
**Тип:** string  
**Пример:** `DOA-DEC-003`

### status
**Тип:** enum  
**Допустимые значения:** `draft`, `review`, `accepted`, `obsolete`

**Примечание:**  
Статус `review` рекомендуется, но не обязателен в MVP.

### date
**Тип:** date  
**Формат:** `YYYY-MM-DD`  
**Convention:** timezone = UTC by convention

### parent
**Тип:** string / null  
**Пример:** `DOA-ARCH-003` или `null`

**Правило:**  
Поле `parent` обязательно должно присутствовать в metadata, но может иметь значение `null`.

---

## 6.4 Расширенные поля metadata (optional)

### version
**Тип:** string  
**Пример:** `v1.0`

### replaces
**Тип:** string / null  
**Пример:** `DOA-OP-017`

**Правило:**  
`replaces` допустим только для документов того же `doc_type`.

### tags
**Тип:** list[string]  
**Пример:** `["mvp", "planning"]`

---

## 6.5 Формат metadata в документе

Для MVP используется markdown-блок в начале документа:

```markdown
## Metadata
- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-003
- Status: accepted
- Date: 2026-04-08
- Parent: DOA-ARCH-003
```

Плохой пример metadata:
- отсутствует `ID`
- `Status: done`
- `Parent` ссылается на несуществующий документ
- `Doc type` не входит в утверждённый набор

**Примечание:**  
В текущей версии выбран markdown-формат для простоты ручной работы.
В будущем он может быть заменён на YAML без изменения смысла полей.

---

## 6.6 Правила валидации metadata

### Validation 1 — Required fields check
Документ содержит все обязательные поля:
- `project`
- `doc_type`
- `id`
- `status`
- `date`
- `parent`

### Validation 2 — Type correctness
Поля соответствуют ожидаемым типам.

### Validation 3 — ID uniqueness
`id` не повторяется в рамках проекта.

**MVP note:**  
На этапе MVP уникальность ID обеспечивается пользователем вручную через naming convention и сквозную нумерацию.

### Validation 4 — Naming compliance
`id` соответствует naming convention проекта.

### Validation 5 — Parent validity
Если указан `parent`, он:
- существует или равен `null`
- допустим для данного `doc_type`
- не создаёт циклическую ссылку
- соответствует правилам раздела 6.7

### Validation 6 — Status consistency
Статус не противоречит роли документа в системе.

### Validation 7 — Parent status consistency
Документ со статусом `accepted` не должен ссылаться на `obsolete` parent,
если явно не указан `replaces`.

---

## 6.7 Разрешённые parent-связи (MVP rules)
- `architecture_draft` → parent = `idea_to_mvp` или `null`
- `midterm_plan` → parent = `idea_to_mvp`, `longterm_plan` или `null`
- `operational_plan` → parent = `midterm_plan`, `architecture_draft` или `null`
- `implementation_snapshot` → parent = `operational_plan` или `null`
- `audit_check` → parent = `implementation_snapshot`, `operational_plan` или `null`
- `decision_log` → parent = любой релевантный документ или `null`

Недопустимо:
- `operational_plan` → parent = `implementation_snapshot`
- `idea_to_mvp` → parent = `audit_check`
- self-reference и циклические parent-ссылки

---

## 6.8 Metadata и create-only
- новый документ получает новый `id`
- старый документ не удаляется
- при логической замене может использоваться `replaces`
- активность документа определяется через `status`

Пример:
- старый plan: `DOA-OP-017`, `status = obsolete`
- новый plan: `DOA-OP-018`, `status = accepted`, `replaces = DOA-OP-017`

---

## 6.9 Запрещённые практики
- документы без metadata
- пропуск обязательных полей
- произвольные названия полей
- дублирование `id`
- неутверждённые значения `status`
- `replaces` между разными doc_types
- изменение `id` задним числом

---

## 6.10 Definition of Done for metadata model
Раздел завершён, если:
- определён обязательный набор полей
- определены optional-поля
- зафиксирован формат metadata-блока
- зафиксированы правила валидации
- определены parent-связи
- metadata согласована с create-only и traceability

---

## 6.11 Итог
Metadata model — базовый слой DocOps Agent.
Она делает возможными валидацию, traceability, planning и безопасную работу в create-only режиме.
