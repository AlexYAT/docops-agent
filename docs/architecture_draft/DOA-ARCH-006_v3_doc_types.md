# architecture_draft — DOA-ARCH-006

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-006
- Status: draft
- Date: 2026-04-08
- Parent: DOA-ARCH-003

---

## 3. Модель документов (v3)

## 3.0 Summary
Раздел фиксирует doc_types как единственный допустимый набор документов для MVP.
Каждый документ выполняет одну функцию, поддерживает traceability и подчиняется create-only.

---

## 3.1 Ключевые уточнения

### architecture_draft
- active version = single source of architecture truth
- если `decision_log` меняет архитектуру:
  - создаётся новый `architecture_draft`
  - предыдущая версия переводится в `obsolete` или сохраняется как исторически `accepted` по принятой политике версий

### operational_plan
- только create-only
- новая версия создаётся с новым ID
- запрещено редактирование существующего плана

### audit_check
- обязателен перед переходом `midterm -> implementation`
- если найдены проблемы:
  - создаётся `decision_log`
  - создаётся новая версия `operational_plan`

---

## 3.2 Классификация
**Обязательные:** `idea_to_mvp`, `architecture_draft`, `decision_log`, `implementation_snapshot`, `midterm_plan`, `operational_plan`  
**Условно-обязательные:** `audit_check`  
**Опциональные:** `longterm_plan`  
Если `longterm_plan` существует, он становится parent-контуром для `midterm_plan`.

---

## 3.3 Правила doc_types
- каждый документ должен принадлежать утверждённому doc_type
- один doc_type = одна функция
- запрещено смешивать роли разных doc_types в одном документе
- все новые документы проходят Validation
- все изменения реализуются через новые документы, а не update существующих

---

## 3.4 Запрещено
- update/перезапись документов
- редактирование существующего `operational_plan`
- параллельные active-версии `architecture_draft` без явной политики версий
- использование `implementation_snapshot` вместо `decision_log`
- создание документов вне утверждённого набора doc_types

---

## 3.5 Валидация
Проверяется:
- `type`
- `purpose`
- `metadata`
- `naming`
- `link`
- согласованность со status и create-only

`parent` допустим только из разрешённых типов для данного doc_type.

---

## 3.6 Flow (уточнённый)
`idea_to_mvp` → `architecture_draft` → `midterm_plan` → `operational_plan` → `implementation_snapshot` → `audit_check`

При отклонениях:
`decision_log` → новая версия `operational_plan`

При архитектурных изменениях:
`decision_log` → новая версия `architecture_draft`

---

## 3.7 Связи (сводка)
- `decision_log` → может изменить `architecture_draft` (новая версия)
- `decision_log` → влияет на `operational_plan`
- `implementation_snapshot` → ссылается на задачу из `operational_plan`
- `audit_check` → инициирует `decision_log` и/или перепланирование

---

## 3.8 Итог
Doc_types образуют жёсткий каркас системы.
Любая работа в DocOps Agent должна выполняться только через этот набор документов.
