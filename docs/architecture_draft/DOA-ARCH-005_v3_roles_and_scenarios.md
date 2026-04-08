# architecture_draft — DOA-ARCH-005

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-005
- Status: draft
- Date: 2026-04-08
- Parent: DOA-ARCH-003

---

## 2. Роли и сценарии (v3)

### 2.1 Роли
- **Primary User** — создаёт документы, ведёт planning, принимает решения, вручную соблюдает правила системы.
- **Reviewer (MVP)** — та же роль пользователя; выполняет проверку документов и меняет статусы при необходимости.
- **System** — набор правил и ограничений; в MVP не является активным компонентом, автоматическое enforcement отсутствует.

---

## 2.2 Ключевые сценарии

### S1: Создание проекта
**Input:** идея  
**Steps:**  
1. Создаётся `DOA-IDEA-XXX` (`idea_to_mvp`)  
2. Создаётся `DOA-MT-XXX` (`midterm_plan`)  
3. Выполняется Validation (см. раздел 3.7 модели документов и раздел 6 metadata model)  
**Output:** `DOA-IDEA-XXX`, `DOA-MT-XXX`

### S2: Формирование ТЗ
**Input:** `DOA-IDEA-XXX`  
**Steps:**  
1. Создаётся `DOA-ARCH-XXX` (`architecture_draft`)  
2. Выполняется Validation  
**Output:** `DOA-ARCH-XXX`

### S3: Планирование
**Input:** `DOA-ARCH-XXX` + optional `DOA-MT-XXX`  
**Steps:**  
1. Создаётся новая версия `DOA-OP-XXX` (`operational_plan`)  
2. В документ добавляются задачи и статусы  
3. Выполняется Validation  
**Output:** `DOA-OP-XXX`

### S4: Принятие решения
**Input:** изменение / альтернатива / конфликт  
**Steps:**  
1. Создаётся `DOA-DEC-XXX` (`decision_log`)  
2. При необходимости создаётся новая версия `DOA-OP-XXX`  
3. Если решение меняет архитектуру, создаётся новая версия `DOA-ARCH-XXX`  
4. Выполняется Validation  
**Output:** `DOA-DEC-XXX`, optional `DOA-OP-XXX`, optional `DOA-ARCH-XXX`

### S5: Выполнение задачи
**Input:** задача из `DOA-OP-XXX`  
**Steps:**  
1. Пользователь выполняет задачу  
2. Пользователь самостоятельно определяет, требуется ли новое `decision_log`  
3. Создаётся `DOA-IMP-XXX` (`implementation_snapshot`)  
4. Выполняется Validation  
**Output:** `DOA-IMP-XXX`, optional `DOA-DEC-XXX`

### S6: Audit
**Input:** набор ID документов проекта / текущее состояние проекта  
**Steps:**  
1. Проверяются metadata, naming, parent-link, traceability и согласованность doc_types  
2. Создаётся `DOA-AUD-XXX` (`audit_check`)  
3. Если обнаружены проблемы, создаётся `DOA-DEC-XXX` и новая версия `DOA-OP-XXX`  
**Trigger:** после завершения `operational_plan`, перед переходом `midterm -> implementation`, или при рассинхроне  
**Output:** `DOA-AUD-XXX`, optional `DOA-DEC-XXX`, optional `DOA-OP-XXX`

---

## 2.3 Ограничения
- Запрещена работа вне `operational_plan`
- Значимые решения фиксируются только через `decision_log`
- Действует create-only: update/перезапись документов запрещены
- Каждый новый документ проходит Validation

---

## 2.4 Flow (уточнённый)
`idea_to_mvp` → `architecture_draft` → `midterm_plan` → `operational_plan` → execution → `implementation_snapshot` → `audit_check` → next `operational_plan`

При значимом отклонении:
`decision_log` → новая версия `operational_plan`  
При архитектурном изменении:
`decision_log` → новая версия `architecture_draft`
